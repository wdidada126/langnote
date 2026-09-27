# 02 表数据与 psql 自动化（原书第 5、7 章）

> 覆盖原书章：**Ch5 Tables and Data · Ch7 Database Administration**。章题 ✅ 双源核实；
> 食谱级小节 ⚠️ 推定（依据搬书匠条目摘要对两章主题的描述：去重/测试数据/装载/分区/MERGE/JSON；可重复脚本/psql 变量与条件）。
> 所有 SQL 为**文档转述 ⚠️**（本机无 PG 实例）。

## 本章地图

| 主题 | 你能做到 | 关键对象/命令 |
| --- | --- | --- |
| 数据类型选型（Ch5） | 用对 JSON/JSONB、数组、范围、IDENTITY 列 | `jsonb`、`GENERATED ... AS IDENTITY`、`serial` vs `identity` |
| 清重复数据（Ch5） | 定位并删除键重复行，留最小 ctid | `ctid`、窗口函数 `row_number()`、自连接 DELETE |
| 造测试数据（Ch5） | 百万行合成数据灌入 | `generate_series`、`md5(random()::text)`、`setseed` |
| 批量装载（Ch5） | COPY 快导快入、路径与权限 | `\copy` vs `COPY`、`COPY FROM program` |
| 分区表（Ch5） | 声明式分区 RANGE/LIST/HASH，裁剪与全局索引缺位认知 | `PARTITION BY`、`pg_partition_tree` |
| MERGE（Ch5） | 一条语句 upsert/差分同步 | `MERGE INTO ... WHEN MATCHED/NOT MATCHED` |
| psql 脚本化（Ch7） | 可重复执行的维护脚本 | `\set`、`\gset`、`:variable`、`\if`、`\echo`、`-v ON_ERROR_STOP=1` |

## 核心精讲

### 1. 去重：ctid 是 PG 的"物理行号"（Ch5，⚠️ 重构）

文档转述 ⚠️：

```sql
DELETE FROM t a USING t b
WHERE a.ctid < b.ctid AND a.k = b.k;   -- 同键保留较大 ctid（习惯写法，语义等价于去重留一）

WITH dups AS (
  SELECT ctid, row_number() OVER (PARTITION BY k ORDER BY ctid) rn FROM t
)
DELETE FROM t WHERE ctid IN (SELECT ctid FROM dups WHERE rn > 1);
```

- 先 `SELECT` 审计再 `DELETE`，配合 `CREATE TABLE t_dup_backup AS ...`——本书反复强调"先看再删"的运维纪律。
- `ctid` 会被 vacuum HOT 整理改变，不能作为长期外键；临时去重可用。

### 2. 测试数据三件套（Ch5）

```sql
INSERT INTO sales
SELECT g, (g % 1000) + 1, (random()*1000)::numeric(10,2),
       timestamp '2020-01-01' + (g || ' sec')::interval
FROM generate_series(1, 1000000) g;
SELECT setseed(0.42);                  -- 可复现随机序列
```

### 3. 装载：COPY 的两种拼法与 program 流（Ch5）

- `COPY ... FROM '/abs/path'`：服务器侧读写，受 `pg_read_server_files` 角色或超级用户限制，路径在**服务器**文件系统。
- `\copy ... FROM 'local'`：psql 客户端代跑，普通用户即可——本书把"分不清 COPY 与 \copy"列为经典坑。
- `COPY t FROM PROGRAM 'gzip -dc file.gz.csv'`：装载压缩文件零临时落地。
- 性能细节：装载期 `maintenance_work_mem` 调高、索引后置（先 COPY 再建索引）、`synchronous_commit = off` 仅限灌数会话。

### 4. 声明式分区（Ch5）

```sql
CREATE TABLE log (ts timestamptz, msg text) PARTITION BY RANGE (ts);
CREATE TABLE log_2024q1 PARTITION OF log
  FOR VALUES FROM ('2024-01-01') TO ('2024-04-01');
SELECT * FROM pg_partition_tree('log');
```

- PG16 事实（✅ 发行说明）：逻辑复制初始同步可走**二进制格式**（订阅 `binary` 选项）、大事务**并行应用**——分区+逻辑复制组合更顺。
- 裁剪（partition pruning）要求约束落在查询谓词可证明的范围内；`ts` 用函数包裹会失剪。
- 无跨分区全局唯一索引：唯一约束只能在分区内（PG11+ 行为，本书语境下仍成立）。

### 5. MERGE：PG15 起的"一条顶三条"（Ch5）

```sql
MERGE INTO tgt s USING src o ON s.k = o.k
WHEN MATCHED AND (s.v IS DISTINCT FROM o.v) THEN UPDATE SET v = o.v
WHEN NOT MATCHED THEN INSERT (k, v) VALUES (o.k, o.v)
WHEN NOT MATCHED BY SOURCE THEN DELETE;   -- PG15 即有；输出可用 RETURNING（PG18 起 RETURNING OLD/NEW）
```

- `IS DISTINCT FROM` 做变更检测防全表 UPDATE——本书 JSON 主题里同样用它比较 `jsonb`。

### 6. psql 变量与可重复脚本（Ch7）

文档转述 ⚠️：

