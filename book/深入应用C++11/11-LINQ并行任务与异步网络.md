# 11 · LINQ to Objects、并行 TaskCpp 与 asio 通信（原书第 14、15、16 章）

> 覆盖原书第 14 章（14.1 LINQ 语义 / 14.2 C++ 中的 LINQ / 14.3 泛化、可调用对象、链式调用 / 14.4 实现 / 14.5 实例）、
> 第 15 章（15.1 TBB / 15.2 PPL / 15.3 选型 / 15.4–15.7 TaskCpp：task、延续、WhenAll/WhenAny、并行算法）、
> 第 16 章（16.1 Reactor/Proactor / 16.2–16.3 asio / 16.4–16.5 服务端客户端 / 16.6 TCP 粘包）。
> 三章共享一条思想：**把控制流做成可组合的值**——查询管道、任务延续、异步回调。
> 大纲形态见 [../深入应用C++11.md](../深入应用C++11.md)；返回 [00-总览与阅读地图.md](00-总览与阅读地图.md)。

## 核心概念速览（中英对照）

- **语言集成查询** — LINQ (Language-Integrated Query)：C# 的声明式容器操作谱系，where/select/聚合操作符代数。
- **惰性求值管道** — lazy pipeline：逐元素拉取的中间态对象链，`ToList/First` 才物化——ranges views 的雏形。
- **链式调用** — fluent interface：操作符返回"下一段管道"而非结果容器，表达式即数据流图。
- **容器与数组的泛化** — range 泛化：`begin/end` 协议统一任意序列源（书 14.3.1），C++20 `std::ranges::range` 概念的制度前身。
- **任务与延续** — task & continuation：`task<T>.then(f)` 把"完成后做什么"编进值，避免回调地狱。
- **任务组合** — WhenAll / WhenAny：多任务汇合语义，fan-in 的两种协议（全等/任一）。
- **并行算法** — parallel_for_each / invoke / reduce：TBB/PPL 风格的批量并行入口，书 15.7 复刻三件套。
- **工作窃取** — work stealing：空闲线程从别人队列偷任务，TaskCpp/cosmos `worksteal` 目录的主题。
- **反应器/主动器** — Reactor / Proactor：就绪通知（可读了你自己 recv）vs 完成通知（recv 完好的 buffer 给你）两代事件模型。
- **Proactor 的 C++11 形态** — asio：completion handler + io_context 线程模型，完成端口/epoll 的统一门面。
- **TCP 粘包/半包** — message framing：字节流无消息边界，长度前缀/分隔符协议化切分（书 16.6 用前缀法）。

## 一、动机：三件"高级语言设施"的 C++ 补课

C# 有 LINQ 与 async/await、Java 有 Stream 与 CompletableFuture，C++98 两手空空。2011 年的
标准件只给到闭包 + future；祁宇用本章把"缺的课"补成三个可开源的库（cosmos 的
`LinqCpp.hpp / 顶层 task 系列 / worksteal`，实测均在仓库）。第 15 章还附送一场工程选型实况：
TBB（跨平台但重）与 PPL（微软原生但锁 Windows）都不合"轻量级"目标，于是自研。

## 二、机制

### 2.1 LINQ 的 C++ 骨架：返回"管道"而非"答案"
```cpp
// 🔧 实测 ch11.cpp 的中间物化简化版（书完整版为惰性迭代器链）
auto evenSquares = select(where(nums, [](int n){ return n % 2 == 0; }),
                          [](int n){ return n * n; });
```
真正的书版 `linq<T>` 持 `function` 谓词链，`ToList()` 时才跑完——**闭包存的是"待执行的计算"**。
14.3.1 的泛化靠 SFINAE 探测 `begin/end`：与 C++20 ranges 的 `range_concept` 探测同一思路，
只是当时要用 20 行 traits 代替 1 行 `ranges::range`。实测踩点：`auto` 返回类型推导的
`where/select` 在 gnu++11 直接编译失败（C++14 特性）——LINQ 库对语言版本的最低要求由此而来。

