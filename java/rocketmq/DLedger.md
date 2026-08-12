# DLedger

上游仓库：<https://github.com/openmessaging/dledger>

一句话定义：`DLedger` 是一个基于 Raft 的 Java 复制日志库，用来构建高可用、高可靠、强一致的 `commitlog`/WAL 系统。RocketMQ 的 `DLedger CommitLog` 和 `Controller` 模式都建立在这个库之上。

## 1. DLedger 到底解决什么问题

如果只看论文，Raft 解决的是“多副本一致复制”；如果落到工程，DLedger 实际解决的是下面 4 件事：

1. 写请求只能由 Leader 接收，避免双主写入。
2. 日志必须复制到多数派后才算提交，避免主挂后数据回退。
3. 已提交日志按顺序回放到状态机，保证所有副本最终状态一致。
4. Leader 宕机后自动重选，业务层不必自己写主从切换逻辑。

这也是本仓库的设计核心：不把 DLedger 当“消息队列”，而是把它当“强一致复制日志底座”，然后在上面构建不同业务状态机。

## 2. 本仓库是怎么用 DLedger 的

本仓库不是 mock Raft，而是直接依赖 `io.openmessaging.storage:dledger:0.3.1.2`，分成 4 个 Maven 模块：

- `dledger-common`：命令信封、通用结果对象、编解码。
- `dledger-core`：嵌入式 3 节点集群、命令写入网关、状态机适配。
- `dledger-scenarios`：6 个业务场景的投影和服务层。
- `dledger-integration-tests`：真实启动 3 节点 DLedger，自测选举、复制、回放和读模型结果。

整体写入链路：

1. 业务命令进入 `ReplicatedCommandGateway.append(...)`。
2. DLedger 把命令追加到 Leader 日志，并复制到多数派。
3. 提交后的日志进入 `ReplicatedStateMachine.onApply(...)`。
4. 不同场景的 `ScenarioProjection` 把日志回放成可查询状态。

这套路径在代码里的关键入口是：

- `dledger-core/src/main/java/cn/wdidada/dledger/core/EmbeddedDLedgerCluster.java`
- `dledger-core/src/main/java/cn/wdidada/dledger/core/ReplicatedCommandGateway.java`
- `dledger-core/src/main/java/cn/wdidada/dledger/core/ReplicatedStateMachine.java`
- `dledger-integration-tests/src/test/java/cn/wdidada/dledger/integration/IndustrialScenariosIntegrationTest.java`

## 3. DLedger 核心特性和本仓库映射

| DLedger 特性 | 通俗解释 | 本仓库对应实现/测试 | 当前状态 |
| --- | --- | --- | --- |
| Leader election | 自动选主，保证同一时刻只有一个写主 | `EmbeddedDLedgerCluster.start(...)`、`awaitLeader(...)`，集成测试启动即触发选主 | 已覆盖 |
| Pre-vote protocol | 真正发起选举前先试探，减少抖动 | `mvn test` 日志里可看到 `WAIT_TO_VOTE_NEXT`、`REVOTE_IMMEDIATELY`、`PASSED` | 已覆盖 |
| Parallel log replication | Leader 并行向多个 Follower 推送日志 | 业务写入统一走 `ReplicatedCommandGateway.append(...)`，由 DLedger 并行复制 | 已覆盖 |
| Strong-consistent commitlog | 多数派确认后才提交 | 所有 6 个场景都依赖提交后再回放状态机 | 已覆盖 |
| State machine | 已提交日志顺序回放成业务状态 | `ReplicatedStateMachine.onApply(...)` + 各场景 `Projection` | 已覆盖 |
| Multi-Raft | 同一进程内可运行多个独立 Raft Group | 新增 `shouldIsolateMultipleRaftGroupsInSameJvm()` | 本次补齐 |
| High reliable storage | 文件型顺序存储/WAL | `DLedgerConfig.FILE`，测试真实落盘到 `target/dledger-it/...` | 已覆盖 |
| Preferred leader election | 优先让指定节点当 Leader | 当前样板未单独演示 | 未直接覆盖 |
| Asynchronous replication | 先本地成功再异步复制，偏性能 | 当前样板走默认强一致写入路径 | 未直接覆盖 |
| Symmetric/Asymmetric partition tolerance | 网络分区下只允许多数派继续写 | 当前仓库没有故障注入测试，但语义由 DLedger/Raft 保证 | 未直接覆盖 |
| Jepsen verification | 上游用故障注入验证一致性 | 这是 DLedger 上游能力，本仓库未复现实验 | 未直接覆盖 |
| Snapshot | 日志快照、加速恢复 | `onSnapshotSave(...)` 当前明确 `done.complete(false)` | 明确未实现 |
| Dynamic membership | 在线增删节点 | 当前样板未实现成员变更编排 | 未实现 |
| SSL/TLS | 复制通道加密 | 测试为了降低复杂度，启动时显式关闭 TLS | 明确未启用 |

