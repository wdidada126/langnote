# L18 双向链表 DLList（哨兵、prev/next 与接口设计总结）

> 对应 spring2024 L18：DLList 实现、哨兵节点、线性表设计复盘。作业：Project1a 发布。项目对应：projects/dllist。

## 1. 核心概念

- **动机**：SLList 只能向前；删除已知节点、倒序遍历、两端操作都需要 `prev`。
- **节点与不变量**：
  ```java
  private class Node {
      T item; Node prev, next;
      Node(T i, Node p, Node n) { item = i; prev = p; next = n; }
  }
  // 哨兵：p61b.util 惯例——sentinel.next 是首元素，sentinel.prev 是尾元素
  private final Node sentinel = new Node(null, null, null);
  DLList() { sentinel.next = sentinel; sentinel.prev = sentinel; size = 0; }
  ```
  空表时哨兵自环；**任何节点 prev/next 永不为 null**，特判归零。
- **插入/删除是"缝合四根线/改两根线"**：
  ```java
  void add(T x) { // addLast
      Node tail = sentinel.prev;
      Node n = new Node(x, tail, sentinel);
      tail.next = n; sentinel.prev = n; size++;
  }
  static void unlink(Node p) { p.prev.next = p.next; p.next.prev = p.prev; }
  ```
- **接口设计总结（L8–L18 收口）**：线性表 API = List（随机访问 + 两端）；按复杂度承诺选实现：随机访问→ArraySeq，频繁两端插删→DLList/ArrayDeque。

## 2. 实现检查清单

1. 双向不变量测试：对任意 p，`p.next.prev == p && p.prev.next == p`（测试里遍历全表断言，Lab/Project1 常用）。
2. 删除唯一节点：`sentinel.next == sentinel.prev == n`，缝合后哨兵自环——哨兵写法天然覆盖。
3. 迭代器 fail-fast：记录 `modCount`，`next()` 时发现结构修改抛 `ConcurrentModificationException`（JDK 同款）。
4. 不要用 DLList 做随机访问容器：`get(i)` 需决定前进还是后退（JDK LinkedList 就做了 `i < size/2 ? 前进 : 后退` 的补偿）。

## 3. 复杂度视角

| 操作 | DLList(哨兵) | SLList | ArraySeq |
| --- | --- | --- | --- |
| addFirst/addLast | Θ(1) | Θ(1) | Θ(1) 摊还（尾）/Θ(n)（头） |
| removeFirst/Last | Θ(1) | Last Θ(n) | Θ(1)/Θ(1) |
| get(i) | Θ(min(i, n−i)) | Θ(i) | **Θ(1)** |
| remove(已知迭代器位置) | Θ(1) | Θ(n)（找 prev） | Θ(n) |
| 内存/节点 | 2 指针 ~+8B vs SLList | | 无指针但扩容复制 |

## 4. 与前后讲联系

- 上承 L16–L17 的"数组/链表互补"，本讲把链表补到"两端 + 回溯"全 O(1)。
- 下启：L19 ArrayDeque 是"数组路线"对两端 O(1) 的答卷；L21 HashMap 的桶内结构（JDK8 后链长 >8 转树，用的正是本讲的"双向 + 可 O(1) 摘除"理由）；L28 堆不涉及，但 L36 Trie 的 children 常挂链表。

## 5. 跨课程联系

- **CS61A**：61A 无双向链表（不可变世界不需要 prev 回溯删除）；61B 用"可变对象 + 双指针"展示命令式数据结构为何存在。
- **CSAPP**：双指针 = 节点膨胀到 ~40B/元素；遍历时每元素 2 次依赖 load，cache 命中率比数组低一个数量级——但换来 O(1) 拼接，Linux `list_head` 因此成为内核默认容器。
- **OS/15-445**：LRU 缓存 = HashMap + DLList（O(1) 查 + O(1) 移动到头部），Redis `evict` 与 15-445 LRU-K replacement 都是这个组合；这是"数据结构组合出 O(1) API"的第一课。
- **DDCA**：双向链表硬件化即总线仲裁链（daisy chain + 回传）。

## 6. 开源项目应用

- **JDK**：`java.util.LinkedList`（Deque+List 双身份，带哨兵字段 `header` 风格实现）；`AbstractSequentialList` 让子类只写 `listIterator(i)` 即得全部 List API——L18 接口设计的收官示范。
- **Linux 内核**：`struct list_head` 侵入式双向环（task_struct 挂调度队列、LRU 页链），无 item 字段、`list_entry` 宏反推宿主——与本课"节点包含数据"相反的布局哲学。
- **RocksDB**：memtable 的 Skiplist 节点内含 backward pointers，本质是"分层 DLList"。
- **Lucene**：字段缓存 `ReaderPool` 的 LRU 用 LinkedHashMap（内部就是 HashMap+DLList）。

## 7. 延伸阅读

- Hug 笔记 "Doubly Linked Lists"；CLRS 10.2（含 10.2-6 O(1) 删除已知节点）。
- JDK `LinkedList` 源码（约 800 行，全是本讲模式）；Linux `include/linux/list.h`（400 行 C 宏，同一结构两种语言）。
- Project1a 官方 spec：矩阵游戏里"该用数组还是链表"的决策文档写法。
