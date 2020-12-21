# Dubbo面试题

dubbo解决了扩容，缩容，以前负载均衡器单点故障

方便运维



### 点对点直连

```
ReferenceConfig<XxxService> reference = new ReferenceConfig<XxxService>(); // 此实例很重，封装了与注册中心的连接以及与提供者的连接，请自行缓存，否则可能造成内存和连接泄漏
// 如果点对点直连，可以用reference.setUrl()指定目标地址，设置url后将绕过注册中心，
// 其中，协议对应provider.setProtocol()的值，端口对应provider.setPort()的值，
// 路径对应service.setPath()的值，如果未设置path，缺省path为接口名
reference.setUrl("dubbo://10.20.130.230:20880/com.xxx.XxxService"); 
```







[Dubbo RPC面试题](https://www.jianshu.com/p/75c55e8bf2a5)



为什么需要dubbo
dubbo代表的分布式架构可以承受更大规模的并发流量





Dubbo服务注册与发现的流程图



[史上最全 40 道 Dubbo 面试题及答案](https://blog.csdn.net/moakun/article/details/82919804)



[经典 Dubbo 面试题](https://blog.csdn.net/samurai77/article/details/96428793)




Dubbo源码相关的问题

