# 02 · 数据管道工程：从 ETL 到 ELT

> ⚠️ 主题重构章（原书目录取证不可得，见 [00-总览与阅读地图.md](00-总览与阅读地图.md) §2）。
> 🔧 实验组 E1 本章落地：SQLite 源 → DuckDB 仓的全量装载 + 水位线增量 MERGE。
> 引擎语法细节归 [../DuckDB_in_Action/00-总览与阅读地图.md](../DuckDB_in_Action/00-总览与阅读地图.md)
> （其 [08-构建数据管道.md](../DuckDB_in_Action/08-构建数据管道.md) 讲"管道作为一等公民"的
> 引擎侧机制），本章讲**管道作为架构组件**的工程模式。

## 1. 管道的解剖学：EL 与 T 的位置之争

- **ETL（变换前置）**：抽取→在中间层（Python/Spark 作业）清洗→装载进目标。适合
  "源脏、目标有强 schema、合规要求脱敏后才入库"。缺点：变换逻辑住在过程代码里，
  复用与测试成本高。
- **ELT（变换后置）**：原样装载→在引擎内用 SQL 建模（dbt 是此道的化身，对读
  [../Analytics_Engineering_with_SQL_and_dbt/00-总览与阅读地图.md](../Analytics_Engineering_with_SQL_and_dbt/00-总览与阅读地图.md)）。
  适合云仓/湖仓：算力弹性、SQL 资产可审查可血缘（06 章）。
- Python 视角的两面性：本册 🔧E1 里 DuckDB 既当**目标仓**又当**执行引擎**，
  而 SQLite 源侧原样读出——EL 两步在同一个进程内完成，T 用 MERGE/CTAS 表达。
  这是"单机 ELT"的典型形态：管道=一个可重跑的 Python 函数集合。

## 2. 分层模式：ODS → staging → mart 为什么要保持粗糙的三层

- **ODS（贴源层）**：与源表结构基本一致，只做类型适配；它的存在让"重放"永远可行。
- **staging**：业务清洗（去重、单位、时区）、增量合并都发生在这里。
- **mart**：面向消费方的聚合/宽表。06 章的血缘边表正是沿这三层生长的。
- 工程纪律：**每层都可从上一层全量重建**。管道可重跑（idempotent）是比任何框架选型
  更重要的性质；编排器（Airflow 等）只负责把重跑排好，不负责对错。

## 3. 🔧E1 实测：水位线增量 + MERGE 幂等摄取（本波最高密度实验之一）

方法（脚本 `D:\develops\tmp\dbwave_w7_mdatap\experiments.py`，seed=42）：

1. 源侧 SQLite `src.db`：`orders` 表 100,000 行，带 `updated_ts`，并建
   `CREATE INDEX ix_orders_ts`（增量的物理前提：按水位线过滤要走索引，否则全表扫）。
2. DuckDB `wh.duckdb`：`INSTALL sqlite; LOAD sqlite; ATTACH 'src.db' AS src (TYPE SQLITE)`
   → `CREATE TABLE ods_orders AS SELECT * FROM src.main.orders`。
   **实测：全量 10 万行 0.042s**。
3. 模拟上游变更 5,000 行（`updated_ts` 推到新水位 `2026-01-02`），增量摄取：
   `CREATE TEMP TABLE delta AS SELECT * FROM src.main.orders WHERE updated_ts > ?`（参数化水位），
   再 `MERGE INTO ods_orders t USING delta s ON t.id=s.id WHEN MATCHED THEN UPDATE ... WHEN NOT MATCHED THEN INSERT *`。
   **实测：增量 merge 0.036s，仓内行数仍 100,000，命中新时间戳的行恰 5,000**。

```sql
MERGE INTO ods_orders t USING delta s ON t.id = s.id
WHEN MATCHED THEN UPDATE SET amount = s.amount, updated_ts = s.updated_ts
WHEN NOT MATCHED THEN INSERT *;
```

