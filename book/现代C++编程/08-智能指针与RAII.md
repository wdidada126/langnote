# 08 智能指针与 RAII（原书第 11 章）

> 覆盖：**第 11 章 智能指针**（11.1 概述 / 11.2 所有权 / 11.3 作用域指针 / 11.4 独占指针 / 11.5 共享指针 / 11.6 弱指针 / 11.7 侵入式指针 / 11.8 可用的智能指针总结 / 11.9 分配器）。
> 返回：[目录](00-总览与阅读地图.md)｜[单文件原笔记](../现代C++编程.md)｜[C++ 系列·总索引](../C++系列·总索引.md)

## 核心概念速览（中英对照）

- **所有权** — ownership：谁负责释放、何时释放的**唯一记录**——本章把口头约定升级为类型
- **独占指针** — `std::unique_ptr`：移动 only、零额外存储（默认删除器下 sizeof==裸指针）、可定制删除器
- **共享指针** — `std::shared_ptr`：控制块（引用计数+弱计数+删除器+allocator）+ 双计数模型，拷贝是原子加
- **`make_shared` 的合块** — single allocation：对象与控制块同次分配；代价：对象内存延活至弱引用清零
- **别名共享** — aliasing constructor：`shared_ptr<T>` 指向 `U` 的成员而共享 `U` 的生命——容器持有一体
- **弱指针** — `std::weak_ptr`：不保命的观察者；`lock()`/`expired()`（C++20 `std::atomic<std::weak_ptr>` 前它连原子读写都没有）
- **循环引用** — reference cycle：shared 互锁致泄漏，weak 破环；观察者缓存/父指针是标准案发现场
- **侵入式引用计数** — intrusive refcounting：计数住在对象里（`enable_shared_from_this` 是其标准形态），少一次分配、多一处纪律
- **作用域指针/守卫** — scope guard：`boost::scope`/`std::experimental::scope_exit` 谱系——「出作用域跑一个动作」而不夺所有权
- **定制删除器** — custom deleter：`unique_ptr<FILE, int(*)(FILE*)>` 式把 free/close/munmap 接入同一 RAII 语法
- **分配器** — allocator：`shared_ptr` 的 allocator 形参与 `scoped_allocator` 构造（11.9），容器章（`09`）回收
- **RAII** — Resource Acquisition Is Initialization：本章 umbrella 概念——资源即对象，析构即撤销，块尾即兑现点（`05` 章语句作用域的兑现方）
- **借用** — borrow：以 `T*`/`T&`/`span`/`string_view` 传「用而不有」，拥有者活在别处——三动词（拥有/移交/借用）里的第三极
- **`enable_shared_from_this`** — 混入基类：对象内部安全再造共享指针的官方通道，前提「已入 shared 之手」，否则 `bad_weak_ptr` 或 UB
- **控制块双计数** — strong/weak count：强计数保对象、弱计数保控制块；`make_shared` 合块让「弱计数续命」直接吊住对象内存——两条账合并读

## 1. 动机：把「谁 delete」从注释写进类型

第 4 章的 SimpleString 演示了手写五法则的痛；第 11 章给出标准库答案：**用类型表达所有权，让析构成为编译器兜底**。原书 11.2 的所有权定义是全书最干净的三句：①单一所有者→`unique_ptr`；②共享所有权→`shared_ptr`；③借用→裸指针/引用/视图（不可空优先引用，`02` 章表回看）。11.3–11.7 按「守卫→独占→共享→观测→侵入」递进，每种指针都交代控制块、拷贝语义、异常路径三张账。

## 2. 机制：三种指针的内部账单

**`unique_ptr` 是「带模板参数的结构体」**：`unique_ptr<T, D>` 默认 D=delete 时经空基优化不占空间；`operator bool/reset/release/get` 五个动词覆盖 99% 用法。`release()` 是**所有权移交给人肉**的危险出口——本章判词：出现 release 的评审要看接盘方。工厂返回 `unique_ptr` 的异常安全论证（new 中途抛出、裸指针入参被别的分配吃掉）是 C++98→11 最经典的一页，`make_unique`（C++14）把论证折叠进一个函数。

