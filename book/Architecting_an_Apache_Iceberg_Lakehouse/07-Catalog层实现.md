# 07 · Implementing the catalog layer（Catalog 层：REST 规范、十一款生态与场景选型）

> 覆盖原书第 7 章。目录来源：✅ Manning 官方 TOC 实抓：7.1 The role of the catalog（职责/与引擎交互）/
> 7.2 Evaluating catalog requirements（性能可用扩展/元数据治理与血缘/安全合规/部署弹性与生态兼容/
> 成本运维/目录联邦与 mesh）/ 7.3 Apache Iceberg REST Catalog specification（7.3.1 规范出现之前、
> 7.3.2 解决方案）/ 7.4 Catalog options（Hadoop、Hive、JDBC、Apache Polaris、Project Nessie、
> Apache Gravitino、Lakekeeper、AWS Glue Data Catalog、Dremio catalog、Snowflake Open Catalog、
> Databricks Unity Catalog）/ 7.5 Choosing the right catalog（八个场景）/ 7.6 Catalog-based access control。
> 本章对应 02 章五层的"entry point"，是全书生态信息密度最高的一章。

## 本章地图

| 小节 | 内容 | 结论（一句话） |
| --- | --- | --- |
| 7.1 | catalog 职责契约 | 表名→元数据位置的注册/发现/授权服务；CAS 提交的地主 |
| 7.2 | 六族要求 | 可用性、治理血缘、安全、部署弹性、成本、联邦——catalog 是治理策略的宿主 |
| 7.3 | REST Catalog 规范 | 把"目录"从各家私有接口升格为开放协议——生态解耦的支点 |
| 7.4 | 十一款选项 | 三个内置轻量件（Hadoop/Hive/JDBC）+ 四个开源服务（Polaris/Nessie/Gravitino/Lakekeeper）+ 四个商业托管（Glue/Dremio/Snowflake Open/Databricks UC） |
| 7.5 | 八场景选型 | 从"Hive 迁移"到"多云联邦治理"，每场景给一条主轴约束 |
| 7.6 | 目录侧访问控制 | 权限下沉到 catalog：行列级策略、凭证代发、跨引擎一致 |

## 7.1–7.2 职责与要求（架构读法）

- 职责三件套：**命名**（namespace→table）、**发现**（引擎握手拿 metadata 位置）、**提交仲裁**
  （原子换指针/版本校验——06 章并发吞吐的天花板）。
- 六族要求的实战化追问（承 04 章）：QPS 与 p95（规划期大量 `loadTable`）、高可用等级（目录挂=全湖
  停摆）、权限粒度（表/列/行？）、凭证模型（vended credentials 有无）、跨目录联邦（多 catalog 并存
  怎么统一治理）、部署形态（自管容器/云托管/混合）。

## 7.3 REST Catalog 规范：为什么是"解耦支点"（⚠️ 协议细节转官方规范）

```text
7.3.1 规范之前：Hive metastore  Thrift 绑定、Glue 私有 API、各引擎各写 adapter——
  N 引擎 × M 目录 = N×M 集成税，且提交语义/凭证语义各家自由发挥。
7.3.2 之后：Iceberg REST Catalog 把目录接口标准化（OpenAPI 在册：loadTable/createTable/
  register/updateTable + requirements 前置断言 + vended credentials 载荷），
  N+M 集成：引擎只认 REST，服务端可换件。
  规范文本（✅ 实抓可达）：https://github.com/apache/iceberg/blob/main/open-api/rest-catalog-open-api.yaml
  提交冲突语义收进 requirements（如 assert-ref-snapshot-id）——7.6 的访问控制与 11 章审计
  都以"目录是可审计服务"为前提。
```

- 编者推论：REST 规范的普及度即生态健康度——07.4 十一款里凡标"支持 REST"者才有跨引擎未来 ⚠️。

## 7.4 十一款目录速记（TOC 实抓 ⚠️ 行为转述；2026 版本现状见末节）

