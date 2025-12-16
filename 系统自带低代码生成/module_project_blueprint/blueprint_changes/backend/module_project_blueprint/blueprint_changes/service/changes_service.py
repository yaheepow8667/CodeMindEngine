from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.entity.vo.common_vo import CrudResponseModel
from module_project_blueprint.blueprint_changes.dao.changes_dao import ChangesDao
from module_project_blueprint.blueprint_changes.entity.vo.changes_vo import DeleteChangesModel, ChangesModel, ChangesPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class ChangesService:
    """
    蓝图变更记录模块服务层
    """

    @classmethod
    async def get_changes_list_services(
        cls, query_db: AsyncSession, query_object: ChangesPageQueryModel, is_page: bool = False
    ):
        """
        获取蓝图变更记录列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 蓝图变更记录列表信息对象
        """
        changes_list_result = await ChangesDao.get_changes_list(query_db, query_object, is_page)

        return changes_list_result


    @classmethod
    async def add_changes_services(cls, query_db: AsyncSession, page_object: ChangesModel):
        """
        新增蓝图变更记录信息service

        :param query_db: orm对象
        :param page_object: 新增蓝图变更记录对象
        :return: 新增蓝图变更记录校验结果
        """
        try:
            await ChangesDao.add_changes_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_changes_services(cls, query_db: AsyncSession, page_object: ChangesModel):
        """
        编辑蓝图变更记录信息service

        :param query_db: orm对象
        :param page_object: 编辑蓝图变更记录对象
        :return: 编辑蓝图变更记录校验结果
        """
        edit_changes = page_object.model_dump(exclude_unset=True, exclude={})
        changes_info = await cls.changes_detail_services(query_db, page_object.id)
        if changes_info.id:
            try:
                await ChangesDao.edit_changes_dao(query_db, edit_changes)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='蓝图变更记录不存在')

    @classmethod
    async def delete_changes_services(cls, query_db: AsyncSession, page_object: DeleteChangesModel):
        """
        删除蓝图变更记录信息service

        :param query_db: orm对象
        :param page_object: 删除蓝图变更记录对象
        :return: 删除蓝图变更记录校验结果
        """
        if page_object.ids:
            id_list = page_object.ids.split(',')
            try:
                for id in id_list:
                    await ChangesDao.delete_changes_dao(query_db, ChangesModel(id=id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入蓝图变更ID为空')

    @classmethod
    async def changes_detail_services(cls, query_db: AsyncSession, id: int):
        """
        获取蓝图变更记录详细信息service

        :param query_db: orm对象
        :param id: 蓝图变更ID
        :return: 蓝图变更ID对应的信息
        """
        changes = await ChangesDao.get_changes_detail_by_id(query_db, id=id)
        if changes:
            result = ChangesModel(**CamelCaseUtil.transform_result(changes))
        else:
            result = ChangesModel(**dict())

        return result

    @staticmethod
    async def export_changes_list_services(changes_list: List):
        """
        导出蓝图变更记录信息service

        :param changes_list: 蓝图变更记录信息列表
        :return: 蓝图变更记录信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'id': '蓝图变更ID',
            'blueprintId': '蓝图ID',
            'changeType': '变更类型 (create, update, delete)',
            'fieldPath': '变更字段路径 如 "dataModels.User.fields"',
            'oldValue': '旧值',
            'newValue': '新值',
            'changedByUserId': '变更者用户ID',
            'createdAt': '创建时间',
        }
        binary_data = ExcelUtil.export_list2excel(changes_list, mapping_dict)

        return binary_data
