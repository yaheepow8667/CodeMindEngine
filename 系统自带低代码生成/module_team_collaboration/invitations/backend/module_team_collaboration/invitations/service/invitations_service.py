from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.entity.vo.common_vo import CrudResponseModel
from module_team_collaboration.invitations.dao.invitations_dao import InvitationsDao
from module_team_collaboration.invitations.entity.vo.invitations_vo import DeleteInvitationsModel, InvitationsModel, InvitationsPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class InvitationsService:
    """
    邀请模块服务层
    """

    @classmethod
    async def get_invitations_list_services(
        cls, query_db: AsyncSession, query_object: InvitationsPageQueryModel, is_page: bool = False
    ):
        """
        获取邀请列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 邀请列表信息对象
        """
        invitations_list_result = await InvitationsDao.get_invitations_list(query_db, query_object, is_page)

        return invitations_list_result


    @classmethod
    async def add_invitations_services(cls, query_db: AsyncSession, page_object: InvitationsModel):
        """
        新增邀请信息service

        :param query_db: orm对象
        :param page_object: 新增邀请对象
        :return: 新增邀请校验结果
        """
        try:
            await InvitationsDao.add_invitations_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_invitations_services(cls, query_db: AsyncSession, page_object: InvitationsModel):
        """
        编辑邀请信息service

        :param query_db: orm对象
        :param page_object: 编辑邀请对象
        :return: 编辑邀请校验结果
        """
        edit_invitations = page_object.model_dump(exclude_unset=True, exclude={})
        invitations_info = await cls.invitations_detail_services(query_db, page_object.id)
        if invitations_info.id:
            try:
                await InvitationsDao.edit_invitations_dao(query_db, edit_invitations)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='邀请不存在')

    @classmethod
    async def delete_invitations_services(cls, query_db: AsyncSession, page_object: DeleteInvitationsModel):
        """
        删除邀请信息service

        :param query_db: orm对象
        :param page_object: 删除邀请对象
        :return: 删除邀请校验结果
        """
        if page_object.ids:
            id_list = page_object.ids.split(',')
            try:
                for id in id_list:
                    await InvitationsDao.delete_invitations_dao(query_db, InvitationsModel(id=id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入为空')

    @classmethod
    async def invitations_detail_services(cls, query_db: AsyncSession, id: int):
        """
        获取邀请详细信息service

        :param query_db: orm对象
        :param id: 
        :return: 对应的信息
        """
        invitations = await InvitationsDao.get_invitations_detail_by_id(query_db, id=id)
        if invitations:
            result = InvitationsModel(**CamelCaseUtil.transform_result(invitations))
        else:
            result = InvitationsModel(**dict())

        return result

    @staticmethod
    async def export_invitations_list_services(invitations_list: List):
        """
        导出邀请信息service

        :param invitations_list: 邀请信息列表
        :return: 邀请信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'id': '',
            'teamId': '团队ID',
            'email': '邀请邮箱',
            'token': '邀请令牌',
            'role': '邀请角色',
            'invitedByUserId': '邀请者用户ID',
            'expiresAt': '邀请过期时间',
            'acceptedAt': '接受时间',
            'createdAt': '创建时间',
        }
        binary_data = ExcelUtil.export_list2excel(invitations_list, mapping_dict)

        return binary_data
