# 第 3 章　缓存中间件 Redis

> 原书第 3 章是**第 2 篇实战的第一章，也是全书最重要的「组件理论章」之一**：
> 从 Redis 是什么、典型场景讲起，落到「Spring Boot 怎么整合 Redis」「RedisTemplate/StringRedisTemplate 怎么用」，
> 再逐个数据结构实战，最后用一个**缓存穿透**案例收尾。这一章奠定了后续第 4、7、8、9 章的缓存与锁基础。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 3.1 Redis 概述与典型应用场景 | 内存 KV、高性能、支持多种结构；缓存/计数器/排行榜/会话 | Redis 定位是「内存中的 Swiss Army Knife」 |
| 3.2.1 快速安装 Redis | Linux 下编译/包管理安装 | 2026 年更推荐 Docker 拉镜像 |
| 3.2.2 Windows 下使用 Redis | 本书教学路径（Windows 版 Redis） | 仅适合学习；生产不用 Windows 版 |
| 3.2.3 Spring Boot 整合 Redis | 引入 starter、配 `spring.redis.*` | 自动装配出 `RedisTemplate`/`StringRedisTemplate` |
| 3.2.4 自定义注入 Bean 组件配置 | 自定义 `RedisTemplate` 序列化（JSON） | 默认 JDK 序列化可读性差，生产用 JSON |
| 3.2.5 RedisTemplate 实战 | opsForValue/Hash/List/Set/ZSet 等 API | Spring 对 Redis 五种结构的统一封装 |
| 3.2.6 StringRedisTemplate 实战 | 专治字符串、默认 String 序列化 | 简单 KV / 分布式锁计数常用 |
| 3.3 常见数据结构实战 | 字符串/列表/集合/有序集合/哈希/Key 失效 | 每种结构对应一类业务语义 |
| 3.4 Redis 实战场景之缓存穿透 | 查不存在的 key 打穿缓存压到 DB | 布隆过滤器 / 空值缓存 / 校验拦截 |
| 3.5 总结 | 收束 Redis 理论章 | 下一章用抢红包把知识落地 |

## 核心精讲

（以下为教学性梳理，代码均**教学示意，不参与构建**。）

### 3.1 Redis 是什么、能干嘛

- **定位**：基于内存、支持持久化的 KV 数据库；单线程命令执行（2026 年 IO 多线程化，见版本演进），
  性能极高（十万级 QPS）。
- **典型场景**：缓存热点数据、分布式会话、计数器（点赞/库存）、排行榜（ZSet）、
  限流、消息队列（List/Stream）、分布式锁（第 7、8 章）。

### 3.2 Spring Boot 整合 Redis（教学示意）

```yaml
# 教学示意，不参与构建：application.yml
spring:
  redis:
    host: localhost
    port: 6379
    password:
    database: 0
    lettuce:           # 2026 年默认客户端是 Lettuce（Netty 事件循环）
      pool:
        max-active: 8
```

```java
// 教学示意，不参与构建：自定义 RedisTemplate（JSON 序列化，避免 JDK 二进制可读性差）
@Configuration
public class RedisConfig {
    @Bean
    public RedisTemplate<String, Object> redisTemplate(RedisConnectionFactory factory) {
        RedisTemplate<String, Object> t = new RedisTemplate<>();
        t.setConnectionFactory(factory);
        t.setKeySerializer(new StringRedisSerializer());
        t.setValueSerializer(new GenericJackson2JsonRedisSerializer());
        return t;
    }
}
```

- **RedisTemplate vs StringRedisTemplate**：后者 key/value 都按 String 序列化，适合纯字符串与简单计数；
  前者支持对象（需配序列化器）。第 9 章排行榜、第 7 章锁都会用到。

### 3.3 数据结构与业务语义

| 结构 | Redis 命令族（opsFor*） | 典型业务 |
| --- | --- | --- |
| 字符串 String | `opsForValue()` | 缓存对象、计数器 `incr` |
| 列表 List | `opsForList()` | 最新列表、简单队列 |
| 集合 Set | `opsForSet()` | 去重、共同好友 |
| 有序集合 ZSet | `opsForZSet()` | 排行榜（第 9 章）、延迟队列分值 |
| 哈希 Hash | `opsForHash()` | 对象字段级缓存 |
| Key 失效 | `expire` / `setex` | 缓存 TTL、防雪崩 |

### 3.4 缓存穿透（本章实战重点）

- **问题**：请求一个**数据库中也不存在**的 key，缓存永远不命中，请求每次都打到 DB，
  恶意刷不存在的 id 就能压垮数据库。
- **解决方案（书中给出并实战）**：

```text
# 教学示意，不参与构建：缓存穿透三板斧
1) 参数校验/拦截：非法 id 直接拒绝（入口层）
2) 缓存空值：查不到也写 "" 并加短 TTL，避免重复打 DB
3) 布隆过滤器：在缓存前加一层 BF，判定"一定不存在"的请求直接返回
   （注意 BF 有误判：说存在可能不存在，说不存在一定不存在）
```

> 缓存穿透 / 击穿（热点 key 失效）/ 雪崩（大量 key 同时失效）是三兄弟，本书 3.4 主要讲穿透，
> 击穿与雪崩在「其他典型问题介绍」里带过——这些在 `../Redis深度历险.md` 有更系统展开。

