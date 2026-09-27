# 05 ETL 编排：Airflow 与 Step Functions（2e Ch5）

> 取证强度：✅ 强（官方 2E 仓 Chapter05/src 全套实抓：`redshift_parts_airflow_dag.py`（Airflow DAG，PostgresHook/PostgresOperator 打 Redshift）、`stepfunction/lambda_submit_redshift_query.py`+`lambda_poll_redshift_query.py`+`stepfunction_job_redshift.json`（提交/轮询双 Lambda+状态机）、`event-bridge-lambda-function.py`、`my-lambda-deployment-package.zip`、`requirements.txt`）。
> 三态：✅ URL/命令实证｜⚠️ 转述推定｜🔧 DuckDB 1.5.5（**非 Redshift 行为，方言已按 DuckDB 改写**）。

## 1. 本章定位

装载有了节奏（Ch4），本章给节奏装上**指挥台**：用编排器把"COPY→转换 SQL→合并→分析→UNLOAD"串成可重放 DAG。2e 一次给出三种编排姿势：Airflow（开源事实标准）、Step Functions（AWS 原生）、EventBridge（事件触发）——覆盖"定时/依赖/事件"三触发模型（✅ 文件集即证据）。

## 2. 配方地图

| 配方 | 核心机制 | 取证 |
|---|---|---|
| Airflow→Redshift | DAG 内 PostgresHook 以 PG 协议连 Redshift（psycopg2 底座）；create_table_sql 内嵌 DDL | ✅ dag 文件前 14 行实抓（import airflow.../PostgresHook/logging）|
| Step Functions 托管作业 | 无原生 Redshift 活动→自定义 Lambda"提交查询+轮询完成"两拍（submit/poll JSON 入出参测试件齐备） | ✅ 6 文件实抓（含 *_test.json 负载样本） |
| EventBridge 事件驱动 | 规则匹配→Lambda→触发下游（源文件独立存在） | ✅ 文件名实抓，链路 ⚠️ 推定 |
| 作业监控 | CloudWatch 指标+日志（配 chapter_5_CFN 栈） | ⚠️ 转述；✅ https://docs.aws.amazon.com/redshift/latest/mgmt/welcome.html 同址 200 |
| 原生红孩儿 | Redshift Scheduler（内置 auto copy/auto WLM/定时 SQL）2022+ | ⚠️ 转述，专页实测 302→mgmt/ 根（登记） |

## 3. 深潜一：Airflow 配方的三处方言（⚠️ 转述+✅ 实抓）

1. **连接复用**：Redshift 无独立 Airflow provider 时代（本书主场景），官方姿势=把 Redshift 当 PostgreSQL 用 `PostgresHook`——仓内 dag 即证（✅ import 行实抓；现代线 `apache-airflow-providers-amazon` 的 `RedshiftDataOperator` 走 Data API，见 §演进）；
2. **SQL 即算子**：`PostgresOperator(sql=create_table_sql)` 把 DDL/COPY/MERGE 逐段成任务——粒度=可重跑单元=表（⚠️ 工程口径）；
3. **凭据出仓**：连接口令进 Airflow 加密后端（或 Secrets Manager 联动，呼应 Ch1 配方），DAG 文件零明文（✅ dag 文件未见明文口令，佐证此纪律）。

Step Functions 双拍子（submit/poll）要点：Data API `execute_statement` 返回 queryId→轮询 `describe_statement` 直到 FINISHED——无长连接、按调用计费、天然幂等重试（⚠️ 转述；✅ Data API 锚 https://docs.aws.amazon.com/redshift/latest/mgmt/data-api.html 同址 200）。仓内 `lambda_submit_redshift_query.py`/`lambda_poll_redshift_query.py` 文件名即此两拍的显影（✅）。

## 4. 深潜二：编排对象清单（本章重构）

```
[DAG] extract_ok(EventBridge) ─→ copy_stg ─→ merge_fact ─→ analyze ─→ refresh_mv ─→ unload_serving
   触发: cron/事件/依赖      幂等: 控制表+清分区重放    观测: 每步计时入 CloudWatch
```
（⚠️ 骨架为重构示意，节点集由本册 03/04/07 配方与 ✅ 文件族互证。）

