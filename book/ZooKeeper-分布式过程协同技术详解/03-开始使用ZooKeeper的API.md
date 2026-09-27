# 第 3 章　开始使用 ZooKeeper 的 API

> 原书第 3 章是从「概念」跨到「能写代码」的第一道坎：怎么建一个 `ZooKeeper` 句柄、连接怎么用
> 监视器（Watcher）回调、同步与异步 API 的差异、以及那些绕不开的异常（尤其
> `ConnectionLossException`、`KeeperException`）。这一章的示例是后面主从实战的「基础件」。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 建立会话 | `new ZooKeeper(connectString, sessionTimeout, watcher)` 得到句柄 | 句柄是**线程安全**的，全应用共享一个即可 |
| 连接监视器 | 实现 `Watcher.process(WatchedEvent)`，靠它感知连接状态变化 | 连接状态（SyncConnected/Expired…）与节点事件**走同一个回调**，需按类型分流 |
| 基本操作 | create / delete / exists / getData / setData / getChildren 的同步签名 | 读操作可带 watch；写操作带版本号可做 CAS |
| 异常体系 | `KeeperException`（服务端错误）+ `InterruptedException`（客户端中断） | `ConnectionLossException` 是写代码时第一个要处理的坑 |
| 同步 vs 异步 | 同步阻塞直到返回；异步靠回调/Context 在 IO 线程返回 | 高吞吐或 UI 线程用异步；简单脚本用同步 |
| 创建节点 | `create(path, data, acl, mode)`，mode 决定持久/临时/顺序 | 这一段把第 2 章的「类型」落到 API 形参上 |

## 核心精讲

（以下为教学性梳理，Java 片段均**教学示意，不参与构建**。）

### 3.1 建立会话：一个句柄，全局共享

```java
// 教学示意，不参与构建：最简连接
ZooKeeper zk = new ZooKeeper(
    "127.0.0.1:2181",            // connectString：逗号分隔的多个 server
    15000,                       // sessionTimeout(ms)
    new Watcher() {              // 连接监视器
        public void process(WatchedEvent e) {
            if (e.getState() == Event.KeeperState.SyncConnected) {
                // 连接已建立，可以开始操作
            }
        }
    });
```

- 句柄**线程安全**，一个进程建一个就够，别每个请求 new 一个（连接代价高）。
- 构造返回**不保证已连上**——`SyncConnected` 事件到达后才算真正可用；很多人踩过「刚 new 完就调
  操作报 ConnectionLoss」的坑。

### 3.2 监视器：连接状态与节点事件同一个回调

`Watcher.process` 收到的是 `WatchedEvent`，含两类信息：

| 维度 | 取值 | 含义 |
| --- | --- | --- |
| `getState()` | `SyncConnected / Disconnected / Expired / AuthFailed` … | **连接级**状态，决定你能不能继续用 |
| `getType()` | `None / NodeCreated / NodeDeleted / NodeDataChanged / NodeChildrenChanged` | **节点级**事件，仅当 `getType()!=None` 时有效 |

> 关键陷阱：当 `getType() == None` 时，事件是**连接状态变化**而非节点变化（如会话过期）。
> 代码必须先看 state，再决定是「重连重注册」还是「处理节点事件」。

### 3.3 同步 API 长什么样

```java
// 教学示意，不参与构建：基本 CRUD 的同步形态
zk.create("/app/config", bytes, ZooDefs.Ids.OPEN_ACL_UNSAFE, CreateMode.PERSISTENT);
byte[] data = zk.getData("/app/config", false, new Stat());   // false=不设 watch
Stat stat = zk.setData("/app/config", newData, stat.getVersion()); // 带版本=CAS
List<String> kids = zk.getChildren("/app/workers", true);     // true=设 watch
zk.delete("/app/config", stat.getVersion());
```

- `exists/getData/getChildren` 的 watch 参数：节点不存在时 `exists` 的 watch 能在「被创建」时触发；
- 版本号（`version`）传 `-1` 表示「不检查版本直接改」，传具体值则是 CAS——并发改同一个节点靠它防覆盖。

### 3.4 异常：两类，处理方式相反

| 异常 | 来源 | 怎么处理 |
| --- | --- | --- |
| `KeeperException` 及其子类（如 `ConnectionLossException`、`NodeExistsException`） | 服务端 / 会话层错误 | 大多可**重试**，但要注意幂等（第 5 章） |
| `InterruptedException` | 客户端线程被中断 | 恢复中断标志（`Thread.currentThread().interrupt()`），由上层决定 |

```java
// 教学示意，不参与构建：ConnectionLoss 的典型重试骨架
try {
    zk.create(path, data, acl, mode);
} catch (ConnectionLossException e) {
    // 连接丢了：操作可能成功也可能没成功 -> 用 exists 探一下再决定
    if (zk.exists(path, false) != null) { /* 已创建，视为成功 */ }
    else { zk.create(path, data, acl, mode); /* 重试 */ }
}
```

> 这正是第 5 章「故障处理」的伏笔：连接丢了，你**不知道服务端做没做**，所以必须靠
> `exists`/幂等来收敛状态。

### 3.5 异步 API：回调 + 上下文

