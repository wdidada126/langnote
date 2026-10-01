# 01 GCP 全家桶里的 BigQuery（Google Cloud and Google BigQuery）

> 对应原书 **Ch.1 "Google Cloud and Google BigQuery"**（章题与节级目录 ✅ QQ 阅读电子版实抓）。
> 正文为基于公开资料的**精读重构**，非原书文本；BigQuery/GCP 机制描述一律「官方文档转述 ⚠️」，
> 所引 `docs.cloud.google.cn` 镜像 URL 于 2026-10-02 亲测 200（✅）。本章无 🔧 实验（类比集中在 03/04/05/08 章）。

## 本章在本书中的位置

原书第一章不急着讲 BigQuery 语法，而是把 BigQuery 摆回 2017 年的 GCP 版图：先讲云存储、再开浏览器跑第一条查询、然后把 Cloud SQL / Datastore / App Engine / Compute Engine 这些"邻居"逐个点名——作者 Haridass 是甲方数据工程负责人视角，他假设读者是从传统企业机房上云的分析工程师，**先认门、再动手**。这一章的节级目录就是全书的电梯：17 节里有 11 节在介绍 BigQuery 之外的产品，这种"生态先行"的写法与 TDG 册第 1 章"直接讲 BQ 是什么"形成镜像（对照 [../Google_BigQuery_TDG/01-GoogleBigQuery是什么.md](../Google_BigQuery_TDG/01-GoogleBigQuery是什么.md)）。

## 1.1 BigQuery 是什么（⚠️ 转述 + ✅ 文档）

- 全托管、无服务器的**列式数据仓库**：不分片、不管集群、不选节点数；容量由平台侧承接（✅ https://docs.cloud.google.cn/bigquery/docs/introduction）。
- 存储与计算解耦，数据落在 Google 分布式存储层；用户看到的对象层级：`项目 → 数据集(dataset) → 表/视图`。
- 四类入口本章先给两个：**Web Console（浏览器）** 与后两章的 **CLI(bq)**、**API**；本书的三段式（界面→SDK→API）正是本章埋下的路线图。
- 计费心智（2017 口径）：按**扫描字节**的查询费 + 存储费两条线，免费额度内可整章白嫖练手（⚠️ 额度数字以官方页为准，书里表格已过期）。

## 1.2 GCP 服务总览（Overviewing Google Cloud Platform services）

书中原话式的分类（重构）：计算类（Compute Engine、App Engine、Container Engine）、数据类（Storage、BigQuery、SQL、Datastore、Spanner 前夜）、工具类（Cloud SDK、Console、APIs）。两个时代化石值得登记：

- 书中写 **"Google container engine"**——该产品 2017-02 已更名 **Google Kubernetes Engine（GKE）**（⚠️ 公开通识，书稿截稿早于改名落地），读到即知本书素材停留在 2016 年。
- **Cloud Datastore** 在 2017 是旗舰 NoSQL；今天它的身份是 Firestore 的 "Datastore mode"（⚠️ 转述），书里"用 Datastore 存行为日志"的例子今天应改读作 Firestore。

## 1.3 Cloud Storage 与 BigQuery 的绑定关系（Google Cloud storage and its features）

- GCS 是 BigQuery 的**装载中转站与导出终点站**：批量装载（Ch.4/Ch.6 反复出现）几乎都走 "文件 → GCS → bq load / API job"（✅ https://docs.cloud.google.cn/bigquery/docs/loading-data-cloud-storage-csv）。
- 书中对比了存储类别（Regional/Multi-Regional/Nearline/Coldline，2017 命名体系）与元数据自定义（⚠️ 今天已演进为 Standard/Close-line/Archive 等新层级，转述登记不展开）。
- 实操提醒（书中原意重构）：GCS URI 形如 `gs://bucket/path`，**大小写敏感**、区域与 BQ 数据集区域不必一致但影响延迟与流量费 ⚠️。

## 1.4 浏览器里跑第一条查询（Working with the browser / Running your first query）

- Compose Query 界面三件套：编辑器、查询历史/已保存查询、结果可视化小图（⚠️ 2026 的 UI 大改：智能补全、查询计划图、文件标签页）。
- 第一条查询的对象是**公共数据集**（下节）——本书是 Packt 式"五分钟见效"写法：先看到行数，再解释语法。
- 错误检查习惯从这里开始养成：BQ 报错信息带**行列号与配额提示**，书中建议每次报错先看是否触发 dry run 可估的扫描量（⚠️ dry run 概念见 Ch.6 API 再展开）。

