# 02 OneLake 统一数据湖与快捷方式 — The Data Engineer's Guide to Microsoft Fabric（⚠️ 主题重构章）

> 本章为 ⚠️ 主题域重构（00 §5 口径）：对位书名 "Data Engineer's Guide" 的**存储底座**面。
> 机制事实全部来自 learn.microsoft.com OneLake 域当日 200 实验页（✅ 转述）；"书里会怎么讲"
> 一律为编者推定。🔧 为本机类比实测（**非 Fabric 行为**）。

## 2.1 为什么数据工程师的第一站是 OneLake

Microsoft Fabric 的存储主线 ⚠️（转述 `https://learn.microsoft.com/en-us/fabric/onelake/onelake-overview` ✅）：
OneLake 是租户级"一个湖"——所有工作负载（Lakehouse/Warehouse/Eventhouse…）的数据统一落在
`abfss://<文件系统>@<湖名>.lakehouse.microsoft.com/<表路径>` 这样的**统一命名空间**下，底层是
OneLake 托管的存储，用户不可见容器、只可见层级路径。对数据工程师的意义（⚠️ 推定的本书视角）：

- **去桶化**：不再有"这个数据放哪个存储账户"的组织级决策；湖是租户默认基础设施。
- **一份数据多引擎**：同一 Delta/Parquet 文件可同时被 Spark（笔记本）、SQL 分析端点、Power BI
  Direct Lake 读——"拷贝漂移"从架构问题降级为偶发运维问题。
- **API 面**：文件级经 OneLake Explorer/REST 暴露（✅ onelake-overview 文内导航）。

对照开放世界：S3+Hadoop 命名空间/表格式 catalog 承担同样职责——通论见
[../Practical_Lakehouse_Architecture/03-存储湖仓架构的核心.md](../Practical_Lakehouse_Architecture/03-存储湖仓架构的核心.md)；
本册是"厂商把这些全收了"的对照组。

## 2.2 Shortcut：零拷贝指针，本章的题眼

✅ 转述 `https://learn.microsoft.com/en-us/fabric/onelake/onelake-shortcuts`：Shortcut 把**外部存储
位置挂进**湖内某路径下，挂载点之后即视同本地文件；数据不动、不复制，移动的是"读的边界"。
文档明列的支持面对象（✅ 当日页）：

| 源 | 语义 |
|---|---|
| Azure Blob / ADLS Gen2 | 原生同云，凭据直连 |
| Amazon S3 / S3 兼容 | 跨云挂接（配连接/凭据管理） |
| Google Cloud Storage | 同上 |
| Dataverse / 本地(经网关) | 企业 SaaS 与 on-prem 面 |

工程师侧的三条硬约束（✅ 同页归纳）：快捷方式是**只读**挂载；层级可嵌套但环路被平台拒绝；
每个湖有快捷方式数量与扫描配额（配额类数字属易变项，⚠️ 以当日页为准，本笔记不抄死数）。

心智模型 ⚠️：Shortcut ≈ UNIX 的 mount（不是 symlink 语义的全部），更精确的类比是
"**表目录级挂载 + 平台侧统一鉴权**"。它解决的是湖仓落地的最后一公里：数据主权在源团队手里，
工程师要的是"看起来在湖里"。

## 2.3 与数据共享、镜像的关系（本章边界声明）

- OneLake **data share**（跨组织分享，⚠️ 见 onelake-overview 导航项 delta sharing 线）与 Shortcut
  方向相反：Shortcut 把外部拉进来，share 把内部推出去（Delta Sharing 协议面）。
- 库→湖的持续复制由 Mirroring 承担，归本册 `06` 章，不在本章混讲。
- #221 通论册对 Shortcut 有平台地图视角的对应章：
  [../Fundamentals_of_Microsoft_Fabric/03-OneLake统一数据湖与快捷方式.md](../Fundamentals_of_Microsoft_Fabric/03-OneLake统一数据湖与快捷方式.md)
  ——两册同一产品面的"地图位 vs 岗位位"互文，读一册即可，深读对读。

## 2.4 🔧 实验 E1：零拷贝指针的最小模型（非 Fabric 行为）

本机实测（DuckDB 1.5.5，脚本 `D:\develops\tmp\dbwave_w9_degfab\exp.py`，输出 `exp_out.txt` 2026-10-02）：
以 20 万行事件表 Parquet（2.99 MB）为"外部湖文件"，两种"挂进湖里"的方式对比——

```text
[E1] shortcut-view create=1.22 ms; query rows=22222 sum=5513745.35 in 4.10 ms;
     view adds 0 bytes on disk; physical COPY materializes 0.35 MB (the duplication shortcut avoids)
```

- `CREATE VIEW sc_sales AS SELECT * FROM read_parquet('…/events.parquet') WHERE region='region-3'`：
  建"快捷方式"仅 1.22 ms，**磁盘增量为 0 字节**，查询时按需扫源文件（22,222 行 4.10 ms）。
- 对照组 `COPY … TO 'copy_sales.parquet'`：立刻物化 0.35 MB ——这就是"不用 Shortcut 的 ETL 团队"
  每挂一个源就付一次的复制税（存储×N、时效×快照日、一致性×对账）。
- 类比结论：Shortcut 的工程价值可量化为「O(复制) → O(指针)」；但注意本机 VIEW 无鉴权、无跨云
  网关、无配额与血缘登记——这些恰是 Fabric 在指针之上加的厂商件（⚠️ 转述 ✅ 文档）。

