# ETH CA 论文与前沿清单（papers.md）

> 本课程以论文为教材，本表挑选贯穿性经典与近五年代表作。关联讲次对应 notes/outline.md。

## 经典论文

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
| --- | --- | --- | --- |
| The Fast Policy for... / Tomasulo An Efficient Algorithm (Tomasulo, IBM JRD) | 1967 | 用寄存器重命名实现乱序执行，超标量奠基算法 | L2 |
| Coherence in Shared Memory Systems (Goodman) / cache-coherence 综述 | 1984(?) | 系统提出共享内存一致性协议框架 | L12–L14 |
| Memory Systems: Cache Coherence (Papamarcos & Patel, SNP '84) 提出 MESI | 1984 | 提出首个实用的 MESI 写无效协议 | L14 |
| An Introduction to Memory Systems / Memory Coherence (Hennessy & Markstein?) → 采用: Cache-Coherence Protocols (Sohi & Goodman 综述) | 1991 | 给出一致性协议分类学，仍是最佳入门综述 | L12–L15 |
| The NoC Book: Route Packets, Not Wires (Dally & Towles) | 2004 | 确立片上网络范式 | L18 |
| FRESCo: Guaranteeing Timing in Multicore / STFM 实时内存调度 | 2008(?) | 内存调度公平性与可预测性的代表作 | L5 |
| Trading DRAM Bandwidth for.../ Ambit (Kim et al., MICRO) | 2015 | 证明可在 DRAM 阵列内直接做逻辑运算 | L9 |
| Flipping Bits in Memory Without Accessing Them: RowHammer (Kim et al., ISCA) | 2014 | 揭示真实 RowHammer 攻击，开创 DRAM 安全方向 | L5 |
| Eyeriss: A Spatial Architecture for Energy-Efficient CNN (Chen et al., ISCA) | 2016 | 提出 dataflow 视角建模 DNN 加速器能效 | L21 |
| A Domain-Specific Architecture for Deep Neural Networks (TPU, Jouppi et al.) | 2017 | 脉动阵列 + 权重固定数据流的工业级 DNN 推理芯片 | L21 |

## 近五年论文（2021–2026）

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
| --- | --- | --- | --- |
| Simplicimonious/ANPL: Automated ... DRAM scheduling for ML (如 Bandwidth-Efficient ... ) | 2021–2023 | 面向 ML 负载的带宽/调度优化 | L3–L5/L17 |
| Aries/RowPress & BLISS: Block-Level ... RowHammer defense 演进 | 2021 | 更低开销的 RowHammer 防御与调度结合 | L5 |
| Iliad / 存内计算编程框架 (UPMEM 生态论文) | 2021–2022 | PIM 落地系统栈与自动数据划分 | L9–L10 |
| AttAcc/GraphPIM: 存内图分析加速 | 2021 | 用 PIM 处理不规则图访存 | L10/L20 |
| SmartNIC/CXL 内存池化 (如 "CXL ... Memory Pooling") | 2022–2023 | 互连/内存解耦新范式，重塑数据中心内存层次 | L8/L18/L19 |
| LLM 推理系统/域专用架构 (如 Aladdin/MAESTRO 建模, Timeloop 演进) | 2021–2024 | 加速器性能建模自动化与稀疏化 | L21 |

## 知识点在开源项目中的应用

| 知识点 | 代表开源项目 | 说明 |
| --- | --- | --- |
| 周期精确处理器模拟 | gem5、Sniper、ChampSim | 课程 Project 的业界等价模拟器 |
| DRAM 调度与 RowHammer 缓解 | Linux EDAC/DRAM 补丁、RowHammer-PoCs | 内核已合入的 tRDRScd 缓解与双行激活防御 |
| PIM/近存计算 | UPMEM SDK、Samsung AiM、HBM-PIM 参考栈 | 真实可编程 PIM 系统栈 |
| 缓存替换/预取 | Hawkeye/SHiP (开源 trace 实现)、Baton | ML 感知替换策略落地 |
| GPU/CXL 内存 | NVIDIA Grace-Hopper NVLink-C2C、CXL 3.0 开源 QEMU/Linux 支持 | 内存池化与异构统一内存 |
| 域专用加速器建模 | Timeloop/Accelergy、MAESTRO、Vitis-AI | DNN 加速器设计与性能建模开源工具 |
