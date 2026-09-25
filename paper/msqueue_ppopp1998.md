# Michael & Scott 1998：Simple, Fast, and Practical Non-Blocking and Blocking Concurrent Queue Algorithms

- 作者：Maged M. Michael, Michael L. Scott
- 出处：8th ACM SIGPLAN Symposium on Principles and Practice of Parallel Programming (PPoPP 1998)
- DOI：10.1145/271530.271533（待核实）
- 原文 PDF：ACM DL / 作者主页 ftp.cs.rochester.edu（本机网络受限，待核实）

## 论文要点

### 问题
并发队列在锁实现下有三个痛点：持锁线程被抢占导致全体阻塞（ convoy ）、锁的调度开销、以及异常/页错误下的安全性。需要非阻塞（non-blocking，即 lock-free）版本保证系统整体永远有进展。

### 核心算法（非阻塞 FIFO 队列）
- 单链表 + 两个原子指针 `Head` / `Tail`，全部操作只用 **CAS（cmp-and-swap）** 完成，无需锁。
- `enqueue`：先在 `Tail->Next` 上 CAS 挂新节点，再 CAS 推进 `Tail`；若发现 `Tail` 落后（另一线程已挂节点未推进），**帮助（help）**推进后再重试。
- `dequeue`：读 `Head->Next` 取值，CAS 推进 `Head`；与并发 `enqueue` 的竞态通过"先改 Next 再改 Tail/Head"的固定顺序与重试循环化解。
- 关键不变式：`Tail` 永远指向最后一个已挂入的节点，且推进前每个节点必然已链接。

### Safe Memory Reclamation 问题（论文最重要遗产）
- 朴素实现里 `dequeue` 释放脱链节点后，并发线程可能还引用它（use-after-free）；先读 `Next` 再 CAS 的两步也暴露 **ABA** 问题。
- 论文给出**双链（2-link）变体**：节点带 `m_next`/`m_prev`，回收前先标记 `NULL` 确认无其他线程在途，实现"延迟回收"；作者明确指出通用解法需要跨对象协调，留作后续工作——这个坑后来由 **Hazard Pointers**（见 paper/hazard_pointers_tpds2004.md）和 Epoch-Based Reclamation 填上。

### 阻塞对偶算法
同一论文还给出一个基于自旋/互斥的阻塞队列，证明在低竞争下比纯 CAS 循环更快，作为"非阻塞不是免费午餐"的对照基线。

## 影响与工程落地

- 教科书地位：CSAPP §12.5、《The Art of Multiprocessor Programming》、《C++ 并发编程实战》均以该队列为无锁队列原型。
- 实现：libcds `MSQueue`（intrusive/container，强制 HP）、Linux `llq`（lkp 试验田）、Java `ConcurrentLinkedQueue`（同一算法，节点改单链+惰性大小，回收靠 GC 解决——JVM GC 天然回答了 safe memory reclamation）。
- 变体：segmented queue、flat combining queue 等（libcds 内即有）。

## 关联

- 笔记：`cpp/library/libcds.md` §2-§3
- 课程：`courses/计算机系统基础/CSAPP`（并发讲次）、`courses/并行与分布式系统/MIT6.824`（线性一致性语义）、`courses/操作系统/MIT6.S081`（锁与 RCU 对照）
