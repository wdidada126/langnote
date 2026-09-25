# 01 · Oracle 12c 体系结构与 CDB / PDB

> **本章地图**：**CDB 的三种容器**（CDB$ROOT / CDB$SEED / PDB$SEED）→ **PDB 的四种形态**（普通 / 模板 / 回放 / 元 PDB）→ **`C##` 公共用户 vs 本地用户** → **连接与容器切换**（`ALTER SESSION SET CONTAINER`、`service_name`、监听里的服务名）→ **数据导入为什么必须先在 CDB 里建 `C##` 公共用户** → **12c 的内存/进程模型相对 11g 的变化** → **与 `数据库系统概念6` 的对照**。

## 一、核心精讲

> 以下 SQL/DDL 均为**教学示意，不参与构建**，不可也不必在真实实例上执行。

### 1.1 逻辑结构：CDB 里套 PDB

12c 把"数据库"这个词拆成了两层：

- **CDB（Container Database，容器数据库）**：真正持有 control file、redo thread、UNDO 表空间的那一层。它是个"仓库容器"。
- **PDB（Pluggable Database，可插拔数据库）**：挂在 CDB 下面的"租户"，每个 PDB 有自己的 SYSTEM/SYSAUX、自己的 undo、自己的 temp、自己的字典。

> 12c 官方文档把 CDB 的容器分为三类：`CDB$ROOT`（根容器，存公共对象）、`CDB$SEED`（种子库，PDB 的模板，只能只读）、以及用户自己创建的 PDB（`PDB$SEED` 则是非 CDB 库升上来后的兼容容器）。原笔记第 1 章批注里留的那条 `SELECT con_id, dbid, name, open_mode FROM v$pdbs;` 就是查这张视图的。

一个典型的 CDB 拓扑（教学示意，不参与构建）：

```
CDB$ROOT  (con_id = 1)   ← 公共用户 C##* / 公共对象 / 公共表空间
 ├── PDB$SEED (con_id = 2)   ← 种子，只读
 ├── PDBORCL  (con_id = 3)   ← 业务 PDB
 └── PDBSHOP  (con_id = 4)   ← 另一个业务 PDB
```

### 1.2 `C##` 前缀：公共用户的强制约定

这是原笔记第三条批注「`C##` 开头」的确切含义：

- 在 CDB 模式下，`CREATE USER` 建的用户**默认必须是 `C##` 开头**（`COMMON USER PREFIX`），否则报错 `ORA-65049: the common user name is not a common user name`；
- 反过来，`C##` 开头且在 CDB$ROOT 下创建的对象叫 **COMMON object**，它的存在范围是"整个 CDB"——所有 PDB 都能看到；
- 普通 PDB 内部建的、不带 `C##` 的用户叫 **LOCAL user**，只属于本 PDB；
- **common user name 有长度上限**（历史上是 25 字节，12.2 起放宽）；具体字节数随版本变化，以当前版本官方文档为准——但"名字被截断/超长"是老 DBA 常撞的一个坑。
- **PDB 的四种形态**（官方分类）：**普通 PDB（ordinary）**、**模板 PDB（template）**、**反射 PDB（reflection，12c 起用于 CDB 内的对象共享）**、**元数据 PDB（metadata）**。本目录重点只有"普通"这一种。

教学示意，不参与构建：

```sql
-- 在 CDB$ROOT 下创建公共用户（C## 前缀是强制的）
CREATE USER c##myshop IDENTIFIED BY "Str0ng#Pass" DEFAULT TABLESPACE users TEMPORARY TABLESPACE temp;
GRANT CONNECT, RESOURCE TO c##myshop;
CONTAINER = ALL;                 -- 12c 语法：对象对 CDB 内所有容器可见

-- 切换到某个 PDB 后，再建本地用户（不需要 C## 前缀）
ALTER SESSION SET CONTAINER = PDBSHOP;
CREATE TABLE shop_login (id NUMBER PRIMARY KEY, user_name VARCHAR2(64), login_at DATE);
-- 注：此时 DEFAULT tablespace 若指向 CDB 级对象，需先 SET DEFAULT TABLESPACE
```

### 1.3 「重点看第 7 章」的前置条件：数据是怎么进去的

原笔记留下的 4 条 `sqlldr` 命令行，把 CDB/PDB 这件事的**实操含义**暴露得很清楚：

