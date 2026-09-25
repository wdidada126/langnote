# 第 5 章 并发 Set 集合类

> `CopyOnWriteArraySet`（基于 COW List）、`ConcurrentSkipListSet`（基于跳表，有序）。本书逐类讲源码与案例。与手册 7 章、之美 09/concepts 互补。

## 一、核心精讲

### 5.1 🔧 CopyOnWriteArraySet
- 内部就是 `CopyOnWriteArrayList`，`add` 前查重（`indexOf`）再写时复制（🔧 读多写少的小集合；元素多时 add 是 O(n) 且复制，很慢）。

### 5.2 ConcurrentSkipListSet
- 基于 `ConcurrentSkipListMap`，无锁跳表，**有序**且高并发（🔧 需要有序/范围查询（`headSet`/`tailSet`/`ceiling`）时用它；无序去重小集合用 COW Set）。

### 5.3 无 ConcurrentHashSet
- JDK 没有 `ConcurrentHashSet`（🔧 用 `ConcurrentHashMap.newKeySet()` 或 `ConcurrentHashMap` 的 keySet 视图）。

## 二、版本演进 / 论文 / 前沿

- 论文：跳表（Pugh 1990）；Lea JSR 166。
- 工业界：JDK `ConcurrentSkipListSet`；eclipse-collections。
- 开源 stars（2026-09）：JDK 23.4k.

## 三、常见误区

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "有 ConcurrentHashSet" | 用 CHM.newKeySet() |
| 2 | "COW Set 元素多" | 慢，用 CHM |
| 3 | "Set 都无序" | SkipListSet 有序 |
