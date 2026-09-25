# MIT 6.5840/6.824 配套项目总表

> 语言：Go（**仅标准库**）。三个渐进项目对应课程三大经典 Lab 思想。
> 约定：本轮"只写不编译"；每个项目自带 `build.bat`（Windows）与 `build.sh`（类 Unix），
> 内容为 `go build ./...`，需本机安装 Go 工具链后自行执行。
> `go.mod` 仅含模块名与 go 版本，零外部依赖；P3 内的 `lraft/` 为 P2 内核的包内复制
> （课程原版做法：lab2 的 raft 包整包拷进 lab3）。

| 项目 | 对应 Lab / 讲次 | 内容 | 验证方式 | 状态 |
|---|---|---|---|---|
| [`p1_mapreduce/`](p1_mapreduce/) | pg1 · L01/L02 | master/worker 任务状态机；心跳超时回收重做；straggler 备份任务；临时文件+rename 幂等发布；进程内 RPC（带超时）模拟 | `go run .`：注入 2 个 worker 宕机跑 wordcount，与单机基准比对全部词频 | 完成（未编译） |
| [`p2_raft/`](p2_raft/) | pg2(2A+2B) · L05/L06/L08 | 选举（term/投票一次/选举限制）+ 日志复制（一致性检查+回退）+ 仅当前 term 直接提交 + Noop + applyCh 有序交付；进程内网络（延迟/丢包/Kill） | `go test ./tests/`：4 个混沌测试（唯一 leader、50 条全序一致无重复、崩溃不丢已提交、少数派禁 commit）+ `go run .` 演示 | 完成（未编译） |
| [`p3_kvraft/`](p3_kvraft/) | pg2/pg3 思想 · L01/L05/L06/L09/L10 | Raft 之上复制状态机：Put/Append/Get；客户端 (clientID,requestID) 去重凑 at-most-once；主存感知重试；"命令被覆盖不得假报成功"修复；线性一致读方案（ReadIndex/LeaseRead）文档化 | `go test ./tests/`：语义/并发/leader 接管/去重 4 组 + `go run .` 杀 leader+follower 剧本 | 完成（未编译） |

## 三项目的进阶主线（与讲义同构）

```
P1 性能与容错的最小闭环：并行 = 切分 + 重做（无共识）
      ↓  单 master 的"可靠"是假的（master 挂 = 作业重跑）
P2 把"顺序"变成共识问题：多数派 + 选举限制 + 安全性不变量
      ↓  Raft 组 = 一条全序命令日志
P3 把日志变成服务：状态机收敛 + 客户端幂等 + 读一致性档位
      →  再往前就是 pg3（持久化+快照）、pg4（分片+主迁移）——README 中列出差距
```

## 已知简化（诚实清单）

- 无跨进程网络：RPC 以进程内调用 + 超时模拟等价表达；
- 无 gob/序列化层：参数经闭包/接口直传；
- P2 无 fast log backoff hints、无 PreVote、无快照与成员变更（README 标注对应讲义章节）;
- P3 不回收去重表、不分片、不持久化（接口已留）。
