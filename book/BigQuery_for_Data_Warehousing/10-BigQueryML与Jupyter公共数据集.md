# 10 BigQuery ML 与 Jupyter 公共数据集

> 对应原书 **Ch.19 BigQuery ML（pp.419–468）**、**Ch.20 Jupyter Notebooks and Public Datasets（pp.469–496）**（章题/页码：Crossref DOI _19 / _20，✅ 实抓）。
> 正文为精读重构；机制为官方文档转述（⚠️），✅ URL 经 `docs.cloud.google.cn` 镜像 2026-10 实测 200。全书最大两章在此（BQML 50 页），合并为一个文件是 00 映射表中的明示取舍。

## 一句话主题

第 19 章把机器学习搬进 SQL：`CREATE MODEL` 即训练，数据一步不搬；第 20 章给「仓库+笔记本+公共数据」的探索组合拳——作者的意图是让**建模与探索成为数仓日常**，而非数据科学团队的专利（Ch.1 「让业务领导者日常受益于数据」信念的 ML 版）。

## Ch.19 BigQuery ML：SQL 里的机器学习

### 19.1 设计哲学（⚠️ 转述 + ✅）

- **模型是仓库对象**：与表/视图同层级，`CREATE MODEL dataset.m1 AS SELECT MODEL_OPTS..., training_query` ——训练数据即特征查询，特征管道复用 Ch.9 的 SQL 手艺（见 [05-仓库养护与查询开发.md](05-仓库养护与查询开发.md)）；
- 免搬运=免泄漏+免同步：TB 级特征出仓训练的传统路线（导出→Notebook→回灌）在 BQML 面前只剩「需要非表格框架」的例外场景；概览 ✅ https://docs.cloud.google.cn/bigquery/docs/bqml-introduction（镜像 200）；
- 权限/治理天然继承：模型跟数据集走 IAM 与 Ch.14 目录（见 [08-数据治理与长期适应.md](08-数据治理与长期适应.md)）——**「模型即数据资产」在 2020 是超前的治理观**，2026 已成 MLOps 教科书常识。

### 19.2 2020 支持清单与语义（⚠️ 时点转述，重构）

- 模型谱系（2020）：`linear_reg / logistic_reg / kmeans / matrix_fact`（推荐）+ `xgboost` 连接器（外部库）+ DNN 类预览（⚠️ 名目以当期文档为准）；`FORECASTING`（ARIMA）恰在本册出版窗口亮相（2020-06 预览），作者成书时未能尽录——本目录补记入文末演进；
- 运维四函数：`ML.TRAINING_INFO`（收敛史）、`ML.EVALUATE`（指标）、`ML.PREDICT`（即席打分）、`ML.CONFUSION_MATRIX`；全部是 SQL 视图=报表系统可直接消费模型质量（17 章仪表板联动）；
- 特征工程=查询工程：宽表 join、窗口聚合特征、`FEATURES` 列省略语法；作者警告——**训练查询的扫描量按 Ch.4 计费口径走**，一轮调参网格可能烧掉半月报表预算（E1 剪枝类比见 [02-数据盘点与成本管控.md](02-数据盘点与成本管控.md)）；
- 适用面裁定（重构）：表格数据的基线模型/批量打分/业务团队自助建模=甜区；深度网络/非结构化/超参重搜索=仍归 Vertex AI 与工程团队（BQML 定位「民主化的 80%」而非全家桶）。

### 19.3 本章教学线（用例重构）

- 全链路示例骨架：Ch.5–6 摄入的明细 → Ch.8 清洗去重 → 特征视图 → CREATE MODEL → ML.EVALUATE 进周报 → ML.PREDICT 结果落表供 Ch.16 报表消费——**ML 是本书管道叙事的自然终点**，两章（19/20）实为 Part VI「把仓库用起来」的升华段。

## Ch.20 Jupyter Notebooks 与公共数据集：探索组合拳

### 20.1 笔记本工作流（⚠️ 2020 转述）

