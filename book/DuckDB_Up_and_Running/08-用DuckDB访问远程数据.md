# 08 · Accessing Remote Data using DuckDB（用 DuckDB 访问远程数据）

> 覆盖原书第 8 章。目录来源：✅ 官方示例文件 `Chapter_8.ipynb` 标题实抓。httpfs 把"对象存储/HTTP 资产"变成本地文件：本章从远程 CSV/Parquet 直读讲到 **HuggingFace 数据集直查**（`hf://`，含私有仓库双鉴权法）——是全书"湖仓最小入口"章。

## 内容规格（小节地图，✅ 实抓自官方示例 notebook）

- **DuckDB's httpfs Extension**：`INSTALL httpfs; LOAD httpfs;`——notebook 原注：支持 **HTTP、HTTPS 与 S3 API endpoint** 直读（✅ 注释实抓）。
- **Querying CSV and Parquet Files Remotely**：**Accessing CSV Files** / **Accessing Parquet Files** 两节：`read_csv_auto('https://…')`、`read_parquet('https://…')`。
- **Querying Hugging Face Datasets**：三子节 ✅——**Reading the Dataset using hf:// Paths**、**Accessing Files Within a Folder**、**Querying Multiple Files Using the Glob Syntax**。
- **Working with Private Hugging Face Datasets**：两鉴权子节 ✅——**CONFIG provider method**（`~/.duckdb/config.ini` 挂 `hf_token`）与 **CREDENTIAL_CHAIN provider method**（provider 链回落环境变量）。

## 核心技术清单

- 远程面：`https://`、`s3://`（含任意 S3 兼容 endpoint）、`hf://datasets/<org>/<ds>@<rev>/…`；凭据面：`CREATE SECRET`（TYPE HF / S3）、config.ini、`HTTPCLIENT` 底层复用 curl 生态。
- **footer 先行**：Parquet 远程读只拉元数据+命中 row group，配合谓词下推把"过湖查询"压到最小 IO。
- 文件编目：本地/对象存储 glob 与 `union_by_name`；HTTP 侧受"不可列举"限制（实测，见下）。
- 缓存三件套：`http_max_retries`、`enable_http_logging`、以及把远程当"冷层"先 `COPY TO` 本地化再反复查（本章数据的标准作业）。
- 与 02 章同一张读函数表，只多了 scheme；与 09 章共享"远端即 catalog"的世界观。

## 🔧 实测（1.5.5 + httpfs 827222f；目标=本书官方示例仓库的 raw.githubusercontent 资产）

1. **安装**：`install+load httpfs` **0.55 s**（已缓存态）；对照冷装：iceberg 24.47 s、spatial 23.53 s、excel 9.63 s、ducklake 0.43 s（均 ✅）。
2. **单文件直读** ✅：`read_parquet('https://…/airports.parquet')` → **322 行 / 0.89 s**（含 TLS 冷启动）；`read_csv_auto('https://…/airports.csv')` → 322 行 ✅；`read_json_auto('https://…/json1.json')` → 3 行 / 1.57 s ✅。
3. **HTTP glob 双重坑** ✅：①默认直接拒：`Globs (*) for generic HTTP file are not supported. Consider SET allow_asterisks_in_http_paths = true`；②开启后仍 404——纯 HTTP **无列举能力**，`year=2015/month=*/*.parquet` 被当字面量 GET。
4. **显式文件列表** ✅：把 12 个月 parquet 拼成 `read_parquet(['url1',…,'url12'])` → **5,819,079 行 / 23.68 s（冷，≈ 含 144 MB 级下载）**；同列表 warm 复跑聚合 Top-3 航司 `[WN 1,261,855 / DL 875,881 / AA 725,984]` **4.04 s**。
5. **单月裁剪** ✅：`month=06/flights.parquet` 直读 **503,897 行 / 2.08 s**、平均出发延误 13.99 min——"按月分区=免费谓词裁剪"的现场证明（对比第 4 条全量）。
6. **本地化再查**：同 12 文件 `COPY TO 'flights2015.parquet'` 物化 144 MB（一次冷跑），后续所有分析章（03/05/09）都吃这份缓存——本章工作流的正确姿势。
7. **hf:// 与私有仓库**：`hf://` 路线与两鉴权法为 **⚠️ 文档转述**（本机未配 HF token、不验证私有仓库；公开数据集可等价改用 `https://huggingface.co/datasets/…/resolve/…` 资产 URL，模式与第 2 条同构）。
8. **自造分区湖回环（消费侧）** 🔧：02 章实测 8 用 `PARTITION_BY` 产出的 `pout/AIRLINE=XX/` 14 分区树，`read_parquet('pout/*/*.parquet', hive_partitioning=1)` 回读 **5,819,079 行 / 0.02 s**——"分区=免费谓词"的生成端与消费端在本目录同机闭环；远程版只是把路径换成第 4 条那种 URL 清单。

