# 02 · 访问途径：控制台、CLI 与 DynamoDB Local

> 章题 ⚠️ 推定（重构依据：✅ 官方导读句「You will learn how to access DynamoDB in the management console, command line, and the Eclipse plugin」「You will also gain insights into DynamoDB Local and CLI commands」；见 [00-总览与阅读地图.md](00-总览与阅读地图.md) §2/§6）。三态：✅ 实证 / ⚠️ 转述推定 / 🔧 本机类比（**非 DynamoDB 行为**）。

## 1. 章定位

- 本书把「怎么碰到 DynamoDB」列为独立能力域，✅ 级证据是导读两句里点名四类入口。
- 四类入口=2014 年 AWS 开发者工作流的原生切片：**管理控制台 / AWS CLI / DynamoDB Local / Eclipse 插件**。
- 今天回读本章有双重价值：一是低层 JSON 心智（可迁移），二是工具考古（大半已换代 ⚠️）。

## 2. 四类入口逐项

### 2.1 管理控制台 ⚠️（书中形态）→ 现状 ✅

- 2014：建表、浏览项、控制台内过滤（本质 Scan）、看容量指标——图形面很薄 ⚠️。
- 现状：控制台覆盖表/索引/流/备份/加密/容量模式全面板 ✅（Introduction.html 为文档树根，台账 §7）。
- 告诫传承：控制台过滤框是**调试工具不是查询接口**——与 [05-查询与扫描访问模式.md](05-查询与扫描访问模式.md) 的 Scan 经济学呼应 ⚠️/✅（best-practices.html）。

### 2.2 AWS CLI（v1 时代）⚠️ → v2 现状 ✅

- 书中示例命令族：`put-item / get-item / update-item / delete-item / query / scan / create-table / list-tables` ⚠️（命令名为本书时代 CLI 通识，逐字对原书不可证，标 ⚠️）。
- CLI 是「HTTP JSON API 的壳」：参数即 JSON、响应即 JSON——06 章 API 层的排练场 ⚠️。
- 跨代事实 ✅：命令族在 CLI v2 中原名保留 ⚠️（v1→v2 为整体更名升级，年代 ⚠️ 约 2020）。

### 2.3 DynamoDB Local ⚠️

- 2014 定位：本地 Java 进程模拟服务端，跑单测免流量费；行为子集 ⚠️。
- 书中「gain insights」句 ✅ 证明其板块地位。
- 现状：仍可得、但「非全保真」口径明确 ⚠️（集成测试以真实表/托管沙箱为准 ⚠️）。

### 2.4 Eclipse 插件（AWS Toolkit for Eclipse）⚠️

- 2014 官方 SDK 配套：表浏览/代码脚手架 ⚠️。
- 其后停维护、让位 IDE 扩展与 CLI ⚠️（现状登记，非本书断言）。
- 书目意义 ✅：工具在场=成书于 Java/Eclipse 中心时代的直接证据。

## 3. 操作序列（控制台/CLI 心智 ⚠️+✅）

1. 建表：定键制式（单键/复合）+ 预留读写容量 ⚠️→✅（WorkingWithTables.html）。
2. 等激活：表状态 CREATING→ACTIVE 异步 ⚠️。
3. 灌数据：put-item 单条全量替换语义；batch-write-item 批量 ≤25 项 ⚠️→✅。
4. 试查询：query 带键 / scan 带过滤（→ [05-查询与扫描访问模式.md](05-查询与扫描访问模式.md)）✅（Query.html/Scan.html）。
5. 看指标：ConsumedCapacity、ThrottledRequests（→ [04-分片与容量规划.md](04-分片与容量规划.md)）⚠️→✅。
6. 改容量：update-table 调预留（2014 手动，后来可自动伸缩 ⚠️）。

## 4. 开发者/DBA 双视角（✅ 导读原文 from a developer/DBA perspective）

| 视角 | 主工具 | 2014 关切 | 2026 平移 |
|---|---|---|---|
| 开发者 | SDK/Local/CLI | 本地闭环、单测 | 容器桩+契约测试 ⚠️ |
| DBA | 控制台/CloudWatch | 容量、限流、拆分 | 按需计费弱化角色 ✅ |
| 共同底线 | — | 键选错全盘返工 | 不变 ⚠️ |

## 5. 本机零凭证纪律说明

- 本波不装引擎、不连真实 AWS：DynamoDB 为托管服务，**不可实测面**先实测确认（curl 探测+工具网络层记录）后降级 ⚠️+✅URL——波10 共通规范条款执行记录 ✅。
- 本机只有 SQLite/DuckDB 类比面（§6），且逐组标注非 DynamoDB 行为。

## 6. 🔧 本机类比实验（**非 DynamoDB 行为**）

