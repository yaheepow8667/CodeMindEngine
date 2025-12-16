from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank
from typing import Optional
from module_admin.annotation.pydantic_annotation import as_query




class BlueprintsModel(BaseModel):
    """
    蓝图表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    id: Optional[int] = Field(default=None, description='蓝图ID')
    project_id: Optional[int] = Field(default=None, description='项目ID')
    name: Optional[str] = Field(default=None, description='蓝图名称')
    description: Optional[str] = Field(default=None, description='蓝图描述')
    version_tag: Optional[str] = Field(default=None, description='版本标签（如 v1.0.0, draft-1）')
    spec_document_id: Optional[str] = Field(default=None, description='独立文档存储中的文档ID')
    spec_summary: Optional[dict] = Field(default=None, description='蓝图摘要信息')
    is_draft: Optional[int] = Field(default=None, description='是否为草稿')
    parent_blueprint_id: Optional[int] = Field(default=None, description='父蓝图ID')
    created_by_user_id: Optional[int] = Field(default=None, description='创建者用户ID')
    created_at: Optional[datetime] = Field(default=None, description='创建时间')
    updated_at: Optional[datetime] = Field(default=None, description='更新时间')

    @NotBlank(field_name='project_id', message='项目ID不能为空')
    def get_project_id(self):
        return self.project_id

    @NotBlank(field_name='name', message='蓝图名称不能为空')
    def get_name(self):
        return self.name

    @NotBlank(field_name='version_tag', message='版本标签不能为空')
    def get_version_tag(self):
        return self.version_tag


    def validate_fields(self):
        self.get_project_id()
        self.get_name()
        self.get_version_tag()




class BlueprintsQueryModel(BlueprintsModel):
    """
    蓝图不分页查询模型
    """
    pass


@as_query
class BlueprintsPageQueryModel(BlueprintsQueryModel):
    """
    蓝图分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteBlueprintsModel(BaseModel):
    """
    删除蓝图模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    ids: str = Field(description='需要删除的蓝图ID')
