# Kotlin 系列·总索引

> 2026-10-07 开波。本文件是 `book/` 下 Kotlin 系列的总索引，收录 **10 本**主流英文书 + 官方资料线的章节目录档案。
> 元数据状态标注：✅ 已核实（含用户提供的联网出处）｜⚠️ 待核验（凭记忆或二手，不写死）｜📄 来自既有笔记。
> 使用约定：只做导航与元数据归档，不改动各书正文笔记；新增书目按分表追加并同步「收录统计」。

## 读者画像与路线（本系列定位）

本系列面向**已有 Java/C++/后端经验**的工程师：不从零基础教材啃，重点是把 Java idiom 翻成 Kotlin idiom，再单独立起「协程/Flow」与「编译器/互操作」两条专项线。

1. **主线**：Kotlin in Action 2e（核心）→ Effective Kotlin（规范）→ Java to Kotlin（迁移）→ 协程专项（官方文档 + kotlinx.coroutines 源码）。
2. **入门补网**：Atomic Kotlin（系统性）；Head First Kotlin / BNRR 仅作二手参考，不建深度档。
3. **函数式线**：Functional Programming in Kotlin ↔ The Joy of Kotlin 对读。
4. **JVM/后端线**：与 `Spring系列·总索引.md` 衔接（Spring Boot + Kotlin、WebFlux/协程、JPA/Jackson 互操作坑）。
5. **语言实现线**（对治本仓 C++/ABI/编译器兴趣线）：官方文档 + KEEP + kotlin compiler 源码：K2/FIR、IR、suspend 状态机/CPS、inline/reified、name mangling、metadata、KSP、compiler plugins——**书依赖度最低，暂不建书档**。

## 一、核心主线（已建章节目录）

| 书 | 目录 | 出版社·年份 | ISBN | 优先级 | 状态 |
|---|---|---|---|---|---|
| Kotlin in Action, 2nd Ed. | [Kotlin_in_Action_2e/](Kotlin_in_Action_2e/00-总览与阅读地图.md) | Manning·2024-04 | 9781617299605 | ★★★ 第一优先 | ✅ 四作者名录实（含 Elizarov） |
| Effective Kotlin | [Effective_Kotlin/](Effective_Kotlin/00-总览与阅读地图.md) | Packt·2022 | ⚠️9781805125897 | ★★ | ⚠️（403 墙） |
| Java to Kotlin: A Refactoring Guidebook | [Java_to_Kotlin/](Java_to_Kotlin/00-总览与阅读地图.md) | O'Reilly·2023 | 中文版 978-7-111-73703-2 ✅ | ★★ | ✅ McGregor & Pryce |
| Atomic Kotlin | [Atomic_Kotlin/](Atomic_Kotlin/00-总览与阅读地图.md) | no starch press·2021-11 | ⚠️9781593279610 | ★★ | ✅ 87 章全目录 |
| Functional Programming in Kotlin | [Functional_Programming_in_Kotlin/](Functional_Programming_in_Kotlin/00-总览与阅读地图.md) | Apress·2021 | ⚠️待核验 | ★ | ⚠️ |

## 二、次线与对照参考

| 书 | 定位 | 处置 |
|---|---|---|
| The Joy of Kotlin（Saumont，Manning 2019）| 函数式深读，与 FPIK 对读 | ✅ 已建档 [The_Joy_of_Kotlin/](The_Joy_of_Kotlin/00-总览与阅读地图.md) |
| Programming Kotlin（Venkat，Packt 2018）| JVM/DSL/异步综论（并发章按 2018 时效降权） | ✅ 已建档 [Programming_Kotlin/](Programming_Kotlin/00-总览与阅读地图.md) |
| Kotlin Cookbook（Kousen，O'Reilly 2022）| 问题驱动食谱 | ✅ 已建档 [Kotlin_Cookbook/](Kotlin_Cookbook/00-总览与阅读地图.md) |
| Head First Kotlin（Griffiths）| 零基础向，本画像跳过 | 不建深度档 |
| Kotlin Programming: BNRR Guide | 实践向，与 Atomic 重叠 | 不建深度档 |
| Kotlin in Action 1e（2017，9781617293290）| ✅ 存在；2017 无协程现代化内容 | 降级为参考书，不另建档 |

