# p05 单周期 RV32I CPU（取指/译码/执行/访存/写回 + 简易汇编器 + .mem 程序加载）

## 对应讲次
- notes/L08.md（ISA、指令格式、立即数编码——`asm2mem.py` 就是"译码器的逆运算"）
- notes/L09.md（本项目的主体：单周期数据通路 + 控制真值表 + 指令周期）
- 复用件思想来自 p01（ALU/mux）、p02（加法）、p03（寄存器堆）
- 下一步改造（流水线/多周期）见 notes/L10–L12 与下方延伸实验

## 文件说明
| 文件 | 内容 |
| --- | --- |
| `riscv_single.v` | CPU 顶层：PC+imem→字段译码→RF→ALU→dmem→写回 mux→PC 更新 |
| `imem.v` | `$readmemh("prog.mem")` 加载程序，组合读出 |
| `dmem.v` | 基址 0x1000 的同步写/组合读数据存储器，越界/非对齐保护 |
| `asm2mem.py` | 简易汇编器（标签两遍扫描；支持子集见文件头 docstring） |
| `prog.s` | 演示程序：算术/逻辑/lui/sw-lw/beq(不跳)/jal(链接+跳过)/sll/srl/循环 bne/halt |
| `prog.mem` | 汇编产物（25 字，每行 8 位十六进制，与 Spike 可交叉验证） |
| `tb_p05.v` | 复位→跑到 halt→自动比对 13 个寄存器终值 + dmem[0]，并转储 RF |

### 指令子集（RV32I + 自定义 halt=custom-0）
`lui addi andi ori xori slli srli add sub and or xor sll srl slt sltu lw sw beq bne jal halt`
（srai/lb/sb/jalr/csr 等刻意留作练习；x0 恒零。）

## 编译与运行（需安装 iverilog）
```sh
cd p05_riscv_single
./build.sh          # 或 build.bat
iverilog -g2005 -o sim.vvp tb_p05.v riscv_single.v imem.v dmem.v
vvp sim.vvp         # 期望：P05: ALL TESTS PASSED + 寄存器转储
# 改程序流程：编辑 prog.s -> python asm2mem.py prog.s prog.mem -> 重跑 build
```

## 知识点对照（每条指令在 TB 中被哪一段覆盖）
- addi/sub/and/or/xor：ALU 多操作复用（L03 §1.4）。
- lui：immU 直通加法（RSIC-V 拼 32 位常数的第一课）。
- sw/lw：地址=rs1+imm 复用 ALU、MemtoReg 写回 mux（L09 §1.2）；x13 链验证"存了再取"。
- beq 未跳/jal 真跳：PC 写回 mux 优先级（jump>branch>pc+4，L09 §4）。
- bne 负偏移回跳：B 型立即数散位列 + 符号扩展（L08 1.5 RISC-V 编码之美）。
- x15=jal 链接值 64：PC+4 写回（函数调用约定的硬件基础）。

## 延伸实验
1. **加 srai 与 shadd**：改译码表 + ALU，体会"ISA 加一条指令 = 表加一行 + datapath 加一根线"。
2. **多周期改造**（L10）：把 lw 拆成"算地址拍→访存拍→写回拍"，加 `state` FSM 与微操作表。
3. **两级流水 + load-use stall**（L11/L12）：在 EX 前插流水寄存器，用 p05 的程序测 CPI。
4. **接 riscv-tests**：用 Spike(`spike --isa=rv32i`) 或 `riscv64-unknown-elf-gcc -march=rv32i` 生成 ELF→转 mem，对拍日志。
5. 对照 PicoRV32（`picorv32.v`）逐段读源码，标出与本实现相同的五个动作。
