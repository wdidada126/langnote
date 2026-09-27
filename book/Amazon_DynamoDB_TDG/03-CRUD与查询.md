# 03 · CRUD 与查询语言：六动词 + 两读法（⚠️ 重构章题）

> 章定位：DynamoDB 的数据面 API 是一个刻意瘦小的动词表。本章按「写族/读族/事务族/表达式语法」四条线讲清每个动词的计费与一致性含义。取证锚：WorkingWithItems.html ✅200、Expressions.UpdateExpressions.html ✅200、HowItWorks.ReadConsistency.html ✅200、transactions.html ✅200。

## 1. 写族：Put / Update / Delete / BatchWrite

- **PutItem**：整条目替换（last-writer-wins 语义下的全量写）；想「只改一个字段还覆盖别人」是经典事故 ⚠️。
- **UpdateItem**：原子修改表达式。SET / REMOVE / DELETE(集合元素) / ADD(数值与集合) 四操作；`#r=:r` 别名语法处理保留字 ✅ 表达式页原文示例含该行法。
- **DeleteItem**；**BatchWriteItem**：≤25 条目/请求的配额约束 ⚠️ 转述（配额页为动态渲染，本代理未取得静态数字实证，按纪律标 ⚠️）。
- 写路径一致性：表内多副本写为服务内部同步复制（跨 AZ），对用户呈现「写成功即持久」⚠️ 转述口径。

## 2. 条件写与乐观锁（最重要的安全阀）

- `ConditionExpression` 挂在 Put/Update/Delete 上，条件不满足返回 `ConditionalCheckFailedException` ✅ 主题页存目。
- **version 属性乐观锁模式** ⚠️ 转述通式：读出 `version`，写回时条件 `version = 旧值` 且 SET 新值——无中心锁的并发更新正解；对位 DDIA [../设计数据密集型应用/07-事务.md](../设计数据密集型应用/07-事务.md) 的 CAS 谱系。
- 幂等 upsert：`attribute_not_exists(id)` 条件实现「存在即不覆盖」⚠️ 社区惯用法转述。

## 3. 读族：Get / Query / Scan

- **GetItem**：按完整主键点查，默认最终一致，可请求强一致 ✅ ReadConsistency 页 200（页面原文含 eventually consistent / strongly consistent 两档表述）。
- **Query**：PK 等值（或若干 IN）+ SK 条件；返回按 SK 有序、1MB 分页 ⚠️ 分页字节口径转述；`ScanIndexForward=false` 取倒序 ⚠️。
- **Scan**：全表（或全索引）逐行过 + FilterExpression 过滤——费用先付后筛，生产环境默认视为反模式 ⚠️。
- **ProjectionExpression**：只取所需列，读费仍按命中条目尺寸算 ⚠️（省网络不省 RCU 的口径来自 05 章计费模型）。
- 表达式语法族：KeyConditionExpression / FilterExpression / ConditionExpression / ProjectionExpression 四套，占位符 `#n :v` 防保留字 ✅ UpdateExpressions 页同族语法。
- **PartiQL**：标准兼容 SQL 子集（SELECT/INSERT/UPDATE/DELETE 走同一服务）⚠️ 转述；文档 tutorial-partiql/QueryWithPartiQL 页 302 跳转（版本化重定向，可引 ⚠️）。

## 4. 事务族：TransactGetItems / TransactWriteItems

- 官方 transactions 页 ✅200（https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/transactions.html）主题：跨条目跨表 ACID、客户端事务令牌幂等、单次上限条目数 ⚠️ 具体上限数字未取得静态实证（记忆为 100/读25 写 口径——标 ⚠️ 不写死）。
- 计费含义：事务读写费用约为普通操作 2 倍 ⚠️ 转述（社区通识，配额页动态）。
- 与条件写的取舍：单条目冲突控制→条件写即可（1 倍费）；多条目原子→才上事务 ⚠️ 最佳实践通识。
- 谱系对照：MongoDB 多文档事务（[../MongoDB_The_Definitive_Guide_3e/00-总览与阅读地图.md](../MongoDB_The_Definitive_Guide_3e/00-总览与阅读地图.md) 第 05/10 章域）与 Dynamo 事务同为「NoSQL 补 ACID」运动 ⚠️。

