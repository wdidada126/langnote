# 第 9 章 图形用户界面应用程序（原书 pp.211-226）

> **本书唯一一章"看起来过时、但思想完全没过时"的内容。**
> Swing 已不再是主流，但"**GUI 必须单线程**"这条规则
> 在 Android、JavaFX、Web 前端、Flutter、SwiftUI 上**原封不动地延续了下来**。
> 本章是理解"**单线程封闭 + 后台执行 + 回到主线程更新**"这套范式的最佳教材。

## 一、本章地图

```
为什么 GUI 要用单线程？（两个原因）
        ↓
串行事件处理：EDT（事件分发线程）
        ↓
线程封闭在 GUI 中的应用：所有组件只由 EDT 碰
        ↓
长时间任务：后台 Executor + invokeLater 回主线程
        ↓
进度、取消、共享数据模型（TableModel/TreeModel）
        ↓
跨框架对照：SWT / JavaFX / Android / Web / Swift / Flutter
```

## 二、为什么 GUI 是单线程的（pp.211-214）

| 原因 | 说明 |
| --- | --- |
| ① **顺序事件处理的需求** | 鼠标点击、键盘输入、重绘事件必须**按发生顺序**处理；多线程会让"先按下的键后处理" |
| ② **大量共享可变状态 + 复杂的锁顺序** | GUI 组件构成**树形结构**，父子互相引用；到处加锁必然产生**锁顺序死锁** |

> 本书 pp.212 给出的经典死锁：一个线程从**顶层向下**遍历组件树并加锁，
> 另一个从**底层向上**遍历 → 死锁。**不用锁而用"线程封闭"才是解法。**

**结论**：**GUI 对象的所有访问都必须在单一线程（事件线程）内完成** ——
这就是第 3 章"线程封闭"在 GUI 领域的极致应用。

## 三、串行事件处理（pp.214-218）

| 框架 | 事件线程 | 从后台回到事件线程 |
| --- | --- | --- |
| **Swing** | **EDT（Event Dispatch Thread）** | `SwingUtilities.invokeLater(Runnable)` / `invokeAndWait(Runnable)` |
| **SWT** | Display 线程 | `Display.asyncExec(Runnable)` / `syncExec(Runnable)` |
| **JavaFX** | **Application Thread** | `Platform.runLater(Runnable)` |
| **Android** | **主线程 / UI 线程**（`Looper.getMainLooper()`） | `Activity.runOnUiThread()` / `View.post()` / `Handler` |
| **Web（浏览器 JS）** | 单线程事件循环 | 本来就在主线程；重活放 **Web Worker**（但不能碰 DOM） |
| **SwiftUI/UIKit** | **Main Actor**（`@MainActor`） | `DispatchQueue.main.async` / `await MainActor.run { }` |
| **Flutter** | UI isolate 的主事件循环 | `MessageChannel` / `compute()` |

```java
// Swing：后台算，回到 EDT 更新
button.addActionListener(e -> {
    executor.execute(() -> {          // ① 后台
        Result r = heavyWork();
        SwingUtilities.invokeLater(() -> label.setText(r.text()));  // ② 回 EDT
    });
});
```

**`invokeLater` vs `invokeAndWait`**：

| 方法 | 行为 | 风险 |
| --- | --- | --- |
| `invokeLater` | 异步投递，立即返回 | ✅ 推荐 |
| `invokeAndWait` | **阻塞**直到 EDT 执行完 | ⚠️ **可能死锁**：从 EDT 里调用它必然死锁 |

## 四、线程封闭在 GUI 中的应用（pp.218-221）

> **规则**：除了 EDT，**任何线程都不应该访问 GUI 组件**（包括读取）。

| 容易违反的场景 | 正确做法 |
| --- | --- |
| 后台线程直接 `label.setText(...)` | 用 `invokeLater` 包起来 |
| 后台线程读 `textField.getText()` | 也要在 EDT 里读 |
| 后台线程遍历组件树 | 禁止；把需要的数据**提前**取出来作为参数传入 |

