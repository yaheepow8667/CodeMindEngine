from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank
from typing import Optional
from module_admin.annotation.pydantic_annotation import as_query




class Generation_jobsModel(BaseModel):
    """
    生成任务表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    id: Optional[int] = Field(default=None, description='生成任务ID')
    project_id: Optional[int] = Field(default=None, description='项目ID')
    blueprint_id: Optional[int] = Field(default=None, description='蓝图ID')
    status: Optional[str] = Field(default=None, description='任务状态 (pending, generating, qa, success, failed)')
    target_tech_stack: Optional[dict] = Field(default=None, description='目标技术栈配置')
    trigger_type: Optional[str] = Field(default=None, description='触发类型 (manual, api, webhook, schedule)')
    triggered_by_user_id: Optional[int] = Field(default=None, description='触发者用户ID')
    started_at: Optional[datetime] = Field(default=None, description='开始时间')
    completed_at: Optional[datetime] = Field(default=None, description='完成时间')
    error_message: Optional[str] = Field(default=None, description='错误信息')
    logs: Optional[dict] = Field(default=None, description='生成日志')
    qa_report: Optional[dict] = Field(default=None, description='质量检查报告')
    created_at: Optional[datetime] = Field(default=None, description='创建时间')

    @NotBlank(field_name='project_id', message='项目ID不能为空')
    def get_project_id(self):
        return self.project_id

    @NotBlank(field_name='blueprint_id', message='蓝图ID不能为空')
    def get_blueprint_id(self):
        return self.blueprint_id


    def validate_fields(self):
        self.get_project_id()
        self.get_blueprint_id()




class Generation_jobsQueryModel(Generation_jobsModel):
    """
    生成任务不分页查询模型
    """
    pass


@as_query
class Generation_jobsPageQueryModel(Generation_jobsQueryModel):
    """
    生成任务分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteGeneration_jobsModel(BaseModel):
    """
    删除生成任务模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    ids: str = Field(description='需要删除的生成任务ID')
