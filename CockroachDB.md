# CockroachDB

CockroachDB是一个支持SQL，支持分布式事务的ACID的分布式数据，支持ANSI SQL的最高隔离级别Serializability。

CockroachDB是一个分布式关系型数据库，主要设计目标是可扩展，强一致和高可靠 。

[CockroachDB 1](https://blog.csdn.net/qq_34924156/article/details/89236693)

[cockroachlabs](https://www.cockroachlabs.com/)

https://github.com/cockroachdb/cockroach/

分布式cache ，alluxio已经做的很好了，不必重复造轮子，也是华裔做的
TIDB 生态和社区做的比较好。但从技术讲，cockroachDB是开源的领军者，cockroach 在很多核心技术实现上都比TIDB 牛逼，cockroch 的事务模型，分层lease , mpp 计算引擎，自己专用的存储引擎，去中心话等，非常有特色，特别是事务模型称得上是创新，性能估计是TIDB 好几倍。TIDB 的中心授时方案与Percolator 是硬伤，5.0 的事务提交优化成了异步提交，估计是参考了cockroach 的并行提交.

