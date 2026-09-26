# 第 05 讲 Go, Threads, and Raft：先立内存模型，再立共识

> 官方标题：**Go, Threads, and Raft**（LEC 5，主讲 rtm）
> 指定必读：**The Go Memory Model**（附官方页代码示例）

## 本章地图

本讲是 Lab 2（Raft）动手前的一讲，做两件事：

1. **讲清楚 Go 的并发与内存模型**——因为 Raft 的绝大多数 bug 都是并发 bug，
   而并发 bug 在 Go 里有一个明确的判定标准（race），和一个明确的检测工具（`-race`）；
2. **给 Raft 一个导论**——为什么需要共识、Paxos 为什么难懂、Raft 是怎么拆的、
   Raft 的基本词汇（状态、任期、两个 RPC）。

主线：为什么用 Go → goroutine/channel → **什么是 data race** → happens-before 的来源 →
race 检测器的能力边界 → 常见的并发写法陷阱 → Raft 的位置与动机 → Raft 的基本机制预览。

## 核心精讲

### 5.1 为什么这门课用 Go

- **goroutine 轻量**：成千上万个并发体很便宜，适合「每个 RPC 一个 goroutine」的模型；
- **channel 与 select**：把「等待/协调」写进类型系统，而不是靠裸锁；
- **内存安全 + GC**：避免 C/C++ 类内存错误（这是分布式调试里最不该出现的噪音）；
- **标准库自带 RPC**（L2 用过）与良好的并发原语；
- 缺点也要承认：**GC 停顿**、以及「并发正确性仍需自己保证」。

### 5.2 什么是 data race（本讲最关键的定义）

> 两个 goroutine 并发访问同一块内存，**其中至少一个是写**，且**两者之间没有同步关系** → data race。

三条限定缺一不可：

- 「同一个变量」——不同变量不算；
- 「至少一个是写」——两个只读不算 race（这也是为什么不可变数据天然安全）；
- 「没有同步关系」——有 happens-before 排序就不算（锁、channel、atomic 都能建立排序）。

Go 内存模型的正式表述是：**若没有 happens-before 关系，读写之间没有任何保证**。
不要指望「它大概率能跑对」——在没有同步的情况下，编译器与 CPU 的重排序都可能让结果出人意料。

### 5.3 happens-before 的来源（Go 里可以依赖的几条）

1. **goroutine 启动**：`go f()` 之前的一切，happens-before `f` 里的执行；
2. **channel**：对无缓冲/有缓冲 channel，**一次发送 happens-before 对应的接收完成**；关闭 channel 也建立排序；
3. **mutex**：`Unlock()` happens-before 后续的同锁 `Lock()`；
4. **`sync.Once`**：`once.Do(f)` 中 `f` 的执行 happens-before 任何 `Do` 的返回；
5. **`sync.WaitGroup`**：`Done()` happens-before `Wait()` 的返回；
6. **`sync/atomic`**：原子操作之间建立全局顺序（需要正确配对使用）。

反例（常见错误直觉）：

- **`time.Sleep` 不是同步**：睡一会儿不能建立 happens-before，睡再久也不算；
- **「我先启动它，所以它先跑」不成立**：启动顺序 ≠ 执行顺序；
- **`sync.Map` 不解决复合操作的原子性**：`Load` 再 `Store` 仍然不是原子的「读改写」。

### 5.4 教学示意：一个典型 race 与它的修法

> **教学示意，不参与构建**——只为说明「检查 + 修改」必须整体同步。

```go
// 教学示意，不参与构建

// 反例：读取与写入之间没有同步 —— 这是 race，不管它「看起来」多不可能出错
func (rf *Raft) badGetState() (int, bool) {
    return rf.currentTerm, rf.role == Leader // <- 与 SetState 并发访问同一字段即为 race
}

func (rf *Raft) badSetState(term int, isLeader bool) {
    rf.currentTerm = term
    if isLeader {
        rf.role = Leader
    }
}

// 正例：用互斥锁把「一组字段」当作一个不变式来保护
func (rf *Raft) getState() (int, bool) {
    rf.mu.Lock()
    defer rf.mu.Unlock()
    return rf.currentTerm, rf.role == Leader
}

func (rf *Raft) setState(term int, isLeader bool) {
    rf.mu.Lock()
    defer rf.mu.Unlock()
    rf.currentTerm = term
    if isLeader {
        rf.role = Leader
    }
}
```

> 更重要的教训（Raft 里天天遇到）：
> **「判断自己是 leader」与「往日志里追加、向 follower 发 RPC」必须发生在同一次持锁期间**，
> 否则你可能在「已经不是 leader」之后还在发 AppendEntries，而 follower 可能已经投给了别人。
> 这类 bug 不会每次复现，但 `-race` 或大量重复跑测试一定能抓到。

### 5.5 并发写法陷阱清单

