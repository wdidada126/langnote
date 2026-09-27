# 11 · 容器与可插拔数据库 CDB/PDB（原书 Ch.12, pp.347-377）

> 章题 ✅ Crossref 实抓（DOI 10.1007/979-8-8688-1038-1_12, "Containers and Pluggables"）。章内小节自拟 ⚠️。Oracle 行为一律 ⚠️ 转述；取证：Concepts 多租户节 ✅ https://docs.oracle.com/en/database/oracle/oracle-database/23/cncpt/index.html 、Administration ✅ …/23/admin/index.html （Multitenant 专册指南码在 /26/ 重排后不可稳定命中，口径见 [00-总览与阅读地图.md](00-总览与阅读地图.md) §2.4）。含 🔧 类比 1 组（非本书引擎行为）。

## 11.1 一图流：CDB 解剖

```
实例(1×SGA+后台进程群)
 └─ CDB(root: CDB$ROOT)  ← 共享代码/字典公共层
     ├─ PDB$SEED           ← 新 PDB 的复制模板(只读)
     ├─ PDB1 (业务/租户)    ← 本地用户/本地对象/可独立开关
     └─ PDB2 ...
 每容器: CON_ID 标识; 字典分公共层(root 存"类")与本地层(PDB 存"实例")
```

- 动机账本（⚠️ 官方叙事转述）：整合密度（一实例养 N 库）、运维批量性（补丁一次修代码层）、资源治理（limit 族参数按 PDB 配额）；代价：故障域放大（root 病全家病）与"共享 UNDO/重做 vs 本地 UNDO"的策略选择 ⚠️。
- **非 CDB 的终局**：12c 双轨→19c 劝退→23ai 事实上多租户单轨（非 CDB 不再演进 ⚠️，迁移章 15 的存在理由）。

## 11.2 生命周期操作集（本章的主语是动词 ⚠️）

| 动作 | 命令族 | 运维注脚 |
|---|---|---|
| 建 | `create pluggable database pdb1 admin user pdb1_admin ... file_name_convert ...` | 从 SEED 秒级；模板可命名保存 |
| 开/关 | `alter pluggable database all open` + **save state** | 实例重启后 PDB 不自开是新手墙，save state 解 |
| 克隆 | `create pluggable database clone from pdb1`（本地）/ from 远端 link（网络克隆）| 热克隆依赖本地 UNDO 或临时离线 ⚠️ |
| 拔/插 | `unplug`（生成 XML 描述文件）→ `plug` 入目标 CDB | 版本/字符集/补丁兼容检查先行；no-pdb-lock 语义 ⚠️ |
| 迁 | `alter pluggable database ... move`（relocate，文件可后台搬）| 停机窗口逐缩 ⚠️ |
| 删 | `drop pluggable database including datafiles` | 留档可 `keep` 成插回模板 ⚠️ |
| 刷新 | `flush` 命名 PDB 的代码/字典公共层 | 打补丁后的收敛动作（→16）⚠️ |

## 11.3 容器内政：用户、字典、资源

- 公共用户 `c##`（全容器通行，05 章）vs 本地用户（PDB 内政）；`common_user_prefix` 在建库时定死 ⚠️；
- 对象两态：**元数据链接（metadata-linked）**——PDB 里只见定义、数据在 root（字典对象一族）vs **数据链接（data-linked）**——定义共享、数据本地（部分组件）⚠️：`dba_objects.sharing` 列是分诊位（→09 章视野）；
- 资源治理：`dbms_resource_manager` 消费者组扩到 PDB 级 + **limit API**（`alter pluggable database ... cpu_count/storage/iops` 型配额族 ⚠️ 名称以文档为准）；23ai 对单 PDB 的可用规格持续放宽 ⚠️（Free 版即"1 CDB 限额"的官方示范）；
- 本地 UNDO（`undo_tablespace` 按 PDB）与共享 UNDO 二选一在建库定 ⚠️：闪回/PITR 按 PDB 粒度时前者是前提（12 章恢复联动）。

