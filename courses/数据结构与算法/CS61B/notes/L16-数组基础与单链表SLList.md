# L16 数组基础与单链表 SLList

> 对应 spring2024 L16：数组与浅/深拷贝、SLList（singly linked list）实现。作业：Lab4 启动。项目对应：projects/dllist 的 ArraySeq 前置练习。

## 1. 核心概念

- **数组**：定长、连续内存、O(1) 随机访问；Java 数组是对象（`.length` 只读），`int[]` 与 `Integer[]` 不同（前者裸数据，后者指针数组）。
- **浅拷贝 vs 深拷贝**：
  ```java
  int[] a2 = a.clone();                    // 浅拷贝：int 数组够用（值语义）
  Term[][] g2 = new Term[r][c];
  for (int i = 0; i < r; i++) g2[i] = g[i].clone(); // 二维需逐行克隆才是"深"
  ```
  对象数组 clone 后共享元素引用——改 `g2[0][0].coeff` 会同时改 `g`，Project 1a 经典事故。
- **SLList**：节点 = `item + next`；头插/尾查天然，无随机访问。
  ```java
  private class Node {
      T item; Node next;
      Node(T i, Node n) { item = i; next = n; }
  }
  private Node first, last; // last 尾指针：addLast 从 Θ(n) 降为 Θ(1)
  ```
- **哨兵（sentinel）**：用哑元 `sentinel.next == 真实首节点`，把"first 是否为 null"的特判消掉——从 L16 贯穿到 L18 DLList、Lab5 ArrayDeque 设计讨论。

## 2. 实现检查清单（Lab/考试手写模板）

1. 指针改写顺序：`n.next = p.next; p.next = n;`（先接新边再拆旧边，反了丢链尾）。
2. 每个公开方法问：空表？单节点？操作恰是首/尾？
3. `size` 作为实例变量维护，O(1) 返回，别每次遍历。
4. 内存：每节点 ≈ 12–16B 对象头 + 8B item 引用 + 8B next 引用；比数组元素多约 3 倍。

## 3. 复杂度视角

| 操作 | SLList（带 last） | 数组 | 说明 |
| --- | --- | --- | --- |
| get(i) | Θ(i) | **Θ(1)** | 链表无随机访问 |
| addFirst | Θ(1) | Θ(n) | 数组头插要搬移 |
| addLast | Θ(1) | Θ(1) 摊还（定长则不能） | |
| removeFirst | Θ(1) | Θ(n) | |
| contains | Θ(n) | Θ(n) | 常数：数组缓存友好更快 |
| 内存 | Θ(n)×指针开销 | Θ(n)×元素大小+头 | |

## 4. 与前后讲联系

- 上承 L04–L06（Node 是内部类的最佳用例）与 L08–L11（Iterable）。
- 平行 L17：数组 + 几何扩容 = 动态数组，与链表构成"两种线性表"的完整对照；L18 双向化解决 SLList 不能回溯/删除中间节点的问题；L19 环形数组再回扣数组。

## 5. 跨课程联系

- **CS61A**：61A 的 `link(first, rest)` 不可变链表是函数式版本；61B 的 SLList 可变、带回溯指针——"同一数据结构，代数数据类型 vs 对象图"两种世界观。
- **CSAPP**：数组 = `base + 8*i` 一条寻址；链表遍历是指针追逐（pointer chasing），预取器失效，DRAM 延迟暴露——这是"Θ(n) 相同、纳秒差十倍"的主战场。
- **6.006**：6.006 把链表达为"对象+引用"仅作直觉，正式分析从数组/哈希起步；61B 手写链表是为理解 JVM 对象图。
- **OS/15-445**：内核链表（Linux `list_head` 侵入式链表）与数据库 free list 都用链表做 O(1) 挂链/摘链，理由与 L18 完全相同。

## 6. 开源项目应用

- **JDK**：`java.util.LinkedList` 就是带哨兵的双向表（不推荐生产使用，缓存不友好）；`HashMap` 每个桶上的冲突链即 SLList。
- **Git**：commit 对象的 `parent` 指针构成 DAG；单父链退化后就是"每节点存 item+next"的 SLList，`git log` 线性历史 = 沿链走。
- **Lucene**：文档 ID 集合的稠密段用 bitset/数组，稀疏段用跳表化链表思想——"数组 vs 链表"的选择在倒排索引中每天发生。
- **RocksDB**：`SkipList` 内存表替代链表做有序集合，印证本课"链表示意、工程加层"的演进路线。

## 7. 延伸阅读

- Hug 笔记 "Array Basis / Linked Lists"；CLRS 10.2（链表练习 10.2-7：链表实现队列/栈）。
- 《CSAPP》Ch.9（动态内存布局下节点分配成本）。
- Martin Thompson "Mechanical Sympathy"（指针追逐 vs 线性扫描的性能讨论）。
