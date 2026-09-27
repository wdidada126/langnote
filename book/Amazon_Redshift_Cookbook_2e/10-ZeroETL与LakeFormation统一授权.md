# 10 Zero-ETL 与 Lake Formation 统一授权（2e Ch10）

> 取证强度：✅ 强（官方 2E 仓 Chapter10 实抓四件：`Chapter10_DataTransferRoleAndLakeFormation.txt`——redshift+glue 双服务信任策略的建角脚本、`Chapter10_LakeFormationSettings.txt`——`aws lakeformation put-data-lake-settings` CLI 全文、`aurora_postgresql_orders_insert.sql`（orders 表造数）、`part.tbl`；另有 chapter_10_CFN.yaml）。提交史：aurora/part 两件 2025-03-18 由 ch9 挪入（✅ 00 §5）——**2e 把 OLTP 直连与湖授权编进同一章，恰是 Zero-ETL+LF 组合拳的摆位**。
> 三态：✅ URL/命令实证｜⚠️ 转述推定｜🔧 DuckDB/SQLite 类比（**非 Redshift 行为，方言已按 DuckDB 改写**）。

## 1. 本章定位

2024 年 Redshift 最重的一新：**Zero-ETL 集成**（Aurora/DynamoDB/MSK 等源→Redshift 免管道自动复制，秒级新鲜度）+ 湖权限总闸 **Lake Formation**（跨 Glue/S3/Redshift 的统一授权面）。仓内两 txt 即证：先建"数据传输角色"（信任 redshift.amazonaws.com + glue.amazonaws.com），再往 LF 数据湖设置里注册——**没有这两步，外表与集成都跑不通**（✅ 文件内容实抓）。

## 2. 配方地图

| 配方 | 机制 | 取证 |
|---|---|---|
| LF 管理员与权限栈 | `put-data-lake-settings`（DataLakeAdmins）+ GRANT DATA location；仓内 CLI 逐字可复现 | ✅ txt 实抓；⚠️ LF 语义转述 |
| 数据传输角色 | 信任策略双服务主体 redshift+glue（跨服务代理取数） | ✅ txt 实抓（含 sts:AssumeRole） |
| Aurora→Redshift Zero-ETL | 建库→`CREATE TABLE ... AUTO`（cdc 自动列）→集成面板选源→表实时出现 | ⚠️ 转述；**专页 zero-etl/working/overview 实测 302→mgmt/ 根（2026-09-28 改版登记）**；入口 ✅ https://docs.aws.amazon.com/redshift/latest/mgmt/welcome.html 同址 200 |
| orders 造数与对账 | aurora_postgresql_orders_insert.sql 灌 OLTP 侧，仓侧查镜像表验证延迟 | ✅ 文件实抓（姿势重构 ⚠️） |
| 受控目录/单元 | LF Tag-based 控制访问（LGFC）⚠️ | 转述 |
| 与 Spectrum 合流 | external schema 经 LF 授权后直读 | ⚠️ 转述；✅ https://docs.aws.amazon.com/redshift/latest/dg/c-spectrum-considerations.html 同址 200 |

## 3. 深潜一：Zero-ETL 的工程含义（⚠️ 转述+✅ 盘上互证）

1. 管道消失：CDC/重试/schema 变更/回填全托管——"本章代码只剩建表与对账"正是 2E 仓 ch10 文件族的显影（✅ 无 pipeline 代码、只有造数与授权脚本——**这是比任何目录都硬的间接证据**）；
2. 表语义：`AUTO` 列/进度列暴露复制位点；不可在目标端写、DDL 有限制（⚠️）；
3. 计费与配额：按 RPU/行数微量计费，单表体量上限需体检（⚠️ 数字不编，以官方页为准）；
4. 适用边界：源必须同 Region 同或可打通网络；跨云/跨大洲仍是 04 的传统管道（⚠️）。
5. 同书对照：DynamoDB 源配方在 ch3 已露一头（CreateAndLoad_dynamodb.py 手动路 ⚠️→本章自动路 ✅ 摆位推断）。

## 4. 深潜二：LF 双层授权心智（✅ 文件+⚠️ 语义）

- **位置层**：S3 前缀注册为 LF 资源（DataLakeSettings 里 admin 决定谁能注册）；
- **库表列层**：GRANT SELECT 到 IAM role/身份，Redshift external schema 声明 `EXTERNAL DATABASE ... IAM_ROLE` 时按 LF 有效权限过滤可见对象——"仓看湖=湖的规矩"（⚠️ 转述；✅ Spectrum 锚）；
- 与仓内 GRANT（→02）、仓间 Datashare（→09）、目录治理（→11）拼成完整四面体（本章重构口径）。

## 5. 🔧 类比：变更数据捕获的最小可测核（本机真实跑过）