```bash
sqlldr MYSHOP/5Edidada@192.168.1.158:1521/TEST control=C:\Users\edidada\Desktop\data\input_login.ctl \
       log=C:\Users\edidada\Desktop\data\input_test.log bad=C:\Users\edidada\Desktop\data\input_test.bad
sqlldr MYSHOP/5Edidada@192.168.1.158:1521/TEST control=...\input_course.ctl ...
sqlldr MYSHOP/5Edidada@192.168.1.158:1521/TEST control=...\input_student.ctl ...
sqlldr MYSHOP/5Edidada@192.168.1.158:1521/TEST control=...\input_sc.ctl ...
```

从中能读出的三条信息：

1. **连接串里的 `TEST` 是 service name/ SID，而不是 PDB 名**——12c 里监听暴露的服务既可以是 CDB 级，也可以是每个 PDB 一个服务名。原笔记连的是 `TEST`，说明该环境把这个服务直接映射到了某个 PDB 或 CDB。
2. **`MYSHOP` 是普通用户**，不在 `C##` 前缀之列。这说明样例库是"非 CDB 兼容模式"下建的，或者用户建在 PDB 内部（LOCAL 用户）——这是一个很典型的"用 12c 但按 11g 习惯做事"的中间态，也是后面导入数据能跑通的原因。
3. **导入的表有 4 张**：`login`、`course`、`student`、`sc`（选课表，典型的学籍管理库，正好和教材第 6 章"数据表"、第 7 章"数据查询"用的例子库一致）。
4. 笔记里另一条 Linux 下的 `sqlldr`，带 `direct = y`，作者自己加了批注「**这块需要特别注意，根据实际业务场景使用，不要随便使用**」——这是**直接路径加载（direct path load）**的开关，绕开 buffer cache 直接写数据文件，速度快但会**在高水位线以上追加**、不产生 redo（可归档模式下仍产生少量）、且**期间表不可用**。这条提醒非常关键，值得单列。

### 1.4 「一个项目 = 一个用户 = 一个 schema」

原笔记批注原文：

> 是 user，同一个数据库，不同的 IT 项目访问，一个项目对应一个用户
> 表在 scheme 下面
> user 和 scheme 同名

这是在记 **Oracle 的 schema 语义**：

- `USER` 和 `SCHEMA` 在 Oracle 里**是同一个东西**，schema 的名等同于该用户；
- 所以"一个项目对应一个用户"≈"一个项目对应一个 schema"，项目的表都落在自己的 schema 下，天然做了数据隔离；
- 这让 CDB/PDB 的价值被削弱了（因为多用户已经能隔离）——所以 12c 推 CDB 的真实卖点是**资源隔离 + 生命周期管理（克隆/插拔）**，而不是多租户隔离本身。

### 1.5 12c 相对 11g 的进程/内存模型变化（与 `02` 章的接口）

为了让"体系结构"这一章不至于和 `02` 章重复，这里只列**和 CDB/PDB 相关**的：

| 主题 | 11g | 12c 起 |
| --- | --- | --- |
| 实例与库 | 一实例对一库 | 一个 CDB 实例可以带 N 个 PDB，实例仍是 N×1 的实例（不是每 PDB 一个实例） |
| 后台进程 | 标准 5 类 | 新增 ADR、TMON、TT00（临时表空间额度）、以及 `VKRM`（12c 起） |
| SGA 组件 | shared pool / buffer cache / large pool / java pool / streams pool | 增加 **In-Memory Area**（12.1.2 起），以及 `DB_FLASHBACK` 相关 |
| 内存自动管理 | `sga_target` / `pga_aggregate_target` | 12c 起 `memory_target` 更常用，并引入 **In-Memory** 与 **heap SGA** |
| 参数 | 大量静态参数 | 12c 起大量参数可 `ALTER SYSTEM SET ... SCOPE=BOTH` 在线改；**但每个 PDB 也可以有自己的参数（12.2 起）** |

### 1.6 与「数据库系统概念」的对照（重要）

[`数据库系统概念6/17-数据库系统体系结构.md`](../数据库系统概念6/17-数据库系统体系结构.md) 把系统分成"集中式 / 客户-服务器 / 并行 / 分布式"四类。CDB/PDB **不属于其中任何一类**——它是**单实例、单共享缓存**内的**字典与对象隔离**机制：

- PDB 之间**共享 SGA、共享 Buffer Cache、共享 redo、共享 Data Guard、共享同一套 latch 与行锁**；
- PDB 之间是**逻辑隔离**（各自的字典表 `USER_*` / `ALL_*` / `DBA_*` 在各自容器内可见），**没有跨 PDB 的分布式事务**；
- 因此"多租户"在 Oracle 12c 里更接近**命名空间/容器化（namespace/container）**，而不是 Docker 那种进程级隔离。真正的资源隔离要靠 **PDB 级别的 CPU/内存限额（12.2 起 `PDB MEMORY LIMIT`、`_CPU_PER_CPU`（即 CPU 配额））**。

