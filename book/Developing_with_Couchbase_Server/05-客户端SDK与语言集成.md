# 05 · 客户端 SDK 与语言集成

> 主题域：官方文案的第一主线——「把 Java、.NET 与脚本平台的客户端连上集群」，以及连接、序列化、拓扑刷新三件事的今昔。
> 章号/章名 ⚠️ 精读重构；✅ 为官方页原句/URL；🔧 为本机类比（本机不装 Couchbase SDK）。

## 1. SDK 在架构里承担什么

Couchbase 的客户端不是「瘦驱动」，它同时是：

1. **拓扑感知的路由器**：持有集群映射（或查询路由信息），把请求发去正确的节点（✅ [connectivity](https://docs.couchbase.com/server/current/learn/clusters-and-availability/connectivity.html)）。
2. **重试与退避的执行者**：映射变更、节点切换、CAS 冲突都是可重试事件（与 [03-键值操作与并发控制.md](03-键值操作与并发控制.md) 的重试环对接）。
3. **序列化的边界**：JSON ⇄ 对象映射（transcoder / mapper）由 SDK 提供，官方文案的「storage formats & object serialisation」正是这一层。
4. **认证与 TLS 的客户端侧**：x509 客户端证书、用户名/口令域、加密上下文（✅ [authentication-domains](https://docs.couchbase.com/server/current/learn/security/authentication-domains.html)、✅ [node-to-node-encryption](https://docs.couchbase.com/server/current/learn/clusters-and-availability/node-to-node-encryption.html)、✅ [encryption-overview](https://docs.couchbase.com/server/current/learn/security/encryption-overview.html)）。

## 2. 语言矩阵（2014 vs 2026）

| 语言 | 2014 基线（⚠️ 推定） | 2026 文档站点（✅，由 sitemap 证实条目数） |
|---|---|---|
| Java | 独立 client 2.x | `java-sdk`（532 页；版本目录含 3.9/3.10/3.11 + `current`）✅ |
| .NET | 独立 client | `dotnet-sdk`（379 页；3.7/3.8 + `current`）✅ |
| PHP | 老 `couchbase-extension` | `php-sdk`（独立 sitemap）✅ |
| Node.js | 老 `couchbase-node-client` | `nodejs-sdk`（349 页；4.4/4.5/4.6 + `current`）✅ |
| Python | 老 `couchbase-python-client` | `python-sdk`（353 页；4.3/4.4/4.5 + `current`）✅ |
| C / C++ | libcouchbase | `c-sdk`、`cxx-sdk`（各自 sitemap）✅ |
| Go | 当时非一等 | `go-sdk` sitemap ✅ |
| Scala / Kotlin / Rust | 之后若干年补齐 | `scala-sdk` / `kotlin-sdk` / `rust-sdk` sitemap ✅ |

**统一 SDK 世代**：各语言文档都保留了同一份迁移指南 `migrating-sdk-code-to-3.n.html`（✅ 已在 `sitemap-java-sdk.xml` 等中确认存在，例：https://docs.couchbase.com/java-sdk/current/project-docs/migrating-sdk-code-to-3.n.html ）——这说明「2.x → 3.x」是一次跨全部语言的重写级换代，本书 2014 年的 SDK 代码基本属于「API 化石」。

## 3. 连接与拓扑：从「手工回调」到「框架内建」

- 2014 姿势（⚠️ 基线）：构造 client → 打开桶 → 注册 `configChangeCallback` 自己处理映射变更；连接池大小、IO 线程数手工调。
- 2026 姿势（✅）：`Cluster.connect(connectionString, ClusterOptions)` 一把梭，内部完成 seed 解析、服务端口发现（`++`/`couchbase://` 协议差异）、映射刷新、故障重路由；服务角色端口语义见 ✅ [install-ports](https://docs.couchbase.com/server/current/install/install-ports.html)（⚠️ 细节以该页为准）。
- 诊断：官方专页 ✅ [sdk-doctor](https://docs.couchbase.com/server/current/sdk/sdk-doctor.html)（把 SDK 日志变成结论），这是 2014 完全没有的能力。
- 🔧 语义类比：SQLite 的连接与「WAL/锁等待」经验可用来体会「客户端必须懂服务器状态机」——本机 E3 中 `synchronous=FULL` 下 5000 次提交 **2143 ops/s（0.47ms/次）** vs OFF **43 180 ops/s（0.02ms/次）**，同一段代码只改一个连接参数就 20× 差；把这条经验平移：**SDK 的连接/超时/重试参数不是运维细节，而是产品 SLA 的一部分**（非 Couchbase 行为）。

## 4. 序列化与对象映射

- 官方把 JSON 的价值讲得很直白：轻量、可读、序列化快、天然适配 Web（✅ [document-data-model](https://docs.couchbase.com/server/current/learn/data/document-data-model.html)）。
- SDK 侧通常给三档：原始字节（自定义编解码）、JSON 树、POCO/实体映射（Java 的 Jackson、.NET 的 System.Text.Json、Node 的 schema 层如 Ottoman ⚠️ 名称转述，`ottoman-release-notes` 页在 ✅ `sitemap-nodejs-sdk.xml` 中在档）。
- 二元值仍被支持（✅ [learn/data/data](https://docs.couchbase.com/server/current/learn/data/data.html)：values can be either binary or JSON），因此「同一桶混存 JSON 与二进制」在数据模型上合法，但会让视图/索引/迁移三处都变复杂（⚠️ 工程判断）。
- 🔧 类比：E4/E5 的 SQLite `json_extract` / `json_patch` 演示了「同一份 JSON 既可整取也可按 path 取」的两种访问成本：整取内嵌聚合 0.13ms、JOIN 分片取 0.06ms（第 6 章给完整表）——序列化层的选择会决定后面所有查询的形状。

## 5. 框架集成层（开发者的真实入口）

| 生态位 | 2026 官方件（✅ sitemap/条目在档） |
|---|---|
| .NET ORM | EF Core provider（`sitemap-efcore-provider.xml`）✅ |
| Java 微服务 | Quarkus extension（`sitemap-quarkus-extension.xml`）✅ |
| 消息/流 | Kafka connector（`sitemap-kafka-connector.xml`）✅ |
| BI | Tableau / Power BI / Superset / Talend connector（各自 sitemap）✅ |
| 批处理 | Spark connector（`sitemap-spark-connector.xml`）✅ |
| 搜索侧 | Elasticsearch connector（`sitemap-elasticsearch-connector.xml`）✅ |
| AI 工具面 | MCP server（`sitemap-mcp-server.xml` 22 页，✅ [get-started/overview](https://docs.couchbase.com/mcp-server/get-started/overview.html)）✅ |
| 多设备/边缘 | Couchbase Lite（1535 页 ✅ [couchbase-lite/current/index.html](https://docs.couchbase.com/couchbase-lite/current/index.html)）+ Edge Server（✅ sitemap 61 页） |

这一整面「connector 墙」是 2014 那本书完全没有的语境：今天回答「怎么把 Couchbase 接进我的技术栈」不再靠手写 SDK 胶水（⚠️ 转述判断，但 ✅ 由 sitemap 存在性支撑）。

## 6. 代码骨架对照（⚠️ 伪代码，非可执行）

```text
# 2014 基线口吻
client = Cluster(uri).openBucket("travel")
doc = client.get("airport_22")            # 拿 CAS
body = json.loads(doc.value); body["taxiway"] = "B7"
client.replace(doc.id, body, cas=doc.cas) # 冲突则抛 → 自行重试

# 2026 统一 SDK 口吻
cluster = Cluster.connect("couchbase://...", ClusterOptions(user, pwd))
coll = cluster.bucket("travel").scope("tenant_a").collection("airport")
res = coll.get("SFO")
coll.mutate_in("SFO", [ArrayInsertDocSpec(path="runways[0]", value={...})],
               expiry=timedelta(hours=1))   # 子文档 + TTL 一次网络往返
```

（键值/子文档/过期语义 ✅ 见 03 章引用页；`scope/collection` 层级 ✅ [scopes-and-collections](https://docs.couchbase.com/server/current/learn/data/scopes-and-collections.html)。）

## 7. 版本兼容矩阵的读法（避坑方法）

1. 先看 ✅ 文档导航给出的服务端版本档（当前 `8.0 / 7.6 / 7.2`，见 https://docs.couchbase.com/server/current/introduction/intro.html 页面导航），确认文档不是「只有 current」。
2. 再看 SDK 侧的 `project-docs/*release-notes*` 与 `compatibility` 类页面（各 SDK sitemap 均有，✅ 例：https://docs.couchbase.com/couchbase-lite/current/android/compatibility.html ）。
3. 老代码升级时**优先读 `migrating-sdk-code-to-3.n`**（✅ 存在）而不是各语言的 API 页——换代点在那儿。
4. Capella 上的 SDK 连接串/证书要求与自建不同（✅ https://docs.couchbase.com/cloud/clouds/connection-troubleshooting.html），照抄书里 `http://:8091/pools/default/buckets/...` 的写法会在云上直接失败。

## 核心概念速览（中英对照）

- **SDK** — Software Development Kit / Client Library：承担路由、重试、序列化与认证的应用侧运行时。
- **统一 SDK 世代** — Unified 3.x SDKs：跨语言重写的 API 代际，与 2.x 不兼容。
- **拓扑感知** — Topology-aware：客户端持有集群映射并直连属主节点。
- **种子节点** — Seed Node：初次连接用于发现完整拓扑的入口地址。
- **transcoder** — 转码器：对象 ⇄ 文档字节的双向编解码组件。
- **POCO 映射** — Entity Mapping：把文档映射为语言对象，隐式引入「仓储层」。
- **子文档 API** — Sub-document API：`lookupIn/mutateIn`，按 path 局部读写。
- **重试与退避** — Retry & Backoff：把映射变更/CAS 冲突当作可恢复事件。
- **认证域** — Authentication Domain：凭据的来源（本地 / LDAP / 组映射）。
- **TLS 加密** — Encryption / x509 认证：客户端-节点与节点-节点两条链路。
- **sdk-doctor** — 官方诊断工具：把 SDK 日志翻译成可执行结论。
- **connector 生态** — Connectors：Spark/Kafka/BI/ES 等外部系统的官方桥。
- **EF Core / Quarkus 扩展** — 框架侧官方集成件：替代手写胶水层。
- **版本档 (current/8.0/7.6/7.2)** — 文档版本目录：判断信息新鲜度的第一线索。

## 最新演进与工业实践

1. **换代幅度**：2.x→3.x 是重写级（各语言均有官方迁移指南，✅ 见第 2 节），因此本书 2014 的客户端示例代码 today 只剩**概念参考价值**，抄不得。
2. **SDK 版本并轨**：不同语言号不同但同属一代（Java 3.1x / .NET 3.8 / Node 4.x / Python 4.x，均由各 sitemap 版本目录证实 ✅），排障时别说「SDK 3.x」而不带语言。
3. **多协议**：Query/Analytics/Search/Vector 各自有 SDK 子模块（`*-analytics-sdk`、`*-columnar-sdk` 等 sitemap 在档 ✅），2026 的「一个 SDK」实际是一族包。
4. **AI 接入面**：官方 **MCP Server** 文档站存在（✅ https://docs.couchbase.com/mcp-server/get-started/quickstart.html ），意味着「让编码代理直接操作集群」已是官方支持路径而非民间 hack；`sitemap-ai.xml`（45 页）对应 AI Data Plane 的 API 指南（✅ https://docs.couchbase.com/ai/api-guide/api-intro.html ）。
5. **云上连接是新的第一号故障源**：`sitemap-cloud.xml` 里专设 `clouds/connection-troubleshooting.html`（✅），私有网络/VPC peering 页也在档（✅ https://docs.couchbase.com/cloud/clouds/private-network.html）——2014 书里「网络问题」章节的等价物今天更长，不在数据库手册而在云手册。
6. **对照阅读**：Redis 客户端语义对位 [../Learning_Redis/02-五大数据类型的语义.md](../Learning_Redis/02-五大数据类型的语义.md)（结构在服务端 vs 在文档里）与 [../Learning_Redis/08-从2015到2026现状对位.md](../Learning_Redis/08-从2015到2026现状对位.md)（同为老书基线→现状对位的写法示范）；Mongo 驱动层对位 [../MongoDB_The_Definitive_Guide_3e/10-应用动态与数据管理.md](../MongoDB_The_Definitive_Guide_3e/10-应用动态与数据管理.md)；NoSQL 概览位 [../nosql精粹.md](../nosql精粹.md)。
7. **诚实缺口**：本章未对任何 SDK 做安装/运行验证（pip/npm 未装 couchbase 包），所有 API 形状描述为 ⚠️ 转述 + ✅ 文档指针；如需可执行结论，请在允许联网装包的环境另行实测。