SQLite 3.45.3 触发器伪 CDC：源表 `orders` + `AFTER INSERT/UPDATE` 触发器把变更追加进 `orders_cdc` 流；灌 **2000 INSERT + 666 UPDATE → cdc 捕获 2666 行**；按 seq 顺序以 `INSERT OR REPLACE` 幂等回放进镜像表 `orders_mirror`：**回放 2ms，对账读回 (2000 行, 金额和 95950.0, PAID=666) 与源侧完全一致**（脚本 cdc_demo.py 同款逻辑、输出 cdc_demo_out.txt，存 tmp/dbwave_w5_rscb/；**非 Redshift 行为，SQLite 语法仅为 CDC 抽象演示**）。抽象结论迁移："源端只追加的变更流+目标端幂等回放"就是 Zero-ETL 的黑盒最小模型；Redshift 把它产品化到免运维（⚠️ 真实现细节禁以本组数字冒充）。

## 6. 常见坑与最佳实践（⚠️ 转述+✅ 锚）

1. LF 与 Glue 权限双账本：只给 Glue CREATE 没进 LF 授权=外表空转（经典排障第一步）；
2. 数据传输角色信任策略漏 glue（仓内 txt 双服务主体的意义，✅ 实抓反证）；
3. Zero-ETL 目标表加列易、改型难——schema 演进策略先设计（⚠️）；
4. 镜像表进 BI 前补一层视图脱敏——OLTP 裸列全量过来常带敏感列（⚠️→TDG 08 DDM，✅ 盘上文件）；
5. 对账 SQL 化：aurora insert 的行数/校验和 vs 仓侧镜像，写进 ch5 的 DAG（✅ 文件族组合推断 ⚠️ 细节）。

## 7. 系列互链

- 概念版：[../Amazon_Redshift_TDG/03-设置您的数据模型和摄入数据.md](../Amazon_Redshift_TDG/03-设置您的数据模型和摄入数据.md)（Zero-ETL 三分支其一）与 [../Amazon_Redshift_TDG/08-数据保护和管理.md](../Amazon_Redshift_TDG/08-数据保护和管理.md)（LF/权限面）；
- DynamoDB 源专册（盘上）：[../Amazon_DynamoDB_TDG/00-总览与阅读地图.md](../Amazon_DynamoDB_TDG/00-总览与阅读地图.md)（云仓长尾三角外的同源服务）；
- Snowflake/BQ 的免管道对照：[../Advanced_Snowflake/08-数据摄入进阶.md](../Advanced_Snowflake/08-数据摄入进阶.md)、[../Google_BigQuery_TDG/04-将数据加载到BigQuery.md](../Google_BigQuery_TDG/04-将数据加载到BigQuery.md)；
- 湖权限的开源面：[../bigdata/09-存储与文件格式.md](../bigdata/09-存储与文件格式.md)。

## 核心概念速览（中英对照）

- Zero-ETL 集成 — zero-ETL integration：OLTP/流源到仓的免管道自动复制
- CDC — change data capture：行级变更流，Zero-ETL 的引擎室
- 数据传输角色 — data transfer role：redshift+glue 双信任的服务代理角色
- Lake Formation — LF：湖统一授权面（位置层+库表列层）
- 数据湖设置 — DataLakeSettings：LF 管理员与外部 Hive 注册总配置
- Tag-based 访问 — LGFC：以标签批量授权的控制访问
- AUTO 列 — auto progression columns：镜像表的复制位点暴露列
- 镜像表 — mirror table：源表在仓内的实时副本（只读）
- external schema — 外部模式：仓看湖/看 RDS 的挂载点
- 对账 — reconciliation：源/目标行级校验和闭环
- 受控目录 — governed table：LF 注册后可跨引擎统一鉴权
- 四面体权限观 — GRANT/datashare/LF/DataZone：02/09/10/11 的合成心智（本章重构）

## 最新演进与工业实践

- **源清单扩张（2024→2026）**：Aurora（PG/MySQL）之后 DynamoDB、Kinesis、MSK、SaaS（Salesforce 系）陆续入列，Zero-ETL 从"功能"升格为"默认摄入范式"（⚠️ 转述；✅ 主站 https://aws.amazon.com/redshift/ 200 实测 2026-09-28 为现状入口）。
- **统一数据体验**：Redshift/SageMaker Lakehouse/Glue 同坐 LF+Iceberg 底座，"一份湖数据多引擎按同一授权查"为 2025+ AWS 主叙事（⚠️ 转述；对照波内兄弟册 `book/Fundamentals_of_Microsoft_Fabric/` 的 OneLake 同款野心——**同波兄弟只登记不链**，见 00 §10B）。
- **工业实践**：Zero-ETL 落地三查（源 DDL 限制/配额/脱敏层），替代了一半"简单 Kafka 管道"外包工作量（⚠️ 转述）。
- **取证提醒**：本章两 txt 为全仓 CLI 密度最高的授权实证——复现即从 put-data-lake-settings 抄起（✅ 原文可用）。
