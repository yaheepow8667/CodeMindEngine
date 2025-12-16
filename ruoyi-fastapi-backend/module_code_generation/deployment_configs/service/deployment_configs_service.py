from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.entity.vo.common_vo import CrudResponseModel
from module_code_generation.deployment_configs.dao.deployment_configs_dao import Deployment_configsDao
from module_code_generation.deployment_configs.entity.vo.deployment_configs_vo import DeleteDeployment_configsModel, Deployment_configsModel, Deployment_configsPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class Deployment_configsService:
    """
    部署配置模块服务层
    """

    @classmethod
    async def get_deployment_configs_list_services(
        cls, query_db: AsyncSession, query_object: Deployment_configsPageQueryModel, is_page: bool = False
    ):
        """
        获取部署配置列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 部署配置列表信息对象
        """
        deployment_configs_list_result = await Deployment_configsDao.get_deployment_configs_list(query_db, query_object, is_page)

        return deployment_configs_list_result


    @classmethod
    async def add_deployment_configs_services(cls, query_db: AsyncSession, page_object: Deployment_configsModel):
        """
        新增部署配置信息service

        :param query_db: orm对象
        :param page_object: 新增部署配置对象
        :return: 新增部署配置校验结果
        """
        try:
            await Deployment_configsDao.add_deployment_configs_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_deployment_configs_services(cls, query_db: AsyncSession, page_object: Deployment_configsModel):
        """
        编辑部署配置信息service

        :param query_db: orm对象
        :param page_object: 编辑部署配置对象
        :return: 编辑部署配置校验结果
        """
        edit_deployment_configs = page_object.model_dump(exclude_unset=True, exclude={})
        deployment_configs_info = await cls.deployment_configs_detail_services(query_db, page_object.id)
        if deployment_configs_info.id:
            try:
                await Deployment_configsDao.edit_deployment_configs_dao(query_db, edit_deployment_configs)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='部署配置不存在')

    @classmethod
    async def delete_deployment_configs_services(cls, query_db: AsyncSession, page_object: DeleteDeployment_configsModel):
        """
        删除部署配置信息service

        :param query_db: orm对象
        :param page_object: 删除部署配置对象
        :return: 删除部署配置校验结果
        """
        if page_object.ids:
            id_list = page_object.ids.split(',')
            try:
                for id in id_list:
                    await Deployment_configsDao.delete_deployment_configs_dao(query_db, Deployment_configsModel(id=id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入部署配置ID为空')

    @classmethod
    async def deployment_configs_detail_services(cls, query_db: AsyncSession, id: int):
        """
        获取部署配置详细信息service

        :param query_db: orm对象
        :param id: 部署配置ID
        :return: 部署配置ID对应的信息
        """
        deployment_configs = await Deployment_configsDao.get_deployment_configs_detail_by_id(query_db, id=id)
        if deployment_configs:
            result = Deployment_configsModel(**CamelCaseUtil.transform_result(deployment_configs))
        else:
            result = Deployment_configsModel(**dict())

        return result

    @staticmethod
    async def export_deployment_configs_list_services(deployment_configs_list: List):
        """
        导出部署配置信息service

        :param deployment_configs_list: 部署配置信息列表
        :return: 部署配置信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'id': '部署配置ID',
            'projectId': '项目ID',
            'name': '配置名称',
            'environment': '部署环境 (development, staging, production)',
            'config': '部署配置内容',
            'isActive': '是否启用',
            'deployedJobId': '已部署的任务ID',
            'deployedAt': '部署时间',
            'deployedByUserId': '部署者用户ID',
            'createdAt': '创建时间',
            'updatedAt': '更新时间',
        }
        binary_data = ExcelUtil.export_list2excel(deployment_configs_list, mapping_dict)

        return binary_data
