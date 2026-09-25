# 11 · RAC 与高可用（Clusterware / ASM / Cache Fusion / TAF）

> **本章地图**：**RAC 是什么**（多个实例 + 共享存储 + 一个库）→ **集群软件三层**（OHAS → CRS/GI → CSSD + **Clusterware 的守护进程**）→ **ASM 作为 GI 的组件**→ **Cache Fusion 与 GRD**（为什么 RAC 上"内存是共享的，锁是分布式的"）→ **DLM / DRM**→ **VIP、SCAN、listener 与连接路由**→ **TAF（Transparent Application Failover）与 Service**→ **RAC One Node 与 GI/DG 的关系**→ **常见 RAC 故障与诊断**（OSWbb、TFA、`crsctl`、`oclumon`）→ **RAC 什么时候不该用**。

## 一、核心精讲

> 以下 SQL/DDL 均为**教学示意，不参与构建**，不可也不必在真实实例上执行。

### 1.1 三个容易混的概念

| 概念 | 含义 |
| --- | --- |
| **Oracle Clusterware（CRS / GI）** | 集群管理软件，管理节点成员、心跳、资源（数据库、监听、VIP、ASM）的启停与 failover |
| **Oracle RAC** | 数据库层面的"多实例共享一份数据" |
| **Oracle ASM** | 存储管理，11gR2 起**随 GI 安装**（所以它属于集群软件，不是数据库的一等公民） |

**从 11gR2 起"装 RAC"的真实动作是"装 GI"**：GI 里包含 Clusterware + ASM（+ 可选负载均衡器），然后 Oracle 数据库软件再挂上去。这解释了为什么 12c 教材第 1 章把 **ORAC（Oracle Real Application Cluster）** 与 **OASM/ASM** 并列在"12c 与云计算"的缩写表里——它们本来就是一整套。

### 1.2 集群软件的关键守护进程（以 11gR2 之后的 GI 为基准）

```
  OHAS        （Oracle High Availability Services， Egyptian god 派：操作系统层）
     └─ 管理 has/ohasd，开机自启，拉起 CRS
          └─ CRSD   （Cluster Ready Services）★ 管理资源（数据库、VIP、监听、ASM）
               └─ CSSD （Cluster Synchronization Services）★ 成员心跳与组管理
                    └─ EVMD、GPNPD、MDNSD（11gR2 起）
```

| 进程 | 作用 | 常用命令 |
| --- | --- | --- |
| `ohasd` | OS 层的 HA 守护 | `crsctl check has` |
| `crsd` | 资源生命周期与 failover | `crsctl stat res -t` |
| `cssd` | **节点心跳**、投票（voting disk）与集群成员变更 | `crsctl check css`、`crsctl stat res -t -v` |
| `evmd` | 事件发布 | `ocrconfig`/`ocrcheck` 相关 |
| `gpnpd` | 网格即插即用配置分发 | |
| `mdnsd` | 服务发现（用于 SCAN） | |

**CSSD 是关键单点**：`cssd` 心跳丢失 → **节点驱逐（eviction）**，被驱逐的节点会 **立即重启**（reboot）而不是优雅降级。这解释了 RAC 上一个"看起来很小的"节点问题为什么会造成整个节点不可用。

教学示意，不参与构建：

```bash
# 集群健康巡检（教学示意，不参与构建）
crsctl check cluster -all
crsctl stat res -t
crsctl check css
crsctl stat res ora.asmdba -p                 # 看资源的详细属性（含 ASM 磁盘组）
ocrcheck                                       # 检查 OCR/voting disk 完整性
```

### 1.3 Cache Fusion：RAC 最核心也最反直觉的部分

**反直觉之处**：RAC 上，**数据不是"每个节点各有一份缓存"，而是"整集群共享一个分布式缓存"**，每个实例的 buffer cache 是整体缓存的一个**分区**：

```
   Inst 1 buffer cache   Inst 2 buffer cache   Inst 3 buffer cache
   （部分块）            （部分块）            （部分块）
        └──────────────────┬────────────────────┘
                           ▼
                  GRD（Global Resource Directory，在集群的共享内存中）
                  记录：每个块的"主节点（master）"与当前持有者
```

**一次跨节点读块的流程**：

1. 节点 A 要读块 X，发现本地没有；
2. 查 **GRD** 找到块 X 的 master 节点是哪个实例；
3. 向 master 申请，若 master 的缓存里也没有，master 去磁盘读；
4. master 把块发给 A（可能要先把块从别的实例的缓存里"哄下来"）；
5. 块在 A 的本地缓存里，**同时更新 GRD**，并标记该块在节点间是"一致"的。

