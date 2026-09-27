# 第 4 章　ZooKeeper 常见命令和 Curator 的使用

> 原书第 4 章是全书篇幅最大的一章（24 个小节），作者自述「命令覆盖率达 90%」，并强调
> Command 是 ZK 核心技术。内容覆盖 create/get 全参数、deleteall、ACL、配额、watch 全系、
> 以及「自实现递归 watch」。这章是 ZK 客户端的实战字典。2026 视角要补：**直接用 Curator 的
> Cache 体系替代手写递归 watch、以及 ACL 的 SASL/Digest 安全实践**。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 4.1 create/get 全参数 | create [-s][-e][-c][-t ttl]、get [-s][-w] | 顺序/临时/TTL/容器节点、stat 与 watch 参数 |
| 4.2 deleteall | 递归删除 | 替代 2.13 不能删含子节点的限制 |
| 4.3 close / 4.4 connect | 断开/重连 | 客户端会话管理 |
| 4.5 getAcl / 4.6 认证授权 | ACL scheme:id:perm | ZK 的权限模型（world/auth/digest/ip） |
| 4.7 quit | 退出客户端 | — |
| 4.8 配额 | setquota/listquota/delquota | 限制子节点数/数据大小（软限制+告警） |
| 4.9 history / 4.10 redo | 历史与重放 | 命令历史回放 |
| 4.11 set -v / 4.12 delete -v | 乐观锁（版本号） | 用 dataVersion 实现 CAS，避免覆盖 |
| 4.13 get -w / 4.14 printwatches | 数据 watch 与开关 | watch 的一次性与打印控制 |
| 4.15 ls -w / 4.16 ls -R / 4.17 ls -s | 子节点 watch / 递归 / 状态 | ls 的三个变体 |
| 4.18 stat / 4.19 removewatches | 状态查看 / 移除 watch | watch 的清理 |
| 4.20 自实现递归 watch | 手写监听整棵子树 | 痛点解法，但 2026 应换 Curator |
| 4.21 whoami / 4.22 version | 当前认证身份 / 版本 | 调试用 |
| 4.23 getAllChildrenNumber / 4.24 getEphemerals | 子树节点计数 / 列出临时节点 | 运维诊断 |

## 核心精讲

（以下为教学性梳理，命令/Java 均**教学示意，不参与构建**。） 

### 4.1 节点创建的四种形态参数

```text
# 教学示意，不参与构建
create /p "d"              # 持久
create -e /p "d"           # 临时（会话结束删）
create -s /p "d"           # 顺序（自动追加 10 位递增序号）
create -e -s /p "d"        # 临时顺序（分布式公平锁基石）
create -t 30000 /p "d"     # TTL 节点（3.5+，超时未改则自动删）
create -c /p "d"           # 容器节点（子节点全删后自动删）
```

### 4.6 / 4.5 ACL 权限模型

- ZK 的 ACL 是 **scheme:id:permission** 三元组：
  - `world:anyone:cdrwa`（默认，任何人全权限）；
  - `auth:/digest:user:pass:crdwa`（登录后用户）；
  - `digest:user:base64(sha1(pass)):crdwa`（密码摘要）；
  - `ip:192.168.1.0/24:cdrwa`（按 IP）。
- permission：`c`reate `d`elete `r`ead `w`rite `a`dmin。注意 `delete` 与 `write` 分离，
  **允许写数据但不允许删子节点**是 ZK ACL 的细粒度特性。

### 4.11 / 4.12 用版本号实现乐观锁

```text
# 教学示意，不参与构建：CAS 更新
get /p -> 看到 dataVersion=3
set -v 3 /p "new"     # 仅当当前版本==3 才成功；期间被别人改过则报 BadVersion
delete -v 3 /p        # 同理，版本不匹配则拒绝
```

> 这是 ZK 实现「并发安全更新」的标准手法，**无锁、靠版本冲突重试**。

### 4.13 / 4.15 / 4.20 Watch 与「递归 watch 痛点」

