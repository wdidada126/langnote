# 第 02 讲 RPC and Threads：分布式的两块积木

> 官方标题：**RPC and Threads**（LEC 2，主讲 fk）
> 指定必读：**Online Go tutorial**（官方页另附 `kv.go`、crawler 示例代码）
> 背景：这是 Lab 1 动手前的工具讲，Lab 1 的 worker/coordinator 与本讲的 crawler 是同一种并发结构。

## 本章地图

本讲讲两件「看起来简单、实际上处处是坑」的基础设施：

1. **线程（Go 里是 goroutine）**——为什么需要、会带来什么问题（竞争、协调、死锁、并发度）；
2. **RPC**——跨节点调用的形状，尤其是**失败语义（failure semantics）**：请求丢了怎么办、回复丢了怎么办、服务器崩了怎么办。

主线：线程动机 → 线程三难题 → crawler 三种写法（串行 / WaitGroup+锁 / channel）→ RPC 结构 → 三种失败语义 →
at-most-once 的实现（kv.go 的重复请求表）→ 「exactly-once」的真相。

## 核心精讲

### 2.1 为什么用线程

| 动机 | 例子 |
| --- | --- |
| **I/O 并发** | 一台 client 同时向多个 server 发请求，不等前一个回来 |
| **利用多核** | 并行执行 CPU 密集任务 |
| **写起来顺手** | 后台周期性任务（心跳、超时扫描）写成独立 goroutine |

难点随之而来：

- **共享数据（race）**：两个 goroutine 同时改一个 map → 需要 mutex 或 channel；
- **协调（coordination）**：一个 goroutine 要等另一个完成 → WaitGroup / channel / condvar；
- **死锁**：加锁顺序不一致、或「等着一个永远不会来的消息」；
- **并发度（granularity）**：并发太少没收益，太多则调度与内存开销反噬。

### 2.2 crawler：同一个问题的三种写法

**写法一（串行 DFS）**：递归抓取，用 map 记录已访问。正确但慢——每个 fetch 阻塞整个流程。

**写法二（WaitGroup + mutex）**：

```go
// 教学示意，不参与构建
type fetchState struct {
    mu      sync.Mutex
    fetched map[string]bool
}

// 注意：必须「先加锁判断并置位，再解锁去抓取」
// —— 若先解锁再抓，两个 goroutine 会同时抓同一个 URL
func (fs *fetchState) checkAndMark(url string) bool {
    fs.mu.Lock()
    defer fs.mu.Unlock()
    if fs.fetched[url] {
        return false
    }
    fs.fetched[url] = true
    return true
}
```

**写法三（channel 版）**：用一个 channel 当「待抓队列 + 完成计数」，
主 goroutine 从 channel 里读结果，直到计数归零。它天然避免了显式锁，但需要小心控制计数器的语义。

> 课程强调的教训：**并发程序里「判断」和「置位」必须原子地一起做**；
> 把它们拆成两步（先 if 再 set），中间一旦有调度切换，就重复抓取。
> 这条经验在后面所有 Lab 里反复出现（Raft 里「检查自己是不是 leader」与「追加日志」必须在同一个锁内完成）。

### 2.3 RPC 的形状

一次 RPC：client 把参数**编组（marshal）**→ 发到 server → server 解组 → 执行 handler → 编组返回值 → 回传 → client 解组返回。
设计问题：参数/返回值如何序列化、如何绑定服务（naming/binding）、如何处理失败。

**RPC 的失败模型是本讲的核心**：client 只知道「超时没收到回复」，而真实情况可能是：

1. 请求根本没到 server；
2. server 收到了、执行了，但崩了（崩在执行前 / 执行后 / 回复前）；
3. server 执行完并回复了，但回复丢了；
4. server 只是慢（还活着，稍后会完成）。

### 2.4 三种失败语义

| 语义 | 客户端行为 | 服务端要求 | 适用 |
| --- | --- | --- | --- |
| **at-least-once** | 一直重试直到收到回复 | 无 | **只适用于幂等操作**（读、覆盖写、幂等 put） |
| **at-most-once** | 重试，但服务端去重 | 维护重复请求表（按 client ID + 序号） | 非幂等操作的起点 |
| **exactly-once** | at-most-once + 无限重试 + **服务端保存执行结果以便重放** + 应用层自身容忍「执行了但不确定是否成功」 | 最重 | 难；通常退化为「at-most-once + 应用可见的状态查询」 |

