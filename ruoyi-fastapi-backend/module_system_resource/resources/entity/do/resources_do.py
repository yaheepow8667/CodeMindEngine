from sqlalchemy import DateTime, Column, String, Text, BigInteger
from config.database import Base


class Resources(Base):
    """
    文件资源表
    """

    __tablename__ = 'resources'
    __table_args__ = {'comment': '文件资源表'}

    id = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False, comment='文件资源ID')
    project_id = Column(BigInteger, nullable=False, comment='项目ID')
    name = Column(String(255), nullable=False, comment='资源名称')
    resource_type = Column(String(50), nullable=False, comment='资源类型 (image, file, json, sql)')
    storage_path = Column(Text, nullable=False, comment='存储路径')
    file_size_bytes = Column(BigInteger, nullable=True, comment='文件大小 (字节)')
    uploaded_by_user_id = Column(BigInteger, nullable=True, comment='上传者用户ID')
    created_at = Column(DateTime, nullable=True, comment='创建时间')



