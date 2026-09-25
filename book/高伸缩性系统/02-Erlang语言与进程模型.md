# 第 2 章 Erlang 简介

> **一句话**：第 2 章是全书的**语言底座**——它要在 40 页内让读者同时拥有"写进程"和"被进程崩溃"两种能力，并为后面所有 OTP 抽象提供词汇表：进程、消息、链接、监视器、ETS。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 递归与模式匹配 | 尾递归、case/if、二元构造子 | 循环要靠递归；模式匹配是 Erlang 的"控制流" |
| 受函数式的影响 | 不可变数据、表达式即值 | 不可变是消息传递安全的前提，也是 GC 友好的前提 |
| 玩转匿名函数 | `fun`、闭包、`lists:map/fold` | 匿名函数是"把控制流交给库"的基础 |
| 列表推导：生成与测试 | `[F(X) || X <- L, Guard]` | 比手写递归更短，但**比尾递归慢**，别拿来写热路径 |
| 进程与消息传递 | `spawn`、`!`、`receive`、邮箱扫描顺序 | 进程是廉价并发体；**消息选择是线性扫描**，顺序有语义 |
| 不怕出错 / 用于监督的链接与监视器 | `link`、`monitor`、`exit/2` 信号 | link 是"死亡传播"，monitor 是"死亡通知不传播"——两者用途完全不同 |
| 记录、映射组、宏 | record / map / define | map 替代了 record 的一部分；OTP 21 起 `maps` 在行为回调里越来越常见 |
| 模块升级 | 换 `.beam` 而不停机 | 热升级的**最小**形态；升级依赖 supervision 树在正确的进程上做 |
| **ETS：Erlang 术语存储** | 四种表、锁选项、内存 | ETS 是**共享可变状态**的唯一正经入口，也是性能与一致性的分水岭 |
| 分布式 Erlang、命名与通信、节点连接与可见性 | `node()`、`register`、`net_kernel` | 分布式可以"顺手写"，但**顺手写的分布是最难修的分布** |

## 核心精讲

> 以下片段均为**教学示意代码，不参与编译、不参与任何构建**。

```erlang
%% 1) 尾递归：状态作为参数在帧间传递，进程不会长胖
loop(Acc, 0) -> Acc;
loop(Acc, N) -> loop(Acc + N, N - 1).

%% 2) 进程与消息：spawn 返回 pid，不知道谁是发信人
start() -> spawn(fun () -> loop(0, 10) end).

send(Pid, Msg) -> Pid ! {request, self(), Msg}.      %% 消息带 self()，才能回话

%% 3) receive：按**写入邮箱的顺序**逐条匹配，匹配到就留下剩余消息
receive
    {result, V} -> V;
    {error, Why} -> {error, Why}
after 5000 -> timeout                                 %% 超时不保证精确，且会把超时消息留在邮箱
end.
```

消息选择的**顺序陷阱**（原书点到但未展开）：`receive` 扫描邮箱，一旦某条不匹配就**继续往后看**，因此一条"永远收不到"的低优先级消息会拖住整条 receive：

```erlang
%% 反例：任何 {log, _} 都会占住邮箱，后续 {data, _} 迟迟取不到
wait() ->
    receive
        {data, D} -> handle(D);
        {log, _}  -> wait()          %% 这一条不死，data 就被后面的 log 挤住
    end.
```

链接与监视器的语义差别（本节最重要的一张图）：

```erlang
%% link：双向死亡信号，默认退出信号 **不捕获就会杀掉接收者**
Pid = spawn_link(fun () -> crash() end),
%% monitor：单向死亡通知，接收者自己不会死
Ref = monitor(process, Pid),
receive {'DOWN', Ref, process, Pid, Reason} -> ok after 3000 -> timeout end.
```

ETS 的最小用法与**必须手动选的锁策略**：

