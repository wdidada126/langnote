# L24 去信任共识：Bitcoin 与 PBFT（附课程复盘）

> 阅读：Nakamoto, *Bitcoin: A Peer-to-Peer Electronic Cash System* (2008)；
> Castro & Liskov, *Practical Byzantine Fault Tolerance*, OSDI 1999
> 主线：把故障模型从"崩溃"升级到"说谎"——共识理论的最后一块拼图，也是全课收官。

## 1. 核心问题

- 此前 23 讲的隐含前提：**节点诚实（最多崩溃）**、成员已知且可鉴权、
  多数派可投票。公网上全部失效：
  1. **拜占庭故障**：节点可任意作恶（发假消息、伪造签名无效但消息格式合法）；
  2. **开放成员（permissionless）**：谁都能加入，Sybil 攻击 = 伪造一万个身份
     即可获得"多数派"。
- 问题定义：去信任网络里对"账本顺序"达成一致（双花 = 分布式一致性问题的金钱版）。

## 2. PBFT（1999）：联盟链的祖师

- 故障模型：**f 个拜占庭副本需 n ≥ 3f+1**（L05 的多数派推广：
  交集论证要应对"说谎的多数"）。
- 三阶段提交：**pre-prepare → prepare → commit**（视图 view 编号 = epoch/term，
  主节点作恶或失联 → 视图切换协议换主）——共识 + 锁 + checkpoint 的完整工业方案。
- 与 Paxos/Raft 的对比：多一轮消息复杂度（O(n²) 的 prepare 互验），
  换"任意 f 台说谎也不出错"；**联盟链（Hyperledger Fabric）至今用 PBFT/其变体**。
- 遗留问题：成员仍需可信名单（permissioned）→ 开放网络还得解决 Sybil。

## 3. Bitcoin（2008）：用经济重写共识

### 3.1 机制
- **UTXO 模型**：不存在"账户余额"，只有未花费输出；
  交易 = 解锁旧输出（脚本/签名）+ 创造新输出 → **双花 = 同一 UTXO 被两笔交易消耗**
  （对照：KV 里是同一 key 两个并发写）。
- **链 = 日志，最长链规则 = 共识选择器**：矿工把交易打包进区块，
  **工作量证明（PoW）**要求区块哈希满足难度前缀 → 追加一个区块 = 付出真金白银的算力。
- **概率性最终一致**：6 确认≈可认为不可逆；攻击需掌握 >50% 算力重排历史，
  成本 > 收益 → **共识安全性从"数学相交"换成"博弈均衡"**。
- Sybil 免疫：身份 = 算力（one-CPU-one-vote → one-hashpower-one-vote）。
### 3.2 系统视角的批判性阅读
- 它是**全球规模、拜占庭、异步**下的 RSM（L05）——但代价巨大：
  吞吐个位数 TPS（Raft/链式复制差 4–5 个数量级）、确认延迟分钟级、能耗。
- **Fork choice（分叉）= L19/L23 的反熵/调和 + L15 的外部一致性退化版**；
  Merkle 树 = L11 反熵的区块内版本； nonce/time = L07 时间的粗糙化身。
- 后续谱系：POS（权益替代算力，仍是"用成本反 Sybil"）、
  HotStuff/Tendermint（BFT + POS）、Layer2（闪电网络 = 把共识下推到链下，
  "别事事上链"≈"别事事强一致"的 L10 教训）。

## 4. 全课复盘：一张图收束 24 讲

```
                    ┌ 性能 ┐        ┌ 一致性 ┐
 并行抽象: MR(L02)→Spark(L17)→数据并行谱系(L18)   时间: Lamport/HLC/TrueTime(L07/L15)
 存储底座: GFS(L03)→Bigtable(L04)→S3/新硬件(L13)  定义: 线性一致谱系(L10)
 ─────────────────────────────────────────────
 容错哲学: 面向故障设计(L09) · FTW · 幂等/超时(RPC L01)
 共识谱系: Paxos(L08)=Raft(L05/06)=ZAB(L12)  CP 阵营
           CR/CRAQ(L19) 拓扑换共识 · FaRM(L22) 硬件换 RTT
           Dynamo(L11)/DHT(L23)/TAO(L21)      AP/最终一致阵营
           Bitcoin/PBFT(L24) 拜占庭阵营
 ─────────────────────────────────────────────
 汇聚: Spanner(L15)=时间+共识+事务 · Fabric(L20)/验证(L22) 单机与证明的边界
```
- 三条主线的答案：
  **可靠性**靠"复制 + 幂等 + 重算/日志恢复"；
  **性能**靠"分层 + 批量 + 并行 + 局部性"；
  **一致性**靠"共识或主动放弃它"。
- 永恒三角：**一致性—可用性—性能，没有免费午餐，只有显式取舍**。

## 5. 跨课程联系

- **自顶向下/CSAPP**：PoW 的哈希、p2p gossip 网络 = 应用层协议的极限压力测试。
- **15-445/15-721**：区块链数据库（Block-DB 论文）把 B 树 + PoW 缝合；
  UTXO vs 账户模型 = 两种存储引擎设计。
- **CS149**：gossip = 全网广播并行；PoW = 无同步的全局速率限制器。
- **CS242/PL**：智能合约的形式化验证（Certora 等）是 L22 验证线程的延续。
- **6.S081**：钱包/节点软件 = 普通系统程序：文件系统、网络、并发一个不少。

## 6. 开源项目中的应用

- **联盟 BFT**：Hyperledger Fabric（PBFT 变体）、Tendermint/CometBFT（Cosmos）、
  Aptos/Sui 的 DAG-BFT（HotStuff 家族）。
- **公链**：Bitcoin Core、Geth（PoS 合并后 = PoS 共识 + 执行层分离，
  "执行/共识分离"与本课"计算/存储分离（L13）"同构）。
- **非区块链应用**：安全关键系统的 BFT（航天/核电三模冗余的现代版）、
  审计日志的 tamper-evident 链（证书透明度 CT = Merkle 树共识的温和应用）。
- 本目录 projects/p3：把 KV 状态机换成"账本状态"、Raft 换成"BFT"即区块链内核雏形。

## 7. 延伸阅读

- Buterin, *In Search of an Understandable Consensus (POS)* 与 HotStuff 论文（DAG-BFT 入门）。
- *Bitcoin: Attack is Cheap* 与 Lightning 网络白皮书（链下扩展）。
- Castro & Liskov BFT (1999) 原论文 + *PBFT 到 HotStuff 的演化* 系列技术博客。
- 收官建议：重读 Raft（L05/L06）——此时你会看到它每个设计对 L07/L08/L10/L24 的回应。
