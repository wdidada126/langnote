# 第 1 章 Trino介绍（Overview of Trino ⚠️ 英题推定）

> 对应原书第一部分第 1 章。二级节标题 ✅ 实抓自 [oreilly.com.cn 官方页](http://www.oreilly.com.cn/index.php?func=book&isbn=978-7-111-73160-3)。
> 本文件为精读重构，示例为教学示意，非原书原文。

## 本章地图

| 节 | 内容 | 一句话结论 |
| --- | --- | --- |
| 1.1 大数据带来的问题 | 数据量、数据种类、数据存放地的三重失控；Hadoop 时代批处理管道答不了「现在查一下」 | 问题不是「算不动」，是「数据分散 + 交互式访问」这对矛盾 |
| 1.2 Trino来救场 | Trino = 高性能分布式 SQL 查询引擎，**只查不存**：把计算推到数据旁边 | 「query engine, not a database」是全章题眼 |
| 1.3 Trino使用场景 | 交互式分析、联邦查询、数据迁移/ETL 辅助、长尾数据湖查询、替代单点库 | 场景的共同前提：ANSI SQL + 多数据源 |
| 1.4 Trino资源 | trino.io 文档、Slack、社区广播、GitHub | 官方入口至今有效，见文末「最新演进」 |
| 1.5 Trino简史 | Facebook Presto → PrestoSQL → Trino 更名（本章重点，见下节展开） | 名字换了三次，工程血脉一条 |
| 1.6 小结 | 与第 2 章安装衔接 | 带着「它为什么不存在自己的存储」的问题去装它 |

## 核心精讲

### 1. Trino 不存数据：定位决定一切

Trino 官方定义（✅ [trino.io/docs/current/overview.html](https://trino.io/docs/current/overview.html)）：「a distributed SQL query engine designed to query large data sets distributed over one or more heterogeneous data sources」。三个推论：

1. 没有自己的表存储、没有 WAL、没有副本——持久性责任全在 connector 背后的系统（HDFS/S3/PG…）。
2. 查询失败不丢数据，只是重跑——这使它天然适合「读多写少 + 高频试错」的分析场景。
3. 与「湖仓表格式」正交：Iceberg/Hudi/Delta 管存储协议，Trino 管查询执行（对照 [../Apache_Iceberg活用入門/00-总览与阅读地图.md](../Apache_Iceberg活用入門/00-总览与阅读地图.md) 的「写侧」视角）。

```sql
-- 教学示意：一次查询跨三个异构源，Trino 不搬数据、只做联邦
SELECT o.id, o.total, c.name, l.last_seen
FROM tpch.tiny.orders o
JOIN memory.default.customers c ON c.id = o.custkey
JOIN es.es.logs l ON CAST(l.order_id AS bigint) = o.o_orderkey;  -- 语法细节见 08 章
```

### 2. 适用与不适用（1.3 的判据化）

| 适合 | 不适合 |
| --- | --- |
| BI/即席/Ad-hoc，亚分钟级交互 | 高并发毫秒级点查（那是 OLTP/KV 的活） |
| 跨 Hive/PG/Kafka/S3 的联邦查询 | 重 ETL 写管道（Spark/Flink 更顺，见 07 章 ETL 节） |
| 数据湖上 SQL 化（配 Iceberg/Hive） | 依赖行级事务的混合负载 |
| 迁移期「新旧库并行验证」 | 需要物化视图全增量刷新编排（Trino 的 MV 偏手动，见 06 章） |

### 3. Trino 简史（1.5）：一条线背下来

- **2012**：Presto 在 Facebook 内部立项（✅ 腾讯科技 2019 报道口径，[实抓](https://m.techweb.com.cn/article/2019-09-24/2755811.shtml)），**2013 前后开源**（开源具体月份 ⚠️ 未本次核实）。
- **2019-01 起**：核心贡献者与 Meta 在治理/商标上分歧，社区侧独立成 **PrestoSQL** 项目（月序 ⚠️ 依中文转载口径，[CSDN 实抓](https://blog.csdn.net/wypblog/article/details/112001074)）。
- **2019-09-24**：Meta/阿里/Twitter/Uber 成立 **Presto 基金会，Linux 基金会托管**——prestodb 线定名（✅ 同上 techweb 实抓）。
- **2020-12-27**：PrestoSQL 官方公告更名 **Trino**（「Announcing Trino」；原链已 404 ⚠️，日期/标题由官方 blog feed 与转载旁证）。动机：脱离商标纠纷，Presto 商标在基金会手里，Trino = **Tri**（三）+ Pr**esto** + **O**（SQL），暗指「社区/用户/贡献者」三方（词源细节 ⚠️ 转述口径）。
- **2022-04**：成立 Trino 软件基金会 TSF，特拉华州独立非营利，**不入**任何大基金会（✅ [trino.io/foundation](https://trino.io/foundation) 实抓；董事会含 Martin Traverso——本书作者之一，Presto 创始成员，[oreilly.com.cn 作者简介](http://www.oreilly.com.cn/index.php?func=book&isbn=978-7-111-73160-3) ✅）。
- **本书沿革** ✅（[trino.io 书页](https://trino.io/trino-the-definitive-guide.html) 实抓）：2020-04 出版为 *Presto: The Definitive Guide* → 2021-04 一修改为 *Trino: The Definitive Guide* → **2022-10 第二版**（基线 Trino 392）。

### 4. 版本命名的小坑（书 1.5 的隐含考点）

351 之前是版本号 = PrestoSQL release 号；Trino 沿用整数递增、无 LTS 语义，约每月 1–2 版。书基线 392（2022-08）与本目录基线 483（2026-07）之间，**安装物从 tar.gz 变为多形态（见 02/05 章）**、connector 面大幅扩张（见 06 章）。

### 5. 双谱系分流一览（1.5 的表格式记忆版）

| 时间 | Trino 线（本册主角） | Presto/prestodb 线 |
| --- | --- | --- |
| 2012–2013 | 同源：Facebook Presto 立项→开源 | 同左 |
| 2019-01 前后 | 社区成员出走，独立治理酝酿（月序 ⚠️） | Meta 强化控制路线 |
| 2019-09 | 社区项目定名 PrestoSQL | Presto 基金会成立、LF 托管 ✅（[techweb/腾讯科技](https://m.techweb.com.cn/article/2019-09-24/2755811.shtml)） |
| 2020-12-27 | PrestoSQL → **Trino** 更名公告（原页 404 ⚠️，标题日期多源旁证） | 商标之争定局 |
| 2021–2022 | 352+ 快速迭代；本书 1e 改名 Trino（2021-04 ✅） | 保持 Presto 0.2xx 版本号风格 |
| 2022-10 | 本书 2e（基线 392）✅ trino.io | 双方言区持续互不兼容 |
| 2022-04→今 | TSF 独立基金会治理 ✅（[trino.io/foundation](https://trino.io/foundation)） | LF 生态内（LFX 收录 ✅） |
| 2026-07 | 483 发布 ✅ | 各自发布线并行（数字未核 ⚠️） |

### 6. 本章的三问自测

1. 为什么 Trino 不自己做存储？（提示：4.2 connector SPI + 湖上「存协议」的繁荣期恰是 2019–2022。）
2. 为什么一个开源项目能改名两次还有人跟？（治理与商标，而非代码质量。）
3. 你的场景里「联邦」是真的吗？（若只有一个数据源，答案可能是 DuckDB/PG，见 00 章第七节三角。）

### 7. 名字、项目与商标的一张关系图

```
Facebook Presto (2012–)
 ├─ prestodb / Presto 基金会 (2019-09, LF 托管 ✅)      → 02 线：版本号 0.2xx
 └─ 社区侧 PrestoSQL (2019–2020)
        └─ 更名 Trino (公告 2020-12-27 ⚠️原页404)       → 版本号 3xx–483 ✅
             └─ Trino 软件基金会 TSF (2022 ✅) ← 本书 1e/2e 的服务对象
```

「Trino」一词的读法与拼写官方口径为小写品牌感强（社区惯写 Trino，包名 `io.trino`，镜像 `trinodb/trino`）——搜证时先对齐这四个符号，能过滤九成 Presto 时代的旧文档。

## 常见误区

- 「Trino 是又一个数据库」——它是引擎；问「表存在哪」的答案永远是某个 connector 背后。
- 「Presto 和 Trino 是两个产品」——2020 年底之前它们是同一个；之后分叉，SQL 方言仍高度同源但发行物、connector、版本互不兼容（《Presto实战》书目与本册的分工即在此，见 [00 章](00-总览与阅读地图.md) 预留互链说明）。
- 「作者署名按任务书」——任务书曾猜「manfred moskwiak」，实为 **Manfred Moser** + Martin Traverso（✅ 双源实抓，见 00 元数据表勘误）。

## 与其他章/其他书的联系

- 本章「只查不存」→ 架构机制在 [04-Trino架构.md](04-Trino架构.md)；「资源」→ 安装见 [02-安装和配置Trino.md](02-安装和配置Trino.md)。
- Spark SQL 对照：[../bigdata/04-SparkSQL与结构化数据.md](../bigdata/04-SparkSQL与结构化数据.md)；引擎演进史：[../bigdata/10-计算引擎的演进.md](../bigdata/10-计算引擎的演进.md)。
- 分叉史的社会维度（基金会/商标）可与 [../分布式系列·总索引.md](../分布式系列·总索引.md) 所收开源治理类笔记互读。

## 核心概念速览（中英对照）

1. **联邦查询** — federated query：一条 SQL 同时查多个异构数据源，由 coordinator 分派。
2. **存算分离** — separation of storage and computation：Trino 无自有存储，持久化在 connector 对端。
3. **即席查询** — ad hoc query：亚分钟级、高频试错的交互式分析负载。
4. **查询引擎** — query engine：解析-优化-执行 SQL 的软件层，区别于 database（含存储）。
5. **连接器** — connector：Trino 访问外部数据源的插件接口（04/06 章展开）。
6. **catalog** — catalog：connector 实例的命名挂载点，其下含 schema/table 层级。
7. **Presto** — Presto：Facebook 2012 年立项的原始项目，双分叉之源头。
8. **PrestoSQL** — PrestoSQL：2019 年社区侧独立项目名，Trino 的直接前身。
9. **Trino 更名** — rename to Trino：2020-12-27 公告，为绕开 Presto 商标归属。
10. **Trino 软件基金会** — Trino Software Foundation (TSF)：2022 年成立的特拉华州独立非营利治理体。
11. **Presto 基金会** — Presto Foundation：2019-09 成立、Linux 基金会托管的另一支。
12. **ANSI SQL 兼容** — ANSI SQL compliant：以标准 SQL 为方言基线（Trino 自称兼容度高于多数引擎）。
13. **早期发布** — early release：O'Reilly 未定稿电子版，本书 2e 的 2022-10 口径含此形态 ⚠️。
14. **版本基线** — version baseline：2e 基于 Trino 392；本目录对照 483。
15. **数据湖查询** — data lake querying：在对象存储 + 开放表格式上做 SQL 分析，本书主战场。

## 最新演进与工业实践

- **发布线到 483（2026-07）**：GitHub API 实抓 `https://api.github.com/repos/trinodb/trino/releases/latest` → tag `483`，[releases 页](https://github.com/trinodb/trino/releases) 可达；[官方逐版发布记录](https://trino.io/docs/current/release/release-483.html) 可回溯 392→483 全部日期（✅）。
- **双基金会现状（分流）**：Trino 走独立 TSF（✅ [trino.io/foundation](https://trino.io/foundation)）；prestodb 侧在 Linux 基金会生态，现状可核实为 LFX 项目目录收录（✅ [insights.linuxfoundation.org/project/presto](https://insights.linuxfoundation.org/project/presto)、[github.com/prestodb/presto](https://github.com/prestodb/presto)）；任务书「2024 加入 LF」的独立公告本机无法核实 ⚠️（prestodb.io 被 Cloudflare 403 拦截）。
- **选型三角**：湖仓读端 Trino、ETL 端 Spark SQL（✅ [spark.apache.org/sql/](https://spark.apache.org/sql/)）、单机端 DuckDB（✅ [duckdb.org](https://duckdb.org/)）；repo 内坐标见 [../bigdata/00-总览与阅读地图.md](../bigdata/00-总览与阅读地图.md) 与 [../数据仓库与OLAP实践教程.md](../数据仓库与OLAP实践教程.md)。
- **官方入口现状** ✅：文档 [trino.io/docs/current/overview.html](https://trino.io/docs/current/overview.html)、用户名录 [trino.io/users.html](https://trino.io/users.html)（工业采用公开证据以此页与 Slack 社区为准；书中所举公司案例未逐家复核 ⚠️）。
- **Presto 论文遗产**：Presto 的技术论文（ICDE 2019，Adya et al. 口径 ⚠️ 未过 CrossRef 逐条核验，故不给 DOI 链接）仍是理解 coordinator 设计的最佳单一文献；理论面配 [../Readings_in_Database_Systems/00-总览与阅读地图.md](../Readings_in_Database_Systems/00-总览与阅读地图.md) 的 MPP 条目与 [../../db/db.md](../../db/db.md) 论文线。
