# DDCA 配套项目总览（讲次 → 项目 → 知识点）

> 语言：**Verilog**（iverilog `-g2005` 为编译基准，另 p06 附 C 模拟器 / p05 附 Python 汇编器）。
> 约定：本轮**只写不编译**；每个目录都有 `build.sh`（Linux/macOS/Git Bash）与 `build.bat`（Windows），
> 运行前需安装 [Icarus Verilog](https://steveicarus.github.io/iverilog)（`scoop install iverilog` / `apt install iverilog` / `brew install icarus-verilog`）。
> 每个 testbench 自带自动判定，末行打印 `P0x: ALL TESTS PASSED` 即通过。

## 讲次 → 项目 → 知识点 映射

| 项目 | 对应讲次 | 内容 | 覆盖知识点 |
| --- | --- | --- | --- |
| `p01_comb_alu_mux/` | L02/L03/L04 | mux2、结构化 mux4、2-4 译码器、4 位 8 操作 ALU | 布尔代数/真值表穷举、Mux=可编程连线、译码器、ALU 控制编码表、TB 三件套 |
| `p02_adders/` | L03/L07/L11 | 半加器→全加器→N 位 RCA→4 位 CLA | 进位传播/生成、关键路径 O(N) vs O(log N)、面积换速度、补码加法语义 |
| `p03_ff_regfile/` | L05/L06/L09 | DFF、使能寄存器、模 N 计数器、32×32 寄存器堆 | 边沿触发、使能反馈 Mux、rollover、组合读/同步写、x0 恒零约定 |
| `p04_fsm/` | L06/L10 | "1011" 重叠序列检测器（Mealy）、交通灯（Moore+计时） | FSM 五步流程、三段式写法、失败回退边（KMP 雏形）、Moore/Mealy 输出对齐、default 安全态 |
| `p05_riscv_single/` | L08/L09（+L10/L11 延伸） | 单周期 RV32I 子集 CPU + 简易汇编器 + `.mem` 程序加载 + 自动比对 TB | 取指/译码/执行/访存/写回、指令与立即数编码（I/S/B/J/U）、控制真值表、PC 写回 mux、jal 链接 |
| `p06_memory_cache/` | L07/L13/L14 | 2 路组相联 cache 模型（Verilog）+ 三配置×三 trace 命中率模拟器（C） | tag/set/offset 三段论、LRU 逐出、冲突缺失、写直达+写分配、hit/miss 计数与 AMAT 直觉 |

## 与课程 Lab 的对应关系
ETH 原课 9 个 Lab 在 Basys 3 FPGA（Vivado）上完成；本项目用 iverilog 仿真覆盖其**设计内核**：
p01/p02≈Lab 1–2（组合），p03/p04≈Lab 3–4（时序与 FSM），p05≈Lab 5–7（datapath→单周期 CPU），
p06 对应课程 cache 章节练习（原课为分析题+Logisim-like 观察）。
若要上 FPGA：Vivado 工程直接复用 p01–p05 各 .v（testbench 不参与综合），引脚约束见 H&H App.C。

## 推荐推进顺序（自学闭环）
1. 读对应讲次 notes → 2. 通读设计源（先注释后代码）→ 3. 改一个参数预测输出再跑 build →
4. 做每个 README 的"延伸实验"（p05 的多周期/流水线改造是通向 L10–L12 的主作业）。

## 工具链升级路线（学有余力）
| 工具 | 用途 | 从哪个项目接入 |
| --- | --- | --- |
| Verilator + cocotb | 编译式高速仿真 + Python 随机激励 | p01–p05 任意 TB 重写 |
| Yosys | 开源综合，看门级网表/统计 | p01/p02（化简与面积对照） |
| Spike (riscv-isa-sim) | ISA 黄金模型 trace 对拍 | p05 |
| riscv-tests (`rv32ui`) | 官方指令回归 | p05 汇编器补全后 |
| ChampSim / gem5 | 替换策略与多级层次研究 | p06 |
| Chipyard / XiangShan | 完整开源 SoC 实战 | 全部讲次学完后 |
