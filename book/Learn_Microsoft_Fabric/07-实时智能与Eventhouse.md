# 07 · 实时智能与 Eventhouse —— Learn Microsoft Fabric（⚠️ 主题重构章）

> **降级声明**：原书目录未获任何渠道实证（负结果台账见 [00 · 总览与阅读地图](00-总览与阅读地图.md) §2），本章为主题重构章。
> 机制 = 官方文档转述 ⚠️（✅ <https://learn.microsoft.com/en-us/fabric/real-time-intelligence/overview>、
> ✅ <https://learn.microsoft.com/en-us/fabric/real-time-intelligence/eventhouse>、
> ✅ <https://learn.microsoft.com/en-us/fabric/real-time-intelligence/create-eventhouse>，2026-10-02 验 200）。
> 兄弟册同题：[../Fundamentals_of_Microsoft_Fabric/07-实时分析Eventhouse与事件流.md](../Fundamentals_of_Microsoft_Fabric/07-实时分析Eventhouse与事件流.md)（不同书，见 00 §3）。

## 1. 本章定位

- Real-Time Intelligence（RTI）= Fabric 的「秒级到分钟级」分析栈：事件流（Eventstream）进、
  KQL 数据库/Eventhouse 存查、实时仪表板看（⚠️ 转述）。
- 教学书的切入姿势（⚠️ 推定）：从「日志/传感器/业务事件」三类活的例子出发，区别于批处理章的
  「历史账本」心智。

## 2. 组件拆解（⚠️ 转述官方 overview）

- **Eventstream**：摄取层——连接 Kafka/嵌入事件应用/Hub 类源，配转换（简 DSL/笔记本介入）后
  写入目标（⚠️ 转述）。
- **Eventhouse**：RTI 的分析库容器，内部是 **KQL 数据库**（Kusto 血统查询引擎）+ 可选
  **实时仪表板**（⚠️ 转述官方 eventhouse 页）。
- **Real-Time Hub / 连接器生态**：预置数据源与 Fabric 生态内联动（与湖仓/仓库互查）（⚠️ 转述；
  该词现行文档形态本轮未单独定位页，登记 ⚠️ 缺口）。
- **Captured/Reference/User-defined 表三分**：平台捕获表、维表参考、自定义流表——保留策略各异（⚠️ 转述）。

## 3. KQL 心智：和 SQL 差在哪（⚠️ 转述 + 重构对比）

- 管道式运算符链（`where → summarize → project`）天然贴合「事件流过滤聚合」叙事；时序默认、
  弱 schema 弹性、高吞吐追加（⚠️ 转述）。
- 与批侧对照：05 章 T-SQL 问「账本余额」，本章 KQL 问「最近 5 分钟发生了什么」——
  **问时态不同，不是语法口味不同**。
- 理论纵深（盘上实链）：流式系统语义（时间戳/窗口/乱序）看
  [../Streaming_Systems/00-总览与阅读地图.md](../Streaming_Systems/00-总览与阅读地图.md) 与
  [../Introduction_to_Apache_Flink/00-总览与阅读地图.md](../Introduction_to_Apache_Flink/00-总览与阅读地图.md)；
  KQL 的「引擎出身」是 Kusto 服务栈——Fabric 侧的裁剪与计费语义本机不可实测 ⚠️。

## 4. Kafka 兼容与生态缝（⚠️ 转述）

- Eventstream 支持 Kafka 兼容端点接入既有生产者——「不改代码先接进来」是迁移卖点（⚠️ 转述，
  兼容级别细则当日页核实）。
- 与湖仓的缝：事件数据沉淀到 OneLake 供批侧 join（RT ↔ batch 汇合点）——教学项目常设
  「告警走实时、日报走批」双车道练习（⚠️ 重构）。

## 5. 上手机 checklist（⚠️ 重构练习位）

1. 建 Eventhouse；选择模板/示例数据源跑通「进→存→看」最短路径（✅ create-eventhouse 页 200）。
2. 写三条 KQL：窗口计数、异常峰值、按设备 top-N；记录墙钟感受保留策略影响。
3. 挂一个事件流源（模拟 JSON 事件亦可），观察迟到与乱序在仪表板上的表现。
4. 把当日事件聚合结果落湖表，与 05 章仓库表 join——打通本册「双流汇 OneLake」的收官动作。

- 注：本章无独立 🔧 实验——RTI 摄取/保留为平台行为，本机 SQLite/DuckDB 无对应语义，
  强行类比反失真；全册 🔧 六组清单见 [00 §7](00-总览与阅读地图.md)（≥4 组义务已由 E1–E6 满足）。

## 6. 本章在盘上目录版中的对位

- 兄弟册 07 章（同题不同书）：口径互证；引用带册别（00 §3）。
- 流式理论：上段已链 Streaming_Systems / Flink；Paimon 流湖对照
  [../Apache_Paimon_Streaming_Lakehouse/00-总览与阅读地图.md](../Apache_Paimon_Streaming_Lakehouse/00-总览与阅读地图.md)。
