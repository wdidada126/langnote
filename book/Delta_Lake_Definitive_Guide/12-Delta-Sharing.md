# 第 14 章 Delta Sharing：跨组织的数据共享协议

> 原书第 14 章「Using Delta Sharing」收尾全书：把治理过的 Delta 表**不搬数据地**交给组织外消费者。
> 本文件按「协议模型 → 服务端形态 → 客户端体验 → 边界与代价」展开。
> 命令/配置为**自拟教学示意，非书中原文**；口径参照 sharing.delta.io（Delta Sharing 协议文档）。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 14.1 共享的四难 | 复制/直挂桶/管道重建/联邦查询都不行 | 需要一个「带权限的按需清单」协议 |
| 14.2 开放协议模型 | share→recipient→表清单 + REST 动作 | 数据不动，元数据按需签发票 |
| 14.3 服务端谱系 | Databricks 共享市场 vs Open Sharing Server | 同一协议两种实现 |
| 14.4 客户端体验 | Databricks 一跳挂载 vs 开源四语言客户端 | Arrow 流是通用出口 |
| 14.5 共享对象扩展 | 表之外：视图/模型/文件（🔧 演进中） | 「数据产品」的载体 |
| 14.6 边界与代价 | 读带宽、预签名过期、CDC 语义缺失 | 共享不是同步 |

## 核心精讲

### 14.1 为什么「老办法」都不成立

| 办法 | 致命伤 |
| --- | --- |
| 拷一份数据给对方 | 存储/传输成本 ×N，版本漂移，泄露面 ×N |
| 给对方云桶 IAM 直读 | 桶级授权过宽（连历史文件一起给）、无审计、格式方言各解 |
| 为对方建一条管道 | 每新增一个消费者重做一遍 ETL |
| 联邦查询（如 JDBC 暴露） | 扫描/权限/计费模型不匹配分析级负载 |

Delta Sharing 的答案：**provider 侧控制「表快照清单 + 文件级预签名 URL」的下发**，
consumer 侧拿到的仍是 Delta 的事务语义（版本、分区裁剪），但**只有被 share 的版本可见**。

### 14.2 协议模型（对象与动作）

```text
对象：Share（一组表 + 各自的历史保留策略）→ Recipient（外部组织身份，token 认证）
动作（REST，教学示意口径以 sharing.delta.io 为准）：
  ① profile：recipient 的入口配置（endpoint + 凭证）
  ② list shares / list tables / query table：拿到表的版本与元数据 URL
  ③ load access configuration：取预签名存储 URL（限时）
  ④ 消费者按预签名直接读对象存储上的 parquet —— 数据平面不过 provider 计算
```

- 关键性质：**只读共享**（写回不在 v1 范围）；**表级/分区级权限**（share 可以按分区过滤行）；
  **历史可控**（share 可限定只暴露最新版本或 N 天历史，防止「白送全库时间旅行」）。
- consumer 读到的仍是合法 Delta 快照——commit 经 provider 过滤后重新下发，
  被共享范围外的文件 URL 根本不会出现在清单里。安全边界在**清单生成**这一步，值得反复体会。

### 14.3 服务端谱系

| 形态 | 适用 | 特点 |
| --- | --- | --- |
| Databricks 共享（UC 注册 share） | provider 已在 Databricks | 与第 11 章文件的 UC 治理无缝：ACL/审计/血缘沿用 |
| Open Sharing Server | 自建、SaaS 厂商想暴露数据 | 无 Databricks 依赖；读本地/HDFS/云存储上的 Delta 表对外服务 |
| 兼容服务（云市场类） | 交易所/数据商城 | 协议同构，计费与发现层私有 |

### 14.4 客户端体验

```python
# 教学示意：开源 Python 客户端
from delta_sharing.reader import DeltaSharingReader
from pyspark.sql import SparkSession
df = DeltaSharingReader.load("customer_share.table.orders", profile_file="profile.share.json")
```

