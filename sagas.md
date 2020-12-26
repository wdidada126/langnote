### Sagas



### 

https://www.cs.cornell.edu/andru/cs711/2002fa/reading/sagas.pdf



https://servicecomb.apache.org/cn/docs/distributed-transactions-saga-implementation/

servicecomb-pack



[架构模式: Saga](https://github.com/apache/servicecomb-pack/blob/master/README_ZH.md)



https://www.cnblogs.com/paxlyf/p/11290604.html





**SAGA**

Saga起源于1987年Hector & Kenneth发表的论文Sagas。



1987年普林斯顿大学的Hector Garcia-Molina和Kenneth Salem发表了一篇Paper Sagas，讲述的是如何处理long lived transaction（长活事务）。Saga是一个长活事务可被分解成可以交错运行的子事务集合。其中每个子事务都是一个保持数据库一致性的真实事务。
 论文地址：[sagas](https://www.cs.cornell.edu/andru/cs711/2002fa/reading/sagas.pdf)



参考地址：

[https://www.cs.cornell.edu/andru/cs711/2002fa/reading/sagas.pdf](https://link.zhihu.com/?target=https%3A//www.cs.cornell.edu/andru/cs711/2002fa/reading/sagas.pdf)

Saga工作原理



执行模块

补偿模块

从事务ACID特性的角度，不支持隔离性



跟TCC对比

没有prepare



问题：

- 更新丢失

- 脏数据读取



Saga模型把一个分布式事务拆分为多个本地事务，每个本地事务都有相应的执行模块和补偿模块（ TCC中的Confirm和Cancel）。当Saga事务中任意一个本地事务出错时，可以通过调用相关的补偿方法恢复之前的事务，达到事务最终的一致性。

当每个Saga子事务 T1, T2, …, Tn 都有对应的补偿定义 C1, C2, …, Cn-1,那么Saga系统可以保证：

- 子事务序列 T1, T2, …, Tn得以完成 (最佳情况)；
- 或者序列 T1, T2, …, Tj, Cj, …, C2, C1, 0 < j < n, 得以完成。

由于Saga模型中没有Prepare阶段，因此事务间不能保证隔离性，当多个Saga事务操作同一资源时，就会产生更新丢失、脏数据读取等问题，这时需要在业务层控制并发，例如：

- 在应用层面加锁；
- 应用层面预先冻结资源。

Saga恢复方式

Saga支持向前和向后恢复：

- 向后恢复：补偿所有已完成的事务，如果任一子事务失败；
- 向前恢复：重试失败的事务，假设每个子事务最终都会成功。

显然，向前恢复没有必要提供补偿事务，如果你的业务中，子事务（最终）总会成功，或补偿事务难以定义或不可能，向前恢复更符合你的需求。理论上补偿事务永不失败，然而，在分布式世界中，服务器可能会宕机、网络可能会失败，甚至数据中心也可能会停电，这时需要提供故障恢复后回退的机制，比如人工干预。

总的来说，TCC和MQ都是以服务为范围进行分布式事务的处理，而XA、BED、SAGA则是以数据库为范围进行分布式处理，我们更趋向于选择后者，对于业务而言侵入小，改造的成本低。

Apache Service Comb是华为开源的微服务框架，其中微服务事务处理框架分为集中式和分布式协调器。未来会在Sharding-Sphere内部集成Saga集中式协调器，支持同一线程内不同服务（本地）间的分布式事务。

Saga以jar包的形式提供分布式事务治理能力。



微服务分布式事务Saga框架

[微服务分布式事务Saga框架](https://www.jdon.com/49306)



<<<<<<< HEAD
[Sagas for microservices](https://github.com/eventuate-tram/eventuate-tram-sagas)



Saga这个概念来源于三十多年前的一篇数据库论文[Sagas](http://www.cs.cornell.edu/andru/cs711/2002fa/reading/sagas.pdf) ，一个Saga事务是一个有多个短时事务组成的长时的事务。 在分布式事务场景下，我们把一个Saga分布式事务看做是一个由多个本地事务组成的事务，每个本地事务都有一个与之对应的补偿事务。在Saga事务的执行过程中，如果某一步执行出现异常，Saga事务会被终止，同时会调用对应的补偿事务完成相关的恢复操作，这样保证Saga相关的本地事务要么都是执行成功，要么通过补偿恢复成为事务执行之前的状态。

自动反向补偿

Saga定义了一个事务中的每个子事务都有一个与之对应的反向补偿操作。由Saga事务管理器根据程序执行结果生成一张有向无环图，并在需要执行回滚操作时，根据该图依次按照相反的顺序调用反向补偿操作。Saga事务管理器只用于控制何时重试，何时补偿，并不负责补偿的内容，补偿的具体操作需要由开发者自行提供。

ShardingSphere采用反向SQL技术，将对数据库进行更新操作的SQL自动生成反向SQL，并交由[saga-actuator](https://github.com/apache/servicecomb-saga-actuator)执行，使用方则无需再关注如何实现补偿方法，将柔性事务管理器的应用范畴成功的定位回了事务的本源——数据库层面。
=======
[Sagas for microservices](https://github.com/eventuate-tram/eventuate-tram-sagas)
>>>>>>> a37e32040eec40d601569c731c313a398efb2dec
