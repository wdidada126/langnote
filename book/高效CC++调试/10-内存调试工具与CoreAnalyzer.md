# 10 内存调试工具与 Core Analyzer（原书第 10、11 章）

> 覆盖《高效C/C++调试》**第 10 章**（10.1 ptmalloc's MALLOC_CHECK_；10.2 Google Address Sanitizer；
> 10.3 AccuTrak；10.4 有效地调试内存损坏；10.5 实战故事6：内存管理器的崩溃问题；10.6 小结）与
> **第 11 章**（11.1 使用示例；11.2 主要功能：搜索引用的对象（水平搜索）/查询地址及其底层对象（垂直搜索）/
> 内存模式分析/查询堆内存块/堆遍历；11.3 小结），原书 pp.207–246。
> 目录来源见 [../高效CC++调试.md](../高效CC++调试.md)。系列导航：[../C++系列·总索引.md](../C++系列·总索引.md)。

## 核心概念速览（中英对照）

- **MALLOC_CHECK_** — glibc 分配器自检开关（环境变量 0/1/3）：每次 malloc/free 校验元数据，轻但粗
- **AddressSanitizer（ASan）** — 编译期插桩+影子内存的内存错误检测器：越界/UAF/泄漏统一捕获（10.2）
- **影子内存** — shadow memory：每 8 字节应用内存映射 1 字节影子字节，记录该块 redzone/合法性比例
- **红区** — redzone：分配块之间与两侧插入的不可读写区，越界即命中并当场报告
- **隔离区** — quarantine：free 后延迟归还的内存池，把「复用掩盖 UAF」变成「必然踩雷」
- **AccuTrak** — 本书作者自研内存追踪器（10.3）：记录每次分配/释放的调用栈与对象状态，在 core 上离线查询
- **Core Analyzer** — 本书作者自研 core 分析器（第 11 章）：水平/垂直引用搜索、内存模式分析、堆块遍历五类功能
- **内存模式分析** — memory pattern analysis（11.2.3）：按字节分布/对齐/字符串性给未归属内存「验尸定类」
- **堆遍历** — heap traversal（11.2.5）：沿分配器元数据走全堆——既查损坏又出统计（[02 篇](02-堆数据结构.md) 手工版的自动化）
- **泄漏 vs 损坏** — leak vs corruption：LSan/ASan 管「没人引用了」，Core Analyzer 管「有人在错误地引用」

## 1. 动机：把 [02](02-堆数据结构.md)/[03](03-内存损坏.md)/[04](04-C++对象布局.md) 章知识产品化

前三章的侦查流程（读元数据→二分写点→引用图合围）人工做一遍要半小时，每单都这样不可持续。
第 10 章把「运行中检测」外包给工具（自检开关/插桩/追踪），第 11 章把「事后分析」外包给
Core Analyzer（在 core 上直接问「谁引用这块」「这块原来是什么」）。本章文件合并两章：
它们共同回答**「内存问题该在哪个阶段花力气」**。

## 2. 机制

### 2.1 运行时检测的三档（10.1–10.3）

| 档位 | 代表 | 开销 | 抓到什么 | 抓不住什么 |
| --- | --- | --- | --- | --- |
| 分配器自检 | MALLOC_CHECK_、`mtrace` | ~0–2× | 元数据破坏的**症状**（报在错误附近） | 越界不碰元数据、UAF 无复用 |
| 编译期插桩 | ASan（10.2） | 2× 时间/2–3× 内存 | 越界/UAF/双 free/泄漏，**当场给两侧栈** | 未插桩的预编译库、非类型化越界（栈上旧式） |
| 全量追踪 | Valgrind memcheck；AccuTrak（10.3） | 10–50×（Valgrind） | 无需重编；记录分配史 | 慢；对 JIT/新指令敏感 |

