# 第 7 章 并发 API（The Concurrency API，Items 35–40）

> 对应原书第 7 章（Items 35–40）。单文件大纲 [../Effective_Modern_C++.md](../Effective_Modern_C++.md)；
> 导航 [00-总览与阅读地图.md](00-总览与阅读地图.md)｜索引 [../C++系列·总索引.md](../C++系列·总索引.md)。
> 本书最「保值」也最「被改写」的一章：保值的是任务抽象与 atomic/volatile 分界，
> 被改写的是它之后十年的并发设施（jthread、协程、std::execution）。

## 核心概念速览（中英对照）

- **任务** — task：一段待执行的工作 + 一个结果信道（`std::future`）；比线程高一层抽象。
- **`std::async`** — std::async：任务启动器；`launch::async` 真并发，`launch::deferred` 惰性「寄生」执行。
- **期值** — future/promise：跨线程结果搬运的凭据对；异常随结果一起传送。
- **不可联结即终止** — unjoinable → terminate：可联结的 `std::thread` 对象析构即 `std::terminate`。
- **线程句柄析构行为** — thread handle destructor behavior：future 析构**不**等任务，
  但 `shared_future`/promise 链上的「最后一棒」可能让任务在析构者线程上跑。
- **void 期值** — `std::future<void>`：一次性事件通知信道；比原子标志位少一对竞态。
- **`std::atomic`** — std::atomic：内存模型层的无锁通信原语，带内存序承诺，可为无锁或有锁实现。
- **`volatile`** — volatile：面向「编译器不可见的外部写」（内存映射 IO、信号处理上下文）的优化屏障，
  **不**是同步原语。
- **`std::jthread`（书后）** — joining thread：C++20 的 RAII 线程，析构自动 request stop + join，配 `stop_token`。

## 本章地图

| Item | 核心论点 |
| --- | --- |
| 35 | 优先任务而非线程：线程是稀缺资源、异常要经 future、任务可同步退化执行、结果回传标准化 |
| 36 | 需要真异步必须显式 `std::launch::async`：deferred 会被「谁 get 谁执行」寄生，条件变量等待里直接死锁 |
| 37 | 让 std::thread 在所有路径不可联结：join 在异常路径上不可达 → 自造 RAII 包装（书中三方案） |
| 38 | 线程句柄析构的隐藏行为：最后一个 future 持有者的析构可能触发任务执行/同步等待 |
| 39 | 一次性事件通信用 `future<void>`（每事件一个 promise）：原子布尔的「检查-动作」窗口在 ping-pong 场景丢事件 |
| 40 | atomic 管并发、volatile 管特殊内存；二者不可互替，volatile 不保证原子性与有序性 |

## 动机：线程是「机制」，任务是「意图」

Item 35 的论证结构值得复盘：`std::thread` 提供的是 OS 线程的薄封装——
① 资源：每线程栈（默认 MB 级）+ 内核对象，过载即崩（线程耗尽 = 拒绝服务）；
② 异常：线程函数抛出 = `std::terminate`，结果无处安放；
③ 调度：把「并行意图」绑死在「一个 OS 实体」上，剥夺实现做工作窃取/复用的空间。
任务抽象（packaged_task/async/future）把三样都解耦：意图与执行载体分离。
这条「面向任务编程」的路线，后来成为 C++20 协程与 C++26 `std::execution` 的官方路线
（见演进节——本书的预言属性在此兑现）。

## 机制：六层展开

### 1. async 与启动策略的暗礁（Item 35/36）

```cpp
// 🔧 已实测（脚本 s6_concurrency.cpp，静态链接运行）：
auto f = std::async(std::launch::async, boom);     // boom 抛异常
try { f.get(); } catch (const std::exception& e) { /* 捕获: task 内异常 */ }
// 同样代码放 std::thread(boom) → terminate。异常传送是任务的第一红利。

auto fd = std::async(std::launch::deferred, work); // 默认策略 = async|deferred，由实现选！
// get() 前 work 一行没跑（实测 ran=0）；get() 在**调用者线程**上执行 work（实测 ran=1）
```

三条实战纪律：① 需要真并发一律写 `std::launch::async`（默认策略可能给你 deferred）；
② deferred 任务会在「任何调 get/wait 的线程」上寄生执行——在持有 `condition_variable` 关联锁的
线程上触发 = 书给的死锁剧本；③ deferred 任务在 future 链上传递（`shared_future` 多消费者时，
「谁第一个 get 谁干活」）。

