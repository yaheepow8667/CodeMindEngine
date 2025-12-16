from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_template_plugin.template_versions.entity.do.template_versions_do import TemplateVersions
from module_template_plugin.template_versions.entity.vo.template_versions_vo import Template_versionsModel, Template_versionsPageQueryModel
from utils.page_util import PageUtil


class Template_versionsDao:
    """
    模板版本模块数据库操作层
    """

    @classmethod
    async def get_template_versions_detail_by_id(cls, db: AsyncSession, id: int):
        """
        根据模板版本ID获取模板版本详细信息

        :param db: orm对象
        :param id: 模板版本ID
        :return: 模板版本信息对象
        """
        template_versions_info = (
            (
                await db.execute(
                    select(TemplateVersions)
                    .where(
                        TemplateVersions.id == id
                    )
                )
            )
            .scalars()
            .first()
        )

        return template_versions_info

    @classmethod
    async def get_template_versions_detail_by_info(cls, db: AsyncSession, template_versions: Template_versionsModel):
        """
        根据模板版本参数获取模板版本信息

        :param db: orm对象
        :param template_versions: 模板版本参数对象
        :return: 模板版本信息对象
        """
        template_versions_info = (
            (
                await db.execute(
                    select(TemplateVersions).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return template_versions_info

    @classmethod
    async def get_template_versions_list(cls, db: AsyncSession, query_object: Template_versionsPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取模板版本列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 模板版本列表信息对象
        """
        query = (
            select(TemplateVersions)
            .where(
                TemplateVersions.template_id == query_object.template_id if query_object.template_id else True,
                TemplateVersions.version == query_object.version if query_object.version else True,
                TemplateVersions.changelog == query_object.changelog if query_object.changelog else True,
                TemplateVersions.template_content == query_object.template_content if query_object.template_content else True,
                TemplateVersions.example_blueprint == query_object.example_blueprint if query_object.example_blueprint else True,
                TemplateVersions.is_active == query_object.is_active if query_object.is_active else True,
                TemplateVersions.published_at == query_object.published_at if query_object.published_at else True,
                TemplateVersions.published_by_user_id == query_object.published_by_user_id if query_object.published_by_user_id else True,
                TemplateVersions.created_at == query_object.created_at if query_object.created_at else True,
            )
            .order_by(TemplateVersions.id)
            .distinct()
        )
        template_versions_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return template_versions_list

    @classmethod
    async def add_template_versions_dao(cls, db: AsyncSession, template_versions: Template_versionsModel):
        """
        新增模板版本数据库操作

        :param db: orm对象
        :param template_versions: 模板版本对象
        :return:
        """
        db_template_versions = TemplateVersions(**template_versions.model_dump(exclude={}))
        db.add(db_template_versions)
        await db.flush()

        return db_template_versions

    @classmethod
    async def edit_template_versions_dao(cls, db: AsyncSession, template_versions: dict):
        """
        编辑模板版本数据库操作

        :param db: orm对象
        :param template_versions: 需要更新的模板版本字典
        :return:
        """
        await db.execute(update(TemplateVersions), [template_versions])

    @classmethod
    async def delete_template_versions_dao(cls, db: AsyncSession, template_versions: Template_versionsModel):
        """
        删除模板版本数据库操作

        :param db: orm对象
        :param template_versions: 模板版本对象
        :return:
        """
        await db.execute(delete(TemplateVersions).where(TemplateVersions.id.in_([template_versions.id])))

