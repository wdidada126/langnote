# 第 10 章 云中的 MySQL（MySQL in the Cloud ⚠️ 英文章题回推）

> **取证**：小节标题与页码 ✅ 中译本目录；英文章题 ⚠️ 作者站 `/learn/cloud-performance/` 页脚 "**Chapter 10**"；
> 要旨 ⚠️ 依该页 Context + Key Points（8 条）/ Pitfalls（7 条）**精读重构**，**不是原书文本**。
> 官方示例仓库**无** `ch10/`。返回：[00-总览与阅读地图.md](00-总览与阅读地图.md)｜上一章：[09-其他挑战.md](09-其他挑战.md)

## 一句话主旨

**云里的 MySQL 就是你认识的那个 MySQL，只是每一 byte 和每一毫秒都要花钱**
（✅ "Performance is money in the cloud."）——所以本书前九章的实践在云上**不是"依然成立"，而是"更加成立"**；
代价是四件新东西：**兼容性差异、托管边界、网络与存储时延、账单**。

## 10.1 兼容性（✅ 目录，p.284）

✅ Key Points 两句："**云里 MySQL 的代码与特性兼容性各不相同**"；
"**你的尽调义务是：弄清相对开源 MySQL 的一切代码或特性不兼容点**"。
云厂商的 fork 常见差异面（⚠️ 本册补注，非原书清单）：默认参数组、被禁的功能/引擎、
参数暴露范围、版本升级节奏、以及 9.5 说的方言位是否被改写。

## 10.2 管理（✅ 目录，p.285）

✅ Key Point："**MySQL 可以是部分托管或全托管，取决于云厂商或第三方公司**"。
✅ Pitfall 更实用："**'托管'数据库解决方案仍然需要大量用户侧管理**"——
参数组、索引、查询、复制延迟、容量、成本，全都还是你的（第 1–9 章一件都跑不掉）。
另一条权限侧的现实（✅ Pitfall）：**在云上你通常没有 `SUPER` 权限**，
于是第 8 章那些"需要 SUPER 的动作"要改用细粒度动态权限（⚠️ 手册口径见下）。

## 10.3 网络和存储时延（✅ 目录，p.287）

本章最硬的两条物理事实（✅ Key Points）：

1. **广域网网络时延会把查询响应时间抬高"几十到几百毫秒"**；
2. **云里的数据通常存在网络附加存储上，而 NAS 的时延是个位数毫秒——相当于机械盘**（"equivalent to a spinning disk"）。

含义（⚠️ 重构）：第 1 章的"响应时间"在云上多了两个不可压缩项（RTT + 存储往返）；
所以**第 4 章的"减少往返/批量操作"在云上是数量级收益，不是微调**，
而第 2 章"靠硬件解决"的红鲱鱼在云上会直接变成第 10.4 节的账单。
✅ Pitfall 与此对应："**云性能低于预期，尤其是长尾延迟**"。

## 10.4 性能就是金钱（✅ 目录，p.289）

✅ Key Points："**云对一切计费，成本可以（而且经常）超出预算**"；
"**云厂商提供折扣，别付全价**"。
读法（⚠️ 重构）：性能优化在云上多了一个非技术但更硬的理由——
**每一条被消掉的查询、每一页少读的缓存、每一次缩小的工作集都是直接的支出减少**；
✅ Pitfall："**意外的云开销：没有事先仔细核算成本**"。

## 10.5 小结 + 10.6 练习：在云中试用 MySQL（✅ 目录，p.290–291）

作者的收尾判断（✅ Context）："**云并不特殊：幕布后面还是数据中心里的物理服务器在跑 MySQL 这样的程序。**"
⚠️ 练习题面未获取，按小节名与 Pitfall（"不做自己的调研与基准测试"）重构：
在目标云实例上跑一次自己的基准（sysbench/`mysqlslap`），并把测得的**单次提交延迟**、
**同区域 RTT**、**跨区 RTT** 与厂商宣称对齐——**不信宣称（✅ Pitfall 第一条）**。

