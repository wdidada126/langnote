# 第 2 章　搭建 ZooKeeper 单机运行环境

> 原书第 2 章是动手章：下载、配置 zoo.cfg、启动/连接/停止/查看状态，以及最基础的
> 节点增删改查（create/ls/get/set/delete）。这是后续所有 ZK 实验的地基，偏操作、理论密度低。
> 2026 视角要补的是：**容器化部署（Docker）、ZK 3.5+ 内嵌管理控制台、以及「单机仅用于本地开发」的边界**。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 2.1 下载 ZooKeeper | 从官网获取发行包 | 认准 apache/zookeeper 官方发布 |
| 2.2 创建 zoo.cfg | 最小配置文件 | 三个核心项：tickTime/dataDir/clientPort |
| 2.3 tickTime/dataDir/clientPort | 配置项含义 | tick=心跳节拍；dataDir=数据目录；clientPort=客户端端口 |
| 2.4 启动服务 | zkServer.sh start | 单机模式启动 |
| 2.5 连接服务 | zkCli.sh -server | 用命令行客户端连 |
| 2.6 停止服务 | zkServer.sh stop | 优雅停止 |
| 2.7 查看状态 | zkServer.sh status / stat | 单机模式显示 standalone |
| 2.8 查看所有命令 | help | ZK CLI 命令清单 |
| 2.9 create 创建节点 | create /path data | 默认持久节点 |
| 2.10 ls 查看子节点 | ls /path | 列出子节点名 |
| 2.11 get 查看值 | get /path | 读节点数据 |
| 2.12 set 设新值 | set /path data | 覆盖写 |
| 2.13 delete 删除节点 | delete /path | 节点有子节点时**不能删** |

## 核心精讲

（以下为教学性梳理，命令/伪代码均**教学示意，不参与构建**。） 

### 2.2 / 2.3 最小配置三件套

```text
# 教学示意，不参与构建：zoo.cfg 最小可用配置
tickTime=2000        # 基础时间单位(ms)：心跳、超时都以其倍数计
dataDir=/tmp/zkdata  # 事务日志+快照存放目录（生产必须独立磁盘）
clientPort=2181      # 客户端连接端口
# 单机模式仅此三项即可启动；集群模式才需要 server.x / initLimit / syncLimit（见第 3 章）
```

- **tickTime**：ZK 所有时间参数的基准。会话超时（sessionTimeout）必须是 tickTime 的 2~20 倍。
- **dataDir**：强烈建议单独挂载盘，且把事务日志（dataLogDir）与快照分开，避免 IO 竞争。
- **clientPort**：客户端连入端口，默认 2181。

### 2.9–2.13 基础节点操作

```text
# 教学示意，不参与构建：ZK CLI 最小操作序列
create /app "v1"          # 创建持久节点（默认），可加 -e 临时 / -s 顺序
ls /app                   # 列出子节点
get /app                  # 读取数据 + stat（版本/czxid/mtime）
set /app "v2"             # 覆盖写（会递增 dataVersion）
delete /app               # 删除（有子节点则失败，需先删子节点；递归删用 deleteall，见第 4 章）
```

> 关键坑：**`delete` 不能删有子节点的节点**（本书 2.13），递归删除要用第 4 章的 `deleteall`。
> 这与 Linux `rm -r` 不同，初学者极易踩。

## 版本演进

- **本书无第二版**；本节写 2022 年口径 → 2026 年视角的变化。
- **Docker / 容器化部署**：2026 年本地起 ZK 几乎都用 `docker run zookeeper`（官方镜像
  `zookeeper:3.9`），不再手动下载解压；本书的「下载 + 改 zoo.cfg」流程已偏传统。
- **ZK 3.5+ 内嵌 AdminServer**：默认 8080 端口提供 HTTP 管理/指标端点，
  本书基于 3.x 早期版，未提及；生产需显式管控该端口（安全）。
- **配置中心化**：Kubernetes 上 ZK 常以 StatefulSet + 配置卷部署，zoo.cfg 由 ConfigMap 注入，
  与本书「单机改文件」范式不同。
- **本地开发 vs 生产**：本书单机模式仅供学习；**生产必须用集群（第 3 章）**，单机 standalone 无容错。

## 经典论文与原始文献

| 文献 | 出处 | 贡献 |
| --- | --- | --- |
| Hunt et al.《ZooKeeper: Wait-free Coordination for Internet-scale Systems》 | USENIX ATC 2010 | ZK 原始论文，含数据模型与 API 设计哲学 |
| Apache ZooKeeper 官方文档（Configuration 章节） | zookeeper.apache.org | zoo.cfg 各项的权威释义（版本较多，以官网当前版为准） |

## 近年研究与工业界开源实践（2015–2026）

- **apache/zookeeper（12811★，2026-09 实测）**：仍在维护，3.9/3.10 系列修复安全与管理端点问题。
- **官方 Docker 镜像 `zookeeper`**：已成为本地起 ZK 的事实标准方式（本书未覆盖）。
- **apache/curator（3173★）**：Java 程序化操作 ZK 的封装，替代裸 zkCli 脚本（见 04）。

## 常见误区与本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「单机 ZK 可用于生产」 | 单机 standalone **无容错**，生产必须用集群（第 3 章） |
| 2 | 「delete 可递归删」 | 裸 `delete` 不能删含子节点的节点，递归用 `deleteall`（第 4 章） |
| 3 | 「dataDir 随便放」 | 事务日志 IO 密集，应与快照分盘，生产级部署的关键 |
| 4 | 🔧 未提容器化部署 | 2026 年本地起 ZK 用 Docker 官方镜像，不再手动下载解压 |
| 5 | 🔧 未提 AdminServer(8080) | ZK 3.5+ 内嵌管理端口，生产需管控（本书基于早期 3.x） |
| 6 | 🔧 未提会话超时与 tickTime 的倍数约束 | sessionTimeout 必须是 tickTime 的 2~20 倍，否则启动报错 |

## 与其他章 / 其他书的联系

- **本书内**：
  - 2.3 配置 → [03-搭建ZooKeeper主从运行环境.md](03-搭建ZooKeeper主从运行环境.md)（集群扩展配置）；
  - 2.9–2.13 基础操作 → [04-ZooKeeper常见命令和Curator的使用.md](04-ZooKeeper常见命令和Curator的使用.md)（命令全集与 watch）；
  - 2.9 create 临时节点 → [07-Dubbo实战技能.md](07-Dubbo实战技能.md)（服务注册落地）。
- [../深入理解分布式共识算法/00-总览与阅读地图.md](../深入理解分布式共识算法/00-总览与阅读地图.md)
  ——理解为什么「单机只是玩具、集群才谈容错」的共识背景。
