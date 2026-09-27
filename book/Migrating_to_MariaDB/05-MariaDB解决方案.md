# 05 · MariaDB Solution（MariaDB 解决方案）

> 原书第 5 章，pp. 59–71（页码 ✅ Springer 章页实抓）。
> 精读重构：骨架取自该章官方摘要（✅）；部署拓扑事实取 MariaDB 官方文档（✅ 可达页 + ⚠️ 转述混合）；
> **🔧 D 组联邦类比在本章 5.4 节**（SQLite/DuckDB 行为，非 MariaDB）。

## 5.1 官方摘要：两步走拓扑——KISS PoC，然后才 HA

摘要关键句逐拆（✅）：

- "keeping with the **KISS principle**, the team chose to stand up a **stand-alone environment
  with replication**" —— PoC 基线=单机+异步复制，不是集群；
- "Using this as the basis for their **proof of concept work** … get an active MariaDB
  environment deployed **quickly and easily**" —— PoC 的目标函数是"快+验证既有判断"，
  不是压测；
- "Once the proof of concept was complete, the team then went on to deploy a **much more robust
  high availability solution**" —— 书里明确 HA 是 PoC 之后的**第二次部署**（摘要未给 HA 细节 ⚠️，
  Galera 为最可能落点：MariaDB 官方打包的同步多主方案，见 5.3）；
- "to get them familiar with the database solution by enabling them to **rapidly deploy and then
  extend their MariaDB footprint**" —— 本章真实主题：**用部署节奏换团队手感**。

## 5.2 PoC 拓扑（pp.59–71 的合理重构 ⚠️ + 官方件取证）

```
[Oracle 现网] --抽取--> [MariaDB 主] --binlog 复制--> [MariaDB 从]
                          └─ 应用只读流量灰度到从库（复制延迟即验收指标）
```

- 复制机制与 MySQL 同源（handler/binlog 世界），机制底图对位：
  [../Understanding_MySQL_Internals/12-复制.md](../Understanding_MySQL_Internals/12-复制.md)、
  [../mysql/12-基于成本的优化.md](../mysql/12-基于成本的优化.md)（从库硬件选型语境）；
- 复制延迟的度量语言直接借 #45：
  [../Efficient_MySQL_Performance/07-复制延迟.md](../Efficient_MySQL_Performance/07-复制延迟.md)——
  PoC 验收表上"延迟 P99"一行就该从彼册的Seconds_Behind指标体系里长出来 ⚠️ 方法移植；
- 官方安装/升级文档：kb "Getting, Installing, and Upgrading MariaDB"（✅ 200 可达；内容 JS 渲染 ⚠️ 句级未抓）。

## 5.3 HA 阶段：Galera 一步的取证与风险登记（✅/⚠️）

书内 HA 细节未放出（两级目录在墙内），本目录按 MariaDB 官方件给对位事实：

- **Galera 是 MariaDB 侧打包的多主同步复制**（✅ 兼容性页原话："Oracle's group replication
  conflicts with MariaDB's Galera architecture"——官方亲自承认与 MySQL MGR 是两套架构）；
- kb 页 mariadb-galera-cluster / about-mariadb-maxscale 均 ✅ 200 可达（JS 渲染，句级 ⚠️）；
- 风险登记（承 Ch.2 方法 ⚠️）：多主写冲突、wsrep 证书/流量隔离、DDL 风暴、从 Oracle RAC
  心智搬过来的误用——"Reactive DBA 团队"（Ch.6 点名 ✅）直接上 Galera 是最典型的技术冒进，
  作者先 PoC 后 HA 的章序正是对此的防呆 ⚠️ 推断；
- **本册给 2026 读者的替换读法**：当年"HA=Galera 三节点"的位置，今天同预算下还有
  主从+自动故障转移（MaxScale/Orchestrator 系）与托管云选项——拓扑选择属于每代重算的工程题 ⚠️。

## 5.4 🔧 D 组：多引擎/联邦——为什么"存储引擎"在 MariaDB 选型里是一等公民

**被类比对象（✅ 官方兼容性页原话）**："MariaDB bundles specialized modules like Spider, Aria,
and HandlerSocket"；"MySQL supports multiple storage engines, but its development efforts are
heavily focused on InnoDB"（mariadb-vs-mysql 页实抓）。kb 单引擎页（aria / connect / spider /
columnstore / storage-engines）✅ 全部 200 可达（句级内容 JS 渲染 ⚠️）。

MariaDB 本机不可装（00 第五节实测备案），用 DuckDB 1.5.5 演示**联邦引擎的行为学**（非 MariaDB 行为）：

```sql
-- 本地 DuckDB 表 + ATTACH 一个真 SQLite 文件（2 行）为"远端引擎"
ATTACH 'D:/develops/tmp/dbwave_w5_mariadb/demo.sqlite' AS sx (TYPE SQLITE);
CREATE TABLE local_t(id INTEGER, note VARCHAR);
INSERT INTO local_t VALUES (1,'local-duckdb');

SELECT s.id, s.v, l.note FROM sx.remote_x s LEFT JOIN local_t l USING(id);
-- => [(1,'from-sqlite','local-duckdb'), (2,'row2',None)]
SELECT count(*) FROM sx.remote_x;   -- => 2   （SQLite 引擎）
SELECT count(*) FROM local_t;       -- => 1   （DuckDB 引擎）
SELECT v, count(*) FROM sx.remote_x GROUP BY v;  -- 远端聚合下推 => 各 1
```