> **在 Android 上这条规则被写进了框架**：
> `ViewRootImpl` 会检查调用线程，非主线程操作 UI 会抛
> **`CalledFromWrongThreadException`**；主线程做网络 I/O 会抛
> **`NetworkOnMainThreadException`**（StrictMode）。

## 五、长时间运行的任务（pp.221-224）

本书给出的完整骨架（取消 + 进度 + 完成，三态）：

```java
// 本书 pp.221 的骨架（现代改写）
class BackgroundTask {
    private Future<?> running;
    void start() {
        if (running != null) return;                    // 防止重复启动
        running = executor.submit(() -> {
            while (moreWork() && !Thread.currentThread().isInterrupted()) {
                doOneUnit();
                SwingUtilities.invokeLater(() -> progressBar.setValue(percent()));
            }
            SwingUtilities.invokeLater(this::onDone);   // 完成也要回 EDT
            running = null;
        });
    }
    void cancel() { running.cancel(true); }             // 第 7 章的中断
}
```

| 要素 | 说明 |
| --- | --- |
| **进度反馈** | 必须用 `invokeLater` 回 EDT；不要高频刷（会淹没事件队列） |
| **取消** | `Future.cancel(true)`；循环里检查 `isInterrupted()` |
| **完成** | 同样走 `invokeLater` |
| **重复启动保护** | 用一个 `Future` 字段做守卫 |

> **替代品**：Swing 有 `SwingWorker`（JDK 6 引入，把上面这套封装好了）；
> Android 有 `AsyncTask`（**已废弃**）→ 现在是 **Kotlin 协程 + `Dispatchers.Main`**；
> JavaFX 有 `Task` + `Service`。

## 六、共享数据模型（pp.224-226）

| 模型 | 说明 |
| --- | --- |
| **`TableModel` / `TreeModel`** | 数据模型；**事件（增/删/改）必须在 EDT 里触发** |
| **拆分型模型（split model）** | 后台线程持有数据的"真实副本"，EDT 持有"视图副本"，两者通过事件同步 |
| **线程安全的数据模型** | 也可以把模型本身做成线程安全（用 `ConcurrentHashMap` 等） |

> **本书 pp.225 的建议**：最简单可靠的做法是
> **让模型本身线程安全 + 把"变更事件"投递到 EDT**，而不是手工做双份数据。

## 七、JDK 5 → 25 与跨平台演进

| 本书论断 | 2020s 的状态 |
| --- | --- |
| "Swing 是主流 GUI 工具包" | Swing 仍在维护但已不是新项目首选；**JavaFX** 是 Java 的现代 GUI |
| "用 `SwingWorker`" | JavaFX 用 `Task`/`Service`；Android 用 **Kotlin 协程** |
| "用 `invokeLater` 回 EDT" | 每个框架都有对应物（`Platform.runLater` / `runOnUiThread` / `DispatchQueue.main`） |
| 手工检查"是不是在 EDT" | **Android 有框架级检查**；Swift 有 **`@MainActor`（SE-0316 Global Actors）编译期强制**；Java 只能靠 `SwingUtilities.isEventDispatchThread()` 自查 |
| 用 `Executor` 跑后台 | 同样；**JDK 21+ 可用虚拟线程**（但注意：EDT 仍是平台线程） |

### 7.1 现代范式对照表

| 平台 | 后台单元 | 回到主线程 | 是否编译期强制 |
| --- | --- | --- | --- |
| Swing | `Executor` / `SwingWorker` | `invokeLater` | ❌（靠 `assert isEventDispatchThread()`） |
| JavaFX | `Task` / `ExecutorService` | `Platform.runLater` | ❌ |
| **Android（Kotlin）** | **协程 `Dispatchers.Default`** | `Dispatchers.Main` / `withContext(Dispatchers.Main)` | ❌（但 `Main` dispatcher 几乎零成本切换） |
| **Swift** | `Task` / `TaskGroup` | **`@MainActor`** | ✅ **编译期检查**（Swift 5.5+） |
| Rust（GUI 生态） | `tokio` / `std::thread` | 主线程消息循环 | ⚠️ 部分靠 `Send`/`!Send` 类型约束 |
| Web | **Web Worker** | `postMessage` | ✅ 结构上强制（Worker 不能碰 DOM） |

