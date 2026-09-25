# CMU 15-213: CSAPP 计算机系统基础（【CORE】）

## 课程信息

| 项目 | 内容 |
| --- | --- |
| 课程全称 | 15-213: Introduction to Computer Systems（配套教材即 CSAPP） |
| 所属学校 | 卡内基梅隆大学（CMU） |
| 主讲 | Randal E. Bryant & David R. O'Hallaron（教材作者） |
| 教材 | Computer Systems: A Programmer's Perspective, 3/E（CSAPP 3/e 中文版《深入理解计算机系统》第 3 版） |
| csdiy 路径 | /计算机系统基础/CSAPP/ |
| 最新期次 | 每年秋季学期开课；课程官网 http://csapp.cs.cmu.edu/ 长期公开全部课件与 Lab |
| 先修要求 | CS61A、CS61B（csdiy 标注）；编程语言 C；难度 🌟🌟🌟🌟🌟；预计学时 150 小时 |
| 状态 | 【CORE】骨架已建（本 README 含全章节目录），notes/papers/projects 正文由后续专人完成 |

## 为什么学

- CMU 镇系神课，系统入门第一课：内容覆盖数据表示、汇编、体系结构、链接、异常控制流、虚拟内存、并发、网络，兼具深度与广度。
- 11 个经典 Lab（Data/Bomb/Attack/Architecture/Cache/Tsh/Malloc/Proxy 等）全部开源框架，是锤炼 C 代码与底层调试能力的最佳途径。
- 是 DDCA、CS61C、6.S081、CS162、15-445、6.824 等后续课程公认的先修基石。
- 配套阅读建议：《程序员的自我修养——链接、装载与库》（补充第 7 章链接理解）；北大大二课程版本即此课。

## 先修与知识联系

| 方向 | 关联课程/知识 |
| --- | --- |
| 先修 | CS61A（程序抽象）、CS61B（数据结构与 C 基础） |
| 后续向下 | DDCA / N2T / CS61C（硬件与体系结构视角）、MIT6.S081 / CS162 / NJUOS / HITOS（操作系统） |
| 平级支撑 | 15-445（内存与存储基础）、6.824 / CS149（进程、线程、网络与并发）、CS144 / topdown（Socket 网络编程对应第 11 章） |
| 直接复用 | CSAPP 第 9 章虚拟内存 → 所有 OS 课；第 12 章并发 → 15445 线程池、6.824 并发模型 |

## 最新年份讲义全章节目录（对应 CSAPP 3/e 章节，15-213 秋季标准排课）

| 讲次 | 标题 | 阅读材料（教材章节） |
| --- | --- | --- |
| L1 | 课程导论：信息、系统抽象与程序生命周期 | CSAPP Ch.1；前言与 Ch.1 全文 |
| L2 | 数据的机器级表示：位运算、整数（补码/溢出） | CSAPP Ch.2.1–2.3；Ch.2.10（C 陷阱） |
| L3 | 数据的机器级表示：浮点数与 IEEE 754 | CSAPP Ch.2.4；Data Lab 发布 |
| L4 | 机器级程序（I）：x86-64 寄存器、操作数与算术 | CSAPP Ch.3.1–3.6；Bomb Lab 发布 |
| L5 | 机器级程序（II）：控制与分支的汇编实现 | CSAPP Ch.3.6–3.7 |
| L6 | 机器级程序（III）：过程、栈帧与递归 | CSAPP Ch.3.8；（Bomb Lab 截止） |
| L7 | 机器级程序（IV）：数据结构、对齐与缓冲区 | CSAPP Ch.3.9–3.11；Attack Lab 发布 |
| L8 | 处理器与硬件：Y86-64 HCL 模型、模拟器 | CSAPP Ch.4（重点 4.1–4.5）；Architecture Lab 发布 |
| L9 | 程序性能优化：消除循环低效率、过程间优化 | CSAPP Ch.5.1–5.11、5.14–5.16；Performance 材料 |
| L10 | 存储器层次结构与缓存 | CSAPP Ch.6；Cache Lab 发布 |
| L11 | 代码优化进阶：循环展开、SIMD 与向量化 | CSAPP Ch.5.12–5.13、5.17 |
| L12 | 链接：目标文件、符号解析、重定位 | CSAPP Ch.7.1–7.9；（Attack Lab 截止） |
| L13 | 共享库、位置无关代码与程序装载 | CSAPP Ch.7.10–7.12；《程序员的自我修养》选读 |
| L14 | 异常控制流：进程与系统级 I/O 回顾 | CSAPP Ch.8.1–8.5 |
| L15 | 进程、信号与并发 ECF | CSAPP Ch.8.5–8.6；Shell Lab 发布 |
| L16 | 虚拟内存：地址空间、页表与 VM 系统调用 | CSAPP Ch.9.1–9.8 |
| L17 | 动态内存分配：malloc/free 与分配器设计 | CSAPP Ch.9.9–9.10；Malloc Lab 发布 |
| L18 | 系统级 I/O、文件与 Unix I/O | CSAPP Ch.10 |
| L19 | 网络编程与 Client-Server | CSAPP Ch.11；Proxy Lab 发布 |
| L20 | 并发编程：线程、线程安全与竞争 | CSAPP Ch.12 |
| L21 | 并行编程：线程池、同步模式与性能 | Ch.12 复习 + Ch.4/5 并行视角；Proxy Lab 截止 |
| L22 | 综合复习：系统全栈串讲 | 全书各章小结（每章 "Understanding Issues"） |

> 课程另有 2 个复习 Q&A 课与期中/期末测验；Lab 共 11 个（含未单列的 Data/Bomb 等，以官网发布节奏为准）。

## 课程资源（摘自 csdiy）

- 课程网站：http://csapp.cs.cmu.edu/
- 课程视频：B 站 BV1iW411d7hd（另有官方 lecture 视频）
- 课程作业：11 个 Project/Lab，代码框架全部开源
- 参考笔记：Arthals 北大 ICS Lab 笔记；九曲阑干 CSAPP 中文讲解
