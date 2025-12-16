from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.entity.vo.common_vo import CrudResponseModel
from module_team_collaboration.team_members.dao.members_dao import MembersDao
from module_team_collaboration.team_members.entity.vo.members_vo import DeleteMembersModel, MembersModel, MembersPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class MembersService:
    """
    团队成员模块服务层
    """

    @classmethod
    async def get_members_list_services(
        cls, query_db: AsyncSession, query_object: MembersPageQueryModel, is_page: bool = False
    ):
        """
        获取团队成员列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 团队成员列表信息对象
        """
        members_list_result = await MembersDao.get_members_list(query_db, query_object, is_page)

        return members_list_result


    @classmethod
    async def add_members_services(cls, query_db: AsyncSession, page_object: MembersModel):
        """
        新增团队成员信息service

        :param query_db: orm对象
        :param page_object: 新增团队成员对象
        :return: 新增团队成员校验结果
        """
        try:
            await MembersDao.add_members_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_members_services(cls, query_db: AsyncSession, page_object: MembersModel):
        """
        编辑团队成员信息service

        :param query_db: orm对象
        :param page_object: 编辑团队成员对象
        :return: 编辑团队成员校验结果
        """
        edit_members = page_object.model_dump(exclude_unset=True, exclude={})
        members_info = await cls.members_detail_services(query_db, page_object.id)
        if members_info.id:
            try:
                await MembersDao.edit_members_dao(query_db, edit_members)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='团队成员不存在')

    @classmethod
    async def delete_members_services(cls, query_db: AsyncSession, page_object: DeleteMembersModel):
        """
        删除团队成员信息service

        :param query_db: orm对象
        :param page_object: 删除团队成员对象
        :return: 删除团队成员校验结果
        """
        if page_object.ids:
            id_list = page_object.ids.split(',')
            try:
                for id in id_list:
                    await MembersDao.delete_members_dao(query_db, MembersModel(id=id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入为空')

    @classmethod
    async def members_detail_services(cls, query_db: AsyncSession, id: int):
        """
        获取团队成员详细信息service

        :param query_db: orm对象
        :param id: 
        :return: 对应的信息
        """
        members = await MembersDao.get_members_detail_by_id(query_db, id=id)
        if members:
            result = MembersModel(**CamelCaseUtil.transform_result(members))
        else:
            result = MembersModel(**dict())

        return result

    @staticmethod
    async def export_members_list_services(members_list: List):
        """
        导出团队成员信息service

        :param members_list: 团队成员信息列表
        :return: 团队成员信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'id': '',
            'teamId': '团队ID',
            'userId': '用户ID',
            'role': '成员角色 (owner, admin, member, viewer)',
            'joinedAt': '加入时间',
            'invitedByUserId': '邀请者用户ID',
            'invitedAt': '邀请时间',
            'createdAt': '创建时间',
        }
        binary_data = ExcelUtil.export_list2excel(members_list, mapping_dict)

        return binary_data
