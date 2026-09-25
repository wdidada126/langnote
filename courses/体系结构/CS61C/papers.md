# CS61C 论文与前沿清单（papers.md）

> 骨架级清单，正文由后续专人展开。关联讲次对应 notes/outline.md。

## 经典论文/著作

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
| --- | --- | --- | --- |
| The Design of RISC I: A VLSI Processor for UNIX (Patterson et al., ISCA) | 1981 | Berkeley RISC 代表作：寄存器窗口与精简指令集落地，RISC-V 思想源头 | L4–L6/L14 |
| The Design of the Mathematical Logic Computer of the IBM Stretch (Bloch, IBM JRD) | 1961 | 确立流水线、交错存储等经典微架构技术 | L14–L16 |
| Virtual Memory (Denning, ACM Computing Surveys) | 1970 | 虚拟化内存的经典综述，分页/置换/局部性理论定名 | L12–L13 |
| Programming a Microprocessor to Compute... / GPU 奠基: "The CUDA Programming Model" 相关 NVIDIA 白皮书 | 2008 | 定义 SIMT 并行编程模型，L18 GPU 内容参照 | L18 |
| The Anatomy of the Tensor Processing Unit / TPU: "TPU: A Domain-Specific Architecture" (Jouppi et al., ISCA) | 2017 | 面向 DNN 推理的脉动阵列域专用架构，L19 专题核心读物 | L19 |
| Roofline: An Insightful Visual Performance Model (Williams, Waterman & Patterson, CACM) | 2009 | 以算术强度界定计算/带宽瓶颈，性能分析可视化利器 | L11/L19 |

## 近五年论文（2021–2026）

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
| --- | --- | --- | --- |
| Chipyard: A Collaborative Framework for Agile SoC Design (FICL) | 2021 | 用 Chisel 敏捷生成 RISC-V SoC，教学级 CPU 设计工业化 | L14–L16 |
| Understanding DRAM-Related Performance in ML Workloads（存储墙系列，如 "Memory-Centric Workload Characterization"） | 2021 | 量化「内存墙」对深度学习的制约 | L12–L13/L19 |
| A Domain-Specific Architecture for...（存内计算 Processing-in-Memory, 如 Samsung HBM-PIM / UPMEM 论文） | 2021–2022 | 把计算搬进内存，突破数据搬运瓶颈的前沿方向 | L12/L19 |
| RISC-V 生态与虚拟化/向量扩展（RVV）综述类论文 | 2021–2024 | RISC-V 向量扩展让 SIMD 内容在开源指令集上落地 | L10 |

## 知识点在开源项目中的应用

| 知识点 | 代表开源项目 | 说明 |
| --- | --- | --- |
| RISC-V 指令集/数据通路 | Berkeley Rocket Chip、CVA6、PicoRV32 | 可综合 RISC-V 核，验证流水线与冒险处理 |
| Logisim 搭 CPU 教学 | Logisim-Evolution、Digital | Project 3 的现代等价工具 |
| SIMD/OpenMP 矩阵运算 | Eigen、BLIS、OpenBLAS | 向量化 + 分块 + 多级缓存优化的教科书级实现 |
| Cache 分析与模拟 | gem5、ChampSim | 周期级模拟器做缺失率/替换策略实验 |
| 汇编↔C 互译理解 | Compiler Explorer (godbolt) | 实时观察 -O 级别下的 RISC-V/ARM 代码生成 |
| TPU/加速器思想 | Vitis AI、TVM、Gloo | 域专用编译与算子调度落地 |
