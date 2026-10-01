# 13 Migrating to Snowflake（pp.229–249 ✅ Crossref）

> 章定性：落地过程学——从存量数仓/Hadoop 迁移到 Snowflake 的方法论：评估、改造、并行、切换。
> 章题/页码 ✅ Crossref `_13`（2019 最长实操章，21 页）；小节 ⚠️ 推定；清单自拟示意；
> 机制 ⚠️ 转述 + ✅ curl-200 URL；本章无独立 🔧（方言差异演示归 04/09 章素材）。

## 1. 章节定位与叙事线

2019 语境：云仓军备竞赛进入"替换存量"阶段（合同到期、一体机维保尾、Hadoop 运维疲劳）。本章
给出一条保守而完整的迁移流水线 ⚠️ 推定：①盘点（ETL 脚本、报表、SQL 方言特性使用频次）→
②概念映射（方言差异表：分布式标记/特殊连接/窗口语法/伪列 ⚠️）→ ③分层试点（先迁历史冷数据
+低风险报表）→ ④双轨并行（源仓与 Snowflake 同跑比对账）→ ⑤切换与退役（流量/权限/保留期
14 章参数收尾）→ ⑥工具与伙伴（官方/第三方转换工具生态，本书时代以伙伴服务为主 ⚠️）。作者
强调迁移是"组织工程"而非"技术搬运"——测试账、回滚案、责任矩阵先于脚本。

## 2. 知识提纲（⚠️ 推定小节）

| # | 推定小节 | 要点 | 现状锚点（✅ curl-200） |
| --- | --- | --- | --- |
| 1 | 迁移动机与时机 | 维保/弹性/成本叙事 | guides-overview-cost |
| 2 | 资产盘点 | 脚本/查询/报表/作业清单 | migrations/README（方法学反照） |
| 3 | 方言映射 | 常见不兼容构造 | snowconvert 翻译参考 ✅ |
| 4 | 数据搬迁 | UNLOAD→COPY 大搬运 | copy-into-table |
| 5 | 双轨验证 | 行数/校验和/业务口径对账 | querying-semistructured（口径沉淀 ⚠️） |
| 6 | 切换剧本 | 冻结窗口/回滚点 | data-time-travel（回滚保险 ⚠️） |
| 7 | 性能回归预算 | 新仓尺寸基线 | performance-query-warehouse-size |

## 3. 深读与机制重构

**（a）方言差异清单（自拟示意，非书中原文；迁移评估的最小样本）**：

```sql
-- Teradata 味：  QUALIFY 在 Snowflake 原生可用；分区表达式需改写为聚簇/过滤 ⚠️
-- Oracle 味：    (+) 外连接 → 标准 LEFT JOIN；ROWNUM → LIMIT/ROW_NUMBER()；
--               伪列/特殊日期算术是转换雷区（官方翻译参考逐条在录 ✅ snowconvert 页）
-- Hadoop 味：   HiveQL UDF/STORED AS 习惯 → 内部函数族与 VARIANT（09 章）承接
-- 通用雷：      隐式类型转换宽容度、聚合 NULL 语义、大小写敏感性（对象名 ⚠️）
```

评估产出物=「特性频次×改造难度」矩阵：TopN 报表与核心 ETL 优先人工重写，长尾用转换工具批量
改写再抽检 ⚠️（2019 以伙伴工具为主；2023+ 官方 SnowConvert 进场，见演进节）。

**（b）数据大搬运的工程学**：源侧 UNLOAD 成压缩文件→对象存储→04 章 COPY 进场；TB 级以上分批
+校验（行数/双端求和/抽样比对）⚠️ 转述 ✅
https://docs.snowflake.com/en/sql-reference/sql/copy-into-table；装载吃专用仓（03 章参数）并
预留回归预算 ✅ https://docs.snowflake.com/en/user-guide/performance-query-warehouse-size。

**（c）双轨并行的账**：并行期成本≈两套平台叠加（1 章弹性叙事的反面账单），所以并行窗口要有
明确出口判据（业务口径一致率、时延达标、权限矩阵验收）⚠️+✅ guides-overview-cost。

**（d）切换与保险**：割接冻结窗→流量切换→源仓转只读保留一个审计周期；回滚依托 Time Travel/
UNDROP 只兜"仓内误操作"，不兜"迁移决策错误"——后者靠双轨对账 ⚠️（14 章联动）。

## 4. 深读问答（自拟）

**Q1：为什么"先迁历史冷数据"？** A：冷数据口径稳定、失败可重来，还能提前暴露容量/成本曲线
——风险最低的探路段 ⚠️。
**Q2：ETL 重写与"保留源逻辑薄壳化"怎么选？** A：报表层可薄壳直读迁移，核心加工层应借机重构成
本章目标架构（11 章）；全量"原样平移"往往把旧债搬进新仓 ⚠️ 经验口径。
**Q3：权限怎么迁不踩坑？** A：不要翻译旧平台 ACL，按 07/08 章角色金字塔重建映射表——迁移是
治理现代化的唯一窗口期 ⚠️+✅ security-access-control-overview。

