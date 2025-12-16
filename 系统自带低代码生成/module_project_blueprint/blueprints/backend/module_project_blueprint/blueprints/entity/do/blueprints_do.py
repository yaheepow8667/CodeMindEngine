from sqlalchemy import DateTime, Column, String, JSON, SmallInteger, Text, BigInteger
from config.database import Base


class Blueprints(Base):
    """
    蓝图表
    """

    __tablename__ = 'blueprints'
    __table_args__ = {'comment': '蓝图表'}

    id = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False, comment='蓝图ID')
    project_id = Column(BigInteger, nullable=False, comment='项目ID')
    name = Column(String(200), nullable=False, comment='蓝图名称')
    description = Column(Text, nullable=True, comment='蓝图描述')
    version_tag = Column(String(50), nullable=False, comment='版本标签（如 v1.0.0, draft-1）')
    spec_document_id = Column(String(100), nullable=True, comment='独立文档存储中的文档ID')
    spec_summary = Column(JSON, nullable=True, comment='蓝图摘要信息')
    is_draft = Column(SmallInteger, nullable=True, comment='是否为草稿')
    parent_blueprint_id = Column(BigInteger, nullable=True, comment='父蓝图ID')
    created_by_user_id = Column(BigInteger, nullable=True, comment='创建者用户ID')
    created_at = Column(DateTime, nullable=True, comment='创建时间')
    updated_at = Column(DateTime, nullable=True, comment='更新时间')



