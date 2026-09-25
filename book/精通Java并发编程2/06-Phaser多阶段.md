# 第 6 章 运行分为多阶段的任务：Phaser 类

> `Phaser`（JDK 7 引入）分阶段屏障：比 `CyclicBarrier` 更灵活（可动态注册/注销 partie、分层 `Tier`）。与艺术 8 章、之美 10 章互补，本书重「分层 Phaser 做树状阶段」。

## 一、本章地图

| 主题 | 关键 |
| --- | --- |
| 阶段屏障 | `arriveAndAwaitAdvance` |
| 动态 partie | `register`/`bulkRegister`/`arriveAndDeregister` |
| 分层 | `Tier` 父子 Phaser 减竞争 |
| 终止 | `onAdvance` 钩子 |

## 二、核心精讲

### 2.1 🔧 Phaser vs CyclicBarrier
- `CyclicBarrier`：固定 partie 数、可重用的代际屏障，无返回值、异常传播弱（🔧 与 `Lock`+`Condition` 实现相关，见之美 10 章）。
- `Phaser`：partie 数**动态**、阶段数任意、可分层（🔧 适合「任务数运行时才确定」或「树状多阶段」）。

### 2.2 分层（Tier）
- 父子 Phaser：子阶段到达后汇总到父，降低单点 `AtomicLong`/`Lock` 竞争（🔧 大并发多阶段首选）。

## 三、版本演进 / 论文 / 前沿

- 论文：Lea Phaser 设计（JDK 7 `java.util.concurrent`）；屏障原语源自 Dijkstra 1975「terminator」问题。
- 工业界：ForkJoin 的 `Phaser` 常与 `RecursiveTask` 配合做分阶段归约。

## 四、常见误区 / 本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "多阶段用 CyclicBarrier" | partie 动态改 Phaser |
| 2 | "Phaser 不用分层" | 大并发用 Tier 降竞争 |
| 3 | "屏障异常自动传播" | 需 onAdvance/包异常 |
