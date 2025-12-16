from fastapi import APIRouter, Depends, Form, Request
from pydantic_validation_decorator import ValidateFields
from sqlalchemy.ext.asyncio import AsyncSession
from config.enums import BusinessType
from config.get_db import get_db
from module_admin.annotation.log_annotation import Log
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_admin.service.login_service import LoginService
from module_template_plugin.template_versions.service.template_versions_service import Template_versionsService
from module_template_plugin.template_versions.entity.vo.template_versions_vo import DeleteTemplate_versionsModel, Template_versionsModel, Template_versionsPageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil


template_versionsController = APIRouter(prefix='/template_versions/template_versions', dependencies=[Depends(LoginService.get_current_user)])


@template_versionsController.get(
    '/list', response_model=PageResponseModel, dependencies=[Depends(CheckUserInterfaceAuth('template_versions:template_versions:list'))]
)
async def get_template_versions_template_versions_list(
    request: Request,
template_versions_page_query: Template_versionsPageQueryModel = Depends(Template_versionsPageQueryModel.as_query),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取分页数据
    template_versions_page_query_result = await Template_versionsService.get_template_versions_list_services(query_db, template_versions_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=template_versions_page_query_result)


@template_versionsController.post('', dependencies=[Depends(CheckUserInterfaceAuth('template_versions:template_versions:add'))])
@ValidateFields(validate_model='add_template_versions')
@Log(title='模板版本', business_type=BusinessType.INSERT)
async def add_template_versions_template_versions(
    request: Request,
    add_template_versions: Template_versionsModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_template_versions_result = await Template_versionsService.add_template_versions_services(query_db, add_template_versions)
    logger.info(add_template_versions_result.message)

    return ResponseUtil.success(msg=add_template_versions_result.message)


@template_versionsController.put('', dependencies=[Depends(CheckUserInterfaceAuth('template_versions:template_versions:edit'))])
@ValidateFields(validate_model='edit_template_versions')
@Log(title='模板版本', business_type=BusinessType.UPDATE)
async def edit_template_versions_template_versions(
    request: Request,
    edit_template_versions: Template_versionsModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    edit_template_versions_result = await Template_versionsService.edit_template_versions_services(query_db, edit_template_versions)
    logger.info(edit_template_versions_result.message)

    return ResponseUtil.success(msg=edit_template_versions_result.message)


@template_versionsController.delete('/{ids}', dependencies=[Depends(CheckUserInterfaceAuth('template_versions:template_versions:remove'))])
@Log(title='模板版本', business_type=BusinessType.DELETE)
async def delete_template_versions_template_versions(request: Request, ids: str, query_db: AsyncSession = Depends(get_db)):
    delete_template_versions = DeleteTemplate_versionsModel(ids=ids)
    delete_template_versions_result = await Template_versionsService.delete_template_versions_services(query_db, delete_template_versions)
    logger.info(delete_template_versions_result.message)

    return ResponseUtil.success(msg=delete_template_versions_result.message)


@template_versionsController.get(
    '/{id}', response_model=Template_versionsModel, dependencies=[Depends(CheckUserInterfaceAuth('template_versions:template_versions:query'))]
)
async def query_detail_template_versions_template_versions(request: Request, id: int, query_db: AsyncSession = Depends(get_db)):
    template_versions_detail_result = await Template_versionsService.template_versions_detail_services(query_db, id)
    logger.info(f'获取id为{id}的信息成功')

    return ResponseUtil.success(data=template_versions_detail_result)


@template_versionsController.post('/export', dependencies=[Depends(CheckUserInterfaceAuth('template_versions:template_versions:export'))])
@Log(title='模板版本', business_type=BusinessType.EXPORT)
async def export_template_versions_template_versions_list(
    request: Request,
    template_versions_page_query: Template_versionsPageQueryModel = Form(),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    template_versions_query_result = await Template_versionsService.get_template_versions_list_services(query_db, template_versions_page_query, is_page=False)
    template_versions_export_result = await Template_versionsService.export_template_versions_list_services(template_versions_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(template_versions_export_result))
