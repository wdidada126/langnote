# USTC 编译原理与技术 — 配套项目计划（本轮只列计划，不写代码）

> 语言统一 C++（与官方框架一致）。双线并行：A) 完成官方 Cminusf 编译器 6 个 Lab；B) 自建 `ustc-lite` 玩具管线（Flex/Bison→LightIR→LoongArch）用于笔记内最小可复现示例。**本轮只写不编译**，集中编译验证稍后由用户执行。

## 章节 → 项目映射表

| 章节 | 建议语言 | 小项目 | 编译方式 |
| --- | --- | --- | --- |
| L2-L5 前端 | C++ (Flex/Bison) | Lab1：Cminusf 前端 + AST dump | Makefile（官方框架 docker） |
| L6-L7 IR 生成 | C++ | Lab2：LightIR 生成，`opt -verify` 自检 | 官方脚本 + llvm 工具链 |
| L8-L9 后端 | C++ | Lab3：LoongArch 汇编输出，qemu-loongarch64 跑通 | 官方脚本 + qemu |
| L10-L11 局部优化 | C++ | Lab4：块内常量传播/CSE/DCE pass | 官方脚本 |
| L12-L13 全局优化 | C++ | Lab5：GVN/循环简化，性能用例基准 | 官方脚本 + benchmark 表 |
| L14-L15 寄存器分配 | C++ | Lab6：干涉图着色 + spill 代价报告 | 官方脚本 |
| L16 总结 | C++ | 全管线回归：功能 + 性能双榜单 | `run_all.sh` |

## 里程碑验收标准

- 每 Lab：官方自动化测试全绿；README 记录该阶段 IR 样例前后 diff。
- 玩具线 ustc-lite：能编译 GCD/冒泡排序并在 qemu 输出正确。
- 性能线：记录每个 pass 带来的用例耗时变化（数据入笔记）。
