# 第 2 章　核心模型：Domain · Park · Node · FttpAdapter · Worker

> 原书用一组 Java 核心类来组织整个框架：Park（协调）、DomainNode（域节点）、
> FttpAdapter（文件适配器）、Worker（计算单元）。本章是后续所有组件的「词汇表」。
> 由于原书未给出可公开核实的权威类图，本章模型描述**依据 fourinone 公开文档与仓库笔记
> 点名的概念重构**，凡无法核实处标注存疑。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 2.1 总体对象模型 | Park / DomainNode / FttpAdapter / Worker 四件套 | 一个「协调 + 计算 + 文件」的最小闭环 |
| 2.2 Park：协调中枢 | 命名、注册、配置、锁的载体 | 相当于「嵌入式 ZooKeeper」，但实现与正确性存疑 |
| 2.3 DomainNode：域节点 | 一组 Worker 的归属与分组 | 类似 YARN 的 NodeManager 概念雏形 |
| 2.4 FttpAdapter：文件适配 | 把文件读写抽象成远程适配器 | 基于 JDK HttpServer 的「ftp over http」 |
| 2.5 Worker：计算单元 | 实际执行并行任务的单元 | 类似 MapReduce 的 Task，但调度模型简化 |
| 2.6 模型总评 | 抽象层级与表达力 | 🔧 抽象偏「教学示意」，缺生产级的容错/扩缩容语义 |

## 核心精讲

（以下为教学性梳理，伪代码/示意均**教学示意，不参与构建**。）

### 2.1 四件套的关系（教学示意）

```text
# 教学示意，不参与构建：fourinone 最小闭环
        +-------------------+
        |   Park (协调中枢)  |  命名/注册/配置/锁
        +---------+---------+
                  | 调度 & 发现
        +---------v---------+
        |  DomainNode (域)   |  一组 Worker 的宿主
        +---------+---------+
                  | 派发任务
        +---------v---------+
        |  Worker (计算单元)  |  执行具体并行任务
        +-------------------+
        +-------------------+
        | FttpAdapter(文件)  |  Worker 通过它读写分布式文件
        +-------------------+
```

### 2.2 Park：把协调塞进一个类

- Park 在 fourinone 里同时承担：服务注册发现、共享配置、分布式锁。
- 设计意图是「免部署独立协调集群」，但代价是**协调逻辑与业务进程耦合**，
  且正确性（选主、脑裂防护）依赖作者实现，书中未给可复核证明。
- 对比 ZooKeeper：ZK 是独立集群 + ZAB 共识协议（有论文、有 Jepsen 测试）；
  Park 的实现细节书里未充分展开，**未能核实原文，存疑**。

### 2.4 FttpAdapter：基于 HTTP 的文件抽象

- 仓库笔记原文：fourinone 的文件系统叫 fttp，名字与 ftp/http 相似，实为「通过 HTTP 上传下载文件」；
  服务端用 JDK6 自带的 `com.sun.net.httpserver.HttpServer`，客户端用 `HttpURLConnection`。
- 这意味着它**不是一个真正的分布式文件系统**（无分块、无副本、无元数据服务器），
  而更像「带 HTTP 接口的远程文件访问」。

```text
# 教学示意，不参与构建：FttpAdapter 的使用心智模型
FttpAdapter fa = new FttpAdapter("fttp://host:port/path/file");
// 实际上背后是 HttpURLConnection 的 PUT/GET
fa.getFttpWriter().write(bytes);
fa.getFttpReader().read(bytes);
// 必须明确知道文件在哪台机器的哪个目录 -> 笔记原文称"会崩溃"
```

### 2.6 模型总评

- fourinone 的抽象胜在**少概念、易上手**（几个类就覆盖了四类需求）；
- 但抽象层级停留在「教学示意」：没有显式的副本/分片/租约/共识概念，
  生产级所需的容错、扩缩容、背压、一致性语义都付之阙如。

## 版本演进

- 本书无第二版记录。
- **2013 年口径**：用一个 Java 类族表达分布式，对初学者「降低门槛」有宣传价值。
- **2026 年视角**：现代框架的抽象更清晰分层——协调归 etcd/ZK（Raft）、
  计算归 K8s/Spark、文件归对象存储、缓存归 Redis。**把四件事塞进几个类反而模糊了边界**。
- 🔧 **必须补入**：共识（Raft，2014）、容器调度（K8s，2014）出现后，fourinone 这类
  「单进程内四合一」模型的必要性与正确性优势都被消解。

## 经典论文与原始文献

| 文献 | 出处 | 贡献 |
| --- | --- | --- |
| Lamport《Paxos Made Simple》 | ACM SIGACT News 2001 | 协调/选主的理论底座（Park 应有但未展示） |
| Ongaro, Ousterhout《In Search of an Understandable Consensus Algorithm》(Raft) | USENIX ATC 2014 | 现代协调服务的默认算法 |
| Vogels《Eventually Consistent》 | ACM Queue 2008 | 副本/一致性概念（模型里缺） |
| 本书引用情况 | — | **未给出明确原始文献**；类模型以 API 演示为主，存疑 |

## 近年研究与工业界开源实践（2015–2026）

- **Park 的对标者**：`apache/zookeeper` 12811★、`etcd-io/etcd`（Raft）52310★（见存储系统书实测）。
  etcd 用共识算法保证协调正确性，是 2026 年的事实标准。
- **fourinone 自身** `fourinone/fourinone` **85★**（2026-09-27 实测），与专业协调组件差距悬殊。
- **调度模型对照**：YARN（`apache/hadoop` 15670★ 内含）的 ResourceManager/NodeManager
  才是生产级「域节点 + 任务派发」模型；fourinone 的 DomainNode 只是其极简雏形。

## 常见误区与本书需修正之处

| # | 误区 | 事实 | 书目 |
| --- | --- | --- | --- |
| 1 | 「几个类就掌握分布式」 | 抽象简化掩盖了副本/共识/容错等核心难题 | 🔧 本书 |
| 2 | 「Park 等于 ZooKeeper」 | Park 无独立集群、无共识协议佐证、正确性存疑 | 🔧 本书 |
| 3 | 「FttpAdapter 是分布式文件系统」 | 实为基于 HttpServer 的远程文件访问，无分块/副本/元数据服务 | 笔记原文 |
| 4 | 「单进程四合一更易维护」 | 四类复杂度耦合，反而难演进、难排障 | 🔧 2026 视角 |
| 5 | 模型图与类关系未给可复核来源 | 本章模型为依公开文档重构，原书权威类图未能核实 | 本章存疑 |

## 与其他章 / 其他书的联系

- **本书内**：2.2 Park → [03-分布式协调与锁：Park 协调服务.md](03-分布式协调与锁：Park 协调服务.md)；
  2.3/2.5 Worker → [04-分布式并行计算：Worker 与 DomainNode.md](04-分布式并行计算：Worker 与 DomainNode.md)；
  2.4 FttpAdapter → [05-分布式文件：FttpAdapter·fttp.md](05-分布式文件：FttpAdapter·fttp.md)。
- [../大规模分布式存储系统/03-分布式系统.md](../大规模分布式存储系统/03-分布式系统.md)
  ——分布式系统的严谨概念（异常/一致性/复制/容错），对照本章「教学示意」级抽象。
- [../深入理解分布式共识算法/00-总览与阅读地图.md](../深入理解分布式共识算法/00-总览与阅读地图.md)
  ——Park 所缺的共识算法，去那里系统补。
- [../分布式系统/00-总览与阅读地图.md](../分布式系统/00-总览与阅读地图.md)（van Steen 教材）
  ——分布式系统模型的标准讲法。
