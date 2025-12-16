from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.entity.vo.common_vo import CrudResponseModel
from module_code_generation.generation_jobs.dao.generation_jobs_dao import Generation_jobsDao
from module_code_generation.generation_jobs.entity.vo.generation_jobs_vo import DeleteGeneration_jobsModel, Generation_jobsModel, Generation_jobsPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class Generation_jobsService:
    """
    生成任务模块服务层
    """

    @classmethod
    async def get_generation_jobs_list_services(
        cls, query_db: AsyncSession, query_object: Generation_jobsPageQueryModel, is_page: bool = False
    ):
        """
        获取生成任务列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 生成任务列表信息对象
        """
        generation_jobs_list_result = await Generation_jobsDao.get_generation_jobs_list(query_db, query_object, is_page)

        return generation_jobs_list_result


    @classmethod
    async def add_generation_jobs_services(cls, query_db: AsyncSession, page_object: Generation_jobsModel):
        """
        新增生成任务信息service

        :param query_db: orm对象
        :param page_object: 新增生成任务对象
        :return: 新增生成任务校验结果
        """
        try:
            await Generation_jobsDao.add_generation_jobs_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_generation_jobs_services(cls, query_db: AsyncSession, page_object: Generation_jobsModel):
        """
        编辑生成任务信息service

        :param query_db: orm对象
        :param page_object: 编辑生成任务对象
        :return: 编辑生成任务校验结果
        """
        edit_generation_jobs = page_object.model_dump(exclude_unset=True, exclude={})
        generation_jobs_info = await cls.generation_jobs_detail_services(query_db, page_object.id)
        if generation_jobs_info.id:
            try:
                await Generation_jobsDao.edit_generation_jobs_dao(query_db, edit_generation_jobs)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='生成任务不存在')

    @classmethod
    async def delete_generation_jobs_services(cls, query_db: AsyncSession, page_object: DeleteGeneration_jobsModel):
        """
        删除生成任务信息service

        :param query_db: orm对象
        :param page_object: 删除生成任务对象
        :return: 删除生成任务校验结果
        """
        if page_object.ids:
            id_list = page_object.ids.split(',')
            try:
                for id in id_list:
                    await Generation_jobsDao.delete_generation_jobs_dao(query_db, Generation_jobsModel(id=id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入生成任务ID为空')

    @classmethod
    async def generation_jobs_detail_services(cls, query_db: AsyncSession, id: int):
        """
        获取生成任务详细信息service

        :param query_db: orm对象
        :param id: 生成任务ID
        :return: 生成任务ID对应的信息
        """
        generation_jobs = await Generation_jobsDao.get_generation_jobs_detail_by_id(query_db, id=id)
        if generation_jobs:
            result = Generation_jobsModel(**CamelCaseUtil.transform_result(generation_jobs))
        else:
            result = Generation_jobsModel(**dict())

        return result

    @staticmethod
    async def export_generation_jobs_list_services(generation_jobs_list: List):
        """
        导出生成任务信息service

        :param generation_jobs_list: 生成任务信息列表
        :return: 生成任务信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'id': '生成任务ID',
            'projectId': '项目ID',
            'blueprintId': '蓝图ID',
            'status': '任务状态 (pending, generating, qa, success, failed)',
            'targetTechStack': '目标技术栈配置',
            'triggerType': '触发类型 (manual, api, webhook, schedule)',
            'triggeredByUserId': '触发者用户ID',
            'startedAt': '开始时间',
            'completedAt': '完成时间',
            'errorMessage': '错误信息',
            'logs': '生成日志',
            'qaReport': '质量检查报告',
            'createdAt': '创建时间',
        }
        binary_data = ExcelUtil.export_list2excel(generation_jobs_list, mapping_dict)

        return binary_data
