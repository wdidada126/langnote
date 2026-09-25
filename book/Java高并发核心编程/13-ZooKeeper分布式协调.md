# 第 13 章 ZooKeeper 分布式协调（卷1）

> ZAB 协议、角色（Leader/Follower/Observer）、ZNode（持久/临时/顺序）、Watcher、分布式锁、选主、配置中心。本书把「CP 协调服务」引入高并发架构，是分布式必备。

## 一、本章地图

| 主题 | 关键 |
| --- | --- |
| ZAB | 原子广播，类 Paxos |
| ZNode | 持久/临时(会话)/顺序 |
| Watcher | 一次性监听 |
| 实战 | 分布式锁/选主/配置中心 |

## 二、核心精讲

### 2.1 🔧 分布式锁（临时顺序节点）
- 抢锁=建 `/lock/seq-` 临时顺序节点，最小序号者得锁；释放=断开会话删节点；Watcher 监听前驱（🔧 比 Redis 锁更「可靠」（CP、防误删），但吞吐低；高频锁用 Redis/etcd）。

### 2.2 临时节点与会话
- 临时节点随会话消失自动删（🔧 实现「存活探测」；会话超时=客户端心跳超时，不是 TCP 断）。

### 2.3 Curator
- `CuratorFramework` 提供 `InterProcessMutex`（分布式锁）、`LeaderSelector`（选主）（🔧 别手搓，Curator 处理了惊群/连接丢失）。

## 三、版本演进 / 论文 / 前沿

- 论文：Hunt et al.《ZooKeeper》(USENIX ATC'10)；ZAB（Junqueira et al.）；Paxos（Lamport 1998）；Raft（Ongaro 2014，etcd/Consul 用）。
- 工业界：ZooKeeper、etcd（K8s）、Consul、Curator（Netflix）。
- 开源 stars（2026-09）：zookeeper 12k / etcd 48k / consul 30k.

## 四、常见误区 / 本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "手搓 ZK 锁" | 用 Curator InterProcessMutex |
| 2 | "Watcher 永久" | 一次性，需重注册 |
| 3 | "ZK 做高频锁" | 高频用 Redis/etcd |
| 4 | "临时节点随 TCP 断" | 随会话超时删 |
