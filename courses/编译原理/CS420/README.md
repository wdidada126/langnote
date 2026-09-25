# KAIST CS420: Compiler Design（KECC：真实 C→RISC-V）

## 课程信息

| 项目 | 内容 |
| --- | --- |
| 全称 | KAIST CS420: Compiler Design |
| 学校 | 韩国科学技术院（KAIST） |
| 主讲 | Jeehoon Kang（kaist-cp 实验室） |
| 教材 | 课程自建 GitHub textbook（kaist-cp/cs420 `textbook/`，无纸质书） |
| csdiy 路径 | https://csdiy.wiki/编译原理/CS420/ （页面更新 2024-07-21） |
| 最新期次 | 2024 版（仓库按学期滚动更新，Rust + KECC 框架） |
| 状态 | 🚧 骨架已建，逐讲正文待填充 |
| 先修要求 | 数据结构、计算机系统基础、Rust 编程基础 |
| 实现语言 | Rust |
| 预计学时 | 约 80 小时（csdiy 难度 ★×4） |

## 为什么学

- 面向**真实 C 语言**而非玩具语言，用 csmith Fuzzing 做差分测试——自学课程中罕见的工业级严谨。
- Rust 编写，所有权系统天然适配编译器 AST/IR 的无痕修改；完成后可读性直接迁移到 rustc。
- 重中端与后端（IR 设计、SSA 生成、CFG 简化、GVN、RISC-V 代码生成），前端理论几乎不讲——正是理解 **LLVM** 的最佳捷径。
- 配套 YouTube 视频逐行讲解代码，练习（homework 占 60%）粒度小、反馈快。

## 先修与知识联系

- **先修**：Rust（CS220 水平）、CSAPP/计组（RISC-V ISA、调用约定）。
- **互练**：USTC/SJTU（同 LLVM 风格 IR 路线）；CS143（补足前端理论短板）；PKU-Compilers（同为 RISC-V 后端但更简）。
- **知识映射**：HIR/LIR ↔ 龙书 ch8；数据流/use-def ↔ ch9；RA/代码生成 ↔ ch8.10/ch9.6。

## 讲义章节目录（2024 版 textbook + 6 个实验；正式笔记以仓库 README 为准）

| 讲次 | 标题 | 阅读材料 |
| --- | --- | --- |
| L1 | 课程总览：C→RISC-V 管线与 KECC 架构 | textbook/overview |
| L2 | 前端速览：lex/parsing/类型检查（框架已给）与 AST 遍历 | textbook/frontend；`src/frontend/` |
| L3 | Lab1：AST 打印与遍历热身 | 实验 README |
| L4 | HIR：高层次 IR 与 CFG 构建 | textbook/hir |
| L5 | LIR：SSA 形式的低层次 IR 与 phi | textbook/lir |
| L6 | 数据流分析基础与支配树、use-def 链 | textbook/lir#dataflow |
| L7 | 优化 I：CFG 简化（不可达块删除、链式合并） | 实验 4 讲义 |
| L8 | 优化 II：GVN（全局值编号）与记忆化 | 实验 4 讲义 |
| L9 | 优化 III：循环优化/内联等高级 pass | textbook/opt |
| L10 | 后端 I：RV64 指令选择与寻址模式 | textbook/backend |
| L11 | 后端 II：栈帧降低与调用约定 | 实验 5 讲义 |
| L12 | 后端 III：寄存器分配与 peephole | 实验 5 讲义；Chaitin/Briggs |
| L13 | 正确性：csmith Fuzzing 与差分测试方法 | textbook/fuzzing |
| L14 | 前沿：Vellvm/Verified 编译器与课程总结 | Vellvm 论文；kaist-cp 相关研究 |

## 备注

- 课程作业（Homework 60%）按学期滚动，骨架先按 2024 稳定版列讲，填充时对照最新 repo。
