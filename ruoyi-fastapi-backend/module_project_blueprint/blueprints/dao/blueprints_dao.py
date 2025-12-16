from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_project_blueprint.blueprints.entity.do.blueprints_do import Blueprints
from module_project_blueprint.blueprints.entity.vo.blueprints_vo import BlueprintsModel, BlueprintsPageQueryModel
from utils.page_util import PageUtil


class BlueprintsDao:
    """
    蓝图模块数据库操作层
    """

    @classmethod
    async def get_blueprints_detail_by_id(cls, db: AsyncSession, id: int):
        """
        根据蓝图ID获取蓝图详细信息

        :param db: orm对象
        :param id: 蓝图ID
        :return: 蓝图信息对象
        """
        blueprints_info = (
            (
                await db.execute(
                    select(Blueprints)
                    .where(
                        Blueprints.id == id
                    )
                )
            )
            .scalars()
            .first()
        )

        return blueprints_info

    @classmethod
    async def get_blueprints_detail_by_info(cls, db: AsyncSession, blueprints: BlueprintsModel):
        """
        根据蓝图参数获取蓝图信息

        :param db: orm对象
        :param blueprints: 蓝图参数对象
        :return: 蓝图信息对象
        """
        blueprints_info = (
            (
                await db.execute(
                    select(Blueprints).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return blueprints_info

    @classmethod
    async def get_blueprints_list(cls, db: AsyncSession, query_object: BlueprintsPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取蓝图列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 蓝图列表信息对象
        """
        query = (
            select(Blueprints)
            .where(
                Blueprints.project_id == query_object.project_id if query_object.project_id else True,
                Blueprints.name.like(f'%{query_object.name}%') if query_object.name else True,
                Blueprints.description == query_object.description if query_object.description else True,
                Blueprints.version_tag == query_object.version_tag if query_object.version_tag else True,
                Blueprints.spec_document_id == query_object.spec_document_id if query_object.spec_document_id else True,
                Blueprints.spec_summary == query_object.spec_summary if query_object.spec_summary else True,
                Blueprints.is_draft == query_object.is_draft if query_object.is_draft else True,
                Blueprints.parent_blueprint_id == query_object.parent_blueprint_id if query_object.parent_blueprint_id else True,
                Blueprints.created_by_user_id == query_object.created_by_user_id if query_object.created_by_user_id else True,
                Blueprints.created_at == query_object.created_at if query_object.created_at else True,
                Blueprints.updated_at == query_object.updated_at if query_object.updated_at else True,
            )
            .order_by(Blueprints.id)
            .distinct()
        )
        blueprints_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return blueprints_list

    @classmethod
    async def add_blueprints_dao(cls, db: AsyncSession, blueprints: BlueprintsModel):
        """
        新增蓝图数据库操作

        :param db: orm对象
        :param blueprints: 蓝图对象
        :return:
        """
        db_blueprints = Blueprints(**blueprints.model_dump(exclude={}))
        db.add(db_blueprints)
        await db.flush()

        return db_blueprints

    @classmethod
    async def edit_blueprints_dao(cls, db: AsyncSession, blueprints: dict):
        """
        编辑蓝图数据库操作

        :param db: orm对象
        :param blueprints: 需要更新的蓝图字典
        :return:
        """
        await db.execute(update(Blueprints), [blueprints])

    @classmethod
    async def delete_blueprints_dao(cls, db: AsyncSession, blueprints: BlueprintsModel):
        """
        删除蓝图数据库操作

        :param db: orm对象
        :param blueprints: 蓝图对象
        :return:
        """
        await db.execute(delete(Blueprints).where(Blueprints.id.in_([blueprints.id])))

