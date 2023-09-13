# sofabolt

node Java支持 语言支持

java
hesssion序列化

https://gitee.com/edidada/sofa-bolt-test



目前推荐的序列化方式是 protobuf，因为它跨语言性做得比较好。在蚂蚁内部其实我们主要使用的是 hessian 序列化



https://github.com/alipay/sofa-bolt



https://github.com/sofastack/sofa-bolt-node



网络心跳包

SOFABolt 是蚂蚁金融服务集团开发的一套基于 [Netty](https://www.oschina.net/p/netty) 实现的网络通信框架。

- 为了让 Java 程序员能将更多的精力放在基于网络通信的业务逻辑实现上，而不是过多的纠结于网络底层 NIO 的实现以及处理难以调试的网络问题，Netty 应运而生。
- 为了让中间件开发者能将更多的精力放在产品功能特性实现上，而不是重复地一遍遍制造通信框架的轮子，SOFABolt 应运而生。