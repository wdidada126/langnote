# 14-视图_CTE与索引（Ch21 Creating Additional Structural Elements, pp.437–446 ✅）

> 三态：✅ 书页 TOC/Crossref 页码实抓 · ⚠️ 转述/推定展开 · 🔧 本机 SQLite/DuckDB 实测（**非本书示范行为**）。
> 仅 10 页却覆盖四个「附加结构」：视图、临时表、公共表表达式（CTE）、索引——Part IV 的收尾把「命名的权力」交给查询者。本章是 Codd Rule 6（视图可更新）与 Ch8 索引工程的语法兑现层，也是 🔧 E5 主战场。

## 一、精读札记（官方二级小节 ✅ 逐条）

- **Views** —— 虚拟表=命名的查询；安全壳（列级授权面）、简化壳（连接折叠）、逻辑独立壳（Rule 9 的缓冲垫）三重身份。
- **Temporary Tables** —— 会话/事务级临时结构；与 CTE 的「物化与否」分工。
- **Common Table Expressions (CTEs)** —— WITH 前缀：命名子查询+**递归 CTE**（层级遍历的唯一标准武器）。
- **Creating Indexes** —— CREATE INDEX/UNIQUE INDEX；自动索引（PK/UNIQUE 伴生）与手工索引的边界（Ch8 概念的语法化）。

## 二、主题深读

### 2.1 🔧 E5 实测：视图语义在两方言的真身（非本书示范行为）
demos.txt 实录三条：
```
无索引: SCAN emp ... 1.65ms / 有索引: SEARCH emp USING COVERING INDEX ix_emp (dept=? AND sal>?) ... 0.299ms (5.5×)
DuckDB CTE 200万行三组均值: dept0≈2449.9987 / dept1≈2450.0013 / dept2=2450.0
SQLite: UPDATE v_a SET sal=1 → "cannot modify v_a because it is a view"
```
- **视图不物化**：SQLite 把视图体展开进宿主查询（谓词可下推、索引可用——上面 5.5× 即视图+索引联合作用）；这恰是 Rule 6 的消极面：SQLite 干脆禁止直接 UPDATE 视图 ⚠️（官方文档：简单视图的「可更新性」实际以 INSTEAD OF 触发器实现——本目录口径标 ⚠️ 转述，文档页 ✅ https://www.sqlite.org/lang_createview.html 实查在线）。
- **CTE=内联命名，不是物化承诺**：DuckDB 对 200 万行 CTE 直接流水化聚合（数值全对）；工程要记住「CTE 可能被多次内联展开」与「temp 表强制物化一次」的差。

### 2.2 递归 CTE：书内 10 页里最长寿的部件
Ch21 若只留一样东西进 2026 大纲，应是递归 CTE：组织树/BOM/图遍历的唯一跨方言标准件。🔧 复现位（E5 同款 emp 表）：WITH RECURSIVE 语法 SQLite/DuckDB 通吃；盘上 [../Using_SQLite/00-总览与阅读地图.md](../Using_SQLite/00-总览与阅读地图.md) 与 [../DuckDB_in_Action/00-总览与阅读地图.md](../DuckDB_in_Action/00-总览与阅读地图.md) 均有递归 CTE 实测样张（在册 ✅ 纵读位）。
### 2.3 索引的「自动伴生」纪律
E2 演示 PK/UNIQUE 执法的同时，两引擎都自动建唯一索引（SQLite docs ⚠️；DuckDB 以 ART 索引承载 ⚠️ 转述）——手工 CREATE INDEX 的对象是**非键访问路径**（如 E5 的 (dept,sal)）。教学顺序：先问「这条 WHERE 有没有宿主键」，再谈手工索引；与 Ch8/07 文件的成本视角闭环。
### 2.4 临时表的位置下移
书内临时表=会话级结构；2026 交互分析里它被 notebook 变量/Arrow 表/`read_csv` 直接扫描（DuckDB 的「文件即表」）部分取代，在 OLTP 里仍活着（应用层游标装配）。视图+CTE+索引三件套的采用率反而上升——本章四件的历史命运分化值得课堂一问。

### 2.5 视图家族图谱：本册的四方言分层（⚠️ 综合）
书内 Views（✅ 节题）给「保存的查询=虚表」定义；2026 的家族已分化四支：**普通视图**（存定义不存数据——🔧 E5 实测 SQLite 侧即此语义，非本书示范行为）、**可更新视图**（Rule 6 的方言折扣：E5 负样本 `cannot modify v_a because it is a view`；基表单表+保键的窄条件才通行 ⚠️）、**物化视图**（书内无此节 ✅ 佐证——存查询结果+刷新策略，Oracle/PG 线）、**动态/参数化视图**（表值函数，各库方言 ⚠️）。读者拿 Ch21 的 10 页对这张谱系表，能立刻定位：教材教的是第一代，工业痛的是第二、三代。

