from sqlalchemy import DateTime, Column, String, Integer, JSON, SmallInteger, Text, BigInteger
from config.database import Base


class Projects(Base):
    """
    项目表
    """

    __tablename__ = 'projects'
    __table_args__ = {'comment': '项目表'}

    id = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False, comment='项目ID')
    team_id = Column(BigInteger, nullable=False, comment='团队ID')
    name = Column(String(200), nullable=False, comment='项目名称')
    slug = Column(String(100), nullable=False, comment='项目标识（团队内唯一）')
    description = Column(Text, nullable=True, comment='项目描述')
    tech_stack = Column(JSON, nullable=True, comment='技术栈配置 {"frontend": "vue3", "backend": "nestjs", "ui": "ant-design-vue"}')
    status = Column(String(20), nullable=True, comment='项目状态 (active, archived, deleted)')
    is_public = Column(SmallInteger, nullable=True, comment='是否公开')
    storage_quota_mb = Column(Integer, nullable=True, comment='存储配额 (MB)')
    created_by_user_id = Column(BigInteger, nullable=True, comment='创建者用户ID')
    created_at = Column(DateTime, nullable=True, comment='创建时间')
    updated_at = Column(DateTime, nullable=True, comment='更新时间')



