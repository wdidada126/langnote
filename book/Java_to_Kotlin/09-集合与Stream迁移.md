# 09 · 集合与Stream迁移（第 13–15 章区间的 Collectors/互操作桥细分续篇，⚠️ 自拟映射）

> 三态标注：✅ = 目次级事实（第 13 章 从流到可迭代对象再到序列、第 14 章 从可累积对象到转换对象、第 15 章 从封装集合到类型别名 ✅ 均已由 [05 档](05-集合迁移.md) 立档）；⚠️ = **本档不主张新章——它是 05 档之外的自拟细分：Java `Collectors` 组合子桥接与 Stream 互操作边界，原书中这些内容的章/小节归属留欠账**；🔧 = 未实测代码（本机无 kotlinc/JDK，示例自写非原书代码）。
> 书目：*Java to Kotlin: A Refactoring Guidebook*，McGregor & Pryce，O'Reilly 2023；中文版机工 ISBN 978-7-111-73703-2 ✅。

## 覆盖章目（⚠️ 续篇定位）

| 本档主题 | 挂靠原书位置 | 与 05 档分工 |
|---|---|---|
| Collectors 组合子 → Kotlin 集合操作 | 第 13–15 章区间 ⚠️ 小节归属未核 | 05 档管 eager/lazy 定形与三步辨析；本档管**组合子逐个对译**与跨界边界 |
| Java Stream ↔ Kotlin 集合进出转换 | 互操作层（00 档"起步"段） | 05 档未展开 BaseStream 非 Iterable 的衔接细节 |

## 机制：Java 原形 → Kotlin 翻法 → 重构步序

**Java 原形（Collectors 组合）** 🔧：

```java
Map<String, Long> countByCity = orders.stream()
    .filter(o -> o.getStatus() == PAID)
    .collect(Collectors.groupingBy(o -> o.getCustomer().getCity(), Collectors.counting()));
Map<Long, Order> byId = orders.stream()
    .collect(Collectors.toMap(Order::getId, o -> o));        // 重复键：抛 IllegalStateException
String csv = orders.stream().map(Order::getReference)
    .collect(Collectors.joining(", "));
```

**Kotlin 翻法（逐组合子直译）** 🔧：

```kotlin
val countByCity: Map<String, Int> =                     // 注意：eachCount 是 Int，非 Long！
    orders.filter { it.status == PAID }
        .groupingBy { it.customer.city }.eachCount()
val byId: Map<Long, Order> = orders.associateBy { it.id }   // 重复键：后者静默覆盖！
val csv: String = orders.joinToString(", ") { it.reference }
```

**中间态与终态**：05 档第 13 章三段已立（`asSequence` 平移→按规模定形）；本档的"终态纪律"是**跨界只换一次**：数据进 Kotlin 侧即 `toList()` 落地，出 Kotlin 侧才 `.stream()` 交差，管道中段绝不让 Stream 与 Sequence/集合混剪。

**重构步序**（⚠️ 归纳）：① 先换**终止操作**（`collect(...)` → `toX/fold/groupBy` 家族）——行为差异全部暴露在这一刀；② 再换中间操作（`map/filter` 去 lambda 显式类型）；③ 删 `.stream()` 头部，核对接收者类型（只读/Mutable，05 档接口分层）；④ `parallel()` 先摘除再测（05 档实验 2 的回退纪律）；⑤ 与 Java API 交接处固化一次转换（入：`toList()`；出：`stream()`）。

迁移对照表（⚠️ 归纳，逐条可测）：

| Java Collector / Stream | Kotlin 对位 | 语义警示 |
|---|---|---|
| `Collectors.toList/toSet` | `toList()/toSet()` | 返回只读接口视图 |
| `toUnmodifiableList` | `toList()` | Kotlin 默认不可 `add`，但协变可强转回改（Effective_Kotlin 03 档"假只读"） |
| `toMap(k,v)` | `associate { k(it) to v(it) }` / `associateBy` | **重复键：抛 vs 静默覆盖** |
| `groupingBy(cls)` | `groupBy { cls }` | 值为 Mutable 列表的 MutableMap |
| `groupingBy(cls, counting())` | `groupingBy{...}.eachCount()` | **Int vs Long 漂移** |
| `groupingBy(cls, reducing())` | `groupBy{}.mapValues{ it.value.fold(...) }` 或 `groupingBy{}.fold()` | 单趟版用后者 |
| `joining(d)` | `joinToString(d)` | — |
| `summingInt/Long` | `sumOf { ... }` | `sumOf` 选重载定返回型 |
| `mapping(f, down)` | `groupBy{}.mapValues{ ... }` | 嵌套组合子拆两行 |
| `flatMapping` | `flatMap` | — |
| `partitioningBy(p)` | `partition { p }` | Pair<List, List> |
| `maxBy/minBy` | `maxByOrNull/minByOrNull` | 空集：Optional vs null |
| `IntStream.range` | `(a until b)` / `step` | 基本类型流特化无对位，见易错点 |
| `Stream.iterate/generate` | `generateSequence` / `sequence{}` | 无限流对位无限 Sequence（05 档实验 5） |