**🔧 类比（非本书引擎行为）——ATTACH：迷你"容器合一体"**：SQLite 的 `ATTACH` 把多个独立库文件挂进同一连接、可跨库联查——CDB"一实例多自治容器"的最小标本。本机 sqlite 3.45.3 实跑（三文件：cdb/pdb1/pdb2）：

```
$ python - <<'EOF'
import sqlite3
c  = sqlite3.connect('cdb.db');  c.execute('create table common(id int)')
p1 = sqlite3.connect('pdb1.db'); p1.execute('create table emp(name text)')
p1.executemany('insert into emp values(?)', [('amy',),('bo',),('cy',)]); p1.commit()
p2 = sqlite3.connect('pdb2.db'); p2.execute('create table dept(dname text)')
p2.execute("insert into dept values('fin')"); p2.commit()
c.execute("attach 'pdb1.db' as pdb1"); c.execute("attach 'pdb2.db' as pdb2")
print(c.execute('select (select count(*) from pdb1.emp),'
                '(select count(*) from pdb2.dept)').fetchone())
EOF
(3, 1)
```

对照点：一连接（=实例）多 schema 前缀库（=PDB）、跨容器查询即"root 视角看租户对象"。**差异（更重要）**：SQLite 无共享代码层/无 CDB$ROOT 字典公共层/无 save state/无热克隆与资源配额——ATTACH 只类比"挂载与命名空间"一层，11.2/11.3 的动词表在 SQLite 全部缺位，这正是 Oracle 多租户的工程管理含量所在。演示于 tmp/dbwave_w4_ora23，非本书引擎行为。

## 11.4 应用容器（Application Container）一笔

- 概念：PDB 的 PDB——`application root`（模板定义共享）+ N 个 `application PDB`（每 SaaS 租户一格）+ 同步钩子（seed/版本升级时跑的 PL/SQL 挂点）⚠️；
- 定位账：多租户 SaaS 的"schema-per-tenant"升级方案，管理面=一次改动 N 租户生效 ⚠️；本册仅登记，深读官方 Multitenant 指南 ⚠️。

## 11.5 值班视角的容器问题分诊（⚠️ 综合）

1. 连不上"PDB 里的库"：listener 动态注册带服务名 vs 手工服务；`alter pluggable database ... save state`；服务是否 `open` 时自起 ⚠️；
2. 锁在 root 解在 PDB：锁用户要按容器执行（`cdb_users` 查 CON_ID，09 章视野）⚠️；
3. 告警按 PDB 归属：`v$diag` 系消息带容器 ID，容量/会话告警按容器分账——传统单库监控模板直接套会失真 ⚠️；
4. 克隆/搬迁后 SID/服务/EM 仓库三方对账（15 章 Fleet 的注册表问题前身）。

## 11.6 容器命令速查（⚠️ 示意，参数以文档为准）

```sql
show pdbs                                   -- 全景: CON_ID/开放模式/受限状态
alter session set container = pdb1;         -- 换帽: DBA 的日常方位切换
create pluggable database pdb2 admin user pdb2_admin identified by "***"
  file_name_convert=('/u01/oradata/cdb1/pdb1','/u01/oradata/cdb1/pdb2');
alter pluggable database pdb2 open;
alter pluggable database pdb2 save state;   -- 重启后仍开(11.5 案一)
create pluggable database pdb3 from pdb2    -- 热克隆(依赖本地 UNDO 形态, 11.3)
  file_name_convert=('/u01/oradata/cdb1/pdb2','/u01/oradata/cdb1/pdb3');
alter pluggable database pdb3 close immediate;   -- 维护/搬迁前置态
-- 拔插对(15 章迁移路线之一的容器侧半):
alter pluggable database pdb3 unplug into '/tmp/pdb3.xml';
drop pluggable database pdb3 keep datafiles;     -- 保留文件待插
create pluggable database pdb3 using '/tmp/pdb3.xml' nocopy;
```

