# seata
seata需要学习相关的背景知识
Seata，意为Simple Extensible Autonomous Transaction Architecture

springboot集成分布式事务Seata
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-seata</artifactId>
    <version>${project.version}</version>
</dependency>
https://blog.csdn.net/zhangchangbin123/article/details/89310131

Seata-AT
https://zhuanlan.zhihu.com/p/340292579

@GlobalTransactional    
注解

seata

QQ群
254657148
需要独立部署一个seata server

tm tc rm

at

模式 默认的

本质上是通过添加一个undo_log来维护事务
数据库事务
套上seata的事务
saga
长事务

Saga 理论出自 Hector & Kenneth 1987发表的论文 Sagas。
https://www.cs.cornell.edu/andru/cs711/2002fa/reading/sagas.pdf
https://www.microsoft.com/en-us/research/wp-content/uploads/2016/10/EldeebBernstein-TransactionalActors-MSR-TR-1.pdf
saga模式的实现，是长事务解决方案。

https://objcoding.com/2019/11/27/seata-at-start/

servicecomb

https://blog.csdn.net/tianyaleixiaowu/article/details/95208906

https://blog.csdn.net/weixin_39860915/article/details/103917845

（AT、TCC、Saga、XA）模式分析
四种分布式事务模式，分别在不同的时间被提出，每种模式都有它的适用场景
AT 模式是无侵入的分布式事务解决方案，适用于不希望对业务进行改造的场景，几乎0学习成本。TCC 模式是高性能分布式事务解决方案，适用于核心系统等对性能有很高要求的场景。Saga 模式是长事务解决方案，适用于业务流程长且需要保证事务最终一致性的业务系统，Saga 模式一阶段就会提交本地事务，无锁，长流程情况下可以保证性能，多用于渠道层、集成层业务系统。事务参与者可能是其它公司的服务或者是遗留系统的服务，无法进行改造和提供 TCC 要求的接口，也可以使用 Saga 模式。XA模式是分布式强一致性的解决方案，但性能低而使用较少。

https://zhuanlan.zhihu.com/p/78599954

XA Protocol

The earliest distributed transaction model was X/Open Distributed Transaction Processing (DTP), or the XA protocol for short.





Seata整合教程:https://www.bilibili.com/video/BV1tz411z7BX/
文字版教程
https://mp.weixin.qq.com/s/2KSidJ72YsovpJ94P1aK1g
springcloud整合demo:
https://gitee.com/itCjb/spring-cloud-alibaba-seata-demo
https://github.com/lightClouds917/springcloud-eureka-feign-mybatis-seata-v100
dubbo整合demo:
https://gitee.com/itCjb/springboot-dubbo-mybatisplus-seata
官方示例:
https://github.com/seata/seata-samples



https://seata.io/

https://juejin.im/post/5e1ee7296fb9a0301942f3c9

https://www.infoq.cn/video/typL12whoFf2RsDzUWDl

