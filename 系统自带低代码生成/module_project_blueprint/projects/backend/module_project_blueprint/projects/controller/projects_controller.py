from fastapi import APIRouter, Depends, Form, Request
from pydantic_validation_decorator import ValidateFields
from sqlalchemy.ext.asyncio import AsyncSession
from config.enums import BusinessType
from config.get_db import get_db
from module_admin.annotation.log_annotation import Log
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_admin.service.login_service import LoginService
from module_project_blueprint.projects.service.projects_service import ProjectsService
from module_project_blueprint.projects.entity.vo.projects_vo import DeleteProjectsModel, ProjectsModel, ProjectsPageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil


projectsController = APIRouter(prefix='/projects/projects', dependencies=[Depends(LoginService.get_current_user)])


@projectsController.get(
    '/list', response_model=PageResponseModel, dependencies=[Depends(CheckUserInterfaceAuth('projects:projects:list'))]
)
async def get_projects_projects_list(
    request: Request,
projects_page_query: ProjectsPageQueryModel = Depends(ProjectsPageQueryModel.as_query),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取分页数据
    projects_page_query_result = await ProjectsService.get_projects_list_services(query_db, projects_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=projects_page_query_result)


@projectsController.post('', dependencies=[Depends(CheckUserInterfaceAuth('projects:projects:add'))])
@ValidateFields(validate_model='add_projects')
@Log(title='项目', business_type=BusinessType.INSERT)
async def add_projects_projects(
    request: Request,
    add_projects: ProjectsModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_projects_result = await ProjectsService.add_projects_services(query_db, add_projects)
    logger.info(add_projects_result.message)

    return ResponseUtil.success(msg=add_projects_result.message)


@projectsController.put('', dependencies=[Depends(CheckUserInterfaceAuth('projects:projects:edit'))])
@ValidateFields(validate_model='edit_projects')
@Log(title='项目', business_type=BusinessType.UPDATE)
async def edit_projects_projects(
    request: Request,
    edit_projects: ProjectsModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    edit_projects_result = await ProjectsService.edit_projects_services(query_db, edit_projects)
    logger.info(edit_projects_result.message)

    return ResponseUtil.success(msg=edit_projects_result.message)


@projectsController.delete('/{ids}', dependencies=[Depends(CheckUserInterfaceAuth('projects:projects:remove'))])
@Log(title='项目', business_type=BusinessType.DELETE)
async def delete_projects_projects(request: Request, ids: str, query_db: AsyncSession = Depends(get_db)):
    delete_projects = DeleteProjectsModel(ids=ids)
    delete_projects_result = await ProjectsService.delete_projects_services(query_db, delete_projects)
    logger.info(delete_projects_result.message)

    return ResponseUtil.success(msg=delete_projects_result.message)


@projectsController.get(
    '/{id}', response_model=ProjectsModel, dependencies=[Depends(CheckUserInterfaceAuth('projects:projects:query'))]
)
async def query_detail_projects_projects(request: Request, id: int, query_db: AsyncSession = Depends(get_db)):
    projects_detail_result = await ProjectsService.projects_detail_services(query_db, id)
    logger.info(f'获取id为{id}的信息成功')

    return ResponseUtil.success(data=projects_detail_result)


@projectsController.post('/export', dependencies=[Depends(CheckUserInterfaceAuth('projects:projects:export'))])
@Log(title='项目', business_type=BusinessType.EXPORT)
async def export_projects_projects_list(
    request: Request,
    projects_page_query: ProjectsPageQueryModel = Form(),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    projects_query_result = await ProjectsService.get_projects_list_services(query_db, projects_page_query, is_page=False)
    projects_export_result = await ProjectsService.export_projects_list_services(projects_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(projects_export_result))
