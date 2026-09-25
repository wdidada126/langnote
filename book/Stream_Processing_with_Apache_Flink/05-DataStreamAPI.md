# 05 DataStream API（原书第 5 章，对齐 Flink 1.7）

> 对应原版第 5 章（中文版「DataStream API（1.7 版本）」）。小节范围按已核实中文目录：
> Hello Flink、设置执行环境、读取输入流、应用转换、输出结果、执行、转换操作（基本转换 /
> 基于 KeyedStream 的转换 / 多流转换 / 分发转换 / 设置并行度）、类型（支持的数据类型 / 类型信息）、
> 定义键值与引用字段（字段位置 / 字段表达式 / 键值选择器）、实现函数（函数类 / Lambda / 富函数）、导入依赖。
> 正文逐字内容未获取，下文按该范围重写（见 [00 总览](00-总览与阅读地图.md) 核实说明）。

## 核心概念速览（中英对照）

- **数据流** — DataStream：无界或有界事件的逻辑序列，是所有转换的输入与输出类型。
- **键控流** — KeyedStream：`keyBy` 之后的流；只有它能声明键控状态、注册计时器（06/07 章）。
- **转换** — transformation / operator：`map`/`filter`/`flatMap` 等一进一出或多出的算子声明。
- **动作** — action：会触发计算的算子（`print`/`addSink`/`addSource` 的汇侧），与「转换」相对。
- **执行环境** — StreamExecutionEnvironment：声明并行度、检查点、时间特性与执行模式的入口对象。
- **类型信息** — TypeInformation / Types：Flink 用来选序列化器、分区器与状态布局的运行时类型描述。
- **字段位置 / 字段表达式** — field position / field expression：`keyBy(0)`（下标，只对元组有效、重构即错位）与
  `keyBy("user.id")`（按名/嵌套路径，Java POJO 可用）。
- **键选择器** — KeySelector：从任意类型提取键的函数（`e => e.userId`），返回类型必须可比较与可哈希；
  键同时决定记录落到哪个子任务与状态归属（02 章）。
- **函数类** — function interface：`MapFunction`/`FilterFunction`/`FlatMapFunction`/`ProcessFunction`…
- **富函数** — RichFunction：带 `open(Configuration)`/`close()` 与 `RuntimeContext` 的函数，状态与广播只在富函数里可用。
- **运行时上下文** — RuntimeContext：在 `open()` 里取状态、参数、并行信息、指标组（07 章）。
- **分发转换** — physical partitioning：`rebalance`/`rescale`/`broadcast`/`global`/`shuffle`/`forward`/`partitionCustom`。
- **多流转换** — multi-stream：`connect`（异构、共享逻辑）、`union`（同构、只合并）、`join`/`intervalJoin`（时间相关，06 章）。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 5.1 | 环境、源、转换、汇、执行五步 | 一切程序都是这五步的排列 |
| 5.2 | 读取输入流 | `fromElements`/`socketTextStream` 用于演示；生产走 `addSource`（08 章） |
| 5.3 | 基本转换 | map/flatMap/filter 无状态；mapPartition 批量、可省序列化 |
| 5.4 | KeyedStream 转换 | keyBy 后才能 `process`/`aggregate`/窗口；键的写法三种 |
| 5.5 | 多流转换 | union 同构合并；connect 异构配对；CoProcessFunction 是唯一能带状态的双流入口 |
| 5.6 | 分发转换 | 选分区 = 选倾斜风险与网络代价；rebalance 治上游倾斜，broadcast 喂规则 |
| 5.7 | 并行度三层 | `env` 默认 → 算子覆盖 → `maxParallelism` 定 key group 数量（07 章） |
| 5.8 | 类型与类型信息 | Scala 自动推导，Java 要 `returns()`/`TypeInformation`；POJO 规则严格 |
| 5.9 | 函数实现三形态 | 接口实现 / Lambda / Rich 函数；要状态或初始化就必须 Rich |

## 核心精讲

### 5.1 五步骨架 🔧

```scala
// 🔧 Scala（Flink 1.7 API 风格，教学示意）
val env = StreamExecutionEnvironment.getExecutionEnvironment
env.setStreamTimeCharacteristic(TimeCharacteristic.EventTime)   // 1.12 起废弃 ⚠️
env.enableCheckpointing(60000)

val src: DataStream[String]  = env.readTextFile("hdfs:///in")   // 或 addSource(kafkaSource)
val words: DataStream[(String, Int)] = src
  .flatMap(_.toLowerCase.split("\\W+").map((_, 1)))
  .returns(Types.TUPLE(Types.STRING, Types.INT))                // Scala 闭包推导失败时的显式类型

words.keyBy(_._1).sum(1).print()
env.execute("wc")
```

Java 侧对照（注意三个差异）：

