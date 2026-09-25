# Nand2Tetris (Hebrew U): 从零构建现代计算机

## 课程信息

| 项目 | 内容 |
| --- | --- |
| 课程全称 | The Elements of Systems / Nand2Tetris I & II（从与非门到编译器） |
| 所属学校 | 希伯来大学（Hebrew University of Jerusalem） |
| 主讲 | Noam Nisan & Shimon Schocken |
| 教材 | 《计算机系统要素：从零开始构建现代计算机》(The Elements of Computing Systems) |
| csdiy 路径 | /体系结构/N2T/ |
| 最新期次 | Coursera 常年滚动开课（Nand2Tetris I / II 两门），全球 400+ 高校采用 |
| 先修要求 | 无；语言任选；难度 🌟🌟🌟；预计学时 40 小时 |
| 状态 | 骨架已建，正文待填充 |

## 为什么学

- Coursera 上被数万人评为满分：零基础上用与非门一路搭出 CPU、汇编器、虚拟机、编译器、操作系统，最后在自家计算机上跑俄罗斯方块。
- 提取计算机本质而不陷于工业细节，是最快的「全局贯通」路线，为 CSAPP/DDCA/CS61C 提供统一心智模型。
- 硬件 + 软件两条线各 6 个 Project，按部就班一个月内可完课，性价比极高。

## 先修与知识联系

| 方向 | 关联 |
| --- | --- |
| 先修 | 无（真正零基础友好） |
| 后续向下 | DDCA/CS61C（同样的门→CPU 路线，深度和严谨度更高） |
| 后续向上 | CSAPP（Jack 编译器 ↔ 编译链；OS ↔ 系统调用），143（编译器工程化） |
| 概念输出 | HDL→Verilog/Chisel；Hack 平台→RISC-V 软核；nand2tetris 工具链是 EDA 教学标配 |

## 最新年份讲义章节目录表（Part I 硬件 6 周 + Part II 软件 6 周，官方固定结构）

| 讲次 | 标题 | 阅读材料 |
| --- | --- | --- |
| L1 (Ch.1) | 布尔逻辑与 HDL：从 Nand 到全部门 | 教材 Ch.1；Project 1 |
| L2 (Ch.2) | 组合逻辑：加法器、多路复用器、ALU | 教材 Ch.2；Project 2 |
| L3 (Ch.3) | 时序逻辑与内存：锁存器、寄存器组、RAM/ROM | 教材 Ch.3；Project 3 |
| L4 (Ch.4) | 机器语言：Hack 平台、汇编与程序示例 | 教材 Ch.4；Project 4 |
| L5 (Ch.5) | 计算机体系结构：CPU 数据通路与控制 | 教材 Ch.5；Project 5 |
| L6 (Ch.6) | 汇编器： Hack 语言到二进制的完整翻译器 | 教材 Ch.6；Project 6 |
| L7 (Ch.7) | 虚拟机 I：栈范式与算术/内存访问翻译 | 教材 Ch.7；Project 7 |
| L8 (Ch.8) | 虚拟机 II：程序控制与函数调用翻译 | 教材 Ch.8；Project 8 |
| L9 (Ch.9) | 高级语言导论：Jack 语言规范 | 教材 Ch.9 |
| L10 (Ch.10) | 编译器：表达式、语句、类与递归 | 教材 Ch.10；Project 10 |
| L11 (Ch.11) | 操作系统：内存/图形/键盘/时钟服务 API | 教材 Ch.11；Project 11 |
| L12 (Ch.12) | 终局：编译器 + OS 跑通俄罗斯方块，全栈回顾 | 教材 Ch.12 |

## 课程资源（摘自 csdiy）

- 课程网站：Nand2Tetris I / II（Coursera）；官方配套 nand2tetris 工具链（硬件模拟器/VM 模拟器）
- 课程作业：10 个 Project 带你造台计算机
- 资源汇总：PKUFlyingPig/NandToTetris 实现合集
