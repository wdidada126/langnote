# 第 12 章 装载 Data Vault（Loading the Data Vault）

> 目录取证：章题与 12.1 Loading Raw Data Vault Entities / 12.2 Loading Reference Tables / 12.3 Truncating the Staging Area ✅ 实抓自 Elsevier 官方 TOC。正文为精读重构；🔧 为本机 DuckDB 1.5.5 实测（脚本 `D:\develops\tmp\dbwave_datavault2\`）。

## 1. 装载层的总合同

**输入**：stage（已含 HK/HD/load_dts/record_source）；**输出**：Raw Vault 三型 + Reference；**约束**：只 INSERT、幂等可重放、按实体并行。本章给出每种型体的「最小装载 SQL 形状」——2015 年用 SSIS/T-SQL 手写或生成，今天由 dbt 宏生成，**形状一字未变**：

```sql
-- Hub：新键才进
INSERT INTO H_CUSTOMER (hk, bk, load_dts, record_source)
SELECT DISTINCT s.hk, s.bk, s.load_dts, s.record_source
FROM stage_customer s
WHERE NOT EXISTS (SELECT 1 FROM H_CUSTOMER h WHERE h.hk = s.hk);

-- Link：新关系才进（含可空成员）
INSERT INTO L_BOOKING (hk_link, hk_cust, hk_flight, load_dts, record_source)
SELECT DISTINCT l.*, ... WHERE NOT EXISTS (同键同关系已存在);

-- Satellite：哈希差变化才进（父键必须已存在于 Hub——依赖顺序）
INSERT INTO S_CUST_ATTR (hk, ldts, end_dts, hd, attrs..., record_source)
SELECT ... FROM stage s
WHERE NOT EXISTS (SELECT 1 FROM S_CUST_ATTR x
                  WHERE x.hk = s.hk AND x.hd = s.hd);   -- 最新版本比较（或全历史比较，见 §3）

