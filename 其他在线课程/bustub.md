# bustub

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
