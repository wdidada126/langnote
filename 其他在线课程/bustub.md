# bustub

CMU 15-445/645 (Database Systems) 课程使用的实验框架 BusTub 在 2020 年至 2026 年间经历了从 单机单线程 到 现代并发架构 的重大重构。以下是核心变更列表：

1. 核心架构与编程范式变更 (2023-2024)
这是近年来最重大的底层重构，旨在提升并发性能和代码健壮性。
变更维度 2020-2022 (旧版) 2023-2026 (新版) 变更说明
并发模型 单线程 或 粗粒度锁 多线程 + 细粒度锁 引入 PageGuard 机制，实现页级锁管理，支持高并发访问 。
内存管理 手动管理 Page 指针 RAII (资源获取即初始化) 引入 ReadPageGuard 和 WritePageGuard，利用 C++ 智能指针自动管理页的生命周期，防止内存泄漏 。
磁盘调度 同步 I/O 异步 I/O (Disk Scheduler) 新增 DiskScheduler 组件，将磁盘读写请求放入队列异步处理，提升吞吐量 。

2. 实验方案与算法升级 (2020-2026)

实验内容从基础实现向工业级标准演进。
实验项目 2020-2022 (旧版) 2023-2026 (新版) 变更说明
Project 0 C++ Primer (基础语法) Trie (字典树) 从简单的语法练习升级为数据结构实现，强调 Modern C++ 特性 。
Project 1 (Buffer Pool) LRU 替换策略 LRU-K 替换策略 算法升级，通过记录最近 K 次访问历史来更精准地预测未来访问模式，解决缓存污染问题 。
Project 2 (Index) 可扩展哈希表 (Extendible Hash) 并发 B+ 树 索引结构从哈希表变更为更实用的 B+ 树，并支持并发操作（蟹行协议）。
Project 3 (Query Execution) 火山模型执行器 火山模型 + 优化器规则 新增对 Sort、Limit 算子的实现，并引入 Top-N 优化等规则 。
Project 4 (Concurrency Control) 2PL 锁管理器 2PL + 死锁检测 新增后台死锁检测线程，支持 READ_UNCOMMITTED、READ_COMMITTED、REPEATABLE_READ 隔离级别 。

3. 新增功能与组件 (2024-2026)
•   异步磁盘调度器 (Disk Scheduler)：在 Project 1 中新增，负责管理磁盘 I/O 请求队列，支持并行读写 。
•   PageGuard 机制：贯穿所有项目，用于管理页的锁和引用计数，是并发控制的核心 。

总结
如果你在 2026 年学习该课程，你将面对一个完全支持并发、使用现代 C++ RAII 范式、具备异步 I/O 能力的数据库内核。相比 2020 年的版本，代码复杂度和工程实践性显著提升。

你提到的“火山模型 + 优化器规则”是数据库查询执行引擎的核心架构。下面为你详细解释这些概念：

1. 火山模型 (Volcano Model)

火山模型是数据库领域最经典的查询执行模型，也称为迭代器模型 (Iterator Model)。

•   核心思想：将查询计划组织成一棵树，每个节点（算子）都实现相同的接口（Init() 和 Next()）。
•   工作方式：
    ◦   拉取式 (Pull-based)：执行从根节点（通常是输出节点）开始，它调用子节点的 Next() 方法获取数据，子节点再调用其子节点的 Next()，如此递归向下。
    ◦   流水线 (Pipeline)：数据像流水一样从叶子节点（如扫描节点）流向根节点，中间不需要物化（Materialize）整个结果集，内存占用小。
•   优点：实现简单，逻辑清晰，易于扩展新算子。
•   缺点：由于每个元组（Tuple）都要经过多次函数调用（Next()），函数调用开销大，在现代 CPU 架构下性能较差（对比向量化模型）。

2. 优化器规则 (Optimizer Rules)

优化器规则是数据库查询优化器（Optimizer）用来重写查询计划（Query Plan）的启发式规则。
•   目的：将用户输入的 SQL 语句（或逻辑计划）转换成执行效率更高的物理计划。
•   工作方式：优化器遍历查询计划树，当发现某个子树符合特定模式时，就应用规则将其替换为更优的结构。

•   常见规则：
    ◦   谓词下推 (Predicate Pushdown)：将过滤条件（WHERE）尽可能下推到靠近数据源的地方，减少后续算子处理的数据量。
    ◦   列裁剪 (Projection Pushdown)：只读取查询中需要的列，减少 I/O 开销。
    ◦   常量折叠 (Constant Folding)：在编译时计算常量表达式，避免运行时重复计算。

3. 算子实现：Sort 与 Limit

在火山模型中，Sort 和 Limit 是两个常见的算子：
•   Sort 算子：
    ◦   功能：对输入的数据进行排序。
    ◦   实现：由于火山模型是流式处理，Sort 算子通常需要阻塞。它必须调用子节点获取所有数据，在内存中排序完成后，才能通过 Next() 输出第一个结果。

•   Limit 算子：
    ◦   功能：限制输出的元组数量。
    ◦   实现：通常是非阻塞的。它从子节点拉取数据，计数达到指定数量后，后续的 Next() 调用直接返回空。