### 1.7 查看与管理容器（教学示意，不参与构建）

```sql
-- 1) 看当前有哪些 PDB、状态如何（原笔记第 1 章批注留的正是这条）
SELECT con_id, dbid, name, open_mode FROM v$pdbs ORDER BY con_id;

-- 2) 看当前会话落在哪个容器
SELECT sys_context('userenv','con_name')  AS 当前容器,
       sys_context('userenv','session_user') AS 会话用户
FROM dual;

-- 3) 切换容器（只在 SESSION 级生效，不影响别人）
ALTER SESSION SET CONTAINER = PDBSHOP;

-- 4) 用 PDB 自己的服务名连接（而不是连 CDB 级服务）
--    客户端： sqlplus user/pwd@//host:1521/pdbshop.service.example.com

-- 5) 打开/关闭一个 PDB（需以 SYS 在 CDB 根上执行）
ALTER PLUGGABLE DATABASE PDBSHOP OPEN READ WRITE;
ALTER PLUGGABLE DATABASE ALL CLOSE IMMEDIATE;   -- 12c 起支持 ALL

-- 6) 查看容器级参数（12.2 起 PDB 可以有自己的参数）
SELECT name, value, isdefault FROM v$system_parameter
WHERE con_id = (SELECT con_id FROM v$pdbs WHERE name = 'PDBSHOP');
```

> 上面 6 条里，**第 3 条最常被误用**：`ALTER SESSION SET CONTAINER` 只改变"我看到哪个容器的字典"，**不改变**你的会话已经打开的游标、已绑定的变量、以及已经开始的事务所在容器。跨容器切换后再提交，提交的仍是**原容器**里的事务。这是 12c 上最隐蔽的一类 bug。

### 1.8 12c 安装时埋下的三个决定性选择

这一节是给"要从 11g/12c 起步的人"的提醒。安装界面上看起来只是几个勾选，实际决定了后面 5 年的运维形态：

| 安装时的选择 | 后果 |
| --- | --- |
| **是否建 CDB** | 一旦选了 CDB，后续想"退回到非 CDB"必须 `UNPLUG` + 重建；反之一个非 CDB 的库想变成 CDB，需要跑 `noncdb_to_pdb.sql` 做校验和转换 |
| **字符集**（AL32UTF8 / ZHS16GBK 等） | 字符集一旦定下几乎不可逆。`sqlldr` 导入时报乱码，第一嫌疑就是控制文件里的 `CHARACTERSET` 参数与库的字符集不一致（原笔记里 Linux 那条 `sqlldr` 就有 `NLS_LANG` 的老问题） |
| **块大小（db_block_size，默认 8K）与 `MAX_STRING_SIZE`** | 12.1 起默认是 `STANDARD`（VARCHAR2 最多 4000 字节）；想要 `VARCHAR2(32767)` 必须建库时设 `MAX_STRING_SIZE=EXTENDED`，**之后不能再改**（见 `14` 的版本坑） |

## 二、版本演进

| 版本 | 与本章主题相关的变化 |
| --- | --- |
| 11g | 无 CDB/PDB。RAC 的 ASM 与 Clusterware 已是主体（见 `11`）。 |
| 12.1.0.1（2013） | CDB/PDB 首次登场；`C##` 公共用户前缀强制；`v$pdbs`、`v$containers` 视图出现。 |
| 12.1.0.2 | In-Memory Column Store 引入；`MAX_STRING_SIZE=EXTENDED` 可用（见 `14` 章的版本坑）。 |
| 12.2（2016） | **PDB 插件化运维**：`CREATE PLUGGABLE DATABASE ... FROM` 支持更多源；PDB 可设置自己的初始化参数；common user name 长度放宽。 |
| 18c | 持续可用性与多租户运维强化；PDB 克隆更快。 |
| 19c | 长期支持（LTS）版本；PDB 的**持续可用 PDB（Always-On PDB）**、`CDB` 打包/搬迁工具；**持续 PRC（贯穿式更新）**落地（见 `14`）。 |
| 21c | 实验性功能较多：自动索引（Auto Index）在 21c 正式登场；JSON Relational Duality 预研。 |
| 23c | **JSON Relational Duality** GA、**向量搜索与 AI 向量**、**自动索引** GA、**Database with Agent / AI 能力**；多租户与 JSON 深度整合（见 `14`）。 |