## 4. 本仓库已经落地的 6 个业务场景

这些场景都不是“直接调 DLedger API 就结束”，而是完整走了“复制日志 -> 状态机回放 -> 只读投影”的工业化路径。

### 4.1 RocketMQ-like 有序消息队列

- 服务类：`dledger-scenarios/.../messagequeue/OrderedMessageService.java`
- 集成测试：`shouldReplicateRocketMqLikeOrderedMessages()`
- 关键点：
  - 同一 `topic + queueId` 严格顺序
  - `messageId` 幂等去重
  - 保留 `traceId/tag` 等消息头
  - 读接口按 `offset` 拉取

### 4.2 配置中心

- 服务类：`dledger-scenarios/.../config/ConfigurationService.java`
- 集成测试：`shouldApplyConfigCasAndDeleteFlow()`
- 关键点：
  - `expectedVersion` 做 CAS
  - 删除不是物理抹除，而是版本推进
  - 历史版本可追溯

### 4.3 审批工作流

- 服务类：`dledger-scenarios/.../workflow/WorkflowService.java`
- 集成测试：`shouldRunSequentialApprovalWorkflow()`
- 关键点：
  - 顺序审批链
  - 防并发越权审批
  - 全链路审计轨迹

### 4.4 分布式租约协调

- 服务类：`dledger-scenarios/.../lease/LeaseCoordinationService.java`
- 集成测试：`shouldCoordinateDistributedLeaseLifecycle()`
- 关键点：
  - 同一资源唯一持有者
  - `fencingToken` 防脑裂写
  - 续租和释放都有版本约束

### 4.5 分布式计数器

- 服务类：`dledger-scenarios/.../counter/DistributedCounterService.java`
- 集成测试：`shouldMaintainDistributedCounterState()`
- 关键点：
  - `INCREMENT/DECREMENT/SET`
  - 维度 + 桶聚合
  - `SET` 走版本校验

### 4.6 分布式限流

- 服务类：`dledger-scenarios/.../ratelimit/DistributedRateLimitService.java`
- 集成测试：`shouldApplyDistributedRateLimitRules()`
- 关键点：
  - `FIXED_WINDOW` 和 `TOKEN_BUCKET`
  - 规则版本化
  - 许可获取本身也经过复制日志，避免各节点局部判断不一致

## 5. 本次补齐的知识点：Multi-Raft

原来的项目已经覆盖了 Leader 选举、状态机回放、业务复制写入，但对 `Multi-Raft` 只有概念，没有一个显式可读的例子。

这次新增了：

- 测试方法：`IndustrialScenariosIntegrationTest.shouldIsolateMultipleRaftGroupsInSameJvm()`

测试做的事情非常直接：

1. 在同一个 JVM 里启动两个 3 节点 DLedger 集群。
2. Group A 叫 `industrial-dledger-group-a`。
3. Group B 叫 `industrial-dledger-group-b`。
4. 两个 Group 都写入同一逻辑键：`orders / shard-a`。
5. 最终断言：
   - Group A 的值是 `11`
   - Group B 的值是 `29`

这就证明了：

- 一个进程里可以跑多个独立的 Raft Group。
- Group 之间的日志、任期、Leader、状态机彼此隔离。
- 这类能力可以直接用于分片计数器、分区任务调度、分库分表元数据治理，不止 RocketMQ。

## 6. 关键代码怎么读

### 6.1 集群启动和选主

`EmbeddedDLedgerCluster.start(...)` 做了几件关键事：

- 为每个节点分配端口和 `selfId`
- 生成 `peers` 字符串
- 创建 `DLedgerServer`
- 注册 `ReplicatedStateMachine`
- `startup()` 全部节点
- `awaitLeader(Duration.ofSeconds(20))` 等待选主完成

这段代码说明：本仓库不是“单机假集群”，而是真实起了 3 个 DLedger 节点。

### 6.2 强一致写入口

`ReplicatedCommandGateway.append(...)` 是统一写入口：

- 把业务命令编码成 `CommandEnvelope`
- 调 `DLedgerClient.append(...)`
- 只有响应码是 `SUCCESS` 才认为写成功