**这就是"内存融合（Cache Fusion）"**——**数据不必先落盘就能在节点间传递**。由此产生的等待事件就是 RAC 专属的那一族：

| 等待事件 | 含义 | 常见原因 |
| --- | --- | --- |
| `gc buffer busy acquire` | 等一个块被别的节点释放 | **热点块**跨节点争用 |
| `gc cr multi block request` | 读一致性块请求 | 大量跨节点一致性读 |
| `gc current block 2-way / 3-way` | 当前块在多节点间传递 | 同一行被多节点并发改写 |
| `gc cr block busy` | 一致性读时发现块正在被改 | 长事务 |
| `gc remaster` | **DRM（动态重映射）** 期间 | 节点增减、资源重分配 |

### 1.4 DLM 与 DRM

- **DLM（Distributed Lock Manager）**：RAC 的全局锁管理，本质上是一个**分布式的多粒度锁管理器**，管理 buffer cache 里的块级锁与 GC 相关的资源（对应 [`数据库系统概念6/15-并发控制.md`](../数据库系统概念6/15-并发控制.md) 里讲的"锁管理器"，但这里是跨实例的）；
- **GRD（Global Resource Directory）**：DLM 的目录，记录每个资源（块）的 master 节点；
- **DRM（Dynamic Remastering）**：**资源 master 可以在运行时迁移**——当某些块被某些节点频繁访问时，Oracle 动态把这些块的 master 迁到"访问最频繁"的节点，减少跨节点通信；
- 🔧 **DRM 相关故障**：11g 上 DRM 有时会在**高压/节点频繁重启**时造成实例 hang（`row cache lock` 与 "DRM" 相关的等待），所以 DBA 攻坚指南里提到"**在 Oracle 11g 中禁用 DRM**"这类操作；12c 起 DRM 更稳定，但**节点频繁加入/退出仍会触发 remaster 风暴**。

### 1.5 VIP、SCAN 与连接路由

```
客户端
  │
  ├─（旧方式）TNS 里写多个节点的 VIP，靠 failove_r 客户端做 TAF
  │
  └─（现代方式）SCAN（Single Client Access Name）
       ├─ SCAN IP（1~3 个，集群级虚拟 IP）
       ├─ SCAN listener 在三个节点上各跑一个，通过 clusterware 通告服务状态
       └─ 负载平衡（按节点负载）把连接分到各节点的 listener
            └─ 每个节点上跑一个 listener，监听VIP 与实例名
```

- **VIP 的作用**：节点故障时，VIP 会被 Clusterware **立即飘到健康节点**上。所以客户端连 VIP 时，故障节点上的连接会**立刻失败**（而不是等 TCP 超时），从而触发快速 failover；
- **客户端 TAF（`FAILOVER=ON`, `TYPE=SELECT`/`SESSION`, `METHOD=BASIC`）**：连接失败后自动重连并重放；`TYPE=SELECT` 可对正在执行的语句做透明切换；
- **Service（服务）**：11g 起推荐的"连接入口抽象"——把"业务名（如 `crm_pdb`）"与"实例集合"解耦，通过服务的 `instance` 属性控制"服务跑在几个节点上"（甚至可以在 RAC One Node 上跑单节点）；
- **`DBMS_SERVICE`** 可在数据库侧动态启停服务（如把某服务只放在一个节点）。

教学示意，不参与构建：

```
# tnsnames.ora 的服务式写法（教学示意，不参与构建）
CRM_PDB =
  (DESCRIPTION =
    (ADDRESS = (PROTOCOL = TCP)(HOST = scan-cluster.example.com)(PORT = 1521))
    (CONNECT_DATA =
      (SERVER = DEDICATED)
      (SERVICE_NAME = crm_pdb)
      (FAILOVER_MODE = (TYPE = SELECT)(METHOD = BASIC)(RETRIES = 180)(DELAY = 5))))
  )
```

### 1.6 RAC One Node 与 GI / DG 的关系

- **RAC One Node**：把 RAC 的"集群感知"用于**单实例**——数据库跑在一个节点上，但**注册为集群资源**，节点故障时可**在另一个节点上重新上线**（不需要 DG）。适用于"要高可用但不需要 RAC 性能"的场景；
- **GI 与 DG 不是替代关系**：
  - **GI/Clusterware** 管**节点与实例**的存活（instance-level HA）；
  - **Data Guard** 管**数据**的副本与切换（database-level HA/DR）；
  - 生产常见组合是 **RAC（本地三节点）+ Data Guard（异地备库）**：RAC 顶住本地故障，DG 顶住机房/地域故障（见 [`12`](12-备份恢复容灾与DataGuard.md)）。

## 二、版本演进

