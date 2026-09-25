# 第 5 章 控制 OTP 行为

> **一句话**：第 5 章讲"**怎么从外面把一个行为的进程撬开**"——`sys` 模块、trace 函数、系统消息、spawn 选项、GC 与内存上限；这既是调试技术，也是把 OTP 行为变成可观测系统的接口层。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| `sys` 模块 | `sys:get_state/1,2`、`sys:replace_name/2`、`sys:handle_system_msg/5` | `sys` 是"行为进程与外界的后门"，也是自定义行为的兼容性保障 |
| 追踪与日志 | `dbg`、`redbug`、`trace/3`、`erlang:trace_pattern`、SASL | 生产环境要**低开销、可开关、有超时**的追踪，而不是长期开着 `dbg` |
| 系统消息 | 系统消息由行为进程**优先**处理，`gen_server` 自动接入 | 系统消息与普通消息共享邮箱，但优先级更高；写自定义行为时**必须**转发 |
| 你自己的 trace 函数 | `sys:handle_system_msg/6` 的扩展点 | 自定义行为若不做转发，会丢掉 trace 能力（可观测性黑洞） |
| 统计、状态与状态 | `sys:get_status/1`、`proc_lib:format/1`、crash report | crash report 是"崩溃后唯一有用的现场"，必须配置到 |
| `sys` 模块回顾 | 行为进程的状态机示意 | 行为 = 一个"带系统消息优先级的消息循环" |
| spawn 选项 | `#{priority/level, min_heap_size, min_bin_vheap_size, max_heap_size}` | 堆上限是**内存泄漏的最后一道闸**；优先级要慎用 |
| 内存管理与 GC | 分代 GC、进程私有堆、复制式清理、`persistent_term` | 内存不是"省出来的"，是"给它上限、让它早 GC" |

## 核心精讲

> 以下片段均为**教学示意代码，不参与编译、不参与任何构建**。

```erlang
%% ---- 1) 从外部撬开一个行为进程 ----
sys:get_state(Pid).                 %% 拿到行为内部状态（调试用，生产少用）
sys:get_status(Pid).                %% 含字典项与状态的结构
sys:replace_name(Pid, NewName).     %% 需要改名时的官方手段

%% ---- 2) 自定义行为必须转发系统消息，否则 trace/统计/重启全部失效 ----
-module(my_beh).
-export([handle_system_msg/6]).
handle_system_msg(Msg, Parent, Debug, Name, State, Mod) ->
    case Msg of
        get_state   -> sys:handle_system_msg(Msg, Parent, Debug, Name, State, Mod);
        _           -> %% 自定义处理，随后继续
                       Nxt = handle(Msg, State),
                       Mod:handle_system_msg(Msg, Parent, Debug, Name, Nxt, Mod)
    end.

%% ---- 3) 低开销追踪：dbg 的带超时调用，别长期开着 ----
dbg:tracer(),
dbg:p(self(), [c]),                                  %% 只追踪自己的进程
dbg:tpl(my_mod, my_fun, [{x, out}], []),             %% 带匹配条件
dbg:stop(),                                          %% 一定记得停

%% erlang:trace 更底层，适合长跑
erlang:trace(self(), true, [all, timestamp]),
erlang:trace_pattern({my_mod, my_fun, 1}, true, [return_to]),
```

spawn 选项：把"单个进程失控"变成"单个进程被杀"：

```erlang
%% 关键不是"能调大堆"，而是"能设上限并在超限时把它杀掉"
Pid = spawn_opt(fun work/0,
                [{max_heap_size, #{size => 32*1024*1024, kill => true,
                                   error_logger => false}}]),

%% 优先反直觉：high 会让普通进程"饿"，别在生产里凭感觉加
spawn_opt(fun cleanup/0, [{priority, high}]),

%% 长生命周期进程持有小 binary 时，最小 binary 堆很关键（省内存但也更慢）
spawn_opt(fun parser/0, [{min_bin_vheap_size, 1024*1024}]).
```

