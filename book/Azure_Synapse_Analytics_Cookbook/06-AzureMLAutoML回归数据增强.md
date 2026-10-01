# 06 Azure ML AutoML 回归数据增强 — Enriching Data Using the Azure ML AutoML Regression Model（原书第 6 章）

> 章题 ✅ Packt 官方 ColorImages PDF 文本层实抓；配方级小节 ⚠️ 推定（一手旁证 = 官方仓库
> `chapter 6/code` 文件夹名：import azureml core / define dataset / define automl config /
> run experiment / create sp.sql——五文件夹几乎逐一对应一条配方）。机制 = Microsoft Learn
> 转述 ⚠️ + ✅ URL（2026-10-02 `curl -sI` 200）；Azure 不可实测 ⚠️；azureml SDK 本机
> 不可装（零新装红线），🔧 仅以 SQLite/DuckDB 类比「特征表+打分」形态，**非平台行为**。

## 6.1 「数据增强」的定位：用预测列补全事实

章题语义（⚠️ 重构口径）：不是搬运数据，而是**给表加一列模型输出**（如缺失指标推算、
未来值预测），让下游报表直接用「增强后事实」。回归模型 = 连续目标（README 特性句
「Work with notebooks for various tasks, including ML」✅ 实抓的展开章）。

## 6.2 集成面：Synapse 工作区链接 Azure ML

✅ `azure/synapse-analytics/machine-learning/what-is-machine-learning` ⚠️ 转述：工作区
「管理→Azure ML」链接既有 ML 工作区（计算目标/数据集共享）；✅
`machine-learning/quickstart-integrate-azure-machine-learning` 给最小配方。笔记本内
`import azureml.core`（✅ 文件夹名实抓）后以 SDK 操作工作区对象 ⚠️。

## 6.3 五步 AutoML 回归配方（对位仓库文件夹逐一展开 ⚠️）

1. **import azureml core**：`Workspace.get(...)`/`Experiment` 句柄 ⚠️；
2. **define dataset**：从专用池/湖上表注册 TabularDataset（SQL 数据集=查询+凭据）⚠️；
3. **define automl config**：`AutoMLConfig(task='regression', primary_metric='normalized_root_mean_squared_error', n_iterations=...)` 语义 ⚠️——AutoML 自动做模型族搜索+特征预处理+超参；
4. **run experiment**：提交到训练计算目标，`run.get_details()` 取排行榜最优模型 ⚠️；
5. **create sp.sql**：把最优模型封装成 T-SQL 打分存储过程——对应官方
   ✅ `azure/synapse-analytics/sql-data-warehouse/sql-data-warehouse-predict`（`sp_predict`
   一键用已注册 ML 模型对查询结果打分 ⚠️）与打分向导
   （✅ toc 实抓 machine-learning/tutorial-sql-pool-model-scoring-wizard）。

「增强」闭环：`EXEC sp_predict 'SELECT ...'` 把预测值作为新列写回增强表 → 07 章报表消费 ⚠️ 编者串联。

## 6.4 特征与目标：回归配方里的数据面

⚠️ 推定（对位本书出租车/温度题材）：目标列=连续量（时长/温度），特征=时间戳派生+
聚合统计；AutoML 的 `allowed_models/explain_model=True` 控制可解释面 ⚠️。
数据泄漏三查（编者归纳 ⚠️）：目标衍生列混入特征？时间边界穿越？训练/服务分布漂移？

## 6.5 打分形态的光谱（本章位置图 ⚠️ 编者归纳）

| 形态 | 引擎 | 新鲜度/延迟 | 适用 |
| --- | --- | --- | --- |
| 笔记本批量重打分（Spark） | 05 章 MLlib/SDK | 批 | 全量增强列 |
| `sp_predict` 库内打分 | 专用池 | 查询即算 | 中小规模、T-SQL 团队 ⚠️（✅ predict 页） |
| 物化增强表 | 池内表 | 批刷新 | 报表直读（07 章） |
| 在线端点（ML 服务） | Azure ML | 毫秒 | 应用侧推理（本书不展开 ⚠️） |

🔧**E7 侧证（非 Synapse）**：SQLite 内联视图每次全聚合 94.12ms vs 物化表+索引 0.08ms
（≈1180×）——「打分结果落表复用」优于「每次查询现算」的量级直觉；库内 `sp_predict`
的每次调用成本同理要按 QPS 折算 ⚠️。

## 6.6 MLOps 检查单（编者归纳 ⚠️）

1. 训练数据集版本固定（Dataset version）可回溯吗？
2. 最优模型注册表命名/阶段（dev→prod）纪律？
3. 打分存储过程的权限面（谁可 EXEC）与资源类（内存重）配了吗（03 章 3.6）？
4. 漂移监控与重训触发器（周期/指标阈值）？
5. 增强列进目录打标签了吗（08 章治理衔接）？

## 6.7 与 repo 其他章/册的联系

