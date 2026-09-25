# 第 3 章 Java内存模型（原书第 2 版 pp.59-98）

> 与《实战》第 16 章、《之美》`concepts/JMM与happens-before.md` 互补。本书特色：**从 as-if-serial → happens-before → 内存语义（volatile/锁/final）→ 重排序 → 顺序一致性**逐层拆，并给出处理器层面的重排类型表。

## 一、本章地图

| 主题 | 关键结论 |
| --- | --- |
| 并发抽象 | 线程通信（共享内存/消息传递）+ 线程同步 |
| `as-if-serial` | 单线程内重排不得改变"串行语义结果" |
| 重排序 | 编译器/处理器/内存系统三级重排；数据依赖保序 |
| `happens-before` | JMM 核心偏序；八规则（与《实战》16 章一致） |
| `volatile` 内存语义 | 写→读 建立 happens-before；禁止特定重排（插入屏障） |
| `锁` 内存语义 | `unlock` happens-before 后续 `lock`；可见性保证 |
| `final` 语义 | 正确构造的 final 字段跨线程可见（JSR 133 修复） |
| `happens-before` 设计 | 程序员好懂 × 编译器能优化 的折中 |

## 二、核心精讲

### 2.1 重排序的三类来源
1. **编译器重排**（JIT）：在不破坏数据依赖前提下重排指令。
2. **处理器重排**：流水线/乱序执行 → ILP（指令级并行）。
3. **内存系统重排**：写缓冲（store buffer）、无效队列导致"其他 CPU 看到顺序不同"。
- JMM 用 **happens-before** 把"允许重排"框定在"不改变正确同步程序的可观察行为"内。

### 2.2 `as-if-serial` vs `happens-before`
- `as-if-serial`：单线程视角——重排对你"好像"没发生（结果一致）。
- `happens-before`：多线程视角——若 A hb B，则 A 的结果对 B **可见且有序**。
- 二者关系：单线程内天然存在 program-order hb；跨线程必须靠 volatile/锁/线程启动等显式建立 hb。

### 2.3 `volatile` 的内存语义（本书给出"屏障插入策略"）
- 线程 A 写 `volatile` 变量 → 把本地修改刷主存；线程 B 读 → 从主存取且令本地缓存行失效。
- **JMM 的屏障策略**（本书表格）：写后插 `StoreStore`+`StoreLoad`、读前插 `LoadLoad`+`LoadStore`，阻止特定重排。
- 注意：x86 本身禁止 `StoreLoad` 之外的多数重排，所以 x86 上 `volatile` 主要成本在 `StoreLoad`（一个 `lock` 前缀/MFENCE）。ARM 上则全部屏障都实打实存在。

### 2.4 `final` 的重排约束（JSR 133）
- `final` 字段的写**禁止重排到构造函数之外**（即构造完成后才能被其他线程看到），保证"看到的对象字段已初始化"。
- 🔧 前提：**构造器内 `this` 不泄漏**；若泄漏，final 保证也救不了。

### 2.5 顺序一致性（Sequential Consistency）模型
- 理想模型：所有操作全局单一顺序、且每个线程内顺序与程序序一致。
- JMM **不是**顺序一致性（为性能允许重排），但通过 happens-before 保证"正确同步的程序"具有**顺序一致性效果**（DRF-SC 定理，Adve & Hill）。

## 三、版本演进

- **JDK 1.0–1.4**：无正式 JMM，行为各 JVM 不一致。
- **JDK 5 (JSR 133, 2004)**：正式 JMM，`volatile` 升级为 acquire/release 语义，`final` 补安全发布保证。
- **JDK 9 (VarHandle)**：plain/opaque/acquire/release/volatile 五档，程序员可精确选屏障强弱（比"全用 volatile"更省）。
- **JDK 21-25**：`Unsafe` 废弃 → 内存屏障走 `VarHandle`/`MemorySegment`；`ScopedValue`（JEP 506, JDK 25 GA）提供更安全的"不可变上下文发布"。

## 四、经典论文 / 原始文献

- **Manson, Pugh, Adve, "The Java Memory Model" (POPL 2005)**——JSR 133 形式化（必读）。
- **Lamport, "Time, Clocks, and the Ordering of Events..." (CACM 1978)**——happened-before 概念源头。
- **Lamport, "How to Make a Multiprocessor Computer That Correctly Executes Multiprocess Programs" (1979)**——顺序一致性定义。
- **Adve & Hill, "Weak Ordering—A New Definition" (ISCA 1990) / "A Unified Formalization" (TPDS 1993)**——DRF-SC 定理（JMM 哲学基础）。
- **Adve & Gharachorloo, "Shared Memory Consistency Models: A Tutorial" (IEEE Computer 1996)**——从 SC 到 release consistency 的桥梁。
- **Sewell et al., "x86-TSO" (CACM 2010)** / **Alglave et al., "Herding Cats" (TOPLAS 2014)**——硬件层重排的严格定义。

## 五、工业界前沿（同《实战》16 章，此处强调验证工具）

| 项目 | Stars | 关联 |
| --- | --- | --- |
| **openjdk/jcstress** | 2.1k | **专门模糊测试** JMM：volatile/final/happens-before 的真实重排行为 |
| **openjdk/jol** | 2.1k | 字段布局/对齐 → 理解伪共享如何破坏"看似无关的 volatile" |
| **herd7 / diy7** | — | litmus 形式化弱内存交错（x86-TSO vs ARM） |
| **openjdk/jdk** | 23.4k | `VarHandle` 五档语义、`MemorySegment` |

## 六、常见误区 / 本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "happens-before = 时间先后" | 是偏序，允许重排；只约束可见性与顺序一致 |
| 2 | "`volatile` 原子" | 只可见+有序；`i++` 非原子 |
| 3 | "x86 跑过就安全" | ARM 弱内存会暴露重排；多架构 CI + jcstress |
| 4 | "final 一定安全" | 构造器 `this` 泄漏则失效 |
| 5 | "全用 volatile 最稳" | 过度屏障伤性能；`VarHandle` 按需选档 |
