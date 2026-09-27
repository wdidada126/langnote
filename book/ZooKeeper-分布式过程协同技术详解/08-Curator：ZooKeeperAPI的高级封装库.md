# 第 8 章　Curator：ZooKeeper API 的高级封装库

> 原书第 8 章是「别再手写那些易错代码」的一章：Netflix 贡献、后进入 Apache 的 **Curator**，
> 把第 3–7 章里要手写的「连接管理、重试、监视器分流、节点存在性探查」全部封装，并提供了
> **开箱即用的协调配方**（锁、屏障、领导者选举、缓存、队列、服务发现）。读完这一章，再回头看
> 第 4–6 章的手写示例，会明白生产代码为什么几乎不裸用 `ZooKeeper` 句柄。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| CuratorFramework | 用 builder 构建 `CuratorFramework`，统一管理连接与生命周期 | 它是「增强版 ZooKeeper 句柄」，取代裸 `new ZooKeeper` |
| 重试策略（RetryPolicy） | `ExponentialBackoffRetry / RetryNTimes / RetryOneTime` 等 | 把第 5 章手写的「ConnectionLoss 探活重试」变成声明式 |
| 连接状态监听 | `ConnectionStateListener` 收到 `LOST / RECONNECTED / READ_ONLY` | 会话过期的「重建 + 重注册」由框架驱动，业务只响应状态 |
| 流式 API（Fluent） | `client.create().withMode(CREATE_MODE).forPath(path, data)` | 把「多参数 create」拼成可读链式调用 |
| 配方：分布式锁 | `InterProcessMutex`（可重入）、`InterProcessSemaphoreMutex` | 第 6 章锁配方的产品化实现 |
| 配方：领导者选举 | `LeaderLatch`（简单）/ `LeaderSelector`（可释放、推荐） | 第 1 章「选举」需求 + 第 6 章 fencing 考量的现成封装 |
| 配方：缓存 | `NodeCache / PathChildrenCache / TreeCache` | 第 4 章「watch 三步闭环」的封装，自动重注册 |
| 配方：屏障 / 队列 / 服务发现 | `DistributedBarrier`、`DistributedQueue`、`ServiceDiscovery` | 把常见协调模式标准化 |

## 核心精讲

（以下为教学性梳理，Java 片段均**教学示意，不参与构建**。）

### 8.1 用 CuratorFramework 取代裸句柄

```java
// 教学示意，不参与构建：构建并启动 CuratorFramework
CuratorFramework client = CuratorFrameworkFactory.builder()
    .connectString("127.0.0.1:2181")
    .sessionTimeoutMs(15000)
    .retryPolicy(new ExponentialBackoffRetry(1000, 3)) // 退避重试
    .build();
client.start();   // 框架接管连接建立、重试、状态机
// 之后所有操作走 client，不再手写 Watcher 分流
```

- 对比第 3 章：你不再实现 `Watcher.process` 去分流连接状态，框架已把「SyncConnected / LOST」
  转成 `ConnectionState` 枚举并回调给你；
- 对比第 5 章：你不再手写 `exists + 重试` 收敛，框架的 `RetryPolicy` 自动处理 `ConnectionLoss`。

### 8.2 重试策略：声明式故障恢复

```java
// 教学示意，不参与构建：重试策略对照第 5 章
new RetryNTimes(3, 1000);                       // 最多 3 次，间隔 1s
new ExponentialBackoffRetry(1000, 5);           // 退避：1s,2s,4s,8s,16s
new RetryUntilElapsed(10000, 500);              // 在 10s 内每隔 500ms 重试
```

- 这些策略直接对应第 5 章「连接丢失后安全重试」的工程需求，且内置了 `ConnectionLoss`
  的识别与退避，避免手写循环出错。

### 8.3 配方：分布式锁（第 6 章锁配方的产品化）

```java
// 教学示意，不参与构建：InterProcessMutex
InterProcessMutex lock = new InterProcessMutex(client, "/locks/resource-A");
lock.acquire();                // 拿锁（内部用顺序临时节点 + 只 watch 前驱，见 6.3）
try {
    // 临界区
} finally {
    lock.release();            // 释放（删自己的顺序节点）
}
```

- 它内置了第 6 章 6.3 的「顺序临时节点 + 只 watch 前驱」正确配方，**且避免了羊群效应**；
- **但默认不含 fencing token**（见 6.5 / 8.6）：若用这把锁保护共享存储，仍需在写入侧自行加单调令牌。

### 8.4 配方：领导者选举

```java
// 教学示意，不参与构建：LeaderSelector（推荐，可优雅释放领导权）
LeaderSelector selector = new LeaderSelector(client, "/election", new LeaderSelectorListenerAdapter() {
    public void takeLeadership(CuratorFramework c) throws Exception {
        // 成为 leader 时进入这里；方法返回即放弃领导权
        doLeaderWork();
    }
});
selector.autoRequeue();   // 失去领导权后自动重新参选
selector.start();
```

- `LeaderLatch` 更简单（抢到就当，直到 `close`），`LeaderSelector` 适合「干完一段就交还」的场景；
- 二者都基于「抢建临时节点 + watch」实现，是第 1 章选举需求的现成落地。

