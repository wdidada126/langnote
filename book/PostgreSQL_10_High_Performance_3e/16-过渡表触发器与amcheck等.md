# 16 PG10 新工具面：过渡表触发器与 amcheck 等

> 章题 ⚠️ 推定；主题域 ✅ 强实证：官方代码仓 `Chapter16` 三文件中，
> `16_2..sql` 是**过渡表（transition table）触发器**的完整实验（在
> `transition_table_base(id,val)` 上建 `LANGUAGE plpgsql` 触发器函数，
> 内部 `EXPLAIN (TIMING off, COSTS off, VERBOSE on) SELECT * FROM oldtable ot
> FULL JOIN newtable nt USING (id)` 遍历 `old table/new table` 快照）；
> `16_3.sql` 是 **amcheck 扩展**的 `bt_index_check` 全库 B-tree 巡检 SQL（联 pg_index/pg_opclass/
> pg_am 按 relpages 降序抽查）。本章以此二件为轴，收束"PG10 给 DBA 的新玩具"。非原书文本。

## 一、过渡表触发器：集合级审计的原生化的（✅ 16_2..sql 现场）

PG10 前触发器只见逐行 NEW/OLD；PG10 起 `AFTER ... REFERENCING OLD TABLE AS oldtable
NEW TABLE AS newtable` 让触发器看到**本语句的批量差集**——
16_2..sql 把差集 FULL JOIN 后 EXPLAIN 输出，正是"语句级变更审计"的最小实现。
性能含义 ⚠️ 转述官方触发器文档：
- 收益：审计/镜像表从 N 次行触发器降为 1 次集合操作，写风暴表上的税大幅下降；
- 代价：过渡表本身是临时元组存储，大语句触发大过渡表 → 内存/临时文件账（05 章 work_mem 语义）；
- 与 15 章路由触发器的关系：**声明式分区缺路由是 10 的痛**，过渡表是当年给"手工分区/审计"
  补性能的关键砖 ⚠️ 框架联读。

## 二、amcheck：把索引一致性变成巡检项（✅ 16_3.sql 现场）

`CREATE EXTENSION amcheck;` 后按 16_3.sql 的目录联查挑最大 B-tree，
`bt_index_check(index_oid)` 校验兄弟链接/条目序（不写锁，轻量版；
`bt_index_parent_check` 加强校验 ⚠️ 转述）。锚点：✅ https://www.postgresql.org/docs/10/amcheck.html （curl 200）。
性能语境：它是 04 章 checksums（堆层）的**索引层补位**——硬件腐蚀/内核 bug 造成的静默索引损坏
从"查询炸了才知道"变为"cron 巡检早知道" ⚠️。书仓 SQL 里"排除临时表/仅 indisvalid"的
注释细节即是生产巡检脚本的成熟形态 ✅（16_3.sql 原文注释）。

## 三、PG10 工具面的其余拼图（⚠️ 转述 + 部分 ✅ 链接）

| 工具 | 用途 | 归章 |
| --- | --- | --- |
| pspg/pgcli | psql 分页高亮/补全（✅ github.com/okbob/pspg 经 api.github.com 校验；✅ https://pgcli.com/ curl 200）| 11 |
| pg_wait_sampling | PG10 缺等待事件视图时的采样补丁（✅ postgrespro/pg_wait_sampling 经 api.github.com 校验存在）| 11 |
| postgres_fdw（增强）| 跨库联邦与 DML 下推（谓词下推于 PG10 加强 ⚠️ 转述）| 本章补位 FDW 议题：2e 的 FDW 独立章在 3e 无专属代码夹，功能讨论并入本章与 10 章 |
| pg_stat_kcache 等采样扩展 | 真 IO 归因到查询（社区扩展 ⚠️）| 11 |
| pgbench 新脚本语法 | 基准工程化（✅ https://www.postgresql.org/docs/10/pgbench.html ）| 03 |

## 四、全书收束：三样东西会过期，三样不会（⚠️ 评价性结语）

会过期：参数默认值（版本代际）、硬件账（04 章）、PG10 语法缺口（分区/触发器路由已内建化）。
不会过期：**测量-假设-实验循环**（03 章）、**MVCC-vacuum 因果模型**（07 章）、
**分层归因视角**（11 章）。本目录 16 章的读法亦循此：代码夹实证的部分当"施工图"读，
⚠️ 占位章当"方法论案例"读。

## 五、与波内/盘上邻居的接口

- PG16 Cookbook 的"新工具"章群与本册互补：食谱 vs 机制（✅ [../PostgreSQL_16_Administration_Cookbook/00-总览与阅读地图.md](../PostgreSQL_16_Administration_Cookbook/00-总览与阅读地图.md)）；
- FDW/数据湖方向的当代纵深见盘上湖仓目录群 ⚠️（本波兄弟册互链义务登记于 00，主代理统一闭环）；
- 中文 FDW/扩展谱系研究在盘上单文件（⚠️ 本目录未逐一核验具体章节，留互链表登记）。

## 细案：把 16 章两件玩具产品化的检查单（⚠️ 教材性 + ✅ 书仓 16_2/16_3 原码特征）

**过渡表审计管道投产检查**：
1. 触发器只挂 AFTER 语句级（行级混挂会双份记账 ⚠️ 语义转述）；
2. 过渡表体积预估 = 单语句最大变更行数 × 行宽（05 章 temp 账）——超限语句先拆批；
3. 审计表与业务表同库不同表空间，防 IO 互踩（04 章）；
4. 16_2..sql 那种"在触发器里跑 EXPLAIN 拼文本"的写法是**实验用途**，
   生产要换成把 old/new 差集直接 INSERT 进审计表（形态学差异 ✅ 代码辨读）；
