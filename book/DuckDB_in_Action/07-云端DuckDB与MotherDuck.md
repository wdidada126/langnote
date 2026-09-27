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