## 🔧 本机机制类比（**这不是 MySQL、也不是云**）

**"每一次提交都要付一次存储往返"**：2,000 次单行提交的 sqlite3 实验（脚本 `exp.py`，`results.json`）：

| 持久化档位 | 2,000 次提交总耗时 | 每次提交 |
| --- | --- | --- |
| `synchronous=OFF`（可丢数据） | 4,777 ms | 2.389 ms |
| `synchronous=FULL`（每次提交 fsync） | **6,704 ms** | **3.352 ms** |
| **WAL + `synchronous=NORMAL`** | **48 ms** | **0.024 ms** |
| 同样 2,000 行、**合并成 1 个事务** | **8 ms** | 0.004 ms |

三点映射（⚠️ 方向性类比，绝对值与 MySQL 无关）：

1. **提交频率 × 单次 fsync 时延 = 响应时间地板**：把每次提交 3.35 ms 换成"云上 NAS 的个位数毫秒"（✅ 10.3），
   就能理解为什么"每次一行一提交"在云上是设计缺陷；
2. **合并提交（组提交/批量）是数量级手段**（1 个事务 vs 2,000 个：8 ms vs 6,704 ms，**≈838×**）；
3. ** durability 与延迟是一根跷跷板**：`OFF` 与 `FULL` 相差 2 倍，换来的是可丢数据——
   对应 MySQL 的 `innodb_flush_log_at_trx_commit` / `sync_binlog` 取舍（⚠️ 手册口径），
   也和第 7 章"半同步要等确认"付的是同一张账单。
4. 与第 8 章同源的观测：`journal_mode=delete` 下 1,500 次提交 **6,569 ms**，WAL 下 **41 ms**（160×，同 `synchronous=NORMAL`）
   ——**"日志写在哪、什么时候 fsync"这一结构选择，比任何参数微调都更值钱**。

## ⚠️ 官方手册口径与可达性取证（MySQL 8.4 / 云厂商）

- 权限清单与"**从 SUPER 迁移到动态权限**"专节（含 `SYSTEM_VARIABLES_ADMIN`、`REPLICATION_SLAVE_ADMIN`）：
  <https://dev.mysql.com/doc/refman/8.4/en/privileges-provided.html>（✅ 200，本目录已抓取并核对关键词）
- 系统变量与状态变量（云上被限制可改的那一类）：<https://dev.mysql.com/doc/refman/8.4/en/server-system-variables.html>、
  <https://dev.mysql.com/doc/refman/8.4/en/server-status-variables.html>
- 托管服务文档可达性（本环境实测）：AWS RDS for MySQL <https://aws.amazon.com/rds/mysql/> ✅ 200；
  Azure Database for MySQL <https://learn.microsoft.com/en-us/azure/mysql/> ✅ 200；
  Google Cloud SQL for MySQL <https://cloud.google.com/sql/docs/mysql/introduction> **⚠️ 本环境 HTTP 000（不可达），故不引用其内容**
- 官方产品/版本入口：<https://www.mysql.com/products/> ✅ 200

## 本章坑（⚠️ 依作者 Pitfalls 条目重构）

**把厂商宣称当事实** · 不做自己的调研与基准测试 · 不事先核算成本（意外账单） ·
云性能低于预期（**尤其长尾延迟**） · "全托管"其实还要大量用户侧管理 ·
**云厂商发现并切换故障实例的速度慢** · 没有 `SUPER` 权限。

## 对位阅读

- 云原生存储分离的设计自述（Aurora，SIGMOD 2017）与数据仓库弹性（Snowflake，SIGMOD 2016）：见下方 DOI，
  论文线索引 [../../db/db.md](../../db/db.md)
- 前九章在云上的"权重变化"：[01-查询响应时间.md](01-查询响应时间.md)（RTT 进响应时间）、
  [02-索引与索引编制.md](02-索引与索引编制.md)（红鲱鱼=账单）、
  [04-访问模式.md](04-访问模式.md)（往返成本被放大）、
  [06-服务器指标与InnoDB.md](06-服务器指标与InnoDB.md)（吵闹的邻居）、
  [09-其他挑战.md](09-其他挑战.md)（`SUPER` 缺失、HA 自动化风险）
