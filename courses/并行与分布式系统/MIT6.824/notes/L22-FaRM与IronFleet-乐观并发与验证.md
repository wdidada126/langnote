# L22 FaRM 与 IronFleet：乐观并发、新硬件与形式化验证

> 阅读：Kalia et al., *FaRM: Fast Remote Memory*, NSDI 2014；
> Hawblitzel et al., *IronFleet: Proving Practical Distributed Systems Correct*, SOSP 2015
> 主线：性能极限（RDMA + OCC）与正确性极限（机器验证）——分布式系统的两极加压测试。

## 1. FaRM：把事务压进 1 RTT

### 1.1 核心问题
- Spanner 类系统：一次跨分片事务 = 2PC + 共识 + 等待，毫秒~秒级。
  FaRM 问：**若网络是 RDMA（10μs 级）且可崩溃恢复（持久内存/NVM），
  分布式事务的下限在哪？**

### 1.2 设计
- **全内存 + 单地址空间**：每台机器的内存经 RDMA 对全体可见，
  对象用 128 位 ID（节点号+偏移）寻址 → **客户端直接 READ 远端数据，绕过服务端 CPU**
  （对比 L13 的硬件解耦：数据路径上"去 CPU 化"）。
- **乐观并发控制（OCC）**：读不加锁；提交时**验证（validation）无冲突**再提交——
  把 2PL 的"读也付锁费"换成"提交期一次性检查"。低冲突负载吞吐极高；
  高冲突 → 大量重试（对照 15-445 的 2PL vs OCC 权衡，网络 RTT 把代价放大）。
- **验证协议**：事务的读集/写集发给各"锁分区"的权威节点（锁哈希到固定节点）
  → 两阶段式提交/中止广播。
- **崩溃一致性**：事务日志（write-behind + 分布式 log）+
  **crash consistency：RDMA 单边写无内核参与，崩溃时可能"半写"→
  用 checksum/epoch 验证每条事务日志**（硬件快 ≠ 语义简单，L09 的"假设一切会坏"）。
- 结果：TPC-C 级负载 100 万+ 事务/秒（2014 年），比 Spanner 快 2–3 个数量级——
  **强假设（同数据中心、全内存、低冲突、私有硬件）换来的强性能**。

## 2. IronFleet：把"应该对"变成"证明对"

### 2.1 核心问题
- 分布式 bug 的噩梦：**并发 × 部分故障 × 时序**——测试（哪怕 jepsen 式混沌）
  只能证伪不能证明。Raft 论文靠纸面证明，但实现（如早期 etcd 的 bug）仍会错。
- IronFleet 主张：**分层细化证明**——
  算法层（原子步骤模型）→ 实现层（异步消息、并发 RPC）→ 代码（F*/Dafny 写）
  逐层证明精化关系；**证明"协议实现 ⟹ 线性一致/共识安全"**（L10 的定义成为定理目标）。

### 2.2 方法与代价
- 证明两段式：**安全性（safety）用不变量 + 细化；活性（liveness）靠部分同步假设**。
- **验证即测试（practical bug-finding）**：把规范（TLA+ 式）拿去跑
  随机交错执行（Ivy 风格）→ 先抓协议设计 bug，再上机器验证实现。
- 案例：IronFleet 验证了类视图戳（viewstamped）复制与多 Paxos 实现，
  过程中在真实代码里抓出数个 bug。
- 代价：万行级证明脚本/千行代码；工程师需形式化方法训练 →
  现状：**证明下沉到"验证核心库/规范"，应用层靠模型检查**
  （AWS **Eagle**（ATC 2021，用 IR 模型检查 EC2/S3 一致性）与
  **Foundry** 是工业化折中，课表常选 Eagle 做延伸阅读）。

## 3. 论文间脉络

- FaRM = L14（事务）+ L13（硬件）+ L19/L05（复制共识）的"性能榨汁机"；
  其 OCC 与 L12 ZooKeeper 的 CAS、L04 LSM 的写放大优化同属"乐观 + 检测冲突"家族。
- IronFleet = L05/L06 安全性证明与 L09 混沌测试之间的第三条路；
  与 Raft（人为证明）、Jepsen（经验测试）构成"正确性三支柱"。

## 4. 跨课程联系

- **15-445/15-721**：2PL/OCC 教科书权衡在 RDMA 下重估（验证阶段本地化、锁分区
  = 把锁表分片）；FaRM 的 crash consistency ↔ 数据库 WAL 校验（15-445 Project 4 同款问题）。
- **体系结构/DDCA**：RDMA 的"旁路内核 + 单边语义"、NVM 的乱序持久化
  （pmem fence）——硬件内存模型知识直接成为系统正确性前提。
- **CS242/PL**：Hoare 逻辑、精化、TLA+/Ivy/Dafny——程序验证课程的最佳下游应用。
- **6.S081**：RCU/seqlock 的"乐观读 + 重试"是单机版 OCC（FaRM 把重试搬到网络上）。

## 5. 开源项目中的应用

- **FaRM 系**：Teleport (ATC'14)、C5 (OSDI'14)、FaS'T (ATC'16)；
  工业回响：**Aqua（ATC'19，Azure Storage 的 RDMA 化）**、VMem、
  Redis/KeyDB 的 active-active CRDT 走另一条乐观路线。
- **OCC on 网络**：TiDB 乐观事务模式、CockroachDB 的"不显式验证但靠 Raft + HLC"、
  FoundationDB 的"提交时定序 + 冲突重试"（最接近 FaRM 精神的可下载实现）。
- **验证生态**：AWS Eagle/Foundry、Iris/VeriFast 学术线、
  Rust 侧用类型系统 + Verus 验证 Raft（Verus、jydowns 的 raft 形式化）、Coq 验证 Raft。
- **模型检查实操入口**：TLA+ 社区（tlaplus.io）跑一遍 Raft 规范，
  用 TLC 找出课表提到的 bug。

## 6. 延伸阅读

- Kalia et al., *FaRM: A Fast Distributed Transaction System for Non-Volatile Memory*（扩展版，含 NVM 崩溃一致性处理）。
- Hawblitzel et al., *IronFleet* 姊妹篇：*Safe Systems Code*（Ivy 工具）；
  以及 Jepsen 作者的一致性验证器 **Elle**——当今最可上手的"验证工程"入口。
- AWS Eagle（ATC 2021）：*Automated Reasoning Meets Real Systems*；同届 Foundry（构建时验证 AWS 服务）。
- 15-445/15-721 的 OCC/MVCC 讲义与 CMU 15-721 的 FaRM case study 幻灯片（互补技术细节）。
