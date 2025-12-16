from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank
from typing import Optional
from module_admin.annotation.pydantic_annotation import as_query




class Api_tokensModel(BaseModel):
    """
    API访问令牌表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    id: Optional[int] = Field(default=None, description='访问令牌ID')
    user_id: Optional[int] = Field(default=None, description='用户ID')
    team_id: Optional[int] = Field(default=None, description='团队ID')
    name: Optional[str] = Field(default=None, description='令牌名称')
    token_hash: Optional[str] = Field(default=None, description='令牌哈希值')
    token_prefix: Optional[str] = Field(default=None, description='令牌前缀')
    scopes: Optional[dict] = Field(default=None, description='权限范围')
    expires_at: Optional[datetime] = Field(default=None, description='过期时间')
    last_used_at: Optional[datetime] = Field(default=None, description='最后使用时间')
    is_active: Optional[int] = Field(default=None, description='是否启用')
    created_at: Optional[datetime] = Field(default=None, description='创建时间')

    @NotBlank(field_name='user_id', message='用户ID不能为空')
    def get_user_id(self):
        return self.user_id

    @NotBlank(field_name='name', message='令牌名称不能为空')
    def get_name(self):
        return self.name

    @NotBlank(field_name='token_hash', message='令牌哈希值不能为空')
    def get_token_hash(self):
        return self.token_hash

    @NotBlank(field_name='token_prefix', message='令牌前缀不能为空')
    def get_token_prefix(self):
        return self.token_prefix

    @NotBlank(field_name='scopes', message='权限范围不能为空')
    def get_scopes(self):
        return self.scopes


    def validate_fields(self):
        self.get_user_id()
        self.get_name()
        self.get_token_hash()
        self.get_token_prefix()
        self.get_scopes()




class Api_tokensQueryModel(Api_tokensModel):
    """
    API访问令牌不分页查询模型
    """
    pass


@as_query
class Api_tokensPageQueryModel(Api_tokensQueryModel):
    """
    API访问令牌分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteApi_tokensModel(BaseModel):
    """
    删除API访问令牌模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    ids: str = Field(description='需要删除的访问令牌ID')
