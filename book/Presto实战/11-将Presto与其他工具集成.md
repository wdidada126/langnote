# 11 将 Presto 与其他工具集成

> 原书第 11 章（中译本 p.203–209）。定位：生态位地图——BI/加速/编排/托管/商业发行五个方向。
> 返回 [00-总览与阅读地图.md](00-总览与阅读地图.md)。

## 本章地图

| 节 | 内容 | 一句话结论 |
| --- | --- | --- |
| 11.1 Apache Superset | 以 Presto 为事实源做查询、可视化乃至语义治理 | 同代开源绝配：SQL-on-Anything × Slice-and-dice |
| 11.2 RubiX | 协调器侧下推缓存：谓词/列裁剪/索引进 Hive 扫描层 | "给扫描装上 Turbo"的第三方加速件 |
| 11.3 Apache Airflow | PrestoHook/operators 编排 SQL 化 ETL | 把即席查询固化为例行管道 |
| 11.4 Amazon Athena | "嵌入式 Presto"托管服务剖析 | 按查询付费的形态实验 |
| 11.5 Starburst | 企业版 Presto：连接器/安全/支持 | 开源核心+商业外壳的开源经济学样本 |
| 11.6 其他集成 | 元数据/血缘/BI 等多点 | 集成即生态投票 |
| 11.7 自定义集成 | REST 协议/客户端二次开发指引 | 协议薄，自定义门槛低 |

## 精讲

### 1. Superset 联姻的技术实质（11.1）
- Superset 以 SQLAlchemy 方言（presto-dbapi/pyhive 系）接 Presto JDBC/REST；
- 交互式看板 = 每次点击一 SQL：Presto 的**低延迟+联邦**恰好覆盖 BI 的"多维上钻/跨源拼图"；
- 组合的软肋：高并发小查询把协调器打穿（12.8 资源组兜底）、缓存缺失反复扫大表（RubiX/物化/上移聚合）。
2026 视角：同构故事由 dbt + 湖仓 + 任一引擎重演（互链
[../数据仓库工具箱.md](../数据仓库工具箱.md) 的建模流水线叙事 ⚠️ 该文为书根笔记）。

### 2. RubiX：下推深化的标本（11.2）
- 定位：C++ 下推库，把列裁剪/谓词/字典过滤/聚合预计算做进 Hive 存储读取路径，JNI 挂 Presto；
- 思想比寿命重要：**引擎与存储层之间的"中间件加速"位**——其后由 Iceberg 元数据剪裁、
  Velox 向量化读、缓存服务（Alluxio 等）分别接管（文末演进）；
- ⚠️ RubiX 项目其后活跃度下降（以仓库状态为准），读本节请把它当"下推为什么分层"的教材。