| 选项 | 类型 | 一句话定位 |
| --- | --- | --- |
| Hadoop catalog（7.4.1） | 内置 | 纯文件系统目录（metadata 最新版靠约定发现）——demo/Python 轻场景，无并发仲裁保障 |
| Hive catalog（7.4.2） | 内置 | 借 Hive metastore 做注册——存量 Hadoop 资产的过渡桥 |
| JDBC catalog（7.4.3） | 内置 | 一张关系表当目录——小团队自管的最低门槛 |
| **Apache Polaris**（7.4.4） | 开源服务 | Iceberg REST 的参考级实现 + 细粒度权限/凭证置换（IBM 捐赠，ASF） |
| **Project Nessie**（7.4.5） | 开源服务 | Git 式目录：分支/合并/历史——03 章 demo 用它演示"数据版本控制" |
| **Apache Gravitino**（7.4.6） | 开源服务 | 多类型元数据联邦（湖仓+消息+模型），"metalake"  umbrella 思路 |
| **Lakekeeper**（7.4.7） | 开源服务 | Rust 实现的轻量 REST catalog：OAuth2、S3Table 兼容面、低运维足迹 |
| AWS Glue（7.4.8） | 云托管 | AWS 默认目录 + Iceberg REST 兼容端点路线 |
| Dremio catalog（7.4.9） | 商业 | 联邦引擎自带目录，与 reflection 加速绑定 |
| Snowflake Open Catalog（7.4.10） | 托管 | Polaris 的托管化对外形态（"目录即服务"卖进 SF 生态） |
| Databricks Unity（7.4.11） | 托管 | UC 从 Delta 之家扩出 Iceberg REST 支持——生态和解信号 ⚠️ |

## 7.5 八场景主轴（TOC 实抓场景名 ⚠️ 结论按题旨重构）

| 场景（7.5.x） | 决策主轴 |
| --- | --- |
| 中型团队迁 Hive | 兼容成本优先：Hive catalog 起步、REST 目标态、双目录共存窗口 |
| 云原生初创快扩展 | 零运维：云托管 REST（Glue/Snowflake Open）一步到位 |
| 跨国企业严治理 | 权限与审计粒度：Polaris/UC 类企业目录，凭证置换成硬需求 |
| SaaS 求运维简单 | 托管 + 租户隔离能力（namespace-per-tenant 模式） |
| 多云联邦治理 | 目录联邦/mesh（7.2.6 的伏笔）：Gravitino/多 REST 端点聚合 |
| 金融日克隆压测 | 元数据克隆速度：Nessie 分支/快照引用式环境复制 |
| 渐进迁移跨旧系统查询 | catalog + 联邦层配合（08 章）：注册存量、逐域改写 |
| Hadoop+Python 轻量湖 | Hadoop catalog/JDBC + PyIceberg（附录 B/本册 13 章）够用哲学 |

## 7.6 目录侧访问控制

- 权限模型下沉：表/列级 allow-list、行级过滤与列掩码（策略引擎因实现而异 ⚠️）；
- **vended credentials**：引擎拿短时对象存储凭证（05 章安全条的闭环）；
- 审计面：所有 `loadTable/updateTable` 过目录=天然访问日志——11 章访问审计的数据源。

## 常见误区

| 误区 | 纠偏 |
| --- | --- |
| "catalog 只是注册表，换起来简单" | 它承载提交仲裁+权限+凭证——换 catalog=换治理体系；04 章要把它按平台级组件定价 |
| "支持 Iceberg 的目录都等价于 REST 语义" | 各家对规范子集（事务端点/扫描规划/凭证载荷）支持深度不同——用官方 OpenAPI 逐端点验收 ⚠️ |
| "Hadoop catalog 能上生产" | 无集中仲裁的并发提交是已知风险区——它适合单写者/实验（7.4.1 的边界） |
| "Nessie=分支玩具" | 分支是环境隔离/发布管道（write-audit-publish）的底座——11 章审计流程复用 |
| 多目录并存忘了唯一真相 | 同一物理表被两个目录各自登记=双写损坏风险；迁移窗口要有"目录锁"纪律 ⚠️ |

## 与其他章 / 其他书的联系

- 机制层深读（Iceberg catalog 接口与声明式提交）→
  [../Apache_Iceberg活用入門/07-Catalog生态.md](../Apache_Iceberg活用入門/07-Catalog生态.md)；三格式目录横评 →
  [../Engineering_Lakehouses_with_Open_Table_Formats/09-Catalog与互操作.md](../Engineering_Lakehouses_with_Open_Table_Formats/09-Catalog与互操作.md)。