## 易错点与陷阱

- **HTTP ≠ 对象存储**：`s3://` 有 ListObjects，`*` glob 与 Hive 分区直读都好使；裸 HTTP 只能枚举**你自己给的文件清单**（实测 404）——给远程湖写查询前先想 scheme。
- **`allow_asterisks_in_http_paths` 是误导开关**：它只是允许把 `*` 送进路径拼接，不赋予列举能力——报错文案里的建议在该场景救不了你（实测）。
- **冷启动时延不是引擎问题**：0.89 s 读 322 行几乎全是 TLS+网络；同文件 warm 与本地 parquet 差两个数量级（本地 count 0.01 s 级）——给远程基准要分 warm/cold 两报。
- **重试与幂等**：高并发远程扫描吃 429/5xx，`http_retries` 调优 + 本地缓存层（第 6 条）才是稳态。
- **token 进 SQL**：`CREATE SECRET` 与 config.ini 别把 token 写进共享 notebook 单元格——本章"CONFIG/CREDENTIAL_CHAIN"两小节的本质就是**凭据与查询分离**。
- **range 请求支持面**：footer 尾部优先读要求服务端支持 `Range`（GitHub raw 支持 ✅；某些 CDN/代理不支持会退化为全文件拉取——看流量诊断）。
- **Range 退化是静默的**：不支持 `Range` 的服务器不会报错，只会整文件慢慢传——远程 parquet"变慢不报坏"，必须靠 cold/warm 双口径基准兜住（陷阱 3 的同源纪律）。
- **URL 清单就是配置**：实测 4 的 12 文件列表硬编码进单元格，上游改名/增月不会全废——清单模板化 + 首步 count 审计（性能模型节第 2 步）是防呆标配。

## 远程直读性能模型（本章实测的三档抽象）

| 档 | 322 行 airports | 50 万行单月(06) | 580 万行全量 12 文件 |
| --- | --- | --- | --- |
| 冷（TLS+字节搬运） | 0.89 s（实测 2） | 2.08 s（实测 5） | 23.68 s（实测 4） |
| 温（连接/缓存复用） | — | — | 4.04 s（实测 4 warm） |
| 本地化后 | 0.00 s 级（05 章 spatial） | 0.01 s 级 | 0.007–0.06 s 级（02/03/05 章） |

- 读法：冷跑常数项在**网络不在引擎**（0.89 s 只为了 322 行）；"查一次远程、物化多次"把常数摊薄进未来每条查询——本表就是实测 6 工作流的价格标签。
- 谓词裁剪改的是分子：`month=06` 只拉 1/11.5 字节；footer+命中 row group 的 IO 模型下，**分区越多、清单越准，远程越接近本地**。

## 把远程湖接进本地分析的三步（本章实测动作化）

1. **列**：拿到文件清单（`['url1',…,'url12']`；HTTP 无列举——实测 3；S3 系有 ListObjects 可跳此步直接 glob）。
2. **量**：先对清单跑 count/DESCRIBE 审 schema 与行数——实测 4 的冷跑 23.68 s 同时就是审计步骤。
3. **物化**：`COPY … TO 'flights2015.parquet'` 本地化（实测 6，144 MB 一次）——03/05/09 章全部吃这份缓存，要增量再回远程。
- 私有仓库在第 1 步后插"凭据段"（下表 SECRET）；三步是"远程=冷层、本地=热层"的操作定义。

## SECRET 语法速查（⚠️ 官方文档转述；本机无凭据未连验）

```sql
CREATE SECRET (TYPE S3, KEY_ID '…', SECRET '…', REGION 'us-east-1');
CREATE SECRET (TYPE S3, PROVIDER CREDENTIAL_CHAIN);     -- 回落 AWS 环境变量/角色
CREATE SECRET (TYPE HF, TOKEN 'hf_…');                  -- 本章私有仓库 CONFIG 路线等价物
CREATE SECRET (TYPE HF, PROVIDER CREDENTIAL_CHAIN);     -- 本章同名小节的主角
```

- 两行 `PROVIDER CREDENTIAL_CHAIN` 是"凭据与查询分离"的对象化形态——token 永不入 SQL 字面量，与 07 章凭据卫生清单第 6 条同规约。

## 关键语法速查（实测注记）

| 用法 | 注记 |
| --- | --- |
| `read_parquet('https://…/f.parquet')` | ✅ 0.89s/322 行（冷） |
| `read_parquet(['urlA','urlB',…])` | ✅ 12 文件 5.8M 行 23.68s 冷 / 4.04s warm |
| `SET allow_asterisks_in_http_paths=true` | ✅ 可开，但 HTTP 列举仍缺（404 实证） |
| `read_csv_auto('https://…')` / `read_json_auto('https://…')` | ✅ 322 行 / 1.57s |
| `read_parquet('…/year=2015/month=*/*.parquet', hive_partitioning=1)`（本地） | ✅ 5,819,079 行 + year/month 伪列 |
| `hf://datasets/…` + `CREATE SECRET (TYPE HF)` / config.ini / CREDENTIAL_CHAIN | ⚠️ 文档转述未实证 |
| `s3://` + `CREATE SECRET (TYPE S3 …)` | ⚠️ 未实证（无凭据） |

