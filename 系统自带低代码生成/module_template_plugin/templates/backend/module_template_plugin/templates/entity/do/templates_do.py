from sqlalchemy import DateTime, Column, String, Integer, JSON, SmallInteger, DECIMAL, Text, BigInteger
from config.database import Base


class Templates(Base):
    """
    模板表
    """

    __tablename__ = 'templates'
    __table_args__ = {'comment': '模板表'}

    id = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False, comment='模板ID')
    name = Column(String(200), nullable=False, comment='模板名称')
    slug = Column(String(100), nullable=False, comment='模板标识')
    description = Column(Text, nullable=True, comment='模板描述')
    category = Column(String(100), nullable=False, comment='模板分类 (ui_component, api_layer, project_scaffold, workflow)')
    target_framework = Column(String(100), nullable=True, comment='目标框架 (vue3, react, nestjs, spring_boot)')
    complexity_level = Column(String(20), nullable=True, comment='复杂度 (basic, intermediate, advanced)')
    is_official = Column(SmallInteger, nullable=True, comment='是否官方模板')
    is_public = Column(SmallInteger, nullable=True, comment='是否公开')
    author_user_id = Column(BigInteger, nullable=True, comment='作者用户ID')
    download_count = Column(Integer, nullable=True, comment='下载次数')
    rating = Column(DECIMAL, nullable=True, comment='评分')
    version = Column(String(50), nullable=True, comment='版本')
    tags = Column(JSON, nullable=True, comment='标签数组')
    created_at = Column(DateTime, nullable=True, comment='创建时间')
    updated_at = Column(DateTime, nullable=True, comment='更新时间')



