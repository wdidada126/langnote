# CS431 配套项目计划（骨架，本轮不写代码）

语言统一 Rust（edition 2021），依赖 crossbeam 仅用于对照不复用核心逻辑；均带本地压力/线性一致性测试。

| 章节 | 建议语言 | 小项目 | 编译方式 |
| --- | --- | --- | --- |
| L2–L3 锁 | Rust | 线程安全 LRU 缓存（Mutex + HashMap + 侵入式链表），对照 moka | `cargo test --release` + loom 模型检查可选 |
| L4–L5 内存模型 | Rust | litmus test 跑批：Relaxed/Acquire/Release 差分实验 | `cargo +nightly` + llmc 或自写循环压测 |
| L7 无锁栈 | Rust | Treiber stack + 指数退避，ABA 触发 demo | `cargo test --release`，多线程 fuzz |
| L8–L9 回收 | Rust | hazard pointer 版无锁链表 + EBR 版对比 | `cargo test --release`；`loom`/`miri -Z extra-checks` 可选 |
| L10 RCU | Rust | 简化用户态 RCU：版本戳 + grace period | `cargo test --release` |
| L11 并发哈希表 | Rust | 分段锁哈希表 → 无锁(HP)哈希表两级实现 | `cargo bench` (criterion) + `--release` |
| L12 STM | Rust | 多版本 OCC 事务内存 + 与锁方案吞吐对比 | `cargo bench --release` |

约定：本轮只列计划；所有压测脚本放 `bench/`，集中编译由用户统一执行。