动作记忆轴：**开/关看服务、克隆看 UNDO、拔插看兼容、锁限看 profile**——四问覆盖值班容器工单大半 ⚠️。

## 11.7 容器化验收清单（建/迁后 30 分钟）

1. `show pdbs` 状态与 `cdb_pdb` 的 OPEN_MODE/RESTRICTED 对齐预期；
2. 每 PDB 的本地 UNDO/TEMP 存在且属性正确（11.3）；
3. 服务注册：`lsnrctl services` 出现各 PDB 应用服务，save state 生效验证（重启演练一次）；
4. 公共用户前缀策略落实（c## 只留管理位，业务用户全本地化，05 章）；
5. 资源配额基线：limit 族/资源程序挂到消费者组（11.3，对应 03 章配额观）；
6. 备份纳管：RMAN 对全部 PDB 的可见性与保留政策（12 章），逐 PDB 恢复演练排队 ⚠️。

## 自测（能默写=过关）

- root/SEED/PDB 三角与元数据链接/数据链接两对象态。
- 拔插的兼容检查清单（版本/字符集/补丁/选项）与 XML 描述件的角色。
- PDB 不自开之谜的两件套答案；本地 UNDO 决定哪些能力。

## 核心概念速览（中英对照）

- **CDB** — container database：一个实例承载多容器的总体。
- **PDB** — pluggable database：可插拔的自治租户单元。
- **CDB$ROOT** — root container：公共代码与字典公共层宿主。
- **PDB$SEED** — seed：新 PDB 的只读模板源。
- **容器 ID** — CON_ID：视图与资源归属的容器坐标。
- **公共用户** — common user：c## 前缀、通行全容器。
- **元数据链接对象** — metadata-linked：定义共享、实例在 root 的对象。
- **数据链接对象** — data-linked：定义共享、数据本地的对象。
- **拔插** — unplug/plug：以 XML 描述件迁 PDB 的原子搬家术。
- ** relocate** — move：PDB 在线迁移、文件后台搬运。
- **save state** — 持久启停态：实例重启后 PDB 自动开/关的登记。
- **limit API** — PDB 配额族：CPU/存储/IO 按容器封顶。
- **应用容器** — application container：模板+租户 PDB 群+同步钩子的 SaaS 结构。

## 最新演进与工业实践

- **多租户从"选项"到"默认现实"**：23ai 的新库、Free、补丁叙事全部 CDB 化 ⚠️（02 章联动）；工业存量（未迁移非 CDB）由 15 章专治——本章是"已迁后"的日常。
- **SaaS 隔离的粒度竞争**：schema-per-tenant（旧）、PDB-per-tenant（Oracle 答案）、行级 RLS（PG/MySQL 路线）三方案的成本-隔离-密度三角是 2024+ 架构评审常设议题 ⚠️；盘上对照：../Database_Administration_2e/00-总览与阅读地图.md（引擎无关的整合动机章）、../PostgreSQL_16_Administration_Cookbook/00-总览与阅读地图.md（schema/库隔离谱系）。
- **自治与容器**：ATP 本身即"托管多租户的 PDB 化交付"（✅ adbsb 文档线），用户视角 PDB 被抽象为"一个实例"——本章知识在云岗位转化为"理解配额与快照的单位" ⚠️ 转述。
- **容器与 AI 工作负载**：单 PDB 承载 RAG 应用（向量+JSON+关系三合一，06/07/08/10 章在租户边界内合龙）是厂商 2024+ 主推场景 ✅（族主页新特性线），隔离与配额（11.3 limit 族）因此进入 AI 基建清单 ⚠️ 趋势句。
- **中文史前语境**：12c 时代 CDB/PDB 的中文操作叙述（含当年"非 CDB 仍主流"口径差）在 ../Oracle12c数据库应用与开发/01-Oracle12c体系结构与CDB-PDB.md，谱系对位声明见 [00-总览与阅读地图.md](00-总览与阅读地图.md) §四——读它时时刻记得 23ai 已无退轨。
