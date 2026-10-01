# 06 BigQuery API 编程：REST、C#/.NET 与 Python（Google BigQuery API）

> 对应原书 **Ch.6 "Google BigQuery API"**（章题与 15 个节题 ✅ QQ 阅读电子版实抓）。
> 正文为**精读重构**，非原书文本；机制描述「官方文档转述 ⚠️」；`docs.cloud.google.cn` URL 2026-10-02 亲测 200（✅）。
> 本章无新增 🔧 实验（成本算术直觉复用 04 章 T1/T5 口径）。

## 本章在本书中的位置

全书唯一的"开发者章"：从 REST 资源模型讲起，拿 Google APIs Explorer 试刀，然后**C#/.NET 与 Python 双语言各走一遍完整闭环**（认证→列举→建集→建表→装载→查询→落表）。作者的双语言设计在 Packt 系里少见——反映他的企业现实：甲方分析栈里 Excel/VBA 退场后坐着的正是 .NET 工程师，而数据科学侧站着 Pythonistas。章末 "Roles and permissions" 一节把话题引向 IAM，是 Ch.8 之前的权限垫片。

## 6.1 REST 资源模型与 APIs Explorer（Accessing Google BigQuery / Introducing Google APIs explorer）

- 资源树（⚠️ 转述 + ✅ https://docs.cloud.google.cn/bigquery/docs/reference/rest）：`projects → datasets → tables → tabledata`，作业独立成 `jobs`（装载/导出/查询都是 job），插入走 `tabledata.insertAll`。
- 书中方法：REST 语法用 HTTP 动词+URI 表格化呈现（jobs.insert 的 configuration.query 嵌套 JSON 占了两页）——这套 JSON 结构今天逐字段有效，只是官方推荐再没人手写 HTTP（客户端库/`bq` 都封了这层）。
- **APIs Explorer**（当时新物）：浏览器里填参数直接发真请求，OAuth 弹框即试——该工具演进为今天 developers.google.com 的 APIs Explorer 家族（⚠️ 转述）。
- 异步协议是本节隐藏考点：`jobs.query` 响应可能带 `jobComplete:false` + jobReference，需轮询或 getQueryResults——书里 Python 节用 `timeoutMs` 演示了这个往返 ⚠️。

## 6.2 凭据与服务账号（Getting credentials / Creating a service account）

- 流程（书中三步，今天骨架不变 ⚠️）：Console 建服务账号 → 下载 JSON key → 环境变量 `GOOGLE_APPLICATION_CREDENTIALS` → 客户端库自动发现（ADC 概念书里没有名分、已有事实）。
- 权限挂接：给服务账号在项目/数据集上授角色（BigQuery Admin / `roles/bigquery.dataViewer` 一类），为 6.4 收束节埋线。
- 2026 修正：长期 JSON key 是官方点名的**头号反模式**，替代面=直绑 SA 到计算身份、Workload Identity Federation、ADC 元数据（⚠️ 转述）——书中流程"能跑、别学久"。

## 6.3 双语言闭环（C# .NET 七节 + Python 三节）

C# 线（书中用 Visual Studio + NuGet `Google.Api.BigQuery.v2`，⚠️ 转述）：

