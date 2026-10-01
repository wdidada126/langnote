# 06 · Spark SQL 与 Datasets（类型化 API 终章）

> 原书第 6 章（Spark SQL and Datasets）。章骨架 ✅ 按 ApacheCN 全译镜像实抓还原：Java/Scala 单一 API／Case Classes 与 JavaBeans 建 Dataset／使用数据集（造样例、转换）／高阶函数与函数式编程／DataFrame↔Dataset 互转／Dataset 与 DataFrame 的内存管理（Encoders、内部格式 vs Java 对象格式、SerDe、使用数据集的成本、缓解策略）。Spark 行为 = ⚠️ 转述 + 官方文档。本章是 2e 里 Scala 浓度最高、也最"换代"的一章——1e 用 RDD 讲这些，2e 用 Encoder 讲。对位：[TDG 06 SparkSQL 与 Dataset](../Spark_The_Definitive_Guide/06-SparkSQL与Dataset.md)、[第 3 章](03-ApacheSpark结构化API.md)。

## 6.1 单一 API 的理想与语言现实

- Spark 2.0 起 `DataFrame = Dataset[Row]` 别名，SQL/DataFrame/Dataset 收敛为一个栈；但**类型红利只有 Scala/Java 有**：`map`/`flatMap` 带编译期类型检查，DataFrame 侧只有运行时列名错。
- Python 视角本章约等于"不存在"：PySpark 无类型化 Dataset（无编译期类型可谈），第 5 章 Pandas UDF + 后来 3.x 类型注解才是 Python 的"类型感"替代。2e 诚实呈现了这个不对称——这是它区别于 TDG（按语言三主线并写）的结构特征。

## 6.2 建 Dataset：case class / JavaBeans

- Scala：`case class Person(name: String, age: Long)` + `spark.createDataFrame(Seq(...)).as[Person]`——`as[T]` 靠 Encoder 重铸类型；
- Java：`Encoders.bean(JavaBean.class)`（getter/setter 约定即 schema）；
- 隐式 Encoder 解析（`implicit enc = Encoders.product[T]`）：shapeless 派生机制 ⚠️ 转述，工程上记"能推导就不要手写 Encoder"。

## 6.3 转换示例与函数式编程面

- `ds.map(p => p.age+1)`：真·用户代码逐行执行（JVM 对象进出）——**与 DataFrame `select(col("age")+1)`（表达式 + codegen）的路线分岔是本章标题级对比**；
- filter/withColumn 族在 Dataset 上仍走表达式；强类型 map/flatMap/foreach 才是类型化特权；
- 高阶函数回顾（map 组合、`reduce` 风格）：函数式语法在类型化一侧更自然——面向 Scala 读者的安抚节。

## 6.4 内存管理与成本（本章硬核）

⚠️ 转述（官方口径 https://spark.apache.org/docs/latest/tuning.html ✅ curl 200）：

- **内部格式 vs 对象格式**：DataFrame 行驻留内存用 **UnsafeRow**（二进制、按位读、免 GC 压力）；类型化 Dataset 一旦 `map` 就**反序列化成 JVM 对象**（对象头 + 引用开销，GC 接管）；
- **SerDe 成本**：typed 侧每次跨界都有 encode/decode 税——"使用数据集的成本"小节的本体；
- **缓解策略**（书给的清单）：尽量把逻辑留在表达式侧（select/where 下推）、跨界只 map 一次、考虑 `Dataset[UnsafeRow]` 黑魔法（进阶，慎用）、能不类型化就不类型化；
- 与第 3 章呼应：Catalyst 对 typed `map` 是黑盒（同 UDF 困境），codegen 断点在此出现。

🔧 **概念对照（非本书 Spark 引擎行为）**：DuckDB 聚合前后对照（meas.txt G6 组）——`CREATE VIEW`（逻辑留引擎侧）首读现场算 17.8ms vs `CREATE TABLE m AS`（物化）建 391ms 后复读 0.63ms；物化换复读，跨界换灵活，**与 UnsafeRow/对象化同一经济学**：每次"把数据从引擎的表示搬到用户的表示"都付一次编解码。SQLite 侧对照：视图计划里 `CO-ROUTINE v`（不物化）——同理。**这是单机类比，Spark 的对应机制（UnsafeRow/Tungsten）不可本机实测，标 ⚠️ 转述。**

## 6.5 何时选 Dataset（重构判断）

- Scala 团队、域模型稳定、想在编译期挡字段错——Dataset；
- 混合语言团队/以 SQL 为一等公民——DataFrame，类型安全交给 schema 显式声明 + 测试；
- 性能敏感路径：先看表达式侧能否表达，再看 AQE/缓存，最后才考虑 typed map 的开销——本章"缓解策略"给出的正是这个决策序。

## 6.6 与 TDG 第 6 章的分工

TDG 把 Dataset 与 SQL 并在一章按操作讲解；本册把"内存成本"单独拔成半章——**教学侧重从"怎么用"移到"什么时候别用"**。两文件互链共读，盘上以本册决策序 + TDG 操作密度配对。

## 6.7 章小节骨架总览（✅ 镜像实抓逐节对账）

