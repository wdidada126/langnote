# 章文件 08 · 事务与并发、DBCC 内部机制（原书第 13–14 章）

> 原书位置：Chapter 13 "Transactions and Concurrency" + Chapter 14 "DBCC Internals"（章题 ✅ LoC 内容附注逐字；14 章执笔推测 Paul Randal 谱系 ⚠️）。
> 转述纪律：机制一律 ⚠️ + ✅ Learn 准绳；🔧 为 SQLite integrity_check 类比，非本书引擎行为。

## 本章地图

| 主题块（转述提纲） | 一句话要旨 | 标注 |
| --- | --- | --- |
| ACID 的工程拆账 | 原子/持久靠 03 章日志；隔离靠锁+版本；一致是约束+应用共责 | ⚠️✅(Learn 事务/Locks and threading 模式页 ⚠️URL 未逐验) |
| 锁模式家族 | S/X/U/IS/IX/IXU…意向锁层级=表级与行级的握手协议 | ⚠️✅(Learn 锁定机制 ⚠️URL 未逐验) |
| 锁粒度与升级 | 行→页→表约 5000 锁阈值触发升级(数字为书时代口径 ⚠️)；升级会打断长持有 ⚠️ | ⚠️ |
| 范围锁语义 | REPEATABLE READ/SERIALIZABLE 下 KEY-RANGE 防幻读；与索引选择耦合 | ⚠️ |
| 阻塞与死锁 | 转换等待链→环路即死锁；优先级/牺牲品；trace flag 1204/1222 取证 ⚠️ | ⚠️✅(Learn deadlock graph/Learn) |
| 悲观四隔离 | READ UNCOMMITTED/COMMITTED(默认)/REPEATABLE READ/SERIALIZABLE=锁强度阶梯 | ⚠️✅(Learn 隔离/Learn) |
| 行版本化两兄弟 | SNAPSHOT(事务级一致性视图)与 RCSI(语句级)；版本存 tempdb、14B 行内指针 | ⚠️✅(Learn row-versioning ⚠️URL 未逐验) |
| 版本链的 GC | 最早活跃事务钉住保留线；长事务=版本存储洪水 ⚠️ | ⚠️ |
| DBCC 全景 | CHECKDB/CHECKTABLE=分配一致+记录/索引一致+元数据一致三段流水 | ⚠️✅dbcc(Learn) |
| CHECKDB 修复 | REPAIR_ALLOW_DATA_LOSS=以重建账本方式"对齐"，可能断链丢页——最后手段 ⚠️ | ⚠️ |
| DBCC 工具箱 | PAGE/DBCC INPUTBUFFER/TABLERESULTS 灌表/TRACEON 旗标管理 | ⚠️✅ |
| 损坏响应剧本 | 823/824/825→单页恢复→CHECKDB→还原链(03 章呼应) | ⚠️ |

## 核心精讲（转述 + ⚠️）

### 1. 锁不是互斥，是"模式协商"
意向锁体系让"我要锁一行"先变成"我在表上声明意图"，于是 TABLOCKX 的请求不必遍历千万行——这是两阶段锁在分层对象上的工程化解法 ⚠️。锁升级的真实动机是**锁管理器内存与闩竞争**(书内口径 ⚠️)。对位阅读：InnoDB 只有行锁+意向锁、无升级(靠 gap/next-key 防幻读)——差异对照 [../MySQL技术内幕_InnoDB存储引擎2.md](../MySQL技术内幕_InnoDB存储引擎2.md) 锁章；理论骨架在 [../事务处理概念与技术.md](../事务处理概念与技术.md) 与 [../数据库系统概念6.md](../数据库系统概念6.md) 冲突可串行化章 ⚠️。

### 2. 版本化：用 tempdb 换并发（转述 ⚠️）
RCSI 把"读加 S 锁"换成"读走版本链"：更新者复制旧行入 tempdb 版本存储、行头 14B 指向它(04 章伏笔在此回收)；SNAPSHOT 更进一步给事务一个一致性时间线，代价是更新冲突时放弃写(更新冲突检测)。**保留线=min(最早活跃事务,最早快照)**——一个僵尸事务就能泡沉 tempdb ⚠️。这与 03 章"日志复用边界"同构：**资源回收永远被最慢的读者钉住**。Hekaton(2014 后)干脆把锁换成乐观验证，论文线 [../../db/Hekaton.md](../../db/Hekaton.md) ✅在盘。

### 3. DBCC CHECKDB：全库审计的三段流水
(a) 分配层：把 PFS/GAM/IAM 三账与对象定义对平；(b) 记录层：逐页重放行格式约束、索引键序、行内数据(含 ROW_OVERFLOW/LOB 跨账本对账，04/06 章呼应)；(c) 元数据层：系统表一致性。书中强调 CHECKDB 内部用**快照**跑(不阻塞业务但吃 tempdb/版本存储 ⚠️)；REPAIR 三档是把"发现权"逐步让渡给"改写权" ⚠️。✅ https://learn.microsoft.com/en-us/sql/t-sql/dbcc-transact-sql 。

