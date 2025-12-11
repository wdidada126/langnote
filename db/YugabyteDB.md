# YugabyteDB

https://github.com/yugabyte/yugabyte-db

### YugabyteDB 介绍

YugabyteDB 是一个开源的分布式 SQL 数据库，专为云原生和地理分布式应用设计。它将 PostgreSQL 的强大功能与分布式架构相结合，提供高性能、弹性、可扩展的解决方案，适用于现代事务型工作负载。作为一个 CP（一致性/分区容错）数据库，它支持分布式 ACID 事务、自动分片和自动平衡，彻底避免了传统 RDBMS 在大规模下的瓶颈。YugabyteDB 100% 开源（Apache 2.0 许可），无供应商锁定，支持多云、多 API 部署，已被 Kroger、Nubank 等企业广泛采用。

#### 核心特性
YugabyteDB 的设计强调简单、高可用和性能，以下是其主要特性：

| 特性类别       | 关键功能                                                                 | 益处 |
|----------------|--------------------------------------------------------------------------|------|
| 一致性和事务 | 支持快照隔离（Snapshot Isolation）、可串行化（Serializable）和读已提交（Read Committed）级别；使用混合逻辑时钟（Hybrid Logical Clocks）实现分布式事务。 | 确保强一致性读写，适用于金融支付等高一致性场景。 |
| 可扩展性   | 水平扩展：自动分片（Sharding）和再平衡，支持无限节点添加，无需手动干预。 | 处理互联网级 OLTP 负载（如 5,000+ 核心，<10ms 延迟）。 |
| 高可用性   | Raft 共识协议实现多副本复制（默认 3 副本）；自动故障转移和自愈；支持跨区域同步/异步复制。 | 零停机升级、节点/区域故障恢复，支持多区域部署（如美欧跨洲）。 |
| 多 API 支持 | YSQL（PostgreSQL 兼容，包括 pgvector 扩展用于向量搜索）；YCQL（Cassandra 启发式）；YEDIS（Redis 兼容）。 | 无缝迁移遗留系统，支持关系型和非关系型工作负载。 |
| 安全性与监控 | 端到端加密、角色-based 访问控制（RBAC）；内置连接池和实时监控。 | 简化运维，减少外部工具依赖。 |
| AI/ML 支持 | 原生向量索引（HNSW 算法），支持 RAG 和 GenAI 应用；集成 LangChain、AWS Bedrock 等。 | 处理数亿向量的高维相似性搜索，低延迟查询。 |

#### 架构概述
YugabyteDB 采用分层架构，将查询层与存储层分离，确保分布式环境下的高效协作。不同于传统单机数据库，它是“共享无”（Shared-Nothing）设计，无单点故障。

| 层级/组件          | 描述                                                                 | 作用 |
|--------------------|----------------------------------------------------------------------|------|
| 查询层（Query Layer） | 复用 PostgreSQL 上半部分（YSQL API），处理 SQL 解析、优化和执行。 | 提供熟悉的 PostgreSQL 语义，包括事务重试、错误码和 CDC（变更数据捕获）。 |
| 存储层（DocDB） | 基于 RocksDB 的 LSM 树（Log-Structured Merge-Tree）分布式文档存储；数据以键值对形式分片（Tablet）。 | 自动分片数据到 Tablet，支持内存缓存 + 磁盘持久化；处理写放大和 compaction。 |
| YB-TServer     | 每个节点上的 Tablet Server，负责数据本地操作、复制和分片管理。 | 执行读写、Raft 日志复制；支持从 follower 读取以降低延迟。 |
| YB-Master      | 集群元数据管理器，协调节点注册、分片分配和负载均衡。 | 维护全局拓扑，确保自动再平衡；多 Master 副本实现高可用。 |
| 复制机制       | Raft 共识协议：每个 Tablet 有 Leader 和 Follower 副本，日志追加确保一致性。 | 故障时 Leader 切换 <1s；支持地理分区（Geo-Partitioning）。 |

整体流程：客户端查询 → 查询层路由到 YB-TServer → DocDB 处理分片 → Raft 复制到副本。存储引擎结合内存（MemTable）和磁盘（SSTable），支持压缩和 Bloom 过滤器优化点查。

#### 部署与云支持
YugabyteDB 支持灵活部署：
- YugabyteDB Aeon：全托管服务（AWS、Azure、GCP），Yugabyte 负责运维，提供免费试用集群。
- YugabyteDB Anywhere：半托管工具，用于 Kubernetes、VM 或裸机部署，支持多云/混合环境。
- 自托管：开源二进制或 Docker，直接在 on-prem 或云上运行。

2025 年，它无缝集成 OpenShift 等容器平台，支持 ARM/x86 架构。

#### 2025 年最新更新（v2025.1 系列）
- AI 原生增强：集成 HNSW 索引，支持高效向量相似性搜索；PostgreSQL 分支升级到 15.0，实现运行时兼容。
- 并发性提升：表级锁，支持 DDL/DML 并发，减少 schema 变更冲突。
- 升级优化：原地在线升级/降级，无需停机；xCluster 复制自动同步 YSQL DDL。
- 备份与恢复：分布式备份 GA，支持 DDL 期间备份；CLI 工具 GA。
- 性能改进：CBO（成本优化器）利用 LSM 索引和批处理嵌套循环，提升 PostgreSQL-like 性能。

这些更新使 YugabyteDB 更适合 GenAI 和事件驱动架构（如 Confluent Hub CDC 连接器）。

#### 与其他数据库的比较
YugabyteDB 在分布式 SQL 领域脱颖而出，以下是与 TiDB、CockroachDB 的简要对比（基于 2025 年实践）：

| 维度             | YugabyteDB                          | TiDB                               | CockroachDB                        |
|------------------|-------------------------------------|------------------------------------|------------------------------------|
| API 兼容     | PostgreSQL + Cassandra + Redis      | MySQL + TiKV KV                    | PostgreSQL（较弱向量支持）         |
| 存储引擎     | RocksDB-based DocDB (LSM)           | TiKV (RocksDB)                     | Pebble (LSM)                       |
| 复制协议     | Raft                                | Raft                               | Raft                               |
| 地理分布     | 原生多区域 + 异步/同步复制          | 强，但 MySQL 兼容性更好            | 优秀，但运维复杂                   |
| AI 支持      | HNSW 向量索引 + pgvector            | 通过插件                           | 基本 pgvector                      |
| 开源程度     | 100% 开源，无企业版壁垒             | 100% 开源                          | 核心开源，企业功能收费             |
| 适用场景     | 多 API、GenAI、全球支付             | OLTP + HTAP（混合事务/分析）       | 金融 + 强一致性                    |

YugabyteDB 的优势在于多 API 统一架构和 PostgreSQL 深度兼容，减少迁移成本；相比 TiDB，它在向量/AI 场景更强；相比 CockroachDB，更易用且开源更彻底。

#### 使用场景
- 金融支付：跨区域零停机 ACID 事务（如 Nubank 处理数亿交易）。
- 零售/电商：高并发 OLTP，支持 300 万月活用户（Kroger 案例）。
- GenAI/RAG：低延迟向量搜索，构建 resilient AI 应用。
- SaaS/微服务：地理分区降低延迟，符合数据驻留法规。

总之，YugabyteDB 是构建弹性、全球规模应用的理想选择。它将 PostgreSQL 的开发者友好性与分布式系统的鲁棒性融合，帮助团队避免遗留数据库的扩展痛点。如果你需要部署指南或具体基准测试，推荐查看官方文档或 GitHub 仓库。