这意味着业务层没有自己绕开 Raft 做本地写。

### 6.3 状态机回放

`ReplicatedStateMachine.onApply(...)` 的逻辑很重要：

- 按提交顺序迭代 `CommittedEntryIterator`
- 解码日志
- 根据 `scenario` 分发到对应 `Projection`
- 更新 `lastAppliedIndex`

所以这里不是“写完直接改内存”，而是“只有 committed log 才能改变业务状态”。

### 6.4 快照边界

当前样板刻意把快照状态说清楚，不做伪实现：

```java
@Override
public void onSnapshotSave(SnapshotWriter writer, CompletableFuture<Boolean> done) {
    done.complete(false);
}
```

这表示：

- 当前工程重点是复制日志与确定性状态机
- 不是快照演示工程
- 如果后续要支持长日志和快速恢复，需要补 snapshot 设计

## 7. 真实测试日志摘录

下面这些日志来自 2026-08-12 在本仓库执行的真实测试，不是伪造样例。

### 7.1 全量回归

执行：

```bash
mvn test
```

结果：

```text
[INFO] Tests run: 7, Failures: 0, Errors: 0, Skipped: 0
[INFO] dledger-integration-tests .......................... SUCCESS [ 39.835 s]
[INFO] BUILD SUCCESS
```

### 7.2 定向验证 Multi-Raft

执行：

```bash
mvn test -pl dledger-integration-tests -am -DfailIfNoTests=false \
  -Dtest=cn.wdidada.dledger.integration.IndustrialScenariosIntegrationTest#shouldIsolateMultipleRaftGroupsInSameJvm
```

结果：

```text
[INFO] Tests run: 1, Failures: 0, Errors: 0, Skipped: 0
[INFO] dledger-integration-tests .......................... SUCCESS [ 31.381 s]
[INFO] BUILD SUCCESS
```

### 7.3 选举与预投票日志

```text
[StateMaintainer] ... [PARSE_VOTE_RESULT] ... result=WAIT_TO_VOTE_NEXT
[StateMaintainer] ... n2_[INCREASE_TERM] from 0 to 1
[StateMaintainer] ... [PARSE_VOTE_RESULT] ... result=REVOTE_IMMEDIATELY
[StateMaintainer] ... [PARSE_VOTE_RESULT] ... result=PASSED
[StateMaintainer] ... [VOTE_RESULT] has been elected to be the leader in term 1
```

这几行正好对应 DLedger 文档里的几个核心概念：

- `WAIT_TO_VOTE_NEXT`：第一次试探投票没形成多数派，先等下一轮。
- `INCREASE_TERM`：任期递增，进入正式竞争。
- `REVOTE_IMMEDIATELY`：有节点任期未就绪，立即重试而不是长期卡住。
- `PASSED`：拿到多数票。
- `has been elected to be the leader in term 1`：Leader 选举完成。

## 8. RocketMQ 和 DLedger 的关系

这个点很容易被说错，单独拎出来：

1. RocketMQ 4.5.0 之前主流是传统主从复制，不是 Raft。
2. RocketMQ 4.5.0+ 通过 `DLedger CommitLog` 把消息存储复制切到 Raft 模式。
3. RocketMQ 5.x 还引入了 `Controller` 模式，用 DLedger 管理 Broker 元数据和主从切换。

所以准确说法是：

- RocketMQ 自己不是从零手写一套 Raft；
- 它是通过 DLedger 这套库获得生产级 Raft 能力。

## 9. 当前样板的边界

这份工程已经足够帮助理解 DLedger 的主路径，但边界也要讲清楚：

- 已直接演示：选主、预投票、强一致复制、状态机、多场景业务投影、Multi-Raft。
- 未直接演示：优先 Leader、异步复制、网络分区故障注入、Jepsen、动态成员变更。
- 明确未实现：Snapshot、TLS。

如果后续继续补，优先级建议是：

1. `Snapshot`：做长日志恢复演示。
2. `Preferred leader election`：让文档从“知道概念”变成“能跑用例”。
3. `Fault injection`：补网络分区/节点宕机实验，让对称/非对称分区不再停留在描述层。

## 10. 一句话总结

`DLedger` 在这个仓库里不是一个抽象概念，而是一套已经跑起来的强一致复制日志底座。当前代码已经用真实 3 节点集群演示了 6 个工业化业务场景，并通过新增 `Multi-Raft` 用例把 “一个进程内多个 Raft Group 隔离运行” 这个知识点补成了可以直接验证的工程事实。
