# MIT 6.5840 (原 6.824) 分布式系统 【CORE · 全量（2026-09）】

## 课程信息

| 项目 | 内容 |
|---|---|
| 全称 | MIT 6.5840: Distributed Computer Systems Engineering（2023 春起由 6.824 更名，内容不变） |
| 学校 | MIT（PDOS 实验室，与 6.S081 同源） |
| 主讲 | Robert Morris（Morris 病毒作者）、Frans Kaashoek |
| 教材 | 无指定教材，以精读分布式经典论文为主 |
| csdiy 路径 | `并行与分布式系统/MIT6.824`（页面 2026-09 更新） |
| 最新期次 | Spring 2025（schedule: pdos.csail.mit.edu/6.5840/schedule.html） |
| 状态 | CORE · 全量（2026-09）：逐讲笔记 notes/L01–L24、论文总表 papers/papers.md、Go 项目 projects/ 全部完成 |

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

## 讲义章节目录（Spring 17 讲骨架 + 官网 2024/2025 日程合并 = 24 讲；以官网 schedule 为准）

| 讲次 | 标题 | 阅读材料（论文） | 笔记 |
|---|---|---|---|
| L01 | 课程导入：分布式系统核心挑战（RPC 与分层设计） | Birrell & Nelson, RPC (1984) | notes/L01 |
| L02 | MapReduce：大规模并行计算的抽象 | Dean & Barroso, OSDI 2004 | notes/L02 |
| L03 | GFS：可扩展分布式文件系统 | Ghemawat et al., SOSP 2003/TOCS 2004 | notes/L03 |
| L04 | Bigtable：可扩展分布式存储 | Chang et al., OSDI 2006 | notes/L04 |
| L05 | Raft（一）：leader 选举与日志复制 | Ongaro & Ousterhout, ATC 2014 | notes/L05 |
| L06 | Raft（二）：安全性、持久化与成员变更 | Ongaro 博士论文相关章节 | notes/L06 |
| L07 | 时间、时钟与事件顺序 | Lamport (1978)；Kulkarni et al. HLC (2014) | notes/L07 |
| L08 | Paxos：共识的原型与难点 | Lamport, Paxos Made Simple (1998/2001) | notes/L08 |
| L09 | 面向故障设计：可重复读与容错策略 | Fox & Schindler (2001)；FTW RPC (NSDI 2006) | notes/L09 |
| L10 | 一致性与线性一致性 | Herlihy & Wing, TOPLAS 1990 | notes/L10 |
| L11 | Dynamo：高可用 key-store 设计 | DeCandia et al., SOSP 2007 | notes/L11 |
| L12 | ZooKeeper 与 ZAB：协调服务产品化 | Hunt et al., ATC 2010 | notes/L12 |
| L13 | 云存储与新硬件：S3 演进 / 可组合硬件 | Unrolling S3 (2017/19)、ElasticBF³ 等 | notes/L13 |
| L14 | 分布式事务与两阶段提交 | Gray (1981)；Helland (2007)；Percolator (2010) | notes/L14 |
| L15 | Spanner：可扩展全球数据库 | Corbett et al., OSDI 2012/TOCS 2013 | notes/L15 |
| L16 | Kafka：分布式消息与日志系统 | Kreps et al., 2011 | notes/L16 |
| L17 | Spark：弹性分布式数据集 | Zaharia et al., NSDI 2012 | notes/L17 |
| L18 | 数据并行系统谱系：Millipipe / GraphX / Lightning / Piccolo | Millipipe (OSDI 2020) 等 | notes/L18 |
| L19 | 链式复制与 CRAQ：读扩展的一致性复制 | van Renesse (OSDI 2004)；CRAQ (ATC 2009) | notes/L19 |
| L20 | Fabric：面向终端用户的高性能虚拟化 | Anil et al., ATC 2019 | notes/L20 |
| L21 | TAO 与 Memcached at Facebook：图谱存储与缓存一致性 | Bronson ATC 2013；Niu NSDI 2013 | notes/L21 |
| L22 | FaRM 与 IronFleet：乐观并发、新硬件与形式化验证 | Kalia NSDI 2014；Hawblitzel SOSP 2015 | notes/L22 |
| L23 | 结构化 P2P：Chord 与 CAN（DHT） | Stoica SIGCOMM 2001；Ratnasamy SIGCOMM 2001 | notes/L23 |
| L24 | 去信任共识：Bitcoin 与 PBFT（附全课复盘） | Nakamoto 2008；Castro & Liskov OSDI 1999 | notes/L24 |

> 注：L08/L10/L12/L14/L19/L22/L23/L24 来自官网 2024/2025 日程（Paxos、Linearizability、
> ZooKeeper、分布式事务、Chain Replication、FaRM/IronFleet、P2P/BFT 等）；
> 各届后半程论文轮换（Millipipe/S3/Fabric/Eagle/SUNDR/Ray/Lambda 等），
> 以当期 schedule.html 为准——笔记的跨讲脉络已覆盖这些主题的交汇点。

## Project 序列

| Project | 内容 | 对应讲次 | 本仓库 |
|---|---|---|---|
| pg1 | Go RPC + MapReduce（含容错调度） | L01–L02 | projects/p1_mapreduce ✅ |
| pg2 | Raft 选举与日志复制 + 容错 KV | L05–L06 | projects/p2_raft + projects/p3_kvraft ✅ |
| pg3 | Raft 持久化、快照与日志压缩 | L05–L09 | 接口已留（lraft.StateStorage），README 列差距 |
| pg4 | 分片（shard）+ 并发请求处理 + 主迁移 | L04, L09–L11 | 未含（README 说明单组→分片的演化） |
| pg5/challenges | LockTable、Raft challenges、分片 GC 等 | 综合 | 延伸建议见各讲笔记 |

## 目录说明

- `notes/`：L01–L24 逐讲中文笔记（论文核心问题/设计/取舍、论文脉络、跨课程联系、
  开源项目应用、延伸阅读）。
- `papers/papers.md`：全课程论文总表（贡献/讲次/工程影响）+ 2021–2026 分布式系统进展表。
- `projects/`：Go 标准库三个渐进项目（MapReduce / Raft / 分布式 KV），
  含 tests 与 build 脚本；本轮只写不编译，执行需本机 Go 工具链（详见 projects/README.md）。