### 4. 死锁取证与预防工程
1222 输出→受害者选择(代价低者)→应用层重试是标准剧本；书给的设计红线：短事务、对象访问顺序一致、正确索引(减少锁面)、低隔离级别够用就别升级 ⚠️。XEvent system_health 抓死锁图是 2012 起的"零成本黑匣" ⚠️(#36 排障章操作化：[../Pro_SQL_Server_Internals/12-锁类型阻塞与死锁.md](../Pro_SQL_Server_Internals/12-锁类型阻塞与死锁.md) ✅在盘)。

## 🔧 类比实验 E5 · 一条 PRAGMA 里的"CHECKDB 之魂"（SQLite 3.45.3）

**非本书引擎行为，仅通用机制演示**：

```
PRAGMA integrity_check → ('ok',)
PRAGMA quick_check     → ('ok',)
```
实测 ✅。语义对照：integrity_check 遍历全部 B+树页验证"页可用、结构自洽、记录完整"——正是 CHECKDB 记录层的单机迷你版；quick_check 跳过部分交叉验证≈DBCC CHECKTABLE/局部检查的速度换覆盖率 ⚠️ 类比。SQLite 没有"分配账本"(单文件、页即一切)，所以 SQL Server 三段流水里最重的分配一致性层在 E5 里**缺席**——缺席本身就是差异说明：多文件/多对象/多索引的"账本宇宙"才需要 CHECKDB 级审计 ⚠️。

## 本章结论速记

- 隔离级别=锁强度与版本成本的连续统：默认 READ COMMITTED 不是免费午餐。
- 版本存储用 tempdb 买并发，被最慢读者钉死——RCSI 部署要先建长事务治理。
- 锁升级是内存自保不是 bug；设计短事务与索引即可少踩。
- CHECKDB 是"账本三方对平"，修复是"以账改实"的最后手段，还原链才是正规军(03 章)。
- 死锁的解法在建模层(顺序一致)，不在提示层。

## 常见误区（转述 ⚠️）

| 误区 | 事实 |
| --- | --- |
| "RCSI 开了就不阻塞" | 写写仍互斥；且扫描可能读旧版本(语句级≠事务级) ⚠️ |
| "SNAPSHOT 会脏读" | 恰恰相反：它读的是本事务开始时的一致视图 ⚠️ |
| "NOLOCK 提升并发没风险" | 结构页重读可致漏行/重行，报表口径都不稳(07 章呼应) ⚠️ |
| "锁升级是灾难要立刻禁" | 禁升级换来锁管理器内存与闩风暴，先治事务与索引 ⚠️ |
| "CHECKDB 报错就 REPAIR" | 先查 823/824 硬件根因与还原链；REPAIR 是断尾 ⚠️ |
| "备份能代替 CHECKDB" | 备份只拷贝页原样，不发现逻辑腐败(书内警句 ⚠️) |
| "死锁=两个都回滚" | 只有牺牲品回滚；重试逻辑缺失才升级成事故 ⚠️ |

## 与其他章/其他笔记的联系

- 上游：14B 版本指针与 ghost → [04-表存储.md](04-表存储.md)；tempdb 双职能 → [02-数据库与数据库文件.md](02-数据库与数据库文件.md)；日志边界同构 → [03-日志与恢复.md](03-日志与恢复.md)；KEY-RANGE 依赖索引形态 → [05-索引内部结构与管理.md](05-索引内部结构与管理.md)。
- 横向：#36 锁四章群 [../Pro_SQL_Server_Internals/13-乐观并发应用锁与模式锁.md](../Pro_SQL_Server_Internals/13-乐观并发应用锁与模式锁.md)(✅在盘)；理论 [../事务处理概念与技术.md](../事务处理概念与技术.md)、[../../db/ARIES.md](../../db/ARIES.md)(恢复与锁的论文线)；PG 的 MVCC"永不回滚版本到 tempdb 而进表本身"对照 [../PostgreSQL数据库内核分析.md](../PostgreSQL数据库内核分析.md) ⚠️。
- 系列入口：[../数据库系列·总索引.md](../数据库系列·总索引.md)。

## 转述扩写：版本存储治理与 CHECKDB 报告解读（⚠️ 转述）

### tempdb 版本存储的三水位（治理仪表盘）
- 平均/最旧事务时间：保留线的"距离"与"年龄"；
- 未处理的 GC 任务数：清理线程积压=链变长的先行指标；
- 生成速率 vs tempdb 增速：写放大预算——RCSI 上线前必须先回答"最坏情况下 tempdb 要扩几倍" ⚠️。
✅ 视图族 sys.dm_tran_* (Learn DMV 文档族 ⚠️URL 未逐条验)。

### 长事务治理清单（版本链的"钉子户"名单）
1. 应用侧：隐式事务未提交/孤儿连接(02 章登录配置呼应) ⚠️；
2. 运维侧：跑整夜的游标批、漏 COMMIT 的 TVP 包装 ⚠️；
3. 复制侧：分发代理卡住的旧事务 ⚠️；
4. 监控侧：TOP N oldest transaction 定时采集+告警阈值 ⚠️。

### CHECKDB 报告解读要点（⚠️ 转述）
- 错误码谱系：823/824=IO 级(疑硬件/撕裂)，8571=键序错，89xx=分配/元数据类——首件事是查 Windows 事件与驱动/电池写缓存 ⚠️；
- 修复档位选择：REPAIR_REBUILD(结构重造，尽量不丢) vs ALLOW_DATA_LOSS(账本对齐优先)；两档都可能重索引+断链 ⚠️；
- 时间预算：CHECKDB 成本≈全库扫描+树重建，大库拆簇/错峰/快照盘上跑是运维常态 ⚠️；
- "备份完立刻 CHECKDB 备份文件"思路(RESTORE ... WITH CHECKDB)在书时代已成形 ⚠️ 转述。

### DBCC 工具箱小抄
| 命令 | 干什么 | 危险度 |
| --- | --- | --- |
| DBCC PAGE(db,file,page,2) | 页转储到消息 | 只读低 |
| DBCC INPUTBUFFER(spid) | 某会话此刻在执行 | 只读低 |
| DBCC TRACEON(1222,-1) | 死锁详单全局开 | 日志量中 |
| DBCC DROPCLEANBUFFERS | 清缓冲池测冷跑 | 生产禁用高 ⚠️ |
| DBCC CHECKIDENT 重置 | 身份种子手术 | 数据语义高 ⚠️ |

## 核心概念速览（中英对照）

1. **意向锁** — Intent Locks (IS/IX/IU)：分层对象的意图声明，表行握手协议 ⚠️。
2. **更新锁** — Update Lock (U)：读转写中间态，防转换死锁经典款 ⚠️。
3. **范围锁** — Key-Range Lock：SERIALIZABLE 下锁"键之间的空隙"防幻读 ⚠️。
4. **锁升级** — Lock Escalation：细锁并成表锁的内存自保 ⚠️✅(Learn)。
5. **转换等待** — Conversion Wait：阻塞链的基本单元，比持有时间更该看 ⚠️。
6. **死锁** — Deadlock：等待图成环，牺牲品+重试是工程终解 ⚠️✅(Learn)。
7. **RCSI** — Read Committed Snapshot Isolation：语句级行版本，写不挡读 ⚠️✅(Learn)。
8. **SNAPSHOT** — Snapshot Isolation：事务级一致视图+更新冲突检测 ⚠️✅(Learn)。
9. **版本存储** — Version Store：tempdb 里的旧行链，保留线=最慢读者 ⚠️。
10. **更新冲突** — Update Conflict：两快照事务改同行，后者出局 ⚠️。
11. **CHECKDB** — DBCC CHECKDB：分配+记录+元数据三段全库审计 ⚠️✅(Learn)。
12. **幽灵腐败** — Ghost/Logical Corruption：备份与还原都发现不了的逻辑错 ⚠️。
13. **单页恢复** — Page-level Restore：824 时代的定点手术(企业版) ⚠️。
14. **DBCC PAGE/TABLERESULTS** — 页转储与结果灌表：内核考古铲 ⚠️✅(Learn)。
15. **TRACEON/旗标** — Trace Flags：运行时开关，TF 1118 时代口水战的证物 ⚠️✅(Learn)。

## 最新演进与工业实践

- **2012→2019**：RCSI/SI 从"企业版专属"到全版本可用 ⚠️ 转述；锁诊断从 1204 文本迁到 XEvent xml deadlock graph；**Hekaton(2014 GA)**以"无锁乐观验证+无页"另起炉灶(✅ https://learn.microsoft.com/en-us/sql/relational-databases/in-memory-oltp/overview-and-usage-scenarios ，[../../db/Hekaton.md](../../db/Hekaton.md) )；TF 1118/1117 之争在 2016+ 随 tempdb 元数据改进而终结 ⚠️。
- **2022→2025**：2025 大版本把"高可用+Kubernetes"合成新叙事(✅ https://learn.microsoft.com/en-us/sql/sql-server/what-s-new-in-sql-server-2025 、✅ https://learn.microsoft.com/en-us/sql/linux/sql-server-linux-overview )——AG 容器化部署下"版本存储钉 tempdb/PVC"成为云容量规划题 ⚠️；RESTORE 侧增强持续，CHECKDB 三段论未被推翻 ⚠️。
- **工业实践**：现代事故复盘模板——阻塞链快照(sp_WhoIsActive)+死锁图持久化(XEvent)+长事务告警(版本存储水位)三件套 ⚠️ 开源工具点名不引数据；"备份+定期 CHECKDB 才配叫数据"的行业警句仍从本书/博客园时代流传至今 ⚠️ 转述。
- **理论线**：ARIES 的日志恢复与本章"边界的钉子"叙事同源([../../db/ARIES.md](../../db/ARIES.md))；隔离级别弱化的现代翻案(Mongo 默认 RC 化、FoundationDB 严格可串行化)对照 [../设计数据密集型应用/00-总览与阅读地图.md](../设计数据密集型应用/00-总览与阅读地图.md) ✅(写前 ls 已验名)。