## 三、官方资料线（非书，协程/实现线主教材）

- kotlinlang.org/docs/books.html（官方推荐书目页，本波 10 书目出处之一 ✅）
- Coroutines and flows guide、Guide to stdlib、K2/FIR 编译器文档、KEEP 仓库、kotlin-compiler 源码
- kotlinx.coroutines API 文档 + 源码（Elizarov 系文章 ⚠️ 具体篇名以原文为准）

## 四、与既有系列的衔接

- **C++ 协程对照**：C++20 co_await 状态机 ↔ Kotlin suspend CPS 转换——两仓合读（见 `C++20模板元编程/` 与本系列 KiA2e 协程章互链）。
- **Spring 线**：Spring Boot Kotlin 支持、jakarta 时代的 `suspend fun` Controller（衔接 `Spring系列·总索引.md` 路线 2/3）。
- **论文线**：无直接对应；协程调度器阅读可对照 `paper/ELEPHANT/dapper` 式源码考古法。

## 五、购买/阅读终裁（对用户粘贴的第三方 AI 结论的核对结果·2026-10-07 联网销账版）

- 五本终裁清单成立 ✅（与官方 books 页一致）。
- **KiA2e 作者四名录实 ✅**：Sebastian Aigner, **Roman Elizarov**, Svetlana Isakova, Dmitry Jemerov（Manning 官方页直证）——第三方结论"含 Elizarov"**成立**，第 1 波的存疑标注撤销；Isakova 同时是 Atomic Kotlin 作者（谱系互锁）。
- **Java to Kotlin 作者勘正 ✅**：Duncan McGregor & Nat Pryce——第三方结论所称 "Duncan DeVore" **为误**；中文版《Java到Kotlin：代码重构指南》机械工业 978-7-111-73703-2，23 章全目录 ✅。
- **Atomic Kotlin ✅**：no starch press/Learn Kotlin，2021-11-22，588 页，官方 7 部 87 章+2 附录全目录取得；印刷 ISBN 仍 ⚠️9781593279610。
- **The Joy of Kotlin ✅**：Saumont，Manning 2019-04，ISBN **9781617295362**（第 1 波记忆 377 为误，已销）。
- 403/404 墙未破、维持 ⚠️：Effective Kotlin（Packt）、Programming Kotlin（Packt）、Kotlin Cookbook（O'Reilly）、FPIK（Apress/Springer）的 ISBN/逐字章目录——购电子版后销账。

## 收录统计

- 2026-10-07 第 1 波：核心 5 本建目录（各 1 枚 00-总览与阅读地图，分章档待第 2 波）+ 本总索引。
- 2026-10-07 同日续批：Joy/Programming/Cookbook 3 本 00 档补齐——**用户书目清单内 8 本可建档者全部落档**（Head First/BNRR 按画像判不建深度档），全系列 9 枚档案 + 索引。
- 待办：第 2 波分章展开（01–NN）；各书 ISBN/作者/逐字目录联网核验销账。
- 2026-10-07 第 2 波收束 ✅：**62 枚分章全落**（KiA2e 01–10、Effective 01–08 条目簇、JtK 01–12、Atomic 01–08、FPIK 01–06、Joy 01–06、Programming 01–06、Cookbook 01–06 食谱带）；kotlin_check 验收 **70 枚文件 / 0 断链**。
  - 链名对账闭环：KiA2e 01/02 与 Effective 01/03 旧前向链改指实档名；Cookbook 01/02 旧「05-空安全与异常Result」带未单列建档，链接改指 06-工程与互操作食谱并挂 ⚠️欠账；Programming 02/03「04-泛型与variance」撞号裁决=02 改指跨系列 KiA2e 06-泛型、03 改指本系列实名 04。
  - 🔧 实测口径：本机无 kotlinc，全系列实验位一律标「未实测」；协程/擦除对照挂 `TypeScript系列·Runtime_vs_Type_System专题.md` 与 C++20 协程档。
  - 仍待销账：Effective/Packt 双册、FPIK、Cookbook 的 ISBN 与逐字目录（403/404 墙）；本系列 commit 均未 push。
