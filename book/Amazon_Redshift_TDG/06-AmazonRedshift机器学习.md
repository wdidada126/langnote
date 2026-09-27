# 06 Amazon Redshift 机器学习（Chapter 6: Amazon Redshift Machine Learning ⚠️ 英题推定）

> 精读重构笔记，非原书文本。Redshift ML/SageMaker 行为一律 ⚠️ 转述 + ✅ 文档 URL（curl 2026-09）；🔧 为本机 DuckDB/SQLite 类比，**非 Redshift 行为**。

## 1. 本章骨架（✅ 译文实抓）

- 6.1 机器学习周期（ML lifecycle 教科书化开场）
- 6.2 Amazon Redshift ML：灵活性 / 开始使用（CREATE MODEL 主线）
- 6.3 机器学习技术：监督学习 / 无监督学习
- 6.4 机器学习算法（名录式过场）
- 6.5 与 Amazon SageMaker Autopilot 的集成：创建模型 / 标签概率 / 解释模型
- 6.6 使用 Amazon Redshift ML 预测学生的结果（全书案例主线落地段）
- 6.7 Amazon SageMaker 与 Amazon Redshift 集成（双向）
- 6.8 Amazon SageMaker 集成——自定义模型（BYOM）：BYOM 本地 / BYOM 远程
- 6.9 Amazon Redshift ML 成本
- 6.10 摘要

## 2. Redshift ML 一句话机制（⚠️ 转述 + ✅ URL）

在 SQL 里 `CREATE MODEL m FROM (SELECT features, label FROM 表)`：
Redshift 把训练样本交给 **SageMaker Autopilot** 自动选算法/调参/训练，模型注册回仓内；
推理用 SQL 函数 `m.predict(...)`（批量）或 `m.predict_proba(...)`（带概率），全程不离开 SQL。
✅ https://docs.aws.amazon.com/redshift/latest/dg/r_CREATE_MODEL.html （200）。
默认 IAM 角色打通 S3 工件桶 + VPC 端点（⚠️ 转述；加密页 ✅ https://docs.aws.amazon.com/redshift/latest/mgmt/security-encryption.html 200 可佐证书加密侧）。

## 3. 为什么"仓内 ML"成立（本章论点重构，⚠️ 转述+评价）

- 数据不出仓：特征即 SQL 视图，省一半管道与治理成本；
- 决策离数据最近：预测作为 SELECT 列参与报表（"成绩预测列"随 BI 查询下发）；
- 代价：模型生态受限于 Autopilot 能力 + BYOM 通道；深度/大模型场景仍回 SageMaker 主场；
- 书中教学段（6.3/6.4）是通识摘要：监督 vs 无监督、回归/分类/异常——对位盘上任何 ML 通识册都比本章深，本章价值在"SQL 门面"这个切面（⚠️ 评价）。

## 4. BYOM：本地与远程（⚠️ 转述）

- **BYOM 本地**：训练好的模型（如 XGBoost/Sklearn 序列化工件）注册进 Redshift ML 在仓侧推理容器调用 ⚠️ 细节口径；
- **BYOM 远程**：预测请求经 SageMaker endpoint / HTTPS 外呼（Lambda 中转口径 ⚠️），延迟敏感场景慎用；
- 双向集成（6.7）：SageMaker 侧用 Redshift 作为特征源/数据连接器（⚠️ 转述——2025 后该线被"SageMaker 统一数据体验"吸收，见演进节）。

## 5. 案例段：预测学生结果（✅ 小节实抓）

沿用 Ch3 学生数据集：特征（出勤/作业分）→ 标签（结果分级）→ CREATE MODEL → 用 predict_proba 出成绩单 + 解释小节看特征重要性（SHAP 口径 ⚠️ 转述）。
成书快照里模型卡输出含"验证精度 0.8706、预计成本 29.81"字段（✅ 译文样例实抓——数字仅为 2024-03 玩具例）。

## 6. 🔧 本机类比（DuckDB 1.5.5，**非 Redshift 行为**）

