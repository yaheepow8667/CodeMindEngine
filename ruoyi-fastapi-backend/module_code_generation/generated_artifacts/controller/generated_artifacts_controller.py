from fastapi import APIRouter, Depends, Form, Request
from pydantic_validation_decorator import ValidateFields
from sqlalchemy.ext.asyncio import AsyncSession
from config.enums import BusinessType
from config.get_db import get_db
from module_admin.annotation.log_annotation import Log
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_admin.service.login_service import LoginService
from module_code_generation.generated_artifacts.service.generated_artifacts_service import Generated_artifactsService
from module_code_generation.generated_artifacts.entity.vo.generated_artifacts_vo import DeleteGenerated_artifactsModel, Generated_artifactsModel, Generated_artifactsPageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil


generated_artifactsController = APIRouter(prefix='/generated_artifacts/generated_artifacts', dependencies=[Depends(LoginService.get_current_user)])


@generated_artifactsController.get(
    '/list', response_model=PageResponseModel, dependencies=[Depends(CheckUserInterfaceAuth('generated_artifacts:generated_artifacts:list'))]
)
async def get_generated_artifacts_generated_artifacts_list(
    request: Request,
    generated_artifacts_page_query: Generated_artifactsPageQueryModel = Depends(Generated_artifactsPageQueryModel.as_query),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取分页数据
    generated_artifacts_page_query_result = await Generated_artifactsService.get_generated_artifacts_list_services(query_db, generated_artifacts_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=generated_artifacts_page_query_result)


@generated_artifactsController.post('', dependencies=[Depends(CheckUserInterfaceAuth('generated_artifacts:generated_artifacts:add'))])
@ValidateFields(validate_model='add_generated_artifacts')
@Log(title='生成产物', business_type=BusinessType.INSERT)
async def add_generated_artifacts_generated_artifacts(
    request: Request,
    add_generated_artifacts: Generated_artifactsModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_generated_artifacts_result = await Generated_artifactsService.add_generated_artifacts_services(query_db, add_generated_artifacts)
    logger.info(add_generated_artifacts_result.message)

    return ResponseUtil.success(msg=add_generated_artifacts_result.message)


@generated_artifactsController.put('', dependencies=[Depends(CheckUserInterfaceAuth('generated_artifacts:generated_artifacts:edit'))])
@ValidateFields(validate_model='edit_generated_artifacts')
@Log(title='生成产物', business_type=BusinessType.UPDATE)
async def edit_generated_artifacts_generated_artifacts(
    request: Request,
    edit_generated_artifacts: Generated_artifactsModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    edit_generated_artifacts_result = await Generated_artifactsService.edit_generated_artifacts_services(query_db, edit_generated_artifacts)
    logger.info(edit_generated_artifacts_result.message)

    return ResponseUtil.success(msg=edit_generated_artifacts_result.message)


@generated_artifactsController.delete('/{ids}', dependencies=[Depends(CheckUserInterfaceAuth('generated_artifacts:generated_artifacts:remove'))])
@Log(title='生成产物', business_type=BusinessType.DELETE)
async def delete_generated_artifacts_generated_artifacts(request: Request, ids: str, query_db: AsyncSession = Depends(get_db)):
    delete_generated_artifacts = DeleteGenerated_artifactsModel(ids=ids)
    delete_generated_artifacts_result = await Generated_artifactsService.delete_generated_artifacts_services(query_db, delete_generated_artifacts)
    logger.info(delete_generated_artifacts_result.message)

    return ResponseUtil.success(msg=delete_generated_artifacts_result.message)


@generated_artifactsController.get(
    '/{id}', response_model=Generated_artifactsModel, dependencies=[Depends(CheckUserInterfaceAuth('generated_artifacts:generated_artifacts:query'))]
)
async def query_detail_generated_artifacts_generated_artifacts(request: Request, id: int, query_db: AsyncSession = Depends(get_db)):
    generated_artifacts_detail_result = await Generated_artifactsService.generated_artifacts_detail_services(query_db, id)
    logger.info(f'获取id为{id}的信息成功')

    return ResponseUtil.success(data=generated_artifacts_detail_result)


@generated_artifactsController.post('/export', dependencies=[Depends(CheckUserInterfaceAuth('generated_artifacts:generated_artifacts:export'))])
@Log(title='生成产物', business_type=BusinessType.EXPORT)
async def export_generated_artifacts_generated_artifacts_list(
    request: Request,
    generated_artifacts_page_query: Generated_artifactsPageQueryModel = Form(),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    generated_artifacts_query_result = await Generated_artifactsService.get_generated_artifacts_list_services(query_db, generated_artifacts_page_query, is_page=False)
    generated_artifacts_export_result = await Generated_artifactsService.export_generated_artifacts_list_services(generated_artifacts_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(generated_artifacts_export_result))