🔧 **2026 年必须补的三条**：
1. **PDB 克隆与插拔已经是常规运维**：`ALTER PLUGGABLE DATABASE ... OPEN READ WRITE`、`UNPLUG INTO`、`CREATE PLUGGABLE DATABASE ... FILE_NAME_CONVERT=(...)` 这类命令在生产里天天用，而 12c 教材只当"第 2 章的一个练习"。
2. **`DBMS_PDB`、`CDB$ROOT` 的公共对象管理**：`CREATE OR REPLACE` 公共同义词、公共角色的统一管理，以及**升级时"先升级 CDB$ROOT 再逐个升级 PDB"**的运维节奏。
3. **12101 之后的兼容性变化**：12.2 起 `optimizer_mode` 默认、`result_cache` 默认、`utf8` 与 `MAX_STRING_SIZE` 默认值均有漂移，跨版本迁移时是高频故障源（见 `14`）。

## 三、经典论文与原始文献

| 文献 | 出处 | 与本主题的关系 |
| --- | --- | --- |
| Jim Gray《The Transaction Concept: Virtues and Limitations》 | VLDB 1981 | 事务概念的奠基文献。CDB 里的 `COMMIT`/`ROLLBACK` 仍是会话级事务语义 |
| Theo Haerder & Andreas Reuter《Principles of Transaction-Oriented Database Recovery》 | ACM Computing Surveys 15(4), 1983 | **通用理论，非 Oracle 专属**：ARIES 之前恢复算法的综述；redo/undo、检查点、STEAL/NO-STEAL 的分类框架 |
| Devinder Mohan 等《ARIES: A Serializability-Preserving Recovery Algorithm With Repeating History》 | SIGMOD 1992 | **通用理论，非 Oracle 专属**：Oracle 的恢复实现与 ARIES 思路同源（重复历史 + 回滚到日志末尾）但不完全相同 |
| Michael Stonebraker《Object-Relational DBMSs: The Next Generation》 | IEEE Computer 1996 | 关于"扩展关系模型"的经典讨论，是 Oracle 对象关系特性（本章 1.5 提到的 "Oracle 数据库中的对象" 一节）的思想源头之一 |
| Oracle《Oracle Database Administrator's Guide, Release 12.1》"Managed Object Dependencies / Pluggable Databases" | Oracle 官方文档（非论文） | CDB/PDB 的**权威定义**来源，本章 1.1/1.2 的说法以此为准 |
| 《Oracle Database 12.1: New Features》白皮书 | Oracle 官方发布材料（非论文） | 12c "c = cloud" 的多租户叙事来源 |

> **诚实标注**：CDB/PDB 是**产品特性而非学术成果**，没有与之对应的顶级会议论文。Oracle 官方的 *Oracle Database Administrator's Guide*（12.1/12.2）与 *Oracle Database Concepts* 才是这里的一手文献。上表其余条目是**恢复与事务的通用理论**，用来给这章提供底座，明确**不是 Oracle 专属论文**。

## 四、近年研究与工业界开源实践（2015–2026）

- **近年研究**：多租户资源隔离在国际学术界更多出现在**容器化/虚拟化上下文**（Kubernetes cgroup、NRG、RTG 等资源治理研究），而不是数据库多租户。Oracle 自己的学术产出集中在 **In-Memory、向量检索、JSON Relational Duality** 上（见 `14`）。
- **工业界趋势**：
  - **PDB 作为"数据库即服务"的交付单位**：云上（OCI Autonomic Database、AWS RDS 的 CDB 兼容层、Azure）普遍把 PDB 当作打包、克隆、迁移的原子单元；
  - **12c 老库正在变成"PDB 存量"**：大量 2013–2018 年的 12.1 库仍在跑，19c/23c 升级的主要问题不是技术而是**停机窗口**——PDB 的 `UNPLUG INTO` + `DBMS_PDB` 校验（`@$ORACLE_HOME/rdbms/admin/noncdb_to_pdb.sql`）是这条路上最常用的两步；
  - 🔧 **Python 生态迁移**：原笔记时代的 `cx_Oracle` 已被 `oracle/python-oracledb` 取代（**star 实测 453**，2026-09-25）。多租户环境下，连接器需要显式指定 service/连接类型（`connect_type="pdb"`、`service_name=...`），否则会静默连到 CDB$ROOT——这是迁移动的高频事故。
- **本主题可直接对照的开源仓库**（star 为 2026-09-25 `gh api` 实测）：

  | 仓库 | star |
  | --- | --- |
  | `oracle/python-oracledb` | 453 |
  | `oracle/node-oracledb` | 2368 |

