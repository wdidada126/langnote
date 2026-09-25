# 第 23 讲 · 蜂窝网络（3G/4G LTE/5G）与移动性管理架构

> 章节：Chapter 7 §7.3–§7.4
> 中文对照：topdown_ustc 第 7 章（蜂窝网与移动 IP）

## 1. 核心概念

- **蜂窝思想**：把覆盖切成小区复用频谱（同频复用距离=干扰与容量的折中）；扇区化（120° 三扇区）再乘 3 倍容量。
- **架构分层（以 LTE 为例）**：
  - 无线接入 E-UTRAN：eNodeB（基站，含控制+用户面）。
  - 核心网 EPC：MME（移动性管理）、S-GW（用户面锚点/切换转发锚）、P-GW（对外网关/策略执行 PCRF→PCF）。
  - 关键接口：S1-MME/S1-U、X2（基站间切换）、Gx/Gy（计费策略）。
- **移动性管理（网络侧）**：
  - 位置区/跟踪区（TA）：周期性 TAU + 寻呼只在"已注册区域"广播——**分页（paging）与跟踪区更新是一对永恒折中**（位置信息新鲜度 vs 信令开销）。
  - 切换：硬切换（先断后连）vs 软切换（宏分集，3G）；LTE 以**基站间 X2/S1 切换**+"数据转发避免丢包"（TCP 在切换期的重传风暴是第 12 讲现实的延伸，移动 Wi-Fi 同理）。
- **5G 增量**：SA/NSA；服务化架构（SBA，控制面 NF 间 HTTP/2+gRPC 通信——"网络协议应用层化"）；网络切片（同一物理网多虚拟专网，联系第 19 讲 SDN/NFV）；毫米波+大规模 MIMO+波束管理；UPF 用户面下沉 MEC 做低时延。
- **移动网络层（§7.4，教材核心考点）**：
  - **IP 寻址的移动性难题**：IP=位置标识，而移动主机 IP 变 ⇒ 正在进行的 TCP 连接全断（第 11 讲：socket 四元组变化即连接死亡）。
  - **移动 IPv6（MIPv6）三角色**：HA（家乡代理）、CoA（转交地址）、CN（通信节点）；**三角路由**：CN→HA（隧道，封装栈再套一层 IP-in-IP）→CoA→MS，回程 MS→CN（直路）——非对称优化=绑定更新 Route Revocation/BU。
  - **代理移动 IPv6（PMIPv6, RFC 5213）**：网络替终端做移动管理（运营商主流），MS 无感知。
  - **蜂窝 Wi-Fi 与切换**：5G 双连接、L4/L7 移动性由 **QUIC 连接迁移（第 12 讲）** 接棒——"连接迁移不靠 IP，靠连接 ID"是对 MIPv6 哲学的工程替代；TCP 侧的间接方案（I-TCP 分片，历史）与 MPTCP（多路径，RFC 8699）。
  - **传输层移动**：TCP 跨切换的四元组问题 + 无线电链路分片/间接；5G+QUIC/HTTP/3 时代"应用自己保连接"（微信/mars、Envoy 移动网关）。

## 2. 关键术语/字段

- 切换参数：TTT（time-to-trigger）、迟滞（hysteresis）——乒乓切换与掉话的权衡（与第 21 讲 STP 收敛同类工程题）。
- EPS 承载：默认承载（APN 级 QCI）+ 专用承载（GBR）——QoS 落在承载而非逐包（DiffServ 思想运营商化，papers.md）。
- MIPv6 绑定更新消息类型、Type 2 路由头（IPv6 隧道封装：外层 src=HA/CoA、内层=原始）。

## 3. 层次间与前后讲联系

- 第 21 讲以太网是固定接入的"本地域"；本讲是"广域移动"，两者在 VoWiFi/双连接缝合。
- MIPv6 的隧道=封装栈的再扩张（IP-in-IP/GRE/VXLAN 同族，第 21 讲）；寻呼依赖"网络知道位置"的假设被移动性打破（第 3 讲"地址=位置"的裂缝）。
- 切换丢包→RTO/快重传（第 11/12 讲）是"无线误码≠拥塞丢包"的著名混淆（第 12 讲 I-TCP/分片动机的来源）。

## 4. 跨课程联系

- **CS162/CS168**：CS162 用蜂窝讲"系统抽象的层次泄漏"；CS168 覆盖 RAN 虚拟化（O-RAN）与 5G 核心网云原生（SBA 即微服务——接 MIT6.824 视角）。
- **MIT6.824**：5G SBA 的 NF 间 REST/gRPC、状态外置（UDM/UDR）是"分布式系统进电信网"的活案例；AMF 容灾≈lab 的复制/故障切换讨论。
- **6.S081**：无直接内核对应；Linux 移动 Wi-Fi/WWAN 由 ModemManager/ofono 用户态守护进程代理（"内核外协议栈"又一例，对照 QUIC）。
- **CSAPP**：蜂窝模块的 AT 指令/QMI 接口≈"设备文件即协议"，与 CSAPP 的 IO 抽象一致。
- **topdown_ustc**：移动 IP 三角路由与代理移动 IP 图解，考试常出"画出 MIPv6 报文路径"。

## 5. 开源项目应用

- **srsRAN / Open5GS / free5GC**：软件 4G/5G 核心网+RAN 全家桶——一台服务器跑通注册/会话建立/切换流程（本讲最佳实验路径，配 USRP 可做空口）。
- **OAI（Open Air Interface）**：学术基站栈（eNB/gNB）。
- **Linux**：NetworkManager+ModemManager（蜂窝拨号）；mmcli 观察承载建立。
- **Envoy/MoQ 生态、mars**：QUIC 连接迁移在移动 App 网关的实践。
- **Wireshark**：GTP-U 抓包（核心网用户面隧道，`udp port 2152`）——"隧道即封装栈"现场。

## 6. 延伸阅读

- RFC 6275（MIPv6）、RFC 5213（PMIPv6）、RFC 3963（Nemo 移动网络）、RFC 8699（MPTCPv1）、RFC 9000（QUIC 连接迁移）、3GPP TS 23.401/23.501（架构规范，按需查）
- Johnson et al.《Mobile IP: Design Principles and Practices》（历史书）；Papadimitriou & Postmus《Mobile Networks: Protocols and Architecture》可选
- 官网 §7.3–7.4 + "蜂窝网三代/四代/五代对比表"

## 7. 自查问题

1. 画出 MIPv6 下 CN→MS 的双向路径，标内层/外层地址；谁做隧道封装？
2. 寻呼与 TAU 频率的折中如何用"移动性状态机"建模？与缓存失效策略同构吗？
3. 软切换为何在 3G 用、LTE 基本弃用？（频谱效率 vs 宏分集增益）
4. QUIC 连接迁移为什么不需要 IP 不变？对 NAT（第 15 讲）路径变化怎么处理？
5. 5G 切片与 VLAN/VXLAN（第 21 讲）的隔离粒度/机制差异？

## 8. 本讲一句话

移动性暴露了"地址=位置"这一因特网根基假设的代价：网络用隧道/代理/寻呼补洞，应用用连接 ID（QUIC）干脆重画——两条路线正决定未来十年的接入体验。
