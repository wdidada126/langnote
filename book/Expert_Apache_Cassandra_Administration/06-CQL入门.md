# 06 Introduction to the Cassandra Query Language（CQL 入门）

> 原书第 6 章章名 ✅ Crossref 实抓；小节结构为推定重构 ⚠️。语法示例按 CQL 3.x 通识
> 重构（⚠️ 非原书代码），执行细节以官方 CQL 3.11 文档域为基线转述。

## 题纲

CQL 是运维面的"合同语言"：schema 用 DDL 谈定，读写用受限查询兑现，权限与批量语义在
附录里各自安家。本章按 DDL→DML→函数/UDF→batch/LWT 的顺序走一遍，并给每类语句标上
"运维后账"（04/05/11 章回环）。

## 1. DDL：先谈键空间再谈表

```sql
CREATE KEYSPACE app WITH replication =
  {'class':'NetworkTopologyStrategy','dc1':3,'dc2':3};  -- 03 章的决定
CREATE TABLE app.events (
  sid uuid, ts timeuuid,                 -- 分区键 sid，聚簇 ts 升序
  kind text, payload text,
  PRIMARY KEY (sid, ts))
  WITH CLUSTERING ORDER BY (ts DESC)
  AND compaction = {'class':'TimeWindowCompactionStrategy'}   -- 05 章选型
  AND default_time_to_live = 7776000;    -- 3 个月自动过期（治删除账单）
```

- 表选项里运维可见的：compaction、`bloom_filter_fp_chance`、`crc_check_chance`、
  compression、`speculative_retry`（SLFR 参数，11 章）。
- ALTER 的雷区（⚠️ 通述）：加列便宜；**改类型近乎不可**；聚簇列不可改；
  schema 变更是全环传播事件，需 `describecluster` 验一致（03 章验收单同款）。
- DROP/TRUNCATE 语义与快照时机（8 章）：TRUNCATE 不走墓碑、直接清表——恢复只能靠快照。

## 2. DML：受限查询是特性不是缺陷

- `INSERT/UPDATE/DELETE`：UPDATE=部分列 upsert，DELETE 可只删列/删范围（=写墓碑，04 章账单）；
  `IF NOT EXISTS` / `IF col = ...` 触发 LWT（SERIAL 一致性、分区内 Paxos，性能另议）。
- `SELECT` 三规矩：WHERE 必含分区键等值（IN 可放宽但要节制）、
  聚簇列按前缀、非常规过滤要 `ALLOW FILTERING`（=全表扫的合法化外衣，生产禁用为默认立场 ⚠️）。
- 排序/分页：ORDER BY 只能聚簇序（或倒序表选项）；驱动天然游标分页（02 章 cqlsh PAGING 同源）。
- 聚合：count/min/max/sum/avg 限分区内或全表慢路；`GROUP BY` 是后话（4.x+，见文末）。

## 3. 类型与函数（3.x 基线速查）

- 标量：`int/bigint/smallint/tinyint/varint/double/float/decimal/boolean/text/ascii/
  blob/uuid/timeuuid/timestamp/date/time/duration/inet`（3.x 后期全集 ⚠️ 通述）。
- `timeuuid→unixTimestamp/minTimeuuid` 系列：时序表的主键搭档。
- 集合函数：`size()/contained/[]`；容器更新语法（`+`/append）注意并发覆盖警告（04 章）。
- 3.x 起 **UDF/UDA 转 GA**（⚠️ 通述）：`CREATE FUNCTION ... CALLED ON NULL INPUT`；
  Java 语言 UDF 默认禁用、须显式开关——升级 4.0 起 Java UDF 被移除、改脚本语言的路线在文末。

## 4. BATCH 与 UNLOGGED 的真相（11 章性能预告）

- `BEGIN BATCH ... APPLY BATCH` 三种：logged（默认，原子+batchlog 开销）/
  unlogged（免 batchlog，**不**跨分区原子）/ counter。
- 运维口径（⚠️ 通述）：batch 不是批量提升吞吐的工具（驱动异步+连接池才是），
  只在"多分区原子失败-重试"需求时用 logged；跨 DC 分布的 logged batch 走 batchlog 复制，延迟加倍。

## 5. 与权限/安全的接缝（12 章预告）

- `CREATE ROLE / GRANT SELECT ON TABLE ... TO ...` 语法归 CQL；
  认证授权开关归 yaml。本书顺序是先会 CQL 再谈锁门——运维时两者要一起验收。
- `LIST ROLES`/`describe role` 是审计工单的第一现场。

## 6. 本章运维判例（精读重构）

1. "SELECT 慢" → 先看是否 ALLOW FILTERING/全表扫，再看墓碑数（05 章）。
2. "UPDATE 没生效" → 查时间戳来源：客户端生成 vs 服务端 now()，LWT 与同刻写竞态（04 章）。
3. "INSERT 报 cannot insert batchlog" → batchlog 所在 DC RF 异常（03 章拓扑题）。
4. "schema 改动部分节点未生效" → describecluster 不一致 → 走修复流程（9 章）。

