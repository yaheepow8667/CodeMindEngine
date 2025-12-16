from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_project_blueprint.blueprint_changes.entity.do.changes_do import BlueprintChanges
from module_project_blueprint.blueprint_changes.entity.vo.changes_vo import ChangesModel, ChangesPageQueryModel
from utils.page_util import PageUtil


class ChangesDao:
    """
    蓝图变更记录模块数据库操作层
    """

    @classmethod
    async def get_changes_detail_by_id(cls, db: AsyncSession, id: int):
        """
        根据蓝图变更ID获取蓝图变更记录详细信息

        :param db: orm对象
        :param id: 蓝图变更ID
        :return: 蓝图变更记录信息对象
        """
        changes_info = (
            (
                await db.execute(
                    select(BlueprintChanges)
                    .where(
                        BlueprintChanges.id == id
                    )
                )
            )
            .scalars()
            .first()
        )

        return changes_info

    @classmethod
    async def get_changes_detail_by_info(cls, db: AsyncSession, changes: ChangesModel):
        """
        根据蓝图变更记录参数获取蓝图变更记录信息

        :param db: orm对象
        :param changes: 蓝图变更记录参数对象
        :return: 蓝图变更记录信息对象
        """
        changes_info = (
            (
                await db.execute(
                    select(BlueprintChanges).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return changes_info

    @classmethod
    async def get_changes_list(cls, db: AsyncSession, query_object: ChangesPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取蓝图变更记录列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 蓝图变更记录列表信息对象
        """
        query = (
            select(BlueprintChanges)
            .where(
                BlueprintChanges.blueprint_id == query_object.blueprint_id if query_object.blueprint_id else True,
                BlueprintChanges.change_type == query_object.change_type if query_object.change_type else True,
                BlueprintChanges.field_path == query_object.field_path if query_object.field_path else True,
                BlueprintChanges.old_value == query_object.old_value if query_object.old_value else True,
                BlueprintChanges.new_value == query_object.new_value if query_object.new_value else True,
                BlueprintChanges.changed_by_user_id == query_object.changed_by_user_id if query_object.changed_by_user_id else True,
                BlueprintChanges.created_at == query_object.created_at if query_object.created_at else True,
            )
            .order_by(BlueprintChanges.id)
            .distinct()
        )
        changes_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return changes_list

    @classmethod
    async def add_changes_dao(cls, db: AsyncSession, changes: ChangesModel):
        """
        新增蓝图变更记录数据库操作

        :param db: orm对象
        :param changes: 蓝图变更记录对象
        :return:
        """
        db_changes = BlueprintChanges(**changes.model_dump(exclude={}))
        db.add(db_changes)
        await db.flush()

        return db_changes

    @classmethod
    async def edit_changes_dao(cls, db: AsyncSession, changes: dict):
        """
        编辑蓝图变更记录数据库操作

        :param db: orm对象
        :param changes: 需要更新的蓝图变更记录字典
        :return:
        """
        await db.execute(update(BlueprintChanges), [changes])

    @classmethod
    async def delete_changes_dao(cls, db: AsyncSession, changes: ChangesModel):
        """
        删除蓝图变更记录数据库操作

        :param db: orm对象
        :param changes: 蓝图变更记录对象
        :return:
        """
        await db.execute(delete(BlueprintChanges).where(BlueprintChanges.id.in_([changes.id])))