### 2. 析构触发任务（Item 38）

更阴的形态：`std::thread` 不能析构即跑，但 **deferred 任务可以**——最后一个指向其共享状态的
future 析构时，标准允许「与析构同步」，实测里表现为：对象在 `f1 = std::move(f2)` 之类的
移动赋值中，被置换出的旧 future 析构把任务在当前线程执行掉。结论与 Item 37 会师：
**不确定谁会在哪跑完，就别把 deferred 放进对象析构链**——或干脆只用 `std::launch::async` + join 纪律。

### 3. 不可联结线程的 RAII 三方案（Item 37）

| 方案 | 思路 | 代价 |
| --- | --- | --- |
| `JRSSThread`（书中命名） | 析构**永远 join** | 异常传播时可能等一个「本该被取消」的线程 |
| `ActiveThread` | 析构时 join 或按选择 terminate | 决策推迟到构造点，API 诚实 |
| `ScopeExit` 工具 | 用退出回调手工 join | 样板代码 |

C++20 的 `std::jthread` 选了第一种并补上取消机制（`stop_token`）——
🔧 实测：jthread 出作用域自动 join，无 terminate（脚本 s6）。本仓库对
ScopeExit 有笔记：[../../cpp/ScopeExit.md](../../cpp/ScopeExit.md)。

### 4. void future 修好 ping-pong（Item 39）

场景：线程 A 产生事件，线程 B 反应，A 还要从 B 收「已处理」回执。
原子布尔方案在「A 设 done=false → B 读 done=true（旧值）→ B 设 done=true」这类
检查-动作窗口里**丢事件**；书的解法：**每个事件一对新的 `promise<void>/future<void>`**——
通道一次性使用，状态编码在 future 的就绪与否里，没有可复用的标志位，即没有竞态窗口。
代价：每事件一次堆分配（控制块）；高吞吐场景退到「条件变量 + 队列」——那是
[../C++并发编程实战2/04-并发操作的同步.md](../C++并发编程实战2/04-并发操作的同步.md) 的主场。

### 5. atomic vs volatile 的分界线（Item 40）

| 维度 | `std::atomic` | `volatile` |
| --- | --- | --- |
| 面向 | 线程间数据竞争（内存模型概念） | 优化器看不见的内存（MMIO、信号处理栈） |
| 原子性 | 承诺（或锁模拟） | **不承诺**（`++v` 仍可撕裂） |
| 顺序 | memory_order 显式约束 | 仅保证「该读写不被删/挪出」，线程间乱序依旧 |
| 可无锁 | `is_always_lock_free` | 不适用 |

🔧 实测（本机 GCC 15.2）：对 `volatile int` 写 `++v`，`-Wall` 即警告
`'++' expression of 'volatile'-qualified type is deprecated [-Wvolatile]`——
C++20 已把 volatile 上的复合赋值/自增自弃用，本书「别拿 volatile 当 atomic 用」
的告诫被标准以弃用投票再次确认（同线程 demo：`a=1 v=1`，脚本 s6）。
两个合法保留地：① 内存映射 IO（`volatile` 保证每笔访问落地，配平台 barrier 指令）；
② `sig_atomic_t`/信号处理函数与主程序共享的变量（此处两者同时使用：`volatile sig_atomic_t`）。

## 权衡

任务化的成本是**控制块/状态分配**与间接层；线程数小的批处理里 `std::thread` 直接了当。
atomic 的成本是 `RMW` 循环与缓存行弹跳，`memory_order_relaxed` 能救计数但不能救协议。
volatile 在 MSVC 老代码里被误用为同步（`volatile` 在 MSVC 默认模型下带 acquire-release 语义），
读跨平台老库时这是考古知识点而非合法用法。

## 相邻概念对比

- **`std::thread` vs `std::jthread`**：join 责任从「程序员每路径兑现」变成析构契约；
  取消从「没有」变成「stop_token 协作式」。
- **future 链 vs 条件变量队列**：一次性事件用 future 省竞态；多路持续事件必须回队列 + 锁。
- **atomic 引用计数 vs shared_ptr 计数**：后者是前者的标准封装；手工 `atomic<shared_ptr>`
  式的「原子拷贝指针变量」是 C++20 前没有 `atomic<shared_ptr>` 时的补丁形态。

