# 第 19 讲 · 传统控制平面运维：OSPF/RIP 细节、ICMP 与 SDN/OpenFlow

> 章节：Chapter 5 §5.3–§5.5（传统控制平面/ICMP/SDN 控制面/排障）
> 中文对照：topdown_ustc 第 5 章（OSPF/ICMP/SDN）

## 1. 核心概念

- **OSPF 工程细节（LS 的生产形态）**：
  - 邻居状态机：Down → Init → 2-Way（DR/BDR 选举！广播网用 0.0.0.6 只与 DR 通信）→ ExStart/Exchange/Loading → Full。
  - LSA 类型：1 Router、2 Network（DR 生成）、3 Summary（ABR）、5/7 External（ASBR）；区域类型：骨干 0、stub/NSSA——层次化 LSDB（第 16 讲"泛洪域"落地）。
  - Hello/Dead 计时器（10/40s 默认）决定收敛速度；`ip ospf network point-to-point` 免 DR。
- **ICMP**：差错型（Destination Unreachable/Medium Unreachable(TTL 超时)、Redirect、Parameter Problem）+ 查询型（Echo、Timestamp、掩码）。差错报文**携带引发错误的原报头+前 8 字节**（让发方匹配 socket！——第 9 讲分用的闭环）；差错不使用可靠性、不违反"数据报服务尽力而为"。
  - ping=Echo 请求/应答；traceroute 两种流派（Linux 默认 UDP 高端口递增 TTL，收到 TTL-exceeded；`-I` 用 Echo、`-T` 用 SYN）。
  - ICMP 被限速/丢弃导致 PMTUD 黑洞（第 14 讲）、误配防火墙的"经典元凶"。
- **SDN 控制平面（教材第 7 版把 §5.3 SDN 作为与"传统"对照的主轴）**：
  - 三平面：转发（flow table）/ 控制（控制器）/ 管理（北向应用）。
  - **OpenFlow 匹配-动作表**：10 字段匹配（in_port、以太网/IP 各字段、TCP 标志、VLAN…）、优先级（最长匹配语义的通配版）、动作（转发/组播/丢弃、改写、计数）；table-miss 上报控制器（packet-in）；流表空闲超时（idle timeout）回收。
  - ONOS/ODL 级联控制器、一致性（虚拟交换机抽象）问题。
  - 现实谱系：OpenFlow 纯派（实验网）→ OVS+FRR/GoBGP 混合（"BGP 即分布式控制面"，第 18 讲）→ P4 可编程（数据面也开放，papers.md）。
- **控制平面排障（§5.5）**：`looking-glass`（运营商远程路由查询）、RouteViews/BGPStream（看全球路由）、`ip route get`/`traceroute` 联动、路由"该在不在"的三源核对（设备 RIB/looking-glass/RPKI）。

## 2. 关键字段/命令速查

- OSPF 报文 5 型：Hello/DBD/LSR/LSU/LSAck（全部 IP 协议号 89、组播 224.0.0.5/6）。
- OpenFlow 典型流表：`priority=100, ip, nw_dst=10.1.0.0/16, actions=2,3`（OVS 语法，`ovs-ofctl dump-flows`）。
- ICMP 类型码：3/0 网络不可达、3/1 主机、3/3 端口、11/0 TTL 超时、8/0 Echo——`traceroute/ping` 的报文真身。

## 3. 层次间与前后讲联系

- OSPF 是本讲与第 16 讲算法的"协议外壳"；RIP 对应第 17 讲。ICMP 把第 13-14 讲"差错→反馈给端"机制化；traceroute 是第 2 讲逐跳排队时延的观测器。
- SDN 把第 13 讲查表（LPM）与第 16-18 讲"表从哪来"统一为控制器视角：路由计算在中心、下发即 FIB。

## 4. 跨课程联系

- **CS168**：SDN 与网络编程（OpenFlow/P4/ONOS）主场；OpenFlow 之后可续读其论文链（papers.md）。
- **6.S081**：xv6 网络实验（P4 版交换机）用"转发即程序"思想——SDN 内核化预演；CS162 讲内核 softirq 中 ICMP 生成路径。
- **CS144**：`traceroute` 是其 router testbench 的验收工具（TTL 逻辑 lab3）。
- **MIT6.824**：OpenFlow 控制器的"全局视图+单点故障"讨论可套 6.824 的容错框架（Kubernetes 的 kube-proxy/OVN 是工业答案）。
- **topdown_ustc**：郑烇老师 OSPF 报文抓包实验与 ICMP 全类型表。

## 5. 开源项目应用

- **FRR `ospfd`**：邻居状态机与 LSA 库源码；`vtysh` 实时看拓扑。
- **Open vSwitch**：`ovs-ofctl`/`ovs-vsctl`——流表实验最低成本入口；OVN 是其控制层。
- **ONOS/ODL**：教科书 SDN 控制器；Floodlight（Mininet 教程标配）。
- **Mininet**：单机虚拟 SDN 拓扑——本讲与第 13 讲实验首选平台。
- **mtr / smokeping / bgpstream**：控制/数据平面联合排障工具链。
- **Linux `ping/traceroute/tracepath`**：tracepath 不需特权、用 PTB（packet too big）探 PMTU（第 14 讲呼应）。

## 6. 延伸阅读

- RFC 2328（OSPF）、RFC 2740（OSPFv3）、RFC 4443（ICMPv6）、RFC 7772（ Redirect 的滥用作废旧）、RFC 1925（网络诸箴言，彩蛋必读）、OpenFlow Switch Spec v1.5（开放网络基金会）
- McKeown et al.《OpenFlow: Enabling Innovation in Campus Networks》(2008, papers.md)
- 官网 §5.3-5.5 + Wireshark ICMP lab

## 7. 自查问题

1. 广播网为何要 DR？断 DR 时邻接如何重建、流量是否瞬断？
2. ICMP "端口不可达"从生成到送达 socket 走哪几层？（差错里嵌 8 字节端口的原因）
3. OpenFlow 的 table-miss + packet-in 等价于传统路由器的什么路径？慢在哪？
4. 为什么说 SDN 没有消灭路由算法而是"搬家"？（第 16-18 讲算法在控制器内复现）
5. `-I` traceroute 与 UDP traceroute 在防火墙后的可见性差异？

## 8. 本讲一句话

控制平面的"运维三件套"：IGP 协议细节（OSPF/RIP）、反馈通道（ICMP）、新范式（SDN 把表变成程序）——排障是把三者摆到同一张拓扑图上找不一致点。
