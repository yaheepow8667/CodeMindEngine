from fastapi import APIRouter, Depends, Form, Request
from pydantic_validation_decorator import ValidateFields
from sqlalchemy.ext.asyncio import AsyncSession
from config.enums import BusinessType
from config.get_db import get_db
from module_admin.annotation.log_annotation import Log
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_admin.service.login_service import LoginService
from module_system_resource.subscriptions.service.subscriptions_service import SubscriptionsService
from module_system_resource.subscriptions.entity.vo.subscriptions_vo import DeleteSubscriptionsModel, SubscriptionsModel, SubscriptionsPageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil


subscriptionsController = APIRouter(prefix='/subscriptions/subscriptions', dependencies=[Depends(LoginService.get_current_user)])


@subscriptionsController.get(
    '/list', response_model=PageResponseModel, dependencies=[Depends(CheckUserInterfaceAuth('subscriptions:subscriptions:list'))]
)
async def get_subscriptions_subscriptions_list(
    request: Request,
subscriptions_page_query: SubscriptionsPageQueryModel = Depends(SubscriptionsPageQueryModel.as_query),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取分页数据
    subscriptions_page_query_result = await SubscriptionsService.get_subscriptions_list_services(query_db, subscriptions_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=subscriptions_page_query_result)


@subscriptionsController.post('', dependencies=[Depends(CheckUserInterfaceAuth('subscriptions:subscriptions:add'))])
@ValidateFields(validate_model='add_subscriptions')
@Log(title='订阅与支付', business_type=BusinessType.INSERT)
async def add_subscriptions_subscriptions(
    request: Request,
    add_subscriptions: SubscriptionsModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_subscriptions_result = await SubscriptionsService.add_subscriptions_services(query_db, add_subscriptions)
    logger.info(add_subscriptions_result.message)

    return ResponseUtil.success(msg=add_subscriptions_result.message)


@subscriptionsController.put('', dependencies=[Depends(CheckUserInterfaceAuth('subscriptions:subscriptions:edit'))])
@ValidateFields(validate_model='edit_subscriptions')
@Log(title='订阅与支付', business_type=BusinessType.UPDATE)
async def edit_subscriptions_subscriptions(
    request: Request,
    edit_subscriptions: SubscriptionsModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    edit_subscriptions_result = await SubscriptionsService.edit_subscriptions_services(query_db, edit_subscriptions)
    logger.info(edit_subscriptions_result.message)

    return ResponseUtil.success(msg=edit_subscriptions_result.message)


@subscriptionsController.delete('/{ids}', dependencies=[Depends(CheckUserInterfaceAuth('subscriptions:subscriptions:remove'))])
@Log(title='订阅与支付', business_type=BusinessType.DELETE)
async def delete_subscriptions_subscriptions(request: Request, ids: str, query_db: AsyncSession = Depends(get_db)):
    delete_subscriptions = DeleteSubscriptionsModel(ids=ids)
    delete_subscriptions_result = await SubscriptionsService.delete_subscriptions_services(query_db, delete_subscriptions)
    logger.info(delete_subscriptions_result.message)

    return ResponseUtil.success(msg=delete_subscriptions_result.message)


@subscriptionsController.get(
    '/{id}', response_model=SubscriptionsModel, dependencies=[Depends(CheckUserInterfaceAuth('subscriptions:subscriptions:query'))]
)
async def query_detail_subscriptions_subscriptions(request: Request, id: int, query_db: AsyncSession = Depends(get_db)):
    subscriptions_detail_result = await SubscriptionsService.subscriptions_detail_services(query_db, id)
    logger.info(f'获取id为{id}的信息成功')

    return ResponseUtil.success(data=subscriptions_detail_result)


@subscriptionsController.post('/export', dependencies=[Depends(CheckUserInterfaceAuth('subscriptions:subscriptions:export'))])
@Log(title='订阅与支付', business_type=BusinessType.EXPORT)
async def export_subscriptions_subscriptions_list(
    request: Request,
    subscriptions_page_query: SubscriptionsPageQueryModel = Form(),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    subscriptions_query_result = await SubscriptionsService.get_subscriptions_list_services(query_db, subscriptions_page_query, is_page=False)
    subscriptions_export_result = await SubscriptionsService.export_subscriptions_list_services(subscriptions_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(subscriptions_export_result))