4. Top-N 优化 (Top-N Optimization)

这是你提到的“优化器规则”中的一个典型例子，它结合了 Sort 和 Limit 的特性。
•   问题：如果查询是 SELECT ... ORDER BY ... LIMIT N，按照常规执行，Sort 算子需要先对所有数据进行排序（可能涉及磁盘外排，非常耗时），然后 Limit 只取前 N 个。
•   优化规则：将 Sort 和 Limit 合并为一个 Top-N 算子。
•   原理：Top-N 算子只需要维护一个大小为 N 的堆（Heap）。它扫描数据时，只保留当前最大的 N 个元素，无需对整个数据集排序。这大大减少了内存使用和计算量。

总结
在 BusTub 的实验中，你不仅需要实现火山模型的执行框架（Next() 接口），还需要实现具体的算子（如 Sort、Limit），并利用优化器规则（如 Top-N 优化）来提升查询性能。

火山模型（Volcano Model）和向量化模型（Vectorized Model）是现代数据库查询执行引擎的两种核心架构。它们的主要区别在于数据处理的粒度和执行方式。

核心差异对比

维度 火山模型 (Volcano Model) 向量化模型 (Vectorized Model)

数据粒度 一次处理一行 (Row-at-a-time) 一次处理一批 (Batch-at-a-time)

执行方式 拉取式 (Pull-based) 推式 (Push-based) 或 拉取式

函数调用 高频率（每行调用一次） 低频率（每批调用一次）

CPU 效率 低（指令缓存不友好） 高（利于 SIMD 指令优化）

内存局部性 差 好

实现复杂度 简单 复杂

1. 火山模型 (Volcano Model)
火山模型是数据库领域的“经典款”，其核心思想是迭代器模式。
•   工作方式：查询计划被组织成一棵树，每个节点（算子）都实现相同的接口（Init() 和 Next()）。执行从根节点开始，它调用子节点的 Next() 方法获取下一行数据，子节点再调用其子节点的 Next()，如此递归向下。

•   特点：
    ◦   拉取式 (Pull-based)：数据像火山喷发一样，从底层（叶子节点）被“拉”到顶层（根节点）。
    ◦   行处理：每次 Next() 调用只返回一行数据。这意味着处理 1000 行数据需要调用 1000 次 Next() 函数。

•   优点：实现简单，逻辑清晰，易于扩展新算子。
•   缺点：函数调用开销巨大。现代 CPU 的指令流水线（Pipeline）和分支预测（Branch Prediction）很难优化这种高频次的虚函数调用，导致 CPU 效率低下。

2. 向量化模型 (Vectorized Model)

向量化模型是数据库领域的“性能优化款”，旨在解决火山模型的 CPU 效率瓶颈。

•   工作方式：算子不再一次处理一行，而是一次处理一批数据（Batch）。每个算子实现 GetNextBatch() 方法，返回一个包含多行数据的向量（Vector）。

•   特点：
    ◦   批处理：数据以列（Column）或行（Row）的批次形式在算子间流动。
    ◦   向量化执行：由于处理的是连续的内存块，数据库可以利用现代 CPU 的 SIMD（单指令多数据） 指令集，在一个时钟周期内处理多个数据，极大提升计算密集型操作（如过滤、聚合）的速度。

•   优点：
    ◦   CPU 友好：大幅减少了函数调用次数，缓解了分支预测失败和缓存未命中的问题。
    ◦   利于编译优化：编译器更容易对处理整批数据的循环进行优化。

•   缺点：实现复杂，需要管理批次大小（Batch Size），且对于某些算子（如嵌套循环连接），批处理可能不如行处理灵活。

3. 总结
•   火山模型 胜在简单通用，适合教学和通用型数据库（如 SQLite、早期 MySQL）。
•   向量化模型 胜在极致性能，适合分析型数据库（OLAP），如 ClickHouse、Snowflake、DuckDB 等。

在 BusTub 课程中，你实现的是火山模型，因为它能让你最直观地理解查询执行的树状结构和数据流动。而在工业界的现代分析数据库中，向量化模型已成为主流。

## B+树可视化
b_plus_tree_printer

## doc
bustub vs huadb
Rust版本
https://github.com/systemxlabs/bustubx

2021年的代码
https://github.com/cdes5804/CMU-15-445-Database-Systems-2021


由于Bustub是在C++17下实现的数据库，因此所有学生都需要在正式开始之前，完成Project #0来检测对C++，尤其是C++现代语法的熟悉程度。
https://15445.courses.cs.cmu.edu/spring2023/

https://15445.courses.cs.cmu.edu/spring2023/schedule.html

Assignment	Solution	Release Date	Due Date
C++ Primer	N/A	Jan 17, 2023	Jan 29, 2023 @ 11:59pm
Buffer Pool Manager	N/A	Jan 30, 2023	Feb 19, 2023 @ 11:59pm
B+Tree Index	N/A	Feb 20, 2023	Mar 22, 2023 @ 11:59pm
Query Execution	N/A	Mar 22, 2023	Apr 09, 2023 @ 11:59pm
Concurrency Control	N/A	Apr 10, 2023	Apr 28, 2023 @ 11:59pm