- 入口双轨：**Colab（Google 托管，免装环境，直连 BQ 认证）**与本地 Jupyter + `google-cloud-bigquery` Python 客户端；`client.query()` 返回 Arrow 行集→pandas 可视——SQL 与 Python 在同格共存；
- 三纪律（作者式，重构）：探索查询必带 `LIMIT`/分区谓词（笔记本是扫描费事故高发区，接 Ch.4）；notebook 版本入库（Git/目录登记，接 Ch.15）；产出「值得产品化的 notebook 查询」→ 晋升为调度 SQL/报表（Ch.10/16 通道，见 [06-作业调度与无服务器函数.md](06-作业调度与无服务器函数.md)、[09-报表仪表板与DataStudio.md](09-报表仪表板与DataStudio.md)）；
- 客户端能力：magic（`%%bigquery`）、异步作业轮询、干跑估算、to_dataframe 的分片下载——探索体验层的东西，2020 已齐。

### 20.2 公共数据集（⚠️ 时点转述）

- 2020 形态：`bigquery-public-data` 巨型项目，GitHub Archive、NOAA 气象、加密币、 census、chromium 崩溃等数百数据源免注册直查；通配语法 `FROM \`publicdata.samples.natality\``（历史项目名并存，⚠️）；
- 作者的公共数据教学法：**先用公共库练手（零装载成本、真实脏度），再对照自家 Ch.3 盘点表复盘**——「GitHub Archive 就是你的一个高吞吐流式源模拟场」；
- 边界提醒：公共≠权威（口径免责）、跨区查询费规则、热门大表必须分区/列裁剪示范（E2 类比场景，见 [03-批量装载与流式摄入.md](03-批量装载与流式摄入.md)）。

## 实操演练建议（不可实测口径下的替代法）

- 公共数据集与 BQML 均不可本机连测（⚠️ 本环境 cloud.google.com 全不可达实测记录）；SQL 方言手感可用 DuckDB 的 `bigquery` 兼容扩展作**近似替身**（`INSTALL bigquery; LOAD bigquery;` 后 `SELECT CAST('1' AS INT64)` 类方言试味，非 BigQuery 行为，仅供语法肌肉记忆）；
- `CREATE MODEL` 语义可类比「把训练任务伪装成一条 SQL 的 job」——其账单面与查询完全同构（扫描量计费、slot 占用），这一定性不依赖平台实测。

## 附：BQML 与笔记本配方卡（自拟教学示意，⚠️ 非原书内容、不可本机执行）

- **训练→评估→打分三连**（语法形状记忆，选项名以当期文档为准 ⚠️）：

```sql
CREATE OR REPLACE MODEL ds.churn_v1
OPTIONS(model_type='logistic_reg', input_label_cols=['churned'],
        data_split_col='fold') AS
SELECT user_age, tenure, tickets_30d, *EXCEPT(churned, fold)
FROM features.users WHERE fold IS NOT NULL;

SELECT * FROM ML.EVALUATE(MODEL ds.churn_v1, TABLE features.users_test);
SELECT user_id, p.churned.prob AS risk
FROM ML.PREDICT(MODEL ds.churn_v1, TABLE features.users_test) p
ORDER BY risk DESC LIMIT 100;
```

- 训练成本三连问（19.2 警告的操作化）：特征查询预估字节多少？调参网格=几轮训练？打分是全量还是增量分区？——三问写进模型卡片元数据（Ch.14 目录挂载点，见 [08-数据治理与长期适应.md](08-数据治理与长期适应.md)）；
- **Colab 探索骨架**（伪码，客户端库 API ⚠️ 转述）：

```python
from google.cloud import bigquery
client = bigquery.Client(project="me")
job = client.query(sql + " LIMIT 1000")          # 笔记本纪律三件套之一
df  = job.to_dataframe()                          # Arrow 通道；大结果走分片
df.plot.scatter("spend", "tenure", c="churned")   # 探索可视化 ≠ 生产报表
```

- 公共数据集练习路径（20.2 教学法落地，题材为 2020 存量示意）：GitHub Archive（事件流→窗口聚合=天然 Ch.17 练习）→ NOAA 天气（时间序列可视化+外部知识 join）→  Census/ births（多表 join 与列裁剪账单实验）——每练习先 dry-run 记录字节再执行，把 Ch.4 肌肉与 Ch.20 素材缝在一起；
- notebook→生产晋升检查单：可复现（数据时点固定）→ 有断言（对账 SQL）→ 有 owner（模型/查询卡片）→ 有预算（调度后估算）→ 有退役条款（无人消费即下线）；五条缺一条不晋升（15.2 消费者合同的 ML 特例）；
- 思考题（5 道）：T1 仓内训练对「特征-训练-服务」三处的搬运成本各省在哪？T2 `ML.PREDICT` 结果落表后与 BI 的关系为何与普通表无异？T3 笔记本扫描费事故高发的组织根因？T4 公共数据集退役潮（见演进节）给「教学素材」形态什么警告？T5 把 E5 物化类比外推到「模型打分复用」的成立边界？

