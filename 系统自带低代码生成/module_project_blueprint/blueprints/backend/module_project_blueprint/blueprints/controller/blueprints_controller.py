from fastapi import APIRouter, Depends, Form, Request
from pydantic_validation_decorator import ValidateFields
from sqlalchemy.ext.asyncio import AsyncSession
from config.enums import BusinessType
from config.get_db import get_db
from module_admin.annotation.log_annotation import Log
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_admin.service.login_service import LoginService
from module_project_blueprint.blueprints.service.blueprints_service import BlueprintsService
from module_project_blueprint.blueprints.entity.vo.blueprints_vo import DeleteBlueprintsModel, BlueprintsModel, BlueprintsPageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil


blueprintsController = APIRouter(prefix='/blueprints/blueprints', dependencies=[Depends(LoginService.get_current_user)])


@blueprintsController.get(
    '/list', response_model=PageResponseModel, dependencies=[Depends(CheckUserInterfaceAuth('blueprints:blueprints:list'))]
)
async def get_blueprints_blueprints_list(
    request: Request,
blueprints_page_query: BlueprintsPageQueryModel = Depends(BlueprintsPageQueryModel.as_query),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取分页数据
    blueprints_page_query_result = await BlueprintsService.get_blueprints_list_services(query_db, blueprints_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=blueprints_page_query_result)


@blueprintsController.post('', dependencies=[Depends(CheckUserInterfaceAuth('blueprints:blueprints:add'))])
@ValidateFields(validate_model='add_blueprints')
@Log(title='蓝图', business_type=BusinessType.INSERT)
async def add_blueprints_blueprints(
    request: Request,
    add_blueprints: BlueprintsModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_blueprints_result = await BlueprintsService.add_blueprints_services(query_db, add_blueprints)
    logger.info(add_blueprints_result.message)

    return ResponseUtil.success(msg=add_blueprints_result.message)


@blueprintsController.put('', dependencies=[Depends(CheckUserInterfaceAuth('blueprints:blueprints:edit'))])
@ValidateFields(validate_model='edit_blueprints')
@Log(title='蓝图', business_type=BusinessType.UPDATE)
async def edit_blueprints_blueprints(
    request: Request,
    edit_blueprints: BlueprintsModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    edit_blueprints_result = await BlueprintsService.edit_blueprints_services(query_db, edit_blueprints)
    logger.info(edit_blueprints_result.message)

    return ResponseUtil.success(msg=edit_blueprints_result.message)


@blueprintsController.delete('/{ids}', dependencies=[Depends(CheckUserInterfaceAuth('blueprints:blueprints:remove'))])
@Log(title='蓝图', business_type=BusinessType.DELETE)
async def delete_blueprints_blueprints(request: Request, ids: str, query_db: AsyncSession = Depends(get_db)):
    delete_blueprints = DeleteBlueprintsModel(ids=ids)
    delete_blueprints_result = await BlueprintsService.delete_blueprints_services(query_db, delete_blueprints)
    logger.info(delete_blueprints_result.message)

    return ResponseUtil.success(msg=delete_blueprints_result.message)


@blueprintsController.get(
    '/{id}', response_model=BlueprintsModel, dependencies=[Depends(CheckUserInterfaceAuth('blueprints:blueprints:query'))]
)
async def query_detail_blueprints_blueprints(request: Request, id: int, query_db: AsyncSession = Depends(get_db)):
    blueprints_detail_result = await BlueprintsService.blueprints_detail_services(query_db, id)
    logger.info(f'获取id为{id}的信息成功')

    return ResponseUtil.success(data=blueprints_detail_result)


@blueprintsController.post('/export', dependencies=[Depends(CheckUserInterfaceAuth('blueprints:blueprints:export'))])
@Log(title='蓝图', business_type=BusinessType.EXPORT)
async def export_blueprints_blueprints_list(
    request: Request,
    blueprints_page_query: BlueprintsPageQueryModel = Form(),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    blueprints_query_result = await BlueprintsService.get_blueprints_list_services(query_db, blueprints_page_query, is_page=False)
    blueprints_export_result = await BlueprintsService.export_blueprints_list_services(blueprints_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(blueprints_export_result))
