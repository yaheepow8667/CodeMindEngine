from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank
from typing import Optional
from module_admin.annotation.pydantic_annotation import as_query




class MembersModel(BaseModel):
    """
    团队成员表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    id: Optional[int] = Field(default=None, description='')
    team_id: Optional[int] = Field(default=None, description='团队ID')
    user_id: Optional[int] = Field(default=None, description='用户ID')
    role: Optional[str] = Field(default=None, description='成员角色 (owner, admin, member, viewer)')
    joined_at: Optional[datetime] = Field(default=None, description='加入时间')
    invited_by_user_id: Optional[int] = Field(default=None, description='邀请者用户ID')
    invited_at: Optional[datetime] = Field(default=None, description='邀请时间')
    created_at: Optional[datetime] = Field(default=None, description='创建时间')

    @NotBlank(field_name='team_id', message='团队ID不能为空')
    def get_team_id(self):
        return self.team_id

    @NotBlank(field_name='user_id', message='用户ID不能为空')
    def get_user_id(self):
        return self.user_id


    def validate_fields(self):
        self.get_team_id()
        self.get_user_id()




class MembersQueryModel(MembersModel):
    """
    团队成员不分页查询模型
    """
    pass


@as_query
class MembersPageQueryModel(MembersQueryModel):
    """
    团队成员分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteMembersModel(BaseModel):
    """
    删除团队成员模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    ids: str = Field(description='需要删除的')
