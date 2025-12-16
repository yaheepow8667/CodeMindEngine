from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.entity.vo.common_vo import CrudResponseModel
from module_system_resource.api_tokens.dao.api_tokens_dao import Api_tokensDao
from module_system_resource.api_tokens.entity.vo.api_tokens_vo import DeleteApi_tokensModel, Api_tokensModel, Api_tokensPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class Api_tokensService:
    """
    API访问令牌模块服务层
    """

    @classmethod
    async def get_api_tokens_list_services(
        cls, query_db: AsyncSession, query_object: Api_tokensPageQueryModel, is_page: bool = False
    ):
        """
        获取API访问令牌列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: API访问令牌列表信息对象
        """
        api_tokens_list_result = await Api_tokensDao.get_api_tokens_list(query_db, query_object, is_page)

        return api_tokens_list_result


    @classmethod
    async def add_api_tokens_services(cls, query_db: AsyncSession, page_object: Api_tokensModel):
        """
        新增API访问令牌信息service

        :param query_db: orm对象
        :param page_object: 新增API访问令牌对象
        :return: 新增API访问令牌校验结果
        """
        try:
            await Api_tokensDao.add_api_tokens_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_api_tokens_services(cls, query_db: AsyncSession, page_object: Api_tokensModel):
        """
        编辑API访问令牌信息service

        :param query_db: orm对象
        :param page_object: 编辑API访问令牌对象
        :return: 编辑API访问令牌校验结果
        """
        edit_api_tokens = page_object.model_dump(exclude_unset=True, exclude={})
        api_tokens_info = await cls.api_tokens_detail_services(query_db, page_object.id)
        if api_tokens_info.id:
            try:
                await Api_tokensDao.edit_api_tokens_dao(query_db, edit_api_tokens)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='API访问令牌不存在')

    @classmethod
    async def delete_api_tokens_services(cls, query_db: AsyncSession, page_object: DeleteApi_tokensModel):
        """
        删除API访问令牌信息service

        :param query_db: orm对象
        :param page_object: 删除API访问令牌对象
        :return: 删除API访问令牌校验结果
        """
        if page_object.ids:
            id_list = page_object.ids.split(',')
            try:
                for id in id_list:
                    await Api_tokensDao.delete_api_tokens_dao(query_db, Api_tokensModel(id=id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入访问令牌ID为空')

    @classmethod
    async def api_tokens_detail_services(cls, query_db: AsyncSession, id: int):
        """
        获取API访问令牌详细信息service

        :param query_db: orm对象
        :param id: 访问令牌ID
        :return: 访问令牌ID对应的信息
        """
        api_tokens = await Api_tokensDao.get_api_tokens_detail_by_id(query_db, id=id)
        if api_tokens:
            result = Api_tokensModel(**CamelCaseUtil.transform_result(api_tokens))
        else:
            result = Api_tokensModel(**dict())

        return result

    @staticmethod
    async def export_api_tokens_list_services(api_tokens_list: List):
        """
        导出API访问令牌信息service

        :param api_tokens_list: API访问令牌信息列表
        :return: API访问令牌信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'id': '访问令牌ID',
            'userId': '用户ID',
            'teamId': '团队ID',
            'name': '令牌名称',
            'tokenHash': '令牌哈希值',
            'tokenPrefix': '令牌前缀',
            'scopes': '权限范围',
            'expiresAt': '过期时间',
            'lastUsedAt': '最后使用时间',
            'isActive': '是否启用',
            'createdAt': '创建时间',
        }
        binary_data = ExcelUtil.export_list2excel(api_tokens_list, mapping_dict)

        return binary_data
