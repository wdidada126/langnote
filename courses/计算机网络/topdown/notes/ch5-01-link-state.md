# 第 16 讲 · 链路状态路由算法：Dijkstra 与 LS 实践（OSPF/BGP/SPF）

> 章节：Chapter 5 §5.1（链路状态部分）
> 中文对照：topdown_ustc 第 5 章（链路状态）；配套项目 projects/ch4_router_sim（Dijkstra 实现）

## 1. 核心概念

- **控制平面两大流派（全章坐标系）**：集中式（SDN，第 19 讲）vs 分布式（路由协议）。分布式再分：链路状态（LS，全局地图各算各的）与距离向量（DV，听邻居吹牛，第 17 讲）。
- **LS 算法三要素**：
  1. **拓扑发现**：Hello 包找邻居、CSNP/DBD 同步链路状态数据库（LSDB）、LLS/MD5/TLS 认证邻居。
  2. **泛洪**：每个节点生成 LSP（v2）/LSA（v3，OSPF）描述"我的边+代价"，可靠泛洪（序号+确认，类似第 10 讲 ARQ）；泛洪范围决定"域"。
  3. **计算**：以自己为根跑 **Dijkstra（SPF）**——`O(E + V log V)`（二叉堆）。
- **Dijkstra 伪码（默写级）**：`N={源}, D[v]=∞(邻居=cost), 重复: w=argmin D∉N; 对每个邻居 v: D[v]=min(D[v], D[w]+c(w,v))`；路径回溯用 parent 表。
- **工程细节**：
  - **等价多路径 ECMP**：等代价下一跳全入 FIB（第 13 讲哈希负载分担）。
  - **防抖**：LSP 泛洪风暴会反复触发 SPF——SPF 延迟/最大次数退避（OSPF 的 `spf-interval`）。
  - **拓扑感知代价**：OSPF 的 cost=参考带宽/接口带宽；TE 扩展（OSPF-TE, RFC 3630）把带宽/色度编进 LSA 供 CSPF 选路（MPLS-TE 的地图）。
  - **泛洪域设计**：OSPF 区域（第 19 讲）、IS-IS level、SDN 的"一控制器一域"都是为控制 LSDB 规模。

## 2. 与 DV 对比表（考试标配）

| 维度 | LS | DV |
| --- | --- | --- |
| 信息量 | 全局拓扑 | 邻居向量 |
| 收敛 | 泛洪+SPF，快（退避可调） | 迭代交换，慢，计数到无穷风险 |
| 度量灵活性 | 难（边权独立，最优子结构成立） | 易任意度量（无环性靠机制保证） |
| 故障定位 | 需全图推理 | 各节点自洽即可 |

## 3. 层次间与前后讲联系

- LS 算出的前缀→FIB（第 14 讲）由路由信息库 RIB→FIB 下装（第 13 讲查表）；泛洪需要链路层广播（第 21 讲）与 Hello（OSPF 用组播 224.0.0.5/6，第 19 讲）。
- LS 的"全局视图"让 BGP 也采用状态+策略混合（第 19 讲用 path vector 消灭环——LS 与 DV 的中间形态）。

## 4. 跨课程联系

- **6.006/6.046（算法课）**：Dijkstra 与 Bellman-Ford 的图论对照在本讲变成协议工程；LS 泛洪=分布式快照，DV=异步 DP（联系 6.824 一致性讨论）。
- **CS144**：其 router lab 不做路由协议（数据平面视角），但 testbench 的"下一跳计算"可用本讲 Dijkstra 离线生成。
- **CS168/CS162**：IS-IS（运营商骨干）与 OSPF 同族；数据中心 Fat-Tree 的 ECMP 依赖 LS 收敛质量。
- **MIT6.824**：LSDB 泛洪是"可靠广播+版本向量"的分布式系统案例；Raft 日志复制与 LSP 序号单调递增思想呼应。
- **topdown_ustc**：Dijkstra 逐步表格演练题与本讲完全同源。

## 5. 开源项目应用

- **FRRouting/Quagga**：`ospf6d/ospfd` 的 `ospf_spf_calculate` 是生产级 Dijkstra（含区域）；读 `spf.c` 是本讲最好的第二遍教材。
- **Linux**：`ip route` 静态注入模拟 LS 结果；`tc netem` 模拟链路代价变化触发重算。
- **Containerlab+GNS3**：多路由器 OSPF 拓扑实验（邻居状态机 ExStart→Full 可视化）。
- **Wireshark**：抓 OSPF Hello/LSA（type-1 router LSA/type-3 summary）；`ospf` 显示过滤器。
- **project 对照**：projects/ch4_router_sim 里 `link_state()` 实现+扰动实验。

## 6. 延伸阅读

- RFC 2328（OSPF v2，LS 协议教科书）、RFC 5340（OSPFv3）、RFC 1131（OSPF 认证）、RFC 3630（OSPF-TE）、RFC 1195（IS-IS 集成）
- McQuillan et al.《Routing Algorithms for Packet-Switched Networks》(1980, 与第 17 讲论文同族)
- 官网 §5.1 动画 + "Dijkstra 手算 6 节点图" 习题

## 7. 自查问题

1. 给定 6 节点图手算 Dijkstra 每轮 N/D 数组（与项目 ch4 输出核对）。
2. 链路代价改大会产生瞬时环吗？LS 如何靠"全局一致视图+各自重算"避免？
3. LSP 序号为何单调+老化（maxage）？泛洪如何既可靠又终止（ack+重传，第 10 讲工具复用）？
4. cost=参考带宽/接口带宽 会让 10G 与 40G 链路同 cost 吗？如何调（auto-cost 参考值）？
5. ECMP 流内乱序问题（多路径分片重组）为何要求五元组哈希而非逐包轮询？

## 8. 本讲一句话

链路状态 = "让每人持有一张真地图后独立算最短路"：泛洪保证地图新鲜、SPF 保证最优、工程退避保证地图风暴不炸网。
