# zookeeper



ZooKeeper’s atomic broadcast protocol: Theory and practice


AP?

一致性

zookeeper做dubbo的服务注册/发现，会出现40-60分钟(几十秒)的不可用



选举的时候，也只是服务上线不可用

服务信息在本地会做缓存



为什么不应该使用ZooKeeper做服务发现

http://dockone.io/article/78



ZK实现分布式锁
基于zookeeper临时有序节点可以实现的分布式锁。
大致思想即为：每个客户端对某个方法加锁时，在zookeeper上的与该方法对应的指定节点的目录下，生成一个唯一的瞬时有序节点。 判断是否获取锁的方式很简单，只需要判断有序节点中序号最小的一个。 当释放锁的时候，只需将这个瞬时节点删除即可。同时，其可以避免服务宕机导致的锁无法释放，而产生的死锁问题。

可以直接使用zookeeper第三方库Curator客户端，这个客户端中封装了一个可重入的锁服务。

Curator提供的InterProcessMutex是分布式锁的实现。acquire方法用户获取锁，release方法用于释放锁。



非阻塞的，无论成功还是失败都直接返回




源码是用什么语言写的？
分别有什么功能，分布式，实现了Paxos？
raft？


自己写zk

ping
pong

zk maillist
edidada@outlook.com

