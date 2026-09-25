# P3 容错分布式 KV（Raft 状态机 + Put/Append/Get + 幂等客户端）

> 对应讲次：L05/L06（内核）、L01（RPC 语义闭环）、L09/L10（故障与一致性）；
> 对应 Lab：6.824 pg2 完整体 + pg3 思想（持久化为接口占位）。

## 架构

```
p3_kvraft/
├── go.mod               # 仅模块名 + go 版本（lraft 为包内复制，非外部依赖）
├── main.go              # 演示剧本：杀 leader/ follower，校验副本一致
├── lraft/               # ★ P2 的 Raft 内核整包复制（课程同款做法：
│   ...                  #    6.824 学生就是把 lab2 的 raft 包 copy 进 lab3）
├── kv/
│   ├── common.go        # Request/Response/Command 协议
│   ├── server.go        # Raft → 状态机 applier + 去重表 + KVCluster
│   └── client.go        # Clerk：超时重试 + (clientID,requestID) 去重 + 主存感知
├── tests/kv_test.go     # 语义/并发/leader 接管/去重 四组多节点测试
└── build.bat / build.sh
```

数据通路：`Clerk.request → leader.Handler → Raft.Start（日志）→ 多数派提交 →
applier 执行进 map + 记入 dup 表 → applied 索引推进 → Handler 返回`。

## 每个模块对应的讲义知识点

| 机制 | 讲义出处 |
|---|---|
| 读也走一遍 Raft（朴素线性一致读） | L10（线性一致定义）、L06 §4 |
| clientID+requestID 去重 = at-most-once | L01（RPC 语义）、L05 §3（客户端交互） |
| 主存感知（先问上次 leader） | L01 绑定策略、pg4 的 config 查询前身 |
| 提交前缀 = 全序命令日志 → 副本确定性收敛 | L05 复制状态机、L14（WAL 重放视角） |
| "命令被新 leader 覆盖则不得假报成功" | kvraft 经典 bug（L09 面向故障） |
| Kill leader 后客户端自动切换 | L05 选举 + L09 超时重试幂等三件套 |

## 与原版 pg3/pg4 的差距（有意留白）

1. **单 Raft 组、不分片**：pg4 要求按 key 分多个 shard（每 shard 一个 Raft 组）
   + 客户端 config 协议 + 主迁移；本实现单组跑通全 key（README 见 papers 对照 L13/TiKV region）。
2. **无持久化**：`lraft.StateStorage` 已留出 pg3 插槽；加一个 gob 文件实现即成"可重启集群"。
3. **无快照**：日志无限增长（pg3 核心）；L06 §2 讲了设计。
4. **去重表不回收**：生产系统需要"视图号/配置号"限制重放窗口（pg4 的 trick：
   命令里带主编号，新主截断旧主的未提交尾巴，README 见 CockroachDB 事务重试类比）。
5. **串行 Handler**：原版 pg4 要求并发处理（`Start` 后立刻释放锁等待应用）；
   本实现 `Handler` 内部已是"Start 快速返回 + 轮询 applied"，天然可并发调用。

## 线性izable read 说明（题目要求的"可选"项）

当前 Get 走完整 Raft 提交 → **线性一致但每个读 = 一次多数派往返**。
两条优化路线（均未实现，论文与工程见下）：

1. **ReadIndex**（Raft §8 思路，etcd/TiKV/CockroachDB 生产使用）：
   leader 记下当前 commitIndex → 发一轮心跳证明"我仍是多数派认可的 leader" →
   直接以旧快照服务读，**免掉日志追加**。安全性：读到的是"开始证明时已提交"的状态。
2. **Lease Read**：leader 依据"心跳周期 + 时钟漂移上界 ε"推断 follower 选举超时
   不会触发（我仍安全在任）→ 连那一轮心跳都省。代价：依赖时钟假设——
   这正是 L15 TrueTime / L06 lease 讨论里"用物理时间换一次 RTT"的账。
3. 反面教材：**Dynamo/Redis 主从的"直接读本地副本"** = 可能读到过期值
   （L10 谱系滑向"单调读"甚至更弱；etcd 的 `serializable=true` 读是显式降级）。

## 如何构建运行（需本机 Go 工具链，本轮未编译）

```sh
cd projects/p3_kvraft
go build ./...
go test ./tests/ -v -count=1
go run .
```

Windows 用 `build.bat`。
