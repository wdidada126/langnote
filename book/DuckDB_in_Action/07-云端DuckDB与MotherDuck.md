# 07 · DuckDB in the cloud with MotherDuck（云端 DuckDB：MotherDuck）

> 覆盖原书第 7 章。目录来源：✅ Manning 官方 TOC 实抓。本章解决 DuckDB 的天然短板——**单机、单进程、无协作**：MotherDuck 把同一引擎接到云上，本地与云共享一个连接字符串宇宙（`md:`）。

## 内容规格（小节地图，✅ 实抓）

- **7.1 Introduction to MotherDuck**：7.1.1 How it works——"查询在云、协调在本地"的混合执行：plan 下推到 MotherDuck 集群，结果以 Arrow 流回本地；也可 `ATTACH 'md:'` 后云表与本地表同 SQL 联查；7.1.2 Why——协作/算力/托管存储，仍保留 DuckDB 开发心智。
- **7.2 Getting started**：7.2.1 Web UI（notebook + SQL + 数据集浏览）；7.2.2 令牌认证：`duckdb 'md:'`（浏览器 OAuth 或 ` MotherDuck_TOKEN` 环境变量），CLI/Python 一行切换本地↔云。
- **7.3 Making the best possible use**：7.3.1 上传本地库（`CALL md_upload_db`/UI 拖拽/逐表复制）；7.3.2 云端建库建表；7.3.3 **共享**（share database/私有读链接，组织内协作）；7.3.4 S3 secrets 管理 + 直读云桶（`CREATE SECRET (TYPE S3 ...)`，httpfs）。

## 核心技术清单

- 混合架构：DuckDB 进程做客户端/部分执行，MotherDuck 集群做重扫描；查询透明拆分（"hybrid execution"）。
- `md:` 连接串 + `motherduck_attach_db` 语义：云库与本地文件在同一 catalog 里 JOIN。
- Token 认证流：OAuth 浏览器一次 → 本地凭据缓存；CI 用 `MD_TOKEN`。
- Secrets 管理器：`CREATE SECRET` 抽象 S3/R2/GCS/Azure 凭据，替代裸 AK/SK。
- 计费/资源：按算力秒 + 存储量；免费额度适合原书教学。
- UDF/镜像：云端支持 Python UDF 上传（⚠️ 细节版本敏感）。
- AI 查询：书出版后上线 Text2SQL 助手类功能（⚠️ 转述，见下节）。

## 🔧 实测说明

⚠️ **本章不可本机实测**：需要 MotherDuck 账号与云令牌，无离线等价物。仅做的本地可达验证：
- `INSTALL md;`（motherduck 客户端扩展）在 duckdb 1.5.5 可安装（core 扩展 ✅ 本工程实测）；未连接实例，`ATTACH 'md:'` 必然超时失败（未运行）。
- 官方站 https://motherduck.com/ ✅ curl 200。
行为结论全部为转述 + 官方文档口径，标 ⚠️。

## 易错点与陷阱

- **把 `md:` 当"另一个 Postgres 连接串"**：云表 JOIN 本地 10 GB 表会把本地数据上行/把云结果下行——网络成为新瓶颈；重活要留在云端（本地表先 `COPY TO parquet` 上桶）。
- **令牌环境变量名**：不同 SDK 版本用 `MD_TOKEN`/`motherduck_token`，CI 里静默回落到交互式 OAuth 直接挂死——显式传 token。
- **云/本地版本漂移**：MotherDuck 引擎版本与本地 duckdb 补丁版本可能差 1–2 个 release，SQL 方言/扩展行为有差异；报告"能跑/不能跑"先对齐 `PRAGMA version` 两边。
- **上传库 ≠ 实时同步**：`upload` 是一次性快照，之后两边分叉；持续管道应写 Parquet/表到云上库而非反复传文件。
- **共享权限粒度**：database 级 share 与表级授权语义在不同套餐不同；按书的演示口径设计生产权限会出安全事故 ⚠️。
- 成本侧：混合执行把"本地免费算力"的账挪到云算力秒——大扫描在 UI 上很便宜、账单上很诚实 ⚠️（转述）。

## 关键对象与配置速查

| 对象/配置 | 用途 |
| --- | --- |
| `duckdb 'md:'` / `duckdb.connect("md:")` | 连接 MotherDuck 默认仓库 |
| `ATTACH 'md:dbname' AS d` | 指定云库 |
| `MD_TOKEN` 环境变量 | CI/无浏览器环境的令牌 |
| OAuth 浏览器流 | 本地开发一次登录缓存凭据 |
| `CREATE SECRET (TYPE S3, ...)` | S3/R2/GCS 凭据托管 |
| `CALL md_upload_db(...)` / UI 上传 | 本地库快照上行（⚠️ 签名以当前文档为准） |
| Share（库级共享链接） | 跨账户只读协作 |
| hybrid execution 开关 | 会话级选择本地/云端执行（⚠️ 细节版本敏感） |
| `motherduck` Python 包 | 组织管理/查询历史等扩展面 |
| `INSTALL md` | DuckDB 内客户端扩展（✅ 本机可装） |

## 本章实测边界与方法（诚实交代）

```text
已验（✅，本机 duckdb 1.5.5）:
  con.execute("INSTALL md;")            # core 扩展可安装
  https://motherduck.com/               # curl 200
未验（⚠️，不伪装）:
  ATTACH 'md:' 真实登录/查询/共享/S3 直读 —— 需账号与出网白名单，本机未执行
  md_upload_db 签名、计费数字、AI 助手行为 —— 转述官方口径
等价本地演练（可迁移心智）:
  多进程各自只读打开同一 Parquet 正常；而共享单一 DuckDB 库文件被进程锁拒绝
  （见 12 章并发实测）——这正是 MotherDuck 要解决的"共享层"问题。
```

