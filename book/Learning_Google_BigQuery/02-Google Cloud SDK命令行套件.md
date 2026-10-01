# 02 gcloud/bq/gsutil 命令行套件（Google Cloud SDK）

> 对应原书 **Ch.2 "Google Cloud SDK"**（章题与节级目录 ✅ QQ 阅读电子版实抓）。
> 正文为**精读重构**，非原书文本；机制描述「官方文档转述 ⚠️」；`docs.cloud.google.cn` URL 2026-10-02 亲测 200（✅）。本章无 🔧 实验。

## 本章在本书中的位置

Ch.1 用浏览器"见效"，Ch.2 立刻把读者推到命令行：装 SDK、认识 gsutil/bq/gcloud 三件套，再用它们去连 Cloud SQL、导出数据库、甚至部署 App Engine。这是全书法式最重、**过期也最快**的一章——2017 年 SDK 安装还是"下载 zip 解包改 PATH"，今天是单一 installer + `gcloud components` 自管理；但 `bq` 命令的动词表（mk/ls/cp/query/load/extract）**十年未变**，这章的核心资产至今可背。

## 2.1 安装 Cloud SDK（Installing Google Cloud SDK：Windows/macOS/Linux 三节）

- 书中路径：官网下载对应平台包 → 安装 → `gcloud init` 配置账户与默认项目 → 把 bin 目录加 PATH（⚠️ 转述当年流程）。
- 三平台差异只在包形态（exe/dmg/tar.gz）与 PATH 写法；书中 Windows 演示用 cmd，作者顺手吐槽了 PowerShell 老版本的兼容问题（叙事重构，未逐字核对 ⚠️）。
- 2026 对账：`curl https://sdk.cloud.google.com | bash` 一代安装脚本已让位于 **google-cloud-cli 安装包/发行版仓库**（⚠️ 转述）；`gcloud init` 与 `gcloud auth login` 仍是日常入口。
- 坑登记：书中强调 **默认项目（default project）决定 bq 命令往哪儿计费**——`gcloud config set project` 忘了设，后面所有 `bq` 操作报 403/404，这是本章例题第一拦路虎（⚠️ 转述 + ✅ https://docs.cloud.google.cn/bigquery/docs/bq-command-line-tool）。

## 2.2 gsutil for Google Cloud Storage

- `gsutil cp/ls/mb/rm` 管 `gs://` 对象；本章用途单一：**把样例 CSV 推上 GCS 给后面的装载例题当弹药**（✅ Ch.1 的 GCS↔BQ 关系）。
- 书中细节（重构）：`gsutil config` 走 OAuth、跨区搬运用 `-m` 并行；凭证文件位置 Win/macOS/Linux 各一（⚠️）。
- 现状：gsutil 已并入 `gcloud storage` 命令组为推荐路径，老命令仍可用（⚠️ 转述）。

## 2.3 bq 工具 for BigQuery（本章心脏）

`bq` 是 BigQuery 专属 CLI，本章给的全动词表至今有效（✅ https://docs.cloud.google.cn/bigquery/docs/bq-command-line-tool）：

```bash
bq mk mydataset                          # 建数据集
bq ls mydataset                          # 列表
bq load --source_format=CSV mydataset.t gs://bucket/*.csv schema.json
bq query --dry_run --use_legacy_sql=false 'SELECT COUNT(*) FROM `p.d.t`'
bq cp mydataset.t mydataset.t_bak
bq extract -c 'gs://bucket/export/*.csv' mydataset.t
bq rm -t mydataset.t
```

- 书中教学顺序与上表一致：mk → load → query → extract，**先建库装载再谈查询**；Ch.4/Ch.5 的分区表例题直接复用本命令面（`bq mk --time_partitioning_type=DAY`）。
- 关键旗标十年考点：`--use_legacy_sql=false`——本书时代 Standard SQL 需显式关 Legacy，2019 后默认已反转（见文末演进节）；`--dry_run` 返回**预计扫描字节**，是"按量计费"的随身计算器（⚠️）。
- `bq ls --all`、`--max_results`、分页 token 等细节书中各一节，今天仍等价（⚠️ 转述）。

