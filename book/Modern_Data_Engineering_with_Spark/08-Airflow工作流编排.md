# 08 — Airflow 工作流编排（Workflow Orchestration with Apache Airflow）

> 《Modern Data Engineering with Apache Spark》第 8 章 · Apress 2022 · Scott Haines
> 章题与章序 ✅ Crossref DOI `10.1007/978-1-4842-7452-1_8` 实抓；**章内小节结构 ⚠️ 推定**（依据章题与 Airflow 官方文档主题域反推），非原书小节文本。
> 三态标记：✅ 实抓 / ⚠️ 推定或转述 / 🔧 本机实测类比（非本书 Spark 平台行为）。

## 1. 本章定位

全书唯一非 Spark 主角章：Apache Airflow 以 Python 声明 DAG，把第 7 章定义的管道单元挂上调度、依赖、重试与补数的传送带。对「mission-critical」承诺而言本章是**运维语义的来源**——作业失败后发生什么，由 Airflow 回答而非 Spark 回答。这也是本书「平台观」最集中的一章：Spark 算、Kafka 传、Postgres 存状态（Airflow 元数据库，⚠️ 推定其演示配置）、Airflow 管。

## 2. DAG 概念栈（⚠️ 按章题域重构，2022 语境 ≈ Airflow 2.2）

- **DAG**：Python 文件中的有向无环图；`dag_id` 即生产身份。官方概念入口 ✅ https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html。
- **Task/Operator**：任务=算子实例；`BashOperator`、`PythonOperator` 教学标配，**`SparkSubmitOperator`/`SparkSubmit`（apache-airflow-providers-apache-spark）** 才是本章与本书主线的焊接点（⚠️ 是否用 provider 包未证实，亦可能 Bash 包 spark-submit）。
- **依赖**：`>>` / `set_downstream`；跨 DAG 依赖 `ExternalTaskSensor`/dataset 前夜形态。
- **调度**：cron + `start_date` 语义陷阱（首 run 延迟、`catchup` 开关）——编排第一坑。
- **重试与告警**：`retries`/`retry_delay`/`on_failure_callback`——mission-critical 的最小配置面。
- **连接管理**：Connections/Variables 把 JDBC 串与密钥挪出代码（呼应第 5 章）。

## 3. Spark 作业作为 Airflow 任务的三种耦合度（⚠️ 重构）

1. **粗**：BashOperator 调 `spark-submit`——传参走 CLI，日志在 worker；本书入门最可能形态（⚠️ 推定）。
2. **中**：SparkSubmitOperator——YARN/Standalone 提交语义内建，`master`/`deploy-mode` 成字段。
3. **细**：Task 内建 SparkSession（管道在 driver 进程内活着）——资源与生命周期纠缠，工程册通常劝退。

- 与 14/15 章的接口：Airflow 提交的目标集群形态（local/Standalone/K8s）决定运维面——本章立契约、后两章履约。

## 4. 补数与分区回放（编排的「时间维度」，⚠️ 重构）

- **Backfill**：以 `data_interval` 逐分区重放——第 7 章「分区重算+回溯窗口」的调度器实现。
- **幂等前提**：补数安全=管道幂等（编排器把 7 章品质清单变成硬约束）。
- **clear/rerun**：任务级重放语义；失败恢复起点由 Airflow 状态机而非 Spark 决定。
- **时间参数注入**：`{{ ds }}`/macros 传入 Spark 作业参数——新鲜度与正确性的接缝。

## 5. 🔧 类比·DAG 语义的最小宿主（SQLite，非 Spark/Airflow 行为）

用 SQLite 物化「任务状态表」，体验编排器的核心数据结构：

```python
import sqlite3, datetime
db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE task_run(task TEXT, part TEXT, state TEXT, ts TEXT, PRIMARY KEY(task,part))")
def run(task, part):
    cur = db.execute("SELECT state FROM task_run WHERE task=? AND part=?", (task, part)).fetchone()
    if cur and cur[0] == 'success':
        return 'skip(幂等重放)'
    # ... 真正执行 ...
    db.execute("INSERT OR REPLACE INTO task_run VALUES(?,?,?,datetime('now'))", (task, part, 'success'))
    return 'ran'
for _ in range(3):
    print(run('aggregate', '2022-03-01'))   # ran, skip, skip
```

- 观察：一张 `task_run` 状态表 + 「成功即跳过」规则 = 编排器最小内核（依赖记录/重试只需再加列）。
- 类比边界：无调度器、无并发 worker、无 XCom——只证明「编排=持久化的状态机+幂等执行」这一抽象（🔧）。

## 6. 编排器选型语境（2022 章内视角 ⇄ 2026 回望）

- 2022：Airflow 社区主导心智（本书选择即其注脚）；Dagster/Prefect 以「资产/任务新模型」挑战。
- 对位盘上：湖仓编排话题见 [../Data_Lakehouse_in_Action/00-总览与阅读地图.md](../Data_Lakehouse_in_Action/00-总览与阅读地图.md)；K8s 原生工作流（Argo 类）与 15 章接口。
- 「DataOps」标签在 2024–2026 淡出，但其内容（CI 进数据管道、观测先行）已被编排器吸收（⚠️ 观察性陈述）。

## 7. 校读清单