```erlang
%% public 表：所有进程可读可写；这是"共享内存"的唯一入口
Tab = ets:new(players, [public, named_table, set, {keypos, 1}]),
ets:insert(Tab, {alice, 42}).

%% 为并发写拆分锁；OTP 25 起可用 auto 让运行时判断
%%   [{write_concurrency, auto}]           %% OTP 25+
%%   [{write_concurrency, true}, {decentralized_counters, true}]  %% OTP 23+
ets:new(counter, [public, named_table, {write_concurrency, true}]).
```

binary 的引用计数（原书强调的坑）：**sub-binary 不会复制，但它撑住整块原始 binary 的生命周期**：

```erlang
%% Body 若来自大 binary 的切片，Body 会"钉住"整块内存，直到 Body 消亡
%% 长生命周期进程持有小 slice = 内存泄漏的经典构造
keep(<<_Head:8/binary, Payload/binary>> = _Whole, BigRef) ->
    erlang:put(large, BigRef),              %% 示例：误持有整块
    Payload.                                %% 真正在用的一直是 slice
```

## 版本演进

| 版本 | 与本章相关的变化 |
| --- | --- |
| OTP 17（2012） | map 类型引入，随即成为 record 的强竞争者 |
| OTP 18（2014，本书基线） | `+binary` 相关优化；`erts` 内存占用下降 |
| OTP 20（2016） | `erlang:binary_to_term` 等安全性改进；本书中译本对应世代 |
| OTP 21（2017） | **调度器 SMP 默认开启**；`ets` 的 `insert` 并发性能继续改善 |
| OTP 22（2018） | **`write_concurrency` 对 `ordered_set` 首次生效**（此前该选项对它无效）；`decentralized_counters` 为 `ordered_set` 提供 |
| OTP 23（2019） | ETS 并发可扩展性覆盖全部表类型；`decentralized_counters` 默认随 `write_concurrency` 开启；数值字面量支持下划线 |
| OTP 25（2021） | ETS `write_concurrency` 新增 **`auto`**（真正的"运行时决定要不要锁拆分"）；`read_concurrency` 建议与它搭配 |
| OTP 26（2022） | **选择性接收优化扩展到"reference 由其他函数返回"的场景**，`receive` 命中不再退化成线性扫描 |
| OTP 27+（2023–2026） | `maybe_expr` 默认启用；map 内部原子键顺序变化（`maps:iterator/2` 提供确定性遍历） |

## 经典论文与原始文献

| 论文 / 文献 | 出处 | 贡献 |
| --- | --- | --- |
| Armstrong, Dijkstra, Cook, *Erlang — The Development of a Robust Telecom Platform* | ICSE 1996 | 进程模型与"错误处理是设计的一部分"最初的表述 |
| Armstrong, *Making Reliable Distributed Systems in the Presence of Software Errors* | KTH 博士论文, 2003 | 形式化讨论 monitors vs links、错误定位、崩溃恢复策略 |
| Dijkstra, *Goals, Concepts, and Design Decisions of the THE Multiprogramming System* | CACM 11(9), 1968 | 分层优先级 + 周期性重排的调度思路；本章"进程很廉价、调度很关键"的历史源头 |
| Borggren, Leifer, Gustafsson, *Mnesia — A Distributed Embedded Database for Mobile Computing* | 1999 | ETS/mnesia 双存储引擎的原始设计动机 |
| Tanenbaum & van Steen, *Distributed Systems: Principles and Paradigms*（第 2 版, 2017） | Pearson | 命名服务、节点可见性、部分失败的通用术语对照 |
| Erlang/OTP *Efficiency Guide* | erlang.org 官方文档 | binary 复制语义、引用计数、ETS 锁与内存开销的一手说明 |

## 近年研究与工业界开源实践（2015–2026）

趋势：ETS 是这十年来 BEAM 性能故事的主角——从"给 ordered_set 加 `write_concurrency`"到"去中心化计数器"再到"`auto` 选项"，方向始终是**让共享表在多核下继续线性扩展**，代价是 `ets:info` 变慢。与此同时，**引用计数 binary 的无拷贝切片**在 OTP 23 之后被更广泛地利用，但也让"误持有 slice 导致整块内存不释放"这类泄漏更容易发生。

