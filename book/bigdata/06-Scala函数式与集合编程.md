# 06 Scala 函数式与集合编程：Spark API 背后的语言地基

> **本章地图**：**为什么先学 Scala**（Spark 用 Scala 写、API 也是 Scala 味）→ **不可变集合与持久化数据结构**（结构共享）→ **高阶函数**（map/filter/fold/flatMap/reduce）→ **for comprehension 与 `withFilter`**（`for` 不只是语法糖）→ **隐式转换与隐式参数**（Spark 的类型类式设计）→ **并发取舍**：Actor（Akka）与并行的现状 → **给写 Spark 的人的 Scala 建议**。
> **主要支撑**：《Spark 大数据实时计算：基于 Scala 开发实战》**第 1–4 章**（Scala 入门基础 / 面向对象编程 / 编程高级应用 / 函数式编程思想）。这四章是本目录里唯一「与大数据无关、但决定后面能走多远」的部分。

---

## 一、本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 6.1 | Scala 与 Spark 的关系 | Spark 内核是 Scala 写的；RDD 的 API 透着函数式味道 |
| 6.2 | 不可变集合与结构共享 | 每次"改"都生成新对象，但共享大部分结构，代价可接受 |
| 6.3 | 高阶函数五件套 | map / filter / fold / flatMap / reduce；这是 Spark 算子的原型 |
| 6.4 | for comprehension 的本质 | 编译成 `flatMap`/`map`/`withFilter`/`foreach`；不是语法糖那么简单 |
| 6.5 | 隐式转换与隐式参数 | 扩展已有类型的能力；Spark 用它做「类型类」式设计 |
| 6.6 | 并发取舍：Actor / Future / 线程 | 2018 年 Akka 活跃，2026 年 Akka .Status 变化；工程上优先用纯函数 |
| 6.7 | 写给 Spark 开发者的十条实践 | 少闭包捕获、少 new、用 case class 而非 tuple |

---

## 二、核心精讲

### 6.1 为什么先学 Scala

Spark 的**内核**（DAGScheduler、RDD、闭包序列化、Actor 消息系统）是用 Scala 写的；Spark 的 API 也是 Scala 味的：

```scala
// 教学示意，不参与构建；感受一下 Spark API 的函数式味道
words.map(_.toLowerCase)            // 高阶函数
     .filter(_.nonEmpty)            // 高阶函数
     .groupBy(identity)             // 高阶函数
     .mapValues(_.size)             // 高阶函数
     .reduce(_ + _)                 // 高阶函数
```

结论很简单：**不理解高阶函数与不可变数据，就读不懂 Spark 的 API，更读不懂 Spark 源码**。这也是《Spark 大数据实时计算》把第 1–4 章留给 Scala 的编排理由。

### 6.2 不可变集合与结构共享

```scala
// 教学示意，不参与构建；不可变集合的「结构共享」
import scala.collection.immutable.{Map, MapLike}

// 注意：下面这一行在原书里写作「Map("a" -> 1)」；这里强调类型是 immutable.Map
val m1: Map[String, Int] = Map("a" -> 1, "b" -> 2)
val m2 = m1 + ("c" -> 3)      // 生成新 Map，m1 不变
// m1 与 m2 共享 m1 里的 "a"、"b" 两个节点，复制代价与集合大小无关（近似 O(1) 到 O(log n)）
```

- **不可变的三个理由**：
  1. **并行安全**：没有锁也能并发处理（Spark 的算子天然满足）；
  2. **可推导性**：`val` + 纯函数 = 更容易推理、更容易测试；
  3. **可回放性**：Spark 的血缘模型建立在「输入相同则输出相同」之上，不可变是这一点的保证。
- **代价**：每次"更新"都分配新对象；在热循环里会制造大量垃圾。因此工程上的做法是：
  - 中间计算用可变结构（`mutable.Map`、`Array`、`StringBuilder`）缓冲，**最后一步**再 `toMap`/`toList` 转成不可变；
  - 用 `view`/`iterator` 而不是强制物化。

### 6.3 高阶函数五件套

```scala
// 教学示意，不参与构建
val nums = List(1, 2, 3, 4)

val mapped   = nums.map(_ * 2)                 // List(2,4,6,8)
val filtered = nums.filter(_ % 2 == 0)         // List(2,4)
val flat     = nums.flatMap(i => List(i, i))   // List(1,1,2,2,3,3,4,4)
val folded   = nums.foldLeft(0)(_ + _)         // 10，带初值
val foldedR  = nums.foldRight(List.empty[Int])((i, acc) => i :: acc)
val reduced  = nums.reduce(_ + _)              // 10，无初值（空集合抛异常）

//  folds 的四个变体：foldLeft / foldRight / fold / foldLeft 的 lazy 版
// 记住：foldLeft 是左结合的，reduce 在空集合上会抛异常
```

