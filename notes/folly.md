# folly
api doc

https://fossies.org/dox/folly-v2025.06.02.00/
https://fossies.org/dox/folly-v2025.06.02.00/classes.html
## code
https://github.com/edidada/testfollycmakevcpkg/

facebook开源库

facebook开源的基础库

folly不支持32bit？

Vcpkg install folly 需要

python3

https://www.cnblogs.com/iam-ironman/articles/10969663.html

## clh队列

Hazard Pointer（风险指针）是一种用于无锁（lock-free）并发数据结构的安全内存回收机制。

它解决的核心问题是：当一个线程正在读取某个对象，而另一个线程准备删除并回收该对象的内存时，如何确保正在被读取的对象不会被提前释放（use-after-free）。

### 核心思想：先“声明”，再访问
Hazard Pointer 的规则非常直观：访问者必须先把要使用的指针“公布”出去，回收者看到有人在使用，就不能回收。

关键规则是：一个已退休（retired）的对象，只有在确定“从它被标记退休之前的那一刻起，没有任何风险指针指向它”之后，才能被回收。

###  基本工作机制
它通过“保护”与“延迟回收”的配合来工作：

1.  保护（Protection）：线程要访问某个对象前，先设置一个属于自己的 Hazard Pointer，让它指向该对象的地址。这相当于向其他线程声明：“我正在用这个对象，别删。”
2.  退休（Retire）：当线程从数据结构中移除一个对象后，它不直接 `delete`，而是调用 `retire()` 把回收责任交给 Hazard Pointer 库。
3.  延迟回收（Deferred Reclamation）：库会在合适的时机进行扫描。它读取所有线程的 Hazard Pointer，把已退休对象与这些指针逐一比对：
    *   如果某个已退休对象没有被任何 Hazard Pointer 指向，就安全地回收它。
    *   如果有 Hazard Pointer 指向它，就把它放回待回收队列，等下次扫描。

### 主要特点
*   优点：内存占用有界（不像 RCU 那样无界增长）；读取线程之间无干扰，读操作可扩展性好；适用于需要非阻塞（lock-free）的场景。
*   代价：每次访问需要写一个内存屏障（memory fence），这会带来一定的开销。

###  在 C++ 中的现状
Hazard Pointer 已被纳入 C++26 标准（P2530R3）。标准接口大致包括：
*   `hazard_pointer`：管理风险指针的对象。
*   `hazard_pointer_obj_base<T>`：需要被保护的对象应继承的基类，提供 `retire()` 方法。
*   `make_hazard_pointer()`：创建一个非空的 `hazard_pointer`。

### Folly 中的实现
你之前接触过 Folly，它正是 Hazard Pointer 在生产环境中的重要实现者和推动者。Folly 从 2017 年左右就开始在内部大量使用相关设施，并贡献了“对象群组（Object Cohorts）”、“批量风险指针（hazptr_array）”等扩展，这些经验也影响了 C++ 标准的制定。

如果你在看 Folly 的源码，`folly/synchronization/Hazptr.h` 是入口，里面会看到 `hazptr_holder`、`hazptr_obj_base`、`hazptr_array` 等组件。
你总结的这两点，核心是抓住了 Folly 与 libcds/JUC 在并发原语设计哲学上的根本差异：Folly 倾向于把控制权显式交给开发者，用命名和接口强制你做出选择；而后者往往内置一套“默认行为”，把复杂性藏在背后。

### 阻塞 vs 自旋：命名即契约

Folly 的 `read()` 确实是非阻塞的，空队直接返回 `false`。只有 `blockingRead()` 才会挂起线程等待元素。这种命名是刻意的设计选择：把“是否阻塞”这个关键决策暴露在调用处，让你无法无意中写出“以为在读、实际在等”的代码。

你提到的实测踩坑非常典型：用 `read()` 当阻塞版，consumer 空队立刻退出，自然只能读到前 2080 个。这不是 Folly 的 bug，而是接口设计在逼你明确意图——要阻塞就用 `blockingRead()`，要非阻塞轮询就用 `read()`，不要指望一个函数兼顾两种语义。

相比之下，libcds 的队列在空时默认自旋 + backoff，JUC 的 `ConcurrentLinkedQueue` 的 `poll()` 也是立即返回 `null`。三者的默认行为不同，压测数据确实不能直接横向对比，因为“空队列时发生了什么”这件事本身就不一样。

### 容量语义：预分配换锁自由

Folly 的 `AtomicHashMap` 要求预分配容量，文档写得很直白：如果你不知道大概会插入多少元素，“you probably shouldn't use this class”。它用固定大小的 slab 拼接来实现增长，每个 slab 本身大小固定，`find` 和迭代是无等待的，但增长意味着后续查找要串行探测多个 submap，性能会下降。

`ConcurrentSkipList` 同样对内存布局有精细控制（如 arena allocator、节点高度分布），本质上是用确定的内存结构换取读路径的锁自由。

而 JUC 的 `ConcurrentLinkedQueue` 是无界的，容量只受内存限制；libcds 的队列通常也不强求预分配。它们的“自由”来自动态节点分配，代价是每个节点一次分配、缓存局部性更差。

一句话总结：Folly 用“预分配 + 命名区分阻塞/非阻塞”把并发控制的决策权交给你，代价是你要自己承担选错的后果；libcds/JUC 用“动态增长 + 默认自旋”减少你的决策负担，代价是性能特征更隐晦、压测时容易被表面数据误导。