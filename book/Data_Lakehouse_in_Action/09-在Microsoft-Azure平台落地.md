# 09 · 在 Microsoft Azure 平台落地

> 目标书：《Data Lakehouse in Action》（Pradeep Menon，Packt，2022-03）。
> ⚠️ 重建声明：章界推定（见 00）；对应简介原文 "Implement Data Lakehouse in a
> cloud computing platform such as Azure"（✅ 简介原文）。
> 本章无 🔧（全为云资源组态，零新装红线不起云环境）；✅ 仅标已验证 URL，
> SKU/计费/预览状态一律 ⚠️ 并视为 2022 快照——**这是本书时效性损耗最快的一章**。

## 1. 本章地图

| 节 | 内容 | 一句话结论 |
| --- | --- | --- |
| §1 | 2022 版 Azure 湖仓积木清单 | Synapse 为伞，ADLS 为底，Spark 为力 |
| §2 | 参考拓扑：从摄入到服务一条线 | 六动词到 Azure 资源的映射表 |
| §3 | 工作区选型：专用池 vs Serverless | 把"该不该抽进仓"变成 SKU 决策 |
| §4 | 网络与安全组态基线 | 私有端点+托管 VNet 是默认答案（⚠️） |
| §5 | 环境工程：IaC/CI 与数据平台 | 管道即代码，湖仓不是手工艺术品 |
| §6 | 2026 迁移提示 | Synapse 叙事降温，Fabric 接棒的读法 |

## 2. 积木清单与映射（§1/§2）

| 湖仓职责（本书六动词） | 2022 Azure 承载 | 备注（⚠️ 转述） |
| --- | --- | --- |
| Ingest | ADF / Synapse Pipelines / Event Hub / IoT Hub | 03 章 §6 表 |
| Store | ADLS Gen2（容器/目录 = 湖根） | ✅ <https://learn.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-introduction> |
| Process | Synapse Spark 池（Delta 默认格式） | 05 章矩阵 |
| Govern | Purview 扫描登记 + HMS/内建 catalog | 06 章 §7 |
| Secure | Entra ID + RBAC/ACL + CMK | ✅ <https://learn.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-access-control> |
| Serve | Synapse Serverless SQL / Dedicated SQL / Power BI | 08 章 §2 |

```
 [源系统] → EventHub/ADF → ADLS Gen2: /bronze → Spark池(Delta) → /silver → /gold
                                             │                       │
                                  Purview 扫描登记        Serverless SQL 端点 → BI
                                             │                       │
                                  Entra/RBAC/ACL/CMK 横切      Power BI / REST
```

- ✅ Synapse 定位（分析服务伞形：数据集成+企业库+管道+多引擎+安全治理）：
  <https://learn.microsoft.com/en-us/azure/synapse-analytics/overview-what-is>。
- Databricks on Azure 平行宇宙（同六动词的另一装配单）：✅ 湖仓口径
  <https://learn.microsoft.com/en-us/azure/databricks/lakehouse/>；中文镜像
  <https://docs.azure.cn/zh-cn/databricks/lakehouse/>。本书以 Synapse 为主、
  Databricks 为辅，2026 读者注意重心已倒置（§6）。

## 3. 专用池 vs Serverless（§3，⚠️）

| 维度 | Dedicated SQL 池 | Serverless SQL 端点 |
| --- | --- | --- |
| 形态 | 预置 MPP 仓（DWU 计费） | 按需扫描量计费 |
| 数据位置 | 仓内表 | 直读 ADLS Delta/Parquet |
| 适合 | 高频看板、ETL 终段 | ad-hoc、回湖查史、轻量 ELT |
| 陷阱 | 湖仓"二传手"化——抽太多回仓等于回到旧架构 | 大扫描账单失控；需成本护栏 |

- 判读：这条"抽不抽"的分界线就是本书 §范式 的试金石——**Gold 层放仓是妥协还是
  回退，取决于查询并发与延迟证据**（08 章三件套先跑满再谈建仓）。
- 2022 后演进 ⚠️：Serverless 对 Delta 的原生读、自动索引与缓存持续增强；专用池
  产品线基本冻结（→ §6）。

## 4. 网络安全基线（§4，⚠️ 概念口径）

1. 托管虚拟网络（Synapse Managed VNet）隔离计算数据面；
2. 存储/密钥/工作区全上**私有端点**，关公网访问（07 章 §2 边界①）；
3. 出站收敛（allowlist 默认拒绝），防"合法作业偷跑公网"；
4. Synapse 工作室的"下载结果"开关按租户政策收紧（⚠️ 2022 痛点评述）。
- 本节刻意不抄门牌号式步骤——组态细节请以 §2 的 ✅ learn 总览页下的安全子树为准
  （发射环境曾验证若干 learn 深链接 404，完整清单见 00 禁引清单）。

## 5. 环境工程（§5，⚠️ 转述 + 本书立场推定）

- 数据平台的 Dev/Test/Prod 三环境 + **同一湖多容器前缀** vs 多湖：成本与隔离的权衡；
- 管道/笔记本即代码：Git 目录结构镜像作业 DAG，ARM/Bicep/Terraform 描述资源；
- 发布纪律：schema 变更走演化流程（06 §3 🔧 的教训——改名/删列在旧文件上有静默
  代价），回滚用表版本而非重灌（02 章快照语义）；
- 监控面：作业失败/新鲜度滞后/查询成本三仪表盘先行（06 §6、08 §5 的运维投影）。