| 组 | 实验与真实输出 | 类比点 | 边界 |
|---|---|---|---|
| T1 | 参数化 `INSERT INTO orders VALUES(?,?,?,?)` | CLI put-item 的 JSON 参数壳 | 无网络层 |
| T5 | JSON 文本列存项，读后手工解析 | put-item 全量替换语义 ≈ 先删后插 | 无服务端类型 |
| D11 | SQLite 显式事务 20k 插 38.1ms / executemany 20k 21.2ms | 单发 vs 批量（batch-write 形状） | 无吞吐配额 |
| D5 | DuckDB `EXPLAIN` 出 `SEQ_SCAN` 节点 | 「消耗可见性」诉求的本机替身 | 计划≠RCU |
| D3/D4 | 200k 批插 0.099s vs 2k 单行 1.989s | CLI 循环单发 vs 批量的形状差 | 数量级不可比 |

## 7. 时差老实录（2014→2026，本章受害最深）

- 四大入口→今天只剩两个直系（控制台 ✅、CLI ✅ 已换代 v2 ⚠️）。
- 插件位易主：Eclipse Toolkit→各 IDE 扩展/NoSQL Workbench ⚠️。
- Local 降级：从推荐工作流到兼容子集 ⚠️。
- 凭证链换代（ini/SSO 等）⚠️——原书所有凭证类示例今天不可直抄。
- 阅读法：把本章当**2014 工具考古**；可迁移的是低层 JSON 心智（→ [06-API集成与数据格式.md](06-API集成与数据格式.md)）。

## 8. 挂点

- 前置 [01-数据建模概念与单键模型.md](01-数据建模概念与单键模型.md)（建表前先定键）。
- 后继 [03-索引体系GSI与LSI.md](03-索引体系GSI与LSI.md)（控制台建 GSI 曾是唯一图形化途径 ⚠️）、[05-查询与扫描访问模式.md](05-查询与扫描访问模式.md)（query/scan 经济学）。
- 平行 [../Amazon_DynamoDB_TDG/00-总览与阅读地图.md](../Amazon_DynamoDB_TDG/00-总览与阅读地图.md) 03/10 章（2022 CRUD 与生态工具面，写前 ls 验名 ✅ 在盘实链）。

## 9. 命令速查与迁移对照（2014 书内形态 → 2026 现行 ⚠️+✅）

| 2014（书内 CLI/工具动作 ⚠️） | 2026 现行入口 ✅/⚠️ | 迁移注记 |
|---|---|---|
| `aws dynamodb create-table` | 同名 CLI v2 ✅ | 键参数名未变 |
| `put-item / get-item` | 同名 ✅ | JSON 参数壳不变 |
| `query / scan` | 同名 ✅；另有 PartiQL ✅ | 表达式参数换代 ⚠️ |
| `update-table`（调预留） | 同名 ✅；容量模式可切 On-demand ✅ | 语义扩展 |
| 控制台建表向导 | 控制台 ✅+NoSQL Workbench ⚠️ | 图形面厚了数倍 |
| DynamoDB Local（java -jar） | 仍可得 ⚠️ | 非全保真口径 |
| Eclipse Toolkit | 无对应物 ⚠️ | 入口死亡样本 |

- 读法：左列是本书示例代码的语法底座 ⚠️，右列是本目录给的「可直抄性」判定——命令族可直抄，凭证/插件层不可 ⚠️。

## 10. FAQ（两问 ⚠️）

- 问：今天还要不要装 DynamoDB Local？
  答：单测可用但别信其行为完备性 ⚠️；关键路径用真实表小规格或托管沙箱 ✅ 口径。
- 问：CLI 还能当 API 教学工具吗？
  答：能——JSON 进 JSON 出最贴近低层协议（→ [06-API集成与数据格式.md](06-API集成与数据格式.md)）✅ 定性。

## 核心概念速览（中英对照）

| 中文 | 英文 | 一句话 |
|---|---|---|
| 管理控制台 | Management Console | 图形入口 ✅ 存续 |
| 命令行接口 | AWS CLI（v1→v2） | 命令族跨代同名 ⚠️ |
| 本地模拟 | DynamoDB Local | 离线桩，行为子集 ⚠️ |
| IDE 插件 | AWS Toolkit for Eclipse | 2014 入口，后退役 ⚠️ |
| 低层 JSON 语义 | low-level JSON API | 各入口共同底座 |
| 表激活 | CREATING→ACTIVE | 建表异步心智 |
| 批量写 | BatchWriteItem | ≤25 项部分失败语义 ⚠️ |
| 容量指标 | ConsumedCapacity/ThrottledRequests | 工具面必读的两张表 ⚠️ |
| 消耗回显 | return-consumed-capacity | CLI 选项级成本可见 ⚠️ |

## 最新演进与工业实践

- 文档锚 ✅（curl 200，台账 §7）：`https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html`、`https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/WorkingWithTables.html`。
- 工具现状 ⚠️：CLI v2、SDK v2.x 线、NoSQL Workbench 建模器、IDE 扩展——本书四入口二去其二；Local 非全保真口径。
- 工业实践 ⚠️：本地主流=容器化桩+契约测试；容量治理入口从「控制台看数」演进为「计费仪表盘+按需模式」（→ [04-分片与容量规划.md](04-分片与容量规划.md)）。
- 盘谱互证：本章为 #113 TDG 10 章（生态工具与 2026 前沿）提供 2014 基线回引（实链 ✅）。
