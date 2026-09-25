# CS220 配套项目计划（骨架，本轮不写代码）

语言统一 Rust（edition 2024，可先 2021），全部用 `cargo test` 验收，模拟课程"无视频、测试驱动"风格。

| 章节 | 建议语言 | 小项目 | 编译方式 |
| --- | --- | --- | --- |
| L2–L3 ADT | Rust | 算术表达式类型 + 求值器（enum + match 递归） | `cargo new expr && cargo test` |
| L4 Trait | Rust | 迷你序列化框架：Serialize trait 手实现 JSON/TOML 两后端 | `cargo test --workspace` |
| L5–L6 所有权/生命周期 | Rust | 零拷贝 JSON token 解析器（&str 切片输出） | `cargo test` + criterion 基准 |
| L7 闭包迭代器 | Rust | 日志统计管道：filter/map/聚合组合子 | `cargo test --release` |
| L8 智能指针 | Rust | 带 Undo 的文本编辑器模型（Rc<RefCell> + Weak） | `cargo test` |
| L9 错误处理 | Rust | 多阶段 CLI 工具：thiserror 风格自定义错误链 | `cargo test` + `cargo clippy -- -D warnings` |
| L10 并发 | Rust | 多线程 web crawler / 8 皇后并行求解 | `cargo test --release`，附基准脚本 |
| L11 unsafe（选做） | Rust | 手写固定容量 Vec（alloc + MaybeUninit + Drop） | `cargo +nightly miri test` |

约定：本轮只列计划；与 cs220 官方 homework 不重名，避免直接复制题面。
