# 第 10 章　运行 ZooKeeper

> 原书第 10 章是「把它跑稳」的章：从单机 `zkServer.sh` 到多机仲裁集群、从 `zoo.cfg` 每一项调参到
> 四字命令监控、从日志与快照运维到配额与 ACL。这是**运维/ SRE** 视角的收口章，也是存量 ZK 集群
> 日常最常用到的内容。2026 年视角下，还要补 3.5+ 的 AdminServer、动态重配置、TLS/SASL 等新能力。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 部署形态 | 单机（开发）/ 集群（2n+1 仲裁）/ 观察者（observer） | 生产必须奇数集群；观察者扩读不削弱写仲裁 |
| zoo.cfg 关键项 | `tickTime / initLimit / syncLimit / dataDir / dataLogDir / clientPort / maxClientCnxns` | 这些参数直接决定心跳、选主、持久化与连接上限 |
| 集群与 myid | `server.N=host:quorumPort:leaderElectionPort` + `myid` 文件 | 每台机器用 `myid` 对应 `server.N` 的 N |
| 观察者（observer） | `peerType=observer` + `server.N=...:observer` | 跨机房只读副本，不参与投票，降低跨机房写延迟影响 |
| 四字命令 | `ruok / stat / srvr / conf / mntr / wchs / envi / cons` 等 | 一线排查与监控的瑞士军刀（默认 2181 的 TCP 文本协议） |
| 监控（mntr） | `mntr` 输出延迟、连接数、znode/watch 数、follower 同步态等指标 | 接入 Prometheus/Grafana 做告警的基础 |
| 日志与快照运维 | `autopurge` 自动清理旧快照/日志；`dataLogDir` 单独盘 | 防磁盘写满、降写延迟的关键 |
| 配额与 ACL | `setquota` 限制子节点数/数据大小；ACL 做节点级授权 | 配额防单业务膨胀，ACL 做授权（非加密） |
| 调优与故障 | 会话超时上下界、fsync 策略、`Leader` 切换演练 | 调优围绕「写延迟」与「故障恢复速度」 |

## 核心精讲

（以下为教学性梳理，配置/命令均**教学示意，不参与构建**。）

### 10.1 最小可跑的 zoo.cfg（集群）

```text
# 教学示意，不参与构建：一个三节点集群的配置骨架
tickTime=2000                # 基本时间单位(ms)：心跳、超时都以此倍数计
initLimit=10                 # follower 初始化同步允许的 tick 数(连不上主的上限)
syncLimit=5                  # follower 与 leader 心跳超时的 tick 数
dataDir=/var/lib/zookeeper   # 快照与内存树持久化目录
dataLogDir=/var/log/zk-txn   # 事务日志单独盘(强烈建议)
clientPort=2181
maxClientCnxns=60            # 单客户端最大连接数，防连接耗尽
server.1=zk1:2888:3888
server.2=zk2:2888:3888
server.3=zk3:2888:3888
# 每台机器在 dataDir 下放 myid 文件，内容分别是 1 / 2 / 3
```

- `2888` 是 quorum 通信口，`3888` 是 leader 选举口；集群里 `N` 要与各机 `myid` 对应；
- `dataLogDir` **单独挂盘**是生产铁律：事务日志是顺序写且对延迟敏感，和快照/其他 IO 混盘会互相拖累。

### 10.2 观察者（observer）：跨机房只读副本

```text
# 教学示意，不参与构建：把一台机器设为 observer
# 在 observer 节点上:
peerType=observer
# 在 zoo.cfg 的 server 列表里:
server.4=zk4:2888:3888:observer
```

- observer **不参与投票**，因此不增加写所需的仲裁规模，但能分担读与 watch 压力；
- 典型用于「跨机房只读副本」：把 observer 放远端，本地读就近、写仍走多数派，避免跨机房拖慢写提交。

### 10.3 四字命令：一线排查

```text
# 教学示意，不参与构建：常用四字命令
echo ruok | nc localhost 2181     # "imok" 表示进程活着（仅存活，不含健康）
echo stat | nc localhost 2181     # 连接数、节点角色、延迟概要
echo srvr | nc localhost 2181     # 类似 stat 但更结构化（单服务端视图）
echo conf | nc localhost 2181     # 当前生效配置
echo mntr | nc localhost 2181     # 监控指标（见 10.4）
echo wchs | nc localhost 2181     # watch 总数与分类
```

- `ruok` 只证明进程在，**不等于服务健康**（leader 选举中也可能回 imok），监控别只靠它；
- 四字命令默认走 2181 的简易文本协议，生产常通过 `4lw.commands.whitelist` 限制可用命令。

### 10.4 mntr：监控指标清单

```text
# 教学示意，不参与构建：mntr 关键指标（节选）
zk_server_state  leader            # 角色：leader / follower / observer
zk_znode_count   12345             # znode 总数（内存树规模）
zk_watch_count   678               # 当前 watch 数
zk_ephemerals_count 12             # 临时节点数（≈在线成员/会话）
zk_avg_latency   0                 # 平均请求延迟(ms)
zk_max_latency   23                # 最大请求延迟(ms)
zk_packets_received 100000         # 累计收包
zk_num_alive_connections 50        # 当前连接数
zk_followers 2                     # (仅 leader) follower 数
zk_synced_followers 2              # (仅 leader) 已同步 follower 数
```

- 把这些指标抓进 **Prometheus/Grafana**，重点盯：延迟突增、`synced_followers` 掉、连接数逼近
  `maxClientCnxns`、磁盘使用率（防快照/日志写满）。

### 10.5 日志与快照的自动清理