- Databricks→Databricks：**一行 SQL 创建外部 catalog**（`CREATE EXTERNAL CATALOG ... USING DELTA SHARING`），
  共享表像本表一样三段式引用——「one-hop sharing」的卖点。
- 非 Databricks：官方开源客户端覆盖 **Spark / pandas / Polars / Delta Sharing Rest**（以及
  Power BI/Tableau 连接器生态），数据以 **Apache Arrow stream** 交付，
  与第 5 章文件的 delta-rs/Kernel 同属「协议生态出口」。

### 14.5 共享对象扩展（🔧 演进线）

- 2022：仅 Delta 表；2023–2025：视图（含参数化视图=「数据 API」）、
  非表文件、ML 模型（feature-store/模型注册联动）逐步进入协议草案与实现。
- 阅读姿势：书稿描述的是早期「表为中心」协议；核对当前能力以 sharing.delta.io 协议版本表为准。

### 14.6 边界与代价（谈单前必须说清的三条）

1. **性能 = 跨云读对象存储**：预签名 URL 直读意味着 provider 的存储出口带宽决定消费者体验；
   大表跨地域共享要么 CDN/镜像策略，要么接受延迟。
2. **新鲜度是拉取语义**：消费者重查才见新版本；要「变更推送」仍需 CDF/Kafka 层（第 10 章文件），
   Delta Sharing 不解决事件流。
3. **权限模型粗于 UC**：share 级/表级/分区级，但行过滤函数、列掩码这类动态策略在协议早期不支持
   （对方拿到的就是明面文件），敏感列请物化脱敏后再入 share。
4. **历史是双刃剑**：share 暴露 N 天历史时，VACUUM 保留期必须 ≥ N（第 4 章文件 5.3），
   否则消费者按旧快照解析到的文件已被清掉，得到的是坏清单而非「旧但完整」的快照。

一条判定线：**内部靠第 11 章文件的治理，外部靠本章的裁剪式清单**——
同一张 gold 表，内部走 UC ACL 全功能，外部走 share 只读子集，两套视图互不干扰。
设计数据产品时先画这条内外分界，再决定脱敏/聚合的落点。

## 版本演进

| 时间 | 事件 |
| --- | --- |
| 2021-06 | Databricks 发布 Delta Sharing，并开放协议规范 |
| 2021–2023 | Open Sharing Server、四语言开源客户端、各数据商城接入 |
| 🔧 2023–2025 | 非表共享对象（视图/文件/模型）协议扩展；生态连接器扩展 |

## 文献与文档

- sharing.delta.io：协议规范、参考实现、profile 格式（本章一切口径的最终出处）。
- Databricks docs *Delta Sharing*（one-hop 外部 catalog 语法）。
- delta-io/delta-sharing GitHub（server/client 代码）。
- 对照：Iceberg REST catalog 的「共享」思路、Snowflake Network Shares——同为「元数据下发+数据直读」流派的私有协议版。

## 常见误区

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「共享 = 对方能改我的表」 | v1 只读；写回/协作是另一类协议能力 |
| 2 | 「share 出去就失控」 | 版本/分区/历史范围都在清单生成时裁剪；收回 = 删 recipient |
| 3 | 「有 Delta Sharing 就不用数据管道」 | 它是「授权读」不是「持续同步」；新鲜度与变换逻辑仍归管道 |
| 4 | 「跨云共享和内部一样快」 | 出口带宽与预签名时效决定体验（14.6） |
| 5 | 🔧 「共享对象仍只有表」 | 协议已扩到视图/文件/模型，核对版本表再设计数据产品 |

## 与其他章 / 其他书的联系

- ← `11`：share 的注册与审计长在 UC 上；← `08`：gold 层是天然的共享出口。
- ← `03`：delta-rs/Kernel 与共享客户端共享同一套协议解析肌肉。
- → [../bigdata/09-存储与文件格式.md](../bigdata/09-存储与文件格式.md)：预签名直读的对象存储前提。
- → 《Engineering Lakehouses with Open Table Formats》精读：**待建**（跨组织共享格式的对照章建成后再链）。
