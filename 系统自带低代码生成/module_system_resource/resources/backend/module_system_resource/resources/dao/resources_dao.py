from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_system_resource.resources.entity.do.resources_do import Resources
from module_system_resource.resources.entity.vo.resources_vo import ResourcesModel, ResourcesPageQueryModel
from utils.page_util import PageUtil


class ResourcesDao:
    """
    文件资源模块数据库操作层
    """

    @classmethod
    async def get_resources_detail_by_id(cls, db: AsyncSession, id: int):
        """
        根据文件资源ID获取文件资源详细信息

        :param db: orm对象
        :param id: 文件资源ID
        :return: 文件资源信息对象
        """
        resources_info = (
            (
                await db.execute(
                    select(Resources)
                    .where(
                        Resources.id == id
                    )
                )
            )
            .scalars()
            .first()
        )

        return resources_info

    @classmethod
    async def get_resources_detail_by_info(cls, db: AsyncSession, resources: ResourcesModel):
        """
        根据文件资源参数获取文件资源信息

        :param db: orm对象
        :param resources: 文件资源参数对象
        :return: 文件资源信息对象
        """
        resources_info = (
            (
                await db.execute(
                    select(Resources).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return resources_info

    @classmethod
    async def get_resources_list(cls, db: AsyncSession, query_object: ResourcesPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取文件资源列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 文件资源列表信息对象
        """
        query = (
            select(Resources)
            .where(
                Resources.project_id == query_object.project_id if query_object.project_id else True,
                Resources.name.like(f'%{query_object.name}%') if query_object.name else True,
                Resources.resource_type == query_object.resource_type if query_object.resource_type else True,
                Resources.storage_path == query_object.storage_path if query_object.storage_path else True,
                Resources.file_size_bytes == query_object.file_size_bytes if query_object.file_size_bytes else True,
                Resources.uploaded_by_user_id == query_object.uploaded_by_user_id if query_object.uploaded_by_user_id else True,
                Resources.created_at == query_object.created_at if query_object.created_at else True,
            )
            .order_by(Resources.id)
            .distinct()
        )
        resources_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return resources_list

    @classmethod
    async def add_resources_dao(cls, db: AsyncSession, resources: ResourcesModel):
        """
        新增文件资源数据库操作

        :param db: orm对象
        :param resources: 文件资源对象
        :return:
        """
        db_resources = Resources(**resources.model_dump(exclude={}))
        db.add(db_resources)
        await db.flush()

        return db_resources

    @classmethod
    async def edit_resources_dao(cls, db: AsyncSession, resources: dict):
        """
        编辑文件资源数据库操作

        :param db: orm对象
        :param resources: 需要更新的文件资源字典
        :return:
        """
        await db.execute(update(Resources), [resources])

    @classmethod
    async def delete_resources_dao(cls, db: AsyncSession, resources: ResourcesModel):
        """
        删除文件资源数据库操作

        :param db: orm对象
        :param resources: 文件资源对象
        :return:
        """
        await db.execute(delete(Resources).where(Resources.id.in_([resources.id])))

