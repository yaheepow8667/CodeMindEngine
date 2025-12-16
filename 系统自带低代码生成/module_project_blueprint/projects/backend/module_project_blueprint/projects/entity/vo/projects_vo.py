from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank
from typing import Optional
from module_admin.annotation.pydantic_annotation import as_query




class ProjectsModel(BaseModel):
    """
    项目表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    id: Optional[int] = Field(default=None, description='项目ID')
    team_id: Optional[int] = Field(default=None, description='团队ID')
    name: Optional[str] = Field(default=None, description='项目名称')
    slug: Optional[str] = Field(default=None, description='项目标识（团队内唯一）')
    description: Optional[str] = Field(default=None, description='项目描述')
    tech_stack: Optional[dict] = Field(default=None, description='技术栈配置 {"frontend": "vue3", "backend": "nestjs", "ui": "ant-design-vue"}')
    status: Optional[str] = Field(default=None, description='项目状态 (active, archived, deleted)')
    is_public: Optional[int] = Field(default=None, description='是否公开')
    storage_quota_mb: Optional[int] = Field(default=None, description='存储配额 (MB)')
    created_by_user_id: Optional[int] = Field(default=None, description='创建者用户ID')
    created_at: Optional[datetime] = Field(default=None, description='创建时间')
    updated_at: Optional[datetime] = Field(default=None, description='更新时间')

    @NotBlank(field_name='team_id', message='团队ID不能为空')
    def get_team_id(self):
        return self.team_id

    @NotBlank(field_name='name', message='项目名称不能为空')
    def get_name(self):
        return self.name

    @NotBlank(field_name='slug', message='项目标识不能为空')
    def get_slug(self):
        return self.slug


    def validate_fields(self):
        self.get_team_id()
        self.get_name()
        self.get_slug()




class ProjectsQueryModel(ProjectsModel):
    """
    项目不分页查询模型
    """
    pass


@as_query
class ProjectsPageQueryModel(ProjectsQueryModel):
    """
    项目分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteProjectsModel(BaseModel):
    """
    删除项目模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    ids: str = Field(description='需要删除的项目ID')
