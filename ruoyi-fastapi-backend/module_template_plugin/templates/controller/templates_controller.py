from fastapi import APIRouter, Depends, Form, Request
from pydantic_validation_decorator import ValidateFields
from sqlalchemy.ext.asyncio import AsyncSession
from config.enums import BusinessType
from config.get_db import get_db
from module_admin.annotation.log_annotation import Log
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_admin.service.login_service import LoginService
from module_template_plugin.templates.service.templates_service import TemplatesService
from module_template_plugin.templates.entity.vo.templates_vo import DeleteTemplatesModel, TemplatesModel, TemplatesPageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil


templatesController = APIRouter(prefix='/templates/templates', dependencies=[Depends(LoginService.get_current_user)])


@templatesController.get(
    '/list', response_model=PageResponseModel, dependencies=[Depends(CheckUserInterfaceAuth('templates:templates:list'))]
)
async def get_templates_templates_list(
    request: Request,
    templates_page_query: TemplatesPageQueryModel = Depends(TemplatesPageQueryModel.as_query),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取分页数据
    templates_page_query_result = await TemplatesService.get_templates_list_services(query_db, templates_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=templates_page_query_result)


@templatesController.post('', dependencies=[Depends(CheckUserInterfaceAuth('templates:templates:add'))])
@ValidateFields(validate_model='add_templates')
@Log(title='模板', business_type=BusinessType.INSERT)
async def add_templates_templates(
    request: Request,
    add_templates: TemplatesModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_templates_result = await TemplatesService.add_templates_services(query_db, add_templates)
    logger.info(add_templates_result.message)

    return ResponseUtil.success(msg=add_templates_result.message)


@templatesController.put('', dependencies=[Depends(CheckUserInterfaceAuth('templates:templates:edit'))])
@ValidateFields(validate_model='edit_templates')
@Log(title='模板', business_type=BusinessType.UPDATE)
async def edit_templates_templates(
    request: Request,
    edit_templates: TemplatesModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    edit_templates_result = await TemplatesService.edit_templates_services(query_db, edit_templates)
    logger.info(edit_templates_result.message)

    return ResponseUtil.success(msg=edit_templates_result.message)


@templatesController.delete('/{ids}', dependencies=[Depends(CheckUserInterfaceAuth('templates:templates:remove'))])
@Log(title='模板', business_type=BusinessType.DELETE)
async def delete_templates_templates(request: Request, ids: str, query_db: AsyncSession = Depends(get_db)):
    delete_templates = DeleteTemplatesModel(ids=ids)
    delete_templates_result = await TemplatesService.delete_templates_services(query_db, delete_templates)
    logger.info(delete_templates_result.message)

    return ResponseUtil.success(msg=delete_templates_result.message)


@templatesController.get(
    '/{id}', response_model=TemplatesModel, dependencies=[Depends(CheckUserInterfaceAuth('templates:templates:query'))]
)
async def query_detail_templates_templates(request: Request, id: int, query_db: AsyncSession = Depends(get_db)):
    templates_detail_result = await TemplatesService.templates_detail_services(query_db, id)
    logger.info(f'获取id为{id}的信息成功')

    return ResponseUtil.success(data=templates_detail_result)


@templatesController.post('/export', dependencies=[Depends(CheckUserInterfaceAuth('templates:templates:export'))])
@Log(title='模板', business_type=BusinessType.EXPORT)
async def export_templates_templates_list(
    request: Request,
    templates_page_query: TemplatesPageQueryModel = Form(),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    templates_query_result = await TemplatesService.get_templates_list_services(query_db, templates_page_query, is_page=False)
    templates_export_result = await TemplatesService.export_templates_list_services(templates_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(templates_export_result))
