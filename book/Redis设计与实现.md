# Redis设计与实现

https://book.douban.com/subject/25900156/

windows 10电脑上
Redis设计与实现.pdf

出版年: 2014-6
作者: 黄健宏
ISBN: 9787111464747

string
list
hash
set
zset

第2章 简单动态字符串

2


第3章 链表 list LinkedList
3

第4章 字典

set a b

a b就是字典

10086个/很多个kv对

dict
dictEntry
dictht

第5章 跳跃表 skiplist

zrang
zcard  `ZCARD`是Redis中用于有序集合（Sorted Set）的命令之一，它用于获取有序集合中指定成员的排名（Rank）。

第6章 整数集合

6


第7章 压缩列表

7

第8章 对象

8


第二部分 单机数据库的实现  
第9章 数据库

9

第10章 RDB持久化
面试题
二进制的 全量备份，恢复

第11章 AOF持久化



第12章 事件

12


第13章 客户端


13


第三部分 多机数据库的实现  
第15章 复制


第16章 Sentinel

第17章 集群


第四部分 独立功能的实现  
第18章 发布与订阅

第19章 事务

19

第20章 Lua脚本

20

第21章 排序

21


第22章 二进制位数组

22


第23章 慢查询日志

23

第24章 监视器

24


## 跨年摘录（2020–2026 日常笔记聚合，2026-09-23 整理）

### 2020-02
> - 《Redis 设计与实现》

### 2021-04
> 其他。根据参与的项目加深学习吧。比如，如果需要写 DSL，可以读一下《领域特定语言》，对 Redis 感兴趣推荐读一下：《Redis 设计与实现》。有两本书，无论做什么项目，都推荐读：《Unix 编程艺术》、《UNIX 环境高级编程(第3版)》。


## 精读补写（系统整理，2026-09-23）

### 版本与 ISBN
- 《Redis 设计与实现》，黄健宏 著，机械工业出版社，2014-06，**ISBN `978-7-111-46474-7`**（豆瓣 https://book.douban.com/subject/25900156/ ）。
- **重要前提**：本书基于 **Redis 3.0 源码**讲解（含复制、Sentinel、集群）。Redis 至今已演进到 7.x/8.x，底层结构已有实质变化，读书时应以"理解设计思想 + 对照当前源码"的方式使用，而非照抄结构细节。
- 主线：**数据结构与对象**（SDS、链表、字典与渐进式 rehash、跳跃表、整数集合、压缩列表、5 种对象与编码转换）→ **单机数据库**（RDB 持久化、AOF 与重写、事件驱动、客户端与服务器、过期键策略）→ **多机**（复制、Sentinel、集群）→ **独立功能**（发布订阅、事务、Lua 脚本、慢查询、监视器）。

### 经典论文与原始文献根基
- **Pugh《Skip Lists: A Probabilistic Alternative to Balanced Trees》**(CACM 1990)——**zset（有序集合）与集群内部数据结构**的出处，这是 Redis 最典型的"论文直接落地"案例。
- **Flajolet 等《HyperLogLog: the analysis of a near-optimal cardinality estimation algorithm》**(AOFA 2007)；Heule 等《HyperLogLog in Practice》(2013)——`PFADD/PFCOUNT` 的基数统计算法，用极省内存换取标准误差率。
- **Bloom《Space/Time Trade-offs in Hash Coding》**(1970)——布隆过滤器（RedisBloom / Redis Stack）与缓存穿透防护的依据。
- **Gray & Reuter《Transaction Processing》**(1993) 与 **ARIES**(Mohan 等, 1992)——虽然 Redis 不是关系库，但 AOF 的**追加写 + 重写**与 WAL/checkpoint 思想同源；RDB 则依赖 **fork + copy-on-write** 快照。
- **Lamport 逻辑时钟/租约思想** 与 **Gossip 协议**——Sentinel 与集群的节点发现与故障判定；注意：**Redis Cluster 并未使用 Raft/Paxos**，它用 Gossip + 哈希槽 + 异步复制，**不保证强一致**（故障切换可能丢写）。

### 最新研究与产业进展
- **版本演进要点**：3.0 集群 → 4.0 模块系统与 LFU → 5.0 **Streams** → 6.0 **多线程 IO**（注意：命令执行仍是单线程）+ 客户端缓存 tracking → 7.0 **Functions**、multi-part AOF、sharded pub/sub → 7.2/7.4 性能与内存持续优化 → **Redis 8（2025）** 引入 **Vector Sets** 等 AI 负载能力并显著提升吞吐。
- **许可证与生态分化（2024 重大事件）**：2024 年 3 月 Redis Labs 将许可证从 BSD 改为 **RSALv2 / SSPLv1**；社区随即分叉出 **Valkey**（Linux Foundation 托管，2024），目前已被多数 Linux 发行版与云厂商采用为默认替代。另有 **KeyDB**（多线程）、**Dragonfly**（2022+，共享无锁架构，宣称极高吞吐）等兼容实现。
- **底层结构的现代变化**：Redis 7 起 **listpack 取代 ziplist**（quicklist 基于 listpack）、SDS 头部按大小分级以省内存、ziplist 逐步退出；字典渐进式 rehash 的设计思想仍然成立。
- **应用趋势**：Redis 从缓存扩展到**分布式锁（Redlock 争议：Martin Kleppmann 与 antirez 的公开辩论值得读）、限流、排行榜、消息队列（Streams）、会话存储、向量检索（Redis Stack / Redis 8 Vector Sets）**；多租户与持久化权衡（AOF fsync everysec 的持久性边界）是面试与生产的常见考点。

### 常见误区 / 纠错
- **"Redis 集群是强一致的"错误**：Cluster 用异步复制，主从切换时会丢失最近未确认的写；它不提供 Raft 式的共识保证。需要强一致时应选 etcd/ZooKeeper/Consul 或 TiKV 类系统。
- **"Redis 6 之后是多线程"需限定**：多线程只用于**网络 IO 与协议解析**，命令执行仍为单线程（这正是其原子性与简单性的来源）；不要据此推断"Redis 已可并行执行命令"。
- **"keys 命令可以用来查"禁止在生产使用**：`KEYS` 会阻塞单线程事件循环，应使用 `SCAN` 系列增量迭代。
- **缓存三大问题的正确解法**：穿透（布隆过滤器 / 空值缓存）、击穿（互斥重建或逻辑过期）、雪崩（TTL 加随机抖动 + 多级缓存 + 熔断限流）——仅靠"设置过期时间"不够。
- 本书的**数据结构章节对应 Redis 3.0**，若笔记据此描述 `ziplist`，应补注"Redis 7+ 已由 listpack 取代"。
