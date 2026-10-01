# 04 Synapse Link 与 Cosmos 实时分析 — Engineering Real-Time Analytics with Azure Synapse Link Using Cosmos DB（原书第 4 章）

> 章题 ✅ Packt 官方 ColorImages PDF 文本层实抓；配方级小节 ⚠️ 推定（一手旁证 = 官方仓库
> `chapter 4/code`：IoT-Temp.json、chapter4.txt——温度传感类 JSON 样本对位 Cosmos 文档）。
> 机制 = Microsoft Learn 转述 ⚠️ + ✅ URL（2026-10-02 `curl -sI` 200）；Azure 不可实测 ⚠️；
> 🔧 类比实验标注**非 Synapse 行为**。

## 4.1 问题陈述：分析不该打扰 OLTP

传统链路「Cosmos → 导出/ETL → 数仓」有延迟与RU双重成本 ⚠️。**Azure Synapse Link for
Azure Cosmos DB** 的答案：在 Cosmos 容器上开启**分析性存储（analytical store）**，
变更 feed 以列式存储自动镜像（默认 5 分钟级新鲜度、全保真），与操作副本（row-based）
同账管双副本 ⚠️：

- ✅ `azure/synapse-analytics/synapse-link/concept-synapse-link-cosmos-db-support`（支持面）；
- ✅ `azure/synapse-analytics/synapse-link/how-to-connect-synapse-link-cosmos-db`（连接配方）；
- 原 `synapse-link-how-it-works` 专页 404 → **缺口登记**，机制描述以上两页现行版为准 ⚠️。

消费侧两路 ⚠️：**服务器端点**（T-SQL `OPENJSON` 语义读文档，4.3）与 **Spark 池**
（synapse-link 连接器读 Parquet 化分析副本，4.4）。

## 4.2 开启与连接配方（对位本章主 recipe）

⚠️ 转述 how-to 页步骤：① 账户/容器启用 analytical store（TTL/分区键约束 ⚠️）→
② Synapse 工作区建链接服务（Cosmos SQL API 连接）→ ③ 即见「Azure Cosmos DB for
Apache Spark」与「Synapse Link」两类容器视图。零数据搬运、零导出作业——**Link 是拓扑
属性不是管道**（与 02 章管道的对照句 ⚠️ 编者归纳）。

🔧**E5（主类比，非 Synapse）**：SQLite WAL 模式下，分析会话先读到快照 5000 行；OLTP
会话继续提交 200 行写入，分析会话仍持旧快照（无锁冲突），下次查询见 5200——「操作写
与分析读互不打扰」正是双副本思想的单机最小模型；再用 `a.backup()` 在线复制到副本库，
重聚合在副本上跑（0.46ms）主库零负担 ≈「分析副本异步镜像」的直觉版。

## 4.3 服务器端点侧：T-SQL 读文档数据

✅ `azure/synapse-analytics/sql/query-cosmos-db-analytical-store` ⚠️ 转述：对分析存储建
容器级外部数据源 + `OPENROWSET(BULK...)` 行集函数，JSON 路径表达式取嵌套字段；
物化成视图/外部表复用。IoT-Temp.json 型样本（✅ 文件夹名）正是「设备遥测 JSON →
温度告警 KPI」的教学载体 ⚠️ 推定。

## 4.4 Spark 侧：DataFrame 直读与写回

✅ `azure/synapse-analytics/spark/apache-spark-overview` + synapse-link 连接器 ⚠️：
`spark.read.synapseLink(...)` 风格 API 读容器为 DataFrame（分区裁剪 + 列裁剪下推），
与 05 章笔记本配方共用；写回 Cosmos 走 connector sink ⚠️。实时面 ⚠️：分析存储非
严格流（5 分钟批式新鲜度），更低延迟需 change feed 自建流（本章「工程权衡」叙事 ⚠️ 推定）。

## 4.5 Synapse Link 家族全景（章末延伸 ⚠️）

| Link 变体 | 源 | 现行文档 ✅ |
| --- | --- | --- |
| Cosmos DB | 文档 OLTP | 4.1 两页 |
| SQL Server 2022 | 本地实例近实时入湖 | `synapse-link/sql-server-2022-synapse-link` |
| Azure SQL Database | 云 SQL | `synapse-link/sql-synapse-link-overview` |
| Dataverse (Power Platform) | 业务应用 | 目录实抓（跨产品路径，弃直引） |

「Link for SQL」以 CDC 连续复制把源库变更落到 ADLS Parquet/Delta 层 ⚠️——与 Cosmos 版
的「同账户双副本」机制不同、目标同构：**别让分析查询扫生产表**。

## 4.6 实时分析工程检查单（编者归纳 ⚠️）

1. 新鲜度 SLA 是分钟级还是秒级？（Link=前者；秒级另起流栈，本书不覆盖）
2. 容器分区键/TTL 与分析查询谓词对齐了吗？
3. JSON schema 漂移策略（服务器端点静态列 vs Spark 推断）定了吗？
4. RU/存储双副本成本进预算了吗 ⚠️？
5. 权限：只读分析主体与工作区角色最小化 ✅ `security/synapse-workspace-synapse-rbac`。

