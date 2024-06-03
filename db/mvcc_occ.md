# mvcc_occ

乐观并行控制协议


单版本OCC

多版本OCC

乐观并行控制协议（OCC）-知乎.mhtml
An Empirical Evaluation of In-Memory Multi-Version Concurrency Control https://dl.acm.org/doi/pdf/10.14778/3067421.3067427
CMU 15-721 Advanced Database System https://15721.courses.cs.cmu.edu/spring2020/
OCC的前世今生 https://zhuanlan.zhihu.com/p/41505168
浅析数据库的并发控制机制 https://catkang.github.io/2018/09/19/concurrency-control.html
Hekaton https://15721.courses.cs.cmu.edu/spring2020/papers/04-mvcc2/p298-larson.pdf

乐观并发控制（OCC）三阶段
读阶段
验证阶段
写阶段

数据项的时间戳
– W_TS  ：对�成功执行写操作的所有事务的最大时间戳
– R_TS  ：对�成功执行读操作的所有事务的最大时间戳
时间戳排序协议：托马斯写规则


数据库 并发控制协议 版本储存 垃圾回收 索引
MySQL-InnoDB MV2PL 回滚段，差异储存 后台回收 逻辑索引
