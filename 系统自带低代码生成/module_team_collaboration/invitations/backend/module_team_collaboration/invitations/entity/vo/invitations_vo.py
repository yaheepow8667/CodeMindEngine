from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank
from typing import Optional
from module_admin.annotation.pydantic_annotation import as_query




class InvitationsModel(BaseModel):
    """
    邀请表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    id: Optional[int] = Field(default=None, description='')
    team_id: Optional[int] = Field(default=None, description='团队ID')
    email: Optional[str] = Field(default=None, description='邀请邮箱')
    token: Optional[str] = Field(default=None, description='邀请令牌')
    role: Optional[str] = Field(default=None, description='邀请角色')
    invited_by_user_id: Optional[int] = Field(default=None, description='邀请者用户ID')
    expires_at: Optional[datetime] = Field(default=None, description='邀请过期时间')
    accepted_at: Optional[datetime] = Field(default=None, description='接受时间')
    created_at: Optional[datetime] = Field(default=None, description='创建时间')

    @NotBlank(field_name='team_id', message='团队ID不能为空')
    def get_team_id(self):
        return self.team_id

    @NotBlank(field_name='email', message='邀请邮箱不能为空')
    def get_email(self):
        return self.email

    @NotBlank(field_name='token', message='邀请令牌不能为空')
    def get_token(self):
        return self.token

    @NotBlank(field_name='expires_at', message='邀请过期时间不能为空')
    def get_expires_at(self):
        return self.expires_at


    def validate_fields(self):
        self.get_team_id()
        self.get_email()
        self.get_token()
        self.get_expires_at()




class InvitationsQueryModel(InvitationsModel):
    """
    邀请不分页查询模型
    """
    pass


@as_query
class InvitationsPageQueryModel(InvitationsQueryModel):
    """
    邀请分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteInvitationsModel(BaseModel):
    """
    删除邀请模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    ids: str = Field(description='需要删除的')
