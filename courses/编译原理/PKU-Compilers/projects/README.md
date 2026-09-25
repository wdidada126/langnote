# PKU 编译原理实践 — 配套项目计划（本轮只列计划，不写代码）

> 课程本体即"实现一个 SysY→RISC-V 编译器"，项目按 9 步增量拆分为可独立提交的里程碑。约定：一个语言特性 = 一个里程碑 = 一批测试用例全绿；**本轮只写代码不编译**，集中编译验证由用户稍后执行。

## 章节 → 项目映射表

| 章节 | 建议语言 | 小项目（里程碑） | 编译方式 |
| --- | --- | --- | --- |
| L1 环境 | C++ 或 Rust | `hello-compiler` 骨架 CLI：读文件、原样输出空汇编 | CMake / cargo build，或 Docker 内 make |
| L2 最简 main | 同上 | main-return 常量编译器（端到端：源码→.s→spike 跑通） | 脚本 `run.sh`：编译+链接+仿真 |
| L3 词法语法 | 同上（前端可用 flex/bison 或 logos） | SysY 子集 token 流 + AST dump（JSON 打印） | Docker 镜像 pku-minic/debian |
| L4 算术表达式 | 同上 | AST→Koopa IR→RISC-V 表达式编译器 + 单测 | koopa 运行时库 + 自动测试脚本 |
| L5 变量赋值 | 同上 | 局部变量/赋值支持；栈槽分配器 v0 | 同上 |
| L6 控制流 | 同上 | if/while/短路求值；CFG 构建与块划分 | 同上 |
| L7 函数调用 | 同上 | 完整调用约定：参数传递、帧指针、递归测试 | 同上 |
| L8 数组 | 同上 | 多维数组地址计算 + getelem；全局数组数据段 | 同上 |
| L9 综合 | 同上 | 通过官方 testcases 的 functional 全套 | auto_test.sh |
| L10 挑战 | 同上 | 优化 pass（常量传播/CSE/内存提升）+ 运行时库；性能用例提速 | 同上，附 benchmark 对比报告 |

## 里程碑验收标准

- 每个里程碑：`testcases/<章节>` 目录全绿 + README 记录设计取舍（为什么这么做/还能怎么做）。
- 最终：functional 全部通过；performance 相对基线有可量化提升（L10 之后）。