| 陷阱 | 现象 | 处理 |
| --- | --- | --- |
| 循环里启动 goroutine 捕获循环变量 | 所有 goroutine 看到同一个值 | 老版本 Go 需在循环体内复制变量；**Go 1.22 起循环变量改为每次迭代独立**（以官方发布说明为准） |
| 用 `time.Sleep` 做协调 | 偶发失败、CI 上不稳定 | 用 channel / WaitGroup / condvar |
| 在持锁期间做 RPC 或耗时 I/O | 吞吐崩塌、易死锁 | 把「读状态」与「发网络请求」分开：持锁读快照，解锁后发请求 |
| 忘记 `defer Unlock` 或提前 `return` | 死锁 | 一律 `defer`；或用小函数包住临界区 |
| 两个 goroutine 按不同顺序加两把锁 | 死锁 | 全局规定加锁顺序 |

### 5.6 race 检测器的能力边界

- `go test -race` 基于 happens-before 的动态检测（ThreadSanitizer 思路），
  **只能发现「这次运行真的发生了」的 race**；没跑到的路径它不报；
- 所以正确做法是：**`-race` + 大量重复运行（如 `-count=100`）+ 覆盖各种故障注入顺序**；
- 反过来，「没有报 race」不等于「没有 race」，只等于「这条执行路径上没触发」。

### 5.7 为什么需要共识：复制状态机的位置

```
客户端请求（带有副作用的命令）
   → 共识模块（Raft/Paxos）把它放进一个「全副本一致的有序日志」
   → 各副本的状态机按日志顺序执行
   → 所有副本状态一致 → 任意一个都能接管服务
```

需要解决的根本问题是：**在部分节点失效、消息乱序/丢失/重复的情况下，让所有存活节点对「第 N 条命令是什么」达成一致。**

### 5.8 Paxos 为什么难，Raft 怎么拆

课程给出的判断：

- 单法令 Paxos（single-decree Paxos）本身就难懂；
- 把它组合成 Multi-Paxos 的**工程细节在原始文献里没有充分规定**（角色关系、日志压缩、成员变更都要自己补）；
- 结果是「实现者最终做出来的系统跟论文描述的已经不是一个东西」。

Raft 的做法是**为可理解性而设计**：

| 手法 | 含义 |
| --- | --- |
| **问题分解** | 拆成领导选举、日志复制、安全性三个可独立理解的子问题 |
| **减少状态空间** | 强领导（日志只从 leader 流向 follower）、日志不允许空洞、用随机化超时避免分裂选举 |
| 基本词汇 | 三种状态（follower / candidate / leader）、**任期 term**（逻辑时钟）、两个 RPC（`RequestVote` / `AppendEntries`，心跳是空的 `AppendEntries`） |

一句话：**Raft 的创新不在「能做到什么」，而在「能让人真的写出来」**——这也是它在工业界被广泛实现的直接原因。

## 版本演进

- **2013–2014**：Raft 论文（Ongaro & Ousterhout）发布，配套可视化与大量实现涌现。
- **2015 前后**：CoreOS etcd 采用 Raft，Raft 成为「事实默认共识算法」（此前 Paxos 只在论文与少数系统里）。
- **2018–2020**：Go 侧：`sync.Map`、错误处理改进、模块系统成熟；课程在 2020 用 Go 讲内存模型，
  正是因为「学生写的 Raft 全是并发 bug」这一经验。
- **2020（本讲）**：L5 的必读是 **Go 内存模型**而不是论文——课程明确把「会写正确的并发 Go」当作前置能力。
- **2022–2024**：Go 1.18 泛型、Go 1.22 循环变量语义变更（每次迭代独立）——这些都会影响「老博客里的 Raft 代码」是否仍然正确。
- **2026**：Raft 已是基础设施共识算法的事实标准；研究侧的注意力转向**无主/多主共识**（EPaxos、Flexible Paxos、Tempo）、
  **地理分布下的延迟权衡**，以及**如何验证**实现（形式化证明、仿真测试）。

## 经典论文与原始文献

| 论文 / 材料 | 出处 | 本讲为何读它 |
| --- | --- | --- |
| **The Go Memory Model**（官方文档） | Go 官方 | L5 **指定必读**（不是论文）。定义 race 与 happens-before |
| Ongaro & Ousterhout《In Search of an Understandable Consensus Algorithm》（Raft） | **USENIX ATC 2014** | 本讲导论的对象；**L6/L7 的正式必读** |
| （对照，非本讲指定）Lamport《Paxos Made Simple》 | 2001 | Raft 论文中「Paxos 难懂」论断的对照物；2020 课表中 Paxos 为 L7 的**选读** |
| （对照，非本讲指定）Lamport《Time, Clocks, and the Ordering of Events》 | CACM 1978 | 「任期 term」这种逻辑时钟的思想来源 |

## 近年研究与工业界开源实践（2015–2026）

