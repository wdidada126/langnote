# 04 · 探索 Snowflake SQL 命令、数据类型与函数（Ch4: Exploring Snowflake SQL Commands, Data Types, and Functions，✅ 章题实抓）

> 原书第 4 章（约 p.112–147）。SQL 方言总览：命令类别、子查询/集合运算、数据类型族（含 VARIANT 半结构化）、
> 函数体系（内置/UDF/外部函数）。中译本第 4 章章题与之逐词对应（⚠️ 佐证见 00 版本史）。示例均为自拟教学示意。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 4.1 | 命令分类：DDL/DML/DQL/DCL/辅助（SHOW/DESCRIBE/系统过程） | 一切皆 SQL：连"点 UI"都有对应命令 |
| 4.2 | 数据操作：INSERT/UPDATE/DELETE/MERGE 全支持，无锁升级心智 | MERGE 是 ELT 主力 |
| 4.3 | 查询语法：QUALIFY、LIKE ANY、ILIKE、CONNECT BY、窗口函数族 | 方言扩展是加分项 |
| 4.4 | 子查询三面：标量/表/相关 + LATERAL + FLATTEN | FLATTEN 打开半结构化世界 |
| 4.5 | 数据类型族：数值/字符/日期时间（LTZ/NTZ/ZONED 三种时间戳！）/布尔/二进制/变体 | TIMESTAMP_* 三分是新手第一大坑 |
| 4.6 | 半结构化：VARIANT/OBJECT/ARRAY + 路径访问 + INFER_SCHEMA | JSON 先进库、后建模 |
| 4.7 | 函数：内置族、聚合/窗口、UDF（SQL/Java/Python）、外部函数（SageMaker/自建 API）、表值函数 | 函数即扩展点 |
| 4.8 | 查询限制与治理参数（结果行数、超时、并发配额 ⚠️） | 限制大多可账户级调 ⚠️ |

## 核心精讲

### 1. 方言扩展三件套（背例）
```sql
-- 教学示意，非书中原文
-- QUALIFY：对窗口结果再过滤，省一层子查询
SELECT emp_id, dept, salary,
       RANK() OVER (PARTITION BY dept ORDER BY salary DESC) rk
FROM emp
QUALIFY rk <= 3;

-- LIKE ANY：多模式匹配，谓词列表糖
SELECT * FROM log WHERE msg LIKE ANY ('%timeout%', '%429%', '%retry%');

-- TIME_TRAVEL 子句（为第 7 章埋点）：查 5 分钟前的表
SELECT * FROM orders AT(OFFSET => -60*5);
```

### 2. 时间戳三分（第一大坑）
- `TIMESTAMP_LTZ`：按会话时区渲染；`TIMESTAMP_NTZ`：无时区裸值；`TIMESTAMP_TZ`：带原时区偏移存储。
- 数据湖侧无此语法糖（Iceberg 统一 timestamptz/micros，⚠️ 转述）→ 迁移分析时先对齐这个差异：
  [../Apache_Iceberg活用入門/02-元数据三层结构.md](../Apache_Iceberg活用入門/02-元数据三层结构.md)。

### 3. VARIANT：无 schema 先行的半结构化通道
```sql
CREATE OR REPLACE TABLE RAW_EVENTS(ts TIMESTAMP_LTZ, v VARIANT);
INSERT INTO RAW_EVENTS
SELECT CURRENT_TIMESTAMP(), PARSE_JSON('{"user":{"id":7,"tags":["a","b"]},"amount":9.9}');

-- 路径访问 + FLATTEN 展开数组
SELECT ts, f.value::STRING AS tag, v:"user"."id"::BIGINT AS uid
FROM RAW_EVENTS, LATERAL FLATTEN(INPUT => v:"user"."tags") f;

-- 装载时自动推断 schema（第 6 章搭档）
SELECT INFER_SCHEMA('@MY_STG/events/', FILE_FORMAT => 'MY_JSON');
```
机制转述 ⚠️：列式微分区里 VARIANT 被"打平（shredding/typed destructuring）"存储优化是后续版本演进，
书稿只有朴素列式描述；开放格式侧 VARIANT 类型 2025–2026 进入 Iceberg v3（官方工程博客：
https://www.snowflake.com/en/engineering-blog/apache-iceberg-v3-variant-type/ ✅200）。

### 4. 函数即生态
| 类别 | 形态 | 备注（转述 ⚠️） |
| --- | --- | --- |
| 内置标量/聚合/窗口/分析 | SQL 关键字函数 | 覆盖面广，含 AI 函数前身 |
| UDF-SQL/Java/Python(Jupyter 上传/conda 通道) | CREATE UDF | 运行在仓库沙箱内 ⚠️ |
| 外部函数 External Function | 指向 API Gateway→SageMaker 等 | 出算力边界，计费另算 ⚠️ |
| 表值函数 UDTF / SYSTEM$ 系统过程 | CALL / SELECT * FROM TABLE(...) | 管理与诊断的后门 |

### 5. 与其他引擎的语法/语义坐标
- 与 PostgreSQL 近亲（可建"兼容数据库" ⚠️ 转述，见演进节），与 Spark SQL 的差异集中在 SEMI/ANTI join 写法、
  ILIKE、QUALIFY → 对照 [../bigdata/04-SparkSQL与结构化数据.md](../bigdata/04-SparkSQL与结构化数据.md)。
