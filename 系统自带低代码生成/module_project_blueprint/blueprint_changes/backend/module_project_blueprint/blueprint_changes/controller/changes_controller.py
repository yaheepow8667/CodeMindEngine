from fastapi import APIRouter, Depends, Form, Request
from pydantic_validation_decorator import ValidateFields
from sqlalchemy.ext.asyncio import AsyncSession
from config.enums import BusinessType
from config.get_db import get_db
from module_admin.annotation.log_annotation import Log
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_admin.service.login_service import LoginService
from module_project_blueprint.blueprint_changes.service.changes_service import ChangesService
from module_project_blueprint.blueprint_changes.entity.vo.changes_vo import DeleteChangesModel, ChangesModel, ChangesPageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil


changesController = APIRouter(prefix='/blueprint_changes/changes', dependencies=[Depends(LoginService.get_current_user)])


@changesController.get(
    '/list', response_model=PageResponseModel, dependencies=[Depends(CheckUserInterfaceAuth('blueprint_changes:changes:list'))]
)
async def get_blueprint_changes_changes_list(
    request: Request,
changes_page_query: ChangesPageQueryModel = Depends(ChangesPageQueryModel.as_query),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取分页数据
    changes_page_query_result = await ChangesService.get_changes_list_services(query_db, changes_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=changes_page_query_result)


@changesController.post('', dependencies=[Depends(CheckUserInterfaceAuth('blueprint_changes:changes:add'))])
@ValidateFields(validate_model='add_changes')
@Log(title='蓝图变更记录', business_type=BusinessType.INSERT)
async def add_blueprint_changes_changes(
    request: Request,
    add_changes: ChangesModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_changes_result = await ChangesService.add_changes_services(query_db, add_changes)
    logger.info(add_changes_result.message)

    return ResponseUtil.success(msg=add_changes_result.message)


@changesController.put('', dependencies=[Depends(CheckUserInterfaceAuth('blueprint_changes:changes:edit'))])
@ValidateFields(validate_model='edit_changes')
@Log(title='蓝图变更记录', business_type=BusinessType.UPDATE)
async def edit_blueprint_changes_changes(
    request: Request,
    edit_changes: ChangesModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    edit_changes_result = await ChangesService.edit_changes_services(query_db, edit_changes)
    logger.info(edit_changes_result.message)

    return ResponseUtil.success(msg=edit_changes_result.message)


@changesController.delete('/{ids}', dependencies=[Depends(CheckUserInterfaceAuth('blueprint_changes:changes:remove'))])
@Log(title='蓝图变更记录', business_type=BusinessType.DELETE)
async def delete_blueprint_changes_changes(request: Request, ids: str, query_db: AsyncSession = Depends(get_db)):
    delete_changes = DeleteChangesModel(ids=ids)
    delete_changes_result = await ChangesService.delete_changes_services(query_db, delete_changes)
    logger.info(delete_changes_result.message)

    return ResponseUtil.success(msg=delete_changes_result.message)


@changesController.get(
    '/{id}', response_model=ChangesModel, dependencies=[Depends(CheckUserInterfaceAuth('blueprint_changes:changes:query'))]
)
async def query_detail_blueprint_changes_changes(request: Request, id: int, query_db: AsyncSession = Depends(get_db)):
    changes_detail_result = await ChangesService.changes_detail_services(query_db, id)
    logger.info(f'获取id为{id}的信息成功')

    return ResponseUtil.success(data=changes_detail_result)


@changesController.post('/export', dependencies=[Depends(CheckUserInterfaceAuth('blueprint_changes:changes:export'))])
@Log(title='蓝图变更记录', business_type=BusinessType.EXPORT)
async def export_blueprint_changes_changes_list(
    request: Request,
    changes_page_query: ChangesPageQueryModel = Form(),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    changes_query_result = await ChangesService.get_changes_list_services(query_db, changes_page_query, is_page=False)
    changes_export_result = await ChangesService.export_changes_list_services(changes_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(changes_export_result))
