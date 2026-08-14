# C#

dotnet-csharp.pdf

https://learn.microsoft.com/zh-cn/dotnet/csharp/

C# 8推出

C# 11 包括对泛型数学、原始字符串字面量、文件范围类型和其他新功能的支持

.NET 7 支持 C# 11。

## 版本
11 .NET 7 支持 C# 11
https://learn.microsoft.com/zh-cn/dotnet/csharp/whats-new/csharp-11

10 .NET 6 支持 C# 10
https://learn.microsoft.com/zh-cn/dotnet/csharp/whats-new/csharp-10

9 .NET 5 支持 C# 9.0
https://learn.microsoft.com/zh-cn/dotnet/csharp/whats-new/csharp-9

8 发布日期：2019 年 9 月
https://learn.microsoft.com/zh-cn/dotnet/csharp/whats-new/csharp-version-history#c-version-80


C# 11 中增加了以下功能：
原始字符串字面量
泛型数学支持
泛型属性
UTF-8 字符串字面量
字符串内插表达式中的换行符
列表模式
文件本地类型
必需的成员
自动默认结构
常量 string 上的模式匹配 Span<char>
扩展的 nameof 范围
数值 IntPtr
ref 字段和 scoped ref
改进了方法组向委托的转换
警告波 7

ECMA-334_6th_edition_june_2022.pdf

## .NET Standard
.NET Standard 是针对多个 .NET 实现推出的一套正式的 .NET API 规范。

.NET 实现主要包括以下方面：

.NET Framework：它是.NET的最初实现，由微软开发，支持Windows操作系统。
.NET Core：它是.NET的跨平台实现，支持Windows、macOS和Linux操作系统。
Mono：它是.NET的开源实现，由Xamarin开发，支持Linux、macOS和Windows操作系统。
Xamarin：它是.NET的移动设备实现，支持iOS、Android和Mac OS X操作系统。
Unity：它是.NET的游戏开发实现，支持多种游戏开发平台和操作系统。
Blazor：它是.NET的Web开发实现，使用C#和HTML进行开发，支持在浏览器中运行。
这些实现都支持使用C#和F#等.NET语言进行开发，并提供了丰富的类库和开发工具。

## C# 与 .NET 综合笔记（截至 2026-08）

### 版本与平台边界

C# 是语言，.NET 是运行时、基础类库、SDK、编译器和部署工具链；不要把 `.NET Framework`、旧称 `.NET Core`、`.NET Standard` 与 C# 语言版本混为一谈。截至 2026-08，C# 14 对应 .NET 10。C# 语言版本可由 SDK/项目配置决定，目标框架（TFM，如 `net10.0`）决定可用运行时/API；二者相关但不是同一个概念。

`.NET Framework` 主要面向既有 Windows 应用，现代跨平台服务优先使用统一 .NET。`.NET Standard` 是 API 兼容规范而非运行时；新应用通常直接面向 `net8.0`、`net10.0` 等具体 TFM，只有需要同时支持旧 Framework 或多种旧实现的库才评估 `netstandard2.0`。Unity、Blazor、MAUI 等是使用 .NET/C# 的应用平台，不是与 .NET 并列的运行时实现。

当前参考：

- C# 文档：https://learn.microsoft.com/zh-cn/dotnet/csharp/
- C# 14 新特性：https://learn.microsoft.com/en-us/dotnet/csharp/whats-new/csharp-14
- .NET 目标框架：https://learn.microsoft.com/en-us/dotnet/standard/frameworks

### C# 14 与现代语言特性

C# 14/.NET 10 的重点包括 extension members、`field` 支持的属性后备字段、更多 `Span<T>`/`ReadOnlySpan<T>` 隐式转换、lambda 参数修饰符、更多 `partial` 成员和文件型应用相关预处理指令。它们提高表达力，不应为了“使用新语法”而破坏团队可读性或兼容较低 SDK 的构建。

现代 C# 的核心能力：nullable reference types 降低空引用风险；`record` 适合值语义 DTO；模式匹配提升分支可读性；泛型和约束实现可复用类型安全 API；`async`/`await` 管理异步 I/O；`Span<T>`、`Memory<T>`、`ref`/`in`/`out` 面向低分配热路径。语言特性并不自动改善架构，尤其 `async` 不能把阻塞 I/O 变成非阻塞。