### 3. Athena 的"嵌入式 Presto"论断要重估（11.4）
- 书中事实（2021）：Athena v1 引擎源自 Presto 分支、语法高度兼容、按扫描字节计费；
- 当代事实（2024–2026）：Athena 引擎已推进到 v2/v3（查询引擎重写、语法/函数与开源 Presto 分叉，
  官方明确列出不兼容面）——**"用 Athena 白嫖托管 Presto"的旧叙事失效**，迁移需按 AWS 文档逐条核对（⚠️ 引
  [docs.aws.amazon.com/athena/latest/ug/engine-versions.html](https://docs.aws.amazon.com/athena/latest/ug/engine-versions.html)，
  本环境 curl 复核：见完工报告核验状态）。
- 方法论保留：托管 Serverless SQL 的"计费面=扫描面"倒逼表格式/分区/列裁剪纪律——与 06 章分区剪裁互为因果。

### 4. Starburst 与开源经济学（11.5）
- 公司化维护发行版：企业连接器（S3 数据湖/Glue、Salesforce 等）、安全与治理、云上托管 Galaxy；
- 对读者的用处：分辨"本书讲的开源件"与"商业增强件"边界（书中演示均开源可复现；Ranger/数据屏蔽等归商业 ⚠️ 以厂商文档为准）；
- 2024–2026 事实核查要点：Starburst 的主线早已全面转向 **Trino**（它即 Trino 商业公司），
  与 prestodb 基金会路线分立——正好用第 01 章的简史收束生态认知。

### 5. 集成层的"协议薄"红利（11.7）
REST + JDBC 两个接口足以支撑：自研网关（B 站 Dispatcher 型）、血缘采集（事件监听器）、结果缓存。
**方法**（🔧 概念级）：任何语言实现 nextURI 轮询循环即得一个最小客户端（协议细节见 03 章精讲 1）；
生产化要补：重试语义、查询取消、会话头、错误分层。

## 常见误区

| 误区 | 现实 |
| --- | --- |
| BI 直连=最优看板架构 | 直连适合探索/中小规模；高并发对外报表仍需物化层/OLAP 引擎（13 章场景账） |
| Athena≈Presto 云版可互换 | v2/v3 语法与函数已分叉 ⚠️；把 Athena 当 Presto 写是迁移事故 |
| 缓存件（RubiX）装完全场景提速 | 它只加速扫描路径；Join/聚合瓶颈不受益，且引入 JNI 运维复杂度 |
| 商业发行=换名字 | 发行版差异在连接器/治理/支持，先列需求清单再评估 |

## 与其他章/其他笔记的联系
- Airflow/编排通识 → [../大数据项目实战.md](../大数据项目实战.md)、[../企业IT架构转型之道.md](../企业IT架构转型之道.md)（书根存在 ✅，见自检）；
- 缓存/下推的湖侧替代 → [../Apache_Iceberg活用入門/09-Spark_Flink_Trino实战.md](../Apache_Iceberg活用入門/09-Spark_Flink_Trino实战.md)；
- 引擎路由与集成形态 → [../bigdata/01-大数据技术全景.md](../bigdata/01-大数据技术全景.md)、[../bigdata/10-计算引擎的演进.md](../bigdata/10-计算引擎的演进.md)；
- 资源组承接 BI 并发 → [12-生产环境中的Presto.md](12-生产环境中的Presto.md)。

## 本章小结与行动清单

三句话带走：
1. 集成层的选型逻辑="这个工具补 Presto 哪块短板"：BI 补呈现、缓存补扫描、编排补周期、托管补运维、发行版补治理——
   补短板可以，叠 buff 要算账（每加一件，故障面×1）；
2. Athena/Starburst 两节是**生态位教材**：Serverless 与商业发行版分别吃掉"不想养团队"与"要 SLA+治理"两类需求；
   读的时候盯住"分叉与漂移"（Athena v2/v3、Starburst=Trino），别把 2021 的等号当真；
3. 协议薄=自定义集成便宜：网关/审计/血缘三件套各自只需几十行协议代码，值得自研而不是急于买平台。

集成架构评审三问：
- [ ] 数据面与控制面是否分离？（查询直连引擎、治理走网关/监听器）
- [ ] 每个集成件回答"失败了怎样"？（Superset 挂了只伤看板，dispatcher 挂了伤全部）
- [ ] 升级兼容性：依赖的引擎方言/参数有没有版本对表机制？（如 SQL 翻译件的语法覆盖列表）
- [ ] 集成件自身的"死亡演练"：拔掉 Superset/缓存/编排件，引擎与查询行为是否无损？

自测：
- [ ] 为什么按扫描计费的服务会反向塑造表设计？（11.4×06.4 分区剪裁闭环）
- [ ] RubiX 型加速件的"后继位"分别被谁接管？（元数据剪裁/向量化读/独立缓存）
- [ ] Starburst 与本书"开源件"的边界怎么向老板解释？（11.5 双坐标：发行方+内核版本）

## 核心概念速览（中英对照）

| 术语 | English | 释义 |
| --- | --- | --- |
| SQL 方言桥接 | SQLAlchemy Dialect | BI 经通用方言层接 Presto |
| 下推缓存 | Pushdown Cache (RubiX) | 谓词/投影在存储读取层先行裁剪的加速件 |
| Hook/Operator | Airflow Hook/Operator | 编排框架调外部引擎的两级抽象 |
| 按扫描计费 | Pay-per-Scanned-Bytes | Athena 型定价：费用=纪律（分区/列裁剪） |
| 嵌入式引擎 | Embedded Engine | 云产品内嵌开源引擎内核的形态（Athena v1） |
| 引擎版本分叉 | Engine Fork | Athena v2/v3 与开源 Presto 语法漂移现象 |
| 商业发行版 | Commercial Distribution | Starburst 式开源核心+企业增强 |
| 开源经济学 | Open-core Economics | 社区件与商业件的边界治理学问 |
| 查询网关 | Query Gateway | 自研统一入口：路由/配额/审计汇聚点 |
| 事件监听 | Event Listener Hook | 以审计流对接血缘/监控体系 |
| 协议薄客户端 | Thin REST Client | 按 nextURI 语义自实现的接入层 |

## 最新演进与工业实践

- **Athena 引擎分叉核对**（本书 11.4 的最大失真点）：AWS 官方引擎版本差异文档
  [docs.aws.amazon.com/athena/latest/ug/engine-versions.html](https://docs.aws.amazon.com/athena/latest/ug/engine-versions.html)
  （✅ 2026-09 curl 复核 200）；v1 退役时间表亦在其公告内 ⚠️ 逐 region 核对。
- **Superset 现状**：Apache Superset 持续活跃（[github.com/apache/superset](https://github.com/apache/superset) ✅ 200），
  Presto/Trino 连接器为其标配方言之一；本章组合仍是开源 BI 主流选型之一。
- **RubiX 的后继位**：扫描加速的当代答案是 Iceberg 元数据剪裁+向量化读+独立缓存——
  [iceberg.apache.org/spec/](https://iceberg.apache.org/spec/) ✅、
  [github.com/facebookincubator/velox](https://github.com/facebookincubator/velox) ✅；
  RubiX 仓库（Qubole 出品）[github.com/qubole/rubix](https://github.com/qubole/rubix)（✅ 2026-09 curl 复核 200；项目活跃度低，仅作史料）。
- **Starburst/Trino 与 prestodb 分立**：商业生态随 2020-12 分叉重组（更名报道
  [sohu.com/a/441573139_315839](https://www.sohu.com/a/441573139_315839) ✅）；选型报告须写"发行方+内核版本"双坐标。
- **国内印证**：美团 AdHoc 统一查询引擎分享（演讲材料镜像
  [tool.lu/deck/L6/detail](https://tool.lu/deck/L6/detail) ⚠️ 第三方镜像）与 B 站 Dispatcher
  （[dbaplus 原文](https://dbaplus.cn/news-73-4481-1.html) ✅）——均把"集成层做成平台"而非散点接工具；
  小红书按查询形态把 StarRocks/HBase/Presto 编组提供在线查询（厂商转述
  [腾讯云开发者社区](https://cloud.tencent.com/developer/article/2704655) ✅）。
