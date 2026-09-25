# p01 排序与渐近（sorting & asymptotics）

- 对应讲次：L03（渐近）、L04（归并/主定理）、L05（插入/不变式）、L18（堆排序）。
- 知识点：三种 O(n²)/O(n log n) 排序的实现与**比较计数**；最好/最坏情况；增长率实测倍率验证 Θ 论证；堆排序自底向上建堆。
- 文件：`main.py`（实现 + 自测 + 文本"绘图"表格）。
- 运行：
  - Windows：`run.bat`
  - Linux/macOS：`bash run.sh`
  - 手动：`python -m py_compile main.py && python main.py`
- 预期输出：200 组对拍通过后，打印 n=500..8000 比较次数表；插入倍率≈4（二次），归并/堆倍率≈2 强一点（n log n）；逆序/已排序输入的 Θ(n²)/Θ(n) 断言。
- 延伸：把 `merge_sort` 换成带插入截断的混合版，观察小 n 时曲线变化（Timsort 思想，L04/L05 联系）。
