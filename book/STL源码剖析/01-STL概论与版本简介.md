# 第 1 章 STL概论与版本简介（Introduction and versions）

> 覆盖原书第 1 章：STL 的接口观念、版本与实现史（HP STL → SGI STL → gcc/STLport → C++ 标准）、
> 六大部件全景图、容器/算法/迭代器的配对关系。
> 本章回答一个地图问题：**六大部件各在哪一层，谁依赖谁。**
> 机制转述自原书框架与 SGI/HP 公开源码谱系，不伪造原书逐字原文。

## 核心概念速览（中英对照）

- **标准模板库** — Standard Template Library (STL)：泛型容器 + 算法 + 迭代器的三元组合库，后为主体并入 ISO C++ 标准库。
- **六大部件** — six components：容器、算法、迭代器、仿函数、配接器、空间配置器；本书（及本目录 00 文件）反复使用的分类。
- **迭代器是胶水** — iterators as glue：算法只认迭代器的五档能力，不认容器内部结构，从而 M 个算法 × N 个容器只需 M+N 份代码。
- **HP STL** — H.P. STL：Hewlett-Packard 的早期实现（类名 `Category` 后缀、`HList`/`HVector`），SGI 的前身。
- **SGI STL** — SGI STL：Silicon Graphics 的增强实现，贡献了 slist/rope/hash 系容器与两级配置器，深刻影响 gcc 2.91 的 libstdc++ 与 STLport。
- **STLport** — 跨平台第三方 STL 发行版（Boris Fung 主导），曾把 SGI 源码大量带走，⚠️ 具体年份未核实。
- **容器类别** — container category：序列式（sequence）与关联式（associative）两大族群，外加适配器形态的栈/队列。
- **算法覆写位置** — in-place vs out-of-place：同名算法以输出迭代器为界分两型，如 `copy` 之于 `transform`。

## 动机：为什么需要「部件化」的库

90 年代初的 C++ 类库各造各的轮子：每个容器自带一套 sort/find，容器和算法互相耦合、
无法复用。Alexander Stepanov（STL 之父）的核心洞察是把「数据在哪里」和「对数据做什么」
正交化：**容器管存储，迭代器管定位，算法管搬运，仿函数管策略，配置器管内存，适配器管缝合**。
有了这层正交，`std::sort` 不需要知道 `vector` 的 `start/finish` 长什么样，
它只需要一个随机访问迭代器；换实现、换容器、换比较策略，代价都是 O(1) 份代码。

本书选择剖析 SGI STL 而非「ISO 标准文本」，理由与此一致：标准只规定语义，
**SGI 源码是当时你能读到的、工程质量最高的完整答案**，而 gcc/MSVC 的现代实现
仍是它的直系后代（libstdc++ 的红黑树、deque 的 512 字节缓冲都能在本地
`bits/stl_deque.h` 里看到同名机制，已实测 g++ 15.2 头文件）。

## 机制：六个部件的依赖层

```text
        ┌──────────┐   驱动    ┌──────────┐
        │ 算法      │◄────────►│ 仿函数    │   ← 策略层：做什么、怎么做
        └────┬─────┘           └────┬─────┘
             │ 只经手               │ 被适配器改造
        ┌────▼─────┐           ┌────▼─────┐
        │ 迭代器    │◄──配接────│ 配接器    │   ← 接口层：在哪读、在哪写
        └────┬─────┘           └──────────┘
        ┌────▼─────┐
        │ 容器      │                  ← 存储层：数据摆成什么形状
        └────┬─────┘
        ┌────▼─────┐
        │ 配置器    │                  ← 地基层：内存从哪来
        └──────────┘
```

关键不变式：**上层永远不知道下层的存在**——算法不知道容器，容器只知道自己的迭代器，
只有配置器与容器的关系是「显式模板参数」级别的耦合（`vector<int, alloc>`），
这也是第 2 章把它放在正文最前面讲的原因（本目录的顺序同理）。

### 版本谱系一图流

```text
1993  HP STL（Stepanov & Lee《The STL Portability Guide》系）
  │     类名带 Category 后缀；容器名 HList/HVector/HDeque...
  ▼
1994-1999 SGI STL 1.x→4.x（Meng Lee、David Musser、Nicolai Josuttis 时代的文档站）
  │     两级 allocator、hash 系容器、slist/rope、concept checking、文档化概念体系
  ▼
1998  ISO C++ 标准（STL 作为主体并入；选 HP 概念模型而非 SGI 全部扩展）
  ├─► libstdc++（gcc 2.91 起大换血采用 SGI 源码；至今仍是 GNU 默认）
  ├─► STLport（把 SGI 源码带到各编译器）
  ├─► MSVC STL（Dinkumware 授权起家，后完全重写，开源 microsoft/STL）
  └─► libc++（LLVM，从 Apple 起步，独立血统）
```