结论与边界：
- 🔧 水位线切片 + MERGE 在 DuckDB 1.5.5 上**语义正确且幂等**（同 delta 重跑两次结果不变，
  因为 ON 键唯一）；MERGE INTO 官方语法 ✅ https://duckdb.org/docs/stable/sql/statements/merge_into.html 。
- ⚠️ 不外推到云管道：真实生产的 CDC（03 章）、背压、schema 演进由 Fivetran/Debezium 类
  工具处理，本机不可测其吞吐行为。
- 对比实验义务（诚实登记）：SQLite 无 MERGE，只能 `INSERT ... ON CONFLICT DO UPDATE`
  （upsert 语法，✅ https://sqlite.org/lang_UPSERT.html ，2026-10-01 curl -sIL 200）——
  同语义两引擎两种写法，本册 🔧E1 因此只测 DuckDB 侧 MERGE，SQLite 侧 upsert 未另测标 ⚠️。

## 4. 增量切片的四种口径与各自的坑

| 切片依据 | 写法 | 坑 |
| --- | --- | --- |
| 更新时间戳（🔧E1） | `WHERE updated_ts > watermark` | 源不维护 updated_ts / 时钟漂移 / 同秒并发漏行（要 `>=` 加去重键） |
| 自增主键 | `WHERE id > max_id` | 只捕获插入，漏更新/删除 |
| 全表哈希对比 | 指纹表（05 章 🔧E3 思想） | 代价 O(n)，只适合小维表 |
| CDC 日志 | binlog/WAL 解码（03 章） | 捕获删除，但基建最重 |

删除是四种口径共同的痛点：水位线与自增键都**看不见物删**。工程答案要么软删除
（源加 is_deleted 列，改 MERGE 语义），要么周期全量重建 ODS（承认 ODS 重建成本<正确性成本）。

## 5. 编排：DAG 是依赖图，不是流程图

- 管道层与编排层分离：函数应**不知道**自己被谁调、何时调（🔧E1 的三个步骤各自可独跑）。
  Airflow/Dagster/Prefect 只是把调用顺序外置成代码化 DAG（⚠️ 转述各家语义差异，
  本册不装平台）。
- 重跑策略三件套：幂等（MERGE/overwrite-partition）、回看窗口（late data 迟到补偿）、
  水位线持久化（存在 05 章的元数据表里——注意**水位线本身就是运营元数据**）。
- 失败语义：区分"可重试"（网络抖动）与"必须人看"（schema 漂移、质量阻断）。
  后者由 04 章闸门触发，是治理闭环（09 章）的入口。

## 6. 与 DuckDB 册的分工声明

[../DuckDB_in_Action/08-构建数据管道.md](../DuckDB_in_Action/08-构建数据管道.md) 从引擎视角讲
DuckDB 作为管道中枢的 COPY/宏/增量刷新；[../DuckDB_Up_and_Running/00-总览与阅读地图.md](../DuckDB_Up_and_Running/00-总览与阅读地图.md)
讲引擎基本盘。本章的增量是**架构层**：为什么分层、删除难题、编排契约、幂等三件套。
同一条 MERGE，两册各讲一次不冲突：引擎册讲语法与执行计划，本册讲它在管道语义里的职务。

## 7. 管道健康七检（评审用清单）

1. 任意管道步骤单独重跑 10 次，终态是否与跑 1 次一致？（幂等，🔧E1 已证 MERGE 路径）
2. 水位线存在哪？崩在装载中途重启会不会跳过一段？（应存 05 章目录/运营表，装载成功
   后才推进游标——两阶段提交的最小 homemade 版）
3. 源删一行，仓里多久能看到？（03 章删除难题；答不上=没有答案，只有假设）
4. ODS 能否从源全量重建且验证行数？（可重放底线；重建脚本应常跑，不跑=不存在）
5. 迟到 3 天的数据到达时会发生什么？（回看窗口 or 静默丢失）
6. schema 漂移时管道是 fail-fast 还是带病续跑？（接 05 章指纹检查）
7. 谁看红灯？（阻断档规则必须有名有姓的 owner，否则退化为噪音——04 章 §4 三档语义）

