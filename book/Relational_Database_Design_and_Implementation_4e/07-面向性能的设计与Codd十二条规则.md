# 07-面向性能的设计与Codd十二条规则（Ch8 Database Design and Performance Tuning, pp.163–169 ✅；Ch9 Codd's Rules for Relational DBMSs, pp.171–180 ✅）

> 三态：✅ 书页 TOC/Crossref 页码实抓 · ⚠️ 转述/推定展开 · 🔧 本机 SQLite/DuckDB 实测（**非本书示范行为**）。
> Part II 收官两章都短（7+10 页）：Ch8 把「设计完≠完」讲清——索引/聚簇/分区三把性能刀；Ch9 用 Codd 12 规则给「什么才配称关系 DBMS」立宪。二者一实一虚，是工程清单与合格线清单。

## 一、精读札记（官方二级小节 ✅ 逐条）

**Ch8（163–169）**
- Indexing —— 索引=按非主码路径访问的复制秩序；写放大与读提速的对价。
- Clustering —— 物理共置减少页读取；表簇与索引簇之分 ⚠️ 转述。
- Partitioning —— 水平切分（范围/散列）；分区裁剪与运维窗口。

**Ch9（171–180）—— 12+1 规则逐条**
- Rule 0 Foundation（须以关系设施管理全部数据）；Rule 1 Information（数据与元数据同表域）；Rule 2 Guaranteed Access（任何值可靠达=表+主键+列）；Rule 3 Systematic Treatment of NULL；Rule 4 Dynamic Online Catalog（目录在线可查）；Rule 5 Comprehensive Data Sublanguage（单一语言覆盖 DDL/DML/约束/事务/控制 ⚠️ 最常被违反）；Rule 6 View Updating（可更新视图必可更新）；Rule 7 High-level Insert/Update/Delete（集合级操作）；Rule 8 Physical Data Independence；Rule 9 Logical Data Independence（模式演进不破应用）；Rule 10 Integrity Independence（约束入模式非入应用）；Rule 11 Distribution Independence；Rule 12 Nonsubversion（低层通路不得绕过完整性——安全章伏笔）。
- TOC 实抓 13 小节（Rule 0–12 ✅），是全书规则条款最密的章。

## 二、主题深读

### 2.1 🔧 E5 实测：Rule 之外的索引工程直觉（非本书示范行为）
2 万行 emp 表视图谓词查询（demos.txt）：
```
无索引: SCAN emp ... 1.65ms
有索引: SEARCH emp USING COVERING INDEX ix_emp (dept=? AND sal>?) ... 0.299ms (5.5×)
```
教学点：①小数据量下差别在微秒级——索引的**规模化**收益与代价都在百万行之后（E5 的 DuckDB CTE 200 万行聚合为镜像样本）；②覆盖索引=把 π 所需列全纳入索引体，SCAN→SEARCH 的计划翻转即 Ch8 Indexing 节的机器自白；③SQLite 与商用 DBMS 的差距在**无统计信息自适应**（2016 教材讲的 ANALYZE/直方图话题本机载体给不了 ⚠️，可对照盘上 [../Cost_Based_Oracle_Fundamentals/00-总览与阅读地图.md](../Cost_Based_Oracle_Fundamentals/00-总览与阅读地图.md) 的成本模型纵深）。

### 2.2 Codd 规则是「合格线」不是「功能表」
12 规则的历史用途：戳穿 1970s「伪关系」产品（只把表当接口、目录藏在代码里）。2026 视角的三条最锋利：
- **Rule 4**：元数据同构可查——today=information_schema/CATALOG 三件套，SQLite 用 `sqlite_schema`+PRAGMA 近似 ⚠️。
- **Rule 5**：单语言全覆盖——SQL 至今没把事务控制语句完全纳入语言核心 ⚠️（工程通说）。
- **Rule 12**：完整性不可被低层绕过——与 Ch23 安全篇「内部威胁」互文（见 16 文件）；API 直写文件的嵌入式架构（SQLite 形态）天然是 Rule 12 的灰色地带（🔧 本目录 E2 的 FK-OFF 即其显式形态）。

### 2.3 与 Date 三部曲的判据衔接
Date 在 [../SQL_and_Relational_Theory/00-总览与阅读地图.md](../SQL_and_Relational_Theory/00-总览与阅读地图.md) 一系把「SQL 产品对 Codd 规则的违约」逐条做成测试案例（NULL 三值/重复行/列序依赖等）；本书 Ch9 给规则原文+简评，是「知道考纲」，Date 册是「逐题批改」。两册合读=本章的正确打开方式。

