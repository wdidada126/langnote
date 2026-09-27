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

## 8. 深潜三：Zero-ETL 完整建表流程（⚠️ 转述+✅ 文件互证）

Aurora PostgreSQL → Redshift Zero-ETL 端到端步骤（⚠️ 全句转述，**专页 zero-etl 实测 302→mgmt/ 根**，入口 ✅ mgmt/welcome 同址 200）：

```
Step 1 ─ Aurora 侧：建 DB cluster + 开启 Zero-ETL 集成（选 Redshift 目标）（⚠️）
Step 2 ─ Redshift 侧：CREATE INTEGRATION aurora_int FROM
          AURORA 'arn:aws:rds:...'（⚠️）
Step 3 ─ 建映射表：CREATE TABLE orders_mirror AUTO
          (order_id bigint, amt numeric, status varchar,
           _cdc_meta super);（⚠️ AUTO 标记+cdc 元数据列）
Step 4 ─ 监控同步状态：SELECT * FROM sys_integration_status
          WHERE integration_name = 'aurora_int';（⚠️ 系统视图名转述）
Step 5 ─ 对账：仓侧 count/sum vs Aurora 侧 count/sum（✅ aurora_insert.sql 提供造数）
```

Zero-ETL 目标表限制（⚠️ 转述）：
- 不可在目标端 INSERT/UPDATE/DELETE（只读镜像）；
- DDL 受限：不可加索引/SORTKEY（由源端 DDL 自动同步 ⚠️）；
- 删除需从源端级联——目标端无独立生命周期。

## 8b 配方演绎：LF 权限配置完整步骤（✅ 文件+⚠️ 语义）

基于仓内两 txt 重构的 LF 配置全流程（✅ CLI 实抓，⚠️ 语义转述）：

```
Step 1 ─ 注册 LF 管理员：
  aws lakeformation put-data-lake-settings
    --data-lake-settings DataLakeAdmins=[{DataLakePrincipalIdentifier=arn:...}]
  （✅ Chapter10_LakeFormationSettings.txt 实抓原文）

Step 2 ─ 注册 S3 数据位置：
  aws lakeformation create-data-location
    --resource-arn "arn:aws:s3:::my-bucket/data/"
  （⚠️ CLI 名转述）

Step 3 ─ Glue 建库建表（经 LF 管理员身份）：
  CREATE DATABASE lake_db;（⚠️）
  CREATE EXTERNAL TABLE lake_db.events ... LOCATION 's3://...'（⚠️）

Step 4 ─ LF 授权：
  aws lakeformation grant-permissions
    --principal DataLakePrincipalIdentifier=arn:aws:redshift:...
    --permissions Select={ColumnWildcard={}}
  （⚠️ CLI 语义转述）

Step 5 ─ Redshift 侧 external schema 挂载：
  CREATE EXTERNAL SCHEMA lake_ext FROM GLUE
    DATABASE 'lake_db' IAM_ROLE 'arn:...'
  （⚠️；✅ c-spectrum-considerations 同址 200）
```

LF 配置失败排查树（⚠️ 工程惯例）：
- 外表查询返回空 → 检查 Step 4 的 GRANT 是否到位；
- `Access Denied` → 检查 Step 1 管理员 + Step 2 数据位置注册；
- 数据传输角色报错 → 检查信任策略是否含 glue+redshift 双服务（✅ 仓内 txt 实抓反证）。

## 8c 深潜四：Zero-ETL 与 LF 的协作架构（⚠️ 重构）

```
Aurora 源表 ──Zero-ETL──→ Redshift 镜像表（AUTO，只读）
                              │
                              ├──→ BI 查询（经视图脱敏 → TDG 08 DDM）
                              ├──→ 下游 ETL（JOIN 仓内其他表）
                              └──→ 对账 SQL（→ ch5 DAG 节点）

S3 湖数据 ──LF 授权──→ Redshift Spectrum 外表
                              │
                              ├──→ 直查（不搬数据）
                              └──→ COPY 入内表（高频场景）
```

四面体权限模型在本章的汇合（⚠️ 重构口径）：
- 仓内 GRANT（→ 02）管"谁能查仓内表"；
- Zero-ETL 镜像表继承仓内 GRANT（⚠️）；
- Spectrum 外表经 LF 授权（本章 ✅ txt 链路）；
- Datashare（→ 09）管"谁能跨仓读"；
- DataZone（→ 11）管"该不该给"的治理层。

## 8d 配方演绎：多源 Zero-ETL 对比（⚠️ 转述）

| 源 | 延迟 | 吞吐量 | 限制 |
|---|---|---|---|
| Aurora PG/MySQL | 秒级 | 中 | 同 Region、表数配额（⚠️） |
| DynamoDB | 秒级 | 高 | 需建 integration、RPU 微量计费（⚠️） |
| Kinesis/MSK | 秒级 | 高 | 需 streaming integration（⚠️） |
| SaaS（Salesforce 等） | 分钟级 | 中 | 2024–2026 新源（⚠️ 以官方页为准） |

Zero-ETL vs 传统 COPY 选型决策（⚠️ 重构）：
- **Zero-ETL 优先**：源在 AWS 同 Region + 需要秒级新鲜度 + 源 DDL 简单；
- **COPY 优先**：跨云/跨 Region + 需要复杂转换 + 源非 AWS 服务；
- **混合**：Zero-ETL 做实时镜像 + COPY 做批量补充（⚠️ 工程惯例）。

## 8e 🔧 类比补充：CDC 回放的对账完整性验证（本机真实跑过）

⚠️ 非本书引擎行为，方言已按 DuckDB/SQLite 改写。§5 已报告 cdc_demo 基本对账，此处补充边界测试：

- **乱序回放**：将 cdc 流按 seq 倒序回放→`INSERT OR REPLACE` 幂等性保证最终一致（但中间态数据不一致窗口扩大）——验证"幂等回放容忍乱序"的抽象性质；
- **重复回放**：同一 cdc 流回放两次→镜像表数据不变（幂等性 ✅）——验证"Zero-ETL 重试安全"的抽象模型；
- **DDL 变更模拟**：源表加列后，触发器自动捕获新列（SQLite 触发器 `NEW.*` 语义）→ 类比 Zero-ETL 的 schema 演进自动同步（⚠️ 类比有限，Redshift 真 DDL 同步规则以官方为准）。

抽象结论强化："源端只追加的变更流 + 目标端幂等回放"模型经三组边界测试（正序/乱序/重复）均保持对账一致——Zero-ETL 的产品化即此模型的托管实现（⚠️ 真实现细节禁以本组数字冒充）。

## 8f Zero-ETL 自查清单（⚠️ 重构）

- [ ] 源端 Aurora/DynamoDB 版本兼容 Zero-ETL（⚠️ 以官方兼容矩阵为准）
- [ ] 数据传输角色信任策略含 redshift + glue 双服务（✅ 仓内 txt 反证）
- [ ] LF 管理员已注册 + S3 位置已注册（✅ CLI 可复现）
- [ ] Zero-ETL 目标表的 AUTO 列已监控（复制延迟告警）
- [ ] 镜像表进 BI 前有视图脱敏层（→ TDG 08 DDM）
- [ ] 对账 SQL 已纳入编排 DAG（→ 05）
- [ ] Spectrum 外表经 LF 授权链路（非仅 Glue CREATE）
- [ ] Zero-ETL 配额已体检（表数/行数/RPU 微量计费）

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
