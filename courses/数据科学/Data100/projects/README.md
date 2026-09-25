# Data100 配套项目计划（本轮不写代码）

统一约定：Python（pandas/numpy/matplotlib/scikit-learn/SQL），每个小项目 = notebook 或 .py + 数据集 + 产出报告；venv + requirements 备查；只写不编译。

| 章节（模块） | 建议语言 | 小项目 | 编译/运行方式 |
| --- | --- | --- | --- |
| Ch1-Ch5 生命周期与统计 | Python | 公交/外卖准时率分析：摘要统计+分组聚合报告 | jupyter/venv |
| Ch6-Ch7 查询 | Python+SQL | 同一业务问题：pandas vs SQLite/Postgres 双实现与计时对比 | venv + sqlite3 |
| Ch8-Ch9 摄取清洗 | Python | 脏数据集清洗竞赛：解析 JSON/缺失/整形，pandera 校验 | venv |
| Ch10-Ch11 EDA 可视化 | Python | 城市开放数据 EDA 长报告（图形语法+叙事，Quarto 导出） | quarto render（配置） |
| Ch13-Ch14 文本与交换 | Python | 爬取新闻 API 建语料库：TF-IDF 主题速览 | venv |
| Ch15-Ch17 建模基础 | Python | 线性/logistic 回归+CV 选型+推断报告（系数置信区间） | venv |
| Ch19-Ch20 ML 与优化 | Python | 不平衡分类（欺诈检测）：指标对比+手写梯度下降验证收敛 | venv |
| Ch21 期末大项目 | Python | 端到端自选项目：取数→清洗→EDA→建模→deploy 为 Streamlit 页面（配置备查） | streamlit run 配置 |