### 2.4 分区的 2016→2026 语义漂移
书内 Partitioning 讲运维切表；2026 湖仓里「分区」变成**目录层谓词**（Iceberg/Hudi 分区演进，盘上 Apache_Hudi_Definitive_Guide、Architecting_an_Apache_Iceberg_Lakehouse、Apache_Iceberg活用入門 三册在册 ✅），语义从物理布局上移到元数据策略——Rule 8 物理独立性的一个漂亮正例：分区方案变了，表还是那张表。

### 2.5 Rule 0–12 逐条 2026 判据表（本册综合，⚠️ 非书内内容）

| Rule（✅ 小节题全十三行在册） | 一句话 | 2026 判据（⚠️/🔧） |
|---|---|---|
| 0 Foundation | 一切以关系呈现 | 主流引擎过；嵌套类型留后门（18） |
| 1 Information | 信息入表不入口头 | 魔法值/注释承载语义仍是常见病 |
| 2 Guaranteed access | 键+表+列可达 | SQL 默认满足 |
| 3 Null treatment | NULL 系统化 | 3VL 余震贯穿 11/12（真值表在 11） |
| 4 Online catalog | 目录在线可查 | 04 §2.7 数据字典→目录工业 |
| 5 Comprehensive sublanguage | 一门全功能语言 | SQL 地位未被动摇 |
| 6 View updating | 视图皆可更新 | 🔧 E5 负样本：SQLite「is a view」拒改（非本书示范） |
| 7 Set-level ops | 集合级 I/U/D | INSERT..SELECT/CTAS 通过 |
| 8 Physical independence | 改存储不改查询 | 索引/分区操作大致兑现（2.6） |
| 9 Logical independence | 改模式少改查询 | 视图/语义层承担；迁移工具时代 |
| 10 Integrity independence | 完整性存于 DB | 🔧 E2 执法矩阵的教义出处 |
| 11 Distribution independence | 位置透明 | 联邦查询部分兑现 |
| 12 Nonsubversion | 低权不得绕高权 | 16 内部威胁节的理论锚 |

十三节小节题（✅ 逐条在册）+ 本表=把 10 页规则章读成 1 页体检单——2.2「合格线非功能表」的用法示范。

### 2.6 Ch8 三节 × Ch21/盘上索引线的织网
Indexing/Clustering/Partitioning（✅ 三节，7 页 163–169）是**设计承诺**，Ch21 的 Creating Indexes（14）是**实现动作**——两章连读才是完整的性能教学线。2026 对位：clustering≈物理布局提示（DuckDB 的区域映射/ORDER BY 写入序、PG 的 BRIN/ZORDER 家族，⚠️ 通识）；partitioning≈时间分区+隐藏分区裁剪，其宏观形态即 17 的湖仓快照（时变特征物理化）。🔧 E5 是本册对 Ch8 唯一的实测回礼：covering index 6.1×（非本书示范行为，demos 原文在 00 §六）。纵深盘上：[../Fundamentals_of_Database_Indexing/00-总览与阅读地图.md](../Fundamentals_of_Database_Indexing/00-总览与阅读地图.md) 与 [../Database_Tuning/01-基本原则.md](../Database_Tuning/01-基本原则.md)（00 §七在册 ✅）。

### 2.7 规则章在教材谱系里的待遇差（⚠️ 评注）
同题材料三种写法：本书给合规清单（10 页十三节，✅）；Date 线给批判对象（SQL 与关系理论册的对读位，00 §七实链）；工业文档给营销话术（「100% 关系」的旧广告）。三者合读的收获是判据意识：**规则是度量衡不是记分牌**——用它问「哪条被谁在何处违反」，比用它打分有用得多。本文件 2.5 表即此问法的全表示范。

## 三、原书 → 2026 对位

| 书内论点 (2016) | 2026 现状 |
|---|---|
| 索引=DBA 手工决策 | 自动索引建议/向量索引（HNSW）加入目录；写放大对价原则不变 |
| 聚簇依赖表空间管理 | 列存/合并引擎（LSM）重排物理秩序；教学载体（SQLite rowid 聚簇 ✅ 本机可讲） |
| 分区手工 DDL | 表格式分区演进+透明分区裁剪；云仓自动分区建议 ⚠️ |
| Codd 规则考「伪关系」 | 考卷换成「HTAP/湖仓是否背叛关系语义」的讨论；规则本身仍是判据底本 |

## 四、阅读自测
1. Rule 2 的三元组（表+主键+列）为何排除「按行号访问」？
2. 用 E5 计划翻转解释覆盖索引消灭的回表动作。
3. Rule 10 与 Rule 12 的分工：一个管「约束住在哪」，另一个管什么？
4. 分区移动为什么是 Rule 8 的示范案例？
5. SQLite 默认 FK-OFF 违反的是哪条 Codd 规则的精神？（提示：Rule 3/10/12 之辨）