```java
// 🔧 Java：泛型擦除 → 必须给 TypeInformation；键用字符串或 KeySelector
DataStream<Tuple2<String, Integer>> words = src
    .flatMap((String in, Collector<Tuple2<String, Integer>> out) -> { ... })
    .returns(Types.TUPLE(Types.STRING, Types.INT))
    .name("split-words").uid("split-words-v1");                 // uid 是状态身份（07 章）

words.keyBy(0).sum(1).print();
```

### 5.2 源与汇：本章只到「能跑」，端到端在第 8 章

| 类别 | 1.7 常用 API | 说明 |
| --- | --- | --- |
| 集合/元素、套接字 | `fromElements`、`fromCollection`、`socketTextStream(host, port)` | 测试与演示（`nc -lk 9000` 喂数据）；集合源并行度为 1 ⚠️ |
| 文件 | `readTextFile`、`writeAsText` | 批式；流式文件汇要 `StreamingFileSink`（08 章） |
| 自定义 | `addSource(SourceFunction)` | Kafka/HTTP/CDC 全在这一层（08 章细讲） |
| 自定义汇 | `addSink(SinkFunction)`、`print` | 幂等/事务性决定端到端语义（08 章） |

### 5.3 基本转换的选型

- `map` / `filter` / `flatMap`：一进一出 / 过滤 / 一进多出。无状态，可任意链化（03 章）。
  `mapPartition` 对整个分区调用一次，适合攒批写外部系统 ⚠️（原书是否列入未核实；属 DataStream 标准算子）。
- 不要做的事：在 `map` 里 new 客户端连接、读配置文件 —— 每条记录一次，性能崩塌；
  改用 `RichMapFunction.open()` 建连接（5.8）。

### 5.4 keyBy 的三种写法与陷阱

```scala
// 🔧 三种键写法（Scala）
ks1 = stream.keyBy(_._1)                    // KeySelector：最灵活，类型安全
ks2 = stream.keyBy(0)                       // 字段位置：只对 Tuple 有效，重构即错
// stream.keyBy("user.id")                  // 字段表达式：Java/POJO 场景（Scala case class 亦可按名）
```

| 写法 | 优点 | 陷阱 |
| --- | --- | --- |
| `KeySelector` | 编译期检查、可组合多字段 | 返回类型若为可变对象（自定义类未实现 hashCode/equals）→ 状态分区错乱 |
| 字段位置 | 最短 | 元组字段顺序变化静默错位；改 schema 时不会报错 |
| 字段表达式 | POJO 可读 | 字段必须 public 或有标准 getter/setter（POJO 规则），否则退化成 GenericTypeInfo 且性能差 |

**键的选择直接决定倾斜**：`keyBy(eventId)` 让每个键几乎只有一个事件（状态碎片爆炸 + 无复用），`keyBy(userId)` 是常规，`keyBy("country")` 可能一个键吃下半边倾斜；热键要加盐（键 + 随机后缀，02/10 章）。

### 5.5 多流：union / connect / CoProcess

```scala
// 🔧 union：同类型，纯合并，不做关联，也不洗牌
val all = clicks.union(purchases)

// 🔧 connect：异构双流，共享一个函数；要按业务键配对就必须两边各自 keyBy 同键
val connected = clicks.keyBy(_.uid).connect(purchases.keyBy(_.uid))
  .process(new CoProcessFunction[Click, Purchase, Alert] {
    override def processElement1(c: Click, ctx: Context, out: Collector[Alert]): Unit = {
      // 把点击存进键控状态，并尝试与已到达的下单配对
      ctx.timerService().registerEventTimeTimer(c.ts + 30 * 60 * 1000L)   // 30 分钟未下单则超时
    }
    override def processElement2(p: Purchase, ctx: Context, out: Collector[Alert]): Unit = { /* 反向配对 */ }
    override def onTimer(t: Long, ctx: OnTimerContext, out: Collector[Alert]): Unit = { /* 发出告警 */ }
  })
```

- `union` 不洗牌（保持上游分区）；`connect` 之后若要按业务键配对，**两条流必须各自 `keyBy` 同一键**。
  `join`（窗口连接）与 `intervalJoin`（时间区间连接）在 06 章讲——它们都需要事件时间。

### 5.6 分发转换与并行度

```scala
// 🔧 治理倾斜与喂广播
hot.keyBy(_.id).aggregate(...).setParallelism(8)          // 算子级并行度（受 maxParallelism 约束）
rules.broadcast()                                        // 把规则流复制给下游每个子任务
data.rebalance()                                         // 轮询洗牌，消除上游空闲并行度
localData.rescale()                                      // 只在本地 TM 内轮询，省网络
```

