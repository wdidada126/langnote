# 08 Azure 侧编排与集成 — Data Orchestration Techniques B 段（原书第 5 章之 Azure 半边，章级 ✅）

> 段归属 ⚠️ 推定（Ch5 双云并写，本章收 Azure 件）。机制全部 ⚠️ 转述 + ✅ URL
> （learn.microsoft.com 域，2026-10-02 验 200）；ADF/Synapse 不可本机实测；
> 🔧G1 复引为 DuckDB/SQLite 类比，**非 Azure 平台行为**。波内辨析：Synapse/Fabric 专深
> 归 #217/#219/#218/#220/#191（只登记不链，00 §5），本章仅取「多云拼件」视角。

## 8.1 ADF：Azure 编排的「主账本」（⚠️+✅）

入口页 ✅ https://learn.microsoft.com/en-us/azure/data-factory/introduction。要点转述 ⚠️：

- **活动族**：Copy（数据流式复制）、数据流（映射数据流=可视化转换）、Execute Pipeline、
  Web/存储过程/Azure Databricks 等外呼活动、控制活动（If/ForEach/Until/过渡）——
  7.3 三公理在 ADF 的原生落点：**重试在连接/活动属性、失败走过渡于 Execute 活动** ⚠️；
- **触发器**：Schedule/Tumbling（窗口回补友好）/Event（Blob 到达等）/Tumbling 窗口对账 ⚠️；
- **集成运行时 IR**：Azure/自托管/Express Route 三型——自托管 IR 是「云内编排伸向本地与
  他云数据源」的标准孔位（多云链路的 Azure 侧接头，⚠️）；
- **VNet 与托管专有网络**：出网受控面与 11 章私网端点同族（⚠️）。

## 8.2 Synapse 管道与专用池的作业耦合（⚠️+✅）

- Synapse 概览 ✅ https://learn.microsoft.com/en-us/azure/synapse-analytics/overview-what-is：
  工作区把专用 SQL 池/无服务器池/Spark/管道收进一个门面；
- 专用池建模与分布 ⚠️+✅ https://learn.microsoft.com/en-us/azure/synapse-analytics/sql-data-warehouse/sql-data-warehouse-overview-what-is：
  03 章 D1 分布式（哈希分发列）的官方出处——ADF/ Synapse 管道对池的作业控制（T-SQL 活动/存储过程）
  即「编排写进仓库事务边界」的 Azure 形态；
- 管道活动语义与 ADF 同源（✅ https://learn.microsoft.com/en-us/azure/data-factory/concepts-pipelines-activities）——
  工业口径：ADF 与 Synapse 管道=同一活动模型的两个宿主，选型看工作区资产与权限形状而非能力差 ⚠️。

## 8.3 湖侧件：Databricks 作业与 ADLS 事件链（⚠️+✅）

- Azure Databricks ✅ https://learn.microsoft.com/en-us/azure/databricks/getting-started/overview：
  多任务作业/Jobs API/触发器使 05 章「性格B」的管道面自带编排——与 ADF 的分工是
  「ADF 管跨源搬运与全局触发，Databricks 管湖上计算 DAG」（⚠️ 通说划界，非书中原文）；
- medallion 官方作业蓝本 ✅ https://learn.microsoft.com/en-us/azure/databricks/lakehouse/medallion（🔧G3 概念出处，05 章）；
- ADLS 事件→触发→回补的闭环在 Blob 事件网格上完成 ⚠️（事件总线产品页本次未单独验真，
  以 medallion/AZ2 现行文档叙述为准——登记 ⚠️）。

## 8.4 🔧 复引 E-G1：无服务器联邦查询的「 Azure 侧税形」（非 Azure 行为）

04 章 G1（ATTACH 双 SQLite 源 JOIN 75.0ms vs 物化 6.2ms，税 ≈12.2×）在此给 Azure 用法：
Synapse 无服务器池对 ADLS 上 Parquet/Delta 的临时探查、跨源 T-SQL 外表查询——**计费按扫描量**，
联邦税从「时延」变形为「账单」⚠️。运维面板/即席分析选它（低频），
生产链路在 8.2 作业耦合里物化成专用池对象（高频）——这条「探查用 serverless、
生产用专用池」的分层纪律即 🔧G1 的制度落点（07 章 7.5 复引）。

## 8.5 多云接口的 Azure 端点清单（⚠️ 重构）

| 接口 | Azure 端 | 配对的 AWS 端（09 章） | 护栏 |
|---|---|---|---|
| 数据进出孔 | ADF 自托管 IR/外呼 Web 活动 | Glue 连接/DMS 端点 | 凭据进 Key Vault⇄Secrets Manager（11 章） |
| 事件总线 | Event Grid 域 ⚠️ | EventBridge/SNS 域 ⚠️ | 跨云事件只做「通知+指针」（7.1 旁路护栏） |
| 身份 | Entra ID 体系 ⚠️ | IAM/Identity Center ⚠️ | 全局令牌交换单点——11 章主战场 |
| 目录投影 | Purview Data Map（✅ https://learn.microsoft.com/en-us/azure/purview/） | Glue Catalog（✅ https://docs.aws.amazon.com/glue/latest/dg/catalog-and-crawler.html） | 一中心一投影（10 章三角裁定） |

## 8.6 本章学习检查点（⚠️ 推定）

1. 说出 ADF 里「重试」与「补偿」分别落在哪个构造（连接属性/过渡设计）；
2. 「ADF 管搬运与全局触发、Databricks 管湖上 DAG」的划界在什么场景应反转（纯仓资产团队）；
3. 🔧G1 的 12.2× 如何同时解释「serverless 探查免费午餐不成立」与 8.4 的分层纪律。

