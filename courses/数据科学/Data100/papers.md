# Data100 论文与应用清单

## 1. 经典论文/奠基文献

| 文献 | 年份 | 主题 | 关联章 |
| --- | --- | --- | --- |
| Cleveland, Visualizing Data / The Elements of Graphing Data | 1985 | 可视化实验与图形感知 | Ch11 |
| Wickham, Tidy Data | 2014 | 数据整形标准 | Ch9 |
| Wilkinson, The Grammar of Graphics | 2005 | 图形语法 | Ch11 |
| Stonebraker, Ingres/System R 关系数据库论文群（Chamberlin-Boyce 1974; Astrahan 1976） | 1974-76 | SQL 根基 | Ch7 |
| Zaharia et al., Resilient Distributed Datasets (Spark) | 2012 | 规模化数据工程 | Ch1/Ch6 |
| Dean-Ghemawat, MapReduce | 2004 | 分布式批处理 | Ch8/Ch14 |
| Pedregosa et al., Scikit-learn | 2011 | ML 工具 API 范式 | Ch15-20 |
| Hastie et al., The Elements of Statistical Learning（教材性经典） | 2001 | 统计学习理论 | Ch15-17 |
| Breiman, Random Forests | 2001 | 集成分类 | Ch19 |
| Blei et al., LDA | 2003 | 主题模型 | Ch13 |
| McKinney, Data Structures for Statistical Computing in Python (pandas) | 2010 | DataFrame 实现 | Ch6 |

## 2. 近 5 年（2021-2026）

| 文献/技术 | 年份 | 方向 | 关联 |
| --- | --- | --- | --- |
| DuckDB: An Embeddable Analytical Database 论文与社区报告 | 2021-2024 | 进程内分析/向量化 SQL | Ch7 |
| Polars 设计文档与"pandas 性能瓶颈"讨论 | 2021-2024 | 表达式引擎/列式 | Ch6 |
| Parquet v2/Arrow 社区规范演进 | 2021-2023 | 列式存储与数据交换 | Ch14 |
| 表格深度学习基准（TabPFN/Gorishankar 对照：NN 是否适合表格） | 2021-2023 | 建模方法 | Ch15-20 |
| LLM 时代数据管道（RAG 数据摄取/向量检索教程与论文） | 2023-2025 | 文本→嵌入→检索 | Ch13-14 |
| Data Science 教育白皮书（DSI/伯克利修订课程报告） | 2022-2024 | 课程设计 | 全课程 |

## 3. 知识点在开源项目中的应用

| 知识点 | 开源项目 | 体现 |
| --- | --- | --- |
| DataFrame/向量化 | pandas、Polars、Dask、Ray Data | Ch6 工具栈 |
| SQL/分析引擎 | SQLite、DuckDB、PostgreSQL、ClickHouse | Ch7 |
| 数据清洗/整形 | pandera（schema 校验）、great_expectations | Ch9 |
| 可视化 | Plotly、Altair/Vega-Lite、Observable(Plot) | Ch11 |
| 文本/特征 | scikit-learn、spaCy、HuggingFace datasets | Ch13 |
| 序列化/摄取 | PyArrow、requests/httpx 生态 | Ch8/Ch14 |
| 建模/优化 | scikit-learn、statsmodels、PyTorch(Ch20 对照) | Ch15-20 |
| 复现与管线 | Jupyter/VS Code 交互计算、dbt、Airflow | Ch1 生命周期 |
| Web 发布 | Quarto、Streamlit/Gradio 作品集 | Ch11/Ch21 |