## 5. 一致性档位：全部读操作的两选项

| 档位 | 延迟代价 | 语义 |
|---|---|---|
| 最终一致（默认） | 低 | 可能读到旧值；写后立读有窗口风险 ⚠️ |
| 强一致 | 略高、按双倍 RCU 计 ⚠️ | 读必见最近确认写 ✅ 定义见 ReadConsistency 页 |

- GSI 上的查询只能最终一致 ✅ SecondaryIndexes 页原文含「eventual consistency only」字样（04 章展开）。
- 概念深挖走 DDIA [../设计数据密集型应用/09-一致性与共识.md](../设计数据密集型应用/09-一致性与共识.md)。

## 6. 重试与错误形态

- 限流错误 `ProvisionedThroughputExceededException` → 指数退避 + 抖动重试 ✅ 主题页 Programming.retries.html 200（含 exponential backoff 口径）。
- 条件失败、资源未找到、校验失败应区分处理——把 `ConditionalCheckFailedException` 当错误吞掉是乐观锁反模式 ⚠️。
- 幂等写设计：client token / 条件写双保险 ⚠️ 转述。

## 7. 本机演示（非 DynamoDB 行为，仅语法直觉）

SQLite 无法演示 RCU/一致性，但可以演示「条件更新=where 子句携带旧值」的乐观锁骨架：`UPDATE t SET v=?, ver=ver+1 WHERE k=? AND ver=?`，`rowcount==0` 即条件失败——对应 DynamoDB ConditionExpression 的编程形状（🔧 属通用 SQL 语义，不算本册类比组计数，类比组见 02/04/05/06）。

## 8. API 动词全表（数据面总账）

| 动词 | 族 | 一致性 | 关键约束 ⚠️/✅ |
|---|---|---|---|
| PutItem | 写 | 强（写即确认） | 整条覆盖；可挂条件 ✅ |
| UpdateItem | 写 | 强 | SET/REMOVE/DELETE/ADD ✅ 表达式页 |
| DeleteItem | 写 | 强 | 可挂条件；幂等（不存在=无声成功）⚠️ |
| BatchWriteItem | 写 | — | ≤上限条目、无事务性 ⚠️ |
| TransactWriteItems | 写(事务) | 原子 | 多条目回滚+令牌幂等 ✅ 页存目 |
| GetItem | 读 | 两档 | 全键定位；强一致双倍 ⚠️✅ |
| BatchGetItem | 读 | 两档 | 部分成功语义 ⚠️ |
| Query | 读 | 两档(基表)/仅最终(GSI) ✅ | PK 必给、SK 可条件 ⚠️ |
| Scan | 读 | 两档 | 全量扫+过滤，费用前置 ⚠️ |
| TransactGetItems | 读(事务) | 快照读 ⚠️ | 上限条目 ⚠️ |
| PartiQL Execute* | 读/写 | 随底操作 | SQL 子集 ⚠️ |

## 9. 错误形态分诊表 ⚠️（✅ 主题域在架）

- `ResourceNotFoundException`：表名/区域/拼写三查。
- `ValidationException`：表达式语法、保留字、类型描述符错。
- `ConditionalCheckFailedException`：乐观锁正常回弹——业务分支处理，非告警。
- `ProvisionedThroughputExceededException`：容量或热点信号（05 章剧本）。
- `ThrottlingException` / `InternalServerError` / 超时无响应：退避重试（✅ retries 页）。
- 事务 `TransactionCanceledException`：内含逐条目原因码，需拆因（幂等冲突/条件失败/可重试）⚠️。

## 10. 写路径演练题（纸面推演，合卷作答）

