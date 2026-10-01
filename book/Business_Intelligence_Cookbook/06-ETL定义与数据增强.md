# 06 · ETL 定义与数据增强（原书 Ch11 Defining the ETL/ELT + Ch12 Enhancing the Data）

> 证据分级同 [00](00-总览与阅读地图.md)：食谱题 ✅ 双源目录；内部论述 ⚠️ 题名级推定重构；Oracle 机制 ⚠️ 转述；
> 🔧 实验 E4/E4c 见 §3，**非 Oracle BI 行为**。Ch11（6 食谱）+ Ch12（6 食谱）= 装载与「装载之外」的半边：
> 前者定义数据怎么进来，后者给数据加上人工输入口与变更留痕。

## 1. 本文件范围与食谱全录（✅ 逐字题名）

### Ch11 Defining the ETL/ELT（6 食谱）

| # | 原食谱题（✅） | 拟译 |
| --- | --- | --- |
| 11.1 | Abstracting your source system | 抽象你的源系统 |
| 11.2 | Separating your extraction from your loading and transforming routines | 抽取与装载/转换分离 |
| 11.3 | Adding additional columns to facilitate error trapping and correction | 加辅助列以利捕获与纠正 |
| 11.4 | Designing ETL error trapping and detection routines | 错误捕获与检测例程 |
| 11.5 | Designing ETL data reconciliation routines | 数据对账例程 |
| 11.6 | Designing a notification routine | 通知例程 |

### Ch12 Enhancing the Data（6 食谱）

| # | 原食谱题（✅） | 拟译 |
| --- | --- | --- |
| 12.1 | Creating your application schema | 建应用模式 |
| 12.2 | Creating your application tables | 建应用表 |
| 12.3 | Developing the journal tables to track changes | 开发日志表追踪变更 |
| 12.4 | Defining the audit triggers | 定义审计触发器 |
| 12.5 | Defining the APEX Upload application | 定义 APEX 上传应用 |
| 12.6 | Creating the Upload interface | 建上传接口 |

## 2. 精读重构（⚠️ 题名级）

**11.1 Abstracting your source system**——问题：转换逻辑直接写死在源表上，源一改版全线崩。骨架 ⚠️：
为每个源系统建**视图/同义词抽象层**，ETL 只消费抽象层；源变更被隔离在抽象层重定义处。消费 8.4 源矩阵
（每个抽象对象=矩阵一行）✅ 结构咬合。2026 等价：source connector/快照层（ingest 层与 transform 层解耦）。

**11.2 E 与 L/T 分离**——问题：ETL 一体机式大脚本不可重放。骨架 ⚠️：三段流水线——抽取落 staging（保真原样）、
装载与转换各自独立可重跑；幂等设计（重跑不重复计数）。题名把 ELT 与 ETL 并写：本书承认两种编排方向，
判据=转换算力放源侧还是目标侧 ⚠️ 编者归纳。Oracle 机制 ⚠️ 转述：书中载体为 OWB 映射与 ODI 包
（ODI 12c 文档在线 ✅ https://docs.oracle.com/middleware/1213/odi/index.html ；OWB 永久链失效 ⚠️ 归档口径）。

**11.3–11.4 辅助列+捕获例程**——问题：坏数据混入仓库后无法定位责任段。骨架 ⚠️：11.3 给每张目标表加
装载审计列（批次号/来源/装载时间/状态位——与 10.9 标准列同族 ✅）；11.4 错误表+拒绝行（reject）模式：
违反约束/规则的行不阻断整批，落错误表待人工纠正后重放（「correction」即此）。2026 等价：DLQ/隔离区表+
重放作业。坑：错误表无「修复责任人」列，DLQ 变垃圾场。

**11.5 对账**——问题：「装载完成」≠「装载正确」。骨架 ⚠️：三层对账——行数（源 staging vs 目标）、
金额/关键度量 SUM、域值分布（复用 Ch9 剖析脚本做前后镜像比对 ✅ 题名级互证：9.x 脚本的消费者之一）。
对账失败挂 3.3 问题册（⚠️ 编者归纳的台账咬合）。2026 等价：自动化校验断言进 CI（05 §4 同路）。

**11.6 通知**——问题：装载窗口事故靠人肉盯控制台。骨架 ⚠️：分级通知（作业失败/对账不平/超时无数据），
路由到值班表；2012 载体为 DBMS_SCHEDULER 作业邮件或 ODI 拓扑告警 ⚠️ 转述（归档口径），2026 等价：
事件总线+IM/工单集成。

**12.1–12.2 应用模式与表**——问题：人工补充数据（预算/映射表/剔除清单）没有受控入口会走 Excel 邮件。
骨架 ⚠️：独立 application schema 与仓库 schema 隔离权限；应用表带 10.9 标准列与 12.3 journal。
**12.3–12.4 journal+审计触发器**——问题：人工数据可被无痕改写。骨架 ⚠️：journal 表记录每次
INSERT/UPDATE/DELETE 的前像/后像/操作人/时间（触发器实现），审计触发器守关键表。Oracle 机制 ⚠️ 转述：
Fine-Grained Auditing/触发器为 11g 既有件（11g 归档入口 ✅ https://docs.oracle.com/cd/E11882_01/index.htm ）。
**12.5–12.6 APEX 上传应用**——问题：给业务方一个带校验的网页上传口。骨架 ⚠️：APEX 向导建 Upload 应用
（CSV 解析→校验→写应用表→触发 journal），接口页限定数据录入员角色（与 Ch14 APEX 认证配方 ✅ 题名咬合：
14 章的自定义认证即保护此入口）。

