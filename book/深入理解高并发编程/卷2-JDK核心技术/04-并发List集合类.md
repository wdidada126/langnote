# 第 4 章 并发 List 集合类

> `CopyOnWriteArrayList`：写时复制技术、初始化/添加/读取/修改/删除/遍历源码、使用案例。本书逐方法讲源码。与手册 7 章、之美 06/concepts 互补。

## 一、核心精讲

### 4.1 🔧 写时复制
- 写操作加锁复制整个数组（`Arrays.copyOf`），读持旧数组引用**无锁**（🔧 读多写少；写频繁 O(n) 拷贝 + 内存翻倍，OOM 风险）。

### 4.2 遍历弱一致
- 迭代器基于创建时的快照，不抛 `ConcurrentModificationException`（🔧 但看不到之后的新增；适合监听器列表、配置缓存）。

### 4.3 不适用
- 大列表高频写、要求实时读到最新（🔧 用 `ConcurrentLinkedQueue` 或锁 + `ArrayList`）。

## 二、版本演进 / 论文 / 前沿

- 文献：JDK 5 引入 COW；Lea JSR 166。
- 工业界：JDK `CopyOnWriteArrayList`；Vavr/持久化集合（结构共享，比 COW 高效）。
- 开源 stars（2026-09）：JDK 23.4k.

## 三、常见误区

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "COW 写多也行" | 仅读多写少 |
| 2 | "迭代会抛 CME" | 弱一致，不抛 |
| 3 | "COW 实时读最新" | 快照，滞后 |
