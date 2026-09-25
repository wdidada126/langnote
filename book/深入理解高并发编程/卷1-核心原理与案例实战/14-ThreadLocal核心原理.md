# 第 14 章 ThreadLocal 核心原理

> `ThreadLocalMap`（线程私有）、弱引用 key 与内存泄漏、为什么必须 `remove()`、`InheritableThreadLocal`、线程池下 `Inheritable` 不继承。本书图解引用链与泄漏。详见《之美》concepts/ThreadLocal与内存泄漏.md、线程与并发编程实践 4 章。

## 一、核心精讲

### 14.1 🔧 内存泄漏
- `ThreadLocalMap` key 弱引用，线程池长生命线程 → value 强引用不回收（🔧 用完 `remove()` 在 finally；阿里规约强制）。

### 14.2 InheritableThreadLocal
- 子线程继承父线程值（🔧 但线程池复用线程，父子关系错乱；跨池传递用阿里 `TransmittableThreadLocal`）。

### 14.3 现代替代
- JDK 21 `ScopedValue`（JEP 506，不可变、无泄漏、结构化并发内安全继承）（🔧 见《之美》concepts/结构化并发与ScopedValue）。

## 二、版本演进 / 论文 / 前沿

- 文献：Lea 线程封闭（线程安全三策略之一）；JEP 506 ScopedValue。
- 工业界：`TransmittableThreadLocal`（阿里，跨线程池传递）。
- 开源 stars（2026-09）：JDK 23.4k.

## 三、常见误区

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "ThreadLocal 不漏" | finally 里 remove |
| 2 | "Inheritable 池内继承" | 用 TTL |
| 3 | "2026 还 ThreadLocal" | 结构化并发用 ScopedValue |