## 五、互链
- 上游：06（设计完成后才谈调优）、04（元数据即表→Rule 1/4）。
- 下游：14（索引语法面）、15（并发是调优的隐藏成本）、16（Rule 12→安全）、10（案例中的索引/分区落点）。
- 谱系：[../Database_Tuning/01-基本原则.md](../Database_Tuning/01-基本原则.md)、[../Fundamentals_of_Database_Indexing/00-总览与阅读地图.md](../Fundamentals_of_Database_Indexing/00-总览与阅读地图.md)、[../Cost_Based_Oracle_Fundamentals/00-总览与阅读地图.md](../Cost_Based_Oracle_Fundamentals/00-总览与阅读地图.md)、[../SQL_and_Relational_Theory/00-总览与阅读地图.md](../SQL_and_Relational_Theory/00-总览与阅读地图.md)。

## 核心概念速览（中英对照）
| 中文 | 英文 | 出处/一句话 |
|---|---|---|
| 索引 | indexing | Ch8 复制的访问秩序 |
| 覆盖索引 | covering index | E5 实测词 |
| 聚簇 | clustering | Ch8 物理共置 |
| 分区 | partitioning | Ch8 水平切分 |
| 物理数据独立性 | physical data independence | Rule 8 |
| 逻辑数据独立性 | logical data independence | Rule 9 |
| 完整性独立 | integrity independence | Rule 10 |
| 分布独立性 | distribution independence | Rule 11 |
| 不可颠覆规则 | nonsubversion rule | Rule 12 |
| 动态在线目录 | dynamic online catalog | Rule 4 |
| 综合数据子语言 | comprehensive data sublanguage | Rule 5 |
| 保证可达 | guaranteed access | Rule 2 |
| 规则体检单 | rules checklist | §2.5 十三行判据表 |
| 度量衡用法 | rule-as-measure | §2.7 非记分牌 |
| 覆盖索引 | covering index | 🔧 E5 本册唯一实测回礼 |
| 物理布局提示 | layout hint | §2.6 clustering 现代身 |
| 分区裁剪 | partition pruning | §2.6 时间分区主收益 |
| 位置透明 | distribution transparency | Rule 11 部分兑现 |
| 绕行防线 | nonsubversion guard | Rule 12→16 内部威胁 |
| 目录在线 | online catalog | Rule 4→04 §2.7 |
| 全功能语言 | comprehensive sublanguage | Rule 5 地位复核 |
| 承诺/动作分工 | promise vs action | §2.6 Ch8↔Ch21 |

## 最新演进与工业实践
- 向量索引与相似检索进入「索引」教学单元：盘上 [../Fundamentals_of_Database_Indexing/01-数据库查询与相似检索导论.md](../Fundamentals_of_Database_Indexing/01-数据库查询与相似检索导论.md) 已把 ANN/HNSW 与传统 B 树并列（在册 ✅），Ch8 的 2026 增补版应含此节。
- SQLite rtree 虚拟表（空间索引）官方文档实查 200：https://www.sqlite.org/rtree.html ✅（2026-10-02）——教学上演示「同一 SQL 面、不同索引结构」的最廉载体。
- Codd 规则的当代「考纲化」：湖仓一致性协议（Iceberg 快照隔离、Hudi 事务时间线）实为 Rule 2/3/9 在对象存储上的重新兑现（三册在册 ✅ 见 §2.4）；本目录主张：读 Ch9 后立刻去湖仓册找对应实现，规则就不再是博物馆展品。
- 2026 用法=架构评审问题清单：合规叙事退场，判据进场（§2.5 表化）。
- 🔧 E5 覆盖索引 6.1× 给 Ch8 体感（demos；非本书示范）。
- 分区语义漂移落锤（§2.4）：2016 性能手段→2026 治理手段（保留期/成本域）。
- 规则三待遇（§2.7）：合规清单/批判对象/营销话术——判据意识防天真。
- 湖仓事务时间线重新兑现 Rule 2/3/9（文末注；Iceberg/Hudi 盘上在册 ✅）。
- 毕业判据：§2.5 表任三行能讲「谁违反、何处、代价」。
- 索引自动伴生账（§2.3）：PK 建索引白拿、加宽 PK 加税——E2 联动。
- 跨文件义务：07 承诺→14 实现→09 工具→17 应用一贯。
- 「考纲化」副产品：十三行表即数据库原理口试题库（⚠️ 评注）。
