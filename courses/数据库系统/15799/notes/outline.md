# 15-799 讲义骨架笔记（notes/outline.md）

> 骨架级要点（Spring 2022 Self-Driving 主题）。

## L01 导论：Self-Driving DBMS
- 定义：自动配置/调优/修补的 DBMS，目标是替代 DBA 日常决策。
- 四大功能划分：预测(forecasting)、设计(physical design)、调优(tuning)、调试(debugging)。
- 为什么 DBMS 比人更适合做决策：数据在手、动作可回滚。

## L02 NoisePage/Pilot 架构巡礼
- NoisePage：MVCC + 编译执行的主存数据库；Pilot 是其自治层。
- 组件：query router / catalog / stats / tuner 的流水线关系。

## L03 负载预测 I：时序方法
- 指标时间序列（QPS、latency、资源）的 ARIMA/指数平滑基线。
- 预测误差度量：MAPE；周期性与漂移处理。

## L04 负载预测 II：异常检测与分类
- 工作负载指纹：查询模板 + 统计分布做分类。
- 异常检测触发重训练/回滚的阈值设计。

## L05 自动物理设计
- 索引选择是组合优化：what-if 假设评估（Hypothetical Indexes）。
- AutoAdmin 的「逐步演化 + 约束预算」框架；索引过多反噬写性能。

## L06 自动查询优化与自适应执行
- 执行中基数纠偏：mid-query plan switching。
- 学习型基数估计的引入点与失败模式。

## L07 参数调优（OtterTune 线）
- Knobs 空间大、反馈噪声强：贝叶斯优化/控制回路的选择。
- 工作负载嵌入 + 迁移学习缩短调优冷启动。

## L08 结构调优
- 统计信息自动重采样、schema 重构（物化视图/分区）触发条件。

## L09 DBMS 自我诊断
- 慢查询根因分类：统计过期 vs 锁等待 vs 计划退化。
- 可观测数据（执行统计、等待事件）是自治的前提。

## L10 机器学习方法的边界
- ML 组件的可靠性/可解释性要求高于一般系统。
- 「模型错了怎么办」：安全护栏与回滚设计（Lero 等无训练数据路线）。

## L11 云与多租户自治
- 资源弹性（autoscaling）与 DB 内调优的耦合。
- Serverless DB 中自治 = 计费优化的同义词。

## L12 PostgreSQL 调优实践（任务一）
- EXPLAIN (ANALYZE, BUFFERS) 读法与常用统计视图。
- 手工调优 checklist：shared_buffers、work_mem、索引、连接池、vacuum。

## L13 Pilot 改进评审（任务二）
- 读 NoisePage Pilot 源码找缺口：预测器/调优器任一模块皆可下手。
- 评估方法：基准 + A/B 对比 + 回归防护。

## L14 前沿回顾与结课
- 2021–2024 自治 DB 趋势：LLM 辅助调优、云厂商内建自治（AutoPilot/Autonomo 对照）。
- 全课地图：预测→决策→执行→反馈闭环。