⚠️ 上表的年份行按公开史料整理（SGI 文档站 "History" 页与 gcc release notes 为据），
未逐条对照原书第 1 章原文。

## 权衡：正交性的账单

| 维度 | 传统类库（成员函数式） | STL（部件正交式） |
| --- | --- | --- |
| 代码量 | M 容器 × N 算法 | M + N |
| 定制策略 | 改容器代码/继承覆写 | 传函数对象，编译期参数化 |
| 内联机会 | 虚函数/成员调用 | 全模板 → 零成本抽象 |
| 学习曲线 | 每容器一本手册 | 先学迭代器五档 + 概念 |
| 报错体验 | 温和 | 模板错误雪崩（98 时代无 concepts）|

「零成本抽象 vs 报错雪崩」这笔债，直到 C++20 concepts 才还掉大半——见
[../C++模板元编程.md](../C++模板元编程.md) 与 07 篇对照。

## 相邻概念对比

- **STL vs 标准库**：STL 是标准库的子集加前身；本书剖析的 slist/rope/hash_map 不在标准内，
  `std::string`/`iostream` 也不在本书正文范围。
- **HP vs SGI**：HP 重概念纯度（为「概念」而写文档），SGI 重工程性能（内存池、内联、
  非标准扩展），所以侯捷选 SGI 剖析「实现」，选 HP 讲「设计」⚠️（此句为机制转述，非原书逐字）。
- **本书 vs Josuttis《C++标准库》**：那本教你用标准件（本仓库 [../C++标准库.md](../C++标准库.md)），
  这本带你造一遍；两本互为横纵轴。

## 最新演进与工业实践

- **概念（concepts）落地**：SGI 当年用 `concept_checks.h`（运行期假装的编译期检查宏，镜像仓库可见该文件）
  预演了概念检查；C++20 concepts 是它的标准化终态。工业界现在写泛型接口首选 constrained template。
- **文档形态演化**：SGI 文档站（sjs/sgi.com/tech/stl）随公司退役，现靠
  [镜像](https://github.com/justinmeiners/sgi-stl-docs) 与 cppreference 双轨存活；cppreference 实际继承了
  SGI「按概念组织」的目录学。
- **谱系现状（2026）**：libstdc++/libc++/MSVC STL 三家开源实现并存竞争（[gcc-mirror/gcc](https://github.com/gcc-mirror/gcc)、
  [llvm/llvm-project](https://github.com/llvm/llvm-project)、[microsoft/STL](https://github.com/microsoft/STL)），
  SGI 血统主要体现在 libstdc++；libc++ 的 deque/vector 结构已多次重写（细节 ⚠️ 未逐一核实，见本目录 07 篇）。
- **学习资源迁移**：与本书配套的开源解读 [SilverMaple/STLSourceCodeNote](https://github.com/SilverMaple/STLSourceCodeNote)
  仍可达（实测 200），可作原书对照读物。

## 常见误区

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「STL = C++ 标准库」 | 标准库还含 string/iostream/数值/并发等；STL 只是容器+算法+迭代器+函数对象等主干 |
| 2 | 「本书讲的是标准」 | 讲的是 SGI 的一份实现；标准只锁语义不锁结构（比如 deque 块大小非标准规定） |
| 3 | 「学 STL 过时了」 | 具体 API 过时，**部件正交 + 零成本抽象**的设计范式统治至今（ranges、absl、 folly 全部沿用） |
| 4 | hash_map 是标准容器 | 本书时代是 SGI 扩展；标准件是 C++11 的 unordered_map（见 05、07 篇） |

## 与其他章 / 其他书的联系

- 部件依赖图里「配置器是地基」→ [02-空间配置器.md](02-空间配置器.md)
- 「迭代器是胶水」的机制展开 → [03-迭代器与traits.md](03-迭代器与traits.md)
- 序列/关联两族群的划分依据 → [04-序列式容器.md](04-序列式容器.md)、[05-关联式容器.md](05-关联式容器.md)
- 适配器谱系与版本史后续 → [06-算法仿函数与配接器.md](06-算法仿函数与配接器.md)、[07-专题-SGI_STL到现代标准库.md](07-专题-SGI_STL到现代标准库.md)
- 单文件版大纲（含豆瓣链接）：[../STL源码剖析.md](../STL源码剖析.md)；
  系列导航：[../C++系列·总索引.md](../C++系列·总索引.md)；用法横轴：[../C++标准库.md](../C++标准库.md)

> 行尾自查：本章引用的外部链接均于 2026-09 实测可达。
