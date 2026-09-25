# CS61C 配套项目计划（projects/README.md）

> 对齐官方 4 Project + 周 Lab 结构，本地化重写为可独立编译的小项目。本轮只列计划不写代码。

| 章节 | 建议语言 | 小项目 | 编译方式 |
| --- | --- | --- | --- |
| L1–L9 汇编与 C | C + RISC-V 汇编 | life：Game of Life（官方 P1 主题）；附加 bomb-lite：给 5 段反汇编手写通过字符串 | `gcc -Wall -Wextra -O1`；汇编用 `riscv64-unknown-elf-gcc -march=rv64im -c` + spike 运行 |
| L4–L9 汇编深入 | RISC-V 汇编 | mnist-asm：查表式单隐层网络推理（官方 P2 主题），纯汇编写矩阵乘+ReLU | `riscv64-unknown-elf-gcc -T link.ld`，MARS/QtSpim 或 spike 运行 |
| L2–L3/L14–L16 电路与 CPU | Logisim (Logisim-Evolution) | pipe-cpu：两级流水线 RISC-V 子集 CPU（官方 P3 主题），跑自检程序 | 无需编译；.circ 文件 + 官方测试脚本 `python3 test.py` |
| L10/L18 并行 | C + OpenMP/SIMD | mininumpy：矩阵乘/逐元素运算并行优化（官方 P4 主题），记录加速比 | `gcc -O3 -fopenmp -mavx2 -mfma`，基准 `./bench` |
| L12–L13 存储层次 | C | cache-sim：组相联缓存模拟器，输出缺失率；用两种矩阵遍历对比局部性 | `gcc -O2`，`./cache_sim 64 8 2` |
| L11/L17 性能与并发 | C + pthread | thread-matrix：手写锁保护并行累加 vs 无锁分块，测 Amdahl 实际上限 | `gcc -O2 -pthread` |