**`shared_ptr` 的核心是控制块**：强计数=对象活；弱计数=控制块活。拷贝/析构的计数增减是**原子**操作（默认 `atomic` 策略，`__gthread_single` 单线程可全退化为非原子）；解引用与读写计数无关——线程安全只到「指针本身」，**不到所指对象**（11.8 总结表的头条警告）。`enable_shared_from_this` 让对象内部合法再造 `shared_ptr`——前提是被 shared 持有，否则 UB（其修复线 [P0497R0](https://wg21.link/p0497)「correct support for operator->」是语言细节，本会话未核 ⚠️ 不展开）。

**`weak_ptr` 的 `lock()` 是 check-then-act 的原子化**：`expired()` 后 `lock()` 仍可能空——两次调用间的竞争窗口是教学必点。缓存（对象池、观察者列表）是 weak 的主场：shared 持缓存本体、weak 挂回调。

**侵入式指针（11.7）**：`boost::intrusive_ptr` 把计数放进对象（`add_ref/release_ref` 钩子），零控制块分配、`shared_from_this` 免前置构造——代价是对象类型被计数协议污染。判据：高频小对象+循环引用少+性能敏感。

**分配器（11.9）**：`shared_ptr` 接受自定义 allocator（内存池/共享堆）；与容器 allocator 的关系是「控制块用谁的分配器」——`allocate_shared` 的答案统一而优雅。现代语境该节让位给 PMR（`09` 章 `polymorphic_allocator` 一线）。

## 3. 权衡：计数、循环与视图

- **shared 是设计妥协不是默认**：出现 `shared_ptr` 集合即「所有权分散」信号——能 `unique` 进工厂、引用传借用就不要 shared；shared 的内存延迟释放（合块+弱计数续命）在数组场景尤其反直觉。
- **`shared_ptr` vs 视图链**：C++20 `std::span`（`01`/`09`）把「只读共享一段内存」从 `shared_ptr<vector>` 手里接走——借用+拥有者分离比「人人有份」更安全。
- **删除器的类型代价**：`unique_ptr<T, std::function<void(T*)>>` 让类型变肥（lambda 删除器需 `function` 擦除）——函数指针/无捕获 lambda/结构体删除器三档成本要算。

## 4. 相邻概念对比

| 概念 A | 概念 B | 分界线 |
| --- | --- | --- |
| `unique_ptr` | 栈对象+RAII | 可移动入容器/延迟构造需要堆时前者胜；否则栈对象零成本 |
| `shared_ptr` | `refcounted` 侵入式 | 控制块外置 vs 内置：通用性 vs 分配数 |
| `weak_ptr::lock()` | 裸指针观察者 | lock 是原子「安全醒来」；裸指针只在不保命且生命周期有外部证明时合法 |
| `auto_ptr`（已故） | `unique_ptr` | 拷贝即偷偷转走（UB 温床），C++11 弃用、C++17 移除 |
| scope guard | 只析构不释放的 unique | guard 跑任意 lambda；析构语义不可定制 |

## 典型误区与修正视角

| 误区 | 症状 | 修正视角 |
| --- | --- | --- |
| 「`shared_ptr` 是安全默认值」 | 满屏 shared，析构顺序玄学 | 默认是**栈对象**，需要堆上唯一所有权才 `unique_ptr`；shared 出现即「所有权分散」信号，先审计能否降级 |
| 「`shared_ptr` 线程安全」 | 多线程改同一元素不挂锁 | 原子性只覆盖**计数与指针本体**；所指对象的读写照常竞争（11.8 总结表头条）；跨线程换指针用 C++20 `atomic<shared_ptr>` |
| 「`make_shared` 永远优于 new」 | 大对象+长弱引用场景内存爆 | 合块使对象内存吊到弱计数清零；对象巨大/weak 长寿时，分开分配反而是逃生门 |
| 「`reset(新指针)` 等价先 release 再 reset」 | 中间态异常资源丢失 | `reset` 自带「先接新再析旧」的安全序；手写 release 链是本章 🔧 之后最常见的回退事故 |
| 「循环引用只在教科书里」 | 观察者列表/父子双向静默泄漏 | parent 用 `weak_ptr`、observer 表存 weak 是两大标准解；析构没跑=先去画所有权图 |
| 「删除器随便用 lambda 塞」 | `unique_ptr` 类型变胖、进不了结构体 | 无捕获 lambda/函数指针/空态 functor 三档成本；要存进固定布局（如共享内存）先算 `sizeof` |
| 「`unique_ptr` 作参数是过防御」 | 明明只借用也收 `unique_ptr` | 按值收 `unique_ptr`=「我接管」；`const unique_ptr&`=「我旁观」；`T*`/`T&`/`T&&`(引用,非右值引用)=「我借用」——签名即合同（EMC++ Item 32 口径） |
| 「scope guard 是语言设施」 | 到处找 `std::scope_exit` | 它仍在 TS/Boost 线（`boost::scope`）⚠️ 未进 ISO 标准；C++ 本体近似物是「析构跑 lambda 的小 RAII 类型」，一行可手写 |

## 练习检查点（对应原书「练习/拓展阅读」栏）

- 11.2：把第 4 章 SimpleString 的裸 `char*` 成员改写成「`unique_ptr<char[]>` + 视图 `string_view` 访问器」，五法则应自动退化到只剩移动两行。
- 11.4：给 `unique_ptr<FILE, decltype(&fclose)>` 写工厂 `open_text(path)`，返回后在调用点用 `if (!f) ...` 验证删除器接住了空指针分支。
- 11.5：`make_shared` 与 `shared_ptr(new T)` 两版各测 `sizeof` 之外的分配次数（配 `-fsanitize=address` 的 alloc 统计或计数 allocator），复述合块省了什么、又欠了什么。
- 11.6：手写「parent↔child 双指针」泄漏标本：不加 weak 时 ASan 报 leak，child 侧改 `weak_ptr` 后清零——循环引用的肉眼确诊流程。
- 11.7：给一个带 `int refs` 成员的对象接 `boost::intrusive_ptr`（或手写 20 行等价物），对比 `shared_ptr` 版少了哪次分配、多了哪条纪律。
- 11.8：执行「shared 审计」：项目/本仓库任意代码里把每个 `shared_ptr` 标注三分类（真共享/可降 unique/应改 weak），交三行统计——这比任何新语法都更接近本章本意。
- 11.9：用 `pmr::unsynchronized_pool_resource` + `allocate_shared` 造一个 1 万次小对象的基准场景，感受「控制块用谁的分配器」在池下的收益。

## 章节依赖图

- 上游：`02` 章移动语义/五法则是三种指针差异的语法根；`03` 章多态使控制块里的删除器可以类型擦除；`05` 章块作用域是 RAII 的兑现地址。
- 平行：`07` 章替身所有权直接用本章三选一模板；`06` 章删除器/比较器是本章的类型参数客户。
- 下游：`09` 章容器持针策略（vector\<unique_ptr\> vs vector\<T\>）与 PMR 接棒 11.9；`13` 章异步处理器捕获 `shared_ptr`/`enable_shared_from_this` 的「活到回调跑完」协议；`14` 章资源句柄（文件/套接字）全线 RAII 化。
- 概念闭环：`01` 章「不要裸 new」的口号在本章拿到类型证明，在 `09` 章拿到容器版本。

## 🔧 实测对照：所有权移交 + `span` 视图 + `weak_ptr` 观测（已实测 g++ 15.2）

```cpp
#include <memory>
#include <span>
#include <cstdio>
void fill(std::span<int> s) { for (auto& x : s) x *= 2; } // 借用：不拥有、不计数
int main() {
    auto arr = std::make_unique<int[]>(4);                 // 唯一所有权在智能指针（C++14 数组工厂）
    for (int i = 0; i < 4; ++i) arr[i] = i + 1;
    fill(std::span<int>(arr.get(), 4));
    std::printf("%d %d\n", arr[0], arr[3]);
    std::shared_ptr<int> owner = std::make_shared<int>(9); // make_shared 合块（C++11）
    std::weak_ptr<int> w = owner;
    owner.reset();
    std::printf("expired=%d\n", (int)w.expired());
}
```

- `-std=gnu++20` 真实输出：`2 8` / `expired=1`。
- 三行账：`span<int>(arr.get(), 4)` 证明「借用视图」不需要第二套所有权；`owner.reset()` 后 `weak` 的 `expired` 为真，而若此处误用裸 `int*` 观察者，读到的是悬垂——这就是 11.6 弱指针存在性的 15 行证明。
- `std::span` 提案 [P0122R7](https://wg21.link/p0122) 本会话实测可达（同库笔记已核标题 "span: bounds-safe views" 系）。

## 最新演进与工业实践

- **C++20/23 对位**：`std::atomic<std::shared_ptr>`/`atomic<unique_ptr>`（C++20，等待/通知同步库 [P1135R6](https://wg21.link/p1135) 同代，实测可达）——多线程共享指针不再靠锁包指针；`std::make_shared<T[]>(n)`（C++20 数组支持）；C++23 `<functional>` 侧 `std::move_only_function` 可持 `unique_ptr` 捕获做「一次性回调」。
- **分配器叙事的接棒者**：`std::pmr`（C++17，`polymorphic_allocator` + `memory_resource`）把「运行时选分配策略」从模板参数移进对象——11.9 的教学在工业界的现代落点；[`abseil/abseil-cpp`](https://github.com/abseil/abseil-cpp) 的 allocator 约定与之相互印证。
- **工业仓库**：[`microsoft/GSL`](https://github.com/microsoft/GSL)（`not_null`、`owner` 概念词表把本章纪律机器可读化，配合 Core Guidelines 的 `[Bounds]` profile）；[`facebook/folly`](https://github.com/facebook/folly) 的 `fbgemm:: IntrusivePtr` 谱系为 11.7 的工业续命。
- **练习/拓展接点**：11.x 练习在 2026 年加一问：把你项目里每个 `shared_ptr<T>` 标成三种之一（真共享/其实可以 unique/应该改 weak），只统计第二三类——所有权审计的入口动作即此。

## 与其他书的联系

- 手写智能指针的「解药配伍」对照：[`../现代C++实战30讲/02-自己动手实现智能指针.md`](../现代C++实战30讲/02-自己动手实现智能指针.md)（与 `02` 章 SimpleString/本章 SimpleUniquePointer 三足互链）。
- 条目化军规：[`../Effective_Modern_C++/04-智能指针.md`](../Effective_Modern_C++/04-智能指针.md)（Item 18–22 正是本章的「该用哪个」判例集）。
- 库内实现视角（控制块在 libstdc++/MSVC STL 源码里长什么样）：[`../C++标准库/02-通用工具与智能指针.md`](../C++标准库/02-通用工具与智能指针.md)；习题实现线：[`../cppprime/09-动态内存.md`](../cppprime/09-动态内存.md)、[`../cppprime/10-拷贝控制.md`](../cppprime/10-拷贝控制.md)。
- 下一站：`09-工具库与容器.md`；回到 [目录](00-总览与阅读地图.md)。
- 向上：[单文件原笔记](../现代C++编程.md)｜[C++ 系列·总索引](../C++系列·总索引.md)。
