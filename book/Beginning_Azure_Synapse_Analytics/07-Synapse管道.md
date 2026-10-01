# 07 Synapse 管道 — Synapse Pipelines（原书第 7 章，pp.151–174）

> 章题与页区间 ✅ Crossref 存款记录实抓（DOI 后缀 `_7`，pp.151–174）；章内小节 ⚠️ 推定（无公开样章），
> 按 learn.microsoft.com 数据集成文档域 + Azure Data Factory 文档域组织。托管集成服务不可实测，机制一律
> 「⚠️ 转述 + ✅ URL（2026-10-02 验 200）」；本章无 🔧 组（五组分布于 02/05/09 章，见
> [00](00-总览与阅读地图.md) §6）。

## 7.1 本章在全书中的位置

第 7 章处理「数据进出与编排」：Synapse Pipelines 的本质是**嵌在工作区里的一个 ADF 服务实例**——活动
（activity）、数据集（dataset）、链接服务（linked service）、管道（pipeline）、触发器（trigger）、
集成运行时（IR）六件套照单全收 ⚠️（✅ `get-started-pipelines`、`azure/data-factory/copy-activity-overview`）。
它与 05 章互锁：管道的 Copy 活动是把湖数据灌进专用池的标准装载工。

## 7.2 对象模型六件套（章内主干 ⚠️ 组织）

1. **链接服务**：外部世界的鉴权描述（存储账户/SQL/HTTP/SaaS 连接器目录极宽 ⚠️ ADF 连接器池）；
2. **数据集**：指向链接服务的表/文件视图，参数化是复用命脉；
3. **Copy 活动**：异构数据搬运，支持分区/增量模式/临时暂存 ⚠️ ✅ `azure/data-factory/copy-activity-overview`；
4. **控制流**：Execute Pipeline/If Condition/Foreach/Lookup/Wait 等——「无代码编排」的表达力上限
   决定何时该升级到脚本/Spark（06 章作业定义）⚠️；
5. **触发器**：日历/滚动窗口/事件触发（Blob 事件）三型 ⚠️；
6. **集成运行时**：执行搬运的算力位——Azure IR（云内免费默认）/自托管 IR（打通 VNet 内与本地数据源）
   /Azure-SSIS IR（lift 现有 SSIS 包）三形态 ⚠️（ADF 文档域概念，本册不单独引未验真页）。

## 7.3 装载专用池的官方主路径

- **Copy 进专用池**（默认装载器）✅ `sql-data-warehouse/load-data-from-azure-blob-storage-using-copy`：
  暂存→分发→CCI 重组的托管流程；宽松列匹配、类型转换容错适合治理尚未到位的源 ⚠️；
- **PolyBase 直灌**：同活动类型切换复制方法，大文件高吞吐路径 ⚠️ 同页；
- **COPY 命令/T-SQL 侧**：调度权交回 SQL 面（05 章）✅ `quickstart-copy-activity-load-sql-pool` 示例线；
- **ELT 设计姿态**：原始先落湖（Bronze）、仓内只做 Silver/Gold——本章页区间与 02 章「过渡路径」互文 ⚠️
  （✅ `sql-data-warehouse/design-elt-data-loading`）。

## 7.4 映射数据流（无代码变换层）

- 设计器式 Spark 变换（数据流调试→优化→集群执行），把「T 侧」逻辑从 SSIS/notebook 搬进画布 ⚠️；
- 工程判断 ⚠️ 推定：轻清洗可用数据流；重业务规则仍回 SQL/Spark 代码，画布复杂度是维护债的另一种写法
  （对照盘上 [../Analytics_Engineering_with_SQL_and_dbt/00-总览与阅读地图.md](../Analytics_Engineering_with_SQL_and_dbt/00-总览与阅读地图.md) 的代码优先论 ⚠️）。

## 7.5 编排、监控与 CI/CD