https://15445.courses.cs.cmu.edu/spring2024/

discuss区域
https://discord.com/channels/724929902075445281/801327143485308949

github repo
https://gitee.com/edidada/bustub
https://github.com/cmu-db/bustub
c++的

编译
Linux
mac

bustdb需要clang14
https://apt.llvm.org/

lsb_release -a

wget -O - https://apt.llvm.org/llvm-snapshot.gpg.key | sudo apt-key add -

sudo vim /etc/apt/sources.list

deb http://apt.llvm.org/focal/ llvm-toolchain-focal-14 main
deb-src http://apt.llvm.org/focal/ llvm-toolchain-focal-14 main

# Linux
sudo build_support/packages.sh

```shell
mkdir build
cd build
cmake ..
make
```

```shell
[100%] Building CXX object tools/htable_bench/CMakeFiles/htable-bench.dir/htable_bench.cpp.o
[100%] Linking CXX executable ../../bin/bustub-bpm-bench
[100%] Built target bpm-bench
[100%] Built target terrier-bench
[100%] Built target sqllogictest
[100%] Linking CXX executable ../../bin/bustub-htable-bench
[100%] Linking CXX executable ../../bin/bustub-btree-bench
[100%] Built target htable-bench
[100%] Built target btree-bench
@edidada ➜ /workspaces/cmu-database-system-lab/bustub-public/build (6327570) $ sudo make install
[  1%] Built target bustub_murmur3
[  8%] Built target duckdb_pg_query
[ 10%] Built target gtest
[ 10%] Built target gmock
[ 11%] Built target gmock_main
[ 11%] Built target gtest_main
[ 13%] Built target fmt
[ 15%] Built target bustub_linenoise
[ 16%] Built target fort
[ 18%] Built target utf8proc
[ 20%] Built target backward
[ 20%] Built target backward_object
[ 26%] Built target bustub_optimizer
[ 33%] Built target bustub_binder
[ 36%] Built target bustub_statement
[ 40%] Built target bustub_buffer
[ 41%] Built target bustub_catalog
[ 43%] Built target bustub_common
[ 45%] Built target bustub_concurrency
[ 46%] Built target bustub_container_disk_hash
[ 61%] Built target bustub_execution
[ 63%] Built target bustub_recovery
[ 65%] Built target bustub_storage_disk
[ 68%] Built target bustub_storage_index
[ 76%] Built target bustub_storage_page
[ 78%] Built target bustub_storage_table
[ 85%] Built target bustub_type
[ 91%] Built target bustub_planner
[ 91%] Built target bustub_primer
[ 91%] Built target bustub
[ 91%] Built target shell
[ 91%] Built target nc-shell
[ 93%] Built target sqllogictest
[ 95%] Built target b_plus_tree_printer
[ 96%] Built target terrier-bench
[ 98%] Built target bpm-bench
[100%] Built target btree-bench
[100%] Built target htable-bench
Install the project...
-- Install configuration: "Debug"
-- Up-to-date: /usr/local/include
-- Installing: /usr/local/include/gmock
-- Installing: /usr/local/include/gmock/gmock-function-mocker.h
-- Installing: /usr/local/include/gmock/gmock-more-matchers.h
-- Installing: /usr/local/include/gmock/gmock-actions.h
-- Installing: /usr/local/include/gmock/gmock-more-actions.h
-- Installing: /usr/local/include/gmock/internal
-- Installing: /usr/local/include/gmock/internal/gmock-internal-utils.h
-- Installing: /usr/local/include/gmock/internal/gmock-pp.h
-- Installing: /usr/local/include/gmock/internal/custom
-- Installing: /usr/local/include/gmock/internal/custom/gmock-generated-actions.h
-- Installing: /usr/local/include/gmock/internal/custom/gmock-matchers.h
-- Installing: /usr/local/include/gmock/internal/custom/README.md
-- Installing: /usr/local/include/gmock/internal/custom/gmock-port.h
-- Installing: /usr/local/include/gmock/internal/gmock-port.h
-- Installing: /usr/local/include/gmock/gmock-nice-strict.h
-- Installing: /usr/local/include/gmock/gmock.h
-- Installing: /usr/local/include/gmock/gmock-matchers.h
-- Installing: /usr/local/include/gmock/gmock-spec-builders.h
-- Installing: /usr/local/include/gmock/gmock-cardinalities.h
-- Installing: /usr/local/lib/libgmock.a
-- Installing: /usr/local/lib/libgmock_main.a
-- Installing: /usr/local/lib/pkgconfig/gmock.pc
-- Installing: /usr/local/lib/pkgconfig/gmock_main.pc
-- Installing: /usr/local/lib/cmake/GTest/GTestTargets.cmake
-- Installing: /usr/local/lib/cmake/GTest/GTestTargets-debug.cmake
-- Installing: /usr/local/lib/cmake/GTest/GTestConfigVersion.cmake
-- Installing: /usr/local/lib/cmake/GTest/GTestConfig.cmake
-- Up-to-date: /usr/local/include
-- Installing: /usr/local/include/gtest
-- Installing: /usr/local/include/gtest/gtest_prod.h
-- Installing: /usr/local/include/gtest/gtest-spi.h
-- Installing: /usr/local/include/gtest/gtest-printers.h
-- Installing: /usr/local/include/gtest/internal
-- Installing: /usr/local/include/gtest/internal/gtest-string.h
-- Installing: /usr/local/include/gtest/internal/gtest-param-util.h
-- Installing: /usr/local/include/gtest/internal/gtest-internal.h
-- Installing: /usr/local/include/gtest/internal/gtest-port.h
-- Installing: /usr/local/include/gtest/internal/gtest-death-test-internal.h
-- Installing: /usr/local/include/gtest/internal/gtest-type-util.h
-- Installing: /usr/local/include/gtest/internal/custom
-- Installing: /usr/local/include/gtest/internal/custom/gtest-printers.h
-- Installing: /usr/local/include/gtest/internal/custom/gtest-port.h
-- Installing: /usr/local/include/gtest/internal/custom/README.md
-- Installing: /usr/local/include/gtest/internal/custom/gtest.h
-- Installing: /usr/local/include/gtest/internal/gtest-port-arch.h
-- Installing: /usr/local/include/gtest/internal/gtest-filepath.h
-- Installing: /usr/local/include/gtest/gtest-message.h
-- Installing: /usr/local/include/gtest/gtest-typed-test.h
-- Installing: /usr/local/include/gtest/gtest-test-part.h
-- Installing: /usr/local/include/gtest/gtest_pred_impl.h
-- Installing: /usr/local/include/gtest/gtest-param-test.h
-- Installing: /usr/local/include/gtest/gtest-death-test.h
-- Installing: /usr/local/include/gtest/gtest-assertion-result.h
-- Installing: /usr/local/include/gtest/gtest-matchers.h
-- Installing: /usr/local/include/gtest/gtest.h
-- Installing: /usr/local/lib/libgtest.a
-- Installing: /usr/local/lib/libgtest_main.a
-- Installing: /usr/local/lib/pkgconfig/gtest.pc
-- Installing: /usr/local/lib/pkgconfig/gtest_main.pc
-- Installing: /usr/local/lib/libfmtd.a
-- Installing: /usr/local/include/fmt/args.h
-- Installing: /usr/local/include/fmt/chrono.h
-- Installing: /usr/local/include/fmt/color.h
-- Installing: /usr/local/include/fmt/compile.h
-- Installing: /usr/local/include/fmt/core.h
-- Installing: /usr/local/include/fmt/format.h
-- Installing: /usr/local/include/fmt/format-inl.h
-- Installing: /usr/local/include/fmt/os.h
-- Installing: /usr/local/include/fmt/ostream.h
-- Installing: /usr/local/include/fmt/printf.h
-- Installing: /usr/local/include/fmt/ranges.h
-- Installing: /usr/local/include/fmt/std.h
-- Installing: /usr/local/include/fmt/xchar.h
-- Installing: /usr/local/lib/cmake/fmt/fmt-config.cmake
-- Installing: /usr/local/lib/cmake/fmt/fmt-config-version.cmake
-- Installing: /usr/local/lib/cmake/fmt/fmt-targets.cmake
-- Installing: /usr/local/lib/cmake/fmt/fmt-targets-debug.cmake
-- Installing: /usr/local/lib/pkgconfig/fmt.pc
-- Installing: /usr/local/lib/libfort.a
-- Installing: /usr/local/include/fort.h
-- Installing: /usr/local/include/fort.hpp
-- Installing: /usr/local/lib/pkgconfig/libfort.pc
-- Installing: /usr/local/lib/cmake/libfort/libfort-config.cmake
-- Installing: /usr/local/lib/cmake/libfort/libfort-config-version.cmake
-- Installing: /usr/local/lib/cmake/libfort/libfort-targets.cmake
-- Installing: /usr/local/lib/cmake/libfort/libfort-targets-debug.cmake
-- Installing: /usr/local/lib/cmake/argparse/argparseConfig.cmake
-- Installing: /usr/local/include/argparse/argparse.hpp
-- Installing: /usr/local/lib/cmake/argparse/argparseConfig-version.cmake
-- Installing: /usr/local/lib/pkgconfig/argparse.pc
-- Installing: /usr/local/include/utf8proc.h
-- Installing: /usr/local/lib/libutf8proc.a
-- Installing: /usr/local/lib/pkgconfig/libutf8proc.pc
-- Installing: /usr/local/include/backward.hpp
-- Installing: /usr/local/lib/backward/BackwardConfig.cmake
-- Installing: /usr/local/include/readerwriterqueue/atomicops.h
-- Installing: /usr/local/include/readerwriterqueue/readerwriterqueue.h
-- Installing: /usr/local/include/readerwriterqueue/readerwritercircularbuffer.h
-- Installing: /usr/local/include/readerwriterqueue/LICENSE.md
```

