# 第 8 讲 · 视频流（DASH）与文件分发（BitTorrent、CDN）

> 章节：Chapter 2 §2.5、§2.6
> 中文对照：topdown_ustc 第 2 章（流媒体与 P2P）

## 1. 核心概念

- **流媒体两大难题**：异构接入带宽 + 长内容传输。解法分层：
  - **HTTP 渐进式下载**：把文件切片，客户端边下边播（起始延迟小、缓冲吸收波动）。
  - **DASH（动态自适应流）**：服务器提供**同一内容的多码率版本**切段（segment 几秒~几十秒），客户端按带宽/缓冲水位**逐段切换码率**——自适应逻辑全在客户端，HTTP 服务器无需特殊支持。
- **HTTP 流式 vs 实时流式**：教材强调"现代视频用 TCP/HTTP 栈"（Nagle、ARQ、拥塞控制参与）——这正是第 12 讲 QUIC 与低延迟媒体（LL-HLS/LL-DASH、WebRTC）要突破的：TCP 重传队头阻塞 vs UDP 实时性。
- **分发网络（CDN）**：pull（边缘缓存，回源）/ push（全量预置边缘）混合；请求重定向（HTTP 302/DNS GSLB）决定去哪个 POP；与第 6 讲 TTL/Anycast 组合。
- **BitTorrent（P2P 案例，公式必背）**：
  - tracker 返回"有内容的邻居"；每个 peer 维护 wanted 集合，**rarest-first** 选择 piece；**tit-for-tat**（以 20s 周期用 4-upload/1-download choke/unchoke 激励互惠）。
  - 下载时间估算：`L·s/Rmax + max{Tc, Ts}` 模型——联系第 1 讲 P2P 自扩展公式：peer 数增加时服务器上行不再是瓶颈。
  - 现代演化：DHT（去 tracker）、webseed、协议加密。

## 2. 关键机制/字段

- DASH MPD（manifest）清单：Period/AdaptationSet/Representation（码率、分辨率、BaseURL/SegmentTemplate）；客户端算法（速率估计+缓冲阈值）是事实上的"拥塞控制外围层"。
- HLS 是其苹果变体（m3u8 playlist + TS/fMP4 段）。
- BitTorrent 报文字典化编码（bencode）：`handshake、keep-alive、have(bitfield)、request(piecing)、piece、choke/unchoke`。

## 3. 层次间与前后讲联系

- 本讲把第 4 讲"需求矩阵"实例化：视频 = 弹性带宽+可靠（TCP 可接受）；直播 = 低延迟优先 → 倾向 UDP/QUIC。
- 向下游依赖：TCP 吞吐收敛速度（第 12 讲）直接决定 DASH 起播体验；QUIC 的 per-stream 恢复（第 12 讲演进段）改善多码率并行下载。
- CDN 是"第 5 讲 HTTP + 第 6 讲 DNS + 第 16-18 讲路由"的交汇产品。

## 4. 跨课程联系

- **MIT6.824**：BitTorrent 常被用作"无中心协调的分布式系统"对照案例（对比 Raft 的强一致：BT 用冗余+最终收敛）。
- **CS144**：其 congestion control 实验解释"DASH 码率选择实为应用层对 TCP 吞吐的跟随"。
- **CS168**：CDN 与视频网络是其重点专题（测量视角：边缘命中率、P95 带宽）。
- **CSAPP**：BT 客户端实现就是第 7 讲 socket + 多线程的经典课程作业。
- **topdown_ustc**：BT 的 tit-for-tat 动画讲解。

## 5. 开源项目应用

- **Nginx + ngx_http_mp4_module / dash-nginx-module**：字节范围请求（`Range:` 头，第 5 讲）支撑渐进式下载。
- **SRS / media-server（ZLMediaKit）/ nginx-rtmp**：直播协议栈（RTMP 入、HLS/DASH 出）。
- **WebRTC (libwebrtc / Pion Go)**：UDP+SRTP 实时栈，"应用层自建可靠"的代表（对照第 10 讲 rdt）。
- **qBittorrent / libtorrent**：BT 协议活文档，源码读 choke 算法。
- **Varnish/Envoy**：CDN 边缘缓存与回源策略。

## 6. 延伸阅读

- RFC 8499（DASH 协议 5. 版：MPD/Segment）、RFC 7234（HTTP 缓存）
- Cohen《Incentives Build Robustness in BitTorrent》(2003, papers.md 经典表)
- LL-HLS / Low-latency DASH 规范摘要（CMAF Chunked Transfer，年份 2020+ 待核实具体条目）
- 官网 §2.5/§2.6 与 interactive quiz

## 7. 自查问题

1. DASH 客户端何时升/降码率？缓冲水位如何参与决策？
2. Range 请求如何让"一个 HTTP 对象并行多连接"安全？
3. BT 的 rarest-first 为什么优于随机？对整群完成时间的影响？
4. tit-for-tat 对自由骑手（free-rider）与吸血节点如何防御？
5. CDN pull 模式下冷启动（cache miss 风暴）如何缓解？

## 8. 本讲一句话

内容分发的一切技巧，都是在"服务器→CDN→P2P"三级成本曲线上，用客户端智能（自适应/选择邻居）换可扩展性。