- 作业化联动：管道中 Execute Spark Job 活动消费 06 章「作业定义」✅ `spark/apache-spark-job-definitions`；
- 运行监控：管道运行视图、活动级重试/续跑、告警挂 Azure Monitor ✅
  `monitoring/how-to-monitor-pipeline-runs`；
- 治理面：ARM RBAC 管资源、Synapse RBAC 管「谁能发布哪条管道」；Git 集成（Azure DevOps/GitHub）→
  协作编辑/模板发布/ARM 模板导出 ✅ `cicd/source-control`——**「画布+Git+ARM 模板」三件套是本章的
  DevOps 收口**。

## 7.6 常见误区

1. **「管道=定时 crontab」**——参数化/触发器/事件驱动下它是编排运行时，语义层级不同 ⚠️。
2. **「Copy 方法永远选 PolyBase」**——小文件/非 Parquet 源下 PolyBase 反而劣化，需按源形态选型 ⚠️ 转述
   ✅ load-data-from-azure-blob-storage-using-copy。
3. **「自托管 IR 是免费旁路」**——它把网络/算力风险搬到客户侧，容量与更新是运维合同的一部分 ⚠️。
4. **「监控页可见=可告警」**——需把指标接入 Azure Monitor 规则才闭环（✅ how-to-monitor-pipeline-runs）。

## 7.7 端到端剧本：湖→专用池的编排全流程（⚠️ 推定组织，工件均指向已验页）

1. **登记源与目**：链接服务两个（ADLS Gen2 + 专用池，SQL 侧用工作区托管身份免密 ⚠️）；
2. **参数化骨架**：管道入参 `win_start/win_end`，数据集文件名模板 `yyyy/MM/dd` 分区目录——
   窗口幂等（重跑覆盖同分区）是装载纪律的第一行（对位 05 章 §5.5 影子表切换 ⚠️）；
3. **Copy 活动**：源=Parquet 外表目录、目标=staging 内表；复制方法先默认装载器保容错，
   基线达标后切 PolyBase 提吞吐 ✅ `sql-data-warehouse/load-data-from-azure-blob-storage-using-copy`；
4. **变换段**：Execute Pipeline 子管道跑 T-SQL（CTAS 影子重建 ✅ `sql-data-warehouse/sql-data-warehouse-develop-ctas`）
   或 Execute Spark Job 活动接 06 章作业定义 ✅ `spark/apache-spark-job-definitions`；
5. **质量闸门**：Lookup+If Condition 做行数/水位断言，失败走失败支路告警（Monitor 接线 §7.5）；
6. **收尾发布**：触发器挂窗（滚动窗口对齐业务日界），Git 发布线走 §7.5 三件套 ✅ `cicd/source-control`。

- 剧本要义：**管道负责「到没到、何时到、坏了谁通知」**，变换语义归 SQL/Spark——07 章与 05/06 章的
  分工线在此最清晰 ⚠️ 推定。

## 7.8 复用与治理速记（参数化三件套+反模式）

- 参数化三件套：管道入参→数据集动态表达式→活动级 `@{pipeline().parameters.*}` 级联；元数据驱动
  （配置表+ForEach 动态管道）是 ADF 社区的标准复用模式 ⚠️ 转述；
- 反模式清单 ⚠️ 推定组织：单管道千活动（不可评审）、Lookup 拉全表（内存炸）、Foreach 串行高并发
  （队列堵）、明文连接串（鉴权漂移）、无幂等窗口（补数即事故）；
- 治理对位：管道资产=ARM 模板+参数文件，环境差异集中在链接服务端点与密钥引用（Key Vault），
  与 08 章发布线同构。

## 7.9 连接器与鉴权小抄（本章工程侧写 ⚠️ 推定组织）