- "预测即 SQL 列"的直觉演示：DuckDB 里把线性回归系数（手工/最小二乘 SQL 解出）当常量注入 SELECT，`score*a+b` 直接作为查询列——这就是 predict() 的裸形态；真实 Redshift 由 Autopilot 托管训练+函数下推（⚠️）；
- "特征即视图"演示：CREATE VIEW features AS SELECT… 再对视图跑聚合，与 CREATE MODEL FROM (SELECT…) 同构——仓内 ML 的第一性原理=**特征管道复用 SQL 引擎本身**；
- 本机不可类比处（诚实 ⚠️）：训练编排、IAM 工件面、推理容器计费——全部转述。

## 7. 三巨头对位（⚠️ 评价）

- Snowflake Cortex（LLM 函数 SQL 化）vs Redshift ML（经典 ML SQL 化）vs BigQuery BQML（SQL 训练+ML.GENERATE 全家）——
  Redshift 起步最晚、SKU 最少，但 BYOM 通道 + SageMaker 母体是其差异化背书；
- 本书出版时（2024）生成式尚未进入 Redshift 门面，2025+ 由 Bedrock/Q 系列补位（见演进节）；
- 向量检索需求（embedding 落仓）三家 2024-2026 陆续补：盘上专题见 [../Vector_Databases/00-总览与阅读地图.md](../Vector_Databases/00-总览与阅读地图.md)。

## 8. 疑点与缺口

- Redshift ML 支持的目标算法清单（Autopilot 内部候选集）未回核英文表格 ⚠️；
- 成本小节把训练（Autopilot 侧）与推理（RPU/集群侧）拆开讲，具体单价 2026 已变 ⚠️；
- "12 列"等译文碎片对应原文特征表，未逐列回核 ⚠️（不影响机制理解）。

## 9. CREATE MODEL 骨架复述（⚠️ 转述语法形态，非原文代码）

```sql
CREATE MODEL student_result
FROM (SELECT attendance, homework_score, final_result FROM student_features)
TARGET final_result
IAM_ROLE default
SETTINGS (s3_bucket '...', max_runtime '2h');
-- 训练异步：SYS_REDSHIFT_ML_MODELS 看状态 → READY
SELECT student_id, student_result.predict(attendance, homework_score) FROM ...;
SELECT *, student_result.predict_proba(attendance, homework_score) FROM ...;
```
- 本质是把 (feature SELECT, label) 交给 Autopilot + 把最佳候选注册回仓内 UDF；
- 模型即 SQL 函数=可进视图/MV/共享（与 Ch7 组合是本章隐藏考点 ⚠️ 评价）；
- 语法细节（模型类型/超参透传）未逐项回核英文 ⚠️，以 ✅ r_CREATE_MODEL.html（200）为准。

## 10. 仓内 ML 适用判定清单（⚠️ 评价性提炼）

- 适合：表格特征已在仓、批量打分、报表内嵌预测、治理敏感（数据不出域）；
- 勉强：特征工程需非 SQL 库（转 Glue/SageMaker 侧）、需要在线低延迟服务（endpoint 另建）；
- 不适合：深度/大模型训练、需要复杂 pipeline 版本治理——回 SageMaker 主场；
- 成本红线：训练走 Autopilot 账、推理吃仓 RPU/集群——**别让 ad-hoc 分析师随手 predict 全表**（⚠️ 实践告诫归纳）。

## 11. 自测三题（合书作答，⚠️ 依本章要点）

1. Redshift ML 的训练发生在哪？——SageMaker Autopilot（CREATE MODEL 异步委托），仓内只留模型对象与函数门面；
2. predict 与 predict_proba 的选择场景？——标签进报表用前者，需要置信度做阈值决策/排序用后者（标签概率小节）；
3. BYOM 远程的最大风险？——网络往返+外部 endpoint 可用性把 SQL 延迟变成不可预测，且数据出仓面扩大需 Ch8 审计联动。

## 12. 与报表面的拼接（⚠️ 转述归纳）

