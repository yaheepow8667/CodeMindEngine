from fastapi import APIRouter, Depends, Form, Request
from pydantic_validation_decorator import ValidateFields
from sqlalchemy.ext.asyncio import AsyncSession
from config.enums import BusinessType
from config.get_db import get_db
from module_admin.annotation.log_annotation import Log
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_admin.service.login_service import LoginService
from module_team_collaboration.invitations.service.invitations_service import InvitationsService
from module_team_collaboration.invitations.entity.vo.invitations_vo import DeleteInvitationsModel, InvitationsModel, InvitationsPageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil


invitationsController = APIRouter(prefix='/invitations/invitations', dependencies=[Depends(LoginService.get_current_user)])


@invitationsController.get(
    '/list', response_model=PageResponseModel, dependencies=[Depends(CheckUserInterfaceAuth('invitations:invitations:list'))]
)
async def get_invitations_invitations_list(
    request: Request,
invitations_page_query: InvitationsPageQueryModel = Depends(InvitationsPageQueryModel.as_query),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取分页数据
    invitations_page_query_result = await InvitationsService.get_invitations_list_services(query_db, invitations_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=invitations_page_query_result)


@invitationsController.post('', dependencies=[Depends(CheckUserInterfaceAuth('invitations:invitations:add'))])
@ValidateFields(validate_model='add_invitations')
@Log(title='邀请', business_type=BusinessType.INSERT)
async def add_invitations_invitations(
    request: Request,
    add_invitations: InvitationsModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_invitations_result = await InvitationsService.add_invitations_services(query_db, add_invitations)
    logger.info(add_invitations_result.message)

    return ResponseUtil.success(msg=add_invitations_result.message)


@invitationsController.put('', dependencies=[Depends(CheckUserInterfaceAuth('invitations:invitations:edit'))])
@ValidateFields(validate_model='edit_invitations')
@Log(title='邀请', business_type=BusinessType.UPDATE)
async def edit_invitations_invitations(
    request: Request,
    edit_invitations: InvitationsModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    edit_invitations_result = await InvitationsService.edit_invitations_services(query_db, edit_invitations)
    logger.info(edit_invitations_result.message)

    return ResponseUtil.success(msg=edit_invitations_result.message)


@invitationsController.delete('/{ids}', dependencies=[Depends(CheckUserInterfaceAuth('invitations:invitations:remove'))])
@Log(title='邀请', business_type=BusinessType.DELETE)
async def delete_invitations_invitations(request: Request, ids: str, query_db: AsyncSession = Depends(get_db)):
    delete_invitations = DeleteInvitationsModel(ids=ids)
    delete_invitations_result = await InvitationsService.delete_invitations_services(query_db, delete_invitations)
    logger.info(delete_invitations_result.message)

    return ResponseUtil.success(msg=delete_invitations_result.message)


@invitationsController.get(
    '/{id}', response_model=InvitationsModel, dependencies=[Depends(CheckUserInterfaceAuth('invitations:invitations:query'))]
)
async def query_detail_invitations_invitations(request: Request, id: int, query_db: AsyncSession = Depends(get_db)):
    invitations_detail_result = await InvitationsService.invitations_detail_services(query_db, id)
    logger.info(f'获取id为{id}的信息成功')

    return ResponseUtil.success(data=invitations_detail_result)


@invitationsController.post('/export', dependencies=[Depends(CheckUserInterfaceAuth('invitations:invitations:export'))])
@Log(title='邀请', business_type=BusinessType.EXPORT)
async def export_invitations_invitations_list(
    request: Request,
    invitations_page_query: InvitationsPageQueryModel = Form(),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    invitations_query_result = await InvitationsService.get_invitations_list_services(query_db, invitations_page_query, is_page=False)
    invitations_export_result = await InvitationsService.export_invitations_list_services(invitations_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(invitations_export_result))
