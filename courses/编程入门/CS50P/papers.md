# Harvard CS50P — 论文与工程实践对照（骨架）

> 入门语言课，经典文献以 Python 语言奠基性文本为主。

## 一、经典论文 / 奠基文献

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
| --- | --- | --- | --- |
| An Introduction to Python（van Rossum） | 1995 | Python 作者亲撰的第一系统教程，L0–L2 语法的历史源头 | L0–L2 |
| Python 语言参考手册（Language Reference） | 1990s–今 | 名字绑定、作用域、数据模型的权威定义 | L0/L8 |
| PEP 8 – Style Guide for Python Guides | 2001 | "Pythonic"风格规范，命名与可读性标准的出处 | 全课 |
| PEP 20 – The Zen of Python | 2004 | "Simple is better than complex" 等设计哲学 | 全课 |
| Unittesting 经典：Art of Software Testing（书视同）/ pytest 官方文档 | 2000s | 测试先行方法论在 Python 生态的落地形态 | L5 |
| Mastering Regular Expressions（Friedl，书视同一手资料） | 1997 | 正则引擎回溯原理，解释 re 模块性能陷阱 | L7 |

## 二、近 5 年论文（2021–2026）

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
| --- | --- | --- | --- |
| A Survey on Automated Program Repair with LLMs（CodeRL/Falcon 等支系） | 2022–2024 | LLM 自动补测试/修 bug，验证 L5 单元测试的自动化前景 | L5 |
| Pynguin / Test-generation for Python 相关研究 | 2021 | 自动单元测试生成工具与论文，pytest 生态延伸 | L5 |
| To Type or Not to Type: Quantifying Detached Type Annotations（类型注解实证研究） | 2021 | 实证度量 Python 类型注解的收益与成本 | L9 |
| RegexREQ / NL2Regex（自然语言生成正则） | 2022–2023 | 模型辅助写正则，降低 L7 门槛 | L7 |

## 三、知识点在开源项目中的应用

| 课程知识点 | 开源项目案例 | 说明 |
| --- | --- | --- |
| 函数/模块组织 | requests、flask 源码顶层 | 小而清晰的函数式入口设计 |
| 异常处理 | pip、black | CLI 程序的用户输入防御范式 |
| 标准库/第三方库 | Poetry/pipx | L4 包管理生态的现实形态 |
| pytest 测试 | pandas、httpx 测试套件 | 大型项目测试组织可直接对照 L5 |
| 文件与 CSV/JSON | Datasette、csv-diff（simonw） | 数据小工具的 I/O 层 |
| 正则 | validators、dateutil | 生产级正则/校验库 |
| OOP magic methods | SQLAlchemy、attrs/pydantic | 装饰器与描述符把 L8 用到极致 |
