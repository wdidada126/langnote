# 《Atomic Kotlin》课带 04 集合与循环（第 40–49 课）——标准库操作谱系

> 三态标注：✅ 本仓已核实条目 / ⚠️ 课名与课号系凭 leanpub/booksource 官方站体例记忆拟题（带界自拟，逐字题名与部界待销账）/ 🔧 自写示意实验，未实测（本机无 kotlinc，验证前不得声称实测）
> 画像裁定前提：Java/C++ 后端老手。集合"三兄弟"的基本面貌第 02 带已收账（Lists/Sets/Maps 章 ✅），本带聚焦操作集与迭代机制的增量。

## 一、课带地图（第 40–49 课，共 10 课）

| 课 | 拟题（⚠️ 待逐字销账） | 一行要点 |
|---|---|---|
| 40 | Collection Abstractions | 只读/Mutable 双接口谱系与 Java 集合框架的映射 |
| 41 | List Operations | filter/map/distinct/take/drop 等操作族 |
| 42 | Sorting | sorted/sortedBy 与 Comparator 惯用法 |
| 43 | Searching & Testing | any/all/find/count 谓词族 |
| 44 | Set Operations | union/intersect/minus 代数运算（Java 要手写） |
| 45 | Map Operations | entries/mapValues/groupBy 与 `[]` 缺键语义回收 |
| 46 | Destructuring in Loops | `for ((k, v) in map)` 解构迭代 |
| 47 | Loops Revisited | for-each 底层 iterator 约定、withIndex/indices |
| 48 | Ranges & Progressions Deep | CharRange/闭合区间对象化、downTo/step 全家 |
| 49 | Summary | 部练习与收束（⚠️ 归属部界待对齐） |

## 二、画像裁定（Java/C++ 后端视角）

- **已通，略**：List/Set/Map 概念与遍历（C++ STL、Java Collections 皆熟）；只读 vs 可变接口的"const 正确性"直觉（02 带 ✅）；for-each 语法本身。
- **增量 1——操作族即主食（41/43）**：Java 8 Stream 的 filter/map/anyMatch 在 Kotlin 是**集合上的普通函数**、即时求值无管道仪式；代价是无 Stream 的并行开关 `parallelStream()`，要并行得上协程/parallel 库 ⚠️。C++20 ranges 同族但推广多年仍未完全落地，Kotlin 是标准库地基。
- **增量 2——Set 代数（44）**：`a + b`、`a intersect b`、`a - b` 语言级中缀；Java 要 retainAll/removeAll 且先拷贝防副作用，C++ 要 std::set_union 写回 inserter。裁决：并集惯用 `+`（返回新集合），别读成原地改 ⚠️。
- **增量 3——Map 的 `[]` 与可空耦合（45）**：`m[k]` 缺键返回 null 的地雷在 02 带埋线 ✅，本带配合 `getOrDefault`/`?:` 正式拆雷；`groupBy` 返回 `Map<K, List<V>>` 一步顶 Java 十行 computeIfAbsent 循环 ⚠️。
- **增量 4——解构迭代（46）**：`for ((k, v) in map.entries)` 靠 componentN；C++ 结构化绑定 `for (auto& [k, v] : m)` 形似而机制不同（Kotlin 走函数调用，可自定义）⚠️。
- **增量 5——区间对象化（48）**：`0..9` 是一等值可存可传（IntRange），对照 C++23 `views::iota` 仍是范围库对象、Java 无对应；`step/downTo` 生成 Progression ⚠️ 术语待核。

## 三、🔧 微实验设计（未实测）

1. **`ops.kt`**：同一 List 分别用链式 filter+map 与 Java 风格 for 循环实现，断言结果一致；用 `measureTime`?? 简化为观察中间集合分配（即时求值 vs Stream 惰性）。**目的**：无惰性=可读优先的立场。
2. **`setalg.kt`**：`setOf(1,2) + setOf(2,3)` 断言得 `{1,2,3}` 且原集合不变；`mutableSetOf` 上试 `s += other` 原地语义差异。**目的**：`+` 与 `+=` 在可变/只读接收者上的分野 ⚠️。
3. **`mapnull.kt`**：`mapOf("a" to 1)` 上 `m["b"]` 打印 null、`m["b"] ?: -1`、`getOrDefault` 三路对照。**目的**：拆 02 带地雷。
4. **`destructure.kt`**：`for ((i, v) in list.withIndex())` 与 `for (i in list.indices)` 双写法输出对齐。**目的**：索引遍历惯用法选型。
5. **`rangeobj.kt`**：`val r = 1..10; r.step(2)`?? 存区间为值、传给函数、`in` 断言。**目的**：区间是一等对象。

## 四、盘谱互链（磁盘 ls 实测 ✅）

- 对位：[../Learning_TypeScript/02-对象与数组类型构造.md](../Learning_TypeScript/02-对象与数组类型构造.md)——TS 的 `Array<T>` 是**接口+运行期数组**双身份、元组进类型系统；Kotlin 本带无元组级静态宽度，`Pair/Triple` 只是 data class（名义类，见 03 带），形状不匹配即不兼容。
- 函数操作族对位：[../Learning_TypeScript/03-函数签名与this.md](../Learning_TypeScript/03-函数签名与this.md)（filter/map 回调的上下文类型推导）。
- 兄弟带：上一带 [03-Classes-and-Properties.md](03-Classes-and-Properties.md)，下一带 [05-Inheritance-and-Polymorphism.md](05-Inheritance-and-Polymorphism.md)。

## 五、核心概念中英对照

| 中文 | 英文 | 一句定义 |
|---|---|---|
| 操作族 | collection operations | 标准库在集合上的函数式动词集 |
| 谓词测试 | predicate (any/all/find) | 接收 Boolean 返回函数的高阶操作 |
| 集合代数 | set operations | union/intersect/minus 的运算 |
| 解构迭代 | destructuring in for | 元素按 componentN 拆入多变量 |
| 带索引遍历 | withIndex / indices | 索引惯用两通道 |
| 区间对象 | range (IntRange) | `..` 产出的一等闭区间值 |
| 级数 | progression ⚠️ | 带步长降序的迭代序列 |
| 分组 | groupBy | 按谓词键聚成 Map<K, List<V>> |
| 即时求值 | eager evaluation | 无 Stream 管道惰性，调用即产出 ⚠️ |
| 缺键语义 | get returning null | `m[k]` 在可空类型下的返回 |

## 六、⚠️ 欠账

- 40–49 逐字题名、是否真有"Collection Abstractions"专章未销；官方 List/Set/Map 章散布在Ⅱ部（16–29 ✅），本带与Ⅱ部重叠边界要重排。
- Progression 术语与 `step` 语法逐字未核。
- sequence（Sequence<T> 惰性版）是否入本书正文未定——若无专章，本带实验 1 的对照表述要改。
