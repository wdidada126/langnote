# 第 4 章 Schema 演化：字段 ID、允许与禁止

> ⚠️ 章题为**推定**（示意日文名：スキーマの進化），原书真实目录未核实，见 [00-总览与阅读地图.md](00-总览与阅读地图.md)。
> 依据：spec §Schema Evolution（field-id 模型、允许/禁止操作表、类型提升规则）与官方 `docs/evolution.md`、`docs/schemas.md`。

## 本章地图

> 一句话：**Iceberg 的列身份是不变的整数 field-id，不是名字、更不是位置——schema 演化因此只是「给 ID 集合打补丁」，永远是元数据层的 O(1) 操作。**

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 4.1 field-id 模型 | 每列一个永不复用的整数 ID | 名字/位置只是显示属性 |
| 4.2 允许的操作 | add/rename/drop/reorder/提升/改注释 | 全部只换根文件 |
| 4.3 类型提升 | int→long、float→double、decimal 加宽 | 有明确的「可无损」清单 |
| 4.4 禁止的操作 | 结构改写类（nesting/flatten/跨父移动） | 会破坏 ID 语义，规范直接禁止 |
| 4.5 嵌套列演化 | 改 struct 内子字段同样安全 | 点号路径引用，ID 定位 |
| 4.6 与 Parquet 的协作 | 文件按 field-id 写/读 | 老文件缺列=按 schema 补 null |
| 4.7 默认值（v3） | initial-default / write-default | 🔧 从「加列必 null」到「加列带默认」 |
| 4.8 与 Hive 对比 | 名字+位置 vs ID | 为什么 Hive 改列名会静默错位 |

## 核心精讲

> **教学示意，不参与构建。** ALTER 语法核对自官方 spark-ddl/evolution 文档。

### 4.1 一切从 field-id 开始

spec 的类型系统给每个字段分配表内唯一整数 ID：嵌套字段的 ID **不随父字段移动而改变**；`last-column-id` 是分配水位（§2.2），删掉的列 ID **永不复用**。三条推论：

1. 改名只是改「标签」：`RENAME COLUMN` 不动任何数据文件里的字节；
2. 删列只是从当前 schema 里去掉一个 ID：老文件里残留的该 ID 数据被读取时忽略；
3. 加列只是新增一个 ID：读老文件时该 ID 不存在 → 返回 null（或 v3 默认值，§4.7）。

统计、分区字段（source-id）、equality delete 的 `equality_ids`、加密与 Puffin 里的列引用……**全部按 ID 键控**——所以改名不会弄坏剪枝，删列不会弄错桶。

### 4.2 允许的操作（规范原文枚举的语义）

| 操作 | 语义 | 代价 |
| --- | --- | --- |
| 加列（含嵌套子列） | 新字段 + 新 ID；历史读取补 null | O(1) |
| 改名 | 仅换标签 | O(1) |
| 删列 | 从当前 schema 移除 ID；数据可能仍在文件里 | O(1) |
| 重排（reorder） | 改 schema 内顺序；读取按 ID 匹配，不靠位置 | O(1) |
| 类型提升 | 见 §4.3 | O(1) |
| 改注释 | 纯元数据 | O(1) |

语法（Spark 方言，已核对官方示例）：

```sql
ALTER TABLE prod.db.sample ADD COLUMNS (new_column string COMMENT 'new_column docs');
ALTER TABLE prod.db.sample ADD COLUMN point.z double;            -- 嵌套
ALTER TABLE prod.db.sample RENAME COLUMN data TO payload;
ALTER TABLE prod.db.sample ALTER COLUMN measurement TYPE double COMMENT 'unit is bytes per second';
ALTER TABLE prod.db.sample ALTER COLUMN nested.col AFTER other_col;
ALTER TABLE prod.db.sample ALTER COLUMN id DROP NOT NULL;        -- 🔧 放宽约束是安全方向
ALTER TABLE prod.db.sample DROP COLUMN id;
```

### 4.3 类型提升（promotion）的边界

允许（「更宽且可无损表示旧值」）：
- `int → long`；`float → double`；`decimal(p,s)` 仅加宽 p（s 不变）；`date → timestamp`（微秒；v3 可到纳秒）；字符串 `→ binary` 与反向的有限情形（UTF-8 字节等价的实现间约定）。

禁止的原因同样规范先行：
- 任何改变**分区 transform 哈希输入**的提升被拒（`int→long` 若该列是 `bucket` 源列：bucket 定义会变→同一值算出不同桶→静默错数据）。identity/day 类变换的源列提升相对宽松，但要逐 transform 核对官方表格；
- `long→int`、精度缩小、时间戳单位缩窄：截断即有损。

**规范给的是「允许集」，不是「实现兜底」**：遇到文档没写的提升组合（如 `timestamp→timestamp(9)` 在 v2），按「不支持即报错」预期。

### 4.4 禁止清单（结构改写类）

以下在规范层面就不存在「安全的演化路径」：

- 把若干字段打包进新嵌套结构（字段 ID 归属变了，读老文件无法还原）；
- 子字段在父结构间迁移；
- 基元列 → struct/list/map；
- 单字段 struct 展平。

要「重构成新形状」：新增目标列 + 后台 `INSERT OVERWRITE`/回填补数据 + 删旧列（三段式），或干脆建 v2 表迁移。**Iceberg 帮你的是演化，不是重构**。

### 4.5 嵌套列

