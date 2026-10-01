# 06 · API 集成与数据格式

> 章题 ⚠️ 推定（重构依据：✅ 官方导读句「Call APIs from applications to DynamoDB and retrieve data in appropriate formats for other applications」，见 [00-总览与阅读地图.md](00-总览与阅读地图.md) §2/§6）。三态：✅ 实证 / ⚠️ 转述推定 / 🔧 本机类比实测（**非 DynamoDB 行为**）。

## 1. 章定位

- 本章从「工具面」（[02-访问途径控制台CLI与插件.md](02-访问途径控制台CLI与插件.md)）下沉到**协议面**：应用如何通过 API 读写 DynamoDB、数据以什么形状进出。
- 2014 语境：Java/PHP/Ruby/.NET/Node/Python SDK 并立，高层/低层两套 API 是 AWS SDK 的既有分层 ✅（概念在场）；书中「appropriate formats」指向与 Redshift/S3/MapReduce 的数据交接（→ [07-AWS生态协同Redshift_S3_MapReduce.md](07-AWS生态协同Redshift_S3_MapReduce.md)）✅ 导读句。

## 2. 两套 API 的分层（⚠️ 转述+✅ 概念）

| 层 | 面向对象 | 数据形状 | 现代对应 ✅ |
|---|---|---|---|
| 低层 API | 手抠协议者 | 类型标签 JSON：`{"S":"x"}`/`{"N":"42"}` | DocumentClient/ResourceClient 线 |
| 高层 API | 应用开发者 | 本地对象↔表项映射（marshalling） | Mapper/ObjectWrapper 线 |

- 类型标签制是 DynamoDB 数据格式的第一性事实 ✅：JSON 无原生数值/二进制/集合区分，故协议层用标签补足 ⚠️。
- 空串不可、数字精度上限等「格式税」⚠️（2014 痛点，部分已随类型演进缓解 ⚠️）。
- SDK 换代登记 ⚠️：boto→boto3、v2 SDK 线为 2014 后事物——本书示例代码今天需整体翻译。

## 3. CRUD 操作语义（API 视角 ⚠️→✅）

- `PutItem`：整项替换——「读-改-写」裸用即竞态 ⚠️；条件写（ConditionExpression）后补 ✅。
- `UpdateItem`：属性级增量（SET/REMOVE/ADD）✅ 概念至今。
- `DeleteItem`：按全键删除 ✅。
- `BatchWriteItem`：≤25 项、无原子性保证、需自处理 UnprocessedKeys ⚠️→✅。
- `TransactWriteItems`：2018 后才有真多表原子——2014 年本书只能给「补偿式设计」⚠️（transactions.html ✅）。
- 幂等：`ClientRequestToken` 消重 ⚠️→✅（文档线收录）。

## 4. 序列化与「适当格式」命题 ✅ 导读+⚠️

- 表项 ↔ 领域对象 ↔ 传输 JSON 的三段映射是「for other applications」的落点 ⚠️。
- 嵌套 Map/List 作文档化建模（→ [01-数据建模概念与单键模型.md](01-数据建模概念与单键模型.md) T5/D10 形状）✅ 类型系统。
- 集合类型（SS/NS/BS）适合标签/去重集，不适合有序列表 ⚠️。
- 分页 token 作为 API 契约外露（→ [05-查询与扫描访问模式.md](05-查询与扫描访问模式.md)）⚠️。

## 5. 🔧 本机类比实验（**非 DynamoDB 行为**）

| 组 | 实验与真实输出 | 类比点 | 边界 |
|---|---|---|---|
| D1 | DuckDB `profile.name` STRUCT 路径取值 | 嵌套属性的路径语法 | 无类型标签 JSON |
| D15 | SQLite `json_extract(doc,'$.user.addr.city')`→'SH' | 深层属性访问/投影 | 服务端无此函数 |
| D13 | `json_extract` 双引擎均可用 | marshalling 前的文本层 | 类型标签制不存在 |
| T7 | 约束冲突→ROLLBACK→0 行 | 事务语义对照 TransactWrite 缺席的 2014 | 单机非分布式 |
| D12 | 条件 UPDATE 成功 1 行/失败 0 行 | 条件写（原子 read-modify-write 形状） | 无网络重试语义 |
| T5 | TEXT 列存整文档再解析 | PutItem 整项替换的粗暴版 | 无 400KB/键约束 |

