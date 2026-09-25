# 第 1 讲 · 网络边缘：主机、接入网与传输媒体

> 章节：Chapter 1 Computer Networks and the Internet | 对应教材：§1.1、§1.4
> 中文对照：topdown_ustc 郑烇老师 第 1 章（网络边缘部分）

## 1. 核心概念

- **网络边缘（edge）**：运行分布式应用的主机（端系统，end system）。两种应用架构：
  - **客户端/服务器（C/S）**：服务器是常开主机、有固定 IP；客户端间歇连接。服务器可数据中心化（DNS、Google 前端集群）。
  - **对等（P2P）**：无永远在线的中心服务器，对等方间歇连接、自扩展性强（BitTorrent、Skype 遗留架构）。理想 P2P 完全去中心，但现实中常保留目录/协调服务器。
- **接入网（access network）**把端系统连到边缘路由器：
  - 家庭：DSL（电话线频分复用：0–4kHz 语音 / 上行 / 下行）、HFC（电缆网，下行共享 42Mbps~1Gbps 量级，非对称）、FTTH（光纤到户，三种架构：交换以太网 / 异频 DSL / **PON 无源分光**——多家共享一根光纤，下行广播+加密、上行 FDM/TDMA）。
  - 企业：以太网（交换式，第 6 章）、Wi-Fi（802.11，第 7 章）。
  - 广域无线：4G LTE / 5G 基站，经电信接入网连到因特网（第 7 章）。
- **传输媒体（guided media）**：双绞线、同轴、光纤（单模 vs 多模；光纤不受电磁干扰、低衰减、适合 >100km，是骨干网绝对主力）、地波/微波/卫星（unguided）。
- **网络的网络**：ISP 分层——Tier-1（跨洲、对等免费）、Tier-2（对等+购买上游 transit）、Tier-3（本地接入 ISP）；IXP（互联网交换点）与私有对等/专用链路解决互联的"结算"经济学问题。
- **WAN 接入遗留**：拨号、帧中继、ATM（教材历史脉络；今日城域以太与 MPLS/SRv6 更常见，见 CS168）。

## 2. 关键数字与结构

- 客户端-服务器 vs P2P 的下载时间对比公式（教材例：100 客户端、10Mbps 服务器）：
  - C/S：`T = N·F / min(us, ulc)`，受服务器上行瓶颈；
  - P2P：`T = F / max(ulc, us/N)`，用户越多自扩展——这是第 2 章 BitTorrent 分析的预演。
- HFC 下行链路 max-delay 计算：`N·L/R`（N 个包同时到达竞争信道）。

## 3. 层次间与前后讲联系

- 本讲是"封装栈"的两端：应用协议（第 2 章）在端系统实现，其下立即是运输层；接入网技术则决定第 6/7 章链路层与物理层的形态（共享介质 → 多路访问协议与 MAC）。
- 下一讲（网络核心）补上中间部分：分组交换与电路交换之辩、时延四件套。

## 4. 跨课程联系

- **CSAPP**：C/S 架构中的 socket 编程在 CSAPP 第 11 章有完整实现（tiny 服务器），与本课 §2.4 双视角。
- **CS168 / CS144**：CS168 从"因特网即软件系统"角度重讲 ISP/IXP 经济学与数据中心网络；CS144 lab 中你要实现的是端系统协议栈，接入网只以"虚拟以太网对（Linux netns/veth）"出现。
- **6.S081/CS162**：内核里网卡驱动（e1000）即"接入网最后一跳"的软件化身。
- **topdown_ustc**：郑烇老师用"快递寄件"类比端系统与中间网络，适合第一遍建立直觉。

## 5. 开源项目应用

- **Linux 内核**：`net/core/` 与 `drivers/net/ethernet/` 中 `dev_queue_xmit` 之下即接入网设备抽象（`struct net_device`）；`tc`（traffic control）在出口模拟 HFC 共享竞争。
- **Wireshark**：抓家庭路由器 WAN 口即可分辨 PPPoE（DSL）、DOCSIS 电缆、以太网帧（FTTH 交换式）。
- **ppp / rp-pppoe**：DSL 时代拨号接入的开源实现，今日仍见于路由器固件（OpenWrt）。

## 6. 延伸阅读

- RFC 1122（Requirements for Internet Hosts——端系统行为总纲）
- ITU-T G.984（GPON 标准，对应教材 XPON 一节）
- RFC 792 之前史：《Packet Switched Communications》（Baran, 1964，见 papers.md）
- Kurose & Ross 第 7 版 §1.1/§1.4 + 官网 Wireshark lab 0（Getting started with Wireshark）

## 7. 自查问题

1. 为什么 PON 上行用 TDMA/FDMA 而不是让所有 ONU 同时发？（提示：共享介质冲突，联系第 20 讲多路访问）
2. FTTH 的三种架构里，为什么运营商最终主流选择 PON？（成本：无源分光器免供电免维护）
3. 计算：100 个客户端从 2Mbps 服务器拉 100KB 文件 vs P2P（各 50Kbps 上行、10Mbps 下行），谁先完成？何时 P2P 开始反超？
4. Tier-1 为什么愿意免费对等？（到达全网的"互达性"价值 > 结算成本）
5. HFC 下行是广播，为什么不影响隐私？（每 ONU 用自己密钥解密——联系在线安全章）

## 8. 本讲一句话与下一讲钩子

接入网决定"最后一公里"的带宽/共享形态与媒体，是 MAC 协议（第 20 讲）与无线（第 22-23 讲）的物理前提；而端系统的 C/S 与 P2P 之争将在第 8 讲（BitTorrent）和第 8 讲（CDN）给出定量答案。
