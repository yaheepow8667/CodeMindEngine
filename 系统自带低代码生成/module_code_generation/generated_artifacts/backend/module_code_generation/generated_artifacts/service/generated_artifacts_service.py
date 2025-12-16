from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.entity.vo.common_vo import CrudResponseModel
from module_code_generation.generated_artifacts.dao.generated_artifacts_dao import Generated_artifactsDao
from module_code_generation.generated_artifacts.entity.vo.generated_artifacts_vo import DeleteGenerated_artifactsModel, Generated_artifactsModel, Generated_artifactsPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class Generated_artifactsService:
    """
    生成产物模块服务层
    """

    @classmethod
    async def get_generated_artifacts_list_services(
        cls, query_db: AsyncSession, query_object: Generated_artifactsPageQueryModel, is_page: bool = False
    ):
        """
        获取生成产物列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 生成产物列表信息对象
        """
        generated_artifacts_list_result = await Generated_artifactsDao.get_generated_artifacts_list(query_db, query_object, is_page)

        return generated_artifacts_list_result


    @classmethod
    async def add_generated_artifacts_services(cls, query_db: AsyncSession, page_object: Generated_artifactsModel):
        """
        新增生成产物信息service

        :param query_db: orm对象
        :param page_object: 新增生成产物对象
        :return: 新增生成产物校验结果
        """
        try:
            await Generated_artifactsDao.add_generated_artifacts_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_generated_artifacts_services(cls, query_db: AsyncSession, page_object: Generated_artifactsModel):
        """
        编辑生成产物信息service

        :param query_db: orm对象
        :param page_object: 编辑生成产物对象
        :return: 编辑生成产物校验结果
        """
        edit_generated_artifacts = page_object.model_dump(exclude_unset=True, exclude={})
        generated_artifacts_info = await cls.generated_artifacts_detail_services(query_db, page_object.id)
        if generated_artifacts_info.id:
            try:
                await Generated_artifactsDao.edit_generated_artifacts_dao(query_db, edit_generated_artifacts)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='生成产物不存在')

    @classmethod
    async def delete_generated_artifacts_services(cls, query_db: AsyncSession, page_object: DeleteGenerated_artifactsModel):
        """
        删除生成产物信息service

        :param query_db: orm对象
        :param page_object: 删除生成产物对象
        :return: 删除生成产物校验结果
        """
        if page_object.ids:
            id_list = page_object.ids.split(',')
            try:
                for id in id_list:
                    await Generated_artifactsDao.delete_generated_artifacts_dao(query_db, Generated_artifactsModel(id=id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入产物ID为空')

    @classmethod
    async def generated_artifacts_detail_services(cls, query_db: AsyncSession, id: int):
        """
        获取生成产物详细信息service

        :param query_db: orm对象
        :param id: 产物ID
        :return: 产物ID对应的信息
        """
        generated_artifacts = await Generated_artifactsDao.get_generated_artifacts_detail_by_id(query_db, id=id)
        if generated_artifacts:
            result = Generated_artifactsModel(**CamelCaseUtil.transform_result(generated_artifacts))
        else:
            result = Generated_artifactsModel(**dict())

        return result

    @staticmethod
    async def export_generated_artifacts_list_services(generated_artifacts_list: List):
        """
        导出生成产物信息service

        :param generated_artifacts_list: 生成产物信息列表
        :return: 生成产物信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'id': '产物ID',
            'jobId': '生成任务ID',
            'artifactType': '产物类型 (source_zip, qa_report, deploy_config, api_docs)',
            'artifactName': '产物名称',
            'storageType': '存储类型 (s3, oss, local)',
            'storagePath': '存储路径',
            'storageUrl': '访问URL',
            'fileSizeBytes': '文件大小 (字节)',
            'mimeType': '文件类型',
            'checksum': '校验和',
            'isCompressed': '是否压缩',
            'createdAt': '创建时间',
        }
        binary_data = ExcelUtil.export_list2excel(generated_artifacts_list, mapping_dict)

        return binary_data
