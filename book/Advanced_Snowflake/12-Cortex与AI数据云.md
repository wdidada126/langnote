# 12 · Cortex 与 AI 数据云（⚠️ 推定主题章，2026 演进义务主场）

> **性质声明**：推定主题重构（[00](00-总览与阅读地图.md)）。新书义务：即使成书于 2024/25，
> 本章按 2026-09 官方文档快照登记 AI 负载现状。机制=转述（⚠️）+✅URL；LLM 行为不可复算，无 🔧。
> TDG 对位：[../Snowflake_The_Definitive_Guide/12-数据云工作负载.md](../Snowflake_The_Definitive_Guide/12-数据云工作负载.md)（DS/ML 负载入门面）。

## 本章地图

| 节 | 内容 | 一句话结论 |
| --- | --- | --- |
| 12.1 | Cortex 版图：SQL 内的 AI 函数族 | "AI 是算子"而非"外挂服务" |
| 12.2 | AISQL 函数学：complete/classify/extract/translate/embed | 语义算子+治理原生的组合优势 |
| 12.3 | 区域可用性与配额 | 2026 文档专页化——合规第一关 |
| 12.4 | Cortex Analyst 与语义视图 | text-to-SQL 的"语义层锚"路线 |
| 12.5 | Cortex Agents | 工具面/技能面的智能体编成（2025+） |
| 12.6 | 向量：VECTOR 类型/Cortex Search | RAG 检索栈仓内闭环 |
| 12.7 | Document AI 与 UNSTRUCTURED 文本 | 第 6 章 VARIANT 的上游进水口 |
| 12.8 | Guardrails 与 AI 成本 | token 计费的暗物质化 |

## 核心精讲

### 1. AISQL 函数族（转述 ⚠️，✅ 正典页）
`AI_COMPLETE`/摘要/情感/翻译/`AI_EXTRACT`/`AI_CLASSIFY` 等以 SQL 函数形态在仓库内执行：
数据不出仓、RBAC/脱敏策略天然生效（第 10 章共振）、批处理可与裁剪/聚簇同一执行计划 ⚠️。
✅ https://docs.snowflake.com/en/user-guide/snowflake-cortex/aisql
✅ https://docs.snowflake.com/en/user-guide/snowflake-cortex/aisql-privileges-and-access （前波已证）
✅ https://docs.snowflake.com/en/user-guide/snowflake-cortex/aisql-regional-availability
✅ https://docs.snowflake.com/en/user-guide/snowflake-cortex/aisql-cost
自拟教学示意（非书中原文）：
```sql
SELECT id, AI_COMPLETE('mistral-large2',
  '用一句话总结投诉：' || substr(payload:"text"::STRING,1,800)) AS gist
FROM support_tickets WHERE dt='2026-09-27' AND lang='zh';
```

### 2. 语义层与 Analyst/Agents 双件套（转述 ⚠️）
- **Cortex Analyst**：以**语义视图/语义模型**（✅ https://docs.snowflake.com/en/sql-reference/sql/create-semantic-view 、
  ✅ https://docs.snowflake.com/en/user-guide/views-semantic/best-practices ）为接地面生成 SQL；
  官方优化页引入 verified queries 口径（⚠️ analyst-optimization，经索引 200 抓得）。
- **Cortex Agents**：工具（tools）/技能（skills）/多步编排的托管智能体框架
  ✅ https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents 、
  ✅ https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-setup （索引均 200 抓得）。
  2026 版 llms 索引中 agent 相关页 32 条——智能体已成文档第二大树（仅次于 Iceberg 67 条）。

### 3. 向量栈（转述 ⚠️）
VECTOR 数据类型（✅ https://docs.snowflake.com/en/sql-reference/data-types-vector ）+
嵌入函数/REST（✅ https://docs.snowflake.com/en/user-guide/snowflake-cortex/vector-embeddings ）+
Cortex Search 托管检索 ⚠️（页名以索引为准，本册不虚构函数签名）。与盘上向量专册对读：
[../Vector_Databases/00-总览与阅读地图.md](../Vector_Databases/00-总览与阅读地图.md)。

### 4. Document AI = 半结构化的 AI 前置（回扣 06 章）
`AI_PARSE_DOCUMENT`（布局解析）/`AI_EXTRACT`（模式化抽取）/`AI_CLASSIFY` 把 PDF/图像转成
VARIANT/表列 ✅ https://docs.snowflake.com/en/user-guide/snowflake-cortex/parse-document 、
✅ https://docs.snowflake.com/en/user-guide/snowflake-cortex/document-extraction 、
✅ https://docs.snowflake.com/en/user-guide/snowflake-cortex/ai-complete-document-intelligence （第 6 章进水口对位）。

### 5. 护栏与账单（转述 ⚠️）
- **Guardrails**：提示注入/有害内容检测函数族 ✅ https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-ai-guardrails ；
  Agent 时代的权限面与第 10 章策略栈缝合 ⚠️。
- **成本**：AI 函数按 token 计 credit（✅ aisql-cost），与"模型区域可用性"（✅ 专页）构成
  AI 负载双闸——进第 2 章预算体系（QUERY_TAG → Budgets 的 AI 维度）。

## 常见误区

