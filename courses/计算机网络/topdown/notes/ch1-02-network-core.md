# 第 2 讲 · 网络核心：电路交换、分组交换、时延与吞吐量

> 章节：Chapter 1 | 对应教材：§1.2、§1.6
> 中文对照：topdown_ustc 第 1 章（网络核心/性能部分）

## 1. 核心概念

- **电路交换**：端到端独占带宽（TDM 时隙/FDM 频带），建立阶段有连接时延，资源利用率低（语音网经典模型）。统计 TDM 的"按需时隙"正是分组交换的雏形。
- **分组交换**：存储转发（store-and-forward）——每跳收到完整分组再转发；链路空闲时共享、超额时排队/丢弃。与电路交换的根本分歧在**突发 admit 与资源预留**（后演化为 DiffServ/IntServ，见 papers.md）。
- **时延四件套**（节点处）：
  - 排队时延 `d_queue`（拥塞核心来源，依赖到达过程）
  - 处理时延 `d_proc`（查表/校验/解析）
  - 传输（序列化）时延 `d_trans = L/R`——**路由器与链路带宽决定**
  - 传播时延 `d_prop = d/s`——**物理距离与介质决定**（光纤约 2×10^8 m/s）
  - `d_node = d_proc + d_queue + d_trans + d_prop`
- **丢包与溢出**：缓冲有限，`Qos` 满则尾丢弃（tail drop）；这正是第 3 章拥塞控制要"在源头收敛"的原因——端到端原则的又一体现。
- **吞吐量**：`throughput = min{us, Rc1..RcN, uc}`；瓶颈链路概念贯穿 CDN（第 2 章）与 TCP 拥塞窗（第 3 章：cwnd 收敛到 BDP 附近）。
- **BDP（带宽时延积）**：`R × RTT` 比特——"管道里能装多少"，是 socket 缓冲大小、TCP 窗口、快速网络 tuning 的第一性指标（100Mbps×100ms ≈ 1.25MB，远超默认 64KB！）。

## 2. 关键公式/模型

- M/M/1 排队近似（§1.2 重点推导）：平均排队 `≈ (L/R)/(1−L·a/R)`，**利用率 ρ = La/R → 1 时时延指数爆炸**——解释"路由器半夜快、晚高峰卡"。
- 流量强度 `La/R` 必须 < 1，否则队列无界增长。

## 3. 层次间与前后讲联系

- 排队时延 → TCP 超时估计的抖动来源（第 11 讲 RTT 样本噪声）；尾丢弃 → 拥塞信号（第 12 讲）。
- 传播 vs 传输之辩在 CS144 lab 中被"可调延迟的虚拟链路"直接实验化。
- 封装栈视角：本讲讨论的"路由器"在第 4 章拆成数据平面（查表转发），交换机在第 6 章拆成 MAC 自学习。

## 4. 跨课程联系

- **CS144**：lab2 的字节流重组正是"存储转发+排队"的端系统对偶；CS144 课程把 d_trans 称为 serialization delay，可直接对照其 replayer。
- **6.S081/CS162**：内核 `qdisc`（pfifo_fast/ fq_codel）实现了 d_queue；CS162 用"缓冲膨胀（bufferbloat）"批评尾部丢弃路由器——主动讲 AQM 与 CoDel（见延伸阅读）。
- **MIT6.824**：MapReduce 集群调度本质是"在数据中心网络里管理 d_prop 与 throughput"。
- **topdown_ustc**：郑烇老师的"高速公路收费站"类比 d_trans/d_prop 非常精确。

## 5. 开源项目应用

- **Wireshark**：用 IAT（帧间到达时间）统计复现排队时延分布；`tcp.stream` 图看吞吐收敛。
- **Linux**：`tc qdisc add dev eth0 root netem delay 100ms loss 1%` 是所有后续实验（含本项目 ch3 ARQ 思想验证）的标准信道注入工具；fq_codel/AQM 源码在 `net/sched/sch_fq_codel.c`。
- **DPDK/VPP**：为了把 `d_proc+d_trans` 压到极限，用轮询+零拷贝绕过内核排队（第 13 讲详述）。
- **iperf3 / netperf**：实测 throughput 与 one-way delay 的事实标准。

## 6. 延伸阅读

- RFC 5842（Bufferbloat Considerations）
- 《Controlling Queue Delay》(Nichols & Jacobson, ACM Queue 2012 —— CoDel)
- RFC 2544（设备吞吐/时延基准测试方法）
- 官网 §1.2 例题 + Wireshark lab：观察 HTTP 分组往返时间

## 7. 自查问题

1. L=512B、R=1Mbps 与 L=1500B、R=10Mbps 两条链路，d_trans 各是多少？谁排队更严重？
2. 为什么"传播时延与分组长度无关，传输时延与距离无关"？各举一个反直觉例子。
3. M/M/1 式中 ρ=0.9 与 ρ=0.99 的平均排队差多少倍？这对数据中心"70-80% 利用率红线"意味着什么？
4. BDP=10Gbps×1ms 需要多大的 TCP 窗口？默认 64KB 够吗？（引出第 12 讲高带宽网络 TCP 调优）
5. 尾丢弃如何同时伤害吞吐与时延？（bufferbloat：队列满→RTT 膨胀→RTO 误判，见第 11 讲）

## 8. 本讲一句话与下一讲钩子

分组交换用"统计复用+存储转发"换来突发适应与鲁棒性，代价是排队与丢包——所有后续的可靠传输（第 10 讲）与拥塞控制（第 12 讲）都是为这笔代价买单；下一讲把视野拉高：分层与封装如何组织这一切。
