# L03 GFS：可扩展的分布式文件系统

> 阅读：Ghemawat et al., *The Google File System*, ACM SOSP 2003 / TOCS 2004
> 承 L02：MapReduce 的输入输出都住在 GFS 上；两者互为动机。

## 1. 核心问题

- 目标负载：数百台廉价商用机（每天坏机是常态）、单文件动辄 GB/TB 级、
  一次写入多次读取（write-once, append-heavy）、大文件顺序扫为主、随机小读为辅。
- 传统 POSIX + 单机文件系统假设"磁盘很快坏不了、追求低延迟"，与云场景全反。
  GFS 的哲学：**为规模与容错优化，为吞吐而非延迟设计**。
- 关键设计前提：组件数量巨大（单集群上千台），故障是"预期内"而非"例外"。

## 2. 设计与取舍

### 2.1 角色
- **单 Master**：管理命名空间（全内存）+ chunk（64MB）到 chunkserver 的映射，
  是全局协调者，也是全系统最大的"单点焦虑"来源（→ 靠复制 + 快速重启而非分布式化解决）。
- **Chunkserver**：把 chunk 存成本地 Linux 文件，追加写落到本地日志；
  每 chunk 默认 3 副本。
- **Client**：无缓存的元数据访问——先从 Master 拿 chunk 位置，再直连 chunkserver 读写。

### 2.2 追加（append）的独创设计
GFS 不假设原子写偏移，而是 **at-least-once append**：客户端说"往这个 chunk 追加这些字节"，
master 选一个副本组，主副本决定偏移并广播；若发生并发，返回 padding + 偏移，
记录可能"部分重复"。**把去重责任上推给应用层**（记录带自描述长度/校验）。
这是"分布式无法便宜地做 exactly-once，就退到 at-least-once 让上层收拾"的经典案例
（对照 L02 MapReduce 幂等、L05 Raft 去重）。

### 2.3 一致性模型（宽松！）
按 chunk 区间的每个 replica 可能处于 7 种状态之一；GFS 只承诺"全局串行一致的
写入顺序"，不承诺各副本某区间一致。**只有 append 与 close 是原子的**。
这种"最终一致 + 应用层去重"的取舍，让系统能在部分故障下继续高可用。

### 2.4 Master 的容错与瓶颈
- Master 把操作日志（operation log）+ 快照复制到备用存储，重启靠重放恢复。
- 心跳 + lease 机制：chunk 版本化，用 replica lease 让主副本裁决写顺序，
  避免"分裂的 chunkserver 复活后污染数据"（fencing 思想，Raft 里变成 term/epoch）。
- 瓶颈缓解：client 可缓存 chunk 位置（但会过时）；预取 + chunk 租约批量授予。

## 3. 论文间脉络

- 与 L02：GFS 提供大文件 + 高吞吐追加，MapReduce 提供在其上的并行计算；
  locality 调度靠的就是 master 知道 chunk 在哪些机器。
- 启 L13：Unrolling S3 讲"对象存储如何把 GFS/HDFS 这类设计工程化到极致"。
- 与 L12 ZooKeeper / L05 Raft：GFS 用"单 master + 复制日志"，
  本质是"用可靠单机抽象回避通用共识"——这正是 Raft/ZooKeeper 要解决的更一般问题。

## 4. 跨课程联系

- **6.S081/CSAPP**：GFS 的 chunkserver ≈ 一个极简日志结构文件系统；
  master 元数据全内存对应 CSAPP 的"用内存换性能"与 mmap 思路。
- **CS149**：顺序扫大文件 = 为带宽而非延迟优化的存储侧对应物。
- **15-445**：GFS 的"写主副本、异步分发、副本 lease"是数据库主从复制的存储版；
  WAL 与 master 操作日志同宗。
- **自顶向下网络**：大文件分块并行拉取，是应用层"并行下载/分片"的鼻祖。

## 5. 开源项目中的应用

- **HDFS**：直接对标 GFS 的开源实现（NameNode/DataNode/block），
  早期几乎逐条复刻，后引入 JournalNode + QJM 用类 Paxos 做 NameNode 高可用。
- **Ceph（RADOS）**：走"去中心元数据（CRUSH 算法）"路线，是对 GFS 单 master 瓶颈的反命题。
- **etcd/TiKV 的存储层、Kafka 日志**：分块 + 副本 + 追加日志的设计母题来自 GFS。
- **Google Colossus**：GFS 后继，去掉单 master 用元数据服务器集群（见 L13）。

## 6. 延伸阅读

- HDFS 设计文档与 *The Hadoop Distributed File System* (MSST 2010)。
- Colossus 相关 talks（Frank Dikeman 的 "Colossus under the Hood"）。
- 6.033/GFS 课内讨论题："GFS append 的一致性给应用带来什么负担？"
