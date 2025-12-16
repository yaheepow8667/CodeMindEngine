from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_team_collaboration.teams.entity.do.teams_do import Teams
from module_team_collaboration.teams.entity.vo.teams_vo import TeamsModel, TeamsPageQueryModel
from utils.page_util import PageUtil


class TeamsDao:
    """
    团队模块数据库操作层
    """

    @classmethod
    async def get_teams_detail_by_id(cls, db: AsyncSession, id: int):
        """
        根据获取团队详细信息

        :param db: orm对象
        :param id: 
        :return: 团队信息对象
        """
        teams_info = (
            (
                await db.execute(
                    select(Teams)
                    .where(
                        Teams.id == id
                    )
                )
            )
            .scalars()
            .first()
        )

        return teams_info

    @classmethod
    async def get_teams_detail_by_info(cls, db: AsyncSession, teams: TeamsModel):
        """
        根据团队参数获取团队信息

        :param db: orm对象
        :param teams: 团队参数对象
        :return: 团队信息对象
        """
        teams_info = (
            (
                await db.execute(
                    select(Teams).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return teams_info

    @classmethod
    async def get_teams_list(cls, db: AsyncSession, query_object: TeamsPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取团队列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 团队列表信息对象
        """
        query = (
            select(Teams)
            .where(
                Teams.name.like(f'%{query_object.name}%') if query_object.name else True,
                Teams.slug == query_object.slug if query_object.slug else True,
                Teams.description == query_object.description if query_object.description else True,
                Teams.logo_url == query_object.logo_url if query_object.logo_url else True,
                Teams.subscription_plan == query_object.subscription_plan if query_object.subscription_plan else True,
                Teams.subscription_status == query_object.subscription_status if query_object.subscription_status else True,
                Teams.subscription_ends_at == query_object.subscription_ends_at if query_object.subscription_ends_at else True,
                Teams.created_by_user_id == query_object.created_by_user_id if query_object.created_by_user_id else True,
                Teams.created_at == query_object.created_at if query_object.created_at else True,
                Teams.updated_at == query_object.updated_at if query_object.updated_at else True,
            )
            .order_by(Teams.id)
            .distinct()
        )
        teams_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return teams_list

    @classmethod
    async def add_teams_dao(cls, db: AsyncSession, teams: TeamsModel):
        """
        新增团队数据库操作

        :param db: orm对象
        :param teams: 团队对象
        :return:
        """
        db_teams = Teams(**teams.model_dump(exclude={}))
        db.add(db_teams)
        await db.flush()

        return db_teams

    @classmethod
    async def edit_teams_dao(cls, db: AsyncSession, teams: dict):
        """
        编辑团队数据库操作

        :param db: orm对象
        :param teams: 需要更新的团队字典
        :return:
        """
        await db.execute(update(Teams), [teams])

    @classmethod
    async def delete_teams_dao(cls, db: AsyncSession, teams: TeamsModel):
        """
        删除团队数据库操作

        :param db: orm对象
        :param teams: 团队对象
        :return:
        """
        await db.execute(delete(Teams).where(Teams.id.in_([teams.id])))