## 3. 🔧 类比实验（非 Oracle BI 行为）

SQLite 3.45.3 触发器方案（本机实抓 2026-10-02，脚本 exp.py）：

- **E4**：20k 插入，带 journal+聚合表触发器 **32ms** vs 无触发器 **19ms**（开销 **1.70×**）——
  12.3/12.4 留痕机制的成本量级示范；Oracle 触发器/CDC 真实开销为 ⚠️ 文档转述域，本机不外推。
- **E4c**：预聚合表读 **0.052ms** vs 即时 SUM **11.242ms**（**216×**）——「维护费换查询费」的权衡曲线，
  对应 Oracle 物化视图/汇总管理动机（23ai DBMS_MVIEW ✅ https://docs.oracle.com/en/database/oracle/oracle-database/23/arpls/DBMS_MVIEW.html ，
  机制 ⚠️ 转述）。
- （E8 journal 行数核对见 [05](05-数据剖析与数据模型构建.md) §3，与本文件 12.3 同族。）

## 4. ETL→ELT 的体裁证词（⚠️ 编者归纳）

Ch11 题名并列「ETL/ELT」是 2012 年过渡期的化石证据：OWB 时代主流 ETL（过程语言生成物），ODI 时代
ELT（推给数据库引擎）兴起。本书以配方中立处理：11.2 的「分离」原则对两个方向同样成立——**抽取永远先行，
转换与装载的次序可换**。2026 年该争论以「ELT 胜出+云连接器化」收束 ⚠️ 转述（对照盘上
[../Analytics_Engineering_with_SQL_and_dbt/00-总览与阅读地图.md](../Analytics_Engineering_with_SQL_and_dbt/00-总览与阅读地图.md) ✅ 实链：
SQL 转换即代码的当代载体）。

## 5. 与 #207 的回链（其 00 §5「07 装载 ↔ OWB/ODI recipe」挂点兑现）

[../Oracle_Data_Warehousing_and_BI_Solutions/07-数据装载与ETL.md](../Oracle_Data_Warehousing_and_BI_Solutions/07-数据装载与ETL.md)（✅ 实链）
讲装载**工具面**（SQL*Loader/外部表/OWB 映射经济学，其 00 §9 E4/E5 实验），本文件讲装载**工程面**
（抽象/分离/捕获/对账/通知的例程设计）——同域不同层，互证不重复。

## 6. 坑与工程注记（⚠️ 编者综合）

1. 11.3 辅助列若进语义层暴露给报表用户，会被当成业务字段聚合——须在 Ch13 别名层屏蔽（跨章咬合）。
2. 12.4 触发器方案在批量装载时先禁用后补审计，否则 E4 的 1.70× 在百万行时变 1.70× 的全量灾难 ⚠️ 类比警示。
3. APEX 上传（12.5/12.6）的校验规则与 6.2 业务规则**同源不同码**——两处各写一份必然漂移，宜共享校验域表。
4. 11.6 通知若无抑制窗（维护窗静默），值班疲劳会漏掉真事故 ⚠️ 编者补位。

## 核心概念速览（中英对照）

| 英文（✅ 原题） | 中文拟译 | 一句释义 |
| --- | --- | --- |
| source abstraction | 源抽象 | 以视图/同义词隔离源 schema 变更 |
| extraction / loading / transforming separation | 抽/装/转分离 | 三段可独立重跑的流水线 |
| ELT vs ETL | 转换算力位置 | 目标库内转换 vs 中间引擎转换 |
| error trapping / detection | 错误捕获/检测 | 拒绝行落错误表不阻断批次 |
| data reconciliation | 数据对账 | 行数/度量/分布三层前后镜像比对 |
| notification routine | 通知例程 | 分级事故路由到值班 |
| application schema | 应用模式 | 人工数据与仓库数据的权限隔离 |
| journal table | 日志表 | 前像/后像/操作人的变更留痕 |
| audit trigger | 审计触发器 | 关键表的强制留痕机制 |
| APEX Upload application | APEX 上传应用 | 带校验的网页受控录入口 |

## 最新演进与工业实践

- **装载引擎**：OWB 终态停售 ⚠️ 归档口径；ODI 12c 文档在线 ✅（§2 URL）、云侧 OCI Data Integration 承接
  （公开精确文档链 404，见 00 §11 弃用清单，不编 URL）；SQL*Loader/Data Pump 仍为现行装载件 ⚠️ 转述
  （19c 工具指南链波9 已验 ✅）。
- **对账/断言**：11.5 三层对账制度化为数据可观测性（新鲜度/体量/分布/血缘四信号）⚠️ 编者归纳。
- **人工数据入口**：12.5 APEX 上传的当代等价仍是 APEX（现行文档 ✅
  https://docs.oracle.com/en/database/oracle/application-express/ ）+ 通用等价「带治理的电子表格回写」。
- **审计**：12.3/12.4 触发器方案在云数仓多被平台级变更捕获（CDC 服务/时间旅行）替代 ⚠️ 转述；
  journal 语义由表快照 diff 承接。
- 工业实践注记：11.2「分离」+11.5「对账」是数据工程里最少被跳过的两条老配方——新栈换名字不换骨架 ⚠️ 编者归纳。
