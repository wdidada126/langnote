# 07 集群架构与 Gossip：环、副本与流（原书第 6 章"架构·网络层"+分布式运营域 ⚠️ 推定）

> 精读重构。本章讲"节点们如何组成一个没有领导的集群"：gossip、snitch、token 环、副本
> 放置、vnode、流式搬迁与修复。基线 2.x，全部 ⚠️ 未实测。

## 7.1 题纲

1. 对等拓扑：协调节点（coordinator）的角色——任何节点都能协调任何请求
2. Gossip：心跳携带什么（generation/hash、application state、heartbeat 版本号 ⚠️）
3. 故障探测：failure detector 的 φ  accrual 式直觉与"宁可误判也不停写"的取向
4. Snitch 家族：Simple/PropertyFile/GossipingPropertyFile/Ec2…——"距离"的定义权
5. 副本放置策略：SimpleStrategy vs NetworkTopologyStrategy 的环上摆法
6. vnode（1.2 实验→2.x 默认 256 token）：均衡、修复粒度、升级路径的三收益
7. 成员变更：加节点（token 重排→streaming）、换死节点（replace）、减节点（decommission/move）
8. 流式传输与修复：bootstrap streams、`nodetool repair` 的 merkle 对账、slf4j 时代的进度观 ⚠️

## 7.2 Coordinator 与请求的旅程

CQL 写请求打到任意节点后（书内标准叙事 ⚠️）：

```
Coordinator:
  1) TokenMap 计算该分区键的副本集合（ring 快照本地维护，gossip 同步版本）
  2) 选一个"副本"做本分区的提示存储（hint 的责任人）
  3) 并发 fan-out 到所有应达副本，按 CL 计数应答
  4) 未达副本 → 记 hint（hints_directory），留给对方复活后投递
```

"协调节点不是数据所有者"这层分离带来两个书内警句：**跨 DC 部署时把 CQL 入口放在离
写入 DC 近的一侧**；以及"客户端连接池要轮询全环，别只连两个 seed"（09 章驱动侧回环）。

## 7.3 Gossip 细节地图（2.x 口径 ⚠️）

- 周期：`SEED_GOSSIP_INTERVAL`/随机散布（书内 100ms/1s 级参数名 ⚠️ 转述）。
- 载荷：每节点每 state 的 (value, generation)——**generation 变大才覆盖**，形成
  "版本化的集群视图"；application state 分 heartbeat（易失）与 normal（持久）。
- 收敛叙事：新节点靠 seeds 起步→全量交换→环更新广播全环，秒级；分区愈合后视图收敛
  同样靠 generation 追赶。
- 与中心协调方案（ES 的 zen discovery/master election）的对照在
  [../Elasticsearch_The_Definitive_Guide/00-总览与阅读地图.md](../Elasticsearch_The_Definitive_Guide/00-总览与阅读地图.md)
  体系（其 15 章/对应 #89 册 03 章的"zen vs gossip"辨析段）；理论通论端在
  [../设计数据密集型应用/08-分布式系统的麻烦.md](../设计数据密集型应用/08-分布式系统的麻烦.md)（✅ 盘上存在）。

## 7.4 Snitch 与放置：距离即策略

`NetworkTopologyStrategy` 在环上摆副本的规则（书内算法转述 ⚠️）：从目标 token 位置出发
沿环走，**优先凑齐同 rack 之外的本机架副本**，跨机架→跨 DC 按配置计数。前置条件是
snitch 正确报告 rack/DC——`DynamicSnitch` 再加一层"按测得的延迟重排读取偏好" ⚠️。

常见拓扑错误（书中案例化重构 ⚠️）：

1. 默认 `SimpleSnitch` 上生产：所有节点"同距"，跨 AZ 流量失控；
2. EC2 snitch 与自建混合时 `endpoint_snitch` 未滚动迁移（02 章坑的回声）；
3. 把 `dc`/`rack` 写进 properties 但 cassandra-rackdc 与云标签漂移。

## 7.5 vnode：2.x 最重要的运维进化

单 token 时代：节点=环上一把锁，加/减节点搬运"半环对半环"的粗粒度数据。
vnode（256 虚拟 token，1.2 实验、**2.x 默认** ⚠️）：

- 新节点从**所有**老节点各割小片→bootstrap 流式均衡并行；
- 死节点 replace 时数据同样从多源汇聚，瓶颈分散；
- 修复与压实压力均匀化（热点 token 不再钉死单节点）。

代价：环元数据变厚（gossip 载荷、诊断复杂度）；`num_tokens` 上线后不可改（2.x 口径 ⚠️）。
概念对照：分区再均衡通论在 [../设计数据密集型应用/06-分区.md](../设计数据密集型应用/06-分区.md)
的"请求路由/再均衡"节。

