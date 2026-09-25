# 第 22 讲 · Wi-Fi：802.11 架构、CSMA/CA、隐藏终端与安全演进

> 章节：Chapter 7 §7.1–§7.2
> 中文对照：topdown_ustc 第 7 章（无线局域网）

## 1. 核心概念

- **802.11 vs 以太网的三个不同**：共享无线介质（干扰而非冲突主导）、信号强度随距离衰减（近-远问题）、移动性（关联可变）。
- **架构**：
  - 基础结构模式（infrastructure）：STA ↔ AP ↔ 分布式系统（DS，骨干）；SSID 是"逻辑网络名"，一个 AP 可发多 BSSID（多 VLAN/多租户，第 21 讲呼应）。
  - ad-hoc/IBSS 与 Wi-Fi Direct（P2P 直连）。
  - **关联生命周期**：扫描（主动 Probe/被动 Beacon 102.4ms 周期）→ 认证（历史遗留，几乎空转）→ 关联（Association）→ DHCP（第 15 讲）→ 数据；**分配向量 NAV**：听到别人声明"信道要忙 T 秒"就虚拟监听。
- **帧格式（三层地址！）**：帧控（Type/Subtype、**To DS/From DS**、More Frag、Power Save）+ **Addr1 接收、Addr2 发送、Addr3 网络内对端/DS**（四地址 WDS 模式历史）+ Seq + 载荷 + FCS；与以太网差异：数据帧也要逐跳 ACK（链路层可靠，第 20 讲哲学），且**MAC 地址≠通信双方**。
- **CSMA/CA（为什么不能 CD）**：收发同频无法自检冲突；先听后发 + **DIFS + 随机退避（指数，窗口加倍）** + 可选 **RTS/CTS 预约**（NAV 解隐藏终端、但浪费两次握手） + 短帧优先（CFP/PCF 历史、802.11e EDCA 语音优先）。
  - 数据→ACK 机制：**每帧确认**（802.11 block ACK 聚合）+ 重试上限——第 10 讲 ARQ 在链路层真实出现。
- **物理层演进（谱系）**：DSSS/FHSS（1-2Mbps）→ OFDM（a/g 54Mbps；子载波抗频率选择性衰落）→ MIMO（n，空间复用）→ OFDMA+MU-MIMO（ac/ax）→ Wi-Fi 6/6E/7（ax=OFDMA+BSS Color+TWT 省电；be=320MHz+4K-QAM+MLO 多链路聚合）。
- **安全（本讲必背演进线）**：WEP（RC4+ICV，IV 复用致命：同密钥同 IV → 密钥恢复攻击）→ WPA/TKIP（过渡补丁）→ WPA2-CCMP（AES-CTR+MAC，802.11i 四次握手/PMK→PTK→GTK）→ WPA3-SAE（拒离线字典、Dragonblood 后仍为主流）+ OWE（开放网络加密）+ 192 位企业套件；802.1X/EAP 企业认证（radius，第 24 讲 TLS-EAP 家族）。
- **移动与共存（§7.2）**：AP 内切换（STA 自主/协助）、**跨 AP/ESS 切换依赖上层**（移动 IP/简单重关联丢缓存）；Mesh（802.11s）、蜂窝 Wi-Fi 卸载（VoWiFi）、同频干扰协调（运营 Wi-Fi 的 channel planning）。

## 2. 关键数字/字段

- 时隙：SIFS（ACK 前）< PIFS < DIFS；EIFS（错帧后惩罚）。
- 速率自适应：ARF/Minstrel（采样-回退），是链路层版"拥塞控制式试探"（第 12 讲对照：一个测信道一个测网络）。
- Beacon/Probe/ACK RTS CTS 帧subtype 与地址字段用法（考试给帧判断 To DS/From DS）。

## 3. 层次间与前后讲联系

- 无线帧=第 20 讲成帧/差错 + 第 21 讲 MAC 寻址的变体；DS 骨干常是以太网（封装栈双帧嵌套：AP 改写外层）。
- CSMA/CA 与 Aloha/CSMA（第 20 讲）直系；WEP 破译需要密码学直觉（第 24 讲）。
- 移动性（第 23 讲）与蜂窝切换的"链路层触发+网络层配合"在此埋点。

## 4. 跨课程联系

- **CS168/CS162**：无线测量（signal strength、干扰热图）是 CS168 实验常见；CS162 把 802.11 每跳 ACK 作为"与 IP 端到端哲学相悖"的讨论案例。
- **6.S081**：无内核无线细节；但 mac80211/cfg80211 子系统是 Linux 里"链路层状态机"代码规模的极端样本（了解名词即可）。
- **DDCA/CS61C**：OFDM 子载波正交、扩频需要一点信号基础（可选先修）。
- **MIT6.824**：无直接对应；可作为"共享介质协调=分布式锁"的类比题。
- **topdown_ustc**：CSMA/CA 退避算法动画、RTS/CTS 时序图与官网同源。

## 5. 开源项目应用

- **Linux**：mac80211/cfg80211（`iw`、`iwconfig`）；**hostapd**（AP 软件栈+802.1X）；wpa_supplicant（STA 侧四次握手）；ath9k/iwlwifi 驱动生态。
- **Wireshark + monitor mode**：官方 802.11 lab——唯一能看 Beacon/RTS/ACK 的姿势；`wlan.fc.type_subtype` 过滤。
- **OpenWrt**：家用路由器全栈（dnsmasq+hostapd+防火墙），把第 15/19/21/22 讲集成在一个设备上。
- **Kismet / Aircrack-ng**：无线抓包与 WEP/WPA 审计工具（仅限自有网络实验，复现第 6 节论文思路）。
- **ESP-IDF/RT-Thread Wi-Fi**：嵌入式 STA 最小实现，读一遍关联/获取 IP 流程。

## 6. 延伸阅读

- IEEE 802.11-2020（标准全书）、RFC 4017（WPA/无线安全早期评估）、RFC 5416（CAPWAP，AC-AP 隧道）、802.11ax/be 白皮书
- Borisov et al.《A Cryptographic Analysis of the WEP Protocol》(2001) 与 Fluhrer-Mantin-Shamir（papers.md 经典表）
- 官网 §7.1 + Wireshark 802.11 lab

## 7. 自查问题

1. 给一帧"AP 转发给 STA 的数据"写出三个地址字段各是谁；为什么 Ethernet 不需要第三个？
2. RTS/CTS 何时净收益为正（帧长×竞争规模推演）？NAV 如何防止第三节点插入？
3. WEP 的 IV 放明文帧头导致什么攻击路径？CCMP 如何修（计数器+AEAD）？
4. 四次握手产出的 PTK/GTK 各保护什么帧？PMK 从哪来（PSK vs EAP）？
5. Wi-Fi 6 的 OFDMA/TWT 分别解决本讲哪个痛点（并发/省电）？

## 8. 本讲一句话

Wi-Fi = 以太网语义（无连接 IP 之上、自管地址）套上一个"不能边听边发、靠退避+ACK+分配向量合作"的共享信道——物理约束决定协议形状的最佳标本。
