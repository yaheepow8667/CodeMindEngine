from pydantic import BaseModel, Field
from typing import Optional
from module_admin.annotation.pydantic_annotation import as_query
import inspect

# 定义一个简单的基础模型
class BaseTestModel(BaseModel):
    name: Optional[str] = Field(default=None, description='名称')
    age: Optional[int] = Field(default=None, description='年龄')

# 定义一个继承基础模型的查询模型
@as_query
class TestPageQueryModel(BaseTestModel):
    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')

# 查看生成的as_query函数的签名
print("查看TestPageQueryModel.as_query的签名:")
sig = inspect.signature(TestPageQueryModel.as_query)
print(sig)

# 查看参数类型
print("\n查看参数类型:")
for param_name, param in sig.parameters.items():
    print(f"{param_name}: type={param.kind}, default={param.default}")

# 尝试调用as_query函数
try:
    result = TestPageQueryModel.as_query(name="test", age=25, page_num=1, page_size=20)
    print(f"\n调用成功: {result}")
except Exception as e:
    print(f"\n调用失败: {e}")