-- Link Satellite：先闭旧（唯一允许的 UPDATE），再插新
```

## 2. 12.1 装载 Raw Vault 实体（✅）

- **依赖顺序**：批内 Hub→Link→Satellite（引用完整性靠装载次序而非外键约束，大仓通常禁 FK；顺序由框架保证并行度上限——Hub 层并行、Link 等 Hub、Sat 等父）；
- **闭区间维护**：卫星新行插入时把同键上一行 `load_end_dts` 置为当前（或依赖 PIT/视图动态算，两种流派，🔧 实测采动态比较式，见 §4）；
- **效果性链接**：换会 UPDATE+INSERT 成对出现（🔧 实测：CLUB_1 闭 `eff_to=2015-06-30` + CLUB_2 开新行，链接表三行并存）；
- **错误处理**：装载拒绝行→Error Mart（第 10.5 落地于此），Meta Mart 记录每实体「读入/新增/过滤」三计数（哈希差过滤数是调优信号）。

## 3. 哈希差比较的两种语义（工程细节，重构）

- 与**最新一行**比（增量语义，社区主流：变化才追加）；
- 与**全历史**比（「见过就不进」的去重语义，书中 SSIS 示例偏向此式，⚠️ 未逐例核）。
两者在多源同批场景结果不同——🔧 实测曾复现该陷阱：同一批内 C1 有 CRM(VIP)/OMS(GOLD) 两行时，全历史比较会吞掉后者；**必须按 (hk, record_source) 分组比最新**，修正后装载计数 4→4（重放 0 新增）→5→6 精确符合预期。此坑在 AutomateDV 文档以「dedup 按 hashdiff+parent」处理，两时代同病。

## 4. 🔧 实测：hash diff vs 全列比较（DuckDB 1.5.5，20 万行卫星装载）

| 场景 | 哈希差过滤 | 全列比较 | 备注 |
| --- | --- | --- | --- |
| 冷批（空历史） | 0.12 s | 0.08 s | 向量化引擎里逐列比较本已廉价，哈希额外花 ~50% |
| 重放同批（应 0 新增） | 0.16 s，added=0 | 0.16 s，added=0 | 两法正确性等价 |

方法：`range(200000)` 造源，`NOT EXISTS` 去重，计时含插入。结论修正书中隐含动机：**哈希差在列式/向量化引擎上不是性能必需品**，其现代价值在于①窄列比较便于跨异构引擎可移植、②比较逻辑与列数解耦（卫星加列不改装载 SQL）、③审计可见（hd 列即版本指纹）。行存+慢网络（当年 SSIS 逐行比较、今天拉取到内存比较的湖场景）仍受益。

## 5. 12.2 Reference 表装载 / 12.3 截断暂存区（✅）

- Reference 允许 UPDATE/MERGE（它是字典不是事实，见 [06-高级建模PIT与Bridge.md](06-高级建模PIT与Bridge.md) §4）；变更建议带版本卫星式历史（字典改值影响所有集市口径）。
- 截断 Stage：批次成功后截断/归档（12.3），保证「重放=重新提取」；与 Error Mart 一起构成批次生命周期闭环（Meta Mart 记批末状态）。
- 全量快照源 vs 增量源的装载差异：快照源天然幂等（哈希差过滤重复）、增量源天然少比较成本。

## 6. 自动化装载谱系（本章思想史的 2015→2026）

1. **手写 T-SQL/SSIS**（书中主线）→ 模板化痛点：每加一个源实体复制 4 段装载 SQL；
2. **生成器时代**：**SQLDBM**（Olschkke 自家工具：画三型图→出 DDL+装载 T-SQL，书中演示；现转型多云建模台，见 [08-物理数仓设计.md](08-物理数仓设计.md)）；**VanDyke**（SSIS 时代的 Data Vault 自动化框架/加速套件，⚠️ 其现状未能核实——注意 vandyke.com 是无关的 SecureCRT 厂商，2026-09 实测确认）；商业 ETL（Informatica/Talend 的 DV 方案）同期存在（⚠️ 书中未展开者不列）；
3. **声明式宏时代**：dbtvault（2018–2023，GitHub org 现已 404，仓库不复存在 ✅ 2026-09 实测）→ 社区延续为 **AutomateDV**（https://github.com/Datavault-UK/automate-dv ，596★，活跃至 2026-02 ✅ API 实测）与 Scalefree 的 **datavault4dbt**（https://github.com/ScalefreeCOM/datavault4dbt ，208★，活跃至 2026-09 ✅）+ **turbovault4dbt** 模型生成器（https://github.com/ScalefreeCOM/turbovault4dbt ，2026-07 ✅）——「映射清单=YAML，装载 SQL=宏展开」正是本章模板思想的 dbt 化终点。

## 7. Link Satellite 的装载（12.1 未尽式，重构）

```sql
-- ① 闭旧（本章唯一合法 UPDATE 家族）
UPDATE S_BOOK_AMT SET load_end_dts = :batch_ts
WHERE (hk_link, load_dts) IN (
  SELECT x.hk_link, MAX(x.load_dts) FROM S_BOOK_AMT x
  JOIN stage_amt s ON s.hk_link = x.hk_link
  WHERE x.load_end_dts = '9999-12-31' GROUP BY x.hk_link);
-- ② 插新（哈希差过滤，父键=Link 非 Hub）
INSERT INTO S_BOOK_AMT SELECT ... FROM stage_amt s
WHERE NOT EXISTS (SELECT 1 FROM (SELECT DISTINCT ON (hk_link) hk_link, hd
                 FROM S_BOOK_AMT ORDER BY hk_link, load_dts DESC) x
                 WHERE x.hk_link=s.hk_link AND x.hd=s.hd);
```

闭旧与插新必须同事务（或先闭后插的补偿锁），否则出现「双开区间行」——卫星时间轴重叠是装载 bug 的头号形态（Meta Mart 加一条「重叠检测」断言即可拦截，10.3 的自反性用例）。

## 8. 编排骨架（依赖顺序的形式化，重构示意）

```text
批 DAG：  Stage 就绪断言（G1）
   ├─ 并行带 A：所有 Hub（互不依赖） ──┐
   ├─ 并行带 A：Reference 表          ──┼─→ 栅栏1
   └──────────────────────────────────┘
   ├─ 并行带 B：所有 Link（父=Hub）＋ 效果性闭旧 ─→ 栅栏2
   ├─ 并行带 C：Hub-Satellites（父=Hub）
   └─ 并行带 C：Link-Satellites（父=Link）        ─→ 栅栏3
