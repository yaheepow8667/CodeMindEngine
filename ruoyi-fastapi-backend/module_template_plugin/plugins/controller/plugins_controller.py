from fastapi import APIRouter, Depends, Form, Request
from pydantic_validation_decorator import ValidateFields
from sqlalchemy.ext.asyncio import AsyncSession
from config.enums import BusinessType
from config.get_db import get_db
from module_admin.annotation.log_annotation import Log
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_admin.service.login_service import LoginService
from module_template_plugin.plugins.service.plugins_service import PluginsService
from module_template_plugin.plugins.entity.vo.plugins_vo import DeletePluginsModel, PluginsModel, PluginsPageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil


pluginsController = APIRouter(prefix='/plugins/plugins', dependencies=[Depends(LoginService.get_current_user)])


@pluginsController.get(
    '/list', response_model=PageResponseModel, dependencies=[Depends(CheckUserInterfaceAuth('plugins:plugins:list'))]
)
async def get_plugins_plugins_list(
    request: Request,
    plugins_page_query: PluginsPageQueryModel = Depends(PluginsPageQueryModel.as_query),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取分页数据
    plugins_page_query_result = await PluginsService.get_plugins_list_services(query_db, plugins_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=plugins_page_query_result)


@pluginsController.post('', dependencies=[Depends(CheckUserInterfaceAuth('plugins:plugins:add'))])
@ValidateFields(validate_model='add_plugins')
@Log(title='插件', business_type=BusinessType.INSERT)
async def add_plugins_plugins(
    request: Request,
    add_plugins: PluginsModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_plugins_result = await PluginsService.add_plugins_services(query_db, add_plugins)
    logger.info(add_plugins_result.message)

    return ResponseUtil.success(msg=add_plugins_result.message)


@pluginsController.put('', dependencies=[Depends(CheckUserInterfaceAuth('plugins:plugins:edit'))])
@ValidateFields(validate_model='edit_plugins')
@Log(title='插件', business_type=BusinessType.UPDATE)
async def edit_plugins_plugins(
    request: Request,
    edit_plugins: PluginsModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    edit_plugins_result = await PluginsService.edit_plugins_services(query_db, edit_plugins)
    logger.info(edit_plugins_result.message)

    return ResponseUtil.success(msg=edit_plugins_result.message)


@pluginsController.delete('/{ids}', dependencies=[Depends(CheckUserInterfaceAuth('plugins:plugins:remove'))])
@Log(title='插件', business_type=BusinessType.DELETE)
async def delete_plugins_plugins(request: Request, ids: str, query_db: AsyncSession = Depends(get_db)):
    delete_plugins = DeletePluginsModel(ids=ids)
    delete_plugins_result = await PluginsService.delete_plugins_services(query_db, delete_plugins)
    logger.info(delete_plugins_result.message)

    return ResponseUtil.success(msg=delete_plugins_result.message)


@pluginsController.get(
    '/{id}', response_model=PluginsModel, dependencies=[Depends(CheckUserInterfaceAuth('plugins:plugins:query'))]
)
async def query_detail_plugins_plugins(request: Request, id: int, query_db: AsyncSession = Depends(get_db)):
    plugins_detail_result = await PluginsService.plugins_detail_services(query_db, id)
    logger.info(f'获取id为{id}的信息成功')

    return ResponseUtil.success(data=plugins_detail_result)


@pluginsController.post('/export', dependencies=[Depends(CheckUserInterfaceAuth('plugins:plugins:export'))])
@Log(title='插件', business_type=BusinessType.EXPORT)
async def export_plugins_plugins_list(
    request: Request,
    plugins_page_query: PluginsPageQueryModel = Form(),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    plugins_query_result = await PluginsService.get_plugins_list_services(query_db, plugins_page_query, is_page=False)
    plugins_export_result = await PluginsService.export_plugins_list_services(plugins_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(plugins_export_result))
