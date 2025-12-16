from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_system_resource.subscriptions.entity.do.subscriptions_do import Subscriptions
from module_system_resource.subscriptions.entity.vo.subscriptions_vo import SubscriptionsModel, SubscriptionsPageQueryModel
from utils.page_util import PageUtil


class SubscriptionsDao:
    """
    订阅与支付模块数据库操作层
    """

    @classmethod
    async def get_subscriptions_detail_by_id(cls, db: AsyncSession, id: int):
        """
        根据订阅与支付ID获取订阅与支付详细信息

        :param db: orm对象
        :param id: 订阅与支付ID
        :return: 订阅与支付信息对象
        """
        subscriptions_info = (
            (
                await db.execute(
                    select(Subscriptions)
                    .where(
                        Subscriptions.id == id
                    )
                )
            )
            .scalars()
            .first()
        )

        return subscriptions_info

    @classmethod
    async def get_subscriptions_detail_by_info(cls, db: AsyncSession, subscriptions: SubscriptionsModel):
        """
        根据订阅与支付参数获取订阅与支付信息

        :param db: orm对象
        :param subscriptions: 订阅与支付参数对象
        :return: 订阅与支付信息对象
        """
        subscriptions_info = (
            (
                await db.execute(
                    select(Subscriptions).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return subscriptions_info

    @classmethod
    async def get_subscriptions_list(cls, db: AsyncSession, query_object: SubscriptionsPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取订阅与支付列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 订阅与支付列表信息对象
        """
        query = (
            select(Subscriptions)
            .where(
                Subscriptions.team_id == query_object.team_id if query_object.team_id else True,
                Subscriptions.plan == query_object.plan if query_object.plan else True,
                Subscriptions.status == query_object.status if query_object.status else True,
                Subscriptions.current_period_start == query_object.current_period_start if query_object.current_period_start else True,
                Subscriptions.current_period_end == query_object.current_period_end if query_object.current_period_end else True,
                Subscriptions.cancel_at_period_end == query_object.cancel_at_period_end if query_object.cancel_at_period_end else True,
                Subscriptions.canceled_at == query_object.canceled_at if query_object.canceled_at else True,
                Subscriptions.stripe_customer_id == query_object.stripe_customer_id if query_object.stripe_customer_id else True,
                Subscriptions.stripe_subscription_id == query_object.stripe_subscription_id if query_object.stripe_subscription_id else True,
                Subscriptions.created_at == query_object.created_at if query_object.created_at else True,
                Subscriptions.updated_at == query_object.updated_at if query_object.updated_at else True,
            )
            .order_by(Subscriptions.id)
            .distinct()
        )
        subscriptions_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return subscriptions_list

    @classmethod
    async def add_subscriptions_dao(cls, db: AsyncSession, subscriptions: SubscriptionsModel):
        """
        新增订阅与支付数据库操作

        :param db: orm对象
        :param subscriptions: 订阅与支付对象
        :return:
        """
        db_subscriptions = Subscriptions(**subscriptions.model_dump(exclude={}))
        db.add(db_subscriptions)
        await db.flush()

        return db_subscriptions

    @classmethod
    async def edit_subscriptions_dao(cls, db: AsyncSession, subscriptions: dict):
        """
        编辑订阅与支付数据库操作

        :param db: orm对象
        :param subscriptions: 需要更新的订阅与支付字典
        :return:
        """
        await db.execute(update(Subscriptions), [subscriptions])

    @classmethod
    async def delete_subscriptions_dao(cls, db: AsyncSession, subscriptions: SubscriptionsModel):
        """
        删除订阅与支付数据库操作

        :param db: orm对象
        :param subscriptions: 订阅与支付对象
        :return:
        """
        await db.execute(delete(Subscriptions).where(Subscriptions.id.in_([subscriptions.id])))

