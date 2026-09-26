# 专题补编：从 SGI STL 到现代 libstdc++/libc++/MSVC STL——容器与分配器的演化对照

> **补编，不冒充原书章节**。把 01–06 篇的每个「机制」映射到 2026 年的标准文本与三家开源实现，
> 回答读者合上书后的最后一个问题：**「所以今天该怎么写？」**
> 本机对照实验均为 MinGW-w64 **g++ 15.2（x86_64, `-std=gnu++23`）** 实测，
> 源文件存于仓库外 `D:\develops\tmp\cppsnippets_stl\`（t1–t4），仓库内不留编译产物。

## 核心概念速览（中英对照）

- **allocator_traits** — C++11 起的分配器适配层：为定制类型自动补默认成员，「接口收缩」的执行者。
- **多态内存资源** — `std::pmr::memory_resource`：运行期虚表分派的分配策略，C++17。
- **多态分配器** — `polymorphic_allocator<T>`：`memory_resource*` 的类型擦除持有者，具备递归传播规则。
- **池资源** — `pool_resource` 家族：`unsynchronized/synchronized_pool_resource`——SGI 二级 free-list 的标准化身。
- **单调缓冲资源** — `monotonic_buffer_resource`：bump pointer + 溢出转上游，整块生命周期结束才释放。
- **空资源** — `null_resource`：一切分配请求都失败的哨兵（C++20）。
- **模板模板实参放宽** — P0522R0（2016，已并入 C++17）：让「参数更多的 allocator」能匹配带默认参数的模板模板形参。
- **平铺哈希表** — flat/open-addressed hash map：absl::flat_hash_map、unordered_dense、robin-map——工业取代链式 unordered_map 的主流形态。
- **范围视图** — ranges::views (C++20)：惰性组合管道，接管 98 代函数/迭代器适配器的大部分场景。
- **非拥有引用类型** — `string_view / span`：把「借用」语义标准化，补 auto_ptr 时代的借用空白。
- **值语义可选/变体/类型擦除容器** — `optional / variant / any`：`uninitialized_*` 手工内存管理的高级语言化替身。
- **容器现代变体** — `std::pmr::vector`、C++26 `vector_bool`（libc++ 首发 ⚠️ 版本细节未逐一核实）等。

## 一、分配器线：从「编译期模板参数」到「运行期虚表指针」

### 年表（已核实的标 ✅，未核实提案号的标 ⚠️）

```text
C++98   allocator<T> 入标；SGI 双轨（alloc + 标准壳）；allocate(n, hint)、construct/destroy 齐备
C++11   allocator_traits 登场：接口默认由 traits 补齐，定制成本大降
C++17   ✅ P0522R0 并入（模板模板实参放宽）——容器套容器传 allocator 的语法堵漏
        std::pmr（memory_resource + polymorphic_allocator）入标（源自 Bloomberg 的 Memory Allocation
        TS；⚠️ 该 TS 的具体文档编号本次未能核实，不猜测）
C++20   std::allocator 瘦身：construct/destroy 移除、hint 版 allocate 移除（本机 t1 实测 ✅）
        pmr::null_resource / 单调资源改进
C++26   ✅ P2875R4《Undeprecate polymorphic_allocator::destroy For C++26》——
        C++20 曾顺手弃用的 pmr::destroy 被复活（标题实测核实于 cplusplus/papers）
```

### 本机实测（已实测 g++ 15.2，🔧 t1）

```cpp
std::allocator<int> a;
auto p = a.allocate(4, nullptr);   // gnu++17: 编译过（deprecated 路径仍在）
a.construct(p, 42);                // gnu++17: 编译过
                                   // gnu++23: 两个都报错 ——
