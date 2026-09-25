# CS144 讲义骨架笔记（notes/outline.md）

> 骨架级要点，待听课+读框架代码后展开。

## L01 课程导论
- 互联网两台「主机」之间的一切：从应用到比特；课程目标是亲手重建 TCP/IP 栈。
- Datagram（无连接、独立路由）vs Virtual Circuit；封装与解封装。
- 复用/解复用：端口、协议号如何让一条链路服务多个连接。

## L02 物理链路
- 带宽×时延积=「管子里的比特数」；吞吐受瓶颈链路限制。
- 编码把比特变信号：曼彻斯特/4B5B/PAM；Shannon 极限给出噪声下上限。
- 串行化时延 vs 传播时延：`L/B` 与 `d/v` 两项分别属于谁。

## L03 以太网
- 帧格式：前导/preamble、MAC 头、类型、FCS（CRC）；MAC 地址是链路层身份。
- 从总线共享到星型交换：全双工消灭碰撞域。
- CRC 的错误检测概率与不可纠错性。

## L04 Wi-Fi
- 无线信道不可全双工监听 → CSMA/CA + ACK 而非 CSMA/CD。
- 隐终端问题与 RTS/CTS；分片。
- BSS/ESS、AP 与桥接到有线网。

## L05 交换
- 学习型交换机：自学习转发表 + 未知目的地泛洪。
- 环路灾难：广播风暴与表震荡；生成树协议（STP）破环。
- 交换机即「多端口、硬件转发的桥」。

## L06 网络服务与 IP
- IP 的极简承诺：尽力而为、可丢失、可乱序、可重复——可靠性被推到端点。
- 32 位地址 = 前缀 + 主机号；子网、CIDR 聚合。
- 转发 vs 路由：per-hop 查表 vs end-to-end 算路。

## L07 IP 路由
- DV 与 LS 两大算法族在 Internet 的落地：RIP/OSPF/BGP。
- BGP 是策略协议：AS 路径与商业关系优先于最短。
- 最长前缀匹配转发的硬件视角。

## L08 ICMP、DHCP、NAT
- ICMP：差错报文与 echo（ping/traceroute 的原料）。
- DHCP：即插即用的地址分发（DORA 流程）。
- NAT：地址短缺的补丁及其对端到端的破坏；NAT 穿透。

## L09 ARP 与转发实战（对接 CP5）
- ARP 把下一跳 IP 解析成 MAC：注意「下一跳」而非「目的 IP」。
- NetworkInterface 抽象：抹平 IP datagram 与 Ethernet frame 的沟。
- 子网判断：`(dst & mask) == (me & mask)` 决定直连还是走默认网关。

## L10 可靠传输协议理论
- 信道不可靠 → 校验和 + 重传；ARQ 家族：停等、GBN、选择重传。
- 序号必须回绕有限（mod 2^32），窗口设计避免旧包歧义。
- 流水线的吞吐 = min(发送窗口/RTT, 链路带宽)。

## L11 TCP 概览
- TCP = 面向连接的可靠字节流：序号按字节而非按报文段。
- 三次握手交换 ISN 与窗口选项；SYN 队列与 SYN flood。
- 框架代码里 connect/accept 被封装——「三次握手去哪了」是精读重点。

## L12 TCP 机制（对接 CP1–3）
- Receiver 端：重组/去重/丢弃乱序、输出流下界（contiguous bytes）。
- Sender 端：重传定时器（指数退避）、拥塞窗口与接收窗口取 min。
- StreamReassembler：内存上限 = 接收窗口，超界必须拒收。

## L13 TCP 拥塞控制总览
- 丢包≈拥塞信号：慢启动指数增长 → 阈值后 AIMD 线性。
- TCP Tahoe/Reno：快重传引入后恢复路径不同。
- 公平性与「抖动收敛到均分带宽」。

## L14 TCP 拥塞控制细节
- CUBIC：窗口按三次曲线爬升，高 BDP 下比 Reno 更激进。
- delay-based（Vegas）与 loss-based 的取舍；bufferbloat 的成因。
- 与 AQM（RED/CoDel/fq_codel）的联动设计。

## L15 真实网络中的 TCP（对接 CP4）
- 用自实现 TCP 跑 webget 与工业实现互操作：几乎标准兼容的验收测试。
- RTT ≥100ms 的真实流量模式：抓取数据→Python 可视化→验证窗口/重传行为。
- TCPSender/TCPReceiver 如何被 TCPMinnowSocket 拼装成双向可靠字节流。

## L16 数据中心网络
- 服务器自己就是路由器：Clos/胖树 + ECMP。
- PFC/DCQCN/RDMA：无损以太与拥塞信令；why TCP 在 DC 里时延不够低。
- 遥测与负载均衡（Flowlet/PLB 思路）。

## L17 中间盒
- 防火墙、LB、NAT 都在「擅自改写」协议语义。
- 中间盒与端到端论据的张力；QUIC 加密头部的动机之一。

## L18 内容分发与流媒体
- CDN：DNS 重定向 + 边缘缓存；热点与 origin 保护。
- 视频自适应码率（DASH）与缓冲对拥塞控制的反馈。

## L19 安全（TLS 概览）
- 对称/非对称/混合：握手协商密钥；证书链建立身份。
- 前向保密；TLS 记录层与 TCP 字节流的关系。

## L20 测量与前沿
- 主动测量（traceroute/ping 网格）与被动测量（NetFlow/sFlow）。
- Keith Winstein 的 measurement 视角：先量化再设计。
- 结课串讲：CP7 把全栈在内存 network_thread 中互联，端到端通信闭环。
