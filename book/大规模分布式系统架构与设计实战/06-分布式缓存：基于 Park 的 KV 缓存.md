# 第 6 章　分布式缓存：基于 Park 的 KV 缓存

> 原书的分布式缓存基于 Park 暴露 KV 能力，单机侧用 `LinkedHashMap`
> （`removeEldestEntry` 做 LRU）实现，远程调用走 RMI。
> 仓库笔记原文**重点炮轰**了这一章：HashMap/LinkedHashMap **不是线程安全的**，
> 高并发扩容会导致死循环、CPU 100%；而 `ConcurrentHashMap` 虽线程安全却**没有 LRU**，
> 作者是否解决了「线程安全 + LRU」这个组合难题，笔记原文表示没看到 sync、存疑。
> 这是全书被批评得最具体、最技术化的一处。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 6.1 分布式缓存的形态 | KV + LRU + 远程访问 | fourinone 缓存类似 memcached（仅 KV） |
| 6.2 单机 LRU 实现 | LinkedHashMap.removeEldestEntry | 非线程安全，是隐患根源 |
| 6.3 并发安全的坑 | HashMap 扩容死循环 | 笔记原文重点质疑点 |
| 6.4 远程暴露 | 通过 RMI 把缓存变分布式 | 继承 RMI 的 BIO 性能天花板 |
| 6.5 与 memcached/Redis 对照 | 能力差距 | 14285 / 76498★ vs 85★ |

## 核心精讲

（以下为教学性梳理，伪代码/示意均**教学示意，不参与构建**。）

### 6.2 LinkedHashMap 做 LRU 的写法（教学示意）

```java
// 教学示意，不参与构建：书中缓存的单机雏形
class LruCache<K,V> extends LinkedHashMap<K,V> {
    private final int max;
    public LruCache(int max) { super(max, 0.75f, true); this.max = max; }
    @Override
    protected boolean removeEldestEntry(Map.Entry<K,V> e) {
        return size() > max;   // 超过容量就淘汰最久未访问
    }
}
```

- `accessOrder=true` 让 `get` 也把元素移到队尾，`removeEldestEntry` 在 `put` 时触发淘汰。
- **但这套是单线程友好的**。`LinkedHashMap` 没有任何同步；多线程下：

### 6.3 并发扩容死循环（笔记原文核心质疑，教学示意）

```text
# 教学示意，不参与构建：HashMap 并发扩容的经典死循环
HashMap 在 put 触发 resize 时，会重建哈希桶并把旧桶元素迁移到新桶。
若两个线程同时 resize，链表迁移过程中可能形成「环」，
后续 get 走到环上 -> 无限循环 -> CPU 100%。
（酷壳/Coolshell 有经典图解；笔记原文明确点名此坑）
```
- 解决路径只有两条：
  1. 加锁（`synchronized` / `ReentrantLock`）——简单但有吞吐代价；
  2. 用 `ConcurrentHashMap`——线程安全，但**原生不提供 LRU**，
     要 LRU 得在其上自行维护访问顺序（如加软引用/定时清理/外部 LRU 索引），
     「淘宝的人这样做过」（笔记原文），并非开箱即用。
- **关键质疑**：fourinone 既没显式 `sync`，也没用带 LRU 的并发结构，
  「作者是怎么解决的，我没有看到 sync」（笔记原文原话）。**未能核实，存疑**。

### 6.4 远程化走 RMI 的代价

- 缓存操作经 RMI 暴露为远程调用：RMI 内部 BIO（每请求一线程）+ JDK 原生序列化。
- 缓存是高并发、小对象、追求极低延迟的场景，**BIO + 原生序列化恰恰最不合适**；
  对比 memcached（C + libevent/epoll）、Redis（C + 自研事件循环），差距明显。

## 版本演进

- 本书无第二版记录。
- **2013 年口径**：memcached 成熟，Redis 2.x 刚流行；「Java 里做个 LRU 缓存」是常见教学题材。
- **2026 年视角**：缓存默认答案是 **Redis（76498★）/ memcached（14285★）**；
  Java 侧则多用 Caffeine（高性能本地缓存，带 W-TinyLFU 淘汰）而非手写 LinkedHashMap。
- 🔧 **必须补入**：现代缓存淘汰已从 LRU 演进到 **TinyLFU / W-TinyLFU**（Caffeine，2016 前后）；
  「线程安全 + 高效淘汰」早已是成熟库能力，无需在 HashMap 上踩坑。

## 经典论文与原始文献

| 文献 | 出处 | 贡献 |
| --- | --- | --- |
| Fitzpatrick《distributed caching with memcached》(PPT/论文) | 2004 | memcached 设计与使用 |
| Redis 设计与实现（Antirez 博客 / 文档） | — | Redis 单线程事件循环范式 |
| 本书引用情况 | — | **未给出明确原始文献**；LRU/并发实现未引权威资料，存疑 |

## 近年研究与工业界开源实践（2015–2026）

- **Redis** `redis/redis` **76498★**（2026-09-27 实测）、
  **memcached** `memcached/memcached` **14285★**：缓存事实标准。
- **Caffeine** `ben-manes/caffeine`（Java 高性能本地缓存，W-TinyLFU）是 Java 侧现代答案，
  star 量级数万，远胜手写 LinkedHashMap 方案。
- **fourinone** `fourinone/fourinone` **85★**：其缓存模块的采用近乎可忽略，
  且与「未完全开源」争议叠加，代码是否完整开放亦存疑。

## 常见误区与本书需修正之处

| # | 误区 | 事实 | 书目 |
| --- | --- | --- | --- |
| 1 | 「LinkedHashMap 就能做并发缓存」 | 非线程安全，并发扩容死循环 → CPU 100% | 笔记原文 |
| 2 | 「ConcurrentHashMap 直接替代」 | 它线程安全但无 LRU，需自行补齐淘汰逻辑 | 笔记原文 |
| 3 | 「RMI 暴露缓存够快」 | RMI 是 BIO + 原生序列化，恰是缓存最忌的 | 🔧 本书 |
| 4 | 线程安全+LRU 如何兼得未讲清 | 笔记原文称未看到 sync，方案存疑 | 笔记原文 |
| 5 | 「fourinone 缓存可比 memcached」 | 采用量/性能/生态差数量级（85 vs 14285/76498） | 🔧 本书 |

## 与其他章 / 其他书的联系

- **本书内**：6.1 缓存依托 ← [03-分布式协调与锁](03-分布式协调与锁：Park 协调服务.md)（Park 提供 KV/注册）；
  远程调用与 [01-概述](01-概述与四合一定位.md) 的 RMI 口径一致。
- [../深入分布式缓存/00-总览与阅读地图.md](../深入分布式缓存/00-总览与阅读地图.md)
  ——仓库另有的缓存专著，Redis/Tair 等主流实现系统讲法（若目录存在则对读）。
- [../大规模分布式存储系统/05-分布式键值系统.md](../大规模分布式存储系统/05-分布式键值系统.md)
  ——Dynamo / Tair 的分布式 KV 范式，对照本章简化版。
- [../设计数据密集型应用/05-复制.md](../设计数据密集型应用/05-复制.md)
  ——缓存与副本/一致性的现代视角。
