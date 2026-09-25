# CS186 配套项目计划（projects/README.md）

> 官方 6 个 Project 用 Java 造一个关系型数据库（Bloom 框架）；本轮只列计划不写代码。下表同时给出章节级自选小练习。

| 章节 | 建议语言 | 小项目 | 编译/运行方式 |
| --- | --- | --- | --- |
| L05 SQL | Java/SQL | 官方 Project 1：SQL 查询书写与关系建模练习集 | `mvn test -Dtest=proj1` |
| L07 NoSQL | Java | 官方 Project 2：MongoDB 风格文档查询 + GridFS? 简化为 JSON 查询器 | `mvn test`（配本地 MongoDB） |
| L08–L09 存储/缓冲池 | Java | 自写 SLASH 记录布局 + Clock 淘汰 buffer pool 单测 | `mvn test -Dtest=BufferPoolTest` |
| L10–L11 B+ 树 | Java | 官方 Project 3：B+Tree 索引（插入/删除/范围扫描/游标） | `mvn test -Dtest=BTreeDebug` |
| L12–L16 执行与优化 | Java | 官方 Project 4：排序算子、Join 算子与查询计划优化器 | `mvn test -Dtest=QueryTest` |
| L17–L20 事务并发 | Java | 官方 Project 5：Lock Manager、死锁检测、多轮并发压力测试 | `mvn test -Dtest=TransactionTest` |
| L21–L22 恢复 | Java | 官方 Project 6：崩溃恢复日志（WAL）与重启重放 | `mvn test -Dtest=RecoveryTest` |
| L23–L24 分布式 | Go | 自选：分片 KV + Raft 复制（对接 etcd/raft 库） | `go test ./...` |
| 全程 复盘 | Python | 用 sqlite3/psql 观测真实引擎：EXPLAIN、隔离级别反例复现 | `python observe_isolation.py` |

环境约定：JDK 17 + Maven（官方 Bloom 骨架）；本轮只写不编译，集中编译由用户稍后统一执行。
