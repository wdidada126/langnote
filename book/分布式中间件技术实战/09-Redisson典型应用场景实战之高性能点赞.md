# 第 9 章　Redisson 典型应用场景实战之高性能点赞

> 原书第 9 章是**Redisson 的落地项目章**：用第 8 章的 `RAtomicLong`、`RMap`、`RScoredSortedSet`（ZSet）
> 等组件，做一个「高性能点赞 + 排行榜」业务。这是把「分布式计数器 / 有序集合」直接服务高并发读写的范例，
> 与第 4 章抢红包（Redis 原生）形成「裸 Redis vs Redisson 封装」的对照。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 9.1 整体业务流程介绍与分析 | 点赞/取消点赞、排行榜查询的需求与并发点 | 读多写少 + 计数高频 |
| 9.2 「点赞与取消点赞」操作模块 | RAtomicLong 计数 + RMap/Set 记录谁点过 | 防重复点赞 + 原子计数 |
| 9.3 「排行榜」业务模块 | RScoredSortedSet（ZSet）按分数排序 | 实时榜、TopN 查询 |
| 9.4 总结 | 收束 Redisson 项目章 | 全书实战收口，第 10 章总结 |

## 核心精讲

（以下为教学性梳理，代码均**教学示意，不参与构建**。）

### 9.1 业务分析

- **点赞**：用户对任意目标（文章/视频）点赞，需①原子自增计数 ②记录「该用户已点」防重复 ③取消时回退。
- **排行榜**：按「点赞数 / 热度」排名，需支持实时 TopN、按分数排序——正是 ZSet 的强项。

### 9.2 点赞与取消点赞（教学示意）

```java
// 教学示意，不参与构建：用 Redisson 做点赞
RMap<String, Boolean> liked = redissonClient.getMap("like:users:" + targetId);
if (liked.putIfAbsent(userId, true) == null) {        // 防重复点赞（原子）
    redissonClient.getAtomicLong("like:count:" + targetId).incrementAndGet();
}

// 取消点赞
if (liked.remove(userId) != null) {
    redissonClient.getAtomicLong("like:count:" + targetId).decrementAndGet();
}
```

- 这里 `RMap.putIfAbsent` 是**原子的**，避免了「查是否已点 → 再点」的竞态；
  计数用 `RAtomicLong` 跨进程一致。

### 9.3 排行榜（教学示意）

```java
// 教学示意，不参与构建：ZSet 做实时榜
RScoredSortedSet<String> board = redissonClient.getScoredSortedSet("hot:board");
board.addScore(targetId, 1.0);                  // 热度+1
Collection<String> top10 = board.entryRangeReversed(0, 9);  // Top10（分数降序）
```

- **ZSet（有序集合）**用「分数」排序，天然支持 `range`/`revrange` 取 TopN、按排名查；
  比关系型 `ORDER BY score DESC LIMIT` 在高频更新下更稳。

### 9.4 总结

这一章把第 8 章的 `RAtomicLong`/`RMap`/`RScoredSortedSet` 串成一个完整高并发业务，
体现了 Redisson「像写本地 Java 代码一样写分布式状态」的设计主张。

## 版本演进

- **本书无第二版**；本节写 2020 年口径 → 2026 年视角。
- **🔧 排行榜的存储选型扩展**：2026 年高并发排行榜也可用 **Redis 原生 ZSet**（本书第 3 章已讲）、
  或专门的**实时分析/OLAP**、或 **Redis 7 + RedisSearch**；Redisson 只是 Java 侧封装之一。
- **🔧 防刷/限流需要叠加**：点赞业务若被刷，需配合限流（Sentinel/Resilience4j）与风控，本书未覆盖。
- **🔧 持久化与最终一致**：Redis/Redisson 的计数在内存，需考虑与 DB 的异步对账（防丢/防偏），
  呼应第 4 章「异步落库」思路。

## 经典论文与原始文献

| 文献 | 出处 | 贡献 |
| --- | --- | --- |
| Redisson 官方文档（RAtomicLong / RMap / RScoredSortedSet） | redisson.org | 本章组件的权威出处 |
| Redis 官方文档：INCR / ZADD / ZRANGE | redis.io | Redisson 底层命令底座（第 3 章同源） |

> 第 9 章是工程实战章，原书不引论文；上表补官方文档出处。

## 近年研究与工业界开源实践（2015–2026）

- **实测 star（2026-09，`gh api` 实测）**：

| 项目 | 定位 | star |
| --- | --- | --- |
| `redisson/redisson` | 本章全部组件的本体 | 24403 |
| `redis/redis` | Redisson 存储底座（ZSet 等） | 76498 |
| `spring-projects/spring-boot` | 项目基座 | 81511 |

- **「点赞/排行榜」是 Redis 最经典的读多写少场景**：工业界几乎都建立在 Redis ZSet / 原子计数之上，
  Redisson 只是 Java 侧的友好封装；与本书第 3 章「ZSet 做排行榜」完全同构。
- **实时榜的进阶**：2026 年大规模榜常叠加「本地缓存 + 定时刷榜 + 分片 ZSet」，避免单 key 热点的写瓶颈。

## 常见误区与本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「点赞计数只存 Redis 就够」 | 需与 DB 异步对账，防 Redis 丢数据导致计数偏差 |
| 2 | 「先查是否点过再决定加」 | 两步非原子会重复计数；用 `putIfAbsent` 原子判定 |
| 3 | 「排行榜用 MySQL ORDER BY」 | 高频更新下 DB 排序扛不住；用 ZSet |
| 4 | 「取消点赞直接 DECREMENT」 | 没点过就取消会变成负计数；必须先判已点 |
| 5 | 🔧 本书未叠加限流/防刷 | 点赞业务需 Sentinel/Resilience4j + 风控，本书未覆盖 |
| 6 | 🔧 本书未提与 DB 对账 | 2026 年内存计数须有持久化兜底与对账 |

## 与其他章 / 其他书的联系

- **本书内**：
  - 9.2 计数/RMap → [08-综合中间件Redisson.md](08-综合中间件Redisson.md)（RAtomicLong/RMap）；
  - 9.3 排行榜 ZSet → [03-缓存中间件Redis.md](03-缓存中间件Redis.md)（3.3 有序集合）；
  - 9.2 并发计数思想 → [04-Redis典型应用场景实战之抢红包系统.md](04-Redis典型应用场景实战之抢红包系统.md)（高并发读写）。
- [../Redis深度历险.md](../Redis深度历险.md)——ZSet 排行榜、计数器的系统讲法。
- [../Redis设计与实现.md](../Redis设计与实现.md)——ZSet 底层跳表结构，理解 9.3 排序复杂度。
- [../亿级流量网站架构核心技术.md](../亿级流量网站架构核心技术.md)——高并发计数/榜的架构延伸。
