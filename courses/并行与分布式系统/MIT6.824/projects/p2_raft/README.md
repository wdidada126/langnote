# P2 Raft 简化核心（选举 + 日志复制）

> 对应讲次：L05（选举/复制）、L06（安全性/持久化伏笔）、L08（Paxos 对照）；对应 Lab：6.824 pg2（2A+2B 范围）。

## 实现了什么 / 有意没实现什么

| 机制 | 状态 | 讲义出处 |
|---|---|---|
| term + 投票一次 + 随机选举超时 | ✅ `raft.go: becomeCandidate` | L05 §2.2 |
| 选举限制（只投"日志不比自己旧"者） | ✅ `handleRequestVote` upToDate | L05 §2.2 / L06 §1 |
| AppendEntries 一致性检查 + nextIndex-- 回退 | ✅ `handleAppendEntries` | L05 §2.3（§3.3 低效版） |
| 只直接提交当前 term 条目 + 新 leader Noop | ✅ `tryAdvanceCommit` / `becomeLeader` | L06 图 4.3 |
| 状态机有序交付（applyCh） | ✅ `applyLoop` + Recorder | lab2B |
| 持久化接口 | 🔶 `StateStorage`（内存实现；FileStorage 留作 pg3 练习） | L06 §2 |
| 快照/日志压缩 | ❌ | L06 §2 |
| 成员变更（Joint Consensus） | ❌ | L06 §3 |
| 快速回退提示（NextIndex/NextRole） | ❌ | Raft §3.3 优化 |
| PreVote / Lease Read | ❌（P3 讨论） | L06 §4 |

## 架构

- `raft/raft.go`：Raft 节点全部状态机逻辑（锁内毫秒级操作，绝不持锁做 RPC——
  这是 lab 里 "deadlock" 系列测试的灵魂教训）。
- `raft/transport.go`：进程内"网络"：随机延迟、概率丢包、Kill/Recover；
  `Cluster` 组装 5 节点并附 `Recorder`（模拟状态机，记录交付序）。
- `raft/persist.go`：`StateStorage` 抽象（pg3 的边界：在这里插磁盘）。
- `main.go`：演示剧本——选举 → 30 条提交 → 杀 leader → 新 leader 续 30 条 →
  校验"应用前缀全一致"安全性不变量。
- `tests/raft_test.go`：四个多节点测试（思想源自 lab 的 go-test）：
  1. `TestBasicElection` 唯一 leader + 崩溃重选 + term 递增；
  2. `TestReplicationAgreement` 50 条 × 5% 丢包，前缀一致/有序/无重复；
  3. `TestReElectionKeepsCommitted` leader 崩溃不丢已提交（选举限制的实证）；
  4. `TestMinorityCannotCommit` 少数派侧禁止推进 commit（防脑裂决断）。

## 如何构建运行（需本机 Go 工具链，本轮未编译）

```sh
cd projects/p2_raft
go build ./...
go test ./tests/ -v -count=1     # 混沌测试有随机性，偶发慢，-count=1 防缓存
go run .                          # 演示剧本
```

Windows 用 `build.bat`。

## 值得停下来想的三件事

1. **为什么 RPC 处理函数必须"先查 term 再动状态"？**（旧 leader 幽灵，L05 §2.1/§2.9）
2. **applyLoop 为什么不能持锁发 applyCh？**（状态机慢 → Raft 心跳停 → 集群抖，
   对应 lab 里"apply hook 阻塞死锁"的坑）
3. **`tryAdvanceCommit` 为什么跳过旧 term 条目？**（图 4.3 反例：旧 term 多数派
   可能是"过期视图"的多数派。）
