#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ch3_congestion —— 《自顶向下方法》§3.6 配套：AIMD / TCP Reno 拥塞窗口演化模拟（纯文本绘图）。

知识点对照（公式全部来自教材 §3.6 与笔记第 12 讲）：
  * 慢启动:  cwnd *= 2 / RTT，直到 ssthresh 或丢包
  * 拥塞避免: cwnd += 1 / RTT（线性）
  * 丢包(3 dupACK 假设): ssthresh = cwnd/2; cwnd = ssthresh      （快恢复，Reno）
  * 超时:     ssthresh = cwnd/2; cwnd = 1                          （回慢启动）
  * 纯 AIMD：加性增 + 乘性减（β=0.5），无慢启动——展示"锯齿"与公平收敛
模型（教学简化）：以 RTT 为时间步；瓶颈容量 K 包/RTT；drop = max(0, Σcwnd − K)
（= 尾丢弃队列溢出），按各流份额分摊；单流丢包→快恢复，整窗丢光→超时。
仅用标准库：random, math。
"""

import random


def render(series, width=64, height=18, label="cwnd"):
    """纯文本位图：横轴 RTT，纵轴窗口。"""
    if not series:
        return ""
    vmax = max(series) or 1
    n = len(series)
    grid = [[" "] * width for _ in range(height)]
    for i, v in enumerate(series):
        col = int(i * (width - 1) / max(1, n - 1))
        row = height - 1 - int((v / vmax) * (height - 1))
        grid[row][col] = "*"
    lines = []
    for r, rowch in enumerate(grid):
        scale = vmax * (height - r) / height
        lines.append("{:>6.0f} |{}".format(scale, "".join(rowch)))
    lines.append("       +" + "-" * width)
    lines.append("        0" + " " * (width - 12) + "t={} RTT".format(n))
    return "\n".join(lines)


class Bottleneck:
    def __init__(self, K=40):
        self.K = K  # 包/RTT


def sim_aimd(flows, K=40, t=200, beta=0.5, seed=1):
    """纯 AIMD：每 RTT 各流 +1；只要本 RTT 有丢包，本流 ×(1-beta)。"""
    random.seed(seed)
    w = [1.0 for _ in flows]
    hist = []
    for _ in range(t):
        total = sum(w)
        drop = max(0.0, total - K)
        for i in range(len(w)):
            share = drop * (w[i] / total) if total else 0.0
            if share > 0:                       # 本流遇到丢包事件
                w[i] = max(1.0, w[i] * (1 - beta))
            else:
                w[i] += 1.0
        hist.append(sum(w))
    return hist


def sim_reno(K=40, t=200, p_timeout=0.03, seed=1):
    """单流 Reno（含慢启动/快恢复/超时三分支）+ 文本绘图。"""
    random.seed(seed)
    cwnd, ssthresh = 1, 16
    hist = []
    events = []
    for rt in range(t):
        sent = cwnd
        drop = max(0, sent - K)                 # 尾丢弃
        if drop and random.random() < p_timeout:
            # 极端：本窗几乎全丢 -> RTO 超时
            ssthresh = max(2, cwnd // 2)
            cwnd = 1
            events.append((rt, "TIMEOUT"))
        elif drop:
            # 视为 3 dupACK 快恢复（教学简化：直接取 ssthresh，省略 +3 爬行段）
            ssthresh = max(2, cwnd // 2)
            cwnd = ssthresh
            events.append((rt, "fast-recover"))
        elif cwnd < ssthresh:
            cwnd *= 2
        else:
            cwnd += 1
        hist.append(cwnd)
    return hist, events


def sim_reno_fair(K=40, t=300, seed=2):
    """双流共享瓶颈：观察 AIMD 公平收敛（RTT 相同情形）。"""
    random.seed(seed)
    c = [1, 1]
    ss = [16, 16]
    hist = []
    for rt in range(t):
        total = sum(c)
        drop = max(0, total - K)
        for i in range(2):
            if drop and (c[i] / total) * drop >= 0.5:   # 该流"有足够份额被丢"
                ss[i] = max(2, c[i] // 2)
                c[i] = ss[i]
            elif c[i] < ss[i]:
                c[i] = min(ss[i], c[i] * 2)
            else:
                c[i] += 1
        hist.append(c[0])
    return hist, c


def main():
    print("=" * 70)
    print("场景 1：单流 TCP Reno（K=40 包/RTT 尾丢弃瓶颈）")
    print("  慢启动指数爬升 -> 越过 K 丢包 -> 快恢复减半 -> AIMD 锯齿")
    hist, events = sim_reno(K=40, t=200, seed=1)
    print(render(hist, label="reno"))
    print("  丢包事件（前 10 个）:", [(e[0], e[1]) for e in events[:10]])
    avg = sum(hist[-80:]) / 80
    print("  稳态平均窗口 ≈ {:.1f} 包（理论：峰 {:.0f} 均 3/4 峰 ≈ {:.1f}）".format(
        avg, 40, 40 * 0.75))

    print("=" * 70)
    print("场景 2：纯 AIMD（无慢启动，β=0.5）双流共享 K=40")
    hist, final = sim_reno_fair(K=40, t=300, seed=2)
    print(render(hist, label="flowA"))
    print("  双流稳态: A={:.1f}, B={:.1f} -> 比值 {:.2f}（公平收敛≈1.0）".format(
        final[0], final[1], final[0] / final[1]))

    print("=" * 70)
    print("场景 3：单流 AIMD 聚合窗口 vs 容量")
    hist = sim_aimd([0], K=40, t=150, seed=3)
    print(render(hist, label="aimd-total"))
    print("\n读图：")
    print("  * 场景1 的'陡坡'=慢启动（指数），'锯齿'=拥塞避免+快恢复。")
    print("  * 把 p_timeout 调大 -> 频繁回 1 -> 吞吐大跌（超时是比快恢复贵得多的信号）。")
    print("  * 场景2 两流同 RTT：收敛到 K/2；若 B 流 RTT 翻倍（自行修改），A 占优——")
    print("    这正是第 12 讲 RTT 不公平性与 LEDBAT/主动信号动机的仿真版。")


if __name__ == "__main__":
    main()