| 原书小节（回译） | 本文件对应 |
| --- | --- |
| Java 和 Scala 的单一 API | 6.1 |
| Scala 的 Case Classes 和 JavaBeans 用于 Datasets | 6.2 |
| 使用数据集（创建示例数据／转换示例数据） | 6.3 |
| 高阶函数和函数式编程 | 6.3 末条 |
| 将 DataFrames 转换为 Datasets | 6.2 `as[T]`、6.3 |
| Datasets 和 DataFrames 的内存管理 | 6.4 |
| Dataset Encoders | 6.2 隐式 Encoder、6.4 |
| Spark 的内部格式与 Java 对象格式对比 | 6.4 首两条 |
| 序列化和反序列化（SerDe） | 6.4 |
| 使用数据集的成本 | 6.4 |
| 缓解成本的策略 | 6.4 末条、6.5 决策序 |

## 6.8 重建示例：case class 往返一次（Scala 语义示意，本目录重做；⚠️ 未执行）

```scala
case class Emp(name: String, dept: String, salary: Long)

val df0: DataFrame = spark.read.parquet("data/emp")          // 无类型
val ds: Dataset[Emp] = df0.as[Emp]                           // ① Encoder 铸型：进类型化
val bonus: Dataset[(String, Long)] =
  ds.map(e => (e.dept, (e.salary * 0.1).toLong))             // ② 对象化：UnsafeRow→JVM 对象
val back: DataFrame = bonus.toDF("dept", "bonus")            // ③ 回表达式域（codegen 恢复）
// 成本审计口诀：①③ 各一次编解码、② 全量对象分配 + GC——"跨界就要钱"（6.4）
```

- 对照实验直觉（🔧 非本书 Spark 引擎行为）：G1 组里"CSV 全扫一遍才知道类型"（DuckDB 推断 BIGINT/DOUBLE）与①的"运行时才定 schema"同型——类型信息永远有获取成本，区别只在付一次还是每行付（meas.txt G1/G6）。

## 6.9 课堂问题（答不出回本文件）

1. `DataFrame = Dataset[Row]` 在运行时有差别吗？在编译期呢？
2. Python 为什么没有类型化 Dataset？其"类型感"替代路线两站（6.1/演进节）？
3. Encoders.product 与 Encoders.bean 分别吃什么约定？
4. UnsafeRow 赢在哪三处（内存/ GC / 下推）？typed map 输在哪一步？
5. "缓解策略"四条的优先序？（尽量表达式侧→跨界一次→能不类型化就不→黑魔法最后）
6. 本章与第 3 章的分工：一个讲"是什么"，一个讲"贵在哪"——各自的标题证据？

## 核心概念速览（中英对照）

- **Dataset[T]** — 类型化分布式集合（Scala/Java 特权）。
- **DataFrame = Dataset[Row]** — 2.0 合并后的别名关系。
- **Encoder[T]** — 类型 T ↔ 内部二进制行的编解码器。
- **Encoders.product/bean** — Scala 产品类型/JavaBean 的推导入口。
- **as[T] 重铸** — DataFrame 升为类型化 Dataset 的把手。
- **UnsafeRow** — Tungsten 二进制行布局：低 GC、可按位下推。
- **对象化成本** — typed map 引发的反序列化 + GC 税。
- **codegen 断点** — 用户闭包打断整段代码生成。
- **函数式转换** — map/flatMap 的类型化组合子。
- **shapeless 派生** — Scala 隐式 Encoder 推导机制（⚠️ 转述）。
- **JavaBean 约定** — Java 侧以 getter/setter 即 schema。
- **决策序** — 表达式→AQE/缓存→typed map 的性能排查次序。

## 最新演进与工业实践

- **Scala 线收缩**：Spark 4.x 对 Scala 2.12/2.13 的支持随版本推进（⚠️ 转述发行说明），新代码社区占比持续下降；3.0 起"支持/弃用语言"公告（第 12 章）是这一章未来老化的主因——R/SparkR 线已实际弱化，类型化 Dataset 变成 Scala 小众特权。
- **Python 的类型感替代**：pandas API on Spark 类型注解 + `applyInPandas`/Pandas UDF 迭代器（4.0 的 Python UDTF/profiling ✅ Release Notes 实抓 https://spark.apache.org/releases/spark-release-4-0-0.html）；"无 Encoder 之痛"由 Arrow 数据帧缓解。
- **Photon/向量化**：Databricks 商业引擎在表达式侧向量化后，"表达式 vs typed map"的差距被进一步拉大——工程结论"能表达式就不闭包"在 2026 更硬（⚠️ 转述）。
- **UnsafeRow 后继**：内部格式演进（如 4.x 行布局讨论）细节 ⚠️ 未逐条核验，仅登记方向。
- **对读**：本章机制的更完整操作对照见 [../Spark_The_Definitive_Guide/06-SparkSQL与Dataset.md](../Spark_The_Definitive_Guide/06-SparkSQL与Dataset.md)；第 3 章催化剂视角回看 [03-ApacheSpark结构化API.md](03-ApacheSpark结构化API.md)。