## 与其他章/本书的互链

- 为什么需要云：单进程互斥 → [12-附录A-客户端API.md](12-附录A-客户端API.md)
- 管道上云：Dagster→MotherDuck 上传一步 → [08-构建数据管道.md](08-构建数据管道.md)
- S3 凭据与 httpfs 直读 → [05-无持久化的数据探索.md](05-无持久化的数据探索.md)
- 开放湖仓替代路线 → [11-结语与未来.md](11-结语与未来.md) 的 DuckLake 节
- 阅读顺序建议：先 12 章（并发约束）再回本章，"共享层为什么值钱"一目了然。

## 思考题（合上笔记再答）

1. `md:` 连接下本地 Parquet 和云表 JOIN，数据往哪边搬？代价是什么？（本地扫描结果上行/云侧下行，瓶颈变网络；重活留云端）
2. 为什么 CI 里必须用 `MD_TOKEN` 而不是复用 OAuth 缓存？（无浏览器；交互式 fallback 直接卡死流水线）
3. MotherDuck 与 DuckLake 都会进你的选型表，一句话区分。（前者"托管的 DuckDB 计算+存储"，后者"开放湖格式+自带 SQL 目录"，引擎可换）
4. 书里 7.3.4 的 S3 直读与本章"上行/下行"有什么关系？（凭据托管解决"能不能读"，混合执行决定"在哪儿读划算"——大表应在云端有副本）

## 2026 视角补注

- 本章的 `md:` 心智在 2026 年已经"平庸化"：多 IDE/CLI 默认带 MotherDuck 入口，团队治理（RBAC/审计/成本标签）成为新的选型焦点 ⚠️（转述）。
- 书里"上传本地库"的教学路径，在生产里通常被"dlt 直接双写本地+云"（08 章）替代——一次性上传是迁移工具不是集成模式。
- 7.3.4 的 S3 secrets 姿势在今天被 DuckDB `CREATE SECRET` 管理器统一（S3/R2/GCS/Azure 四方言同构），书中"裸凭据入 SQL"的写法要按新语法改写再照搬 ⚠️。
- 混合执行的账单心智：本地免费算力 vs 云端算力秒，把"哪些表值得上行"当作数据布局设计题来做。
- 与开源侧的合流趋势：DuckDB 社区把 `md:` 纳入 core 扩展（✅ 本机 INSTALL 成功），意味着"云接入"不再是外挂而是标准件。
- 给系列读者的定位一句话：07 章讲的是"DuckDB 的中心化泄压阀"，11 章的 DuckLake 是"去中心化共享层"——两者共享同一引擎、争夺同一批中小客户，选型前先想清楚目录与凭据归谁。
- 安全侧补课：云令牌最小权限（库级 token 而非账户级）、共享链接过期时间、以及"上传即离开本机掌控"的合规评审，都是原书未展开、2026 年必答的题 ⚠️（实践判读）。

## 本地 ↔ 云能力对照（本章速记）

| 能力 | 本地 DuckDB | MotherDuck |
| --- | --- | --- |
| 多人共享同一库 | ✗（进程独占，12 章实测） | ✓ 托管目录+share |
| 权限/审计 | ✗（仅文件权限） | ✓ 组织级 RBAC ⚠️ |
| 大扫描算力 | 单机核数封顶 | 弹性集群 |
| 离线/演示 | ✓ 零网络 | ✗ 需出网与令牌 |
| 成本模型 | 电费 | 算力秒+存储 |
| 学习曲线 | 即本书 01–06 | 本书 01–06 + 一把令牌 |

## 核心概念速览（中英对照）

- **混合执行** — Hybrid execution：同一查询在本地与云集群间自动分工。
- **md: 连接串** — `md:` URI：DuckDB 客户端识别 MotherDuck 的方言前缀。
- **令牌认证** — Token auth：OAuth 或环境变量 `MD_TOKEN` 的无密码登录。
- **Secrets 管理** — Secret manager：`CREATE SECRET` 托管对象存储凭据。
- **数据库共享** — Share：跨账户只读协作对象。
- **托管目录** — Managed catalog：云端维护的库/表元数据服务。
- **上行/下行传输** — Ingress/egress：混合执行的网络搬运成本。
- **Notebook UI** — 云端 SQL+可视化协作界面。
- **Text2SQL 助手** — AI query：自然语言转 SQL 的云端功能（成书后新增 ⚠️）。
- **serverless 数仓** — Serverless warehouse：无集群运维、按用计费形态。

## 最新演进与工业实践

- **MotherDuck 客户端已是一等公民**：`md:` 作为 core 扩展进入 DuckDB 官方扩展仓库（1.1 起，✅ 本机可 INSTALL；版本线参照 https://github.com/duckdb/duckdb/releases ✅ API 实抓）。
- **产品面扩张（2024–2026，⚠️ 转述自官网口径）**：AI 助手（自然语言查询）、Fusion 协作笔记本、S3 直读写与增量摄取；官网 https://motherduck.com/ ✅。
- **竞争格局**：2026-04 DuckLake 1.0 发布（✅ https://ducklake.select/2026-04-13/ducklake-10/）给出"开放湖仓 + 任意引擎"路线，与 MotherDuck 的"托管云 DuckDB"路线形成互补/竞争张力——企业开始按"目录归属权"选型（定性判断，两来源各自 ✅ 可核）。
- **工业实践**：dbt/Dagster + `md:` 已成为"本地开发、云端跑数"的主流双环境模式（书第 8 章管道的云化延伸；⚠️ 社区口径）。
