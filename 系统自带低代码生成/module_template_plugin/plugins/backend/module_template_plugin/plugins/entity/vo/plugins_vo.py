from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank
from typing import Optional
from module_admin.annotation.pydantic_annotation import as_query




class PluginsModel(BaseModel):
    """
    插件表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    id: Optional[int] = Field(default=None, description='插件ID')
    name: Optional[str] = Field(default=None, description='插件名称')
    plugin_type: Optional[str] = Field(default=None, description='插件类型 (code_generator, qa_checker, deployer)')
    target_framework: Optional[str] = Field(default=None, description='目标框架')
    version: Optional[str] = Field(default=None, description='版本')
    author_user_id: Optional[int] = Field(default=None, description='作者用户ID')
    is_approved: Optional[int] = Field(default=None, description='是否已审核')
    install_count: Optional[int] = Field(default=None, description='安装次数')
    config_schema: Optional[dict] = Field(default=None, description='插件配置JSON Schema')
    created_at: Optional[datetime] = Field(default=None, description='创建时间')
    updated_at: Optional[datetime] = Field(default=None, description='更新时间')

    @NotBlank(field_name='name', message='插件名称不能为空')
    def get_name(self):
        return self.name

    @NotBlank(field_name='plugin_type', message='插件类型 (code_generator, qa_checker, deployer)不能为空')
    def get_plugin_type(self):
        return self.plugin_type


    def validate_fields(self):
        self.get_name()
        self.get_plugin_type()




class PluginsQueryModel(PluginsModel):
    """
    插件不分页查询模型
    """
    pass


@as_query
class PluginsPageQueryModel(PluginsQueryModel):
    """
    插件分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeletePluginsModel(BaseModel):
    """
    删除插件模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    ids: str = Field(description='需要删除的插件ID')
