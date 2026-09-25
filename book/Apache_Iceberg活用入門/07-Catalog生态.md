# 第 7 章 Catalog 生态：Hive / Glue / JDBC / Nessie / REST

> ⚠️ 章题为**推定**（示意日文名：カタログの仕組み），原书真实目录未核实，见 [00-总览与阅读地图.md](00-总览与阅读地图.md)。
> 依据：官方 `docs/rest-catalog.md`、`docs/hive.md`、`docs/aws.md`、`docs/nessie.md`、`docs/jdbc.md` 与 REST Open API / 提交协议（已核对 REST 文档的「单一客户端对接任意合规服务端」「OAuth2 token/credential」表述）。

## 本章地图

> 一句话：**catalog 是 Iceberg 的「事务仲裁者 + 命名服务」：它存表指针、发号提交、管命名空间；选 catalog 等于选原子提交协议与权限模型。REST 规范让这一切第一次可以跨云复用。**

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 7.1 catalog 到底管什么 | 命名/指针/提交 CAS/（可选）凭证 | 三个接口面：Catalog、SessionCatalog、TableOperations |
| 7.2 内置实现一览 | hadoop/hive/glue/jdbc/nessie/rest | 能力与原子性强弱对照表 |
| 7.3 REST Catalog | 端点、requirements+updates、OAuth2 | 「一套客户端 ↔ 任意服务端」 |
| 7.4 Polaris/Lakekeeper 等服务端 | 第三方 REST 实现 | 规范与产品两层要分开 |
| 7.5 分支/标签/WAP | refs 字段 + 过程面 | 数据侧的 Git 化从这里起步 |
| 7.6 选型 | 云绑定度/运维成本/多引擎 | 2025+ 默认答案：能用 REST 用 REST |

## 核心精讲

### 7.1 职责清单

1. **命名服务**：`namespace（db）→ 表 → 当前 metadata 文件路径`，外加 create/drop/rename/register；
2. **提交仲裁**：`TableOperations.commit(base, metadata)` 的 CAS（第 6 章的心脏）；
3. **（部分实现）额外元数据**：表属性、权限委托、凭证 vending（Glue/REST）；
4. **不负责**：数据文件内容、快照列表、schema——那些全在 metadata 文件里（§2.2），所以「catalog 挂了，已缓存根路径的读仍可行」。

Java API 的三面：`Catalog`（加载/建表）、`SessionCatalog`（引擎会话/USE 语义）、`TableOperations`（提交协议）；自定义实现门槛不高（`docs/custom-catalog.md`），但**必须保证 commit 的原子与线性化**，否则一切白搭。

### 7.2 内置实现对照

| catalog | 指针存在哪 | 提交 CAS 原语 | 特点/风险 |
| --- | --- | --- | --- |
| `hadoop` | 文件系统目录 + `version-hint.text` | rename | **零依赖**；官方定位为测试/单写者，不抗并发——别上生产 |
| `hive` | HMS 表参数（metadata_location） | rename 约定 + 重试 | 最普及、与存量 Hive 生态共元数据；HMS 无强 CAS，历史上并发提交有坑（新版靠重试+校验），跨引擎共享同一 HMS 时注意版本 |
| `glue` | Glue Data Catalog 表版本 | `UpdateTable` 的 `version` 条件 | AWS 托管；受 Glue API 限流影响大，高频小提交场景要盯配额；支持凭证 vending |
| `jdbc` | JDBC 表（表名→metadata 路径+版本列） | 数据库事务 | 自带强 CAS、易自托管；命名空间能力简单 |
| `nessie` | **版本控制系统**（commit 图） | 内容寻址提交 | 表集合整体版本化：分支/合并/回滚跨越单表（§7.5 之外的「仓库级时间旅行」）；运维一个专门服务 |
| `rest` | 服务端背后（任意） | **协议化**：requirements+updates | 见 §7.3；引擎侧只需一个 REST 客户端 |

### 7.3 REST Catalog：把提交协议写进 HTTP

设计初衷（官方文档原话大意）：**「一套客户端实现适用于任意合规服务端」**——引擎不再为每个目录服务写连接器。