- predict 列进视图 → QuickSight 直接消费"预测+事实"同屏——本章与 Ch2 BI 小节的隐藏连线；
- 模型版本意识：CREATE MODEL 同名重建即覆盖，治理上应 schema 隔离+命名带日期（书中未强调，⚠️ 实践补充）；
- 共享联动：含 predict 的视图经 datashare 递出时，推理算力落在消费方集群（⚠️ 转述，Ch7 同构）；
- 成本可见性：predict 大表=CPU 密集查询，纳入 Ch5 WLM 队列管理，别混在交互队列里。

## 核心概念速览（中英对照）

- Redshift ML — 仓内机器学习：CREATE MODEL→SageMaker 训练→SQL 推理的托管桥
- CREATE MODEL — 建模型语句：声明特征 SELECT 与目标列，异步训练至 READY
- predict / predict_proba — 预测函数：SQL 内调用模型出标签/带概率
- SageMaker Autopilot — 自动 ML：算法选择、调参、候选排名（Redshift ML 的训练引擎 ⚠️）
- BYOM — bring your own model：自带模型注册（本地工件/远程 endpoint 两式）
- 监督学习 — supervised learning：有标签拟合（本章学生案例主线）
- 无监督学习 — unsupervised learning：无标签聚类/异常发现
- 特征重要性 — feature importance / 解释模型：预测归因段（SHAP 口径 ⚠️）
- 标签概率 — label probability：多分类置信输出（predict_proba）
- 模型状态 READY — 模型就绪：异步训练完成标志（✅ 译文样例字段）
- 统一数据体验 — unified data experience：2025+ SageMaker×Redshift 融合叙事（见演进）
- 数据不出仓 — data stays in warehouse：仓内 ML 的核心卖点（治理+管道成本论）
- Autopilot 候选排名 — candidate ranking：多算法横评选出最佳模型的内部流程（⚠️ 转述）
- 解释性输出 — explainability：特征重要性/标签概率双件套（6.5 小节主题）
- 训练工件 — artifacts：S3 桶里的模型文件与元数据（BYOM 的落点 ⚠️）
- 推理 SQL 化 — inference in SQL：把 ML 服务降级为一个 SELECT 列的革命性平庸
- 异步训练状态机 — training status：CREATING→TRAINING→READY/FAILED 的可观测面（✅ 样例字段）
- 特征选择即 SQL — feature engineering as SQL：CREATE MODEL 的 FROM 子句=特征管道本体
- 模型即函数 — model-as-function：训练产物以 SQL 函数形态参与查询/视图/共享

## 最新演进与工业实践

- 2024→2026：Amazon Q 进入查询编辑器（自然语言生成/解释 SQL）与 Redshift ML 的"SQL 门面"叙事合流（⚠️ 转述，以 AWS 官网为准）；SageMaker HyperPod/统一目录使"仓做特征、SageMaker 做重训"成为官方推荐分形（⚠️ 转述）；
- 统一数据体验（AWS 2025 发布线）：SageMaker 与 Redshift 元数据/权限打通、跨服务共享目录——本章 6.7"双向集成"的正统续作；⚠️ 逐条日期未核，登记缺口；
- 向量/生成式补课：仓内 embedding 与向量检索能力 2024+ 路线（⚠️ 转述；盘上 [../Vector_Databases/00-总览与阅读地图.md](../Vector_Databases/00-总览与阅读地图.md) 有 ANN 原理纵览）；
- 工业实践：报表内嵌"预测列"（churn/LTV/成绩）是仓内 ML 最稳用例；训练重活仍归 SageMaker/离线管线（⚠️ 社区共识）；
- 取证：✅ r_CREATE_MODEL.html、security-encryption.html curl 200（2026-09）；Redshift ML 专章旧页 dg/redshift-machine-learning.html 实测 302→根（文档改版，✅ 登记）。
- 案例口径提醒（⚠️）：§5 的精度 0.8706 是 2024-03 玩具数据的快照值，教学演示产物——勿在评审材料中当作 Redshift ML 能力基准引用；
- 与兄弟册关系：SF 册 ML 面（Cortex）在其 12 章，本册 Ch6 与之对照读可见两家"SQL 门面"的代际差：2024 Redshift=经典 ML，2024 SF=LLM 函数优先（⚠️ 评价）。
