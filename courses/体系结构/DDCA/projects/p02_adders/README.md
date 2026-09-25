# p02 加法器：半加器 → 全加器 → 行波进位(RCA) / 超前进位(CLA)

## 对应讲次
- notes/L03.md §1.1–1.2（加法器家族、减法复用、补码预告）
- notes/L07.md §1.4（RCA 的模 2^n 语义与溢出）
- notes/L11.md §1.2（"最长段定 T_clk"——本项目的 RCA/CLA 是关键路径分析第一个实例）

## 知识点
- `half_adder.v`：S=A⊕B，C=A·B。
- `full_adder.v`：**结构化**——两个半加器+或门拼成全加器。
- `rca.v`：参数化 N 位行波进位；`generate for` 展开；关键路径随 N 线性增长。
- `cla4.v`：4 位超前进位；G/P 布尔式直写，进位两级门并行产生——与 rca 对照即"面积换速度"。
- `tb_p02.v`：4 位穷举 512 向量三方对拍（rca、cla、行为级期望），8 位随机抽查。

## 编译与运行（需安装 iverilog）
```sh
cd p02_adders
./build.sh          # 或 build.bat
iverilog -g2005 -o sim.vvp tb_p02.v half_adder.v full_adder.v rca.v cla4.v
vvp sim.vvp         # 期望：P02: ALL TESTS PASSED
```

## 延伸实验
1. 用 cla4 + 组间超前进位（G=P·g 组合）拼 16 位两级 CLA，比较 8 位 rca 的估计延迟。
2. 给 rca 传参 N=16/32，用 `yosys stat` 看单元数是否线性（O(N) 门）；再估 CLA 门数（指数展开 vs 分组）。
3. 减法实验：`a - b = a + ~b + 1`，在 cla4 上加 cin=~0 与 b 取反验证 L03 §1.2 结论。
4. 把 full_adder 换成 L02 学的两级与非门实现，验证"一切皆 NAND"（P&P Ch.2）。
