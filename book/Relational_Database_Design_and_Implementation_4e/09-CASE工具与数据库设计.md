# 09-CASE工具与数据库设计（Ch12 Using CASE Tools for Database Design, pp.215–230 ✅）

> 三态：✅ 书页 TOC/Crossref 页码实抓 · ⚠️ 转述/推定展开 · 🔧 本机 SQLite/DuckDB 实测（**非本书示范行为**）。
> 16 页的「工具章」：CASE（Computer-Aided Software Engineering）在数据库设计工作流中的位置——ER 报告、数据流图、数据字典、代码生成、输入输出设计、绘图环境。2016 年写这章已带挽歌气质，2026 重读则变成「设计自动化前史」，其每一件功能都找到了新的宿主。

## 一、精读札记（官方二级小节 ✅ 逐条）

- **CASE Capabilities** —— CASE 全景：仓库（repository）+ 方法论顾问 + 文档/代码生成；数据库设计子集才是本书关切。
- **ER Diagram Reports** —— 图→报告→评审件：实体清单、联系矩阵、基数核对表。
- **Data Flow Diagrams** —— DFD 与 ER 的分工（Ch4「建模≠数据流」的工具化落点）。
- **The Data Dictionary** —— 工具化字典：属性域/缺省值/约束的集中登记（Rule 4 的工具侧镜像）。
- **Code Generation** —— ERD→DDL 正向工程 + 逆向工程（DB→图）；本章与 Ch11 的接缝。
- **Sample Input and Output Designs** —— 屏幕/报表原型：数据库设计的下游消费者视角审查。
- **The Drawing Environment** —— 绘图环境要素：符号库、缩放、打印布局——2016 的桌面工具形态 ⚠️。

## 二、主题深读

### 2.1 CASE 之死与重生：功能去向清单
| Ch12 的 CASE 功能 | 2026 宿主 |
|---|---|
| ER 图绘图环境 | 在线建模（draw.io/Erwin/Navicat 类）+ **DBML/PlantUML 文本图**（图入版本控制） |
| 数据字典 | 元数据平台/数据目录（../Data_Observability_for_Data_Engineering 在册 ✅） |
| 代码生成（正向工程） | 迁移工具生成 DDL；ORM→schema 反向潮流 |
| 逆向工程 | SchemaCrawler/DataGrip 类实时反读 |
| 输入输出原型 | 前端/BI 原型工具与 dbt 语义层合流 ⚠️ 通说 |
- 结论：CASE 作为「套件」死亡，作为「功能原子」全部存活并各自工业化。

### 2.2 逆向工程的廉价 🔧 实验（非本书示范行为）
2026 教学最小 CASE=三行 Python+SQLite：
```python
import sqlite3
for r in sqlite3.connect("app.db").execute("SELECT sql FROM sqlite_schema WHERE type='table'"):
    print(r[0])
```
`sqlite_schema` 即 Ch12「数据字典」与 Ch5「Data Dictionary」、Ch9「Rule 4 动态目录」三处的物理汇聚点；E2/E5 建过的全部表都能被这条查询吐回（本目录 🔧 会话实测可用）。DuckDB 侧对应 `duckdb_tables()/duckdb_constraints()` 系统视图族（本机可查 ✅ 🔧 语法级实证，细节 ⚠️ 未逐一贴表）。

### 2.3 Code Generation 的正确教学位序
书内把代码生成放 CASE 章、DDL 语法放 Ch11——隐含论断：**图是设计语言，DDL 是法律语言，工具管翻译**。本章应配一个手工练习：把 Ch10 案例三（SmartMart）的 ERD 手译成 E1 式五表 DDL，再用 PRAGMA table_info 对译物检——这正是 2026「建模即代码」评审流的原型（正向工程=生成 PR diff，逆向工程=schema 漂移检测）。

### 2.4 DFD 遗产的当代回响
Ch12 的 DFD 小节在 2026 的回响是**数据血缘**：算子级 DAG（dbt lineage/查询计划血缘提取）继承 DFD 的图形语法，但语义从「文档」升级为「运维事实源」（影响分析与事故定位——盘上 ../Data_Observability_for_Data_Engineering/01-数据可观测性工程动机.md 在册 ✅，对位章）。