GC 与内存：BEAM 的 GC 是**分代 + 按进程私有堆复制式**，进程之间互不影响：

```erlang
%% 触发一次对该进程的 GC（生产里谨慎使用，会停顿）
erlang:garbage_collect(Pid),
erlang:garbage_collect(Pid, async).                  %% 异步 GC

%% 常驻不变的大只读数据用 persistent_term（OTP 21+），
%% 读它是**无需 GC 扫描**的，比 ETS 更省、比进程字典更规整
persistent_term:put(my_config, Config),
Cfg = persistent_term:get(my_config).
```

## 版本演进

| 版本 | 与本章相关的变化 |
| --- | --- |
| OTP 20（2016） | `max_heap_size` 支持 `kill` 选项，内存失控从"拖垮节点"变成"只杀一个进程" |
| OTP 21（2017） | `spawn_opt/3,4` 支持**用 map 一次传多个选项**；`min_bin_vheap_size`/`min_heap_size` 成为常规调优旋钮；`persistent_term` 登场 |
| OTP 22（2018） | dirty scheduler 体系成形（用于 NIF 的阻塞调用），本章"GC 与调度器交错"的讨论对象变复杂 |
| OTP 23（2019） | **移除 `scheduler_poll` 与 async I/O 的 dtrace/LTTng 探针**；trace 基础设施不再靠内核探针 |
| OTP 24 / 24.2（2020–2021） | dirty scheduler 的 allocator 可用 `+Mdai` 单独开启（默认关闭）；代码清理的并发请求数被限制为调度器数的 2 倍，避免"大量进程时代 purging 拖死响应性" |
| **OTP 26（2022）** | 新增 **`call_memory` trace**（按调用统计 GC 贡献）；**`erts_internal` 大量函数与调用被移除（潜在不兼容）**；`proc_lib:start*` 在子进程失败时同步失败 |
| OTP 27+（2023–2026） | `persistent_term` 与 `erts` 内存管理继续收敛；JIT 让"解释期开销"这一测量维度不再主导 |

## 经典论文与原始文献

| 论文 / 文献 | 出处 | 贡献 |
| --- | --- | --- |
| Wilson, Beam, Waddell, *Uniprocessor Garbage Collection Techniques* | IJPP 23(2), 1995 | 分代 GC、标记清扫 vs 复制、保守式收集的经典分类，是 BEAM 分代 + 复制式 GC 的背景 |
| Dijkstra, *The Structure of the THE Multiprogramming System* | CACM 8(5), 1965 | 分层抽象 + 周期性调度重排；本章"进程堆 GC 与调度器交错"的历史源头 |
| Sigelman et al., *Dapper, a Large-Scale Distributed Systems Tracing Infrastructure* | Google Technical Report dapper-2010-1, 2010 | 采样式低开销追踪的模型，今天所有 APM 的祖先 |
| Kreps, *The Log: What every software engineer should know about real-time data's unifying abstraction* | LinkedIn Engineering Blog, 2012 | 日志即数据流的观点，说明本章"日志"小节为什么值得单独一章篇幅 |
| Erlang/OTP *erts* / `sys` / `dbg` 文档与 release notes | erlang.org | spawn 选项、trace 探针、GC 参数的一手说明 |

## 近年研究与工业界开源实践（2015–2026）

趋势：2015 年之后服务端可观测性从"打日志 + 采样"走向 **OpenTelemetry 统一协议**；BEAM 侧也在 2021 年之后补齐了官方遥测基座（`telemetry`）与 OpenTelemetry 实现，使得本书"用 `fprof`/`dbg`/`Observer` 现场看"的旧范式被"先埋点、后下钻"的新范式部分替代。内存治理方面，从"调大堆"转向"设上限 + `persistent_term` + 分片"。