- 硬件与容量视角的传统写法（本书刻意弱化）：[../高性能mysql.md](../高性能mysql.md)、[../数据库高效优化.md](../数据库高效优化.md)
- 云上 MySQL 的运维纵深：[../MySQL运维内参.md](../MySQL运维内参.md)、[../MySQLDBA工作笔记.md](../MySQLDBA工作笔记.md)

## 核心概念速览（中英对照）

- **托管 / 部分托管** — (fully/partially) managed：厂商负责多少取决于服务等级，用户侧仍有大量管理。
- **兼容性尽调** — code and feature compatibility：相对开源 MySQL 的特性/参数差异核查义务。
- **WAN 时延** — wide-area network latency：几十至几百毫秒量级，直接进入响应时间。
- **网络附加存储** — network-attached storage (NAS)：云数据库的常见底座，个位数毫秒时延≈机械盘。
- **长尾延迟** — long tail latency：云上的典型惊喜来源（✅ Pitfall 点名）。
- **性能即金钱** — performance is money：每个 byte、每毫秒都计费。
- **折扣与承诺用量** — committed-use / reserved discount：作者判语"别付全价"。
- **参数组** — parameter group：云上可改参数的边界（⚠️ 厂商侧概念）。
- **`SUPER` 缺失** — no SUPER privilege：托管实例的常见限制，需改用动态权限。
- **故障检测与切换速度** — failover detection time：作者判为云厂商可能偏慢的一环。
- **基准测试义务** — own research and benchmarks：对厂商宣称的唯一有效反驳手段。
- **计算存储分离** — disaggregated storage：云上 MySQL 变体（如 Aurora）的核心结构选择。

## 最新演进与工业实践

**2024–2026 现状**：

1. **"云上是另一套 MySQL"的担忧更具体了**：托管服务普遍基于 8.0/8.4 LTS 打补丁并限制部分参数，
   本目录实测可达的官方文档面：AWS <https://aws.amazon.com/rds/mysql/>（✅ 200）、
   Azure <https://learn.microsoft.com/en-us/azure/mysql/>（✅ 200）；GCP 页面在本环境**不可达（000）**，
   故**不对其现状作任何断言**。
2. **`SUPER` 的退场是本书 Pitfall 的正式解**：MySQL 8.4 提供"从 SUPER 迁移到动态权限"的专节
   （<https://dev.mysql.com/doc/refman/8.4/en/privileges-provided.html> ✅ 已核对含该节标题）——
   云上不能给 `SUPER` 的现实，与官方把权限拆细的方向**是同一件事的两端**。
3. **成本驱动优化（FinOps）已与性能优化合流**：2024 年后"少一次查询=少一笔账单"成为可交付的论证方式，
   这正是本章 10.4 的表述方式在组织层面的胜出。
4. **架构论文线（本目录已做 DOI 校验）**：
   *Amazon Aurora: Design Considerations for High Throughput Cloud-Native Relational Databases*, SIGMOD 2017,
   DOI <https://doi.org/10.1145/3035918.3056101>（✅ Crossref 200）；
   *The Snowflake Elastic Data Warehouse*, SIGMOD 2016, DOI <https://doi.org/10.1145/2882903.2903741>（✅ 200）——
   前者是"云上 MySQL 兼容"的结构性替代方案，后者是"把分析型负载搬离 OLTP 主库"的原型，
   对应本书 5.4 与 4.4 的两条出路。
5. **厂商宣称仍须自测**：作者在本章列的文章（✅ 作者站）包括
   *Are Aurora Performance Claims True?* 与 *COMMIT Latency: Aurora vs. RDS MySQL 8.0*——
   与本章 🔧 的立场一致：**先测提交路径与 RTT，再谈架构选择**。
