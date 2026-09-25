# MIT 6.100L — 配套项目计划（骨架）

> 本轮不写代码。主线：官网每课的 in-class/lab code 必跟写；Problem Sets 独立实现（无答案，对照 Alidme/MIT6.100L 仓库复盘）；期末做一个综合小项目。

| 章节 | 建议语言 | 小项目 | 编译/运行方式 |
| --- | --- | --- | --- |
| L1–L6 基础 | Python | `bmi_grade.py`：输入-计算-分支评级小程序（跟完 Lab1） | `python bmi_grade.py` |
| L7–L13 函数与复合数据 | Python | 学生成绩登记簿：嵌套 list/dict、别名陷阱复现与修复（Lab2） | `python roster.py` |
| L14–L18 算法与复杂度 | Python | 搜索/排序实验台：自己实现二分与归并 + doctest + 计时对比曲线（Lab3） | `pytest --doctest-modules`；`python bench.py` |
| L19–L21 OOP 与文件 | Python | 图书借阅系统：类建模 + CSV 持久化 + 异常处理 | `python library.py` |
| L22–L24 数据与模拟 | Python | 随机游走/排队模拟 + matplotlib 可视化报告（Lab4） | `python sim.py && python plot.py` |
| L25–L26 综合 | Python | 期末综合项目：以上模块合体为一个带测试与文档的小应用 | `pytest && python app.py` |

## 验收清单
- [ ] 4 个 Lab 代码全部跟写；PS 至少完成 80% 并复盘；
- [ ] 期末小项目含 doctest/pytest 测试与复杂度说明文档。
