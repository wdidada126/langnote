# 第 13 章 JVM 中的并发处理：Clojure、Groovy(GPars)、Scala

> 本书独有章：跳出 Java，看 JVM 上三门语言的并发模型——Clojure 的不可变+STM、Groovy 的 GPars（Agent/Dataflow/Parallel）、Scala 的 Actor（Akka）+ Future。与《之美》concepts/并发模型跨语言对比 互文。

## 一、本章地图

| 语言 | 并发模型 |
| --- | --- |
| Clojure | 持久化不可变数据结构 + STM（Ref）+ Agent + core.async（CSP） |
| Groovy(GPars) | Agent / Dataflow / Parallel Collections / PGroup |
| Scala | Actor（Akka）/ Future/Promise / ScalaSTM |

## 二、核心精讲

### 2.1 Clojure 的不可变优先
- 默认持久化不可变集合（结构共享，写时复制但 O(log n) 共享前缀）→ 天然线程安全（🔧 可变状态用 `Ref`+STM 事务，或 `Atom`（无协调 CAS）、`Agent`（串行邮件处理））。
- `core.async` 提供 Go 式 CSP 通道（`>!`/`<!!`），与 Java 的 `BlockingQueue`+协程思路同源。

### 2.2 Scala / Akka Actor
- Actor 模型：状态私有、消息驱动、无共享（🔧 见葛一鸣 7 章、之美 concepts/并发模型跨语言对比）；`Future` 是 Akka 的异步句柄。
- GPars（Groovy）：Agent/Dataflow 变量 + Parallel Collections，把并行 map/reduce 加到 Groovy。

## 三、版本演进 / 论文 / 前沿

- 论文：Hewitt Actor（IJCAI'73）；Shapiro STM 综述；Baker-Ponder Futures（1977）；Go CSP（Hoare 1978，core.async 借鉴）。
- 工业界：Akka 13.3k / clojure 10.5k / scala 14.5k / kotlinx 13.8k（Kotlin 在 JVM 上提供协程，竞争 Actor）。
- 开源 stars（2026-09）：JDK 23.4k。

## 四、常见误区 / 本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "JVM 并发=Java 一套" | Clojure/Scala 模型更先进 |
| 2 | "STM 万能" | 长事务冲突退避，慎用 |
| 3 | "Actor 替代一切" | 简单并行用并行集合/虚拟线程 |
| 4 | "GPars 还在主流" | Groovy 并发用 kotlinx 协程替代 |