## 8.7 ADF 对象速查（⚠️ 转述 ✅AZ2/AZ9 域）

| 对象 | 一句话定位 | 多云视角挂点 |
|---|---|---|
| Pipeline | 活动容器+参数域 | 中枢清单的模板单元（7.4） |
| Dataset | 源/目标指针抽象 | 「传指针不传数据」纪律载体（7.1） |
| Copy Activity | 高吞吐搬运活动 | 跨云搬运面 Azure 端（8.5 行①） |
| 数据流 | 托管映射转换 | 重转换可让位 Databricks（8.3 划界） |
| Tumbling 触发器 | 时间分格+回补 | 窗口对账优于事件补录 |
| 自托管 IR | 云外/他云孔位 | 8.5 端点表第一行接头 |

## 8.8 Azure 侧误读与运维备忘（⚠️ 编者注）

1. 「ADF 与 Synapse 管道二选一」——同活动模型两宿主（8.2），差异在工作区权限资产不在能力；
2. 「数据流能替 Spark 重活」——湖上计算 DAG 归 Databricks 件，划界别越（8.3）；
3. 「无服务器池适合一切只读」——高频刷新=账单曲线陷阱（🔧G1×频率，8.4 分层纪律）；
4. 排障序：触发器→活动→IR→网络→权限；自托管 IR 离线占跨云故障大头（⚠️ 通说经验）；
5. 模板漂移比手工双环境更贵——环境矩阵进 CI 是 7.4 的纪律重申，密钥永不进模板（11.3）。

## 8.9 Azure 端点排障速查（⚠️ 通说编者注）

| 症状 | 首查 | 次查 | 锚 |
|---|---|---|---|
| 管道不点火 | 触发器状态/时区 | 事件路由订阅 | 8.1 |
| 复制超时 | IR 在线与出网 | 目标端限流 | 8.5 |
| 数据流 OOM | 执行核数/拆分列 | 源端分区倾斜 | 8.7 |
| 湖上读慢 | 文件小碎（合并作业） | 谓词能否裁剪 | 🔧G2/G3 |
| 权限忽通忽断 | 双身份（工作区+存储）混用 | 令牌有效期 | 11.3 |

排障表的意义：把「平台玄学」拆成「对象状态」——编排章（07）公理在 Azure 宿主的查表化。
表外一条经验 ⚠️：跨云排障永远先分清「控制面断了」还是「数据面慢了」——前者查本表行①②，后者查行④。

## 8.10 读后回环二问（自测 ⚠️）

1. 你司 ADF 里 Tumbling 窗口用了还是没用？没用——回补靠什么？（7.2 触发轴自测）
2. 「探查用 serverless、生产用专用池」写进你司的哪份规范了？写不出来=没落地（8.4）；
3. 8.5 端点表四行，你司已「成对」建了几行？缺的行先补目录与身份两行（10/11 章优先级高于管道）。

## 核心概念速览（中英对照）

| 中文 | 英文 | 一句话 |
|---|---|---|
| Azure Data Factory | ADF | Azure 托管编排服务：活动/触发器/IR 三件套（✅AZ2） |
| 集成运行时 | Integration Runtime | ADF 的执行接头：Azure/自托管/ExprRoute 三型（8.1） |
| 映射数据流 | Mapping Data Flows | 可视化转换活动族（⚠️） |
| 滚动窗口触发器 | Tumbling Window Trigger | 时间分格+回补语义的对账型触发 |
| Synapse 工作区 | Synapse Workspace | 池+Spark+管道的统一门面（✅AZ1） |
| 专用/无服务器池 | Dedicated / Serverless SQL Pool | 生产物化面 vs 按扫描计费探查面（8.2/8.4） |
| 活动 | Activity | ADF/Synapse 管道原子：数据/控制/外呼三类 |
| Purview Data Map | Purview Data Map | Azure 目录中心（✅AZ3；10 章主场） |
| 托管虚拟网络 | Managed VNet | 出网受控面（8.1 ⚠️） |
| 端点配对 | Endpoint Pairing | 8.5 多云接口的两云同名孔位表 |

## 最新演进与工业实践

- **ADF→Fabric Data Factory 的能力上移**（2023–，⚠️ 时间口径；✅ https://learn.microsoft.com/en-us/azure/data-factory/introduction 与 https://learn.microsoft.com/en-us/fabric/get-started/microsoft-fabric-overview 双现行页）：Copy Job/Mapping Flows 获得 Fabric 镜像形态，本册 8.1/8.2 的活动模型在 2026 仍是两宿主的公约数；Fabric 专深登记波内兄弟册不链（00 §5）。
- **Synapse Manifest/新工作区形态收敛**（⚠️ 转述；✅AZ1/AZ8 域）：微软主推口径向 Fabric-first 倾斜——多云蓝图里 Azure 侧「仓件」的采购路径从 Synapse 专用池扩展到 Fabric 仓（8.5 端点表在 2026 需为身份/目录两行增加 Fabric 口径，本册按成书快照保留原行 ⚠️）。
- **Databricks Jobs 的多云一致性红利**（⚠️；✅AZ6 域）：同一 Jobs API 在 Azure 与 AWS 的 Databricks 上行为趋同——7.4「一份定义两云可跑」的模板在中立引擎侧比 ADF⇄Glue 双方言路线更易达成，是 2024–2026 工业实践的常见折中（09 章对位收口）。
- **自托管 IR 的跨云孔位定型**（⚠️ 通说）：Azure 侧「伸出去」的标准姿势从 VM 代理演进到受控专线+存储网关混合；本册维持「跨云只传指针/令牌、数据不过编排器」的 7.1 护栏判断。
