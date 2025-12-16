from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.entity.vo.common_vo import CrudResponseModel
from module_template_plugin.templates.dao.templates_dao import TemplatesDao
from module_template_plugin.templates.entity.vo.templates_vo import DeleteTemplatesModel, TemplatesModel, TemplatesPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class TemplatesService:
    """
    模板模块服务层
    """

    @classmethod
    async def get_templates_list_services(
        cls, query_db: AsyncSession, query_object: TemplatesPageQueryModel, is_page: bool = False
    ):
        """
        获取模板列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 模板列表信息对象
        """
        templates_list_result = await TemplatesDao.get_templates_list(query_db, query_object, is_page)

        return templates_list_result


    @classmethod
    async def add_templates_services(cls, query_db: AsyncSession, page_object: TemplatesModel):
        """
        新增模板信息service

        :param query_db: orm对象
        :param page_object: 新增模板对象
        :return: 新增模板校验结果
        """
        try:
            await TemplatesDao.add_templates_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_templates_services(cls, query_db: AsyncSession, page_object: TemplatesModel):
        """
        编辑模板信息service

        :param query_db: orm对象
        :param page_object: 编辑模板对象
        :return: 编辑模板校验结果
        """
        edit_templates = page_object.model_dump(exclude_unset=True, exclude={})
        templates_info = await cls.templates_detail_services(query_db, page_object.id)
        if templates_info.id:
            try:
                await TemplatesDao.edit_templates_dao(query_db, edit_templates)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='模板不存在')

    @classmethod
    async def delete_templates_services(cls, query_db: AsyncSession, page_object: DeleteTemplatesModel):
        """
        删除模板信息service

        :param query_db: orm对象
        :param page_object: 删除模板对象
        :return: 删除模板校验结果
        """
        if page_object.ids:
            id_list = page_object.ids.split(',')
            try:
                for id in id_list:
                    await TemplatesDao.delete_templates_dao(query_db, TemplatesModel(id=id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入模板ID为空')

    @classmethod
    async def templates_detail_services(cls, query_db: AsyncSession, id: int):
        """
        获取模板详细信息service

        :param query_db: orm对象
        :param id: 模板ID
        :return: 模板ID对应的信息
        """
        templates = await TemplatesDao.get_templates_detail_by_id(query_db, id=id)
        if templates:
            result = TemplatesModel(**CamelCaseUtil.transform_result(templates))
        else:
            result = TemplatesModel(**dict())

        return result

    @staticmethod
    async def export_templates_list_services(templates_list: List):
        """
        导出模板信息service

        :param templates_list: 模板信息列表
        :return: 模板信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'id': '模板ID',
            'name': '模板名称',
            'slug': '模板标识',
            'description': '模板描述',
            'category': '模板分类 (ui_component, api_layer, project_scaffold, workflow)',
            'targetFramework': '目标框架 (vue3, react, nestjs, spring_boot)',
            'complexityLevel': '复杂度 (basic, intermediate, advanced)',
            'isOfficial': '是否官方模板',
            'isPublic': '是否公开',
            'authorUserId': '作者用户ID',
            'downloadCount': '下载次数',
            'rating': '评分',
            'version': '版本',
            'tags': '标签数组',
            'createdAt': '创建时间',
            'updatedAt': '更新时间',
        }
        binary_data = ExcelUtil.export_list2excel(templates_list, mapping_dict)

        return binary_data
