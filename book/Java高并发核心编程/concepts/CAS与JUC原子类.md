# 卷2·CAS 原理与 JUC 原子类（尼恩）

> 卷2 第 3 章。CAS（`Compare-And-Swap`）三参数（地址/期望/新值）、CPU `lock cmpxchg`、ABA、`AtomicXxx`、自旋。本书独有「面试视角 + 多语言 CAS（C++/Go/PHP）」。详见《之美》concepts/CAS与原子操作.md（底层更细）。

## 一、核心精讲

### 1.1 🔧 CAS 三段式
- 读-算-写用一条原子指令完成；失败时自旋重试（🔧 高争用下自旋烧 CPU，需退避或改用 `LongAdder` 分段）。

### 1.2 多语言对照（尼恩强调面试会问）
- C++：`std::atomic::compare_exchange_weak`；Go：`sync/atomic` `CompareAndSwap`；PHP：`Swoole`/扩展提供；Rust：`AtomicU64::compare_exchange`（🔧 语义一致，内存序参数不同：Java 默认 seq-cst，C++ 可选 acquire/release/relaxed）。

### 1.3 ABA 与解决
- ABA：值 A→B→A，CAS 误判未变（🔧 `AtomicStampedReference` 加版本戳；或 `AtomicMarkableReference` 布尔标记）。

## 二、版本演进 / 论文 / 前沿

- 硬件：x86 `LOCK CMPXCHG`；ARM `LDREX/STREX`（LL/SC）。
- JDK：`Unsafe` 字段 CAS（JDK 21+ 废弃，JEP 471/498）→ `VarHandle`（5 档语义，见《之美》CAS 专篇）。
- 开源 stars（2026-09）：JDK 23.4k.

## 三、常见误区

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "CAS 不会失败" | 自旋重试，高争用烧 CPU |
| 2 | "不知 ABA" | 用戳版本号 |
| 3 | "直接 Unsafe" | 改 VarHandle |