- **近年研究**：
  - **Raft 的形式化验证**：多个工作用 TLA+/Coq/Verdi 验证 Raft 的关键属性（选举安全、日志匹配、状态机安全）；
    以及 **IronFleet**（SOSP 2015）用 Dafny 证明「实现 + 协议」一致——6.5840 2026 已单列一讲；
  - **确定性仿真测试**：把 Raft 实现放进确定性模拟器里暴力搜索调度（`madsim` 一类），
    比 `-race` 更强，因为它能复现「极低概率的时序」；
  - **无主共识**：EPaxos（SOSP 2013）、Flexible Paxos（OPODIS 2016）、Tempo 等，
    挑战「强领导在广域网跨地域下延迟高」的问题。
- **工业界开源（star 数 2026-09-26 `gh api` 实测）**：
  - `golang/go`（**139027★**）：本讲的语言与 `-race` 检测器来源。
  - `etcd-io/etcd`（**52310★**）：最知名的生产级 Raft 实现（Kubernetes 的元数据存储），
    `etcd-io/raft`（**1128★**）是其可复用的 Raft 库。
  - `hashicorp/raft`（**9136★**）：Go 生态另一个 widely-used Raft 库，Consul/Nomad 用过。
  - `tikv/raft-rs`（**3401★**）：Rust 版 Raft 库，TiKV 的共识层；可与 Go 实现对照看「同一协议的语言差异」。

## 常见误区与本课程需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「没报 race 就没有 race」 | 检测器只发现**本次执行发生**的 race；要靠重复运行 + 故障注入覆盖路径 |
| 2 | 「睡一会儿就能同步」 | `time.Sleep` 不建立 happens-before，不算同步 |
| 3 | 「两个读会 race」 | 只有至少一个是写才可能 race；不可变数据是安全的 |
| 4 | 「Raft 比 Paxos 更强」 | 二者**能力等价**（都能解共识），Raft 的优势是**可理解性与可实现性** |
| 5 | 「Go 的并发原语保证正确性」 | goroutine/channel 只是工具；「检查 + 修改」的原子性仍需自己组织 |
| 6 | 🔧 2020 课程未覆盖 | **Go 1.22 循环变量语义变更**：老教程/老代码里的 `v := v` 复制在新语义下已成为历史包袱；读旧代码要注意版本 |
| 7 | 🔧 2020 课程未覆盖 | **持锁期间禁止做 RPC/磁盘 I/O**：这是 Raft 实现里最常见的吞吐与死锁根源，课程只在零散处提及 |
| 8 | 🔧 2020 课程未覆盖 | **结构化并发**（`errgroup` / context 取消）：2026 的 Go 并发写法已普遍用 context 传递取消与截止时间（呼应 [02-RPC与线程.md](02-RPC与线程.md)） |
| 9 | 🔧 2020 课程未覆盖 | **泛型与类型安全的状态机**：Go 1.18 泛型后，状态机与应用层解耦的写法有了新选项；课程代码仍是 Go 1.x 老写法 |

## 与其他章 / 其他书的联系

- **本目录内**：
  - [02-RPC与线程.md](02-RPC与线程.md)——本讲是它的形式化（加锁的理由从「经验」升级为「happens-before」）；
  - [06-容错Raft一.md](06-容错Raft一.md)——本讲是导论，L6 进入 Raft 正文（选举 + 日志复制）；
  - [07-容错Raft二.md](07-容错Raft二.md)——快照/成员变更/线性一致读；
  - [13-Labs总结与2026视角.md](13-Labs总结与2026视角.md)——Lab 2 的调试方法（`-race` + 重复跑 + 仿真）。
- **跨书**：
  - [../多处理器编程的艺术2/03-并发对象与可线性化.md](../多处理器编程的艺术2/03-并发对象与可线性化.md)、[../多处理器编程的艺术2/05-同步原语的相对能力.md](../多处理器编程的艺术2/05-同步原语的相对能力.md)——共享内存并发的形式口径（可线性化即本讲 race 判定的理论基础）；
  - [../多处理器编程的艺术2/08-管程与阻塞同步.md](../多处理器编程的艺术2/08-管程与阻塞同步.md)——与 [../分布式系统/03-进程.md](../分布式系统/03-进程.md) 一起提供线程/管程的教材口径；
  - [../深入理解分布式共识算法/07-Raft.md](../深入理解分布式共识算法/07-Raft.md)——中文视角的 Raft 推导，与本讲对读；
  - [../深入理解分布式共识算法/04-Paxos.md](../深入理解分布式共识算法/04-Paxos.md)——补上 2020 课表里 Paxos 只是选读的缺憾；
  - [../深入理解分布式共识算法/12-FLP不可能定理.md](../深入理解分布式共识算法/12-FLP不可能定理.md)——解释「为什么 Raft 必须靠随机化超时绕开 FLP」。

> **Lab 提示（思路，不给代码）**：做 Lab 2 前先把「哪些字段由 `rf.mu` 保护」写进注释，
> 并保证**所有**对这些字段的访问都持同一把锁；RPC handler 里先持锁读快照、解锁后再发网络请求。
> 本目录不提供、也不链接任何公开解答仓库。
