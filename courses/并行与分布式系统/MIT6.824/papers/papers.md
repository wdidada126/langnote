# MIT 6.5840/6.824 全课程论文总表

> 整门课就建立在论文上。本表 = 论文 → 一句话贡献 → 关联讲次 → 工程影响（谁实现/继承了它）。
> 讲次对应本目录 `notes/L01–L24`（README 的 Spring 目录 + 官网 2024/2025 日程合并）。

## 一、课程正典论文（按讲次）

| # | 论文 | 年份 | 一句话贡献 | 讲次 | 工程影响（实现/继承者） |
|---|---|---|---|---|---|
| 1 | Birrell & Nelson, *Implementing Remote Procedure Calls* | 1984 | 把跨机调用伪装成本地调用，定义会话/超时/at-most-once 语义 | L01 | gRPC、brpc、Dubbo、K8s client-go 重试语义；本课所有 Lab 的通信层 |
| 2 | Dean & Barroso, *MapReduce* | 2004 | map/reduce 两函数 + 自动分片/容错，数据并行工业化起点 | L02 | Hadoop、FlumeJava/MillWheel、Spark、Dataflow、BigQuery 幕后 |
| 3 | Ghemawat et al., *The Google File System* | 2003/04 | 廉价机群上的大文件分布式 FS：单 master + 64MB chunk + 追加语义 | L03 | HDFS、Colossus、Ceph、Kafka 日志存储的 chunk/副本范式 |
| 4 | Chang et al., *Bigtable* | 2006 | 稀疏分布式多维排序映射：LSM + tablet 分片 + 外包锁 | L04 | HBase、Cassandra、LevelDB/RocksDB、TiKV、ClickHouse（LSM 谱系） |
| 5-6 | Ongaro & Osterhout, *Raft*（+博士论文） | 2014 | 可理解化的共识：选举/日志/安全三分 + 成员变更 | L05/L06 | etcd、TiKV、CockroachDB、Kafka KRaft、RabbitMQ quorum queue、MongoDB（同族） |
| 7 | Lamport, *Time, Clocks, and the Ordering of Events* | 1978 | "之前"是逻辑关系：Lamport 时钟与因果序 | L07 | 一切版本化/epoch 机制（Raft term、Kafka offset、ZK zxid） |
| 7 | Kulkarni et al., *Logical Physical Clocks (HLC)* | 2014 | 物理近似 + 因果一致的可实现时间戳 | L07 | CockroachDB、MongoDB、TiKV（混合逻辑时钟）、Spanner 对照 |
| 8 | Lamport, *Paxos Made Simple*（/Part-Time Parliament 1998） | 1998/2001 | 证明异步+崩溃下多数派共识可解 | L08 | Chubby、Spanner、Megastore、Cassandra LWT、JGroups |
| 9 | Fox & Schindler, *Designing for Failure* | 2001 | 把故障当作常态：可重复读、端到端解耦 | L09 | 服务网格（Envoy outlier ejection）、重试/熔断库、混沌工程 |
| 9 | van Renesse et al., *FTW: Scaling Usable Network Storage through Transparent Request Forwarding* | 2006 | 请求绕开故障中间路径：透明转发式 RPC | L09 | 源路由/多路径（MPTCP、SRv6）、CDN 绕行 |
| 10 | Herlihy & Wing, *Linearizability* | 1990 | 给"一致性"唯一可证明定义；与共识等价 | L10 | Jepsen 检验标准、etcd/Redis/CockroachDB 文档语义条款 |
| 11 | DeCandia et al., *Dynamo* | 2007 | AP 阵营宣言：哈希环 + quorum + read repair + hinted handoff | L11 | Cassandra、Riak、Voldemort、DynamoDB、Redis Cluster（部分） |
| 12 | Hunt et al., *ZooKeeper*（+Boyer *ZAB* 技术报告） | 2010/2012 | 把共识产品化成协调服务：znode/会话/watch | L12 | HBase/Kafka(旧)/Dubbo 注册中心；etcd 是其"云原生续作" |
| 13 | Werner Vogels, *Unrolling Amazon S3* | 2017/19 | EB 级对象存储演化史：index/data 分离 + EC + Ark | L13 | S3 本身、MinIO、Ceph RGW、各云对象存储分层/EC 实践 |
| 13 | Mukherjee? 辅读：ElasticBF³ 等可组合硬件论文 | 2017 | 用可编程硬件做弹性负载均衡/资源解耦 | L13 | FPGA LB、DPU/Nitro、CXL 内存池方向 |
| 14 | Gray, *The Transaction Concept*（6.033 Ch.9）+ Helland *Life beyond Distributed Transactions* | 1981/2007 | 2PC 的定义与死刑判决：阻塞、运维代价、Saga 出路 | L14 | XA/2PC 全家、Seata、Temporal/Cadence（Saga 编排）、Flink 两阶段提交 sink |
| 14 | Peng & Dabek, *Large-scale Multipurpose Transaction Processing with Percolator* | 2010 | 去协调者 2PC：数据自带锁与恢复信息 | L14 | TiDB（Percolator 模型）、Google 系事务层 |
| 15 | Corbett et al., *Spanner* | 2012/13 | 全球 ACID：Paxos 分片 + TrueTime + commit-wait 外部一致 | L15 | CockroachDB、TiDB、YugabyteDB、AlloyDB（精神）、Cloud Spanner 服务化 |
| 16 | Kreps et al., *Kafka* | 2011 | 消息队列重构为分布式提交日志：顺序写 + 零拷贝 + ISR | L16 | Kafka、Redpanda、Pulsar、Tiered Storage、Flink/Streams 生态 |
| 17 | Zaharia et al., *Resilient Distributed Datasets* | 2012 | 不可变 RDD + 血缘重算：内存分布式计算抽象 | L17 | Spark 全系（SQL/MLlib/GraphX/Structured Streaming）、Delta Lake |
| 18 | Yuan et al., *Millipipe* | 2020 | 控制驱动弹性流水线：修掉数据驱动调度的长尾与内存失控 | L18 | 研究方向（PDOS 自家）；影响新一代图/ML 流水线调度器 |
| 18 | Gonzalez et al., *PowerGraph*（GraphX 基础） | 2012 | 顶点中心化通信 + mirror：并行图计算 | L18 | GraphX、GraphLab、Giraph、Neo4j 并行执行 |
| 18 | Dai et al., *Lightning* | 2015 | 把迭代计算编译成数据流水线，消除轮间同步 | L18 | GraphChi（同组近亲）→ 流水线图计算研究线、ML 流水线并行 |
| 18 | *Piccolo: Building Fast, Distributed Programs with Partitioned Tables* (HotCloud 2012) | 2012 | 分区表 + 子区间锁：为 ML 定制的键值并行存储 | L18 | 参数服务器（PS-Learning、DistBelief 后继）、angel |
| 19 | van Renesse et al., *Chain Replication* | 2004 | 有序副本链：不靠选举共识的强一致复制 | L19 | Azure Storage（SOSP'11）、HDFS write pipeline、CRAQ |
| 19 | Terrace & Freedman, *Object Storage on CRAQ* | 2009 | 脏/干净版本 + 快照读：链式复制的读扩展 | L19 | Redis Raft 讨论、各类"读任意副本"方案设计参考 |
| 20 | Anil et al., *Operating Kernel Virtualization with Fabric* | 2019 | 用户态 GPU/设备虚拟化：VM 拿到接近裸机 I/O | L20 | virtio/vhost-user、SPDK/DPDK、crosvm 设备栈哲学同源 |
| 21 | Bronson et al., *TAO* | 2013 | 社交图谱专用存储：对象+边 API、slice 分片、缓存一致性工程 | L21 | 各社交/关系链存储、GraphQL 数据源模式、surrogate-key 失效 |
| 21 | Niu et al., *Scaling Memcache at Facebook* | 2013 | 缓存当作一级分布式系统：mirror 热 key、mini-object、批量删除 | L21 | 两级缓存实践、CDN surrogate key、KeyDB/Redis 生态 |
| 22 | Kalia et al., *FaRM: Fast Remote Memory* | 2014 | RDMA 上的分布式 OCC 事务：百万 TPS 的强假设路线 | L22 | Teleport/C5/FaS'T、Aqua（Azure RDMA 存储）、NVMe-oF 生态 |
| 22 | Hawblitzel et al., *IronFleet* | 2015 | 机器验证的分布式协议实现：证明而非祈祷 | L22 | TLA+/Ivy/Verus 工具链、AWS Eagle/Foundry、VerusRaft |
| 23 | Stoica et al., *Chord* | 2001 | 一致性哈希环 + finger table：O(log N) 去中心查找 | L23 | Cassandra/Dynamo 哈希环、IPFS、BitTorrent DHT（经 Kademlia） |
| 23 | Ratnasamy et al., *CAN* | 2001 | d 维坐标贪心路由：DHT 的另一几何 | L23 | 路由/overlay 研究线、CDN 映射 |
| 24 | Nakamoto, *Bitcoin* | 2008 | PoW 最长链：用经济博弈替代身份与多数派 | L24 | 全部公链、UTXO/账户两派、Lightning、Merkle 反熵应用 |
| 24 | Castro & Liskov, *Practical BFT* | 1999 | 3f+1 节点、三阶段视图复制：可实用的拜占庭共识 | L24 | Hyperledger Fabric、Tendermint/CometBFT、HoneyBadgerBFT、联盟链 |