## 五、常见误区与本书需修正之处

| # | 误区 | 修正 | 书目 |
| --- | --- | --- | --- |
| 1 | "CDB 是 12c 才有的新东西，所以 11g 不需要了解" | 大量生产库停在 11.2.0.4 / 12.1，且 19c/23c 也支持非 CDB 库；非 CDB 库要升上来需要跑 `noncdb_to_pdb.sql` | 全部 9 本均未覆盖（12c 教材只在第 2 章提创建） |
| 2 | "PDB 之间是完全隔离的，一个 PDB 挂了不影响另一个" | PDB **共享 SGA、共享 redo、共享控制文件**；任一 PDB 的**强制启动/关闭、redo 丢失、ADR 故障**都可能拖垮整个 CDB | 12c 教材（第 2 章"操作"） |
| 3 | "`C##` 只是命名规范" | 它是**强制约束**（`COMMON USER PREFIX`），违反直接 `ORA-65049`；且公共对象的变更会影响**所有** PDB | 12c 教材未正面强调前缀的强制性 |
| 4 | "多租户就一定能做资源隔离" | 12.1 的 PDB **几乎无资源限额**；真正的 CPU/内存配额要到 12.2 的 `_CPU_PER_CPU` 与 PDB memory limit 才完善 | 全部 9 本均未覆盖 |
| 5 | 🔧 "PDB 只能创建，不能克隆/插拔/搬迁" | 12.2 起克隆、插拔、`-relocate` 已是常规运维；19c 更有持续可用 PDB（Always-On PDB） | 🔧 全部 9 本（成书 2009–2021）均未覆盖 12.2 之后的运维形态 |
| 6 | 🔧 "12c 教材讲的多租户就是 CDB/PDB 这两个词" | 2026 年的多租户还包含 **PDB 打包（CDB 级备份/升级单元）、PDB 资源限额、PDB 快照克隆给开发/测试用（"clone to dev"）、PDB relocate 做零停机搬迁** | 🔧 12c 教材（第 2 章） |
| 7 | 🔧 "direct path load（`direct = y`）随时可以用，快就行" | 原笔记作者自己已标注"不要随便使用"：direct path 会**在 HWM 以上追加**、**期间表不可用**、**触发 Space Traveling / 表锁定**，且对有依赖的索引会造成运行期争用 | 原笔记批注；12c 教材的 `sqlldr` 示例未提风险 |
| 8 | "PDB 名就是连接串里的服务名" | PDB 名 ≠ 服务名。服务名在监听里配置（`listener.ora`），PDB 通过服务对外暴露；连错服务会静默落到 CDB$ROOT | 12c 教材（第 3 章"服务与 SQLPlus"）未点破 |

## 六、与其他章 / 其他书的联系

- **前序**：[`00-总览与阅读地图.md`](00-总览与阅读地图.md) 的「重点看第 7 章」条目的解读在这里落地。
- **下一章 **[`02-实例内存与后台进程.md`](02-实例内存与后台进程.md)****：本章 1.5 表列的"12c 相对 11g 的变化"是接口，第二章展开 SGA/PGA 与 DBWn/LGWR/CKPT/SMON/PMON/ARCn。
- **强相关 **[`11-RAC与高可用.md`](11-RAC与高可用.md)**：ASM 是 12c 里 ASM 已并入 GI 之后的版本，CDB 下的每个 PDB 可以落在共享存储或不同 ASM 磁盘组上。
- **强相关 **[`12-备份恢复容灾与DataGuard.md`](12-备份恢复容灾与DataGuard.md)**：RMAN 备份粒度是 "CDB + 全部 PDB / 单个 PDB / 仅 PDB 的表空间"，这是 CDB 之后最实务的变化。
- **理论对照**：[`数据库系统概念6/17-数据库系统体系结构.md`](../数据库系统概念6/17-数据库系统体系结构.md)（集中式/并行/分布式的分类框架 vs CDB 的"容器"定位）；[`数据库系统概念6/26-高级事务处理.md`](../数据库系统概念6/26-高级事务处理.md)（跨 PDB 的 XA 与本章"没有跨 PDB 事务"的结论）。
- **其他书**：《Oracle RAC核心技术详解》第 1 章（集群技术简介、share-nothing / share-everything 结构）为本章"PDB 共享 SGA"提供集群层面的对照；《Oracle 12c数据库应用与开发》第 1 章的缩写表（ORAC / OASM / ODI / OBDC）与本章呼应。
