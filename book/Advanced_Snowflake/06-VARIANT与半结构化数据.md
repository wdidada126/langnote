# 06 · VARIANT 与半结构化数据深潜（⚠️ 推定主题章，任务书 ★ 关键词）

> **性质声明**：推定主题重构（[00](00-总览与阅读地图.md)）。机制=官方文档转述（⚠️）+✅URL；
> 🔧 全部实验用本机 DuckDB 1.5.5 `read_json_auto`/STRUCT/UNNEST 类比（**非 Snowflake 行为**）。
> TDG 对位：[../Snowflake_The_Definitive_Guide/04-SQL命令数据类型与函数.md](../Snowflake_The_Definitive_Guide/04-SQL命令数据类型与函数.md)。

## 本章地图

| 节 | 内容 | 一句话结论 |
| --- | --- | --- |
| 6.1 | VARIANT 的二进制存储本质 | 不是 JSON 文本，是自描述树+类型混存 |
| 6.2 | 路径访问与类型系统 | `:`/`::`/TRY_CAST 的失败语义 |
| 6.3 | FLATTEN：表值展开的正典 | LATERAL + 数组/对象展开 |
| 6.4 | 装载侧：INFER_SCHEMA 与演化 | 模式推断托管化 |
| 6.5 | 微分区里的"列化" | 高频路径列转列存储的托管优化 ⚠️ |
| 6.6 | 建模抉择：宽表 vs VARIANT 列 | 进阶团队的三层收敛法 |
| 6.7 | 🔧 类比：read_json_auto→STRUCT 与 UNNEST | 0.079s 载入/2,092 行谓词/13,451 展开行 |

## 核心精讲

### 1. VARIANT 存储与访问语义（转述 ⚠️）
> VARIANT 以**紧凑二进制**存自描述类型树（对象/数组/标量混合）；路径语法 `v:a.b[0]`，
> 类型转换用 `::`，**转换失败整列报错，容错用 TRY_CAST**；同键混型（今天字符串明天数字）使
> 谓词与统计双侧劣化——官方专页列了"混型/超大对象/嵌套过深"等注意事项。
> —— ✅ https://docs.snowflake.com/en/user-guide/semistructured-considerations
> ✅ https://docs.snowflake.com/en/user-guide/semistructured-concepts
> ✅ https://docs.snowflake.com/en/user-guide/querying-semistructured
> ✅ https://docs.snowflake.com/en/sql-reference/functions/flatten

### 2. FLATTEN 惯用法（转述 ⚠️）
```sql
-- 教学示意，非书中原文
SELECT e.id, f.value:"tag"::STRING AS tag
FROM events e, LATERAL FLATTEN(input => e.props:tags) f;
```
FLATTEN 是表值函数：`seq/index/key/path/value/this` 六件套输出；嵌套展开靠多层 LATERAL。
进阶点：展开后的列仍要过第 5 章的谓词卫生关（`::` 转换放在**外层**，内层路径不参与裁剪）。

### 3. 装载侧模式演化（转述 ⚠️）
`INFER_SCHEMA` 表函数/`AUTOINFERSCHEMA` 装载选项：从 Parquet/Avro/ORC/JSON 推断列与类型，
字段级增量演化由平台吸收（新增键不炸表——这是"schema-on-read 落仓"的关键卖点 ⚠️）。
✅ https://docs.snowflake.com/en/sql-reference/functions/infer_schema

### 4. 建模三段论（方法论重述 ⚠️）
1) **原始层**整包 VARIANT（审计/回放/模式演化安全）；2) **清洗层**FLATTEN 出高价值路径；
3) **消费层**转关系列+聚簇/搜索优化。每下沉一层，查询从"路径解析"转为"列裁剪"，
账单随裁剪命中下降（第 3/4 章联动）。

### 5. 🔧 本地镜像实验（DuckDB 1.5.5，**非 Snowflake 行为**）
20,000 行 JSONL（含 `user{}`、`props{page,clicks,tags[]}` 嵌套+数组）：
- `read_json_auto` 推断：`user→STRUCT(id BIGINT, tier VARCHAR)`、`props→STRUCT(page VARCHAR,
  clicks BIGINT, tags VARCHAR[])`——**载入 0.079s**。对照 Snowflake：`INFER_SCHEMA` 同题、
  VARIANT 则"不推断、混存"——**推断成 STRUCT=强类型化，是 DuckDB 与 VARIANT 的本质分歧**。
- 路径谓词 `user.tier='pro' AND props.clicks>20` → **2,092 行**（≈`v:user.tier::STRING` 语义）。
- `UNNEST(props.tags)` ≈ `LATERAL FLATTEN`：展开后过滤 `tag='t1'` → **13,451 行**。
- JSON 混型容错演示：对无键路径转 INT，DuckDB binder 直接拒绝（struct 键必须存在），
  Snowflake VARIANT 则运行时 NULL/TRY_CAST 兜住——**同一坑的两种引擎哲学**（记录差异，不判优劣）。
（脚本 E1；方法：jsonl 生成 seed=42 可复现。）

## 常见误区