- `get -w`、`ls -w` 注册**一次性** watch；触发后要重新注册。
- 监听「整棵子树」的变更需要**递归**地在每个子孙节点上注册 watch——这就是 4.20 手写递归 watch 的动机。
- 但手写极易漏注册（新节点创建时忘记挂 watch），导致「丢通知」。

```java
// 教学示意，不参与构建：用 Curator 的 NodeCache/TreeCache 替代手写递归 watch
CuratorFramework client = CuratorFrameworkFactory.newClient(
        "127.0.0.1:2181", new ExponentialBackoffRetry(1000, 3));
client.start();
TreeCache cache = TreeCache.newBuilder(client, "/app").build();
cache.getListenable().addListener((c, event) -> {
    // 一次性拿到 子节点增删改/数据变更 的全量事件，无需手写递归注册
});
cache.start();
```

## 版本演进

- **本书无第二版**；本节写 2022 年口径 → 2026 年视角的变化。
- **Curator Cache 替代手写递归 watch**：4.20 的自实现在 2026 年应直接用
  `CuratorCache` / `TreeCache` / `NodeCache`（apache/curator 3173★），更稳定、无漏注册。
- **容器节点（Container）/ TTL 节点**：本书基于 3.x 早期，可能未完整覆盖 `-c`/`-t`；
  它们是「临时父节点 + 子节点全删自动回收」的现代用法。
- **ACL 安全实践**：生产必须用 `digest`/`ip`/`SASL` 收紧 `world:anyone` 的默认全开，本书只在命令层面演示。
- **配额是软限制**：本书 4.8 的 quota 超出只**告警不拒绝**（ZK 软配额），别误以为能硬限流。

## 经典论文与原始文献

| 文献 | 出处 | 贡献 |
| --- | --- | --- |
| Hunt et al.《ZooKeeper: Wait-free Coordination for Internet-scale Systems》 | USENIX ATC 2010 | Watch、ACL、原子操作的原始定义 |
| Apache ZooKeeper 官方文档（ZooKeeper CLI / ACLs / Quotas） | zookeeper.apache.org | 命令与 ACL scheme 的权威释义（版本较多） |

## 近年研究与工业界开源实践（2015–2026）

- **apache/curator（3173★，2026-09 实测）**：ZK Java 客户端事实标准，提供 Cache/锁/选举/重试；
  是 4.20 手写递归 watch 的工程化替代。
- **apache/zookeeper（12811★）**：3.5+ 引入容器/TTL 节点、动态重配置，命令面持续扩展。
- **zkclient（历史项目）**：早于 Curator 的封装，现已基本被 Curator 取代，本书未提及属正常。

## 常见误区与本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「watch 是持久订阅」 | 一次性，触发后失效，需重注册 |
| 2 | 「手写递归 watch 是最佳实践」 | 2026 年直接用 Curator Cache，手写易漏注册丢通知 |
| 3 | 「quota 能硬限制」 | ZK 配额是**软限制**，超出只告警不拒绝 |
| 4 | 「ACL 默认安全」 | 默认 `world:anyone:cdrwa` 全开，生产须收紧 |
| 5 | 「delete 可删带子节点的节点」 | 裸 delete 不行，必须 `deleteall`（4.2） |
| 6 | 🔧 未完整覆盖容器/TTL 节点 | ZK 3.5+ 的 `-c`/`-t` 是现代常用节点形态 |
| 7 | 🔧 未提 Curator Cache 体系 | 4.20 自实现应让位于 Curator，本书仍停留在手写下沉 |

## 与其他章 / 其他书的联系

- **本书内**：
  - 4.1 节点类型 → [01-ZooKeeper核心理论.md](01-ZooKeeper核心理论.md)（1.10 四种类型）；
  - 4.13/4.15/4.20 watch → [01-ZooKeeper核心理论.md](01-ZooKeeper核心理论.md)（1.2 一次性语义）；
  - 4.6 ACL → [03-搭建ZooKeeper主从运行环境.md](03-搭建ZooKeeper主从运行环境.md)（集群安全延伸）。
- [../深入理解分布式共识算法/00-总览与阅读地图.md](../深入理解分布式共识算法/00-总览与阅读地图.md)
  ——ZK 机制背后的协调/共识原理。