## 2.4 gcloud 工具与邻居服务（Using the gcloud utility → Deploying to Google App Engine 五节）

- `gcloud sql` 家族：列实例、代理连接（下节）、`gcloud sql export` 导出 .sql.gz 到 GCS（✅ Ch.1 的中转模式）。
- **Connecting to Cloud SQL using gcloud** + **Connecting using a proxy script**：2017 正解是 **Cloud SQL Auth Proxy**（书里叫 proxy script）本地监听 3306 再连；今天该代理仍是官方推荐通道之一（⚠️ 转述），新增 Private IP/直连-peering 选项。
- **Authorizing the client machine via Google Cloud Console**：客户端授权=生成服务账号密钥 JSON + `GOOGLE_APPLICATION_CREDENTIALS`，此伏笔在 Ch.6 API 章引爆（服务账号正式登场）。
- **Deploying to Google App Engine**：`gcloud app deploy` 收尾演示"SDK 不只管数据"；对本册读者可跳过，但**它证明了 gcloud 的多产品同构体验**——一个 CLI 打天下。

## 2.5 本章的知识资产负债表（重构）

| 到 2026 仍直用 | 已换代 | 需翻译 |
| --- | --- | --- |
| bq 全动词表、--dry_run、dataset/table 命令面 | SDK 安装方式（zip 解包→installer） | proxy script→Cloud SQL Auth Proxy |
| gcloud config/auth 骨架 | gsutil→gcloud storage（并轨） | app deploy 示例运行时版本 |
| 服务账号密钥授权路径 | Legacy SQL 旗标默认值 | Datastore 导出命令面 |

## 2.6 串演一遍：本章命令连成一条流水线（重构自书各节顺序）

把 2.2–2.4 的散点命令按书中例题顺序串起来，就是 Ch.4 之前需要的全部工具面：

```bash
# 0. 一次性配置（2.1）
gcloud auth login && gcloud config set project my-demo-project
# 1. 把样例 CSV 推上 GCS（2.2 + Ch.1 的伏笔）
gsutil mb gs://my-demo-bucket
gsutil cp natality_small.csv gs://my-demo-bucket/
# 2. 建数据集与表并装载（2.3，schema 来自 Ch.3 的类型知识）
bq mk demo_ds
bq load --source_format=CSV demo_ds.natality gs://my-demo-bucket/natality_small.csv schema.json
# 3. 先看账单再运行（2.3 的 dry_run 心法）
bq query --dry_run --use_legacy_sql=false 'SELECT COUNT(1) FROM `my-demo-project.demo_ds.natality`'
bq query --use_legacy_sql=false 'SELECT source_year, COUNT(1) n FROM `demo_ds.natality` GROUP BY 1 ORDER BY n DESC LIMIT 5'
# 4. 结果回写文件（2.3 尾 + extract）
bq extract --destination_format CSV 'demo_ds.natality' gs://my-demo-bucket/out/*.csv
# 5. 邻居侧（2.4）：把 Cloud SQL 的一个库导出到同一个桶
gcloud sql export sql my-sql-instance gs://my-demo-bucket/sqlbak.sql.gz --database appdb
```

- 这条线在本目录 04/05 章被反复复用（分区例题从第 2 步变体而来），**抄写一遍胜过读三遍**；
- 书中未走但今天必走的一步：给 `bq` 设 `--maximum_bytes_billed` 预算闸（配额与成本面 ⚠️ 转述，✅ https://docs.cloud.google.cn/bigquery/docs/bq-command-line-tool 有旗标）。

## 2.7 本章与 Ch.6 的分工（防止读串）

- Ch.2 = **人敲命令**（交互式运维：建、查、搬）；Ch.6 = **程序调 API**（把同批动作嵌进应用）；两章共享同一 REST 面，`bq` 只是它的表亲壳；
- 因此 Ch.2 的每个命令在 Ch.6 都能找到等价作业类型：load→JobConfigurationLoad、query→jobs.query、extract→JobConfigurationExtract——读 Ch.6 前先默写这组映射；
- 今天再加第三个壳：Terraform/声明式（演进节），三者同源同权限模型（IAM/服务账号在 2.4 埋线、Ch.6 引爆）。

