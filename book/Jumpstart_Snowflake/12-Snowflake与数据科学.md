# 12 Snowflake and Data Science（pp.213–228 ✅ Crossref）

> 章定性：消费矩阵的 DS 列展开——数据科学家如何"少搬数据"地用上云仓：拉取式工具链、
> 仓内计算雏形、ML 工程化的 2019 快照。章题/页码 ✅ Crossref `_12`；小节 ⚠️ 推定；代码自拟
> 示意；机制 ⚠️ 转述 + ✅ curl-200 URL；本章无独立 🔧（特征工程素材见 09 章实验）。

## 1. 章节定位与叙事线

2019 时点的现实：Snowflake 尚无 Python UDF（2020-05 GA ⚠️ 年代线）、无 Snowpark（2022 GA ⚠️），
数据科学协作=「SQL 做重活 + 客户端 Python/R 做模型」的拉取式范式。本章叙事链 ⚠️ 推定：
DS 工作流痛点（数据搬运/隐私/复现）→ 用 SQL+VARIANT（09 章）做特征工程 → connector/
pandas 生态限量拉数 → notebook（Jupyter ⚠️ 时代主流）侧训练 → 结果回写表供 BI 消费 →
仓外 ML 服务通过**外部函数**调用（当年 AWS SageMaker 集成样板 ⚠️）→ 治理提醒（角色 08 章、
仓库 03 章配额）。

## 2. 知识提纲（⚠️ 推定小节）

| # | 推定小节 | 2019 形态 | 现状锚点（✅ curl-200） |
| --- | --- | --- | --- |
| 1 | DS×云仓矛盾论 | 数据大、模型小、要复现 | guides-overview-ai-features（反照） |
| 2 | SQL 特征工程 | VARIANT 展平+窗口函数 | querying-semistructured |
| 3 | 拉取式训练 | Python connector+chunked fetch | developer-guide/snowpark（对照） |
| 4 | 结果回写 | 小表/PUT 上传 | copy-into-table |
| 5 | 外部函数雏形 | SageMaker 调用打分 | （2019 专页未验真 ⚠️） |
| 6 | 环境与时限 | DS 仓配额+资源监视器 | resource-monitors |
| 7 | 复现与血缘 | Time Travel 定版数据 | user-guide/data-time-travel |

## 3. 深读与机制重构

**（a）拉取式管道样板（自拟示意，非书中原文）**：

```sql
-- 仓内：特征表（09 章手法 + 窗口函数）
CREATE TABLE ml.f_user_features AS
SELECT user_id,
       count(*)                              AS n_orders_30d,
       sum(amount) / count(distinct day)     AS avg_daily_spend,
       avg(payload:basket.value:size::INT)   AS basket_trend      -- JSON 特征
FROM sales.core.orders, LATERAL FLATTEN(...)                     -- 示意省略
WHERE day >= dateadd('d', -30, current_date())
GROUP BY user_id;
```

```python
# 客户端：分批拉取，避免"SELECT * 全量拖库"
# （2019 = connector-python；today 同位 = Snowpark fetch / 仓内训练 ⚠️）
from snowflake.connector import connect            # 包名示意，非本书代码
cur = ctx.cursor()
cur.execute("SELECT * FROM ml.f_user_features")
df = cur.fetch_pandas_all()                        # 时代 API 口径 ⚠️ 转述
```

**（b）为什么 2019 要"把 ML 请出仓库"**：仓内执行面只有 SQL/JS UDF ⚠️，Python 生态（sklearn/
XGBoost）进不来；外部函数（external function → API Gateway → SageMaker）是当年唯一的"仓内触发
仓外模型"通道，打分场景可用、运维重 ⚠️（专页未验真，按时代转述登记）。

**（c）复现性武器=Time Travel**：训练集用 `AT => TIMESTAMP(...)` 克隆定版（14 章机制在此兑现
第一个业务价值）✅ https://docs.snowflake.com/en/user-guide/data-time-travel——本章把它用作
"数据版本控制"卖点 ⚠️ 推定同书立场。

**（d）DS 的资源纪律**：为 DS 单切仓库（11 章拓扑）、挂监视器（07 章）、用按需尺寸（03 章）——
数据科学是"最贵的临时查询"高发区 ⚠️+✅ resource-monitors。

## 4. 深读问答（自拟）

**Q1：拉取式的两个天花板？** A：隐私合规（数据出院）与规模（特征表大于内存）——正是 2020+
仓内 Python/Snowpark 要拆的墙 ⚠️+✅ developer-guide/snowpark。
**Q2：特征放仓内还是特征库？** A：2019 本章立场偏仓内 SQL 特征表；行业后来分化出特征平台
（含 Snowflake Feature Store ⚠️ 后时代产品，sitemap 在录、未逐一验真）。
**Q3：本章内容今天还剩多少？** A：方法论层（少搬数、快定版、贵配额）完整保留；工具层几乎全换
——见演进节五条。

