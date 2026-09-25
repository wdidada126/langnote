# 15-799 配套项目计划（projects/README.md）

> 官方任务：任务一 PostgreSQL 手动性能调优；任务二基于 NoisePage Pilot 改进 Self-Driving DBMS（不限特性）；另有 Group Project。本轮只列计划不写代码。

| 章节 | 建议语言 | 小项目 | 编译/运行方式 |
| --- | --- | --- | --- |
| L03–L04 负载预测 | Python | 对 pg_stat 采样指标做时序预测（ARIMA/Prophet 基线）并画出 MAPE 对比 | `python forecast.py --metrics stats.csv` |
| L05 索引自动设计 | Python/SQL | 给定查询工作负载，贪心索引选择器 + 假设索引收益评估 | `python idx_selector.py workload.json` |
| L06 自适应执行 | C++ | 在 Postgres `jit/EXECUTOR` 观测下模拟 mid-query 计划切换的小实验 | SQL 脚本 + `EXPLAIN (ANALYZE, BUFFERS)` |
| L07 参数调优 | Python | 简化版 OtterTune：高斯过程/随机森林选 knobs 的贝叶斯优化循环（基准：TPC-C 缩样） | `python tuner_loop.py --db pg` |
| L12 任务一：PostgreSQL 调优 | SQL/PLpgSQL | 慢查询根因分析手册：统计过期/索引缺失/NLJ 退化 三类案例的手动修复前后对比 | `psql` + 基准脚本 `run_bench.sh` |
| L13 任务二：NoisePage Pilot 改进 | C++ | Pilot 某模块（预测/调优/回滚护栏）的改进 PR 级实现与 A/B 评测 | `cmake -B build && cmake --build build`（官方流程，本轮不编译） |
| L14 Group Project | 自选 | 自治组件集成 demo：指标采集→异常触发→动作执行→回滚验证 闭环 | 独立 build 脚本 |
| 对照阅读 F2013 | Java/Go | 图计算（PowerGraph 风格 PageRank）与流处理（MillWheel 风格窗口聚合）各一个小实现 | `mvn package` / `go build` |

环境约定：Python ≥3.10（pandas/statsmodels）、PostgreSQL 15+、NoisePage 源码（Ubuntu/CMake）；本轮只写不编译，集中编译由用户稍后统一执行。
