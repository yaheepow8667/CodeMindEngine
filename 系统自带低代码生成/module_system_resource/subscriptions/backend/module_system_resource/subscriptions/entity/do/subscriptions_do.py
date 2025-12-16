from sqlalchemy import DateTime, Column, String, SmallInteger, BigInteger
from config.database import Base


class Subscriptions(Base):
    """
    订阅与支付表
    """

    __tablename__ = 'subscriptions'
    __table_args__ = {'comment': '订阅与支付表'}

    id = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False, comment='订阅与支付ID')
    team_id = Column(BigInteger, nullable=False, comment='团队ID')
    plan = Column(String(50), nullable=False, comment='订阅计划')
    status = Column(String(20), nullable=True, comment='订阅状态')
    current_period_start = Column(DateTime, nullable=True, comment='当前订阅周期开始时间')
    current_period_end = Column(DateTime, nullable=True, comment='当前订阅周期结束时间')
    cancel_at_period_end = Column(SmallInteger, nullable=True, comment='是否在周期结束时取消')
    canceled_at = Column(DateTime, nullable=True, comment='取消时间')
    stripe_customer_id = Column(String(255), nullable=True, comment='Stripe客户ID')
    stripe_subscription_id = Column(String(255), nullable=True, comment='Stripe订阅ID')
    created_at = Column(DateTime, nullable=True, comment='创建时间')
    updated_at = Column(DateTime, nullable=True, comment='更新时间')