| 误区 | 事实（转述 ⚠️） |
| --- | --- |
| "Cortex=把外部 LLM 接进来" | 执行在仓内治理边界，函数与表同权限域 |
| "语义视图只是报表元数据" | 它是 Analyst 接地正确性的主变量，错了 text-to-SQL 全错 |
| "向量列当普通列用" | 检索路径（Cortex Search/索引形态）与扫描语义不同，成本模型也不同 |
| "AI 成本可忽略" | token 计费随批处理行数爆炸，须先 LIMIT 试算再全量（aisql-cost 口径） |
| "Agent 自主=免治理" | 工具白名单/身份传播/审计三件套恰是 agents-setup 的主张 ✅ |

## 与其他章、其他书的联系

- 上游数据形态 → [06-VARIANT与半结构化数据.md](06-VARIANT与半结构化数据.md)；AI 账单 →
  [02-成本模型与计费内核.md](02-成本模型与计费内核.md)；Agent 权限 →
  [10-治理与安全进阶.md](10-治理与安全进阶.md)；AI 负载算力形态 →
  [01-计算模型与弹性深潜.md](01-计算模型与弹性深潜.md)、[09-Snowpark与编程面.md](09-Snowpark与编程面.md)（容器内推理）。
- 入门对读：TDG-12。
- 谱系：[../Vector_Databases/00-总览与阅读地图.md](../Vector_Databases/00-总览与阅读地图.md)、
  [../Streaming_Databases/00-总览与阅读地图.md](../Streaming_Databases/00-总览与阅读地图.md)（AI×数据的负载观对读）、
  [../bigdata/10-计算引擎的演进.md](../bigdata/10-计算引擎的演进.md)。

## 本章自测（3 分钟）

1. 为什么"AISQL 函数在仓库内执行"对合规团队是卖点、对 FinOps 团队是警报？各举一例。
2. Cortex Analyst 答错数——排查顺序前三步（语义视图建模质量→verified queries→检索接地）。
3. 文档 AI 进 VARIANT（第 6 章）再进列化管线（第 7 章）：画出端到端最小 DAG，并标出三处计费点。

## 核心概念速览（中英对照）

1. **Cortex** — Snowflake 托管 AI 能力总称（SQL 函数+REST+智能体）。
2. **AISQL** — 仓内 SQL 形态的 LLM 函数族（✅ 总页 200）。
3. **AI_COMPLETE/AI_EXTRACT/AI_PARSE_DOCUMENT** — 生成/抽取/文档解析代表函数。
4. **Cortex Analyst** — 语义视图接地的 text-to-SQL 服务。
5. **语义视图** — semantic view：指标/维度/关系的机器可读契约。
6. **Cortex Agents** — 托管智能体框架（工具/技能/编排）。
7. **verified queries** — 已验证查询样本：Analyst 准确率供给（⚠️ 页内为准）。
8. **VECTOR 类型** — 一维浮点数组一等公民（✅200）。
9. **Cortex Search** — 托管混合检索（向量+全文）⚠️。
10. **Guardrails** — 提示注入/内容风险检测函数族。
11. **token 计费** — AI credit 的计量形态，进第 2 章预算循环。
12. **区域可用性** — 模型×区域矩阵：合规与架构双闸门（✅ 专页）。

## 最新演进与工业实践

**2024–2026（URL 均 2026-09-27 curl -L 实测 200 ✅，除标注）：**

- **2026 快照**：llms 索引中 Cortex 树 111 页 + Cortex Code（AI 编码代理）独立 76 页
  （✅ https://docs.snowflake.com/en/user-guide/cortex-code/llms.txt 为索引本体）——"AI 写仓内代码"
  成产品面；文档首页亦提示"Cortex AI 函数语法演化最快，勿凭记忆"（✅ 顶部 llms.txt 原文要旨）。
- **Agents 体系成型**（cortex-agents + setup/skills/toolsets 页组 ✅）：从 2025 Summit 公告
  （✅ https://www.snowflake.com/en/blog/announcements-snowflake-summit-2025/ 本波复核 200）
  到文档正典的完整落地。
- **语义层回归主流**：semantic views 文档 30+ 条 ✅（建模/开发/审计最佳实践成套），与 dbt 式
  语义层在仓内会师 ⚠️。
- **工业实践 ⚠️（转述）**：2026 数据平台 AI 负载三板斧——文档进仓（Document AI）、问答接地
  （语义视图+Analyst）、检索增强（Cortex Search）；每板斧第一道评审都是成本试算+区域合规矩阵。
- 与前波互认：TDG-12 演进节的 Adaptive/Cortex 口径与本快照一致；向量理论深潜导流
  [../Vector_Databases/00-总览与阅读地图.md](../Vector_Databases/00-总览与阅读地图.md)。

**文献与文档**：cortex/aisql / aisql-cost / aisql-regional-availability / aisql-privileges-and-access /
cortex-analyst（前波+本波 ✅）/ cortex-analyst/analyst-optimization / cortex-agents /
cortex-agents-setup / parse-document / document-extraction / ai-complete-document-intelligence /
vector-embeddings / cortex-ai-guardrails / data-types-vector / create-semantic-view /
views-semantic/best-practices / cortex-code llms 索引 / summit-2025 博客（✅200 逐条实测）。
