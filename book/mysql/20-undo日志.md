# 第 20 章 后悔了怎么办——undo 日志

> 原书说明：标题为「后悔了怎么办——undo日志」，基于 MySQL 5.7.22 撰写。本文件按其思路展开**回滚段、insert/update 的 undo 记录、版本链、purge 与长事务问题**，并补齐 5.7/8.0 的演进与 2020 年之后必须补的**8.0 独立 undo 表空间、trx_id 复用陷阱、大事务拆分**。

## 本章地图

> 一句话：**undo 回答「后悔了怎么办」——它既是一条「反向操作」的记录，也是 MVCC 版本链的载体；提交之后它不会被删除，而是等 purge 线程在「最老读视图之后」才回收。**

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 20.1 三种 undo 记录 | `TRX_UNDO_INSERT_REC` / `TRX_UNDO_UPD_EXIST_REC` / `TRX_UNDO_DEL_MARK_REC` | 插入的 undo 可直接丢弃；其余需保留 |
| 20.2 回滚段（rollback segment） | 段 / slot / undo 页的分配与复用 | 一个事务最多 4（max 96）个 undo 记录段 |
| 20.3 行格式里的两个隐藏列 | `DB_TRX_ID`(6B) 与 `DB_ROLL_PTR`(7B) | 没有它们就没有版本链 |
| 20.4 版本链（history list） | `roll_pointer` 串起来的历史版本 | 一致性读靠它往前找 |
| 20.5 insert 与 update 的差别 | 插入 undo 提交即可丢；更新 undo 必须留 | 写放大与 purge 压力的来源不同 |
| 20.6 回滚（ROLLBACK）怎么发生 | 顺着 undo 链反向执行 | 已提交事务也可能被「partial rollback」 |
| 20.7 purge 与长事务 | 最老 read view 卡住 purge → undo 膨胀 | 线上最常见的 undo 事故 |
| 20.8 🔧 2026 视角 | 8.0 独立 undo 表空间、trx_id 复用、undo 在线收缩 | 原书的「重启才能回收」部分已被改进 |

## 核心精讲

> **教学示意，不参与构建。** 下文结构与 `--` 片段仅用于说明 undo 的组织方式，**未在本机编译、未启动任何 MySQL 实例执行**；数值随版本变化。

### 20.1 undo 记录的三类

| 类型 | 产生时机 | 内容 | 提交后能否立刻丢弃 |
| --- | --- | --- | --- |
| `TRX_UNDO_INSERT_REC` | `INSERT` | 只记**主键**，回滚时按主键删掉 | ✅ 可以（没人会读这个版本） |
| `TRX_UNDO_UPD_EXIST_REC` | `UPDATE`（未改主键） | 记**改之前的整行镜像**（old version） | ❌ 必须留（MVCC 要读） |
| `TRX_UNDO_DEL_MARK_REC` | `DELETE`（或 `UPDATE` 把主键改了） | 记删除标记前的行，回滚时**取消删除标记** | ❌ 必须留 |

- 一个有趣的事实：**MySQL 的 `DELETE` 不是真删**，第一步只是「打删除标记」（`delete_mask=1`），真正的物理删除由 purge 线程在后台做。
- 同理，**主键.update 在 InnoDB 里常常是「删 + 插」**，代价接近一次 `DELETE` + 一次 `INSERT`。

### 20.2 回滚段：undo 存放的地方

- **结构**（教学示意，不参与构建）：
  ```text
  rollback segment (回滚段，最多 96 个)
    └─ slot (每个 undo 记录类型一个 slot，最多 1024 个)
         └─ undo page (存放实际的 undo 记录，页内复用)
  ```
- 每个事务开始时会在回滚段里占一个 slot；事务的 undo 记录写在该 slot 指向的 undo 页上（不够就再申请页）。
- InnoDB 每个事务最多同时持有 **4 个** undo 段（insert / update / …），这也是「一个事务里有 1000 个大 `DELETE` 会写爆 undo」的原因之一。
- 回滚段的分配与复用：事务结束后 slot 不立刻销毁，而是标记为空闲供下一个同类事务复用（代价是必须复用旧记录空间）。

