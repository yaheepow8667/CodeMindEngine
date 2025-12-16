from fastapi import APIRouter, Depends, Form, Request
from pydantic_validation_decorator import ValidateFields
from sqlalchemy.ext.asyncio import AsyncSession
from config.enums import BusinessType
from config.get_db import get_db
from module_admin.annotation.log_annotation import Log
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_admin.service.login_service import LoginService
from module_system_resource.api_tokens.service.api_tokens_service import Api_tokensService
from module_system_resource.api_tokens.entity.vo.api_tokens_vo import DeleteApi_tokensModel, Api_tokensModel, Api_tokensPageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil


api_tokensController = APIRouter(prefix='/api_tokens/api_tokens', dependencies=[Depends(LoginService.get_current_user)])


@api_tokensController.get(
    '/list', response_model=PageResponseModel, dependencies=[Depends(CheckUserInterfaceAuth('api_tokens:api_tokens:list'))]
)
async def get_api_tokens_api_tokens_list(
    request: Request,
    api_tokens_page_query: Api_tokensPageQueryModel = Depends(Api_tokensPageQueryModel.as_query),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取分页数据
    api_tokens_page_query_result = await Api_tokensService.get_api_tokens_list_services(query_db, api_tokens_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=api_tokens_page_query_result)


@api_tokensController.post('', dependencies=[Depends(CheckUserInterfaceAuth('api_tokens:api_tokens:add'))])
@ValidateFields(validate_model='add_api_tokens')
@Log(title='API访问令牌', business_type=BusinessType.INSERT)
async def add_api_tokens_api_tokens(
    request: Request,
    add_api_tokens: Api_tokensModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_api_tokens_result = await Api_tokensService.add_api_tokens_services(query_db, add_api_tokens)
    logger.info(add_api_tokens_result.message)

    return ResponseUtil.success(msg=add_api_tokens_result.message)


@api_tokensController.put('', dependencies=[Depends(CheckUserInterfaceAuth('api_tokens:api_tokens:edit'))])
@ValidateFields(validate_model='edit_api_tokens')
@Log(title='API访问令牌', business_type=BusinessType.UPDATE)
async def edit_api_tokens_api_tokens(
    request: Request,
    edit_api_tokens: Api_tokensModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    edit_api_tokens_result = await Api_tokensService.edit_api_tokens_services(query_db, edit_api_tokens)
    logger.info(edit_api_tokens_result.message)

    return ResponseUtil.success(msg=edit_api_tokens_result.message)


@api_tokensController.delete('/{ids}', dependencies=[Depends(CheckUserInterfaceAuth('api_tokens:api_tokens:remove'))])
@Log(title='API访问令牌', business_type=BusinessType.DELETE)
async def delete_api_tokens_api_tokens(request: Request, ids: str, query_db: AsyncSession = Depends(get_db)):
    delete_api_tokens = DeleteApi_tokensModel(ids=ids)
    delete_api_tokens_result = await Api_tokensService.delete_api_tokens_services(query_db, delete_api_tokens)
    logger.info(delete_api_tokens_result.message)

    return ResponseUtil.success(msg=delete_api_tokens_result.message)


@api_tokensController.get(
    '/{id}', response_model=Api_tokensModel, dependencies=[Depends(CheckUserInterfaceAuth('api_tokens:api_tokens:query'))]
)
async def query_detail_api_tokens_api_tokens(request: Request, id: int, query_db: AsyncSession = Depends(get_db)):
    api_tokens_detail_result = await Api_tokensService.api_tokens_detail_services(query_db, id)
    logger.info(f'获取id为{id}的信息成功')

    return ResponseUtil.success(data=api_tokens_detail_result)


@api_tokensController.post('/export', dependencies=[Depends(CheckUserInterfaceAuth('api_tokens:api_tokens:export'))])
@Log(title='API访问令牌', business_type=BusinessType.EXPORT)
async def export_api_tokens_api_tokens_list(
    request: Request,
    api_tokens_page_query: Api_tokensPageQueryModel = Form(),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    api_tokens_query_result = await Api_tokensService.get_api_tokens_list_services(query_db, api_tokens_page_query, is_page=False)
    api_tokens_export_result = await Api_tokensService.export_api_tokens_list_services(api_tokens_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(api_tokens_export_result))