**关键点**：Go 标准库 `net/rpc` 提供的是 **at-least-once**——超时就报错，重试由调用方决定。
课程用 `kv.go` 演示怎么在它上面搭出 at-most-once：

```go
// 教学示意，不参与构建：at-most-once 的重复请求表
type Clerk struct {
    server   *rpc.Client
    id       int64 // 每个 clerk 唯一，启动时分配
    seq      int   // 单调递增序号
}

type PutArgs struct {
    Key, Value string
    ClerkID    int64
    Seq        int
}

// 服务端：
//   table[ClerkID] = {Seq, Result}
//   - 若入参 Seq <= 记录的 Seq → 重复请求，直接返回记录的 Result，不再执行
//   - 否则执行，覆盖记录（因此每个 clerk 只占一行，内存有界）
//
// 语义边界（务必记住）：
//   1. 若 clerk 崩溃后以「相同 id」重启，序号从 0 开始 → 去重表会误判为重复请求
//      （课程里的做法是从一个唯一 id 服务获取新 id）
//   2. 去重表不解决「客户端崩溃后不知道结果」的问题 —— 那只靠重试 + 结果重放缓解
//   3. 这仍然不是线性一致的「exactly-once」：它只是「同一 clerk 的同一序号最多执行一次」
```

### 2.5 一个常被忽略的结论：没有「完美的 RPC」

- 若 client 崩溃后重启并发同一个请求，服务端无法区分「新请求」与「旧请求重发」，除非有**跨 client 生命周期的标识**；
- 若操作本身非幂等且无状态可查（例如「余额减 10」），要在分布式环境做到「一定且仅一次」，
  必须把「去重」下沉到**状态机层面**（这正是后面 Raft KV 里 session + seq 的由来，见 [08-ZooKeeper.md](08-ZooKeeper.md)）；
- 实务上的答案通常是：**请求带幂等键 + 服务端去重 + 客户端重试 + 读回确认**。

## 版本演进

- **1980s–1990s**：RPC 由 Birrell & Nelson（1984）与 Sun RPC/NFS 推广；当时的争论是「RPC 是否该长得像本地调用」
  （反对意见：透明性会掩盖失败，分布式必须让失败显式）。
- **2000s**：SOAP/WS-*、CORBA 的复杂度引发反弹，转向轻量 HTTP+JSON；
  Thrift（Facebook）、Protocol Buffers（Google）把「接口定义 + 编解码」标准化。
- **2010s**：gRPC（HTTP/2 + Protobuf + 流式）成为云原生默认 RPC；
  服务网格（Envoy/Linkerd）把重试、超时、熔断下沉到 sidecar——**本质上就是在统一实现本讲的失败语义**。
- **2020（本讲）**：课程用 Go `net/rpc` 教学，是因为它足够小、能看清失败语义；
  课程明确说明真实系统不会这么用。
- **2026**：gRPC 与 HTTP/3（QUIC）并存；重试策略、对冲请求（hedged request）、
  截止时间传播（deadline propagation）已成为框架默认能力，
  但「at-least-once 只适用于幂等操作」这条规则一点没变——它只是被框架藏起来了。

## 经典论文与原始文献

| 论文 / 材料 | 出处 | 本讲为何读它 |
| --- | --- | --- |
| Online Go tutorial（`tour.golang.org`） | Go 官方 | L2 **指定的 Preparation**（不是论文）。官方页附 FAQ 与 Question |
| `kv.go`、`crawler.go`（示例代码） | 课程官方 notes | 本讲的两个教学载体：at-most-once 去重表 / 并发爬虫 |
| （背景，非本讲指定）Birrell & Nelson《Implementing Remote Procedure Calls》 | ACM TOCS 1984 | RPC 的奠基；解释「为什么 RPC 要长得像本地调用」以及当时的取舍 |

> 注意：2020 年的 L2 **不读论文**，这与后面每讲一篇论文的节奏不同；不要把 MapReduce / GFS 当成 L2 的阅读。

## 近年研究与工业界开源实践（2015–2026）

- **近年研究**：
  - **对冲请求与尾部容忍**（Google *The Tail at Scale*, CACM 2013）：同一请求延迟 P99 后发第二份，谁先回用谁——
    这是把本讲「at-least-once 重试」从「失败后重试」推进到「慢了就重试」；
  - **截止时间传播与级联失败治理**：研究与实践都确认「每个 RPC 必须携带绝对截止时间」，
    否则重试风暴会打垮下游；
  - **形式化验证 RPC 状态机**（如 IronFleet，SOSP 2015；6.5840 2026 已单列一讲）用证明覆盖「重试是否安全」。
