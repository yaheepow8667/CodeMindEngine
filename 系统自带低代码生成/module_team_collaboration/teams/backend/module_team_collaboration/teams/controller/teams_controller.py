from fastapi import APIRouter, Depends, Form, Request
from pydantic_validation_decorator import ValidateFields
from sqlalchemy.ext.asyncio import AsyncSession
from config.enums import BusinessType
from config.get_db import get_db
from module_admin.annotation.log_annotation import Log
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_admin.service.login_service import LoginService
from module_team_collaboration.teams.service.teams_service import TeamsService
from module_team_collaboration.teams.entity.vo.teams_vo import DeleteTeamsModel, TeamsModel, TeamsPageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil


teamsController = APIRouter(prefix='/teams/teams', dependencies=[Depends(LoginService.get_current_user)])


@teamsController.get(
    '/list', response_model=PageResponseModel, dependencies=[Depends(CheckUserInterfaceAuth('teams:teams:list'))]
)
async def get_teams_teams_list(
    request: Request,
teams_page_query: TeamsPageQueryModel = Depends(TeamsPageQueryModel.as_query),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取分页数据
    teams_page_query_result = await TeamsService.get_teams_list_services(query_db, teams_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=teams_page_query_result)


@teamsController.post('', dependencies=[Depends(CheckUserInterfaceAuth('teams:teams:add'))])
@ValidateFields(validate_model='add_teams')
@Log(title='团队', business_type=BusinessType.INSERT)
async def add_teams_teams(
    request: Request,
    add_teams: TeamsModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_teams_result = await TeamsService.add_teams_services(query_db, add_teams)
    logger.info(add_teams_result.message)

    return ResponseUtil.success(msg=add_teams_result.message)


@teamsController.put('', dependencies=[Depends(CheckUserInterfaceAuth('teams:teams:edit'))])
@ValidateFields(validate_model='edit_teams')
@Log(title='团队', business_type=BusinessType.UPDATE)
async def edit_teams_teams(
    request: Request,
    edit_teams: TeamsModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    edit_teams_result = await TeamsService.edit_teams_services(query_db, edit_teams)
    logger.info(edit_teams_result.message)

    return ResponseUtil.success(msg=edit_teams_result.message)


@teamsController.delete('/{ids}', dependencies=[Depends(CheckUserInterfaceAuth('teams:teams:remove'))])
@Log(title='团队', business_type=BusinessType.DELETE)
async def delete_teams_teams(request: Request, ids: str, query_db: AsyncSession = Depends(get_db)):
    delete_teams = DeleteTeamsModel(ids=ids)
    delete_teams_result = await TeamsService.delete_teams_services(query_db, delete_teams)
    logger.info(delete_teams_result.message)

    return ResponseUtil.success(msg=delete_teams_result.message)


@teamsController.get(
    '/{id}', response_model=TeamsModel, dependencies=[Depends(CheckUserInterfaceAuth('teams:teams:query'))]
)
async def query_detail_teams_teams(request: Request, id: int, query_db: AsyncSession = Depends(get_db)):
    teams_detail_result = await TeamsService.teams_detail_services(query_db, id)
    logger.info(f'获取id为{id}的信息成功')

    return ResponseUtil.success(data=teams_detail_result)


@teamsController.post('/export', dependencies=[Depends(CheckUserInterfaceAuth('teams:teams:export'))])
@Log(title='团队', business_type=BusinessType.EXPORT)
async def export_teams_teams_list(
    request: Request,
    teams_page_query: TeamsPageQueryModel = Form(),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    teams_query_result = await TeamsService.get_teams_list_services(query_db, teams_page_query, is_page=False)
    teams_export_result = await TeamsService.export_teams_list_services(teams_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(teams_export_result))