列表按位置存（list 元素没有独立命名的历史？——有：元素字段也有 ID，重排/改元素类型受同样规则约束；map 的 key/value 亦然），读取端按「`a.b.c` 路径 → ID 序列」匹配，缺路径返回 null。`ALTER COLUMN point.z TYPE float` 提升叶子即可，不必动 `point`。

### 4.6 文件层怎么配合（Parquet 视角）

Iceberg 写 Parquet 时把 field-id 写进列元数据（`field.id` key-value）；读老文件：Parquet 列 → ID → 当前 schema 字段名。于是：

- 文件里的列名/顺序与当前 schema 不一致**无所谓**；
- 老文件没有的新 ID → 规划器注入 null 常量列；
- 已删列残留在文件里 → 被忽略（想物理清掉要重写，第 8 章 compaction 顺带做）。

这也是与 [../bigdata/09-存储与文件格式.md](../bigdata/09-存储与文件格式.md) 的接口点：**Iceberg 的演化纪律把「列式文件的按名读取」升级成了「按 ID 读取」。**

### 4.7 🔧 v3 默认值

v1/v2 加列永远补 null（「NOT NULL 列只能后加？」——不能，加列必可空，v3 之前）。v3 在 schema 上声明：

- `initial-default`：读历史缺失数据时使用的默认值（如 0、`'unknown'`）；
- `write-default`：写入未指定时的默认值。

限制：复杂/半结构化类型（struct/list/map/variant）不允许 non-null 默认。对「事件表后来加维度列不想看 null」的场景，这是从「回填任务」到「一行 DDL」的替代。老引擎读到带默认值的 v3 schema 会失败——版本混用纪律同 §4.3。

### 4.8 与 Hive 表的正面对比

| 场景 | Hive（名字+位置对齐） | Iceberg（ID 对齐） |
| --- | --- | --- |
| 改列名 | Metastore 改了，文件里还是旧名；**按位置读的老引擎静默错位** | 安全，O(1) |
| 中间插入列 | 后续列全体错位（除非 SerDe 按名） | 安全 |
| 删列 | 文件残留，读时偏移 | 安全（按 ID 忽略） |
| 类型变更 | 基本靠重写赌一把 | 允许集内即时生效 |

注意：Iceberg **不修复**你从 Hive 迁移来的历史文件里名字/位置的脏问题（migrate/snapshot 过程只登记文件）；迁移时保证列顺序与类型对当前 schema 一致是前置检查项（第 8/9 章 migrate）。

## 版本演进与兼容性

- 完整演化语义自 0.6（2018）起是 Iceberg 的立身之本；
- 1.x 期间逐引擎补齐 DDL 面（Trino `SET NOT NULL`、Flink 部分 ALTER 依赖版本）；
- v3：默认值、`unknown` 类型（占位列，读时 null/默认——配合部分回填补数据的语义）；🔧 变体 `variant` 半结构化列的引入（第 1.5 节）。
- 兼容性铁律：**所有写引擎必须支持当前 schema 特性**；一个不认 v3 的边车写引擎会把默认值写丢，这类「按最低版本行事」在多方共享表上要写进 runbook。

## 常见误区

| 误区 | 事实 |
| --- | --- |
| 「加列要回填才能查」 | 读老数据即时补 null（v3 可补默认值）；只有业务要求非空值才需要回填 |
| 「删列=数据没了」 | 只是当前 schema 不再引用该 ID；文件里可能仍有，物理清理靠重写 |
| 「改名后历史查询用新名查不到旧数据」 | 会：查询一律用当前 schema 的名字——旧名字在新 schema 里不存在 |
| 「类型提升随便做」 | 分区源列受限；v2 时间戳单位/decimal 缩放有明确禁止项 |
| 「重排列顺序会重写文件」 | 不会；顺序只是 schema 列表属性，读取按 ID |
| 「Iceberg 支持任意嵌套结构重构」 | 禁止清单（§4.4）就是禁止清单，没有逃生门 |

## 与其他章 / 其他书的联系

- field-id 与 `last-column-id`、`schemas[]` 历史在根文件中的位置：[02-元数据三层结构.md](02-元数据三层结构.md) §2.2；按 ID 键控的统计见 §2.5。
- 分区源列与提升的互锁：[03-隐藏分区与分区演化.md](03-隐藏分区与分区演化.md) §3.2/3.6。
- equality delete 的 `equality_ids` 也是字段 ID：[05-行级删除与删除文件.md](05-行级删除与删除文件.md)。
- 姊妹目录：[../Engineering_Lakehouses_with_Open_Table_Formats/07-Schema与分区演化.md](../Engineering_Lakehouses_with_Open_Table_Formats/07-Schema与分区演化.md)（三格式演化能力横评）、[../Use_Iceberg_with_Spark/05-演化与隐藏分区.md](../Use_Iceberg_with_Spark/05-演化与隐藏分区.md)。
- 模式演化的理论面（关系模式迁移）：[../数据库系统概念6/08-关系数据库设计.md](../数据库系统概念6/08-关系数据库设计.md)。

## 思考题

1. `RENAME COLUMN a TO b` 之后，`SELECT a`、Parquet 文件里的列名、manifest 的 `lower_bounds` 键分别是什么状态？
2. 为什么「ID 永不复用」对**已删除列的残留数据**是必需的？（设想复用会发生什么。）
3. 表按 `bucket(8, user_id)` 分区后想把 user_id 从 int 升 long，会发生什么？改怎么办？
4. v3 的 `initial-default` 和「加列 + 回填作业」相比，故障面与一致性各差在哪？
5. 从 Hive 表 `add_files`/`migrate` 进 Iceberg 时，哪个历史遗留问题 Iceberg 也救不了？
