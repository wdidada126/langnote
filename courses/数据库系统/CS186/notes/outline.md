# CS186 讲义骨架笔记（notes/outline.md）

> 骨架级要点，待听课/读讲义后展开。

## L01 课程导论
- 数据库 vs 文件系统：并发性、持久性、随机访问、数据独立性的四大痛点。
- DBMS 组件鸟瞰：解析器、优化器、执行引擎、缓冲池、事务管理器（后续每讲回填一块）。
- 三层数据模型：概念/逻辑/物理。

## L02 ER 模型与数据库设计
- 实体、属性、关系；一对一/一对多/多对多。
- 弱实体与识别依赖；继承。
- ER → 关系模式的映射规则。

## L03 关系模型
- 关系 = 元组集合；域与笛卡儿积形式化。
- 超键/候选键/主键；实体完整性与参照完整性。
- SQL 类型系统概览。

## L04 关系代数
- 一元：σ 选择、π 投影；二元：×、⋈、∪、−。
- 除法 ☵ 处理「所有/全部」类查询。
- 代数等价变换是查询优化的地基。

## L05 SQL 基础
- SELECT-FROM-WHERE 求值顺序 ≠ 书写顺序。
- 连接谓词 vs JOIN 语法；空值三值逻辑陷阱。
- 聚合与 GROUP BY/HAVING 语义。

## L06 SQL 进阶
- 相关子查询与解相关；EXISTS/ANY/ALL。
- 窗口函数 OVER (PARTITION BY ... ORDER BY)。
- UPDATE/DELETE 与约束修改。

## L07 NoSQL 与半结构化
- 动机：写扩展、schema 灵活性、可用性取舍（CAP 直觉）。
- 键值/文档/列族/图四类；MongoDB/Redis/DynamoDB 风格对比。
- JSON 查询与无模式设计反模式。

## L08 存储与 I/O
- 磁盘模型：寻道/旋转/传输；页是 I/O 单位。
- SLASH 记录布局：定长 vs 变长记录、指针重排。
- 堆文件页组织与 free-space map。

## L09 Buffer Pool
- 页面淘汰：LRU 的缺陷、Clock/LRU-K、pin 计数与脏页写回。
- BufferPool 是上层一切算法的地基：所有读页必须走它。
- Project 3/4 中 bufferPool 性能直接决定作业分数。

## L10 索引 I：为什么是 B+ 树
- 全表扫描 vs 索引；哈希索引的等值优势与范围劣势。
- 多路平衡搜索树压缩树高、适配页 I/O。
- 聚簇 vs 非聚簇、二级索引回表。

## L11 索引 II：B+ 树操作
- 插入分裂、删除合并/借位；内部节点只存键+子指针，叶节点链成有序链表。
- 游标 (cursor) 与范围扫描。
- Project 3：实现 B+ 树并跑并发测试。

## L12 查询执行 I：迭代器模型
- Volcano/火山模型：open/next/close；生产者-消费者流水线。
- 物化算子 (sort/hash agg) 打断流水线。
- 表达式求值与投影/过滤算子。

## L13 查询执行 II：排序
- 外部归并排序：pass 0 内存跑批 + 多路归并；I/O 代价分析。
- Project 4 核心：SortOperator 处理超内存排序。

## L14 查询执行 III：连接算法
- NLJ/索引连接/Block NLJ；Sort-Merge Join；Hash Join（build/probe、溢出分区）。
- 各算法的 I/O 代价公式与适用条件。

## L15 优化 I：统计与基数估计
- 直方图/NDV；谓词选择率估计（等值/范围/LIKE）。
- 组合谓词的独立性假设（常错但便宜）。
- 基数估计错误是优化器翻车的根源。

## L16 优化 II：代价与连接顺序
- 自底向上动态规划枚举连接树；系统目录存统计。
- 表达式改写规则（谓词下推、投影下推）。
- Project 4 的 query optimizer 部分。

## L17 事务与 ACID
- 事务边界、savepoint；隔离级别在 SQL 标准中的四大异常定义。
- 丢失更新、脏读、不可重复读、幻读的具体反例。

## L18 并发控制 I：串行化与 2PL
- 冲突可串行化：冲突图 + 无环判定。
- 严格 2PL：读写锁、锁升级、与死锁。
- Project 5：LockManager + 死锁检测（wait-die/wound-wait）。

## L19 并发控制 II：MVCC 与快照隔离
- 时间戳排序、T/O 恢复动作。
- 快照隔离与两版本/多版本；写偏斜 (write skew) 反例。
- Postgres/MySQL 的实际隔离级别对照。

## L20 死锁
- 检测：等待图找环；处理：victim 选择策略。
- 预防：超时、优先级时间戳方案。

## L21 恢复 I：WAL 与 ARIES
- Steal/No-force 缓冲策略与日志充分性。
- WAL 协议、LSN、redo/undo；ARIES 的 DPT 思想。
- Project 6：给数据库加日志与恢复。

## L22 恢复 II：检查点与故障分类
- Fuzzy checkpoint 缩短恢复时间；分析/redo/undo 三阶段。
- 事务故障 vs 系统故障 vs 介质故障的不同药方。

## L23 分布式 I：复制与共识
- 主-备、多主、无主复制；读-your-writes 等一致性保障。
- Quorum R+W>N；Paxos/Raft 定位（配合 6.824）。

## L24 分布式 II：分片与 NewSQL
- 范围/哈希分片、再平衡；跨分片查询与 2PC。
- Spanner/BigQuery 风格；并行数据库 Shared-Nothing。

## L25 总结
- 一条 SQL 的完整旅程串讲：parse → rewrite → plan → execute → buffer → disk → commit → recovery。
- 六个 Project 的知识点映射复盘。