- 训练/打分宿主笔记本 → [05-SynapseNotebook与Spark数据工程.md](05-SynapseNotebook与Spark数据工程.md)；
- 增强表消费 → [07-PB级可视化报表与物化视图.md](07-PB级可视化报表与物化视图.md)；
- 权限与密钥 → [08-数据目录与治理.md](08-数据目录与治理.md)；
- 论文线根基：模型评估/特征工程经典文献走 [../../db/db.md](../../db/db.md)（跨域指路，
  本册主题偏工程）；
- 治理面同题册（跨波实链 ✅ 验名）：[../Data_Governance_in_the_Era_of_AI_2e/00-总览与阅读地图.md](../Data_Governance_in_the_Era_of_AI_2e/00-总览与阅读地图.md)——ML 资产治理的更广视角。

## 6.8 回归配方的数据画像（⚠️ 重构口径）

AutoML 回归任务对输入表的三前提（对位 6.3 步 2 的 TabularDataset 定义 ⚠️）：

1. **目标列单列连续**：无缺失、量纲统一（温度/时长/金额三型对应本书样本题材）；
2. **特征列全数值化就绪**：类别列先 one-hot/编码（AutoML 预处理可代劳但训练服务
   两侧要一致 ⚠️）；时间列派生周期特征（小时/星期/节假日）；
3. **行粒度=预测粒度**：增强列回写时按什么键 JOIN 回事实表，训练时就按什么粒度造样。

样本量与切分 ⚠️：AutoML 默认随机切分，时序问题改**按时间边界切**（6.4 泄漏三查
第 2 项的落地）；`n_iterations` 控制搜索预算——排行榜前 5 名通常已收敛。

## 6.9 打分存储过程骨架（示意 SQL，编者按 Learn 语义改写，**非书中原文** ⚠️）

```sql
-- 注册：把 AutoML 最优模型登记进专用池（语义对位 sp 系管理过程 ⚠️）
EXEC sp_create_ml_model @name = N'reg_model_v1', ... ;   -- 参数面以现行文档为准
-- 打分：对查询结果集批量预测，输出增强列
EXEC sp_predict @model_name = N'reg_model_v1',
     @query = N'SELECT id, f1, f2, f3 FROM staging.features_daily';
-- 增强：预测列并入报表消费表（07 章直读面）
CREATE TABLE fact_enriched AS
  SELECT a.*, p.prediction AS est_value
  FROM fact a LEFT JOIN #predict_result p ON a.id = p.id;
```

三注意 ⚠️：①`sp_predict` 内存重，归大资源类（6.6 项 3 ↔ 03 章 3.6）；②模型版本
入表名/列名（`_v1`）留升级缝；③批量打分后统计重建（03 章 3.5 同理）。

## 核心概念速览（中英对照）

- **数据增强** — Data enrichment：以模型预测列补全事实表 ⚠️ 章题语义重构。
- **AutoMLConfig（回归）** — 自动模型搜索+预处理+超参，主指标 RMSE 族 ⚠️。
- **TabularDataset** — ML 工作区数据集抽象（SQL/湖两源）⚠️（✅ 文件夹名旁证）。
- **实验排行榜** — Experiment run details：最优模型选择面 ⚠️。
- **sp_predict** — 专用池 T-SQL 打分存储过程 ⚠️（✅ sql-data-warehouse-predict）。
- **打分向导** — Scoring wizard（专用池）：无代码注册+封装路径 ⚠️（✅ toc 实抓）。
- **模型注册/阶段** — Model registry dev→prod：MLOps 纪律面 ⚠️ 编者归纳。
- **数据泄漏三查** — Leakage checklist：衍生列/时间穿越/漂移 ⚠️ 编者归纳。

## 最新演进与工业实践

2022→2026（URL 均 ✅ 200；状态 ⚠️ 转述）：

- **SDK v1→v2 代际**：本书用 `azureml.core`（v1 风格，✅ 文件夹名），现行 Azure ML 文档
  主推 v2 SDK/CLI 与「数据科学」产品线，v1 进入弃用轨道 ⚠️——配方语义不变、API 面重写。
- **Synapse ML 入口收缩**：`machine-learning/what-is-machine-learning` 页仍在（✅），但
  新功能重心移向 Fabric 数据科学项与独立 Azure ML 工作室 ⚠️；`sp_predict` 系能力保留在
  专用池文档线（✅ predict 页现行）。
- **AutoML 现状**：任务类型/终止策略/LLM 辅助特征等能力在 Azure ML 文档持续演进 ⚠️
  （✅ `azure/machine-learning/overview-what-is-azure-machine-learning` 为现行总览入口，
  本波验证 200）。
- **工业实践**：「增强列」模式在 Feature Store 语境下制度化（离线批增强 + 在线低延迟
  打分双面）；库内打分（sp_predict 型）适合 BI 就近消费，特征一致性由注册表兜底 ⚠️。
- 🔧 数字口径：E7 为 SQLite 本机实测，仅证「预计算复用 vs 现算」量级差，**非 Synapse/
  Azure ML 行为**；azureml SDK 未装未测（零新装红线）。