## 4.7 与 repo 其他章/册的联系

- 直读引擎面 → [03-多节点最优处理与专用池调优.md](03-多节点最优处理与专用池调优.md) 3.7；
- Spark 消费 → [05-SynapseNotebook与Spark数据工程.md](05-SynapseNotebook与Spark数据工程.md)；
- 下游报表 → [07-PB级可视化报表与物化视图.md](07-PB级可视化报表与物化视图.md)；
- 湖仓谱系（跨波实链 ✅ 验名）：[../Data_Lakehouse_in_Action/00-总览与阅读地图.md](../Data_Lakehouse_in_Action/00-总览与阅读地图.md)（开放表格式对照——Link 的分析存储为托管列式，非 Iceberg/Delta 语义）；[../Practical_Lakehouse_Architecture/00-总览与阅读地图.md](../Practical_Lakehouse_Architecture/00-总览与阅读地图.md)；
- 治理衔接 → [08-数据目录与治理.md](08-数据目录与治理.md)。

## 4.8 端到端配方：IoT 温度告警链（⚠️ 对位 chapter 4 的 IoT-Temp.json 样本重构）

把本章零件拼成一条可教学习题链（语义 ⚠️ 转述，样本文件名 ✅ 仓库实抓）：

1. **写入面**：设备遥测以文档形式入 Cosmos 容器（分区键=设备/时间桶 ⚠️），
   容器开分析存储（4.2）；
2. **镜像面**：Link 自动把变更列存化进分析副本，5 分钟新鲜度（4.1）⚠️；
3. **计算面**：服务器端点建容器视图/外部表，T-SQL 窗口函数算「滑动均值+阈值越限」
   （4.3）⚠️（✅ query-cosmos-db-analytical-store）；
4. **动作面**：告警查询挂管道定时活动（02 章），或笔记本转 Spark 流式画像（05 章）⚠️；
5. **呈现面**：Power BI 直连端点视图出温度 KPI 板（07 章）⚠️。

教学价值点：同一份数据**零 ETL** 走完 OLTP→分析→告警→报表，对比 02 章管道版
（要建导出作业）——「Link 是拓扑属性不是管道」的实证（4.2 呼应）。

**schema 漂移预案 ⚠️**：文档库字段增删对端点静态列定义是持续摩擦源；
Spark 侧推断更宽容、T-SQL 侧需显式列——两刀流（先 Spark 画像、后端点固化）是
稳妥姿势（对位 5.6 检查项 5）。同理，分析存储的 `_ts`（版本时间戳）与
`_etag` 系统列是增量对账的天然抓手 ⚠️（✅ concept-synapse-link-cosmos-db-support 页主题域）。

## 核心概念速览（中英对照）

- **Synapse Link（Cosmos）** — 操作/分析双副本免 ETL 桥 ⚠️（✅ how-to/concept 两页）。
- **分析性存储** — Analytical store：容器内自动列式镜像，5 分钟新鲜度 ⚠️。
- **双副本模型** — Operational + analytical copy：写走行存、读走列存 ⚠️。
- **OPENROWSET 容器视图** — Serverless 侧 T-SQL 读文档 ⚠️（✅ query-cosmos-db-analytical-store）。
- **synapse-link Spark 连接器** — 分区/列裁剪下推的 DataFrame 直读 ⚠️。
- **Link for SQL** — SQL Server 2022/Azure SQL 的 CDC 入湖变体 ⚠️（✅ 两页现行）。
- **新鲜度权衡** — Freshness vs streaming：分钟级 Link vs 秒级流栈 ⚠️ 编者归纳。
- **RU 成本面** — Request unit cost：双副本与读写的计费维度 ⚠️。

## 最新演进与工业实践

2022→2026（URL 均 ✅ 200；状态 ⚠️ 转述）：

- **机制页重组**：`synapse-link-how-it-works` 已 404（缺口登记），机制并入 concept/how-to
  现行页；Cosmos 侧文档迁往 `azure/cosmos-db/` 域——引用时以本目录验证过的存活 URL 为准。
- **Link 家族向 Fabric Mirroring 收敛**：微软现行叙事把「免 ETL 近实时副本」升格为 Fabric
  镜像数据库（Delta Sharing 落地），Synapse Link 为其前身 ⚠️；本册与 #218/#220 的波内
  分工挂点（00 §6 登记）。
- **工业实践**：遥测/订单类「OLTP 旁路分析」默认双副本化（Cosmos Link、PG logical
  replication→列存、SQL Server 2022 Link 同构）；秒级需求仍走流处理栈——与
  [../Data_Lakehouse_in_Action/00-总览与阅读地图.md](../Data_Lakehouse_in_Action/00-总览与阅读地图.md) 的流批分层互认。
- 🔧 数字口径：E5 为 SQLite 3.45.3 本机实测（WAL 快照读 5000→5200、副本聚合 0.46ms），
  仅演示「读写解耦/异步镜像/副本承载重查询」三抽象，**非 Cosmos/Synapse 平台行为**。