## 1.5 BigQuery 公共数据集（BigQuery public datasets）

- 2017 年公共数据集无门槛随便查，是本书教学素材的基石（GitHub、Stack Overflow、维基百科、气象、纽约出租车……）。
- 现状对账：公共数据集仍在，但**免费公共数据引入查询档位/限额约束**（⚠️ 转述）；官方示例数据集入口 ✅ https://docs.cloud.google.cn/bigquery/docs/sample-tables 与体验场 ✅ https://docs.cloud.google.cn/bigquery/docs/sandbox（不绑卡即用）。
- 表限定名写法 `public-data-set.dataset.table` 是本章埋的语法伏笔（Ch.4 "Qualifying tables in query" 收口）。

## 1.6 邻居服务区（Cloud SQL / Datastore / App Engine / Compute Engine）

| 书中服务 | 2017 定位（重构） | 与 BigQuery 的关系 | 今日状态 |
| --- | --- | --- | --- |
| Cloud SQL | 托管 MySQL/PostgreSQL | 导出→GCS→装载（无原生 CDC） | ✅ 现有 Datastream/transfer 直连 ⚠️ |
| Cloud Datastore | schemaless NoSQL | 分析侧靠导出中转 | Firestore Datastore mode ⚠️ |
| App Engine std/flex | PaaS 双环境 | 书里当"部署演示载体"（Ch.2 尾） | 仍在，边缘角色 ⚠️ |
| Compute Engine | IaaS VM | 自建 Hadoop 对照物 | 仍在 ⚠️ |
| Container Engine | Docker 集群 | 一句带过 | 更名 GKE ⚠️ |

作者意图（重构）：让读者明白 **BigQuery 不是孤岛**，但它与邻居的"管道"在 2017 基本靠 GCS 文件中转——这正是后续章节 Dataprep（清洗）与 Pub/Sub（流式）存在的理由，本章先把问题摆出来。

## 1.7 前言与致谢区读法（Foreword / Dedication / Preface，✅ 电子版全文实抓）

- **Foreword（Andz Czarnecki 序，✅ read/1036700382/4 原文）**：以"茶水间对话"引出全书动机——多年行为日志如何存、如何秒级问、如何近实时可视化；序作者身份（BigQuery 生态从业者）为本书"甲方实操"定调背书（⚠️ 人名按原文照录，中文不译）。
- **About the Authors / Reviewers（✅ p3/p5/p6）**：作者团与审校团的履历本身就是 2017 年 BigQuery 用户画像抽样——企业数据工程师（Haridass）+ 咨询顾问（Brown）+ 平台侧深度用户（审校 Berlyant：SO 千答、BigQuery Mate 扩展作者）；读书时留意审校者批注痕迹（例：公共数据集配额话题书中偏轻，恰是 Berlyant 在 SO 上的高频问题域 ⚠️ 推断）。
- **Preface 六件套（✅ 目录实抓）**：What this book covers / What you need / Who this book is for / Conventions / Reader feedback / Customer support——Packt 标准模板；其中 **Conventions 节定义了本书代码字体**（等宽=可敲、斜体=占位），本目录引用时沿用该约定；
- **Downloading the example code 节**：Packt 例码走网站下载制（非 GitHub 仓库），链接已随 Packt 改版大面积失效（⚠️ 负结果登记）——本目录各章代码均为自拟等价物，不依赖原书例码。

## 1.8 三册第一章对读（同一产品三种开场）

| 开场动作 | 本册 Ch.1 | TDG Ch.1 | BQDW Ch.1 |
| --- | --- | --- | --- |
| 第一句话回答 | "BigQuery 在 GCP 哪里" | "BigQuery 能替你省什么" | "要不要搬进 BigQuery" |
| 代码量 | 一条浏览器查询 | 零（概念图为主） | 零（章程表格） |
| 隐含读者 | 上手工程师 | 平台架构师 | 技术管理者 |
| 读后动作 | 装 SDK（Ch.2） | 直接写查询 | 写立项书 |

三章互为盲区补片：预算敏感读 BQDW、机制饥渴读 TDG、**两手空空从本册开始**。

## 1.7 本章的四条主线与一条暗线（结构图）

```
GCP 全景 ──┬── 存储层：Cloud Storage ──┐
           ├── 计算层：GCE / GKE / App Engine
           ├── 交易层：Cloud SQL / Datastore ──(导出中转)──┐
           └── 分析层：BigQuery ◄──────────────────────────┘
                        └─ 浏览器 + 公共数据集 = 第一条查询
```