- 作者是否配置过 Airflow 元数据库到 Postgres（默认 sqlite 并发限制）？——本地平台成熟度标志。
- DAG 文件里是否内嵌了 Spark 代码路径的打包说明（`--py-files`/venv）？——部署章伏笔。
- 是否演示 `airflow dags test`/`dag-factory` 类工程件？——预期没有（2022 惯例）。

## 9. DAG 骨架示意（本目录重构伪码，⚠️ 非原书代码）

```python
# dags/spark_daily_pipeline.py —— 概念骨架，API 形态按所用 Airflow 版本校准
with DAG("spark_daily", schedule="0 2 * * *",
         start_date=datetime(2022,1,1), catchup=True,
         default_args={"retries":2, "retry_delay":timedelta(minutes=5)}) as dag:
    check_source  = SensorOperator(...)                     # 依赖哨兵（7 章品质3）
    aggregate     = SparkSubmitOperator(                    # 本章主焊点
                        application="./jobs/agg.py",
                        conf={"spark.master":"spark://master:7077"},  # → 14 章
                        conn_id="spark_default")
    publish       = BashOperator(cmd="refresh serving view") # → 6/12 章消费面
    check_source >> aggregate >> publish
```

- 读法要点：每个 Operator 参数都是一个「章节跳转链接」——注释行即本章在全书的位置。
- 2026 校准：TaskFlow API（`@task` 装饰器）与 provider 包名为现行主流；上骨架的 Operator 风格仍可运行但非新代码首选 ⚠️。

## 10. 本章实验卡（⚠️ 非原书代码）

1. `airflow dags test spark_daily <date>` 三连：首跑、重跑、改代码后跑——感受「调度状态机的记忆」。
2. 把 aggregate 人为失败一次：观察 `retries` 消耗与最终 `failed` 通知路径——§2「mission-critical 最小配置面」验收。
3. `catchup=False` 起新 DAG 回放历史分区，再 `airflow tasks clear` 补数：两种时间旅行对照（§4）。
4. 连接迁移：把 Spark master 串从 Connection 读取而非硬编码——密钥出代码运动（呼应 5 章）。
5. UI 考古：graph view/gantt 各看一次失败 run——编排器版「看执行」（2 章 UI 训练的调度侧）。

## 11. 校读问答（五问五答）

- **Q：为什么本书用整章讲 Airflow？** A：编排是数据工程师的「第二母语」（01 章版图），也是 mission-critical 的失败处理器——Spark 自己不管「明天还要不要跑」。
- **Q：会讲 CeleryExecutor/KubernetesExecutor 吗？** A：⚠️ 预期点到部署拓扑；深水区与 15 章合流。
- **Q：与 10 章流式怎么共存？** A：流作业不进 cron DAG（长跑进程无「run」概念）；进的是**发布/巡检/恢复演练**类任务——编排与长驻的边界，工程册的诚实话。
- **Q：DAG 即代码的评审面？** A：Python 可 lint/可测/可回滚——比 cron+shell 的进步要讲透，否则读者学成了「带 UI 的 crontab」。
- **Q：Airflow 3.x 还读本章吗？** A：概念层（DAG/依赖/补数/幂等前提）全部有效；Operator 名与默认语义按迁移指南校准（✅ https://airflow.apache.org/docs/）。

## 核心概念速览（中英对照）

- **DAG** — Directed Acyclic Graph：Airflow 的任务依赖声明单元。
- **Operator** — Operator：任务类型模板；SparkSubmitOperator 连 Spark。
- **调度区间** — Data Interval：cron 语义下的数据窗口，补数的坐标轴。
- **catchup** — Catchup：按 start_date 追放历史 run 的开关。
- **backfill** — Backfill：历史分区的显式重放。
- **sensor** — Sensor：等待外部条件（文件/上游 DAG）的任务原语。
- **connection** — Connection：外置的凭据与端点仓库。
- **XCom** — Cross-Command：任务间小量数据传递机制。
- **SLA/回调** — SLA & on_failure_callback：新鲜度承诺的告警实现。
- **provider 包** — Provider Package：Airflow 1.x→2.x 拆分出的外部系统集成件。

## 最新演进与工业实践

- **Airflow 3.0（2025 发布线）**：调度器/执行面重构（TaskSDK、事件驱动、移除旧 UI 的一部分假设），本书 2.x 心智的 DAG 定义仍大体兼容，但 `start_date/catchup` 等默认语义需重校准 ⚠️（官方 ✅ https://airflow.apache.org/docs/ 与迁移指南，引用前实测 200）。
- **数据集/事件驱动调度**：`datasets`（2.10 引入、3.x 强化）把 §4 的跨 DAG 依赖一等公民化——ExternalTaskSensor 手工哨兵退役中（⚠️ 转述）。
- **编排层多元格局**：Dagster（资产模型）、Prefect（flow-as-code）、Argo/FlightRules（K8s 原生）分流企业用例；Airflow 仍是招聘市场最大公约数（⚠️ 观察性陈述）。
- **Spark 提交形态迁移**：Connect/K8s operator 使 `spark-submit` 不再是唯一入口，第 15 章与编排器的集成随之改道（⚠️ 转述）。
- **可观测合流**：OpenLineage 等血缘标准把 Airflow 事件自动转为血缘记录——本书「记日志」清单的产品化去向（⚠️ 观察性陈述）。
