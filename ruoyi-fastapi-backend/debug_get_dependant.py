import inspect
import sys

# 查看get_dependant函数的内容
try:
    from fastapi.dependencies import utils
    print("查看get_dependant函数的内容:")
    source = inspect.getsource(utils.get_dependant)
    lines = source.split('\n')
    print(f"函数总共有 {len(lines)} 行")
    print("\n第280-290行:")
    # 打印第280-290行
    for i in range(279, min(290, len(lines))):
        print(f"第{i+1}行: {lines[i]}")

except Exception as e:
    print(f"查看源代码时出错: {e}")
    sys.exit(1)
