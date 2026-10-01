# 06 OneLake 与湖仓落地 — OneLake & Lakehouse Landing（⚠️ 重构章，非原书 TOC）

> 章题为 ⚠️ 推定重构（00 §2）；机制 = 官方文档转述 ⚠️ + ✅ URL；OneLake 本机不可实测（⚠️）；
> 🔧 E2 为 DuckDB ATTACH 跨库类比（**非 Fabric 平台行为**）。本章是「湖仓 ETL 对位」硬义务主战场。

## 6.1 OneLake：统一数据湖的「一个账户一个湖」（⚠️ 转述）

权威页：`https://learn.microsoft.com/en-us/fabric/onelake/onelake-overview` ✅ O1。要点：

- OneLake = Fabric 的全局单一湖 ⚠️：每个租户自动获得，所有工作负载（Lakehouse/Warehouse/
  实时/DF）的数据在**同一命名空间**下共存，文件层默认 Delta Parquet 开放格式（口径以现行页为准）。
- 对 FDF 的意义：copy/暂存的**默认落点**——03 章的 sink 一旦指向 Lakehouse，路径即
  `Files/` 或表目录（⚠️ 表/文件双视图细节以 O1/现行文档为准）；「搬完即可查」消灭了
  传统「先落对象存储再注册外表」的一段工程税。
- 与 ADLS 的关系 ⚠️：OneLake 底层与 Azure 存储的映射/直通语义官方有专述，本册不抄细节；
  剧本层面只需记住：外部对象存储 = 源/目标之一（连接器，03 章），OneLake = 家族资产。

## 6.2 快捷方式（Shortcuts）：不改位置的联邦（⚠️ 转述）

权威页：`https://learn.microsoft.com/en-us/fabric/onelake/onelake-shortcuts` ✅ O2。

- Shortcut = 把外部存储（S3/ADLS/Dropbox…清单以 O2 现行页为准）**挂载**进 OneLake 命名空间，
  数据不动、路径统一 ⚠️——与 copy 的哲学互补：**能引用就别搬运**（03 章 3.6「何时不用
  Copy」的平台原生答案）。
- 剧本影响：①源侧接入评估先问「能不能 shortcut」，再问「copy 参数怎么调」；②shortcut
  读出的分区裁剪/统计能力弱于本地 Delta 表（⚠️ 机制推断，性能剧本以 10 章实测流程复核）；
  ③治理面：引用数据与搬运数据的血缘/权限在目录中形态不同（盘上治理册群对位见 6.5）。

## 6.3 🔧 实测 E2：统一命名空间类比——ATTACH 跨库移动（非 Fabric 平台行为）

DuckDB 1.5.5，`warehouse.duckdb` 为主库，`ATTACH 'exp/landing.duckdb' AS landing` 后跨
catalog 直接 `CREATE TABLE landing.raw_orders AS SELECT ... FROM orders`（exp_out.txt 实抓）：

```
=== T2 ATTACH 跨库移动（OneLake 统一存储类比）===
 order_id customer  amount order_date
        1     Acme   120.5 2024-01-05
        4    Gamma   300.0 2024-01-07
```

- 类比映射：`warehouse`=源系统、`landing`=湖内暂存库、ATTACH=OneLake 命名空间统一、
  跨 catalog SELECT=「同湖内移动只是 SQL，不是网络搬运」。
- 失配登记 🔧：DuckDB ATTACH 无权限模型、无异步复制、无外部对象存储形态（shortcut 的
  「数据不动」在这里只能靠「同文件多 schema」勉强示意）——**非 Fabric 平台行为**，
  仅证「统一命名空间让搬运降级为 SQL」这一条直觉。

## 6.4 落地分层剧本：bronze/silver/gold 在 FDF 的对象映射（⚠️ 编者框架）

| 层 | Fabric 对象 | FDF 侧动作 | 章链 |
| --- | --- | --- | --- |
| bronze | Lakehouse（copy 直落，分区目录） | Copy job/activity + 显式映射 | 03 章 🔧E1 |
| silver | 同库 Delta 表 | Notebook/作业定义清洗 + MERGE | 05/07 章 🔧E3 |
| gold | 语义模型/Warehouse 侧 ⚠️ | 编排收尾 + 质量断言 | 09 章 |

- 分区策略 ⚠️：落地即分区（日期列，🔧E1 的 `order_date=…` 形态）决定后续所有增量剧本的
  扫描经济学（10 章）；「先全量后分区」等于把税延到查询期。
- 与湖仓理论书的对位（**波1 在盘实链，ls 验名 ✅**）：
  [../Practical_Lakehouse_Architecture/03-存储湖仓架构的核心.md](../Practical_Lakehouse_Architecture/03-存储湖仓架构的核心.md)
  回答「湖的存储层为什么这样设计」，本章回答「在 Fabric 里这套设计以哪些 item 呈现」；
  其 05 计算引擎章 ↔ 本册 05 章（编排视角）经纬互见。

## 6.5 与 repo 其他书的联系

- 湖仓对位主链（义务册）：[../Practical_Lakehouse_Architecture/00-总览与阅读地图.md](../Practical_Lakehouse_Architecture/00-总览与阅读地图.md) ✅
  （其「平台四件套」框架中，本册=「计算/编排」件套在 Fabric 的落地说明书）。