```csharp
public sealed record CreateOrder(string OrderId, decimal Amount);

public async Task<Order> GetOrderAsync(string id, CancellationToken ct)
{
    var order = await repository.FindAsync(id, ct);
    return order ?? throw new KeyNotFoundException($"order {id} not found");
}
```

项目应启用 `<Nullable>enable</Nullable>` 并逐步消除警告，而不是到处使用 `!` 关闭检查。DTO 的必填性、反序列化、数据库空值和外部 API 仍需运行时校验；nullable 注解是静态分析契约，不是数据验证。

### 运行时、内存与异步并发

.NET 使用托管堆和分代 GC。短命对象主要进入 Gen 0，长期对象会提升代际；大对象、频繁分配、字符串拼接、闭包捕获、装箱和无界缓存可能导致 GC 压力。先用 `dotnet-counters`、`dotnet-trace`、PerfView/Profiler 或 OpenTelemetry 指标确认瓶颈，再考虑 `ArrayPool<T>`、`ObjectPool`、`Span<T>`、批处理或数据结构重构；对象池不是默认优化。

| 场景 | 建议 | 避免 |
| --- | --- | --- |
| 网络/数据库 I/O | 端到端 `async`，传递 `CancellationToken` | `.Result`、`.Wait()`、同步包裹异步造成线程池饥饿。 |
| CPU 密集工作 | 有界并发的 worker/`Parallel`，隔离资源 | 对每个请求盲目 `Task.Run`。 |
| 共享可变状态 | 不可变对象、`lock`、`Interlocked`、`Channel<T>` 等明确同步机制 | 认为 `volatile` 能解决复合操作或竞态。 |
| HTTP 服务 | `IHttpClientFactory`、超时、连接池、重试策略 | 每次请求 `new HttpClient()` 或无限重试。 |

`Task` 代表异步操作，不必然代表新线程。`async void` 仅适用于事件处理器；业务代码应返回 `Task`/`Task<T>`，使调用方能够 await、取消和观察异常。异常会在 `await` 时重新抛出，后台 fire-and-forget 任务若没有监督、日志和生命周期管理，失败将变得不可观测。

### ASP.NET Core、数据访问与部署

ASP.NET Core 服务的最小闭环是：配置绑定并校验、DI 生命周期正确、鉴权/授权、输入验证、统一错误响应、结构化日志、健康检查、指标/tracing、数据库迁移和优雅终止。Singleton 不可直接持有 Scoped 服务；DbContext 通常为 Scoped，避免跨线程复用。EF Core 能提升开发效率，但 N+1 查询、无索引过滤、过度 Include、隐式跟踪和大结果集仍需用 SQL/执行计划诊断。

发布方式可选 framework-dependent、self-contained、single-file、container 与 Native AOT。Native AOT 有启动和内存优势，但反射、动态加载、序列化和部分 ORM/插件生态需专门验证；不能把它当成所有 Web 服务的零风险开关。生产镜像固定 SDK/runtime 版本，使用非 root 用户，做 SBOM/漏洞扫描，并将配置与密钥从镜像分离。

### Java 开发者迁移与学习路径

| Java 概念 | C#/.NET 对应 | 注意 |
| --- | --- | --- |
| JVM/JDK | CLR/.NET SDK | 均有 GC/JIT，但工具链、运行时和部署模型不同。 |
| `CompletableFuture` | `Task`/`ValueTask` | 首选 `await` 组合，不要手写回调链。 |
| Spring DI | ASP.NET Core 内置 DI | 生命周期与扫描/容器能力不同。 |
| `Optional` | nullable 注解、模式匹配 | 不用 `null` 抑制符替代空值设计。 |
| Java Stream | LINQ | 延迟执行、表达式树和数据库翻译需分别理解。 |

学习顺序：语言基础和类型系统 -> `async`/取消/并发 -> ASP.NET Core 与 DI -> EF Core/SQL -> GC/诊断/发布。仓库中的 [Visual Studio](visualstudio.md)、[WPF](wpf.md)、[MSBuild](msbuild.md) 可辅助专项学习。面试或设计说明应能回答：异步链路如何取消、异常如何传播、对象生命周期如何管理、SQL 如何观测、扩容后 session/缓存如何处理，而不只罗列语法糖。
