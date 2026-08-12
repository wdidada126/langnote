# redis smaz

https://github.com/antirez/smaz


当然可以！以下是对你提供的项目 `redis-cp-rewrite-sim` 的清晰、简洁介绍：

###  项目名称：  
`redis-cp-rewrite-sim`  
GitHub 地址：[https://github.com/antirez/redis-cp-rewrite-sim](https://github.com/antirez/redis-cp-rewrite-sim)

###  项目简介（一句话）

> 这是一个 内部模拟项目，由 Redis 作者 Antirez（Salvatore Sanfilippo）编写，用于模拟 Raft 共识算法 + Redis 快照机制，研究随机化快照策略如何影响系统的可用性与容错能力。

###  核心目的

- 模拟一个基于 Raft 一致性算法的分布式 Redis 系统。
- 研究 “随机化快照”（randomized snapshotting） 策略：
  - 不是定期做快照，而是以某种概率或条件随机触发快照
  - 目的是减少所有节点同时做快照带来的资源竞争和可用性下降
- 分析这种策略对系统：
  - 可用性（Availability）
  - 恢复速度（Recovery Time）
  - 网络与磁盘负载

的影响。


###  技术特点

| 特性 | 说明 |
|------|------|
|  编程语言 | 纯 C 语言（ANSI C），轻量高效 |
|  编译要求 | 必须使用 `-O2` 优化编译，否则性能极慢：<br>`gcc -O2 *.c -o sim` |
|  功能模块 | - 模拟 Raft 节点（Leader/Follower）<br>- 日志复制（Log Replication）<br>- 快照生成与加载（Snapshotting）<br>- 网络分区、节点故障模拟 |
|  可配置性 | 所有参数（如节点数、快照概率、网络延迟等）都在 C 源文件中，直接修改代码即可调整 |
|  输出结果 | 打印系统状态、选举次数、快照次数、不可用时间等统计信息 |

###  如何使用？

1. 克隆项目
   ```bash
   git clone https://github.com/antirez/redis-cp-rewrite-sim.git
   ```

2. 编译（必须加 -O2）
   ```bash
   cd redis-cp-rewrite-sim
   gcc -O2 *.c -o sim
   ```

3. 运行
   ```bash
   ./sim
   ```

4. 修改参数
   - 打开 `*.c` 文件（如 `main.c` 或 `simulation.c`）
   - 修改顶部的宏定义，例如：
     ```c
     #define NODES 5
     #define SNAPSHOT_PROBABILITY 0.1  // 10% 概率触发快照
     #define FAILURE_RATE 0.01
     ```
   - 重新编译运行


###  为什么重要？（背景）

在分布式系统中：
- 快照（Snapshotting） 是为了减少日志体积，加快恢复。
- 但如果所有节点同时做快照，会导致：
  - CPU、磁盘、内存瞬间飙高
  - 节点变慢甚至超时，引发不必要的主从切换（Leader Election）
  - 降低系统可用性

随机化快照 就是让每个节点独立决定何时做快照，避免“雪崩效应”，提升整体稳定性。

这个项目就是用来验证这个想法是否有效。

###  适合谁看？

- 分布式系统学习者
- Raft 算法研究者
- Redis 深度用户
- 想了解“模拟实验”如何用于系统设计决策的人


###  总结

| 项目 | 说明 |
|------|------|
| 类型 | 分布式系统模拟器（非生产代码） |
| 作者 | Antirez（Redis 作者） |
| 核心 | 模拟 Raft + Redis 快照机制 |
| 创新点 | 探索“随机化快照”对可用性的影响 |
| 使用方式 | 修改 C 文件参数 → `-O2` 编译 → 运行观察输出 |


>  一句话总结：  
> 这是一个“纸上演算”的代码版，用 C 写了一个微型分布式 Redis，专门用来测试“错峰做快照”能不能让系统更稳定。

如果你感兴趣，我也可以帮你：
- 解读源码结构
- 添加中文注释
- 将输出结果导出为 CSV 做图表分析
