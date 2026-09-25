# MIT 6.5840 (原 6.824) 分布式系统 【CORE · 全量笔记占位，正文由后续专人完成】

## 课程信息

| 项目 | 内容 |
|---|---|
| 全称 | MIT 6.5840: Distributed Computer Systems Engineering（2023 春起由 6.824 更名，内容不变） |
| 学校 | MIT（PDOS 实验室，与 6.S081 同源） |
| 主讲 | Robert Morris（Morris 病毒作者）、Frans Kaashoek |
| 教材 | 无指定教材，以精读分布式经典论文为主 |
| csdiy 路径 | `并行与分布式系统/MIT6.824`（页面 2026-09 更新） |
| 最新期次 | Spring 2025（schedule: pdos.csail.mit.edu/6.5840/schedule.html） |
| 状态 | CORE：本 README 为完整版章节目录；notes/ papers/ projects/ 留空待专人填充 |

- 课程网站/日程：https://pdos.csail.mit.edu/6.5840/schedule.html
- 视频：见课程网站；中文翻译：mit-public-courses-cn-translatio.gitbook.io/mit6-824
- 语言：Go；作业：5 个 Project（MapReduce → Raft KV → 持久化 → 分片）+ challenges
- csdiy 资源汇总：PKUFlyingPig/MIT6.824；OneSizeFitsQuorum Lab 文档

## 为什么学

- 每讲精读一篇分布式系统奠基论文（MapReduce/GFS/Bigtable/Raft/Spanner…），直接吸收大师的设计取舍。
- Project 以难度著称：从零实现基于 Raft 的容错 KV 存储，在随机性与并发 bug 中淬炼分布式工程能力。
- 是理解 etcd、TiKV、CockroachDB、Kubernetes 等现代开源基础设施共识层的唯一捷径路径。

## 先修与知识联系

- 先修：计算机体系结构、并行编程（CS149/15-418 推荐）、6.S081（系统视角）、熟悉 Go。
- 联系：CS149 讲单机/集群内并行，本课讲跨机的容错与一致性；下游对接 15-721/数据库内核、云存储与 LLM 服务系统（Orca/vLLM 分布式化）。

## 讲义章节目录（最新届 Spring 2025 版整理，以官网 schedule 为准）

| 讲次 | 标题 | 阅读材料（论文） |
|---|---|---|
| L1 | 课程导入：分布式系统核心挑战（RPC 与分层设计） | Birrell & Nelson, RPC (1984) |
| L2 | MapReduce：大规模并行计算的抽象 | Dean & Barroso, OSDI 2004 |
| L3 | GFS：可扩展分布式文件系统 | Ghemawat et al., TOCS 2004 |
| L4 | Bigtable：可扩展分布式存储 | Chang et al., OSDI 2008 |
| L5 | Raft 共识算法（一）：leader 选举与日志复制 | Ongaro & Ousterhout, ATC 2014 |
| L6 | Raft 共识算法（二）：安全性与成员变更 | Ongaro 博士论文相关章节 |
| L7 | 时间、时钟与事件顺序 | Lamport (1978)；Kulkarni et al. (2014) |
| L8 | 面向故障设计：可重复数据读与容错策略 | Fox & Schindler, SIGCOMM CR 2001 等 |
| L9 | Dynamo：高可用 key-store 设计 | DeCandia et al., SOSP 2007 |
| L10 | 云存储与新硬件：S3 演进 / 可组合硬件 | "Unrolling S3" (HotStorage'19)、ElasticBF³ (SIGCOMM'17) |
| L11 | Spanner：可扩展全球数据库 | Corbett et al., TOCS 2013 |
| L12 | 并行数据处理的另一半：Kafka 消息系统 | Kafka: A Distributed Messaging System (2011) |
| L13 | Spark：弹性分布式数据集 | Zaharia et al., NSDI 2012 |
| L14 | 数据并行系统谱系：Millipipe / GraphX / Lightning / Piccolo | Millipipe (OSDI'20) 等节选 |
| L15 | Fabric：面向终端用户的高性能虚拟化 | Anil et al., ATC 2019（或当期替换论文） |
| L16 | TAO：Facebook 社交图谱存储 | Bronson et al., ATC 2013 |
| L17 | 课程复盘与选课指南 | 综合 |

> 注：6.5840 各届后半程论文有轮换（如 Millipipe/S3/Fabric 等），最终目录以当期 schedule.html 逐条对齐后由笔记负责人确认。

## Project 序列（骨架）

| Project | 内容 | 对应讲次 |
|---|---|---|
| pg1 | Go RPC + MapReduce（含容错调度） | L1–L2 |
| pg2 | Raft 选举与日志复制 + 容错 KV（2PC 对照） | L5–L6 |
| pg3 | Raft 持久化、快照与日志压缩 | L5–L9 |
| pg4 | 分片（shard）+ 并发请求处理 + 主迁移 | L4, L9–L11 |
| pg5/challenges | LockTable（部分届次）、Raft challenges、分片 GC 等 | 综合 |

## 目录说明

- `notes/`、`papers/`、`projects/` 目前为**空目录占位**：CORE 课正文（逐讲笔记、论文精读卡片、项目代码）由后续专人负责，勿在本轮填写。