// error: no matching function for call to std::allocator<int>::allocate(int, nullptr_t)
// error: 'class std::allocator<int>' has no member named 'construct'
```

**结论**：02 篇讲的那套「allocator 亲手起对象」的接口在标准侧已收缩为
「分配/释放 + construct 交给 allocator_traits 默认（placement new）」。
教学价值不变（机制仍在，只是搬家到 traits），**工程上别再手写 `a.construct`**。

### pmr 取代「到处带 allocator 模板参数」（已实测 g++ 15.2，🔧 t2）

`std::pmr::vector<int>` + 自定义 `counting_resource`：`push_back` 1000 次（libstdc++ 几何扩容）
共触发 **11 次分配、8188 字节**——02 篇「翻倍成长 + 整块搬家」的算法形状直接可从分配序列读出；
`monotonic_buffer_resource` 配 4KB 栈缓冲，100 个长度 20 的 `pmr::string`（超过 SSO 走堆）
**全部落在栈缓冲内、零 malloc**。这就是今天做「每请求 arena」的正规姿势——
SGI 二级池的思想换了一副皮：档位变成 pool_resource，整块不还变成单调缓冲，粗锁变成每线程无锁资源。

## 二、容器线：形状之争的现代结局（🔧 t3 已实测 g++ 15.2）

| SGI 机制（本目录 04/05） | libstdc++ 15 | libc++ | MSVC STL | 工业建议 |
| --- | --- | --- | --- | --- |
| deque 512B 块 + map | 仍是 512（`_GLIBCXX_DEQUE_BUF_SIZE`，本机头文件实测 ✅） | 三指针 + map，块策略多次重写 ⚠️ | 小对象 16B 块策略 ⚠️ 未本机核对 | 默认仍 vector；队列用 deque 或专用 SPSC |
| vector 翻倍 | 翻倍（2 的幂或 ×2） | ×2 | ×1.5（缓解 memcpy 峰值带宽 ⚠️ 理由按公开文档） | 高频增长先 reserve |
| vector\<bool\> proxy | 保留 | **vector_bool 新物种**（C++26 方向 ⚠️） | 保留 | 需要位打包用真 vector\<bool\> 之外首选 bitvec 库或 std::bitset<N> |
| rb_tree（map/set） | 节点制红黑树，接口换 C++11 emplace/try_emplace、C++17 node handles | 同源结构（红黑树，节点制） | 红黑树 + 每树节点计数优化 ⚠️ | 读多 + 区间查询：map 依旧；纯计数/字典：trie/排序 vector 更快 |
| 开链 hash（扩展） | unordered_map：桶 + 前向节点链 | 桶 + 双向链（cache 优化过）| 桶 + 数组化 slot 实验 ⚠️ | **热路径换 absl::flat_hash_map / unordered_dense** |
| slist | forward_list（标准件） | 同 | 同 | 很少真用得上，优先排序 vector |
| rope | 无 | 无 | 无 | 文本 buffer 自建（引用计数思想见 04 篇） |

实测补充（🔧 t3）：vector 5000 元素首末地址差 = 19996 B（恰 4999×4，连续）；
deque 同规模差 = 145708 B（离散分块），`push_front` 5000 次后**既有元素地址与值不变**
——04 篇「map 搬家不搬元素」在 2026 年的 libstdc++ 上依然字面成立。

## 三、算法/仿函数/适配器线：三条退役，三条转正

- **退役**：`ptr_fun/bind1st/bind2nd/not1/not2/mem_fun(_ref)` 全族 C++17 移除
  （年表为三家实现与标准共识；⚠️ 逐项删除决议编号未核实）。
  继承 `unary_function/binary_function` 不再是义务——03 篇的「证书」在现代由
  `std::invokable` 约束（ranges）或干脆 `auto` 形参（模板 lambda）替代。
- **转正**：`for_each/transform/copy` 的语义原样，但书写方式变成 ranges 管道；
  `reverse_iterator` 存活，`views::reverse` 更通用；插入迭代器存活（`std::back_inserter` 仍是标准答案）。
- **谱系迁移**：compose/bind 的函数式思想在 C++23 `ranges::zip`、C++20 投影（projection）
  （`ranges::sort(v, {}, &Widget::key)`——05 篇 `select1st` 萃取器的语言化）中延续。

## 四、内存工程：SGI 思想的三个现代传人（工业实践）

1. **线程本地档位缓存**：jemalloc tcache、mimalloc 的 bins——02 篇 free-list 数组的无锁化重做；
2. **生命周期整体释放**：`pmr::monotonic_buffer_resource`、每 arena 一请求的服务框架——「不还得碎片」哲学制度化；
3. **可观测 + 策略化**：分配计数器（本目录 🔧 t2 的 `counting_resource`）、
   `new_delete` 钩子（mimalloc 集成方式）——把 SGI 编译期选池变成运行期开关，这正是 pmr 的存在理由。

## 本目录实测附注（可复现清单，均在仓库外）

| 文件 | 内容 | 结果 | 标注 |
| --- | --- | --- | --- |
| t1.cpp | `allocate(n,hint)` 与 `construct` 在 gnu++17 vs gnu++23 | 17 编译过 / 23 两处编译错误（错误信息原文见 02 篇引文） | 已实测 g++ 15.2 |
| t2.cpp | pmr::vector 配 counting_resource（1000 push_back）；monotonic_buffer_resource 承接 100 个长 string；allocator 指针相等验证传播 | allocs=11, bytes=8188；单调缓冲内完成；propagation=true | 已实测 g++ 15.2 |
| t3.cpp | vector/deque 首末元素地址差；push_front 后地址稳定性 | 19996 vs 145708；稳定性=true | 已实测 g++ 15.2 |
| t4.cpp | `iterator_traits` 对裸指针/const 指针/自定义 forward 迭代器/vector 迭代器的抽取 + static_assert | 全部通过 | 已实测 g++ 15.2 |

## 链接的开源仓库与文献（写作时逐一可达性核实）

- SGI 源码：[karottc/sgi-stl](https://github.com/karottc/sgi-stl) ✅｜文档镜像：[justinmeiners/sgi-stl-docs](https://github.com/justinmeiners/sgi-stl-docs) ✅
- 配套解读：[SilverMaple/STLSourceCodeNote](https://github.com/SilverMaple/STLSourceCodeNote) ✅
- 现代实现：[gcc-mirror/gcc（libstdc++）](https://github.com/gcc-mirror/gcc) ✅｜[llvm/llvm-project（libc++）](https://github.com/llvm/llvm-project) ✅｜[microsoft/STL](https://github.com/microsoft/STL) ✅
- 哈希：[abseil/abseil-cpp](https://github.com/abseil/abseil-cpp) ✅｜[martinus/unordered_dense](https://github.com/martinus/unordered_dense) ✅（作者旧仓库 robin_hood 实测 404）｜[Tessil/robin-map](https://github.com/Tessil/robin-map) ✅
- 其他：[fmtlib/fmt](https://github.com/fmtlib/fmt) ✅｜[ericniebler/range-v3](https://github.com/ericniebler/range-v3)（ranges 前身，本目录内文引用）
- 提案：[P0522R0（2016）](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2016/p0522r0.html) ✅标题实测｜
  [P3310R5（2024）](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p3310r5.html) ✅正文实测（其 Introduction 载明 P0522R0「adopted into C++17」）｜
  P2875R4（C++26，标题经 cplusplus/papers 仓库检索核实 ✅，URL 未逐一直链）

## 与其他章的联系

- 全部「⚠️ 现代细节」的原文机制：[02-空间配置器.md](02-空间配置器.md)、[04-序列式容器.md](04-序列式容器.md)、[05-关联式容器.md](05-关联式容器.md)
- 适配器谱系的退役名单细节：[06-算法仿函数与配接器.md](06-算法仿函数与配接器.md)
- 版本史背景：[01-STL概论与版本简介.md](01-STL概论与版本简介.md)
- 用法手册：[../C++标准库.md](../C++标准库.md)；现代特性：[../C++17完全指南.md](../C++17完全指南.md)、[../C++20模板元编程.md](../C++20模板元编程.md)
- 语言演化史观：[../C++语言的设计与演化.md](../C++语言的设计与演化.md)
- 上游：[00-总览与阅读地图.md](00-总览与阅读地图.md)；单文件版 [../STL源码剖析.md](../STL源码剖析.md)、
  [../STL源码剖析简体中文完整版.md](../STL源码剖析简体中文完整版.md)；导航 [../C++系列·总索引.md](../C++系列·总索引.md)

## 一页带走

```text
分配：默认 new/delete；高频小对象 → pmr（synchronized_pool）或每请求单调缓冲；
      极端规模 → mimalloc/jemalloc 接管全局。别再造状态化 allocator 模板参数。
容器：vector 默认；两头 → deque；只读字典 → 排序 vector + binary_search；
      热哈希 → absl::flat_hash_map/unordered_dense；树只在你真需要有序遍历时用。
策略：lambda；管道 → std::ranges；证书 → 已死，约束(concepts)接班。
引用：借用给 string_view/span；所有权给 unique_ptr；共享最后才 shared_ptr；
      auto_ptr 的坟头草已经二十年了。
```
