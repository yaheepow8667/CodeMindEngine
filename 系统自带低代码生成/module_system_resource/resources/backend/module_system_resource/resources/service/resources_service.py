from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.entity.vo.common_vo import CrudResponseModel
from module_system_resource.resources.dao.resources_dao import ResourcesDao
from module_system_resource.resources.entity.vo.resources_vo import DeleteResourcesModel, ResourcesModel, ResourcesPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class ResourcesService:
    """
    文件资源模块服务层
    """

    @classmethod
    async def get_resources_list_services(
        cls, query_db: AsyncSession, query_object: ResourcesPageQueryModel, is_page: bool = False
    ):
        """
        获取文件资源列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 文件资源列表信息对象
        """
        resources_list_result = await ResourcesDao.get_resources_list(query_db, query_object, is_page)

        return resources_list_result


    @classmethod
    async def add_resources_services(cls, query_db: AsyncSession, page_object: ResourcesModel):
        """
        新增文件资源信息service

        :param query_db: orm对象
        :param page_object: 新增文件资源对象
        :return: 新增文件资源校验结果
        """
        try:
            await ResourcesDao.add_resources_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_resources_services(cls, query_db: AsyncSession, page_object: ResourcesModel):
        """
        编辑文件资源信息service

        :param query_db: orm对象
        :param page_object: 编辑文件资源对象
        :return: 编辑文件资源校验结果
        """
        edit_resources = page_object.model_dump(exclude_unset=True, exclude={})
        resources_info = await cls.resources_detail_services(query_db, page_object.id)
        if resources_info.id:
            try:
                await ResourcesDao.edit_resources_dao(query_db, edit_resources)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='文件资源不存在')

    @classmethod
    async def delete_resources_services(cls, query_db: AsyncSession, page_object: DeleteResourcesModel):
        """
        删除文件资源信息service

        :param query_db: orm对象
        :param page_object: 删除文件资源对象
        :return: 删除文件资源校验结果
        """
        if page_object.ids:
            id_list = page_object.ids.split(',')
            try:
                for id in id_list:
                    await ResourcesDao.delete_resources_dao(query_db, ResourcesModel(id=id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入文件资源ID为空')

    @classmethod
    async def resources_detail_services(cls, query_db: AsyncSession, id: int):
        """
        获取文件资源详细信息service

        :param query_db: orm对象
        :param id: 文件资源ID
        :return: 文件资源ID对应的信息
        """
        resources = await ResourcesDao.get_resources_detail_by_id(query_db, id=id)
        if resources:
            result = ResourcesModel(**CamelCaseUtil.transform_result(resources))
        else:
            result = ResourcesModel(**dict())

        return result

    @staticmethod
    async def export_resources_list_services(resources_list: List):
        """
        导出文件资源信息service

        :param resources_list: 文件资源信息列表
        :return: 文件资源信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'id': '文件资源ID',
            'projectId': '项目ID',
            'name': '资源名称',
            'resourceType': '资源类型 (image, file, json, sql)',
            'storagePath': '存储路径',
            'fileSizeBytes': '文件大小 (字节)',
            'uploadedByUserId': '上传者用户ID',
            'createdAt': '创建时间',
        }
        binary_data = ExcelUtil.export_list2excel(resources_list, mapping_dict)

        return binary_data