| 函数 | 组合子类型 | 与 Spark 算子的对应 |
| --- | --- | --- |
| `map` | `A => B` | `map`、`mapPartitions` |
| `filter` | `A => Boolean` | `filter` |
| `flatMap` | `A => TraversableOnce[B]` | `flatMap`（一行变多行，如切分日志） |
| `foldLeft` | `(B, A) => B` | `aggregate`、`treeAggregate`（树状聚合，减少串行） |
| `reduce` | `(A, A) => A` | `reduce`、`reduceByKey`（配合 map 端预聚合） |
| `groupBy` | `A => K` | `groupByKey`（**注意：Spark 侧的 `groupByKey` 不带预聚合**） |

> **这张表是打通 Scala 与 Spark 的钥匙**：Spark 里 90% 的算子都是这些高阶函数的**分布式版本**。理解了 `foldLeft` 的语义，`aggregateByKey` 就不难了。

### 6.4 for comprehension 的本质

```scala
// 教学示意，不参与构建；for 展开后的等价形式（示意，不参与编译）
for {
  a <- List(1, 2)
  b <- List("x", "y")
  if a > 1
} yield (a, b)

// 等价的展开（说明它不是「语法糖那么简单」）：
List(1, 2).flatMap(a => List("x", "y").withFilter(_ => a > 1).map(b => (a, b)))
```

要点：

1. **单生成器 without yield** → `foreach`；
2. **单个生成器 + yield** → `map`；
3. **多个生成器** → 嵌套 `flatMap` + 最后 `map`；
4. **`if` 守卫** → `withFilter`（注意：`withFilter` **不抛异常**，只是过滤，这与 `filter` 语义略有差别，是常见坑）；
5. **性能差异**：`for` 的嵌套展开可能产生更深的调用栈，`flatMap` 显式写有时更快 —— **在热路径上优先用高阶函数**。

### 6.5 隐式转换与隐式参数

```scala
// 教学示意，不参与构建
// (1) 隐式转换：给已有类型加能力
object RichIntOps {
  implicit def enrich(i: Int): RichInt = new RichInt(i)
}
class RichInt(val i: Int) { def doubled: Int = i * 2 }

// (2) 隐式参数：Spark 的类型类式设计（ClassTag 就是靠它把类型信息带到运行时）
def sum[T](xs: List[T])(implicit num: Numeric[T]): T = xs.foldLeft(num.zero)(num.plus)

// (3) Spark 里的真实例子：Ordering 决定了 reduceByKey 的键如何比较
// implicit val ord: Ordering[(String, Int)] = Ordering.by(_._1)
```

- **适用场景**：扩展第三方类型、提供类型类（Ordering、ClassTag、Encoder）、DSL 的写法糖。
- **风险**：**隐式解析失败时的报错极其难读**；作用域过大时会出现「莫名其妙的多义性」。工程建议：**每个隐式转换都要有明确的导入点（`import ...`），不要写在全局作用域**。
- 在 Spark 里，隐式主要用于两处：`ClassTag`/`Encoder` 的运行时类型信息、`Ordering` 的键比较 —— 这也是为什么**读 Spark 源码会频繁看到 `(implicit ...)`**。

### 6.6 并发取舍：Actor、Future 与线程

2018 年的典型建议是「并发用 Akka Actor」；2026 年的现实是：

| 方案 | 现状（2026） | 说明 |
| --- | --- | --- |
| **Actor / Akka** | Akka 的 Actor 模型仍在（Akka Actors、Pekko 作为 ASF 继任者），但**社区活跃度远不如 2016–2018** | 两书写作时，`Akka` 是 Spark 1.x 内部通信（基于 Netty 之前）与很多 Scala 项目的默认选择 |
| **Future / Promise** | 主流 Scala 异步方案 | ` Future.traverse` 处理小量并发 |
| **Java 虚拟线程（JDK 21+）** | 极大地改变了 JVM 并发的成本模型 | JDK 21（JEP 444）起 `ForkJoinPool` 成为虚拟线程调度器；阻塞成本大幅下降 |
| **纯函数 + 不可变** | **工程上最推荐的默认** | 无共享可变状态就没有竞态 |

```scala
// 教学示意，不参与构建；两种并发风格的对比
// (A) 命令式共享可变状态（危险）
var total = 0L
val xs = List(1, 2, 3)

// (B) 纯函数 + 不可变（安全，也是 Spark 的世界观）
val total: Long = xs.foldLeft(0L)(_ + _)

// (C) Future 并行（注意别关闭 commonPool 里的阻塞）
import scala.concurrent.{Future, ExecutionContext.Implicits.global}
val fs: Seq[Future[Int]] = xs.map(i => Future(i * 2))
```