D12 补充叙述：`UPDATE c SET stock=stock-1 WHERE pk='sku1' AND stock>0` 返回 rowcount=1、值变 4；换不可能条件 rowcount=0——这正是 DynamoDB 条件写「失败=0 影响」直觉的本机替身（**非 DynamoDB 行为**）。

## 6. API 设计检查单（本章工程输出 ⚠️）

- 读接口是否透传游标（LastEvaluatedKey）而非页码 ⚠️。
- 写接口是否声明幂等键（ClientRequestToken 类）⚠️。
- DTO 与表项解耦：类型标签 JSON 不应漏进公网 API ⚠️。
- 数值一律走 N 标签或字符串承载，避免浮点尾差 ⚠️。
- 大项（近 400KB）走「文档拆块+计算键」方案而非塞单行 ⚠️（联动 [01-数据建模概念与单键模型.md](01-数据建模概念与单键模型.md)）。

## 7. 演进桥（2014→2026，详见文末节）

- 本书时代：无事务 API、无 PartiQL、条件参数用旧式 Expected ✅ 导读语境+⚠️。
- 现代：条件写/幂等 token/事务/PartiQL 全面补位 ⚠️（年代转述）。
- 「appropriate formats」的当代答案同时包括：标准 JSON 序列（低层）与 **DynamoDB 数据模型 JSON 规范**（导入导出/S3 用）✅（S3DataImport.html 线收录格式文档 ⚠️ 命名转述）。

## 8. 挂点

- 前置 [02-访问途径控制台CLI与插件.md](02-访问途径控制台CLI与插件.md)（CLI=API 壳）、[05-查询与扫描访问模式.md](05-查询与扫描访问模式.md)（读写动词）。
- 后继 [07-AWS生态协同Redshift_S3_MapReduce.md](07-AWS生态协同Redshift_S3_MapReduce.md)（数据格式的外溢通道）。
- 平行 [../Amazon_DynamoDB_TDG/00-总览与阅读地图.md](../Amazon_DynamoDB_TDG/00-总览与阅读地图.md) 03 章（2022 CRUD 实操，在盘实链）；NoSQL API 谱系对照 [../MongoDB_The_Definitive_Guide_3e/00-总览与阅读地图.md](../MongoDB_The_Definitive_Guide_3e/00-总览与阅读地图.md)（驱动/序列化层同题，在盘实链）。

## 9. 类型标签速查（低层 JSON 形状 ⚠️ 示例为本目录自拟）

| 类型 | 标签形状 | 注意 |
|---|---|---|
| 字符串 | `{"S":"x"}` | 不可空串（历史约束）⚠️ |
| 数字 | `{"N":"42.5"}` | 字符串承载数值 ✅ |
| 二进制 | `{"B":"base64"}` | SDK 编码差异 ⚠️ |
| 布尔 | 无原生标签 → `{"BOOL":true}` ✅ | 2014 后补位 ⚠️ |
| 空 | `{"NULL":true}` ✅ | 与「缺属性」两概念 ⚠️ |
| 列表 | `{"L":[…]}` ✅ | 有序可重 |
| 映射 | `{"M":{…}}` ✅ | 嵌套文档主体 |
| 集合 | `{"SS"/"NS"/"BS":[…]}` ✅ | 无序去重同质 |

## 10. 集成模式清单（「for other applications」的落地形 ⚠️）

