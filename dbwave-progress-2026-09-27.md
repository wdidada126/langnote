# 数据库目录版工程·进度快照（2026-09-27 深夜快照）

> 本文件为人工编辑友好版进度存档。后续接续会话时，主代理读此文件即可恢复状态。
> 累计完成：**80 / 224**

---

## 一、波次总览

| 波次 | 总数 | 已验收 | 在飞 | 累计 |
|---|---|---|---|---|
| 波 1-3 | 42 | 42 ✅ | 0 | 42/224 |
| 波 4 | 14 | 12 | 2 (#177/#117) | 54/224 |
| 波 5 | 14 | 10 | 4 (#28/#48/#54/#165) | 64/224 |
| 波 6 | 14 | 2 | 12 | 68/224 |
| 波 7-15 | 126 | 0 | 0 | — |
| **合计** | **224** | **80** | **18** | **80/224** |

---

## 二、波 4 已验收（12/14）

| # | 目录 | 备注 |
|---|---|---|
| 155 | Advanced_Snowflake | 14 通道全阴，人工裁定存在性 ⚠️ |
| 189 | Data_Governance_in_the_Era_of_AI_2e | 0642 异形号判决 |
| 13 | Database_Design_Know_It_All | |
| 14 | Seven_Databases_in_Seven_Weeks_2e | |
| 46 | Google_BigQuery_TDG | |
| 56 | Amazon_Redshift_TDG | |
| 58 | Amazon_DynamoDB_TDG | |
| 113 | Introduction_to_Apache_Flink | 作者未获证 ⚠️ |
| 17 | What_Is_Database_Design_Anyway | ISBN 异形号 ⚠️ |
| 178 | Understanding_Data_Governance | |
| 160 | Developing_with_Couchbase_Server | 14 通道全阴，人工裁定 ⚠️ |
| 195 | Advanced_Analytics_with_Spark_2e | |

**在飞 2 本**：
- #177 BigQuery（书名待补）
- #117 Couchbase（书名待补）

---

## 三、波 5 已验收（10/14）

| # | 目录 | 备注 |
|---|---|---|
| 57 | Database_Design_for_Mere_Mortals_3e | |
| 27 | Data_Model_Patterns | |
| 16 | Fundamentals_of_Database_Indexing | |
| 9 | Oracle_Performance_Tuning_2e | 3 章 thin，在修 |
| 47 | MySQL_8_Administrators_Guide | 14 章 thin，在修 |
| 86 | Learn_PostgreSQL_2e | 13 章 thin，在修 |
| 100 | PostgreSQL_High_Performance_Cookbook | |
| 221 | Fundamentals_of_Microsoft_Fabric | 作者未获证 ⚠️ |
| 226 | Fundamentals_of_Data_Observability | |
| 63 | SQL_Server_2014_Query_Tuning | 作者 "McGiffen" 零证据，TOC 推定重建 ⚠️ |

**在飞 4 本（仍在修 thin 章）**：
- #28 Oracle_Performance_Tuning_2e（3 thin）
- #48 MySQL_8_Administrators_Guide（14 thin）
- #54 Learn_PostgreSQL_2e（13 thin）
- #165 Amazon_Redshift_Cookbook_2e（9 thin）

---

## 四、波 6 已验收（2/14）

| # | 目录 | 备注 |
|---|---|---|
| 210 | Data_Fabric_as_Modern_Data_Architecture | 14 通道全阴，人工裁定 ⚠️ |
| 186 | Data_Governance_Elsevier | |

**在飞 12 本**：
- #209 Data_Fabric_Architectures
- #212 Principles_of_Data_Fabric
- #202 Data_Fabric_and_Data_Mesh_with_AI
- #188 Data_Governance_in_the_Era_of_AI_2e（波4 已收，波6 为兄弟登记补充）
- #192 Data_Governance_with_Unity_Catalog
- #223 What_Is_Data_Observability
- #136 Data_Lakehouse_in_Action
- #224 Data_Observability_for_Data_Engineering
- #174 Apache_Polaris_TDG
- #163 Analytics_Engineering_with_SQL_and_dbt
- #173 Unlocking_dbt
- #215 Spark_The_Definitive_Guide

---

## 五、勘误总账（本会话 +18 条，累计见总索引）

### 系统性勘误（所有波次通用）
1. **Crossref /isbn/ 路由下线**：`api.crossref.org/isbn/<isbn>` 全部 404；必须改用 `api.crossref.org/works?filter=isbn:<isbn>`
2. **O'Reilly/Packt ISBN 整批不在 Crossref**："not found" = 覆盖缺口，非否定证据
3. **AWS docs 2025-26 批次 302→root**：所有 docs.aws.amazon.com 链接需实测，不可盲信
4. **docs.oracle.com /23/ → 301→/26/**：23ai→26ai 重命名证据

### 单册勘误
- #160 Advanced Snowflake：14 通道全阴，存在性 ⚠️
- #210 Data Fabric MDA：14 通道全阴，存在性 ⚠️
- #63 SQL Server 2014 Query Tuning：作者 "McGiffen" 零证据（Crossref 只有 Apress Matthew McGiffen 加密书），TOC 推定重建 ⚠️
- #17 ISBN 异形号 ⚠️
- #113 Flink 作者未获证 ⚠️
- #155 Advanced Snowflake 作者未获证 ⚠️
- #221 Microsoft Fabric 作者未获证 ⚠️
- 总索引 line 67 MariaDB 署名修订：彭立勋→张金鹏/张成远（Douban 26340413）
- 总索引 line 310 DMD5e 署名修订：Silverston 5e→Teorey/Lightstone/Nadeau/Jagadish 5e

---

## 六、验收 checker 路径

| 波次 | checker 路径 |
|---|---|
| 波 4 | `D:\develops\tmp\dbwave_close4\check.py` |
| 波 5 | `D:\develops\tmp\dbwave_close5\check.py` |
| 波 6 | `D:\develops\tmp\dbwave_close6\check.py` |

运行方式：`python check.py [dir_name...]`（不传参=全波 14 目录）

---

## 七、规范文件路径

| 文件 | 用途 |
|---|---|
| `D:\develops\tmp\dbwave-common.md` | 基础规范（所有波次通用） |
| `D:\develops\tmp\dbwave-w2-common.md` | 波 2 补充 |
| `D:\develops\tmp\dbwave-w3-common.md` | 波 3 补充 |
| `D:\develops\tmp\dbwave-w4-common.md` | 波 4 补充 |
| `D:\develops\tmp\dbwave-w5-common.md` | 波 5 补充 |
| `D:\develops\tmp\dbwave-w6-common.md` | 波 6 补充 + 波 7-9 草案 |

---

## 八、剩余波次计划（草案，波 6 规范尾部已登记）

### 波 7·引擎长尾收官（14）
- SQL Server 余三：#35 2008 Internals（盘上中文单文件→目录版升级）、#68 Advanced Troubleshooting、#71 2022 Inside Out
- Oracle 余四：#44 Oracle Essentials 5e、#61 Oracle Security、#66 Problem Solving Handbook、#74 Oracle Internals Intro
- DB2 三册：#75/#76/#77
- 安全：#51 Database Hacker's Handbook
- 原理收尾：#93 Databases Illuminated 4e、#222 Modern Data Architectures with Python
- NoSQL 抽一：#103 Advanced Elasticsearch 7.0

### 波 8·大数据流批+云仓长尾（14）
- Spark 七册：#216 HPS 2e、#196 Learning Spark 2e、#150 Modern DE with Spark、#152 Beginning Spark 3、#154 Spark Cookbook、#193 Spark 2、#194（含 #153 Wiley 版查重）
- 流批四册：#156 Streaming Architecture、#157 Real-Time Analytics、#199 Unlocking Value RTA、#166 Rise of Operational Analytics
- 云仓抽一：#214 Tuning the Snowflake Data Cloud

### 波 9·Azure/Fabric 余量+数仓方法论（14）
- Azure 线：#217/#218/#219/#220/#191（0642 号先例）/#146/#147
- 数仓方法论：#142/#143/#145/#168/#205/#206/#204/#207 择 7（#207 与 #204 同作者团查重）

### 波 10-15·NoSQL 多+湖仓余量清尾（约 5-6 波收官）
- ES 余 #99/#101/#102/#104/#105/#122/#123
- Cassandra 余 #97/#110/#111/#126/#129/#130
- Mongo 余 #80/#84/#106/#108/#128
- Redis 余 #82/#85/#131
- Neo4j 余 #91/#96/#133
- DynamoDB 余 #109/#112/#114
- Couch 系 #115–#120、#125 Seven NoSQL
- 湖仓余 #137/#140/#141/#144/#149(0642)/#170/#171/#172/#187/#203
- 原理余 #1/#2/#3/#5/#6/#10/#18/#19/#21/#22/#24/#26
- Oracle 余 #41/#43/#59/#60/#67/#72/#78
- 云仓余 #158/#161/#162/#164/#165✓w5/#179–#183/#211/#213
- 治理余 #185/#190✓/#208/#223✓w6 等

**全部 224 本预计第 14-15 波收满。**

---

## 九、Git 状态

- 最新提交：`bb86bd02` "book: 数据库目录版·波4-6验收登记（累计79/224）——波4 12/14、波5 9/14、波6 2/14；勘误总账+18条；总索引 DMD5e/MariaDB 署名两处修订"
- 并行会话提交：`ea773f2b` "add"（22:20 by somessyy，已提交所有新波目录）
- 远端：三远端已推（待下次提交后同步）

---

## 十、待人工裁定项（非阻塞）

| 项 | 类型 | 备注 |
|---|---|---|
| RTCP 06 ASSERT | 复核 | |
| TOP 3e 疑云 | 版次 | |
| ES print 403 | 取证 | |
| DUAR librowndev 镜像 | 取证 | |
| EDC 双谱系 | 辨析 | |
| #92 辨析 D | 辨析 | |
| #190/#124 作者 ⚠️ | 作者 | |
| PGHP3e 版次标签 | 版次 | |
| #155/#113/#221 作者未获证 | 作者 | |
| #17 ISBN 异形号 | ISBN | |
| #160/#210 存在性 | 存在 | 14 通道全阴 |
| #63 作者/TOC | 作者+TOC | McGiffen 零证据 |

---

## 十一、接续会话启动清单

1. 读 `D:\develops\tmp\dbwave-w6-common.md` 获取波 6 规范 + 波 7-9 草案
2. 读 `D:\develops\tmp\dbwave-common.md` 获取基础规范
3. 运行对应波次的 `check.py` 确认在飞书目状态
4. 波 4 收尾：等 #177/#117 返回 → 验收 → 波4 收束三件套（closure 脚本 + 补充文件登记 + 总索引波4节 + 提交推送）
5. 波 5 收尾：等 #28/#48/#54/#165 修 thin 章返回 → 验收 → 波5 收束三件套
6. 波 6 继续：12 本在飞，逐本验收 → 波6 收束三件套
7. 波 7 发射前：按 w6 规范尾部名册，先做中译反查+盘上查重，再发射

---

*快照生成时间：2026-09-27 深夜*
*下次更新：波 4/5/6 在飞书目全部返回并验收后*
