# UCB CS168 — Introduction to the Internet（互联网导论）

## 课程信息

| 项目 | 内容 |
| --- | --- |
| 全称 | Introduction to the Internet: Architecture and Protocols |
| 学校 | UC Berkeley（加州大学伯克利分校） |
| 主讲 | UCB 网络方向教学团队（SP2025 期以课程主页公布为准） |
| 教材 | 课程配套开源教材 https://textbook.cs168.io/ （csdiy 评价：内容全面、简洁生动，可当手册查阅） |
| csdiy 路径 | 计算机网络/CS168 |
| 最新期次 | SP2025 |
| 状态 | 骨架（notes / papers / projects 待后续填充） |

## 为什么学

- 这是伯克利的「互联网架构与协议概论」，侧重 **Internet 的设计原则与核心协议**：分层结构、寻址机制、域内/域间路由、可靠传输、拥塞控制，以及 TCP、UDP、IP、DNS、HTTP 等，并覆盖以太网、无线等技术。
- 理论与实践结合：三个动手项目（Traceroute、路由、TCP 传输）让你亲手构建并调试网络协议，体验深入且全面。
- 配套教材质量极高，是 csdiy 特别推荐的「可当手册」的教材。
- 定位为「导论 + 架构视角」，与 Stanford CS144（工程实现视角）、自顶向下（教材体系视角）互补。

## 先修与知识联系

- 先修要求：CS61B；推荐 CS61C；具备基础 Python 编程与 Unix 使用经验。
- 语言：Python + Unix shell；难度 🌟🌟🌟；预计学时约 140 小时（14 周 × 10 小时/周）。
- 知识联系：上承 CS61C（系统基础），横向与 CS144 互为印证（CS144 提供 C++ 全栈实现），后续可衔接 6.824/CS168 进阶网络方向（SDN、数据中心网络论文）。

## 讲义章节目录（SP2025，14 周）

> 注：官方课程仓库/日程每期更新，本表按课程配套教材的 part 结构（Introduction / Routing / Transport / Applications / End-to-End / Datacenters / Beyond Client-Server / Wireless）整理的骨架，具体周次以官方 schedule 为准。

| 讲次 | 标题 | 阅读材料 |
| --- | --- | --- |
| L01 | 课程导论：互联网的端到端图景与设计原则 | Textbook Part I Introduction |
| L02 | 网络边缘与接入网、链路层：以太网 | Textbook Part I Introduction |
| L03 | 网络层寻址：IP/IPv6、NAT 与地址体系 | Textbook Part I–II 衔接章节 |
| L04 | 域内路由：距离向量 vs 链路状态（RIP/OSPF） | Textbook Part II Routing |
| L05 | 域间路由：BGP 与商业策略、路由扩展性 | Textbook Part II Routing |
| L06 | 路由实践与项目周（Project 2：路由） | Textbook Part II Routing |
| L07 | 传输层：UDP 与复用/解复用 | Textbook Part III Transport |
| L08 | TCP：连接管理与可靠传输机制 | Textbook Part III Transport |
| L09 | TCP 拥塞控制：从 AIMD 到 CUBIC/BBR | Textbook Part III Transport |
| L10 | 应用层：DNS 与内容分发 | Textbook Part IV Applications |
| L11 | 应用层：HTTP 与现代 Web 传输 | Textbook Part IV Applications |
| L12 | 端到端论据与网络安全（TLS） | Textbook Part V End-to-End |
| L13 | 数据中心网络 | Textbook Part VI Datacenters |
| L14 | 无线与移动网络、Beyond Client-Server（P2P/命名数据）与总结 | Textbook Part VII–VIII |

## 资源

- 课程网站：SP2025（见 csdiy 页面链接）；教材：https://textbook.cs168.io/
- 作业：3 个 Python Projects（Traceroute / Routing / TCP），相对简单
- 资源汇总：PKUFlyingPig/UCB-CS168（GitHub，含全部资源与作业实现）