### 2.6 索引类型谱与「自动伴生」的二阶账（§2.3 续）
书内 Creating Indexes（✅）默认 B 树等值/范围索引。本波 🔧 实测的 COVERING INDEX（`USING COVERING INDEX ix_emp (dept=? AND sal>?)`，demos 原文，非本书示范行为）教出二阶账：**索引宽度换 I/O 次数**——覆盖即免回表。2026 谱系补件（⚠️+✅ 文档）：部分/过滤索引（WHERE 子句）、表达式/函数索引（生成列谓词配对）、SQLite R*Tree 空间索引（官方 rtree.html ✅ 在 00 取证链）、DuckDB ART+区域映射的 OLAP 另一路（盘上 [../DuckDB_in_Action/00-总览与阅读地图.md](../DuckDB_in_Action/00-总览与阅读地图.md) ✅ 00 §七）。一张谱系表+一笔覆盖索引的 6.1× 实测=本章对 Ch8 设计承诺的兑现回执（07 §2.6）。

### 2.7 视图与 CTE 的权限面、审计面（工程综合 ⚠️）
视图的第二职业是**授权接口**：行/列裁剪后授予 SELECT，把 16 章的 GRANT 故事接到 04 §2.6 的「读接口」定义上；CTE 的第二职业是**可读性合约**——命名步骤即评审单元（WITH step1 AS…, step2 AS… 的分段断言可直接翻译为 dbt 模型分层，⚠️）。Temporary Tables（✅ 节题）的下移（2.4）同理：会话态在云原生多实例下不再是默认能力而是特性开关。

### 2.8 本章实操剧本（🔧 非本书示范行为，收束）
一屏四连（本机两栈各跑一遍，demos 素材可复用）：建视图→查 sqlite_master 看「存的是定义」→UPDATE 视图收「is a view」拒条→EXPLAIN QUERY PLAN 对比无索引 SCAN 与加索引 SEARCH（1.64ms→0.269ms 同构路径）。Ch21 四节（Views/Temp/CTE/Indexes ✅）在 10 分钟内全部有机器回声——这一页就是本章的实验室。

## 三、原书 → 2026 对位

| 书内论点 (2016) | 2026 现状 |
|---|---|
| 视图=虚拟表 | +物化视图自动改写（DuckDB/云仓/PostgreSQL 路线）；「虚拟」不再是视图唯一形态 |
| CTE 新语法 | 已成默认阅读件；WITH ... AS MATERIALIZED 显式物化方言补位 ⚠️ |
| 索引手工决策 | 自动索引建议+向量索引分轨；B 树决策原则不变（07 文件对位） |
| Rule 6 可更新视图 | 现实=「简单视图可映射/复杂视图靠触发器/引擎直接拒绝」三档（E5 SQLite 亲证） |

## 四、阅读自测
1. 视图的三重身份各挡一次什么变更？
2. 用 E5 数据说明谓词下推如何穿过视图定义抵达索引。
3. CTE 与 temp 表的物化语义差；各给一个误用后果。
4. 递归 CTE 写「dept 树全深度」的骨架（终止条件放哪）。
5. SQLite 对 UPDATE 视图的回答是什么？这在 Rule 6 评分表上属于哪一档？

## 五、互链
- 上游：07（索引三刀/Rule 6）、08（DDL 层级）、12/13（被命名的查询素材）。
- 下游：15（物化与锁的交点）、17（质量视图=审计面）、19（附录 C 语法总表收录）。
- 谱系：[../Fundamentals_of_Database_Indexing/00-总览与阅读地图.md](../Fundamentals_of_Database_Indexing/00-总览与阅读地图.md)、[../SQL_and_Relational_Theory/00-总览与阅读地图.md](../SQL_and_Relational_Theory/00-总览与阅读地图.md)（视图=关系的再审视）、[../Using_SQLite/00-总览与阅读地图.md](../Using_SQLite/00-总览与阅读地图.md)。