- **配置面**（Spark）：`type=rest`、`uri=https://.../iceberg`、`warehouse=<prefix>`；Flink：`'catalog-type'='rest'` + `uri`（已核对 flink-connector 文档的配置方式）；
- **命名空间端点**：`GET /v1/namespaces`、`POST /v1/namespaces`、`.../namespace/{ns}` 等 CRUD；
- **表端点**：`loadTable`（直接返回 metadata JSON，省一跳）、`createTable`、`dropTable`、`renameTable`、`registerTable`、`listTables`；
- **提交**：`POST /v1/.../tables/{t}` 的 body = **`requirements[]` + `updates[]` 的声明式对**：requirements 是「我以为世界是什么样」（assert-ref-snapshot-id：`main` 必须指向快照 X），updates 是「我要世界变成什么样」（add-snapshot、set-snapshot-ref、assign-uuid、upgrade-format-version…）。服务器仲裁：不满足即 409，客户端刷新后重放（第 6 章的协议化）；
- **认证**：OAuth2 —— 初始化用 `credential`（`client_id:client_secret`）换 token，或自带 `token`；令牌过期自动刷新；官方明确警告凭据字段须做日志脱敏（rest-catalog 文档原文）；
- **凭证 vending 🔧**：`loadTable`/`createTable` 响应可携带临时对象存储凭证（`config` 映射 + per-table 凭证），引擎免持长期 AK/SK——这是「集中式数据访问治理」的关键抓手（实现相关，规范提供扩展位）。

**prefix** 允许一个服务端承载多租户/多目录（`/v1/namespaces` 前缀隔离）。

### 7.4 服务端实现：规范与产品的两层

- ⚠️ 核实状态：以下服务端信息**未能逐一从官网核实**（本环境网络受限），仅给出口径，采用前请自查文档。
- **Apache Polaris**（2024 入 Apache 孵化，源自 Snowflake 贡献）：完整 REST 实现 + RBAC、细粒度权限、凭证 vending、多仓库；
- **Lakekeeper**（独立开源项目）：轻量 Rust 实现的 REST catalog，常见于自建湖仓；
- **Onehouse / Dremio / Tabular（Salesforce）**：商业化 REST/catalog 平台（Tabular 创始团队即 Iceberg 主要作者背景）；
- **云托管映射**：AWS Glue 的 Iceberg REST endpoint、Azure Fabric/Databricks、GCP BigLake 等各自提供 REST 兼容面（成熟度/兼容性矩阵请以各家 2026 年文档核对）。

一句话：**Iceberg 生态的「目录层竞争」已经从实现库转移到 REST 服务端与权限治理**——学规范里的协议，比背某产品的私有 API 保值。

### 7.5 refs：分支、标签与 write-audit-publish

根文件 `refs` 字段（§2.2）：`{name → {snapshot-id, type(branch|tag), retain/max-reference-age}}`。`main` 只是默认分支。能力面：

```sql
CALL sys.create_branch('db.t', 'audit-2024-06', snapshot_id => 58504…);
CALL sys.create_tag('db.t', 'release-v1', 58504…);
-- WAP（write-audit-publish）流程：
CALL sys.create_branch('db.t', 'wap123', 'main');
INSERT INTO t FOR VERSION AS OF wap123 ...;          -- 写到分支
-- 外部审计…
CALL sys.fast_forward('db.t', 'wap123', to => 'main');  -- 审核通过后主干快进（原子换 main 指针）
CALL sys.publish_changes('db.t', wap_id => 'wap123');   -- Spark 扩展的封装过程
```

- 读分支：`SELECT ... FROM t VERSION AS OF 'audit-2024-06'`；
- **branch/tag 影响保留**：expire 不会删被 refs 引用的快照（retain 策略可各自设定），第 8 章窗口计算要把 refs 算进去；
- Nessie 则是「仓库级分支」，与表级 refs 是互补的两层抽象（§7.2）。
- 分支/标签的过程 API 在 1.4+ 逐步齐备；🔧 更细的 tag/branch SQL（`ALTER TABLE ... CREATE BRANCH`）依引擎而异。

### 7.6 选型决策树（2026 口径）

