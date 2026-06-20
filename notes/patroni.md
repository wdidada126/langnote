# patroni

https://patroni.readthedocs.io/en/latest/

pg数据库高可用方案
A template for PostgreSQL High Availability with Etcd, Consul, ZooKeeper, or Kubernetes

https://github.com/zalando/patroni

## 版本
https://patroni.readthedocs.io/en/latest/releases.html

v4.1.0
v4.0.7 Sep 23, 2025
v4.0.0 Aug 29, 2024
v3.2.0 Oct 25, 2023
v3.0.0 Jan 30, 2023
## 编程语言
Python

## 编译脚本
which pip
which python
pip install setuptools wheel
git clone https://github.com/patroni/patroni.git
cd patroni
git checkout v4.0.0
ls -la setup.py
pip install -r requirements.txt
pip install -r requirements.dev.txt
python setup.py bdist_wheel
ls -la dist/

# 安装 build 工具
pip install build
# 执行打包
python -m build --wheel


Patroni 是一个基于 Python 的PostgreSQL高可用性（HA）解决方案模板，它通过分布式配置存储（DCS）来管理 PostgreSQL 集群的状态，实现自动故障转移和主从切换。以下是其架构的详细介绍：
1. 核心架构组件
Patroni 架构主要由以下三个核心组件构成：

•   Patroni 守护进程：运行在每个 PostgreSQL 节点上的 Python 进程。它负责监控 PostgreSQL 实例的健康状态，并通过 REST API 与 DCS 通信，执行集群管理操作（如提升为主库、降级为备库）。
•   分布式配置存储（DCS）：这是 Patroni 的“大脑”，用于存储集群的元数据和状态信息。Patroni 支持多种 DCS 后端，包括：
    ◦   etcd：最常用的选择，基于 Raft 算法，提供强一致性。
    ◦   Consul：由 HashiCorp 提供，也基于 Raft。
    ◦   ZooKeeper：基于 ZAB 协议。
    ◦   Kubernetes：利用 Kubernetes 的 API 作为 DCS。
•   PostgreSQL 实例：实际的数据库节点，运行在主库（Leader）或备库（Replica）模式下。Patroni 通过流复制（Streaming Replication）来同步数据。

2. 工作流程与选举机制

Patroni 通过“租约（Lease）”机制来管理主库选举：
1.  启动与注册：每个 Patroni 节点启动时，会在 DCS 中注册自己，并尝试获取一个“Leader Key”的租约。
2.  主库选举：只有一个节点能成功获取租约，该节点将启动或提升其 PostgreSQL 实例为主库。其他节点则作为备库，从主库同步数据。
3.  心跳与健康检查：主库节点需要定期（通过 loop_wait 参数控制）向 DCS 续租。如果主库节点故障（如进程崩溃、网络分区），导致无法续租，租约将过期。
4.  故障转移：当租约过期后，DCS 中的 Leader Key 被释放。此时，备库节点会检测到这一变化，并开始新一轮的选举。最健康的备库（通常是 WAL 延迟最小的）将获得租约并提升为新主库。

3. 关键特性
•   异步与同步复制：支持配置异步复制（默认）和同步复制（通过 synchronous_mode 参数），以满足不同的数据一致性需求。
•   配置管理：集群配置（如 postgresql.conf 参数）可以存储在 DCS 中，实现配置的集中管理和动态下发。
•   REST API：提供 HTTP API 接口，用于查询集群状态、手动切换主备、重新加载配置等操作。
•   与负载均衡器集成：通常配合 HAProxy 或 Keepalived 使用，为应用提供一个统一的读写入口。

4. 官方文档与资源
•   官方文档：最权威的文档位于 https://patroni.readthedocs.io，其中详细介绍了配置参数、部署指南和故障排除方法。
•   GitHub 仓库：源代码和最新发布信息位于 https://github.com/zalando/patroni。

Patroni 的读音是 /pəˈtroʊni/，中文谐音近似为 “帕特罗尼”。
•   发音分解：
    ◦   Pa：发音类似中文的“帕”，重音在第二个音节。
    ◦   tro：发音类似英文单词“throw”中的“tro”。
    ◦   ni：发音类似中文的“尼”。

