# erueka

https://gitee.com/edidada/eureka-producer-consumer.git

### erueka jar依赖
ribbon -> netty
jersey


### log springcloudlogging
目前是在项目根路径下面
linux部署，需要放在 /data/log路径下 如何处理

相对路径
java执行的 logs路径下

使用logback配置文件 可以更改log文件名称 路径

springcloudlogging

### erueka jar包依赖
ribbon
跟zk对比
archaius

### spring boot test

@SpringBootTest 测试用的注解
@SpringBootApplication


### jersey
需要打印下jersey http接口的日志


### ribbon

使用了Netty


### erueka的数据存哪儿？
内存 ConcurrentHashMap
![erueka的数据](imgs/20200908131751554.png)

### lease

com.netflix.eureka.lease.Lease

[Eureka注册表的数据存储](https://blog.csdn.net/chengqiuming/article/details/80658491)
访问http://localhost:8761/eureka/apps

eureka 1.6.2 使用slf4j这个日志库
com.netflix.eureka.registry.AbstractInstanceRegistry

    private final ConcurrentHashMap<String, Map<String, Lease<InstanceInfo>>> registry = new ConcurrentHashMap();