ASan 的「当场给两侧栈」是其决定性优势：报错格式含「分配栈 + 释放栈 + 越界访问栈」三联，
[08 篇](08-调试方法论与复现.md) 的归因直接被自动化。机制三件套（影子内存+redzone+quarantine）
见经典论文（Serebryany/Bruening/Potapenko/Vyukov, USENIX ATC'12；无 DOI，核实记录见 [03 篇](03-内存损坏.md)）。

🔧 **已实测（平台边界）**：本机 MinGW-w64 GCC 15.2 `g++ -fsanitize=address` 链接失败
`ld.exe: cannot find -lasan`——该工具链未随附 ASan 运行时。Windows 上的等价路径：
MSVC `/fsanitize=address`（VS2019 16.9+；docs `learn.microsoft.com/cpp/build/reference/fsanitize` 实测可达）
或 clang++（自带 ASan 运行时）。结论：**别假设「有 g++ 就有 ASan」，跨栈团队要按发行版逐一确认运行时随附**。

### 2.2 三联栈怎么读（ASan 报告的解剖学）

一条典型 heap-buffer-overflow 报告三段：**ERROR 行**（越界读写方向+偏移量，`0 bytes to the right of
8-byte region` 直接给出「越了几字节」）→ **allocated by thread / freed by thread**（块的生与死，
两条栈）→ **崩溃线程访问栈**（写坏它的那一行）。读法纪律：先看「偏移量与邻块类型」判断是数据流越界
还是 size class 混淆；再用生/死栈的时间差推断是「忘 free 前被改」还是「并发释放」；三条栈对不上任何
模块时，怀疑预编译依赖未插桩（ASan 盲区，转 Valgrind/AccuTrak 路线）。

🔧 快速上手参数：`ASAN_OPTIONS=detect_leaks=1:abort_on_error=1:malloc_context_size=30`
（Linux；Windows 经 MSVC ASan 用 `set ASAN_OPTIONS=...` 同型）；`halt_on_error=1` 配合
`ASAN_OPTIONS=external_symbolizer_path` 可把 ASan 变成「崩溃即断点」的交互式体验。

### 2.3 有效地调试内存损坏（10.4）——工具也要讲流程

原书给出的顺序（转述）：先用最便宜的（编译器告警、MALLOC_CHECK_/自检）缩小到「堆问题」，
再上 ASan/追踪器拿三联栈，最后才动用元数据手术刀手工验证——与 [08 篇](08-调试方法论与复现.md) 的
假设-实验循环同构：每档工具=一个假设检验器。10.5 实战故事6「内存管理器的崩溃问题」的教训样本：
**崩溃点栈里出现分配器≠分配器 bug**，先用工具证明元数据被外部写坏，再谈「谁写的」。

### 2.4 Core Analyzer 五功能（第 11 章）

对照 11.2 目录逐条给「输入→输出→对应手工流程」：

1. **搜索引用的对象（水平）**：输入地址/对象 → 输出所有指向它的字及其宿主对象/栈帧——回答
   「谁还在引用已释放对象」（[04 篇](04-C++对象布局.md) 4.4 自动化）；
2. **查询地址及其底层对象（垂直）**：输入一个可疑字 → 试探「能否按 T 解释且整族指针合法」→
   输出最可能宿主对象——回答「这个脏值是不是某对象的中段」；
3. **内存模式分析**：对无主区域做统计画像（字节熵、对齐性、指针密度、字符串性）——
   区分「栈残渣/堆残骸/JIT 码/填充」；
4. **查询堆内存块**：给定用户指针 → 定位其 chunk 头、size class、邻块、free 状态；
5. **堆遍历**：全堆一致性检查+分配直方图——一屏看出「20 万个 64 字节块」这类泄漏指纹。

使用姿势（11.1）：attach core 而非 live 进程，功能 1/2 组合即「对象引用图重建」。

## 3. 权衡

- **检测阶段前移 vs 现场真实性**：ASan 重编改变时序与布局（测出的 UAF 真实，但「只在 ASan 出现」的
  报告也存在——quarantine 放大时间窗）；生产上 GWP-ASan 以抽样换 1% 级开销+真实现场。