## 阅读策略与坑

1. 本章所有命令**今天逐条可跑**（装 gcloud 免费 CLI 即可；查询计费用 `--dry_run` 零成本验证）——Packt 书的例题保鲜度由此章撑起；
2. 书里 Windows 路径分隔符与 GCS URI 混用处（`gs://` 用正斜杠），照抄会翻车，注意甄别；
3. `bq query` 多行 SQL 在 cmd/PowerShell 的引号转义是书中踩过并吐槽的点（重构 ⚠️），今天建议用 `--command_file`；
4. 本章没讲 **bq script（脚本模式，`bq query --nary_script_mode`/`bq script`）**，那是书后的世界（⚠️ 转述），进阶见 TDG 开发章 [../Google_BigQuery_TDG/05-使用BigQuery进行开发.md](../Google_BigQuery_TDG/05-使用BigQuery进行开发.md)。

## 2.8 学完本章的自测四题

1. `bq` 忘了设默认项目，报错长什么样、改哪条配置？（403/404 家族，`gcloud config set project`）
2. `--dry_run` 与 `--maximum_bytes_billed` 一个管看、一个管拦——各自命令面写法？（前者估字节、后者超限直接拒跑 ⚠️）
3. gsutil 的现代替代命令组？（`gcloud storage`，并轨过渡中 ⚠️）
4. 服务账号 key 在 2017/2026 的角色差异？（当年的标准答案、今天的头号反模式——见演进节）

## 核心概念速览（中英对照）

| 中文 | 英文 | 一句话 |
| --- | --- | --- |
| 云开发工具包 | Google Cloud SDK | gcloud/gsutil/bq 的发行载体 |
| 初始化配置 | gcloud init / config | 定账户与默认项目 |
| 对象存储命令行 | gsutil | gs:// 世界的 cp/ls |
| BigQuery 命令行 | bq tool | 数据集/表/装载/查询/导出 |
| 试运行 | dry run | 不执行只报扫描量 |
| 旧版 SQL 旗标 | --use_legacy_sql | 本书时代需显式 false |
| 批量装载 | bq load | GCS 文件→表 |
| 表导出 | bq extract | 表→GCS 文件 |
| SQL 代理 | Cloud SQL Auth Proxy | 本机端口隧道连托管库 |
| 服务账号密钥 | service account key JSON | 机器身份的程序化授权 |
| 应用部署 | gcloud app deploy | PaaS 发布演示 |
| 数据库导出 | gcloud sql export | SQL 实例→GCS 备份 |

## 最新演进与工业实践

- **SDK 本体**：安装从"下载解包改 PATH"进化为平台化 installer + 自动组件管理；`gcloud storage` 取代 gsutil 成为推荐命令组（⚠️ 转述）。
- **bq 的边界扩大**：新增 `bq rm -r --and_snapshot`、物化视图 `bq update --materialized_view`、容量 `bq reservation` 组（✅ 概念见 https://docs.cloud.google.cn/bigquery/docs/reservations-intro；逐条命令 ⚠️ 转述）。
- **认证趋势**：长期有效的 JSON key 被 Google 官方点名"尽量避免"，推荐**直接绑定服务账号 / Workload Identity Federation / ADC 元数据**（⚠️ 转述）——书中 2.4 的密钥文件流程今天属"能跑但不推荐"。
- **工程实践**：命令行章节的现代化对应物是**基础设施即代码 + CI 里跑 bq dry_run 做成本门禁**（估算扫描字节超阈值即 fail PR）；这是 2017 书里没有、2026 标配的一环（⚠️ 通识转述）。
- 与盘上互链：TDG 册把 CLI/客户端讲成"BigQuery 工具链"（[../Google_BigQuery_TDG/05-使用BigQuery进行开发.md](../Google_BigQuery_TDG/05-使用BigQuery进行开发.md)），BQDW 册从项目角度谈 SDK 治理（[../BigQuery_for_Data_Warehousing/02-数据盘点与成本管控.md](../BigQuery_for_Data_Warehousing/02-数据盘点与成本管控.md)）；本册这章是**肌肉记忆层**。
