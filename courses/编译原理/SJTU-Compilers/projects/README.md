# SJTU 编译原理 — 配套项目计划（本轮只列计划，不写代码）

> 语言统一 C++（与课程一致）。主线复刻官方 Lab1-Lab7 序列；每个 Lab 独立目录、自带 `Makefile` 与测试脚本。**本轮只写不编译**，集中编译验证稍后由用户执行。

## 章节 → 项目映射表

| 章节（Lab） | 建议语言 | 小项目 | 编译方式 |
| --- | --- | --- | --- |
| L2 / Lab1 直线解释器 | C++ | Bison 驱动的表达式求值器 | Makefile（flex/bison + g++） |
| L3 / Lab2 Lexer | C++ | Tiger 词法器（字符串/注释/位置） | Makefile |
| L4 / Lab3 Parser | C++ | Tiger 文法→带行号 AST dump | Makefile + 用例 diff |
| L5 / Lab4 Type Checking | C++ | 类型环境与报错器（record/array 递归） | Makefile |
| L6+L9 / Lab5 Escape→LLVM | C++ | AST→LLVM IR 直译，`opt -verify` 自检 | cmake + LLVM 包 |
| L10 / Lab6 代码生成（选做） | C++ | Machine IL→RISC-V/MIPS 汇编 | Makefile + qemu 运行 |
| L12 / Lab7 寄存器分配（选做） | C++ | 在线着色分配器 + spill 统计 | Makefile |
| L13 GC 专题（扩展） | C++ | 标记-清除小回收器玩具 | Makefile |

## 里程碑验收标准

- 每 Lab：官方风格测试集全绿；仓库内留存 `examples/` 输入输出对照。
- 综合：Tiger 源→LLVM IR→汇编三级产物可追溯（笔记引用样例）。
- 选做完成度：RA 后性能用例相对朴素映射的提升数据记录。
