# 06 · 从Builder到命名参数与默认值（第 7–12 章区间内的 builder 章位，⚠️ 自拟映射）

> 三态标注：✅ = 目次级事实（23 章全目录已取得，01–05 档已列逐字章名）；⚠️ = **本档章名按 [00 档](00-总览与阅读地图.md) 骨架"Builder→默认参/data class"条目自拟映射，中文版 23 章逐字对应留欠账，勿引为原文**；🔧 = 未实测（本机无 kotlinc/JDK，代码为自写风格示例非原书代码）。书目：*Java to Kotlin: A Refactoring Guidebook*，Duncan McGregor & Nat Pryce，O'Reilly 2023；中文版《Java到Kotlin：代码重构指南》，机械工业，ISBN 978-7-111-73703-2 ✅。

## 覆盖章目：推定位在第 7–12 章区间的 builder 章 ⚠️ 编号未核——00 档"惯用化：Builder→默认参" ✅；第 5 章"构造重载→默认参数"首刀已由 [04 档](04-从Bean到值.md) 覆盖，本档是独立成章的深水区续篇

## 机制：Java 原形 → Kotlin 翻法 → 重构步序

**Java 原形（Effective Java 静态内部 Builder，⚠️ 通行记载）** 🔧：

```java
public class SearchQuery {
    public static class Builder {
        private String term; private int page = 0; private int pageSize = 20;
        public Builder term(String t) { this.term = t; return this; }
        public Builder page(int p) { this.page = p; return this; }
        public Builder pageSize(int n) { this.pageSize = n; return this; }
        public SearchQuery build() {
            if (term == null || term.isBlank()) throw new IllegalStateException("term required");
            return new SearchQuery(this);
        }
    }
}   // 用法：new SearchQuery.Builder().term("kotlin").pageSize(50).build();
```

**中间态（IDE 转换产物）** 🔧：Builder 类原样直译成 Kotlin（`fun term(t: String): Builder`）——能编译能跑，但"半初始化窗口 + 位置耦合调用"两大 Bean 债（04 档）分文未还。

**终态（命名参数 + 默认值 + copy）** 🔧：

```kotlin
data class SearchQuery(
    val term: String,
    val page: Int = 0,
    val pageSize: Int = 20,
) {
    init { require(term.isNotBlank()) { "term required" } }
}
val q = SearchQuery(term = "kotlin", pageSize = 50)   // 具名自文档，布尔/整型不靠位置猜
val paged = q.copy(page = q.page + 1)                  // 改一字段再造，交 copy 接管
```

**重构步序**（每步可编译可测试，⚠️ 归纳）：① 主构造器补默认值，消灭 telescoping 重载；② 调用处补命名实参；③ `build()` 校验迁 `init { require }`；④ builder 复用改值处换 `copy`；⑤ 调用点清零后删嵌套 Builder——Java 调用方仍在则边界挂 `@JvmOverloads` 或薄 Builder 门面（联动 [12 档](12-测试与互操作迁移.md)）。

迁移对照表（⚠️ 归纳，review checklist）：

| Java Builder idiom | Kotlin 对位 |
|---|---|
| `Builder().a(x).b(y).build()` | `Foo(a = x, b = y)` 命名实参 |
| telescoping 构造器重载 | 默认参数 `b: T = d`（调用点求值，天然禁可变默认） |
| `build()` 前置校验 | `init { require(...) }` |
| 复用 builder 逐步改字段 | `copy(字段 = 新值)`（04 档） |
| Lombok `@Singular` 收集 | 只读集合参数 + 边界处 `+`/`toList` |
| SDK/链式 DSL | 带接收者 lambda 的类型安全 builder（合法保留区） |

## 老手易错点与批判读法（画像：Java/C++ 经验者）

- **默认值表达式不得引用其他参数**（`b: Int = a` 非法 ⚠️ 语言事实待验）：Builder 时代"后字段默认取前字段"要改函数默认或构造后 copy。
- **@JvmOverloads 组合爆炸**：十个默认参数生成的重载构造器数量可观（🔧 实验 1 javap 计数）——它是还债工具不是日常配置。
- **命名参数超过四五个是信号**：该抽参数对象（data class，04 档），不是继续加名字。
- **C++ 对照**：named arguments ≈ C++20 designated initializers 完整版；重排参数声明序对命名调用不 breaking（位置调用才破），与 02 档 componentN 顺序敏感恰成两极，判据同为"按名耦合 vs 按位耦合"。
- **别一刀切全删 builder**：分阶段构建、Java 消费方、DSL 三场景仍是正解；工序是"默认值+具名先行，builder 退守边界"（⚠️ 归纳）。

## 🔧 微实验设计（未执行，方案自写）

1. **@JvmOverloads 计数**：3 参与 8 参默认构造器各加注解，`javap` 数 `<init>` 重载数。
2. **变异测试对照**：默认 pageSize 20→30，比较 builder 版与默认参数版各自暴露失败的测试位置（故障半径差）。
3. **Java 侧残量**：Java 写 `SearchQuery("kotlin")`（无 @JvmOverloads）编译失败清单——即 12 档"边界残量"仪表盘。

## 核心概念中英对照

| 中文 | 英文 | 一句话 |
|---|---|---|
| 建造者模式 | builder pattern | 分步赋值后 build() 的构造协议 |
| 伸缩构造器 | telescoping constructors | 逐参重载的构造器阶梯 |
| 命名/默认参数 | named / default arguments | 按名不按位；声明处给缺省 |
| 参数对象 | parameter object | 参数过多的收纳方案（data class） |
| 构造器生成 | `@JvmOverloads` | 为 Java 侧展开默认值重载 |
| 半初始化窗口 | half-initialized window | builder 累积期的非法状态带（04 档同源） |

## 盘谱互链

- 本系：[04-从Bean到值.md](04-从Bean到值.md)（第 5 章首刀）、[02-从Java类到Kotlin类.md](02-从Java类到Kotlin类.md)、[12-测试与互操作迁移.md](12-测试与互操作迁移.md)（残量计数）。
- 兄弟：[../Kotlin_in_Action_2e/01-语言基础与结构.md](../Kotlin_in_Action_2e/01-语言基础与结构.md) ✅ 在架（参数/默认值地基）；Effective_Kotlin 无对应分档，落 [00 档](00-总览与阅读地图.md)。

## ⚠️ 欠账

- 原书逐字章名/章号（7–12 区间内定位）；"builder 退守边界"是否书中明说（现为归纳）。
- 默认参数语言细节（引用前参禁令、@JvmOverloads 生成规则）🔧 全部未实测（本机无 kotlinc）。
