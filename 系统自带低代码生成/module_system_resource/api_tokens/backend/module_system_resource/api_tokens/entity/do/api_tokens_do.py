from sqlalchemy import DateTime, Column, String, JSON, SmallInteger, BigInteger
from config.database import Base


class ApiTokens(Base):
    """
    API访问令牌表
    """

    __tablename__ = 'api_tokens'
    __table_args__ = {'comment': 'API访问令牌表'}

    id = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False, comment='访问令牌ID')
    user_id = Column(BigInteger, nullable=False, comment='用户ID')
    team_id = Column(BigInteger, nullable=True, comment='团队ID')
    name = Column(String(200), nullable=False, comment='令牌名称')
    token_hash = Column(String(255), nullable=False, comment='令牌哈希值')
    token_prefix = Column(String(10), nullable=False, comment='令牌前缀')
    scopes = Column(JSON, nullable=False, comment='权限范围')
    expires_at = Column(DateTime, nullable=True, comment='过期时间')
    last_used_at = Column(DateTime, nullable=True, comment='最后使用时间')
    is_active = Column(SmallInteger, nullable=True, comment='是否启用')
    created_at = Column(DateTime, nullable=True, comment='创建时间')



