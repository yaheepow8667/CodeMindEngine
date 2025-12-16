from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_template_plugin.templates.entity.do.templates_do import Templates
from module_template_plugin.templates.entity.vo.templates_vo import TemplatesModel, TemplatesPageQueryModel
from utils.page_util import PageUtil


class TemplatesDao:
    """
    模板模块数据库操作层
    """

    @classmethod
    async def get_templates_detail_by_id(cls, db: AsyncSession, id: int):
        """
        根据模板ID获取模板详细信息

        :param db: orm对象
        :param id: 模板ID
        :return: 模板信息对象
        """
        templates_info = (
            (
                await db.execute(
                    select(Templates)
                    .where(
                        Templates.id == id
                    )
                )
            )
            .scalars()
            .first()
        )

        return templates_info

    @classmethod
    async def get_templates_detail_by_info(cls, db: AsyncSession, templates: TemplatesModel):
        """
        根据模板参数获取模板信息

        :param db: orm对象
        :param templates: 模板参数对象
        :return: 模板信息对象
        """
        templates_info = (
            (
                await db.execute(
                    select(Templates).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return templates_info

    @classmethod
    async def get_templates_list(cls, db: AsyncSession, query_object: TemplatesPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取模板列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 模板列表信息对象
        """
        query = (
            select(Templates)
            .where(
                Templates.name.like(f'%{query_object.name}%') if query_object.name else True,
                Templates.slug == query_object.slug if query_object.slug else True,
                Templates.description == query_object.description if query_object.description else True,
                Templates.category == query_object.category if query_object.category else True,
                Templates.target_framework == query_object.target_framework if query_object.target_framework else True,
                Templates.complexity_level == query_object.complexity_level if query_object.complexity_level else True,
                Templates.is_official == query_object.is_official if query_object.is_official else True,
                Templates.is_public == query_object.is_public if query_object.is_public else True,
                Templates.author_user_id == query_object.author_user_id if query_object.author_user_id else True,
                Templates.download_count == query_object.download_count if query_object.download_count else True,
                Templates.rating == query_object.rating if query_object.rating else True,
                Templates.version == query_object.version if query_object.version else True,
                Templates.tags == query_object.tags if query_object.tags else True,
                Templates.created_at == query_object.created_at if query_object.created_at else True,
                Templates.updated_at == query_object.updated_at if query_object.updated_at else True,
            )
            .order_by(Templates.id)
            .distinct()
        )
        templates_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return templates_list

    @classmethod
    async def add_templates_dao(cls, db: AsyncSession, templates: TemplatesModel):
        """
        新增模板数据库操作

        :param db: orm对象
        :param templates: 模板对象
        :return:
        """
        db_templates = Templates(**templates.model_dump(exclude={}))
        db.add(db_templates)
        await db.flush()

        return db_templates

    @classmethod
    async def edit_templates_dao(cls, db: AsyncSession, templates: dict):
        """
        编辑模板数据库操作

        :param db: orm对象
        :param templates: 需要更新的模板字典
        :return:
        """
        await db.execute(update(Templates), [templates])

    @classmethod
    async def delete_templates_dao(cls, db: AsyncSession, templates: TemplatesModel):
        """
        删除模板数据库操作

        :param db: orm对象
        :param templates: 模板对象
        :return:
        """
        await db.execute(delete(Templates).where(Templates.id.in_([templates.id])))