### 2.2 TaskCpp：延续是"包装好的回调"
`task<T>::then(f)`：把 `f` 存进本任务 shared state 的完成动作表，完成时投递执行——
与 15.2 的 PPL `then()` 语义对齐（这正是作者对照两家后选定的 API）。`WhenAll/WhenAny`
用原子计数 + promise 兑现实现（实测复刻：`vector<future>` 全 get ≈ WhenAll，总=60）。
延续链的每个节点都是对象，异常沿链传播——future 异常语义（[05 章](05-多线程开发变得简单.md)）的组合放大。

### 2.3 asio 的 Proactor 三件套
`io_context`（事件循环/完成队列）+ `socket.async_read_some(buffer, handler)`（完成通知请求）+
`strand`（同资源 handler 串行化）。C++11 的贡献是把 handler 写成捕获 `shared_ptr` 的 lambda，
会话对象生命期自管理（书 16.4/16.5 服务端客户端的当代标准写法，沿用至今）。粘包处理在流式
`read_some` 上必须先凑长度再取体：`async_read` + 组合匹配器（`transfer_exactly`）即协议化答案。

## 三、权衡与实战提示

- 中间物化（实测简化版）实现十分钟、惰性管道是三个月——LINQ 类库的成本在**迭代器类型爆炸**，
  2026 年直接 ranges 别自研。
- 自研 task 库的停机/优先级/取消语义都是深坑（书 15 章做到"延续+组合+三并行算法"即收笔，
  诚实的"轻量级"定位）；生产选型仍是 TBB/asio/`std::execution`。
- Proactor 的完成回调在对象销毁后的悬垂是 asio 头号事故源——`bind_executor(strand, handler)` +
  `steady_timer` 取消协议，或一切收敛到协程（见演进节）。
- 任务 `then` 延续 vs 协程的分界不是性能而是**栈的所有权**：延续链是堆上对象 + 显式数据流，
  协程是堆栈帧的暂停 + 隐式控制流；前者调试看链、后者调试看帧。
- 粘包协议要带"前缀上限"安全设定（如 4 字节长度 + 最大报文约束）：无界前缀=内存 DoS；
  书 16.6 的前缀法今天仍是教科书写法，端序（网络字节序）仍是第一踩坑位。

## 四、相邻概念对比

| 对比 | 差异一句话 |
| --- | --- |
| LINQ 链 vs ranges 管道 | 同一代数；前者自造惰性迭代器，后者语言级概念约束 + 组合子 |
| async/await（PPL 时期）vs future 链 | 语法级续体 vs 手工 then 拼接；coroutines 把 C++ 拉到前者表达力 |
| Reactor vs Proactor | 就绪通知省拷贝、完成通知省轮询；asio 两头都提供（posix/reactor 化，windows/IOCP） |
| WhenAll vs 线程池 join | 组合子语义（值）vs 同步点（语句）；前者可继续编排 |
| TaskCpp vs std::execution | 私有延续协议 vs 标准 sender/receiver 协议，2026 年分界线 |

## 五、实测（🔧 三档 + ranges 专项：g++ 15.2，gnu++11/17/23，`ch11.cpp`）

```text
gnu++11: 编译失败——error: 'where' function uses 'auto' type specifier without trailing return type
             （LINQ 返回类型推导 = C++14 门槛，实测红字）
gnu++17: OK  linq-style sum=171700（2²+4²+…+100²，与手算 4·Σk²(1..50) 一致）
             whenAll total=60（0+10+20+30）
gnu++23: OK  追加 ranges sum(first5 even squares)=220（2²+4²+6²+8²+10²，filter|transform|take 管道）
```

- `views::filter | views::transform | views::take(5)` 在 gnu++17 档是硬编译错误（ranges 属 C++20）——
  书 14 章的自研管道与标准管道的**代际分界**被一档实测钉死。
- `220` 恰是全序列读数 `171700` 的前五项部分和（2²+…+10²）：`take(5)` 截断不跑全序列，
  惰性管道的语义差异用两个数字就能看见。

## 六、最新演进与工业实践