[seata](https://segmentfault.com/a/1190000020639849)

saga

at

tcc

xa

server的

核心概念
tc（事务管理中心
tm(全局事务管理器)
rm（单个事务数据库的事务管理器

以上图片为已经使用Seata的部分用户，已经使用Seata但未登记的用户，请联系我进行使用登记，登记后可进入企业支持群。

f重庆网友使用了
(原Fescar已更名为Seata)

./seata-server.bat  -p 8091 -h 127.0.0.1 -m file


Seata 是一款开源的分布式事务解决方案，致力于在微服务架构下提供高性能和简单易用的分布式事务服务。在 Seata 开源之前，Seata 对应的内部版本在阿里经济体内部一直扮演着分布式一致性中间件的角色，帮助经济体平稳的度过历年的双11，对各BU业务进行了有力的支撑。经过多年沉淀与积累，商业化产品先后在阿里云、金融云进行售卖。2019.1 为了打造更加完善的技术生态和普惠技术成果，Seata 正式宣布对外开源，未来 Seata 将以社区共建的形式帮助其技术更加可靠与完备。 

ap使用jar
seata-server开启 8091端口

2019年1月开源

https://github.com/seata/ 

https://seata.io/zh-cn/ 

如果你需要一个强大的分布式事务解决方案,我推荐以下几款产品:
1. Seata:开源免费,功能完善,是目前使用最广的分布式事务中间件。
主要优点:
- 提供AT和TCC两种事务模式
- 注解声明全局事务
- 支持多种语言和数据库
- 完善的运维和监控系统
2. MyCat - Transaction Manager:MyCAT出的分布式事务产品。
主要优点:
- 基于MyCAT数据库代理,整合能力强
- 基于MySQL InnoDB的事务隔离
- 全面兼容MySQL协议
3. Narvar:收费产品,功能很强大,主打多品种支撑。
主要优点:
- 主张"多品种事务",支持多种分布式场景
- 提供完善的监控与运维工具
- 一键生成分布式事务流程
4. Circle:专业的分布式事务中间件,产品强调安全可靠。
主要优点:
- 强调资源隔离和授权控制
- 提供基于X/Open XA的分布式事务
- 支持多种应用框架和多种数据库
总的来说,上述四款产品都是功能强大的分布式事务中间件,对比如下:
- Seata/MyCAT - 开源免费,提供完整而强大的分布式事务解决方案。
- Narvar/Circle - 收费产品,强调多种分布式事务场景与安全可靠性。
选择时主要看中产品的功能和强项是否符合你的需求。如果你更看重多种事务场景的支撑或安全性,收费产品会是一个不错的选择。
希望能给你一些参考,选择合适你的分布式事务中间件。有任何问题欢迎随时和我交流!

## Fescar
Fescar和Seata都是为了解决微服务场景下的分布式事务问题而产生的，它们有以下一些区别：

名称：Fescar的原名是Fast&Easy Commit And Rollback，是阿里巴巴开源的分布式事务中间件。Seata则是Fescar的升级版本，从2019年4月起，更名位seata。
解决问题的方式：Fescar使用的是二阶段提交协议，而Seata则采用了更优化的方式来解决分布式事务问题。
除此之外，Fescar和Seata还有很多相似之处：

都是为了解决微服务场景下面临的分布式事务问题。
都支持高效并且对业务0侵入的方式。
都提供了两种模式：AT和TCC，当然这两个模式也可以混用。
总之，Fescar和Seata都是为了解决分布式事务问题而产生的，它们之间有一定的区别和相似之处。具体使用哪个可以根据实际需求来选择。
Fescar更名为Seata的主要原因是为了打造更中立、更开放、生态更加丰富的分布式事务开源社区。

在社区核心成员的投票下，Fescar升级为Seata，意为Simple Extensible Autonomous Transaction Architecture，即一套一站式分布式事务解决方案。这一更名也得到了社区的广泛认可和支持，旨在更好地推动分布式事务的发展和创新。

同时，为了实现适用于所有的分布式事务业务场景的目标，社区也积极吸引更多的开发者、用户和贡献者加入，共同打造一个更加繁荣、开放和创新的分布式事务开源生态。

因此，现在Fescar已经正式更名为Seata，标志着社区的进一步发展和壮大。

初步的版本规划

v0.1.0：

微服务框架支持: Dubbo
数据库支持: MySQL
基于 Spring AOP 的 Annotation
事务协调器: 单机版本

v0.5.x：

微服务框架支持: Spring Cloud
MT 模式
支持 TCC 模式事务的适配
动态配置和服务发现
事务协调器: 高可用集群版本

v0.8.x：

Metrics
控制台: 监控/部署/升级/扩缩容

v1.0.0：

General Availability: 生产环境适用

v1.5.x：
数据库支持: Oracle/PostgreSQL/OceanBase
不依赖 Spring AOP 的 Annotation
热点数据的优化处理机制
RocketMQ 事务消息纳入全局事务管理
NoSQL 纳入全局事务管理的适配机制
支持 HBase
支持 Redis

v2.0.0：
支持 XA
当然，项目迭代演进的过程，我们最重视的是社区的声音，路线图会和社区充分交流及时进行调整。

## 源代码分包解析 v1.3.0



 https://javadoc.dev/online/api/io.seata/seata-all/1.3.0/index.html



程序包

io.seata.common

io.seata.common.exception

io.seata.common.executor

io.seata.common.holder

io.seata.common.loader

io.seata.common.thread

io.seata.common.util

io.seata.compressor.bzip2

io.seata.compressor.gzip

io.seata.compressor.lz4

io.seata.compressor.sevenz

io.seata.compressor.zip

io.seata.config

io.seata.config.apollo

io.seata.config.consul

io.seata.config.custom

io.seata.config.etcd3

io.seata.config.nacos

io.seata.config.springcloud

io.seata.config.zk

io.seata.core.compressor

io.seata.core.constants

io.seata.core.context

io.seata.core.event

io.seata.core.exception

io.seata.core.lock

io.seata.core.logger

io.seata.core.model

io.seata.core.protocol

io.seata.core.protocol.transaction

io.seata.core.rpc

io.seata.core.rpc.netty

io.seata.core.rpc.netty.v1

io.seata.core.rpc.processor

io.seata.core.rpc.processor.client

io.seata.core.rpc.processor.server

io.seata.core.serializer

io.seata.core.store

io.seata.core.store.db

io.seata.core.store.db.sql.lock

io.seata.core.store.db.sql.log

io.seata.discovery.loadbalance

io.seata.discovery.registry

io.seata.discovery.registry.consul

io.seata.discovery.registry.custom

io.seata.discovery.registry.etcd3

io.seata.discovery.registry.eureka

io.seata.discovery.registry.nacos

io.seata.discovery.registry.redis

io.seata.discovery.registry.sofa

io.seata.discovery.registry.zk

io.seata.integration.dubbo

io.seata.integration.dubbo.alibaba

io.seata.integration.grpc.interceptor

io.seata.integration.grpc.interceptor.client

io.seata.integration.grpc.interceptor.server

io.seata.integration.http

io.seata.integration.motan

io.seata.integration.sofa.rpc

io.seata.rm

io.seata.rm.datasource

io.seata.rm.datasource.exec

io.seata.rm.datasource.exec.mysql

io.seata.rm.datasource.exec.oracle

io.seata.rm.datasource.exec.postgresql

io.seata.rm.datasource.sql

io.seata.rm.datasource.sql.serial

io.seata.rm.datasource.sql.struct

io.seata.rm.datasource.sql.struct.cache

io.seata.rm.datasource.undo

io.seata.rm.datasource.undo.mysql

io.seata.rm.datasource.undo.mysql.keyword

io.seata.rm.datasource.undo.oracle

io.seata.rm.datasource.undo.oracle.keyword

io.seata.rm.datasource.undo.parser

io.seata.rm.datasource.undo.postgresql

io.seata.rm.datasource.undo.postgresql.keyword

io.seata.rm.datasource.util

io.seata.rm.datasource.xa

io.seata.rm.tcc

io.seata.rm.tcc.api

io.seata.rm.tcc.interceptor

io.seata.rm.tcc.remoting

io.seata.rm.tcc.remoting.parser

io.seata.saga.engine

io.seata.saga.engine.config

io.seata.saga.engine.evaluation

io.seata.saga.engine.evaluation.exception

io.seata.saga.engine.evaluation.expression

io.seata.saga.engine.exception

io.seata.saga.engine.expression

io.seata.saga.engine.expression.seq

io.seata.saga.engine.expression.spel

io.seata.saga.engine.impl

io.seata.saga.engine.invoker

io.seata.saga.engine.invoker.impl

io.seata.saga.engine.pcext

io.seata.saga.engine.pcext.handlers

io.seata.saga.engine.pcext.interceptors

io.seata.saga.engine.pcext.routers

io.seata.saga.engine.pcext.utils

io.seata.saga.engine.repo

io.seata.saga.engine.repo.impl

io.seata.saga.engine.sequence

io.seata.saga.engine.serializer

io.seata.saga.engine.serializer.impl

io.seata.saga.engine.store

io.seata.saga.engine.store.db

io.seata.saga.engine.store.utils

io.seata.saga.engine.strategy

io.seata.saga.engine.strategy.impl

io.seata.saga.engine.utils

io.seata.saga.proctrl

io.seata.saga.proctrl.eventing

io.seata.saga.proctrl.eventing.impl

io.seata.saga.proctrl.handler

io.seata.saga.proctrl.impl

io.seata.saga.proctrl.process

io.seata.saga.proctrl.process.impl

io.seata.saga.rm

io.seata.saga.statelang.domain

io.seata.saga.statelang.domain.impl

io.seata.saga.statelang.parser

io.seata.saga.statelang.parser.impl

io.seata.saga.statelang.parser.utils

io.seata.saga.tm

io.seata.serializer.hessian

io.seata.serializer.kryo

io.seata.serializer.protobuf

io.seata.serializer.protobuf.convertor

io.seata.serializer.protobuf.generated

io.seata.serializer.protobuf.manager

io.seata.serializer.seata

io.seata.serializer.seata.protocol

io.seata.serializer.seata.protocol.transaction

io.seata.spring.annotation

io.seata.spring.annotation.datasource

io.seata.spring.event

io.seata.spring.tcc

io.seata.spring.util

io.seata.sqlparser

io.seata.sqlparser.druid

io.seata.sqlparser.druid.mysql

io.seata.sqlparser.druid.oracle

io.seata.sqlparser.druid.postgresql

io.seata.sqlparser.struct

io.seata.sqlparser.util

io.seata.tm

io.seata.tm.api

io.seata.tm.api.transaction
