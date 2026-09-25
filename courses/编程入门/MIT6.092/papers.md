# MIT 6.092 参考文献与开源应用（骨架）

## 经典论文 / 文献

| 文献 | 作者/年份 | 关联讲次 | 说明 |
| --- | --- | --- | --- |
| The Java Virtual Machine Specification | Lindholm & Yellin, 1999 (2nd ed.) | L1 | 理解"编译到字节码"的权威出处 |
| Effective Java (1st/后续版) | Joshua Bloch, 2001 起 | L4–L7 | 从语法到惯用法的必读文献 |
| Efficient Learning Machines?（Java 安全性）"Java Security: Hostprotect..." | Dean, Felix & Woods, 1996 | L1/L7 | JVM 沙箱与异常机制背景 |
| How to Think Like a Computer Scientist: Learning with Python/Java | Allen Downey et al. | 全课 | 课程指定教材 |
| Growing a Sublanguage: Java Threads/Exceptions 讨论 → "Handling Exceptions"? | — | L7 | 可选：Goosevm 或 Downey 附录 |

> 骨架注：6.092 本身是语法入门课，经典文献以语言规范与风格经典为主，证明型论文较少。

## 近 5 年文献 / 资料（2021–2025）

| 资料 | 年份 | 关联讲次 | 说明 |
| --- | --- | --- | --- |
| JEP 444: Virtual Threads (Project Loom) | 2022–2023 | L1 | JVM 演进：轻量级线程改变并发写法 |
| JEP 401/421/445: Generics on Value Classes 等 (Project Valhalla) | 2021+ | L5 | 对象内存布局与基本类型的边界演进 |
| Google Java Style Guide（持续更新） | 2021+ | L3 | 课程代码风格要求的现代工业版 |

## 知识点在开源项目中的应用

| 知识点（讲次） | 开源项目 | 体现 |
| --- | --- | --- |
| 字节码/JVM (L1) | GraalVM / OpenJDK | 多语言 JVM 生态 |
| 字符串不可变性 (L4) | Lucene | Term/BytesRef 设计对照 String 内存代价 |
| 类与封装 (L5) | Spring Framework | IoC/DI 建立在基础 OOP 之上 |
| 继承与多态 (L6) | JUnit | Extension/Runner 接口体系 |
| 异常处理 (L7) | OkHttp / Guava | 受检异常取舍与 Preconditions 风格 |
