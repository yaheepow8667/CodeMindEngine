from fastapi import APIRouter, Depends, Form, Request
from pydantic_validation_decorator import ValidateFields
from sqlalchemy.ext.asyncio import AsyncSession
from config.enums import BusinessType
from config.get_db import get_db
from module_admin.annotation.log_annotation import Log
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_admin.service.login_service import LoginService
from module_team_collaboration.team_members.service.members_service import MembersService
from module_team_collaboration.team_members.entity.vo.members_vo import DeleteMembersModel, MembersModel, MembersPageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil


membersController = APIRouter(prefix='/team_members/members', dependencies=[Depends(LoginService.get_current_user)])


@membersController.get(
    '/list', response_model=PageResponseModel, dependencies=[Depends(CheckUserInterfaceAuth('team_members:members:list'))]
)
async def get_team_members_members_list(
    request: Request,
members_page_query: MembersPageQueryModel = Depends(MembersPageQueryModel.as_query),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取分页数据
    members_page_query_result = await MembersService.get_members_list_services(query_db, members_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=members_page_query_result)


@membersController.post('', dependencies=[Depends(CheckUserInterfaceAuth('team_members:members:add'))])
@ValidateFields(validate_model='add_members')
@Log(title='团队成员', business_type=BusinessType.INSERT)
async def add_team_members_members(
    request: Request,
    add_members: MembersModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_members_result = await MembersService.add_members_services(query_db, add_members)
    logger.info(add_members_result.message)

    return ResponseUtil.success(msg=add_members_result.message)


@membersController.put('', dependencies=[Depends(CheckUserInterfaceAuth('team_members:members:edit'))])
@ValidateFields(validate_model='edit_members')
@Log(title='团队成员', business_type=BusinessType.UPDATE)
async def edit_team_members_members(
    request: Request,
    edit_members: MembersModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    edit_members_result = await MembersService.edit_members_services(query_db, edit_members)
    logger.info(edit_members_result.message)

    return ResponseUtil.success(msg=edit_members_result.message)


@membersController.delete('/{ids}', dependencies=[Depends(CheckUserInterfaceAuth('team_members:members:remove'))])
@Log(title='团队成员', business_type=BusinessType.DELETE)
async def delete_team_members_members(request: Request, ids: str, query_db: AsyncSession = Depends(get_db)):
    delete_members = DeleteMembersModel(ids=ids)
    delete_members_result = await MembersService.delete_members_services(query_db, delete_members)
    logger.info(delete_members_result.message)

    return ResponseUtil.success(msg=delete_members_result.message)


@membersController.get(
    '/{id}', response_model=MembersModel, dependencies=[Depends(CheckUserInterfaceAuth('team_members:members:query'))]
)
async def query_detail_team_members_members(request: Request, id: int, query_db: AsyncSession = Depends(get_db)):
    members_detail_result = await MembersService.members_detail_services(query_db, id)
    logger.info(f'获取id为{id}的信息成功')

    return ResponseUtil.success(data=members_detail_result)


@membersController.post('/export', dependencies=[Depends(CheckUserInterfaceAuth('team_members:members:export'))])
@Log(title='团队成员', business_type=BusinessType.EXPORT)
async def export_team_members_members_list(
    request: Request,
    members_page_query: MembersPageQueryModel = Form(),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    members_query_result = await MembersService.get_members_list_services(query_db, members_page_query, is_page=False)
    members_export_result = await MembersService.export_members_list_services(members_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(members_export_result))
