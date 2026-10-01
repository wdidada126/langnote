# 07 Snowflake Administration（pp.107–128 ✅ Crossref）

> 章定性：管理面总章——用户/角色/授权骨架、资源监视器、用量观测与" edition 决定保留期/能力"
> 的订阅心智。章题/页码 ✅ Crossref `_7`；小节 ⚠️ 推定；SQL 自拟示意；机制 ⚠️ 转述 +
> ✅ curl-200 URL；本章无独立 🔧（成本观测类比归 03/04 章实验组）。

## 1. 章节定位与叙事线

本书从"会用"跨到"能带团队用"的一章：先立**角色金字塔**（ACCOUNTADMIN/SYSADMIN/SECURITYADMIN/
USERADMIN + 业务自建角色），再讲**授权经济**（GRANT OF ROLE 与对象 USAGE 两条线），然后进入
**钱的仪表盘**——资源监视器（RESOURCE MONITOR）如何给仓库/账户封顶与告警；收尾是版本订阅
（Standard/Enterprise/Business Critical/VPS ⚠️ 2019 名录）对 Time Travel 上限、合规特性的决定
作用（与 14 章直接联动）。本章与 08 章构成治理双联：07 管组织与成本，08 管信任与权限语义。

## 2. 知识提纲（⚠️ 推定小节）

| # | 推定小节 | 要点 | 现状锚点（✅ curl-200） |
| --- | --- | --- | --- |
| 1 | 内置角色层级 | SYSADMIN 建对象/SECURITYADMIN 管身份 | user-guide/security-access-control-overview |
| 2 | 用户与登录策略 | 命名规范/密码策略/SSO 衔接 | security-access-control-overview ⚠️ |
| 3 | 授权两轴 | GRANT <role> TO ROLE / GRANT USAGE ON ... | 同上 |
| 4 | 主角色与默认角色 | PRIMARY ROLE/DEFAULT ROLE 会话行为 | 同上 ⚠️ |
| 5 | 资源监视器 | 阈值/动作(SNOOZE·SUSPEND·通知)/频率 | user-guide/resource-monitors |
| 6 | 用量账本 | metering/query/load 历史视图族 | sql-reference/account-usage/warehouse_metering_history |
| 7 | 订阅版本与能力矩阵 | 保留期/合规/支持差异 | editions 具体页未验真 ⚠️（见 §8） |
| 8 | 任务与依赖入门 | CREATE TASK 定时 SQL 编排 | sql-reference/sql/create-task |

## 3. 深读与机制重构

**（a）角色骨架（自拟示意，非书中原文）**：

```sql
-- 治理三件套：身份域、权限域、成本域
GRANT ROLE ingester   TO ROLE sysadmin_stub;           -- 角色图>角色名：先设计图再发权限
GRANT USAGE ON DATABASE sales TO ROLE analyst_ro;
GRANT SELECT ON ALL TABLES IN SCHEMA sales.core TO ROLE analyst_ro;
ALTER USER analyst_01 SET DEFAULT_ROLE = analyst_ro, DEFAULT_WAREHOUSE = 'wh_bi';
```

设计口诀（本章时代精神）：**人→低权限业务角色→（GRANT OF）→框架角色→内置金字塔**；对象授权
尽量打在 SCHEMA 层以控爆炸半径 ⚠️ 转述 ✅
https://docs.snowflake.com/en/user-guide/security-access-control-overview。

**（b）资源监视器=成本刹车**：账户级与仓库级两类挂载点；阈值触发通知或硬停；计费周期口径
⚠️ 转述 ✅ https://docs.snowflake.com/en/user-guide/resource-monitors。2019 书中"给试验仓挂
监视器防爆账"的动作，今天仍是企业开通第一周的标准作业（演进节有补）。

**（c）账本视图族**：`SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY` 是 credit 归因的地面
真值 ✅ https://docs.snowflake.com/en/sql-reference/account-usage/warehouse_metering_history；
同族还有 QUERY_HISTORY/LOGIN_HISTORY/COPY_HISTORY 等 ✅（account-usage 主题页）。书中"管理=
可观测"的论点在 2026 由这套视图+Snowsight 成本中心双轨兑现 ⚠️。

**（d）编排初体验**：TASK 把"仓库+调度+SQL"绑定成平台原生定时器——比 05 章 crontab 方案多了
依赖 DAG 与状态机 ✅ https://docs.snowflake.com/en/sql-reference/sql/create-task；本章点到为止，
11 章方案图里复用。

**（e）版本订阅心智（2019 名录 ⚠️）**：Time Travel 上限随版本抬升（详见 14 章）；企业合规特性
（如列级脱敏/网络池）当时按版本销售 ⚠️；2026 版本面已重组（见演进节），读本章时把"版本=能力
开关"换成"版本=默认上限+计费方案"更符合现状 ⚠️。

## 4. 深读问答（自拟）