## 5. 🔧 实测：编排语义的最小可测核——"物化视图刷新步"值不值（本机真实跑过）

脚本 demo.py（D4），DuckDB 1.5.5——**非 Redshift 行为，方言已按 DuckDB 改写**（Redshift 对应 `CREATE MATERIALIZED VIEW ... AUTO REFRESH YES`，✅ https://docs.aws.amazon.com/redshift/latest/dg/materialized-view-create-sql-command.html 同址 200；自动增量刷新语义 ⚠️ 转述 https://docs.aws.amazon.com/redshift/latest/dg/materialized-view-overview.html 同址 200）：
- 基表 5e6 行全量 GROUP BY 聚合 14ms；把结果物化成 2500 行日汇总后，下游"取某日前合计"：**0.76ms（读汇总）vs 4ms（基表现算）≈ 5×**；
- 编排含义：`refresh_mv` 节点的存在意义=用一次批处理买下游千次查询的 5× 体验；DuckDB 无自动刷新（手动 CTAS 模拟），恰好演示"刷新步"在 DAG 里是显式节点而 Redshift 可交给 AUTO REFRESH（差异 ⚠️ 转述）。

## 6. 常见坑与最佳实践（⚠️ 转述+✅ 锚）

1. **重试≠幂等**：COPY 重跑必先删目标分区数据，否则双算（→ 03 §6-5 对账法）；
2. Airflow 并发×Redshift WLM 槽位=隐性资源谈判——DAG 的 `parallelism` 要对齐队列并发上限（⚠️ 转述；✅ 总览锚 https://docs.aws.amazon.com/redshift/latest/mgmt/redshift-performance.html 实测已 302→mgmt/ 根，登记改版）；
3. Lambda 轮询要给足超时预算：大查询分钟级，poll 间隔指数退避防 Data API 限频（⚠️；✅ data-api 锚同址 200）；
4. EventBridge 触发风暴：同分钟多文件落 S3 会打多 DAG——去重窗/合批（⚠️ 工程惯例）；
5. 一切编排元数据（批次/水位/行数）落仓内控制表，别只留编排器日志——对账要 SQL 可查（⚠️）。

## 7. 系列互链

- 概念版编排叙事：[../Amazon_Redshift_TDG/04-数据转换策略.md](../Amazon_Redshift_TDG/04-数据转换策略.md)（ELT vs ETL、库内转换、编排选型）；
- 调度学理：[../bigdata/11-调度资源与运维.md](../bigdata/11-调度资源与运维.md)（DAG/水位/补数概念谱系）；
- Snowflake 的仓内编排对照（Tasks/Streams 免外部编排器）：[../Advanced_Snowflake/07-Streams与Tasks编排.md](../Advanced_Snowflake/07-Streams与Tasks编排.md)；
- Data Pipeline 数据质量节点：[../bigdata/12-数据质量与工程实践.md](../bigdata/12-数据质量与工程实践.md)。

## 8. 配方演绎一：Airflow DAG 骨架（✅ 依仓内 redshift_parts_airflow_dag.py 的 import 族重构示意，非原书文本）

```python
from airflow import DAG
from airflow.operators.postgres_operator import PostgresOperator  # Redshift 当 PG 用 ✅
from airflow.hooks.postgres_hook import PostgresHook              # ✅ import 行实抓
with DAG("redshift_parts", schedule_interval="0 */6 * * *",
         catchup=False, max_active_runs=1) as dag:                 # 幂等三闸 ⚠️
    t1 = PostgresOperator(task_id="copy_stg", sql=COPY_STG_SQL)
    t2 = PostgresOperator(task_id="merge_fact", sql=MERGE_SQL)     # →03 §5 五步
    t3 = PostgresOperator(task_id="refresh_mv", sql=REFRESH_SQL)   # →§5 的 D4 账
    t4 = PostgresOperator(task_id="unload_serving", sql=UNLOAD_SQL)# →04 §5 的出口
    t1 >> t2 >> [t3, t4]
```
读法：**任务粒度=表粒度=幂等单元**；`max_active_runs=1` 防同表并发合并互踩（⚠️ 工程惯例）。

