# 第 12 章　事务性 Topology 实现

> 原书第 12 章是在第 10 章 at-least-once 之上，进一步追求 **Exactly-once 语义**的
> Storm 式方案——「事务性 Topology」。它先给 **Exact-once 语义解决方案**（分阶段批处理：
> 处理阶段并行、提交阶段强有序），再讲**设计细节**，最后给**事务性 Topology API**。
> 这是 2016 年 Storm 实现 exactly-once 的经典手法，也是全书的「高级可靠性」收尾。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 12.1 Exact-once 语义解决方案 | 事务拓扑：把流分成有序事务批次，处理与提交分离 | Storm 式 exactly-once = 并行处理 + 强序提交 |
| 12.2 设计细节 | 事务 ID、两阶段（processing/commit）、状态提交 | 每个 batch 有唯一 txid，提交串行保证无重叠 |
| 12.3 事务性 Topology API | 用户实现 `ICommitter`/事务 Spout/Bolt | 暴露事务钩子给用户 |
| 12.4 本章小结 | 收束 | — |

## 核心精讲

### 12.1 Storm 事务拓扑的核心思想

原书复刻 Storm 的「事务性 Topology」：把无界流切成**有序的、全局单增的事务批次（batch）**，
每个 batch 带一个 `txid`：

```text
# 教学示意，不参与构建：事务拓扑两阶段(对照 Storm Transactional Topology)
阶段1 processing(并行):  同一 txid 的所有 tuple 被各 Bolt 并行处理, 结果暂存
阶段2 commit(串行):     按 txid 严格递增顺序提交; 只有上一个 txid commit 完才 commit 下一个

保证:
  - 同一 txid 内的计算可重试(at-least-once 兜底, 见第10章)
  - commit 串行 => 不会有两个不同的 txid 同时生效 => 无交叉 => exactly-once(对状态更新而言)
```

> 这是 **Storm 在 Flink 出现前**实现 exactly-once 的办法：用「强有序提交」规避并发写状态
> 导致的重复/错乱。代价是**吞吐受 commit 串行化限制**，且只保证「状态更新 exactly-once」，
> 不保证端到端（sink 仍需幂等）。

### 12.2 txid 与两阶段提交（对照）

原书把事务拆成 processing + commit 两个流水线阶段，commit 阶段全局串行，
确保 `txid=n` 的提交一定在 `txid=n-1` 之后。这与数据库 2PC 有神似，但更简单——
它不为「分布式原子提交」而是为「有序状态落地」。

> 🔧 2026 视角：这种方案已被 **Flink 分布式快照（Chandy-Lamport）** 取代——
> 快照对应用透明、且不强制 commit 串行，吞吐更高。见第 10 章 10.3 的 🔧 补丁。

## 版本演进

- **本书无第二版**；本节写 2016 年口径 → 2026 年视角的变化。
- **12.1 的事务拓扑 → Flink 快照式 exactly-once**：Flink 用周期性全局快照 +
  可重放源（Kafka）实现 exactly-once，**不要求 commit 串行**，应用无感；
  Storm 事务拓扑因吞吐受限已基本退出主流。
- **exactly-once 语义的精化**：2026 年要区分 **处理 exactly-once**（状态）与
> **端到端 exactly-once**（sink 也恰好一次）——后者仍需幂等/事务 sink，
> 本书未做此区分（🔧 补）。
- **Kafka 事务**：`apache/kafka`（33849★）的幂等生产者 + 事务使「at-least-once + 幂等」
  成为常见落地，比事务拓扑更轻（🔧 补）。

## 经典论文与原始文献

| 文献 | 出处 | 贡献 |
| --- | --- | --- |
| Toshniwal et al.《Storm@Twitter》 | SIGMOD 2014 | 事务拓扑/Transactional Topology 的蓝本（12.1–12.3） |
| Chandy, Lamport《Distributed Snapshots》 | ACM TOCS 1985 | 🔧 现代 exactly-once 快照理论（取代事务拓扑） |
| Carbone et al.《Apache Flink》 | IEEE Computer 2015 | Flink 快照式 exactly-once（12.1 的现代答案） |
| Gray, Lamport 等相关事务文献 | — | 2PC/提交串行化的背景（12.2 对照） |

## 近年研究与工业界开源实践（2015–2026）

- **Flink 端到端 exactly-once**：`apache/flink`（26367★）配合 Kafka/Pulsar 事务 sink，
  实现端到端恰好一次，无需 Storm 式事务拓扑。
- **Kafka 事务/幂等**：`apache/kafka`（33849★）使廉价 exactly-once 落地普及。
- **Storm 事务拓扑已成历史**：`apache/storm`（6695★）虽支持，但实践中极少使用，
  社区重心早转向 Flink。

## 常见误区与本书需修正之处

| # | 误区 | 事实 | 书目 |
| --- | --- | --- | --- |
| 1 | 「事务拓扑 = 真正端到端 exactly-once」 | 只保证状态更新 exactly-once；sink 仍需幂等 | 12.1/12.3 |
| 2 | 「exactly-once 一定慢」 | Flink 快照式可并行提交；Storm 事务拓扑因 commit 串行才慢 | 12.1 |
| 3 | 🔧 应补「Flink 分布式快照替代事务拓扑」 | 现代主流，对应用透明、吞吐更高 | 12.1 |
| 4 | 🔧 应补「端到端 vs 处理 exactly-once 区分」 | 二者不同，端到端还需幂等 sink | 12.1 |
| 5 | 🔧 应补「Kafka 事务/幂等落地」 | 廉价路线，弱化事务拓扑必要性 | 12.2 |

## 与其他章 / 其他书的联系

- **本书内**：12.1 建立在 [10-可靠消息处理.md](10-可靠消息处理.md) 的 at-least-once 之上；
  12.3 的 API 扩展 [06-](06-实时处理系统编程接口设计.md)/[09-](09-实时处理系统编程接口实现.md) 接口；
  commit 串行化与 [08-](08-管理服务设计与实现.md) President 调度相关。
- [../设计数据密集型应用/11-流处理.md](../设计数据密集型应用/11-流处理.md)（若存在）——
  DDIA 对 exactly-once、Flink 快照、Kafka 幂等的权威讲法（**必配**）。
- [10-可靠消息处理.md](10-可靠消息处理.md) ——acker 与事务拓扑的承接关系。
