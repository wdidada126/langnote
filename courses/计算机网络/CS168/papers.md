# CS168 论文与应用清单（papers.md）

## 经典论文

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
| --- | --- | --- | --- |
| End-to-End Arguments in System Design (Saltzer, Reed, Clark) | 1984 | 论证智能功能应置于通信端点而非网络内部，是互联网架构的第一性原理 | L01/L12 |
| A Domain Name System (Mockapetis) | 1987/1988 | 提出层次化、分布式、可缓存的名字解析服务 | L10 |
| Congestion Avoidance and Control (Van Jacobson) | 1988 | 定义慢启动/AIMD/快重传，拯救了 1986 年的 Internet 拥塞崩溃 | L09 |
| RED: Managed Fairness in an Unfair World / Random Early Detection (Floyd & Jacobson) | 1993 | 用主动队列管理在路由器上公平地处理过载与丢包 | L09 |
| A Border Gateway Protocol 4 (Rekhter & Li, RFC 4271) | 2006 | 现行域间路由标准，把策略置于路径选择核心 | L05 |
| OSPF Specification (Moy, RFC 2328) | 1998 | 链路状态域内路由的工业标准 | L04 |
| The Internet Society. RFC 791 IP / RFC 793 TCP (Postel) | 1981 | 定义 IP 数据报与 TCP 字节流语义，分层模型的基石 | L03/L07/L08 |
| DiffServ Architecture (Blake et al., RFC 2475) | 1998 | 用粗粒度等级服务在核心网提供 QoS 的折中方案 | L09/L12 |
| OpenFlow: Enabling Innovation in a White Box Switches (McKeown et al.) | 2008 | 转发与控制分离，开启软件定义网络（SDN）时代 | L05/L13 |
| CUBIC: A New TCP-Friendly High-Speed TCP Variant (Ha, Rhee, Xu) | 2008 | 用三次函数窗口增长适配高带宽时延积网络，Linux 默认 | L09 |
| BBR: Congestion-Based Congestion Control (Cardwell et al.) | 2017 | 以带宽/时延建模替代丢包信号，重开拥塞控制设计空间 | L09 |
| Improved Traceroute / RTT 测量方法（Vixie 等） | 1994–2000s | 基于 TTL 超时的路径探测与主动测量基础 | L01/L03 |

## 近 5 年论文（2021–2026）

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
| --- | --- | --- | --- |
| QUIC: A UDP-Based Multiplexed and Secure Transport (RFC 9000) | 2021 | 在用户态重建可靠传输+加密+多流复用，成为 HTTP/3 底座 | L07/L11 |
| PLB: Congestion Signals Are Simple and Effective for Network Load Balancing (Google) | 2022 | 仅靠 TCP 部署 RTO/FL 等端侧信号即可绕开网络热点 | L09/L13 |
| Canopy: Cost-Efficient Congestion Control in Datacenters via Inband Network Telemetry | 2021 | 用带内网络遥测在商用硬件上实现细粒度拥塞控制 | L09/L13 |
| SDCP: Software Congestion Control with Predictors (Harvard) | 2021 | 网卡旁路+主机侧模型预测实现超低时延传输 | L07/L09 |

## 知识点在开源项目中的应用

| 知识点 | 开源项目 | 说明 |
| --- | --- | --- |
| TCP 拥塞控制算法 | Linux 内核 net/ipv4 (CUBIC/BBR) | `ss -ti` 观测；模块可插拔 |
| 路由协议 (OSPF/BGP) | FRRouting (FRR) | 生产级路由栈，含 BGP 策略引擎 |
| 包捕获与协议解析 | Wireshark / libpcap / Scapy | L02–L03 链路层/网络层实验工具 |
| 内核旁路高性能转发 | DPDK | 用户态轮询转发，L13 数据中心场景 |
| XDP/eBPF | Linux 内核 + libbpf/Cilium | 网卡驱动层处理包，现代 L4/L7 负载均衡底座 |
| QUIC/HTTP3 | quic-go / nginx / Cloudflare | L07/L11 的现代落地 |
| traceroute/DNS | iputils / bind9 / unbound | L03/L10 的工业实现参照 |