- **工业界开源（star 数 2026-09-26 `gh api` 实测）**：
  - `grpc/grpc`（**45342★**）：事实标准的 RPC 框架；重试、对冲、截止时间、流式都在框架层。
  - `golang/go`（**139027★**）：本讲的 goroutine / channel / `sync` 包与 `-race` 检测器都来自它。
    `go test -race` 是做 6.824 Lab 时最重要的工具之一（L5 会专门讲 Go 内存模型）。
  - `nats-io/nats-server`（**20771★**）、`apache/kafka`（**33848★**）：消息系统路线——
    当「at-least-once + 消费者幂等」比 RPC 的同步语义更合适时的替代选择（对比见 [../设计数据密集型应用/04-编码与演化.md](../设计数据密集型应用/04-编码与演化.md)）。

## 常见误区与本课程需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「RPC 就是函数调用」 | 它是**可能不执行、可能执行了但没回、可能执行多次**的调用；失败语义必须显式设计 |
| 2 | 「超时 = 没执行」 | 超时只代表「没收到回复」，server 可能已经执行成功 |
| 3 | 「加个锁就线程安全了」 | 锁定的是**不变式**而不是单个变量；「检查 + 置位」必须整体加锁 |
| 4 | 「at-most-once = exactly-once」 | at-most-once 只保证「最多一次」，客户端崩溃后可能「零次」；exactly-once 还要结果重放 |
| 5 | 「去重表无限增长」 | 按（clerk ID → 最新 seq + 结果）单行存储即可有界；但代价是不支持同一 clerk 的并发请求 |
| 6 | 🔧 2020 课程未覆盖 | **重试风暴与熔断**：课程只讲单个 RPC 的重试，2026 必须补「重试必须有预算（retry budget）+ 熔断 + 指数退避 + jitter」 |
| 7 | 🔧 2020 课程未覆盖 | **截止时间（deadline）与取消传播**：现代 RPC 把超时挂在 context 上跨服务传递，否则一个慢下游拖垮全链路 |
| 8 | 🔧 2020 课程未覆盖 | **HTTP/3 / QUIC 与连接迁移**：传输层换了（UDP + 0-RTT 重连），但「请求可能重复」的语义反而更强（0-RTT 重放），幂等设计要求更高 |
| 9 | 🔧 2020 课程未覆盖 | Go 的 `net/rpc` 在真实项目里已很少直接用；2026 主流是 gRPC / 自有协议。学的是**语义**，不是这个库 |

## 与其他章 / 其他书的联系

- **本目录内**：
  - [01-引言与MapReduce.md](01-引言与MapReduce.md)——Lab 1 就是本讲 RPC + 并发结构的直接应用；
  - [05-Go线程与Raft导论.md](05-Go线程与Raft导论.md)——L5 讲 Go 内存模型，是本讲「加锁」直觉的形式化；
  - [06-容错Raft一.md](06-容错Raft一.md)——Raft 的每个 RPC（RequestVote / AppendEntries）都必须按本讲的失败语义审视；
  - [08-ZooKeeper.md](08-ZooKeeper.md)——`kv.go` 的去重表在 Raft KV 里升级为 session + 序号。
- **跨书**：
  - [../分布式系统/04-通信.md](../分布式系统/04-通信.md)——教材口径的 RPC 语义分类（at-least/at-most）、异步 RPC 与消息中间件，可作本讲的系统化补充；
  - [../设计数据密集型应用/08-分布式系统的麻烦.md](../设计数据密集型应用/08-分布式系统的麻烦.md)——DDIA 对「不可靠网络 / 超时是唯一信息」的论述，与本讲完全同调；
  - [../Linux内核完全剖析/08-内核代码.md](../Linux内核完全剖析/08-内核代码.md)——单机内核里的并发与锁是「并发」直觉的另一半来源。

> **Lab 提示（思路，不给代码）**：写 Lab 1 前先在纸上列出「哪些状态被多个 goroutine 共享」，
> 给每一份共享状态指定唯一的保护者（一把锁或一个 channel），并让所有 RPC handler 都走同一条加锁路径。
> 本目录不提供、也不链接任何公开解答仓库。
