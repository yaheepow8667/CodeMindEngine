from sqlalchemy import Column, BigInteger, Text, String, DateTime
from config.database import Base


class Teams(Base):
    """
    团队表
    """

    __tablename__ = 'teams'
    __table_args__ = {'comment': '团队表'}

    id = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False, comment='')
    name = Column(String(200), nullable=False, comment='团队名称')
    slug = Column(String(100), nullable=False, comment='团队URL标识')
    description = Column(Text, nullable=True, comment='团队描述')
    logo_url = Column(Text, nullable=True, comment='团队logo')
    subscription_plan = Column(String(50), nullable=True, comment='订阅计划 (free, team, enterprise)')
    subscription_status = Column(String(20), nullable=True, comment='订阅状态 (active, canceled, past_due)')
    subscription_ends_at = Column(DateTime, nullable=True, comment='订阅到期时间')
    created_by_user_id = Column(BigInteger, nullable=True, comment='创建者用户ID')
    created_at = Column(DateTime, nullable=True, comment='创建时间')
    updated_at = Column(DateTime, nullable=True, comment='更新时间')



