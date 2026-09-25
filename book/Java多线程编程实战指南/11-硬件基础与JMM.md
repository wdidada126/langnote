# 第 11 章 多线程编程的硬件基础与Java内存模型（原书 pp.378-414）

> **本书补强章**：从 CPU 缓存一致性、内存屏障讲到 JMM——比《艺术》3 章更偏"硬件→模型"的推导。与《艺术》2/3 章 + 《实战》16 章互补，本书重"硬件为什么需要 JMM"。

## 一、本章地图

| 主题 | 关键 |
| --- | --- |
| CPU 缓存层级 | L1/L2/L3、缓存一致性（MESI） |
| 写缓冲/无效队列 | 可见性延迟的根源 |
| 重排序 | 编译器/处理器/内存系统三级 |
| 内存屏障 | 禁止特定重排（LoadLoad/StoreStore/...） |
| JMM | happen-before 偏序；as-if-serial |
| 顺序一致性 | DRF-SC 定理 |

## 二、核心精讲

### 2.1 硬件为什么需要 JMM
- 多核各有 L1/L2，共享 L3/内存；写经写缓冲、读经无效队列 → 其他核"看到"的顺序与程序序不同。
- 缓存一致性协议（MESI/MESIF/MOESI）保证最终一致，但有传播延迟 → 需要屏障约束。

### 2.2 重排序三级
- 编译器（JIT）、处理器（乱序执行/流水线）、内存系统（写缓冲/无效队列）。JMM 用 happen-before 框定"允许重排"的范围。

### 2.3 内存屏障（与《艺术》2/3 章一致）
- `LoadLoad`/`StoreStore`/`LoadStore`/`StoreLoad`；x86 仅 `StoreLoad` 实打实存在（其余被硬件禁止），ARM 全有。
- `volatile` 写插 `StoreStore`+`StoreLoad`，读插 `LoadLoad`+`LoadStore`。

### 2.4 JMM 与 DRF-SC
- `happen-before` 偏序（八规则）；正确同步的程序具有顺序一致性效果（DRF-SC 定理，Adve & Hill）。
- `final` 安全发布（JSR 133）；DCL 必须 `volatile`。

## 三、版本演进

- **JDK 5 (JSR 133)**：正式 JMM。**JDK 9**：`VarHandle` 五档语义。**JDK 21+**：`Unsafe` 废弃；`ScopedValue`（JDK 25）。

## 四、经典论文 / 原始文献

- **Lamport, "Time, Clocks..." (1978)** / "How to Make a Multiprocessor..." (1979)。
- **Adve & Hill, "Weak Ordering" (ISCA 1990) / "A Unified Formalization" (TPDS 1993)**——DRF-SC。
- **Sewell et al., "x86-TSO" (CACM 2010)** / **Alglave et al., "Herding Cats" (TOPLAS 2014)**。
- **Manson-Pugh-Adve (POPL 2005)**——JSR 133 形式化。

## 五、工业界前沿

| 项目 | Stars | 关联 |
| --- | --- | --- |
| **openjdk/jcstress** | 2.1k | JMM 模糊测试 |
| **openjdk/jol** | 2.1k | 字段布局/伪共享 |
| **herd7/diy** | — | 弱内存 litmus |
| **openjdk/jdk** | 23.4k | `VarHandle`/`MemorySegment` |

## 六、常见误区 / 本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "happen-before = 时间先后" | 偏序，允许重排 |
| 2 | "volatile 原子" | 只可见+有序 |
| 3 | "x86 跑过就安全" | ARM 弱内存翻车；多架构 CI |
| 4 | "final 一定安全" | 构造器 this 泄漏则失效 |
| 5 | "全用 volatile 最稳" | VarHandle 按需选档更省 |