1. Web API 直连 SDK：低延迟但凭证明文风险上移 ⚠️。
2. 代理层收口：API Gateway/Lambda 形态为 2014-2015 后主流 ⚠️（本书时代只能 EC2 自建 ⚠️）。
3. 批处理侧车：Hadoop/Spark 读写表（→ [07-AWS生态协同Redshift_S3_MapReduce.md](07-AWS生态协同Redshift_S3_MapReduce.md)）。
4. 移动客户端直连：本书「Eclipse 插件」年代的典型画像 ✅ 工具句旁证。
5. 异构双写：DynamoDB 主存+搜索引擎副存（OpenSearch/Elastic 类）最终一致对账 ⚠️。

## 11. 错误与重试预算（API 面 ⚠️→✅）

- `ProvisionedThroughputExceededException`：2014 单键模型时代最常见的「客户端责任错误」——超限即回，指数退避+抖动是 SDK 层标配 ✅（best-practices.html 线收录 ⚠️ 措辞转述）。
- `Throttling` 与 `ConditionalCheckFailed` 必须在应用侧分道处理：前者重试、后者是业务语义（如库存已抢完）不可盲重 ⚠️。
- 批量写残项 `UnprocessedItems` 的重投循环要有次数上限与告警出口，否则形成无限自 DoS ⚠️。
- 读侧一致性开关（强一致读按 2 倍 RCU 计费）⚠️→✅：「appropriate formats」之外，API 还暴露「appropriate consistency」这一维。
- 对照本机：SQLite `busy_timeout`/`SQLITE_BUSY` 是单机版「限流重试」同构题（见 [00-总览与阅读地图.md](00-总览与阅读地图.md) 🔧 台账，**非 DynamoDB 行为**）。

## 核心概念速览（中英对照）

| 中文 | 英文 | 一句话 |
|---|---|---|
| 低层 API | low-level API | 类型标签 JSON 直写 ✅ |
| 高层 API | high-level/document API | 对象-项映射层 ⚠️ |
| 类型标签 | attribute value（S/N/B/MAP/LIST/SET） | JSON 之上的类型补足 ✅ |
| marshalling | 序列化/映射 | 本地对象↔项转换 ⚠️ |
| 条件写 | conditional write | 表达式化约束 ✅（语法后补 ⚠️） |
| 幂等 token | ClientRequestToken | 重试去重 ✅ |
| 批量写残项 | UnprocessedItems | 部分失败自理 ⚠️→✅ |
| 属性路径 | attribute path（`$.a.b` 形） | 嵌套访问语法 ✅/⚠️ |
| 事务写 | TransactWriteItems | 2018 补位 ✅/⚠️ |
| PartiQL | PartiQL for DynamoDB | 关系语法入口（2021 ⚠️）✅ URL |

## 最新演进与工业实践

- 文档锚 ✅（curl 200 台账 §7）：`https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html`、`https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/transactions.html`、`https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/LowLevelPartiQL.html`。
- **事务**（2018 ⚠️）：TransactGet/TransactWrite 为多表原子与竞争条件（库存扣减类）提供服务端保证——本书时代只能应用补偿的痛点被官方收编 ✅ 页面存在。
- **PartiQL**（2021 ⚠️）：`SELECT` 风格读写 + 批量语句 ✅（LowLevelPartiQL.html）——「appropriate formats」命题新增 SQL 方言出口。
- SDK 现状 ⚠️：v2/v3 多语言 SDK 与 AWS SDK 统一品牌；高层映射成为默认姿势。
- 工业实践 ⚠️：DTO/表项双 schema 管理、幂等 token 标配化、近 400KB 大项改走 S3+引用模式（联动 [07-AWS生态协同Redshift_S3_MapReduce.md](07-AWS生态协同Redshift_S3_MapReduce.md)）。
- 盘谱对位：MongoDB 驱动序列化（[../MongoDB_The_Definitive_Guide_3e/00-总览与阅读地图.md](../MongoDB_The_Definitive_Guide_3e/00-总览与阅读地图.md) 在盘）与 DynamoDB marshalling 同为解决「对象↔存储文档」断层 ⚠️。