## 7.6 流式与修复：数据在环上流动

- **Bootstrap/streaming**：新节点申请所属虚拟区间→老节点按文件流式（`streams` 并发默认
  很小 ⚠️，书内"调大 streams 提速"的时代建议后来被证明易打爆 GC/带宽，现代默认转保守）。
- **Repair（反熵）**：`nodetool repair -full/-pr` 对 token 区间建 merkle 树比对，只传分歧；
  `-pr`（primary range）策略与"60 天 gc_grace 内全量修一遍"的运维节律 ⚠️ 转述——
  这条节律后来成为 #89 册 09 章"repair 日程"专题的主题。
- **拓扑变更的安全带**：decommission 先流走数据再退环；`remove` 用于永久死节点；
  replace 保 IP/token。书内全部流程在 3.x/4.x 大体同构 ⚠️（细节差异见 #89 册 03 章）。
- **观测面**：`nodetool statusgossip`/`failures`/`viewpaxos`（后两个按版 ⚠️）+
  `system.local/system.peers` 虚表是本章所有概念的"可看证据"；书中时代的命令行输出
  样例与今天字段名有漂移，诊断语义不变 ⚠️。

## 7.7 本章在全目录中的挂点

- 读写时的副本互动 → [08-一致性与读写路径](08-一致性与读写路径.md)
- 文件级搬运工（sstableloader/快照）→ #89 册 [08-备份恢复与数据迁移](../Expert_Apache_Cassandra_Administration/08-备份恢复与数据迁移.md)
- 环的内存端（分区→节点映射的来源）→ [06-存储引擎与SSTable](06-存储引擎与SSTable.md)
- 理论端（无领袖复制谱）→ [../设计数据密集型应用/05-复制.md](../设计数据密集型应用/05-复制.md)

## 核心概念速览（中英对照）

- **Coordinator** — Coordinator node：接收并扇出请求的对等节点，不承担所有权。
- **Gossip** — Gossip：周期两两交换的版本化集群视图传播协议。
- **Generation** — Generation number：gossip 状态的单调版本，冲突以新覆盖旧。
- **Failure detector** — Failure detector：φ-accrual 式怀疑器，怀疑≠踢出环。
- **Snitch** — Snitch：把传输地址翻译成 DC/rack/延迟偏好的拓扑插件。
- **NetworkTopologyStrategy** — NTS：跨机架优先、按 DC 计数摆副本的策略。
- **Token ring** — Ring：Murmur3 哈希值围成的责任环，vnode 使其多段化。
- **vnode** — Virtual node：每物理节点 256（默认 ⚠️）虚拟 token 的均衡机制。
- **Bootstrap** — Bootstrap：新节点加入并从环上既有节点流入所属数据。
- **Streaming** — Streaming：节点间 SSTable 级数据搬运，并发度可调。
- **Repair** — Repair：merkle 树对账反熵，`-pr`/`-full` 的强度选择。
- **Decommission/Replace/Remove** — 拓扑三操作：体面退环/原地换机/强删死节点。
- **Hints directory** — Hints dir：暂存"本该给缺席副本"的写的磁盘信箱。
- **SLF4J/进度观测** — 书内时代的 repair/stream 日志查看法，后被虚表替代 ⚠️。

## 最新演进与工业实践

（除注明外均本会话 ✅；集群行为 ⚠️ 纪律）

- **Gossip 的继任者**：6.0 官方特性 **TCM（Transactional Cluster Metadata）**——拓扑/状态变更
  改为事务化复制元数据，gossip 的重活被结构性接管（预发布 ⚠️）。源：
  https://cassandra.apache.org/doc/6.0/cassandra/new/index.html 。
- **修复自动化**：6.0 文档新增 **Auto Repair** 管理章（6.0 侧栏 ✅ 实抓于
  https://cassandra.apache.org/doc/6.0/cassandra/new/index.html 的导航）——"60 天人工节律"
  的历史包袱开始卸下；5.0 已有相关虚表/指标支撑 ⚠️。
- **Transient replication**：4.0 起为"cheap 第三副本"引入 `NetworkTopologyStrategy` 扩展参数
  （`DC:transient_replication_factor` ⚠️），修复制式改变（源：4.0 new 页 ✅ 列出 Transient replication）。
- **拓扑变更现代化**：3.x 的 `removenode`/`replace` 工法延续；K8s/operator 场景下
  换机=声明式动作（对照 #89 册 07 章与 00 生态行 ✅ 基线）。
- **工业实践**：环诊断的标准动作已是"查虚表+metrics"（system.local/system.peers_v2 的
  `peers_v2` 修正了跨 NAT 端口记录 ⚠️ 版本点）；书中"翻 gossip 日志"的技艺退役。