自检问答（读毕应有答案）：
- 🔧E1 里为什么增量前提是先建 `ix_orders_ts` 索引？（水位线过滤走全表扫则增量成本≈全量）
- MERGE 的幂等性依赖什么约束？（ON 键唯一；键不唯一时 MATCHED 行为未定义级风险）
- 为什么"每层可全量重建"比框架选型重要？（重跑能力是全部运维假设的地基）

## 核心概念速览（中英对照）

1. **ELT** — Extract-Load-Transform：原样装载、引擎内变换的管道方向，云仓时代主流。
2. **ODS 贴源层** — Operational Data Store：与源同构的可重放底线层。
3. **水位线** — Watermark：增量切片的游标（常为 max(updated_ts)），本身要持久化。
4. **幂等摄取** — Idempotent Ingestion：同一批数据重跑任意次，终态不变。
5. **MERGE** — MERGE INTO：按键匹配则更新、不匹配则插入的单语句 upsert（🔧E1）。
6. **回看窗口** — Rerun/Lookback Window：为迟到数据故意重放最近 N 天的补偿带。
7. **软删除** — Soft Delete：以标记列表达删除，绕开水位线看不见物删的盲区。
8. **CDC** — Change Data Capture：从变更日志捕获增删改的摄取方式（03 章）。
9. **编排/调度分离** — Orchestration Separation：管道函数不感知 DAG，顺序外置。
10. **质量闸门** — Quality Gate：管道步骤间阻断式检查（04 章），失败走人工。
11. **微批** — Micro-batch：分钟级增量运行的工程折中，逼近流语义（01 章 §3）。
12. **单机 ELT** — Single-node ELT：DuckDB 同进程完成 EL+T 的最小管道形态（🔧E1）。

## 最新演进与工业实践

- **DuckDB MERGE INTO**：1.0 后进入稳定语法集，✅ https://duckdb.org/docs/stable/sql/statements/merge_into.html （2026-10-01 curl 200，重定向后）；🔧E1 在 1.5.5 实测通过。
- **sqlite_scanner 扩展**：ATTACH TYPE SQLITE 直查活的 SQLite 文件，官方扩展文档 ✅ https://duckdb.org/docs/stable/extensions/overview ；本册 🔧E1 全链依赖此件（引擎侧细节让渡给 [../DuckDB_in_Action/02-快速上手CLI与扩展系统.md](../DuckDB_in_Action/02-快速上手CLI与扩展系统.md)）。
- **Airflow 3.x**（2025 起）：任务 API/DAG 解析重构，事件驱动调度补强（⚠️ 转述，发布注逐条未核）。Dagster 的"资产导向"与本册"ODS/mart 分层 + 元数据表"思想同源：把 DAG 顶点从"任务"换成"数据资产"（⚠️ 转述）。
- **dbt 增量模型**：`incremental` materialization 即水位线+去重的声明式封装，对读 [../Analytics_Engineering_with_SQL_and_dbt/00-总览与阅读地图.md](../Analytics_Engineering_with_SQL_and_dbt/00-总览与阅读地图.md) 与 [../Unlocking_dbt/00-总览与阅读地图.md](../Unlocking_dbt/00-总览与阅读地图.md)；dbt-duckdb 适配器让 🔧E1 的一切可以原样搬进 dbt 项目。
- **工业口径**：Fivetran/Airbyte 类 EL 工具+dbt 的"现代 ELT 栈"仍是 2024–2026 中小团队默认叙事（⚠️ 转述）；本册价值在**不依赖任何 SaaS** 的手撕版本，理解 EL 工具替你保管的水位线与 schema 演进契约到底是什么。
