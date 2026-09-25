# 第 7 章 使用Akka构建高并发程序（原书）

> **本书独有"Actor 模型实战"章**：Akka 的 Actor、消息传递、邮箱、路由、持久化、集群。与《之美》`concepts/并发模型跨语言对比.md` 互补（本书给 Java 生态的 Akka 落地）。对比"共享内存 + 锁"模型，Actor 用"消息 + 邮箱"避免共享状态。

## 一、本章地图

| 主题 | 关键 |
| --- | --- |
| Actor 模型 | 封装状态 + 收消息改状态；无共享内存 → 无竞态 |
| 消息传递 | 不可变消息；异步；邮箱排队 |
| 路由 | RoundRobin/Random/Broadcast 分发 |
| 持久化/集群 | 事件溯源、位置透明 |
| 对比锁模型 | Actor 天然避免死锁（但不避免消息饥饿/邮箱溢出） |

## 二、核心精讲

### 2.1 Actor 模型（与《之美》跨语言对比一致）
- 每个 Actor 有私有状态 + 邮箱；只通过**不可变消息**交互 → 无共享可变状态 → 无数据竞争/死锁（经典死锁在 Actor 模型下不存在）。
- 对比：共享内存模型要自己管锁/可见性；Actor 把"并发安全"交给框架。

### 2.2 Akka 落地
- `ActorSystem`/`ActorRef`/`receive`；消息用 `case class`/record（不可变）。
- 路由：把消息分发给 Worker 池（RoundRobin 等）→ 类似 Master-Worker 模式但框架托管。
- 持久化：事件溯源（Event Sourcing）+ 快照；集群：位置透明（Actor 可跨节点）。

### 2.3 注意点
- 邮箱溢出：消息生产快于消费 → 内存涨；需背压（Akka Streams）。
- 阻塞 Actor：Actor 内做阻塞 I/O 会卡住该 Actor 的邮箱 → 用 `pipeTo`/异步或独立调度器。
- 消息顺序：同一 Actor 按顺序处理自己的消息（保序），跨 Actor 无序。

### 2.4 🔧 现代对照
- 虚拟线程（JEP 444）让"轻量任务"在 JVM 原生可行 → Actor 的"轻量实体"优势被部分削弱；但 Actor 的"隔离状态 + 消息"仍是结构化并发之外的重要范式。
- Kotlin `kotlinx.actor`（已废弃，转向 `Flow`/`Channel`）；Rust `actix`；Erlang/OTP（Actor 祖宗）。

## 三、版本演进

- **Akka 2.x**（2012+）：JVM Actor 事实标准。**JDK 21**：虚拟线程冲击"为何需要 Actor"叙事。
- Erlang/OTP（1986+）：Actor 模型工业源头（WhatsApp 等）。

## 四、经典论文 / 原始文献

- **Hewitt, Bishop, Steiger, "A Universal Modular ACTOR Formalism" (IJCAI 1973)**——Actor 模型起源。
- **Armstrong, "Making Reliable Distributed Systems in the Presence of Software Errors" (PhD 2003)**——Erlang/OTP（Akka 灵感）。
- **JEP 444 (Virtual Threads)**——轻量实体的现代对照。

## 五、工业界前沿

| 项目 | Stars | 关联 |
| --- | --- | --- |
| **akka/akka** | 13.3k | JVM Actor 框架 |
| **ReactiveX/RxJava** | 48k | 响应式（消息流） |
| **Kotlin/kotlinx.coroutines** | 13.8k | `Channel`/`Actor`（协程版） |
| **erlang/otp** | 12.3k | Actor 模型工业祖宗 |
| **openjdk/jdk** | 23.4k | 虚拟线程（轻量实体原生） |

## 六、常见误区 / 本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "Actor 不会死锁所以绝对安全" | 邮箱溢出/消息饥饿/阻塞 Actor 仍会卡 |
| 2 | "Actor 内可随意阻塞" | 卡邮箱；用异步/独立调度器 |
| 3 | "Actor 一定比锁快" | 消息传递有开销；小任务锁更省 |
| 4 | "新项目必上 Akka" | 虚拟线程 + 结构化并发已覆盖多数轻量并发 |
