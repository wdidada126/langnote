# 第 12 章 CAP 理论：误解、PACELC 与分布式锁

> 原书第 12 章（P189–195），对应 12.1「CAP 理论的误解」、12.2「现实世界不存在'强一致性'（PACELC 理论）」、12.3「典型案例：分布式锁」。
> 这一章是原书对前两章（第 10、11 章）的**收尾与纠偏**：当你理解了共识算法的复杂度，接下来要回答的问题是——**我们真的需要那个 C 吗？**

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 12.1 CAP 理论的误解 | 常见的三种误读：三选二、C/A 是开关、分区故障 = 停机 | CAP 只在**分区发生时**才有取舍；不分区时 C 与 A 可以同时满足 |
| 12.2 现实世界不存在"强一致性"（PACELC） | 引入 PACELC：除了 P，还要看 E（延迟）与 L（一致性） | 取舍不是二元的，是**多维的连续谱**；延迟是真正的隐形约束 |
| 12.3 典型案例：分布式锁 | Redis/Redis Lock / ZooKeeper / etcd 三种锁与 Redlock 争议 | 分布式锁的正确性靠 **fencing token**，不是靠"加锁成功"这句话 |

## 核心精讲

> ⚠️ 以下为**教学示意，不参与构建**，用于说明概念结构，不含任何可直接运行的实现。

### 12.1 CAP 理论的误解

原书指出最常见的三种误读，逐一澄清：

**误解一：「CAP 是三选二，必须舍弃一个」。**
CAP 的真实命题（Gilbert & Lynch 形式化）是：**在异步网络模型下，无法实现一个既能读能写（A）又保证读取到最新值（C）的数据存储，如果它还允许任意分区（P）**。注意前提：

- **P 不是你选的**。可能分区的网络是既成事实，CAP 讨论的是「一旦发生分区，你要保 C 还是保 A」；
- 在**没有分区**（绝大多数时间）时，C 与 A 可以同时满足，系统应当**同时提供**强一致与高可用 —— 这恰恰是「误解」最贵的代价：为了迁就一个每天 occurrence 不足 0.1% 的故障，牺牲常态下的强一致。

**误解二：「C 就是 ACID 的 C」。**
两个不同层面的东西：

| | ACID 的 C | CAP 的 C |
| --- | --- | --- |
| 含义 | 事务结束后状态正确（约束不被破坏） | 读到的值是最新的（线性一致） |
| 关注点 | 单个事务内的不变式 | 跨节点副本之间 |
| 典型反例 | 转账后总额对不上 | 读到了旧副本的值 |

**误解三：「A 就是系统不挂」。**
CAP 的 A 是**每个非故障节点都能在有限时间内响应**（不保证返回的是正确结果）。返回一个过期的、带明显提示的降级结果，**不违反 CAP 的 A，但违反了「用户感知上的可用」** —— 这个落差是很多线上事故的解释来源。

教学示意（伪码，非可运行）：

```
// 「分区时保 C」的典型写法：宁可拒绝服务
if (quorum_unavailable && must_be_consistent) {
    return Error("service unavailable");   // 分区期间 A 被牺牲
}
```

### 12.2 「现实世界不存在强一致性」与 PACELC

原书用「现实世界不存在强一致性」作 12.2 的小标题，表达的是：**人们口中的强一致，在真实延迟预算下几乎总是被偷偷换成了最终一致**。

Daniel Abadi 提出的 **PACELC** 把这个洞补上了：

```
If there is a Partition: choose Availability or Consistency
Else (normal operation): choose Latency or Consistency
```

- **P/A/C** 与 CAP 同源；
- **E**（Else，无分区时的常态）与 **L**（Latency）；即：**正常运行时，你在用「延迟」换「一致性」**——等一个强一致副本的确认要花 5ms，等三个跨机房副本的确认要花 50ms，那 5ms 换来的就是「一致性稍弱或副本数更少」。

由此可得三条工程结论（原书隐含但值得写清楚）：

