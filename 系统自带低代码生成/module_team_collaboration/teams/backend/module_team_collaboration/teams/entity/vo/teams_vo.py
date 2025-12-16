from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank
from typing import Optional
from module_admin.annotation.pydantic_annotation import as_query




class TeamsModel(BaseModel):
    """
    团队表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    id: Optional[int] = Field(default=None, description='')
    name: Optional[str] = Field(default=None, description='团队名称')
    slug: Optional[str] = Field(default=None, description='团队URL标识')
    description: Optional[str] = Field(default=None, description='团队描述')
    logo_url: Optional[str] = Field(default=None, description='团队logo')
    subscription_plan: Optional[str] = Field(default=None, description='订阅计划 (free, team, enterprise)')
    subscription_status: Optional[str] = Field(default=None, description='订阅状态 (active, canceled, past_due)')
    subscription_ends_at: Optional[datetime] = Field(default=None, description='订阅到期时间')
    created_by_user_id: Optional[int] = Field(default=None, description='创建者用户ID')
    created_at: Optional[datetime] = Field(default=None, description='创建时间')
    updated_at: Optional[datetime] = Field(default=None, description='更新时间')

    @NotBlank(field_name='name', message='团队名称不能为空')
    def get_name(self):
        return self.name

    @NotBlank(field_name='slug', message='团队URL标识不能为空')
    def get_slug(self):
        return self.slug


    def validate_fields(self):
        self.get_name()
        self.get_slug()




class TeamsQueryModel(TeamsModel):
    """
    团队不分页查询模型
    """
    pass


@as_query
class TeamsPageQueryModel(TeamsQueryModel):
    """
    团队分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteTeamsModel(BaseModel):
    """
    删除团队模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    ids: str = Field(description='需要删除的')
