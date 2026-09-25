# ETH CA 配套项目计划（projects/README.md）

> 课程 5 个 Project 主线：Verilog RT 流水线 + C 周期精确模拟器 + 内存/Cache 专题。本轮只列计划不写代码。

| 章节 | 建议语言 | 小项目 | 编译方式 |
| --- | --- | --- | --- |
| L2/L11–L14 模拟基础 | C++ | sim-core：周期精确顺序核模拟器骨架（取指/流水/Cache 接口） | `g++ -std=c++17 -O2`，CMake `cmake -B build && cmake --build build` |
| L2 流水线 RT | Verilog | pipe-rt：两级 MIPS RT 流水线 + testbench 自检 | Vivado/iverilog `iverilog -g2012 *.v` + `vvp` |
| L3–L5 DRAM 调度 | C++ | dramsim-mini：行缓冲命中模型 + FR-FCFS/STFM 调度，对比平均/尾延迟 | `g++ -O2 -std=c++17`，脚本 `python3 sweep.py` 出图 |
| L9–L10 PIM | C++/Python | pim-mm：把矩阵向量乘「下沉」到 bank 并行的数据划分与模拟 | `g++ -O2 -march=native`；Python 版 `pip install numpy` |
| L11 Cache 替换 | C++ | cache-repl：LRU/LFU/随机 + trace 回放，缺失率对比（可接入 ChampSim trace） | `g++ -O2 -std=c++17`，`./cache --trace x.trace --size 32K --assoc 8` |
| L17 GPU/并行 | C++ | warp-sim-lite：SIMT 栈模拟小 kernel，观察 warp divergence 影响 | `g++ -O2`；有 GPU 可选 `nvcc -arch=native` |
