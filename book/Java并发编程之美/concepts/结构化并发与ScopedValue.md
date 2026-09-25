# 专篇：结构化并发与 ScopedValue

> 对应本书 1.11（`ThreadLocal`）、8（线程池）、10（同步器）的现代替代。
> **结构化并发是本书整套"线程/任务管理"范式的后继者**——
> 它把"并发任务的生命周期"约束到代码的**词法作用域**里，从而消灭孤儿线程与泄漏。

## 一、一句话概括

**结构化并发（Structured Concurrency）**：并发任务的生命周期必须**嵌套**在语法结构里——
一个作用域内 fork 出的所有子任务，**必须在该作用域退出前全部结束**（完成、失败或被取消）。

就像结构化编程消灭了 `goto`（控制流必须落在 `if`/`while`/函数这样的块里），
结构化并发要消灭的是"**fire-and-forget 的孤儿任务**"。

## 二、问题：非结构化并发的三大顽疾

```java
// 传统写法：两个任务并发，用 CountDownLatch 或 ExecutorService
ExecutorService pool = Executors.newFixedThreadPool(2);
Future<String> user  = pool.submit(() -> fetchUser());
Future<String> order = pool.submit(() -> fetchOrder());

String u = user.get();       // 若 user 抛异常...
String o = order.get();      // ...order 仍在后台跑，成为孤儿任务
```

| 顽疾 | 表现 |
| --- | --- |
| **孤儿任务** | 一个子任务失败/超时，其他子任务仍在后台运行，占资源、可能产生副作用 |
| **取消无法传播** | 父任务被取消，子任务收不到信号 |
| **异常聚合困难** | 多个子任务都失败时，只能拿到第一个 |
| **调用栈丢失** | 异步任务的栈与发起者无关，排查时看不出"谁发起的" |

## 三、结构化并发的解法（JDK 21+ 预览，JDK 25 仍预览）

```java
Response handle() throws ExecutionException, InterruptedException {
    try (var scope = StructuredTaskScope.open()) {     // ① 开作用域
        Subtask<String> user  = scope.fork(() -> fetchUser());    // ② fork 子任务
        Subtask<String> order = scope.fork(() -> fetchOrder());

        scope.join();                                   // ③ 等待全部完成

        return new Response(user.get(), order.get());   // ④ 取结果
    }
    // ⑤ 作用域退出：自动取消所有未完成的子任务，join() 保证不会有孤儿
}
```

**`try-with-resources` 是关键**：作用域的 `close()` 会：

1. 等待所有子任务结束（若 `join()` 未调用）
2. **取消**所有仍未结束的子任务
3. 等待它们响应取消

→ **退出这个代码块时，一定没有任何子任务还在跑。**

### 两种策略

```java
// ① ShutdownOnFailure：任一失败就取消其他（适合"要么全成要么全败"）
try (var scope = StructuredTaskScope.open(Joiner.awaitAllSuccessfulOrThrow())) {
    ...
}

// ② ShutdownOnSuccess：任一成功就取消其他（适合"竞速"，如多副本查询取最快）
try (var scope = StructuredTaskScope.open(Joiner.anySuccessfulResultOrThrow())) {
    Subtask<String> a = scope.fork(() -> queryReplicaA());
    Subtask<String> b = scope.fork(() -> queryReplicaB());
    scope.join();
    return (String) scope.result();     // 最快的那个
}
```

### 与虚拟线程的关系

`StructuredTaskScope` **默认在虚拟线程上运行** fork 出的任务——
两者是配套设计的：**虚拟线程让"每任务一线程"变廉价，结构化并发让"这些线程的生命周期"变可控**。

## 四、`ScopedValue`（JEP 506，JDK 25 GA）

结构化并发解决"任务生命周期"，`ScopedValue` 解决"**数据如何传给这些任务**"——
它是 `ThreadLocal` 在结构化并发下的替代品。

```java
private static final ScopedValue<User> CURRENT_USER = ScopedValue.newInstance();

void handleRequest(User user) {
    ScopedValue.where(CURRENT_USER, user).run(() -> {
        // 作用域内：CURRENT_USER.get() 返回 user
        processRequest();          // 内部（含嵌套调用）都可读
    });
    // 退出作用域：自动解绑，无需 remove()
}

// 需要返回值时用 call()
Result r = ScopedValue.where(CURRENT_USER, user).call(() -> compute());

// 多个值可链式绑定
ScopedValue.where(USER, u).where(TRACE_ID, tid).run(() -> handle());
```

**对比 `ThreadLocal`**：

| | `ThreadLocal` | `ScopedValue` |
| --- | --- | --- |
| 可变 | ✅ `set()` 任意改 | ❌ **不可变**（绑定后只读） |
| 解绑 | 手动 `remove()`，**极易遗漏** | **自动**（词法作用域退出） |
| 泄漏 | 线程池下高危 | **不可能**（结构保证） |
| 传递 | `InheritableThreadLocal`，线程池下失效 | **结构化并发下自动传给子任务** |
| 虚拟线程 | 内存代价大 | 优化过（内部用 carrier 的绑定） |
| 适用 | 需要可变状态（MDC、计数器） | 请求上下文、认证信息、TraceID |

> **分工建议**：
> - **只读的请求上下文**（用户、TraceID、Tenant）→ `ScopedValue`
> - **需要修改的状态**（MDC、累加器）→ 仍需 `ThreadLocal`，或改用显式参数/返回

## 五、`StructuredTaskScope` 的关键 API

