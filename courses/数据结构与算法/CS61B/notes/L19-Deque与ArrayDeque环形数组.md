# L19 Deque 抽象与 ArrayDeque（环形数组）

> 对应 spring2024 L19：Deque 接口、环形数组、head/tail 与取模。作业：Lab5（ArrayDeque）。

## 1. 核心概念

- **Deque（double-ended queue）**：两端 add/remove/peek 全 Θ(1) 的 ADT；Queue/Stack 是它的受限视图（61B 立场：忘掉 Stack 类，Deque 通吃）。
- **环形数组（circular array）**：容量 cap 的数组上，索引对 cap 取模绕回：
  ```java
  public class ArrayDeque61B<T> implements Deque61B<T> {
      private T[] items; private int size, nextFirst, nextLast;
      ArrayDeque61B() { items = (T[]) new Object[8]; size = 0; nextFirst = 3; nextLast = 4; }
      public void addFirst(T x) {
          if (size == items.length) resize(2 * size);
          nextFirst = (nextFirst - 1 + items.length) % items.length; // +len 防负
          items[nextFirst] = x; size++;
      }
      public T removeLast() {
          if (isEmpty()) throw new EmptyDequeException();
          nextLast = (nextLast - 1 + items.length) % items.length;
          T x = items[nextLast]; items[nextLast] = null; size--; return x;
      }
  }
  ```
- **两大坑**：
  1. 负数取模：Java `%` 对负数返回负值，必须 `(i - 1 + cap) % cap`（或三元判断）。
  2. `null` 语义：用 `items[idx] == null` 判空则不能存 null（JDK ArrayDeque 禁止 null 的正式理由）；本课用 `size` 计数。
- **head/tail 三种约定**（nextFirst 指向"下次 addFirst 的位置" vs 当前首元素）——选一种并在 javadoc 写死，Lab5 spec 即训练此表达。

## 2. 复杂度视角

| 操作 | ArrayDeque | DLList | ArrayList |
| --- | --- | --- | --- |
| addFirst/removeFirst | Θ(1) 摊还 | Θ(1) | Θ(n) |
| addLast/removeLast | Θ(1) 摊还 | Θ(1) | Θ(1) 摊还 |
| get(i) | Θ(1)：`items[(nextFirst+i)%cap]` | Θ(n) | Θ(1) |
| 迭代 | Θ(n)，连续内存 cache 友好 | Θ(n) 指针追逐 | Θ(n) |
| 扩容 | 复制 + 重排成"从中间展开"或归一化 nextFirst=3 | 无 | 复制 |

摊还论证与 L17 完全相同（几何倍增），resize 时把逻辑序"拉直"到新数组。

## 3. 与前后讲联系

- 上承 L16–L18 线性表全谱：本课到此回答"要快又省内存的通用序列选谁"——ArrayDeque（随机访问 + 两端）完胜 LinkedList（Jdk 开发者共识："don't use LinkedList"）。
- 下启：L28 堆的数组表示是"完全二叉树塞进连续数组"，同一"取模/整除换算父子"技巧；L30 BFS 队列直接用 Deque；Lab5 的测试来自 L13。

## 4. 跨课程联系

- **CS61A**：61A 用 Python `list` 假装 deque（`pop(0)` 是 O(n) 陷阱！），61A 不追究；61B 逼你直面"API 一样、复杂度不同"。
- **6.006**：6.006 把 queue 当黑盒只用于 BFS；环形缓冲在 6.006 无对应，是 61B 的工程增量。
- **CSAPP**：环形缓冲 = 经典"生产者-消费者 ring buffer"；DPDK、io_uring、Kafka 的日志切片全是它的并发版。取模用 `& (cap-1)` 需 cap 为 2 的幂——CSAPP 章节的位技巧落地。
- **OS/15-445**：环形页缓冲/预读窗口、串口 tty 缓冲。
- **DDCA**：FIFO 硬件即环形缓冲 + 读写指针比较。

## 6. 开源项目应用

- **JDK**：`java.util.ArrayDeque`（JDK6 起，head/tail 两个 int 取模实现；禁止 null；性能全面优于 `Stack`/`LinkedList` 被其 javadoc 点名）。
- **Netty**：`MPSC ring buffer`（JCTools）支撑无锁队列；LMAX Disruptor 以环形数组 + 序号替代队列，延迟降低一个数量级——"环形数组+摊还扩容"的极限工程。
- **Linux 内核**：`kfifo`；**Kafka**：`OrderedMap` 内部 log 段缓存用环形数组。
- **Git**：object 写出缓冲、`pack-objects` 窗口内的 delta 链缓存。

## 7. 延伸阅读

- Hug 笔记 "Deque"；Lab5 spec 与官方测试样例（重点研读其 null/empty 约定）。
- JDK ArrayDeque javadoc（"probably faster than Stack and LinkedList" 一段）。
- Sedgewick algs4 1.3（ResizingArrayDeque 双栈折叠实现，另一路设计）。
