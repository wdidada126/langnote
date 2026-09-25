# 第 10 章 CAS 核心原理

> CAS 三参数、CPU `lock cmpxchg`、ABA 问题、`AtomicXxx`、自旋开销、多语言 CAS（C++/Go/Rust）、`Unsafe`→`VarHandle`。本书图解 CAS 流程与 ABA。详见《之美》concepts/CAS与原子操作.md、高并发核心编程 concepts/CAS与JUC原子类.md。

## 一、核心精讲

### 10.1 🔧 CAS 自旋
- 读-算-写用一条原子指令；失败重试（🔧 高争用烧 CPU；退避或 `LongAdder` 分段）。

### 10.2 ABA + 解决
- A→B→A 误判未变（🔧 `AtomicStampedReference` 戳版本；或 `AtomicMarkableReference`）。

### 10.3 多语言
- C++ `compare_exchange`、Go `atomic`、Rust `compare_exchange`（🔧 内存序参数不同；Java 默认 seq-cst）。

## 二、版本演进 / 论文 / 前沿

- 论文：Herlihy Wait-Free（PODC'91）；x86 指令集。
- 工业界：JDK `VarHandle`；JCTools 无锁。
- 开源 stars（2026-09）：JDK 23.4k.

## 三、常见误区

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "CAS 不失败" | 自旋烧 CPU |
| 2 | "不知 ABA" | 戳版本号 |
| 3 | "直接 Unsafe" | VarHandle |