c++ primer
https://15445.courses.cs.cmu.edu/spring2023/project0/

CMU数据库（15-445）实验1-BufferPoolManager
lru算法
https://15445.courses.cs.cmu.edu/spring2023/project1/

有四点，
1. Bustub用到的最难的算法是Deadlock Detector里的DFS，和BPM里的LRU-K
2. 如果读/写Bustub（你所谓的 Toy Project）的代码都觉得吃力，我并不觉得去看工业界的代码提升有多大（反过来也一样，一个能熟练读懂工业界代码的同学，自身就自然知道需不需要做Project）
3. 光看不练，等于白看
4. 已经工作的同学，我相信随便一本工业界的工具书作为词典的作用，比这些Lectures/Notes的作用更大，i.e, DDIA is all you need

另外，Bustub是传统的Row Store DB，如果连最简单最经典的的行存磁盘数据库都看不懂，也不想做，那就更别说去看工业级DB的源码了

自己作为数据库方向的phd，并且现在也在业界当一个数据库内核开发人员，整体上是比较同意guyuan的说法的。
15-445确实是一门好课，但是Bustub确实是过于toy了，如果想从事数据库内核研发，看Bustub的代码意义不大。pg、mysql、clickhouse的代码可以多看看（虽然mysql的代码比较丑），而且源码分析的博客也挺多的。
当然作者的说法也没错，每个人的需求不一样，很多新人没有大型项目的代码阅读&开发经验，做一个课程pj入门这个领域也挺好的。
总结就是，这个项目适合新人入门。新人入门后如果在这个项目上花很多时间做性能优化/细读这个项目其他模块的源码，则意义不大。去业界实习/看成熟数据库源码会更高效。

