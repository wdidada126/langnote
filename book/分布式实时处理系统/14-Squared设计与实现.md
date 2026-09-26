# 第 14 章　Squared 设计与实现——实现高级抽象元语

> 原书第 14 章在 Hurricane 基础算子（Spout/Bolt）之上，复刻 Storm 的 **Trident**
> 高级抽象，做出 **Squared**：把「一系列 tuple 操作」封装成更高层的「批/状态/聚合」元语，
> 让用户在更高层级写流处理逻辑（类似微批 + 状态 + 聚合），而不必手搓每个 Bolt。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 14.1 Storm Trident 介绍 | Trident 的高级抽象：状态/聚合/批 | Trident = Storm 上的微批高层 API |
| 14.2 Squared 实现 | 在 Hurricane 上实现类似 Trident 的批/状态/聚合 | Squared 是 Hurricane 的「Trident」 |
| 14.3 本章小结 | 收束 | — |

## 核心精讲

### 14.1 Trident 解决了什么

原书先介绍 Storm Trident：在「逐 tuple 的 Spout/Bolt」之上提供
**批（batch，称为 transaction/tuple 小批）、状态（state，持久化聚合）、聚合（aggregation）、
流式分组」**等高层原语，使用户写「计数/去重/窗口聚合」时不必手动维护状态与幂等。

```text
# 教学示意，不参与构建：Trident / Squared 抽象层级
底层(第6-9章):  Spout -> Bolt -> Bolt   (逐 tuple, 手搓状态)
高层(本章):      spout.batch().each().groupBy().aggregate(state)  (批 + 状态 + 聚合)
```

> 这本质上是 2016 年「在 Storm 上补微批/状态」的尝试。🔧 2026 视角：Flink 从一开始就把
> 状态/窗口/聚合作为**内建原语**，比在 Storm 上外挂 Trident 自然得多。

### 14.2 Squared 的实现要点

原书让 Squared 复用 Hurricane 的 Task/Collector/acker，把「高层操作」翻译回底层 tuple 流：
- **批**：把若干 tuple 攒成一个小批次再交给算子；
- **状态**：在 Bolt 内接入持久化存储（呼应第 1 章 1.5 的存储系统），保证聚合可恢复；
- **聚合**：基于批做 sum/count 等，借第 12 章事务保证 exactly-once 落地。

> 这与 [12-事务性Topology实现.md](12-事务性Topology实现.md) 的 exactly-once 直接挂钩——
> Squared 的状态聚合需要事务语义才正确。

## 版本演进

- **本书无第二版**；本节写 2016 年口径 → 2026 年视角的变化。
- **Trident 范式 → Flink 原生状态/窗口**：Trident 是「在流框架上补批」的补丁；
> Flink 把 **keyed state + 窗口 + 事件时间** 作为引擎原生能力，表达力与性能都更好。
- **流批一体**：2026 年「批=有界流」让 Squared 这种「单独微批层」失去必要。

## 经典论文与原始文献

| 文献 | 出处 | 贡献 |
| --- | --- | --- |
| （Storm Trident 官方文档 / 设计笔记） | 2012–2013（版本较多） | 14.1 Trident 蓝本（未以正式论文发表，注明） |
| Carbone et al.《Apache Flink》 | IEEE Computer 2015 | 内建状态/窗口的现代替代（14.2 的演进方向） |
| Akidau et al.《The Dataflow Model》 | VLDB 2015 | 窗口/聚合/状态的统一模型 |

## 近年研究与工业界开源实践（2015–2026）

- **Flink 原生状态与窗口**：`apache/flink`（26367★）的 `keyBy().window().aggregate()`
  直接取代 Squared/Trident 的「外挂微批 + 状态」。
- **Kafka Streams DSL**：`apache/kafka`（33849★）的 `KTable`/聚合同样内建状态。
- **Beam**：把窗口/触发/累加模式标准化，跨引擎可用。

## 常见误区与本书需修正之处

| # | 误区 | 事实 | 书目 |
| --- | --- | --- | --- |
| 1 | 「Trident/Squared 是高性能必选」 | 它是在流框架上补微批，有额外开销；Flink 原生更优 | 14.1 |
| 2 | 🔧 应补「Flink 原生状态/窗口」 | 现代框架内建，无需外挂高层层 | 14.2 |
| 3 | 🔧 应补「流批一体淘汰微批层」 | 批=有界流，Squared 的独立微批不再必要 | 14.1 |
| 4 | 「Squared 状态可随意存内存」 | 状态需持久化+事务(第12章)才能容错 | 14.2 |

## 与其他章 / 其他书的联系

- **本书内**：14.2 建立在 [06–09 章](06-实时处理系统编程接口设计.md) 的底层算子之上；
  14.2 的状态聚合依赖 [12-事务性Topology实现.md](12-事务性Topology实现.md) 的 exactly-once；
  存储选型呼应 [01-分布式计算概述.md](01-分布式计算概述.md) 1.5。
- [05-分布式实时处理系统.md](05-分布式实时处理系统.md) 5.2——Storm 全景，Trident 是其高级层。
- [../设计数据密集型应用/11-流处理.md](../设计数据密集型应用/11-流处理.md)（若存在）——窗口/聚合/状态的现代讲法。