| 仓库 | star | 说明 |
| --- | --- | --- |
| `erlang/otp` | **12337★** | `erts` 的 ETS 实现与选项演进的一手来源 |
| `basho/riak_core` | **1274★** | 大量 ETS 表 + 按桶分片进程的现实样本 |
| `processone/ejabberd` | **6733★** | 数千会话进程 + RTXE 会话表的经典用法 |
| `rabbitmq/rabbitmq-server` | **13876★** | queue 索引与指标走 ETS，节点元数据走 mnesia |
| `apache/couchdb` | **6963★** | 文档存储 + 视图，适合对照 ETS 的"纯内存共享"取舍 |
| `golang/go` | **138993★** | 对照：Go 没有共享表，`sync.Map` 承担了类似角色 |

## 常见误区与本书需修正之处

| 现象 | 说明 | 现状 / 修正 |
| --- | --- | --- |
| 🔧 **ETS `write_concurrency` 被当成全局开关** | 原书把它描述成"开启就并发写"，实际上它是**按表选择的锁粒度策略**：读写的切换变贵，小表加它反而更慢 | 按 OTP 25+ 文档：优先用 `write_concurrency` + `auto`，并几乎总是搭配 `decentralized_counters`；注意它 **不改变原子性与隔离性** |
| 🔧 **`write_concurrency` 对 `ordered_set` 无效的历史** | 原书成书时该选项对 ordered_set 基本没效果 | 自 OTP 22 起它对该表类型生效；automatic 行为在 OTP 25 变成 `auto` |
| 🔧 **`receive` 的线性扫描陷阱** | 原书说明了"消息按写入顺序被扫描"，但没有给出"一条永远不匹配的低优先级消息会拖死整条 receive"的后果 | 补：配合 OTP 26 的选择性接收优化，把 pattern 写得"可命中"（如先匹配 `{tcp, _,_}` 再匹配兜底），并保留独立超时分支 |
| 🔧 **`after` 超时不是精确闹钟** | 原书只说"超时不保证精确"，但没说 **超时后消息仍在邮箱里** | 补：超时分支里要么立即 `flush` 掉残留消息，要么把兜底模式写进 pattern，否则下一轮 receive 会被"幽灵消息"触发 |
| **用列表推导写热路径** | 看起来最函数式、也最慢 | 热路径用尾递归或 `lists:foldl`；推导适合非热点 |
| **误持有 sub-binary** | 小切片钉住整块大 binary | 长生命周期进程只保存真正需要的切片，别把原始 binary 存进进程字典/ETS |
| **进程字典当全局缓存** | `erlang:put` 让进程"不再纯净"，且与热升级、GC 交互微妙 | 用 `persistent_term`（OTP 21+）或显式参数传递 |
| **把 ETS 当数据库用** | `public` 表没有事务 | 单对象操作原子，多对象不原子；需要一致性就去看 `09-` 与 mnesia/外部 DB |

## 与其他章 / 其他书的联系

- 后续：`03-` 把进程包装成 `gen_server`，`06-` 把进程挂进监督树，`09-` 把节点连起来。
- 与 `book/多处理器编程的艺术2/`：艺术版 Ch4 讲顺序一致性与原子寄存器，回答"共享数据在没有锁时意味着什么"；本章的 ETS 则是**显式开了锁的共享数据**，两者的对照点集中在 `write_concurrency` 与 `decentralized_counters`。
- 与 `book/C++并发编程实战2/`：C++ 侧用 `std::atomic` 与锁达同一目标，风险点在**内存序与数据竞争**；Erlang 侧共享只在 ETS 这一个点，风险点在**锁策略与内存持有**。
- 与 `book/Java并发编程之美/`：Java 的 `ConcurrentHashMap` 之于 ETS，类似于 `synchronized` 之于消息传递——一个压进共享地址空间，一个绕开它。