## 7. CQL 速查卡（本章面）

```sql
-- DDL
ALTER TABLE app.events ADD tags set<text>;                  -- 加列便宜
ALTER TABLE app.events WITH compaction = {'class':'TimeWindowCompactionStrategy'};
DROP TABLE app.events;                                      -- 先快照！(8 章)
-- DML
UPDATE app.events USING TTL 3600 SET payload='x' WHERE sid=? AND ts=?;
DELETE tags['urgent'] FROM app.events WHERE sid=? AND ts=?; -- 删集合元素=墓碑(04 章)
INSERT INTO app.events (...) VALUES (...) IF NOT EXISTS;    -- LWT/SERIAL
-- 查询合同
SELECT count(*) FROM app.events WHERE sid=?;               -- 分区内聚合 OK
SELECT * FROM app.events WHERE kind='a' LIMIT 100;         -- ✗ 无分区键
SELECT * FROM app.events WHERE kind='a' ALLOW FILTERING;   -- 生产默认拒绝
-- 元信息
LIST ROLES; LIST PERMISSIONS OF app_rw;
SELECT keyspace_name, table_name FROM system.schema_columns; -- 3.x 系统表(4.x+ 改 system.*)
```

## 8. 本章十问（自测）

1. 表选项里哪些直接影响运维账单？（§1）
2. 聚簇序"建表定死"的自由度具体剩多少？（§1）
3. TRUNCATE 与 DELETE 的恢复路径差别？（§1/8 章）
4. "UPDATE=部分列 upsert"在 cell 层意味着什么？（§2）
5. 范围 DELETE 的墓碑后果与替代方案？（§2/04 章）
6. SELECT 三规矩各对应哪条底层约束？（§2）
7. 3.x UDF 的语言开关与升级路线风险？（§3/文末）
8. logged batch 何时才是"对的用法"？（§4）
9. `token()` 函数的运维用途？（速览/9 章）
10. 2026 年 GROUP BY/vector 函数分别补了什么课？（文末）

## 核心概念速览（中英对照）

- **keyspace** — 键空间：RF/DC 策略挂载点，schema 传播的基本单元。
- **clustering order** — 聚簇序：建表时定死（可 DESC 反转一次），查询排序的全部自由度。
- **default_time_to_live** — 表级默认 TTL：用过期代替删除，压墓碑存量。
- **upsert** — 插入即更新：CQL 的 INSERT/UPDATE 在 cell 层面同义。
- **LWT** — 轻事务：IF 条件写入，分区内 Paxos，SERIAL/LOCAL_SERIAL 一致性。
- **ALLOW FILTERING** — 过滤豁免：允许非常规查询的开关，生产默认拒绝。
- **UDF/UDA** — 自定义函数/聚合：3.x GA，语言沙箱与升级路线多舛。
- **logged batch** — 原子批：经 batchlog 保证投递原子，性能税自负。
- **batchlog** — 批日志：跨分区写意图的暂存副本系统表。
- **token(...)** — 环查询函数：SELECT ... WHERE token(pk)... 查数据在环上的落点（9 章用）。
- **WRITETIME** — 版本时间戳探针：诊断 last-write-wins 竞态的望远镜（4.x+ 增 UNIXTIMESTAMP_OF 家族）。
- **TRUNCATE vs DELETE** — 清空分野：前者瞬时清表，后者全量写墓碑。
- **GRANT/REVOKE** — 授权语句：与 yaml 的 authorizer 开关配对生效。

## 最新演进与工业实践

- **5.0 的 CQL 增量（✅ 官方 new features 页实抓）**：新数学函数 `abs/exp/log/log10/round`、
  集合的新原生标量函数、**vector 类型与 similarity 函数（CEP-30）**、
  集合/UDT 上可取 **TTL()/writetime()**、**动态数据脱敏 DDM（CEP-20）** 的列级语法——
  本章"3.x 速查表"到 2026 年按此扩列。
- **GROUP BY/标量子查询线**：`GROUP BY` 自 4.x 引入、聚合持续补强（⚠️ 精确 minor 版本不可实证）；
  与 SQL 的差距逐年收窄但"必带分区键"的合同从未撕毁。
- **UDF 沙箱换代**：4.0 移除 Java 语言 UDF、引入沙箱化 JS/ WASM 实验路线（CEP-36）⚠️ 通述；
  本书的 Java UDF 剧本在 4.x+ 集群等于技术债。
- **协议与驱动**：原生协议 v5（beta v6）+ 各语言新驱动成为默认通道；
  thrift 于 4.0 移除（✅ NEWS.txt）后，"CQL-only"从运维建议变成物理事实。