## 5. 与其他书/章联系

- 依赖 04（搬运）05（脚本改造）07（角色）11（目标架构）14（回滚保险）；被 00 谱系表用于
  "波内云仓三角"对位（BigQuery/Redshift 迁移同理异构 ⚠️）。
- [../Snowflake_The_Definitive_Guide/00-总览与阅读地图.md](../Snowflake_The_Definitive_Guide/00-总览与阅读地图.md)：对象/方言参考面（波1 ✅）；[../Tuning_the_Snowflake_Data_Cloud/00-总览与阅读地图.md](../Tuning_the_Snowflake_Data_Cloud/00-总览与阅读地图.md)：迁移后性能回归深潜（波8 ✅）；[../Advanced_Snowflake/00-总览与阅读地图.md](../Advanced_Snowflake/00-总览与阅读地图.md) ⚠️ 降级册仅辨析。

## 6. 本章检验点

1. 写出迁移流水线六步及每步出口判据。
2. 举出三类方言雷区并给一个改写样例。
3. 说明双轨并行的成本逻辑与退出条件。
4. 区分 Time Travel 与双轨对账各自兜什么风险。

## 7. 迁移工具年表卡

| 年份 | 形态 | 状态 |
| --- | --- | --- |
| 2019 | 伙伴服务+手工重写+通用 ETL 导出 | 本书时代 ⚠️ |
| 2020s | 云厂商各出搬运器（通用 ⚠️） | 生态期 |
| 2023+ | 官方 SnowConvert（评估/转换/自动化） | ✅ https://docs.snowflake.com/en/migrations/README ✅ https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/oracle/pseudocolumns |
| 2024+ | AI 辅助改写进入工具箱 | ✅ https://docs.snowflake.com/en/guides-overview-ai-features（边界 ⚠️） |
| 2026 | 仓↔开放表格式双向搬迁常态化 | ✅ https://docs.snowflake.com/en/user-guide/tables-iceberg ⚠️ 展望口径 |

## 8. 取证与标注说明

章题/页码 ✅ Crossref `_13`（pp.229–249）；✅ URL（curl-200）：migrations/README、
migrations/snowconvert-docs/translation-references/oracle/pseudocolumns、copy-into-table、
guides-overview-cost、performance-query-warehouse-size、security-access-control-overview、
data-time-travel；六步流水线与经验判断均 ⚠️ 推定重构（未获样章）；工具名录 2019 部分按时代
转述不点名 ⚠️。

## 核心概念速览（中英对照）

| 中文 | 英文 | 一句话释义 |
| --- | --- | --- |
| 资产盘点 | workload inventory | 迁移前的全量账目 |
| 方言映射 | dialect translation | 源 SQL 到目标 SQL 的改写规则 |
| 特性频次矩阵 | feature-frequency matrix | 改造优先级排序器 |
| UNLOAD/COPY 搬运 | bulk transfer | 存量数据两段式搬家 |
| 双轨并行 | parallel run | 新旧同跑对账的过渡态 |
| 割接 | cutover | 流量正式切换的窗口 |
| 回滚点 | rollback plan | 切换失败退回路径 |
| 薄壳化 | thin migration | 原样平移少改造的极端 |
| 对账 | reconciliation | 双端口径一致性验证 |
| 退役 | decommission | 源系统正式下线 |

## 最新演进与工业实践

- **官方工具入场（本章最大改写）**：SnowConvert Service 把"伙伴手工时代"升级为"评估+自动
  转换+验证"产品线 ✅ https://docs.snowflake.com/en/migrations/README；Oracle/Teradata 等
  方言的逐构造翻译参考公开在录 ✅（snowconvert translation-references，见 §8 URL）。
- **AI 辅助迁移**：LLM 参与 SQL 改写与测试生成 2024+ 成趋势 ⚠️+✅ guides-overview-ai-features；
  人工抽检+对账的纪律不变。
- **迁移对象扩容**：2019"数仓搬到 Snowflake"→2026 还包括"仓内表迁托管 Iceberg（反向开放化）"
  ✅ https://docs.snowflake.com/en/user-guide/tables-iceberg——迁移从单向变双向 ⚠️。
- **工业实践**：2026 迁移项目标配=评估报告（自动化产物）→试点域（1-2 个数据产品）→双轨对账
  指标看板 ✅ account-usage→财务退出判据 ✅ guides-overview-cost；把"迁移当架构升级窗口"
  仍是本章最值钱的一句话 ⚠️ 经验口径。