## 6. 2026 迁移提示：从 Synapse 章读 Fabric 现实（§6）

- Microsoft 2023-2026 把"企业数据服务"叙事整体迁到 **Fabric/OneLake**：湖仓
  （Fabric 里的 Lakehouse 对象）+ 仓（Warehouse）+ 管道（Dataflows/Pipelines）+
  Power BI 语义层一体化 ✅（盘上 #221 目录版系统展开：
  [../Fundamentals_of_Microsoft_Fabric/00-总览与阅读地图.md](../Fundamentals_of_Microsoft_Fabric/00-总览与阅读地图.md)）。
- 本书第 9 章的读法修正：把 "Synapse 工作区" 脑内替换为 "Fabric 域工作区 +
  OneLake 湖仓对象"，六动词映射大体仍成立；**ADLS 直接落位、Spark 池手调**的
  自由度则相应收窄——托管化是 2026 的总方向。
- Databricks 线（Azure 上的第一公民地位强化）✅
  <https://learn.microsoft.com/en-us/azure/databricks/lakehouse/>。
- 波6同题参照：#210《Data Fabric as Modern Data Architecture》在盘（
  [../Data_Fabric_as_Modern_Data_Architecture/00-总览与阅读地图.md](../Data_Fabric_as_Modern_Data_Architecture/00-总览与阅读地图.md)），
  其编织层讨论以本书平台章为"被编织对象"的下层（→ 10 章）。

## 7. 常见误区

| 误区 | 修正 |
| --- | --- |
| "按书照抄 SKU 清单" | 2022 SKU 表过时最快（§1/§6 替换读法） |
| "Serverless 省掉建模" | 无 Gold 层的裸湖扫查=账单与延迟双爆（§3） |
| "上了 Synapse 即湖仓" | 抽全量回专用池=旧数仓换皮（§3 判读） |
| "网络安全=防火墙开关" | 私有端点+出站收敛+托管 VNet 是三件独立事（§4） |
| "IaC 是大厂专属" | 无代码化管道的回滚/审计/复制成本三年后必然反噬（§5） |
| "Fabric 出现前 Azure 无湖仓答案" | 本书正是"前 Fabric 时代"完整拼装样本，史料价值高（§6） |

## 与其他章 / 其他书的联系

- 被映射的六动词各章 → 03/04/05/06/07/08 各篇
- 大图案关系 → [10-与大图案结合Data-Mesh与Fabric.md](10-与大图案结合Data-Mesh与Fabric.md)
- Fabric 纵深（盘上实链）→ [../Fundamentals_of_Microsoft_Fabric/00-总览与阅读地图.md](../Fundamentals_of_Microsoft_Fabric/00-总览与阅读地图.md)
- 非 Azure 平台的"仓服务湖"对照 → [../Amazon_Redshift_TDG/00-总览与阅读地图.md](../Amazon_Redshift_TDG/00-总览与阅读地图.md)
- 时效对账总表 → [11-2022到2026的演进对账.md](11-2022到2026的演进对账.md)

## 核心概念速览（中英对照）

- **Synapse Analytics** — 微软分析伞形服务（集成/库/管道/多引擎）✅ 官方口径。
- **ADLS Gen2** — Azure 数据湖存储第二代：对象存储+分层命名空间 ✅。
- **专用池 / Serverless** — Dedicated / Serverless SQL：预置仓与按需湖上查询两形态（§3）。
- **托管 VNet** — Managed Virtual Network：工作区数据面网络隔离（§4 ⚠️）。
- **私有端点** — Private Endpoint：PaaS 资源落入私网边界（§4）。
- **管道即代码** — Pipelines-as-Code：ETL 资产纳入 Git/CI 纪律（§5）。
- **OneLake / Fabric** — 微软 2023+ 统一数据底座：本书第 9 章的当代替身（§6）。
- **容器前缀法** — Container-per-Environment：多环境共用一湖的隔离方案（§5）。
- **成本护栏** — Cost Guardrail：扫描量上限/自动取消等 serverless 保险丝（§3）。
- **DWU** — Data Warehouse Unit：专用池预置计费单位（⚠️ 2022 快照）。

## 最新演进与工业实践

- **Fabric GA 与 Synapse 定位收缩**（2023-2026）：新建工作负载默认 Fabric，Synapse
  存量继续支持；本书 Azure 章从"施工图"变成"历史剖面"（盘上 #221 册为现行教材）。
- **Databricks-SQL/Warehouse 化**：湖仓平台自身长出"仓"服务面，与微软路线双向收敛
  ✅ <https://learn.microsoft.com/en-us/azure/databricks/lakehouse/>——09 章的
  仓/湖边界之争在平台层被吸收。
- **开放格式反向进入托管平台**：Fabric/托管湖仓对 Parquet/Delta/Iceberg 的直读与
  互转持续增强（⚠️ 转述；对账详见 11 章），"绑定私有格式"的风险自 2022 起单调下降。
- **工程方法迁移**：环境即代码、数据平台测试金字塔、CI 中的 schema 演化检查等
  2022 年本书着墨轻的环境工程段，2026 已是岗位基本功——方法层请配盘上工程册
  [../Engineering_Lakehouses_with_Open_Table_Formats/11-引擎集成与工程化落地.md](../Engineering_Lakehouses_with_Open_Table_Formats/11-引擎集成与工程化落地.md)。
