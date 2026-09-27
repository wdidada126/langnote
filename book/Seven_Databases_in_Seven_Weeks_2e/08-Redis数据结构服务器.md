# 08 Redis（Data Structure Server Store）——键值与数据结构

> 对应官方页实抓目录（✅）：Day1 CRUD and Datatypes｜Day2 Advanced Usage, Distribution｜Day3 Playing with Other Databases｜Wrap-Up。
> Redis 本机**无安装**（`where redis-cli` 无果，⚠️ 不装不测）；命令/持久化/集群运行行为 ⚠️ 转述（纵深让位盘上 Redis 专册群）。🔧 类比用 SQLite 3.45.3 复现「有序集合排名 / 原子自增 / 取 Top-K」的语义，**非 Redis 行为**。
> 纵深全景：[../Learning_Redis/00-总览与阅读地图.md](../Learning_Redis/00-总览与阅读地图.md)、[../Redis_Cookbook/00-总览与阅读地图.md](../Redis_Cookbook/00-总览与阅读地图.md)、[../Redis设计与实现.md](../Redis设计与实现.md)、[../Redis深度历险.md](../Redis深度历险.md)、[../Redis实战.md](../Redis实战.md)、[../Redis5设计与源码分析.md](../Redis5设计与源码分析.md)、[../master-redis.md](../master-redis.md)、[../Redis入门指南.md](../Redis入门指南.md)。

## 8.0 Redis 不是「普通 KV」，而是「数据结构服务器」

Redis 表面是 key→value 的内存键值存储，本质是**把服务端数据结构做成命令**：string/hash/list/set/zset 各有原子操作。它的价值主张是**延迟极低 + 结构即语义 + 单线程命令天然串行**（免锁的原子性）。书把它放最后一库，因为「缓存 / 计数 / 排行 / 队列」几乎每个其它库都要和它配对（见 Day3）。

## 8.1 Day 1：CRUD 与数据类型

- **key→value 基础**：`SET/GET/DEL/EXPIRE`；TTL 让 Redis 天然是缓存。
- **五大类型**：`string`（可当整数 INCR）、`hash`（对象 field→value）、`list`（两端 O(1)）、`set`（无序唯一 + 交并差）、`zset`（按 score 排序 + 排行）。
- ⚠️ 转述：Day1 用 `redis-cli` 跑通各类型的基本命令，强调「一条命令 = 一个原子结构操作」。

> 🔧 **类比组 E：zset 排名 / Top-K / INCR（非 Redis，SQLite 3.45.3）**
> Redis 的有序集合语义（score 排序 + 名次 + 取前 N）可放 SQL 里感受。本机 `z(member,score)` 5 行 `(a,10)(b,25)(c,7)(d,40)(e,18)`：
> ```sql
> SELECT member,score FROM z ORDER BY score DESC LIMIT 3;          -- ZREVRANGE 0 2
> SELECT (SELECT COUNT(*)+1 FROM z z2 WHERE z2.score>(SELECT score FROM z WHERE member='c'));  -- ZRANK
> UPDATE z SET score=score+5 WHERE member='a';                     -- ZINCRBY a 5
> ```
> 真实输出：Top-3=`[('d',40),('b',25),('e',18)]`；`c` 的名次=**5**（末位，score=7）；`a` 自增后 score=**15**（10→15）（✅）。要点：Redis 把这三步做成 O(logN) 的单命令，而 SQL 里「排名」天然是一次有序扫描（ZRANK 类比 O(N)）——Redis 靠 skiplist 把它压到 O(logN)；对照 [../数据库系统概念6/11-索引与散列.md](../数据库系统概念6/11-索引与散列.md)。声明：SQLite 非 Redis，无内存 skiplist/原子单线程语义，仅类比「排序集合」计算语义。与 [../Learning_Redis/00-总览与阅读地图.md](../Learning_Redis/00-总览与阅读地图.md) 的类型语义章互为映射。

## 8.2 Day 2：高级用法与分布式

- **持久化**：RDB 快照 + AOF 日志（内存库的耐久化两条路）；混合持久化。
- **事务与脚本**：`MULTI/EXEC/WATCH`（队列式，非回滚型）+ Lua 脚本服务端原子执行。
- **发布订阅 / Stream**：`PUB/SUB` 广播；5.0 的 `Stream` 追加日志（书基线后的重要增补 ⚠️）。
- **分布式**：主从复制（Replication）→ Sentinel 哨兵（自动故障转移）→ Cluster（16384 哈希槽分片）。
- ⚠️ 转述：Day2 命令族与集群语义细节全转述，运行不可本机测。

## 8.3 Day 3：和其它数据库一起玩（Redis 作加速器）

- **缓存旁路（cache-aside）**：读时先查 Redis、未命中回落 PG/Mongo 再回填——本书「跨库」主题的收束章。
- **把 Redis 当第二索引**：PG 复杂查询的结果集按 key 缓进 Redis，用 TTL 换掉重复重计算。
- **会话 / 计数器 / 限流**：Web 层横切需求统一交给 Redis，把主库留给真相存储。
- ⚠️ 转述：Day3 演示「Redis + 另一库」的组合拳；真实命中率/回源风暴等运行指标不可本机测。

