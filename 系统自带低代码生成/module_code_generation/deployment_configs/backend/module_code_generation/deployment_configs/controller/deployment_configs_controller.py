from fastapi import APIRouter, Depends, Form, Request
from pydantic_validation_decorator import ValidateFields
from sqlalchemy.ext.asyncio import AsyncSession
from config.enums import BusinessType
from config.get_db import get_db
from module_admin.annotation.log_annotation import Log
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_admin.service.login_service import LoginService
from module_code_generation.deployment_configs.service.deployment_configs_service import Deployment_configsService
from module_code_generation.deployment_configs.entity.vo.deployment_configs_vo import DeleteDeployment_configsModel, Deployment_configsModel, Deployment_configsPageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil


deployment_configsController = APIRouter(prefix='/deployment_configs/deployment_configs', dependencies=[Depends(LoginService.get_current_user)])


@deployment_configsController.get(
    '/list', response_model=PageResponseModel, dependencies=[Depends(CheckUserInterfaceAuth('deployment_configs:deployment_configs:list'))]
)
async def get_deployment_configs_deployment_configs_list(
    request: Request,
deployment_configs_page_query: Deployment_configsPageQueryModel = Depends(Deployment_configsPageQueryModel.as_query),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取分页数据
    deployment_configs_page_query_result = await Deployment_configsService.get_deployment_configs_list_services(query_db, deployment_configs_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=deployment_configs_page_query_result)


@deployment_configsController.post('', dependencies=[Depends(CheckUserInterfaceAuth('deployment_configs:deployment_configs:add'))])
@ValidateFields(validate_model='add_deployment_configs')
@Log(title='部署配置', business_type=BusinessType.INSERT)
async def add_deployment_configs_deployment_configs(
    request: Request,
    add_deployment_configs: Deployment_configsModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_deployment_configs_result = await Deployment_configsService.add_deployment_configs_services(query_db, add_deployment_configs)
    logger.info(add_deployment_configs_result.message)

    return ResponseUtil.success(msg=add_deployment_configs_result.message)


@deployment_configsController.put('', dependencies=[Depends(CheckUserInterfaceAuth('deployment_configs:deployment_configs:edit'))])
@ValidateFields(validate_model='edit_deployment_configs')
@Log(title='部署配置', business_type=BusinessType.UPDATE)
async def edit_deployment_configs_deployment_configs(
    request: Request,
    edit_deployment_configs: Deployment_configsModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    edit_deployment_configs_result = await Deployment_configsService.edit_deployment_configs_services(query_db, edit_deployment_configs)
    logger.info(edit_deployment_configs_result.message)

    return ResponseUtil.success(msg=edit_deployment_configs_result.message)


@deployment_configsController.delete('/{ids}', dependencies=[Depends(CheckUserInterfaceAuth('deployment_configs:deployment_configs:remove'))])
@Log(title='部署配置', business_type=BusinessType.DELETE)
async def delete_deployment_configs_deployment_configs(request: Request, ids: str, query_db: AsyncSession = Depends(get_db)):
    delete_deployment_configs = DeleteDeployment_configsModel(ids=ids)
    delete_deployment_configs_result = await Deployment_configsService.delete_deployment_configs_services(query_db, delete_deployment_configs)
    logger.info(delete_deployment_configs_result.message)

    return ResponseUtil.success(msg=delete_deployment_configs_result.message)


@deployment_configsController.get(
    '/{id}', response_model=Deployment_configsModel, dependencies=[Depends(CheckUserInterfaceAuth('deployment_configs:deployment_configs:query'))]
)
async def query_detail_deployment_configs_deployment_configs(request: Request, id: int, query_db: AsyncSession = Depends(get_db)):
    deployment_configs_detail_result = await Deployment_configsService.deployment_configs_detail_services(query_db, id)
    logger.info(f'获取id为{id}的信息成功')

    return ResponseUtil.success(data=deployment_configs_detail_result)


@deployment_configsController.post('/export', dependencies=[Depends(CheckUserInterfaceAuth('deployment_configs:deployment_configs:export'))])
@Log(title='部署配置', business_type=BusinessType.EXPORT)
async def export_deployment_configs_deployment_configs_list(
    request: Request,
    deployment_configs_page_query: Deployment_configsPageQueryModel = Form(),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    deployment_configs_query_result = await Deployment_configsService.get_deployment_configs_list_services(query_db, deployment_configs_page_query, is_page=False)
    deployment_configs_export_result = await Deployment_configsService.export_deployment_configs_list_services(deployment_configs_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(deployment_configs_export_result))
