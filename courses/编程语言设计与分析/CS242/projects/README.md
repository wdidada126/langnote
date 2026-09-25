# Stanford CS242 — 配套项目计划（本轮只列计划，不写代码）

> 语言按作业原生：OCaml + Rust，形式化线用 Lean/F*。每个 HW 一个独立目录；**本轮只写不编译**，集中编译验证稍后由用户执行。

## 章节 → 项目映射表

| 章节 | 建议语言 | 小项目 | 编译方式 |
| --- | --- | --- | --- |
| L2 JSON 形式化 | Lean 4 或纸笔 | mini-JSON 语法/语义形式化 + 2 条性质证明 | lake build |
| L3-L5 函数式语言 | OCaml | 从 λ→ 到含 pair/unit 的类型检查器 + 解释器（dune 工程，自带测试） | dune build && dune test |
| L6 WebAssembly | OCaml/Rust | Wasm 二进制解析器 + 栈式 VM 子集解释器 | dune/cargo test |
| L7 所有权 | Rust | 迷你线性类型检查器（move/borrow 判定玩具版） | cargo test |
| L8 异步 | Rust | 手写 mini-executor（poll/waker）+ channel 集成测试 | cargo test（无网络） |
| L9 会话类型 | Rust | typestate 风格 TCP 协议库（本地回环测试） | cargo test |
| L10 大作业 A | Lean/F* | Lean：证明 TAPL 小定理集；或 F* 验证简易 KV 存储 | lake/fstar 脚本 |
| L11 大作业 B | Rust/OCaml | RLU 并发队列 或 OCaml 迷你深度学习框架（前向+反向 AD） | cargo test / dune test |
| L12 总结 | — | 一张"理论→防住的 bug 类别"迁移图谱（笔记） | 无 |

## 里程碑验收标准

- 每个 HW 目录：`README.md`（题目复述）+ `tests/`（本地可跑）+ 实现代码；只写不编译。
- 大作业二选一深入，另一条线写 1 页方案对比。
- 与 `notes/outline.md` 双向链接：每讲要点标注对应代码位置。
