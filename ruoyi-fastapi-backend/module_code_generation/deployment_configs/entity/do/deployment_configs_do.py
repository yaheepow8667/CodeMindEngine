from sqlalchemy import DateTime, Column, String, JSON, SmallInteger, BigInteger
from config.database import Base


class DeploymentConfigs(Base):
    """
    部署配置表
    """

    __tablename__ = 'deployment_configs'
    __table_args__ = {'comment': '部署配置表'}

    id = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False, comment='部署配置ID')
    project_id = Column(BigInteger, nullable=False, comment='项目ID')
    name = Column(String(200), nullable=False, comment='配置名称')
    environment = Column(String(50), nullable=False, comment='部署环境 (development, staging, production)')
    config = Column(JSON, nullable=False, comment='部署配置内容')
    is_active = Column(SmallInteger, nullable=True, comment='是否启用')
    deployed_job_id = Column(BigInteger, nullable=True, comment='已部署的任务ID')
    deployed_at = Column(DateTime, nullable=True, comment='部署时间')
    deployed_by_user_id = Column(BigInteger, nullable=True, comment='部署者用户ID')
    created_at = Column(DateTime, nullable=True, comment='创建时间')
    updated_at = Column(DateTime, nullable=True, comment='更新时间')