### 20.3 行格式里的隐藏列：版本链的物理锚点

- 每条 InnoDB 行（无论 `COMPACT` / `DYNAMIC` / `REDUNDANT`）在聚簇索引里都有隐藏列：
  | 列名 | 长度 | 含义 |
  | --- | --- | --- |
  | `DB_ROW_ID`（`row_id`） | 6B | 无主键时 InnoDB 自动生成的隐藏主键 |
  | `DB_TRX_ID` | 6B | **最后修改（或创建）这条记录的事务 ID** |
  | `DB_ROLL_PTR` | 7B | **指向该行上一条版本的 undo 记录** |
- 于是「一条记录的多副面孔」（原书第 21 章标题）就有了物理载体：
  ```text
  当前记录 (trx_id=100, roll_ptr → U1)
      U1 (trx_id=88,  old image)  --roll_ptr→ U2
          U2 (trx_id=54, 更旧的 old image) --roll_ptr→ U3 ...
  ```
- 🔧 **加长字段不免费**：每一行多 6+7=13 字节；一张 1 亿行的表就是 1.3GB —— 这也是「用 `VARCHAR(255)` 还是 `TEXT` 都无所谓」这种说法不成立的原因之一。

### 20.4 版本链与 history list

- **版本链**：同一行的所有历史版本通过 `roll_ptr` 串成一条链，存放位置是 **undo 段**，不在主索引里。
- **history list（历史链表）**：把所有**已提交事务产生的 undo 记录**按「最早修改时间」串起来，purge 线程按这个链表顺序回收。
- **关键约束**：purge 必须跳过「还有人可能读到它们」的版本 —— 也就是**最老活跃 read view 之前的版本才能删**。
  ```text
  history list: [ v1, v2, v3, v4, v5 ] → purge 能删到「最老 read view 所对应位置」
  ```

### 20.5 insert 与 update 的差别：为什么 update 的 undo 更「贵」

- `INSERT` 的 undo 提交后即可删：**回滚空间几乎不增长**（除非事务一直不提交）。
- `UPDATE` / `DELETE` 的 undo 会**一直留到 purge 完成**：于是
  - 频繁更新的表 → undo 膨胀、history list 变长；
  - 一致性读的成本变高（要顺着版本链多读几个 undo 记录）；
  - purge 线程繁忙，进一步抢 IO。
- 🔧 一个可操作的推论：**「读多写少」的表（报表表、配置表）非常适合 MVCC；「写密集」的表要控制单行更新频率或用批量合并更新。**

### 20.6 回滚是怎么发生的

- `ROLLBACK` 时，InnoDB 从 undo 记录里取出「改之前的镜像」，**反向执行**回到原状态：
  - `INSERT` → 按主键删除；
  - `UPDATE` → 用 old image 覆写；
  - `DELETE` → 取消 `delete_mask`。
- 注意：**回滚不会「原地重写一遍原 SQL」**，而是直接应用 undo 里的镜像；这也是 undo 被称作**逻辑日志**的原因（redo 是物理日志）。
- 崩溃恢复中的「回滚未提交事务」也走同一套路径（见 `19-redo日志.md` 19.6 第 ③ 步）。
- 另一个常忽略的点：`ROLLBACK TO SAVEPOINT` 也是同样的机制，但**已获得的锁不会释放**（见 `18-事务的庐山真面目.md`）。

### 20.7 purge 与长事务：undo 事故的完整链条

```text
一个运行了 3 小时的报表事务（一直拿着 read view）
  → 最老 read view 停在 3 小时前
  → purge 线程不敢回收该时刻之后的所有版本
  → history list 无限增长
  → undo 表空间暴涨 / ibdata1 或 undo_0*.ibs 文件撑满磁盘
  → 后续 UPDATE 因为没有空间复用而失败（"Cannot allocate space" 类错误）
```

