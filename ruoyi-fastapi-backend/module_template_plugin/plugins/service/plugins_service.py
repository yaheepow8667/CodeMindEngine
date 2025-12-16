from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.entity.vo.common_vo import CrudResponseModel
from module_template_plugin.plugins.dao.plugins_dao import PluginsDao
from module_template_plugin.plugins.entity.vo.plugins_vo import DeletePluginsModel, PluginsModel, PluginsPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class PluginsService:
    """
    插件模块服务层
    """

    @classmethod
    async def get_plugins_list_services(
        cls, query_db: AsyncSession, query_object: PluginsPageQueryModel, is_page: bool = False
    ):
        """
        获取插件列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 插件列表信息对象
        """
        plugins_list_result = await PluginsDao.get_plugins_list(query_db, query_object, is_page)

        return plugins_list_result


    @classmethod
    async def add_plugins_services(cls, query_db: AsyncSession, page_object: PluginsModel):
        """
        新增插件信息service

        :param query_db: orm对象
        :param page_object: 新增插件对象
        :return: 新增插件校验结果
        """
        try:
            await PluginsDao.add_plugins_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_plugins_services(cls, query_db: AsyncSession, page_object: PluginsModel):
        """
        编辑插件信息service

        :param query_db: orm对象
        :param page_object: 编辑插件对象
        :return: 编辑插件校验结果
        """
        edit_plugins = page_object.model_dump(exclude_unset=True, exclude={})
        plugins_info = await cls.plugins_detail_services(query_db, page_object.id)
        if plugins_info.id:
            try:
                await PluginsDao.edit_plugins_dao(query_db, edit_plugins)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='插件不存在')

    @classmethod
    async def delete_plugins_services(cls, query_db: AsyncSession, page_object: DeletePluginsModel):
        """
        删除插件信息service

        :param query_db: orm对象
        :param page_object: 删除插件对象
        :return: 删除插件校验结果
        """
        if page_object.ids:
            id_list = page_object.ids.split(',')
            try:
                for id in id_list:
                    await PluginsDao.delete_plugins_dao(query_db, PluginsModel(id=id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入插件ID为空')

    @classmethod
    async def plugins_detail_services(cls, query_db: AsyncSession, id: int):
        """
        获取插件详细信息service

        :param query_db: orm对象
        :param id: 插件ID
        :return: 插件ID对应的信息
        """
        plugins = await PluginsDao.get_plugins_detail_by_id(query_db, id=id)
        if plugins:
            result = PluginsModel(**CamelCaseUtil.transform_result(plugins))
        else:
            result = PluginsModel(**dict())

        return result

    @staticmethod
    async def export_plugins_list_services(plugins_list: List):
        """
        导出插件信息service

        :param plugins_list: 插件信息列表
        :return: 插件信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'id': '插件ID',
            'name': '插件名称',
            'pluginType': '插件类型 (code_generator, qa_checker, deployer)',
            'targetFramework': '目标框架',
            'version': '版本',
            'authorUserId': '作者用户ID',
            'isApproved': '是否已审核',
            'installCount': '安装次数',
            'configSchema': '插件配置JSON Schema',
            'createdAt': '创建时间',
            'updatedAt': '更新时间',
        }
        binary_data = ExcelUtil.export_list2excel(plugins_list, mapping_dict)

        return binary_data
