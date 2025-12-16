from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_project_blueprint.projects.entity.do.projects_do import Projects
from module_project_blueprint.projects.entity.vo.projects_vo import ProjectsModel, ProjectsPageQueryModel
from utils.page_util import PageUtil


class ProjectsDao:
    """
    项目模块数据库操作层
    """

    @classmethod
    async def get_projects_detail_by_id(cls, db: AsyncSession, id: int):
        """
        根据项目ID获取项目详细信息

        :param db: orm对象
        :param id: 项目ID
        :return: 项目信息对象
        """
        projects_info = (
            (
                await db.execute(
                    select(Projects)
                    .where(
                        Projects.id == id
                    )
                )
            )
            .scalars()
            .first()
        )

        return projects_info

    @classmethod
    async def get_projects_detail_by_info(cls, db: AsyncSession, projects: ProjectsModel):
        """
        根据项目参数获取项目信息

        :param db: orm对象
        :param projects: 项目参数对象
        :return: 项目信息对象
        """
        projects_info = (
            (
                await db.execute(
                    select(Projects).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return projects_info

    @classmethod
    async def get_projects_list(cls, db: AsyncSession, query_object: ProjectsPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取项目列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 项目列表信息对象
        """
        query = (
            select(Projects)
            .where(
                Projects.team_id == query_object.team_id if query_object.team_id else True,
                Projects.name.like(f'%{query_object.name}%') if query_object.name else True,
                Projects.slug == query_object.slug if query_object.slug else True,
                Projects.description == query_object.description if query_object.description else True,
                Projects.tech_stack == query_object.tech_stack if query_object.tech_stack else True,
                Projects.status == query_object.status if query_object.status else True,
                Projects.is_public == query_object.is_public if query_object.is_public else True,
                Projects.storage_quota_mb == query_object.storage_quota_mb if query_object.storage_quota_mb else True,
                Projects.created_by_user_id == query_object.created_by_user_id if query_object.created_by_user_id else True,
                Projects.created_at == query_object.created_at if query_object.created_at else True,
                Projects.updated_at == query_object.updated_at if query_object.updated_at else True,
            )
            .order_by(Projects.id)
            .distinct()
        )
        projects_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return projects_list

    @classmethod
    async def add_projects_dao(cls, db: AsyncSession, projects: ProjectsModel):
        """
        新增项目数据库操作

        :param db: orm对象
        :param projects: 项目对象
        :return:
        """
        db_projects = Projects(**projects.model_dump(exclude={}))
        db.add(db_projects)
        await db.flush()

        return db_projects

    @classmethod
    async def edit_projects_dao(cls, db: AsyncSession, projects: dict):
        """
        编辑项目数据库操作

        :param db: orm对象
        :param projects: 需要更新的项目字典
        :return:
        """
        await db.execute(update(Projects), [projects])

    @classmethod
    async def delete_projects_dao(cls, db: AsyncSession, projects: ProjectsModel):
        """
        删除项目数据库操作

        :param db: orm对象
        :param projects: 项目对象
        :return:
        """
        await db.execute(delete(Projects).where(Projects.id.in_([projects.id])))

