# ETH Zurich CA: Computer Architecture 计算机体系结构

## 课程信息

| 项目 | 内容 |
| --- | --- |
| 课程全称 | Computer Architecture（ETH 代码 220.071，DDCA 的进阶课） |
| 所属学校 | 苏黎世联邦理工学院（ETH Zurich） |
| 主讲 | Onur Mutlu（SafeSYS / ETH-Zurich 系统组） |
| 教材 | 无指定教材，每讲配大量文献；主线参照 Mutlu 课件 + 体系结构经典论文 |
| csdiy 路径 | /体系结构/CA/ |
| 最新期次 | 每年秋季开课；公开课件最新为 2022 秋（B 站有 2020 版搬运；官网 ethz.ch/teaching/ca 滚动更新） |
| 先修要求 | DDCA（官方先修）；语言 C/C++、Verilog；难度 🌟🌟🌟🌟；预计学时 70 小时 + |
| 状态 | 骨架已建，正文待填充 |

## 为什么学

- 体系结构顶级学者 Mutlu 的研究型课程：不只是「怎么造 CPU」，而是内存系统（DRAM/NVM/Flash/PIM）、多核一致性、GPU、互连网络、域专用加速器的前沿全景。
- 阅读材料极丰富，相当于听一学期领域讲座；B 站 UP 建议作为 CMU 18-447 的补充。
- 5 个 Project 偏内存与 Cache：周期精确模拟器 + Verilog MIPS 流水线 RT 实现，理论实践并重。
- 学完能读懂近五年 ASPLOS/ISCA/MICRO 主流论文的问题设定。

## 先修与知识联系

| 方向 | 关联 |
| --- | --- |
| 先修 | DDCA（必须）、CSAPP Ch.5–6 有帮助 |
| 平级 | CS61C（广度类似但深度更高）、18-447（CMU 对应课，可互参） |
| 后续 | 并行与分布式（CS149/6.824 依赖一致性与互连知识）、MLSys（加速器专题）、DRAM 安全方向 6.858 延伸 |
| 知识输出 | RowHammer → 内核缓解补丁；PIM → UPMEM/AiM 开源工具链；调度器研究 → Linux mq-deadline/Borg-Scheduler |

## 最新年份讲义章节目录表（22 讲骨架，对应 2020/2022 秋公开排课主题，每年微调）

| 讲次 | 标题 | 阅读材料 |
| --- | --- | --- |
| L1 | 导论：体系结构研究方法与性能/能耗度量 | 课程讲义；Hennessy-Patterson 获奖文 The Future of Architectures (CACM 2019) |
| L2 | 指令级并行回顾：流水线、乱序执行与超标量 | Shen & Lipasti 教材节选； scoreboard/Tomasulo 经典文 |
| L3 | 内存技术 I：DRAM 原理、行激活与访问机制 | DRAM 教材章 (Mutlu "Main Memory: From Transistors to...")；JEDEC DDR 规范节选 |
| L4 | 内存技术 II：DRAM 缩放瓶颈、3D 堆叠 HBM | HBM 标准文档；"Ambit" MICRO'15（延伸） |
| L5 | 内存调度与安全：公平调度、TWL 与 GoGo 防御 | Mutlu 内存调度系列讲义；RowHammer 论文 MICRO'14 |
| L6 | 非易失内存 I：PCM/ReRAM 器件与系统挑战 | "Write-Backless Caching" 等 PCM 经典；NVM 综述 |
| L7 | 非易失内存 II：Flash 与 SSD 系统栈 | Flash 教材章；SSD FTL 论文 |
| L8 | 存储系统：文件系统与 SSD/OS 协同（FTL/日志） | Bottled I/O (SOSP'13)；CrossLog (OSDI'18) |
| L9 | 存内计算 Processing-in-Memory I：动机与架构 | Ambit、SIMDRAM 论文 |
| L10 | 存内计算 II：PIM 实用化（UPMEM/AiM 生态） | PIM  workshop 论文精选 |
| L11 | 缓存设计：多级缓存、替换策略、预取 | Cache 经典章；"Perceptron-based Prefetching" |
| L12 | 主存与处理协同：内存层次一致性协议入门 | 教材：Memory Consistency 概述 |
| L13 | 多核 I：共享地址空间与可扩展性 | "The Multi-core Power Wall" 等 |
| L14 | 多核 II：缓存一致性协议（MESI/目录协议） | MESI 论文；DirScale 讲义 |
| L15 | 内存一致性与同步：TSO/C++11 模型、内存屏障 | Adve & Ghar 综述；C++11 内存模型文档 |
| L16 | 虚拟内存与页表硬件：TLB、转译旁路 | TLB/页表 walk 论文精选 |
| L17 | GPU 体系结构：SIMT、warp 调度与内存系统 | Lindholm CUDA 论文；GPU 微架构基准文 |
| L18 | 互连与网络：NoC、片上网络与拓扑 | Dally NoC 教材章选 |
| L19 | 异构计算：CPU+GPU+FPGA 与调度 | 异构综述（当期指定） |
| L20 | 域专用架构 I：图分析与生物信息学加速器 | GraphGrind、SAIF 等论文 |
| L21 | 域专用架构 II：机器学习加速与稀疏计算 | Eyeriss、Timeloop 论文 |
| L22 | 期末复习 + 未来方向：内存墙、敏捷硬件、可持续计算 | 全部讲义回顾 |

## 课程资源（摘自 csdiy）

- 课程网站：2020 Fall / 2022 Fall（ethz 公开）
- 课程视频：官网链接；B 站 2020 版搬运
- 课程作业：5 个 Project，多为内存/Cache 相关；Verilog RT 流水线 + C 周期精确模拟器
- 阅读材料：每讲大量文献，「相当于听一学期讲座」
