# 05 使用BigQuery进行开发（原书第 5 章 · Developer Tools / Developing with BigQuery）

> 章首注：原书页区间 ⚠️ 推定 p.145–180；一级章题 ✅ 目录实抓（中译作"使用BiaQuerv进行开发"系转录笔误，按英文章节与上下文订正为"进行开发"）；
> **本章二级小节 ⚠️ 推定**——按配套代码 `05_devel/` ✅ 实抓文件族（bq_query.sh、rest_list.sh/rest_query.sh/rest_query_async.sh、
> bigquery_cloud_client.ipynb、google_api_client.ipynb、magics.ipynb、pandas.ipynb、bq_to_slides.gs、launch_notebook.sh）组织。

## 本章地图（⚠️ 推定结构，锚点为 ✅ 配套文件）

| 组 | 小节主题 | 锚点 |
| --- | --- | --- |
| 控制台 | Web UI：编辑器/作业面板/直方图（2019 版经典 UI） | ⚠️ |
| bq CLI | `bq query/load/cp/mk/ls`、`--format`、脚本化 | ✅ bq_query.sh |
| REST API | jobs.insert 同步/异步、轮询 jobStatus | ✅ rest_*.sh |
| 客户端库 | Python google.cloud.bigquery、pandas 互通 | ✅ bigquery_cloud_client.ipynb、pandas.ipynb |
| 笔记本 | Colab/Jupyter 魔符（`%%bigquery`） | ✅ magics.ipynb |
| 周边自动化 | Apps Script 出片到幻灯片 | ✅ bq_to_slides.gs |
| 认证 | ADC/服务账号/API key 的选型 | ✅ google_api_client.ipynb |
| BI 与其他生态 | Looker/Data Studio/Tableau 接驳概览 | ⚠️ |

## 核心精讲

### 1. 三种调用形态=三种延迟预算（⚠️ 转述 + ✅ 配套）

| 形态 | 会话 | 典型场景 |
| --- | --- | --- |
| 控制台 | 人肉 | 探索/演示 |
| bq CLI | 短进程 | cron、CI、临时运维 |
| REST/客户端库 | 程序 | 产品内嵌分析、批编排 |

✅ 配套 `bq_query.sh`：`bq --format=prettyjson query "SELECT ..."` 一行入管道；
✅ `rest_query.sh`/`rest_query_async.sh` 对照展示 jobs.insert 的同步等待与
"提交→轮询 `jobs.get` 取 jobStatus"两姿势（06 章深入作业生命周期）。

### 2. 客户端库与 DataFrame（✅ 配套 + ⚠️ 转述）

`google-cloud-bigquery` 的 `client.query().to_dataframe()`（读侧）+ pandas `to_gbq`/Write API（写侧）
把 BQ 变成"远端执行器的 pandas"——**compute pushdown 才是常态**（`to_dataframe()` 受 10GB 页大小限制需走
BQ Storage API，⚠️ 官方 Batching read API → Storage Read API 演化转述）。对照本地版同谱系：
[../DuckDB_in_Action/06-融入Python生态.md](../DuckDB_in_Action/06-融入Python生态.md)——pandas↔引擎胶水是同题，
差别只在"DuckDB 进程内零搬运 / BQ 跨网络搬结果"。

### 3. 魔符笔记本（✅ magics.ipynb）

`%%bigquery df --params` 把 SQL 结果直接落成 DataFrame、自动处理异步与进度条（配套文件即演示）。
配套 `launch_notebook.sh` ✅ 给 Cloud Shell/VM 拉起笔记本的端口姿势。2019 后这条线被官方产品化为
BigQuery Studio/Colab Enterprise（⚠️ 见演进节，Studio 文档 ✅ cn 镜像实抓于版本说明内多处）。

### 4. 认证三件套（⚠️ 转述）

用户 OAuth（ADC）/ 服务账号 key / Compute 默认 SA——本章配套 notebook 恰好覆盖前两种
（✅ google_api_client.ipynb 走 discovery API + key，bigquery_cloud_client.ipynb 走 ADC）。
产品化后：Workload Identity 取代长期 key（⚠️ IAM 演进，10 章治理面呼应，
✅ docs.cloud.google.com/bigquery/docs/access-control 为总入口）。

### 5. 应用侧模式清单（⚠️ 转述，本册自拟归纳）

- 参数化查询防注入（08 章 ✅ 配套 param_*.py）；
- 结果页/游标分页（jobs.getQueryResults）；
- 物化结果供低延迟应用读（09/07 章）；
- 用 BI Engine/容量承诺兜住看板 SLA（⚠️ 07 章）。

### 6. 错误处理与重试策略（⚠️ 转述，本册自拟归纳）

调用 BigQuery API 的工程纪律：

| 错误类型 | 处理策略 |
| --- | --- |
| rateLimitExceeded | 指数退避重试（初始 1s，最大 30s，上限 5 次） |
| concurrentJobLimit | 排队等待或拆分作业（⚠️ 默认并发上限以官方 quotas 页为准） |
| duplicate/alreadyExists | 幂等设计：作业 ID 由客户端生成→重试安全 |
| invalidQuery | 不重试——修复 SQL 后重新提交 |
| backendError / internalError | 短暂等待后重试；持续出现则提工单 |

