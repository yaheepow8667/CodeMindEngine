from sqlalchemy import DateTime, Column, String, SmallInteger, Text, BigInteger
from config.database import Base


class GeneratedArtifacts(Base):
    """
    生成产物表
    """

    __tablename__ = 'generated_artifacts'
    __table_args__ = {'comment': '生成产物表'}

    id = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False, comment='产物ID')
    job_id = Column(BigInteger, nullable=False, comment='生成任务ID')
    artifact_type = Column(String(50), nullable=False, comment='产物类型 (source_zip, qa_report, deploy_config, api_docs)')
    artifact_name = Column(String(255), nullable=False, comment='产物名称')
    storage_type = Column(String(50), nullable=True, comment='存储类型 (s3, oss, local)')
    storage_path = Column(Text, nullable=False, comment='存储路径')
    storage_url = Column(Text, nullable=True, comment='访问URL')
    file_size_bytes = Column(BigInteger, nullable=True, comment='文件大小 (字节)')
    mime_type = Column(String(100), nullable=True, comment='文件类型')
    checksum = Column(String(255), nullable=True, comment='校验和')
    is_compressed = Column(SmallInteger, nullable=True, comment='是否压缩')
    created_at = Column(DateTime, nullable=True, comment='创建时间')