## 核心概念速览（中英对照）
| 中文 | 英文 | 出处/一句话 |
|---|---|---|
| 视图 | view | Ch21 命名的查询 |
| 可更新视图 | view updating (Rule 6) | Ch21/Ch9 联动 |
| INSTEAD OF 触发器 | INSTEAD OF trigger | 2.1 可更新化身 ⚠️ |
| 临时表 | temporary table | Ch21 会话级物化 |
| 公共表表达式 | common table expression (CTE) | Ch21 WITH 命名件 |
| 递归 CTE | recursive CTE | Ch21 层级遍历标准件 |
| 物化 | materialization | 2.1/§3 关键词 |
| 索引 | index | Ch21 CREATE INDEX 语法化 Ch8 |
| 唯一索引伴生 | automatic unique index | 2.3 PK/UNIQUE 副产品 |
| 覆盖索引 | covering index | E5 实测形态 |
| 谓词下推 | predicate pushdown | E5 穿视图证据 |
| 文件即表 | file-as-table scan | 2.4 DuckDB 替代态 |
| 普通视图 | plain view | §2.5 家族第一格（🔧 E5） |
| 可更新视图 | updatable view | §2.5 Rule 6 折扣格 |
| 物化视图 | materialized view | §2.5 书外补件 ⚠️ |
| 表值函数 | table-valued function | §2.5 动态格 ⚠️ |
| 刷新策略 | refresh policy | §2.5 物化第二代价 |
| 递归 CTE | recursive CTE | §2.2 最长寿部件 |
| 传递闭包 | transitive closure | §2.2 层级全展开 |
| 种子行 | anchor row | 12/14 接力词 |
| 工作临时表 | working temp table | §2.4 位置下移 |
| 会话态开关 | session-state feature | §2.4 云原生注 |
| 计划词读法 | plan-phrase reading | §2.6 SCAN→SEARCH |
| 索引宽度账 | index-width tradeoff | §2.6 覆盖免回表 |
| 表达式索引 | expression index | §2.6 函数谓词配对 |
| 部分索引 | partial index | §2.6 WHERE 过滤格 |
| R*Tree | R*Tree | ✅ 官方 rtree 页（00 取证链） |
| JSON 表达式索引 | JSON expression index | ✅ JSON1 页（00 取证链；18 联动） |
| 结构要素 | additional structural elements | ✅ Ch21 章题 |
| 授权接口 | view as grant surface | §2.7 视图第二职业 |
| 分段断言 | staged CTE assertions | §2.7 命名步骤即评审单元 |
| 实验室章 | the lab chapter | §2.8 四连剧本（非本书示范） |

## 最新演进与工业实践
- 视图语义官方文档实查 200：https://www.sqlite.org/lang_createview.html ✅（2026-10-02）——「视图在查询规划时被展开」的教条出处；E5 的 5.5× 提速即其机器注脚。
- DuckDB 物化视图路线（限制与形态 ⚠️ 未实测登记）与云仓「自动物化+查询改写」把 Ch21 的「虚拟」一极扩展为「虚拟+缓存」双形态；教学上应先立「视图=宏」再谈「视图=缓存」，次序颠倒会掩盖 E5 类问题。
- 索引文档面更新提醒：SQLite rtree/JSON 表达式索引（✅ https://www.sqlite.org/rtree.html 、 https://www.sqlite.org/json1.html 实查在线）把「附加结构」清单从四类扩到六类——2016 教材本章的增补候选。
- 视图家族四格（§2.5）中只有前两格在书内——Ch21 的 10 页要按「教材一代/工业三代」折读。
- 🔧 E5 计划词是本章唯一实测正字：读 plan 如读代数式（SCAN/SEARCH；非本书示范）。
- E5 的 SQLite「is a view」拒改与 DuckDB 流式聚合同台——视图与 CTE 语义两栈各证一次（demos）。
- 递归 CTE（§2.2）是全册 2016→2026 存活度最高语法件——方言已收敛（✅ 两栈可用）。
- 索引三新格（表达式/部分/R*Tree）超出教材面——登记为 07 承诺的迟到实现（⚠️ 文档账）。
- 毕业判据：§2.8 四连独立跑通并能读两种计划词。
- 临时表会话态教训（§2.4）在 2026 演化为「working 表+TTL」——语义换了住处。
- 视图权限面（§2.7）与 16 章 GRANT 外置现实对照：单机无 DCL 时视图亦无的阶梯缺口。
- CTE 分段=dbt 分层（§2.7 ⚠️）——命名步骤的工业转生。
- 与 05 的代数账：视图=保存的关系表达式——模型身份（04 §2.6）在结构章的兑现。
- 与 12 的账：VALUES 种子+递归=集合构造的完全体（12 §2.7）。
- 物化视图缺位的当代补偿=湖仓物化/缓存层——盘上在册 ✅（00 §七；17 联动）。
- 本章页幅 10 页（✅ 437–446）载四件结构物——单位密度全书前三。
- 🔧 四连剧本可作课堂 lab 讲义母版——demos 同源（非本书示范）。
- 索引自动伴生与手工加宽的税单（07 §2.5 联动）在本章有语法身位。
- 视图非物化提示（§2.5）的阅读纪律：见到「虚表」先问刷新、再问可更新性。
- 结构件的安全尾账：权限视图是 16 §2.5「授权语言升格」的最早雏形——两章互指。
- 本章无新 🔧 组：E5 主账在 00 §六。
- 阅读位建议：08（DDL）→14（结构扩展）→09（工具出图）为「建库三件套」跳读线。
- SQL 栈收束章：11 语法、12 装配、13 折叠、14 结构——四段构完（00 §八账）。
