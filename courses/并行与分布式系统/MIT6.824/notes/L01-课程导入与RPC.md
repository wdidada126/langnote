# L01 课程导入：分布式系统的核心挑战（RPC 与分层设计）

> 阅读：Birrell & Nelson, *Implementing Remote Procedure Calls*, ACM TOCS 1984
> 本课全名 6.5840: Distributed Computer Systems Engineering；整门课 = 精读论文 + 从零写容错 KV。

## 1. 本讲核心问题

- 分布式系统的定义：**独立机器的集合，对上层表现为一台机器**（Tanenbaum）。
  三个不可回避的物理事实：网络不完全可靠、各机时钟不严格同步、没有共享内存与全局时钟。
- 工程难点不是"算"，而是**部分失效（partial failure）**：单机要么坏要么好，
  分布式系统里"一半是好的"是常态，程序必须正确应对"叫了 RPC 却不知道对方做没做"。
- 课程主线预告：如何在不可靠的部件上构建可靠的系统？两大答案贯穿全课——
  **复制（redundancy）** 与 **共识（consensus）**。

## 2. RPC 论文：设计与取舍

### 2.1 核心思想
把"跨机过程调用"包装成与本地调用同签名的桩（stub），让程序员**用同步调用
的直觉写分布式程序**，把复杂性下沉到运行时库。这是"抽象分层"在分布式里的第一次胜利。

### 2.2 关键机制（论文四问）
- **传输**：支持连接式（TCP）与无连接（UDP）两种。选 UDP + 应用层自管可靠性，
  换取低时延与多播可能；代价是必须自己处理乱序、丢失、重复。
- **语义**：论文给出 at-most-once（至多一次）。实现方式：会话 + 每次调用带 nonce，
  服务端缓存最近结果；**无法做到 exactly-once**——因为无法区分"响应丢了"和"请求没到"。
  这一节是全课程 repeated RPC / 幂等设计 / 去重的源头。
- **绑定**：三选一（启动即绑 / 首次调用绑 / 每次调用查名字服务），
  性能与位置透明性此消彼长——课程 Project 里的"客户端问 primary 要 config"正是第三种。
- **异常**：远端异常与本地异常必须分开编码（论文用 reply message 区分），
  否则网络故障会被误报成业务异常。

### 2.3 取舍总结
同步阻塞调用 ↔ 异步回调：RPC 选了同步（好写好调试），牺牲吞吐上限；
Go 的 goroutine（本课程指定语言）用 M:N 调度把"阻塞"变得廉价，是 1984 年取舍的现代补丁。

## 3. 论文脉络定位

L01 是全课的"语法"：此后每一篇论文（MapReduce/GFS/Raft/Dynamo/Spanner）
的控制面通信都是 RPC。L02 起论文开始回答本课总问题：
**性能（并行）→ 可靠性（复制/容错）→ 一致性（共识）→ 三者的权衡**。

## 4. 跨课程联系

- **6.S081**：本机进程间通信（pipe、共享内存、socket）与 RPC 是同构问题——
  参数传递、序列化、错误传播；内核 IPC 无部分失效，RPC 有，这正是本质差异。
- **CSAPP / 自顶向下计算机网络**：CSAPP Ch.11 网络编程给出 socket 字节；
  topdown 的 TCP 可靠性（重传、序列号、确认）正是 RPC 论文"传输与语义"一节的底层——
  RPC 的 at-most-once 若跑在 TCP 上，连接断裂时的"请求已发出但未知是否执行"依然存在。
- **CS149**：并行编程的通信-计算重叠思想在 RPC 层表现为异步/流水线调用。
- **15-445**：数据库的 client-server 协议（如 MySQL 协议）本质是带自定义语义的 RPC。

## 5. 知识点在开源项目中的应用

- **gRPC**：现代 RPC 标杆——HTTP/2 多路复用解决 head-of-line blocking，
  protobuf 做 IDL，拦截器链对应论文的"运行时库"。
- **brpc / tRPC / Dubbo**：连接管理、超时、重试、熔断，全部围绕论文指出的
  "不可靠网络上的调用语义"展开。
- **etcd 的 clientv3**：与 Raft 通信的 Watch/Lease API 就是带会话的 RPC，
  其 KeepAlive 机制是对"服务器可能已死"的显式建模。
- Go 标准库 `net/rpc`（已冻结）与 `rpc/jsonrpc` 生态：课程 pg1 早期版本用
  `net/rpc`，新版改为 gorilla/rpc，思想不变。

## 6. 延伸阅读

- Tanenbm/Van Steen《Distributed Systems》Ch.1（导论）与 Ch.11（RPC）。
- Vonicak 等关于 RPC 语义演进：*In Search of an Understandable Consensus* 前置阅读。
- 对照阅读：Sottile《The elements of style: RPC》与 gRPC ADR 中关于重试/幂等的讨论。
- 课程网站第一章幻灯片：pdos.csail.mit.edu/6.5840/lectures/s1intro.pdf。
