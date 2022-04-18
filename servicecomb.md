# servicecomb

华为

ServiceComb与业界流行生态互通:Zipkin、Skywalking、Prometheus等Tracing/APM生态,Apollo配置中心生态,Istio生态,K8S生态,Spring、SpringCloud等流行开源框架。



我始终认为Spring Cloud 社区一味地坚持rest是不明智的。他们搞出一个feign来把客户端做成一个rpc调用的形式。Dubbo的那套远程rpc明显直接好用多了，却被spring cloud社区看不上。
分布式服务明明可以做得更简单直接，即使要支持多语言，也不用一定要坚持只能rest。
这方面ServiceComb是领先了Spring Cloud和Dubbo的。Dubbo的问题是和Java绑死了，而Spring Cloud，则因为过度迷信rest导致性能和易用性上做出了很大牺牲。
作为一个同时用过并研究过Spring Cloud和Dubbo，并且是ServiceComb早期主要开发者，我可以说，由于它的后发优势，ServiceComb做的比前两者都好。



ServiceComb基于华为内部的CSE(Cloud Service Engine)框架开源而来



微服务 单进程


https://servicecomb.apache.org/


1987年普林斯顿大学的Hector Garcia-Molina和Kenneth Salem发表了一篇Paper Sagas，讲述的是如何处理long lived transaction（长活事务）。Saga是一个长活事务可被分解成可以交错运行的子事务集合。其中每个子事务都是一个保持数据库一致性的真实事务。

https://www.cs.cornell.edu/andru/cs711/2002fa/reading/sagas.pdf


