libcds

> 以下内容由 2026-09-23 日记（`2026/202609/20260923.md`）扩展整理。

# libcds：C++ 无锁并发数据结构库

## 1. 库概览

- 作者 Max Khon（KhronoXG），仓库 `github.com/khronoxg/libcds`（本机网络无法访问 GitHub，链接以 awesome-cpp 收录项为准，待核实）。
- 定位：模板实现的**无锁（lock-free）与细粒度锁**并发容器库，覆盖栈、队列、跳表、map/set、FIFO 等，核心卖点是可插拔的安全内存回收（reclamation）方案。
- 编译依赖 Boost（部分版本），CMake 构建；线程必须先注册到库的线程管理器才能操作容器（见 §4）。

## 2. Michael-Scott 队列：MSQueue（20260923 日记核心内容）

libcds 中 MS 算法的对应实现类是 `MSQueue`，分侵入式与非侵入式两个版本。

### 2.1 核心实现类

| 类 | 头文件 | 特点 |
|---|---|---|
| `cds::intrusive::MSQueue` | `<cds/intrusive/msqueue.h>` | 要求 `value_type` 派生自 `msqueue::node`（或含该成员/可转换）；节点嵌入用户数据结构，零额外分配 |
| `cds::container::MSQueue` | `<cds/container/msqueue.h>` | 基于侵入式实现构建，用户不改结构，队列内部分配与管理节点 |

### 2.2 模板参数 GC：只支持 Hazard Pointer

关键约束在模板参数 `GC`：MSQueue **只支持 `gc::HP` 与 `gc::DHP`**，这是 MS 算法安全回收内存的必要条件；每个操作线程需要 **2 个 hazard pointer**。

### 2.3 基本接口

- `enqueue` / `dequeue` 为主操作，`push` / `pop` 为同义函数。
- 非侵入式版本额外提供移动语义 `enqueue(value_type&&)` 与原地构造 `emplace`。

### 2.4 在库中的定位

libcds README 明确标注 MSQueue 对应 Michael & Scott 1998 年论文《Simple, fast, and practical non-blocking and blocking concurrent queue algorithms》。同库还有该算法变体（flat combining queue、segmented queue）以及基于 Hunt 等人算法的 RWQueue。

## 3. 为什么 MS 队列离不开 HP

- MS 队列的 pop 会把头节点脱链后立即释放，而其他线程可能仍持有该节点的指针（tail/next），直接 free 是 use-after-free；先 `next` 再 CAS `head` 的两步操作也构成经典 ABA 风险。
- libcds 的 MSQueue 实现采用 **2-link 变体**（节点带 m_next/m_prev，论文中"safe memory reclamation"版本），把节点回收延迟到确认无人引用——这套延迟回收正是靠 HP 的"发布指针前先挂警示"机制完成。
- 对比：Treiber 栈等结构简单容器在 libcds 中还可选 epoch/lightgc，但 MSQueue 不接受，属于 API 层面的强约束。

## 4. 使用骨架（API 细节以所用版本文档为准）

```cpp
#include <cds/init.h>
#include <cds/gc/hp.h>
#include <cds/container/msqueue.h>

int main() {
    cds::Initialize();                 // 1. 库初始化
    cds::gc::HP::instance();           // 2. 启用 Hazard Pointer GC
    {
        cds::TSInitializer ci;         // 3. 当前线程绑定线程管理器（前置要求）

        cds::container::MSQueue<int, cds::gc::HP> q;
        q.push(42);
        int v;
        if (q.pop(v)) { /* 使用 v */ }
    }                                  // 线程退出自动解绑
    cds::Terminate();
}
```

要点：任何调用线程都要有 `cds::TSInitializer`（或手工 `cds::threading::Manager::attachThread()`）；侵入式版本则自定义结构内嵌 `cds::intrusive::msqueue::node<>` 并声明 hook。

## 5. 库内其他并发容器速查

| 容器 | 算法出处 | 备注 |
|---|---|---|
| TreiberStack | Treiber 1986 | 可选 HP/epoch |
| MichaelHeap | Michael 2002 无锁优先队列 | 基于跳表 |
| SkipListSet/Map | Herlihy et al. 无锁跳表 | HP |
| Feldman-HashMap / Michael-Map78 / FlatCombiningMap | 三种并发哈希表路线 | 对比细粒度锁/CAS/合并更新 |
| SegmentQueue / BoundedMeteredQueue | MS 队列变体 | 分段减少尾部 CAS 竞争 |
| RWQueue | Hunt 等人的读写队列 | README 中与 MSQueue 并列 |

## 6. 知识联系

- **CSAPP 第 12 讲（并发编程）**：从互斥锁/信号量到无锁的动机——CAS 与 ABA 问题的工程答案；libcds 是 CSAPP 教材体系之外"教科书算法 → 生产级实现"的典型样本。
- **安全内存回收谱系**：Hazard Pointer（Michael 2004）↔ Epoch-Based Reclamation ↔ 内核 RCU（6.S081 L11 / DDCA 之后并行线）；Rust `cs431`（KAIST）用所有权系统在编译期解决同一问题，可对照阅读。
- **6.824 / MIT 分布式线**：队列的线性一致性语义与分布式队列/Kafka 分区顺序是同一抽象在不同层的投影；flat combining 则与批处理/合并写优化（如 LSM、I/O 合并）共享思想。
- **C++ 并发书单**：《C++ Concurrency in Action》讲内存序与 wrapper 风格；libcds 头文件里大量 `memory_order` 显式用法是 std::atomic 内存序的实战教材。
- 关联笔记：`book/C++并发编程实战（第2版）`、`courses/编程入门/cs431`、`courses/计算机系统基础/CSAPP`。

## 7. 参考

- 论文笔记：[Michael & Scott 1998《Simple, fast, and practical non-blocking and blocking concurrent queue algorithms》PPoPP](/D:/develops/git/github/langnote/paper/msqueue_ppopp1998.md)；[M. Michael 2004《Hazard Pointers: Safe Memory Reclamation for Lock-Free Objects》TPDS](/D:/develops/git/github/langnote/paper/hazard_pointers_tpds2004.md)（两篇均为论文而非书，归 `paper/`）。
- libcds README 与 doxygen 文档（khronoxg/libcds，待核实）。
- 原始日记：`2026/202609/20260923.md`。