## 8.4 Wrap-Up：Redis 适合什么、不适合什么

- **适合**：低延迟点查、缓存、计数/排行/队列、会话、需要结构即语义的场景；作其它库的读加速层。
- **不适合**：大规模持久真相存储（受内存约束）、复杂 ad-hoc 检索（无二级索引原生）、强事务/关系完整性。
- ⚠️ 转述：作者结论——Redis 几乎不「替代」主库，而是「配」主库；这正是它排在末章、Day3 专讲联动的原因。

## 8.5 本册内互链

- 给关系库当缓存 → [02-PostgreSQL关系锚点.md](02-PostgreSQL关系锚点.md)（PG 真相 + Redis 加速）。
- 给文档/宽列补低延迟读 → [04-MongoDB文档模型.md](04-MongoDB文档模型.md)、[07-DynamoDB托管NoSQL.md](07-DynamoDB托管NoSQL.md)。

## 8.6 常见坑与设计要点（⚠️ 转述，Redis 通识，纵深让位专册）

- **大 key / 热 key**：单 key 存百万元素或超大 value 会阻塞单线程、拖垮复制——拆 key、用 hash 分桶。
- **缓存三兄弟**：穿透（查不存在的键→打库，用空值/布隆）、击穿（热 key 过期瞬间并发回源，用互斥锁/逻辑过期）、雪崩（大批 key 同刻过期，TTL 加随机抖动）。
- **内存即上限**：`maxmemory` + 逐出策略（`allkeys-lru` 等）决定它能否当「缓存」而非「存储」——放大数据集前先算账。
- **持久化不是零成本**：RDB fork 有停顿、AOF everysec 有丢数据窗口；把 Redis 当「可重建缓存」比当「唯一真相」安全。
- **别拿 Redis 做检索**：无内建二级索引/复杂查询（除 RediSearch 模块），ad-hoc 查询该去 Mongo/PG/ES（[04](04-MongoDB文档模型.md)、[02](02-PostgreSQL关系锚点.md)、ES 专册）。

## 8.7 Wrap-Up 练习重构（✅ 体例 + ⚠️ 题面转述）

1. 用 `ZSET`（score=时间戳）实现一个「延迟队列」，`ZRANGEBYSCORE` 轮询到期任务。
2. 用本机 🔧 组 E（SQLite `ORDER BY + COUNT`）复现 Top-K 与 ZRANK，再讨论 Redis 为何能 O(logN)。
3. **跨库题（本书招牌）**：给 PostgreSQL（[02](02-PostgreSQL关系锚点.md)）的一条昂贵聚合加 Redis cache-aside，设计失效策略。
4. 思辨题：把会话放 Redis 而非关系表，换来的是什么、失去的是什么？（速度/易过期 vs 持久/可查）

## 8.8 Redis 命令小抄（⚠️ 书体例反推 + ✅ redis.io 常识；sorted-sets 页实测 200）

| 目的 | Redis 命令 | SQL / 本册对照 |
| --- | --- | --- |
| 缓存读写 | `SET k v EX 60` / `GET` | `SELECT WHERE pk`（TTL 内建） |
| 计数 | `INCR` / `HINCRBY` | 🔧 组 E `UPDATE SET score=+5` |
| 排行 | `ZREVRANGE` / `ZREVRANK` | 🔧 组 E `ORDER BY … LIMIT` |
| 集合运算 | `SINTER`/`SUNION` | `INTERSECT`/`UNION` |
| 队列 | `LPUSH`/`BRPOP` | （关系库需轮询） |
| 原子事务 | `MULTI/EXEC` + Lua | PG 显式事务（[02](02-PostgreSQL关系锚点.md)） |

## 8.9 持久化、内存与一致性的真实边界（⚠️ 转述，纵深让位专册）

- **RDB vs AOF 的选择**：RDB 是定时全量快照（恢复快、丢数据窗口=上次快照到崩溃）、AOF 是命令日志（`appendfsync everysec` 丢约 1s）；现代默认「混合持久化」= AOF 头 + RDB 体。把 Redis 当**可重建缓存**时，持久化要求可大幅放宽。
- **fork 停顿**：RDB/`BGSAVE` 靠 `fork` 子进程做 COW，大内存实例 fork 会瞬时阻塞主线程——这是「内存上限」之外的另一道隐形墙。
- **复制是异步的**：主先应答、从后追，故障转移可能丢未复制写——**Redis 默认不是「零丢失存储」**；要耐久要么开 AOF+多实例要么承认它是缓存。
- **单线程的利与弊**：命令天然串行→免锁原子（🔧 组 E 的 INCR 语义），但一个 O(N) 大命令（`KEYS`、`SORT`、大 `LRANGE`）会阻塞全站——所以生产禁用 `KEYS`、用 `SCAN` 渐进遍历。