**读法三则**：① 同一会话里两种引擎并存、行数各算各的——对位 MariaDB 每表可选 ENGINE 的心智；
② 联邦表的能力边界（这里靠下推、MariaDB Spider 靠远端 SQL 方言 ⚠️）决定优化器可见性——
迁移验收要按引擎分别跑执行计划；③ 跨引擎没有统一事务/统一统计，**"多引擎是资产还是负债"
取决于你的运维是否按引擎分域**——这正是 Ch.6 标准化主题的伏笔 ⚠️。

## 5.5 引擎家族速览表（✅ 可达 kb 页 + ⚠️ 通识，供未读 MariaDB 者建立名词表）

| 引擎 | 一句话定位 | 取证 |
| --- | --- | --- |
| InnoDB/XtraDB | 默认事务引擎（分叉两侧同源底图见 ../mysql/ 目录版） | ⚠️ + [../mysql/01-InnoDB与MySQL的架构.md](../mysql/01-InnoDB与MySQL的架构.md) |
| Aria | 崩溃安全 MyISAM 替代，读密集/内部临时表 | ✅ kb/aria 可达 200（⚠️ 句级） |
| Spider | 分片/联邦表（MySQL 协议远端） | ✅ kb/spider 可达 200（⚠️ 句级） |
| CONNECT | 异构数据源表（CSV/ORC/JDBC…） | ✅ kb/connect 可达 200（⚠️ 句级） |
| ColumnStore | 列存分析引擎 | ✅ kb/columnstore 可达 200（⚠️ 句级） |
| Sequence | 03 章 §3.4 的主角，序列对象的后端 | ✅ docs 序列页实抓 |

对位盘上原创册：《MariaDB原理与实现》第 2.1 节"更多的存储引擎/全新的 Aria"（✅ 盘上目录实读）
与本表互证——**国内原创册 2015 年就把引擎多样性列为 MariaDB 头牌特性，本书 2019 年把它
放进取决于团队的"解决方案"章**，两册时间差 4 年，特性面几乎没漂移，这是选型写作的好素材 ⚠️ 评论。

## 5.6 本章检查清单（重构提炼 ⚠️）

1. PoC 是否刻意"薄"（单机+复制，不带 HA 复杂度）——厚 PoC 是项目拖延的常见形态；
2. 复制延迟验收指标是否引用了独立度量体系（#45 对位）而非拍脑袋；
3. HA 决策是否与团队成熟度挂钩（Ch.6 的前置证据）；
4. 引擎选择是否建了"分域登记表"（哪个业务域允许哪些 ENGINE=）；
5. 快速部署路径是否文档化（"rapidly deploy and then extend" ✅ 摘要原话的执行版）。

## 核心概念速览（中英对照）

- **KISS 原则** — Keep It Simple：PoC 拓扑的第一设计约束（✅ 摘要点名）
- **概念验证** — PoC (Proof of Concept)：以"快+验证判断"为目标的最小部署（✅ 摘要点名）
- **高可用方案** — HA Solution：PoC 后第二部署；官方语境 Galera vs MGR 两套架构（✅）
- **Galera 集群** — Galera Cluster：MariaDB 打包的同步多主复制（✅ 兼容性页点名）
- **MaxScale** — MaxScale：官方代理层，故障转移/读写分离（✅ kb 可达 ⚠️ 句级）
- **可插拔引擎** — Pluggable Storage Engines：Spider/Aria/HandlerSocket 捆绑（✅ 官方原话）
- **联邦查询** — Federated Query：跨引擎/跨实例联表（🔧D 以 DuckDB ATTACH 演示）
- **下推** — Pushdown：聚合等算子交给远端引擎执行（🔧D 实测项）
- **引擎分域** — Engine Zoning：按业务域圈定可用 ENGINE 的标准化动作（5.4 读法③ ⚠️）
- **部署节奏换手感** — Deploy-Driven Learning：本章摘要末句的方法论直译 ⚠️

## 最新演进与工业实践

- **拓扑选项 2026**：Galera/主从自动切换/MariaDB 托管云三线并存；社区版节奏上 11.4/11.8 LTS
  是当前部署主流锚点（✅ mariadb.org 维护表实抓，10.6 于 2026-07-06 出保，存量 PoC 话术应更新）；
- **引擎面的收缩与专注**：HandlerSocket 等早期捆绑件的当代维护状态不一 ⚠️（本目录仅登记
  兼容性页 2026 仍列其名 ✅，不推断存活度）；ColumnStore 在 MariaDB 云战略中位置上升（⚠️ 转述）；
- **MaxScale 的再定位**：从"读写分离代理"扩展到 K8s Operator/企业平台组件（✅ mariadb.com 导航
  实抓中现 "Enterprise Kubernetes Operator" 条目），本章 5.3 的"当年替换读法"在 2026 已成默认选项之一；
- **同题对位**：多引擎话题的机制层讨论在 repo 内有更深的锚——
  [../Understanding_MySQL_Internals/10-存储引擎掠影.md](../Understanding_MySQL_Internals/10-存储引擎掠影.md)
  （2003 年 handler 世界）——读 5.5 表后回看，能直观感受"引擎多样性"二十年叙事的变化与不变。
