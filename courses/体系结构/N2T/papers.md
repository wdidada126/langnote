# Nand2Tetris 论文与前沿清单（papers.md）

> 骨架级清单，正文由后续专人展开。关联讲次对应 notes/outline.md。

## 经典文献

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
| --- | --- | --- | --- |
| A Symbolic Analysis of Relay and Switching Circuits (Shannon) | 1938 | 证明开关电路与布尔代数同构，数字电路设计理论起点 | L1 |
| On Computable Numbers (Turing) | 1936 | 提出图灵机与存储程序思想的可计算性根基 | L4/L9 |
| First Draft of a Report on the EDVAC (von Neumann) | 1945 | 确立存储程序计算机（冯·诺依曼架构）经典设计 | L5 |
| Introduction to VLSI Systems (Mead & Conway) | 1978 | 建立「层次化设计 + 软硬件协同抽象」的现代芯片设计范式 | L12 |
| The Elements of Computing Systems (Nisan & Schocken, 书) | 2005/2008 | 本课教材：用 12 层抽象从 Nand 走到 Tetris | 全课程 |

## 近五年论文（2021–2026）

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
| --- | --- | --- | --- |
| OpenROAD: An Open, Scalable, Silicon-to-Software Framework (IEEE Micro) | 2021 | 开源端到端芯片设计流程，N2T 式教学可衔接真实硅上实现 | L1–L5 |
| Automatic Design of RISC-V Cores for SoCs / CVA6 系列 (DATE) | 2021 | 参数化生成开源 RISC-V 核，「自己造 CPU」的工业化版本 | L5/L6 |
| TinyTapeout: Open-Source Small-Design Chipsets（配套开源项目文） | 2023 | 让学习者把 HDL 小设计以极低成本流片，N2T 精神延续 | L1–L3 |
| RISC-V 教育/压缩指令扩展相关教学论文（如 "Teaking RISC-V..."，持续补充） | 2021–2025 | 用 RISC-V 替代 x86 教授体系结构的基础教育趋势 | L4–L8 |

## 知识点在开源项目中的应用

| 知识点 | 代表开源项目 | 说明 |
| --- | --- | --- |
| HDL 与门级综合 | Yosys、Verilator | 开源综合/仿真工具链，可编译 N2T 风格电路到真实网表 |
| Hack CPU / 寄存器组 | picorv32、PicoSoC | 极简可综合 RISC-V 核，理解 CPU 组装的最小参照物 |
| 汇编器/链接器思路 | LLVM (lld)、GNU binutils | 两段式符号解析是全部真实汇编器的原型 |
| 栈式虚拟机 | CPython vm、JVM 字节码 | jack.vm 与 Python 字节码/JVM 指令同构 |
| 编译器前端 | tree-sitter、 antlr 示例语言 | 递归下降与语法生成器路线可互相印证 |
| 简易 OS | SerenityOS、xv6（对照） | 图形/内存/键盘服务 API 的教学对照 |
| 上板验证 | TinyTapeout、iCEstick/Basys3 FPGA 社区 | 把虚拟硬件跑在真实芯片上 |