- Spark 侧 catalog 配置逐参数 → [../Use_Iceberg_with_Spark/02-Catalog配置与接入.md](../Use_Iceberg_with_Spark/02-Catalog配置与接入.md)。
- 平台视角的目录职能（与本章互补）→
  [../Practical_Lakehouse_Architecture/04-数据目录.md](../Practical_Lakehouse_Architecture/04-数据目录.md)、
  [../湖仓架构大规模数据平台的设计和实现/04-数据目录.md](../湖仓架构大规模数据平台的设计和实现/04-数据目录.md)；
  企业目录/治理学通识 → 波内 #190 The_Enterprise_Data_Catalog_2e（写作时未落盘，挂点登记 00）。
- 目录与消费层的权限贯通 → [09-消费层与开放接口.md](09-消费层与开放接口.md)；审计运维 →
  [11-运维化-编排审计与容灾.md](11-运维化-编排审计与容灾.md)。

## 核心概念速览（中英对照）

- **Catalog** — 目录：表名→元数据位置的注册/发现/授权/提交仲裁服务（7.1）。
- **REST Catalog 规范** — Iceberg 的目录接口标准：OpenAPI 在册，N+M 解耦的关键。
- **requirements 断言** — 提交前置条件（如 ref 当前快照匹配）：乐观并发的协议化表达。
- **Vended Credentials** — 目录代发的短时存储凭证：引擎不持桶密钥的安全模式。
- **Apache Polaris** — IBM 捐赠 ASF 的 REST catalog 参考实现：细粒度权限/凭证置换。
- **Project Nessie** — Git 式 Iceberg catalog：分支/合并/历史，03 章 demo 目录件。
- **Apache Gravitino** — 多类型元数据联邦服务（metalake）：湖仓/消息/模型同伞。
- **Lakekeeper** — Rust 轻量 REST catalog：OAuth2、低运维足迹的自管选项。
- **Glue / Unity / Open Catalog / Dremio catalog** — 四大商业目录：云绑定点与目录策略的杂交面。
- **目录联邦** — Catalog Federation/Mesh：多目录统一寻址与治理——7.2.6/7.5.5 的前沿题。
- **Write-Audit-Publish** — 写入-审计-发布：借分支语义实现的数据发布管道。
- **Namespace-per-Tenant** — SaaS 多租户的目录布局模式。

## 最新演进与工业实践

（2025–2026 实查，全部带核验链）

- **版本现状（✅ 2026-09-27 GitHub API 实抓）**：Polaris 主仓持续活跃（`apache/polaris`，最近推送
  2026-09-27，https://github.com/apache/polaris 200、官网 https://polaris.apache.org/ 200；毕业具体
  时点 ⚠️ 未逐文核，以 ASF 公告为准）；**Lakekeeper v0.13.6**（2026-09-22，
  `https://api.github.com/repos/lakekeeper/lakekeeper/releases/latest` ✅，仓库 https://github.com/lakekeeper/lakekeeper 200）；
  **Nessie nessie-0.108.8**（2026-09-09，https://projectnessie.org/ 200）；**Gravitino v1.3.0**
  （2026-06-29，https://github.com/apache/gravitino 200）。
- **REST 规范演进（✅）**：OpenAPI 文本在 `apache/iceberg` 仓库 `open-api/rest-catalog-open-api.yaml`
  在册；本书附录 C.4 覆盖的配置端点/OAuth2/扫描规划端点等条目，落地时以当期 yaml diff 为准 ⚠️。
- **商业托管化**：Snowflake Open Catalog（Polaris 托管形态）与 Databricks UC 对 Iceberg REST 的
  支持（7.4.10/7.4.11）使"目录即服务"在 2025–2026 成为大厂标配——自管 vs 托管的 7.2.5 成本天平
  逐年右移 ⚠️（作者同题综述 ✅ https://dev.to/alexmercedcoder/the-state-of-apache-iceberg-catalogs-in-june-2026-265e）。
- **盘上互读**：本章十一款速记与活用入門 07 章（规范+服务端两层）互补——它讲协议怎么工作，
  本章讲服务怎么选；DUAR/DuckDB 侧的 catalog 消费形态（ATTACH TYPE ICEBERG 的 REST 路线）→
  [../DuckDB_Up_and_Running/09-云端DuckDB与MotherDuck.md](../DuckDB_Up_and_Running/09-云端DuckDB与MotherDuck.md)。
