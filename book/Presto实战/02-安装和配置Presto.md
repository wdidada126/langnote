# 02 安装和配置 Presto

> 原书第 2 章（中译本 p.16–21）。定位：把"最小可查询集群"跑起来的两条路。
> 返回 [00-总览与阅读地图.md](00-总览与阅读地图.md)。

## 本章地图

| 节 | 内容 | 一句话结论 |
| --- | --- | --- |
| 2.1 Docker 容器尝鲜 | `prestodb/presto` 镜像一键起协调器+CLI | 教学首选，生产禁用（书中语义） |
| 2.2 归档文件安装 | 下载 tar.gz、JVM（Java 8 时代）、Python 依赖、目录结构、四大配置文件 | 理解配置分层的正路 |
| 2.2.4 配置 | `etc/config.properties` / `jvm.config` / `log.properties` / `catalog/*.properties` | 一个文件一个关切 |
| 2.3 添加数据源 | example / jmx / memory 连接器起步，再挂 Hive | catalog 即"命名了的数据源" |
| 2.4 运行 Presto | `launcher start/stop`，Web UI `:8080` | 健康检查=查询 `system.runtime.nodes` |

## 精讲

### 1. 配置四件套的分层思想
```text
etc/
├── config.properties      # 节点角色与引擎参数：coordinator=true / node-scheduler.*
│                          #   http-server.http.port=8080 / query.max-memory-per-node 等
├── jvm.config             # JVM 参数：-Xmx、G1GC、CodeCache、直接内存上限（与 12.7 呼应）
├── log.properties          # 日志级别（log.level=INFO/DEBUG）
└── catalog/               # 每文件一个 catalog：connector.name=hive-hadoop2 等
    ├── hive.properties
    ├── tpch.properties
    └── memory.properties
```
- **协调器与工作者同包不同配置**：`coordinator=true/false` 是唯一的身份开关，
  worker 还需 `discovery.uri` 指向协调器。理解这点，第 5 章的集群部署就是复制粘贴的纪律问题。
- ⚠️ 书中示例基于 34x 版（Java 8 时代）；当前 prestodb/Trino 均要求 Java 17+，参数面有换代（见文末）。

### 2. 节点发现的最小拓扑（单进程）
教学镜像把"协调器 + 内嵌发现服务 + 一个工作者"塞进一进程；生产必须拆开——
发现服务在 0.2xx 后由外部 etcd 收敛为**协调器内嵌**（`catalogs.properties` 之外无 etcd 依赖，
书中时代仍介绍过外部 etcd 方案 ⚠️ 细节未逐页核对）。展开见
[04-Presto的架构.md](04-Presto的架构.md) 的 4.3 与 [05-生产环境部署.md](05-生产环境部署.md)。

### 3. 第一个数据源：TPCH 与 memory 的分工
- `tpch` 连接器：秒级生成可复现实验数据（书中鸢尾花/航班数据集之外的"随手基准"），学优化器行为首选；
- `memory` 连接器：表存内存、重启即失，用来验证 CTAS/视图等 DDL 语义（第 8 章实验台）;
- `jmx` 连接器：把引擎自身指标当表查（`jvm.memory.*`、`query.*`），监控入门兼 debug 利器——第 6.6 节深挖。
**方法**（🔧 可在任意版本执行验证 CLI 语义）：
```sql
CREATE SCHEMA memdemo.t AS SELECT * FROM tpch.tiny.nation;
SELECT * FROM system.runtime.nodes;   -- 应列出本拓扑全部节点
```

### 4. 从"尝鲜"到"能查生产"的缺口清单
本章跑通后你还没有：认证（第 10 章）、资源组（12.8）、统计信息（4.12）、监控（12.1）。
书中刻意把"跑起来"与"跑得好"分成两个世界——第 2 章与第 5/12 章的落差就是运维成熟度的路线图。

## 常见误区

| 误区 | 现实 |
| --- | --- |
| Docker 端口映射了就能横向扩展 | 单镜像只是拓扑演示；多 worker 需共享同一 `coordinator` 与目录权限、发现配置 |
| JVM `-Xmx` 拉满就好 | Presto 还有**引擎级内存池**（general/reserved），-Xmx 与 `query.max-memory-per-node` 必须一起设计（12.3） |
| catalog 名字随便起 | catalog 名进入用户 SQL 命名空间（`hive.dwd.x`），改名=全量断引用，生产要当 API 管理 |
| 配了 Hive metastore URI 就能读 HDFS | Kerberos 环境还需 principal/keytab（10.8），这是国内 Hadoop 集群最常见卡点 |

## 与其他章/其他笔记的联系
- 部署深化 → [05-生产环境部署.md](05-生产环境部署.md)；JVM 参数与内存池 → [12-生产环境中的Presto.md](12-生产环境中的Presto.md)；
- 连接器配置展开 → [06-连接器.md](06-连接器.md)；
- 与 Spark 的本地起法对照（同为"教学单机版"）→ [../Spark大数据分析与实战.md](../Spark大数据分析与实战.md)。

