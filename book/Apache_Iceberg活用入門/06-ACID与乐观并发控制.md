# 第 6 章 ACID 事务与乐观并发控制

> ⚠️ 章题为**推定**（示意日文名：ACID 処理と楽観ロック），原书真实目录未核实，见 [00-总览与阅读地图.md](00-总览与阅读地图.md)。
> 依据：spec §Concurrency（原子替换、retry、validation 规则）与官方 `docs/reliability.md`（已核对原文：读者「always use a consistent snapshot without holding a lock」等表述）。

## 本章地图

> 一句话：**Iceberg 的「事务」= 在不可变文件上预演一次状态变更，然后用一次原子换根把它落到 catalog；没有锁表，只有「基快照还成立吗」的乐观校验——失败就重放或重算，绝不阻塞读。**

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 6.1 ACID 四字的落地 | 文件不可变+原子指针=ACID 的湖式翻译 | 逐字对应，不是修辞 |
| 6.2 提交协议 | 读基→写文件→CAS 换根 | 唯一的关键原语在 catalog |
| 6.3 冲突检测 | requirements：基快照/文件存在性 | 前提不成立即拒绝 |
| 6.4 重试语义 | 元数据重放 vs 数据重做 | 序列号继承让重试不重写数据 |
| 6.5 隔离级别 | 读=快照隔离；写=可串行化（校验达成） | 读永不排队 |
| 6.6 典型冲突场景 | 双 compaction、backfill、双 overwrite | 哪些该让、哪些该输 |
| 6.7 参数与观测 | commit.retry.*、metrics | 重试次数=表健康的体温计 |

## 核心精讲

> **教学示意，不参与构建。**

### 6.1 ACID 在湖里的翻译

| 字母 | 传统 DB（对照 [../数据库系统概念6/14-事务.md](../数据库系统概念6/14-事务.md)、[../mysql/18-事务的庐山真面目.md](../mysql/18-事务的庐山真面目.md)） | Iceberg 的实现 |
| --- | --- | --- |
| A | 日志保证全做/全不做 | 新文件先写完；换根前读者看不到任何变更；换根单点生效 |
| C | 约束检查、恢复 | 提交前的 validation（§6.3）+ 元数据自洽的 schema/spec 校验 |
| I | 锁/MVCC | **快照隔离天然成立**：读固定在自己的基快照上 |
| D | WAL + fsync | 依赖对象存储的文件持久性；「Durability 外包给 S3，原子性外包给 catalog」 |

「外包」不是贬义：Iceberg 把**它不擅长**的（字节持久化、目录指针 CAS）交给已有强保证的系统，把**它擅长的**（可回滚的状态树）做成规范——这正是规范先行的架构品味。

### 6.2 提交协议：TableOperations 的 CAS

```text
commit(当前基 metadata B, 新状态 ops):
  1. 写数据文件（并行 task 完成，全部不可变）
  2. 写新 manifest / manifest list（引用 1 的产物）
  3. 基于 B 生成新 metadata 文件 B'（current-snapshot-id=新快照,
     last-sequence-number=+1, snapshot-log/metadata-log 追加）
  4. operations.commit(B' 相对 B 的变更):
       catalog 层面把「表指针 == B」原子替换为 == B'   ← 全部协议的心脏
     失败（指针已不是 B）→ 重新刷新 current → §6.4
```

不同 catalog 的 CAS 原语不同（第 7 章）：Hive=Metastore 行记录+rename（历史上靠 rename 约定，有并发缺陷，新版有改良）；Hadoop=version-hint 文件 rename（**无锁，仅单写者假设**，官方明确不推荐生产）；Glue=UpdateTable 条件更新（`version` 参数）；JDBC=行级事务；REST=`updateTable` 携带 requirements（§6.3），服务器仲裁。**原子性强度取决于 catalog**——选型的第一道安全题。

### 6.3 冲突检测：requirements 与 validation

事务被建模为「**前提 + 动作**」（reliability 文档原话：transaction = assumptions + actions）。常见前提：

- **快照前提**：「我的基快照仍是当前」（append 类提交常用：基变了直接失败/重试均可，append 无数据冲突）；
- **内容前提**（v2 backfill/compaction 类）：「本次替换涉及的文件，在提交时**仍然全部存在**」——reliability 文档的例子正是 rewrite：若并发改写已把源文件删掉，前提不成立，提交被拒；
- **schema/spec 前提**：「schema 未变」（DDL 互斥）。

规范还定义了一组可串行化校验（§Serializable isolation 的 validation rules，v2 核心）：按序列号比较，拒绝「删除了本次将要新增的同一行」「重复消费同一批位置」等病态交错。**调低校验严格度 = 主动放弃可串行化**，入门阶段不要动。

### 6.4 重试：重放元数据，不重做数据

冲突失败后引擎刷新 current，然后：

- **可重放**（推荐路径）：把「我加的快照」重新挂到新 current 上——只需重写 manifest list（引用不变的 manifest），数据文件与 manifest 文件本身不动；序列号由新提交点重新分配（§5.5 的继承规则保证删除语义在新世界仍正确）。这就是规范说的「retry 只要求重写 manifest list」的高效来源。
- **须重算**：backfill/compaction 的源文件集合变了 → 整个 job 重做或收缩范围（新版 rewrite 支持 partial-progress 续跑，第 8 章）。
- **该放弃**：DDL 互斥、schema 不兼容——重试无意义，报错给人看。

### 6.5 隔离级别与读侧行为

