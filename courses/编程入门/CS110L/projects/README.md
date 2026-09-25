# CS110L 配套项目计划（骨架，本轮不写代码）

语言统一 Rust（edition 2021），cargo 管理；对应 6 Lab + 2 Project 的主题改造。

| 章节 | 建议语言 | 小项目 | 编译方式 |
| --- | --- | --- | --- |
| L2–L3 所有权 | Rust | 迷你 grep：借用与移动语义的 CLI 工具 | `cargo build --release` + `cargo test` |
| L4–L5 trait/泛型 | Rust | 泛型表达式计算器（trait 对象 vs 泛型两版对比） | `cargo test` |
| L6 迭代器 | Rust | 日志管道分析器：map/filter/fold 链 | `cargo test --release` |
| L7 智能指针 | Rust | 图结构玩具：Rc<RefCell<Node>> + 循环引用检测 | `cargo run` + valgrind 可选 |
| L8 线程/Project1 方向 | Rust | 线程版简单调试器（/proc + ptrace via nix crate） | `cargo build`（Linux only），分阶段 milestone |
| L9–L10 异步/Project2 方向 | Rust | 负载均衡器：thread-per-connection、mio、tokio 三实现 + wrk 压测脚本 | `cargo build --release`；bench/ 下附对比脚本 |

约定：本轮只列计划；依赖锁定 `Cargo.lock`，集中编译由用户稍后统一执行。
