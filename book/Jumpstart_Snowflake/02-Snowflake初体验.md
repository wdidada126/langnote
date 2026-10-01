# 02 Getting Started with Snowflake（pp.19–34 ✅ Crossref）

> 章定性：全书第一次"上手"章——开通试用、认界面、建立三层架构心智、摸一遍对象目录。
> 章题/页码/作者 ✅ Crossref 章级 DOI `10.1007/978-1-4842-5328-1_2`；小节结构 ⚠️ 推定；
> SQL 全部自拟教学示意；Snowflake 云产品不可本机实测，机制一律 ⚠️ 转述 + ✅ curl-200 URL。

## 1. 章节定位与叙事线

2019 时点的"Getting Started"实操链：注册 30 天试用（选云厂商+区域：AWS/Azure/GCP 三角色分工
的起点）→ 首次登录改密/建角色 → Classic Console 主界面导览（Shelves：Database/Warehouse/
Data Exchange/Admin）→ 用 UI 内建样例数据集走一遍建表/装载/查询 → 顺势讲解三层架构与对象
层级。本章把 01 章"hub 隐喻"落成可点击的界面元素，并为 03 章仓库参数、04 章装载向导铺路。
⚠️ 上述环节顺序按本书 step-by-step 体裁与 2019 官方快速入门推定，非样章实证。

## 2. 知识提纲（⚠️ 推定小节）

| # | 推定小节 | 2019 形态 | 2026 现状锚点 |
| --- | --- | --- | --- |
| 1 | 试用注册与区域选择 | AWS 俄勒冈默认 | 组织账户/多区域读回 ✅ account-usage 系 |
| 2 | 登录与安全基线 | 账密+建议 SSO | MFA/SSO/OAuth 全矩阵 ⚠️ |
| 3 | Classic Console 导览 | 五 Shelf 布局 | Snowsight 一统（2021 GA）⚠️ |
| 4 | 三层架构：云服务/虚拟仓库/存储 | 官方三色图 | 不变 ✅ warehouses-overview |
| 5 | 对象层级 DB>SCHEMA>表/视图/stage | 含共享数据库 | +Iceberg 表 ✅ tables-iceberg |
| 6 | 样例数据一键装载 | UI sample | 现文档 getting-started 线 ⚠️ |
| 7 | 第一个查询与结果下载 | 表格视图 | 工作表/故事 ✅ snowsql-use 并列生态 |

## 3. 深读与机制重构

**（a）三层架构的"读者版"表述**（⚠️ 转述，架构事实以官方为准）：云服务层（SQL 解析优化、
元数据、访问控制、查询编排）+ 虚拟仓库层（MPP 计算集群，查询缓存驻留本地 SSD）+ 存储层
（集中式对象存储上以微分区文件组织，详见 04 章与 🔧 E1）。三者独立扩缩是 01 章论点的具体化。
✅ https://docs.snowflake.com/en/user-guide/warehouses-overview 开篇即此模型。

**（b）对象目录的最小心智**（自拟示意，非书中原文）：

```sql
-- 层级：ACCOUNT > DATABASE > SCHEMA > (TABLE | VIEW | STAGE | PIPE | TASK | ...)
CREATE DATABASE demo;
CREATE SCHEMA demo.raw;
CREATE TABLE demo.raw.events(id BIGINT, payload VARIANT);   -- 09 章伏笔：VARIANT
CREATE STAGE demo.raw.mystore;                                -- 04 章伏笔：外部装载入口
SHOW OBJECTS IN SCHEMA demo.raw;                              -- 元数据即席盘点
```

**（c）多云 = 部署属性而非运行时属性**：注册时选定云厂商与区域后，数据驻留在该云；跨云
=另建账户。2019 语境这是"选型问题"，2026 已演化为"复制/容灾/近数据计算"问题 ⚠️，演进节再述。

**（d）UI 内建样例装载与 COPY 的分水岭**：本章用 UI 按钮体验装载（背后就是 04 章 COPY INTO
+自动临时 stage），让读者"先跑通再学原理"——本书教学法的一个刻意安排 ⚠️ 推定。

## 4. Console 导览的 2026 归宿速记（⚠️ 时代对照卡）

| 2019 Classic Console 元素 | 2026 归宿 | 备注 |
| --- | --- | --- |
| Databases Shelf | Snowsight Data/Worksheets | 层级不变 ✅ semistructured 页含示例 |
| Warehouses Shelf | Snowsight Admin>Warehouses | 参数面见 03 章 ✅ create-warehouse |
| Data Exchange Shelf | Snowflake Marketplace + Horizon | 10 章演进节展开 ⚠️ |
| Admin Shelf | Snowsight Admin 中心 | 07 章对位 ⚠️ |
| Worksheets（旧） | Snowsight Worksheets ✅ | 文档线 ui-snowsight 系 |
| 试用注册页 | 官方 getting-started-for-users 索引 | ✅ llms.txt 实抓 |

