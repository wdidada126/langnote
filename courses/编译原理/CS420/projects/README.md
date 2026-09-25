# KAIST CS420 — 配套项目计划（本轮只列计划，不写代码）

> 语言统一 Rust（课程框架 KECC）。两种玩法并行：A) 在 KECC 上完成 6 个官方 homework；B) 自建玩具版 `mini-kecc`（HIR→LIR→RV64）加深理解。**本轮只写不编译**，集中编译验证稍后由用户执行。

## 章节 → 项目映射表

| 章节 | 建议语言 | 小项目 | 编译方式 |
| --- | --- | --- | --- |
| L2-L3 前端/AST | Rust | KECC Lab1：AST 打印；mini-kecc 用 syn/winnow 解析子集 C | cargo test（KECC 自带 runner） |
| L4 HIR | Rust | KECC Lab2：CFG 构建；mini-kecc HIR 定义 + dot 可视化 | cargo test / dot 渲染 |
| L5-L6 LIR/SSA | Rust | KECC Lab3：LIR 生成与 phi 放置；支配树算法独立单测 | cargo test |
| L7-L9 优化 | Rust | KECC Lab4：CFG 简化 + GVN；mini-kecc 加常量传播 pass | cargo test + csmith 差分 |
| L10-L12 后端 | Rust | KECC Lab5：RV64 指令选择/帧降低/RA；输出 .s 用 gcc 链接 | cargo test + spike/ qemu 跑通 |
| L13 正确性 | Rust | KECC Lab6：csmith 差分脚本 + 崩溃归约最小化 | shell 脚本 `fuzz.sh`（长跑） |
| L14 前沿 | Rust/Coq | 阅读 Vellvm 片段并写对照笔记（不做实现） | 无 |

## 里程碑验收标准

- 每个 KECC Lab：仓库 `./test.sh labN` 全绿（填充期在本地 Docker 执行）。
- mini-kecc：能编译 GCD/快排/矩阵乘三个基准程序并在 qemu-riscv64 输出正确。
- 记录每个优化 pass 的"合法性论证"笔记（对照 L13 方法学）。