⚠️ 客户端库（`google-cloud-bigquery`）内置部分重试逻辑（⚠️ 以库文档为准）；
REST 调用需自行实现退避。配套 `rest_query_async.sh` 的轮询循环即是重试/等待的工程化示范（✅ 实抓）。

## 常见误区（⚠️ 转述）

| 误区 | 事实 |
| --- | --- |
| `to_dataframe()` 拉全表不限量 | 默认受结果行数/大小限制；大结果走 Storage Read API 或写中间表 |
| CLI 查询比 API 便宜 | 计费看字节/槽位，入口无关 |
| API key 可当生产凭证 | key 只配 discovery 面；数据面必须 OAuth/SA（✅ 配套 notebook 的分工即是教材） |
| notebook 魔符=本地计算 | 执行在 BQ 侧，笔记本只是遥控器 |
| BI 连 BQ=零成本 | BI 生成的每 SQL 都进计费/槽位面（07 章） |

## 与其他章、其他书联系

- 异步作业与轮询的机制底座 → [06-BigQuery架构.md](06-BigQuery架构.md)；参数化/脚本 → [08-高级查询.md](08-高级查询.md)。
- 写侧管道工具化 → [04-将数据加载到BigQuery.md](04-将数据加载到BigQuery.md)；ML notebook → [09-BigQuery中的机器学习.md](09-BigQuery中的机器学习.md)。
- 本地同谱系 Python 生态：[../DuckDB_in_Action/06-融入Python生态.md](../DuckDB_in_Action/06-融入Python生态.md)、[../DuckDB_Up_and_Running/00-总览与阅读地图.md](../DuckDB_Up_and_Running/00-总览与阅读地图.md)（在盘 ✅）。
- 云仓对读：Snowflake 工具面（Snowsight/worksheets）[../Snowflake_The_Definitive_Guide/11-Snowsight可视化.md](../Snowflake_The_Definitive_Guide/11-Snowsight可视化.md)、[../Snowflake_The_Definitive_Guide/01-开始上手.md](../Snowflake_The_Definitive_Guide/01-开始上手.md)。
- Trino/Presto 客户端面（JDBC/CLI 生态）：[../Trino_The_Definitive_Guide_2e/11-将Trino与其他工具集成.md](../Trino_The_Definitive_Guide_2e/11-将Trino与其他工具集成.md)、[../Presto实战/11-将Presto与其他工具集成.md](../Presto实战/11-将Presto与其他工具集成.md)。
- BI/可视化通识落点：[../数据库系统概念6/09-应用设计和开发.md](../数据库系统概念6/09-应用设计和开发.md)。

## 核心概念速览（中英对照）

| 术语 | English | 释义 |
| --- | --- | --- |
| bq CLI | BigQuery command-line tool | gcloud 家族的分析入口，脚本化首选 |
| jobs.insert | Jobs API | REST 面提交查询/装载/复制作业 |
| 异步轮询 | job polling | 提交拿 job id → 周期 jobs.get 查状态 |
| ADC | Application Default Credentials | 本地/云上统一凭证解析链 |
| 服务账号 | service account | 机器身份，数据面 API 授权主体 |
| 魔符 | magic command (%%bigquery) | notebook 内 SQL→DataFrame 胶水 |
| BQ Storage Read API | Storage Read API | 大结果并行直读通道（绕 10GB 结果页限） |
| pandas 下推 | query pushdown | 在 BQ 侧算、只拉聚合结果的开发姿势 |
| to_gbq | pandas→BQ 写入 | 探索期小批量入口（生产用 Write API ⚠️） |
| Apps Script | Google Apps Script | ✅ 配套 bq_to_slides.gs：把查询结果自动进幻灯片 |
| Cloud Shell | Cloud Shell | 预装 gcloud/bq 的零本地环境（⚠️） |
| BI 连接器 | BI connector | Looker/Data Studio/Tableau 的 BQ 驱动面 |

## 最新演进与工业实践

- **BigQuery Studio 成为默认工作台**（版本说明 ✅ 2026-09 条目持续更新：结果表行号常显、查询文本热力图
  定位高耗阶段等 ✅ 实抓）——本章"控制台+notebook 魔符"两节已被产品级整合；
  SQL/笔记本资产可绑 **Git 仓库版本控制**（✅ 版本说明实抓），开发面正式进入 GitOps 叙事。
- **自然语言开发入口**：conversational analytics 与 Data Engineering Agent GA（✅ 版本说明 2026 条目），
  "写 SQL→审 SQL"成为新工作分工；data canvas 拖拽（✅ docs.cloud.google.com/bigquery/docs/data-canvas）。
- **可观测性外联**：JDBC 驱动支持 OpenTelemetry 跟踪/日志（✅ 版本说明实抓）——2019 本章的
  "自写轮询脚本"诉求被标准化协议吸收。
- **SDK 面扩张**：版本说明按 Go/Java/Python 客户端库逐版本列 changelog（✅ 页面结构实抓），
  本册 ch04 的 Write API 与 ch09 的模型管理都优先出现在这些库中。
- 工业实践：小结果交互面（BI/看板）与批管道分离到不同 reservation（⚠️ 07 章），对读
  Snowflake 同题 [../Snowflake_The_Definitive_Guide/08-账户成本管理.md](../Snowflake_The_Definitive_Guide/08-账户成本管理.md)。
