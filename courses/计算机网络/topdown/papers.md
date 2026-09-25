# 计算机网络（topdown）· 论文与规范清单

> 与 notes/ 24 讲对应；RFC/标准按"讲次→出处"组织。年份为公开发表/发布年份；拿不准处标"待核实"。

## 1. 经典论文/规范表（打地基）

| # | 文献 | 年份 | 对应讲次 | 一句话要点 |
| --- | --- | --- | --- | --- |
| 1 | RFC 791 — Internet Protocol | 1981 | 13/14 | IPv4 数据报、分片、逐跳校验和的原始定义 |
| 2 | RFC 793 — Transmission Control Protocol | 1981 | 11 | TCP 状态机与序号/ACK 的原点（细节已被 RFC 9293, 2022 重写澄清） |
| 3 | RFC 768 — UDP | 1980 | 9 | 8 字节首部的"裸传输" |
| 4 | RFC 1034/1035 — Domain Names / Implementation | 1987 | 6 | 分层命名+引路+缓存的分布式数据库范本 |
| 5 | Fielding — Architectural Styles and the Design of Network-based Software Architectures（REST 博士论文） | 2000 | 5 | HTTP 方法与无状态的架构学根基 |
| 6 | Jacobson — Congestion Avoidance and Control (SIGCOMM'88) | 1988 | 2/12 | 拥塞崩溃急救：慢启动/拥塞避免/（随后的）快重传三件套出处 |
| 7 | Saltzer, Reed, Clark — End-to-End Arguments in System Design | 1984 | 3 | 端到端原则原文：功能该放哪层的判定准则 |
| 8 | RFC 896 — Congestion Control in IP/TCP (Nagle) | 1984 | 11 | 小报文自时钟拥塞与 Nagle 算法 |
| 9 | Jacobson — Modified TCP Congestion Avoidance Algorithm（内部备忘录，"fast recovery"） | 1990 | 12 | Reno 快恢复的原始描述（非正式发表） |
| 10 | RFC 6582 — The NewReno Modification to TCP's Fast Recovery | 2000 | 12 | 一个 RTT 内多丢包的"部分 ACK"恢复 |
| 11 | RFC 2018 — TCP Selective Acknowledgment Options (Mathis, Mahdavi, Romanow, Zhu) | 1996 | 10/12 | SACK：把 SR（第 10 讲）搬进 TCP；后由 RFC 3517 更新 |
| 12 | RFC 1122 — Requirements for Internet Hosts (Braden ed.) | 1989 | 1/11 | 端系统 TCP/IP 行为总要求 |
| 13 | RFC 2475 — Architecture for Differentiated Services (Blake et al.) | 1998 | 12/14 | DSCP/PHB：QoS 从"逐流状态"改为"类状态" |
| 14 | RFC 3031 — MPLS Architecture (Rosen, Viswanathan, Callon) | 2001 | 13/14 | 定长标签交换；转发与控制解耦的运营商版 |
| 15 | McKeown, Anderson, et al. — OpenFlow: Enabling Innovation in Campus Networks | 2008 | 19 | SDN 开山宣言：控制面外置+流表抽象 |
| 16 | Perlman — Rethinking the Design of a Local Area Network（学习桥/STP，IEEE Trans. Comm. 时期论文） | 1985–1988 | 21 | 自学习桥与生成树：交换机的两台发动机 |
| 17 | RFC 2002 → RFC 6275 — IP Mobility Support for IPv4/IPv6 (Johnson, Perkins et al.) | 1996/2011 | 23 | CoA/HA/三角路由：移动 IP 的正式表达 |
| 18 | RFC 6550 — RPL: Routing Protocol for LLN | 2012 | 17 | DV 思想在低功耗无线网的当代后裔（DAG） |
| 19 | Al-Fares, Loukissas, Vahdat — A Scalable, Commodity Data Center Network Architecture (Fat-Tree, SIGCOMM'08) | 2008 | 16/21 | 等值成本可扩展交换拓扑与 ECMP 路由 |
| 20 | Greenberg et al. — VL2: A Scalable and Flexible Data Center Network (SIGCOMM'09) | 2009 | 21 | 规模化数据中心二层与 Anycast 目录服务 |
| 21 | Raiciu et al. — Denial of Architecture?/ "Improvements to a Suite of Heuristics for Multipath"? 以 Wisely 为准：Is Multipath TCP Beneficial? (SIGCOMM'11) | 2011 | 12 | MPTCP 调度与耦合度决定公平性（"丢包即全窗"问题） |
| 22 | Zhu et al. — Congestion Control for Large-Scale RDMA Deployments (DCQCN, SIGCOMM'15) | 2015 | 2/12 | ECN+pacing+priority 反压：lossless 以太上的拥塞控制 |
| 23 | Gao & Rexford — Stable Internet Routing Without Global Routing Policies (ACM ToN) | 2001 | 18 | 客户/对等商业约束 ⇒ 策略路由收敛且无环 |
| 24 | Labovitz, Ahuja, Cohen, Jahanian — Internet Routing Instability（SIGCOMM'95 测量系列与 ToN 1999 集成版） | 1995–1999 | 18 | 路由抖动/会聚测量：BGP 运维科学起点 |
| 25 | RFC 9000 — QUIC: A UDP-Based Multiplexed and Secure Transport (Iyengar & Swett) | 2021 | 12/24 | 用户态、TLS1.3 内嵌、每流独立恢复、连接迁移 |
| 26 | Jacobson — Network Congestion Control: A Dynamic Systems Approach（专著） | 1996 | 12 | 控制论视角统一拥塞控制全书 |
| 27 | IETF RFC 1661/1662 — PPP/HDLC Framing | 1994 | 20 | 0 比特填充与成帧的工程范本 |

> 注：#21 论文全名以 ACM DL 检索为准（Raiciu 等 SIGCOMM'11 关于 MPTCP 公平性的工作），此处保留"待核实"提示；#16 Perlman 的桥接/STP 成果散见博士论文（1984）与期刊版，年份给区间。

## 2. 近 5 年动态表（2021–2026）

| 主题 | 文献/事件 | 年份 | 对应讲次 | 状态 |
| --- | --- | --- | --- | --- |
| HTTP/3 标准化 | RFC 9114 HTTP/3（2022-06）；前身草案 RFC 8979 线 | 2022 | 5/12 | 已发布；主流浏览器/CDN 默认启用 |
| QUIC 基座 | RFC 9000/9001/9002 | 2021 | 12/24 | RFC 9002 为通用框架，不绑定具体算法 |
| QUIC 周边 | RFC 9204 QPACK；RFC 9298? （H3 Datagram，待核实号段）；DoQ RFC 9250 | 2022 | 6/12 | DoQ（DNS over QUIC）2022 发布 |
| MASQUE（代理/隧道 over H3） | RFC 9484（代理连通性测试）与 connect-ip/port 草案族 | 2023–2025 | 15/19 | VPN-over-H3 演进中；具体条目待核实 |
| BBRv2 | Google 论文/草案线（Cardarelli 等）；RFC 9469 仅规范 BBRv1 | 2021 起 | 12 | v2 长期实验、未标准化；部署比例待核实 |
| Multipath | RFC 8699 MPTCPv1（2020）；Linux 主线完善（5.6 引入→6.x full-mesh/netlink 路径管理） | 2020–2024 | 11/23 | 内核可用；应用生态待成熟 |
| 数据中心以太 | IEEE 802.3df 1.6TbE（2024）；Ultra Ethernet Consortium 1.0 规范发布 | 2024–2025 | 21 | UEC 面向 RDMA/集合通信；条款细节待核实 |
| Wi-Fi 7 | IEEE 802.11be（2024 批准）：MLO、320MHz、4K-QAM | 2024 | 22 | 与教材 §7.1 演进线一致 |
| 5G-Advanced | 3GPP Rel-18 冻结（2024）、Rel-19/20 推进；RedCap 规模商用 | 2024–2025 | 23 | 商用时间表按运营商，待核实 |
| 卫星直连 | 3GPP NTN Rel-17 起步、Rel-18 扩展；Starlink/T-Mobile 文本直连（2024-25） | 2024–2025 | 23 | 手机直连卫星进入标准与试点 |
| BGP 安全 | RPKI/ROV 部署率上升；RFC 9807? （RPKI 证书清单更新类 RFC，编号待核实） | 2023–2025 | 18 | 劫持检出率仍有限 |
| 新传输算法学术线 | delay-based（Copa/Sprout）、L4S（Low Latency, Low Loss, Scalable Throughput）RFC 9331/9332 部署实验 | 2021–2023 | 12 | L4S 双队列+ECN/AQM 组合进入标准实验 |
| io_uring 网络 | Linux zcrx（零拷贝接收）、io_uring 网络扩展持续合入 | 2023–2025 | 7/13 | 内核高性能 IO 的当代答案之一 |

## 3. 知识点 ↔ 开源项目映射表

| 知识点（讲次） | Linux 内核 | 用户态/其他 | 观察/实验工具 |
| --- | --- | --- | --- |
| TCP：状态机/RTT/窗口/拥塞（11/12） | `net/ipv4/tcp_*.c`、`tcp_cubic.c`、`tcp_bbr.c` | FreeBSD `netinet/`（教学友好）、lwIP（嵌入式）、DPDK TCP/IP 栈 | `ss -ti`、`ip ss`、Wireshark、`tc netem` |
| UDP/分用/GRO（9） | `net/ipv4/udp.c` | 全部 QUIC 栈（下行） | `ss -ua`、perf（softirq） |
| QUIC/HTTP-3（5/12/24） | —（用户态） | **quiche**（Rust）、**lsquic**（C）、picoquic、quic-go、msquic、s2n-quic、ngtcp2 | qlog、Wireshark QUIC 解密 |
| HTTP 服务器/路由/反向代理（5/7） | — | **Nginx**、**Envoy**、h2o、Caddy、Apache | `curl -v`、`tcpdump`、wrk |
| DNS（6） | — | BIND9、Unbound、CoreDNS、dnsdist | `dig +trace`、Wireshark DNS |
| 数据平面/LPM（13/14） | `net/ipv4/fib_trie.c` | **DPDK** l3fwd、**FD.io VPP**（ip6-lookup）、SONiC+SAI | `ip route show`、testpmd、`vppctl` |
| 拥塞控制/AQM（2/12） | `tcp_cubic.c`、`sch_fq_codel.c`、`sch_red.c` | Netem、CoDel/PIE 实现 | `tc -s qdisc`、`ip ss`、Grafana |
| 以太网/CRC/交换机（20/21） | bridge、`lib/crc32.c`、e1000/ixgbe、NAPI | OVS、DPDK l2fwd、Mininet | `bridge fdb`、`ovs-ofctl` |
| SDN/OpenFlow/P4（19） | — | OVS、Floodlight/ONOS/ODL、BMv2/P4 | `ovs-ofctl dump-flows`、mininet+ryu |
| 路由协议 LS/DV/BGP（16–18） | — | **FRRouting**（bgpd/ospfd/ripd）、GoBGP、BIRD | `vtysh`、`gobgp rib`、RouteViews/BGPStream |
| ICMP/ping/traceroute（19） | `net/ipv4/icmp.c` | iputils、mtr | `strace ping`、`tcpdump icmp` |
| Wi-Fi 802.11/安全（22） | mac80211/cfg80211、wext | hostapd、wpa_supplicant、OpenWrt | monitor 模式 Wireshark、`iw` |
| 蜂窝/移动性（23） | — | srsRAN、Open5GS、free5GC、ModemManager | GTP-U 抓包（udp 2152）、`mmcli` |
| TLS/加密/VPN（24） | crypto API、WireGuard | OpenSSL/BoringSSL、mbedTLS、strongSwan、Tailscale | `openssl s_client`、SSLKEYLOGFILE |
| socket 边界/高性能 IO（7） | `fs/io_uring.c` | liburing、Tokio/epoll 系 | `strace`、io_uring 观测工具 |

## 4. 使用建议

- 第 6/10/12/17/18 讲优先配论文精读：DNS(1034/1035)、SACK(2018)、Jacobson'88、RIP/计数到无穷原始报告、Gao-Rexford。
- CS144 实验周（拥塞控制）与本表 #6/10/11/25 对照读，公式↔代码双通道。
- 近 5 年表用于"延伸阅读"的持续更新入口；标"待核实"的条目以 IETF Datatracker / ACM DL 检索为准。