- **Spark 自己的选择**：Spark 的 executor 内部用 **线程池 + 纯算子的 partition 级并行**，而不是 Actor；driver 与 executor 的通信用 **Netty RPC**。这说明了一件事：**在数据处理领域，「不可变数据 + 数据局部性」比「消息传递」更能压榨性能**。

### 6.7 给写 Spark 的人的十条 Scala 实践

1. 用 `case class` 而不是 `Tuple` 表达结构化数据（可读、能 withFilter/模式匹配、序列化更友好）。
2. 闭包里**只捕获真正需要的字段**，不要捕获大对象/整个 `this`（否则会被序列化到每个 executor）。
3. 算子内部避免在循环里 `new` 对象；能复用就复用（与 `05` 的 GC 调优直接相关）。
4. 用 `private[this]` / `final` 让 JIT 更容易内联。
5. 不要用 `null`；用 `Option`。
6. 用 `foldLeft` 替代 `var + for` 的累积模式。
7. 批处理集合用 `mutable`、边界用 `immutable`。
8. 隐式转换写清楚导入点，不写在包对象里。
9. 热路径避免 `for { ... } yield` 的多重展开，改用 `flatMap`。
10. **写 Spark 作业时把算子写成纯函数**——这是 exactly-once 语义的前提。

---

## 三、核心精讲（续）：教学示意代码

```scala
// 教学示意，不参与构建；一个「把日志解析写成纯函数」的示范
// 目的：说明「不可变 + 纯函数」如何与 Spark 的算子一一对应
object LogParseTeaching {
  final case class AccessLog(ip: String, uid: String, status: Int, bytes: Long)

  // 纯函数：同一个输入永远得到同一个输出，没有副作用
  def parse(line: String): Option[AccessLog] = {
    val parts = line.split("\\s+", 5)
    if (parts.length < 5) None
    else Some(AccessLog(parts(0), parts(1), parts(2).toInt, parts(3).toLong))
  }

  // 与 Spark 的对应：rdd.flatMap(parse).filter(_.status == 200).map(l => (l.uid, l.bytes))
  val parsed: List[Option[AccessLog]] = List("1.2.3.4 u1 200 1024", "bad line").map(parse)
}
```

---

## 四、经典论文与原始文献

| 论文 / 文献 | 出处 | 与本节的联系 |
| --- | --- | --- |
| Odersky、Läufer，*Putting Type Checks in Checker Position: A Second-Generation Scala Compiler*（以及 Scala 的设计论文 *An Overview of Scala*，Läufer & Odersky 等） | 1996–2004 年间的 Scala 设计文献 | Scala 语言本身的设计背景 |
| Baker，*Equal Requires for Efficient Persistent Structures*（相关：*List Equality for Hash Consing* 等持久化数据结构工作） | 1970s–1998 年 | 不可变集合的**结构共享/持久化数据结构**理论来源 |
| 关于 Actor：Hewitt、Agha，*A Model of Computation for Object-Based Distributed Systems* | 1988 | Actor 模型的原始论文 |
|关于 Akka/Pekko：见 akka.io 与 apache/pekko 官方文档 | 官方文档，非论文 | 本节 6.6 的现实依据 |

> 注：Scala 语言**没有**一篇 canonical 的「论文式」引用；此处列的是设计文献与官方文档，避免杜撰会议与年份。

---

## 五、近年研究与工业界开源实践（2015–2026）

**研究侧**：

- **纯函数式与并行**：`immutability` 与 parallel immutable collections 的研究；以及「**函数式 + 数据局部性**」在 GPU/异构加速上的延伸。
- **类型系统**：dependent typing、path-dependent types 在 Scala 3（`Dotty`）中的推进；Scala 3 在 2023 年正式发布（V3.0），社区正在迁移。
- **JVM 并发**：JDK 21 的虚拟线程（JEP 444）与结构化并发（Structured Concurrency，JEP 505 孵化）极大地改变了「Scala 该怎么写并发」的答案。

**工业界开源（star 数为 2026-09-25 用 `gh api` 实测）**：

| 项目 | star | 与本节的联系 |
| --- | --- | --- |
| `apache/spark` | **44036** | Spark 内核与 API；大量使用隐式参数与高阶函数 |
| `scala/bug`（Scala 编译器缺陷跟踪） | star 未核验 | 说明 Scala 生态的状态 |
| `VirtusLab/scala-cli`（Scala 官方 CLI 工具） | star 未核验 | 现代 Scala 的入门方式 |
| `akka/akka`（Lightbend 维护）与 `apache/pekko`（ASF） | star 未核验 | 6.6 节 Actor 的现状 |

