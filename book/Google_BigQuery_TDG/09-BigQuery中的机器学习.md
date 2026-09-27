# 09 BigQuery中的机器学习（原书第 9 章 · Machine Learning with BigQuery / BQML）

> 章首注：原书页区间 ⚠️ 推定 p.321–370；一级章题 ✅ 目录实抓（配套仓库 `09_bqml` ✅）；
> **本章二级小节 ⚠️ 推定**——按配套代码 `09_bqml/` ✅ 实抓文件族（bqml_*.sql 训练/评估/预测 SQL）
> 与官方 BQML 文档页组织。BigQuery ML 的核心卖点是**用 SQL 做 ML**——无需导出数据到外部 ML 平台。

## 本章地图（⚠️ 推定结构，锚点为 ✅ 配套文件 + 官方文档主题）

| 组 | 小节主题 | 锚点 |
| --- | --- | --- |
| BQML 总纲 | SQL 内训练/评估/预测的闭环 | ⚠️ 官方 BQML 概览页 |
| 监督学习 | 线性回归/逻辑回归/DNN 分类与回归 | ✅ bqml_*.sql 训练 SQL |
| 特征工程 | ML.TRANSFORM、预处理、特征哈希 | ⚠️ |
| 模型评估 | ML.EVALUATE、ROC/AUC/RMSE | ✅ bqml_*.sql 评估 SQL |
| 预测 | ML.PREDICT、批量/在线预测 | ✅ bqml_*.sql 预测 SQL |
| 无监督学习 | K-means 聚类、PCA 降维（2024+ ⚠️） | ⚠️ |
| 模型管理 | CREATE MODEL、模型版本、IAM 权限 | ⚠️ |
| 外部模型导入 | TensorFlow/ONNX/XGBoost 导入 BQML | ⚠️ |
| 与 Vertex AI 协同 | BQML ↔ Vertex AI 模型注册表 | ⚠️ |

## 核心精讲

### 1. "用 SQL 做 ML"——BQML 的第一性原理（⚠️ 转述）

传统 ML 流程：导出数据 → Python/R 训练 → 部署模型服务 → 应用调用。
BQML 的颠覆：**训练和预测都在 SQL 里完成**——数据不出 BigQuery。

```sql
-- 自拟教学示意（非原书文本）：BQML 训练闭环
CREATE MODEL `dataset.my_model`
OPTIONS(model_type='LOGISTIC_REG', input_label_cols=['label']) AS
SELECT feature1, feature2, label
FROM `dataset.training_data`;

-- 预测
SELECT * FROM ML.PREDICT(MODEL `dataset.my_model`,
  (SELECT feature1, feature2 FROM `dataset.new_data`));
```

⚠️ 适用场景：表格数据的监督学习（分类/回归）、特征工程在 SQL 内完成；
不适用：图像/音频/非结构化深度学习（需 Vertex AI）。

### 2. 特征工程：ML.TRANSFORM（⚠️ 转述）

```sql
-- 自拟教学示意（非原书文本）：预处理管道
CREATE MODEL `dataset.preprocess`
TRANSFORM(
  feature1 AS NUMERIC(SCALE=1),
  ML.ONE_HOT_ENCODE(category_col) AS encoded,
  ML.MIN_MAX_SCALE(numeric_col) AS scaled
)
OPTIONS(model_type='LOGISTIC_REG', input_label_cols=['label']) AS
SELECT * FROM `dataset.raw_data`;
```

⚠️ `TRANSFORM` 子句把预处理逻辑**绑定到模型**——预测时自动复用同一变换，
解决了原书提及的"特征 schema 漂移是 BQML 训练事故主因"（04 章模式演化节呼应）。

### 3. 模型评估（✅ 配套仓库 bqml_*.sql）

配套仓库 `09_bqml/` 的评估 SQL（✅ 实抓注释标题）：

```sql
-- 配套仓库风格示意（非原书文本）
SELECT * FROM ML.EVALUATE(MODEL `dataset.my_model`,
  (SELECT * FROM `dataset.eval_data`));
-- 输出：precision/recall/accuracy/roc_auc/rmse 等指标行
```

⚠️ ML.EVALUATE 返回标准指标表——分类模型含混淆矩阵行、回归模型含 RMSE/MAE/R²。
03 章的近似聚合函数（APPROX_*）在大表评估时可节省计算成本（07 章视角）。

### 4. 无监督学习与模型导入（⚠️ 转述）

- **K-means 聚类**：`CREATE MODEL ... OPTIONS(model_type='KMEANS')`——无需标签列；
- **外部模型导入**：TensorFlow SavedModel / ONNX / XGBoost 可导入 BQML 直接用 SQL 预测
  （⚠️ 格式支持范围以官方 BQML 文档为准）；
- **Vertex AI 集成**：BQML 模型可注册到 Vertex AI Model Registry→跨平台部署（⚠️ 2026 状态以官方文档为准）。