截断 Stage（12.3）→ Meta Mart 批末计数落账（10.2）→ Error Mart 翻牌
```

三个栅栏=三层依赖的最低限度；粒度还能更细（按分区/按源），但「卫星等父键」不可再松——用生成器（SQLDBM 时代）或宏（dbt 的 `ref()` DAG）让依赖自动显形，是 12→自动化演进的主轴。

## 9. 幂等性自检清单（装载框架验收用，重构）

1. 同批重跑 ×2：所有表新增=0（🔧 本目录卫星实测达成）；
2. 杀批中途重放：栅栏原子性成立（无半批）；
3. 乱序批（先收到 07-01 再收 06-01）：load_dts 定序或拒绝晚到（两策略二选一并写进框架配置，社区默认前者 ⚠️ 书中策略未核）；
4. 效果性双开检测 SQL 常跑（§7 断言）；
5. 引用完整性视图（Link 孤儿=父缺失）恒空。

## 10. FAQ

- **Q：无外键约束怎么防孤儿键？** 靠栅栏编排+孤儿检测视图+告警（§9 第 5 条），比 FK 便宜且可解释——FK 在 MPP/湖仓上本就不被普遍支持（第 8 章）。
- **Q：装载窗口撑不住先动哪里？** 顺序：① 增量提取（11 章）；② 卫星按变更分组（哈希差过滤率上升）；③ 并行带扩容；④ 最后才考虑砍历史（归档≠删除，留可重放指针）。
- **Q：dbt 宏生成的装载 SQL 和手写差在哪？** 形状同源（§1 模板），差在**映射清单成为唯一手工工件**+测试/文档随模型生成——第 3 章工作包思想的完全体。

## 核心概念速览（中英对照）

- **原始装载** — Raw Loading：把 stage 无损搬进三型的过程。
- **幂等重放** — Idempotent Replay：同批重跑结果不变（NOT EXISTS 族）。
- **装载顺序** — Load Order：Hub→Link→Satellite 的依赖次序。
- **依赖顺序并行** — Ordered Parallelism：层级内并行、层级间串行。
- **过滤计数** — Filtered Row Count：被哈希差挡掉的行数（Meta Mart 指标）。
- **闭旧插新** — Close-and-Insert：效果性/区间维护的成对操作。
- **字典可更新** — Mutable Reference：Reference 表是不可变性的例外。
- **批末截断** — Post-load Truncate：12.3 的 stage 清理纪律。
- **模板生成器** — Code Generator：SQLDBM/VanDyke/dbt 宏一脉。
- **声明式映射** — Declarative Mapping：以 YAML 清单代替手写 SQL。
- **宏** — Macro (dbt)：可复用的装载 SQL 模板单元。
- **去重语义** — Dedup Semantics：全历史比 vs 最新比的分歧点。
- **按源去重** — Per-record-source Dedup：多源同批互不吞行的分组。
- **加速套件** — Accelerator：预置 ETL 框架的商品形态。

## 最新演进与工业实践

- **dbtvault 之死与续命（✅ 2026-09 实测）**：`dbtvault/dbtvault` 仓库与其 GitHub org 均已 404（原 dbtvault Inc. 项目停摆）；其模式由两条线继承——社区托管的 **AutomateDV**（Datavault-UK org，2026-02 仍活跃、文档站 https://automate-dv.com/（403 反爬，存在性以搜索引擎收录为据 ⚠️））与 Scalefree 官方 **datavault4dbt**（2026-09 仍高频更新，并配 AI 代理技能包 https://github.com/ScalefreeCOM/datavault4dbt-agent-skills ✅）——后者是「装载自动化 × LLM」的 2026 前沿样本。
- **湖上装载**：Iceberg/Delta/Hudi 的 MERGE 原语直接实现「NOT EXISTS」族（books 见 ../Apache_Iceberg活用入門/00-总览与阅读地图.md 等），装载并行度由 Spark/DuckDB 进程数×文件分片决定——本章 Hub/Link/Sat 三形状在 Databricks/Trino 上照抄即可（社区实践通述 ⚠️）。
- **增量引擎**：Fivetran/Airbyte 负责 §5 之前的提取，本章之后接 dbt 宏；「ELT 中的 T 变薄」的口号在 Vault 语境下恰好反过来成立：**T 只是从存储过程变成了模板**。
- ⚠️ 原书 SSIS 包结构、CDC 组件配置等 2015 工具细节本目录不再重述，只保留其模式语义。