- 实时 OLAP 对照：[../Amazon_Redshift_TDG/00-总览与阅读地图.md](../Amazon_Redshift_TDG/00-总览与阅读地图.md) 的流式装载章、
  Snowflake 册的 Snowpipe 语义（登记于 00 §6）。
- 索引：[../数据库系列·总索引.md](../数据库系列·总索引.md)。

## 7. RTI 名词到动线的映射表（重构速查）

| 动线环节 | 名词 | 一句话职责 |
|---|---|---|
| 接 | Eventstream 源设置 | Kafka/事件应用类入口挂子 |
| 转 | Eventstream 转换器 | 轻清洗与路由分叉 |
| 存 | KQL 数据库（Eventhouse 内） | 高吞吐追加与保留策略宿主 |
| 查 | KQL 查询面 | 窗口/异常/top-N 的时态问法 |
| 看 | 实时仪表板 | 秒级可视出口 |
| 沉 | 湖表落点 | 与批侧汇合的沉淀口 |

## 8. 教学 FAQ（重构问答位，⚠️ 非原书）

- **问：KQL 要专门学吗？** 答：会 SQL 者一周上手管道式语法；真正的门槛是**时态心智**
  （乱序/迟到/窗口），理论补课见 §3 的流处理书目实链。
- **问：Eventhouse 和湖仓表谁做事件的主存储？** 答：热窗（分钟-天级）在 KQL，长史沉淀进
  Delta/开放表；「全放 KQL」付保留成本，「全放湖」付新鲜度损失——按查询时态半径切（⚠️ 判读）。
- **问：捕获表结构漂移怎么办？** 答：KQL 弱 schema 弹性是特性，但下游 join 需契约化
  （投影视图当接口）（⚠️ 重构共识）。
- 无 🔧 声明重申：RTI 摄取/保留/并发为平台行为，本机无对应物，本册不硬凑类比
  （全册 🔧 义务由 E1–E6 在 02/03/04/05/08/10 章满足，见 00 §7）。

## 9. 章末自测（重构题，⚠️ 非原书习题）

1. 用六个环节复述「一条传感器 JSON 从进来到进报表」的动线。
2. 「最近 5 分钟」与「账本余额」两个问时态分别落到哪个面？
3. Kafka 兼容端点对既有生产者意味着改什么、不改什么（⚠️ 当日核兼容级别）。
4. 写出 RT 双车道项目的两条 SLA 草案（告警延迟/日报新鲜度）。

## 10. 快照与复核记录（本册取证纪律的章内落点）

- 本章 ✅ 快照日：2026-10-02（全册统一）；引用的 ✅ URL 清单登记于 [00 §5](00-总览与阅读地图.md)，
  正文未逐条重复验证的**细页**默认 ⚠️ 转述（波 5 册同纪律，两册快照相隔 5 天即有 404 漂移，
  见 00 §5 互证段）。
- 复核动作三件套：①当日站内搜索现行 URL；②比对 whats-new（✅ 2026-10-02 验 200）近 90 天条目；
  ③把与本章冲突的旧二手资料标注「化石」而非直接引用。
- 考点互鉴（⚠️ 推定口径）：DP-600 域与本小节的对应关系已在 00 §6 阅读地图标注，复习时
  按「名词→动线→边界声明」三层过一遍，不背未实证数值。

## 核心概念速览（中英对照）

| 中文 | 英文 | 一句话 |
|---|---|---|
| 实时智能 | Real-Time Intelligence | Fabric 秒-分钟级分析栈 |
| 事件流 | Eventstream | 摄取与轻量转换层 |
| 事件库 | Eventhouse | KQL 数据库的分析容器 |
| KQL | Kusto Query Language | 管道式时态查询语言 |
| 捕获表 | captured table | 平台按源自动建的事件表 |
| 参考表 | reference table | 流侧 join 的小维表 |
| 实时仪表板 | real-time dashboard | RTI 原生可视面 |
| Kafka 兼容 | Kafka-compatible endpoint | 既有生产者零改接入 |

## 最新演进与工业实践

- 增量线（⚠️ 转述）：RTI 是 Fabric 各栈中最新的一族——Eventhouse 正式命名、Kusto 血统资产
  并入、Real-Time Hub 场景包扩充都在 2024–2026 滚动发生；教学书版本间差异最大的通常就是本章，
  **凡「预览」字样一律当日重验**（✅ whats-new 页 2026-10-02 验 200）。
- 工业实践：事件面治理三问=保留期×PII×告警疲劳；RTI 项目失败常因把「实时」当默认——
  先问业务真需要秒级吗（⚠️ 转述共识）；DP-600 考点画像：分清 Eventstream/Eventhouse/
  湖表三者的数据停留位置（⚠️ 推定）。