人均445和6.824，指简历上都有，一查提交记录，都没有

多线程调试，打印同步日志，ide断点调试效果不好。
测试用例，完备
自己的机器上跑的好好的，测试服务器上就挂了，因为有些bug是偶发的

BusTub 是传统的 Row Store DB 的意思是：BusTub（CMU 15-445/645 数据库系统课程的教学用数据库系统）采用的是行式存储（Row-oriented / Row-store）架构，这是一种经典的、传统的数据库存储方式。

简单拆解一下这个说法：

### 1. 什么是 Row Store（行式存储）？
- 数据按行（一条完整记录）连续存储在磁盘/内存上。
- 比如一张表有 id、name、age、city 四个字段，一行数据可能是：
  ```
  [1, "Alice", 25, "Beijing"] → [2, "Bob", 30, "Shanghai"] → ...
  ```
  在物理存储上，这些字段是挨着放的：id1 + name1 + age1 + city1 + id2 + name2 + ...
- 读取一条完整记录（SELECT * FROM table WHERE id=1）非常高效，因为一次 I/O 就能把整行数据都读出来。
- 适合的操作：频繁的单行读写、插入、更新、删除（典型 OLTP 场景：订单系统、电商、银行交易等）。

### 2. 与之相对的是 Column Store（列式存储）
- 数据按列连续存储：所有 id 放一起，所有 name 放一起，所有 age 放一起……
  ```
  ids:   1, 2, 3, ...
  names: "Alice", "Bob", "Charlie", ...
  ages:  25, 30, 28, ...
  ```
- 适合的操作：分析型查询（OLAP），比如 SELECT AVG(age) FROM table GROUP BY city，只需读 age 这一列，压缩率高、I/O 少很多。
- 典型系统：ClickHouse、Snowflake、Vertica、Parquet 文件格式等。

### 3. 为什么说 BusTub 是“传统的” Row Store？
- BusTub 是为教学设计的单用户、面向磁盘的 DBMS，目标是让学生实现经典关系型数据库的核心组件。
- 它的存储引擎默认就是 Row Store：
  - 表数据以 Tuple（行）的形式存储在页面（Page）里。
  - Buffer Pool 管理固定大小的页面（通常 4KB 或 8KB）。
  - 索引（B+树）也是基于 RID（Row ID，指向某页 + 槽位）来定位整行。
  - 查询执行器（Project 3）用 Volcano 模型，操作符处理的是整行 Tuple。
- 这和 PostgreSQL、MySQL InnoDB、Oracle、SQL Server 等商用 OLTP 数据库的默认存储方式高度一致 → 所以叫传统的、行存数据库。
- 而现代很多分析型数据库（BigQuery、Redshift、DuckDB 的列存模式等）会偏向 Column Store。

一句话总结：
BusTub 是“传统的 Row Store DB” 意思就是：它像大多数经典事务型数据库（MySQL、PostgreSQL）一样，用行式存储来组织数据，优化的是事务处理（OLTP）场景，而不是分析型（OLAP）的列式存储。

这也是为什么 BusTub 实验里你会大量接触 Tuple、RID、Slot、Page 等基于行的概念，而不是列向量（Column Vector）或向量化执行。

在 Bustub 数据库中，Trie 是一种用于存储和检索字符串键的高效数据结构，特别适用于实现字符串索引。
什么是 Trie？
Trie（发音为 "try"，源自 retrieval）也叫前缀树或字典树，是一种有序树形数据结构，用于存储关联数组，其中的键通常是字符串。
Trie 在 Bustub 中的角色
在 Bustub 中，Trie 主要用于：
1. 字符串索引实现
Bustub 的 Trie 实现位于：
src/container/trie/

