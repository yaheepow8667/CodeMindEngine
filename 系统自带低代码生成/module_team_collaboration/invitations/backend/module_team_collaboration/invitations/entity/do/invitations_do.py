from sqlalchemy import BigInteger, String, Column, DateTime
from config.database import Base


class Invitations(Base):
    """
    邀请表
    """

    __tablename__ = 'invitations'
    __table_args__ = {'comment': '邀请表'}

    id = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False, comment='')
    team_id = Column(BigInteger, nullable=False, comment='团队ID')
    email = Column(String(255), nullable=False, comment='邀请邮箱')
    token = Column(String(255), nullable=False, comment='邀请令牌')
    role = Column(String(50), nullable=True, comment='邀请角色')
    invited_by_user_id = Column(BigInteger, nullable=True, comment='邀请者用户ID')
    expires_at = Column(DateTime, nullable=False, comment='邀请过期时间')
    accepted_at = Column(DateTime, nullable=True, comment='接受时间')
    created_at = Column(DateTime, nullable=True, comment='创建时间')