[zk github repo](https://github.com/apache/zookeeper)

maven组织的
java开发的

October, 2008: release 3.0.0 available



zk在dubbo hadoop中的应用



ZooKeeper是一个开源的**分布式协调服务**，由雅虎创建，是Google **Chubby的开源实现**。分布式应用程序可以基于ZooKeeper实现诸如**数据发布/订阅、负载均衡、命名服务、分布式协调/通知、集群管理、Master选举、分布式锁和分布式队列**等功能。



https://blog.csdn.net/shmily_lsl/article/details/81479158





书籍

zab协议



https://blog.csdn.net/liweisnake/article/details/70045164



ZooKeeper’s atomic broadcast protocol: Theory and practice

Andr ́e Medeiros March 20, 2012





zk上如何看到dubbo库中请求zk server的记录的

zkCli 操作dubbo
https://blog.csdn.net/keep_learn/article/details/71090259

[zookeeperInternals](http://zookeeper.apache.org/doc/r3.5.0-alpha/zookeeperInternals.html)

[zk操作](https://blog.csdn.net/feixiang2039/article/details/79810102#zookeeper-cli)

Zookeeper是Apacahe Hadoop的子项目，是一个树型的目录服务，支持变更推送

zkCli -server host:port
连接远程zk

dubbo的在向zookeeper注册服务时，放了些什么数据进去？
dubbo的负载均衡是dubbo自己做的，还是zookeeper做的？

dubbo_zookeeper.png

dubbo在zookeeper存储的格式
1、根节点：dubbo
2、一级子节点：提供服务的服务名
3、二级子节点：固定的四个子节点：分别为：consumers、configurators、routers、providers

dubbo的负载均衡是dubbo自己做的，还是zookeeper做的
Dubbbo自己做的

[dubbo在zookeeper存储的格式](https://blog.csdn.net/duzm200542901104/article/details/80949282)

[Zookeeper 保存的Dubbo信息详解](https://blog.csdn.net/robin90814/article/details/86523502)



Consumers:
/dubbo/com.example.dubbo.service.CityService/consumers/consumer://192.168.198.1/com.example.dubbo.service.CityService?application=consumer&category=consumers&check=false&dubbo=2.5.3&interface=com.example.dubbo.service.CityService&methods=findCityByName&pid=1976&side=consumer&timestamp=1547599528693

?

application：应用名

category：类型

check：检查

dubbo：dubbo版本

interface：接口名称

methods：接口方法名

pid：进程号

side：消费端或服务端

timestamp：时间戳

Providers
/dubbo/com.example.dubbo.service.CityService/providers/dubbo://192.168.198.1:20880/com.example.dubbo.service.CityService?anyhost=true&application=provider&dubbo=2.5.3&interface=com.example.dubbo.service.CityService&methods=findCityByName&pid=17608&side=provider&timestamp=1547599515151

anyhost：

application：应用名

dubbo：dubbo版本

interface：接口名称

methods：接口方法名

pid：进程号

side：消费端或服务端

timestamp：时间戳



Routers
配置路由规则

/dubbo/com.example.dubbo.service.CityService/routers/route://0.0.0.0/com.example.dubbo.service.CityService?category=routers&dynamic=false&enabled=true&force=false&name=cityservice&priority=10&router=condition&rule=method+=+findCityByName+&+consumer.host+=+192.168.198.1+=>+provider.port+=+20881+&+provider.port+!=+20880&runtime=false

?

Category：类型

Dynamic：是否动态调整，false表示需要手动调整

Enabled：是否启动

Force：是否强制，false表示，如果没有匹配到则调用其它可调用的服务

Name：路由名称

Priority：优先级

Router：condition符合条件则路由

Rule：路由规则

访问控制

禁止

/dubbo/com.example.dubbo.service.CityService/routers/route://0.0.0.0/com.example.dubbo.service.CityService?category=routers&dynamic=false&enabled=true&force=true&name=com.example.dubbo.service.CityService+blackwhitelist&priority=0&router=condition&rule=consumer.host=192.168.198.1=>false&runtime=false

?

Category：类型

Dynamic：是否动态调整，false表示需要手动调整

Enabled：是否启动

Force：是否强制

Name：接口名称

Priority：优先级

Router：condition符合条件则路由

Rule：路由规则IP为192.168.198.1的消费者禁止访问



Configrators
负载均衡
/dubbo/com.example.dubbo.service.CityService/configurators/override://0.0.0.0/com.example.dubbo.service.CityService?category=configurators&dynamic=false&enabled=true&loadbalance=random


Category：类型
Dynamic：是否动态调整，false表示需要手动调整
Enabled：是否启动
Loadbalance：负载均衡策略

权重
/dubbo/com.example.dubbo.service.CityService/configurators/override://192.168.198.1:20880/com.example.dubbo.service.CityService?category=configurators&dynamic=false&enabled=true&weight=200
Category：类型
Dynamic：是否动态调整，false表示需要手动调整
Enabled：是否启动
Weight：权重



zk clinet Watch机制

推送

重Leader



zookeeper

client实现



Zookeeper原生Java API、ZKClient和Apache Curator 区别对比
https://blog.csdn.net/l18848956739/article/details/99693299

1、zookeeper原生Java API
Zookeeper客户端提供了基本的操作，比如，创建会话、创建节点、读取节点、更新数据、删除节点和检查节点是否存在等。但对于开发人员来说，Zookeeper提供的基本操纵还是有一些不足之处。

Zookeeper API不足之处

（1）Watcher注册是一次性的，每次触发之后都需要重新进行注册；
（2）Session超时之后没有实现重连机制；
（3）异常处理繁琐，Zookeeper提供了很多异常，对于开发人员来说可能根本不知道该如何处理这些异常信息；
（4）只提供了简单的byte[]数组的接口，没有提供针对对象级别的序列化；
（5）创建节点时如果节点存在抛出异常，需要自行检查节点是否存在；
（6）删除节点无法实现级联删除；
基于以上原因，直接使用Zookeeper原生API的人并不多。

2、ZkClient

ZkClient是一个开源客户端，在Zookeeper原生API接口的基础上进行了包装，更便于开发人员使用。解决如下问题：

1）session会话超时重连
2）解决Watcher反复注册
3）简化API开发
虽然 ZkClient 对原生 API 进行了封装，但也有它自身的不足之处：

几乎没有参考文档；
异常处理简化（抛出RuntimeException）；
重试机制比较难用；
没有提供各种使用场景的实现；


Apache Curator
Curator是Netflix公司开源的一套Zookeeper客户端框架，和ZkClient一样，解决了非常底层的细节开发工作，包括连接重连、反复注册Watcher和NodeExistsException异常等。目前已经成为 Apache 的顶级项目。

其特点：

Apache 的开源项目
解决Watch注册一次就会失效的问题
提供一套Fluent风格的 API 更加简单易用
提供更多解决方案并且实现简单，例如：分布式锁
提供常用的ZooKeeper工具类
编程风格更舒服
除此之外，Curator中还提供了Zookeeper各种应用场景（Recipe，如共享锁服务、Master选举机制和分布式计算器等）的抽象封装。




```shell
<dependency>
    <groupId>com.101tec</groupId>
    <artifactId>zkclient</artifactId>
    <version>0.10</version>
</dependency>
<dependency>
    <groupId>org.apache.zookeeper</groupId>
    <artifactId>zookeeper</artifactId>
    <version>3.4.14</version>
    <type>pom</type>
</dependency>
```



```xml
        <dependency>
            <groupId>org.apache.curator</groupId>
            <artifactId>curator-framework</artifactId>
            <version>2.8.0</version>
        </dependency>
        <dependency>
            <groupId>org.apache.curator</groupId>
            <artifactId>curator-recipes</artifactId>
            <version>2.8.0</version>
        </dependency>
```







kafka也用zk

kafaka集群的 broker，和 Consumer 都需要连接 Zookeeper。
Producer 直接连接 Broker。
https://www.jianshu.com/p/a036405f989c