- 格式纵深：[../Data_Lakehouse_in_Action/00-总览与阅读地图.md](../Data_Lakehouse_in_Action/00-总览与阅读地图.md) ✅、
  [../Apache_Iceberg活用入門/00-总览与阅读地图.md](../Apache_Iceberg活用入門/00-总览与阅读地图.md) ✅（OneLake 默认 Delta vs Iceberg 阵营对照，ls 验名）。
- Fabric 组件浅层：[../Fundamentals_of_Microsoft_Fabric/03-OneLake统一数据湖与快捷方式.md](../Fundamentals_of_Microsoft_Fabric/03-OneLake统一数据湖与快捷方式.md) ✅
  （与本 6.1/6.2 同题双档：全景一段话 vs 剧本级展开）。
- 目录/血缘治理：[../The_Enterprise_Data_Catalog_2e/00-总览与阅读地图.md](../The_Enterprise_Data_Catalog_2e/00-总览与阅读地图.md) ✅（6.2 治理面登记，ls 验名）。
- 波内登记（不链）：#218/#191 的 OneLake 节；#217/#219（Synapse 线落 ADLS 世代，与 6.1
  「一段工程税」的历史对照）。

## 6.7 接入评估清单：shortcut 还是 copy？（6.2 剧本的展开 ⚠️ 编者）

| 判据 | 倾向 shortcut | 倾向 copy |
| --- | --- | --- |
| 读频 | 低频直读/偶发审计 | 高频扫描（裁剪/格式收益大） |
| 写需求 | 只读源 | 目标端加工/落地 |
| 性能 | 可容忍引用层裁剪弱 ⚠️ | SLA 紧，需本地 Delta 统计 |
| 治理 | 数据主权在源方、不想留副本 | 需要湖内血缘/生命周期策略 |
| 成本 | 省存储驻留（10.1③） | 重复网络传输高的场景反而该搬 ⚠️ 价签现场核 |

- 决策口诀：**「引用优先、热数据搬运、搬了就分区」**（6.2 + 6.4 + 🔧E1 三节压缩）。

## 6.8 本章自测（答案均在上文 ⚠️ 编者）

1. OneLake 消灭的「一段工程税」具体指什么步骤？（6.1：落对象存储再注册外表）
2. 🔧E2 里 ATTACH 类比映射了 OneLake 的哪个性质、漏了哪些？（6.3：统一命名空间；
   权限/异步/外部形态全缺）
3. bronze 分区键为什么「在 copy sink 处定生死」？（6.4，联动 10.3）
4. 引用数据与搬运数据在治理面的差异登记在哪节？（6.2③）
5. 本册与 PLA 册的分工一句话？（6.4/11.4：图纸与工序）
## 6.9 一页小结卡（背卡式 ⚠️ 编者）

- OneLake：租户一湖、命名空间统一（✅ O1）；Shortcut：引用不搬运（✅ O2）。
- 口诀：引用优先、热数据搬运、搬了就分区（6.7）。
- 三层映射：bronze=copy 落点 / silver=MERGE 收编 / gold=语义层（6.4）。
- 对位：PLA 册给图纸，本册给工序（6.4/11.4 两处实链）。
## 核心概念速览（中英对照）

- **OneLake** — 统一数据湖：租户级单一命名空间，全负载共湖（✅ O1）。
- **快捷方式** — Shortcut：外部存储引用挂载，数据不动路径统一（✅ O2）。
- **湖内搬运降级** — 统一命名空间使「复制」退化为 SQL（🔧E2 类比主旨）。
- **bronze/silver/gold** — 落地三层与 FDF 对象映射表（6.4 ⚠️ 编者框架）。
- **落地即分区** — Partitioned landing：分区键在 copy sink 处定生死（🔧E1 形态）。
- **能引用就别搬运** — shortcut-first 评估序：接入决策第一步（6.2 剧本）。
- **开放格式默认值** — Delta/Parquet 文件层（✅ O1 口径，细节以现行页为准 ⚠️）。
- **引用 vs 搬运血缘差** — 治理形态差异登记（6.2③，治理册对位）。

## 最新演进与工业实践

- **口径演进**（✅ O1/O2 现行页，⚠️ 转述纪律）：OneLake 的格式选项（Direct Lake/外部格式
  支持面）与 shortcut 连接器清单是 2025–2026 更新最密集的区域之一；本册只钉「命名空间统一
  + 引用/搬运互补」两条不会过时的骨架，清单类内容全部指向现行页。
- **湖仓阵营对照** ⚠️：FDF+OneLake 的组合相当于「编排器 + 托管湖」一体化，与
  「Airflow/dbt + 自建 Iceberg」开源栈的分工差异，可对照
  [../Engineering_Lakehouses_with_Open_Table_Formats/00-总览与阅读地图.md](../Engineering_Lakehouses_with_Open_Table_Formats/00-总览与阅读地图.md) ✅（ls 验名）——选型讨论的双方素材各在本目录 02/05 章与该册格式对比章。
- **工业实践**：①shortcut 先行的接入评审（6.2）能把一次性搬运需求砍掉相当比例 ⚠️ 编者综合；
  ②bronze 分区键与 SLA 对齐（日/小时粒度按业务迟到容忍定）；③「同湖多负载」的账单归因
  需要 CU 计量侧配合（10 章回收）。
- **本机互鉴** 🔧：E2 的 ATTACH 演示适合入职培训讲「为什么统一命名空间值钱」（**非 Fabric
  平台行为**）。
