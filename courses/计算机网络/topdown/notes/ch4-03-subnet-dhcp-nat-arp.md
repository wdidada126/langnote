# 第 15 讲 · 子网划分、CIDR、DHCP、NAT、ARP 与数据平面排障

> 章节：Chapter 4 §4.4–§4.6
> 中文对照：topdown_ustc 第 4 章（IP 地址/子网/ARP）；配套项目 projects/ch4_router_sim（FIB 部分）

## 1. 核心概念

- **子网（subnet）**：把网络号再借位成"子网号+主机号"；路由器接口=子网边界；一台多网口主机可属多子网。
- **CIDR（无类域间路由）**：`a.b.c.d/n` 前缀表示，取代 A/B/C 类；聚合（route aggregation）让 FIB 规模可控——这是 LPM（第 14 讲）存在的根因。
- **DHCP**：`DISCOVER(广播) → OFFER → REQUEST → ACK`（DORA），分配 IP/掩码/网关/DNS（选项 6/15/43 等）；"租约+续约"；中继（DHCP relay）跨子网集中管理。IPv6 有状态 DHCPv6 / 无状态 SLAAC（第 14 讲）之争=配置哲学差异。
- **NAT/NAPT**：把私有地址（RFC 1918）复用为全球地址+端口；映射表是六元组（内外 IP/端口+协议）；**NAT 类型（锥形/全锥形/对称）**决定 P2P 打洞可行性；ALG（FTP/SIP 载荷改写）是"翻译应用层地址"的补丁，也是安全漏洞温床。
- **ARP**：`who-has IP? tell MAC` 广播请求+单播应答；ARP 缓存（`ip neigh`）；**ARP 是链路/网络的胶水**：同子网直接 ARP 目标 MAC，跨子网 ARP 默认网关 MAC——"MAC 只解决最后一跳"的铁律由此出。
- **数据平面排障**：`ping`（通/断层面定位）、`traceroute`（UDP 递增 TTL 或 ICMP echo 型，暴露逐跳路径与黑洞）、`dig`（第 6 讲）、`mtr`（持续路径统计）；经典故障：NAT 超时导致长连接静默断（keepalive 与 TCP 保活参数，第 11 讲呼应）。

## 2. 关键计算/字段

- 子网划分公式：`主机位 h 位 ⇒ 每子网 2^h−2（传统去网络/广播地址）`；`可借 s 位 ⇒ 2^s 子网`。现代 /31 点对点链路不再减 2。
- VLSM：从大到小分配再聚合回 CIDR；CIDR 聚合=相同前缀最长公共位。
- 私有地址段：10/8、172.16/12、192.168/16；链路本地 169.254/16（APIPA，DHCP 失败兜底）。
- ARP 报文：硬件类型/协议类型/操作码（1 请求 2 应答）/发送方+目标（MAC/IP）。ARP 无法跨路由器（广播域限制，第 21 讲 VLAN 进一步收缩广播域）。

## 3. 层次间与前后讲联系

- 本讲把"地址从哪来"（DHCP/子网）、"跨子网怎么走"（默认网关/ARP/CIDR 聚合）、"不通怎么查"（traceroute）三件事一次说清——是第 13/14 讲数据平面的运维侧。
- NAT 打洞为第 8 讲 P2P 补上现实约束；ARP/以太网广播域在第 21 讲由交换机/VLAN 展开；移动 IP 的隧道（第 23 讲）复用本讲"改写外层地址"思路。
- 封装栈：ARP 请求封装在以太帧里（type 0x0806）——"网络层协议走链路层信道"的奇例。

## 4. 跨课程联系

- **CSAPP**：CSAPP 实验里容器/虚拟机的私有网段+DHCP 配置即本讲工程版。
- **6.S081**：xv6 的网络栈实验（P4 网络）中 ARP/子网概念由内核协议栈执行；`ip neigh` 的"邻居子系统"在 Linux `net/ipv4/arp.c`。
- **CS162/CS168**：地址空间经济学（IPv4 枯竭→NAT 续命→IPv6 缓慢部署）、SD-WAN 中的 NAT 穿透。
- **CS144**：其 lab 的 network interface 层抽象里，ARP/以太网封装由 harness 提供，理解"为什么接口有 next_hop 字段"靠本讲。
- **topdown_ustc**：郑烇老师子网计算习题系列（画/26、聚合 CIDR）与考试题型一致，必刷。

## 5. 开源项目应用

- **Linux**：`ip addr/ip route/ip neigh`（`iproute2` 全家桶）；dnsmasq（DHCP+DNS 一体，家用路由器标配）；keama/ISC-DHCP（企业级）；conntrack+nftables（NAPT/ALG）。
- **systemd-networkd / NetworkManager**：DHCP 客户端工程实现，`networkctl` 观察 DORA。
- **Wireshark**：官方 DHCP/ARP lab（广播+端口 67/68 细节）。
- **GNS3/Packet Tracer/Containerlab**：子网/NAT/traceroute 演练沙盒；Containerlab+Linux=用真内核做拓扑实验（projects/ch4_router_sim 思路同源）。
- **Coturn（STUN/TURN）**：NAT 穿透失败的兜底中继，WebRTC 基础设施。

## 6. 延伸阅读

- RFC 1918（私有地址）、RFC 2131/3315（DHCP/v6）、RFC 1542（DHCP 中继）、RFC 4632（CIDR）、RFC 826（ARP）、RFC 4861（NDP，v6 的 ARP+）、RFC 5382（STUN）、RFC 4787（NAT 行为要求）
- 官网 §4.4-4.6 + Wireshark DHCP/ARP labs + 子网习题集

## 7. 自查问题

1. 同子网两主机通信，ARP 解析谁的 MAC？跨子网呢？写出两帧的目的 MAC 差异。
2. DHCP 首次发现为何用广播？服务器如何知道客户端在哪个子网（relay-agent 选项）？
3. 给定 192.168.10.0/24 划分 4 个等大子网：各前缀、可用主机数、广播地址。
4. 对称 NAT 为什么让打洞失败（映射随目的变化）？TURN 兜底的代价？
5. traceroute 用 UDP 高端口的原始动机（RFC 791 之前的 ICMP 限制/特权）？现代 `-M tcp` 型原理？

## 8. 本讲一句话

数据平面的"人间烟火"：地址靠 DHCP 租、路径靠 CIDR 聚、最后一跳靠 ARP、故障靠 ping/traceroute——工具与协议一一对应，背熟即可实战。

## 9. 记忆卡

- DORA 四步；/30 与 /31；192.168/10/172.16 私有段；169.254 链路本地。
- ARP：同网直 arp 目标，异网 arp 网关；广播不出路由。
- traceroute 两流派（UDP-TTL / TCP-SYN）；`ip neigh`/`ip route get` 是最快自检双板斧。
