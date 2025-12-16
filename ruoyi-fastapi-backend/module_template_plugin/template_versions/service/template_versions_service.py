from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.entity.vo.common_vo import CrudResponseModel
from module_template_plugin.template_versions.dao.template_versions_dao import Template_versionsDao
from module_template_plugin.template_versions.entity.vo.template_versions_vo import DeleteTemplate_versionsModel, Template_versionsModel, Template_versionsPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class Template_versionsService:
    """
    模板版本模块服务层
    """

    @classmethod
    async def get_template_versions_list_services(
        cls, query_db: AsyncSession, query_object: Template_versionsPageQueryModel, is_page: bool = False
    ):
        """
        获取模板版本列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 模板版本列表信息对象
        """
        template_versions_list_result = await Template_versionsDao.get_template_versions_list(query_db, query_object, is_page)

        return template_versions_list_result


    @classmethod
    async def add_template_versions_services(cls, query_db: AsyncSession, page_object: Template_versionsModel):
        """
        新增模板版本信息service

        :param query_db: orm对象
        :param page_object: 新增模板版本对象
        :return: 新增模板版本校验结果
        """
        try:
            await Template_versionsDao.add_template_versions_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_template_versions_services(cls, query_db: AsyncSession, page_object: Template_versionsModel):
        """
        编辑模板版本信息service

        :param query_db: orm对象
        :param page_object: 编辑模板版本对象
        :return: 编辑模板版本校验结果
        """
        edit_template_versions = page_object.model_dump(exclude_unset=True, exclude={})
        template_versions_info = await cls.template_versions_detail_services(query_db, page_object.id)
        if template_versions_info.id:
            try:
                await Template_versionsDao.edit_template_versions_dao(query_db, edit_template_versions)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='模板版本不存在')

    @classmethod
    async def delete_template_versions_services(cls, query_db: AsyncSession, page_object: DeleteTemplate_versionsModel):
        """
        删除模板版本信息service

        :param query_db: orm对象
        :param page_object: 删除模板版本对象
        :return: 删除模板版本校验结果
        """
        if page_object.ids:
            id_list = page_object.ids.split(',')
            try:
                for id in id_list:
                    await Template_versionsDao.delete_template_versions_dao(query_db, Template_versionsModel(id=id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入模板版本ID为空')

    @classmethod
    async def template_versions_detail_services(cls, query_db: AsyncSession, id: int):
        """
        获取模板版本详细信息service

        :param query_db: orm对象
        :param id: 模板版本ID
        :return: 模板版本ID对应的信息
        """
        template_versions = await Template_versionsDao.get_template_versions_detail_by_id(query_db, id=id)
        if template_versions:
            result = Template_versionsModel(**CamelCaseUtil.transform_result(template_versions))
        else:
            result = Template_versionsModel(**dict())

        return result

    @staticmethod
    async def export_template_versions_list_services(template_versions_list: List):
        """
        导出模板版本信息service

        :param template_versions_list: 模板版本信息列表
        :return: 模板版本信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'id': '模板版本ID',
            'templateId': '模板ID',
            'version': '版本号',
            'changelog': '更新日志',
            'templateContent': '模板JSON定义',
            'exampleBlueprint': '示例蓝图',
            'isActive': '是否启用',
            'publishedAt': '发布时间',
            'publishedByUserId': '发布者用户ID',
            'createdAt': '创建时间',
        }
        binary_data = ExcelUtil.export_list2excel(template_versions_list, mapping_dict)

        return binary_data