1. **不要问"我们系统是什么 CAP 类型"，要问"这个读接口在什么延迟下能达到什么一致性"**；
2. **一致性配置文件要按操作分级**：扣款要线性一致，商品详情页可以 200ms 陈旧，搜索索引可以秒级陈旧；
3. **权衡要落在代码里**：`Read-your-writes`、`Monotonic reads`、`Bounded staleness` 这些细粒度语义，比一个笼统的 "CA/CP" 标签有用得多。

**一个可落地的取舍模板**（教学示意，非规范）：

| 业务操作 | 一致性要求 | 延迟预算 | 允许的最大陈旧 | 实现方式 |
| --- | --- | --- | --- | --- |
| 扣款/下单 | 线性一致 | < 200ms | 0 | 主库 + 强一致读，分区时降级为「拒绝」 |
| 库存扣减 | 串行化 | < 100ms | 0 | 行锁 / CAS + 幂等 |
| 订单详情 | 因果一致性 | < 50ms | ≤ 2s | 从库 / 本地缓存，可接受短暂陈旧 |
| 商品列表 | 最终一致 | < 50ms | ≤ 10s | 搜索引擎 / 预聚合 |
| 报表统计 | Eventually + Exactly-once | 分钟级 | ≤ 15min | CDC → 数仓，对账兜底 |

这张表就是 PACELC 的工程化：它把「系统级标签」拆成了「操作级参数」，也让 14 章的**非功能性需求分析**有了可填写的格子。

### 12.3 典型案例：分布式锁

原书用分布式锁具体化 CAP 取舍。三种实现路径：

| 实现 | 机制 | 一致性来源 | 代价 |
| --- | --- | --- | --- |
| Redis 单机/主从 | `SET key v NX PX 30000` | 单点，主从切换可能丢锁 | 切换瞬间可能双锁 |
| ZooKeeper | 临时节点 + `EphemeralSequential` 顺序最小者持锁 | zxid 顺序 + 临时节点会话绑定 | 写性能低（每次写要多数派落盘） |
| etcd | `txn` 事务 + lease/compare-and-swap | Raft 日志顺序 + lease | 同样需要多数派 |

性能排序（粗）：Redis > etcd ≈ ZooKeeper；一致性强度：etcd ≈ ZooKeeper > Redis。

教学示意（伪码，非可运行）：

```
// 非原子地"检查并加"是错的
if (redis.get(lock) == null) { redis.set(lock); }   // 竞态窗口

// 正确形态：原子 + 超时
ok = redis.set(lock, uuid, NX, PX=ttl)
if (!ok) return false
try { doWork() } finally { release_if_owner(uuid) }
```

**释放锁的陷阱**：超时后可能业务还没跑完，锁已经被别人拿走 → 释放了别人的锁。**解法是 fencing token / 校验 owner**，而不是把 TTL 调大：

```
doWork(fencingToken) {
   storage.write(cmd, token)   // 存储层拒绝比当前 token 旧的写
}
```

#### 🔧 Redlock 的争议（2019 年集中爆发，2026 年的结论）

原书写作于 2019 年上半年，此时 **Redlock** 已被大量采用，原书对它的评价基本是正面/中性的。而 2017–2019 年发生的事情值得补记：

- Martin Kleppmann 在 2017 年撰文质疑 Redlock 在时钟漂移与异步模型下的安全性；
- Salvatore Antirez（Redis 作者）在 2019 年 4 月发布《Redlock analysis》逐条回应，认为在合理假设下可用；
- 结论分歧的本质：Redlock 的安全性依赖**对时钟漂移的上界假设**，而「时钟可信」本身就是 CAP 里最不该免费假设的东西。

2026 年的工程结论（比 2019 年清晰得多）：

1. **Redis 官方在 2024 年更新的分布式锁文档中已不再推荐 Redlock**，改为建议考虑单实例锁 + fencing token，或改用具备更强一致性保证的协调服务（etcd / ZooKeeper）；
2. 若必须用 Redis 做锁，**必须实现 fencing token 并在存储层校验**，否则「加锁成功」只代表「此刻没人加过」，不代表接下来安全；
3. 更现代的做法是**根本不用分布式锁**：用数据库唯一约束、乐观锁版本号、CAS + 幂等接口替代，把「互斥」降级为「幂等」。

## 版本演进

