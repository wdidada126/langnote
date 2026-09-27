# 03 使用 Presto

> 原书第 3 章（中译本 p.22–36）。定位：四类客户端 + 第一串真正跑通的 SQL。
> 返回 [00-总览与阅读地图.md](00-总览与阅读地图.md)。

## 本章地图

| 节 | 内容 | 一句话结论 |
| --- | --- | --- |
| 3.1 Presto CLI | 分页、命令历史、额外诊断、执行查询、输出格式、忽略错误 | 交互探索的最佳"手感"工具（Java 写的瘦客户端） |
| 3.2 JDBC 驱动 | 下载注册、`jdbc:presto://host:port/catalog/schema`、properties 传会话属性 | BI/Java 应用的通道；认证参数也在此传 |
| 3.3 ODBC | 面向 Excel/BI 的老桥 | 时代产物，当代更多用 REST/Arrow 通道 |
| 3.4 客户端库 | presto-python-client、prestodb（社区版）等按语言薄封装 REST API | 协议是 REST+JSON，封装都很薄 |
| 3.5 Web UI | 查询列表/阶段 DAG/实时进度 | 运维与 debug 第一现场（深化在 12.1） |
| 3.6 执行 SQL | 概念 + 鸢尾花入门案例 | catalog.schema.table 三段式命名 + SELECT 全家桶 |

## 精讲

### 1. 一切客户端都薄，重量全在引擎
CLI/JDBC/ODBC/Python 只是 REST `/v1/statement` 协议的不同外衣：查询提交后服务端返回
nextURI 链式轮询直至完成。由此推论：
- 客户端语言生态"够用即可"，没有厚 SDK 的错觉；
- **会话属性**（`session.query_priority` 之类）统一经 `X-Presto-Session` 头传递，各客户端只是语法糖；
- 网络抖动导致的"客户端断、查询亡"是设计使然——需要结果持久化就得 `CREATE TABLE ... AS` 落表（第 8.6.3 节）。
⚠️ 具体头名按你所用发行版/版本核对。

### 2. 三段式命名与"当前目录"
`catalog.schema.table` 是全限定形态；CLI 的 `--catalog/--schema` 与 JDBC URL 的尾段决定默认前缀。
联邦查询的第一课就是刻意写全限定名，让 `mysql.sales.orders` 与 `hive.dwd.orders` 同屏对比——
这正是 1.3.4 场景的操作化身（更多跨源实例在 7.6）。

### 3. 入门案例的解剖（3.6.2 鸢尾花）
```sql
SELECT species, ROUND(AVG("sepal length in cm"), 2) AS avg_len
FROM iris.iris.iris_dataset
GROUP BY species
ORDER BY avg_len DESC;
```
五步心智：三段定位表 → 带空格列名需双引号（ANSI 引用标识符）→ 聚合在 worker 分片做局部聚合、
协调器汇总（第 4.9.4 的"局部聚合"优化在此已默默生效）→ ORDER BY/LIMIT 是全局收尾算子 → 结果经 nextURI 分批回传（3.1.2 分页）。

### 4. CLI 的工程细节
- `--paginate`：pager 配合大结果；`--debug`/`--extra-credential` 等把协议头暴露成命令行；
- 退出码与 `--ignore-errors`：脚本化使用时"错误不中断批处理"的取舍；
- 输出格式 `--output-format=CSV`/ALIGNED：管道喂给下游的最优解。
**方法**（🔧 教学可复现性验证，需任一可跑的 Presto/Trino 实例；无实例时用 tpch 内存拓扑，参见 02 章第 3 节）：
同一查询分别用 CLI/JDBC 跑一次，在 Web UI 里看到两条 Query ID 的 stage 图完全同形——即"客户端薄"的铁证。

### 5. Web UI 的第一眼
本章只教"认门"：列表页看 state（QUEUED/PLANNING/RUNNING/FINISHING）、执行时间、进度条；
点进单查询看 stage DAG。真正的调优读图法在 [12-生产环境中的Presto.md](12-生产环境中的Presto.md) 12.1 展开。

## 常见误区

| 误区 | 现实 |
| --- | --- |
| JDBC 连接池 = 会话保持 | 每个连接独立 session；SET SESSION 属性不跨连接，池化后"配置漂移"常见 |
| CLI 大结果刷屏是渲染慢 | 是 nextURI 全量拉回；先 LIMIT/物化再浏览 |
| 双引号可以换成反引号 | Presto 按 ANSI：双引号引用标识符、单引号字符串；反引号是 Hive 习惯，直接报错 |
| Web UI 关掉查询就没了 | 默认保留窗口有限；审计需事件监听器（第 10/12 章安全运维配套）⚠️ 默认保留时长按版本核对 |

## 与其他章/其他笔记的联系
- 命名空间与 DDL 全貌 → [08-在Presto中使用SQL.md](08-在Presto中使用SQL.md)；函数与高级特性 → [09-高级SQL特性.md](09-高级SQL特性.md)；
- 执行模型（为什么客户端只需轮询）→ [04-Presto的架构.md](04-Presto的架构.md) 4.7；
- SQL 语法与通用 SQL 习惯差异 → [../SQL系列·总索引.md](../SQL系列·总索引.md) 内 ANSI 方言相关条目；
- 与 Spark SQL 客户端生态对比 → [../bigdata/04-SparkSQL与结构化数据.md](../bigdata/04-SparkSQL与结构化数据.md)。