### 2.5 逆向工程的最小机器标本（§2.2 的方法论化）
2016 CASE 的 forward/reverse 双向同步，2026 的答案是「谁是真相源」三选一：图是真相（建模工具正向出码）、库是真相（从 sqlite_master/information_schema 反推出图——🔧 非本书示范行为，本波实验栈三十行可达）、迁移脚本是真相（**schema-as-code**：评审即建模、历史即血缘，Flyway/dbt/Atlas 类 ⚠️ 通识）。§2.2 已登记的 🔧 最小反推=用元数据表反推 ER 草图——它证明教材命题「工具应服务于模型一致性」在零安装环境同样成立；变的只有工具名。

### 2.6 Code Generation 的当代三胞胎（2.3 续）
书内「ERD→DDL」的生成观（✅ 节题）已裂变为三个生成源：①模型→迁移（声明式 schema 工具链，⚠️）；②自然语言→SQL（LLM 副驾——2026 课堂真议题，其纪律恰与 CASE 同构：**生成物必须过人审**）；③运行时清单→目录（自动采集，17 §2.3 的承接位）。2.3 论教学位序：先手写后生成——本节给结论：生成时代这条序**更重要而非更松**，因为未手写过的人审不动生成物。

### 2.7 ER Diagram Reports / Data Dictionary 节的目录学后置
两节（✅）在书内是报告功能清单，在 2026 是两个产业的前身：ER 报告→文档化自动出图（dbdiagram/Mermaid-ER/PlantUML，「图即文本」评审流 ⚠️）；数据字典→元数据平台（盘上 observability 线在册 ✅，00 §七）。The Drawing Environment（✅）的交互画布则被双轨替代：鼠标画布活着（在线建模工具），代码画布新增（ERD-as-code 进 Git）。一章六节，节节的尸检都能开出器官捐献单——这正是本章的教学当代价值：**功能不会死，功能只是搬家**。

## 三、原书 → 2026 对位

| 书内论点 (2016) | 2026 现状 |
|---|---|
| CASE=桌面套件 | 功能原子化入 IDE/目录平台/迁移工具三堆 |
| 图评审为主交付 | schema PR 评审+自动漂移检查；图退居讲解媒介 |
| 数据字典=CASE 模块 | 开放标准元数据（information_schema/事件化目录） |
| 代码生成是卖点 | 生成是标配，**校验**（约束完备性/迁移可回滚）是新卖点 |
| 输入输出原型审查 DB | 语义层/契约测试承担同一「下游视角」审查职能 |

## 四、阅读自测
1. 说出 CASE 五功能各自的 2026 宿主与一句话理由。
2. 「建模即代码」相对桌面 CASE 套件的两条硬优势？
3. sqlite_schema 查询如何同时兑现 Ch5/Ch9/Ch12 三处「目录」承诺？
4. 正向/逆向工程成对出现的原因是什么？（提示：漂移）
5. DFD→血缘的语义升级发生在「文档 vs 事实源」哪一侧？

## 五、互链
- 上游：03（ER 词表）、04（Rule 1/4）、08（DDL 目标语言）。
- 下游：10（三案例是 CASE 全流程的手工演练场）。
- 谱系：[../Databases_Illuminated_4e/00-总览与阅读地图.md](../Databases_Illuminated_4e/00-总览与阅读地图.md)、[../Data_Observability_for_Data_Engineering/01-数据可观测性工程动机.md](../Data_Observability_for_Data_Engineering/01-数据可观测性工程动机.md)、[../Database_Modeling_and_Design_5e/00-总览与阅读地图.md](../Database_Modeling_and_Design_5e/00-总览与阅读地图.md)。

