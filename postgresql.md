# postgresql

https://www.postgresql.org/docs/9.1/transaction-iso.html

db/pg_ssi.jpg

A Critique of ANSI SQL Isolation Levels
https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr-95-51.pdf

CLOG管理
CLOG（Commit Log）在数据库系统中，特别是PostgreSQL中，用于记录事务的最终状态。以下是对CLOG管理的简要概述：

概述：
CLOG日志记录的是事务的最终状态，包括事务的提交、终止等状态。
CLOG日志管理器负责管理CLOG日志缓冲池，该缓冲池基于SLRU（Sequential LRU）策略实现。
日志结构：
PostgreSQL中事务系统一共记录了四种事务状态，包括事务正在运行、已提交、被终止和子事务已提交。
由于需要记录的事务状态只有四种，因此只需要2个字节就能记录一个事务状态信息。
一个页面（8K）能保存32K个日志记录，每个CLOG日志文件段由32个页组成，因此能保存1M个日志记录。
日志文件：
CLOG日志文件保存在PGDATA/pg_xact目录下。
文件命名使用段号（segment number），以4位16进制数字命名。
理论上可以存在的CLOG日志文件数量受限于事务ID的范围，但实际数量会少于理论值。
日志定位：
给定一个事务ID（xid），可以通过一个四元组（<segmentno, Pageno, Byte, Bindex>）定位到其在日志中的位置。
其中，segmentno是段号，Pageno是页号，Byte是页面偏移，Bindex是字节内偏移。


串行快照隔离 SSI
Serial Snapshot Isolation

Posgres的MVCC实现牛逼不，牛。serial snapshot isolation是很强。
是的,PostgreSQL的MVCC(Multiversion Concurrency Control,多版本并发控制)实现确实非常强大和出色。其中的串行快照隔离(Serial Snapshot Isolation)是PostgreSQL MVCC的核心机制之一,是它支持高并发读写的关键所在。
具体来说,PostgreSQL的MVCC及串行快照隔离机制有以下几个优点:
1. 高并发性能
   - MVCC允许多个事务并发读取同一数据,而不会相互阻塞。这大大提升了数据库的并发处理能力。
   - 串行快照隔离确保每个事务看到的数据都是一致的,不会出现脏读、不可重复读等问题。
2. 事务隔离性
   - 串行快照隔离是最高级别的隔离级别,可以避免幻读等隔离问题。
   - 即使事务之间存在并发,也能保证事务的原子性和隔离性。
3. 快照一致性
   - MVCC机制会为每个事务维护一个数据快照,确保事务内部看到的数据是一致的。
   - 即使数据在事务执行过程中发生变更,事务内部也能看到一致的快照数据。
4. 数据库恢复
   - MVCC的快照机制有利于数据库的恢复和审计,可以轻松地实现点in时间恢复。
5. 低锁开销
   - MVCC不需要对数据行加锁即可实现并发控制,大大降低了锁的开销。
总的来说,PostgreSQL的MVCC及串行快照隔离机制是其数据库引擎的核心优势之一,确实是非常出色的并发控制技术。这也是PostgreSQL广受欢迎的重要原因之一。

好的,让我来详细介绍一下串行快照隔离(Serializable Snapshot Isolation,SSI)的论文和代码实现。

论文方面:

- 串行快照隔离最初由Michael Cahill等人在2008年发表于SIGMOD会议上的论文《Serializable Isolation for Snapshot Databases》中提出。
- 论文中提出了一种基于依赖图的SSI算法,可以在不牺牲并发性的情况下实现可串行化的事务隔离。
- 论文详细阐述了SSI的原理和实现细节,包括如何检测和解决可串行化冲突。

代码实现方面:

- PostgreSQL就是最著名采用SSI机制的数据库系统之一。
- PostgreSQL的SSI实现主要集中在以下几个模块:
  1. 事务管理模块:维护事务的快照信息和依赖关系。
  2. 锁管理模块:检测可串行化冲突并加锁。
  3. 查询执行模块:根据事务快照提供一致的数据视图。
  4. 恢复模块:支持基于SSI的数据库恢复。
- PostgreSQL的SSI实现在9.1版本中引入,并在之后的版本中不断完善和优化。
- 除了PostgreSQL,Oracle数据库和某些NoSQL数据库如FaunaDB也采用了类似的SSI机制。

