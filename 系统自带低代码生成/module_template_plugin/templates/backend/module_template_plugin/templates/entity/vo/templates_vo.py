from decimal import Decimal
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank
from typing import Optional
from module_admin.annotation.pydantic_annotation import as_query




class TemplatesModel(BaseModel):
    """
    模板表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    id: Optional[int] = Field(default=None, description='模板ID')
    name: Optional[str] = Field(default=None, description='模板名称')
    slug: Optional[str] = Field(default=None, description='模板标识')
    description: Optional[str] = Field(default=None, description='模板描述')
    category: Optional[str] = Field(default=None, description='模板分类 (ui_component, api_layer, project_scaffold, workflow)')
    target_framework: Optional[str] = Field(default=None, description='目标框架 (vue3, react, nestjs, spring_boot)')
    complexity_level: Optional[str] = Field(default=None, description='复杂度 (basic, intermediate, advanced)')
    is_official: Optional[int] = Field(default=None, description='是否官方模板')
    is_public: Optional[int] = Field(default=None, description='是否公开')
    author_user_id: Optional[int] = Field(default=None, description='作者用户ID')
    download_count: Optional[int] = Field(default=None, description='下载次数')
    rating: Optional[Decimal] = Field(default=None, description='评分')
    version: Optional[str] = Field(default=None, description='版本')
    tags: Optional[dict] = Field(default=None, description='标签数组')
    created_at: Optional[datetime] = Field(default=None, description='创建时间')
    updated_at: Optional[datetime] = Field(default=None, description='更新时间')

    @NotBlank(field_name='name', message='模板名称不能为空')
    def get_name(self):
        return self.name

    @NotBlank(field_name='slug', message='模板标识不能为空')
    def get_slug(self):
        return self.slug

    @NotBlank(field_name='category', message='模板分类 (ui_component, api_layer, project_scaffold, workflow)不能为空')
    def get_category(self):
        return self.category


    def validate_fields(self):
        self.get_name()
        self.get_slug()
        self.get_category()




class TemplatesQueryModel(TemplatesModel):
    """
    模板不分页查询模型
    """
    pass


@as_query
class TemplatesPageQueryModel(TemplatesQueryModel):
    """
    模板分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteTemplatesModel(BaseModel):
    """
    删除模板模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    ids: str = Field(description='需要删除的模板ID')