> **趋势**：从"**运行时约定 + 抛异常**"走向"**编译期强制**"（`@MainActor`、Rust 的 `Send`）。
> 这正是第 3 章"把线程封闭写进文档"这一主张的现代化终点。

## 八、经典论文 / 原始文献

| 文献 | 贡献 |
| --- | --- |
| **Myers, B. A. & Rosson, M. B. 1992. "Survey on User Interface Programming." CHI '92, pp. 195-202.** | 系统研究 UI 编程的困难，**指出事件驱动 + 回调模型是主要痛苦来源**——与本章"单线程封闭"形成对照 |
| **Hoare, C. A. R. 1974. "Monitors." CACM 17(10).** | 管程；GUI 事件队列的并发抽象基础 |
| **Brinch Hansen 1973《Operating System Principles》** | 管程的并行发明 |
| **Dijkstra 1968 "Go To Statement Considered Harmful"** | 本书"事件回调 = 并发里的 goto"这一后来观点的源头（见结构化并发篇） |
| **Swift Evolution SE-0316 "Global Actors" / SE-0304** | `@MainActor` 与结构化并发的官方提案 |
| **Android 官方文档 "Processes and Threads"** | 主线程模型与 `CalledFromWrongThreadException` 的权威说明 |
| **Oracle Java Tutorial: "Concurrency in Swing"** | Swing 单线程规则的官方教程 |

## 九、近年研究与工业界前沿

### 近年研究

- **UI 响应性（responsiveness）的可量化定义**：近年 HCI 研究把"响应性"与"感知延迟阈值（约 100ms）"挂钩，并研究如何在不阻塞事件循环的前提下做增量渲染（React 的 concurrent rendering、SwiftUI 的 async 渲染即工业答案）。
- **结构化并发进入 GUI**：`async let` / `TaskGroup` / 协程让"后台任务 + 取消 + 回到主线程"的生命周期与**视图生命周期**绑定（如 Android `viewModelScope`、Swift `.task {}` 修饰符）——这正是本书"任务生命周期管理"思路的现代化。
- **主线程的编译期安全**：`@MainActor`（Swift）与 Rust 的 `Send` 把本章的"规则"变成了"类型"。

### 工业界开源实现

| 项目 | Stars | 与本章关系 |
| --- | --- | --- |
| **Kotlin/kotlinx.coroutines** | 13.8k | **`Dispatchers.Main` + `viewModelScope`**：Android 上本章范式的现代实现 |
| **openjdk/jfx**（JavaFX） | — | `Platform.runLater`、`Task`、`Service` |
| JetBrains Compose Multiplatform | — | 声明式 UI；单线程模型 + 协程 |
| Swift `swift-async-algorithms` | — | `@MainActor` 与异步序列 |

## 十、常见误区 / 本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "GUI 组件加锁就能多线程访问" | 组件树是嵌套结构 → **必然死锁**；用**线程封闭**（只由 EDT 访问） |
| 2 | "从 EDT 里调用 `invokeAndWait` 没问题" | **必然死锁**（EDT 等自己） |
| 3 | "后台线程读一下组件的值没关系" | 也是违反封闭；读到的是不一致的中间状态 |
| 4 | "`SwingWorker` 过时了" | 仍然可用；只是 JavaFX/Android 有更现代的对应物 |
| 5 | "Android 的 `AsyncTask` 还能用" | **已废弃**（易泄漏 Activity）；用协程 + `viewModelScope` |
| 6 | "Java 有编译期检查防止跨线程改 UI" | **没有**；只能自查 `isEventDispatchThread()`（Swift 的 `@MainActor` 才有编译期检查） |
| 7 | "进度更新越频繁越好" | 高频 `invokeLater` 会**淹没事件队列**，导致 UI 更卡；要节流 |
| 8 | "后台跑完直接改 UI" | 必须回到事件线程（每个框架都有自己的 `runLater`） |
| 9 | "Web Worker 可以直接改 DOM" | **不能**；只能通过 `postMessage`（结构上的强制封闭） |
| 10 | "GUI 单线程规则只适用于桌面" | 同样适用于 **Android / iOS / 浏览器 / Flutter**——是**普适**的 |