```sql
\set tbl sales_2024
SELECT count(*) FROM :"tbl";
SELECT pg_size_pretty(pg_total_relation_size(:'tbl')) \gset size_
\echo 表大小 :size_pg_size_pretty
\if :{?define_env} \echo 已定义 \else \echo 未定义 \endif
```

- 生产脚本三防：`psql -v ON_ERROR_STOP=1 --single-transaction`、变量一律 `:'x'` 引用插值防注入、
  `\gset` 把查询结果拉进 shell/后续语句做条件分支。
- "可重复执行"（幂等）套路：`CREATE TABLE IF NOT EXISTS`、`INSERT ... ON CONFLICT DO NOTHING`、
  `CREATE OR REPLACE FUNCTION`、对象存在性判断写进 `\gset` 分支。

## 常见坑与判读

| 症状 | 根因 | 处置 |
| --- | --- | --- |
| `COPY` 报权限错 | 把客户端路径给了服务器 | 改 `\copy` 或放服务器可读目录 |
| 分区查询全分区扫 | 谓词含函数包裹分区键 | 谓词写成范围常量，验证 `Explain` 里 pruning |
| MERGE 报 cannot affect row a second time | ON 条件一对多 | 源侧先聚合去重再 MERGE |
| psql 脚本失败却"看起来成功" | 未设 ON_ERROR_STOP | 加 `-v ON_ERROR_STOP=1`，CI 里判非零退出码 |

## 与其他章 / 其他笔记的联系

- 索引选择与代价：分区裁剪、MERGE 的执行计划在 [05-性能与并发.md](05-性能与并发.md) 展开；优化器源码级原理见
  [../PostgreSQL技术内幕_查询优化深度探索.md](../PostgreSQL技术内幕_查询优化深度探索.md)。
- `jsonb` 的存储与 TOAST：[../PostgreSQL数据库内核分析.md](../PostgreSQL数据库内核分析.md)。
- 查询执行引擎中 COPY/INSERT 路径：[../PostgreSQL查询引擎源码技术探析.md](../PostgreSQL查询引擎源码技术探析.md)。
- 与 MySQL 装载/唯一冲突语义对照：`../mysql/00-总览与阅读地图.md`（`ON DUPLICATE KEY` vs `ON CONFLICT`/`MERGE`）。
- 备份视角：大表装载后立刻影响 [06-备份与恢复.md](06-备份与恢复.md) 的 WAL 量与归档压力。

## 核心概念速览（中英对照）

- **ctid** — 物理行指针（块号+行偏移）：去重的临时抓手，非稳定标识。
- **恒等列** — identity column：`GENERATED ... AS IDENTITY`，标准 SQL 自增，优于 serial。
- **JSONB** — binary JSON：可索引（GIN）、可 IS DISTINCT FROM 比较的 JSON 存储形态。
- **声明式分区** — declarative partitioning：RANGE/LIST/HASH 三种，父表只是路由壳。
- **分区裁剪** — partition pruning：靠谓词可证范围，函数包裹即失效。
- **MERGE** — SQL:2003 复合语句：PG15 引入，MATCHED/NOT MATCHED 分支。
- **COPY vs \copy** — 服务器侧装载与 psql 客户端代理装载：权限与路径语义完全不同。
- **FROM PROGRAM** — 管道装载：COPY 直接消费外部命令 stdout。
- **gset** — psql 元命令：查询结果转变量，脚本条件化的核心。
- **ON_ERROR_STOP** — psql 严格模式：出错即非零退出，自动化脚本必开。
- **setseed** — 随机种子：可复现合成数据的前提。
- **generate_series** — 集合生成函数：造数与日历/序列表的万能发生器。

## 最新演进与工业实践

- **PG16（✅ 发行说明）**：初始表同步二进制拷贝、逻辑订阅大事务并行应用、更多场景的增量排序（含 DISTINCT）；
  发布页 https://www.postgresql.org/docs/release/16.0/ 。
- **PG17（✅）**：`JSON_TABLE()` 把 JSON 直接表值化（替代手写 jsonb_to_recordset）；SQL/JSON 查询族补全；
  VACUUM 内存体系重做。
- **PG18（✅）**：虚拟生成列成为 GENERATED 列默认语义（读时计算、不占存储）；`MERGE ... RETURNING` 支持
  `OLD/NEW` 引用；时间约束（temporal constraints，主键/唯一/外键作用于范围不重叠）。
- **分区表工业现状**：PG 原生分区已能承担按时间滚动的主线场景，但"全局索引缺位 + 在线换分区"仍常借
  pg_partman（https://github.com/pgpartman/pg_partman ，✅ 已验证可达）做自动滚动创建/保留。
- **装载工程**：大规模装载普遍直接走并行 `COPY FROM PROGRAM` + 对象存储管道；索引后置与
  `maintenance_work_mem` 调优仍是 PG16–18 不变的组合拳。
- **MERGE vs ON CONFLICT**：2024–2026 社区讨论（Pg.conf 演讲与邮件列表，⚠️ 未逐篇核验 DOI/链接）倾向于：
  简单 upsert 用 `INSERT ... ON CONFLICT`，批量差分同步用 `MERGE`——与本书食谱口径一致。
