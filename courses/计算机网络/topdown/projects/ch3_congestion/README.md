# ch3_congestion —— AIMD / Reno 拥塞窗口演化模拟（纯文本绘图）

## 对应章节

- 教材：§3.6（TCP 拥塞控制：慢启动/拥塞避免/快重传/快恢复、AIMD、公平性）
- 笔记：`notes/ch3-04-tcp-congestion.md`（第 12 讲）；公式对照笔记"关键场景/图示"节

## 模型要点

1. 时间步 = 1 RTT；瓶颈容量 K（包/RTT）；**尾丢弃**：本窗发出 cwnd>K 的部分即丢。
2. Reno 三分支：慢启动 ×2；dupACK 快恢复 `ssthresh=cwnd/2`；超时（按 p_timeout 随机触发）`cwnd=1`。
3. 纯 AIMD：+1 / ×0.5，无慢启动——与 Reno 对照看"起步速度"与"稳态锯齿"。
4. 双流公平性：同 RTT 收敛 1:1；改 RTT 即复现第 12 讲的 RTT² 不公平议题。
5. 稳态平均 ≈ 3/4·峰值（教材公式），程序自动核对。

## 运行

```
python congestion_sim.py     # 或 ./run.sh（py_compile 自检 + 运行三场景）
```

输出为 ASCII 位图（纵轴窗口、横轴 RTT）与统计行。

## 实验建议

- `p_timeout=0.03→0.3`：锯齿变"锯条"（频繁回 1），理解"超时信号远贵于 dupACK"。
- 把快恢复改为 Tahoe 行为（丢包即 cwnd=1）对比（教材习题思路）。
- 延伸：实现 CUBIC `W(t)=C(t-K)³+Wmax`，与 Reno 锯齿并排画——CS144 lab6 的同款作业。
