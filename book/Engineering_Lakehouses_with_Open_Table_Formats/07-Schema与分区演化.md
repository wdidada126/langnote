# 第 7 章 Schema 与分区演化

> ⚠️ 章题为**推定**（见 [00-总览与阅读地图.md](00-总览与阅读地图.md)）。
> 事实来源：Iceberg Spec（Schema Evolution / Partition Evolution）、Delta Protocol（Column Mapping）、
> Hudi 文档（Schema Evolution / 分区路径语义）。教科书对照：[../数据库系统概念6/08-关系数据库设计.md](../数据库系统概念6/08-关系数据库设计.md) 的模式演化讨论、Parquet 模式兼容规则。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 7.1 | 为什么 Hive 式改列会静默错数 | 位置绑定 vs 名字绑定 vs ID 绑定 |
| 7.2 | Iceberg：field-id 一统 schema 与分区 | 演化是"改映射表"不是"改文件" |
| 7.3 | Delta：column mapping 后发制人 | 内部 id ↔ 外部名的两本账 |
| 7.4 | Hudi：写入即演化 + 分区键的枷锁 | 灵活与约束并存 |
| 7.5 | 分区演化：Iceberg 独舞，两家绕行 | 换布局不换文件 |
| 7.6 | 演化工程守则 | 兼容矩阵、下游契约、回滚窗口 |

## 核心精讲

### 7.1 三档绑定方式

Parquet 文件按列名/列 id 自描述，但 Hive 读表按**位置**对齐 schema——
经典事故：`ALTER TABLE ADD COLUMN age INT` 加在中间位置，
旧文件的第 3 列（其实是 salary）被按名错位读成 age，**无报错、全错数**。

```text
位置绑定（Hive 原生）  最脆弱：列序即契约
名字绑定（Parquet 直读） rename 即丢数据（旧文件找不到列）
ID   绑定（Iceberg/Delta） 名字只是显示层，身份是不变整数 → 演化自由
```

### 7.2 Iceberg：一切皆 id

（详见 03 章 3.1）Schema 演化规则（Spec 明文）：

- **add column**：只改 `metadata.json` 的新 schema（分配新 `last-column-id`），
  旧文件缺列 → 读时按 `default-null`/缺省值补齐，**零数据移动**；
- **rename column**：改名字典，id 不动，旧文件照常按 id 命中；
- **drop column**：从当前 schema 移除 id；旧文件里该 id 的物理列读时被丢弃
  （列仍占存储，重写时才真正消失）；
- **update（类型放宽）**：仅允许无损加宽 int→long、float→double、
  decimal 扩精度、date→timestamp 等 Spec 枚举的"widening"；
  🔧 v3 起对嵌套字段的支持更完整（list/struct 内字段的增删改名）。

**读端投影机制**：引擎拿"查询 schema（当前）→ 文件 schema（旧）"的
id 映射改写 Parquet 读取请求。Parquet 文件写有
`schema.field-id`（Iceberg writer 负责落），这是整套机制的物证。

### 7.3 Delta：column mapping 模式

`spark.sql.delta.columnMapping.mode = none | name | id`：

- **name 模式**：列 id = 列名（当前），rename 安全（改映射），drop 后
  同名新增会**分配新 id**（靠 id 隔离）；
- **id 模式**：`delta.columnMapping.uuid` 全内部化，重命名/删除/重排彻底安全，
  代价是必须经过一次"重写元数据映射"的表属性变更；
- 限制（协议文档）：开启 mapping 后不可关闭；分区列改名受限
  （分区值物理上就在目录路径里，**这是 Delta 分区演化弱的根**）。

对照记忆：Iceberg 从第一天就是"id 模式"；Delta 是给存量表补了这门课。

### 7.4 Hudi：写入面灵活、分区面保守

- **schema evolution（写入触发）**：`hoodie.datasource.write.schema.evolve` 等
  配置下，新列自动并入表 schema（union by name 语义）；删除/改名依赖
  显式操作或 Spark `ALTER`，历史文件的列按名/位置对齐规则处理，
  **比 Iceberg 的 id 纪律弱**，宽表频繁改名场景易踩坑；
- 表 schema 存在 `.hoodie/.../meta`（commits 的 metaData）与 MDT schema 里；
- **分区路径即记录的一部分**：record key 索引含 partition path，
  分区演化 = 数据"分裂"在两种目录语义下，索引与查询都需双路兼容
  ——实践建议：分区键在建表时定死，演化需求交给 clustering。

