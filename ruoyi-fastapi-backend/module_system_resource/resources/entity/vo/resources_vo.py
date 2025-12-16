from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank
from typing import Optional
from module_admin.annotation.pydantic_annotation import as_query




class ResourcesModel(BaseModel):
    """
    文件资源表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    id: Optional[int] = Field(default=None, description='文件资源ID')
    project_id: Optional[int] = Field(default=None, description='项目ID')
    name: Optional[str] = Field(default=None, description='资源名称')
    resource_type: Optional[str] = Field(default=None, description='资源类型 (image, file, json, sql)')
    storage_path: Optional[str] = Field(default=None, description='存储路径')
    file_size_bytes: Optional[int] = Field(default=None, description='文件大小 (字节)')
    uploaded_by_user_id: Optional[int] = Field(default=None, description='上传者用户ID')
    created_at: Optional[datetime] = Field(default=None, description='创建时间')

    @NotBlank(field_name='project_id', message='项目ID不能为空')
    def get_project_id(self):
        return self.project_id

    @NotBlank(field_name='name', message='资源名称不能为空')
    def get_name(self):
        return self.name

    @NotBlank(field_name='resource_type', message='资源类型 (image, file, json, sql)不能为空')
    def get_resource_type(self):
        return self.resource_type

    @NotBlank(field_name='storage_path', message='存储路径不能为空')
    def get_storage_path(self):
        return self.storage_path


    def validate_fields(self):
        self.get_project_id()
        self.get_name()
        self.get_resource_type()
        self.get_storage_path()




class ResourcesQueryModel(ResourcesModel):
    """
    文件资源不分页查询模型
    """
    pass


@as_query
class ResourcesPageQueryModel(ResourcesQueryModel):
    """
    文件资源分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteResourcesModel(BaseModel):
    """
    删除文件资源模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    ids: str = Field(description='需要删除的文件资源ID')
