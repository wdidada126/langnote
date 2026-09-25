# 第 21 讲 · 以太网、交换机自学习与 STP/VLAN（附：网卡与 XPON）

> 章节：Chapter 6 §6.4–§6.6
> 中文对照：topdown_ustc 第 6 章（以太网与交换机）；配套项目 projects/ch5_ethernet_sim（帧/交换机学习）

## 1. 核心概念

- **历史线**：10Mbps 总线（CSMA/CD，同轴）→ 10Mbps 星形中继器/集线器（冲突域不变）→ 交换机（每口一域，全双工，CSMA/CD 退役）→ 快速/千兆/万兆（光纤为主，MPLS/数据中心演进见 CS168）。
- **以太网帧（II 型）**：`前导码 7B + SFD 1B | 目的 MAC 6 | 源 MAC 6 | (VLAN tag 4: 0x8100+TCI) | 类型 2（0x0800 IP / 0x0806 ARP）| 载荷 46–1500 | FCS 4`。
  - **MTU 1500**=载荷上限；最小帧 64B 源于总线时代冲突检测窗（时延×带宽/2 的几何论证），今天保留兼容——**以太网不做分片，交给 IP（第 14 讲）**；巨型帧（jumbo 9000）是运维选项。
- **MAC 地址**：48 位扁平、烧录+本地管理位/组播位；OUI 分配。
- **交换机 = "自学习+存储转发"的二层桥**：
  - **学习**：从入帧**源 MAC** 填表 `(MAC → 端口, 老化时间默认 300s)`；
  - **转发/泛洪**：查目的 MAC——已知则单播该口，未知/广播则**除入向全部泛洪**；广播帧每 VLAN 一次。
  - 对比集线器：冲突域/带宽/全双工三点全赢；"插错口"不再需要。
- **多交换机与 STP**：物理冗余⇒逻辑成环⇒广播风暴+MAC 表漂移；**802.1D 生成树**（根桥选举→根端口/指定端口→阻塞冗余口，BPDU 2s 周期）；快速收敛演进：RSTP(802.1w)/MSTP(802.1s)/PVST+（每 VLAN 一棵树）。
- **VLAN（802.1Q）**：二层广播域切分；access/trunk 端口、native VLAN；VLAN 间需三层路由（"单臂路由"→ 三层交换机 SVI）；VXLAN（第 19 讲 SDN 语境：MAC-in-UDP，48-bit VNI 解决多租户扩展——"云计算的以太网"）。
- **链路层在 OS（§6.5）**：网卡（NIC）= 链路层+物理层硬件；驱动负责 DMA 环（TX/RX ring）、中断→NAPI 轮询、offload（checksum/TSO/LRO）——**这些 offload 正是抓包"看不到正确校验和"的原因**（第 20 讲 CRC 的软件对照）。
- **XPON 附块（§6.6 教材中文增补）**：GPON 帧结构（下行 GEM 帧广播+加密、上行 TDMA 测距 alloc）；EPON 与 10G-PON 共存波长规划；与第 1 讲 PON 接入呼应、与第 20 讲多路访问对应。

## 2. 关键数字/表

- 交换机转发方式：存储转发（全帧校验后查表，时延=L/R）vs 直通（cut-through，读到目的 MAC 即转发）vs 碎片过滤。
- MAC 表规模、端口数、背板容量（线速=端口×带宽×2 双向）——数据中心交换机规格阅读法。
- STP 计时器：forward delay 15s×2、max age 20s——"改口要等 30-50s"的历史阴影（RSTP 亚秒级）。

## 3. 层次间与前后讲联系

- 封装栈：IP 数据报进以太网帧（type 字段=protocol 字段的二层对应，第 14/15 讲）；ARP（第 15 讲）是交换机之上唯一"看见 IP"的时刻。
- 交换机自学习对照路由器 LPM：MAC 精确匹配、无层级、靠泛洪 bootstrap——**扁平地址 vs 分层地址**的代价表（第 3 讲）。
- VLAN/STP 的广播域收缩是 Wi-Fi（第 22 讲）与数据中心 overlay（VXLAN）共同背景。

## 4. 跨课程联系

- **CS144**：lab 中下一跳的以太网封装在 harness 完成；理解了自学习就明白"为什么 CS144 不需要 ARP/交换机模型"。
- **CS168**：以太网/数据中心桥接（FCoE/DCB/PFC/ECN，RDMA lossless fabric）把 STP 换为 ECMP+拥塞信号——读 papers.md 的 DCQCN。
- **6.S081/CS162**：xv6 e1000 驱动实验（e1000.c 的 TX 描述符环）是本讲 §6.5 的可读代码版；CS162 用 NAPI/interrupt 讨论链路层上收边界。
- **CSAPP**：tiny 服务器跑在以太网之上但不可见；容器网络实验里 `bridge` 网络即 Linux bridge（交换机软件实现）。
- **topdown_ustc**：郑烇老师交换机学习/泛洪逐步动画与 STP 端口状态图。

## 5. 开源项目应用

- **Linux bridge**：`bridge fdb show` 看自学习表；`tc` 模拟老化/风暴；`systemd-networkd` VLAN/bridge 配置。
- **OVS**：可编程二层（流表代替学习逻辑），SDN 的第一层落点（第 19 讲）。
- **FRR + freeradius**：802.1X 端口认证生态；hostapd 的 wired/wireless 统一。
- **DPDK**：`l2fwd` 演示用户态 MAC 表转发（学习+老化自实现）；VPP 的 `l2` 插件同构。
- **Wireshark**：官方 Ethernet lab（ARP+DHCP+交换机泛洪抓包）；BPDU 过滤 `stp`。
- **dpdk-testpmd / OpenNetworkLab（ONL 白盒）/ FRR**：从虚拟到白盒交换机的进阶玩具。

## 6. 延伸阅读

- IEEE 802.3（帧）、802.1Q（VLAN）、802.1D/802.1w（STP/RSTP）、RFC 7348（VXLAN）、draft-ietf-nvo3-vxlan-gpe（VXLAN-GPE 扩展）
- Perlman《Rethinking the Design of LAN Bridging》(1988)——学习桥的原始论文（papers.md 经典表）
- 官网 §6.4 + Wireshark Ethernet lab

## 7. 自查问题

1. 交换机如何学到"MAC 在哪个口"？新接入主机第一条帧会怎样被处理？
2. 为什么以太网最小帧 64B 与"总线最大跨距"相关？全双工交换机后该约束还有必要吗？
3. STP 阻塞的端口能收发 BPDU 吗？根桥选举靠什么？
4. VLAN 与子网必须一一对应吗？跨 VLAN 通信经过哪几层？
5. VXLAN 为什么用 UDP 承载二层？对路由器/防火墙意味着什么（封装栈再穿一层）？

## 8. 本讲一句话

以太网赢在"简单+兼容"（扁平地址、不分片、不重传），交换机赢在"自学习+泛洪兜底"；二者合力让二层成为"廉价的、可无限复制的本地域"，而一切规模问题交给 STP/VLAN/overlay 打补丁。
