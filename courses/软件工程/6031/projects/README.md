# 6.031 配套项目计划（骨架，本轮不写代码）

主语言：Java 17（与课程一致）；构建：Gradle（多子项目），测试 JUnit 5 + jqwik（属性测试）。
课程原版为 4 个编程作业 + 1 个 Project；下表把它们拆成"每章一个可独立编译的小项目"，并保留对应的作业编号映射。
约定：`s01_xxx/` 每个子目录含 `src/main/java`、`src/test/java`、`README.md`（规格 + RI/AF 说明）与 `build.sh`（Gradle wrapper），本轮只写不编译。

| 章节（讲次） | 建议语言 | 小项目 | 编译方式 |
| --- | --- | --- | --- |
| L2–L5 Java/测试（≈A01） | Java 17 | 有理数/日期工具类：先写规格再写 JUnit 参数化用例，覆盖率报告（JaCoCo） | `./gradlew :s01:test :s01:jacocoTestReport` |
| L6–L7 规格与测试策略 | Java 17 | `Tournament` 排名系统（对应课程经典作业）：规格 + 输入分区导出用例 + jqwik 属性测试（传递性/幂等） | `./gradlew :s02:test` |
| L8–L9 ADT 与不可变（≈A02） | Java 17 | 不可变 `RangeSet`/`Interval`：AF/RI 注释、深拷贝、缓存与 `hashCode/equals`；附"表示暴露"自查清单 | `./gradlew :s03:test` |
| L10–L12 接口/泛型/子类型（≈A03） | Java 17 | 表达式求值器（不可变 AST + Visitor）与 `ReadOnlySet<T>` 泛型层次：证明 LSP 不被破坏 | `./gradlew :s04:test` |
| L13 可变 ADT | Java 17 | `TextBuffer`/编辑器缓冲区：观察者-变更者分离、迭代器失效演示、快照视图 | `./gradlew :s05:test` |
| L14–L15 OO 设计与模式 | Java 17 | 记账/外卖订单系统：分层 + 策略（折扣）+ 工厂（订单）+ 装饰（加料），一次"重构 diff"演练 | `./gradlew :s06:test :s06:checkstyleMain` |
| L16–L18 并发（≈A04） | Java 17 | 线程安全 `TaxiDispatcher`/`Broker` 队列：Guarded Object、锁顺序、ExecutorService 与并行流对比；含死锁演示用例 | `./gradlew :s07:test` + `-DenableDeadlockDemo` |
| L19 性能与记忆化 | Java 17 | 带容量上界的 LRU/Memoizer（线程安全），JMH 风格简易基准与命中率统计 | `./gradlew :s08:bench`（脚本内 `java -jar` 执行） |
| L20–L21 Web 服务（≈Project 后端） | Java 17（JDK 内置 `com.sun.net.httpserver`） | 无状态 TODO/任务 REST 服务：路由-服务-存储三层、幂等与错误规范、契约测试 | `./gradlew :s09:run`（`build.sh` 生成 fat jar） |
| L22–L23 Web 安全（≈Project 安全加固） | Java 17 | 把 s09 改造成"可被攻击再修好"：注入/XSS/CSRF/会话固定四类漏洞各写 PoC 测试，再修复使其转绿 | `./gradlew :s10:test`（含 `--tests "*SecurityRegression*"`） |
| L24 综合交付 | Java 17 | 迷你全栈 Project（对应课程 Project 精神）：不可变领域模型 + 线程安全服务层 + REST 接口 + 安全回归测试 + 代码审查清单 | `./gradlew build`（checkstyle + spotless + test） |

> 语言备选：若想练现代语言同一套概念，可用 Kotlin（`data class` 天然不可变）或 Rust（编译器即 RI 检查）复刻 s03/s04/s07 三个最关键的项目；`build.sh` 结构保持一致。
> 质量门禁建议：每个子项目都接 `spotlessCheck` + `checkstyle`，把课程"代码风格也是评分一环"的思想固化到脚本里。