- **C++14→C++20 主线**：`where/select` 的当代等价物是 `std::views::filter/transform/take`
  （ranges 库经 P0896R4 并入工作草案，wg21.link/p0896 实测解析至 r4；概念约束 P0734R0 实测）；
  `for` 循环里的 range-for 与 ranges 算法构成"第二篇 LINQ"的完整闭环。展开见
  [../C++17完全指南.md](../C++17完全指南.md) 与 [../现代C++实战30讲/16-未来篇Concepts-Ranges-协程.md](../现代C++实战30讲/16-未来篇Concepts-Ranges-协程.md)。
- **协程（C++20）**：`co_await/co_return` 把 TaskCpp 的 then 链改写成同步式代码；
  asio 官方已提供 `awaitable` + `co_spawn` 门面——16 章的 lambda 回调树在 2026 年教程里
  已是"旧写法对照"。
- **senders/receivers**：P2300R10（wg21 路线，实测解析至 2024 文档 p2300r10.html）并入工作草案推进中，
  目标把"任务/延续/WhenAll/并行算法"统一进 `std::execution`——TaskCpp 的每个小节都能在该 TS 找到归宿。
- **案例库现状对账（本次实测）**：
  - **TBB**：Intel 开源版迁移至 Linux 基金会 UXL——[uxlfoundation/oneTBB](https://github.com/uxlfoundation/oneTBB)
    实测最新 release v2023.1.0（2026-07-13），原 oneapi-src/oneTBB 路径已重定向；书 15.1 的
    `parallel_for/task_group` API 在新版仍兼容。
  - **PPL**：微软 Concurrency Runtime（`ppl.h`）随 VS 维护但不再是推荐新绿路径 ⚠️（官方立场未逐字核实）；
    书 15.3 的"弃 PPL 取跨平台"判断已被时间追认。
  - **Eigen**：官方主场在 GitLab——[gitlab.com/libeigen/eigen](https://gitlab.com/libeigen/eigen) 实测可达（HTTP 200），
    GitHub `libeigen/eigen` 路径 API 返回 404；`parallel_reduce` 场景的 Eigen 向量化与本章并行算法互补。
  - **protobuf**：序列化对侧（书 16 章自定义包头 的工业替代）——仓库已迁
    [protocolbuffers/protobuf](https://github.com/protocolbuffers/protobuf)（原 google 组织路径重定向，
    实测 2026-09 活跃、约 7.2 万 star），依赖 abseil 工具链（见 [09 章](09-AOP库与IoC容器.md) 对账）。
- **asio 现状**：[chriskohlhoff/asio](https://github.com/chriskohlhoff/asio) 实测 2026-07 仍活跃；
  Networking TS 进标准的努力由 asio 作者团队推动（C++26 目标，进度细节以 wg21 文档为准 ⚠️）。

## 七、交叉互链

- 大纲：[../深入应用C++11.md](../深入应用C++11.md)；总索引：[../C++系列·总索引.md](../C++系列·总索引.md)
- 上游章：[02 章完美转发](02-右值引用与性能改进.md)、[05 章 future 家族](05-多线程开发变得简单.md)、[08 章线程池](08-半同步半异步线程池.md)、[10 章消息协议](10-消息总线与SQLite封装.md)
- 条款版：[../Effective_Modern_C++/07-并发API.md](../Effective_Modern_C++/07-并发API.md)、[../Effective_Modern_C++/09-专题-书后演进时间线.md](../Effective_Modern_C++/09-专题-书后演进时间线.md)（std::execution 预言项）
- 专著：[../C++并发编程实战2/00-总览与阅读地图.md](../C++并发编程实战2/00-总览与阅读地图.md)；网络工程：[../Linux多线程服务端编程.md](../Linux多线程服务端编程.md)、[../C++服务器开发精髓.md](../C++服务器开发精髓.md)
- 教程线：[../现代C++实战30讲/13-数字计算与Boost.md](../现代C++实战30讲/13-数字计算与Boost.md)（Eigen 同题）、[../modern-cpp-tutorial.md](../modern-cpp-tutorial.md)
- 全书收束：本目录止于工程应用；语言演化史看 [../C++语言的设计与演化.md](../C++语言的设计与演化.md) 与 [../在拥挤和变化的世界中茁壮成长C++2006–2020.md](../在拥挤和变化的世界中茁壮成长C++2006–2020.md)；辨析：[../C++实战.md](../C++实战.md)
