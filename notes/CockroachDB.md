# CockroachDB

CockroachDB是一个支持SQL，支持分布式事务的ACID的分布式数据，支持ANSI SQL的最高隔离级别Serializability。
CockroachDB是一个分布式关系型数据库，主要设计目标是可扩展，强一致和高可靠 。
[CockroachDB 1](https://blog.csdn.net/qq_34924156/article/details/89236693)
[cockroachlabs](https://www.cockroachlabs.com/)

https://github.com/cockroachdb/cockroach/
分布式cache ，alluxio已经做的很好了，不必重复造轮子，也是华裔做的
TIDB生态和社区做的比较好。但从技术讲，cockroachDB是开源的领军者，cockroach在很多核心技术实现上都比TIDB牛逼，cockroch的事务模型，分层lease, mpp 计算引擎，自己专用的存储引擎，去中心话等，非常有特色，特别是事务模型称得上是创新，性能估计是TIDB好几倍。TIDB的中心授时方案与Percolator 是硬伤，5.0 的事务提交优化成了异步提交，估计是参考了cockroach的并行提交.

zoom用了CockroachDB

#### 是 NewSQL 数据库
- NewSQL 是一类兼具传统 SQL 的事务一致性（ACID）和 NoSQL 的水平扩展能力的分布式数据库。
- CockroachDB 正是 NewSQL 的典型代表之一，提供：
  - 强一致性（Strong Consistency）
  - 水平扩展（Horizontal Scalability）
  - SQL 接口（兼容 PostgreSQL 协议）
  - 分布式事务（分布式 ACID 事务）
  - 自动分片与复制（Automatic Sharding & Replication）

#### 被 Zoom 使用
- Zoom确实使用了CockroachDB。
- 根据公开的技术博客和演讲（如 Zoom 在 2021 年的线上分享），Zoom 在其全球基础设施中引入 CockroachDB 来解决多区域（multi-region）数据一致性和高可用问题。
- 特别是在其 账户管理、用户配置、会议元数据 等需要强一致性和全球分布的场景中，CockroachDB 提供了跨区域复制（Geo-Partitioning）能力。
> 参考来源：Zoom Engineering Blog、CockroachDB 官方案例研究（https://www.cockroachlabs.com/customers/zoom）

### CockroachDB 简介

| 特性 | 说明 |
|------|------|
| 类型 | 分布式 NewSQL 数据库 |
| 设计目标 | “像蟑螂一样顽强”（Cockroach = 蟑螂），高容错、高可用 |
| SQL 兼容性 | 兼容 PostgreSQL 协议和语法（客户端驱动兼容） |
| 一致性模型 | 强一致性（基于 Raft 协议） |
| 部署模式 | 支持本地、云、混合云、多区域部署 |
| 开源 | 是（核心功能开源，商业版提供更多企业功能） |
| 适用场景 | 全球分布式应用、金融系统、SaaS 平台、高可用服务 |

### 类似 NewSQL 数据库对比

| 数据库 | 特点 | 与 CockroachDB 区别 |
|--------|------|-------------------|
| Google Spanner | Google 云原生 NewSQL，TrueTime + Paxos，全球一致 | 商业闭源，仅限 GCP |
| TiDB | PingCAP 开发，类 Google Spanner 架构 | 兼容 MySQL 协议 |
| YugabyteDB | 类似 CockroachDB，兼容 PostgreSQL + Redis | 支持文档、KV 模型 |
| CockroachDB | 强一致性、PostgreSQL 兼容、多区域部署 | 专注于全球一致 SQL |

### 总结

> 你所说的“c开头的，Zoom用的newsql数据库”，极大概率就是 CockroachDB。

- C 开头：CockroachDB
- NewSQL：支持分布式事务、SQL 接口、水平扩展
- 被 Zoom 使用：用于全球多区域数据一致性管理


如果你听到的是“Zoom 用的 C 开头 NewSQL”，那几乎可以确定是 CockroachDB。