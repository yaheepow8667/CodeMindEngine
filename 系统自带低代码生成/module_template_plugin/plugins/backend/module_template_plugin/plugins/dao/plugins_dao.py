from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_template_plugin.plugins.entity.do.plugins_do import Plugins
from module_template_plugin.plugins.entity.vo.plugins_vo import PluginsModel, PluginsPageQueryModel
from utils.page_util import PageUtil


class PluginsDao:
    """
    插件模块数据库操作层
    """

    @classmethod
    async def get_plugins_detail_by_id(cls, db: AsyncSession, id: int):
        """
        根据插件ID获取插件详细信息

        :param db: orm对象
        :param id: 插件ID
        :return: 插件信息对象
        """
        plugins_info = (
            (
                await db.execute(
                    select(Plugins)
                    .where(
                        Plugins.id == id
                    )
                )
            )
            .scalars()
            .first()
        )

        return plugins_info

    @classmethod
    async def get_plugins_detail_by_info(cls, db: AsyncSession, plugins: PluginsModel):
        """
        根据插件参数获取插件信息

        :param db: orm对象
        :param plugins: 插件参数对象
        :return: 插件信息对象
        """
        plugins_info = (
            (
                await db.execute(
                    select(Plugins).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return plugins_info

    @classmethod
    async def get_plugins_list(cls, db: AsyncSession, query_object: PluginsPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取插件列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 插件列表信息对象
        """
        query = (
            select(Plugins)
            .where(
                Plugins.name.like(f'%{query_object.name}%') if query_object.name else True,
                Plugins.plugin_type == query_object.plugin_type if query_object.plugin_type else True,
                Plugins.target_framework == query_object.target_framework if query_object.target_framework else True,
                Plugins.version == query_object.version if query_object.version else True,
                Plugins.author_user_id == query_object.author_user_id if query_object.author_user_id else True,
                Plugins.is_approved == query_object.is_approved if query_object.is_approved else True,
                Plugins.install_count == query_object.install_count if query_object.install_count else True,
                Plugins.config_schema == query_object.config_schema if query_object.config_schema else True,
                Plugins.created_at == query_object.created_at if query_object.created_at else True,
                Plugins.updated_at == query_object.updated_at if query_object.updated_at else True,
            )
            .order_by(Plugins.id)
            .distinct()
        )
        plugins_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return plugins_list

    @classmethod
    async def add_plugins_dao(cls, db: AsyncSession, plugins: PluginsModel):
        """
        新增插件数据库操作

        :param db: orm对象
        :param plugins: 插件对象
        :return:
        """
        db_plugins = Plugins(**plugins.model_dump(exclude={}))
        db.add(db_plugins)
        await db.flush()

        return db_plugins

    @classmethod
    async def edit_plugins_dao(cls, db: AsyncSession, plugins: dict):
        """
        编辑插件数据库操作

        :param db: orm对象
        :param plugins: 需要更新的插件字典
        :return:
        """
        await db.execute(update(Plugins), [plugins])

    @classmethod
    async def delete_plugins_dao(cls, db: AsyncSession, plugins: PluginsModel):
        """
        删除插件数据库操作

        :param db: orm对象
        :param plugins: 插件对象
        :return:
        """
        await db.execute(delete(Plugins).where(Plugins.id.in_([plugins.id])))

