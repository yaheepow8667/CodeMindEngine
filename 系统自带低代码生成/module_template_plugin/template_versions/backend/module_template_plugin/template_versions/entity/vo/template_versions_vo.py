from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank
from typing import Optional
from module_admin.annotation.pydantic_annotation import as_query




class Template_versionsModel(BaseModel):
    """
    模板版本表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    id: Optional[int] = Field(default=None, description='模板版本ID')
    template_id: Optional[int] = Field(default=None, description='模板ID')
    version: Optional[str] = Field(default=None, description='版本号')
    changelog: Optional[str] = Field(default=None, description='更新日志')
    template_content: Optional[dict] = Field(default=None, description='模板JSON定义')
    example_blueprint: Optional[dict] = Field(default=None, description='示例蓝图')
    is_active: Optional[int] = Field(default=None, description='是否启用')
    published_at: Optional[datetime] = Field(default=None, description='发布时间')
    published_by_user_id: Optional[int] = Field(default=None, description='发布者用户ID')
    created_at: Optional[datetime] = Field(default=None, description='创建时间')

    @NotBlank(field_name='template_id', message='模板ID不能为空')
    def get_template_id(self):
        return self.template_id

    @NotBlank(field_name='version', message='版本号不能为空')
    def get_version(self):
        return self.version

    @NotBlank(field_name='template_content', message='模板JSON定义不能为空')
    def get_template_content(self):
        return self.template_content


    def validate_fields(self):
        self.get_template_id()
        self.get_version()
        self.get_template_content()




class Template_versionsQueryModel(Template_versionsModel):
    """
    模板版本不分页查询模型
    """
    pass


@as_query
class Template_versionsPageQueryModel(Template_versionsQueryModel):
    """
    模板版本分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteTemplate_versionsModel(BaseModel):
    """
    删除模板版本模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    ids: str = Field(description='需要删除的模板版本ID')
