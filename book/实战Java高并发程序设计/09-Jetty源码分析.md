# 第 9 章 多线程优化示例——Jetty核心代码分析（原书）

> **本书独有"真实系统源码"章**：剖析 Jetty 这个高并发 Web 服务器的并发设计——NIO 多路复用、`Selector` 模型、`EndPoint`/`Connection` 的状态机、线程池与 NIO 的协作。把前面所有概念落到"工业级服务器"里。与《Java高并发核心编程》(Netty/Reactor) 互补（Jetty 是另一个 NIO 服务端实现视角）。

## 一、本章地图

| 主题 | 关键 |
| --- | --- |
| Reactor 模式 | 单/多 `Selector` 多路复用（见《高并发核心编程》4 章） |
| `EndPoint`/`Connection` | 连接状态机；事件驱动 |
| 线程模型 | Acceptor + Selector + Worker 协作 |
| 背压/限流 | 连接数/请求数控制 |

## 二、核心精讲

### 2.1 Reactor 模式落地
- **Acceptor 线程**：监听 `ServerSocketChannel`，接受新连接 → 注册到 `Selector`。
- **Selector 线程**：`select()` 等待 I/O 事件（读/写就绪）→ 派发给 `EndPoint`/`Connection` 处理。
- 对比：Netty 用 `EventLoopGroup`（多 Reactor，主从分工）；Jetty 用类似 Acceptor + 多 Selector。

### 2.2 连接状态机
- `EndPoint`：封装一个连接的 I/O（`fill`/`flush`）。
- `Connection`：解析协议（HTTP）→ 生成 `HttpServletRequest` → 交给应用 `Handler`。
- 状态机：READ → PARSE → HANDLE → WRITE → 循环；阻塞点用异步回调避免占 Selector 线程。

### 2.3 线程模型
- I/O 多路复用（少量 Selector 线程管海量连接）+ 业务处理线程池（处理慢 Handler 不让 Selector 卡）。
- 关键：Selector 线程**绝不做阻塞业务** → 否则所有连接饿死（与 `parallelStream` 提交阻塞任务同理）。

### 2.4 限流/背压
- 连接数上限、请求队列上限；过载时拒绝（类比线程池拒绝策略）。

### 2.5 🔧 现代
- 虚拟线程（JEP 444）让"每连接/每请求一线程"重获可行 → 传统 NIO Reactor 的"少量线程管海量连接"复杂度可被虚拟线程简化（但 NIO 仍适合极高连接数 + 低活跃度场景）。

## 三、版本演进

- **Jetty 9/10/11/12**：模块化、HTTP/2、虚拟线程适配（Jetty 12 支持虚拟线程处理）。
- **JDK 7**：NIO.2（`AsynchronousChannel`）；**JDK 21**：虚拟线程。

## 四、经典论文 / 原始文献

- **Schmidt et al., "Reactor: An Object Behavioral Pattern" (POSA2, 1996)**——Reactor 模式权威。
- **Welsh, Gribble, Brewer, "Event-Based Structured Concurrency" (2001)**——事件 vs 线程（Loom 先声）。
- **JEP 444 (Virtual Threads)**。

## 五、工业界前沿

| 项目 | Stars | 关联 |
| --- | --- | --- |
| **eclipse/jetty.project** | 4k | 本书分析对象 |
| **netty/netty** | 34k | 另一 NIO 服务端（主从 Reactor） |
| **openjdk/jdk** | 23.4k | NIO / 虚拟线程 |
| **LMAX-Exchange/disruptor** | 18.5k | 服务端内无锁 RingBuffer |

## 六、常见误区 / 本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "Selector 线程能做业务" | 会饿死所有连接；业务交线程池 |
| 2 | "NIO 一定比线程模型快" | 高连接低活跃 NIO 优；否则虚拟线程更简 |
| 3 | "连接无限接收" | 需限流/拒绝，避免 OOM |
| 4 | "新服务端必手写 NIO" | 虚拟线程 + 框架可大幅简化 |
