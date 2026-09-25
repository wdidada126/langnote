# CS431 讲义要点（骨架）

## L1 导论
- 并发 bug 的本质：非确定性交错 + 共享状态。
- Rust 的 Send/Sync 只挡住一类错误，正确算法仍需设计。

## L2 Linearizability
- 并发对象正确性标准：每个操作原子化到某时刻。
- 组合性与局部性：为何它是"可组合的正确性"。

## L3 锁
- 自旋 vs 阻塞：futex 思想；读写锁与升级死锁。
- 锁粒度设计与性能；Rust MutexPoison 语义。
- HW：并发安全 LRU 缓存（锁 + HashMap + 链表）。

## L4 内存模型 I
- 编译器优化与 CPU 乱序导致的重排。
- SC vs 真实硬件；litmus test（store buffering 等）。

## L5 内存模型 II
- C11/Rust atomic：Ordering（Relaxed/Acquire/Release/AcqRel/SeqCst）。
- happens-before 与数据竞争的机器可检定义。

## L6 Promising Semantics
- 给弱内存模型一个可推理的操作语义（promise/excerpt 机制）。
- Rust 别名模型 (Stacked Borrows) 与并发的交互。

## L7 无锁栈/队列
- Treiber stack + backoff；Michael-Scott queue 的 help-first CAS。
- 无锁 vs 无等待 (wait-free) 层级。

## L8 CAS 与 ABA
- CAS 循环的活锁风险与 backoff 策略。
- ABA 的真实成因：内存复用；引出 L9。

## L9 内存回收
- 无锁结构为何不能直接 free：读者悬垂。
- EBR 安全点；hazard pointer 逐指针发布（HW 重点）。

## L10 RCU
- 读端零开销：grace period 等待写者收敛。
- Linux RCU 与 Rust 库实现的差异。

## L11 并发哈希表
- 粗锁 → 分段 → 无锁（authoritative/spin lock、Robin Hood）谱系。
- Flurry (C++ folly 移植) 案例研读。

## L12 STM
- OCC：多版本 + 验证-写回；与锁的性能分界。
- 为何生产环境少用（组合性/性能坑）。

## L13 验证初步
- 分离逻辑/资源推理思想（Iris）；为课程理论收官。
