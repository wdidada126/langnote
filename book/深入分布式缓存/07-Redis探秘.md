# 第 7 章　Redis 探秘

> 框架篇的核心章之一。这一章（与第 8 章分工）讲 Redis **单机内核**：为什么单线程还能那么快、
> 它的数据结构与对象体系、以及持久化（RDB/AOF）。分布式能力留到第 8 章。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 7.1 单线程事件循环 | 单线程 + I/O 多路复用（epoll/kqueue）+ 文件事件处理器 | 单线程避免锁竞争；瓶颈在网络/内存而非 CPU 核数 |
| 7.2 数据结构与对象 | SDS、ziplist、skiplist、dict、intset、quicklist；string/hash/list/set/zset | 底层结构随数据规模自动切换，兼顾内存与性能 |
| 7.3 持久化 | RDB（快照）+ AOF（追加日志）；混合持久化 | 两者权衡「恢复速度 vs 数据丢失窗口」 |
| 7.4 内存管理 | 过期删除（惰性+定期）、内存回收、maxmemory + 淘汰策略 | 内存是 Redis 的硬约束，淘汰策略决定行为 |

## 核心精讲

（以下为教学性梳理，伪代码/SQL 均**教学示意，不参与构建**。）

### 7.1 单线程为什么快

```text
# 教学示意，不参与构建：Redis 事件循环（伪代码）
while true:
    events = epoll_wait(fds, timeout)        # I/O 多路复用，单线程监听所有连接
    for e in events:
        if e is 新连接: accept + 注册可读
        if e is 可读:   读请求 -> 解析 -> 执行命令 -> 写回缓冲
    # 关键: 命令执行是**串行的**，无锁；靠「纯内存 + 非阻塞 IO」吃满单核
```

- 单线程的代价：一个**慢命令（如 `KEYS *`、大 `HGETALL`）会阻塞整实例**。这是 Redis 使用铁律。

### 7.2 数据结构：以 zset 为例

```text
# 教学示意，不参与构建：有序集合的底层
zset = dict(key -> score)  +  skiplist(score 有序)
查询 member 的 score:    dict  O(1)
按排名/分数范围遍历:       skiplist O(logN)
小数据时使用 ziplist/listpack 紧凑存储以省内存（随规模切换到 skiplist+dict）
```

- Redis 的「对象类型」与「底层编码」解耦：同一个 `hash` 在小数据时用 `ziplist`，大时转 `hashtable`。

### 7.3 持久化对照

| 方式 | 原理 | 优点 | 缺点 |
| --- | --- | --- | --- |
| **RDB** | 定时 fork 子进程做内存快照 | 恢复快、文件小 | 可能丢最近一次快照后的数据 |
| **AOF** | 追加每条写命令；定期 rewrite 压缩 | 数据丢失窗口小 | 文件大、恢复慢 |
| **混合（🔧 4.0+）** | AOF 头 + RDB 体 | 兼顾两者 | 需较新版本 |

## 版本演进

- **本书无第二版**；本节写 2017 年口径（Redis 3.x/4.0）→ 2026 年视角的变化。
- **🔧 多线程网络 I/O（Redis 6.0，2020）**：本书成书时 Redis 是「纯单线程」；
  6.0 引入**多线程处理网络读写**（命令执行仍单线程），大吞吐下显著提升 QPS、降低延迟。
  2026 年说「Redis 单线程」必须补这句——是「单线程**命令执行** + 多线程 **IO**」。
- **🔧 客户端缓存（Client-side caching / tracking，6.0）**：服务端在 key 变更时通知客户端作废本地副本，
  把 [01-缓存为王.md](01-缓存为王.md) 1.4 的「客户端缓存」真正落地。
- **🔧 Redis 7.0（2022）**：Functions（取代部分 Lua 脚本）、Sharded Pub/Sub、listpack 全面替代 ziplist；
  `HELLO 3` / RESP3 成熟。
- **🔧 Valkey 分叉（2024）**：Redis 改 SSPL/RSAL 许可后，Linux 基金会接管 **Valkey**（valkey-io/valkey，**27297★**），
  Redis 7.2.4 的直接分叉；2026 年许多云厂商默认提供 Valkey。本书只讲 Redis 一家，需补「分叉之争」。
- **🔧 Dragonfly / KeyDB 等新内核**：`dragonflydb/dragonfly`（**31685★**，C++ 线程级并行、宣称兼容 Redis）、
  `Snapchat/KeyDB`（**12504★**，多线程 Redis 分叉）成为替代选项，挑战「单线程」范式。