> 这些「运行级」细节盘上已被 Redis 专册群穷举：内部实现看 [../Redis设计与实现.md](../Redis设计与实现.md)、[../Redis5设计与源码分析.md](../Redis5设计与源码分析.md)，实战模式看 [../Redis实战.md](../Redis实战.md)、[../Redis深度历险.md](../Redis深度历险.md)，命令速查看 [../Redis_Cookbook/00-总览与阅读地图.md](../Redis_Cookbook/00-总览与阅读地图.md) 与 [../Learning_Redis/00-总览与阅读地图.md](../Learning_Redis/00-总览与阅读地图.md)。本册只负责把它放回「七库之一」的坐标系。

## 8.10 Redis 作「加速层」与其余六库的组合拳（本册 Day3 的收束）

本书把 Redis 排末章、Day3 专讲联动，是因为 Redis 几乎从不独立当真相库，而是给别的库补延迟：

| 组合 | 谁做真相 | 谁做加速 | 典型手法 |
| --- | --- | --- | --- |
| Redis + PostgreSQL | PG（[02](02-PostgreSQL关系锚点.md)） | Redis | cache-aside 缓存昂贵聚合/join 结果 |
| Redis + MongoDB | Mongo（[04](04-MongoDB文档模型.md)） | Redis | 热点文档/会话/排行进 zset |
| Redis + DynamoDB | Dynamo（[07](07-DynamoDB托管NoSQL.md)） | Redis | 二级查询结果缓存（补 Dynamo 不能 ad-hoc） |
| Redis + 图 | Neo4j（[06](06-Neo4j图数据库.md)） | Redis | 高频推荐结果物化，避免重复遍历 |

> 心智：把 Redis 想成「**一张会自己过期、按 key O(1) 命中、还能算排行/计数的高速便签**」——它不回答「数据从哪来（真相在别的库）」，只回答「这次要不要再算一遍」。
> 🔧 提醒：上表全部为 ⚠️ 架构语义描述；本册唯一一手数字是 🔧 组 E（SQLite zset 类比），不代表任何真实 Redis 命中率/延迟。

## 8.11 一句话对比其它六库

Redis vs 其余：它把「一致性/关系/遍历/检索/海量持久」全部让出，只换一样东西——**极致的按键低延迟与原子结构操作**。理解了这个取舍，就理解了为什么每个库的 Wrap-Up 都建议「拿 Redis 给它当缓存」。

## 核心概念速览（中英对照）

- **数据结构服务器** — data structure server：类型即命令语义。
- **TTL / EXPIRE** — 键级过期，缓存的根能力。
- **string / INCR** — 原子自增，计数/限流原语。
- **hash** — field→value 二级映射，对象局部读写。
- **list / set / zset** — 队列 / 唯一集 / 排序集合（排行）。
- **ZRANK / ZREVRANGE** — 名次 / 按分取前 N（🔧 组 E 类比）。
- **RDB / AOF** — 快照 / 追加日志两种耐久化。
- **MULTI/EXEC / Lua** — 队列事务与服务端原子脚本。
- **replication / Sentinel / Cluster** — 主从 / 故障转移 / 哈希槽分片。
- **cache-aside** — 缓存旁路：Redis 配主库的经典模式。
- **Stream** — 5.0 追加日志类型（书基线后增补 ⚠️）。

## 最新演进与工业实践

- **大版本（⚠️ 转述 + ✅ 文档现状）**：书基线（≈Redis 2.8/3.0）到 2026 已到 **8.x**；官方文档 https://redis.io/docs/latest/ ✅ 200，`zset` 页 https://redis.io/docs/latest/develop/data-types/sorted-sets/ ✅ 200。关键增补：Stream(5.0)、模块系统、client-side caching、Function(7.0)、ACL、以及 hash 字段级 TTL（`HEXPIRE`，7.4+）。
- **License 事件与 Valkey 分叉**：2024 年 Redis 8 之前改用 RSALv2/SSPL 非开源许可，Linux 基金会发起 **Valkey** 兼容分叉（Redis 7.2 谱系延续开源）；GitHub https://github.com/valkey-io/valkey ✅ 实测 200——这是 2018 书完全无法预见的最大生态变动，工业选型须先问许可。
- **能力外扩**：Redis Stack 把 JSON、搜索（RediSearch）、向量（queryable via vectors）并入，逼近「多模内存服务器」；与向量/全文专册的边界模糊化，对照 [../Vector_Databases/00-总览与阅读地图.md](../Vector_Databases/00-总览与阅读地图.md)、[../Elasticsearch_The_Definitive_Guide/00-总览与阅读地图.md](../Elasticsearch_The_Definitive_Guide/00-总览与阅读地图.md)。
- **纵深归位**：持久化/复制/集群/内存逐出的工程细节盘上已有专册群（见本章头部八连链），本册仅给「数据结构 + 缓存联动」的导论视角。
- **取证口径**：目录 ✅ 官方页实抓；命令/集群/命中率运行 ⚠️ 转述（本机无 Redis）；🔧 组 E = SQLite 3.45.3 一手数字且非 Redis 行为。
