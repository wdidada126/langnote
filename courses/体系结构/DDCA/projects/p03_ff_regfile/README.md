# p03 时序元件：D 触发器 → 使能寄存器 → 计数器 → 32×32 寄存器堆

## 对应讲次
- notes/L05.md §1.2（DFF）、§1.4（寄存器与寄存器堆）、§1.5（计数器/分频）
- notes/L06.md §1.2（"计数器是最小 FSM"）
- notes/L09.md §1.2（寄存器堆是单周期 CPU 的读/写口部件）

## 知识点
- `dff.v`：上升沿 + 异步低有效复位；对比同步/异步两种写法（讲义 §4 坑 3）。
- `reg_en.v`：**n 位寄存器 = n 个 DFF + 使能反馈 Mux**——L09/L10 一切 datapath 寄存器的模板。
- `counter.v`：同步模 N 计数器 + rollover 输出；理解"en=0 隐式保持是 FF 不是 latch"。
- `regfile.v`：32×32，双组合读口 + 单同步写口，x0 恒零（RISC-V 约定）；行为级数组模型可被 iverilog 仿真、可被综合器推断为 RF/SRAM。
- `tb_p03.v`：单时钟域自动判定：装载/保持/回绕/零寄存器/复位。

## 编译与运行（需安装 iverilog）
```sh
cd p03_ff_regfile
./build.sh          # 或 build.bat
iverilog -g2005 -o sim.vvp tb_p03.v dff.v reg_en.v counter.v regfile.v
vvp sim.vvp         # 期望：P03: ALL TESTS PASSED
```

## 延伸实验
1. 给 regfile 加同步读模式（RISC-V 常用 1 拍读）：对比 L09 单周期 datapath 需要怎样多一拍。
2. 把 counter 改写成显式 FSM（10 状态独热），两版对拍——体会 L06 "计数器=FSM 特例"。
3. 用 reg_en 拼一个 8 位移位寄存器（en 装载 + 移位两种模式 Mux），即 L07 桶形移位器的 1 位版。