## 与其他章/书的互链

- 远程文件全家桶的本地版 → [02-数据导入DuckDB.md](02-数据导入DuckDB.md)；JSON 细节 → [06-DuckDB与JSON文件.md](06-DuckDB与JSON文件.md)
- "无持久化探索 + httpfs"的 DIA 系统版 → [../DuckDB_in_Action/05-无持久化的数据探索.md](../DuckDB_in_Action/05-无持久化的数据探索.md)、云端篇 → [../DuckDB_in_Action/07-云端DuckDB与MotherDuck.md](../DuckDB_in_Action/07-云端DuckDB与MotherDuck.md)
- 本章是湖仓消费侧最小样本 → [../Apache_Iceberg活用入門/00-总览与阅读地图.md](../Apache_Iceberg活用入門/00-总览与阅读地图.md)（Iceberg 直读走 iceberg 扩展，1.5.5 可装 ✅ 版本 45163a28；本机构造不出公共 Iceberg 仓库 ⚠️）、[../Practical_Lakehouse_Architecture/00-总览与阅读地图.md](../Practical_Lakehouse_Architecture/00-总览与阅读地图.md)
- S3/对象存储 IO 优化原理 → [../../db/db.md](../../db/db.md)（湖仓存储论文线）

## 思考题（合上笔记再答）

1. 为什么 HTTP glob 开了开关还 404？两条替代方案？（无 ListObjects；显式 URL 列表/换 s3:// 或先落本地）
2. 用本章数据说明"分区裁剪"省了什么（2.08 s/503,897 行 vs 全量组）。
3. hf 私有仓库的两种鉴权形态各自适合什么环境？（配置文件=单机开发；凭据链=CI/多租户，转述自本章小节结构 ⚠️）
4. 冷跑 23.68 s 为什么"值得"？给出三步作业与每步的实测号。（一次性常数换 N 次 0.0x s；列=实测 3/4、量=实测 4、物化=实测 6）

## 2026 视角补注

- httpfs 已是事实上的"远程 IO 标准层"：MotherDuck/S3/R2/GCS/Azure 全走它（https://duckdb.org/docs/stable/extensions/httpfs.html ✅ 200）；1.4/1.5 线持续修重试与凭证刷新。
- "直读 HuggingFace 数据集"在 2024–2026 成为 LLM 数据工程日常（parquet 化的 dataset 卡片天然适配 `hf://` glob）；本书该节是全系列（两本 DuckDB 书）里对 HF 最系统的一章。
- 开放湖仓侧：iceberg 扩展可 ATTACH REST Catalog 的能力在快速演进（文档 https://duckdb.org/docs/stable/extensions/iceberg.html ✅），与 DuckLake（09 章）构成"外湖/自湖"两条线。

## 核心概念速览（中英对照）

- **httpfs** — DuckDB 远程文件系统扩展（HTTP/HTTPS/S3/HF）。
- **直读** — Direct query on remote files：不下载整文件先查。
- **footer 优先** — Parquet 元数据尾部先行读取策略。
- **Range 请求** — HTTP 分段拉取：远程列存的前提。
- **列举能力** — ListObjects：s3:// 与裸 HTTP 的分水岭（实测）。
- **Hive 分区（远程）** — 目录即列，远程同样免费（给清单的前提下）。
- **hf:// 路径** — HuggingFace 数据集寻址。
- **CREATE SECRET** — 凭据对象化：与查询解耦。
- **凭据链** — Credential chain：多来源回落。
- **冷/温基准** — cold/warm：远程性能报告的双口径。

## 最新演进与工业实践

- **扩展治理**：httpfs 与 iceberg 的依赖关系（avro/parquet 侧）在 1.x 线由 core 化理顺；本目录实测 install 均一行成功（版本 commit 号实抓 ✅）；官方清单见 https://duckdb.org/community_extensions/ ✅。
- **工业实践**："S3/HTTP 直查 + 本地热缓存"的混合姿势（本章第 6 条 COPY 物化）是单机分析对 TB 级湖的标准答案；DIA 10 章 NYC 出租车 Parquet 与本章航班是同一模式的两个量级样本 → [../DuckDB_in_Action/10-大数据集性能考量.md](../DuckDB_in_Action/10-大数据集性能考量.md)。
- **安全线**：2025 后各扩展 URL 校验/SSRF 加固趋严——远程直读生产化时把 scheme+host 白名单化（定性，来源为官方 release notes 群 ⚠️ 未逐条引）。
