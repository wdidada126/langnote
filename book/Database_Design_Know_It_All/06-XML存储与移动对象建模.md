# 06 · XML 存储与移动对象建模（合集第 10+11 章）

> **覆盖**：原书 Ch.10 *Storing XML* + Ch.11 *Modeling and Querying Current Movement*（✅ 章题实抓）。
> **归源（✅ 实证）**：
> - Ch.10 ← Melton & Buxton（等）《Querying XML》(Morgan Kaufmann, ISBN 978-1-55860-711-8) 之 *Storing: XML and Databases* 章，DOI 10.1016/b978-155860711-8/50009-5（章记录 2006 口径 ⚠️ 年份从源书版权页）；
> - Ch.11 ← Güting & Schneider《Moving Objects Databases》(Morgan Kaufmann 2005, ISBN 978-0-12-088799-6) 同名章 *Modeling and Querying Current Movement*，DOI 10.1016/b978-012088799-6/50004-9（同书另有 *...History of Movement* 章 50005-0 ✅，合集未选）。
> 撰稿人 Jim Melton（SQL/XML 标准操盘人，盘上 [../SQL_and_Relational_Theory/00-总览与阅读地图.md](../SQL_and_Relational_Theory/00-总览与阅读地图.md) 一系的标准侧证人）、Ralf Hartmut Güting、Markus Schneider（空间/时态数据库两大名家）。精读重构，非原书文本。

## 1. Ch.10 · XML 存储：文档与关系的二十年婚姻咨询（⚠️ 重构）

### 1.1 三种存储姿态（SQL/XML 时代格局，2006 口径）

1. **文件系统外挂**：XML 存 OS/LOB，DB 只登记路径——查询能力归零，完整性归零；
2. **整体存储（whole-document）**：XMLType/CLOB 列存整档 + 路径索引（order/path），配合 `extractValue()` 类函数——写快读抽，更新粒度粗；
3. **分解存储（shredding）**：把文档按 DTD/XML Schema 拆进关系表（结点表 Big Row/Element-centric 等模型 ⚠️ 术语转述），查询走 SQL、重组靠 `XMLELEMENT/XMLFOREST/XMLQUERY`——读写俱佳，装载与模式维护最贵。

Melton 立场（标准作者视角 ⚠️ 转述）：**SQL 与 XML 是互补而非替代**——数据有结构时关系模型赢，结构漂移/异构交换时文档模型赢；设计问题=为负载选姿态，并为混合形态（部分分解+残档整体保存）留退路。

### 1.1.1 三姿态决策表（重构 ⚠️，非原书表格）

| 维度 | 文件外挂 | 整体存储 | 分解存储 |
|---|---|---|---|
| 装载速度 | 最快（零解析） | 快 | 慢（解析+校验） |
| 查询粒度 | 无 | 路径抽取 | 任意关系运算 |
| 更新代价 | 全文档替换 | 文档级/部分† | 行级精确 |
| 模式维护 | 无成本 | 低 | 高（双模式同步） |
| 典型场景 | 归档/外发交换 | 日志型流水 | 主数据/交易 |

†部分更新（updateXML 类）2008 为商业引擎卖点（⚠️ 不可实测）。

### 1.2 🔧 类比实测：shredding 的语义与代价（SQLite 3.45.3，✅ 实跑 E6）

300 份 `<order><cust/><item sku qty/></order>` 文档双轨入库（python 标准库 xml.etree 解析，脚本 E6）：

- CLOB 整档列 + `doc LIKE '%S3%'`：**0.083ms**，命中 43；
- shredding 成 `xitem(oid,sku,qty,cust)` + `WHERE sku='S3'`：**0.028ms**，命中 43（等值可索引）。

样本太小仅示**语义**：分解后"属性变列、列可建索引、结果可 JOIN"三件事同时发生。⚠️ 商业引擎的 XMLType/注册模式、路径索引（Oracle）、`xml_column`（DB2）均不可本机实测；现代替代品 PostgreSQL `xmltype()`/SQL/XML 见 ✅ https://www.postgresql.org/docs/current/datatype-xml.html （200 可达）——SQL 标准里的 XML 类型在开源世界的活标本。

### 1.3 本章的 2026 墓志铭与转世

XML 作为**交换格式**败给 JSON（REST→Webhook→配置文件全线），但作为**存储建模问题**赢了：Ch.10 的三姿态逐字平移到 JSON 文档入仓的讨论（原样存/半结构化列/拍平成表）——SQLite JSON1 扩展（✅ https://www.sqlite.org/json1.html ，200）、DuckDB 的 JSON/嵌套类型路线即当代战场；SQL:2023 的 SQL/JSON 表函数把"shredding"标准化为 `JSON_TABLE`（⚠️ 标准号转述）。对读盘上：[../bigdata/09-存储与文件格式.md](../bigdata/09-存储与文件格式.md)（列存文件格式层的文档嵌套处理）。

