# 第 2 章 安装和配置Trino（Installing and Configuring Trino ⚠️ 英题推定）

> 对应原书第一部分第 2 章。二级节标题 ✅ 实抓自 [oreilly.com.cn 官方页](http://www.oreilly.com.cn/index.php?func=book&isbn=978-7-111-73160-3)。精读重构，配置片段为教学示意。

## 本章地图

| 节 | 内容 | 一句话结论 |
| --- | --- | --- |
| 2.1 使用Docker容器探索Trino | 单节点容器起最快，适合跟书练 | 学习用途首选，但容器内默认限制要放开 |
| 2.2 使用归档文件安装Trino | tarball 解开即装：etc/ 与 plugin/ 两大目录 | Java 依赖由随附 launch脚本兜底 |
| 2.3 添加数据源 | 在 `etc/catalog/` 放一个 properties 文件 = 挂一个 catalog | 「加数据源」=「写一个 connector 配置」 |
| 2.4 运行Trino | launcher start/stop、看日志、验活 | `trino --execute "SELECT 1"` 通了才算装完 |
| 2.5 小结 | 进入第 3 章客户端世界 | — |

## 核心精讲

### 1. 四个文件撑起一个「集群」（教学示意，非原书原文）

Trino 的配置极简模型——单节点 also 是「coordinator 自己给自己干活」：

```properties
# etc/config.properties —— coordinator=true 时兼任 worker
coordinator=true
node-scheduler.include-coordinator=true   # 生产上通常 false，见 12 章
http-server.http.port=8080
discovery.uri=http://localhost:8080
```

```properties
# etc/jvm.config（392 书稿口径的示例；JDK17+ 需追加 --add-opens 系列，见「最新演进」）
-server -Xmx4G
-Duser.timezone=UTC
```

```properties
# etc/catalog/tpch.properties —— 2.3 节核心：一个文件一个 catalog
connector.name=tpch
```

```properties
# etc/catalog/memory.properties
connector.name=memory
```

- `etc/node.properties`：`node.id` 必须集群内唯一且**重启不变**（官方文档 [installation/deployment.html](https://trino.io/docs/current/installation/deployment.html) ✅；392 起不强制手写 `node.environment` 的口径变化 ⚠️ 未逐版核对）。
- 概念链条：catalog ↔ connector 实例 ↔ 一个外部数据系统；`SHOW CATALOGS` 即时可验。

### 2. Docker 路径（2.1）

```bash
# 教学示意：官方镜像 trinodb/trino，挂载三个 etc 文件
docker run -d --name trino -p 8080:8080 \
  -v $PWD/config.properties:/etc/trino/config.properties \
  -v $PWD/jvm.config:/etc/trino/jvm.config \
  -v $PWD/catalog:/etc/trino/catalog \
  trinodb/trino:latest
docker exec -it trino trino
```

官方容器文档口径：镜像默认配置即单节点可用；容器内 JVM 堆大小与宿主机可见内存的错配是新手第一坑（✅ [installation/containers.html](https://trino.io/docs/current/installation/containers.html)）。483 时代该页同时覆盖 Kubernetes/Helm 内容，与 05 章呼应。

### 3. 归档路径（2.2）与运行时依赖

- 下载 tarball → 解压 → `bin/launcher run|start`。Trino 启动器（launcher）自带 JVM 下载逻辑或要求预装 JDK（书稿口径：预装 Java；483 口径：发行物自带 runtime 依赖细节 ⚠️ 未逐项核）。
- 392→483 的实质变化：**Java 版本线一路水涨船高**（JDK 17 成为硬性下限后 add-opens/add-exports 清单进入 jvm.config 标配），抄书中旧 jvm.config 会起不来——这是跟书实践最常见的失败点（483 文档 installation 章节 ✅）。

### 4. 验证与「加数据源」的仪式感（2.3/2.4）

```sql
-- 教学示意
SHOW CATALOGS;                     -- 应见 system/memory/tpch...
SELECT * FROM tpch.tiny.nation ORDER BY nationkey LIMIT 5;
CREATE SCHEMA memory.sales;        -- memory connector 支持 DDL，顺手建练习场
```

排错三板斧（与 [03 章](03-使用Trino.md) Web UI 联用）：`bin/launcher status`、`var/log/server.log`、浏览器 `http://localhost:8080`。

### 5. 安装路径决策树（本章收束）

```
目的=跟书学习        → Docker（2.1），钉 tag，别用 latest
目的=单机长期实验    → tarball + memory/tpch 双 catalog（2.2+2.3）
目的=上生产          → 直接跳 05 章三形态选型，本集群只当彩排
```

目录心智：`bin/`（launcher）、`etc/`（三份配置+catalog/）、`lib/`（引擎 jar）、`plugin/`（connector jar）、`var/`（运行期日志/数据）——五个目录读完，2.2 的「装」就完整了；「跑」的验收只有一条：`SELECT 1` + UI 打开无红字。

## 常见误区

- 把 `node-scheduler.include-coordinator=true` 带进生产：学习集群无妨，生产集群 coordinator 不跑 task（12 章展开）。
- 以为改 catalog 文件要重启：472 等近版已支持部分 connector 的 catalog 动态注册/更新（官方 release notes 口径 ✅ [release-483.html](https://trino.io/docs/current/release/release-483.html) 同索引页可回溯；「动态 catalog」完整 GA 范围 ⚠️ 未逐 connector 核）。
- Docker 里 `latest` 与书基线 392 行为不一致却不自知——跟书请钉版本 tag。
- 忘配 `discovery.uri` 指向自己/或 worker 指错 coordinator：worker 起得来但查不出数据，UI 里显示 0 worker。

## 与其他章/其他书的联系

- 生产化安装（RPM/云/Helm）在 [05-生产环境部署.md](05-生产环境部署.md)；客户端连接在 [03-使用Trino.md](03-使用Trino.md)。
- catalog/schema/table 三级命名空间的概念化在 [04-Trino架构.md](04-Trino架构.md)。
- 大数据平台上「Hadoop + Trino 共存」的资源视角，参见 [../bigdata/00-总览与阅读地图.md](../bigdata/00-总览与阅读地图.md) 与 [../bigdata/11-调度资源与运维.md](../bigdata/11-调度资源与运维.md)。

## 核心概念速览（中英对照）

1. **协调器（单节点模式）** — embedded coordinator：`node-scheduler.include-coordinator=true` 时一人分饰两角。
2. **发行包** — server tarball：解压即得的官方二进制分装。
3. **启动器** — launcher：`bin/launcher` 脚本，管理进程/JVM/日志。
4. **配置目录** — etc directory：`config.properties`、`jvm.config`、`node.properties` 三件套所在。
5. **catalog 目录** — catalog directory：`etc/catalog/*.properties`，一文件一数据源。
6. **发现服务** — discovery：worker 注册与拓扑发现的组件，`discovery.uri` 指向 coordinator。
7. **TPCH 连接器** — TPC-H connector：内存态合成数据源，装完即有练习库。
8. **内存连接器** — memory connector：表存 JVM 堆内、可 DDL 的试验田（✅ [connector/memory.html](https://trino.io/docs/current/connector/memory.html)）。
9. **容器镜像** — Docker image：`trinodb/trino` 官方镜像，学习路径最短。
10. **JVM 配置** — jvm.config：堆大小/GC/模块 opens 的 JVM 参数清单。
11. **节点标识** — node.id：集群内唯一且持久的节点身份证。
12. **插件目录** — plugin directory：connector 与服务扩展的落地处（6.10/7.x 的伏笔）。
13. **动态 catalog** — dynamic catalogs：近版新增的不重启增改 catalog 能力 ⚠️ 范围未逐核。
14. **服务器日志** — server.log：`var/log/` 下第一排查现场。

## 最新演进与工业实践

- **安装文档现状** ✅：[deployment](https://trino.io/docs/current/installation/deployment.html) 与 [containers](https://trino.io/docs/current/installation/containers.html)（483 基线）；官方镜像仓库 `ghcr.io/trinodb/trino` 与 Docker Hub 并行（容器化口径 ⚠️ 未逐一抓）。
- **Java 基线**：书稿 392 时代 JDK 11/17 混用可行；483 时代最低 Java 版本显著提高、`--add-opens` 清单进标配文档（逐版最低 JDK 矩阵未核 ⚠️，以官方 docs installation 页为准）。
- **Kubernetes 主流化**：2e 写作时 Helm chart 已在演进，2024–2026 社区 chart（`trinodb/charts`，仓库存在性经 GitHub 搜索可见但本次未逐项抓 ⚠️）与 CloudNeutral/运营商托管并存；生产部署普遍按「coordinator StatefulSet + worker 可扩缩」拓扑。
- **发行形态**：483 时代除 tarball 外提供 RPM/DEB、独立 CLI、JDBC 驱动 jar 的下载矩阵（✅ trino.io/download 一线入口；逐项格式 ⚠️ 未全抓）。
- **配套仓库实操资源** ✅：书官方仓库含 `single-installation/`、`cluster-installation/` 样例配置目录，可与本章对照（[trinodb/trino-the-definitive-guide](https://github.com/trinodb/trino-the-definitive-guide) README 实抓）。
