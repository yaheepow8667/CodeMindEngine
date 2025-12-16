from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_team_collaboration.invitations.entity.do.invitations_do import Invitations
from module_team_collaboration.invitations.entity.vo.invitations_vo import InvitationsModel, InvitationsPageQueryModel
from utils.page_util import PageUtil


class InvitationsDao:
    """
    邀请模块数据库操作层
    """

    @classmethod
    async def get_invitations_detail_by_id(cls, db: AsyncSession, id: int):
        """
        根据获取邀请详细信息

        :param db: orm对象
        :param id: 
        :return: 邀请信息对象
        """
        invitations_info = (
            (
                await db.execute(
                    select(Invitations)
                    .where(
                        Invitations.id == id
                    )
                )
            )
            .scalars()
            .first()
        )

        return invitations_info

    @classmethod
    async def get_invitations_detail_by_info(cls, db: AsyncSession, invitations: InvitationsModel):
        """
        根据邀请参数获取邀请信息

        :param db: orm对象
        :param invitations: 邀请参数对象
        :return: 邀请信息对象
        """
        invitations_info = (
            (
                await db.execute(
                    select(Invitations).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return invitations_info

    @classmethod
    async def get_invitations_list(cls, db: AsyncSession, query_object: InvitationsPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取邀请列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 邀请列表信息对象
        """
        query = (
            select(Invitations)
            .where(
                Invitations.team_id == query_object.team_id if query_object.team_id else True,
                Invitations.email == query_object.email if query_object.email else True,
                Invitations.token == query_object.token if query_object.token else True,
                Invitations.role == query_object.role if query_object.role else True,
                Invitations.invited_by_user_id == query_object.invited_by_user_id if query_object.invited_by_user_id else True,
                Invitations.expires_at == query_object.expires_at if query_object.expires_at else True,
                Invitations.accepted_at == query_object.accepted_at if query_object.accepted_at else True,
                Invitations.created_at == query_object.created_at if query_object.created_at else True,
            )
            .order_by(Invitations.id)
            .distinct()
        )
        invitations_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return invitations_list

    @classmethod
    async def add_invitations_dao(cls, db: AsyncSession, invitations: InvitationsModel):
        """
        新增邀请数据库操作

        :param db: orm对象
        :param invitations: 邀请对象
        :return:
        """
        db_invitations = Invitations(**invitations.model_dump(exclude={}))
        db.add(db_invitations)
        await db.flush()

        return db_invitations

    @classmethod
    async def edit_invitations_dao(cls, db: AsyncSession, invitations: dict):
        """
        编辑邀请数据库操作

        :param db: orm对象
        :param invitations: 需要更新的邀请字典
        :return:
        """
        await db.execute(update(Invitations), [invitations])

    @classmethod
    async def delete_invitations_dao(cls, db: AsyncSession, invitations: InvitationsModel):
        """
        删除邀请数据库操作

        :param db: orm对象
        :param invitations: 邀请对象
        :return:
        """
        await db.execute(delete(Invitations).where(Invitations.id.in_([invitations.id])))

