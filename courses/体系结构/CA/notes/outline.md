# ETH CA 讲义骨架（notes/outline.md）

> 每讲 3–5 条要点，骨架级。研究型课程，要点以「问题-方法-权衡」组织。

## L1 导论
- 体系结构 = 在性能/能耗/面积/成本间做量化权衡。
- CPU 时间分解：指令数 × CPI × 时钟周期，逐层找瓶颈。
- 课程主线：从「计算墙」转向「数据搬运墙（内存墙）」。
- 研究方法：benchmark + 模拟 + 假设检验。

## L2 指令级并行回顾
- 超标量、乱序执行（Tomasulo）、寄存器重命名。
- ILP 天花板：依赖链与分支误 predicted。
- 为后续多核/并行讲做铺垫。

## L3 内存技术 I：DRAM
- 1T1C 单元：电荷存储→刷新与破坏性读。
- 访问序列 ACT→READ→PRE，行缓冲（row buffer）命中即快。
- 行冲突（row buffer conflict）是尾延迟主因。
- DDR 通道/bank/组交织。

## L4 内存技术 II：DRAM 缩放与 HBM
- 电容微缩极限：保持时间下降、刷新开销上升。
- 3D 堆叠（HBM/HMC）用宽接口换带宽。
- Bank-level 并行与通道并行的收益/代价。

## L5 内存调度与安全
- 公平/低延迟内存调度器（STFM、PAR-BL）。
- RowHammer：反复激活引发行间位翻转，安全漏洞。
- TRR、TWL、GoGo 等缓解机制与开销。

## L6 非易失内存 I：PCM/ReRAM
- 器件特性：非易失、字节可寻址、写慢于读、写次数有限。
- 写干扰、耐久性问题与磨损均衡。
- 存储级内存（SCM）对 OS/文件系统的冲击。

## L7 非易失内存 II：Flash/SSD
- NAND 页/块/擦除语义与「读改写」。
- FTL：地址映射、垃圾回收、写放大。
- SLC/MLC/TLC/QLC 密度与可靠性权衡。

## L8 存储系统与 OS 协同
- 文件系统与 SSD 语义错配（块设备假设）。
- 日志结构、bottled I/O、CrossLog 减少元数据同步开销。
- 掉电一致性与原子写。

## L9 存内计算 I
- 数据搬运能耗远大于计算，PIM 把算子下沉到 DRAM bank。
- Ambit（DRAM 内位运算/拷贝）、SIMDRAM 矩阵向量乘。
- 并行粒度受 bank/channel 结构约束。

## L10 存内计算 II：实用化
- UPMEM/DAP、Samsung AiM、HBM2-PIM 系统栈。
- 编程模型与数据划分是落地难点。
- 与近存计算（near-memory）路线对比。

## L11 缓存设计
- 替换策略：LRU 局限、SHiP/Hawkeye 感知预测。
- 预取： stride、delta、perceptron/ML 预取。
- 非包含 vs 包含层次、victim cache。

## L12 内存层次与协议入门
- 从单缓存到多缓存一致性问题浮现。
- snoop vs directory 两种发现机制。

## L13 多核 I
- 频率停滞→多核时代；扩展性由共享资源瓶颈决定。
- 功耗墙与暗硅（dark silicon）。

## L14 多核 II：缓存一致性
- MESI 四状态协议与总线嗅探。
- 目录协议（full/limited pointer）扩展到大核数。
- 内存排序与一致性协议正交。

## L15 内存一致性与同步
- 顺序一致 vs TSO vs 弱内存模型。
- acquire/release 语义与内存屏障映射。
- happens-before 与数据竞争定义。

## L16 虚拟内存与页表硬件
- 多级页表、TLB 层次、页表遍历（walk）机制。
- TLB reach 与大页；转译旁路成本。
- 内存虚拟化（两级转译）开销。

## L17 GPU 体系结构
- SIMT/warp 执行、大规模多线程隐藏延迟。
- GPU 内存层级（寄存器/共享/L2/HBM）与 warp divergence。
- 图形/通用双管线与调度器。

## L18 互连与网络
- 片上网络 NoC：拓扑、路由、流控。
- 网络-on-chip 是多核/GPU 可扩展关键。

## L19 异构计算
- CPU+GPU+FPGA/加速器协同与任务划分。
- 统一内存与数据迁移瓶颈（NVLink/CXL）。

## L20 域专用架构 I
- 图分析（不规则访存）→ GraphGrind/SAIF 等。
- 生物信息学（Smith-Waterman）加速。
- 域特征决定硬件形态。

## L21 域专用架构 II：ML 加速
- DNN 数据流（weight/stationary/output-stationary）。
- 脉动阵列、Eyeriss、Timeloop 建模。
- 稀疏加速与量化。

## L22 复习与未来
- 贯穿主线：内存墙、数据搬运、可扩展性。
- 敏捷硬件（Chisel）、可持续计算、域专用体系结构（Hennessy-Patterson 新黄金时代）。
- 论文精读方法与研究选题导引。
