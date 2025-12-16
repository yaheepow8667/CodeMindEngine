from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.entity.vo.common_vo import CrudResponseModel
from module_project_blueprint.blueprints.dao.blueprints_dao import BlueprintsDao
from module_project_blueprint.blueprints.entity.vo.blueprints_vo import DeleteBlueprintsModel, BlueprintsModel, BlueprintsPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class BlueprintsService:
    """
    蓝图模块服务层
    """

    @classmethod
    async def get_blueprints_list_services(
        cls, query_db: AsyncSession, query_object: BlueprintsPageQueryModel, is_page: bool = False
    ):
        """
        获取蓝图列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 蓝图列表信息对象
        """
        blueprints_list_result = await BlueprintsDao.get_blueprints_list(query_db, query_object, is_page)

        return blueprints_list_result


    @classmethod
    async def add_blueprints_services(cls, query_db: AsyncSession, page_object: BlueprintsModel):
        """
        新增蓝图信息service

        :param query_db: orm对象
        :param page_object: 新增蓝图对象
        :return: 新增蓝图校验结果
        """
        try:
            await BlueprintsDao.add_blueprints_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_blueprints_services(cls, query_db: AsyncSession, page_object: BlueprintsModel):
        """
        编辑蓝图信息service

        :param query_db: orm对象
        :param page_object: 编辑蓝图对象
        :return: 编辑蓝图校验结果
        """
        edit_blueprints = page_object.model_dump(exclude_unset=True, exclude={})
        blueprints_info = await cls.blueprints_detail_services(query_db, page_object.id)
        if blueprints_info.id:
            try:
                await BlueprintsDao.edit_blueprints_dao(query_db, edit_blueprints)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='蓝图不存在')

    @classmethod
    async def delete_blueprints_services(cls, query_db: AsyncSession, page_object: DeleteBlueprintsModel):
        """
        删除蓝图信息service

        :param query_db: orm对象
        :param page_object: 删除蓝图对象
        :return: 删除蓝图校验结果
        """
        if page_object.ids:
            id_list = page_object.ids.split(',')
            try:
                for id in id_list:
                    await BlueprintsDao.delete_blueprints_dao(query_db, BlueprintsModel(id=id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入蓝图ID为空')

    @classmethod
    async def blueprints_detail_services(cls, query_db: AsyncSession, id: int):
        """
        获取蓝图详细信息service

        :param query_db: orm对象
        :param id: 蓝图ID
        :return: 蓝图ID对应的信息
        """
        blueprints = await BlueprintsDao.get_blueprints_detail_by_id(query_db, id=id)
        if blueprints:
            result = BlueprintsModel(**CamelCaseUtil.transform_result(blueprints))
        else:
            result = BlueprintsModel(**dict())

        return result

    @staticmethod
    async def export_blueprints_list_services(blueprints_list: List):
        """
        导出蓝图信息service

        :param blueprints_list: 蓝图信息列表
        :return: 蓝图信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'id': '蓝图ID',
            'projectId': '项目ID',
            'name': '蓝图名称',
            'description': '蓝图描述',
            'versionTag': '版本标签',
            'specDocumentId': '独立文档存储中的文档ID',
            'specSummary': '蓝图摘要信息',
            'isDraft': '是否为草稿',
            'parentBlueprintId': '父蓝图ID',
            'createdByUserId': '创建者用户ID',
            'createdAt': '创建时间',
            'updatedAt': '更新时间',
        }
        binary_data = ExcelUtil.export_list2excel(blueprints_list, mapping_dict)

        return binary_data
