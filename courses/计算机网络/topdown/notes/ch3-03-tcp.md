# 第 11 讲 · TCP：报文结构、RTT 估计、流量控制与连接管理

> 章节：Chapter 3 §3.5
> 中文对照：topdown_ustc 第 3 章（TCP）

## 1. 核心概念

- **TCP 服务模型**：点对点、可靠、按序字节流、全双工、**面向连接**（握手→传输→挥手）；不建模消息边界、不保证时延/带宽。
- **报文段结构（字段必背）**：`源/目的端口(16×2) | 序号(32) | 确认号(32) | 数据偏移(4)+保留+标志(URG/ACK/PSH/RST/SYN/FIN) | 窗口(16) | 校验和(16) | 紧急指针(16) | 选项`。
  - 选项：MSS（仅 SYN）、SACK-permitted + SACK 块、时间戳（RTTM，用于精确 RTT 与 PAWS）、窗口缩放（WS，突破 64KB 窗，RFC 7323）。
  - 序号/确认号以**字节**为单位——与第 10 讲包序号 ARQ 的本质差别（流而非报文）。
- **RTT 估计（Jacobson/Karels，公式要默写）**：
  - `SampleRTT` 取自未重传报文；`EstimatedRTT = (1−γ)·Est + γ·Sample`，γ≈0.125（指数加权）
  - `DevRTT = (1−β)·Dev + β·|Sample−Est|`，β≈0.25
  - `TimeoutInterval = EstRTT + 4·DevRTT`（Karn 修正：重传包样本不计入）。
- **流量控制（receiver-driven）**：`LastByteSent − LastByteAcked ≤ RcvWindow`；窗口 0 ⇒ 发送方**坚持探测（persist/probing）**；TCP 用延迟 ACK（每 2 段确认一次，Linux 默认 40ms 上限）平衡开销。
- **连接管理状态机（默画）**：
  - 三次握手：SYN(seq=x) → SYN+ACK(seq=y, ack=x+1) → ACK(ack=y+1)；半连接/全连接队列对应第 7 讲 backlog。
  - SYN 洪水防御：SYN Cookie；TIME_WAIT 持续 2MSL（确保最后 ACK 重传+旧分组消亡），高并发服务器需 `tcp_tw_reuse`/连接池权衡。
  - 同时打开/关闭、RST 异常路径、FIN 的"再见但不保证 ACK 送达"语义。

## 2. 传输与恢复要点（为第 12 讲铺垫）

- 重传超时（RTO）触发慢启动；**快重传**：3 个 dupACK 即重传丢失段（不等 RTO），前提是乱序不会误触发（Linux `tcp_reordering` 自适应）。
- 慢启动：cwnd 每 ACK **+1 MSS（指数）**，阈值 ssthresh；拥塞避免：每 RTT **+1 MSS（线性）**——AIMD 锯齿。
- RTO 低估的代价（假重传→假快重传）是"重传定时器是 TCP 最难部分"的出处。

## 3. 层次间与前后讲联系

- 第 10 讲概念→本讲工程实现对照表：GBN≈TCP 累积确认+全重传、SR≈SACK 块、超时→Karels。
- 流控 vs 拥塞控制（必考辨析）：RcvWindow 保护**接收端**，cwnd 保护**网络**；发送窗 `min(rwnd, cwnd)`。
- 第 7 讲 socket 的每个系统调用背后都是本讲状态机；第 14-15 讲 IP 的 MTU/分片决定 MSS 协商（第 5 讲 keep-alive 对应第 2MSL）。

## 4. 跨课程联系

- **CSAPP**：CSAPP 把 TCP 当黑盒，可靠流是其"IO 抽象"成立的根基；tiny 服务器处理 close 时的半关闭就是 FIN/ACK 语义。
- **6.S081/CS162**：xv6 无 TCP，CS162 讲 Linux TCP 在 `tcp_sock` 中的状态与定时器软中断执行；`ss -ti` 输出字段（rto, retrans, rcv_space）与本讲一一对应。
- **CS144**：其 whole course = 本讲实现化——reassembler（序号空间）、sender/receiver（窗口）、`tcp_conn` 状态机、定时器；lab 标题与本讲几乎逐节对应。
- **MIT6.824**：RPC 超时 vs TCP 超时双层计时器的冲突（重传导致"连接还活着但请求卡死"）在读 `time.After` 策略时体会最深。
- **topdown_ustc**：中文板书的状态机图（尤其同时关闭）与官网一致；推荐对照。

## 5. 开源项目应用

- **Linux 内核 TCP**：`include/linux/tcp.h`、`tcp_input.c`（`tcp_rcv_state_process`）、`tcp_output.c`；`/proc/net/tcp`、`ss` 全套观察。
- **Nginx**：`proxy_next_upstream`、超时参数全是本讲的用户可调面；`tcp_nodelay` 默认开启与 Nagle 的取舍。
- **Wireshark**：官方 TCP lab——看三次握手、dupACK、zero window、window update 流。
- **quiche/Envoy**：Envoy 的 `tcp_keepalive`、连接池 drain 直接映射 TIME_WAIT/优雅关闭运维问题。
- **FreeBSD/dpdk-tcp**：历史悠久的 RFC 793 教学实现（`netinet/tcp_var.h`），读代码门槛低于 Linux。

## 6. 延伸阅读

- RFC 793（原始定义，注意已勘误）、RFC 5681（拥塞控制基准）、RFC 6298（**RTT 与 RTO 计算规范**，本讲公式的规范版）、RFC 7323（TCP 选项：WS/TCP 时间戳）、RFC 4987（SYN 洪水）、RFC 8894（PRR 混合丢包恢复）
- 《TCP: Design and Implementation》(Stevens) 第 4/7/10/16/21 章（可选进阶）

## 7. 自查问题

1. 为什么 TCP 序号是字节流编号？给"SYN/FIN 各占 1 序号"带来的 ACK 算术题。
2. rwnd=0 后连接靠什么复活？坚持窗口何时退避？
3. 3 dupACK 规则在 SACK 时代还需不需要？（SACK 块可精确指出空洞）
4. TIME_WAIT 为什么在主动关闭方？服务器大量 499/短连接如何减少其影响？
5. 用 Karels 公式手算：Est=200ms、Dev=40ms、新样本 260ms → 新 Est/Dev/RTO。

## 8. 本讲一句话

TCP = 一个由定时器驱动、在序号空间上滑动两个窗口（rwnd/cwnd）的状态机——所有"玄学调参"都能回到本讲公式解释。