•   词源背景：Patroni 源自拉丁语，意为“守护者”或“保护者”，在英语中常指“守护神”或“赞助人”。在数据库领域，它特指一个用于管理 PostgreSQL 高可用集群的开源工具，即“PostgreSQL 的守护者”。

PostgreSQL 的高可用方案非常丰富，除了 Patroni，还有多种适用于不同场景（如传统运维、云原生、轻量级需求）的成熟方案。以下是主流方案的对比及推荐：

1. 主流方案全景对比

方案名称 核心机制 适用场景 推荐指数 核心特点

Patroni DCS (etcd/Consul) 大中型生产、云原生 ⭐⭐⭐⭐⭐ 社区首选。基于分布式一致性存储，自动故障转移，功能最全面。

Repmgr Agent (守护进程) 中小规模、传统部署 ⭐⭐⭐⭐ 轻量级元老。历史悠久，配置简单，无需外部 DCS，适合中小团队。

pg_auto_failover Monitor (监控节点) 轻量级 HA、Citus 集群 ⭐⭐⭐⭐ 微软出品。无需外部依赖，架构简单，与 Citus 集成好。

Stolon DCS (etcd/K8s API) Kubernetes 环境 ⭐⭐⭐⭐ 云原生专用。专为 K8s 设计，支持连接代理和无状态设计。

Pacemaker + Corosync Linux-HA 集群 金融级、传统数据中心 ⭐⭐⭐ 企业级标准。功能强大，支持共享存储，但配置极复杂，学习成本高。

PgPool-II 中间件代理 读写分离 + 连接池 ⭐⭐⭐ 多合一方案。集成了连接池、负载均衡和故障转移，但自身可能成为瓶颈。

2. 各方案深度解析
1. Repmgr (Replication Manager)
•   定位：轻量级、无外部依赖的复制管理工具。
•   特点：由 EDB (原 2ndQuadrant) 开发，通过 repmgrd 守护进程监控状态，提供自动故障转移。相比 Patroni 更“轻”，但脑裂防护能力稍弱（需依赖 witness 节点）。
•   适用：不想维护 etcd/Consul 的中小规模环境，或 EDB 商业产品用户。

2. pg_auto_failover
•   定位：简单、开箱即用的自动故障转移。
•   特点：由 Microsoft/Citus 团队开发，只需一个独立的 Monitor 节点（也是 PostgreSQL 实例）来仲裁，无需引入 etcd 等复杂组件。
•   适用：Citus 集群的配套高可用，或追求最小化外部依赖的场景。

3. Stolon
•   定位：云原生和 Kubernetes 原生的高可用方案。
•   特点：通过 K8s API 或 DCS 协调，包含 Sentinel（决策）、Keeper（管理实例）和 Proxy（连接路由）三个角色，非常适合在容器化环境中运行。

4. Pacemaker + Corosync (金融级方案)
•   定位：企业级、高可靠的传统集群方案。
•   特点：这是 Linux 高可用项目的标准套件。在金融行业（如银行）中，常配合共享存储（Shared Storage）使用，实现 RPO=0（零数据丢失）。其核心是“资源独占”管理，确保数据只被一个节点挂载，通过存储层冗余（如双活存储）实现高可用，完全规避了流复制的网络风险。但配置极其复杂，需要专业运维团队。

5. PgPool-II
•   定位：连接池 + 高可用中间件。
•   特点：它位于应用和数据库之间，主要提供连接池和负载均衡，同时通过 Watchdog 机制实现自身高可用。注意：它通常不直接管理 PostgreSQL 的流复制状态，而是通过健康检查来切换后端连接，常与 Patroni 或 Repmgr 配合使用。

3. 选型建议
•   企业级生产/云原生：首选 Patroni，功能最全，社区最活跃。
•   中小规模/轻量级：选 Repmgr 或 pg_auto_failover，部署更简单。
•   Kubernetes 环境：Stolon 或 Patroni 都是好选择。
•   金融/高合规：考虑 Pacemaker + Corosync 配合共享存储，但需评估运维成本。

•   需要连接池：PgPool-II 作为中间件补充，但需注意性能调优。
