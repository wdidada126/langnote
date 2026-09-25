# CS122 配套项目计划（projects/README.md）

> 官方作业在 NanoDB（Java/Maven）上完成 7 Assignments + 2 Challenges；本轮只列计划不写代码。推荐使用 IDEA 打开工程，注意日志相关配置（csdiy 提示）。

| 章节 | 建议语言 | 小项目 | 编译/运行方式 |
| --- | --- | --- | --- |
| L02–L04 存储/DML（A1） | Java | delete/update 语句支持；buffer pool pin/unpin 修补；insert 性能提升且控制文件膨胀 | `mvn test`（A1 测试集） |
| L05–L07 计划与 Join（A2） | Java | 简单计划生成器：AST → 执行计划；nested-loop join 支持 inner/outer；补齐单元测试 | `mvn test`（A2 测试集） |
| L08–L10 统计与代价（A3） | Java | 表统计收集、节点成本计算、谓词选择率、输出元组统计传播 | `mvn test`（A3 测试集） |
| L11 B+ 树 | Java | NanoDB 索引实验：插入/分裂/范围扫描 | `mvn test -Dtest=*Index*` |
| L12 聚合 | Java | Agg / GROUP BY 算子（hash/sort 两种策略与代价选择） | `mvn test` |
| L13 子查询 | Java | IN/EXISTS 子查询执行与去相关改写 | `mvn test` |
| L14 WAL/事务 | Java | 日志记录 + 崩溃恢复重放实验 | `mvn test -Dtest=*Wal*` |
| L15 Challenge 1 | Java | 多表连接顺序优化器升级（DP 枚举 vs 贪心对比报告） | `mvn verify` + 实验记录 |
| L15 Challenge 2 | Java | 更精细统计（直方图）驱动的选择率改进 | `mvn verify` |
| 自选加深 | Python | 用 sqlite3 `EXPLAIN QUERY PLAN` 对照自家计划生成结果 | `python compare_plans.py` |

环境约定：JDK 8+/11 + Maven，GitLab 私有仓库克隆（cs122-19wi）；本轮只写不编译，集中编译由用户稍后统一执行。