## 最新演进与工业实践

- **C++20 并发包**：`std::jthread`/`std::stop_token`（Item 37 的官方答案）、
  `std::atomic::wait/notify`（Item 39 的一半场景升级为库原语）、`std::latch/barrier/semaphore`。
  逐项讲解见 [../C++并发编程实战2/02-线程管控.md](../C++并发编程实战2/02-线程管控.md) 与
  [../C++并发编程实战2/05-Cpp内存模型与原子操作.md](../C++并发编程实战2/05-Cpp内存模型与原子操作.md)。
- **packages/tasks 预言的兑现链**：本书 Item 35 展望的「executors + packaged_task」进入
  Parallelism TS v2 工作稿 [N4620](https://wg21.link/N4620)（2016；⚠️ 标题逐字未核），
  后与 executors 合并为发送者/接收者模型：[P2300R10「std::execution」](https://wg21.link/P2300)
  （Dominiak/Evtushenko/Baker/Teodorescu/Howes/Shoop/Garland/Niebler/Lelbach，2024；
  经 wg21.link 解析核实，标题与作者已核）——cppreference 将其登记为 C++26 库组件
  （⚠️ 收录会次的精确日期未核）。工业实现：[NVIDIA/stdexec](https://github.com/NVIDIA/stdexec)
  （P2300 参考实现）、[facebook/folly](https://github.com/facebook/folly) 的 `folly::coro`
  与 `folly::Executor` 系。
- **协程（C++20）**：`co_await` 把「任务」内联进语言；`std::execution` 与协程的组合
  （sender 的 awaitable 适配）是 2024–2026 的主流异步栈形态。对本书「基于任务」主张而言
  这是完成时，不是反驳。
- **`std::atomic_ref`（C++20）**：对既有非原子对象施加原子视图（生命周期纪律严格），
  补上「不能改类型但需要原子性」的场景。
- **volatile 的持续被审**：SC22 德国代表团 2022 年提交意见书质疑 volatile 的设计
  （"On the Dubious Nature of volatile in C++"；⚠️ 文档编号未核实），与 GCC/Clang
  的 `-Wvolatile` 共同构成「volatile 正在被逐步边缘化」的信号——但 MMIO 仍无标准替代。
- **对本书结论的修订**：Item 35/36/40 存活且被强化；Item 37 被 jthread 收编；
  Item 38 的「句柄析构怪癖」在教学语境让位给「sender 的生命周期契约」；Item 39 的
  `future<void>` 方案仍是好品味，但 `atomic::wait` 更便宜。

## 常见误区

1. 「`std::async` 默认就是起线程」——默认策略含 deferred；`valid()` 的 future 析构不等
   （async 任务的等待发生在**任务句柄**而非 future 的通用规则要分开记）。🔧 实测分叉。
2. 「detach 是解决 terminate 的办法」——detach 把所有权丢给系统，资源不可控；
   书的立场：让所有路径**不可联结**（join 或 transfer），不是放任。
3. 「volatile 读写是原子的」——不承诺；实测警告即证其不可靠（x86 上对齐 int 的「碰巧」不是合同）。
4. 「atomic 就是 lock-free」——`is_lock_free()` 可为 false（128 位原子在多数平台走锁表）。
5. 「future.get 会阻塞等所有任务」——只等**这一份**结果；deferred 情形下是「现在就跑给你看」。

## 与其他章/其他笔记的联系

- 闭包携带任务：[06-lambda表达式.md](06-lambda表达式.md)（Item 32 → 异步任务）；
  const/原子缓存的接口契约：[03-转向现代C++.md](03-转向现代C++.md)（Item 16）。
- 本仓库目录版并发全书：[../C++并发编程实战2/00-总览与阅读地图.md](../C++并发编程实战2/00-总览与阅读地图.md)；
  中文讲解：[../现代C++实战30讲/11-thread与future及内存模型.md](../现代C++实战30讲/11-thread与future及内存模型.md)。
- 笔记：[../../cpp/cpp_atomic.md](../../cpp/cpp_atomic.md)、[../../cpp/pthread.md](../../cpp/pthread.md)（底层视角对照）。

---
上一章：[06-lambda表达式.md](06-lambda表达式.md) ｜ 下一章：[08-微调与全书收束.md](08-微调与全书收束.md) ｜ 返回：[00-总览与阅读地图.md](00-总览与阅读地图.md)