## 核心概念速览（中英对照）
| 中文 | 英文 | 出处/一句话 |
|---|---|---|
| CASE 工具 | CASE tools | Ch12 设计自动化套件 |
| 仓库 | repository | Ch12 CASE 中枢存储 |
| ER 报告 | ER diagram reports | Ch12 图→文档 |
| 数据流图 | data flow diagrams (DFD) | Ch12 流程侧模型 |
| 数据字典 | data dictionary | Ch12/Ch5/Rule 4 三栖 |
| 正向工程 | forward engineering | Ch12 图→DDL |
| 逆向工程 | reverse engineering | Ch12 DB→图 |
| 代码生成 | code generation | Ch12 交付自动化 |
| 输入输出设计 | input/output designs | Ch12 下游审查 |
| 绘图环境 | drawing environment | Ch12 符号与版面 |
| 模式漂移 | schema drift | 2.3/§3 当代词 |
| 建模即代码 | modeling as code | §2.1 重生形态 |
| 真相源三选一 | truth-source trio | §2.5 图/库/脚本 |
| 模式即代码 | schema-as-code | §2.5 迁移即模型 |
| 双向同步 | forward/reverse sync | §2.5 2016 答案 |
| 生成物评审 | generated-review gate | §2.6 人审铁律 |
| 自然语言生码 | NL to SQL | §2.6 LLM 副驾 |
| 运行时采集 | runtime cataloging | §2.6 目录自动发现 |
| 图即文本 | diagram-as-code | §2.7 评审流新画布 |
| 数据流图 | data flow diagram | ✅ 节题；血缘前身 |
| 血缘图 | lineage graph | §2.7 自动 DFD ⚠️ |
| 代码生成 | code generation | ✅ 节题；教学位序 §2.3 |
| 绘制环境 | drawing environment | ✅ 节题；双轨画布 |
| 功能搬家 | capability migration | §2.7 功能不死论 |
| 元数据反推 | metadata reverse-engineering | 🔧 §2.2（非本书示范） |
| 最小 CASE 工作台 | minimal CASE bench | 🔧 三行元数据+闭包脚本（文末注） |
| 报告自动化 | reporting automation | §2.7 ER 报告→文档流 |
| 工具尸检法 | tool autopsy | §2.1 功能去向清单法 |

## 最新演进与工业实践
- 元数据即产品：数据目录（含业务元数据+血缘+质量分数）成为独立采购品类；Ch12 的「数据字典」小节读毕应直接对读 [../Data_Observability_for_Data_Engineering/00-总览与阅读地图.md](../Data_Observability_for_Data_Engineering/00-总览与阅读地图.md)（在册 ✅）与 Fabric 线目录实践（../Data_Engineers_Guide_to_Microsoft_Fabric/00-总览与阅读地图.md 在册 ✅）。
- 「图」的文本化：DBML/PlantUML-ER/Mermaid-erDiagram 使 ER 图可 diff 可评审——本波 00 §二取证链的「目录即证据」精神与之一致：结构描述进入版本控制是一切自动化的前提。
- 🛠️ 低成本课堂重建（非本书示范）：SQLite+三行元数据查询+递归 CTE 闭包脚本（E3）即可搭「最小 CASE 工作台」：字典读取、依赖检查、DDL 生成三件套，替代已逝的桌面套件教学。
- 本章是工具章保质期标本：软件名过期、功能清单全部转生（§2.7 文末注在册）。
- 🔧 三行元数据查询+闭包脚本=零安装最小 CASE 工作台（demos/E3；非本书示范）。
- schema-as-code 评审流：PR 即建模评审、合并即发布——工具换三代，一致性教义不换（§2.5）。
- LLM 生码给 Code Generation 节加「评审者能力税」：不会写的人审不动生成物（§2.6）。
- DFD 墓碑与复活：设计工具死、运行时视图活——列级血缘是转正通知书（§2.7）。
- 毕业判据：六节功能（✅）各配一个 2026 去向（§2.1 清单默写）。
- 数据字典报告节与 04 §2.7 同谱系：目录工业两页源头。
- 逆向教训：库是运行时真相、图是设计时真相——两者须版本会师（§2.5 ⚠️）。
- 「工具服务于模型一致性」命题的盘上纵深走工具册——本章只给判据。
- 双轨画布含义：鼠标保交互、代码保 diff——缺一则评审断链（§2.7）。
- 本章与 10 互文：CASE 输入=案例产物——图、文、库三件对账。
- E3 复用登记：闭包脚本即依赖检查功能——06/09 一样本（00 §六）。
- 报告职能升格：ERD→文档→目录卡片——元数据即交付物（⚠️）。
- §2.1/§2.6 合表可作工具选型提纲——教材文体、采购用途。
- 波尾登记：本章不产生新对外链；盘上承接全走 00 §七账。