总的来说,串行快照隔离是一种非常强大的并发控制技术,通过精心设计的算法和数据结构实现,确保了数据库事务的正确性和高并发性能。PostgreSQL在这方面的实现可以说是业界的标杆之一。

可串行化冲突
确保即使多个事务同时执行，每个事务的执行结果也应该与它们按某种顺序串行执行的结果相同
在数据库系统中，可串行化冲突是指两个或多个事务的操作可能导致数据不一致或读取错误的一种情况，尤其是在并发环境下。可串行化是数据库并发控制的一个目标，旨在确保即使多个事务同时执行，每个事务的执行结果也应该与它们按某种顺序串行执行的结果相同。下面我将进一步解释这个概念。

### 什么是可串行化？
在英文中，“可串行化冲突”通常被称为 Serializable Conflict。这个术语主要用来描述在数据库并发控制中，保证事务执行结果与按某种顺序串行执行的结果相同的一种机制。此外，当提到具体的冲突类型时，通常会使用以下英文术语：
1. Write-Read Conflict - 写读冲突
2. Write-Write Conflict - 写写冲突
3. Read-Write Conflict - 读写冲突

这些术语帮助描述并发事务中可能发生的不同类型的数据访问冲突，这些冲突需要通过并发控制机制如锁定或时间戳排序来管理，以实现事务的可串行化。
可串行化是衡量数据库并发事务执行结果正确性的一个标准。如果一个并发执行的事务集合可以被重排为一个不产生冲突的串行执行序列，那么这个事务集合就是可串行化的。

### 冲突与可串行化
在并发环境中，冲突通常发生在以下两个事务之间：
1. 读写冲突（Write-Read Conflict）：当事务A修改了一个数据项，而事务B随后读取了同一个数据项，这种情况下，如果事务A和B是并发执行的，事务B可能会读取到错误的数据。
2. 写写冲突（Write-Write Conflict）：当两个事务都试图修改同一个数据项时，如果没有适当的同步机制，最终的数据可能会反映两个事务中的任何一个或两个事务都没有正确执行。
3. 读写冲突（Read-Write Conflict）：如果事务A读取了一个数据项，而事务B随后修改了同一个数据项，在事务A基于旧数据做出决策后，事务B的修改可能会导致事务A的决策失效。

### 如何实现可串行化？

数据库系统通常通过两种主要的并发控制技术来实现事务的可串行化：

1. 锁定机制（Locking）：数据库管理系统使用锁来控制对数据项的访问。基本策略包括共享锁（用于读取操作）和排他锁（用于写入操作）。通过这种方式，锁定机制确保没有其他事务可以访问同一数据项进行冲突操作。

2. 时间戳排序（Timestamp Ordering）：每个事务在开始时分配一个唯一的时间戳。数据库系统根据事务的时间戳来决定事务的执行顺序，确保时间戳较早的事务能够在时间戳较晚的事务之前执行相关操作。

### 总结

可串行化冲突的管理对于确保数据库操作的正确性和一致性至关重要。通过有效的并发控制机制，如锁定和时间戳排序，数据库系统能够提供可靠和一致的数据访问，即使在多个用户和应用程序并发访问的情况下也是如此。

在C++中，有许多开源库可以帮助实现线程同步和可串行化冲突。一个常用的库是Intel的Threading Building Blocks (TBB)。TBB提供了高级并行编程抽象，可以方便地实现线程安全和高效的并行计算。

下面是一个使用TBB实现可串行化冲突的示例代码：

### 使用Intel TBB实现可串行化冲突

首先，你需要安装Intel TBB库。如果你还没有安装，可以通过以下方式安装：

- 在Linux上，你可以使用包管理器安装，比如`apt-get`：
```bash
sudo apt-get install libtbb-dev
```

- 在Windows上，你可以从Intel官网下载安装包。

接下来，是示例代码：