## 5. 与其他书/章联系

- 09（特征原料）、11（消费矩阵定位）、14（定版复现）强耦合；03/07（配额纪律）。
- [../Snowflake_The_Definitive_Guide/00-总览与阅读地图.md](../Snowflake_The_Definitive_Guide/00-总览与阅读地图.md)：UDF/connector 参考面（波1 ✅）；[../Tuning_the_Snowflake_Data_Cloud/00-总览与阅读地图.md](../Tuning_the_Snowflake_Data_Cloud/00-总览与阅读地图.md)：DS 负载成本画像（波8 ✅）；[../Advanced_Snowflake/00-总览与阅读地图.md](../Advanced_Snowflake/00-总览与阅读地图.md) ⚠️ 降级册仅辨析（AI 负载推定章）。

## 6. 本章检验点

1. 复述"仓内特征→客户端训练→回写消费"的三段管道。
2. 说出 2019 仓内计算的两个合法位点（SQL 加工 + 外部函数调用）。
3. 解释 Time Travel 在 ML 复现中的角色。
4. 给 DS 团队设计"仓库+监视器+角色"三元组（11 章公式应用）。

## 7. 工具链年表卡（本章↔2026）

| 年份 | 事件 | 对本章含义 |
| --- | --- | --- |
| 2019 | 本书出版：SQL+外部函数 | 拉取式为主 ✅ 章题 |
| 2020 | Python UDF/SP + Anaconda ⚠️ | "仓内跑 sklearn"成为可能 |
| 2022 | Snowpark GA ⚠️+✅ snowpark |  DataFrame API 进仓 |
| 2023+ | ML Functions/Feature Store ⚠️+✅ forecasting 页 | SQL 直接调用训练/预测 |
| 2024+ | Cortex AISQL 线 ⚠️+✅ ai-features | LLM 函数进 SELECT |

## 8. 取证与标注说明

章题/页码 ✅ Crossref `_12`（pp.213–228）；✅ URL（curl-200）：developer-guide/snowpark、
udf/python/udf-python-batch、ml-functions/forecasting、guides-overview-ai-features、
guides-overview-ml-functions、data-time-travel、resource-monitors、querying-semistructured；
Python connector API 细节、外部函数/SageMaker 集成与"本书主张"均 ⚠️ 时代转述（未获样章）；
代码为自拟示意。

## 核心概念速览（中英对照）

| 中文 | 英文 | 一句话释义 |
| --- | --- | --- |
| 拉取式 ML | fetch-based ML | 数据到客户端训练的反向管道 |
| 特征工程 | feature engineering | 从原料造模型输入的工序 |
| 特征表 | feature table | 仓内沉淀的可复用特征 |
| 外部函数 | external function | 仓内触网调用远端模型的钩子 ⚠️ |
| 数据定版 | data versioning | Time Travel 快照训练集 |
| 配额纪律 | quota discipline | DS 高开销负载的护栏 |
| 仓内计算 | in-warehouse compute | UDF/Snowpark 时代的正解 |
| 结果回写 | score writeback | 预测值以最小面入库供 BI |
| 复现 | reproducibility | 数据+代码+环境三定版 |
| ML 工程化 | MLOps（后时代词） | 本章痛点的制度化答案 |

## 最新演进与工业实践

- **仓内 Python 生态**：Python UDF/存储过程+Anaconda 依赖面，2019"请出仓库"翻转为"把库请进
  仓库" ✅ https://docs.snowflake.com/en/developer-guide/udf/python/udf-python-batch。
- **Snowpark**：DataFrame API 多语言进仓，拉取式退化为小样本特例 ✅
  https://docs.snowflake.com/en/developer-guide/snowpark；容器服务（Snowpark Container
  Services ⚠️）承接大训练负载。
- **SQL 即 ML**：AI/ML 函数族把分类/预测/嵌入写进 SELECT ✅
  https://docs.snowflake.com/en/user-guide/ml-functions/forecasting ✅
  https://docs.snowflake.com/en/guides-overview-ml-functions ✅
  https://docs.snowflake.com/en/guides-overview-ai-features。
- **Agent 化消费**：Snowflake Intelligence（2025-08 首发）把自然语言分析做成 DS/BI 融合面 ✅
  https://docs.snowflake.com/en/release-notes/2025/other/2025-08-01-snowflake-intelligence。
- **工业实践**：2026 团队把本章三段管道改写为"仓内特征+仓内训练小模型+仓外大模型走 AISQL/
  代理层"；数据定版习惯保留（Time Travel/克隆成本低、审计价值高 ⚠️+✅ data-time-travel）。
