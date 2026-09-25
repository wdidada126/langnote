# CS346 讲义骨架笔记（notes/outline.md）

> 骨架级要点，按 RedBase 四大组件 + 扩展组织。

## L01 课程导论与 RedBase 架构
- RedBase = 记录管理 + 索引 + 系统管理 + 查询语言 四组件的单机关系数据库。
- 与 15-445 BusTub 对照：目录结构、测试驱动方式、C++ 风格差异。

## L02 记录管理：记录与 RID
- 属性类型系统（int/float/string）与记录二进制布局。
- RID = (page number, slot number)：上层一切定位的基石。

## L03 页与表空间管理
- paged file 抽象：读页/写页/分配页；DB 头页与空闲页链。
- 页内目录（slot directory）与删除回收——避免文件膨胀的老问题。

## L04 B+ 树索引组件
- 内部节点/叶节点分离、叶链、分裂与再分配。
- 游标遍历与范围扫描；与 445 P2 的对拍点。

## L05 索引与记录层联动
- 二级索引键→RID 回表；聚簇索引键→记录。
- 删除记录时索引项清理的级联一致性。

## L06 系统管理：DDL
- create/drop table 的解析、校验与元数据落盘。
- 类型检查与名字唯一性在 DDL 层的职责边界。

## L07 命令行与数据加载
- CLI 交互循环：命令分发、错误处理、退出清理。
- load 数据文件：批量插入时 buffer pool/页分配的批处理优化。

## L08 元数据管理（Catalog）
- schema/catalog 的持久化结构与系统表设计。
- 启动时重建内存目录；DDL 与 catalog 的事务性（本课简化点）。

## L09 查询语言 RQL 设计
- RQL 语法：select/insert/delete/update + where 子句。
- 解析器与 AST：手写 vs lex/yacc 的取舍。

## L10 RQL 执行
- 谓词下推到扫描/索引选择：有索引走 B+ 树，否则全表扫描。
- insert/delete/update 复用记录层原语的实现路径。

## L11 表达式求值与过滤
- 属性比较、常量折叠、类型转换。
- 过滤算子与迭代器风格封装。

## L12 扩展：Blob 类型
- 变长大对象存储：溢出页链与外部文件两种方案。

## L13 扩展：网络模块 / 连接算法
- 把 CLI 换成 socket 服务：会话与协议帧设计。
- 增加 NLJ/Sort-Merge/Hash Join 并比较代价。

## L14 扩展：CBO / OLAP / 事务
- 从规则优化到代价优化：引入统计信息的最小改动。
- OLAP：group by 聚合；事务：锁表 + WAL 补课。

## L15 总结
- RedBase 与真实 DBMS 的差距清单：并发、恢复、优化器、复制。
- 读 Architecture of a Database System 复盘全局视野。
