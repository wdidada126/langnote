# CS346 配套项目计划（projects/README.md）

> 官方主线即在 RedBase（C++）上完成 4 Projects + 1 Extension；本轮只列计划不写代码。

| 章节 | 建议语言 | 小项目 | 编译/运行方式 |
| --- | --- | --- | --- |
| L02–L03 记录管理（P1） | C++ | Record/RID 布局 + paged file 读写与页分配完善 | `make redbase && ./test_driver`（官方测试驱动） |
| L04–L05 B+ 树（P2） | C++ | 索引组件：插入/删除/分裂 + 范围游标 | `make && ./index_test` |
| L06–L08 系统管理（P3） | C++ | DDL 解析执行、CLI 命令循环、load 数据、catalog 持久化 | `make && ./rcp`（RedBase CLI） |
| L09–L11 查询语言（P4） | C++ | RQL select/insert/delete/update 端到端跑通 | `make && ./rcp` + 官方 RQL 脚本 |
| L12 扩展：Blob | C++ | 溢出页链实现大对象存取 | 扩展测试 `make ext_blob_test` |
| L13 扩展：网络模块 | C++ | TCP 服务器包装 CLI：会话协议 + 并发客户端 | `make server && ./rb_server` |
| L13 扩展：连接算法 | C++ | NLJ → Hash Join，TREC/TPC-H 小基准对比 | `make join_bench` |
| L14 扩展：CBO | C++ | 收集统计 + 代价选择访问路径 | `make cbo_test` |
| L14 扩展：事务 | C++ | 表级锁 + WAL redo-only 恢复 | `make txn_test` |
| 对照学习 | C++ | 同一 RQL 查询在 SQLite `EXPLAIN QUERY PLAN` 下的行为对照 | `sqlite3` 手工实验脚本 |

环境约定：C++17、CMake 与官方 Makefile 并存；代码库克隆自 github.com/junkumar/redbase；本轮只写不编译，集中编译由用户稍后统一执行。
