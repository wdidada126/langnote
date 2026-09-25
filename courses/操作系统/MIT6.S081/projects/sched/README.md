# sched — 多级反馈队列（MLFQ）调度器模拟器

对应讲次：**L01（进程抽象）**、**L02（并发/控制流）**（调度主题在 xv6 由 `proc.c: scheduler()` 一笔带过，
本课用 OSTEP 的 MLFQ 规则做一台"看得见的调度器"，与 xv6 默认时间片轮转对照）。

## 机制说明

- 5 级优先级队列，规则（Arpaci-Dusseau MLFQ）：
  1. 优先级高者先跑；同级 RR；
  2. 用完一个时间片仍活跃 → 降一级；
  3. 主动让出（IO 型进程）→ 保持原级（"interactive 保持"规则）；
  4. 每 `BOOST` 个 tick 全部拉回最高级（防饥饿/防刷级）；
  5. 时间片大小 = `BASE << 级别`（低优先级拿更长片，摊薄切换）。
- 进程模型：交替的 CPU 段/IO 段（LCG 确定性生成）；单核事件驱动模拟，输出甘特图
  与平均周转/响应时间，与 FIFO、纯 RR 基线对比。
- 与内核联系：xv6 `scheduler()` 就是"第 5 条都去掉"的裸 RR；Linux CFS 换成虚拟运行时间
  ——MLFQ 的"启发式 + 防作弊"演进史在 README 问题里让你亲手踩坑。

## 构建与运行

```sh
./build.sh   # cc -std=c11 -O2 -Wall -Wextra → sched_demo
```
```bat
build.bat    # cl /W3 /O2 → sched_demo.exe（Developer Command Prompt）
```

## 扩展练习
- 把 `demote-after-one-slice` 改成"累计 CPU 时间超阈值才降级"，观察对长作业吞吐的影响；
- 加一个"计算型进程伪装 IO"策略（CPU 段极短但从不真 IO），重现 MLFQ 的经典攻击；
- 与 `projects/locking` 的多核场景结合：每 CPU 一个队列 + 负载迁移。
