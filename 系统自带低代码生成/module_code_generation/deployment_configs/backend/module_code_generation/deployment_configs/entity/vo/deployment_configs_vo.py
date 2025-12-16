from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank
from typing import Optional
from module_admin.annotation.pydantic_annotation import as_query




class Deployment_configsModel(BaseModel):
    """
    部署配置表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    id: Optional[int] = Field(default=None, description='部署配置ID')
    project_id: Optional[int] = Field(default=None, description='项目ID')
    name: Optional[str] = Field(default=None, description='配置名称')
    environment: Optional[str] = Field(default=None, description='部署环境 (development, staging, production)')
    config: Optional[dict] = Field(default=None, description='部署配置内容')
    is_active: Optional[int] = Field(default=None, description='是否启用')
    deployed_job_id: Optional[int] = Field(default=None, description='已部署的任务ID')
    deployed_at: Optional[datetime] = Field(default=None, description='部署时间')
    deployed_by_user_id: Optional[int] = Field(default=None, description='部署者用户ID')
    created_at: Optional[datetime] = Field(default=None, description='创建时间')
    updated_at: Optional[datetime] = Field(default=None, description='更新时间')

    @NotBlank(field_name='project_id', message='项目ID不能为空')
    def get_project_id(self):
        return self.project_id

    @NotBlank(field_name='name', message='配置名称不能为空')
    def get_name(self):
        return self.name

    @NotBlank(field_name='environment', message='部署环境 (development, staging, production)不能为空')
    def get_environment(self):
        return self.environment

    @NotBlank(field_name='config', message='部署配置内容不能为空')
    def get_config(self):
        return self.config


    def validate_fields(self):
        self.get_project_id()
        self.get_name()
        self.get_environment()
        self.get_config()




class Deployment_configsQueryModel(Deployment_configsModel):
    """
    部署配置不分页查询模型
    """
    pass


@as_query
class Deployment_configsPageQueryModel(Deployment_configsQueryModel):
    """
    部署配置分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteDeployment_configsModel(BaseModel):
    """
    删除部署配置模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    ids: str = Field(description='需要删除的部署配置ID')