| 误区 | 事实（转述 ⚠️） |
| --- | --- |
| "VARIANT 就是存 JSON 字符串" | 二进制自描述树，且混型代价由**你**付（统计/转换） |
| "半结构化免建模" | 三段论不省：原始层只保证演化安全 |
| "FLATTEN 随便多层套" | 每层展开行数相乘，爆行先估 `tags×events` 基数 |
| "路径过滤也能裁剪" | `v:clicks>20` 在 VARIANT 上不走微分区值域裁剪 ⚠️，列化后才吃布局红利 |
| "AUTOINFERSCHEMA 永远开着" | 类型推断错判需要人工兜底（显式映射/CAST 层） |

## 与其他章、其他书的联系

- 展开后的表进布局线 → [03-微分区与裁剪引擎.md](03-微分区与裁剪引擎.md)、[04-聚簇与搜索优化.md](04-聚簇与搜索优化.md)；
  FLATTEN 大表的 JOIN 形态 → [05-查询优化与JOIN策略.md](05-查询优化与JOIN策略.md)；
  装载侧主场 → [08-数据摄入进阶.md](08-数据摄入进阶.md)。
- 入门对读：TDG-04（数据类型/函数面）。
- 文档数据库谱系对照（同为嵌套数据，模型迥异）：
  [../MongoDB_The_Definitive_Guide_3e/00-总览与阅读地图.md](../MongoDB_The_Definitive_Guide_3e/00-总览与阅读地图.md)、
  聚合管道展开对照 → [../Practical_MongoDB_Aggregations/00-总览与阅读地图.md](../Practical_MongoDB_Aggregations/00-总览与阅读地图.md)（$unwind≈FLATTEN）；
  Parquet 嵌套列原理 → [../bigdata/09-存储与文件格式.md](../bigdata/09-存储与文件格式.md)；
  DuckDB 侧正典 → [../DuckDB_in_Action/04-高级聚合与数据分析.md](../DuckDB_in_Action/04-高级聚合与数据分析.md)。
- 【登记·同波不链】BigQuery REPEATED/RECORD 与 STRUCT/UNNEST 深对照，波尾挂 `Google_BigQuery_TDG`。

## 本章自测（3 分钟）

1. 为什么 `v:clicks::INT > 20` 不吃微分区裁剪，而列化后的 `clicks>20` 吃？（路径谓词与统计的关系）
2. FLATTEN 两层嵌套（事件→items→tags）最坏行数是多少？装载前你如何预估并设护栏？
3. DuckDB 把 JSON 推断成 STRUCT、Snowflake 存成 VARIANT——对"新增键"和"改类型"两种演化，
   两种模型各炸在哪一步？（🔧E1 的 binder 拒绝就是其中一种"早炸"）

## 核心概念速览（中英对照）

1. **半结构化数据** — semi-structured data：自描述、模式可演化的数据形态。
2. **VARIANT** — Snowflake 通用容器类型：对象/数组/标量的二进制混存。
3. **路径访问** — path access：`v:a.b[0]` 语法，配 `::` 转型。
4. **FLATTEN** — 表值展开函数：LATERAL + seq/index/key/path/value/this。
5. **INFER_SCHEMA** — 装载侧模式推断表函数（✅200）。
6. **TRY_CAST** — 容错转换：混型地带的护城河。
7. **混型退化** — mixed-type degradation：同键多型使统计与谓词双侧失效（⚠️）。
8. **列化** — tabularization：高频路径下沉为关系列吃裁剪红利（三段论第 3 层）。
9. **STRUCT**（🔧类比物）：DuckDB 强类型嵌套记录，与 VARIANT 的"推断 vs 混存"对照。
10. **UNNEST**（🔧类比物）：数组展开表函数，≈FLATTEN 之于数组。
11. **schema-on-read** — 读模式：原始层安全垫，消费层反面教材。
12. **AUTOINFERSCHEMA** — 装载选项：COPY 时自动推断目标列（⚠️ 转述）。

## 最新演进与工业实践

**2024–2026（URL 均 2026-09-27 curl -L 实测 200 ✅）：**

- **考虑事项页持续扩条**（semistructured-considerations ✅）：大小限制、混型、深度等官方"坑表"
  是进阶运维的第一依据。
- **向量列与 VARIANT 的分流**：2025+ 出现一等 **VECTOR 数据类型**（✅
  https://docs.snowflake.com/en/sql-reference/data-types-vector），AI 嵌入类半结构化需求
  从 VARIANT 迁出——本册第 12 章接口。
- **文档 AI 反哺**：AI_PARSE_DOCUMENT/AI_EXTRACT 把非结构化文档直接落成 VARIANT/表列
  （✅ snowflake-cortex/parse-document、document-extraction，第 12 章主场）。
- **工业实践 ⚠️（转述）**：事件管线普遍"原始 VARIANT + 契约层列化"双轨；FLATTEN 展开量作为
  成本护栏指标（每事件展开行数告警）进入 2025+ FinOps 手册。
- 🔧 复现：E1 全套（20k 行、seed 固定）适合"VARIANT vs 强类型"对比教学。

**文献与文档**：semistructured-considerations / semistructured-concepts / querying-semistructured /
functions/flatten / functions/infer_schema / data-types-vector（✅200）；🔧 experiments.py E1。
