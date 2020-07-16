# seata

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

长事误

Saga 理论出自 Hector & Kenneth 1987发表的论文 Sagas。

https://www.cs.cornell.edu/andru/cs711/2002fa/reading/sagas.pdf

https://www.microsoft.com/en-us/research/wp-content/uploads/2016/10/EldeebBernstein-TransactionalActors-MSR-TR-1.pdf

saga模式的实现，是长事务解决方案。

https://objcoding.com/2019/11/27/seata-at-start/

servicecomb

https://blog.csdn.net/tianyaleixiaowu/article/details/95208906

https://blog.csdn.net/weixin_39860915/article/details/103917845

**（AT、TCC、Saga、XA）模式分析**

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



QQ交流群

f重庆网友使用了



(原Fescar已更名为Seata)





 ./seata-server.bat  -p 8091 -h 127.0.0.1 -m file


 Seata 是一款开源的分布式事务解决方案，致力于在微服务架构下提供高性能和简单易用的分布式事务服务。在 Seata 开源之前，Seata 对应的内部版本在阿里经济体内部一直扮演着分布式一致性中间件的角色，帮助经济体平稳的度过历年的双11，对各BU业务进行了有力的支撑。经过多年沉淀与积累，商业化产品先后在阿里云、金融云进行售卖。2019.1 为了打造更加完善的技术生态和普惠技术成果，Seata 正式宣布对外开源，未来 Seata 将以社区共建的形式帮助其技术更加可靠与完备。 



 ap使用jar
 seata-server开启 8091端口

 2019年1月开源



 https://github.com/seata/ 



 https://seata.io/zh-cn/ 



https://github.com/seata/seata-samples