5. 压测回放：用 03 章 runbook 的 T3 场景量审计税（目标 <15% 写放大 ⚠️ 经验值）。

**amcheck 巡检投产检查**：
1. 抽样策略：16_3.sql 的 `ORDER BY relpages DESC LIMIT n` 是"最大先查"，
   全量则按 relpages×频率加权轮转 ⚠️ 教材性；
2. 时段与限流：bt_index_check 有读放大，挂谷段并配 statement_timeout（10 章熔断）；
3. 阳性剧本：索引损坏 → CONCURRENTLY 重建 → 记 runbook（09/12 章联动）；
4. 版本意识：PG10 的 amcheck 仅 B-tree；后续版本扩到更多 AM ⚠️ 版本注记。

## 章内自测（两问两答）

- **问：过渡表触发器和逻辑解码都在"抓变化"，选边判据？** 答：库内审计/同步影子表→前者（同事务语义）；跨系统 CDC→后者（不占业务写路径事务 ⚠️ 结构对比）。
- **问：为什么本册没有 FDW 专章也算合理？** 答：3e 把 2e 的 FDW/PL 章打散重组（⚠️ 编排推定），
  postgres_fdw 要点已在 10 章下推与本节工具表出现；深读可回 2e（9X 之颠中译，谱系见 00）✅。

## 本册工具清单终表（16 章收口 ⚠️ 生态口径 + ✅ 已验锚）

| 工具 | 层级 | 一句话定位 | 归章 |
| --- | --- | --- | --- |
| psql+`\watch` | 内核自带 | 零依赖观测原语 | 11 |
| pspg / pgcli | 客户端 | 终端面板体验层（✅ github.com/okbob/pspg、✅ pgcli.com）| 11/16 |
| pg_buffercache | 扩展 | 缓冲池内窥镜（5_7.sql）| 05 |
| pgstattuple 族 | 扩展 | 膨胀精测卡尺 | 07 |
| amcheck | 扩展 | 索引结构体检（16_3.sql ✅）| 16 |
| pg_wait_sampling | 扩展 | 等待归因外挂（✅ postgrespro/pg_wait_sampling）| 11 |
| pgbench | 内核自带 | 引擎极限形状探针 | 03 |
| postgres_fdw | 内核自带 | 跨库联邦与下推 | 16/10 |
| 过渡表触发器 | 内核新语法 | 语句级集合审计（16_2..sql ✅）| 16 |

**终表读法**：凡 ✅ 者本次已做仓库/页面级校验；凡 ⚠️ 者按各章"最新演进"节的时间线自行对表。
一张工具清单即全书机制索引——16 章以"玩具"始、以"地图"终，这是书系三代同堂里
3e 相对 2e 最鲜明的编排签名 ⚠️ 评价口径。

## 核心概念速览（中英对照）

- **过渡表** — Transition Table：REFERENCING 子句暴露的语句级 OLD/NEW 集合（16_2..sql）。
- **AFTER 语句触发器** — Statement Trigger：每语句一次，配合过渡表做批量审计。
- **amcheck** — 索引体检扩展：B-tree 结构一致性校验（16_3.sql）。
- **bt_index_check** — 轻校验函数：无锁级兄弟链/序检查。
- **静默损坏** — Silent Corruption：无 checksum/amcheck 时不可见的块/索引病变（04 章）。
- **谓词下推** — Predicate Pushdown：postgres_fdw 把过滤搬到远端执行的收益开关。
- **pg_wait_sampling** — 等待采样扩展：PG10 归因缺位的社区补丁（11 章）。
- **pspg** — psql 分页器：终端监控面板的乐高件（11 章）。
- **数据生命周期自动化** — Retention Automation：过渡表/巡检脚本的 cron 化（本章工程义）。
- **工具面拼图** — Tooling Map：把 16 章工具挂回各机制章的阅读法（本章方法论）。
- **dellstore2** — 实验数据集：贯穿 10/15 章的教学库（✅ 提示符实证）。
- **施工图 vs 方法论** — as-built vs method：本目录对可实证章与占位章的分级读法。

## 最新演进与工业实践

- **过渡表后继有人**：PG 生态的变更捕获首选已移向逻辑解码（14 章），过渡表退守
  "库内审计表"niche ⚠️ 转述；但合规行业行级留痕需求使其在 2026 仍有真实用户 ⚠️。
- **amcheck 常态化**：定期 bt_index_check 进多家云厂商的托管巡检清单；错误索引重建
  （REINDEX CONCURRENTLY，PG12+ ⚠️ 版本注记）与 amcheck 形成"发现→无锁处置"闭环。
- **postgres_fdw → 湖仓接口**：FDW 家族在 PG13/14+ 的异步执行、并行扫描增强 ⚠️ 转述；
  跨源查询议题与盘上 Iceberg/Delta 目录群共同构成 2026 的"数据流动"版图 ⚠️ 指针。
- **等待事件内建化**：PG13+ `pg_stat_io`/wait event 细化使 pg_wait_sampling 类外置补丁退役 ⚠️ 转述版本史；
  这是本册"工具面"里迭代最快的一格。
- **观测 UX**：pspg/pgcli 长维护（✅ 两仓库经 api.github.com 校验存在），
  "终端即仪表盘"哲学与现代 Grafana 栈并存 ⚠️ 生态口径。
