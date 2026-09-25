# 第 18 讲 · BGP：域间路由、策略、iBGP/eBGP 与会聚风险

> 章节：Chapter 5 §5.2
> 中文对照：topdown_ustc 第 5 章（BGP）；对应 CS168 域间路由专题

## 1. 核心概念

- **BGP = 因特网的"外交协议"**：AS（自治系统）之间交换可达性+路径，并**以策略为先、最优性为后**（policy over performance）——与域内 IGP（第 16-17/19 讲）哲学相反。
- **四种客户/供应关系与 Gao-Rexford 稳定性条件**：客户/对等/提供商三边方向；无商业循环（客户≠反向客户）⇒ best-path 推理收敛且无环（论文在 papers.md）。
- **eBGP vs iBGP**：
  - eBGP 跨 AS，TTL=1（单跳防欺骗/多跳需 `multihop`）；路径属性里 AS_PATH 防环。
  - iBGP 同 AS 内同步 BGP 信息：**全网格要求（split horizon 式：iBGP 学到的不再传 iBGP）**⇒ 规模 O(n²) 会话 ⇒ **路由反射器 RR（RFC 4456）与联邦（confederation）** 打破网格（运营商核心标配）。
- **消息与属性**：OPEN（协商 hold timer 90/180s、BGP ID）、UPDATE（前缀+路径属性+撤销）、NOTIFICATION、KEEPALIVE；TCP 179 承载（第 11 讲——长连接+增量更新+周期性保活）。
- **属性与决策**：Well-known（ORIGIN、AS_PATH、NEXT_HOP、LOCAL_PREF 仅 iBGP）、Optional（MED、COMMUNITY）；决策序列简版：local-pref↑ → 短 AS_PATH → MED → eBGP>iBGP → 到 IGP next-hop 近 → …（可配 router-id 决胜）。
- **路由反射与聚合**：RR 客户侧与非客户侧规则（cluster-id、originator-id 防环）。
- **风险面**：前缀劫持（hijack）、路由泄漏（leak，对等误当客户传播）、巨址泄露（0.0.0.0/0 default 误宣告）、慢会聚与 MRAI/路由抖动；RPKI（ROA+验证）是密码学补丁，部署率仍在爬坡（2026 现状可述，待核实最新数字）。

## 2. 关键数字/机制

- 全球完整表（DFZ）~90+ 万条前缀（2024-25 量级，待核实当前值）——FIB 规模与 TCAM 之争（第 13/14 讲）的现实压力。
- 会聚：withdraw 比 announce 传播快（路径属性比较不对称）——"黑洞 30 分钟"类故障的成因。
- BMP（BGP Monitoring Protocol, RFC 7854）：向采集器实时上报 RIB 变化，运营商可观测性基建。

## 3. 层次间与前后讲联系

- BGP 决定 AS 间出口（NEXT_HOP 可达性靠域内 IGP+static 补齐，"BGP/IGP 解耦"）；出口选择影响第 12 讲流量分布与第 16 讲 SPF。
- 第 6 讲 CDN 用 Anycast+BGP 前缀宣告（"任播即路由声明"）；SDN（第 19 讲）在数据中心用 BGP 作为"可扩展控制协议"重新流行（RFC 7938 线）。

## 4. 跨课程联系

- **CS168**：BGP 是其核心章——测量、路由安全、RPKI/ROV 全部展开；若读完本课再读 CS168 BGP 章会无缝。
- **MIT6.824**：BGP 的"分布式 best-path 计算+策略剪枝"与 MapReduce 的调度约束问题同形；Gao-Rexford 收敛证明可类比 Raft 安全性论证的"经济学版本"。
- **CS162/CS144**：CS162 用 BGP 讲"middlebox 与地址政治"；CS144 无涉（超出其范围）。
- **6.S081**：无内核对应，但 `ss -tn 'dport = 179'` 看 BGP 会话即是 TCP 长连接范本（第 11 讲 keepalive）。
- **topdown_ustc**：郑烇老师讲 BGP 用"村-镇-县"类比 AS 层次，中文语境好记。

## 5. 开源项目应用

- **FRRouting**：`bgpd` 是事实标准（属性编解码、决策、RR）；`bfdd` 配毫秒级故障检测。
- **GoBGP（osrg）**：Python/Go API 友好的实验平台，写"策略即代码"教程常见。
- **BIRD**：轻量，Linux 发行版常见默认路由守护进程。
- **RIPE RIS / RouteViews + pyroute**：公共 BGP 流数据（histories），做劫持检测实验的原料；`bgpmon`。
- **Wireshark**：BGP 报文 dissect（parse OPEN/UPDATE）；`bgpdump` 转换归档。

## 6. 延伸阅读

- RFC 4271（BGP-4）、RFC 4456（RR）、RFC 5065（AS 分配与多宿主）、RFC 6483/6487（RPKI 框架与验证）、RFC 7938（USE BGP 数据中心架构）、RFC 7854（BMP）
- Gao & Rexford《Stable Internet Routing Without Global Routing Policies》(ToN 2001, papers.md)
- 官网 §5.2 + CAIDA 路由劫持案例新闻（2008 YouTube/Rostelecom、2018 Amazon BGP 盗币）

## 7. 自查问题

1. 为什么 eBGP 默认 TTL=1？攻击者如何伪造 BGP 会话（TCP 序列爆破/MD5）？
2. iBGP 全网格为什么不可扩展？RR 的 client/non-client 转发规则两条是什么？
3. 客户 AS 收到来自"另一客户"的前缀该不该传 provider？（Gao-Rexford 规则推演）
4. MED 属性跨 AS 生效吗（只在相邻 AS 比较）？COMMUNITY 如何承载导出策略？
5. RPKI 验证的三种状态（valid/invalid/not-found）在路由器上分别怎么处置？

## 8. 本讲一句话

BGP 是"经济协议"：安全靠关系（客户/对等）、防环靠路径、扩展靠反射与聚合——它教会我们：路由正确性常常是治理问题，不是算法问题。
