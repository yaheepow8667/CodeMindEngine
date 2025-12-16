from sqlalchemy import DateTime, Column, String, Integer, JSON, SmallInteger, BigInteger
from config.database import Base


class Plugins(Base):
    """
    插件表
    """

    __tablename__ = 'plugins'
    __table_args__ = {'comment': '插件表'}

    id = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False, comment='插件ID')
    name = Column(String(200), nullable=False, comment='插件名称')
    plugin_type = Column(String(50), nullable=False, comment='插件类型 (code_generator, qa_checker, deployer)')
    target_framework = Column(String(100), nullable=True, comment='目标框架')
    version = Column(String(50), nullable=True, comment='版本')
    author_user_id = Column(BigInteger, nullable=True, comment='作者用户ID')
    is_approved = Column(SmallInteger, nullable=True, comment='是否已审核')
    install_count = Column(Integer, nullable=True, comment='安装次数')
    config_schema = Column(JSON, nullable=True, comment='插件配置JSON Schema')
    created_at = Column(DateTime, nullable=True, comment='创建时间')
    updated_at = Column(DateTime, nullable=True, comment='更新时间')



