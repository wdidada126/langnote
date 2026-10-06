"""提取 markdown 中的 python 代码块并逐个运行，仅用于本地校验教学片段。
不属于笔记内容，用完即删。
"""
import re
import pathlib
import sys
import traceback

TARGET = sys.argv[1]
text = pathlib.Path(TARGET).read_text(encoding="utf-8")
blocks = re.findall(r"```python\n(.*?)```", text, re.S)
print(f"=== {pathlib.Path(TARGET).name}: {len(blocks)} 个代码块 ===")
for i, b in enumerate(blocks, 1):
    ns = {"__name__": "__main__"}
    try:
        exec(compile(b, f"<block{i}>", "exec"), ns)
        print(f"[OK] block {i}")
    except Exception:
        print(f"[FAIL] block {i}")
        traceback.print_exc()