| 版本 | RAC / 集群相关变化 |
| --- | --- |
| 10g | CRS 独立安装（`CRS` 与 database 分开），ASM 独立 |
| 11gR1 | 引入 **OHAS**、`gpnpd`/`mdnsd`；GI 概念雏形 |
| **11gR2** | **GI 正式成型，ASM 并入 GI**；**SCAN** 引入；Clusterware 守护进程体系定型 |
| 12.1 | RAC One Node GA；`PDB` 与 RAC 结合；集群资源模型更统一 |
| 12.2 | Hydride Cluster / Flex Cluster（**管理员节点（Hub）/ 只读子节点（Leaf）**）引入，节点可以"不等份" |
| 19c | LTS；持续可用（Always On）能力增强；集群与云基础设施整合更紧 |
| 23c | 与云/自治深度融合；多租户与集群继续强化 |

🔧 **2026 年必须补的三条**：
1. **Flex Cluster（12.2 起）** 改变了"集群必须是同构机器"的假设（Hub 节点 + Leaf 节点），本书（成书 2015）完全没有；
2. **RAC 在国产化/-cloud 场景的退化形态**：很多"去 RAC"项目把 RAC 换成 **OceanBase/PolarDB/TiDB/GaussDB**，它们的"多副本 + Paxos/Raft"在架构上更接近"分布式一致性"而非 RAC 的"共享存储内存融合"——迁移时最难的正是"RAC 上的应用要改什么连接语义"（TAF、服务、实例亲和性）；
3. **RAC 的适用场景被重新审视**：RAC 解决的是"实例可用性 + 写扩展的读多写少"，**不解决写扩展**；2026 年大量系统将"热点写"交给分库分表或分布式数据库，RAC 退守到"读多写少的 OLTP + 高可用底座"。

## 三、经典论文与原始文献

| 文献 | 出处 | 与本主题的关系 |
| --- | --- | --- |
| Stonebraker《The Case for Shared-Nothing》/《Shared-Nothing Architecture》相关论述 | 1980s 技术文献 | **通用理论，非 Oracle 专属**：share-nothing / share-everything / share-original 的分类，正是 RAC 书第 1 章的骨架 |
| Bernstein, Hadzilacos & Goodman《Concurrency Control and Recovery in Database Systems》 | Addison-Wesley, 1987（书） | **通用理论，非 Oracle 专属**：多处理器/分布式环境下的锁管理与恢复，DLM 的学术基础 |
| Agrawal 等《Cache Fusion 的先驱：Delta Ripple Join / 或直接引 Oracle 的 *Oracle RAC 白皮书*》 | Oracle 官方材料 | **通用理论，非 Oracle 专属**：Cache Fusion 的产品化描述 |
| Oracle《Oracle Grid Infrastructure Administrator's Guide》 | Oracle 官方文档（非论文） | GI/Clusterware/ASM/SCAN/服务的权威描述 |
| Oracle《Oracle Real Application Clusters Administration and Deployment Guide》 | Oracle 官方文档（非论文） | RAC 架构、Cache Fusion、TAF、Service 的权威描述 |

> 说明：**RAC 是产品实现**，其学术底座是"分布式锁管理与多处理器数据库"的通用研究（明确**不是 Oracle 专属论文**）。集群软件行为以 Oracle 官方文档为准。

## 四、近年研究与工业界开源实践（2015–2026）

- **近年研究**：**分布式数据库的"无主/多主"与共识**（Paxos/Raft + 多副本强一致，如 Google Spanner 的 TrueTime、TiDB 的 Raft、CockroachDB 的 HLC），与 RAC 的"共享存储 + 分布式缓存"是**截然不同的路线**；Paper 层面的对照见 [`数据库系统概念6/26-高级事务处理.md`](../数据库系统概念6/26-高级事务处理.md)（确定性事务、存算分离）。
- **工业界**：
  - **`crsctl` / `oclumon` / OSWbb / TFA** 仍是诊断 RAC 的主力工具（RAC 书 Cover 了 OSWbb 与 TFA）；
  - 🔧 **容器内跑 RAC** 是 2020 年代的一个活跃方向（多副本 + 分布式存储），但复杂度高，生产少见；
  - 🔧 **国产替代里的"RAC 平替"**：
    - `oceanbase/oceanbase`（star 实测 ≈10291）：**MySQL 兼容为主，Oracle 兼容模式（租户级）可跑 PL/SQL**，其"三副本 Paxos + 无共享"提供的可用性接近 RAC 但不共享存储；
    - `polardb/PolarDB-for-PostgreSQL`（star 实测 ≈3205）：**存算分离 + 共享存储的多节点架构（PolarDB 的 Read-Only Node 共享底层存储，思路与 RAC 最接近）；
    - `pingcap/tidb`（≈40586★）：分布式分片，写可扩；与 RAC 定位差别最大。
  - 🔧 **监控**：国产化替代项目中，`apache/shardingsphere`（≈20804★）常作为"分库分表 + 读写分离"的中间件层，替代 RAC 的"横向扩展"职能。