2. 目录结构

bustub/src/container/trie/
├── trie.h              # Trie 头文件
├── trie.cpp           # Trie 实现
├── trie_node.h        # Trie 节点定义
├── trie_header.h      # 头部信息
└── ...


Trie 的核心特性

数据结构特点

class TrieNode {
  bool is_value_node_;       // 是否是值节点
  std::map<char, shared_ptr<TrieNode>> children_;  // 子节点映射
  std::string value_;        // 存储的值（如果是叶子节点）
};

工作方式

以存储 ["cat", "car", "dog"] 为例：

      root
     /    \
    c      d
   /        \
  a          o
 / \          \
t*  r*         g*


Bustub 中 Trie 的实现
1. 基本操作
// 在 trie.h 中
class Trie {
 public:
  // 插入键值对
  bool Insert(const std::string &key, std::string value);
  
  // 查找键
  std::optional<std::string> GetValue(const std::string &key);
  
  // 删除键
  bool Remove(const std::string &key);
  
  // 检查键是否存在
  bool Contains(const std::string &key);
};

2. 磁盘持久化支持
Bustub 的 Trie 支持持久化到磁盘：
class Trie {
  // 序列化到页面
  void SerializeTo(Page *page);
  
  // 从页面反序列化  
  static std::unique_ptr<Trie> DeserializeFrom(Page *page);
};


使用示例

1. 在代码中使用 Trie

#include "container/trie/trie.h"
int main() {
  // 创建 Trie
  auto trie = std::make_unique<bustub::Trie>();
  
  // 插入数据
  trie->Insert("user:1001", "Alice");
  trie->Insert("user:1002", "Bob");
  trie->Insert("product:5001", "Laptop");
  
  // 查询
  auto result = trie->GetValue("user:1001");
  if (result.has_value()) {
    std::cout << "Found: " << result.value() << std::endl;  // 输出: Alice
  }
  
  return 0;
}

2. 在数据库中作为索引
-- 假设支持 Trie 索引
CREATE INDEX idx_name ON users(name) USING TRIE;

Trie 的优势
优势 说明
前缀搜索 高效查找所有以特定前缀开头的键
有序遍历 按键的字典序自动排序
内存效率 共享公共前缀，节省空间
查找速度 O(L) 时间复杂度，L 是键的长度

测试 Trie

Bustub 包含 Trie 的测试：
# 运行 Trie 测试
make starter_trie_test
./test/starter_trie_test

# 测试特定功能
./test/starter_trie_test --gtest_filter="*Insert*"
./test/starter_trie_test --gtest_filter="*Remove*"

实际应用场景
1. 字符串前缀搜索
-- 查找所有以 "Joh" 开头的名字
SELECT * FROM users WHERE name LIKE 'Joh%';
-- Trie 可以高效支持这种查询

2. 自动补全
// 获取所有以前缀开头的键
std::vector<std::string> GetKeysWithPrefix(const std::string &prefix);

3. 字典实现
适合实现拼写检查、单词自动补全等功能。
与其他索引的对比
索引类型 适用场景 Bustub 中的实现
Trie 字符串前缀搜索 src/container/trie/
B+树 范围查询、排序 src/storage/index/b_plus_tree.h
哈希表 等值查询 src/container/hash/

项目中的位置
# 查找所有 Trie 相关文件
find . -name "*.cpp" -o -name "*.h" | xargs grep -l "class Trie\|TrieNode" | grep -v ".git"
# 查看实现
cat -n src/container/trie/trie.h | head -50
编译和运行

# 构建整个项目（包含 Trie）
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Debug
make -j$(nproc)

# 只构建 Trie 测试
make starter_trie_test

总结
在 Bustub 中，Trie 是一个高效的字符串索引数据结构，主要用于：
1. 字符串键的存储和检索
2. 前缀搜索和自动补全
3. 字典序遍历
4. 教学目的，展示不同的索引结构实现

它是 Bustub 教学数据库系统中的一个重要组件，用于展示如何实现和优化字符串索引。Trie 特别适合需要前缀匹配的场景，比如搜索建议、联系人自动补全等应用。

欢迎来到数据库内核开发的“炼狱”——CMU 15-445 BusTub。既然你已经开始关心文件的存储路径和实验思路，说明你正准备从宏观视角审视这个系统。

BusTub 是一个面向磁盘的存储系统，它的设计哲学是“不要相信操作系统”。以下是针对各个 Lab 的思路梳理以及你关心的文件存储细节。



## 一、 各阶段实验核心思路 (Lab Overview)

### Lab 1: Buffer Pool Manager (内存管理)

这是整个系统的地基。你的任务是接管内存，不让操作系统插手。

* LRU-K Replacer: 实现页面置换算法，决定哪个“倒霉蛋”页面被踢出内存。
* Buffer Pool Manager: 负责从磁盘读取 Page 到内存中的 Frame，并维护页表。

### Lab 2: B+ Tree Index (索引结构)

这是公认最难的一个环节，主要处理数据的快速检索。

