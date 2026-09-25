# Michael 2004：Hazard Pointers — Safe Memory Reclamation for Lock-Free Objects

- 作者：Maged M. Michael
- 出处：IEEE Transactions on Parallel and Distributed Systems (TPDS), Vol.15 No.2, 2004
- DOI：10.1109/TPDS.2004.1276924（待核实）

## 论文要点

### 问题：无锁数据结构的安全内存回收（SMR）
无锁算法反复 CAS 改指针，任何线程都可能在任意瞬间持有仍在使用中的节点地址；被脱链的节点何时能安全释放，是 1998 MS 队列留下的开放问题（见 paper/msqueue_ppopp1998.md）。

### Hazard Pointer 协议
- 每个线程持有固定数量（与算法相关，如 MS 队列需 2 个）的全局可见指针槽 **HP[k]**，语义："我当前可能在引用此对象"。
- 三步协议：**发布**（写入 HP，普通存储）→ **加载**（读目标指针）→ **复核**（对比对象当前值是否仍是所读，防止发布后指针已变/ABA）。
- 释放侧：脱链对象不立即回收，先与所有线程的 HP 比对；不被任何 HP 引用的才进入可回收链，且回收前用**内存栅栏/批量协议**确认没有线程正处于"已加载未发布"窗口。
- 特性：读者等待自由（wait-free 读、lock-free 写），空间开销 O(线程数×HP 数)，可精确到对象级。

### 与其他回收方案的对比（论文表格结论）
| 方案 | 粒度 | 进展保证 | 问题 |
|---|---|---|---|
| 引用计数 | 对象级 | 无界竞态可延迟回收 | 计数更新本身在共享热行上，CAS 循环昂贵 |
| Epoch-Based (EBR) | 区间级 | lock-free | 长驻线程可无限延迟回收（unbounded） |
| 延迟队列/RCU | 区间级 | 依赖静默点 | 读侧要求"可识别空闲"，通用容器难满足 |
| **Hazard Pointers** | 对象级 | 有界（bounded） | 每对象释放要 O(线程) 扫描，读侧多一次栅栏 |

## 影响与工程落地

- libcds：`gc::HP` / `gc::DHP`（延迟发布版），MSQueue/TreiberStack/SkipList 的默认回收方案。
- Boost.LockFree `hazard_pointer`；C++ 提案 P2231（HP for lock-free）；Windows XP SP2 起内核用 HP 变体做句柄表延迟关闭。
- 与内核 RCU 的分野：RCU 用"静默周期"换读侧零开销，代价是回收无界；HP 用读侧一次栅栏换回收有界——6.S081 RCU 讲次的对照案例。

## 关联

- 笔记：`cpp/library/libcds.md` §3
- 课程：`courses/操作系统/MIT6.S081`（L11 RCU）、`courses/并行与分布式系统/CS149`、`courses/编程入门/cs431`（Rust 所有权 = 编译期 SMR）
