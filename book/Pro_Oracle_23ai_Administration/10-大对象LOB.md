# 10 · 大对象 LOB（原书 Ch.11, pp.327-345）

> 章题 ✅ Crossref 实抓（DOI 10.1007/979-8-8688-1038-1_11, "Large Objects"）。章内小节自拟 ⚠️。Oracle 行为一律 ⚠️ 转述；取证：Concepts ✅ https://docs.oracle.com/en/database/oracle/oracle-database/23/cncpt/index.html 、DBMS_LOB 等包 ✅ https://docs.oracle.com/en/database/oracle/oracle-database/23/arpls/index.html 。

## 10.1 LOB 家族与两种栖身方式

| 类型 | 承载 | 典型负载 |
|---|---|---|
| BLOB | 二进制 | 文档/图片/序列化对象 |
| CLOB | 字符（库字符集） | 长文本/XML/（23ai JSON 底层之一）|
| NCLOB | 国家字符集 | 多语长文本 |
| BFILE | **外置**文件的只读句柄 | 影像库挂载盘 |

- **内联（inrow）**：小块直接住行内（默认阈值约千字节级 ⚠️ 具体以文档为准，`enable/disable storage in row` 可控）；超限转**LOB 段**分块（chunk）存放，行内留定位器（locator）⚠️。
- BFILE 无 LOB 段、不随导出走（目录对象+OS 路径即全部依赖 →13 章目录对象同源）⚠️。

## 10.2 SecureFiles vs BasicFiles：本章的主战场

- **BasicFiles**：8i 时代的遗产布局（独立段、.freelist 风格链），行为兼容位 ⚠️；
- **SecureFiles**：11g 起旗舰——统一分配器、**压缩/去重/加密**三件套（`compress/deduplicate/encrypt` 子句，EE 许可项 ⚠️ 逐项核对）、better-than-VFS 的块管理；
- 判定：`dba_lobs.securefile` 列 + 表空间属性（SecureFiles 需 ASSP/本地管理+段自动管理空间）⚠️；
- 迁移路径：`dbms_lob.move`（Basic→Secure 在线迁移的官方梯子）⚠️；23ai 新库默认已是 SecureFiles（`dbfile_create_as_secure_files`? 口径为 `SECUREFILE` 默认行为，⚠️ 以参考手册为准）——**本章知识增量在"识别遗留 BasicFiles 并排期改造"**。

## 10.3 访问语义与事务纠缠

- **定位器生命周期**：SELECT 取回 locator，读写经它路由；`nocopy` 语义减少服务器内拷贝 ⚠️；事务边界外的 locator 失效（ORA-01002 类）是应用工单常客 ⚠️；
- LOB 读写仍受 UNDO/redo 支配：`nocache`/`cache`/`logging` 三旋钮决定 IO 与恢复语义（NOLOGGING 大装载与 12 章备份契约同 07 章逻辑）⚠️；
- LOB 段的空间行为独立于宿主表：HWM 不随 DELETE 自动还、`shrink space cascade` 才连带——"表小段大"名案 ⚠️（04 章 HWM 的 LOB 分册）；
- `DBMS_LOB` 包（GETLENGTH/READ/WRITE/APPEND/INSTR...）+ JDBC/OCI 流式 API 是服务端/客户端两条正门 ⚠️（✅ arpls 线）。

## 10.4 保留与一致性：LOB 的"版本学"

- 段内 LOB 的读一致性同样吃 UNDO；**SECUREFILE 独有**保留策略族（`retention`/`nopartitioning` 等，类比闪回保留窗口）：决定旧版本块何时可重用 ⚠️——ORA-01555 在 LOB 读场景的排障位在此；
- 分区表上的 LOB 分区对齐（`store as (as partition)`）与逐分区维护 ⚠️；
- 空间估算公式（管理侧草算 ⚠️）：LOB 段 ≈ 行数 × avg 长度 ÷ 压缩率 × chunk 取整放大——`average` 靠 `dbms_lob.getlength` 采样估。

## 10.5 JSON 时代的大对象（23ai 联动位 ⚠️）