| 仓库 | star | 说明 |
| --- | --- | --- |
| `erlang/otp` | **12337★** | `erts`（GC、调度器、trace）与 `sys`/`dbg` 的一手实现 |
| `open-telemetry` 生态（`opentelemetry-erlang` 等 Hex 包） | Hex 分发为主 | OTP 的官方遥测基座由 `telemetry` 提供，OpenTelemetry 实现走 Hex |
| `rabbitmq/rabbitmq-server` | **13876★** | 把 `telemetry` 事件做成 Prometheus/Graphite exporter 的成熟样例 |
| `emqx/emqx` | **16755★** | 大规模 MQTT 集群的指标与追踪体系 |
| `elixir-lang/elixir` | **26677★** | `Observer`/`Telemetry` 在 Elixir 生态的等价实践 |
| `golang/go` | **138993★** | 对照：`pprof` 内建，语言层就有 tracing/CPU/heap 三类画像 |

## 常见误区与本书需修正之处

| 现象 | 说明 | 现状 / 修正 |
| --- | --- | --- |
| 🔧 **`sys:get_state/1` 长期开着** | 它会在行为进程里插入调试路径，生产长期调用有明显开销与安全面 | 只在排障时用；生产优先用 `telemetry`/结构化日志 |
| 🔧 **自定义行为不转发系统消息** | 少了 `sys:handle_system_msg/6` 转发，`sys` 的 trace、统计、`get_state` 全部失效，成为**可观测性黑洞** | 见上文代码；同时注意 `handle_common_reply` 一类宏也依赖转发 |
| 🔧 **长期开着 `dbg` 跑生产** | `dbg` 是调试工具，开销量级与 `erlang:trace(self(), true, [all])` 相近 | 用 `redbug` 或 `dbg:tpl` 加超时、加匹配条件，且**必须有 stop** |
| 🔧 **给所有进程设 `priority, high`** | 高优先级进程抢占低优先级，普通进程被饿死，表现为"整体更慢" | 只给真正的实时任务（如心跳、超时探测）用 |
| 🔧 **内存泄漏靠"调大堆"解决** | 堆越大 GC 停顿越长，节点越容易一起慢下来 | 用 `max_heap_size` + `kill => true` 把故障限制在单进程；单进程泄漏只是局部现象，积累到全节点就是故障 |
| **以为 GC 是全局停顿（stop-the-world）** | BEAM 按进程 GC，进程之间互不影响 | 反过来推论：进程越多，GC 越多但每次更短；进程越少，GC 更少但每次更长 |
| 🔧 **`persistent_term` 被当"只读缓存"滥用** | 写入 `persistent_term` **会触发全局 GC 扫描** | 只放"写一次、读很多"的少量固定数据；频繁写会拖慢全节点 |
| 🔧 **`erts_internal` 的旧调用** | OTP 26 移除了大量 `erts_internal` 函数与调用（自 OTP 24 起预告） | 依赖它的第三方库需升级；业务代码不应直接使用 |

## 与其他章 / 其他书的联系

- 前序：`03-` 定义行为，`04-` 提供"从外部观察与控制行为"的能力。
- 后续：`06-` 讲 supervisor 如何重启这些进程，`10-` 把这些观测手段升级成指标与熔断。
- 与 `book/多处理器编程的艺术2/`：艺术版 Ch16 讲 work-stealing 与调度，本章讲 BEAM 的调度与 GC 交互；**调度器是共享内存世界的隐形基础设施，在 Erlang 里则是可见的公共财产**。
- 与 `book/C++并发编程实战2/`：后者第 11 章讲 TSan/ASan 与性能回归；Erlang 没有数据竞争，但**有进程内存与邮箱增长**这两类专属问题。
- 与 `book/Java并发编程之美/`：Java 侧 GC 停顿是系统级 stop-the-world，Erlang 侧 GC 是进程级——这也是两种并发哲学在运维体验上最大的差异。
