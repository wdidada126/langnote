# p11 在线算法（分页竞争 + ski rental）

- 对应讲次：L21（splay/列表更新，竞争分析入门）、L22（分页：LRU/FIFO/Marked/Belady-OPT、随机化）。
- 知识点：竞争比的形式化——同一请求流上在线策略 vs 离线最优的缺页数之比；LRU 是 k-竞争（+加性常数），FIFO 无界（异常上升）；Belady OPT 用 `future.index` 驱逐"下次请求最远"的页。ski rental：确定性"租满 B 天就买"最坏比 2（紧），随机化阈值混合把最坏期望比压向 e/(e−1)≈1.58。
- 文件：`main.py`（LRU/FIFO/Marked/OPT 四策略 + simulate；`ski_worst_ratio`/`ski_tune` 用粗网格数值调优三点混合阈值分布，解析最坏比 + 蒙特卡洛双重复核，不对未实现的连续分布做过度声称）。
- 运行：`run.bat` / `bash run.sh`；手动 `python -m py_compile main.py && python main.py`。
- 预期输出：k=3 经典序列 LRU=10、OPT=7；300 条随机序列上 max LRU/OPT 落在包络内；四类负载×两档容量的缺页表（cyclic(9) 时 LRU=OPT=500，栈式最优）；ski 表显示确定性 2.00 → 调优随机化 ≈1.6–1.8。
- 延伸：L21 splay 的动态最优猜想；实际系统对照 Linux page cache 驱逐、DB 缓冲池（LRU-K/2Q），CDN 缓存命中率模拟；6.824 中在线视角（租约续约 vs 提前续租即 ski rental）。
