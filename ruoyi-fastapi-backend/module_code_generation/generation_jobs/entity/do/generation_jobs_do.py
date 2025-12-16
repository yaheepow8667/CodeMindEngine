from sqlalchemy import DateTime, Column, String, JSON, Text, BigInteger
from config.database import Base


class GenerationJobs(Base):
    """
    生成任务表
    """

    __tablename__ = 'generation_jobs'
    __table_args__ = {'comment': '生成任务表'}

    id = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False, comment='生成任务ID')
    project_id = Column(BigInteger, nullable=False, comment='项目ID')
    blueprint_id = Column(BigInteger, nullable=False, comment='蓝图ID')
    status = Column(String(50), nullable=True, comment='任务状态 (pending, generating, qa, success, failed)')
    target_tech_stack = Column(JSON, nullable=True, comment='目标技术栈配置')
    trigger_type = Column(String(50), nullable=True, comment='触发类型 (manual, api, webhook, schedule)')
    triggered_by_user_id = Column(BigInteger, nullable=True, comment='触发者用户ID')
    started_at = Column(DateTime, nullable=True, comment='开始时间')
    completed_at = Column(DateTime, nullable=True, comment='完成时间')
    error_message = Column(Text, nullable=True, comment='错误信息')
    logs = Column(JSON, nullable=True, comment='生成日志')
    qa_report = Column(JSON, nullable=True, comment='质量检查报告')
    created_at = Column(DateTime, nullable=True, comment='创建时间')



