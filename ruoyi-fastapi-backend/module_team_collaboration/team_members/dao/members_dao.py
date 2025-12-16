from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_team_collaboration.team_members.entity.do.members_do import TeamMembers
from module_team_collaboration.team_members.entity.vo.members_vo import MembersModel, MembersPageQueryModel
from utils.page_util import PageUtil


class MembersDao:
    """
    团队成员模块数据库操作层
    """

    @classmethod
    async def get_members_detail_by_id(cls, db: AsyncSession, id: int):
        """
        根据获取团队成员详细信息

        :param db: orm对象
        :param id: 
        :return: 团队成员信息对象
        """
        members_info = (
            (
                await db.execute(
                    select(TeamMembers)
                    .where(
                        TeamMembers.id == id
                    )
                )
            )
            .scalars()
            .first()
        )

        return members_info

    @classmethod
    async def get_members_detail_by_info(cls, db: AsyncSession, members: MembersModel):
        """
        根据团队成员参数获取团队成员信息

        :param db: orm对象
        :param members: 团队成员参数对象
        :return: 团队成员信息对象
        """
        members_info = (
            (
                await db.execute(
                    select(TeamMembers).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return members_info

    @classmethod
    async def get_members_list(cls, db: AsyncSession, query_object: MembersPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取团队成员列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 团队成员列表信息对象
        """
        query = (
            select(TeamMembers)
            .where(
                TeamMembers.team_id == query_object.team_id if query_object.team_id else True,
                TeamMembers.user_id == query_object.user_id if query_object.user_id else True,
                TeamMembers.role == query_object.role if query_object.role else True,
                TeamMembers.joined_at == query_object.joined_at if query_object.joined_at else True,
                TeamMembers.invited_by_user_id == query_object.invited_by_user_id if query_object.invited_by_user_id else True,
                TeamMembers.invited_at == query_object.invited_at if query_object.invited_at else True,
                TeamMembers.created_at == query_object.created_at if query_object.created_at else True,
            )
            .order_by(TeamMembers.id)
            .distinct()
        )
        members_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return members_list

    @classmethod
    async def add_members_dao(cls, db: AsyncSession, members: MembersModel):
        """
        新增团队成员数据库操作

        :param db: orm对象
        :param members: 团队成员对象
        :return:
        """
        db_members = TeamMembers(**members.model_dump(exclude={}))
        db.add(db_members)
        await db.flush()

        return db_members

    @classmethod
    async def edit_members_dao(cls, db: AsyncSession, members: dict):
        """
        编辑团队成员数据库操作

        :param db: orm对象
        :param members: 需要更新的团队成员字典
        :return:
        """
        await db.execute(update(TeamMembers), [members])

    @classmethod
    async def delete_members_dao(cls, db: AsyncSession, members: MembersModel):
        """
        删除团队成员数据库操作

        :param db: orm对象
        :param members: 团队成员对象
        :return:
        """
        await db.execute(delete(TeamMembers).where(TeamMembers.id.in_([members.id])))