## 经典论文与原始文献

| 文献 | 出处 | 贡献 |
| --- | --- | --- |
| Salvatore Sanfilippo（antirez）Redis 设计与文档 | 官方文档 / blog | **Redis 的原始设计与演进记录**（工程，非论文） |
| Pugh《Skip Lists: A Probabilistic Alternative to Balanced Trees》 | CACM 1990 | **跳表**，zset 的底层（7.2） |
| Ousterhout《Why Threaded Programs Are Hard》等 | — | 单线程事件循环的论证背景 |
| Redis 官方 persistence / replication 文档 | redis.io | 7.3 持久化一手出处 |

> 说明：Redis 是工程系统，权威出处是 antirez 的设计文档与官方文档；底层算法（跳表等）见上表。

## 近年研究与工业界开源实践（2015–2026）

- **实测 star（2026-09，`gh api` 实测）**：

| 项目 | 定位 | star |
| --- | --- | --- |
| `redis/redis` | Redis 本体（本章主角，3.x→7.x 演进） | 76487 |
| `valkey-io/valkey` | Redis 2024 分叉（Linux 基金会），兼容协议 | 27297 |
| `dragonflydb/dragonfly` | C++ 线程级并行，宣称 Redis/Memcached 兼容 | 31685 |
| `Snapchat/KeyDB` | 多线程 Redis 分叉 | 12504 |
| `redisson/redisson` | Redis 的 Java 客户端/分布式对象（🔧 现代） | 24403 |
| `redis/lettuce` | 异步响应式 Java 客户端（🔧 现代） | 5779 |

- **多线程化成为主线**：Redis 6.0 IO 多线程、KeyDB 全程多线程、Dragonfly 线程级并行，
  共同说明「单线程」不再是 Redis 生态的唯一答案。
- **许可（license）变局**：Redis 2024 改协议触发 Valkey 分叉，2026 年选型必须同时考虑「功能 + 许可」，
  本书成书时不存在此问题。
- **客户端现代化**：Lettuce（异步）、Redisson（分布式锁/对象）成为 Java 主流客户端，本书只提 Jedis（同步阻塞）。

## 常见误区与本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「Redis 是单线程的」 | 准确说：**命令执行单线程，网络 IO 自 6.0 起多线程**；Dragonfly/KeyDB 更是全程多线程 |
| 2 | 「Redis 慢命令无所谓」 | 慢命令阻塞整实例（单线程串行执行），生产禁用 `KEYS`/`FLUSHALL` 大键操作 |
| 3 | 「AOF 一定比 RDB 安全」 | AOF 丢窗口小但恢复慢、文件大；混合持久化才兼顾，且都需合理配置 |
| 4 | 「Redis 数据都在内存，不怕丢」 | 持久化配置不当或宕机仍可能丢数据；需按业务选 RDB/AOF/混合 |
| 5 | 🔧 本书未提 Redis 6.0 多线程 IO | 2026 年「单线程」论断必须补「IO 多线程」（2020 引入） |
| 6 | 🔧 本书未提客户端缓存（tracking） | Redis 6.0 客户端缓存是 2026 年读路径优化关键，应补 |
| 7 | 🔧 本书只讲 Redis 一家 | 🔧 2024 Valkey 分叉 + Dragonfly/KeyDB 替代方案，2026 年必补 |
| 8 | 🔧 本书客户端只提 Jedis | 🔧 Lettuce/Redisson 已成主流，应补 |

## 与其他章 / 其他书的联系

- **本书内**：
  - 7.1 单线程 → [08-分布式Redis.md](08-分布式Redis.md) 8.1（单线程下的复制模型）；
  - 7.3 持久化 → [08-](08-分布式Redis.md) 8.1（主从同步 RDB 传输）；
  - 7.4 淘汰 → [01-缓存为王.md](01-缓存为王.md) 1.5（淘汰策略理论）。
- [../大规模分布式存储系统/02-单机存储系统.md](../大规模分布式存储系统/02-单机存储系统.md)
  ——Redis 的「内存 + 持久化」与单机存储引擎（2.5 故障恢复、2.6 压缩）对读。
- [../设计数据密集型应用/03-存储与检索.md](../设计数据密集型应用/03-存储与检索.md)
  ——跳表/SSTable/LSM 等结构与 Redis 底层编码的对照。
- [../深入分布式缓存.md](../深入分布式缓存.md)——大纲版提到「redis 是缓存」「Redis 在美团叫 Squirrel」。
