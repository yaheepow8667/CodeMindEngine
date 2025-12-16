import inspect
import sys

# 查看analyze_param函数的完整内容并显示行数
try:
    from fastapi.dependencies import utils
    print("查看analyze_param函数的完整内容:")
    source = inspect.getsource(utils.analyze_param)
    lines = source.split('\n')
    print(f"函数总共有 {len(lines)} 行")
    print("\n完整内容:")
    for i, line in enumerate(lines):
        print(f"第{i+1}行: {line}")

except Exception as e:
    print(f"查看源代码时出错: {e}")
    sys.exit(1)