## 五、常见误区与本书需修正之处

| # | 误区 | 修正 | 书目 |
| --- | --- | --- | --- |
| 1 | "RAC 能把写入也横向扩展" | RAC 共享同一份数据、**同一个 redo**；写操作仍是单份。RAC 提升的是**可用性 + 读扩展** | OracleRAC核心技术详解（第 10–13 章）讲得准；12c 教材第 1 章容易让人误解 |
| 2 | "RAC 上内存是每实例独立的一份" | **整集群共享一个分布式缓存**，靠 GRD 记录块的位置；这是 Cache Fusion 的前提 | OracleRAC核心技术详解（Cache Fusion 章） |
| 3 | "节点心跳丢了会优雅降级" | **CSSD 心跳丢失 → 立即驱逐（重启节点）**，不是降级 | OracleRAC核心技术详解（CSS/CRS 章） |
| 4 | "VIP 飘走后客户端会等一会儿才失败" | VIP 由 Clusterware **立即**飘到健康节点，客户端会**快速**失败（这正是 VIP 的价值） | OracleRAC核心技术详解（集群管理软件部分） |
| 5 | "GI 和 Data Guard 二选一" | 二者管的是**不同层**（实例存活 vs 数据副本），通常一起用 | 12c 教材第 15–16 章只讲 RMAN/闪回，未把 GI/DG 的关系讲清 |
| 6 | "RAC 越节点越多越快" | 节点越多，跨节点通信与 remaster 越频繁；2–4 节点是常见甜点区 | OracleRAC核心技术详解有 RAC 调优章，但未强调"别过度扩容" |
| 7 | 🔧 "RAC 是 2026 年高可用最优解" | 定位已被重新审视：**RAC 退守"读多写少 + 本地高可用"**，写扩展交给分布式数据库；国产替代（OB/PolarDB/TiDB/GaussDB）用"多副本共识"路线替代 RAC | 🔧 全部 9 本（成书 2009–2021） |
| 8 | 🔧 "从 RAC 迁到国产库不用改应用" | 需要重建的是**连接语义**（TAF/Service/实例亲和）、**PL/SQL 资产**、以及**序列自增与分片键设计**——这才是迁移的真实成本 | 🔧 全部 9 本未涉及迁移 |
| 9 | 🔧 "RAC 只在 11g/12c 时代才有价值" | 12.2 的 **Flex Cluster（Hub/Leaf）**、19c 的持续可用让它在云化/异构节点场景仍有生命力 | 🔧 OracleRAC核心技术详解（2015）只覆盖到 12c 早期 |

## 六、与其他章 / 其他书的联系

- **上一章**：[`10-PLSQL高级与工程化.md`](10-PLSQL高级与工程化.md)（RAC 上**每个实例各自一份 PL/SQL 包状态**；节点间不共享）
- **下一章**：[`12-备份恢复容灾与DataGuard.md`](12-备份恢复容灾与DataGuard.md)（GI 与 DG 的分工；RAC 上的备份恢复要点）
- **强相关**：[`07-SQL性能诊断与调优实践.md`](07-SQL性能诊断与调优实践.md)（Cluster 类等待事件 `gc %` 的诊断方法在这里，其他等待事件在那里）
- **强相关**：[`03-存储结构-表空间与段区块.md`](03-存储结构-表空间与段区块.md)（ASM 是 RAC 的存储底座；热点块问题在 RAC 上表现为 `gc buffer busy acquire`）
- **强相关**：[`13-高并发系统的架构与设计.md`](13-高并发系统的架构与设计.md)（RAC 与读写分离、连接池、分库分表的关系）
- **理论对照**：[`数据库系统概念6/19-分布式数据库.md`](../数据库系统概念6/19-分布式数据库.md)（分布式事务、副本一致性、与 RAC "共享一切"路线的对照）；[`数据库系统概念6/15-并发控制.md`](../数据库系统概念6/15-并发控制.md)（DLM 是跨实例的锁管理器）
- **其他书**：《Oracle RAC核心技术详解》是本章唯一的主支撑（13 章，第一部分集群软件 + 第二部分的 GRD/DLM/DRM/调优/连接管理）；《DBA攻坚指南》讲"11g 中禁用 DRM"与"row cache lock 诊断"，是本章 1.4 的运维化补充。