### 7.5 分区演化：布局是元数据

Iceberg partition evolution 的机制（03 章 3.3 的推论）：

```text
spec 列表不可变 + 每个 data file 记住自己的 spec-id
查询规划：按"文件所属 spec"分别做谓词→分区值的转换
→ 新旧数据各用各的隐藏分区，互不干扰，零回填
```

典型路径：`day(ts)` 高基数扛不住 → 切 `month(ts)` 或直接上
`bucket(id, 512)`；旧文件保持 day 布局。代价：

1. **混合 spec 期间规划变复杂**（多套 transform 都要评估）；
2. 旧文件的分区裁剪按旧 spec 生效——想要新布局的裁剪红利，
   需要 `RewriteDataFiles` 按新 spec **重聚类**（第 8 章）。

Delta 的绕行方案是 **Liquid Clustering**：不设显式分区列，
按 clustering 列渐进重排文件（OPTIMIZE 增量执行），"演化"变成
"换 clustering 列 + 后台重排"；Hudi 对应 **clustering layout**（第 8 章对照）。

### 7.6 演化工程守则

| 守则 | 理由 |
| --- | --- |
| 改列名/类型走格式 API，禁止直接改 catalog 里的 schema 字段 | 绕过 id 映射 = 回到位置绑定的地狱 |
| 演化前列"下游谁在读"：BI 语义层、流式 sink、ML 特征快照 | 格式层零成本 ≠ 组织层零成本；time travel 读者可能被 schema 变更惊到 |
| 大改（拆/合并列）用"新增→双写→回填→切换→删除"五步 | 保持每步都向后兼容，回滚只是关双写 |
| 分区键变更前先做 30 天基数画像 | 演化虽免费，**错误的初始分区仍是昂贵的**（小文件/裁剪失效） |

## 例子：一次"改名 + 换分区"的完整时间线（Iceberg，教学示意）

```sql
ALTER TABLE orders RENAME COLUMN cust_id TO customer_id;   -- 仅 schema 层，秒级
ALTER TABLE orders ADD PARTITION FIELD bucket(32, customer_id)
  WITH DROP PARTITION FIELD days(order_ts);                -- 新 spec 成为 default
-- 新写入按 bucket 布局；旧文件仍按 days 布局可被正确裁剪
CALL iceberg.rewrite.sort_data_file_metadata(...)          -- 可选：按新布局重聚类旧数据
```

## 常见误区

| 误区 | 事实 |
| --- | --- |
| "drop column 省存储" | 当前读不再输出它，但旧文件里的列还在；空间只有重写才回收 |
| "改名要重写所有文件" | id 绑定下是 O(元数据)；需要重写的只是"直接读 Parquet 绕过表格式"的旁路消费者 |
| "分区演化后查询自动变快" | 旧数据不迁就新 spec；混合期规划开销可能先升后降（靠重写收敛） |
| "类型随便加宽，反悔也容易" | widening 单向（int 回不了 tinyint）；演化是**棘轮**，设计时留余量 |

## 与其他章的联系

- 7.2/7.5 → 03 章 3.1/3.3 的元数据结构支撑；
- 7.3 → 05 章 5.6 协议特性；
- 7.5 重写收敛 → 08 章"按新布局重聚类"；
- Parquet 名/id 绑定基础 → [../bigdata/09-存储与文件格式.md](../bigdata/09-存储与文件格式.md)；
- 模式变更作为架构主题的上位讨论 → [../设计数据密集型应用.md](../设计数据密集型应用.md)（演化与兼容章）。

## 思考题

1. 画一张"查询 schema→当前 schema→文件 schema"的三层映射图，
   解释 Iceberg 读一个"列已改名两次、类型加宽一次"的旧文件时，
   每一跳靠什么信息完成。
2. Delta 的 name 与 id 模式在"同名列被 drop 再 add"上的行为差异是什么？
   哪种模式下旧数据可能泄漏进新列？（协议文档求证。）
3. 为什么 Hudi 把"record key 含 partition path"的决策会让分区演化
   变成二等公民？从索引一致性角度给一条论证。
4. 设计题：一张被 200 个下游视图引用的表要改分区。
   利用 branch + 双写 + time travel 窗口，给一个**可回滚**的切换 runbook。
