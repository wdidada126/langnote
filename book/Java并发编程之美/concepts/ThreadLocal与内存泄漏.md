# 专篇：ThreadLocal 与内存泄漏

> 对应本书 1.11 节（基本用法）与 11.10 节（泄漏）。
> 这是 **Java 并发里最经典的生产事故**之一，也是虚拟线程时代必须重新审视的机制。

## 一、一句话概括

`ThreadLocal` 是「**每个线程一份独立副本**」的容器，实现为 `Thread` 对象内的一个 `ThreadLocalMap`。
泄漏的根源是：**线程池里的线程永远不销毁，而 `ThreadLocalMap` 的 key 是弱引用、value 是强引用**——
`ThreadLocal` 被 GC 后 key 变 `null`，但 value 仍被强引用，形成「永远访问不到又永远不释放」的内存。

## 二、结构与引用链

```java
// Thread 类内部
class Thread {
    ThreadLocal.ThreadLocalMap threadLocals = null;      // 普通 ThreadLocal
    ThreadLocal.ThreadLocalMap inheritableThreadLocals = null;  // 可继承的
}

static class ThreadLocalMap {
    static class Entry extends WeakReference<ThreadLocal<?>> {   // ⭐ key 是弱引用
        Object value;                                            // ⭐ value 是强引用
    }
    private Entry[] table;
}
```

引用链画图：

```
Thread (强, 线程池里永不销毁)
   └─→ threadLocals: ThreadLocalMap (强)
           └─→ Entry[] table (强)
                   └─→ Entry
                          ├─→ key:   WeakReference<ThreadLocal>  ─弱→  ThreadLocal 对象
                          └─→ value: 强引用 ──────────────────强→  你的对象（如 1MB 的 byte[]）
```

## 三、泄漏是怎么发生的（四步）

```java
void handleRequest() {
    threadLocal.set(new byte[1024 * 1024]);    // 1MB
    // ... 忘了 remove()
}
```

1. 线程池线程 T 执行任务，`ThreadLocalMap` 里加了一条 `Entry(TL → 1MB byte[])`
2. 任务结束，**线程 T 归还线程池，不销毁** → `threadLocals` 还在
3. 某个时刻 `TL` 这个 `ThreadLocal` 变量本身不再被引用（比如是方法内的局部变量，或类被卸载）→ **GC 回收 TL**
4. 于是 `Entry.key` 变成 `null`（弱引用被清理），**但 `Entry.value` 仍强引用着那 1MB**
   → 这 1MB **永远无法通过 `get()` 访问到**（key 是 null 了），**也永远不会被释放**（线程活着）

**每个请求泄漏 1MB × 线程池 200 线程 × 运行几天 = 堆 OOM。**

## 四、JDK 的"补救"及其局限

`ThreadLocalMap` 在 `set()` / `get()` / `remove()` 时**顺带做清理**（`expungeStaleEntry`）：

```java
private int expungeStaleEntry(int staleSlot) {
    Entry e = table[staleSlot];
    e.value = null;              // ⭐ 断开强引用，让 value 可被 GC
    table[staleSlot] = null;
    size--;
    // 并对后续连续段做 rehash 清理...
}
```

**为什么这不够？** 因为清理是**惰性、触发式**的：

- 只有再次访问**同一个 `ThreadLocalMap`** 且**哈希命中附近**时才会清理
- 如果某线程之后**再也不碰任何 `ThreadLocal`**，那条脏 Entry 会一直留到线程死亡
- 线程池线程恰恰符合「长期存活 + 可能不再访问 ThreadLocal」

> **结论：JDK 的清理是"尽力而为"，不是保证。根本解法仍然是显式 `remove()`。**

## 五、正确用法（三条防线）