```java
// 教学示意，不参与构建：异步 create
zk.create("/app/tasks/task-", data, acl, CreateMode.PERSISTENT_SEQUENTIAL,
    new AsyncCallback.StringCallback() {
        public void processResult(int rc, String path, Object ctx, String name) {
            // rc: 返回码(0=成功)；path: 请求路径；name: 实际创建名(含序号)；ctx: 透传上下文
        }
    }, "my-context");
```

- 异步不阻塞调用线程，结果在 ZK 的 IO 线程回调；
- 回调里拿到的 `rc`（return code）对应 `KeeperException.Code`，要手动翻译。

## 版本演进

- **本书无第二版**；本节写 2013 年口径 → 2026 年视角的变化。
- **Curator 早已取代手写 `ZooKeeper` 句柄**：第 8 章会讲，`CuratorFramework` 把连接管理、重试、
  监视器封装掉，2013 年还要自己写的「连接状态分流 / 重试骨架」，今天基本不用手写。**读第 3 章理解
  原理即可，真写业务请用 Curator**。
- **ZK 3.5+ 引入 `ZooKeeper` 的新构造与 fluent 配置、SASL 认证支持增强**，但同步/异步的核心签名
  基本稳定，本章 API 形态仍有效。
- **客户端生态外溢**：Python（kazoo）、Go（go-zookeeper）、Node 等社区客户端语义与 Java 一致，
  但重连/重试策略各异，「连接状态分流」这个坑在每种语言里都存在。

## 经典论文与原始文献

| 文献 | 出处 | 贡献 |
| --- | --- | --- |
| Hunt et al.《ZooKeeper: Wait-free Coordination for Internet-scale Systems》 | USENIX ATC 2010 | **API 语义（CRUD + watch + 顺序节点）的原始定义** |
| Ousterhout et al.《The ZooKeeper Client API》（随原版书配套文档 / 设计笔记） | Apache 文档 | 客户端会话与异常模型的设计说明（版本较多，按官方文档为准） |

## 近年研究与工业界开源实践（2015–2026）

- **Curator（高层 API 的事实标准）**：`apache/curator`（3173★）把第 3 章要手写的「连接监视器分流、
  重试、节点存在性探查、顺序节点创建」全部封装，现代 Java 项目几乎不直接用裸 `ZooKeeper` 句柄。
- **etcd 客户端（gRPC + 流 watch）**：`etcd-io/etcd`（52309★）的 clientv3 用 gRPC 双向流实现**持久
  监听**，与 ZK「一次一注册」的异步回调风格差异明显，选型时直接对比第 3 章的异步模型。
- **ZK 多语言客户端生态**：Python `kazoo`、Go `go-zookeeper`、C 客户端（第 7 章）等，API 形态都
  复刻本章的「句柄 + watch + 版本 CAS」三件套。
- **ZK 自身持续维护**：`apache/zookeeper`（12811★）3.8/3.9 线仍提供稳定的 Java API 与 C 客户端。

## 常见误区与本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「new 完 ZooKeeper 就能直接调操作」 | 构造返回不保证已连上，需等 `SyncConnected` 事件 |
| 2 | 「连接断了 = 操作失败」 | 连接断时你不知道服务端做没做，必须靠 `exists`/幂等收敛（第 5 章） |
| 3 | 「watch 事件里能拿到新数据」 | ZK 的事件**只通知「变了」**，不含新值；要再 `getData` 拉一次 |
| 4 | 「异常都能无脑重试」 | `ConnectionLoss` 可重试但需幂等；`NodeExists`/`NoNode` 等语义不同，别一刀切 |
| 5 | 「每个请求建一个句柄」 | 句柄线程安全、连接昂贵，应全应用共享一个 |
| 6 | 🔧 第 3 章未提 Curator 封装 | 2026 年 Java 生产代码几乎都用 Curator，裸 API 仅用于理解原理（见第 8 章） |
| 7 | 🔧 未提 etcd 的流 watch 对比 | 现代协调客户端多用持久监听，读本章时宜对照 etcd clientv3 的模型 |

## 与其他章 / 其他书的联系

- **本书内**：
  - 第 3 章的**句柄/监视器/异常** → 第 4 章「处理状态变化」的 watch 实战；
  - 第 3 章的 **ConnectionLoss 重试** → 第 5 章「故障处理」的系统化；
  - 第 3 章的 **create + 模式** → 第 4–6 章的锁/选举/队列配方；
  - 第 3 章的 **Watcher 回调** → 第 2 章 watch 语义的代码落地。
- [../设计数据密集型应用/09-一致性与共识.md](../设计数据密集型应用/09-一致性与共识.md)
  ——客户端「读后是否最新、sync 语义」与第 3 章 getData 的时效界对读。
- [../深入理解分布式共识算法/00-总览与阅读地图.md](../深入理解分布式共识算法/00-总览与阅读地图.md)
  ——连接丢失/会话过期的底层（leader 切换、Zab 恢复）在那边展开，呼应第 3 章异常。
- [../凤凰架构/](../凤凰架构/) ——云原生客户端（etcd/k8s client）与 ZK 客户端在「重连/重试」上的
  现代实践，是本章的 2026 年延伸。