- **自研工具依赖布局假设**：AccuTrak/Core Analyzer 这类堆遍历器与分配器实现强耦合（ptmalloc 版本
  敏感）；通用替代=「调试分配器+日志」或 ASan 的 `malloc_context_size` 换现场完整度。
- **core 体积 vs 功能 1/2/3 可用性**：coredump_filter 砍掉堆的 core 只能跑功能 4/5——
  上报系统要为「疑难工单」保留完整 core 通道（[11 篇](11-系统级观测与崩溃上报.md)第 13 章）。

## 4. 相邻概念对比

- **ASan vs LSan vs MSan vs TSan vs UBSan**（全景见「最新演进」表）：同族但抓的类别正交；
  ASan 管空间+释放后，LSan 管「没人引用」，MSan 管「没写过」，TSan 管时序，UBSan 管语言规则。
- **Core Analyzer vs GDB 脚本（[09 篇](09-拓展调试器能力.md)）**：后者是「人写查询」，前者把高频查询
  做成命令；GDB Python 完全可复刻功能 1/2 的简化版（练习方向）。
- **堆遍历 vs 泄漏检测**：遍历给「快照统计」，LSan 给「分配栈归因」；OOM 前夜两者互为印证。

## 最新演进与工业实践

- **Sanitizers 全家桶现状**（Linux/clang；Windows 见下条）：

  | 成员 | 抓什么 | 典型开销 | 备注 |
  | --- | --- | --- | --- |
  | ASan/LSan | 越界/UAF/double-free/泄漏 | 2×/2–3× | CI 标配 |
  | UBSan | 溢出/空解引用/非法对齐等 UB | <2× | `-fsanitize=undefined,implicit-conversion` |
  | TSan | 数据竞争 | 5–15× | 与 ASan **互斥**编译 |
  | MSan | 未初始化读 | ~3× | 需全量插桩（含 libc），门槛最高 |
  | HWAsan | 同上越界/UAF，真指针标签（AArch64+MTE 为硬件版） | ~10% 时间 | 移动/ARM 服务器主力；`arm64_mte` 内核支持 |

- **Windows 官方化**：MSVC 的 `/fsanitize=address`（VS2019 16.9 起，版本以微软文档为准）与
  `/fsanitize=thread`（VS2022 中后期，⚠️ 具体版本号未细核）使双栈团队在 VS 里同一开关；
  MinGW-w64 主流发行版至今不随附 libasan（本机实测）。
- **生产内存安全**：Chromium GWP-ASan、Android Scudo（硬化分配器，HWASAN 的硬件化 MTE 在 Pixel/服务器
  ARM 上试点）；Corretti/错误注入类「影子部署」检测 UAF 的新研究 ⚠️ 前沿观察。
- **AI 辅助（⚠️ 前沿观察）**：LLM 解读 ASan 三联栈、生成最小复现的流水线已有公开演示
  （AutoCodeRover 类，arXiv:2404.05427 实测存在）；把本表当「该跑哪个工具」的决策树喂给它仍是主流用法。
- **开源仓库逐点对应**：`llvm/llvm-project`（compiler-rt/lib/asan 即影子内存实现）、
  `google/sanitizers`（issue 复现库=活教材）、`gdb`（`catch syscall` 与 ASan 断点协同）。

## 互链

- 原书大纲：[../高效CC++调试.md](../高效CC++调试.md)
- 分配器机制前提 → [02-堆数据结构.md](02-堆数据结构.md)；损坏类别学 → [03-内存损坏.md](03-内存损坏.md)
- 垂直搜索的合法性判定依赖映射表 → [06-进程镜像与CoreDump.md](06-进程镜像与CoreDump.md)
- 泄漏专题（第 14 章）与 RAII → [12-泄漏协程远程容器与预防.md](12-泄漏协程远程容器与预防.md)
- 工具操作版（VS CRT 泄漏例程、ASan 开关实操） → [../C++代码调试的艺术.md](../C++代码调试的艺术.md) 第 6 章