```java
// ① 必须 remove()，放 finally
try {
    TL.set(ctx);
    doWork();
} finally {
    TL.remove();        // ⭐ 唯一可靠的防御
}

// ② 声明为 static final（避免 ThreadLocal 自身被 GC 导致 key 变 null）
private static final ThreadLocal<Ctx> TL = new ThreadLocal<>();
//  ⚠️ 用 ThreadLocal.withInitial() 更安全：
private static final ThreadLocal<Ctx> TL =
    ThreadLocal.withInitial(() -> new Ctx());

// ③ 不要往里面放大对象；不要放整个 Request/Session
```

> **为什么 `static final` 重要？**
> 如果 `ThreadLocal` 是**实例变量**或**局部变量**，它自己会被 GC → key 变 null → 脏 Entry。
> `static final` 让它与类同生命周期，key 不会变成 null（虽然 value 仍会随线程存活而泄漏，
> 但至少 `get()` 还能访问到、能 `remove()`）。

## 六、`InheritableThreadLocal`：另一个坑

```java
InheritableThreadLocal<String> TL = new InheritableThreadLocal<>();
TL.set("parent-value");
new Thread(() -> System.out.println(TL.get())).start();   // 子线程能看到 "parent-value"
```

**机制**：`Thread` 构造时会把父线程的 `inheritableThreadLocals` **浅拷贝**给子线程。

**四大坑**：

1. **只在线程创建时拷贝一次** —— 父线程之后改值，子线程看不到
2. **线程池下完全失效** —— 线程是预先创建的，拷的是"创建时"的值（通常是 null），且复用线程会**串数据**
3. **浅拷贝** —— 父子共享同一个对象引用，不是深拷贝
4. **异步框架下丢失** —— `CompletableFuture` / Reactor 的线程切换不会传递它

**正解**：用 **Alibaba TransmittableThreadLocal（TTL）** 或 JDK 21+ 的 `ScopedValue`。

## 七、虚拟线程时代：问题被放大，解法也变了

| 维度 | 平台线程 + 线程池 | 虚拟线程 |
| --- | --- | --- |
| 线程数量 | 几百 | **百万级** |
| `ThreadLocal` 内存 | 几百 × 每个 TL 大小 | **百万 × 每个 TL 大小** → 灾难 |
| 泄漏风险 | 高 | **极高** |
| 推荐替代 | `remove()` + `static final` | **`ScopedValue`**（JDK 25 GA） |

### `ScopedValue`（JEP 506，JDK 25 转正）

```java
private static final ScopedValue<User> CURRENT_USER = ScopedValue.newInstance();

void handle(User user) {
    ScopedValue.where(CURRENT_USER, user).run(() -> {
        // 作用域内可读
        process();                    // 内部可直接 CURRENT_USER.get()
    });
    // ⭐ 退出作用域自动清除，无需 remove，不会泄漏
}
```

对比：

| | `ThreadLocal` | `ScopedValue` |
| --- | --- | --- |
| 可变性 | ✅ `set()` 可改 | ❌ **不可变**（绑定后不能改） |
| 生命周期 | 与线程绑定，需手动清理 | **词法作用域**，自动清除 |
| 继承 | `InheritableThreadLocal`（有坑） | **结构化并发下自动传递** |
| 内存 | 每线程一份 | 更轻量，且自动回收 |
| 虚拟线程友好 | ❌ | ✅ |

> ⚠️ **`ScopedValue` 不是 `ThreadLocal` 的完全替代**：它**不可变**，
> 需要"在作用域内修改值"的场景（如 MDC、计数器）仍需 `ThreadLocal` 或其他方案。

## 八、JDK 版本演进

| 版本 | 变化 |
| --- | --- |
| JDK 1.2 | `ThreadLocal` 引入 |
| JDK 5 | `ThreadLocal.remove()` 加入（早期版本只有 `set` / `get`，泄漏更严重） |
| JDK 8 | `ThreadLocal.withInitial()`；`ThreadLocalMap` 清理逻辑改进 |
| JDK 21 | 🔴 虚拟线程 GA —— `ThreadLocal` 内存代价放大；`ScopedValue` 孵化（JEP 429） |
| JDK 22-24 | `ScopedValue` 持续预览 |
| **JDK 25** | 🔴 **`ScopedValue` GA**（JEP 506）—— `ThreadLocal` 的现代替代正式可用 |