## 版本演进

- **本书基于 Redis 5**；到 2026 年主线已到 **Redis 7.x**。
- **🔧 Redis 6 引入多线程网络 IO（IO threads）**：命令执行仍单线程，但读/写 socket 可多线程，
  高并发下吞吐显著提升——本书「单线程」表述需补这一笔。
- **🔧 Redis 6 引入 ACL**：细粒度用户权限；本书默认无密码/简单密码的本地教学需补。
- **🔧 Redis 7 的 Functions（替代 Lua 脚本管理）、RedisJSON / RedisSearch / RedisBloom 模块**：
  本书讲的「布隆过滤器」在 2026 年多直接用 RedisBloom 模块或外部 Guava/BF，而非手写 bit 数组。
- **客户端**：本书时期 Jedis 仍常见；2026 年 Spring Boot 默认 **Lettuce**（基于 Netty、线程安全、支持响应式）。
- **集群**：本书多讲单机/主从；2026 年 Redis Cluster（16384 槽）已是标准高可用形态。

## 经典论文与原始文献

| 文献 | 出处 | 贡献 |
| --- | --- | --- |
| Redis 官方文档（redis.io/documentation） | redis.io | 数据结构、命令、持久化、集群的权威出处 |
| Antirez（Salvatore Sanfilippo）Redis 设计与实现博客/源码 | GitHub redis/redis | Redis 本体与实现哲学 |
| Bloom《Space/Time Trade-offs in Hash Coding with Allowable Errors》 | CACM 1970 | 布隆过滤器（本章 3.4 缓存穿透方案之一） |

> 第 3 章是工程实战章，原书不引论文；上表补「缓存穿透布隆过滤器」与官方文档出处。
> 想系统学 Redis 原理见 `../Redis设计与实现.md`、`../深入理解Redis.md`。

## 近年研究与工业界开源实践（2015–2026）

- **实测 star（2026-09，`gh api` 实测）**：

| 项目 | 定位 | star |
| --- | --- | --- |
| `redis/redis` | Redis 本体（C 实现） | 76498 |
| `redisson/redisson` | 基于 Redis 的 Java 分布式对象/锁框架（第 8 章） | 24403 |
| `redis/jedis` | 老牌 Java Redis 客户端 | 12372 |
| `lettuce-io/lettuce` | Spring Boot 3 默认 Java 客户端（Netty） | 5779 |
| `spring-projects/spring-data-redis` | Spring 对 Redis 的抽象层 | 1872 |

- **Redis 从「缓存」扩张为「多功能数据平台」**：2026 年 Redis 生态含 JSON、Search、Bloom、TimeSeries、
  Stream（MQ）等模块；本书 2020 年仅把它当缓存 + 简单结构。
- **客户端格局**：Spring Boot 默认 Lettuce（异步/响应式友好），Jedis 仍活跃（同步、简单易用）。
- **云托管成熟**：云厂商托管 Redis（含集群、自动故障转移）已替代大量自运维，呼应 00-实验工具链。

## 常见误区与本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「Redis 是单线程，所以并发差」 | 命令执行单线程避免锁竞争；Redis 6+ IO 多线程、Cluster 分片横向扩展 |
| 2 | 「缓存穿透=缓存击穿=缓存雪崩」 | 三者成因不同：不存在 key / 热点 key 失效 / 大量 key 同时失效 |
| 3 | 「缓存永不过期最安全」 | 不过期会内存爆 + 数据 stale；应设 TTL + 主动更新 |
| 4 | 「RedisTemplate 默认序列化够用」 | 默认 JDK 序列化存二进制，可读差、体积大；生产用 JSON |
| 5 | 🔧 本书基于 Redis 5 | 2026 应提 Redis 7 的 IO 多线程、ACL、Functions、模块生态 |
| 6 | 🔧 本书布隆过滤器手写 bit | 2026 多用 RedisBloom 模块或 Guava BF，减少手搓 |
| 7 | 🔧 本书讲 Windows 版 Redis | 生产不用 Windows 构建；2026 用 Docker/云托管 |

## 与其他章 / 其他书的联系

- **本书内**：
  - 3.2 整合 → [02-搭建微服务项目.md](02-搭建微服务项目.md)（Spring Boot 基座）；
  - 3.3 ZSet → [09-Redisson典型应用场景实战之高性能点赞.md](09-Redisson典型应用场景实战之高性能点赞.md)（排行榜）；
  - 3.4 缓存穿透 + 3.2.6 → [04-Redis典型应用场景实战之抢红包系统.md](04-Redis典型应用场景实战之抢红包系统.md)（高并发读写）；
  - 3.2.6 StringRedisTemplate → [07-分布式锁实战.md](07-分布式锁实战.md)（基于 Redis 的锁 SET NX）。
- [../Redis设计与实现.md](../Redis设计与实现.md)、[../深入理解Redis.md](../深入理解Redis.md)
  ——Redis 线程模型、持久化、集群原理，补本章「只讲用法」的部分。
- [../Redis深度历险.md](../Redis深度历险.md)——缓存穿透/击穿/雪崩、分布式锁、布隆过滤器系统讲法。
- [../深入分布式缓存.md](../深入分布式缓存.md)——缓存架构与一致性，2026 延伸。
