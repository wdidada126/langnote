# servicecomb

ServiceComb的另一个优势，那就是分布式事务最终一致性。
ServiceComb曾联合京东金融云和中国人保进行创新，提供分布式事务最终一致性解决方案，解决微服务场景下不能依靠单一数据库来实现跨服务事务一致性的难题；用户只需要通过注解方式定义事务的执行方法以及撤销方法，Saga框架会自动保证分布式事务执行的最终一致性。

华为

ServiceComb与业界流行生态互通:Zipkin、Skywalking、Prometheus等Tracing/APM生态,Apollo配置中心生态,Istio生态,K8S生态,Spring、SpringCloud等流行开源框架。

我始终认为Spring Cloud 社区一味地坚持rest是不明智的。他们搞出一个feign来把客户端做成一个rpc调用的形式。Dubbo的那套远程rpc明显直接好用多了，却被spring cloud社区看不上。
分布式服务明明可以做得更简单直接，即使要支持多语言，也不用一定要坚持只能rest。
这方面ServiceComb是领先了Spring Cloud和Dubbo的。Dubbo的问题是和Java绑死了，而Spring Cloud，则因为过度迷信rest导致性能和易用性上做出了很大牺牲。
作为一个同时用过并研究过Spring Cloud和Dubbo，并且是ServiceComb早期主要开发者，我可以说，由于它的后发优势，ServiceComb做的比前两者都好。

ServiceComb基于华为内部的CSE(Cloud Service Engine)框架开源而来

微服务 单进程
# code
https://servicecomb.apache.org/

https://github.com/apache/servicecomb-pack

```xml
    <dependency>
      <groupId>org.apache.servicecomb.pack</groupId>
      <artifactId>omega-spring-starter</artifactId>
      <version>${pack.version}</version>
    </dependency>
    <dependency>
      <groupId>org.apache.servicecomb.pack</groupId>
      <artifactId>omega-transport-resttemplate</artifactId>
      <version>${pack.version}</version>
    </dependency>
```

TCC and Saga distributed transaction co-ordination solutions
## saga
1987年普林斯顿大学的Hector Garcia-Molina和Kenneth Salem发表了一篇Paper Sagas，讲述的是如何处理long lived transaction（长活事务）。Saga是一个长活事务可被分解成可以交错运行的子事务集合。其中每个子事务都是一个保持数据库一致性的真实事务。

https://www.cs.cornell.edu/andru/cs711/2002fa/reading/sagas.pdf

saga

https://blog.csdn.net/dev_csdn/article/details/79852498

saga 不应该学习的，公司不用，浪费时间