# 第 9 章 Catalog 与互操作

> ⚠️ 章题为**推定**（见 [00-总览与阅读地图.md](00-总览与阅读地图.md)）。
> 事实来源：Iceberg REST Catalog Spec、Hive Metastore Thrift API、Apache Polaris /
> Lakekeeper / Nessie / Unity Catalog 公开文档、Hudi Iceberg 元数据表、Delta UniForm 文档。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 9.1 | catalog 到底管什么 | 三件事：命名、指针、提交仲裁 |
| 9.2 | 三格式与 catalog 的耦合方式 | 谁可脱钩、谁不能 |
| 9.3 | Iceberg REST Catalog：事实标准之路 | 从"一种实现"到"一套 HTTP 协议" |
| 9.4 | 主流实现矩阵 | HMS / Glue / Polaris / Unity / Nessie / Lakekeeper |
| 9.5 | 跨格式互操作 | 元数据镜像与联邦读取 |
| 9.6 | 治理面：权限、多租户、审计 | catalog 正在成为策略执行点 |

## 核心精讲

### 9.1 catalog 的三职责

```text
① 命名空间：catalog.db.table → 表位置/元数据入口
② 指针存储：表当前 metadata 位置（Iceberg）/ 版本解析辅助（Delta/Hudi）
③ 提交仲裁：原子 CAS 点（第 6 章 6.6 的另一面）
+ 派生职责：锁与租约、属性缓存、统计信息、权限与审计
```

一个常被忽略的事实：**表格式解决"单表一致性"，catalog 解决
"表的身份与可达性"**；云厂商竞争（S3 Tables、各 managed Iceberg）
争的正是 ③+治理面。

### 9.2 三格式 × catalog 耦合度

| 格式 | 发现机制 | 提交依赖 | 可否"无 catalog 裸跑" |
| --- | --- | --- | --- |
| Iceberg | 必须（catalog 给 metadata.json 位置） | **强依赖**（CAS 仲裁点；Hadoop catalog 除外且弱） | 只读可以（path 直连），写不行 |
| Hudi | 表同步到 HMS（metastore sync 内建） | Timeline 条件写/MDT；HMS 非仲裁点 | 可以（目录即表），但锁与查询入口退化 |
| Delta | 约定 `_delta_log` 在数据目录内；catalog 可选 | 文件系统条件写为仲裁点 | 是（目录挂载即可读写） |

这解释了生态现象：**Iceberg 天生"catalog 中心"，Delta 天生"目录中心"**；
第 3 家 Hudi 介于两者（数据在目录、协作靠 timeline+索引）。

### 9.3 Iceberg REST Catalog

动机（REST spec 自述）：HMS/云专有 API 让"任意引擎 × 任意实现"
矩阵爆炸（m 引擎 × n 实现）。REST Catalog 把 Iceberg 表操作收敛成
HTTP JSON 协议：

```text
/v1/config            协商凭证与 defaults/overrides
/v1/namespaces…       命名空间与表 CRUD
/v1/…/tables/…        加载（返回 metadata-location 或直接内联 metadata）
                      更新（assertion + 原子替换：update-table 携带 requirements
                      ——如 assert-ref-snapshot-id——由服务端执行 CAS）
```

要点：**协议把第 6 章的 CAS 语义下沉进 API**——客户端只声明
"我认为当前快照是 X"，服务端负责校验与原子换。
🔧 生态：该规范已外溢为多格式趋势（S3 Tables、BigLake、
各云托管服务均以"REST 兼容"为卖点；SageMaker Lakehouse/Unity 亦支持）。

### 9.4 主流实现速览

| 实现 | 性质 | 一句话定位 |
| --- | --- | --- |
| Hive Metastore（Thrift） | 老牌默认 | 三格式都兼容；锁与扩展性是老债 |
| AWS Glue Data Catalog | 云托管 | 多格式统一入口；Iceberg 可经 REST/Lake Formation 治理 |
| Apache Polaris（🔧 已顶级） | 开源、REST 原生 | Iceberg REST 参考实现 + OAuth2/Ranger 级权限 |
| Snowflake Open Catalog | 托管 Polaris | 同上，绑定 Snow 生态体验 |
| Unity Catalog | 开源核心+多云 | 多格式（Delta 原生、Iceberg REST 兼容）+ 血缘/权限 |
| Project Nessie | git-like | 分支化元数据：`main/feature` 切表集，跨表事务视图 |
| Lakekeeper / Gravitino | 新世代 | 轻量自托管 / 联邦元数据（跨 HMS/Glue 的统一抽象） |

