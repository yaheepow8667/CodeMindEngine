from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank
from typing import Optional
from module_admin.annotation.pydantic_annotation import as_query




class SubscriptionsModel(BaseModel):
    """
    订阅与支付表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    id: Optional[int] = Field(default=None, description='订阅与支付ID')
    team_id: Optional[int] = Field(default=None, description='团队ID')
    plan: Optional[str] = Field(default=None, description='订阅计划')
    status: Optional[str] = Field(default=None, description='订阅状态')
    current_period_start: Optional[datetime] = Field(default=None, description='当前订阅周期开始时间')
    current_period_end: Optional[datetime] = Field(default=None, description='当前订阅周期结束时间')
    cancel_at_period_end: Optional[int] = Field(default=None, description='是否在周期结束时取消')
    canceled_at: Optional[datetime] = Field(default=None, description='取消时间')
    stripe_customer_id: Optional[str] = Field(default=None, description='Stripe客户ID')
    stripe_subscription_id: Optional[str] = Field(default=None, description='Stripe订阅ID')
    created_at: Optional[datetime] = Field(default=None, description='创建时间')
    updated_at: Optional[datetime] = Field(default=None, description='更新时间')

    @NotBlank(field_name='team_id', message='团队ID不能为空')
    def get_team_id(self):
        return self.team_id

    @NotBlank(field_name='plan', message='订阅计划不能为空')
    def get_plan(self):
        return self.plan


    def validate_fields(self):
        self.get_team_id()
        self.get_plan()




class SubscriptionsQueryModel(SubscriptionsModel):
    """
    订阅与支付不分页查询模型
    """
    pass


@as_query
class SubscriptionsPageQueryModel(SubscriptionsQueryModel):
    """
    订阅与支付分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteSubscriptionsModel(BaseModel):
    """
    删除订阅与支付模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    ids: str = Field(description='需要删除的订阅与支付ID')