```text
全栈某云且不想自运维？ → 云的托管 catalog（Glue/BigLake/Fabric…）但要读其限流/权限模型
存量 HMS、多引擎混读？  → hive catalog（过渡方案；接受其并发与耦合债）
要权限治理/跨云/凭证 vending？ → REST（Polaris/Lakekeeper/云托管 REST）
需要「整个数据湖可分支」？   → Nessie
学习/试验              → jdbc（比 hadoop 更接近真实并发语义）或 docker 起的 REST 演示服务
```

与「湖仓架构中的 catalog」宏观讨论对照：[../湖仓架构大规模数据平台的设计和实现/04-数据目录.md](../湖仓架构大规模数据平台的设计和实现/04-数据目录.md)。

## 版本演进与兼容性

- REST 规范：2022 首发 Open API（v0.x 迭代）→ 1.4（2023）OAuth2 与多前缀完善 → 1.5–1.9（2024–2025）async table commit（202）、register/claims、bearer 认证细节、关系端点等持续修订——**客户端/服务端版本配对**要看双方 release notes，本目录未逐项核实；
- 各引擎 connector 的 catalog 列表（第 9 章）随版本变；Flink 1.16+ 才补齐主流 catalog；Hive catalog 对 Flink/Spark 行为一致性历史上是兼容性问题多发区；
- 🔧 Glue 已提供 Iceberg REST 兼容端点；跨云迁移时优先把 catalog 换成 REST 层是 2025–2026 的普遍做法（口径性陈述）。

## 常见误区

| 误区 | 事实 |
| --- | --- |
| 「catalog 只是元数据的目录，换个没影响」 | 换 catalog = 换提交协议与权限模型；Hadoop→Hive 迁移官方过程 `add_files`/`register_table` 只搬登记，不搬历史语义 |
| 「REST catalog 会自己存快照列表」 | 表状态全在 metadata 文件；服务端通常只存指针+做仲裁（有的服务端也缓存元数据，实现细节） |
| 「分支要复制数据」 | branch 只是命名指针，零复制（Git 分支的类比在 refs 上成立） |
| 「有分支就不用 WAP 工具了」 | WAP 的价值在「写→审计→快进」的规程与过程封装，不是指针本身 |
| 「HMS 慢所以不是好 catalog」 | 真痛点是并发 CAS 弱与耦合；性能问题另有元数据缓存与 `all-properties` 面 |
| 「REST = 一定安全」 | 认证、审计、vending 的实现由服务端负责；规范只保证协议可表达 |

## 与其他章 / 其他书的联系

- 7.1 的「指针 + CAS」= 第 6 章提交协议的另一半：[06-ACID与乐观并发控制.md](06-ACID与乐观并发控制.md)；refs 在根文件中的定义：[02-元数据三层结构.md](02-元数据三层结构.md) §2.2。
- expire 与 refs 保留的交互：[08-表维护操作.md](08-表维护操作.md)；各引擎 connector 配置：[09-Spark_Flink_Trino实战.md](09-Spark_Flink_Trino实战.md)。
- 姊妹目录：[../Use_Iceberg_with_Spark/02-Catalog配置与接入.md](../Use_Iceberg_with_Spark/02-Catalog配置与接入.md)、[../Engineering_Lakehouses_with_Open_Table_Formats/09-Catalog与互操作.md](../Engineering_Lakehouses_with_Open_Table_Formats/09-Catalog与互操作.md)。
- catalog 在治理全景中的位置：[../湖仓架构大规模数据平台的设计和实现/06-湖仓架构中的数据与AI治理和安全.md](../湖仓架构大规模数据平台的设计和实现/06-湖仓架构中的数据与AI治理和安全.md)。

## 思考题

1. 为什么「catalog 挂掉」时已加载根文件的会话仍能读、却不能提交？这暴露了职责的哪条分界？
2. `requirements: assert-ref-snapshot-id(main, 58504)` 失败返回 409，客户端该重放还是重算（对照 §6.4）？
3. 用 JDBC 自建 catalog 和用 Nessie，「回滚整库到昨天」各自怎么做？
4. Glue 限流为什么在「高频小批量提交 + expire 并发」场景特别容易踩？（结合第 6/8 章。）
5. WAP 快进与直接 `set_current_snapshot` 的区别是什么（提示：基校验）？