```cpp
#include <iostream>
#include <vector>
#include <tbb/tbb.h>

// 共享资源
int shared_resource = 0;

// 一个线程执行的函数
void increment(int thread_id) {
    tbb::mutex::scoped_lock lock(mtx);  // 锁定互斥锁
    
    // 访问和修改共享资源
    std::cout << "Thread " << thread_id << " is incrementing the shared resource." << std::endl;
    shared_resource++;
    std::cout << "Shared resource after increment: " << shared_resource << std::endl;
}

int main() {
    const int num_threads = 10;
    std::vector<std::thread> threads;

    // 使用tbb::parallel_for并行执行线程
    tbb::parallel_for(0, num_threads, [](int i) {
        increment(i);
    });

    std::cout << "Final value of shared resource: " << shared_resource << std::endl;
    return 0;
}
```

### 代码解释：

1. 共享资源：`shared_resource`是所有线程访问和修改的共享变量。
2. TBB库：包括头文件`tbb/tbb.h`来使用TBB库中的功能。
3. 互斥锁：使用`tbb::mutex`来保护共享资源的访问。
4. 线程函数：`increment`函数在访问和修改共享资源前锁定互斥锁。
5. 主函数：
    - 使用`tbb::parallel_for`并行执行线程，避免了手动管理线程的创建和同步。
    - 打印最终的共享资源值。

TBB库提供了更高层次的抽象，使并行编程更加简洁和高效。通过使用`tbb::parallel_for`，我们可以轻松地并行执行多个线程，并保证线程安全。

在C++中实现可串行化冲突（Serializable Conflict）通常涉及使用线程锁（如互斥锁）来确保多个线程不会同时访问和修改共享资源。以下是一个示例代码，演示了如何在C++中实现可串行化冲突。

这个例子使用了`std::mutex`来保护对共享资源的访问。`std::mutex`是一个标准的互斥锁，它可以确保同时只有一个线程可以访问共享资源。

```cpp
#include <iostream>
#include <thread>
#include <mutex>
#include <vector>

// 共享资源
int shared_resource = 0;

// 互斥锁
std::mutex mtx;

// 一个线程执行的函数
void increment(int thread_id) {
    // 锁定互斥锁
    std::lock_guard<std::mutex> lock(mtx);
    
    // 访问和修改共享资源
    std::cout << "Thread " << thread_id << " is incrementing the shared resource." << std::endl;
    shared_resource++;
    std::cout << "Shared resource after increment: " << shared_resource << std::endl;
}

int main() {
    const int num_threads = 10;
    std::vector<std::thread> threads;

    // 创建并启动多个线程
    for (int i = 0; i < num_threads; ++i) {
        threads.push_back(std::thread(increment, i));
    }

    // 等待所有线程完成
    for (auto& th : threads) {
        th.join();
    }

    std::cout << "Final value of shared resource: " << shared_resource << std::endl;
    return 0;
}
```

### 代码解释：

1. 共享资源：`shared_resource`是所有线程访问和修改的共享变量。
2. 互斥锁：`std::mutex mtx`用来保护对共享资源的访问。
3. 线程函数：`increment`函数是每个线程执行的代码，它在访问和修改共享资源前锁定互斥锁，并在修改完成后自动解锁（由`std::lock_guard`管理）。
4. 主函数：
    - 创建并启动多个线程，每个线程运行`increment`函数。
    - 使用`std::thread`类创建线程，并存储在一个`std::vector`中。
    - 使用`join`方法等待所有线程完成。
    - 打印最终的共享资源值。

在这个例子中，`std::lock_guard`自动管理互斥锁的锁定和解锁，可以确保即使在异常情况下互斥锁也会被正确解锁。这种机制可以有效避免由于线程竞态条件（race conditions）导致的数据不一致问题。

冲突可串行化(Conflict Serializable)是指一个并发执行的事务集合,在执行顺序上等价于某个串行执行的事务集合,也就是说,任何并发执行的情况都可以转换成某个串行执行的情况

冲突等价(ConﬂictEquivalence) 可串行化调度(Serializable Schedules),事务事务(transaction)是在数据库上执行的一个或多个操作构成的序列,用来完成数据库系统的高级功能。

https://geek-docs.com/dbms/dbms-tutorial/dbms-conflict-serializability.html

产品架构  Shared-Everything

https://zhuanlan.zhihu.com/p/656483356

德歌
https://github.com/digoal/blog

### pg scheme
pg数据库下面有模式(scheme)，模式下面有表