| 源族 | 典型链接服务 | 鉴权首选 | 备注 |
| --- | --- | --- | --- |
| Azure 存储/仓 | BlobFS/专用池 | 托管身份 RBAC | 免密主线（08 章三角） |
| SaaS/HTTP | REST/Http | Key Vault 托管密钥 | 轮转纪律入发布参数 |
| 内网 SQL/Oracle 等 | 对应连接器 | 自托管 IR+域账号/证书 | 网络负债在客户侧 |
| SSIS 遗产 | SSISIR | 包配置+代理账户 | lift 路径不动逻辑 |

- 鉴权三问模板：谁执行（IR 身份）、以谁的身份读（连接器凭据来源）、失败暴露在哪（活动错误页+
  Monitor）——每个新链接服务答齐再合入 ⚠️。
- 与 08 章关系：连接器目录属数据面资产，发布随 ARM 模板走；密钥值永远不进 Git（Key Vault 引用
  参数化），这是三件套的硬边界（✅ `cicd/source-control` 域内实践 ⚠️ 转述）。

## 核心概念速览（中英对照）

- **管道** — Pipeline：活动序列+控制流的编排单元，Synapse 内嵌 ADF 实例执行 ⚠️ ✅ get-started-pipelines。
- **活动** — Activity：Copy/Lookup/Execute Pipeline 等最小编排步骤（控制流活动族）⚠️。
- **数据集** — Dataset：链接服务之上的表/文件抽象，参数化复用载体 ⚠️。
- **链接服务** — Linked Service：外部数据源/算力的连接与鉴权描述 ⚠️。
- **集成运行时** — Integration Runtime：执行搬运的算力位（Azure/自托管/SSIS 三型）⚠️。
- **触发器** — Trigger：日历/滚动窗口/事件三类调度入口 ⚠️。
- **映射数据流** — Mapping Data Flows：画布式无代码 Spark 变换层 ⚠️。
- **复制方法** — Copy Method：默认装载器 vs PolyBase 的吞吐/容错折中开关 ✅ load…using-copy。
- **作业定义联动** — Pipeline↔Spark Job Definition：Execute Spark Job 活动打通 06/07 章 ✅。
- **三件套发布** — Canvas+Git+ARM Template：管道资产进生产环境的 DevOps 路径 ✅ cicd/source-control。

## 最新演进与工业实践

2021→2026（URL 均 2026-10-02 验证 ✅ 200；描述 ⚠️ 转述）：

- **官方迁移路径**：Synapse 管道→Fabric Data Factory 升级指南 ✅
  https://learn.microsoft.com/en-us/azure/data-factory/how-to-upgrade-your-azure-synapse-analytics-pipelines-to-fabric-data-factory
  ——活动/数据集/IR 对象模型平移，计费并入 Fabric 容量 ⚠️；本书六件套概念即迁移的「源端词典」。
- **旧集成概览页 404 勘误**：2021 代 `integrate-data-overview` 已下线（实测 404，登记
  [00](00-总览与阅读地图.md) §2）；现役入口为 `get-started-pipelines` ✅ 与本册 §7.1 引用面。
- **事件驱动扩张**：Event Grid/OneLake 事件触发成为 2026 编排新默认节奏，管道触发器概念仍在但重心
  转向湖上事件 ⚠️ 转述（Fabric 文档域）；盘上实时分析架构专著仅登记主题对位（目标文件实名未逐一复核，
  按波规不建链；登记见 [00](00-总览与阅读地图.md) §7）。
- **工业实践**：装载面「Copy 治百病」的旧习惯被三件事改写——湖上直写（Spark/Delta）、仓侧直读（外部表
  视图化）、零 ETL 旁路（09 章 Link/Mirroring）；管道的价值收敛到**编排、跨源搬运与治理接线** ⚠️。
- **SSIS 遗产线**：Azure-SSIS IR 仍是微软官方承认的迁移跳板 ⚠️；2026 Fabric 无对应 SSIS IR，长尾
  包多留在 ADF/Synapse 存量侧（波内 #220 Data Factory Playbook 登记主题，不链）⚠️。