1. 库存扣减：读 5 件库存→改 4→写回。给出你的 ConditionExpression 与失败后策略；为什么不能用 PutItem 裸写？
2. 会话续期：同一 session 两条并发写，期望「最后到达者赢」——该用哪种写动词？何时反而会害你？
3. 「下单写 3 表」的场景清单：哪些能拆成幂等补偿、哪些必须原子？对应 §4 的哪条判据？
4. Query 分页：LastEvaluatedKey 回环的正确退出条件与费用预算法（提示：1MB 页 ⚠️）。

## 11. 读写动词的「费用-一致性」双轴速记 ⚠️ 汇总

- 最便宜读：基表 Query 最终一致 + 投影 + 前缀精确 → 一页命中（05 章 RCU 颗粒）。
- 最贵读：Scan 全表 + Filter + 强一致 —— 双罚（扫得多、颗粒加倍）⚠️。
- 最安全写：UpdateItem + ConditionExpression（原子、单条目、1 倍费）✅ 域。
- 最重写：事务多条目（原子域扩张的代价）⚠️；能拆幂等就别上事务。
- 批式动词无原子承诺：Batch 两兄弟是「多请求打包」不是「事务」——语义读官方动词表确认 ⚠️。
- 分页三件套：Limit / ExclusiveStartKey / LastEvaluatedKey——Query 扫穿即继续，账单不看你的循环 ⚠️。

## 12. 一句话记忆卡

- 六动词两读法：写要条件，读要前缀。
- Put 是覆盖不是合并——事故榜第一名 ⚠️。
- Query 花钱在键，Scan 花钱在命不中的每一行 ⚠️。
- 条件写是 NoSQL 里的 CAS，用熟它事务能省一半。
- 分页三件套不带「够了」信号，账单也不带。

## 核心概念速览（中英对照）

1. **PutItem/UpdateItem/DeleteItem** — 写族三动词：整写/表达式改/删 ✅。
2. **BatchWriteItem** — 批量写：受请求内条目上限约束 ⚠️。
3. **条件写** — conditional write：`ConditionExpression` 原子上架；失败抛 ConditionalCheckFailedException ✅。
4. **乐观锁** — optimistic concurrency control：version 属性条件回写模式 ⚠️。
5. **GetItem** — 主键点查：两档一致性可选 ✅。
6. **Query** — 键查询：PK 前缀 + SK 条件，天然有序分页 ⚠️。
7. **Scan** — 全扫：先付钱后过滤的反模式默认态 ⚠️。
8. **FilterExpression** — 过滤器：命中后才筛，不减免读费 ⚠️。
9. **ProjectionExpression** — 投影：列裁剪，省网络不省 RCU ⚠️。
10. **PartiQL** — 标准 SQL 子集接口 ⚠️（页面 302 跳转口径）。
11. **TransactWriteItems** — 事务写：多条目原子 + 回滚，费用加倍 ⚠️。
12. **指数退避** — exponential backoff：限流后的标准客户端行为 ✅ 200 页。
13. **强一致读** — strongly consistent read：见最近确认写，双倍读费 ⚠️。

## 最新演进与工业实践

- **取证快照（2026-09-27）**：本章四张核心 docs 页全部 200 实抓（Items/UpdateExpressions/ReadConsistency/transactions），retries 页 200；PartiQL 两页与 BackupRestore 类旧 slug 为 302 版本化跳转——写引用时注意 docs 站内重命名常态。
- **条件写仍是 2026 年无锁并发的第一推荐**：AWS 博客与文档持续以 version 模式为示范 ⚠️ 转述；对照 Cassandra LWT（盘上 [../Cassandra_The_Definitive_Guide/00-总览与阅读地图.md](../Cassandra_The_Definitive_Guide/00-总览与阅读地图.md) 05 章域）同为「轻量级 CAS 上架」运动。
- **事务与 DynamoDB**：Transact API 已成无服务器编排的兜底组件，社区常以「Saga + 条件写」替代重事务控费 ⚠️。
- **工业实践 ⚠️**：生产团队普遍把 Scan 列为需审批操作（CloudWatch 告警 + IAM deny），配套 DAX/缓存层见 05 章。
