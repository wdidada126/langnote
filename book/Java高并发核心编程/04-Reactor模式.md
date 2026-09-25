# 第 4 章 鼎鼎大名的 Reactor 模式（卷1）

> Reactor 模式（事件驱动）：单线程 Reactor、多线程 Reactor、主从 Reactor（Main-Sub Reactor）、Proactor（异步）。本书把「模式」与 Netty 线程模型对应，是网络高并发的中枢章。

## 一、本章地图

| 模式 | 结构 |
| --- | --- |
| 单线程 Reactor | 1 个线程管 accept+read+handle |
| 多线程 Reactor | 主 Reactor accept，子 Reactor 管 IO，业务线程池 |
| 主从 Reactor | Main 接连接，Sub 管已建连接 IO |
| Proactor | 真异步（完成端口 IOCP） |

## 二、核心精讲

### 2.1 🔧 主从 Reactor（Netty 默认）
- `BossGroup`（Main Reactor）只做 `accept`；`WorkerGroup`（Sub Reactor）管已连接 Channel 的读写（🔧 Netty `EventLoopGroup` 即一组 Reactor；每个 `EventLoop` 绑定一个线程 + 一个 `Selector`，串行处理自己 Channel 的事件，天然无锁）。

### 2.2 Reactor vs Proactor
- Reactor：事件就绪（可读）通知，仍由用户读（同步 IO）；Proactor：IO 完成通知（真异步，Windows IOCP）（🔧 Linux 上 Java 多用 Reactor+epoll；AIO/`io_uring` 才接近 Proactor）。

## 三、版本演进 / 论文 / 前沿

- 论文：Schmidt《Reactor: An Object Behavioral Pattern》（POSA2, 1996）；《Proactor》（POSA2）；Doug Schmidt ACE/Java NIO 实践。
- 工业界：Netty、Nginx、Node.js（libuv）、Redis（单 Reactor 单线程）、Tokio（Rust，类似 Sub Reactor）。
- 开源 stars（2026-09）：netty 34k / nginx 25k / node 110k / tokio-rs 33.2k。

## 四、常见误区 / 本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "Reactor=异步" | 它是同步 IO 就绪通知 |
| 2 | "业务阻塞在 EventLoop" | 丢给业务线程池 |
| 3 | "Boss/Worker 随便配" | Worker 数≈核数，Boss 1-2 |
| 4 | "单 Reactor 够用" | C10M 用主从 |
