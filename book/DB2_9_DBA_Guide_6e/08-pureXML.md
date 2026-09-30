# 08 · pureXML Storage Engine（Ch8 · DB2 9 的王牌）

> 章名 ✅ InformIT 出版社页实抓；正文 ⚠️ 转述重构。XML 存储引擎细节以 IBM Redbooks/公开文档口径，不可实测。

## 一、章定位

pureXML 是 DB2 9 区别于"把 XML 塞 CLOB"竞品的核心：XML 以二进制有序树（XDA）原生落盘，配 XML 索引、XQuery/XPath 嵌入 SQL、以及 9.5 的"标注分解（annotated shredding）"把 XML 内容映射到关系表。本章是全书技术纵深最深的一章之一，也是 733/735 XML 线考点源。

## 二、存储模型（⚠️ 转述）

1. 两种 XML 存储形态：
   - **well-formed**：整棵 XML 树存 XDA（XML Data Area），存于表内或独立 XDA 表空间。
   - **shredded（分解）**：按 XML Schema 注解把元素/属性映射进关系表（9.5 annotated shredding），SQL 直查、更新透明。
2. XDA 内部：节点有序编码、路径字典?（⚠️ 实现细节以 Redbooks 为准，本处保守转述）。
3. 数据流：XMLPARSE/XMLSERIALIZE 做 CLOB↔XML 显式转换；DB2XMLCACHE（纯 Java 环境需配）承担解析缓存（⚠️ 组件名以现行核）。
4. 验证：带 `VALIDATED`/`NO VALIDATION` 的列属性配 XML Schema Registry；注册走 `db2xdbreg`?（⚠️ 工具名存疑，原书演示以 SQL/XML 注册语法为主）。

## 三、查询面（XQuery + SQL/XML 双轨，⚠️ 转述）

```text
XQuery 独立语句：
  XQUERY 'for $c in db2-fn:xmlcolumn("CUST.INFO")/customer
          where $c/@status="A" return $c/name'
SQL/XML 嵌入：
  SELECT XMLQUERY('$d/customer/city' PASSING INFO AS "d")
  FROM cust WHERE XMLPASSING('exists($d/addr[@zip="10001"])' PASSING INFO);
```

- 谓词三件套：`XMLCONTAINS`/`XMLPASSING`/`XMLEXISTS`——写法演进淘汰关系（⚠️ 年代细节从简）。
- 函数族：XMLFOREST/XMLROOT/XML ELEMENT 构造，XMLCAST/XMLVALIDATE 校验转型。
- 驱动消费：CLI/JDBC 以 `SQL_XML` 类型与 `XMLEscape` 方言（⚠️ 细节存疑），应用层 DOM/SAX 慎用。

## 四、XML 索引（本章运维重点，⚠️ 转述）

1. 三型：**path index**（全局路径字典，几乎必建）、value index（标量/区域）、node/value 区域索引组合。
2. 建法：`CREATE INDEX ... ON t(info) PATH DEFAULT? INCLUDE (...)`（语法面 ⚠️ 保守）。
3. 裁决逻辑：优化器用路径索引定位候选区域，再值索引/扫描过滤——选择率统计与 12 章 RUNSTATS 的 XML 面（distribution on path）衔接。
4. 分解表上则是普通 B 树索引——shredded 形态下"XML 性"消失，性能换表达力。

## 五、性能与容量视角（原书实验叙事，⚠️）

- well-formed：写入快（免解析落库）、查询靠索引、更新粗（整文档替换倾向）。
- shredded：读关系侧极快、装载需经分解器批量重解析、schema 变更即数据迁移。
- 混合策略（本章结论）：文档整体读少改、或结构不稳定 → well-formed+path/value 索引；查询谓词稳定高频字段 → 标注分解。
- XML 列入分区表/压缩等组合限制逐版漂移（⚠️ 以现行文档核）。

## 六、易错雷点（例题库精华）

1. 忘建 path 索引，XQuery 全表扫 + 文档解析风暴。
2. `XMLVALIDATE` 未配 schema 注册，校验静默失效。
3. CLOB 隐式转 XML 每行重解析：批量迁移应先 `XMLPARSE` 后 INSERT。
4. 分解表的"更新透明"在嵌套可选节点上触发整文档回写，隐性热点。
5. DB2XMLCACHE 关闭/配置漂移导致 Java 侧性能悬崖（⚠️ 组件年代）。
6. 字符集：XML 声明编码与库 codepage 不一致致序列化乱码（→15 章）。

## 七、自查问题

- well-formed vs shredded 的六维对比（写/读/更/索引/schema 演化/装载）？
- path 索引为何"几乎必建"？它存的是什么？
- XMLEXISTS 与 XMLCONTAINS 的代际关系（⚠️ 保守答）。
- 标注分解里"注解（annotation）"绑定的是什么与什么？
- XML 列统计怎么采、怎么进优化器成本？（接 12 章）
- 为何说 pureXML 是"关系-文档双模型"而非文档数据库？与 MongoDB 的本质差异一句话？
- 本章在 #76 认证册（登记名）中对应域为何弱化？（Db2 11 考纲 XML 权重 ⚠️）
- XML 列上做范围分区/压缩各受什么限制？（第五节末条，保守答）
- 整文档替换更新为何是 well-formed 形态的软肋？（第五节第 1 条推演）
- XMLEXISTS 谓词与 path 索引的加速关系链条？（第四节第 3 条）
- 分解形态下"XML 性消失"具体指哪三件能力退化？（第四节第 4 条）

