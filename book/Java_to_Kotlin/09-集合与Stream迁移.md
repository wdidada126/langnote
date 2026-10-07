# 09 · 集合与Stream迁移（第 13–15 章区间的 Collectors/互操作桥细分续篇，⚠️ 自拟映射）

> 三态标注：✅ = 目次级事实（第 13 章 从流到可迭代对象再到序列、第 14 章 从可累积对象到转换对象、第 15 章 从封装集合到类型别名 ✅ 均已由 [05 档](05-集合迁移.md) 立档）；⚠️ = **本档不主张新章——它是 05 档之外的自拟细分：`Collectors` 组合子桥接与 Stream 互操作边界，原书章/小节归属留欠账**；🔧 = 未实测（本机无 kotlinc/JDK，示例自写）。书目：*Java to Kotlin: A Refactoring Guidebook*，McGregor & Pryce，O'Reilly 2023；中文版机工 ISBN 978-7-111-73703-2 ✅。

## 覆盖章目（续篇定位）：挂靠第 13–15 章区间 ⚠️ 小节归属未核——05 档管 eager/lazy 定形与三段辨析；本档管**组合子逐个对译**与跨界"只换一次"纪律

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
val countByCity: Map<String, Int> =                   // 注意 eachCount 给 Int，非 Long！
    orders.filter { it.status == PAID }
        .groupingBy { it.customer.city }.eachCount()
val byId: Map<Long, Order> = orders.associateBy { it.id }   // 重复键：后者静默覆盖！
val csv: String = orders.joinToString(", ") { it.reference }
```

中间态/终态骨架见 05 档第 13 章三段（`asSequence` 平移→按规模定形）；本档补的终态纪律是**跨界只换一次**：数据进 Kotlin 侧即 `toList()` 落地，出 Kotlin 侧才 `.stream()` 交差，管道中段不让 Stream 与 Sequence/集合混剪。

**重构步序**（⚠️ 归纳）：① 先换**终止操作**（`collect(...)`→`toX/fold/groupBy` 家族）——行为差异全在这一刀；② 再换中间操作（去 lambda 显式类型）；③ 删 `.stream()` 头部并核对接收者类型（只读/Mutable，05 档分层）；④ `parallel()` 先摘除再测（05 档实验 2 回退纪律）；⑤ 与 Java API 交接固化一次转换（入 `toList()`，出 `stream()`）。

迁移对照表（⚠️ 归纳，逐条可测）：

| Java Collector / Stream | Kotlin 对位 | 语义警示 |
|---|---|---|
| `toMap(k,v)` | `associate/associateBy` | **重复键：抛 vs 后者静默覆盖** |
| `groupingBy(cls)` | `groupBy { }` | 返回 MutableMap，值为可变列表 |
| `groupingBy(cls, counting())` | `groupingBy{...}.eachCount()` | **Int vs Long 类型漂移** |
| `groupingBy(cls, reducing())` | `groupBy{}.mapValues{fold}` / `groupingBy{}.fold()` | 单趟版用后者 |
| `toList/toUnmodifiableList` | `toList()` | 只读接口≠锁——协变强转可回改（Effective_Kotlin 03 档"假只读"） |
| `joining/summingInt/maxBy` | `joinToString/sumOf/maxByOrNull` | 空集：Optional vs null |
| `partitioningBy/flatMapping` | `partition/flatMap` | Pair<List,List> 结构 |
| `Stream.iterate/generate` | `generateSequence` / `sequence{}` | 无限流对位无限 Sequence（05 档实验 5） |

## 老手易错点与批判读法（画像：Java/C++ 经验者）

- **重复键策略漂移是静默数据事故**：`toMap` 抛错、`associateBy` 后者胜——迁移含唯一键假设的管道，先 🔧 实验 1 对拍，再决定 `groupBy + single()` 补校验与否。
- **计数/求和类型漂移**：`counting→Long` 对 `eachCount→Int`、`sumOf` 靠重载推断返回型——大数聚合跌回 Int 是隐形溢出位。
- **BaseStream 不是 Iterable**：`stream().asSequence()` 直觉写法不成立；走 iterator 视图还是 `toList()` 落地 ⚠️ 措辞未验，务实配方由 🔧 实验 3 固化。
- **primitive 特化流的装箱账**：IntStream/LongStream 的 `mapToInt` 族在 Kotlin 无对位，`sumOf` 路径装箱需实测（🔧 实验 2）——C++ 人对"零成本抽象"的期待在此打折。
- **批判一句**：组合子对译看着机械，真决策只有一处（05 档已言）：**这条管道需要 lazy 吗**——其余是语法搬运，别为"全 Kotlin 化"重设计本已合理的并行管线。

## 🔧 微实验设计（未执行，方案自写）

1. **重复键对拍**：同一含重复键输入分别过 `Collectors.toMap` 与 `associateBy`，记录异常/覆盖差异。
2. **跨界衔接四象限**：Java 方法入 `List`/出 `Stream`，Kotlin 侧进出各试 `stream()/toList()/iterator().asSequence()`，产出"进出转换配方卡"；另测 `mapToInt().sum()` vs `sumOf{}` 的 10^6 元素分配计数（探针方法同 05 档实验 1）。
3. **单趟 vs 两趟**：`groupBy+mapValues` vs `groupingBy{}.fold()` 中间集合计数差；`filter+filterNot` 双扫 vs `partition` 单扫断言同划分。

## 核心概念中英对照

| 中文 | 英文 | 一句话 |
|---|---|---|
| 收集器 | collector (`Collectors`) | Stream 终止操作的状态化归并协议 |
| 终止/中间操作 | terminal / intermediate operation | 产出结果 vs 惰性搭管道 |
| 重复键策略 | duplicate key policy | 抛错（toMap）vs 后值覆盖（associate） |
| 特化流 | specialized stream (IntStream) | 基本类型免装箱的流形态 |
| 分割/分组 | partition / groupBy | 二路划分 vs 按键聚簇（Kotlin 版返回可变视图） |
| 落地 | materialize (`toList`) | 跨界把惰性流固化为集合 |

## 盘谱互链

- 本系主链：[05-集合迁移.md](05-集合迁移.md)（第 13/14/15 章三段核心，先读本档才成立）、[08-从命令式到函数式风格.md](08-从命令式到函数式风格.md)（循环形状六分）。
- 兄弟：[../Effective_Kotlin/03-集合与解构.md](../Effective_Kotlin/03-集合与解构.md) ✅ 在架（假只读/协变逃逸条目）；[../Kotlin_in_Action_2e/02-函数与Lambda.md](../Kotlin_in_Action_2e/02-函数与Lambda.md) ✅ 在架（lambda 即组合子替身）；TS 侧无对位，落 [00 档](00-总览与阅读地图.md)。

## ⚠️ 欠账

- Collectors 题材在原书的章/小节归属（是否确在第 13 章内）。
- `eachCount` 返回型、`associateBy` 覆盖语义、`Iterator.asSequence` 可用性——⚠️ 语言事实待验、🔧 未实测；组合子对译表本体为自写，非原书还原。