- 读者：规划开始即固定 `snapshot-id`，之后所有文件按该快照解释——**快照隔离 + 无锁**；长查询安全，但要理解：它引用的文件在快照过期前不能被物理删除（第 8 章的保留窗口与「运行中的回滚历史」冲突是经典事故）。
- 写者之间：靠 §6.3 校验达到可串行化；并发 append 互不干扰，并发 overwrite/delete 按规则判胜负。
- `UPDATE`/`MERGE` 读基、写删的「读己之写」在同一事务内成立；跨事务无「行锁」概念——**不要拿 OLTP 直觉来湖上抢同一行**（热点行 upsert 的正确解是攒批 + 单写者作业，第 9 章 Flink/第 5 章 MERGE）。

### 6.6 典型冲突剧本（教学示意）

| 剧本 | 结果 | 启示 |
| --- | --- | --- |
| 两个 append | 一先一后，后者重放 manifest list 成功 | 正常态，retry 几毫秒 |
| append vs delete | 通常都成功（作用于不相交集合） | 序列号隔离了影响域 |
| 两个 compaction 同分区 | 后提交者源文件已没了 → 校验拒收 | 维护作业要**分区错峰 + 互斥锁（编排层）** |
| compaction vs 流式 append | append 成功（新 seq）；rewrite 前提若只锁旧集合可成功 | `use-starting-sequence-number=false` 等参数差异见第 8 章 |
| 两个 overwrite 同分区 | 后者基校验失败 → 重放后可能覆盖对方的分区语义？ | overwrite 的前提是「替换当前集」，重放=以对方结果为基；确需互斥时用业务锁 |

### 6.7 参数与观测

```properties
commit.retry.num-retries=4          # 默认 4：乐观提交的重试上限
commit.retry.min-wait-ms=100
commit.retry.max-wait-ms=60_000
commit.retry.total-timeout-ms=1_800_000
```

- 观测点：metrics 报告里的 commit 尝试次数/耗时（`docs/metrics-reporting.md`）；**重试均值上升 = 写者争抢加剧**，先查有没有两个作业在同一批分区做 rewrite，再考虑扩分区隔离。
- Flink 侧同名 `commit.retry.*` 参数决定 checkpoint 提交超时（第 9 章）。

## 版本演进与兼容性

- 原子换根模型自规范 0.x 不变；v2 的序列号体系让「可串行化校验」得以形式化（§5.5/6.3），v1 表没有这层保护，行级并发编辑能力本就受限。
- REST catalog 把 requirements 显式化为协议字段（assert-ref-snapshot-id 等，第 7 章）——**协议化冲突检测是 2023–2025 的主线**，旧版「靠实现自觉」的部分被规范吸收。
- 🔧 Glue/DynamoDB 类条件写能力的边界、Hive 的 `lock` 表方案（第三方）等 catalog 细节随版本变动，选型时以对应连接器文档实测为准（本目录未逐一核实的项已在 07 章标注）。

## 常见误区

| 误区 | 事实 |
| --- | --- |
| 「Iceberg 有行锁，两个 MERGE 会排队」 | 没有锁；有前提校验与重试。抢同一批行请改单写者管道 |
| 「失败的事务留下了垃圾文件，表坏了」 | 没换根的孤儿文件不影响正确性（下次 remove_orphan_files 回收）；正确性只锚定在根指针 |
| 「读阻塞写、写阻塞读」 | 读零阻塞（快照）；只有写-写冲突仲裁 |
| 「catalog 只是个查询入口」 | 它是**提交仲裁者**；catalog 的原子性弱 = 整表的原子性弱（§6.2） |
| 「retry 次数多说明表好」 | 反了：说明争抢或维护作业设计有问题（§6.7） |
| 「事务=快照，所以 expire 无所谓」 | 运行中的读者/下游依赖其基快照；expire 窗口必须 > 最长查询 + 缓冲（第 8 章） |

## 与其他章 / 其他书的联系

- 提交协议的载体（指针与 CAS）：[07-Catalog生态.md](07-Catalog生态.md)；序列号继承：[05-行级删除与删除文件.md](05-行级删除与删除文件.md) §5.5。
- 元数据树与换根对象：[02-元数据三层结构.md](02-元数据三层结构.md) §2.2/2.6。
- 教科书对照：两阶段锁与可串行化 [../数据库系统概念6/15-并发控制.md](../数据库系统概念6/15-并发控制.md)；快照隔离与 MVCC [../mysql/21-事务隔离级别与MVCC.md](../mysql/21-事务隔离级别与MVCC.md)、[../../db/mvcc.md](../../db/mvcc.md)（行级版本链 vs 文件级快照链的最佳辨析材料）；恢复视角 [../数据库系统概念6/16-恢复系统.md](../数据库系统概念6/16-恢复系统.md)。
- 姊妹目录：[../Engineering_Lakehouses_with_Open_Table_Formats/06-事务与并发写.md](../Engineering_Lakehouses_with_Open_Table_Formats/06-事务与并发写.md)（三格式并发协议横评）。

## 思考题

1. 为什么「换根前写好的数据文件」不算脏数据？这对失败重试的幂等性有什么用？
2. Hadoop catalog 的 `version-hint` rename 为何不满足生产多写者？缺了哪个原语？
3. 两个并发 compaction 同分区，后提交者被拒——如果放宽校验让它成功，会弄丢什么？
4. 长 ETL 读到 t0 快照；t0+1h 有人 expire 了 t0 之前的快照并删了文件——它一定没事/一定出事吗？关键变量是什么？
5. 把 §6.6 每行剧本画成 snapshot 树，与 [../mysql/21-事务隔离级别与MVCC.md](../mysql/21-事务隔离级别与MVCC.md) 的 read view 时间线对照，哪一步是「湖式多版本」与 DB 多版本的本质分岔？