## 2. Ch.11 · 移动对象的"当前运动"建模（⚠️ 重构）

### 2.1 问题设定

Güting 谱系的经典设定：跟踪器持续上报轨迹点 `(tracker, t, x, y[, v, heading])`，数据库要同时服务两类质询：

- **当前态查询**："现在谁在缓冲区 R 内？"——高频、要毫秒答；
- **历史/预测查询**："昨天 10 点谁在近机场路？""按当前速度 5 分钟后谁出界？"——合集未选的姊妹章 *History of Movement* 主题。

设计核心矛盾：**新鲜度 vs 存储 vs 查询模式**。三种基线方案：

1. **现态表**（current snapshot：每跟踪器一行，UPDATE 覆盖）——当前查询秒杀，历史全丢；
2. **历史表**（append-only 全轨迹）——历史全在，"当前"= `MAX(t)` 分组切片，贵；
3. **混合+轨迹数据类型/分段线性函数建模**（TLinP 等表示 ⚠️ 术语转述）——学术解，工程上退化为"热层现态+冷层分区轨迹"。

网络约束移动（road network，位置=路段+偏移）是本章的另一半：欧氏空间索引（R-tree 族 ⚠️）不再适用，改用路网图+最短路径距离——这是当年"特殊负载要不要特殊模型"的极端教具。

### 2.1.1 概念查询示意（依 Güting 系论文语言重构 ⚠️，不可执行）

```text
-- "现在谁在(2,2)半径5之内"
SELECT * FROM vehicles WHERE within(location, circle(point(2 2), 5), now());
-- "10:00~11:00 期间走过某走廊的车辆"（历史谓词，合集未选的姊妹章主题）
SELECT * FROM vehicles WHERE over(track, linestring(…), during([10:00, 11:00]));
```

两类谓词共用一套"位置随时间变化"的抽象——当年靠专用数据类型（seqdata/moving real）实现 ⚠️；今天拆给"空间类型+时间旅行+流状态"三件商品化拼图。

### 2.2 🔧 类比实测：当前切片的税（SQLite 3.45.3，✅ 实跑 E7）

200 跟踪器×1000 时刻=20 万点：

- 历史表求"ts=999 且 x>1000"切片：**6.69ms**；
- 现态表同谓词直查：**0.01ms**（约 670x 差）。

数字即本章全部设计张力：要么每次付切片的税，要么预维护一张会撒谎的快照（更新滞后=脏"当前"）。**工程折中是三层**（⚠️ 重构）：热层=现态表+最近增量（秒级新鲜度承诺）、温层=时间分区历史表（切片税可接受）、冷层=压缩轨迹归档（查询走导出通道）；TTL 与"现态更新滞后预算"作为设计工件写入文档——这正是 Ch.11 权衡在 2026 时序数据库产品手册里的直系后代。⚠️ 本书时代的轨迹索引（RTree 3D、TP-Tree 等）不可实测；现代对位：PostGIS 及其时态扩展 ✅ https://postgis.net/ （200）。

### 2.3 谱系对读

- 时序数据库=移动对象学的工业转世：盘上 [../Time_Series_Databases/00-总览与阅读地图.md](../Time_Series_Databases/00-总览与阅读地图.md)（其"最新值视图+压缩历史"正是 §2.1 方案 3 的商品化）；
- 流式新鲜度：现态表维护的现代形态=流上增量维护的物化视图——[../Streaming_Systems/00-总览与阅读地图.md](../Streaming_Systems/00-总览与阅读地图.md)；
- 空间数据论文线：[../../db/db.md](../../db/db.md)。

## 3. 为什么编辑把这两章放在合集末尾（⚠️ 推定）

2008 年的"数据库设计前沿"=**半结构化**与**带时间轴的连续域**两大越狱运动；两章给前半部"静止关系世界"的问题集各加一维（结构维、时间维）。今天回看：XML 一维被 JSON+列存格式吸收，移动一维被时序/流式吸收——**前沿两章全部过时但全部转世**，这是精读它们唯一正确的姿势。

## 4. 自测题（重构 ⚠️）

1. 电商订单报文（结构十年稳定、查询全是关系聚合）选三姿态哪种？（分解为主+残档归档兜底——决策表 §1.1.1 逐格论证。）
2. 传感器"最新读数"大屏用现态表还是历史切片？给出 🔧E7 数字支持你的选择，并说明失效模式（更新滞后=脏当前态）。
3. shredding 后"模式双维护"具体维护哪两份 schema？（DTD/XMLSchema 与关系 DDL，二者演进节奏必须锁死。）
4. 网络约束移动为什么让 R-tree 失效？（距离度量从欧氏换到图上最短路，包围盒语义崩塌。）
5. `JSON_TABLE` 时代"谁审计 FD"？（回到 03 文件清单——工具换了，纪律没换。）

