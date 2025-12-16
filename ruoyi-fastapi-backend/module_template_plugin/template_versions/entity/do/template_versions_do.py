from sqlalchemy import DateTime, Column, String, JSON, SmallInteger, Text, BigInteger
from config.database import Base


class TemplateVersions(Base):
    """
    模板版本表
    """

    __tablename__ = 'template_versions'
    __table_args__ = {'comment': '模板版本表'}

    id = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False, comment='模板版本ID')
    template_id = Column(BigInteger, nullable=False, comment='模板ID')
    version = Column(String(50), nullable=False, comment='版本号')
    changelog = Column(Text, nullable=True, comment='更新日志')
    template_content = Column(JSON, nullable=False, comment='模板JSON定义')
    example_blueprint = Column(JSON, nullable=True, comment='示例蓝图')
    is_active = Column(SmallInteger, nullable=True, comment='是否启用')
    published_at = Column(DateTime, nullable=True, comment='发布时间')
    published_by_user_id = Column(BigInteger, nullable=True, comment='发布者用户ID')
    created_at = Column(DateTime, nullable=True, comment='创建时间')



