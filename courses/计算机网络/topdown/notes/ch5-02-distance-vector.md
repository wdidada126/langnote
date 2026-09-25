# 第 17 讲 · 距离向量路由：Bellman-Ford、毒性逆转与计数到无穷

> 章节：Chapter 5 §5.1（距离向量部分）
> 中文对照：topdown_ustc 第 5 章（距离向量）；配套项目 projects/ch4_router_sim（DV 含计数到无穷演示）

## 1. 核心概念

- **DV 方程（Bellman-Ford 分布式版，默写）**：
  `Dx(y) = min over neighbors v { c(x,v) + Dx_v(y) }`——我对 y 的估计 = 各邻居"报给我的距离"+直连代价取最小；记录最优邻居为 next hop。
- **异步迭代交换**：邻居间周期/触发交换整张向量表；好消息立刻传播（降距离），坏消息**只能逐渐爬升**——计数到无穷（count-to-infinity）的根源。
- **计数到无穷演示**（经典 3 节点 A–B–C，代价 1/1/1000）：链路断开后 A、B 互相把对方当备胎，距离以每秒 +2 节奏爬到 ∞。实验见 projects/ch4_router_sim 的 dv_count_to_infinity()。
- **缓解机制谱系**：
  - 定义无穷上限（RIP 的 15 跳/16 不可达）——把爬升封顶。
  - **毒性逆转（poison reverse）**：B 经 A 到 X ⇒ B 向 A 报 ∞。
  - **水平分割（split horizon）**：不向"该前缀的下一跳"通告该前缀。
  - **路径向量（path vector）**：BGP 把 AS 序列捎带上报，收到含自身 AS 的通告即丢弃——环消灭于源头（第 18 讲）。
  - **触发更新+hold-down/慢重启（GR/NSR）**：减少误学与重启风暴。
- **DV 度量的自由度**：任意"无负环"度量皆可（跳数、时延、延迟×带宽），但必须满足最优子结构，否则协议不收敛——对比 LS 对边权独立性的要求（第 16 讲表）。

## 2. RIP 关键事实（DV 的代表协议）

- v1（RFC 1058）有类别/广播；v2（RFC 2453）无类别/组播 224.0.0.9+简单认证；计时器：update 30s、invalid 180s、flush 270s。
- 15 跳=实用上限 ⇒ 只能做小域内部网关（今天基本被 OSPF 替代，但 IoT/低功耗仍有 RIP 变体，如 RPL，RFC 6550）。

## 3. 层次间与前后讲联系

- DV 报文本身走 UDP 520（第 9 讲分用/第 7 讲 socket）——"路由协议是应用"的实感案例。
- 收敛期间的 FIB 不一致 ⇒ 临时环/黑洞（第 13 讲转发视角）；DV 的分布式 DP 与第 16 讲 LS 的全局计算构成算法课对偶。
- SDN 集中式（第 19 讲）本质是把 DV/LS 的"协商"换成"控制器单点计算+下发"。

## 4. 跨课程联系

- **6.006**：Bellman-Ford 集中式算法（V−1 轮松弛）与协议版逐行对照；负权边为何禁止——协议即"无中心负环检测器"。
- **MIT6.824**：DV 的"最终一致但可能环"是讲一致性/收敛反例的最佳材料；6.824 作业里"坏消息传播慢"与 Raft 的 term 单调（防旧信息复活）同一思想族。
- **CS144/CS162**：CS162 用 DV 讲"分布式系统中本地最优≠全局最优"；CS144 不涉及（数据平面）。
- **topdown_ustc**：郑烇老师 3 节点爬升表格逐轮板书，考试原题风格。

## 5. 开源项目应用

- **FRR**：`ripd` 源码极短（向量表+计时器），是本讲最佳可读实现；`zebra` 负责 RIB→FIB 下装（第 13 讲）。
- **Quagga 前身/inetd 时代 gated**：历史脉络；Linux `ip route`+`bird` 也有 RIP 插件。
- **Contiki-NG / RPL（6TiSCH）**：无线传感器网的 DV 后裔（DAG 树代替表交换），现代工业场景。
- **Containerlab**：两路由器 RIP 邻居 + `tc netem` 断链观察计数到无穷；`tcpdump udp port 520`。
- **Wireshark**：官方 RIP lab。

## 6. 延伸阅读

- RFC 1058/2453（RIP v1/v2）、RFC 6209（RIPng IPv6）、RFC 6550（RPL）、RFC 4760（BGP Multiprotocol 的路径向量前身）
- McQuillan, Richer, Rosen《The New Routing Algorithms for the ARPANET》(1980) 与《Improving the Availability of Routing Algorithms》(1980)——计数到无穷的原始解法论文（papers.md 经典表）
- 官网 §5.1 DV 动画 + 习题"8 字拓扑代价表"

## 7. 自查问题

1. 手算图示网络各节点 D 向量收敛过程（与项目 ch4 输出对比）。
2. 毒性逆转在 A→X 与 B→X 都可用时会不会把"好路"封掉？双工毒性逆转的代价？
3. RIP 的 30s 周期在大型网络会制造多少背景流量？触发更新解决什么、引入什么风险？
4. 为什么 BGP 的路径向量的"含己则弃"对 AS 级环是充分条件，而 DV 的跳数上限只是缓解？
5. RPL 的 rank/DAG 如何把 DV 思想移植到"多父可省"的无线场景？

## 8. 本讲一句话

距离向量把最优子结构换成分布式简单性，坏消息传播的病（计数到无穷）用一圈补丁（上限/逆转/分割/路径向量）治了四十年，最后被 BGP 与 SDN 分别以"路径"和"集中"根治。