* 分层设计: 分为 Internal Page 和 Leaf Page。
* 分裂与合并: 当节点满了要拆分（Split），空了要合并（Merge/Redistribute）。
* 并发控制: 引入 Latch Crabbing 机制，确保多线程下爬树不会把树爬塌了。

### Lab 3: Query Execution (算子实现)

到了这一步，你开始实现 SQL 的执行逻辑。

* Volcano Model: 采用迭代器模型，每个算子通过 `Next()` 函数向上层返回一行数据。
* 算子实现: 顺序扫描 (SeqScan)、插入 (Insert)、哈希连接 (HashJoin) 和聚合 (Aggregation)。

### Lab 4: Concurrency Control (事务并发)

最后的疯狂，确保多个事务同时运行不会导致数据混乱。

* Lock Manager: 实现行级锁（S, X, IS, IX, SIX）。
* 死锁检测: 通过构建等待图 (Wait-for Graph) 并寻找环来解决死锁。



## 二、 存储路径与文件分布

在 BusTub 中，存储并不是零散的，而是高度集约化的。

### 1. 核心存储路径

BusTub 的所有数据物理上通常表现为单个文件，由 `DiskManager` 统一管理。

| 文件类型 | 常见物理路径 (Build 目录下) | 说明 |
|  |  |  |
| 数据/表文件 | `test.db` | 所有的表数据、元数据都存在这个 `.db` 文件中。 |
| 日志文件 | `test.log` | 预写日志 (WAL)，用于系统崩溃后的恢复。 |
| 临时文件 | `/tmp/bustub-test-XXXXXX` | 单元测试时生成的临时数据库文件，跑完通常会删除。 |

### 2. 逻辑上的存储结构

* 表文件 (Table Files): 在 BusTub 中，表数据被切分成一个个 16KB 的 Page。逻辑上由 `TableHeap` 管理。
* 索引文件 (Index Files): 索引并不独立存在于另一个磁盘文件，而是同样作为 Page 存储在 `.db` 文件中。系统通过 `page_id` 来区分哪个 Page 是数据，哪个是索引。
* 目录/元数据: 存储在 `catalog.h` 定义的系统目录中，记录了表名、表 ID、Schema 等信息的映射关系。



## 三、 避坑指南：给你的建议

1. 关于路径: 不要试图在代码里写死任何绝对路径。BusTub 使用 `DiskManager` 抽象了底层存储，你只需要关注 `page_id`。
2. 关于 Debug: 当你发现 B+ Tree 报错时，优先检查 `ParentPageID` 是否更新正确，这是新手最常栽跟头的地方。
3. 关于内存: 记得给 Page 加锁（Latch）和解锁。`UnpinPage` 时务必搞清楚 `is_dirty` 标志位，否则你的修改永远写不到磁盘上。

> 提示：如果你在 Lab 2 调优时感到绝望，可以先去看看 `src/storage/page/` 下的各类 Page 定义，理解了内存布局，逻辑自然就顺了。

你想先从 Lab 1 的 LRU-K 算法实现细节聊起，还是想看看 Lab 2 B+ 树分裂的具体伪代码？

LRU-K 算法是 Lab 1 的核心，也是 Buffer Pool Manager 决定“谁该滚出内存”的裁判。相比于传统的 LRU（只看最后一次访问时间），LRU-K 能够有效解决“扫描抗性” (Scan Resistance) 问题，防止一次全表扫描就把热点数据全部挤出去。

以下是实现 LRU-K Replacer 的关键逻辑与细节：



## 1. 核心数据结构

你需要一个 `LRUKNode` 类来记录每个 Frame 的状态。

* `history_`: 一个大小为  的列表（通常用 `std::list` 或 `std::deque`），记录该 Frame 最近  次访问的时间戳。
* `k_`: 也就是算法里的 。
* `is_evictable_`: 只有被标记为 `true` 的 Frame 才能被踢出（由 Buffer Pool Manager 通过 `SetEvictable` 控制）。
* `fid_`: Frame ID。

在 `LRUKReplacer` 类中，你通常需要：

* `node_map_`: `unordered_map<frame_id_t, LRUKNode>`，用于  时间找到节点。
* `latch_`: 互斥锁。记住，Replacer 是会被多线程并发访问的。



## 2. 驱逐策略 (Evict Logic)

这是最容易写出 Bug 的地方。驱逐优先级遵循以下两个原则：

### 第一优先级：访问次数少于 K 次的节点

如果一个 Frame 的访问历史记录不足  次，它的 -distance 被视为 +∞。

* 如果有多个节点访问次数都少于 ，则采用 FIFO (First In First Out) 原则：驱逐其中最早被第一次访问的那个节点。

### 第二优先级：访问次数达到 K 次的节点

如果所有可驱逐节点都已访问了至少  次：

* 计算每个节点的 -distance = 。
* 驱逐 -distance 最大的那个（即其倒数第  次访问发生得最早的）。



## 3. 关键函数实现细节

### `RecordAccess(frame_id)`

* 动作：当 Buffer Pool 访问一个 Page 时调用。
* 逻辑：
1. 如果 `frame_id` 不存在，创建一个新节点。
2. 更新该节点的 `history_`。如果记录数超过 ，弹出最老的那个。
3. 增加全局 `current_timestamp_`。