## 系列互链

- 同书纵向：特征 SQL 手艺 [05-仓库养护与查询开发.md](05-仓库养护与查询开发.md)；训练成本 [02-数据盘点与成本管控.md](02-数据盘点与成本管控.md)；模型资产治理 [08-数据治理与长期适应.md](08-数据治理与长期适应.md)；模型质量进报表 [09-报表仪表板与DataStudio.md](09-报表仪表板与DataStudio.md)。
- 他书横向：湖仓上的表格模型工作流对位 [../Data_Lakehouse_in_Action/00-总览与阅读地图.md](../Data_Lakehouse_in_Action/00-总览与阅读地图.md)；Spark ML 出仓训练谱系对照读物 [../Spark_The_Definitive_Guide/00-总览与阅读地图.md](../Spark_The_Definitive_Guide/00-总览与阅读地图.md)（「仓内训练 vs 出仓训练」两极，盘上已验名；同波 Spark 诸册 #216/#196/#193/#194 按兄弟规则只登记于 00）。

## 核心概念速览（中英对照）

- **BQML** — BigQuery ML：以 CREATE MODEL SQL 在仓内训练/评估/打分的托管 ML 层。
- **模型即对象** — Model as Warehouse Object：模型与表/视图同层级共享 IAM 与目录。
- **训练查询** — Training Query：喂给 CREATE MODEL 的特征 SELECT，账单=扫描量。
- **ML.PREDICT** — ML.PREDICT：对模型即席批量打分的表函数。
- **ML.TRAINING_INFO** — Training Info：迭代-损失-超参的训练史系统视图。
- **自动调参** — HP Tuning：CREATE MODEL 选项触发的交叉验证网格搜索。
- **矩阵分解** — matrix_fact：仓内协同过滤基线模型（2020 谱系成员）。
- **Colab** — Colab：托管笔记本环境，与 GCP 认证打通的探索入口。
- **大magic** — %%bigquery：IPython 单元格级查询语法糖。
- **Arrow 行集** — Arrow RecordBatch：BQ→pandas 的列式零拷贝传输通道。
- **公共数据集** — Public Datasets：免注册直读的第三方托管数据目录。
- **晋升通道** — Notebook-to-Production：探索查询产品化为调度资产的过程。

## 最新演进与工业实践

- **BQML 谱系大扩容（2021–2026）**：`FORECASTING/ARIMA_PLUS`（2022 GA，含节假日 regressor）、`xgboost/tfdf` 内置化、导入外部模型（`IMPORTED_MODEL`，ONNX/TF）、**远程模型/LLM 函数**（`ML.GENERATE_TEXT` 系接 Vertex，2023–2024）、向量嵌入与相似检索（`AI.GENERATE_EMBEDDING`/向量检索 2024，✅ https://docs.cloud.google.cn/bigquery/docs/vector-search 镜像 200）；模型目录从「80% 甜区」扩到生成式面——19 章的边界裁定需整体刷新 ⚠️（canonical 文档不可直连，转述）。
- **Notebook 产品化**：BigQuery Enterprise Notebooks/Dataframes（BigQuery DataFrames 以 polars 引擎提速，2022–2023 ⚠️ 转述）——20 章「Colab+客户端」组合升格为托管 IDE；Colab 本体仍可用（社区文档线）。
- **公共数据集退役潮（2023–2025）**：`bigquery-public-data` 部分数据集向 Analytics Hub 共享目录迁移、若干老牌数据集（GitHub Archive 等）宣布退役/转归档 ⚠️——**20 章的教学素材池本身经历了「适应长期变化」的活案例**，恰好验证 Ch.15 的文档时效性风险论（见 [08-数据治理与长期适应.md](08-数据治理与长期适应.md)）。
- **工业实践（2024–2026）**：仓内基线模型+LLM 特征（文本理解列）成为表格 ML 新常态；「训练查询必须 dry-run 审批」进入各厂 FinOps 门禁清单；notebook→生产的晋升通道由 Vertex Pipelines/dbt 测试双轨承接（对位 [../Analytics_Engineering_with_SQL_and_dbt/00-总览与阅读地图.md](../Analytics_Engineering_with_SQL_and_dbt/00-总览与阅读地图.md)）。