| 年份 | 事件 |
| --- | --- |
| 1988 | Birman 等的工作与 primary-copy 协议已隐含 CAP 式取舍 |
| 1998 | Gilbert 与 Lynch 给出 CAP 的形式化（后以 SIGACT News 2002 论文广为流传） |
| 2000 | Eric Brewer 在分布式计算原理研讨会（PODC）的 keynote 提出 CAP「猜想」，用于解释浏览器一致性取舍 |
| 2002 | Gilbert & Lynch《Brewer's Conjecture and the Feasibility of Consistent, Available, Partition-tolerant Web Services》—— CAP 成为定理 |
| 2012 | Brewer 本人撰文澄清 CAP 的意涵（"CAP Twelve Years Later: How the 'Rules' Have Changed"），明确「不分区时无取舍」；Abadi 提出 PACELC |
| 2012 | Gilbert & Lynch《Perspectives on the CAP Theorem》IEEE Computer |
| 2017–2019 | 分布式锁安全性的公开争论（Kleppmann ⟷ Antirez） |
| 2020 | Jepsen 对 etcd、CockroachDB 的线性一致性检验，把「CAP 取舍」变成可实测的对象 |
| 2023 | CAP 出现「再评估」的讨论（如 Abadi 与 Kingsbury 关于 CAP 表述严谨性的往复），社区更强调「一致性是连续谱」 |
| 2024 | Redis 官方分布式锁文档改写，撤回 Redlock 推荐 |

## 经典论文与原始文献

| 文献 | 出处 | 贡献 |
| --- | --- | --- |
| Gilbert & Lynch《Brewer's Conjecture and the Feasibility of Consistent, Available, Partition-tolerant Web Services》 | ACM SIGACT News, 2002 | CAP 的异步模型形式化证明：不存在同时满足 C/A/P 的原子读写寄存器 |
| Brewer《CAP Twelve Years Later: How the 'Rules' Have Changed》 | 2012（原为 PODC 2000 keynote） | 澄清 CAP 常被误读；提出 P 是既成事实、无分区时无取舍 |
| Gilbert & Lynch《Perspectives on the CAP Theorem》 | IEEE Computer, 2012 | 从研究视角评述 CAP 的适用边界与常见误解 |
| Abadi《PACELC: A Better Endpoint to the CAP Criterion》 | 博客 dbms.blogspot.com, 2012 | 补上「无分区时的延迟 vs 一致性」这一维 |
| Kleppmann《How to do distributed locking》 | 2017 及后续修订（含 2019 对 Redlock 的回应） | 分布式锁的正确用法与 fencing token |
| Antirez《Redlock analysis》 | antirez.com, 2019 | Redis 作者对 Redlock 安全性的逐条论证 |
| Kingsbury《Jepsen: A Framework for Distributed System Verification》及 etcd 检验博客 | jepsen.io, 2020 | 实测视角：CAP 中的 C 必须在实现中验证，不能凭论文 |

## 近年研究与工业界开源实践（2015–2026）

- **一致性检验成为标配**：`jepsen-io/jepsen`（≈7.5k★）及其线性一致性检查器被工业界定期用于审计；`pingcap/tidb`（≈40.6k★）、`cockroachdb/cockroach`（≈32.5k★）、`etcd-io/etcd`（≈52.3k★）都接受过 Jepsen 检验。结论是：CAP 的 C 是**可测量的属性**，不是一个标签。
- **细粒度一致性等级落地**：CockroachDB 的 `TRANSACTIONAL`/`SERIALIZABLE`、`TiDB` 的强一致读 / follower read / stale read、MongoDB 的 `readConcern` + `writeConcern`，本质都是把 12.2 的「连续谱」变成 API。
- **Coordinated Omission 与实测方法论**：Jepsen 在测试中暴露的「协调遗漏」问题说明：只测吞吐/延迟平均值会掩盖故障期行为，验证必须包含故障注入。
- **分布式锁的现代实践**：Redis 官方 2024 年文档建议避免 Redlock 并用 fencing token；`redis/redis`（≈76.5k★）生态里主流写法是 `SET NX PX` + owner 校验 + token；ZooKeeper 的 `apache/zookeeper`（≈12.8k★）仍以 `apache/curator` 的 `InterProcessMutex` 提供「教科书式」的锁；`etcd-io/etcd` 上用 `txn` + lease 实现锁也很常见。
- **客户端生态佐证**：`redis/node-redis`（≈17.6k★）、`redis/go-redis`（≈22.2k★）均已提供 `SET NX PX` 与 token 化锁的封装，说明「原子加锁 + 校验 owner」已成为默认最佳实践。
- **对 CAP 表述的再讨论**：2023 年前后 Abadi 与 Kingsbury 关于「CAP 公式是否准确」的公开往复，进一步推动社区从「CAP 三选二」转向「一致性/延迟/可用性三维权衡 + 分区时的行为」。