### `Evict()`

* 逻辑：
1. 遍历 `node_map_`（或者你维护的辅助队列）。
2. 筛选：只看 `is_evictable_ == true` 的节点。
3. 两轮搜索：
* 第一轮：找历史记录少于  的节点里，最早出现的。
* 第二轮：如果没有第一类，找已满  次记录里，-th timestamp 最小的。


4. 清理：从 `node_map_` 中删除该节点，并减少 `curr_size_`。



### `SetEvictable(frame_id, set_evictable)`

* 逻辑：改变一个 Frame 的可驱逐状态。
* 注意：这会改变 `curr_size_`（即 Replacer 中目前“可驱逐”节点的总数），但不会删除节点。



## 4. 常见坑点

1. 时间戳并非系统时间：通常使用一个简单的计数器 `size_t current_timestamp_`，每次访问自增即可。
2. 并发安全：`Evict` 和 `RecordAccess` 必须加锁。不要在持有锁的情况下调用其他也会加同一把锁的函数（死锁警告！）。
3. 内存管理：确保在 `Evict` 成功后，相关的数据结构被清理干净，避免内存泄漏。



## 5. 性能优化建议

虽然作业要求很简单，但如果你想追求极致性能：

* 不要在 `Evict` 时遍历全表：这会把  变成 。你可以尝试维护两个不同的 `std::set` 或带优先级的队列，分别存储“不足 K 次”和“满 K 次”的节点，从而实现更快的查找。

Lab 1 的第二部分是 Buffer Pool Manager 本身，它需要调用你写的这个 Replacer。你准备好去处理那些繁琐的 `page_id` 和 `frame_id` 映射了吗？

在 BusTub 的 Lab 1 中，`page_id` 和 `frame_id` 的映射确实是让很多开发者感到“绕”的地方。如果你能理清这两者的关系，Buffer Pool Manager (BPM) 就成功了一半。

我们可以把 Buffer Pool 想象成一家酒店：

* `page_id`：客人的身份证号（数据在磁盘上的永久唯一标识）。
* `frame_id`：酒店的房间号（内存中固定数量的槽位/槽位索引）。
* `Page` 对象：房间里的床位和设施（实际存储数据的地方）。



## 1. 映射的核心：`page_table_`
在代码中，你需要维护一个 `std::unordered_map<page_id_t, frame_id_t> page_table_`。
* 它的作用：快速告诉你，“身份证号为 X 的客人，目前住在哪个房间？”
* 为什么需要它：磁盘上有成千上万个 Page，但内存（Buffer Pool）里可能只有 10 个 Frame。当你要找某个 Page 时，必须先查表看它是否已经在内存里了。

## 2. 核心函数中的映射逻辑
### FetchPage(page_id)
这是最常用的函数，逻辑如下：

1. 查表：在 `page_table_` 里找 `page_id`。
2. 命中：如果在，直接找到对应的 `frame_id`，增加 `pin_count`，返回该 Page。
3. 不命中：
* 找一个空闲 Frame（从 `free_list_` 拿，或者从 `replacer_` 踢出一个）。
* 关键一步：如果踢出了旧 Page，记得在 `page_table_` 里删掉旧的映射。
* 从磁盘读入新 Page，在 `page_table_` 里建立新的映射：`page_table_[page_id] = frame_id`。

### NewPage(page_id)
逻辑与 Fetch 类似，区别在于：
* 你不需要从磁盘读，而是调用 `DiskManager` 分配一个新的 `page_id`。
* 同样需要在 `page_table_` 中记录这个新页面占用了哪个 `frame_id`。

## 3. 处理映射时的“避坑”准则
为了不让系统崩溃，请务必遵守这三条铁律：
1. 先清理再建立：当你决定驱逐（Evict）一个 `frame_id` 里的旧页面时，必须先根据旧页面的 `page_id` 从 `page_table_` 中将其删除，后再写入新页面的映射。
2. Pin Count 的意义：`pin_count` > 0 的页面绝对不能被 `replacer_` 踢走。如果所有的 Frame 都被 Pin 住了，`FetchPage` 或 `NewPage` 应该返回 `nullptr`。
3. Dirty Bit 的维护：在映射被销毁（驱逐）之前，检查 `is_dirty`。如果页面在内存里被改过，必须先调用 `DiskManager::WritePage` 写回磁盘。

## 4. 线程安全（Concurrency）

不要忘记 `std::mutex latch_`。在 BPM 中，几乎所有的操作（查表、改映射、调 Replacer）都需要全程加锁。

* 不要在持有 BPM 锁的情况下调用磁盘 I/O 以外的耗时操作（虽然在实验里通常没问题，但在生产环境这是性能杀手）。
* 小心死锁：确保你的加锁顺序是一致的。



### 总结：你的数据流向图

> Disk (page_id) <——> DiskManager <——> BufferPool (frame_id) <——> Page Table (Map)

搞定了这个映射，你就已经跨过了磁盘到内存的鸿沟。

你现在是打算开始编写 `FetchPage` 的具体代码，还是想先看看如何测试你的 `page_table_` 逻辑是否正确？