## 核心概念速览（中英对照）

- **整体存储** — Whole-document Storage：XMLType/CLOB 存全档+路径索引，更新粒粗（⚠️ 商业机制转述）。
- **分解存储** — Shredding：文档拆为关系表列，读写全走 SQL（🔧E6 语义）。
- **部分分解** — Hybrid/Partial Shredding：热路径拆列、冷残档整存，设计留退路。
- **SQL/XML** — ISO 标准原语：XMLELEMENT/XMLFOREST/QUERY 族（Melton 主其事 ⚠️）。
- **DTD/XML Schema** — 模式声明：shredding 的前提，结构漂移的度量衡。
- **跟踪器** — Tracker/Moving Object：持续上报位置的实体，数据=带时间戳采样流。
- **当前态查询** — Current/Now Query：对"新鲜度"敏感的即时质询（🔧E7 现态表）。
- **历史切片** — Snapshot at Time Point：MAX(t)/时间戳定位，付扫描税（🔧E7 6.69ms）。
- **分段线性表示** — Piecewise Linear (TLinP)：轨迹的函数化建模（⚠️ 术语转述）。
- **网络约束移动** — Network-constrained Movement：位置=路段+偏移，欧氏索引失效。
- **新鲜度 vs 存储** — Freshness/Storage Duality：移动对象设计的第一权衡。
- **模式迁移** — Schema Migration for Documents：结构漂移下 DDL 治理的失能区。
- **路径索引** — Path Index：整体文档内抽取加速的二级结构（⚠️ 商业引擎转述）。
- **时间切片** — Time Slicing：从 append-only 轨迹重建"某时刻快照"（🔧E7 交税模型）。
- **冷热分层** — Hot/Warm/Cold Tiering：新鲜度预算的产品化落点（⚠️ 重构）。

## 最新演进与工业实践

1. **XML→JSON 的存储战争收官**：2026 语义上 Ch.10 应改名 "Storing JSON"。三姿态原样平移：原样 CLOB/`json` 列→shredding→`JSON_TABLE`/jsonb/GIN——SQLite JSON1 ✅ https://www.sqlite.org/json1.html （200）、DuckDB 原生嵌套+✅ 扩展目录 https://duckdb.org/docs/stable/core_extensions/overview （200）、PostgreSQL XML/JSON 类型文档 ✅ https://www.postgresql.org/docs/current/datatype-xml.html （200）。湖仓侧 Parquet/Iceberg 的嵌套列处理见 [../bigdata/09-存储与文件格式.md](../bigdata/09-存储与文件格式.md)；XML 仅存于公文/GIS/金融报文等强制 schema 世界（⚠️ 行业观察转述）。
2. **移动对象学分裂为三**：时序数据库（现态+历史一体：盘上专册 [../Time_Series_Databases/00-总览与阅读地图.md](../Time_Series_Databases/00-总览与阅读地图.md)）、流处理（"当前"=增量维护的状态：[../Streaming_Systems/00-总览与阅读地图.md](../Streaming_Systems/00-总览与阅读地图.md)）、空间分析（PostGIS/DuckDB spatial ✅ https://postgis.net/ ）。Güting 的函数化轨迹建模未成商品，但其"查询语言要认识时间"的主张全面胜利（temporal tables、time travel 已是云仓默认卖点 ⚠️ 转述）。
3. **向量对象是新"移动对象"**：embedding 漂移（模型换代=坐标系搬家）与轨迹新鲜度问题同构，故向量索引+元数据版本化吃的是 Ch.11 的问题卷——对读 [../Vector_Databases/00-总览与阅读地图.md](../Vector_Databases/00-总览与阅读地图.md)。
4. **IoT/车联网场景的教具价值**：本章的"每跟踪器一行 vs append-only"抉择在 2026 仍每台车每天发生一次，只是栈名换成 MQTT→时序库→对象存储分层（⚠️ 实践综述）。🔧E7 的 670x 切片税是选型会上少数可当场演示的数字。
5. **不可实测声明**：SQL/XML 全功能、XMLType 路径索引、轨迹索引结构（RTree/TP-Tree）、DB2 pureXML、Oracle XMLDB 均属 ⚠️ 文档转述范围——本文件零伪装；取证口径见 [00-总览与阅读地图.md](00-总览与阅读地图.md) §7/§9。