## 常见误区与本书需修正之处

| # | 误区 | 修正（含 2026 视角） |
| --- | --- | --- |
| 1 | "CAP 三选二" | 正确表述：分区时要在 C 与 A 之间选；**无分区时两者可以兼得**。Brewer 本人 2012 年已明确澄清 |
| 2 | "我们系统是 CP/AP，所以已经解决了" | 系统不同部分可以取不同策略：支付是 CP，商品详情是 AP。按**操作**分级而非按**系统**分类 |
| 3 | "A = 不挂 = 用户能操作" | CAP 的 A 只保证「非故障节点在有限时间内有响应」，不保证响应**有用**；返回错误不违反 CAP，却违反用户体验 |
| 4 | "CAP 的 C = 事务一致性" | CAP 的 C 是**线性一致（跨副本的即时可见）**，与 ACID 的 C 不是一回事；Serializable 与 Linearizable 也不能混用 |
| 5 | 🔧 本书对 Redlock 的立场需要更新 | 2024 年 Redis 官方文档已**撤回 Redlock 推荐**；今天的说法是「若用 Redis 锁，至少要有 fencing token；否则优先用 etcd/ZooKeeper 或数据库唯一约束」 |
| 6 | 🔧 本书未覆盖 Jepsen 实测结论 | 2020 年 Jepsen 对 etcd 的检验发现 leader lease 相关实现存在线性一致性违反。结论：CAP 的 C 要**实测**，算法正确不等于实现正确 |
| 7 | 🔧 本书未覆盖 PACELC 之后的「延迟一致性曲线」 | 今天的追问是「p99 延迟下的一致性窗口是多少」，可用 Jepsen 的 `knossos`/`porcupine` 与业务侧的「陈旧读监控」共同度量 |
| 8 | 🔧 本书未覆盖「客户端可见性语义」 | `Read-your-writes` / `Monotonic Read` / `Bounded Staleness` 才是真正该写进需求的一致性规格，而不是"CAP 类型" |

## 与其他章 / 其他书的联系

- **第 11 章 多副本一致性**（`11-多副本一致性.md`）：Raft/Paxos/Zab 全部是 CP 取向（分区时保 C 并牺牲部分可用）；本章告诉你**这个取舍是否值得**。
- **第 10 章 事务一致性**（`10-事务一致性.md`）：柔性事务是「牺牲 C 换 A」的具体手法；2PC 是分区/宕机时保 C 的最强但也最阻塞的做法。
- **第 6 章 6.4 事务与锁**：单机隔离级别是 CAP 中 C 的最内层实现；隔离级别放松（RC/RR）与 CAP 的取舍同构。
- **第 9 章 高可用与稳定性**：限流、熔断、降级本质上就是在**主动制造分区**（对部分请求降级），从而把 CAP 的取舍变成可调的旋钮。
- **第 13、14 章**：一致性等级是**非功能性需求**的一种，必须在需求阶段由业务方参与定义，不能由技术方单方面决定。
- `book/数据库系统概念6/26-高级事务处理.md`：串行化与更强隔离的实现路径，可与「线性一致」对照。
- `book/多处理器编程的艺术2/03-并发对象与可线性化.md`：可线性化的精确定义与历史，是 CAP 中 C 的形式化底座。
- `book/C++并发编程实战2/05-Cpp内存模型与原子操作.md`：单机内存序与「可见性」的含义，帮助区分「缓存可见性」与「跨节点线性一致」。
