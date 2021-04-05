# spring eureka

Spring cloud
Eureka
1.9版本
https://zhuanlan.zhihu.com/p/182408464
Eureka
传输数据默认是压缩json
Ap系统
Eureka server默认有client跟集群中的其他节点通信

服务提供者 消费者 全量 增量从eureka server中获取数据
保护模式

Eureka操作
Eureka也支持通过rest接口来操作注册中心
比如
DELETE eureka/v2/apps/appID/instanceID
该命令可以主动下线一个已有服务
详细接口参考
https://github.com/Netflix/eureka/wiki/Eureka-REST-operations
这个链接里有点老，当前版本的urll改成了以eureka/apps开头
默认是采用xml协议，如果想要json协议的，在http请求头中加入配置