**Q1：为什么 SYSADMIN 与 SECURITYADMIN 要分离？** A：建对象与管身份的爆炸半径不同；分离后
"谁能进系统"与"谁动了数据对象"两本账天然解耦，审计清晰 ⚠️+✅ access-control-overview。
**Q2：资源监视器触发 SUSPEND 后谁倒霉？** A：正在跑的查询被杀、队列全停——所以阈值要留逃生
缓冲与分级动作（先通知后硬停）✅ resource-monitors ⚠️ 转述。
**Q3：账本视图有延迟，能当实时刹车吗？** A：不能；实时封顶靠监视器，账本用于归因复盘 ✅
account-usage ⚠️ 边界转述。

## 5. 与其他书/章联系

- 03 章（仓库参数）与本章（仓库的钱袋子）互为孪生；14 章保留期上限在本章的版本矩阵里定数。
- 08 章承接"授权语义"深水区；11 章环境隔离用本章角色图落地。
- [../Tuning_the_Snowflake_Data_Cloud/00-总览与阅读地图.md](../Tuning_the_Snowflake_Data_Cloud/00-总览与阅读地图.md)：计费/成本深潜主场（波8 ✅）；[../Snowflake_The_Definitive_Guide/00-总览与阅读地图.md](../Snowflake_The_Definitive_Guide/00-总览与阅读地图.md)：角色/授权全表（波1 ✅）；[../Advanced_Snowflake/00-总览与阅读地图.md](../Advanced_Snowflake/00-总览与阅读地图.md) ⚠️ 降级册仅辨析。

## 6. 本章检验点

1. 画出内置角色金字塔并标注业务角色挂点。
2. 写出资源监视器"通知→硬停"两段式配置意图。
3. 说出 metering 视图与监视器的实时性分工。
4. 解释版本订阅在 2019 如何决定 Time Travel 上限（联动 14 章）。

## 7. 关键对象速查卡

| 对象/视图 | 域 | 一句话 |
| --- | --- | --- |
| ROLE / GRANT OF ROLE | 身份 | 角色图边关系 |
| RESOURCE MONITOR | 成本 | 阈值+动作+频率 |
| WAREHOUSE_METERING_HISTORY | 账本 | credit 时间序列 ✅ |
| QUERY_HISTORY | 账本 | 查询画像源表 |
| LOGIN_HISTORY | 审计 | 进系统台账 |
| TASK | 编排 | 平台原生定时器 |
| PARAMETERS（用户/会话） | 体验 | 默认角色/仓库/时区 |

## 8. 取证与标注说明

章题/页码 ✅ Crossref `_7`（pp.107–128）；✅ URL（curl-200）：security-access-control-overview、
resource-monitors、account-usage、account-usage/warehouse_metering_history、create-task；
2019 版本名录（Standard/Enterprise/BC/VPS）与能力矩阵 ⚠️ 未获现行验真页，仅作时代记录；
授权粒度经验值属 ⚠️ 转述。

## 核心概念速览（中英对照）

| 中文 | 英文 | 一句话释义 |
| --- | --- | --- |
| 角色层级 | role hierarchy | GRANT OF 构成的权限 DAG |
| 内置管理角色 | system admin roles | ACCOUNT/SYS/SECURITY/USERADMIN |
| 主角色 | primary role | 会话生效的最高业务角色 |
| 资源监视器 | resource monitor | credit 阈值与自动动作 |
| 计量史 | metering history | 仓库 credit 用量账本 |
| 归因 | chargeback/showback | 把账本拆到团队/项目 |
| 订阅版本 | edition | 能力与上限的销售载体 |
| 任务 | task | 依赖可调度的定时 SQL |
| 治理双联 | admin × security | 07/08 章分工隐喻 |
| 爆炸半径 | blast radius | 一次误授权的波及面 |

## 最新演进与工业实践

- **成本面产品化**：Snowsight 内置成本用量报表与预算告警；Cost & Billing 主题线成一级文档 ✅
  https://docs.snowflake.com/en/guides-overview-cost——本章"手搓监视器"之上多了开箱仪表盘 ⚠️。
- **治理统一目录**：Horizon Catalog（2025+）把标签/策略/血缘集中管理 ⚠️（专页 URL 本目录未
  逐一验真；关联锚点 ✅ https://docs.snowflake.com/en/release-notes/2026/other/2026-07-21-delta-sharing-horizon-catalog-ga 实证 Horizon 品牌在产线）。
- **版本面重组**：2019 四档名录已被"按能力订阅+优化包"的现行结构替代 ⚠️——引用本章版本
  结论前务必查现行官方口径。
- **工业实践**：2026 平台组标准作业=角色模板仓库化（git 管 SQL ✅
  https://docs.snowflake.com/en/developer-guide/git/git-overview）、监视器分级（开发 10×生产
  1×⚠️示意）、metering 视图接 BI 做 FinOps 周报；Adaptive Compute 时代"何时自动缩容"成为
  新的管理参数面 ✅ https://docs.snowflake.com/en/user-guide/warehouses-adaptive。