## 9. 配方演绎二：Step Functions submit/poll 状态机（✅ 六文件族+⚠️ 语义）

```
Submit Lambda: redshift-data:ExecuteStatement → 返回 Id
Wait: Wait 30s →（指数退避 ⚠️）
Poll Lambda: DescribeStatement(Id).Status
   FINISHED → next task        FAILED → Fail(告警→CloudWatch)
   FINISHING → Wait again      （仓内 *_test.json 即此三态入出参样本 ✅）
```
与 Airflow 路的分工：**重依赖图→Airflow；轻量事件后作业→Step Functions**（⚠️ 本章重构口径）。

## 10. 编排层对账清单（⚠️ 提炼）

- [ ] 每任务先写"批次水位"再改数据（顺序反了=崩溃即双算）
- [ ] 重试策略分三类：幂等读（裸重试）/重放写（先删后插）/外部调用（退避+死信）
- [ ] 补数窗口与保留期对齐：S3 生命周期到期前能把历史跑完
- [ ] DAG 失败告警直连值班渠道，日志含 batch_key 可 grep
- [ ] 每月一次"拔电演练"：kill -9 中间态重跑，验证全套幂等
- [ ] 编排器重启不丢状态：状态在仓内控制表，不在 DAG Run 属性里

## 11. 本章自查五问

1. PostgresHook 能连 Redshift 的协议根基是什么？边界在哪？
2. submit/poll 为何天然适配 Data API 的无长连接模型？
3. refresh_mv 节点删掉会怎样？多久后 BI 用户先发现？（→§5 D4）
4. EventBridge 风暴与 `max_active_runs` 的组合拳漏了哪类事件？
5. Redshift Scheduler 何时够用、何时必须外挂编排？

## 核心概念速览（中英对照）

- DAG — directed acyclic graph：任务依赖的有向无环图编排单元
- PostgresHook — psycopg2 兼容通道：Airflow 把 Redshift 当 PG 驱动接入
- submit/poll 两拍 — submit+poll lambdas：Data API 无长连接的作业跟踪模式
- EventBridge 触发 — event-driven ingestion：S3/服务事件驱动流水线
- Redshift Scheduler — 内置调度：auto copy+定时 SQL 的免外挂方案（⚠️）
- 幂等重跑 — idempotent rerun：分区删除+重放式的安全重试
- 高水位控制表 — watermark control table：编排元数据落仓的账本
- 指数退避 — exponential backoff：轮询防限频
- SLA/报警 — CloudWatch alarms：队列等待/复制延迟红线
- 补数 — backfill：历史窗口重放，编排器的第二公民
- auto copy — AUTO COPY：装载调度交系统（→03）
- refresh 节点 — MV refresh step：DAG 中显式的预聚合刷新位

## 最新演进与工业实践

- **Managed Airflow（MWAA）+ Amazon Provider**：2023+ 官方线把 Redshift 算子升级为 `RedshiftDataOperator`/`RedshiftSQLOperatorAsync`（Data API 原生、免 PG 兼容层）（⚠️ 转述；✅ Data API 同址 200 锚支撑底座）。
- **Step Functions 服务集成直连 Data API**：submit/poll 双 Lambda 被"服务集成+回调任务"取代趋势明显，仓内 2024 代码仍留双拍=教材快照价值（✅ 文件实抓；现状 ⚠️）。
- **仓内编排扩张**：Redshift Scheduler 承担轻量定时，重依赖上抬 MWAA/Glue Workflows/dbt Cloud——2026 分工线（⚠️ 转述）。
- **工业实践**：湖仓管道（Iceberg 表+多引擎）倒逼编排层"SQL 与 Spark 混排"，与 [../Use_Iceberg_with_Spark/00-总览与阅读地图.md](../Use_Iceberg_with_Spark/00-总览与阅读地图.md) 的工程叙事在 AWS 侧汇流（⚠️ 对照）。
