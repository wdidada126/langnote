# ETH Zurich DDCA: Digital Design and Computer Architecture（【CORE】）

## 课程信息

| 项目 | 内容 |
| --- | --- |
| 课程全称 | Digital Design and Computer Architecture（SS 体系结构入门，ETH 代码 220.070） |
| 所属学校 | 苏黎世联邦理工学院（ETH Zurich） |
| 主讲 | Onur Mutlu |
| 教材 | ① Harris & Harris, 《Digital Design and Computer Architecture》(MIPS Edition, 2/E，中文译本《数字设计和计算机体系结构(原书第2版)》)；② Patt & Patel, 《Introduction to Computing Systems》 |
| csdiy 路径 | /体系结构/DDCA/ |
| 最新期次 | 每年秋季开课；公开课件最新为 2023 秋季（csdiy 收录 2020/2023），实验平台 Basys 3 FPGA + Xilinx Vivado |
| 先修要求 | CS50 或同阶课程，最好有 C 语言基础；语言 C/Verilog/MIPS/LC-3 汇编；难度 🌟🌟🌟；预计学时 100 小时 |
| 状态 | 【CORE】骨架已建（本 README 含全章节目录），notes/papers/projects 正文由后续专人完成 |

## 为什么学

- 体系结构大牛 Onur Mutlu 亲自授课，从晶体管、逻辑门一路讲到微架构、缓存与虚拟内存，是「从零造 CPU」最扎实的学院派路线。
- 9 个 FPGA Lab（Basys 3 + Vivado）带你从组合电路、时序电路逐级搭建完整 MIPS CPU，动手成分远超一般理论课。
- 是 ETH CA（Computer Architecture，同教授进阶课）与 MIT 6.004 的官方先修，也是读懂 CSAPP 第 4 章硬件模型的最佳搭档。
- 除 Lab 答案与当期考试答案外资料全部开源，还穿插体系结构领域最新研究进展介绍。

## 先修与知识联系

| 方向 | 关联课程/知识 |
| --- | --- |
| 先修 | CS50/CS61A 级别的编程基础、C 语言 |
| 平级互补 | N2T（更轻量的同主题路线）、CS61C（同主题但广度更大）、CSAPP Ch.4（Y86 与本课 MIPS 对照） |
| 后续 | ETH CA（Mutlu 进阶课，直接先修）、15-447（CMU 对应进阶）、6.004（MIT） |
| 知识输出 | Verilog/数字电路 → Chisel/FPGA 生态、RISC-V 开源芯片（Chipyard/OpenC910） |

## 最新年份讲义全章节目录（对应 2023 秋季课程排课与 Harris & Harris 2/E 章节）

| 讲次 | 标题 | 阅读材料（教材章节） |
| --- | --- | --- |
| L1 | 课程导论：从开关到计算机系统（Patt & Patel Ch.1 视角） | H&H Ch.1；P&P Ch.1 |
| L2 | 组合逻辑 I：布尔代数、逻辑门、真值表 | H&H Ch.2 |
| L3 | 组合逻辑 II：加法器、ALU、多路选择器、编码器/译码器 | H&H Ch.2–3 |
| L4 | Verilog 硬件描述语言与 Vivado/FPGA 工具链 | H&H App.B/C；Lab 1–2 手册 |
| L5 | 时序逻辑：锁存器、触发器、寄存器、计数器 | H&H Ch.5 |
| L6 | 有限状态机（FSM）：建模、状态编码与实现 | H&H Ch.5 |
| L7 | 存储元件与算术：RAM/ROM、移位器、补码算术、乘法器 | H&H Ch.4–5；P&P Ch.4–5 |
| L8 | 从 C 到硬件：MIPS 指令集架构与编译执行全过程 | H&H Ch.6；P&P Ch.4 |
| L9 | 单周期微架构：数据通路、控制单元、指令周期分析 | H&H Ch.6 |
| L10 | 多周期微架构：指令分阶段与状态机控制 | H&H Ch.6 |
| L11 | 流水线（I）：理想流水线、加速比、结构/数据冒险 | H&H Ch.7 |
| L12 | 流水线（II）：控制冒险、转发（forwarding）、MIPS 流水线实现 | H&H Ch.7 |
| L13 | 缓存：映射方式、替换策略、写策略与平均访存时间 | H&H Ch.5/8；补充 Mutlu 讲义 |
| L14 | 虚拟内存与地址翻译：页表、TLB、与缓存的配合 | H&H Ch.4.6–4.7 + 补充讲义 |
| L15 | I/O、总线和系统：把 CPU 接进一台完整计算机 | H&H Ch.9；P&P 相应章节 |
| L16 | 期末复习：从晶体管到完整系统的贯穿串讲 + 前沿研究导览 | 全部讲义回顾 |

> 实验共 9 个（Lab 1–9）：组合电路 → 时序电路 → FSM（交通灯等）→ 数据通路 → 单周期 CPU → 流水线 CPU，全部在 Basys 3 FPGA 上部署验证；课程另含 LC-3 汇编作业（源自 P&P 教材路线）。

## 课程资源（摘自 csdiy）

- 课程网站：2020 / 2023 版（ethz.ch 公开）
- 课程视频：YouTube 官方；B 站 2020 版搬运
- 课程实验：9 个实验从零设计 MIPS CPU，详见课程网站
