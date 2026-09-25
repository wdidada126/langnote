# 第 3 章 volatile 为什么能解决可见性和有序性问题

> `volatile` 的两大语义：可见性（写立即刷主存、读绕过本地缓存）、有序性（禁止特定重排序 + 内存屏障）、不保证原子性。本书从「CPU 缓存一致性（MESI）+ 内存屏障」角度揭秘。详见《之美》concepts/volatile与内存可见性.md（含 x86 屏障成本表）。

## 一、核心精讲

### 2.1 🔧 可见性来源
- 写 volatile → 触发缓存一致性协议（MESI）使其他核缓存行失效 + 加**写屏障**刷主存；读 volatile → 加**读屏障**使本地缓存失效重读（🔧 x86 本身 TSO 强序，写屏障几乎免费，StoreLoad 才需 `mfence`/`lock`）。

### 2.2 有序性（happens-before）
- volatile 写-读建立 happens-before（🔧 禁止「volatile 写之后的代码」重排到写前、「volatile 读之前的」重排到读后——即 JMM 的 volatile 规则）。

### 2.3 不保原子
- `i++` 非原子（读-改-写），volatile 不救（🔧 用 `AtomicInteger` 或锁；或「volatile + 单写多读」模式仅保证可见）。

## 二、版本演进 / 论文 / 前沿

- 论文：JSR 133（Manson-Pugh-Adve POPL'05）、x86-TSO（Sewell CACM'10）、Adve-Hill DRF-SC（TPDS'93）。
- 工具：JOL、jcstress（验证 volatile 语义）。

## 三、常见误区

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "volatile 原子" | 仅可见+有序 |
| 2 | "任意平台无需屏障" | ARM 弱内存需真屏障 |
| 3 | "volatile 替代锁" | 复合状态仍要锁 |
| 4 | "DCL 不加 volatile" | 半初始化，必加 |