- 四条主线（存储/计算/交易/分析）对应原书四组节题；一条暗线是**"数据只在分析层被问，其余层负责送"**——作者整章没明说，但 17 节的取舍全在这句话里（重构）；
- 画这张图的读法收益：后 7 章每一章都能落回图上一个箭头——Ch.2 命令行是"送"的工具、Ch.6 是"送"的程序化、Ch.8 是"送"的实时化；
- 对照 [../Google_BigQuery_TDG/00-总览与阅读地图.md](../Google_BigQuery_TDG/00-总览与阅读地图.md) 的"云仓三角"表，本册这张图的 Google 象限更细，湖仓/开源象限则完全缺席（短册边界，登记不批评）。

## 阅读策略与坑

1. 本章可 20 分钟读完，但 1.3 的 GCS↔BQ 心智必须扎牢：本书**所有装载例题都隐含这一步**；
2. 别按书背产品名——用上表做 2017→2026 翻译，否则会被 "container engine"、"Datastore" 卡住；
3. "先浏览器后命令行"的顺序在今天依然正确：sandbox 项目零成本复现本章全部操作（✅ 上述 sandbox URL）；
4. 本章 Summary 节无实质内容（Packt 模板件），可跳过。

## 1.9 学完本章的六个自测问题（答案全在正文）

1. 为什么作者要先讲 GCS 再讲第一条查询？（装载中转 vs 见效节奏的双重动机）
2. "Google container engine" 该翻译成什么产品？改名发生在哪一年附近？（GKE，2017-02 ⚠️）
3. 公共数据集例题里四段表名和反引号各解决什么问题？（跨项目引用/含点开头的标识符）
4. 零成本复现本章操作的正确入口是什么？（sandbox，✅ URL 见 1.5）
5. 2017 年 Cloud SQL 进仓的路径有几步？今天缩短成什么？（导出→GCS→装载三步 vs 托管 CDC 直连 ⚠️）
6. 本章哪三样东西到 2026 已经改名或变性？（container engine→GKE、Datastore→Firestore 模式、Data Studio 前身年代的产品地图 ⚠️）

答不出 4/5/6 属于没读演进节——本章的"考古翻译表"比操作步骤值钱。

## 核心概念速览（中英对照）

| 中文 | 英文 | 一句话 |
| --- | --- | --- |
| 无服务器数据仓库 | serverless data warehouse | 用户不管容量与集群 |
| 列式存储 | columnar storage | 按列组织，扫描量=读列之和 |
| 项目/数据集/表 | project / dataset / table | BQ 三级对象模型 |
| 云存储 | Google Cloud Storage (GCS) | 装载与导出的文件枢纽 |
| 公共数据集 | public datasets | 免装载的教学/探索数据 |
| 托管关系库 | Cloud SQL | 交易库，经导出进仓 |
| 键值/文档库 | Cloud Datastore | 今 Firestore 的 Datastore 模式 |
| 应用引擎 | App Engine (standard/flexible) | PaaS，本书仅作部署演示 |
| 虚拟机 | Compute Engine | IaaS 对照组 |
| 容器集群 | Container Engine → GKE | 书中为改名前旧称 |
| 网络控制台 | web console / browser UI | 第一条查询的发生地 |
| 扫描量计费 | pay for bytes scanned | 本书时代的计费主线 |

## 最新演进与工业实践

- **产品地图重画**（2017→2026）：Container→GKE、Datastore→Firestore、Mongo/Hadoop 代际竞品退场；BigQuery 侧长出 **BQML、Omni 多云、Data Canvas、向量检索**（✅ https://docs.cloud.google.cn/bigquery/docs/vector-search；⚠️ Omni 线此后大幅收缩，转述）。
- **接入面进化**：书里"GCS 文件中转"的今天默认解是 **Datastream/CDC、BigQuery Data Transfer Service**（✅ https://docs.cloud.google.cn/bigquery/docs/transfer-service-overview），本章 1.6 表格里"靠导出"的四个邻居现已各有托管管道。
- **免费学习面**：Google Skills Boost / 云赠金 + sandbox（✅ 上 URL）取代了书中"直接开项目"的路径；公共数据集配额档位是书后新增坑（⚠️）。
- **工业实践**：现代团队把"1.2 服务总览"级别的选型沉淀为**基础设施即代码**（Terraform 管项目/数据集骨架），而不是像 2017 靠控制台点选；盘上工程化视角续读 [../BigQuery_for_Data_Warehousing/01-入住BigQuery与仓库项目启动.md](../BigQuery_for_Data_Warehousing/01-入住BigQuery与仓库项目启动.md)。