## 本章小结与行动清单

三句话带走：
1. 安装章的真正知识点是**配置分层**：角色开关（config）/JVM（jvm.config）/日志/数据源（catalog/）四刀切干净；
2. `etc/catalog/*.properties` 每个文件=一个用户可见命名空间——命名纪律从第一天开始；
3. 单机跑通 ≠ 会部署：把"跑通"到"能服务"之间的缺口清单（认证/资源组/统计/监控）钉在工位上，它们分别是 10/12.8/4.12/12.1 章。

实操检查单（任一发行版通用骨架；参数名按版本对表 ⚠️）：
- [ ] 协调器与 worker 以差分配置分离启动，`node-scheduler.include-coordinator=false`；
- [ ] `system.runtime.nodes` 返回全部节点且 roles 正确；
- [ ] tpch/memory/jmx 三个实验 catalog 可查；
- [ ] 杀一个 worker，观察在途查询失败语义（为 04/13 章的容错讨论攒现场感）；
- [ ] 配置目录整体纳入版本库（配置即代码第一次演练）。

自测：
- [ ] `-Xmx` 与 `query.max-memory-per-node` 谁包谁？（提示：联立不等式在 12.3）
- [ ] 为什么生产建议协调器不兼 worker？至少说出两条（规划抖动/Exchange 挤兑）。

## 核心概念速览（中英对照）

| 术语 | English | 释义 |
| --- | --- | --- |
| 归档安装 | Standalone tarball install | 下载 tar.gz 解压自建，非包管理器/容器 |
| 启动器 | Launcher | `launcher run/start/stop` 进程管理脚本 |
| 配置属性文件 | config.properties | 节点角色与引擎主配置 |
| JVM 配置 | jvm.config | 堆大小、GC、CodeCache 等纯 JVM 参数 |
| catalog 目录 | etc/catalog/*.properties | 一文件一数据源命名空间的约定 |
| 协调器开关 | coordinator=true | 同包异配区分协调器/工作者 |
| 发现 URI | discovery.uri | 工作者寻址协调器的入口 |
| 内嵌发现 | Embedded Discovery | 协调器内置节点发现服务（etcd 外置为历史方案 ⚠️） |
| TPCH 连接器 | TPC-H Connector | 生成式基准数据源，开箱可查 |
| 内存连接器 | Memory Connector | 数据驻留内存的试验表，重启即失 |
| JMX 连接器 | JMX Connector | 把运行时指标暴露成 SQL 表的自省源 |
| 系统运行时模式 | System Runtime Schema | `system.runtime.nodes` 等引擎自省表 |
| Python 依赖 | Python Runtime Dep | 旧版 CLI/工具链对解释器的要求（时代印记） |

## 最新演进与工业实践

- **运行时要求换代**：prestodb 与 Trino 当前版本均要求 Java 17+（Trino 483 文档实抓，
  [trino.io/docs/current/overview.html](https://trino.io/docs/current/overview.html) ✅）；书中 Java 8 路径已是历史，
  照抄会直接起不来——升级必读各版本 Release Notes（[github.com/prestodb/presto/releases](https://github.com/prestodb/presto/releases) ✅）。
- **容器化的今天**：官方与社区镜像持续维护（`prestodb/presto`、`trinodb/trino`），生产形态主流已转为
  **Kubernetes Operator/自定义编排 + 对象存储**；GitHub 主仓库为事实文档入口
  （[github.com/prestodb/presto](https://github.com/prestodb/presto) ✅ 200；[github.com/trinodb/trino](https://github.com/trinodb/trino) ✅ 200；
  prestodb.io ⚠️ 实抓 403 不作内容依据）。
- **湖仓默认件**：新集群的最小可用配置从"挂 Hive metastore"转向"挂 **Iceberg REST/Glue/Nessie catalog**"——
  [iceberg.apache.org/docs/latest/](https://iceberg.apache.org/docs/latest/) ✅、
  [Trino Iceberg connector](https://trino.io/docs/current/connector/iceberg.html) ✅；
  操作细节互链 [../Apache_Iceberg活用入門/09-Spark_Flink_Trino实战.md](../Apache_Iceberg活用入門/09-Spark_Flink_Trino实战.md)。
- **国内实践印证**：B 站在路由层做"引擎选路"前先解决各引擎的可运维部署（Dispatcher 统一提交）——
  [dbaplus 原文](https://dbaplus.cn/news-73-4481-1.html) ✅；美团早期部署同样是先跑通最小拓扑再谈规模——
  [tech.meituan.com Presto 实践](https://tech.meituan.com/2014-06-16/presto.html) ✅。
- **🔧 可本机验证的替代物**：想体会"catalog 即数据源"的配置手感而无集群时，可用本机 DuckDB 的
  `INSTALL httpfs; SELECT * FROM read_parquet('https://.../x.parquet');` 感受"引擎不落地读远端文件"的同构体验
  （🔧 DuckDB 本机可跑；Presto 本体不在本机实测范围，凡涉及其运行行为的结论一律转述+⚠️）。
