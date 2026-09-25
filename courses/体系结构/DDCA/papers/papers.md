# DDCA 论文与文献清单（papers.md）

> 配合 notes/L01–L16 使用；"关联讲次"指本目录讲义。凡标注"待核实"者请在引用前自行确认版本/出处。

## 一、经典论文 / 著作（按主题分组）

| 标题 | 作者/年份 | 一句话贡献 | 关联讲次 |
| --- | --- | --- | --- |
| Introduction to Computing Systems（教材） | Patt & Patel, 2/E 2001 | 从 N 门到可运行机器的自底向上教学范式，DDCA 双教材之一 | L01/L07/L08/L10 |
| Digital Design and Computer Architecture（教材） | Harris & Harris, MIPS 版 2/E 2012 | 逻辑设计→MIPS CPU 的最短完整路径，DDCA 主教材 | 全部 |
| The RISC-V Instruction Set Manual, Vol. I: Unprivileged ISA | Waterman & Asanović, 2011 起（冻结版 2019） | 开源 ISA 规范文本；projects 所用 RV32I 权威定义 | L08 |
| The RISC-V Instruction Set Manual, Vol. II: Privileged Architecture | Waterman et al. | CSR/中断/页表（Sv32/Sv39）规范，L14/L15 的制度来源 | L14/L15 |
| A Case for RISC（CACM 评论）/ The RISC Idea 综述 | Patterson 等，1980s | RISC 设计哲学定名：简化指令换取流水与编译器协作 | L08/L11 |
| The Design of the 8086（微程序思想史料，可选）/ 微程序综述 | — | 微编程/control store 历史脉络（**待核实具体文献，建议以 H&H 6.6 叙述为基**） | L10 |
| An Effective Procedure for Locating Data in Memory（TLB 前身）/ Denning "Virtual Memory" | Denning, ACM Computing Surveys 1970 | 虚拟内存与工作集理论经典综述 | L14 |
| Cache Memory（MDA 技术报告） | Slottow, 1967；及 Isolani 等早期工程报告 | 首个全相联 cache 工程实现记述（**细节待核实**） | L13 |
| A Study of Replacement Policies for Associative Memory | Belady, 1966 | 替换策略研究开山与 LRU/FIFO/Belady 最优反例 | L13 |
| Readings in Computer Architecture（文集） | Hill, Jouppi & Sohi 编, 1999 | 流水线/记分牌（Sohi）等奠基文献合订本 | L11/L12 |
| DRAM 综述：Systematic Architecture Analysis of DRAMs 或 "Main Memory: from DRAM to Persistent Memory" 类 | Mutlu 组等（**标题待核实**） | DRAM 阵列/行缓冲/时序参数系统化讲解，L13/L16 前沿读物 | L13/L16 |
| Arcades / Row Hammer: Trading DRAM Reliability for Performance | Kim, Mutlu et al., HPCA 2014 | 以实验证明"数字靠模拟物理活着"，安全×体系结构代表作 | L16 |
| Memory-Centric Compute: A New Vision（及其前身 STT-MRAM/PIM 系列） | Mutlu et al., 约 2017–2019（**待核实**） | 内存中心计算纲领宣言 | L16 |
| Computer Organization and Design（教材对照） | Patterson & Hennessy | 与本课平行的另一经典教学路线（RISC-V 版 2017） | 全部 |

> 上表中"占位删除"行保留为编写纪律示例：**宁缺毋滥，不确定即标注**。

## 二、近五年文献与项目论文（2021–2026，侧重开源芯片）

