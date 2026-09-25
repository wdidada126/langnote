# ch4_router_sim —— 最长前缀匹配 FIB + Dijkstra + 距离向量（含计数到无穷）

## 对应章节

- 教材：§4.3（数据平面：LPM）、§5.1（链路状态/Dijkstra、距离向量/Bellman-Ford）
- 笔记：`notes/ch4-02-ip-datagram-lpm.md`（第 14 讲）、`notes/ch5-01-link-state.md`（第 16 讲）、`notes/ch5-02-distance-vector.md`（第 17 讲）

## 要点

1. **FIB 二进制 trie**：逐比特下行、记录最后一次非空下一跳 ⇒ 天然最长前缀优先；
   `0.0.0.0/0` 即根节点默认路由。与 Linux `ip route`、DPDK lpm 库同一语义。
2. **Dijkstra**：二叉堆实现 `O(E+V logV)`；对每个源各跑一次得全源 FIB 下一跳表；
   六节点拓扑取自教材 Fig.5.3。
3. **DV 异步迭代**：每轮各节点用邻居向量做一次性松弛；**断链只作废"经由被断邻居"的路由**，
   陈旧估计保留 ⇒ x 与 y 互为备胎、距离逐轮 +2 爬升 = 计数到无穷。
4. **毒性逆转**：`vector_to(peer)` 把"我经由 peer 到达"的目的对 peer 宣告 inf，
   同样断链快速走 x-w-z-y——两个场景连续跑，输出直接对比。

## 运行

```
python router_sim.py     # 或 ./run.sh（py_compile 自检）
```

## 实验建议

- 给 FIB 加 `/26` 表项验证优先级；再实现"按前缀展开成精确匹配"的第二种转发引擎（教材硬件讨论）。
- DV 场景加水平分割（不向 next-hop 方向通告该前缀），对比收敛轮数。
- 用本脚本输出核对笔记第 16/17 讲自查题的手算结果。
