# p01 组合逻辑：Mux / 译码器 / 4 位 ALU

## 对应讲次
- notes/L02.md（布尔代数与真值表穷举验证方法）
- notes/L03.md §1.3（Mux/译码器）、§1.4（ALU=并行功能阵列+输出选择 Mux）
- notes/L04.md（testbench 组织方式）

## 知识点
- `mux2.v`：参数化位宽 2 选 1 Mux（`assign` 连续赋值 = 组合逻辑）。
- `mux4.v`：**结构化建模**，3 个 mux2 实例拼 4 选 1——层次化设计第一次实践。
- `decoder.v`：2-4 译码器带使能；高有效独热输出；是 L07 存储阵列行译码的原子。
- `alu.v`：8 操作 4 位 ALU + zero 标志；`case` 描述"功能由选择线决定"的真值表压缩形态。
- `tb_p01.v`：穷举 2048 向量对照行为级期望，自动打印 PASS/FAIL——"组合逻辑可全检"（L02 §1.2）。

## 编译与运行（需安装 iverilog）
```sh
cd p01_comb_alu_mux
./build.sh          # Linux/macOS；Windows 双击/命令行 build.bat
# 等价手动命令：
iverilog -g2005 -o sim.vvp tb_p01.v mux2.v mux4.v decoder.v alu.v
vvp sim.vvp         # 期望末行输出：P01: ALL TESTS PASSED
```

## 延伸实验
1. 把 mux4 改写成行为级 `assign y = dd_i[sel]`，对比两种写法综合出的门级网表（`yosys -m verilog` 可选）。
2. 给 alu 增加算术右移（funct=3'b111 改为 sra，slt 另开一位 funct），同步补 TB 向量。
3. 思考：本 ALU 的 8 种功能对应的"控制编码表"如何推广到 L09 的 ALUOp 信号？