- 排查清单（教学示意，不参与构建，需实际连接实例）：
  1. `information_schema.INNODB_TRX` 里找 `trx_started` 最老且 `trx_state='RUNNING'` 的事务；
  2. `SHOW ENGINE INNODB STATUS` 看 `History list length`；
  3. 与之相关的等待事件（undo 页分配）。
- 常见来源：**备份工具开着事务（`mysqldump --single-transaction`）、报表查询、ORM 里忘了提交的连接池连接**。
- 处置：杀掉长事务（或先 `KILL` 再观察），undo 会在 purge 恢复后**缓慢回落**（不会立刻降）。
- 🔧 **定期巡检项**：把「最老活跃事务时长」与「history list length」纳入监控，比事后救火便宜得多。

### 20.9 🔧 undo 事故的完整处置流程

```text
1) 识别：information_schema.INNODB_TRX 找最老且仍在 RUNNING 的事务
2) 止损：KILL 该事务（或杀掉会话），先停止 undo 继续膨胀
3) 观察：History list length 是否开始回落（purge 恢复工作）
4) 排查：谁开的这个事务（应用日志 / 连接池 / 备份任务 / 报表任务）
5) 加固：
   - 把「最老活跃事务时长」加入监控与告警
   - 报表查询改走只读从库
   - 备份工具避免长时间持有事务（用 --single-transaction 的注意点）
   - 连接池设置连接级超时
6) 复盘：undo 文件大小是否需要调整；能否改为按业务高峰前预清理
```

- 判断「该不该杀事务」的准则（教学示意，不参与构建，需结合业务）：
  - 若事务只是「开着没提交」（如应用 bug），杀掉几乎无成本；
  - 若事务已经做了大量修改（undo 巨大），杀掉要执行大量 undo 回滚，**代价可能比让它继续更大** —— 此时更应优先止损磁盘、并和业务方确认。
- 🔧 **不可自动缩小**：undo 文件在 purge 追上前不会变小；`innodb_undo_log_truncate`（5.7+）在特定条件下可回收表空间，但同样「先满足 purge 条件才谈得上 truncate」。

## 版本演进

| 版本 | undo 相关变化 |
| --- | --- |
| 5.5 | undo 默认存在共享表空间 `ibdata1` 里 |
| 5.6 | `innodb_undo_tablespaces` / `innodb_undo_logs` 可让 undo **独立成文件**，并支持在线 truncate |
| 5.7 | **默认独立 undo 表空间**（`undo_001` / `undo_002`）；`innodb_undo_log_truncate` 支持在线回收 |
| 8.0 | 独立 undo 表空间成为默认且可配置数量；`performance_schema` 里可更细观测 undo 子系统 |
| 🔧 8.0.x | `innodb_max_trx_id` 相关事务 ID 管理（见 `21-事务隔离级别与MVCC.md` 的 trx_id 复用陷阱） |

## 经典论文与原始文献

| 文献 | 出处 | 贡献 |
| --- | --- | --- |
| Bernd, *The Design of a Practical Transaction Management System*（Tandem 的 TMF，Gray 的 *The Transaction Processing Concepts* 中有完整整理） | 1993 | undo 与回滚、影子分页到 undo 的演进 |
| Mohan et al., *ARIES: A Transaction Recovery Method Supporting Fine-Granularity Locking and Partial Rollbacks* | SIGMOD 1992 | undo 与 redo 混合、按需 undo、partial rollback |
| Reuter, *Concepts of Transaction Processing*（《Database Systems: Design, Implementation, & Operation》附录） | 1988 | undo 语义与恢复分类 |
| Postgres 相关论文（Stonebraker 等，MVCC 与版本存储） | 1986+ | **版本链放在主索引 / 堆内多元组**的另一种做法，与 InnoDB 的「版本放 undo」形成对照 |
| MySQL 官方文档：Undo Logs / InnoDB Undo Tablespaces | dev.mysql.com | 回滚段结构、独立表space、truncate 条件的权威口径 |

