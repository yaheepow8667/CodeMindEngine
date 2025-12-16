from fastapi import APIRouter, Depends, Form, Request
from pydantic_validation_decorator import ValidateFields
from sqlalchemy.ext.asyncio import AsyncSession
from config.enums import BusinessType
from config.get_db import get_db
from module_admin.annotation.log_annotation import Log
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_admin.service.login_service import LoginService
from module_system_resource.resources.service.resources_service import ResourcesService
from module_system_resource.resources.entity.vo.resources_vo import DeleteResourcesModel, ResourcesModel, ResourcesPageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil


resourcesController = APIRouter(prefix='/resources/resources', dependencies=[Depends(LoginService.get_current_user)])


@resourcesController.get(
    '/list', response_model=PageResponseModel, dependencies=[Depends(CheckUserInterfaceAuth('resources:resources:list'))]
)
async def get_resources_resources_list(
    request: Request,
resources_page_query: ResourcesPageQueryModel = Depends(ResourcesPageQueryModel.as_query),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取分页数据
    resources_page_query_result = await ResourcesService.get_resources_list_services(query_db, resources_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=resources_page_query_result)


@resourcesController.post('', dependencies=[Depends(CheckUserInterfaceAuth('resources:resources:add'))])
@ValidateFields(validate_model='add_resources')
@Log(title='文件资源', business_type=BusinessType.INSERT)
async def add_resources_resources(
    request: Request,
    add_resources: ResourcesModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_resources_result = await ResourcesService.add_resources_services(query_db, add_resources)
    logger.info(add_resources_result.message)

    return ResponseUtil.success(msg=add_resources_result.message)


@resourcesController.put('', dependencies=[Depends(CheckUserInterfaceAuth('resources:resources:edit'))])
@ValidateFields(validate_model='edit_resources')
@Log(title='文件资源', business_type=BusinessType.UPDATE)
async def edit_resources_resources(
    request: Request,
    edit_resources: ResourcesModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    edit_resources_result = await ResourcesService.edit_resources_services(query_db, edit_resources)
    logger.info(edit_resources_result.message)

    return ResponseUtil.success(msg=edit_resources_result.message)


@resourcesController.delete('/{ids}', dependencies=[Depends(CheckUserInterfaceAuth('resources:resources:remove'))])
@Log(title='文件资源', business_type=BusinessType.DELETE)
async def delete_resources_resources(request: Request, ids: str, query_db: AsyncSession = Depends(get_db)):
    delete_resources = DeleteResourcesModel(ids=ids)
    delete_resources_result = await ResourcesService.delete_resources_services(query_db, delete_resources)
    logger.info(delete_resources_result.message)

    return ResponseUtil.success(msg=delete_resources_result.message)


@resourcesController.get(
    '/{id}', response_model=ResourcesModel, dependencies=[Depends(CheckUserInterfaceAuth('resources:resources:query'))]
)
async def query_detail_resources_resources(request: Request, id: int, query_db: AsyncSession = Depends(get_db)):
    resources_detail_result = await ResourcesService.resources_detail_services(query_db, id)
    logger.info(f'获取id为{id}的信息成功')

    return ResponseUtil.success(data=resources_detail_result)


@resourcesController.post('/export', dependencies=[Depends(CheckUserInterfaceAuth('resources:resources:export'))])
@Log(title='文件资源', business_type=BusinessType.EXPORT)
async def export_resources_resources_list(
    request: Request,
    resources_page_query: ResourcesPageQueryModel = Form(),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    resources_query_result = await ResourcesService.get_resources_list_services(query_db, resources_page_query, is_page=False)
    resources_export_result = await ResourcesService.export_resources_list_services(resources_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(resources_export_result))