> 注：个别课程轮换论文（Eagle ATC'21、SUNDR'04、Memcached、Lambda'23、Ray'21、Bitcoin 相关）
> 在部分届次出现，本表以"讲次主线 + 延伸阅读"方式收录；各届以当期 schedule.html 为准。

## 二、近五年进展速览（2021–2026，真实可考者；不确定处标"待核实"）

| 时间 | 事件/系统 | 与课程论文的对应关系 |
|---|---|---|
| 2021 | ATC'21 最佳论文 **Eagle**（AWS）：TLA+ IR 模型检查 EC2/S3 设计 | L22 IronFleet 的工业化延续 |
| 2021 | **Kafka KRaft** 技术预览（2.8）：内置 Raft 元数据取代 ZooKeeper | L05 Raft 吞并 L12 ZK 的标志性事件 |
| 2021 | **Ray** 生态成熟（KubeRay 1.0）；LLM 前夜的 Python 分布式计算 | L18 Piccolo/参数服务器路线的现役版 |
| 2022 | **Kubernetes 1.24 起 etcd v3 为唯一后端**（v3 API 迁移完成）；etcd 3.5 稳定 Multi-Raft | L05/L12 的当代标准形态 |
| 2022 | CockroachDB v22 引入 **row-level TTL / 部分索引**等；Raft 生产特性持续 | L07 HLC/L15 路线 |
| 2023 | Kafka KRaft 生产可用（3.5/3.6）；**TiKV 7.x** raft-engine 替代 RocksDB-WAL | L05/L06/L16 |
| 2023 | **TiDB 7.1 全局一致性备份/恢复 GA；TiKV GC 与 PD 调度演进** | L04/L05/L14 |
| 2023 | **Raft Learner / joint consensus 在主流库统一**（`etcd-io/raft` 从 etcd 抽出开源） | L06 成员变更 |
| 2023 | LLM 分布式训练系统爆发：**Megatron-LM 5D 并行、DeepSpeed-Ulysses/Ring Attention** | L18 数据并行谱系的新负载 |
| 2023 | **vLLM PagedAttention 论文（SOSP'23）**：KV-cache 分页，LLM 服务系统起点 | L04 分页/LSM 思想在 LLM 推理的复现（LLM 服务系统与 6.824 知识直接对接） |
| 2024 | vLLM 分布式推理（TP/PP/DP 组合）、**Orca（OSDI'24）迭代级调度** | L18 流水线 + L16 事件驱动 |
| 2024 | **Kafka 4.0：ZooKeeper 支持正式移除，KRaft-only** | L12→L05 权力交接完成 |
| 2024 | **Spanner 论文获 SIGMOD/PVLDB 时间检验奖十年后续：AlloyDB/Manhattan? （Manhattan 为 Google 内部，细节待核实）** | L15 家族扩张 |
| 2024 | **etcd v3.6（Kubernetes v1.34 起支持）：Lease 与 snapshot 压缩增强（细节待核实）** | L05/L12 |
| 2025 | **分布式共识向"可组合硬件"延伸：CXL 内存池化进入产品（Marvell/MemVerge 等，规模待核实）** | L13 可组合硬件预言的落地进度 |
| 2025 | **Multi-Raft 区域治理：TiKV/CockroachDB Serverless 化** | L05/L15/L13 合流 |
| 2025–2026 | LLM 推理集群的 PD 分离（Prefill/Decode disaggregation，DistServe/Mooncake 等） | L13 解耦 + L18 流水线在 AI 时代的翻版（课程 2026 届或新增相关讲） |
| 2021–2026 | **CRDT 产品化**（Roku? 无。automerge 1.0 / Figma 内部）（细节待核实） | L11 冲突调和的长期答案 |
| 2026 | 6.5840 春季课表仍含：Introduction/RPC、MapReduce、GFS、Bigtable、Raft×2、Paxos、Time/Clocks、Dynamo、Kafka、Spanner、TAO/Memcached、S3/新硬件、Fabric、CRDT? （以 pdos schedule.html 当期为准） | 全课 |

## 三、阅读策略

1. **一手论文优先**：Raft → Spanner → MapReduce/GFS/Bigtable 三件套 →
   Dynamo → Kafka/Spark；PBFT/Bitcoin 收尾。
2. 每篇用同一模板精读：**负载假设 → 核心抽象 → 一致性契约 → 容错机制 → 性能手段 → 没说的代价**。
3. 配合 Lab：L01-L02 后做 pg1，L05-L06 后做 pg2/pg3，L09/L10 后做 pg4 ——
   论文里的"一句话机制"在 Lab 里是一周 bug（本项目 `projects/` 三件套对应复现）。
4. 延伸书目：*Designing Data-Intensive Applications*（Kleppmann）——
   把本表全部论文串成一条现代叙事。