## 九、经典论文 / 原始文献

| 主题 | 文献 | 出处 |
| --- | --- | --- |
| 线程局部存储的原始概念 | **Butterfield et al., *Thread-Local Storage in Programming Languages*** | 相关讨论见 GCC/ELF 的 TLS 规范；概念出自 1990 年代多线程系统的 ELF TLS 设计 |
| 弱引用的语义 | **Jones et al., *The Garbage Collection Handbook*（第 10 章）** | CRC 2011（第 2 版 2023）—— 弱/软/虚引用的权威说明 |
| 作用域绑定（ScopedValue 的学术前身） | **Najafzadeh, *Structured Concurrency***；另见 **Fluet et al., *Semantics of Future and Anomaly*** | 作用域限定的值绑定在函数式语言（如 Koka、OCaml 的 `let`）中历史悠久 |
| Java 侧的权威规范 | **JEP 506: Scoped Values** | https://openjdk.org/jeps/506 |
| 内存泄漏的实证研究 | 见 [11 章](../11-并发编程实践.md)：Lu et al., ASPLOS 2008 | — |

## 十、近年研究与工业界前沿（2020-2026）

**工业界资料（非同行评审）**

- **Alibaba TransmittableThreadLocal（TTL）**：国内最广泛使用的 `ThreadLocal` 跨线程池传递方案，
  解决了 `InheritableThreadLocal` 在线程池下失效的问题（通过包装 `Runnable`/`Callable` 在提交时快照、执行时恢复）。
  https://github.com/alibaba/transmittable-thread-local
  ⚠️ 它仍有**必须清理**的问题，且对虚拟线程支持需要额外注意。
- **Micrometer Context Propagation / Reactor Context**：响应式框架用自己的 `Context` 而非 `ThreadLocal`，
  因为线程会频繁切换。这是"放弃 ThreadLocal"的一条成熟路线。
- **SLF4J MDC 的 `ThreadLocal` 陷阱**：MDC 底层是 `ThreadLocal`（或 `InheritableThreadLocal`），
  在异步/线程池场景下**链路追踪 ID 会丢失**——这是分布式追踪最常见的"断链"原因。
  解法：TTL 或显式在任务提交时传递 MDC。
- **Spring Security `SecurityContextHolder`**：默认 `MODE_THREADLOCAL`，
  异步方法（`@Async`）里拿不到认证信息，必须配 `MODE_INHERITABLETHREADLOCAL` 或 `DelegatingSecurityContextRunnable`。

## 十一、常见误区（本书 1.11 / 11.10 需修正之处）

1. **❌「用完不 remove 也没事，反正线程会被回收」** —— **线程池线程永不回收**，这是泄漏的直接原因。
2. **❌「JDK 有弱引用就自动安全了」** —— 弱引用的是 **key**，**value 仍是强引用**，这才是泄漏的根源（见第三节）。
3. **⚠️ 必须 `static final`** —— 否则 `ThreadLocal` 自身被 GC 会让 key 变 null，连 `remove()` 的机会都没有。
4. **❌「`InheritableThreadLocal` 能在线程池里传值」** —— **完全不能**，线程是复用的（见第六节）。改用 TTL。
5. **⚠️ `remove()` 必须放 `finally`** —— 异常路径最容易漏。
6. **⚠️ 虚拟线程下优先考虑 `ScopedValue`** —— 百万级虚拟线程 × `ThreadLocal` 是不可接受的。
7. **❌「`ScopedValue` 能完全替代 `ThreadLocal`」** —— 它**不可变**，需要修改值的场景（MDC、计数器）不行。
8. **⚠️ 框架层的 `ThreadLocal` 泄漏你很难发现** —— MDC、Spring Security、各种 TraceContext 都可能泄漏；
   排查手段：heap dump 后看 `Thread.threadLocals` 里哪个 value 占了大量内存。
