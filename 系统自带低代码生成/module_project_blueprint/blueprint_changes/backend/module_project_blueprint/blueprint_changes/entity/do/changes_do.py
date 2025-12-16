from sqlalchemy import DateTime, Column, String, JSON, BigInteger
from config.database import Base


class BlueprintChanges(Base):
    """
    蓝图变更记录表
    """

    __tablename__ = 'blueprint_changes'
    __table_args__ = {'comment': '蓝图变更记录表'}

    id = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False, comment='蓝图变更ID')
    blueprint_id = Column(BigInteger, nullable=False, comment='蓝图ID')
    change_type = Column(String(50), nullable=True, comment='变更类型 (create, update, delete)')
    field_path = Column(String(500), nullable=True, comment='变更字段路径 如 "dataModels.User.fields"')
    old_value = Column(JSON, nullable=True, comment='旧值')
    new_value = Column(JSON, nullable=True, comment='新值')
    changed_by_user_id = Column(BigInteger, nullable=True, comment='变更者用户ID')
    created_at = Column(DateTime, nullable=True, comment='创建时间')