```java
// fork 返回 Subtask（不是 Future）
Subtask<T> subtask = scope.fork(() -> work());

subtask.get();                    // 获取结果（未完成会抛 IllegalStateException）
subtask.state();                  // UNAVAILABLE / RUNNING / SUCCESS / FAILED
subtask.exception();              // 失败时的异常

// join 与超时
scope.join();                                    // 无限等
scope.joinUntil(Instant.now().plusSeconds(5));   // ⭐ 带 deadline（强烈推荐）

// 自定义 Joiner 可实现"收集所有结果"等策略
```

**⚠️ 务必用 `joinUntil` 而非 `join()`** —— 无限等待会重新引入"挂起"这个老问题。

## 六、JDK 版本演进（这个特性迭代极快，务必核对版本）

| 版本 | 状态 |
| --- | --- |
| JDK 19 | **JEP 428**：结构化并发首次孵化（API 为 `StructuredTaskScope` 早期形态） |
| JDK 20 | JEP 437：第二次孵化 |
| **JDK 21** | **JEP 453**：第一次预览（随虚拟线程 GA 一同发布） |
| JDK 22 | JEP 462：第二次预览 |
| JDK 23 | JEP 480：第三次预览 |
| JDK 24 | JEP 487：第四次预览（**API 大改**：`ShutdownOnFailure`/`ShutdownOnSuccess` 被 `Joiner` 取代） |
| JDK 25 | JEP 505：第五次预览（**仍在预览**） |
| **JDK 25** | 🔴 **JEP 506：`ScopedValue` GA**（转正） |

> ⚠️ **API 在 JDK 24 发生过一次破坏性变更**（从 `ShutdownOnSuccess`/`ShutdownOnFailure` 策略类
> 改为 `Joiner.awaitAllSuccessfulOrThrow()` / `Joiner.anySuccessfulResultOrThrow()`）。
> **网上大量 2023-2024 年的教程已过时**，请以当前 JDK 版本的 javadoc 为准。
> 且结构化并发**至今仍是预览特性**，生产使用需 `--enable-preview`。

## 七、经典论文 / 原始文献

| 主题 | 文献 / 规范 | 出处 |
| --- | --- | --- |
| **权威规范** | **JEP 505: Structured Concurrency (Fifth Preview)** | https://openjdk.org/jeps/505 |
| `ScopedValue` | **JEP 506: Scoped Values** | https://openjdk.org/jeps/506 |
| 起源 | **JEP 428: Structured Concurrency (Incubator)** | https://openjdk.org/jeps/428 |
| **核心思想出处** | **Najafzadeh, *Structured Concurrency*** —— Martin Sústrik（ZeroMQ 作者）的系列论述 | 该概念在 libdill（C）/ Trio（Python）/ Kotlin 协程中先行落地 |
| 学术形式化 | **de'Liguoro & Padovani, *A Foundation for Structured Concurrency*** | 相关类型系统工作见 Padovani 等关于"结构化并发的类型"的研究 |
| 结构化编程的原始论述 | **Dijkstra, *Go To Statement Considered Harmful*** | **CACM 11(3), 1968** —— 结构化并发的类比来源 |
| Kotlin 协程的结构化并发 | Kotlin 官方文档 *Coroutines: Structured concurrency* | 工业界最早大规模落地的结构化并发实现 |
| Python Trio | *Trio: structured concurrency for Python* | 该库的文档对"nursery"模型的论述极清晰 |

> **值得一读的类比**：结构化并发之于并发，正如 `goto` 之于控制流。
> Dijkstra 1968 年的那篇短文是理解"为什么要结构化"的最好入口。

## 八、工业界资料（非同行评审）

- **Kotlin 协程的 `coroutineScope` / `supervisorScope`**：结构化并发最早的工业级实现，
  `StructuredTaskScope` 的设计大量借鉴它。概念：子协程失败会取消整个 scope（`coroutineScope`）
  或不传播（`supervisorScope`）。
- **Python Trio 的 nursery 模型**：`async with trio.open_nursery() as nursery:` ——
  与 `try (var scope = ...) { scope.fork(...) }` 结构几乎一致。
- **Swift 的 `withTaskGroup`**：Swift 5.5+ 的结构化并发，也是同一思路。
- **Go 的 `errgroup`**：`golang.org/x/sync/errgroup` 提供了"任一失败取消全部"的近似语义，
  但**不是语言级的结构保证**（Go 仍有大量 goroutine 泄漏问题）。
- **OpenJDK Loom 项目页**：https://openjdk.org/projects/loom/

## 九、常见误区

1. **❌「结构化并发已经 GA 了」** —— 到 **JDK 25 仍是预览特性**，需 `--enable-preview`。只有 `ScopedValue` 在 JDK 25 转正。
2. **❌「`StructuredTaskScope` 能替代线程池」** —— 不能。它替代的是"**一组相关任务的生命周期管理**"；
   长期运行的服务、CPU 密集的后台计算仍需线程池。
3. **⚠️ API 在 JDK 24 变过** —— 旧教程里的 `ShutdownOnFailure` 已废弃，改用 `Joiner`（见第六节）。
4. **⚠️ 必须用 `joinUntil(deadline)`** —— 裸 `join()` 会重新引入无限挂起。
5. **❌「`ScopedValue` 完全替代 `ThreadLocal`」** —— 它**不可变**；需要修改值的场景（MDC、计数器）仍要 `ThreadLocal`。
6. **⚠️ `ScopedValue` 只在其动态作用域内可见** —— 若在其中 fork 了**非结构化**的任务（如提交到线程池），
   那个任务里 `get()` 会失败。必须配合 `StructuredTaskScope` 使用才能自动传递。
7. **⚠️ 取消是协作式的** —— `StructuredTaskScope` 关闭时会中断子任务，但**子任务必须响应中断**才会真正停止。
   不响应中断的任务仍会跑完（这是所有 Java 取消机制的共同限制）。