## 十、XML 运维工单清单（DBA 视角，⚠️ 重构）

1. 新表含 XML 列：确认 XDA/独立表空间落位（11 章）、schema 注册与 VALIDATED 策略。
2. 慢 XQuery 三联查：path 索引存在?→统计新鲜度（12 章 distribution）→谓词可否下推为 SQL（shred 候选评估）。
3. 索引爆炸控制：value 索引按热点路径裁剪，忌"全路径建值索引"。
4. 分解表漂移：schema 变更=重分解工程——评审时按迁移项目估工时。
5. 缓存巡检：DB2XMLCACHE 命中率/内存参数（年代组件，⚠️ 现役读法为通用缓冲池面，11 章）。
6. 坏文档治理：验证失败的入库路径（应用侧前置 vs 库侧 XMLVALIDATE 拒收）要有裁决记录。
7. 容量趋势：XML 列高增长表的 XDA 页膨胀监控（快照/表函数面，14 章接口）。
8. 退役评审：是否把稳定谓词字段"晋升"为关系列或分解表——每季一次架构复盘。

## 十一、标准与代际时间轴（⚠️ 保守口径）

| 件 | 时间锚点 | 状态 |
|---|---|---|
| XQuery 1.0 / XPath 2.0 W3C 建议 | 2007 | 与本书同年，DB2 9 跟进 |
| SQL/XML 标准函数族 | 2000s | DB2 为早期拥趸 |
| annotated shredding | 9.5 | 本章主打之一 |
| XML 检索/文本增强 | 9.7–10 | 书后 |
| JSON 函数族 | 11.5 | 本章的接班叙事 |

## 十二、快速回看卡（本文件内导航）

- 一句话定调：pureXML≠CLOB 伪装——第一节与第二节第 1 条。
- 形态选择口诀：第三节末"文档读少改→well-formed；谓词稳定→shred"。
- 索引三型与建法：第四节 1–2 条；统计衔接→12 章 E 组类比（🔧 在 12 章，非本章）。
- 雷点优先级：第 1 条（忘 path 索引）占实战事故半壁。
- 跨引擎出口：本节时间轴 + 演进节 Snowflake/Redshift 半结构化对照。

## 核心概念速览（中英对照）

- **pureXML** — 原生 XML 存储：二进制有序树落盘的引擎特性
- **XDA** — XML Data Area：XML 树存储区（可独立表空间）
- **well-formed** — 良构存储：整文档形态保存
- **shredding** — 分解：XML 内容映射进关系表
- **annotated shredding** — 标注分解：Schema 注解驱动映射（9.5）
- **XQuery** — XML 查询语言：FLWOR 式文档查询
- **SQL/XML** — SQL 的 XML 函数族：XMLQUERY/XMLTABLE 等
- **path index** — 路径索引：全局 XML 路径字典加速
- **value index** — 值索引：标量/区域路径上的值加速
- **XMLSchema registry** — Schema 注册：校验与分解的依据库
- **XMLPARSE/XMLSERIALIZE** — 序列化对：CLOB↔XML 显式转换
- **XMLPASSING/XMLEXISTS** — 存在谓词：谓词式文档过滤
- **DB2XMLCACHE** — XML 解析缓存（⚠️ 年代组件）

## 最新演进与工业实践

- 现状：pureXML 仍是 Db2 LUW 在售特性，Db2 11.5/12 文档保留 XQuery/XML 索引全量；但**JSON 半结构化**（JSON 类型、JSON_TABLE，11.5+）接棒新场景，XML 退守存量政务/报文/医疗 HL7 等（⚠️ 趋势转述；入口 ✅ https://www.ibm.com/docs/en/db2 ）。
- 标准侧：XQuery 3.1/XML 1.1 在 DB2 覆盖有限（⚠️）；SQL/XML 标准函数族持续对齐。
- 工业对照：Snowflake/BigQuery 的半结构化以 VARIANT/RECORD 面重演"文档 vs 分解"取舍——本章的六维权衡框架跨引擎可复用（对照 [../Amazon_Redshift_TDG/00-总览与阅读地图.md](../Amazon_Redshift_TDG/00-总览与阅读地图.md) SUPER 数据类型节）。
- 理论锚点："关系-层次双模型"之争可回读红宝书脉络与论文线 [../../db/db.md](../../db/db.md)（对象关系/XML 条目）；教材面 [../高性能mysql.md](../高性能mysql.md) 未涉 XML，本册补半结构化历史一环。
- 备考提示：Db2 11.1 认证域 XML 权重低（⚠️），以 #76 登记册考纲为准；本章读法转为"半结构化存储设计思维"。
