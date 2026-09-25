# CS346 论文与应用清单（papers.md）

## 经典论文

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
| --- | --- | --- | --- |
| Architecture of a Database System (Hellerstein, Stonebraker, Hamilton) | 2007 | DBMS 全栈架构综述，RedBase 四组件的坐标系 | L01/L15 |
| Organization and Maintenance of Large Ordered Indexes (Bayer & McCreight) | 1972 | B 树原始论文：平衡多路索引的源头 | L04 |
| The Ubiquitous B-Tree (Comer) | 1979 | B/B+ 树系统综述，索引组件理论底本 | L04/L05 |
| The Design and Implementation of POSTGRES (Stonebraker et al.) | 1986 | POSTGRES 原型：扩展类型与自研查询语言的参照 | L09/L12 |
| Object-Relational Support in PostgreSQL (Stonebraker & Kemnitz) | 1991 | 大对象/扩展类型（Blob）支持的设计经验 | L12 |
| Access Path Selection in a Relational Database Management System (Selinger et al.) | 1979 | CBO 代价优化器奠基，L14 优化器扩展蓝本 | L14 |
| Query Optimization Techniques (Graefe 综述/教材) | 1993 | 连接/排序/哈希算子体系化综述，L13 扩展参考 | L13 |
| ARIES: A Transaction Recovery Method (Mohan et al.) | 1992 | WAL/ARIES 恢复算法，L14 事务扩展参考 | L14 |
| Morsel-Driven Parallelism (Leis et al.) | 2014 | 并行执行调度模型 | L13/L14 |

> 填正式笔记时每条附原文链接。

## 近 5 年论文（2021–2026）

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
| --- | --- | --- | --- |
| Umbra: A Disk-Based System with In-Memory Performance 后续系列 (Fretags, Kohn, Rendle et al.) | 2021–2023 | 编译执行 + 指针钉住的现代混合存储引擎 | L02–L05/L13 |
| BtrBlocks: Efficient Column-Oriented Compression (Kohn, Leis, Marks) | 2023 | 列压缩新标杆，扩展 OLAP 时可参考 | L14 |
| Data Management for Data Science: Towards Embedded Analytics 后续工程篇 (Raasveldt & Munz, DuckDB 系列) | 2021–2023 | 嵌入式分析引擎的执行与序列化设计，RedBase 式小内核的现代样本 | L11/L13 |

## 知识点在开源项目中的应用

| 知识点 | 开源项目 | 说明 |
| --- | --- | --- |
| 记录/页管理 | SQLite（页格式）、PostgreSQL heap | L02–L03 的工业对应 |
| B+ 树索引 | InnoDB、SQLite、LMDB | L04–L05 |
| DDL/Catalog | PostgreSQL pg_catalog、MySQL 8.0 data dictionary | L06–L08 |
| 自研查询语言执行 | DuckDB（SQL→算子树）、SQLite VM | L09–L11 |
| 连接算法扩展 | DuckDB（Hash Join）、PostgreSQL（三种 Join） | L13 |
| Blob/大对象 | PostgreSQL TOAST、MySQL 外部存储 | L12 |
| 事务与恢复 | SQLite journal/WAL、InnoDB redo | L14 |