- 23ai 原生 `JSON` 类型（06 章）的存储底层走 **BINARY JSON**，中小文档可 inrow、大文档落 LOB 段——"JSON 是不是 LOB"的正解：**语义层不是、物理层常常是** ⚠️（✅ adjsn/Concepts 文档线，措辞转述）；
- 运维推论：JSON 负载的容量模型要按 LOB 段方法算（chunk/平均文档尺寸），duality 视图（08 章）拆回的嵌套集合若含 JSON 列亦同 ⚠️ 本目录整理；
- XML DB（XMLType）是 LOB 章的传统连体兄弟：本册仅登记对象名，Stock/SecureFile 存储选项与 shredding 出范围 ⚠️。

## 10.6 本章陷阱清单（⚠️ 原书性格重构）

1. 用 VARCHAR2 拼长文本"绕过 LOB"→ 4000/32767 墙+转义地狱，两头成本；
2. 大 LOB 表与高并发 OLTP 同段混布：buffer cache 被 chunk 扫描冲刷（03 章缓存配置的连带案）；
3. 备份窗口未计 LOB 段体积：RMAN 增量对高 churn LOB 的收益折损（12 章）；
4. BFILE 迁移忘搬目录文件与授权——"逻辑备份完整、物理对象失踪"；
5. 客户端流式 API 误整读进内存：大文档 OOM 归应用层但根因在 DBA 未给容量指引。

教训共性：LOB 的事故多不在"LOB 列"本身，而在它与表/段/备份/缓存四邻的接缝处 ⚠️。

## 10.7 LOB 盘点与巡检 SQL 骨架（⚠️ 示意）

```sql
-- 全家底: 谁是 BasicFiles、谁还内联、chunk 多大
select owner, table_name, column_name, securefile, retention, chunk, tablespace_name
  from dba_lobs where owner not in ('SYS','XDB');
-- 段大小与宿主表脱节度(10.4 空间账)
select segment_name, bytes/1024/1024 mb from dba_segments
 where segment_name like 'SYS_LOB%' order by bytes desc fetch first 10 rows only;
-- 平均文档/大字段尺寸采样(容量模型输入)
select avg(dbms_lob.getlength(doc)) avg_len, count(*) from json_docs sample (10);
-- SecureFiles 化迁移(在线梯子的骨架, 停机面评估先行)
alter table docs move lob(doc) store as securefiles
  (enable storage in row chunk 8192 compress high) online;
```

巡检三看：**看身份**（securefile 列，改造排期依据）、**看体量**（LOB 段 vs 表段比例，备份窗口与缓存冲刷预警）、**看策略**（inrow 阈值/chunk/retention 与负载形态匹配）⚠️。

## 10.8 LOB 负载的容量-性能联算（⚠️ 承 03/04 章）

- **缓存经济学**：LOB chunk 不进 buffer cache（nocache 默认倾向），但 locator 操作与 inrow 部分进——"LOB 表热"多数热在元数据与小块，分表策略按"大小块混布比例"定 ⚠️；
- **重做账**：LOB 写产生 redo（logging 缺省下），cache/nocache × logging/nologging 旋钮组合决定 I/O 与恢复语义，nologging 的备份契约同 07 章；批量装载三件套=并行+append+LOB nologging 段（或干脆走 13 章 DATAPUMP 外部表路线）⚠️；
- **压缩红利估算法**：随机二进制（已加密/已压缩的图像）压缩率趋零，文本/XML 族收益显著——**先采样再建表**：`dbms_lob` 抽样 + `compress` 试验表对比字节数，别信厂商通用倍数 ⚠️ 本目录立场；
- **去重适用问句**："同一文件多行引用"形态（模板库/附件复用）才有 dedup 红利，且要求全 chunk 对齐——OLTP 图片列基本无戏 ⚠️。

## 10.9 LOB 与备份/恢复的三笔暗账（⚠️ 联动 12 章）

1. **体积账**：LOB 段常为"库大的真正原因"——增量备份（12.2）的读放大与备份窗口被 LOB churn 主导，level1 收益对高频覆写 LOB 折损明显 ⚠️；
2. **NOLOGGING 账**：LOB 段 nologging 化的批量件不在恢复重放内——`report unrecoverable` 名单常客（12.5 契约在本章的具名债务）⚠️；
3. **一致性账**：大对象分块写+多段（inrow 行/LOB 段/BFILE 外置件）=**备份一致性覆盖不到的"第三样"**：恢复后 BFILE 指向的 OS 文件是另一台主机的旧版——外置件必须有独立快照/副本计划，写进 12.8 演练日历的跨件项 ⚠️。

三账合并一句话：**LOB 把"备份数据库"变成"备份数据库+文件系统+密钥"**——交付物清单要跟着变大 ⚠️ 本目录立场。