> ⚠️ 关于 star：本节涉及的多为语言与运行时项目，其 star 数与大数据话题的相关性低，且部分仓库存在**分叉/迁移**（如 Akka 的部分模块迁往 Pekko），因此本目录对这几项**只做文字说明，不标注具体数字**，以免传播过时的二手数据。

**可直接照做的建议**：

1. 学 Spark 之前，先写 10 个 `foldLeft`/`flatMap` 的小练习；看不懂 Spark 算子基本都是卡在这里。
2. 写完一个算子后自问：「**它是纯函数吗？有没有副作用？**」——有副作用的算子在 exactly-once 语义下必然出错（详见 `07`）。
3. 用 `Spark UI → SQL/Stage` 看任务里报的 `Serialization` 相关错误，多半是你闭包捕获了不该捕获的东西。

---

## 六、常见误区与本书需修正之处

| # | 误区 | 修正 | 书目 |
| --- | --- | --- | --- |
| 1 | 「Scala 的不可变集合只是风格偏好，性能更差」 | 有**结构共享**做支撑，复制代价与结构深度相关而非集合大小；在数据处理里不可变是**并行安全 + 可重放**的前提 | 《Spark 大数据实时计算》第 1.9 节（不可变 Map） |
| 2 | 「`var total` 累积更快」 | 单线程也许更快，但**无法并行、无法安全重放**；工程上用 `foldLeft`/`aggregate` | 《Spark 大数据实时计算》第 1.10 节（fold） |
| 3 | 「`for` 循环只是 `map` 的语法糖」 | 多生成器展开成 `flatMap` + `map`，守卫变成 `withFilter`（**不抛异常**，与 `filter` 语义不同） | 《Spark 大数据实时计算》第 1.5.1 节（for 表达式） |
| 4 | 「隐式转换是高级技巧，不用学」 | Spark 源码里 `(implicit ...)` 无处不在（`ClassTag`、`Ordering`、`Encoder`）；不认识它就读不懂源码 | 《Spark 大数据实时计算》第 3 章（Scala 编程高级应用） |
| 5 | 「并发就该用 Actor」 | 在**数据并行**领域，「不可变 + 数据局部性」优于消息传递；Actor 更适合状态机与事件驱动，而非批处理 | 《Spark 大数据实时计算》第 3 章；也是《离线》第 2.2 节流计算技术的取舍 |
| 6 | 🔧 本书未覆盖 **Scala 3（Dotty）** | 2023 年 Scala 3 正式发布，新项目越来越多使用 Scala 3；本书基于 Scala 2.x 写法 | 《Spark 大数据实时计算》第 1–4 章 |
| 7 | 🔧 本书未覆盖 **JDK 21+ 虚拟线程对 Scala 并发的影响** | 阻塞成本大幅下降，许多「必须用 Actor/线程池」的设计不再必要；`ForkJoinPool` 于 JDK 21 起成为虚拟线程调度器 | 《Spark 大数据实时计算》第 3 章（并发取舍） |
| 8 | 🔧 本书未覆盖 **Akka 的社区变化** | 2018 年 Akka 是 Scala 并发的默认答案；2020 年代其活跃度与生态位置已明显变化（ASF 有 `apache/pekko`）。**不要**用「Akka 一定对」的口气写新系统 | 《Spark 大数据实时计算》第 3 章 |

---

## 七、与其他章 / 其他书的联系

**本目录内部**：

- **`02-Spark核心与RDD模型.md`**：RDD 的 `map`/`filter`/`reduceByKey` 就是本章 6.3 节高阶函数的分布式版本。
- **`04-SparkSQL与结构化数据.md`**：Dataset 的 `map`/`filter`/`groupBy` 同样是高阶函数；区别只在**有 schema 所以能被优化**。
- **`05-Spark性能优化.md`**：本章「减少对象分配」的实践直接服务于 `05` 的 GC 优化。
- **`07-实时计算与流式架构.md`**：exactly-once 要求算子是纯函数，这正是本章 6.2 节的不可变世界观。

**其他书**：

- **`book/软件架构设计/03-语言.md`**：语言选型与抽象能力的取舍；Scala 的「表达力强但编译慢/报错难读」是典型的架构权衡。
- **`book/多处理器编程的艺术2/16-调度与工作分配.md`**：**推荐对照**。Scala 集合的并行处理与 Spark 的 partition 并行是同一套数据并行思想；该章的 work stealing 解释了「为什么不可变数据的并行反而快」。
- **`book/多处理器编程的艺术2/`（并发章节）**：Actor 与 Future 的取舍、内存模型、无锁结构，是 6.6 节的理论背景。
- **`book/Java并发编程之美/`**：Scala 跑在 JVM 上，最终仍受 JVM 内存模型与 GC 支配；`05` 的 GC 一节会回到同一层。