### 9.5 跨格式互操作：三条现实路线

**路线 A：单一数据 + 镜像元数据**（读端各取所需）

```text
Hudi 表 → 开启 Iceberg 元数据表：写端在 commit 时同步产出 Iceberg 兼容
          元数据，Trino/Athena 的 Iceberg 连接器直读同一份数据。
Delta 表 → UniForm：同理想同时镜像 Iceberg（及 Hudi）元数据。
```

代价：镜像有提交延迟与特性子集（如复杂类型/ DV 语义未必全映射），
**定位是"让别家引擎能读"，不是"让别家引擎能写"**。

**路线 B：转换/迁移**（一次性）：`ALTER TABLE ... CONVERT TO ICEBERG`
类命令（各云提供 Hive→Iceberg 就地转换、Delta↔Iceberg 迁移工具）。
见第 12 章迁移剧本。

**路线 C：catalog 联邦 + 引擎多连接器**：Gravitino/Polaris 类聚合层，
把三格式表统一暴露给 SQL 网关；数据仍是各写各的。

### 9.6 治理面：catalog 成为策略执行点

- 权限：REST catalog 的 OAuth2 + 行/列级策略（Polaris 集成 Ranger；
  Unity 的细粒度 GRANT）；
- 多租户：catalog = 计费与隔离边界（namespace 配额、限流）；
- 审计：所有"指针变化"天然留痕于 catalog 侧（与 commit 内审计互补）；
- 🔧 新现象：**catalog 侧托管维护**——注册表即可开启
  compaction/expire（S3 Tables、各 managed service），
  "谁来跑维护作业"（8.6 之问）的答案正在从"你自己"变成"catalog"。

## 常见误区

| 误区 | 事实 |
| --- | --- |
| "catalog 挂了只是查不到表" | Iceberg 连提交都不行（6.6）；catalog 吞吐 = 表写吞吐上限之一 |
| "REST catalog 只是换个协议" | 它把提交仲裁与断言校验标准化，改变了信任模型（客户端可被约束） |
| "元数据镜像 = 双向同步" | 主流镜像都是单向（写格式 → 镜像读格式），反向写会撕裂 |
| "HMS 能锁所以够用" | HMS 锁历史上脆弱且覆盖不全，多引擎并发写仍需格式层 OCC 兜底 |

## 与其他章的联系

- 9.1/9.4 → 06 章 6.6（原子性锚点的另一半）；
- 9.3 → 02 章 2.2（通用提交协议的标准化）；
- 9.5 → 04 章 4.6 后（Hudi/Iceberg 镜像）、05 章 5.6（UniForm）；
- 9.6 → 12 章选型考量（锁定效应与多引擎退出成本）；
- 数据接入生态对照 → [../bigdata/08-消息中间件与数据接入.md](../bigdata/08-消息中间件与数据接入.md)。

## 思考题

1. 论证："对 Iceberg 而言，catalog 可用性 SLA 必须 ≥ 写入管线 SLA。"
   反例场景：你能设计出 catalog 短暂不可用而写入不受影响的架构吗？
   （提示：只读缓存 + 写队列重放、REST assertion。）
2. Nessie 的"分支化 catalog"与 Iceberg 原生 refs（branch/tag，3.1）
   解决的是同一层问题吗？各自适合什么规模的多环境（dev/stage/prod）流程？
3. 设计：一张 Hudi 主管线写的表，同时有 Trino（Iceberg 读）、Spark
   （Hudi 读写）、BI（Delta 只读）三类消费者。用 9.5 的路线拼一个
   可行的最小架构，并指出两处"镜像语义失真"的风险点。
4. 若明天出现"官方 SQL 标准的湖仓表 DDL"，catalog 层会被架空还是强化？
   从 9.6 的策略执行点趋势论证你的立场。
