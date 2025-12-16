import inspect
import sys

# 查看analyze_param函数的完整内容
try:
    from fastapi.dependencies import utils
    print("查看analyze_param函数的完整内容:")
    source = inspect.getsource(utils.analyze_param)
    print(source)

except Exception as e:
    print(f"查看源代码时出错: {e}")
    sys.exit(1)