## 老手易错点与批判读法（画像：Java/C++ 经验者）

- **重复键策略漂移是静默数据事故**：`toMap` 抛错、`associateBy` 后者胜——迁移含唯一键假设的管道时，先用 🔧 实验 1 对拍，再决定要不要 `groupBy + single()` 补校验。
- **计数/求和的类型漂移**：`counting→Int`、`sumOf` 重载推断——大数聚合从 Long 跌回 Int 是隐形溢出位。
- **BaseStream 不是 Iterable**：`stream().asSequence()` 直觉写法不成立——Kotlin `Iterator<T>.asSequence()` 走的是 Spliterator 的 iterator 视图 ⚠️ 措辞未验；务实解是 `.toList()` 落地或 Java 侧收口（🔧 实验 3）。
- **primitive 特化流的装箱账**：IntStream/LongStream 的 `mapToInt` 一族在 Kotlin 无对位；`sumOf { it.longValue }` 路径的装箱行为需实测（🔧 实验 2），C++ 人对"零成本抽象"的期待在此要打折。
- **`peek` 无对位**：调试用 `peek` 迁移成 `onEach`，但 List 链的 `onEach` 即时执行、Sequence 链的延迟到消费——副作用时机跟着求值策略走（05 档辨析表）。
- **批判一句**：组合子对译表看着机械，真正的决策只有一处（05 档已言）：**这条管道需要 lazy 吗**——其余都是语法搬运，别为"全 Kotlin 化"重设计本来好好的并行管线。

## 🔧 微实验设计（未执行，方案自写）

1. **重复键对拍**：同一含重复键输入分别过 `Collectors.toMap` 与 `associateBy`，记录异常/覆盖行为差异。
2. **装箱显微**：`mapToInt(...).sum()` vs `sumOf {}` 在 10^6 元素下的分配计数（方法同 05 档实验 1 探针）。
3. **跨界衔接四象限**：Java 方法入参收 `List`/出参给 `Stream`，Kotlin 侧进出各测 `stream()/toList()/iterator().asSequence()` 编译与运行表现，固化"进出转换配方卡"。
4. **groupingBy.fold 单趟**：`groupBy+mapValues` 两趟 vs `groupingBy{}.fold()` 单趟，中间集合计数差。
5. **partition 等价**：`filter+filterNot` 双扫 vs `partition` 单扫断言同划分。

## 核心概念中英对照

| 中文 | 英文 | 一句话 |
|---|---|---|
| 收集器 | collector (`Collectors`) | Stream 终止操作的状态化归并协议 |
| 终止/中间操作 | terminal / intermediate operation | 产出结果 vs 惰性搭管道 |
| 重复键策略 | duplicate key policy | 抛错（toMap）vs 后值覆盖（associate） |
| 特化流 | specialized stream (IntStream) | 基本类型免装箱的流形态 |
| 分割 | `partition` | 按谓词二路划分（partitioningBy 对位） |
| 分组 | `groupBy` / `groupingBy` | 按键聚簇；Kotlin 版返回可变异视图 |
| 折叠 | fold / reduce | 自定义组合子（reducing）的统一替身 |
| 落地 | materialize (`toList`) | 跨界把惰性流固化为集合 |

## 盘谱互链

- 本系主链：[05-集合迁移.md](05-集合迁移.md)（第 13/14/15 章三段核心，先读）、[08-从命令式到函数式风格.md](08-从命令式到函数式风格.md)（循环形状）。
- 兄弟：[../Effective_Kotlin/03-集合与解构.md](../Effective_Kotlin/03-集合与解构.md) ✅ 在架（假只读/协变逃逸条目）；[../Kotlin_in_Action_2e/02-函数与Lambda.md](../Kotlin_in_Action_2e/02-函数与Lambda.md) ✅ 在架（lambda 即组合子替身）。
- TS 侧无直接对应，落 [00 档](00-总览与阅读地图.md)。

## ⚠️ 欠账

- Collectors 题材在原书的章/小节归属（是否确在第 13 章内）。
- `eachCount` 返回类型、`associateBy` 覆盖语义、`Iterator.asSequence` 可用性全部 ⚠️ 语言事实待验、🔧 未实测。
- 原书是否给出组合子对译表本体——本档表为自写。
