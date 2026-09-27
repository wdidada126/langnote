# 第 3 章　搭建 ZooKeeper 主从运行环境

> 原书第 3 章把单机升级为集群（ensemble）：initLimit/syncLimit、myid、启动各实例、
> 验证主从复制、查看角色、sync 命令。这一章把第 1 章的「角色/Leader/Follower/ZAB」
> 落到了可操作的部署层面，是理解「ZK 怎么做到高可用」的关键。
> 2026 视角要补：**Observer 角色、动态重配置（reconfig）、以及 ZK 集群写瓶颈**。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 3.1 initLimit / syncLimit | 集群同步相关超时 | initLimit=选主/初始化同步上限；syncLimit=心跳失联上限 |
| 3.2 myid 与 cfg | 每个节点的 id 文件 + server.x 列表 | myid 决定该节点是 server.几 |
| 3.3 启动各实例 | 逐台 zkServer.sh start | 多数派起来即可对外服务 |
| 3.4 Leader 写 / Follower 读 | 验证主从数据一致 | 写只走 Leader，读可走 Follower |
| 3.5 获取角色 | stat / status 看 Leader/Follower | 确认选主结果 |
| 3.6 sync 命令 | 强制 Follower 与 Leader 同步 | 解决「读从节点可能读到旧值」的兜底 |

## 核心精讲

（以下为教学性梳理，配置/命令均**教学示意，不参与构建**。） 

### 3.1 initLimit 与 syncLimit（都是 tickTime 的倍数）

```text
# 教学示意，不参与构建：集群 zoo.cfg 关键项
server.1=zk1:2888:3888
server.2=zk2:2888:3888
server.3=zk3:2888:3888
#   格式：server.<myid>=<host>:<peer端口>:<选举端口>
initLimit=10     # 单位=tickTime；Follower 初次连接/同步 Leader 的超时上限
syncLimit=5      # 单位=tickTime；Follower 与 Leader 心跳失联判定上限
```

- **initLimit**：Follower 启动时与 Leader 做**初始数据同步**的最长时间（超时则放弃加入）。
- **syncLimit**：正常运行中，Follower 超过该时长未收到 Leader 心跳 → 判定失联、被剔出。

### 3.2 myid 与 server.x

- 每台机器在 `dataDir/myid` 里写一个数字（1/2/3…），与 `server.x` 的 x 对应；
- 这是 ZK 识别「我是谁、我该连谁」的依据。**myid 写错是集群起不来的头号原因**。

### 3.4 / 3.5 写走 Leader、读走任意

```text
# 教学示意，不参与构建：主从复制语义
client 连到 Follower-A，发起写请求
  -> Follower-A 把写转发给 Leader
  -> Leader 用 ZAB 提议，多数 Follower 确认后提交
  -> 写成功后各节点数据一致
client 连到 Follower-B 读：默认可能读到尚未同步的旧值 -> 用 sync 命令先对齐
```

### 3.6 sync 命令

- `sync /path` 强制当前 Follower 先与 Leader 对齐再返回，是「读从节点前想要强一致」的兜底手段。
- 代价是多了一次同步往返，仅在**读一致性要求高**时按需使用。

## 版本演进

- **本书无第二版**；本节写 2022 年口径 → 2026 年视角的变化。
- **Observer 角色**：本书只讲 Leader/Follower（与第 1 章一致），但生产集群常加
  **Observer**（只提供读、不参与投票）来扩展读吞吐，且不增加选主/写确认的复杂度。
- **动态重配置（reconfig，ZK 3.5+）**：本书用的是「改 zoo.cfg + 重启」的静态配置，
  现代 ZK 支持 `reconfig` 在线增减节点，无需全集群重启。
- **写瓶颈重申**：第 1 章提过，集群再大，**写仍只走单一 Leader**；超大规模注册场景下
  这是 ZK 被 etcd / 应用级服务发现替代的根本原因（见 06/07 补丁）。
- **TLS / 安全**：本书未讲 ZK 集群间与客户端 TLS、SASL 认证，生产必配。

## 经典论文与原始文献

| 文献 | 出处 | 贡献 |
| --- | --- | --- |
| Hunt et al.《ZooKeeper: Wait-free Coordination for Internet-scale Systems》 | USENIX ATC 2010 | 集群角色与主备复制的原始设计 |
| Junqueira, Reed《Zab: High-performance Broadcast for Primary-backup Systems》 | DSN 2011 | ZAB 原子广播（主从同步的协议层） |
| Apache ZooKeeper 官方文档（Cluster 配置 / Dynamic Reconfiguration） | zookeeper.apache.org | initLimit/syncLimit/reconfig 的权威释义（版本较多） |

## 近年研究与工业界开源实践（2015–2026）

- **apache/zookeeper（12811★，2026-09 实测）**：3.5+ 支持动态重配置与 TLS；存量集群庞大。
- **etcd-io/etcd（52310★ 量级）**：Raft、可在线扩缩容、MVCC 快照，云原生集群协调的现代对照。
- **apache/curator（3173★）**：Java 客户端，内含 Leader 选举、分布式锁等集群语义封装。

## 常见误区与本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「集群里每台都能写」 | 写统一走 **Leader**，Follower 只转发写、提供读 |
| 2 | 「加节点就能提升写吞吐」 | 写受单 Leader 限制，加节点只扩展读（Observer） |
| 3 | 「myid 随便写」 | myid 必须与 server.x 对应，写错集群起不来 |
| 4 | 「Follower 读一定最新」 | 默认可能读到旧值，强一致读需先 `sync` |
| 5 | 🔧 未提 Observer 角色 | 生产集群常用 Observer 扩展读，本书只讲 Leader/Follower |
| 6 | 🔧 静态配置需重启 | ZK 3.5+ 支持 `reconfig` 在线变更，本书仍是改文件重启范式 |
| 7 | 🔧 未提集群 TLS/SASL | 生产集群间与客户端必须加密与认证，本书安全维度缺失 |

## 与其他章 / 其他书的联系

- **本书内**：
  - 3.1/3.2 配置 → [01-ZooKeeper核心理论.md](01-ZooKeeper核心理论.md)（角色、选举理论）；
  - 3.4 主从复制 → [08-Dubbo高级技能.md](08-Dubbo高级技能.md)（集群/主备思想的延伸）；
  - 3.6 sync → [04-ZooKeeper常见命令和Curator的使用.md](04-ZooKeeper常见命令和Curator的使用.md)（命令全集）。
- [../深入理解分布式共识算法/00-总览与阅读地图.md](../深入理解分布式共识算法/00-总览与阅读地图.md)
  ——ZAB/选举/容错的算法级补全。
- [../设计数据密集型应用/09-一致性与共识.md](../设计数据密集型应用/09-一致性与共识.md)
  ——主备复制与一致性保证的现代讲法。