| 节 | 动作 | 今日对位 |
| --- | --- | --- |
| Authenticating | 基类 ClientSecrets 加载 key | Google.Cloud.BigQuery.V2 走 ADC |
| Listing datasets/tables | BigqueryService.Datasets.List | 同 API 面 |
| Creating dataset / table | Datasets.Insert / Tables.Insert | 客户端糖 `client.CreateDataset` |
| GCS→BQ 装载 | JobConfigurationLoad(sourceUris gs://...) | 不变，多 format options |
| 查询并展示 | Jobs.Query + 轮询 GetQueryResults | `client.ExecuteQuery` 自动轮询 |
| 查询落新表 | destinationTable 参数 | destination + writeDisposition |

Python 线（书中裸 `googleapiclient.discovery.build('bigquery','v2')` 资源式写法 ⚠️）：Import 库→load 作业→query+copy 到新表三节。**旧式 discovery 客户端已被半官方退役**，今天正解是 python-bigquery 高级库（`from google.cloud import bigquery; client.query(sql).result()`），SQL 仍可参数化、类型化行对象（⚠️ 转述）。

- 两线共同保留的架构知识（值得照抄进笔记的三件事）：**装载即作业（异步+可查状态）、查询默认 10000 行走 results 页、落表要管 writeDisposition（WRITE_TRUNCATE 心智）**（✅ 概念面 reference/rest）。

## 6.4 角色与权限收束（Roles and permissions）

- 书中口径（⚠️ 转述）：预定义角色三层（项目级 bigquery.admin / 数据集级 can_read/can_write / 表级 ACL），API 调用者身份=服务账号，最小权限从本章开始示范。
- 现实校准：dataset ACL 时代之后来了 **IAM 统一（数据集访问迁移）+ 细粒度访问控制（行级策略/列级脱敏，2023-24 ⚠️）**（✅ https://docs.cloud.google.cn/bigquery/docs/access-control）。
- 建议动作：把 6.2 的 key 文件改成"只给测试 SA 只读角色"再跑全章例题——书中从未做这一步，这是老教程的通病。

## 6.5 同构对照：一个装载作业的两语言骨架（书中例的 2026 校准版）

```python
# Python（google-cloud-bigquery 高级库；书中 discovery 裸写法的等价替身 ⚠️）
from google.cloud import bigquery
client = bigquery.Client(project="my-demo-project")        # ADC 认身份（6.2 的 key 环境变量）
job = client.load_table_from_uri(                          # 6.3 的 JobConfigurationLoad
    "gs://my-demo-bucket/natality_small.csv",
    "my-demo-project.demo_ds.natality",
    job_config=bigquery.LoadJobConfig(source_format=bigquery.SourceFormat.CSV))
job.result()                                                # 阻塞至作业完成（异步协议 6.1）
rows = client.query("SELECT COUNT(1) c FROM `demo_ds.natality`").result()
```

```csharp
// C#/.NET（Google.Cloud.BigQuery.V2；书中 v2 资源库写法的现代替身 ⚠️）
var client = BigQueryClient.Create("my-demo-project");
var job = client.UploadCsv("demo_ds", "natality",
    new[] { GoogleCloudFilename.From("natality.csv") }, "my-demo-bucket/object.csv",
    new CreateUploadCsvOptions { WriteMode = WriteMode.Truncate });
job.PollUntilCompleted();
var results = client.ExecuteQuery("SELECT COUNT(1) c FROM `demo_ds.natality`", null);
```

- 两骨架共享的四件套：**身份（ADC/key）→ 作业对象 → 阻塞轮询 → 行迭代器**——换任何语言客户端都是这四拍；
- 书中 C# 线用基类手工装 ClientSecrets、Python 线用 discovery build——**今天两门都收敛到 ADC 自动发现**，认证代码比 2017 更短而不是更长（⚠️ 转述），这是本章最反直觉的演进；
- `insertAll` 行协议的 JSON 骨架（书 6.3 尾节，⚠️ 转述）：

```json
{ "rows": [ { "json": {"name":"a","ts":"2017-01-01 00:00:00 UTC"} },
            { "json": {"name":"b","ts":"2017-01-01 00:00:01 UTC"} } ] }
→ 响应带 errors[] 逐行定位，坏行不挡好行
```

## 6.6 本章练习题三则（自拟）

1. 用 APIs Explorer 手工发一次 `jobs.insert`（query 落表版），对照 Python 高级库同名作业的 JSON dump——理解"库只是格式化请求器"；
2. 把 6.3 的查询轮询改为 `timeoutMs=0` 立即返回再自旋 getQueryResults，观察 jobComplete 翻转——交互式/作业式边界（Ch.4 回收）；
3. 给服务账号只挂 `roles/bigquery.dataViewer` 再跑建表例题，记录 403 的 `message` 文本——比读十页 IAM 文档都管用（✅ access-control 页对照）。

## 阅读策略与坑

1. C#/Python 二选一精读、另一门扫结构即可——**作业模型与 JSON 配置面是共享的 80% 价值**；
2. 书中 NuGet 包名带 `.v2` 后缀（v2 资源库时代），照抄会装到古董；Python 的 discovery 写法在异常处理与重试上无保护，生产必须换高级库（⚠️）；
3. `insertAll` 流式插入（6.3 表中 Streaming insert of rows 一节）与 Ch.8 Pub/Sub 是同一入口的两端——先在本章看清 JSON 行协议（`{"json":{"name":...}}` + 行级错误数组），Ch.8 会回收；
4. 与兄弟册互读：官方客户端库全家福与错误重试策略见 TDG 开发章（[../Google_BigQuery_TDG/05-使用BigQuery进行开发.md](../Google_BigQuery_TDG/05-使用BigQuery进行开发.md)）；管道工程化见 BQDW 04 号章文件。

## 6.7 本章地图（REST 动词 → 客户端糖 → CLI 三列表）

| REST 动作 | Python 高级库 | bq 命令 |
| --- | --- | --- |
| datasets.insert | client.create_dataset | bq mk |
| tables.insert | client.create_table | bq mk --schema |
| jobs.insert(Load) | client.load_table_from_uri | bq load |
| jobs.query | client.query | bq query |
| jobs.get / getQueryResults | job.result() 自动轮询 | （内置等待） |
| tabledata.insertAll | client.insert_rows_json | （无直配，走 API） |

- 三列背通即本章毕业：前两列是"程序化"的今昔，第三列是 Ch.2 的回声——**BigQuery 没有第七种访问方式，只有同一层的七件外衣**；
- insertAll 行无 CLI 对应恰是伏笔：行级高频写入走的是与本章批量作业**不同的通道家族**（Ch.8 主场，✅ streaming 页）。

## 核心概念速览（中英对照）

| 中文 | 英文 | 一句话 |
| --- | --- | --- |
| 资源模型 | REST resource model | projects/datasets/tables/jobs |
| 作业 | job | 装载/导出/查询皆异步作业 |
| 查询轮询 | getQueryResults / jobComplete | 交互式超时转作业模式 |
| API 试验台 | Google APIs Explorer | 浏览器发真请求 |
| 服务账号 | service account + JSON key | 机器身份，今日限用 |
| 应用默认凭据 | ADC | 书中有实无名的机制 |
| 目标表 | destinationTable + writeDisposition | 查询落表与覆盖策略 |
| 行级插入 | tabledata.insertAll | 流式 JSON 协议 |
| 加载作业 | JobConfigurationLoad | GCS→表 的声明式装载 |
| 发现式客户端 | googleapiclient discovery (Python) | 已退役的裸 API 写法 |
| 高级客户端库 | google-cloud-bigquery / .NET V2 | 当代正解封装层 |
| 预定义角色 | predefined IAM roles | admin/dataViewer 最小权限 |

## 最新演进与工业实践

- **通道分层重画**：insertAll 仍是流式入口之一，但高吞吐推荐 **Storage Write API**（gRPC 流式 +  Exactly-once 的 Append 流，2023-24 GA 化 ⚠️ 转述；✅ 概念对照 https://docs.cloud.google.cn/bigquery/docs/streaming-data-into-bigquery）。
- **API 面扩容**：本章 JSON 之外的新面——reservations（✅ https://docs.cloud.google.cn/bigquery/docs/reservations-intro）、data policies（脱敏策略 ✅ data-catalog 邻页）、analytics hub（数据交换 ⚠️）——"编程访问 BQ"的外延已是容量+治理。
- **凭据治理**：密钥轮换强制化、SA impersonation 审计、禁止项目级 Editor 一刀切（⚠️ 通识转述）；6.2 的下载 key 流程在企业里需走 secret manager。
- **库生态**：Python 侧 pandas-Gbq（`pd_gbq.read_gbq/to_gbq`）让书中 20 行样板缩成 1 行（⚠️ 转述）；R 客户端 bigrquery 同代际成熟（Ch.7 呼应）。
- 工业实践：**"API 章的正确打开方式"=把 6.3 闭环翻译成 IaC**——datasets/tables 用 Terraform 声明、装载作业用工作流引擎调度，书中一次性脚本是原型不是产线（⚠️ 通识）。