## 5. 深读问答（自拟）

**Q1：为什么 2019 书的界面导览如今几乎全部作废，架构导览仍可用？**
A：控制台是产品外壳（Classic Console→Snowsight 已整代更替 ⚠️），三层架构与对象层级是产品
内核，文档锚点至今在位 ✅ warehouses-overview、✅ data-types-semistructured（层级示例）。

**Q2：试用账户与生产账户的运营差异在哪？**
A：计费、保留期、资源监视器默认值与支持通道；本书不展开，波8 Tuning 册计费面深潜 ⚠️。

**Q3：本章"下载结果"为什么值得记？**
A：它是 10 章共享的对照面——下载=复制数据，共享=数据不动查询动；作者在此埋伏笔 ⚠️ 推定。

## 6. 与其他书/章联系

- 前接 01（认知），后启 03（仓库参数实操）、04（装载原理化）。
- [../Snowflake_The_Definitive_Guide/00-总览与阅读地图.md](../Snowflake_The_Definitive_Guide/00-总览与阅读地图.md)：其架构章为本章三层模型的"全量表"版本（波1 ✅）。
- [../Tuning_the_Snowflake_Data_Cloud/00-总览与阅读地图.md](../Tuning_the_Snowflake_Data_Cloud/00-总览与阅读地图.md)：从本章"能跑"到其"跑得省"（波8 ✅）。
- [../Advanced_Snowflake/00-总览与阅读地图.md](../Advanced_Snowflake/00-总览与阅读地图.md)：⚠️ 存在性未一手证实降级册，仅辨析（00 §4）。
- 同波 #164 Snowflake_Essentials：只登记不链（00 §5）。

## 7. 本章检验点（读完自测）

1. 不看笔记画出三层架构与对象层级两张图。
2. 说出注册时"云厂商+区域"决策影响什么、不影响什么。
3. 解释样例装载按钮背后对应的 SQL 语句族（COPY INTO，见 04 章）。
4. 区分"下载结果"与"共享数据库"两种数据流动语义（为 10 章准备）。

## 8. 取证与标注说明

章题/页码 ✅ Crossref `_2` 记录（pp.19–34）；机制现状 ✅ warehouses-overview / tables-iceberg /
account-usage / snowsql-use / data-types-semistructured（本轮 curl 200 名单）；UI 环节与小节
顺序 ⚠️ 推定；本章无 🔧（全册实验落点见 00 §6，云端 UI 无本地类比价值）。

## 核心概念速览（中英对照）

| 中文 | 英文 | 一句话释义 |
| --- | --- | --- |
| 云服务层 | cloud services layer | SQL 编译、元数据、访问控制的大脑 |
| 虚拟仓库 | virtual warehouse | 无共享 MPP 计算集群，可多仓并存 |
| 存储层 | storage layer | 微分区数据集中存储、全仓库共享 |
| 组织/账户 | account | 一次订阅的隔离边界，绑定一个云+区域 |
| 数据库/架构 | database / schema | 对象命名的两级容器 |
| 内部/外部暂存区 | internal / external stage | 文件装载的逻辑入口 |
| 查询缓存 | result & data cache | 仓库本地缓存，秒回重复查询 |
| 经典控制台 | Classic Console | 本书时代的 Web UI（后被 Snowsight 替代） |
| 样例数据集 | sample datasets | 免装载体验用的演示库 |
| 零拷贝共享 | zero-copy sharing | 见 10 章，本章以"下载"作反面对照 |

## 最新演进与工业实践

- **界面代际**：Classic Console 已退役，Snowsight 自 2021 GA 后成为唯一 Web 前台（工作表/
  仪表板/故事/ notebooks ⚠️）；本章截图式教学在 2026 只能作史料读。
- **入门路径官方化**：2026 文档以 `getting-started-for-users` 主题线组织 ✅（llms.txt 索引
  实抓）；组织账户（org-account）成为新账户默认标识格式 ✅（docs llms.txt 头部注记原文）。
- **湖仓入口并入**：试用者现在第一屏即可见 Iceberg 托管表 ✅
  https://docs.snowflake.com/en/user-guide/tables-iceberg，2019"样表+CSV"入门叙事已扩容。
- **工业实践**：企业落地普遍把"注册即治理"前置——SSO/MFA/网络策略在首个数据入库前配置；
  认证矩阵 ⚠️ 转述 ✅ https://docs.snowflake.com/en/user-guide/security-access-control-overview。
- **对本册读者的提示**：本章价值不在步骤而在心智模型；凡步骤与 2026 控制台冲突，以官方
  getting-started 线为准 ⚠️。
