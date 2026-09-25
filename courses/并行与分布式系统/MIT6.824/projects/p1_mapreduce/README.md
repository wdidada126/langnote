# P1 MapReduce（进程内 master/worker 模拟）

> 对应讲次：L01（RPC 语义）、L02（MapReduce 论文）；对应 Lab：6.824 pg1。

## 这个项目在演示什么

| 论文/讲义概念 | 代码位置 |
|---|---|
| map/reduce 用户函数抽象（§2） | `main.go: wcMap/wcReduce`，`mapreduce.SetMapF/SetReduceF` |
| master 任务状态机（waiting/inprogress/done） | `mapreduce/master.go: task/Master` |
| RPC + 超时（L01 at-most-once 的现实困境） | `mapreduce/rpc.go: Call/SetDown` |
| 心跳超时 → 任务回收重做（§2.4/2.5） | `Master.checkTimeouts`（`crashAfter` worker 宕机触发） |
| 备份任务对付 straggler（§3） | `Master.maybeBackupStragglers` + `BackupWatch` |
| 幂等发布：临时文件 + rename 原子替换（§2.4 "reduces 原子的秘密"） | `writeKVFile`、`mapPartitionFile` |
| reduce 依赖全部 map 完成 | `acquireReduceTask` 的门控循环 |
| 正确性校验 = 与单机基准对比 | `main.go: referenceCount/readOutput` |

## 架构

单进程内：1 个 Master（被互斥锁保护的"服务端"）+ 5 个 worker goroutine，
worker 通过 `Call()`（带 300ms 超时的进程内 RPC 模拟）领取/上报任务。
两个 worker 被设定在运行中途"宕机"（goroutine 直接退出）——
master 观察不到心跳即回收其 in-progress 任务，由存活 worker 重做。
输入 6 文件、reduce 分区 3。运行结束打印：完成、重做数、备份数、与单机词频对照的 mismatch 数。

```
p1_mapreduce/
├── go.mod                # 仅模块名 + go 版本，零外部依赖
├── main.go               # 驱动剧本：造数据 → 起集群 → 注故障 → 校验
├── mapreduce/
│   ├── rpc.go            # 进程内 RPC（超时/宕机模拟）
│   ├── master.go         # 调度器：任务状态机、超时回收、备份派发、统计
│   └── worker.go         # map/reduce 执行、分区、临时文件 + rename 发布
└── build.bat / build.sh
```

## 如何构建运行（需本机 Go 工具链，本轮未编译）

```sh
cd projects/p1_mapreduce
go build ./...     # 或 go run .
```

Windows 用 `build.bat`，类 Unix 用 `./build.sh`。

## 与原版 Lab 的差距（有意简化）

1. 无跨进程网络（`net/rpc`/gorilla）——机制用锁 + goroutine 等价表达；
2. map 函数不经 RPC 注册传输（同进程直接共享闭包）；
3. 无 `WithLock/kill` 式"任务执行中崩溃后旧输出文件清理"（重做者用同名
   分区文件覆盖写 + rename，最终一致）；
4. master 不做故障转移（论文原样：master 挂 = 作业重跑）。

## 延伸思考

- 若两个备份 reduce 实例同时到达 `writeKVFile` 的 rename，会怎样？（幂等发布）
- `checkTimeouts` 为什么必须"每次可能改变状态的操作前"都调用？（惰性回收）
- pg1 challenge：worker 崩溃时 master 如何知道它已完成的 map 是否可信？
  （本实现：Done 只在 rename 后由 worker 上报，崩溃者上报丢失 → 重做，与论文一致。）