## 自测（能默写=过关）

- 内联/段存两栖的判定阈值与 locator 的角色。
- SecureFiles 三件套各自开关、许可注意与判定视图。
- LOB 读一致性为何吃 UNDO、SECUREFILE 保留策略答什么题。
- 内联阈值调整（enable/disable storage in row）分别服务的两类负载。
- BFILE 在备份交付物清单里的正确写法（三件套：件+目录对象+授权）。
- 23ai JSON 与 LOB 的语义/物理两层关系一句话。

**复述模板（各 3 句内）**：向开发解释"为什么 VARCHAR2 存不下这篇合同"；向审计解释"为什么加密备份的密钥托管单比备份单更重要"；向运维解释"为什么删了数据、备份窗口却没跟着变小"。

**串读题（≤5 句答）**：一张存合同 PDF（BLOB）+ 全文（CLOB）+ 签署状态（BOOLEAN，23ai 新列型）的表，上线前你要给运维/审计/备份三方各留哪一条说明？——三方各对应 §10.8 压缩采样、§10.9 加密密钥、§10.9 BFILE/段账之一，答对即本章毕业。

## 核心概念速览（中英对照）

- **LOB** — large object：BLOB/CLOB/NCLOB/BFILE 家族总称。
- **定位器** — locator：指向 LOB 值的句柄，随事务存活。
- **内联存储** — inrow/in-line storage：小值住行内免跳段。
- **chunk** — LOB 块大小：LOB 段分配与 I/O 的原子粒度。
- **BasicFiles** — 遗产 LOB 布局：兼容但无压缩/去重红利。
- **SecureFiles** — 现代 LOB 布局：压缩/去重/加密+统一分配器。
- **去重** — deduplication：相同 LOB 值只存一份段内物理块。
- **NOCACHE/CACHING** — 缓存策略族：LOB 读写的 buffer 与日志三旋钮之一。
- **DBMS_LOB** — LOB 服务端操作包：读写/截断/比对全家桶 ✅ arpls。
- **BFILE** — 外置文件 LOB：只读句柄，不随库备份走。
- **保留策略** — LOB retention：段内旧版本块可重用前的保护窗口。
- **BINARY JSON** — 23ai JSON 的二进制物化形态，大块经 LOB 通道 ⚠️。
- **storage in row** — 内联开关：强制小值住行内或一律出段的表态条款。
- **LOB 段（SYS_LOB*）** — 大值本体所在独立段，与宿主表段分账计量。

## 最新演进与工业实践

- **对象存储合流（⚠️ 转述）**：23ai/26ai 线 DBMS_CLOUD/对象存储直连族把"库外大文件"纳为库内可查询资源（✅ 官方 PL/SQL 包参考线含 DBMS_CLOUD 族；本册正文未展开），与 BFILE 的"挂载盘"哲学构成两代外置方案对照 ⚠️。
- **JSON 对 LOB 章的改写**：文档负载新贵多走 JSON 类型+duality 视图（08 章），LOB 章的存量重心移向"历史 CLOB 列的瘦身与 SecureFiles 化"——数据湖仓对照：大对象外置+表格式管理成为湖仓主流叙事（盘上 [../Delta_Lake_Definitive_Guide/00-总览与阅读地图.md](../Delta_Lake_Definitive_Guide/00-总览与阅读地图.md)、[../Apache_Iceberg活用入門/00-总览与阅读地图.md](../Apache_Iceberg活用入門/00-总览与阅读地图.md)），与"库内 LOB"形成两种成本曲线 ⚠️ 立场句。
- **AI 负载带入的新体量**：向量列（07 章）+文档原文（BLOB/CLOB）+embedding 管道的组合是 2024+ RAG 落地标准件，LOB 容量模型第一次进了 AI 基建预算表 ✅（vldbg 文档线的用例章 ⚠️ 转述）。
- **跨引擎对照（盘上）**：PG 的 TOAST（行外压缩切片、自动触发阈值）与 Oracle LOB 的"手动声明型"哲学差异是建模课经典题，见 ../PostgreSQL_16_Administration_Cookbook/00-总览与阅读地图.md；MySQL InnoDB 大字段页外溢（overflow page）机制对照见 ../Understanding_MySQL_Internals/00-总览与阅读地图.md——三家都把"大值"请出行内，参数名与自动度各异；本目录未做 TOAST 类比实测（🔧 面留给 04/07/09 章组）。