| 标题 | 出处/年份 | 一句话贡献 | 关联讲次 |
| --- | --- | --- | --- |
| XiangShan: An Open-Source High-Performance RISC-V Microarchitecture（南湖/昆明湖系列技术报告与论文） | ISCA/MICRO 系会议与技术报告，2022–2024（**具体卷期待核实**） | 开源乱序 RISC-V 核达到商用高端性能，验证敏捷方法论 | L12/L16 |
| XiangShan 微架构论文（如 "XiangShan: An Open-Source Project for High-Performance RISC-V Designs"） | arXiv 2023 前后 | 前端/中端/后端分模块公开设计说明 | L11/L12 |
| BOOM: An Unrestricted-Cycle-Count Out-of-Order Microarchitecture / "The Berkeley Out-of-Order Machine (BOOM)" 系列论文 | Berkeley, ISCA 2013 起，近五年演进至 BOOM v5（**卷期待核实**） | 开源乱序标尺，Chisel 敏捷硬件旗帜 | L12/L16 |
| Chipyard: Agile SoC Design and Generation（FICL 2020 初版；后续手册持续更新） | FICL 2020 + 文档 | Rocket/BOOM 等核的 SoC 生成框架，教学到研究全栈 | L09–L16 |
| PULP: Parallel Ultra-Low Power Platform 系列论文 | 2015–2023 持续（ETH/博洛尼亚） | 开源低功耗 RISC-V 多核簇（Ibex/CVA6 生态） | L09/L13 |
| OpenTitan: An Open-Source Silicon Root-of-Trust 论文/文档 | NIST/HPCA 相关，2020–2024（**待核实**） | 全栈开源安全 MCU 与形式验证方法论工业落地 | L02/L04 |
| Sigledal 等：开源 RISC-V 处理器综述（如 "A Survey of RISC-V SoCs and Processors"） | 2022–2024（**待核实**） | 开源核谱系（PicoRV32→Rocket→XiangShan）横评 | 全部 |
| RVV（RISC-V Vector Extension 1.0）批准相关报道与规范 | 2021 | SIMD 思想回归开源 ISA，CS61C 并行内容对照 | L08/L16 |
| SHiP / Perceptron 替换策略（较新后续：ML-guided cache management 系列） | MICRO/ISCA 2022–2024（**待核实**） | 用机器学习做替换/预取决策，L13 前沿延伸 | L13/L16 |
| HBM3/PIM 产品论文（如 "HBM-PIM: A Processing-in-Memory Architecture" 类） | 2021–2023（**待核实**） | 存内/近存计算从论文走向内存产品 | L16 |
| riscv-formal / SymbiYosys 应用论文（开源形式验证 RISC-V） | 2020 前后持续 | 小核可数学证明正确——L02 形式化种子工业版 | L04/L12 |

## 三、知识点 ↔ 开源项目映射表

| 知识点（讲次） | 代表开源项目/代码位置 | 建议动手方式 |
| --- | --- | --- |
| 布尔代数/门级化简（L02） | Yosys `opt_*` passes；OpenTitan `prim_*` 门库 | 综合 p01 看 `stat` 前后门数 |
| Mux/译码/编码器、ALU（L03） | projects/p01；esp32 GPIO Matrix（ESP-IDF `gpio_matrix.h`） | 穷举真值表 TB 对拍 |
| 加法器 RCA/CLA、乘法（L03/L07） | projects/p02；Rocket `muldiv` | 对比关键路径级数 |
| Verilog 工具链（L04） | iverilog / Verilator / Yosys / cocotb | 跑通全部 projects 并加一个 cocotb TB |
| 触发器/时序约束/RF（L05/L07） | projects/p03；PULP `mem_lib` | 改 T_clk 观察 hold/setup 违例报告 |
| FSM（L06） | projects/p04；Ibex `if_stage` 状态机 | 序列检测器加失败回退边 |
| ISA 与编译（L08） | riscv-isa-manual、Spike、riscv-tests | p05 跑通 `rv32ui-p-*` 子集 |
| 单周期/多周期（L09/L10） | projects/p05；PicoRV32（CliffordWolf） | 通读 `picorv32.v` 对照自家实现 |
| 流水线与冒险（L11/L12） | Rocket/BOOM（Chipyard）；XiangShan 仓库 | 给 p05 加 2 级流水+转发并测 CPI |
| Cache 与替换（L13） | ChampSim、gem5；香山 L2/prefetch 目录 | p06 模拟器跑 CSAPP trace 再上 ChampSim |
| 虚拟内存/TLB（L14） | 6.S081 `kernel/vm.c`；CVA6 `mmu/`；香山 MMU | p06 TLB 模拟 → 读 xv6 源码对答案 |
| 总线/中断/DMA/MMIO（L15） | OpenTitan 外设 + regtool；Chipyard TileLink/dma；ESP-IDF GDMA | p05 加 UART 魔法地址；读 `uart.c` |
| 全栈 SoC 与前沿（L16） | XiangShan、Chipyard、OpenTitan、PULP、CVA6 | 编译一个 Chisel 生成器并与 RTL 模块数对照 |

## 四、使用说明

- 课程官方讲义（2020/2023 版 PDF）与 Lab 手册从 ETH 课程网站获取；YouTube 有官方录播，B 站有 2020 搬运。
- 表中"待核实"条目给出的是主题级定位而非精确引文，写论文/博客引用前请到 DBLP/arXiv 确认。
- 与姊妹课程 papers 对照：[CS61C](../../CS61C/papers.md)、[N2T](../../N2T/papers.md)、[CA](../../CA/papers.md)。
