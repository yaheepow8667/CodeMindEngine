from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank
from typing import Optional
from module_admin.annotation.pydantic_annotation import as_query




class ChangesModel(BaseModel):
    """
    蓝图变更记录表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    id: Optional[int] = Field(default=None, description='蓝图变更ID')
    blueprint_id: Optional[int] = Field(default=None, description='蓝图ID')
    change_type: Optional[str] = Field(default=None, description='变更类型 (create, update, delete)')
    field_path: Optional[str] = Field(default=None, description='变更字段路径 如 "dataModels.User.fields"')
    old_value: Optional[dict] = Field(default=None, description='旧值')
    new_value: Optional[dict] = Field(default=None, description='新值')
    changed_by_user_id: Optional[int] = Field(default=None, description='变更者用户ID')
    created_at: Optional[datetime] = Field(default=None, description='创建时间')

    @NotBlank(field_name='blueprint_id', message='蓝图ID不能为空')
    def get_blueprint_id(self):
        return self.blueprint_id


    def validate_fields(self):
        self.get_blueprint_id()




class ChangesQueryModel(ChangesModel):
    """
    蓝图变更记录不分页查询模型
    """
    pass


@as_query
class ChangesPageQueryModel(ChangesQueryModel):
    """
    蓝图变更记录分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteChangesModel(BaseModel):
    """
    删除蓝图变更记录模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    ids: str = Field(description='需要删除的蓝图变更ID')