### 8.5 配方：缓存（第 4 章 watch 闭环的封装）

```java
// 教学示意，不参与构建：PathChildrenCache
PathChildrenCache cache = new PathChildrenCache(client, "/tasks", true);
cache.getListenable().addListener((c, event) -> {
    switch (event.getType()) {
        case CHILD_ADDED:    /* 新任务 */ break;
        case CHILD_REMOVED:  /* 任务消失 */ break;
    }
});
cache.start();   // 框架自动：初始拉全量 + 注册 watch + 事件触发后重注册
```

- 这正是第 4 章 4.2「三步闭环」的封装：你只写「事件来了怎么办」，重读与重注册交给框架；
- `NodeCache` 监听单节点、`TreeCache` 监听子树，覆盖了不同粒度的 watch 需求。

## 版本演进

- **本书无第二版**；本节写 2013 年口径 → 2026 年视角的变化。
- **Curator 在 2013 年后持续扩展**：新增 `ServiceDiscovery`（服务注册发现）、`Modeled Framework`
  （强类型节点）、`CuratorCache`（统一替代旧 `NodeCache/PathChildrenCache/TreeCache`，减少概念碎片）。
- **容器节点（container znode）支持**：Curator 提供 `PersistentNode` / `Container` 封装，对应 ZK 3.5+
  的容器节点，是本书 2013 年版本没有的节点类型（见第 2 章）。
- **Curator 仍是 Java 生态的事实标准客户端**，但**新项目选型时仍要问「为什么不是 etcd」**
  （K8s 用 etcd、Raft 系更主流），Curator 主要服务 Hadoop 系存量与既有 ZK 集群。

## 经典论文与原始文献

| 文献 | 出处 | 贡献 |
| --- | --- | --- |
| Apache Curator 官方文档（《Curator Recipes》《Curator Framework》） | Apache 文档 | **配方与框架 API 的权威出处**（版本较多，以对应版本文档为准） |
| Hunt et al.《ZooKeeper: Wait-free Coordination for Internet-scale Systems》 | USENIX ATC 2010 | Curator 所有配方（锁/选举/屏障/队列）的语义源头 |

## 近年研究与工业界开源实践（2015–2026）

- **Curator 自身**：`apache/curator`（3173★）持续维护，是 Java 项目用 ZK 的默认依赖。
- **etcd 客户端生态（对照）**：`etcd-io/etcd`（52309★）的 clientv3 在 Go 生态提供等价能力，且
  持久 watch + lease 让「缓存/选举」更内聚，是 Curator 在 Raft 系的对位物。
- **Consul / Nacos 的内置服务发现**：`hashicorp/consul`（30087★）、`alibaba/nacos`（33419★）
  把 Curator `ServiceDiscovery` 的能力内建进自身，减少「ZK + Curator 做注册中心」的新建需求。
- **ZK 自身**：`apache/zookeeper`（12811★）仍是 Curator 的服务端底座，3.8/3.9 线稳定。

## 常见误区与本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「用了 Curator 锁就绝对安全」 | `InterProcessMutex` 不含 fencing token，保护共享存储仍需自加单调令牌（6.5） |
| 2 | 「Curator 自动处理一切故障」 | 框架接管连接/重试，但**业务逻辑的幂等**仍要自己保证（第 5 章） |
| 3 | 「缓存事件含最新数据」 | 缓存事件仍是「通知」，需要的数据从 `event.getData()` / 本地缓存取，仍属通知语义 |
| 4 | 🔧 第 8 章未提 `CuratorCache` 统一缓存 | 新版本用 `CuratorCache` 取代三套旧 Cache，概念更简洁，需补 |
| 5 | 🔧 未提 ServiceDiscovery / Modeled Framework | 这是 2013 年后 Curator 的重要扩展，现代用法必含 |
| 6 | 🔧 未对比 etcd clientv3 的 lease+watch | 新项目「选 Curator 还是 etcd 客户端」是 2026 年的真实决策，需补对照 |
| 7 | 🔧 未提示容器节点封装 | ZK 3.5+ 容器节点 + Curator `PersistentNode` 是本书原版没有的能力 |

## 与其他章 / 其他书的联系

- **本书内**：
  - 第 8 章的 **CuratorFramework/重试/状态监听** → 第 3 章裸句柄 + 第 5 章故障处理的封装版；
  - 第 8 章的 **锁/选举配方** → 第 6 章 caveats 的「正确配方 + 其局限（fencing）」；
  - 第 8 章的 **缓存** → 第 4 章 watch 三步闭环的封装；
  - 第 8 章的 **配方语义** → 第 2 章数据模型 / 第 9 章这些写如何经 Zab 一致生效。
- [../深入理解分布式共识算法/00-总览与阅读地图.md](../深入理解分布式共识算法/00-总览与阅读地图.md)
  ——leader 选举底层（Zab/Raft）与第 8 章 `LeaderSelector` 的对读。
- [../设计数据密集型应用/09-一致性与共识.md](../设计数据密集型应用/09-一致性与共识.md)
  ——fencing、leader lease 与第 8 章锁/选举正确性对读。
- [../凤凰架构/](../凤凰架构/) ——云原生服务发现/选主（多用 etcd/K8s Lease）与 Curator 配方的
  2026 年对照。