## 近年研究与工业界开源实践（2015–2026）

- **近年研究**：**多版本级联回收与 GC 设计**——InnoDB 的 undo 放在回滚段 + 历史链表，PostgreSQL 的 tuple 版本放在堆内（HOT 更新）、Oracle 放在 undo 表空间，三者的 GC 策略差异是持续研究对象；**HTAP 下的版本可见性**（TiFlash、Aurora 的读隔离需要「一致的时间戳 + 版本链」）；**长事务对系统资源的影响**被系统性研究后，工业界普遍把它列为 SLO 指标。
- **工业界开源**（star 数 2026-09-25 通过 `gh api` 实测）：
  - `mysql/mysql-server`（≈12.4k★）：undo 实现 `storage/innobase/trx/trx0undo.cc`；purge `trx0purge.cc`；行隐藏列与版本链在 `storage/innobase/include/rem0rec.h` 周边。
  - `mariadb/server`（≈8.3k★）：独立 undo 表空间的早期实现者，可与 MySQL 8.0 的默认值对照。
  - `postgres/postgres`（≈22.2k★）：**HOT 更新 + 堆内多版本**，`autovacuum` 即是它的「purge」，把「长事务卡住回收」的机理摆得非常清楚。
  - `pingcap/tidb`（≈40.6k★）：MVCC 的 GC 由 `gc worker` 按安全时间点（safe point）推进，是「版本回收受最老读事务限制」的现代工程版本。
  - `facebook/mysql-8.0`（≈115★）：大量线上关于 undo 膨胀、purge 滞后、大事务拆分的补丁与工具。

## 常见误区与本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「`DELETE` 就是把记录删掉」 | 先打 `delete_mask`，物理删除由 purge 异步完成 |
| 2 | 「提交之后 undo 就没用了」 | 还要给**一致性读**用；purge 受最老 read view 限制 |
| 3 | 「改主键的 `UPDATE` 只是改几个字段」 | 接近「删 + 插」，代价更高且会让二级索引更乱 |
| 4 | 「ibdata1 无限增长只能重启」 | 5.6+ 有独立 undo 表空间 + 在线 truncate；🔧 8.0 默认已独立，减少了 `ibdata1` 膨胀这一经典故障 |
| 5 | 「undo 文件删掉会变小」 | 已分配的文件不会自动缩小；回收靠 purge，缩小靠 truncate（需要条件满足） |
| 6 | 🔧 **本书未覆盖** | 原书基于 5.7.22，**没有** 8.0 对 undo 表空间的默认独立化配置细节，**没有** `innodb_max_trx_id` 与 trx_id 复用相关的可见性陷阱（见 `21-事务隔离级别与MVCC.md`） |
| 7 | 🔧 **本书未覆盖** | **「最老活跃事务」如何纳入监控**、以及大事务拆分的量化收益；这两条是 2026 年 undo 事故复盘的高频结论 |

## 与其他章 / 其他书的联系

- → `19-redo日志.md`：redo 重做之后由 undo 回滚未提交事务，二者共同完成崩溃恢复。
- → `21-事务隔离级别与MVCC.md`：版本链的可见性判断是 undo 的存在理由。
- → `X2-日志系统专题.md`：undo 与 redo 同属事务的「双写」成本。
- → `18-事务的庐山真面目.md`：原子性的实现者。
- → `22-锁.md`：undo 的写入需要行锁保护；长事务持有锁会放大锁冲突。
- → [15-并发控制.md](../数据库系统概念6/15-并发控制.md)：MVTO / MV2PL / 快照隔离与版本存储的三种谱系。
- → [16-恢复系统.md](../数据库系统概念6/16-恢复系统.md)（若存在）：undo 在恢复流程中的位置。