- ANSI 教科书视角：[../数据库系统概念6/05-高级SQL.md](../数据库系统概念6/05-高级SQL.md)、
  [../SQL_and_Relational_Theory/00-总览与阅读地图.md](../SQL_and_Relational_Theory/00-总览与阅读地图.md)。

## 常见误区

| 误区 | 事实（转述 ⚠️） |
| --- | --- |
| "VARIANT 很慢" | 列式+打平后单路径读取成本接近原生列；乱 CAST 才是慢因 |
| "UPDATE/DELETE 需要独占锁规划" | 托管 MVCC 语义，用户不做锁管理；并发写冲突自动处理 ⚠️ |
| "函数下推=全下推" | 复杂 UDF/外部函数常形成行级 RPC 成本，先物化再调 |
| "MERGE 幂等无需设计" | 源含重复键时 MERGE 报冲突；幂等要自己设计键与批次 |

## 与其他章、其他书的联系

- 查询历史/EXPLAIN/画像工具 → [09-查询性能分析与优化.md](09-查询性能分析与优化.md)。
- TIME_TRAVEL 子句的恢复语义 → [07-数据保护与恢复.md](07-数据保护与恢复.md)。
- 半结构化装载全流程 → [06-数据加载与卸载.md](06-数据加载与卸载.md)。
- SQL 通识与窗口/递归对照：[../sql进阶教程.md](../sql进阶教程.md)、[../SQL经典实例.md](../SQL经典实例.md)。

## 核心概念速览（中英对照）

1. **QUALIFY** — QUALIFY：对窗口函数结果集做过滤的子句（Snowflake 方言语义，非 Oracle 保留字语义）。
2. **LIKE ANY** — LIKE ANY：多模式 OR 匹配谓词。
3. **TIMESTAMP_TZ/LTZ/NTZ** — 三种时间戳：带时区 / 会话时区渲染 / 裸值。
4. **VARIANT** — VARIANT：半结构化超类型，存 JSON/Avro 等的路径可寻址列。
5. **FLATTEN** — FLATTEN：表值函数，把数组/对象展开成行。
6. **LATERAL** — LATERAL：行级关联的子查询/函数调用。
7. **INFER_SCHEMA** — INFER_SCHEMA：从文件自动推断列与类型的系统函数。
8. **MERGE** — MERGE：匹配更新+不匹配插入的批量 UPSERT 语句。
9. **UDF** — user-defined function：SQL/Java/Python 三形态自定义函数。
10. **外部函数** — external function：经 API Gateway 调用外部推理/服务的函数。
11. **表值函数** — table function / UDTF：返回表形状的函数。
12. **子查询家族** — scalar / table / correlated subquery：三类嵌套查询形态。
13. **会话参数** — session parameter（TIMEZONE、QUERY_TAG 等）：改变解释与计账的开关。

## 最新演进与工业实践

**SQL 面 2024–2026（URL 均 2026-09 验证 200）：**

- **AISQL / Cortex AI 函数进 SQL**：AI_COMPLETE/AI_CLASSIFY/AI_SUMMARIZE/AI_EXTRACT 等让 LLM 调用变成
  一等 SQL 函数（官方口径页：https://docs.snowflake.com/en/user-guide/snowflake-cortex/aisql）。
  本书 2022 稿的"外部函数调 SageMaker"路线正被此内生化替代。
- **Iceberg v3 Variant 类型**：Snowflake 把 VARIANT 生态扩展到开放格式（工程博客，2025-11）：
  https://www.snowflake.com/en/engineering-blog/apache-iceberg-v3-variant-type/；
  格式侧 GA：https://docs.snowflake.com/en/release-notes/2026/other/2026-05-07-iceberg-v3-ga。
- **SQL 执行性能持续迭代**：官方工程博客 2026 改进综述
  https://www.snowflake.com/en/engineering-blog/sql-performance-improvements-2026/。
- **Snowpark（多语言 DataFrame）2024–2026 扩张**：Python/Java/Scala 客户端与 Container Services 打通
  （https://docs.snowflake.com/en/developer-guide/snowpark-container-services/overview）；社区译作《Snowpark 终极指南》
  中文连载流传（⚠️ 非官方核实书目，仅存目）。
- **PostgreSQL 兼容数据库（2024-06 Preview 起）**：`CREATE DATABASE ... EDITION='standard'` 下 PG 线协议/驱动/
  SQL 子集直连（转述 ⚠️，GA 时间线以官方为准）。工业实践：存量 PG 应用迁移评估期，双写+兼容层是常见形态。
- **半结构化基准**：湖仓侧对同一问题的答案是"打平 + 删除向量 + 类型演进"，对比阅读
  [../Delta_Lake_Definitive_Guide/07-高级特性-DV与CDF.md](../Delta_Lake_Definitive_Guide/07-高级特性-DV与CDF.md)、
  [../Apache_Iceberg活用入門/05-行级删除与删除文件.md](../Apache_Iceberg活用入門/05-行级删除与删除文件.md)。

**文献与文档**
- 官方配套仓库 Chapter04.sql（章题 + "Page 112" 锚点 ✅ 实抓）
- AISQL / Variant / Iceberg / 性能改进：上文 ✅200 链接
