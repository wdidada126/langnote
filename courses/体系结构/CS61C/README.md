# UCB CS61C: Great Ideas in Computer Architecture 计算机体系结构

## 课程信息

| 项目 | 内容 |
| --- | --- |
| 课程全称 | CS61C: Great Ideas in Computer Architecture (Machine Structures) |
| 所属学校 | 加州大学伯克利分校（UC Berkeley） |
| 主讲 | 每年轮换（Fa25 当前教学团队见官网；历史名讲包括 Borriello、Patterson 时代奠定框架） |
| 教材 | 无必修纸质教材；参考 Patterson & Hennessy, 《Computer Organization and Design: RISC-V Edition》 |
| csdiy 路径 | /体系结构/CS61C/ |
| 最新期次 | Fall 2025（csdiy 收录 Fa24/Fa20 页面备份与 Su20/Fa20 视频，Project 以最新学期为准） |
| 先修要求 | CS61A、CS61B；语言 C（+RISC-V 汇编）；难度 🌟🌟🌟🌟；预计学时 100 小时 |
| 状态 | 骨架已建，正文待填充 |

## 为什么学

- 伯克利 CS61 三部曲收官之作：从 C 到 RISC-V 汇编再到电路执行，全链路打通软硬件边界。
- 四个 Project 极具代表性：C 写 Game of Life、RISC-V 汇编写 MNIST 神经网络、Logisim 搭流水线 CPU、OpenMP/SIMD 实现迷你 Numpy。
- 比 N2T 更深更难，覆盖流水线、Cache、虚存与并发，是衔接 CSAPP 与真正体系结构研究（18-447/ETH CA）的桥梁。

## 先修与知识联系

| 方向 | 关联 |
| --- | --- |
| 先修 | CS61A（抽象）、CS61B（数据结构与 C） |
| 平级 | CSAPP Ch.2–6（重叠但本课含电路与 SIMD 更强）、DDCA/N2T（硬件线） |
| 后续 | CS162（OS 依赖虚存/中断理解）、CS152/18-447/ETH CA（进阶体系结构）、CS168/并行课 |
| 知识输出 | 流水线与 Cache 概念 → 6.824 性能分析、15445 BufferPool、深度学习推理优化（SIMD） |

## 最新年份讲义章节目录表（Fa25 排课骨架，20 讲，参照近年公开 syllabus）

| 讲次 | 标题 | 阅读材料 |
| --- | --- | --- |
| L1 | 导论：十大伟大思想与课程地图 | O&D RISC-V Ch.1；61C 课程讲义 |
| L2 | 数字逻辑与布尔电路（Logisim 入门） | O&D Ch.4.1–4.5 |
| L3 | 组合/时序电路、寄存器与时钟 | O&D Ch.4 |
| L4 | RISC-V I：指令格式与算术 | O&D Ch.2；61C 汇编 cheatsheet |
| L5 | RISC-V II：分支、函数调用约定 | O&D Ch.2.7 |
| L6 | RISC-V III：load/store、地址模式 | O&D Ch.2.5–2.6 |
| L7 | C 语言 I：指针、数组与内存布局 | K&R Ch.5；61C C refresher |
| L8 | C 语言 II：结构体、动态内存与字符串 | K&R Ch.6–7；valgrind 手册 |
| L9 | 汇编与 C 的互译、栈帧剖析 | 61C lecture notes + gcc -S 实验 |
| L10 | 数据并行：SIMD 与向量化 | O&D Ch.4.17 / 并行扩展讲义 |
| L11 | 性能度量：延迟/吞吐、Amdahl 定律 | O&D Ch.1.8–1.9 |
| L12 | 存储器层次：Cache 映射与替换 | O&D Ch.5.1–5.4 |
| L13 | 虚拟内存与地址翻译、TLB | O&D Ch.5.5–5.7 |
| L14 | 单周期与多周期数据通路 | O&D Ch.4.13–4.19 |
| L15 | 流水线与三大冒险 | O&D Ch.4.20–4.24 |
| L16 | 分支预测与异常/中断 | O&D Ch.4.25 |
| L17 | 并发 I：线程、锁与内存模型 | O&D App.4.C/D；61C 并发讲义 |
| L18 | 并发 II：OpenMP、GPU 与并行编程模式 | 并行补充讲义 |
| L19 | 专题：ML 芯片/DNN 加速器前沿 | 当期阅读（如 TPU 论文摘选） |
| L20 | 期末复习：软硬件全栈串讲 | 历年 final review 材料 |

## 课程资源（摘自 csdiy）

- 课程网站：官网随学期更新；csdiy 备份 Fa24/Fa20（WayBack）
- 课程视频：Su20/Fa20（B 站与 YouTube）
- 课程作业：4 个 Project + 每周 Lab，Fa20 备份含完整框架
- 资源汇总：PKUFlyingPig/CS61C-summer20、InsideEmpire/CS61C-fall20、RisingUppercut/CS61C-fall24
