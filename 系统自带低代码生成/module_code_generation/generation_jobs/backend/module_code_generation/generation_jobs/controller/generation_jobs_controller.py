from fastapi import APIRouter, Depends, Form, Request
from pydantic_validation_decorator import ValidateFields
from sqlalchemy.ext.asyncio import AsyncSession
from config.enums import BusinessType
from config.get_db import get_db
from module_admin.annotation.log_annotation import Log
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_admin.service.login_service import LoginService
from module_code_generation.generation_jobs.service.generation_jobs_service import Generation_jobsService
from module_code_generation.generation_jobs.entity.vo.generation_jobs_vo import DeleteGeneration_jobsModel, Generation_jobsModel, Generation_jobsPageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil


generation_jobsController = APIRouter(prefix='/generation_jobs/generation_jobs', dependencies=[Depends(LoginService.get_current_user)])


@generation_jobsController.get(
    '/list', response_model=PageResponseModel, dependencies=[Depends(CheckUserInterfaceAuth('generation_jobs:generation_jobs:list'))]
)
async def get_generation_jobs_generation_jobs_list(
    request: Request,
generation_jobs_page_query: Generation_jobsPageQueryModel = Depends(Generation_jobsPageQueryModel.as_query),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取分页数据
    generation_jobs_page_query_result = await Generation_jobsService.get_generation_jobs_list_services(query_db, generation_jobs_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=generation_jobs_page_query_result)


@generation_jobsController.post('', dependencies=[Depends(CheckUserInterfaceAuth('generation_jobs:generation_jobs:add'))])
@ValidateFields(validate_model='add_generation_jobs')
@Log(title='生成任务', business_type=BusinessType.INSERT)
async def add_generation_jobs_generation_jobs(
    request: Request,
    add_generation_jobs: Generation_jobsModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_generation_jobs_result = await Generation_jobsService.add_generation_jobs_services(query_db, add_generation_jobs)
    logger.info(add_generation_jobs_result.message)

    return ResponseUtil.success(msg=add_generation_jobs_result.message)


@generation_jobsController.put('', dependencies=[Depends(CheckUserInterfaceAuth('generation_jobs:generation_jobs:edit'))])
@ValidateFields(validate_model='edit_generation_jobs')
@Log(title='生成任务', business_type=BusinessType.UPDATE)
async def edit_generation_jobs_generation_jobs(
    request: Request,
    edit_generation_jobs: Generation_jobsModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    edit_generation_jobs_result = await Generation_jobsService.edit_generation_jobs_services(query_db, edit_generation_jobs)
    logger.info(edit_generation_jobs_result.message)

    return ResponseUtil.success(msg=edit_generation_jobs_result.message)


@generation_jobsController.delete('/{ids}', dependencies=[Depends(CheckUserInterfaceAuth('generation_jobs:generation_jobs:remove'))])
@Log(title='生成任务', business_type=BusinessType.DELETE)
async def delete_generation_jobs_generation_jobs(request: Request, ids: str, query_db: AsyncSession = Depends(get_db)):
    delete_generation_jobs = DeleteGeneration_jobsModel(ids=ids)
    delete_generation_jobs_result = await Generation_jobsService.delete_generation_jobs_services(query_db, delete_generation_jobs)
    logger.info(delete_generation_jobs_result.message)

    return ResponseUtil.success(msg=delete_generation_jobs_result.message)


@generation_jobsController.get(
    '/{id}', response_model=Generation_jobsModel, dependencies=[Depends(CheckUserInterfaceAuth('generation_jobs:generation_jobs:query'))]
)
async def query_detail_generation_jobs_generation_jobs(request: Request, id: int, query_db: AsyncSession = Depends(get_db)):
    generation_jobs_detail_result = await Generation_jobsService.generation_jobs_detail_services(query_db, id)
    logger.info(f'获取id为{id}的信息成功')

    return ResponseUtil.success(data=generation_jobs_detail_result)


@generation_jobsController.post('/export', dependencies=[Depends(CheckUserInterfaceAuth('generation_jobs:generation_jobs:export'))])
@Log(title='生成任务', business_type=BusinessType.EXPORT)
async def export_generation_jobs_generation_jobs_list(
    request: Request,
    generation_jobs_page_query: Generation_jobsPageQueryModel = Form(),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    generation_jobs_query_result = await Generation_jobsService.get_generation_jobs_list_services(query_db, generation_jobs_page_query, is_page=False)
    generation_jobs_export_result = await Generation_jobsService.export_generation_jobs_list_services(generation_jobs_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(generation_jobs_export_result))
