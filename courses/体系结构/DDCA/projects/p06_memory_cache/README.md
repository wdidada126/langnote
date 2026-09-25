# p06 存储与缓存：2 路组相联 cache（Verilog）+ 映射策略模拟器（C）

## 对应讲次
- notes/L07.md §1.1–1.2（SRAM 阵列、译码+Mux 的存储结构）
- notes/L13.md §1.2 地址划分 / §1.3 LRU 与冲突缺失 / §1.4 写直达+写分配 / §1.5 命中率→AMAT
- notes/L14.md 可再叠加 TLB（延伸实验 4）

## 文件说明
| 文件 | 内容 |
| --- | --- |
| `cache.v` | 256B/4组/2路/块2字 cache 行为模型：tag 并行比较→命中 Mux、缺失整行填充、LRU victim 位、写直达+写分配、hit/miss 计数器 |
| `tb_p06.v` | 三段剧情：set0 上的 LRU 逐出序列（M M H H M H M）、不同 set 无冲突证明、写后回读+主存更新证据，全部自动判定 |
| `cache_sim.c` | C 辅助模拟器：直接映射/2路/4路 × 顺序/大步长/随机 trace 的命中率矩阵，亲手复现"步长=组数×块长→颠簸" |

## 编译与运行（需安装 iverilog；C 部分需 gcc）
```sh
cd p06_memory_cache
./build.sh          # 或 build.bat
iverilog -g2005 -o sim.vvp tb_p06.v cache.v && vvp sim.vvp   # 期望：P06: ALL TESTS PASSED
gcc -O2 -o cache_sim cache_sim.c && ./cache_sim
```

## 知识点观察点
1. `ways=1` 重编译（tb 里改参数）→ 同一冲突序列命中率暴跌 ⇒ 相联度=冲突预算（L13 §1.2）。
2. `backing[w]=w*4` 的"可预测主存"让任何读错立刻现形——验证方法学：数据要有签名。
3. 写直达 + 写分配的组合下 `hit_cnt/miss_cnt` 的期望值如何推导（考试题源）。
4. LRU 用 1 bit/组：2 路专属技巧；4 路需要树形 pseudo-LRU（ChampSim 里看真实现）。

## 延伸实验
1. 把 `cache.v` 的 WAYS 改 1（generate 已参数化的部分要手工调 victim 逻辑）→ 观察 tb 剧情第 5 步变成 hit。
2. 加"缺失需 3 拍总线等待"的 FSM（valid/ready 握手）→ 接 L10 §1.4 与 L15 §1.2。
3. 用 `cache_sim.c` 复现 CSAPP 6.4 的矩阵转置块大小实验（扩展 trace 生成器为 2D 遍历）。
4. 再套一层"TLB"：把地址先过全相联 8 项 TLB 模型（数组遍历即全相联），算联合命中率（L14 §1.3/1.5）。
