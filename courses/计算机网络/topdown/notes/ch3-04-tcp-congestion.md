# 第 12 讲 · TCP 拥塞控制：Tahoe/Reno/Cubic、公平性与 QUIC/TLS 演进

> 章节：Chapter 3 §3.6–§3.7
> 中文对照：topdown_ustc 第 3 章（拥塞控制与 TCP 演进）；配套项目 projects/ch3_congestion

## 1. 核心概念

- **拥塞崩溃历史**：1986-88 ARPANET 三次全网吞吐崩塌（Van Jacobson 急救），确立"端到端拥塞控制 + 网络只丢包给信号"的因特网路线——与第 2 讲排队/尾丢弃合起来就是拥塞问题的完整因果链。
- **拥塞窗演化（核心公式，必须默写）**：
  - 慢启动：`cwnd = 1 MSS`，每收 1 ACK ⇒ `cwnd += 1 MSS`（每 RTT **翻倍**），直到 ssthresh 或丢包。
  - 拥塞避免：`cwnd += MSS·MSS/cwnd` 每 ACK（每 RTT +1 MSS，**线性**）。
  - 超时（RTO）：`ssthresh = cwnd/2; cwnd = 1`，回慢启动（**乘性减**）。
  - 3 dupACK（Reno 快恢复）：`ssthresh = cwnd/3/2 或 cwnd/2（版本差异）；cwnd = ssthresh + 3`，收一个 dupACK **+1**（拥塞窗口"爬行"），收到新 ACK 回到 ssthresh。
- **Tahoe vs Reno vs NewReno vs SACK**：
  - Tahoe：任何丢包都回慢启动。
  - Reno：快恢复只处理**单段**丢失；RTT 内多丢则误判。
  - NewReno：一个 RTT 内未全恢复前，部分 ACK 只加 1，恢复完才退出快恢复（RFC 6582）。
  - SACK：用 SACK 块精确算空洞，一次恢复多丢多段（RFC 3517→已更新为 RFC 2018 线）。
- **AIMD 公平性**：加性增 β_增=1、乘性减 β_减=1/2 ⇒ 收敛到等带宽份额；**窗口 RTT² 反比问题**（`W ∝ 1/RTT` 而非 1/RTT²）→ 同瓶颈短 RTT 流占优；Low Priority TCP 实验（RFC 3511/6817 线）与 LEDBAT 用于后台流量。
- **CUBIC（Linux 默认）**：`W(t) = C(t−K)³ + Wmax`，`K = (Wmax·β/C)^(1/3)`——基于时间的三次曲线，高 BDP 网络下比 Reno 更稳、与 RTT 解耦（公平性靠"同一目标速率"近似）；BBR 则"测带宽+RTT 建模"，不靠丢包信号（争议：与丢包基协议共存公平性）。
- **§3.7 活动与演进**：TCP 在内核难改（middlebox 干扰、实现惯性）→ QUIC 用户态化：0-RTT 建连、每流独立恢复、连接迁移（第 23 讲移动性）。TLS1.3（第 24 讲）把握手压缩到 1-RTT、密钥轮换。

## 2. 关键场景/图示

- 拥塞周期锯齿：W 峰谷比 β=0.5 ⇒ `RTT 数 ≈ log2(W)`、吞吐均值 `≈ 3/4 Wmax`（教材公式）。
- "bufferbloat vs 小缓冲"：AQM（CoDel/DCQCN）目标=低队列+高利用（呼应第 2 讲；数据中心 RDMA 用 DCQCN/PFC，见 papers.md）。

## 3. 层次间与前后讲联系

- 需要第 11 讲的 RTO/dupACK 作信号源；丢包信号本身来自第 2 讲路由器尾丢弃。
- 第 8 讲 DASH 码率跟随 = cwnd 的应用层镜像；第 14 讲 IP 层的 ECN/RED 是"显式信号"路线（与 TCP 隐式探测对接）。
- 第 7 讲 socket：`SO_SNDBUF`、`TCP_CONGESTION=cubic/bbr` 是本讲调参入口。

## 4. 跨课程联系

- **CS144**：其 congestion control 章节（lab5/6，BIC/CUBIC/FAST/DCTCP 实现）与本讲几乎同构——**强烈建议同周对照**，本讲公式在其测试器里可视化。
- **MIT6.824/CS162**：数据中心 TCP（Homa/NDP/pFabric）是论文级话题；CS162 用本讲解释"为什么云里需要可编程拥塞控制"。
- **CSAPP**：无直接对应，但 `setsockopt` 切换拥塞算法是 CSAPP 风格的 API 实践。
- **topdown_ustc**：郑烇老师的 Reno 锯齿板书与官网动画一致。

## 5. 开源项目应用

- **Linux 内核**：`net/ipv4/tcp_cubic.c`（K 值与 HyStart 探测慢启动退出）、`tcp_bbr.c`（pacing_rate/bandwidth filter）、插件化 `inet_connection_sock`。
- **quiche**：内置 Reno/CUBIC/BBR 可换（用户态拥塞控制自由度的展示）。
- **Wireshark**：`tcp.stream`+IoGraph 绘制吞吐锯齿；实验：`tc netem loss 1%` 观察 cwnd（ip ss 输出）。
- **Nginx/Envoy**：连接池与重试风暴治理本质是"应用层拥塞观"（指数退避+jitter，AWS 架构指南）。

## 6. 延伸阅读

- RFC 5681（TCP 拥塞控制基准）、RFC 6582（NewReno）、RFC 3517（SACK）、RFC 8312（CUBIC）、RFC 7661（Reno 公平性考量）、RFC 9469（BBRv1 规范版）、RFC 7567（AQM 分类）、RFC 9002（QUIC 自有拥塞控制框架）
- Jacobson《Congestion Avoidance and Control》SIGCOMM'88（papers.md 头条）
- 官网 §3.6 全套动画 + "TCP 拥塞窗口"交互演示

## 7. 自查问题

1. 同一瓶颈两流 RTT=10/20ms，Reno 稳态吞吐比多少？改成 1/RTT² 目标需要什么（ hinted: LEDBAT/主动信号）？
2. cwnd=24、丢 1 段→Reno 快恢复后每 dupACK/每新 ACK 的窗口轨迹？
3. 为什么快恢复的 dupACK 阈值是 3（重排序容限与丢包检测时延的折中）？
4. BBR 不依赖丢包，为什么与 CUBIC 共存时可能"饿死后者"？（队列不建满→丢包基看不到竞争）
5. QUIC 把 CC 搬进用户态带来什么运维问题（内核可观测性丧失）？

## 8. 本讲一句话

因特网用"端到端猜丢包"的方式绕开了全网拥塞协调这个不可能任务；BBR/QUIC/AQM 正在把"猜"升级为"测"与"协商"。