并行度三层优先级：`env.setParallelism` 定默认 → 算子 `setParallelism` 覆盖 →
`maxParallelism`（= key group 数）确定后**不可随意改**，否则键控状态无法恢复（07 章）。

### 5.7 类型体系：为什么 Java 老报错

Flink 需要三件事：序列化器（快）、分区器（键 hash）、可比类型（键/排序）。

| 类型 | 支持度 | 备注 |
| --- | --- | --- |
| 基本类型、`String`、`SqlDate` 等 | 一等 | 专用序列化器 |
| `Tuple1..25`、case class | 一等 | Scala/Java 都友好，字段位置可用；case class 可作 POJO |
| POJO | 一等 | 条件严格：public 类 + public 无参构造 + 每个字段 public 或标准 getter/setter |
| `Row` | 一等 | 与 Table API 互转的桥梁（13 补编） |
| 其他（Guava/自定义/第三方类） | `GenericTypeInfo` | 走 Kryo，慢且不可用字段表达式；建议显式给 `TypeInformation` |

### 5.8 函数三形态

```java
// 🔧 形态一：匿名 Lambda（简洁，但不能拿状态/上下文）
stream.filter(v -> v > 100);
// 🔧 形态二：实现接口的静态类（可命名、可测试）
public class IsPositive implements FilterFunction<Integer> {
  public boolean filter(Integer v) { return v > 0; }
}
// 🔧 形态三：Rich 函数（有 open/close/RuntimeContext → 状态、参数、指标、连接池）
public class ToUpper extends RichMapFunction<String, String> {
  private transient Properties cfg;
  @Override public void open(Configuration p) { cfg = /* ParameterTool.fromMap(getRuntimeContext().getGlobalJobParameters()) */ null; } // ⚠️ 取作业参数
  @Override public String map(String v) { return v.toUpperCase(); }
  @Override public void close() { /* 释放连接 */ }
}
```

要点：Lambda 无法访问 `RuntimeContext` → 想声明状态、注册计时器、读作业参数，一律 Rich 函数或
`ProcessFunction`（它本身是 Rich 的）。

## 版本与兼容性

- 本章 API 名与类名为 **Flink 1.7**：`env.setStreamTimeCharacteristic`（1.12 废弃）、
  `writeAsText`（后废弃，改 `FileSink`/`Sink` API）、`SourceFunction`/`SinkFunction`（FLIP-27 取代）、
  `DataSet` 相关批 API（2.0 移除）；`env.addSource(...)` 的现代写法是 `env.fromSource(source, WatermarkStrategy, "kafka")`
  ⚠️ 具体版本节点以官方迁移指南为准。
- Scala API：Flink 2.x 计划移除/已移除独立 Scala DataStream 层 ⚠️（未逐条核实）；
  字段位置 `keyBy(0)` 在新版仍合法，但官方更推荐 `KeySelector`，`name()`/`uid()` 建议长期保留。

## 常见误区

| 误区 | 事实 |
| --- | --- |
| 「Java 报 types 错误是 Flink 的锅」 | 泛型擦除后 Flink 推不出类型，需 `returns()` 或 `TypeInformation.of(...)` |
| 用 `keyBy(0)` 后改字段顺序 | 不报错，静默错键；跨版本重构请用 KeySelector 或字段表达式 |
| 「`map` 里 new KafkaProducer 没关系」 | 每条记录一个 producer：连接泄漏 + GC 灾难；必须放 `open()`（5.8） |
| 「broadcast 和 keyBy 是一回事」 | broadcast 是「复制给所有子任务」，keyBy 是「按 hash 分给一个子任务」 |
| 「POJO 只要有 getter」 | 还需 public 无参构造、非 final 字段或标准 setter；不满足则退化 Kryo，性能与字段表达式都丢 |

## 与其他章 / 其他书的联系

- `env` 配置项在集群侧的对应 → [09-集群部署与配置.md](09-集群部署与配置.md)；
  `KeyedStream` 才能用的状态 API → [07-有状态函数与状态管理.md](07-有状态函数与状态管理.md)。
- `CoProcessFunction` 与计时器、窗口/间隔连接 → [06-时间与窗口算子.md](06-时间与窗口算子.md)；
  生产级源/汇（Kafka、文件、自定义、异步 IO）→ [08-读写外部系统.md](08-读写外部系统.md)；
  `Row`/类型体系与表层的 schema 映射 → [13-补编-TableAPI与SQL分层.md](13-补编-TableAPI与SQL分层.md)。
- 仓库互链：元组与函数式风格 → [../bigdata/06-Scala函数式与集合编程.md](../bigdata/06-Scala函数式与集合编程.md)；
  与 Spark DataFrame 转换概念的对照 → [../bigdata/02-Spark核心与RDD模型.md](../bigdata/02-Spark核心与RDD模型.md)。
