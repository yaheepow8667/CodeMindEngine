from sqlalchemy import BigInteger, String, Column, DateTime
from config.database import Base


class TeamMembers(Base):
    """
    团队成员表
    """

    __tablename__ = 'team_members'
    __table_args__ = {'comment': '团队成员表'}

    id = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False, comment='')
    team_id = Column(BigInteger, nullable=False, comment='团队ID')
    user_id = Column(BigInteger, nullable=False, comment='用户ID')
    role = Column(String(50), nullable=True, comment='成员角色 (owner, admin, member, viewer)')
    joined_at = Column(DateTime, nullable=True, comment='加入时间')
    invited_by_user_id = Column(BigInteger, nullable=True, comment='邀请者用户ID')
    invited_at = Column(DateTime, nullable=True, comment='邀请时间')
    created_at = Column(DateTime, nullable=True, comment='创建时间')



