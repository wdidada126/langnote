# 第 6 讲 · DNS：名字空间、服务器层次与攻击面

> 章节：Chapter 2 §2.3
> 中文对照：topdown_ustc 第 2 章（DNS）；配套项目 projects/ch2_dns_query

## 1. 核心概念

- **DNS 是分布式分层数据库**（名字→资源记录），同时是应用层协议（UDP 53 为主，区域传输走 TCP）。三大角色：客户端（resolver）、层级名字服务器（root → TLD → authoritative）、以及中间的本地名字服务器（ISP/企业递归器，"代理+缓存"）。
- **查询模式**：递归查询（客户端→本地：把答案办到底）与迭代查询（本地→root/TLD/授权：每次问"下一步找谁"，靠 referral 引路）。默认路径：主机→本地（递归）→ 三层（迭代）。
- **资源记录（RR）四元组**：`(name, value, type, TTL)`：
  - A：名字→IPv4；AAAA：→IPv6；NS：该域权威服务器（用于 referral）；CNAME：规范名（别名链，CDN 常用）；MX：邮件。
- **服务器层次**：13 组 root（任播后实际数千实例）、gTLD（.com/.org）与 ccTLD（.cn）、机构授权服务器。`dig trace`/`nslookup` 可复现全过程。
- **TTL 是 DNS 一切行为的调节旋钮**：缓存时间、故障切换速度（低 TTL ≈ 快速 GSLB 切换，CDN 命脉）、DDoS 放大窗口。
- **负载均衡与 GSLB**：权威服务器对不同来源返回不同 A 记录（地理/DNS 轮询/Anycast 三派，CDN 第 8 讲）。

## 2. 关键协议字段（DNS 报文，全二进制，对比 HTTP 文本风格）

- 头部：`ID(16b) | Flags: QR, Opcode, AA, TC, RD, RA, RCODE | QCOUNT/ANCOUNT/NSCOUNT/ARCOUNT`。
- 问题段：QNAME、QTYPE、QCLASS。
- 回答段可能是**压缩指针**（0xC0 开头，偏移指向之前的名字）——手工解析器最容易踩的坑（本项目 ch2_dns_query 专门处理）。
- TC=1 表示需改用 TCP 重试（响应超 512B，DNS over UDP 时代）。

## 3. 层次间与前后讲联系

- 第 5 讲 HTTP 的 `Host:` 头进入本讲：URL→IP 的转换发生在 TCP 握手**之前**；"一天"时间线里 DNS 常贡献 1~2 个 RTT（浏览器预解析/预连接的动机）。
- 传输层视角：DNS 用 UDP 追求快，可靠性由应用层重试兜底——第 10 讲 rdt 原则的现场应用；区域传输/大响应用 TCP（第 11 讲连接管理）。
- 封装栈：DNS 报文→UDP 段→IP→链路帧，是观察三层封装最干净的抓包样本。

## 4. 跨课程联系

- **CSAPP**：`getaddrinfo` 即 libc 里的完整 DNS 客户端（还含 hosts/缓存），本项目用它对比手工解析。
- **MIT6.824**：DNS 是"读多写少、容忍短暂陈旧"的分布式 KV 经典案例，与 6.824 的缓存一致性讨论同构；其分层+复制也常作 MapReduce/ Raft 讲解时的反面（DNS 不做强一致）。
- **CS144/CS162**：`nslookup` 抓包看 UDP 解复用（第 9 讲）；CS162 用 DNS 讲 Anycast 路由耦合（第 18 讲 BGP）。
- **topdown_ustc**：郑烇老师把 referral 过程画成"问路三连"，记忆负担小。

## 5. 开源项目应用

- **BIND 9 / Unbound / Knot**：权威/递归参考实现；`dig +trace` 是官方推荐实验。
- **Wireshark**：DNS lab（官网官方），看压缩指针与 referral 链。
- **AdGuard Home / Pi-hole / mosdns**：本地递归器+黑名单——把"递归器"变成产品。
- **CoreDNS**：Kubernetes 集群 DNS，服务发现与 K8s Service 记录联动，生产级案例。
- **getaddrinfo/musl**：libc 侧实现，NSSwitch（`/etc/nsswitch.conf`）决定 hosts/DNS 顺序。

## 6. 延伸阅读

- RFC 1034/1035（DNS 核心）、RFC 7871（EDNS0——扩展 UDP 尺寸）、RFC 8484（DNS over HTTPS）、RFC 9460（DoQ 用 QUIC 承载 DNS）、RFC 9077（缓存投毒反应）
- DNSSEC 链（RFC 4033/4034/4035）——从信任根到 RR 签名
- 《You Can't Spell DNSSEC as DNSSec》等运维经验帖（可选）

## 7. 自查问题

1. 本地未命中缓存时，`www.example.com` 解析经过几个查询？每步问谁？
2. NS 记录与 glue record（附加段 A）分别解决什么问题？
3. 为什么压缩指针存在？解析时如何正确处理 0xC0 偏移？
4. TTL=30s 与 TTL=1d 对故障切换与放大攻击各意味着什么？
5. DNS 劫持 vs 投毒 vs DDoS 反射：三者的攻击面分别在哪一段（见下）。

## 8. 攻击面小结与本讲一句话

- 放大反射（查询小响应大，source spoof）；投毒（ID 爆破+端口随机化不足）；域名劫持（注册商/授权层）；缓存副作用（共享递归器上的串扰）。
- 一句话：DNS 用"分层引路+全局缓存"换来极致的读性能，代价是一致性弱、安全靠后续补丁（DNSSEC/DoH/DoQ）。