[PostgreSQL 在国内公司应用](https://www.zhihu.com/question/19685185)

Greenplum开源
Massively Parallel Postgres for Analytics
Experience Greenplum Database, an open-source massively parallel data platform for analytics, machine learning and AI 

支持存储过程debug

sp（存储过程的作用

编程，避免大量的sql中间数据在网络上传输

### windows 10 安装版本

PostgreSQL 10.8
[PostgreSQL查看版本信息](https://blog.csdn.net/kmblack1/article/details/78721653)

PostgreSQL 10.12 Documentation

https://www.postgresql.org/docs/10/index.html


卸载了，中国电信云安装


开发语言 c

sql解析 flex bison

source repo
https://github.com/postgres/postgres



maillist

centos 7安装

https://www.postgresql.org/download/linux/redhat/

postgresql权限管理，如何添加一个网段的ssl访问权限？
配置参考文档：https://www.jianshu.com/p/21d25c0d6ab4

180.167.0.0/16
PostgreSQL安装后默认只能localhost:5432访问

本机登录
su - postgres
qsql -U postgres ？？？

核心的登录命令
psql "postgresql://[用户名]:[密码]@[服务器地址]:[端口]/[数据库名称]"
示例：psql postgresql://postgres:123456@192.168.51.17:5432/database

https://www.jianshu.com/p/823702d6643e
psql -Upostgres -h 118.182.97.157 -p 5432 -d postgres
psql -Upostgres -h 118.182.97.157 sonarqube
CREATE DATABASE sonarqube;
\q

命令行方式登录PostgreSQL

配置文件
/var/lib/pgsql/10/data/pg_hba.conf

在 PostgreSQL 10 中，要允许任何 IP 地址访问数据库，您需要进行以下配置更改：
1. 找到 PostgreSQL 的配置文件 `postgresql.conf`。在 Linux 上，该文件通常位于 `/etc/postgresql/10/main` 目录下；在 Windows 上，它通常位于 `C:\Program Files\PostgreSQL\10\data` 目录下。
2. 打开 `postgresql.conf` 文件，并找到以下配置项：

   ````conf
   #listen_addresses = 'localhost'    # 默认值为 'localhost'
   ```

   ````
2. 将 `listen_addresses` 的值修改为 `'*'`，以允许来自任何 IP 地址的连接：
   ````conf
   listen_addresses = '*'
   ```

   ````
3. 保存并关闭 `postgresql.conf` 文件。
4. 在 PostgreSQL 10 中，还需要修改 `pg_hba.conf` 文件来配置访问控制规则。找到并打开 `pg_hba.conf` 文件。
5. 在 `pg_hba.conf` 文件中，为允许任何 IP 地址访问数据库，请添加以下规则到文件的末尾：

   ````conf
   # 允许来自任何 IP 地址的连接
   host    all             all             0.0.0.0/0               md5
   ```

   这条规则允许任何 IP 地址以 `md5` 加密方式连接到任何数据库。

   ````
6. 保存并关闭 `pg_hba.conf` 文件。
7. 重新启动 PostgreSQL 服务器，以使配置更改生效。
请注意，允许任何 IP 地址访问数据库存在一定的安全风险。建议仅在开发或受信任的环境中使用此配置。在生产环境中，应该明确指定允许访问数据库的 IP 地址范围，并采取其他安全措施来保护数据库。

### pgsql 创建数据库
navicate图形界面创建数据库？ 登录，进命令行 CREATE DATABASE dbname;

PostgreSQL 创建数据库
https://www.runoob.com/postgresql/postgresql-create-database.html


PostgreSQL 数据库内核分析

https://book.douban.com/subject/6971366/

适合刚开始研读PG源代码的朋友
数据库执行计划用到了动态规划和图论等相关知识
开源数据库中，对空间地理数据支持比较好的要数PG的插件Postgi

Oracle ACE

第九届PostgreSQL中国技术大会
张文升
著有书籍《PostgreSQL实战》
《PostgreSQL指南：内幕探索》

/postgres# find . -name "*.y"
./contrib/cube/cubeparse.y
./contrib/seg/segparse.y
./src/test/isolation/specparse.y
./src/backend/replication/repl_gram.y
./src/backend/replication/syncrep_gram.y
./src/backend/utils/adt/jsonpath_gram.y
./src/backend/bootstrap/bootparse.y
./src/backend/parser/gram.y
./src/bin/pgbench/exprparse.y
./src/pl/plpgsql/src/pl_gram.y