## 2.5 治理钩子：指针背后必须有连接管理

⚠️ 推定的本书工程提醒（机制依据 ✅ `onelake/onelake-shortcuts` 与 `security/security-overview`）：
快捷方式背后是"连接+凭据"，租户策略（敏感标签继承、外发保护、网络隔离）都挂在挂载点粒度上——
**挂载点即治理边界**。10 章讲 OneLake 目录/血缘时回收本节：Shortcut 在血缘图上表现为"源切换边"。

## 2.6 常见误区（⚠️ 编者归纳）

1. 把 Shortcut 当备份用——它只读且不落数据，源删即失，合规快照必须真复制。
2. 在 Shortcut 路径上写表——写路径只属于平台托管表（Lakehouse/Warehouse 自己的存储区）。
3. 跨云 Shortcut 当本地延迟——网络往返真实存在，重扫描负载应配下游物化层（medallion 银层，`09` 章）。
4. 忽略配额面——单湖快捷方式/扫描上限是软限制，规划期就要向容量所有者确认（`01` 章容量心智）。

## 2.7 与盘上诸书的联系

- 产品全景与湖安全：[../Fundamentals_of_Microsoft_Fabric/00-总览与阅读地图.md](../Fundamentals_of_Microsoft_Fabric/00-总览与阅读地图.md)。
- 开放表格式的中立视角（Shortcut 挂进来后"像表"需要什么条件）：
  [../Use_Iceberg_with_Spark/00-总览与阅读地图.md](../Use_Iceberg_with_Spark/00-总览与阅读地图.md)、
  [../Apache_Iceberg活用入門/00-总览与阅读地图.md](../Apache_Iceberg活用入門/00-总览与阅读地图.md)——
  Fabric 湖内默认 Delta 而非 Iceberg（⚠️ 现状以当日文档为准），两册是"如果客户坚持开放格式"的答案库。
- 湖仓两面对照：[../The_Data_Lakehouse/00-总览与阅读地图.md](../The_Data_Lakehouse/00-总览与阅读地图.md)。
- 🔧 工具书基线：[../DuckDB_Up_and_Running/00-总览与阅读地图.md](../DuckDB_Up_and_Running/00-总览与阅读地图.md)。
- 波内兄弟（#217/#218/#219/#220）：只登记不链（00 §8）。

## 核心概念速览（中英对照）

- **统一命名空间** — OneLake Namespace：租户级"一个湖"，abfss 路径寻址，容器对用户不可见 ⚠️✅。
- **快捷方式** — Shortcut：外部存储零拷贝挂进湖内路径；只读；挂载点即治理边界 ✅。
- **去桶化** — Bucket-free Storage：存储账户决策被平台吸收，工程面只剩逻辑层级 ⚠️。
- **一份数据多引擎** — One Copy, Many Engines：Spark/SQL/BI 同读一套 Delta/Parquet ✅。
- **数据共享** — Data Share（Delta Sharing 线）：向外的分享协议，与 Shortcut 方向相反 ⚠️。
- **连接与凭据** — Shortcut Connections：跨云/跨 SaaS 挂载的鉴权件，配额与审计挂此 ⚠️✅。
- **复制税** — Duplication Tax（编者词）：不用指针时每源一份物理拷贝的存储+时效+对账成本 🔧E1。
- **环路拒绝** — Cycle Rejection：快捷方式嵌套成环被平台禁止 ✅。
- **挂载点边界** — Mount-as-Governance-Boundary：敏感标签/网络策略在挂载粒度的落点（10 章回收）。
- **只读外表** — Read-only External Surface：Shortcut 语义的核心限定，写路径归托管表 ✅⚠️。

## 最新演进与工业实践

2024→2026（URL 均 2026-10-02 `curl` 实测 200；产品行为描述为文档转述 ⚠️）：

- **快捷方式面持续外扩**：当日 `onelake/onelake-shortcuts` ✅ 文档已列 GCS/S3 兼容/本地网关等
  多源矩阵，并配套 `onelake-shortcut-security`、`manage-shortcut-connections` 等专页
  （✅ 文件名实抓自 MicrosoftDocs/fabric-docs GitHub 仓库清单，00 §2#17）——"跨云零拷贝"
  从预览话术变成有安全专页的正式面。
- **文档重组警示**：旧路径 `/fabric/onelake/shortcuts-overview` 实测 404（00 §9 禁引清单），
  现行 `onelake-shortcuts`——工业实践引用 Fabric 文档必须当日重验（波5 #221 同款教训复现）。
- **湖资源治理件**：OneLake Explorer/文件级管理页在架（✅ onelake 域文件清单实抓）；配额数字类
  内容本册故意不抄——以当日页为准是本书对读者的纪律，也是本笔记的纪律。
- **工业实践画像**（⚠️ 通识推断，非本书内容）：多租户数据平台的"入湖"评审清单通常收敛为
  四问：数据主权在谁（→Shortcut 还是复制）、更新频率（→06 镜像还是 05 批集成）、格式（→03 Delta
  生命周期）、合规外发（→10 治理）——本章回答第一问。
- 书目侧：本册作者/出版年/印刷 ISBN 仍为 ⚠️ 未定谳项（00 §2/§4），演进节据此不写"本书第 2 版"
  之类未来时承诺；#221 姊妹册（Nikola Ilic/Ben Weissman，印刷 ISBN 978-1098172923）截至取证日亦未见
  第 2 版记录（⚠️ 其 00 同款登记）。