### 5. 模型管理与权限（⚠️ 转述）

- 模型是 BigQuery 数据集内的**一等对象**——有 IAM 权限、可共享、可版本化；
- `CREATE MODEL` / `ALTER MODEL` / `DROP MODEL` 构成完整生命周期；
- ⚠️ 训练消耗计算资源（按字节扫描 + 训练时间计 ⚠️）——大表训练的成本意识（07 章）。

## 常见误区（⚠️ 转述）

| 误区 | 事实 |
| --- | --- |
| BQML 替代 Python ML | BQML 适合表格数据 SQL 内闭环；复杂深度学习仍需 Vertex AI/外部框架 |
| 训练免费 | 训练消耗计算资源（扫描字节 + 训练时间 ⚠️），大表训练成本显著 |
| 特征漂移无所谓 | TRANSFORM 绑定模型可缓解；手动特征管道漂移是事故主因（04 章） |
| 导入模型即插即用 | 导入模型的输入 schema 必须匹配；特征不一致则预测失败 |
| ML.PREDICT 只支持批量 | BQML 支持批量预测；在线低延迟预测需 Vertex AI Endpoints（⚠️） |
| 模型无权限管理 | 模型是数据集内对象，受 IAM 管控（10 章治理面） |

## 与其他章、其他书联系

- 特征工程所需的函数族 → [03-数据类型函数和运算符.md](03-数据类型函数和运算符.md)；训练数据的装载 → [04-将数据加载到BigQuery.md](04-将数据加载到BigQuery.md)。
- 开发工具（notebook 训练脚本）→ [05-使用BigQuery进行开发.md](05-使用BigQuery进行开发.md)；模型权限 → [10-BigQuery安全管理.md](10-BigQuery安全管理.md)。
- 训练成本意识 → [07-性能与成本优化.md](07-性能与成本优化.md)（槽位/字节双维）。
- 云仓 ML 对读：Snowflake Snowpark ML（⚠️ 盘上若有对应笔记待补链）；
  传统 ML 工程底座：[../bigdata/12-数据质量与工程实践.md](../bigdata/12-数据质量与工程实践.md)。
- 本机 DuckDB 环境：[../DuckDB_in_Action/04-高级聚合与数据分析.md](../DuckDB_in_Action/04-高级聚合与数据分析.md)（特征工程的 SQL 聚合基础）。

## 核心概念速览（中英对照）

| 术语 | English | 释义 |
| --- | --- | --- |
| BQML | BigQuery ML | SQL 内训练/评估/预测的 ML 能力 |
| CREATE MODEL | CREATE MODEL | SQL DDL 创建 ML 模型 |
| ML.PREDICT | ML.PREDICT | SQL 函数，用模型做预测 |
| ML.EVALUATE | ML.EVALUATE | SQL 函数，评估模型指标 |
| ML.TRANSFORM | TRANSFORM clause | 预处理管道绑定到模型（防特征漂移） |
| 逻辑回归 | logistic regression | BQML 内置分类算法 |
| 线性回归 | linear regression | BQML 内置回归算法 |
| DNN | deep neural network | BQML 内置深度学习能力 |
| K-means | K-means clustering | BQML 内置无监督聚类 |
| 模型注册表 | model registry | Vertex AI 统一模型管理 |
| 特征漂移 | feature drift | 训练/预测时特征 schema 不一致（⚠️ 事故主因） |
| 导入模型 | imported model | TensorFlow/ONNX/XGBoost 外部模型导入 BQML |
| Vertex AI | Vertex AI | GCP 统一 ML 平台，BQML 的进阶延伸 |

## 最新演进与工业实践

- **AI.GENERATE / AI.EMBED 函数族（2024-2026 ✅ 版本说明实抓）**：BQML 的边界从"传统 ML"扩到
  "LLM in SQL"——`AI.GENERATE` 调 Gemini、`AI.EMBED` 生成嵌入向量，直接在 SQL 内完成推理。
- **向量检索 GA（2026-07 ✅）**：`VECTOR_SEARCH` 支持 HYBRID 模式——BQML 嵌入 + 向量检索闭环在引擎内完成。
- **Gemini 嵌入模型更新**：2026-04 官方支持 `gemini-embedding-2-preview` 多模态嵌入
  （文本/图/音/视频/PDF ✅ 版本说明实抓）——原书 2019 的"BQML = 表格 ML"定义已大幅扩展。
- **AutoML 集成**：BigQuery 内 AutoML 训练（⚠️ 以官方文档为准）使"SQL 一键训练"从显式算法选择
  扩展到自动算法搜索。
- **工业实践**：BQML 的典型定位是"表格数据快速实验 + 特征工程闭环"；
  生产级深度学习/大规模推理仍走 Vertex AI Endpoints——二者通过 Model Registry 桥接。
  对读 Snowflake Snowpark ML 同题演进（⚠️ 盘上若有对应笔记待补链）。