```text
# 教学示意，不参与构建：自动清理，避免磁盘被旧快照撑满
autopurge.snapRetainCount=3        # 保留最近 3 份快照及其日志
autopurge.purgeInterval=24         # 每 24 小时清理一次
```

- 不开自动清理，老快照+日志会无限增长；但保留太少又不利于「回滚/审计」，按容量权衡。

## 版本演进

- **本书无第二版**（2013 年口径）；本节写 2013 → 2026 的实际运维演进。
- **ZK 3.5+ 动态重配置（reconfig）**：无需停服改 `zoo.cfg` 重启即可增减成员，运行期更安全；
  对应第 9 章「配置作为特殊事务」的能力落地。
- **AdminServer（默认 8080）**：3.5+ 新增基于 HTTP 的管理/四字命令入口，与老 2181 文本协议并存。
- **TLS / SASL 增强**：3.5+ 对客户端—服务端、服务端—服务端（quorum）通信的加密与认证支持更完整，
  补上「ACL 不含链路安全」的短板（见第 2 章）。
- **审计日志（audit）**：较新版本支持开启审计，记录敏感操作，满足合规。
- **容器节点 / TTL 节点运维**：3.5+ 引入，影响配额与生命周期管理（见第 2 章）。

## 经典论文与原始文献

| 文献 | 出处 | 贡献 |
| --- | --- | --- |
| Hunt et al.《ZooKeeper: Wait-free Coordination for Internet-scale Systems》 | USENIX ATC 2010 | 运维模型（仲裁、日志、快照、会话超时）的原始定义 |
| Junqueira et al.《Zab》 | DSN 2011 | 内部复制与选主，决定集群部署与恢复行为的底层 |
| Apache ZooKeeper 官方文档《Administrator's Guide》《ZooKeeper Internals》 | Apache 文档 | `zoo.cfg` 参数、四字命令、动态重配置、AdminServer 的权威出处（版本较多） |

## 近年研究与工业界开源实践（2015–2026）

- **ZK 自身持续维护**：`apache/zookeeper`（12811★）3.8/3.9 线，含动态重配置、TLS、AdminServer、
  审计等 3.5+ 能力；存量 Hadoop/Spark/HBase/Solr 生态仍依赖它运维。
- **云托管 ZK / 协调即服务**：公有云提供托管 ZK（如阿里云 MSE 注册配置中心含 ZK、AWS 相关托管
  集成），运维边界从「自己管进程」转向「托管实例 + 关注业务使用」，是 2026 年运维形态的变化。
- **etcd 运维对照**：`etcd-io/etcd`（52309★）自带 `/metrics`（Prometheus）端点、defrag、快照压缩，
  监控与运维范式与 ZK 的 `mntr` 异曲同工，但更云原生；Kubernetes 用 etcd 即此形态。
- **ClickHouse Keeper**：`ClickHouse/ClickHouse`（50091★）用 Raft 实现 ZK 协议兼容的协调服务，
  运维侧提供「ZK 替代」选项，对应第 10 章的部署对照。
- **Kafka KRaft**：自 3.3 起去除 ZK 依赖，原依赖 ZK 做元数据/选主的集群改为自管 Raft，减少一套
  需要独立运维的协调系统——这是「要不要继续运维 ZK」的现实考量。

## 常见误区与本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「ruok 返回 imok 就等于服务健康」 | ruok 只证进程存活，选举/脑裂中也可能 imok；健康要看 `mntr`/角色与同步态 |
| 2 | 「偶数台集群更稳」 | 偶数台不增加容错（N=4 仍只容 1），照用 2n+1 |
| 3 | 「事务日志和快照放同一盘无所谓」 | 混盘会互相拖累写延迟与恢复；`dataLogDir` 单独盘是生产铁律 |
| 4 | 「ACL 开了就安全」 | ACL 是节点级授权，不含链路加密；传输安全靠 TLS/SASL（3.5+） |
| 5 | 「不配 autopurge 也无妨」 | 旧快照/日志会无限增长撑满磁盘，必须设 `autopurge` |
| 6 | 🔧 第 10 章未提 3.5+ 动态重配置 | 在线增减成员已成常态，原版「停服改配置」流程需更新 |
| 7 | 🔧 未提 AdminServer / TLS / 审计 | 2013 年后运维能力大幅增强，需补入部署与监控 |
| 8 | 🔧 未提云托管 ZK / 协调即服务 | 2026 年运维边界已变，自建 vs 托管是现实决策 |
| 9 | 🔧 未对比 etcd/Keeper 的运维范式 | 新系统多选 etcd（Prometheus 原生）或 ClickHouse Keeper，对照有助选型 |

## 与其他章 / 其他书的联系

- **本书内**：
  - 第 10 章的 **集群/仲裁/选举** → 第 9 章 Zab 与 quorum 的运维落地；
  - 第 10 章的 **会话超时参数** → 第 2、5 章会话与故障恢复的服务端配置；
  - 第 10 章的 **ACL/配额** → 第 2 章 ACL 概念、第 6 章容量注意；
  - 第 10 章的 **监控指标** → 第 1 章「协调服务可观测性」的生产化。
- [../深入理解分布式共识算法/00-总览与阅读地图.md](../深入理解分布式共识算法/00-总览与阅读地图.md)
  ——leader 选举、quorum 的算法层机制，解释第 10 章部署参数为何如此。
- [../大规模分布式存储系统/00-总览与阅读地图.md](../大规模分布式存储系统/00-总览与阅读地图.md)
  ——分布式系统运维（故障、容错、跨机房）的通用视角，与第 10 章互为参照。
- [../凤凰架构/](../凤凰架构/) ——云原生下「etcd + K8s 健康检查 + Prometheus 监控」的运维范式，
  是本章 ZK 运维的 2026 年对照样本。