## 本章小结与行动清单

三句话带走：
1. "客户端薄、协议简单、重量全在引擎"是本技术栈最反直觉也最解放的一点——选客户端只看团队语言栈，不用供着；
2. 双引号/CAST/三段式三个 ANSI 纪律，是从 Hive/MySQL 迁来的团队最先交的学费（8 章整章在还这笔账）；
3. 每次"客户端问题"都应先在 Web UI 复核定性与 stage 形态，再怀疑驱动/网络——多数锅在查询本身。

实操检查单：
- [ ] 同一查询分别经 CLI、JDBC（任意 Java/Python 程序）、REST 手撸轮询三条路发起，确认计划与结果一致（协议同构铁证）；
- [ ] `SET SESSION` 一个参数（如时区）后重跑含 `now()` 的查询，观察会话级生效边界；
- [ ] 故意跑一个必失败的查询（错列名），记录三客户端各自的报错形态与信息保真度（行号/列名/位置）；
- [ ] 在 Web UI 找到刚才三条查询记录并对比，确认列表保留窗口内可回看。

自测：
- [ ] 客户端断网后查询会怎样？为什么？要保住结果该怎么办？（事件轮询+结果持久化）
- [ ] 连接池场景下 SET SESSION 为什么会"漂移"？工程上怎么钉死会话属性？

一句话总结：**把客户端当浏览器，把引擎当网站**——所有"接入层玄学"都能在 Web UI 的查询详情里找到真相。

## 核心概念速览（中英对照）

| 术语 | English | 释义 |
| --- | --- | --- |
| Presto CLI | Presto CLI | Java 实现的终端瘦客户端 |
| 语句协议 | Statement REST Protocol | `/v1/statement` + nextURI 链式取结果的交互协议 |
| 会话属性 | Session Properties | 按查询/会话生效的引擎参数，经头或参数传递 |
| JDBC 驱动 | JDBC Driver | BI 与 Java 应用接入的标准通道 `jdbc:presto://...` |
| ODBC 驱动 | ODBC Driver | C 层 BI 桥（Excel/Tableau 旧链路） |
| 三段式命名 | Three-part Name | `catalog.schema.table` 全限定对象名 |
| 引用标识符 | Quoted Identifier | 双引号包裹含空格/保留字的列名 |
| 分页输出 | Paginated Output | CLI 用 pager 呈现大结果的模式 |
| 输出格式 | Output Format | ALIGNED/CSV 等结果呈现选项 |
| Web UI | Web UI | 协调器内建的查询监控页面 |
| 查询状态机 | Query State Machine | QUEUED→PLANNING→RUNNING→FINISHING→DONE 的生命周期 |
| 事件轮询 | NextURI Polling | 客户端反复 GET nextURI 直到查询完成的模式 |
| 客户端库 | Client Libraries | presto-python-client 等薄封装 |

## 最新演进与工业实践

- **客户端生态现状（2024–2026）**：CLI 与 Python/Go/Java 官方客户端在两条线均持续维护；
  更值得关注的是**结果通道加速**：Arrow Flight SQL 等列式结果流进入讨论与实现序列（Trino 实验特性 ⚠️ 以
  [trino.io/docs/current/overview.html](https://trino.io/docs/current/overview.html) 及各 Release Notes 为准；
  [github.com/trinodb/trino](https://github.com/trinodb/trino) ✅）。
- **Web UI 的后继者**：开源替代/增强（查询详情可视化、慢查询分析器）社区项目众多；
  官方 UI 源码随主仓演进（[github.com/prestodb/presto](https://github.com/prestodb/presto) ✅ 200）。
- **BI 接入的现实迁移**：Excel-ODBC 链路收缩，Superset/Metabase/Looker 等直连 REST/JDBC 成主流；
  Superset 集成在本书 11.1，跨源 BI 的当代形态互见
  [../Apache_Paimon_Streaming_Lakehouse/12-多引擎生态与四大湖格式对比.md](../Apache_Paimon_Streaming_Lakehouse/12-多引擎生态与四大湖格式对比.md)。
- **国内印证**：B 站把 AdHoc/BI/DQC/数据探查统一由 Dispatcher 路由到 Presto 等引擎——
  即"客户端薄、调度厚"的工业版——[dbaplus 原文](https://dbaplus.cn/news-73-4481-1.html) ✅；
  美团点评的 AdHoc 统一查询引擎分享（演讲稿镜像）[tool.lu/deck/L6/detail](https://tool.lu/deck/L6/detail)（⚠️ 第三方镜像，原稿为对外技术分享）。
- **论文延伸**：REST+流水线交互协议的设计在 *Presto: SQL on Everything*（ICDE 2019,
  DOI [10.1109/icde.2019.00196](https://doi.org/10.1109/icde.2019.00196) ✅ Crossref 校验）有专节描述；条目见 [../../db/db.md](../../db/db.md)。
