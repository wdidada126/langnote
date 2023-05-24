# Dubbo

支持grpc protobuf
https://zhuanlan.zhihu.com/p/101921347

@Spi
@Adapter

spring boot starter

doc
https://dubbo.apache.org/zh/docs/v2.7/dev/source/dubbo-spi/


dubbo 注册中心支持redis zk nacos
负载均衡算法支持
网络协议支持

Dubbo 如何测试
类比http测试 ip 端口 发送报文

dubbo
lb 负载均衡
https://www.cnblogs.com/wyq178/p/9822731.html


dubbo xml配置项
https://blog.csdn.net/niugang0920/article/details/81975421

Filter invoke invoketion



获取调用方参数

maven 多module，注意jar包引用情况，idea 整个项目的依赖包，不是单个module的依赖包



dubbo main函数启动，不依赖servlet容器 Spring容器







http://dubbo.apache.org/zh/docs/v2.7/dev/impls/protocol/

- spring xsd
- java api



dubbo 跟http对比
http是url port 等等
dubbo是zk ip port，直连，底层Netty，dubbo协议
一个Java接口，通过方法参数传参。

dubbo多了接口发现，接口下线

http使用nginx做发在均衡，dubbo自带负载均衡

http feign做序列化

dubbo自带



### dubbo cxf



dubbo 协议
rest 协议
基于标准的Java REST API——JAX-RS 2.0（Java API for RESTful Web Services的简写）实现的REST调用支持
http 协议
hessian 协议
redis 协议
thrift 协议
gRPC 协议
memcached 协议
rmi 协议
webservice 协议



###### 服务提供者

```java
import org.apache.dubbo.rpc.config.ApplicationConfig;
import org.apache.dubbo.rpc.config.RegistryConfig;
import org.apache.dubbo.rpc.config.ProviderConfig;
import org.apache.dubbo.rpc.config.ServiceConfig;
import com.xxx.XxxService;
import com.xxx.XxxServiceImpl;
 
// 服务实现
XxxService xxxService = new XxxServiceImpl();
 
// 当前应用配置
ApplicationConfig application = new ApplicationConfig();
application.setName("xxx");
 
// 连接注册中心配置
RegistryConfig registry = new RegistryConfig();
registry.setAddress("10.20.130.230:9090");
registry.setUsername("aaa");
registry.setPassword("bbb");
 
// 服务提供者协议配置
ProtocolConfig protocol = new ProtocolConfig();
protocol.setName("dubbo");
protocol.setPort(12345);
protocol.setThreads(200);
 
// 注意：ServiceConfig为重对象，内部封装了与注册中心的连接，以及开启服务端口
 
// 服务提供者暴露服务配置
ServiceConfig<XxxService> service = new ServiceConfig<XxxService>(); // 此实例很重，封装了与注册中心的连接，请自行缓存，否则可能造成内存和连接泄漏
service.setApplication(application);
service.setRegistry(registry); // 多个注册中心可以用setRegistries()
service.setProtocol(protocol); // 多个协议可以用setProtocols()
service.setInterface(XxxService.class);
service.setRef(xxxService);
service.setVersion("1.0.0");
 
// 暴露及注册服务
service.export();
```


###### 服务消费者
```java
import org.apache.dubbo.rpc.config.ApplicationConfig;
import org.apache.dubbo.rpc.config.RegistryConfig;
import org.apache.dubbo.rpc.config.ConsumerConfig;
import org.apache.dubbo.rpc.config.ReferenceConfig;
import com.xxx.XxxService;
 
// 当前应用配置
ApplicationConfig application = new ApplicationConfig();
application.setName("yyy");
 
// 连接注册中心配置
RegistryConfig registry = new RegistryConfig();
registry.setAddress("10.20.130.230:9090");
registry.setUsername("aaa");
registry.setPassword("bbb");
 
// 注意：ReferenceConfig为重对象，内部封装了与注册中心的连接，以及与服务提供方的连接
 
// 引用远程服务
ReferenceConfig<XxxService> reference = new ReferenceConfig<XxxService>(); // 此实例很重，封装了与注册中心的连接以及与提供者的连接，请自行缓存，否则可能造成内存和连接泄漏
reference.setApplication(application);
reference.setRegistry(registry); // 多个注册中心可以用setRegistries()
reference.setInterface(XxxService.class);
reference.setVersion("1.0.0");
 
// 和本地bean一样使用xxxService
XxxService xxxService = reference.get(); // 注意：此代理对象内部封装了所有通讯细节，对象较重，请缓存复用
```




https://bbs.pediy.com/thread-260266.htm



git repo

- incubator-dubbo-annotation
- dubbo-dubbo-2.6.6
- dubbospringcustomer
- dubbospringprovider
- dubboalone
- testspringbootdubbo
- testspringclouddubbo

https://gitee.com/edidada/testspringbootdubbo




###### dubboalone

ServiceConfig不设置实现类

```shell
Exception in thread "main" java.lang.IllegalStateException: Failed to connect to config center (zookeeper): 127.0.0.1:2181 in 30000ms.
	at org.apache.dubbo.configcenter.support.zookeeper.ZookeeperDynamicConfiguration.<init>(ZookeeperDynamicConfiguration.java:75)
	at org.apache.dubbo.configcenter.support.zookeeper.ZookeeperDynamicConfigurationFactory.createDynamicConfiguration(ZookeeperDynamicConfigurationFactory.java:29)
	at org.apache.dubbo.configcenter.AbstractDynamicConfigurationFactory.getDynamicConfiguration(AbstractDynamicConfigurationFactory.java:33)
	at org.apache.dubbo.config.AbstractInterfaceConfig.getDynamicConfiguration(AbstractInterfaceConfig.java:274)
	at org.apache.dubbo.config.AbstractInterfaceConfig.prepareEnvironment(AbstractInterfaceConfig.java:249)
	at org.apache.dubbo.config.AbstractInterfaceConfig.startConfigCenter(AbstractInterfaceConfig.java:239)
	at org.apache.dubbo.config.AbstractInterfaceConfig.lambda$null$7(AbstractInterfaceConfig.java:580)
	at java.util.Optional.orElseGet(Optional.java:267)
	at org.apache.dubbo.config.AbstractInterfaceConfig.lambda$useRegistryForConfigIfNecessary$8(AbstractInterfaceConfig.java:573)
	at java.util.Optional.ifPresent(Optional.java:159)
	at org.apache.dubbo.config.AbstractInterfaceConfig.useRegistryForConfigIfNecessary(AbstractInterfaceConfig.java:571)
	at org.apache.dubbo.config.AbstractInterfaceConfig.checkRegistry(AbstractInterfaceConfig.java:167)
	at org.apache.dubbo.config.ServiceConfig.checkAndUpdateSubConfigs(ServiceConfig.java:270)
	at org.apache.dubbo.config.ServiceConfig.export(ServiceConfig.java:328)
	at cn.wdidada.dubbo.samples.echo.EchoProvider.main(EchoProvider.java:19)
```

zk网络超时


```shell
Exception in thread "main" java.lang.IllegalStateException: ref not allow null!
	at org.apache.dubbo.config.ServiceConfig.checkRef(ServiceConfig.java:369)
	at org.apache.dubbo.config.ServiceConfig.checkAndUpdateSubConfigs(ServiceConfig.java:292)
	at org.apache.dubbo.config.ServiceConfig.export(ServiceConfig.java:328)
	at cn.wdidada.dubbo.samples.echo.EchoProvider.main(EchoProvider.java:19)
```







```java
org.apache.dubbo.config.AbstractInterfaceConfig
List<RegistryConfig> registries
```

上述代码说明dubbo支持多注册中心

dubbo telnet invoke

https://blog.csdn.net/u012489091/article/details/83314798

失败

`invoke cn.wdidada.dubbo.samples.echo.api.EchoServic.echo({"msg":"123"})`



`invoke cn.wdidada.dubbo.samples.echo.api.EchoService.echo(123)`

`invoke cn.wdidada.dubbo.samples.echo.api.EchoService.echo("123")`

`invoke cn.wdidada.dubbo.samples.echo.impl.EchoServiceImpl.echo("123")`





 `invoke EchoService.echo({"msg":"msg"})`

 `invoke EchoService.echo("msg")`

 `invoke EchoService.echo(msg)`



`invoke cn.wdidada.dubbo.samples.echo.api.EchoService.echo({"msg":"msg","class":"java.lang.String"})`



ls EchoService

ls -l EchoService



http://dubbo.apache.org/zh-cn/docs/user/references/telnet.html

```
dubbo 版本 2.7.0
```



如何搞定？

debug源码了





###### books

- 深入理解Apache Dubbo与实战
- 深度剖析Apache Dubbo核心技术内幕

Dubbo容错

Dubbo etcd



Dubbo vs Brpc

brpc没有注册中心

Dubbo有集群，避免单点故障

thrift grpc tars有没有？




#### rc

zookeeper是注册中心

dubbo是配合Spring使用的，可以脱离Spring使用
log4j是日志
Dubbo QoS命令 quality of service
https://www.jianshu.com/p/e117b580b996



在Dubbo中，QoS这个概念被用于动态的对服务进行查询和控制。例如对获取当前提供和消费的所有服务，以及对服务进行动态的上下线，即从注册中心上进行注册和反注册操作。





http://dubbo.apache.org/zh-cn/blog/introduction-to-dubbo-qos.html

#### dubbo使用zk
netty





[可以跑起来的dubbo例子](https://www.cnblogs.com/chenmz1995/p/10683012.html)



Dubbo源码解析（四）注册中心——dubbo
https://segmentfault.com/blog/dubboanalysis

自定义logger
com.alibaba.dubbo.common.logger







com.alibaba.dubbo.rpc.Protocol接口有InjvmProtocol、DubboProtocol、RmiProtocol、HttpProtocol、HessianProtocol等实现



模块设计的可拔插原则

Dubbo扩展机制SPI
（一）注解@SPI
（二）注解@Adaptive
（三）注解@Activate
（四）接口ExtensionFactory
（五）ExtensionLoader

com.alibaba.dubbo.common.extension.ExtensionLoader

com.alibaba.dubbo.common.extension.ExtensionFactory
都是静态类
Cluster cluster = ExtensionLoader.getExtensionLoader(Cluster.class).getAdaptiveExtension();



```java
@SPI("dubbo")
public interface Protocol {
    
    int getDefaultPort();
  
    @Adaptive
    <T> Exporter<T> export(Invoker<T> invoker) throws RpcException;
   
    @Adaptive
    <T> Invoker<T> refer(Class<T> type, URL url) throws RpcException;
 
    void destroy();
}
Protocol refprotocol = ExtensionLoader.getExtensionLoader(Protocol.class).getAdaptiveExtension();
```





[dubbo 2.6 源码解读](https://github.com/CrazyHZM/dubbo/tree/analyze-2.6.x/dubbo-registry/dubbo-registry-api/src/main/java/com/alibaba/dubbo/registry)



spi破坏了双亲委派模型



app

boostrap

ext

https://blog.csdn.net/kunpeng90/article/details/100189580#comments



##### 4  [注册中心——开篇](https://segmentfault.com/a/1190000016905715)



dubbo-registry-api的解读
RegistryService

```java
void register(URL url);
void unregister(URL url);
void subscribe(URL url, NotifyListener listener);
void unsubscribe(URL url, NotifyListener listener);
List<URL> lookup(URL url);
```

Registry
```java
public interface Registry extends Node, RegistryService {
}

public interface Node {
    //获得节点地址
    URL getUrl();
    //判断节点是否可用
    boolean isAvailable();
    //销毁节点
    void destroy();

}


```


RegistryFactory
```java
@SPI("dubbo")
public interface RegistryFactory {

    @Adaptive({"protocol"})
    Registry getRegistry(URL url);

}
```

上面四个类的关系清楚了
RegistryFactory生产Registry
Registry接口继承Node, RegistryService





#### 5 support包下的AbstractRegistry
com.alibaba.dubbo.registry.support.AbstractRegistry
class，实现了Registry接口

AbstractRegistry实现的是Registry接口，是Registry的抽象类。为了减轻注册中心的压力，在该类中实现了把本地URL缓存到property文件中的机制，并且实现了注册中心的注册、订阅等方法。

https://segmentfault.com/a/1190000016905715

#### 6 support包下的FailbackRegistry

com.alibaba.dubbo.registry.support.FailbackRegistry
抽象类 实现了AbstractRegistry

FailbackRegistry继承了AbstractRegistry，AbstractRegistry中的注册订阅等方法，实际上就是一些内存缓存的变化，而真正的注册订阅的实现逻辑在FailbackRegistry实现，并且FailbackRegistry提供了失败重试的机制。

#### 7 support包下的AbstractRegistryFactory
com.alibaba.dubbo.registry.support.AbstractRegistryFactory
抽象类，实现了RegistryFactory

实现了RegistryFactory接口，抽象了createRegistry方法，它实现了Registry的容器管理。


#### 8 support包下的ConsumerInvokerWrapper && ProviderInvokerWrapper
这两个类实现了Invoker接口，分别是服务消费者和服务提供者的Invoker的包装器，其中就包装了一些属性
#### 9 support包下的ProviderConsumerRegTable

#### 10 support包下的SkipFailbackWrapperException

#### 11 status包下的RegistryStatusChecker

#### 12 integration包下的RegistryProtocol && RegistryDirectory

dubbo中registry、route、directory、cluster、loadbalance、route的关系以及一个引用操作和调用操作到底干了啥
https://www.cnblogs.com/notlate/p/10088829.html

RegistryProtocol implements Protocol

com.alibaba.dubbo.registry.integration.RegistryProtocol

[RegistryProtocol 与 DubboProtocol的区别](https://blog.csdn.net/u013076044/article/details/80614633)
RegistryProtocol 通过 URL 的 registry:// 协议头标识， DubboProtocol通过 URL 的dubbo://协议头标识


com.alibaba.dubbo.registry.integration.RegistryDirectory

[源码分析Dubbo服务注册与发现机制RegistryDirectory](https://blog.csdn.net/prestigeding/article/details/80727275)



RegistryProtocol

实际的协议（dubbo . rmi）包装者

RegistryDirectory

注册中心服务，维护着所有可用的远程Invoker或者本地的Invoker



##### 5 [注册中心——dubbo](https://segmentfault.com/a/1190000016921721)






https://www.bilibili.com/video/BV1ns411c7jV





https://dubbo.gitbooks.io/dubbo-user-book/content/





问：dubbo的负载均衡策略?



在 Dubbo 中，所有负载均衡实现类均继承自 AbstractLoadBalance，该类实现了 LoadBalance 接口，并封装了一些公共的逻辑。

2.1 RandomLoadBalance

RandomLoadBalance 是加权随机算法的具体实现，它的算法思想很简单



2.2 LeastActiveLoadBalance

LeastActiveLoadBalance 翻译过来是最小活跃数负载均衡



2.3 ConsistentHashLoadBalance

2.4 RoundRobinLoadBalance

加权轮询负载均衡



[Dubbo 官方doc 负载均衡](http://dubbo.apache.org/zh-cn/docs/source_code_guide/loadbalance.html)





### dubbo 集群容错策略

 

- #### failover cluster 模式

　　失败自动切换，自动重试其他机器，默认就是这个，常见于读操作。（失败重试其它机器）

- #### failfast cluster模式

　　一次调用失败就立即失败，常见于写操作。（调用失败就立即失败）

- #### failsafe cluster 模式

　　出现异常时忽略掉，常用于不重要的接口调用，比如记录日志。

- #### failback cluster 模式

　　失败了后台自动记录请求，然后定时重发，比较适合于写消息队列这种。

- #### forking cluster 模式

　　并行调用多个 provider，只要一个成功就立即返回。

- #### broadcacst cluster

　　逐个调用所有的 provider。



问：dubbo单词传输信息量多大？
8M

Dubbo支持的协议？

推荐使用 Dubbo 协议
1、http
2、thrift
3、hession
4、dubbo
5、rmi
6、webservice
7：memcached
8、redis
9、rest


com.alibaba.dubbo.common.logger.LoggerFactory

dubbo协议抓包



dubbo源码有哪些异常？





dubbo源码使用了哪些中间件开发策略？

自定义spi 相对于传统的Java spi 解决了一次加载全部缓存的问题

使用java编译器





dubbo配置项？





dubbo是不是跟Spring强耦合的？

Dubbo可以脱离Spring单独使用，采用API 配置
[API 配置](http://dubbo.apache.org/zh-cn/docs/user/configuration/api.html)



[Dubbo 整合 Pinpoint 做分布式服务请求跟踪](https://blog.csdn.net/yanpenglei/article/details/81217258)



[Spring Boot 2.x 基础案例：整合Dubbo 2.7.3+Nacos1.1.3](https://www.jianshu.com/p/b0dddce1d404)



[dubbo-go](https://github.com/apache/dubbo-go/tree/1.3.0)



- Cluster Strategy
  - Failover
  - [Failfast](https://github.com/apache/dubbo-go/pull/140)
  - [Failsafe/Failback](https://github.com/apache/dubbo-go/pull/136)
  - [Available](https://github.com/apache/dubbo-go/pull/155)
  - [Broadcast](https://github.com/apache/dubbo-go/pull/158)
  - [Forking](https://github.com/apache/dubbo-go/pull/161)
- Load Balance
  - Random
  - [RoundRobin](https://github.com/apache/dubbo-go/pull/66)
  - [LeastActive](https://github.com/apache/dubbo-go/pull/65)



[技术中台建设为什么比较愿意引入Dubbo而去掉Cloud体系](https://zhuanlan.zhihu.com/p/101529698)




xsd文件格式

基于spring自定义xsd文件

import

beans

tool

dubbo可以实现provicer的高可用




[使用seata-spring-boot-starter外部化配置轻松上手Dubbo的分布式事务](https://blog.csdn.net/u010046908/article/details/103887891)



使用seata-spring-boot-starter外部化配置轻松上手Dubbo的分布式事务






Dubbo没有熔断限流，鉴权

dubbo开启deubg日志


log4j.properties



log4j.rootLogger = verbose,stdout

### output console ###
log4j.appender.stdout = org.apache.log4j.ConsoleAppender
log4j.appender.stdout.Target = System.out
log4j.appender.stdout.layout = org.apache.log4j.PatternLayout
log4j.appender.stdout.layout.ConversionPattern = [%-5p] %d{yyyy-MM-dd HH:mm:ss,SSS} method:%l%n%m%n




dubbo解决bug的代码


先把Dubbo的功能先搞清楚

Rpc
负载均衡
熔断（假设）
分布式

http://www.ityouknow.com/springcloud/2017/11/20/dubbo-update-again.html


Exception in thread "main" java.lang.IllegalStateException: No such application config! Please add <dubbo:application name="..." /> to your spring config.
	at com.alibaba.dubbo.config.AbstractInterfaceConfig.checkApplication(AbstractInterfaceConfig.java:145)
	at com.alibaba.dubbo.config.ServiceConfig.doExport(ServiceConfig.java:310)
	at com.alibaba.dubbo.config.ServiceConfig.export(ServiceConfig.java:217)
	at com.alibaba.dubbo.config.spring.ServiceBean.export(ServiceBean.java:266)
	at com.alibaba.dubbo.config.spring.ServiceBean.onApplicationEvent(ServiceBean.java:106)
	at com.alibaba.dubbo.config.spring.ServiceBean.onApplicationEvent(ServiceBean.java:53)
	
	
目前开发和测试人员在测试dubbo接口时，都采用telnet 命令的方式，此种方式操作不方便、易出错、交互不友好，为了提高测试准确率、节省测试耗时，特开发dubbo接口测试平台，用户可以在浏览器上直接测试dubbo接口。
公司默认端口20880

https://www.cnblogs.com/feiqihang/p/4387330.html


Dubbo的历史

2011/10/27：阿里巴巴巴宣布 Dubbo 开源。

2012/10/23：发布最后一个版本 2.5.3 并停止维护更新。

2017/07/31：起死回生，官方宣布开启重新更新，并会得到重点维护。

2017/09/07：发布起死回生的第一个版本：dubbo-2.5.4。


Dubbo xsd

Dubbo  vs HSF

测试对应IP和端口下的dubbo服务是否连通，cmd命令如下

telnet localhost 20880

正常情况下，进入telnet窗口，键入回车进入dubbo命令模式。

http://dubbo.apache.org/zh-cn/docs/user/references/telnet.html

dubbo从2.0.5开始支持telnet

2.7.1有问题，尽量用2.7.2
风险提示：升级到2.7.1版本后，注册中心（多数是zookeeper）在某些特殊场景下会出现重复URL地址数据无法删除，导致消费方拿到的是失效地址，从而导致调用失败的问题，2.7.2版本里面会修复此问题，预计6月初发布。详细原因请参考#4213。

https://github.com/apache/dubbo/issues/4213



dubbo:annotation

两个Spring格式的dubbo配置文件

```java
Caused by: 
java.lang.IllegalStateException: Duplicate application configs: <dubbo:application name="test-isomerization-proxy" id="test-isomerization-proxy" /> and <dubbo:application name="test-isomerization-proxy" id="test-isomerization-proxy2" />
	at com.alibaba.dubbo.config.spring.ServiceBean.afterPropertiesSet(ServiceBean.java:167)
	at com.alibaba.dubbo.config.spring.AnnotationBean.postProcessAfterInitialization(AnnotationBean.java:173)
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.applyBeanPostProcessorsAfterInitialization(AbstractAutowireCapableBeanFactory.java:423)
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.initializeBean(AbstractAutowireCapableBeanFactory.java:1633)
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.doCreateBean(AbstractAutowireCapableBeanFactory.java:555)
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.createBean(AbstractAutowireCapableBeanFactory.java:483)
	at org.springframework.beans.factory.support.AbstractBeanFactory$1.getObject(AbstractBeanFactory.java:306)
	at org.springframework.beans.factory.support.DefaultSingletonBeanRegistry.getSingleton(DefaultSingletonBeanRegistry.java:230)
	at org.springframework.beans.factory.support.AbstractBeanFactory.doGetBean(AbstractBeanFactory.java:302)
	at org.springframework.beans.factory.support.AbstractBeanFactory.getBean(AbstractBeanFactory.java:202)
	at org.springframework.beans.factory.config.DependencyDescriptor.resolveCandidate(DependencyDescriptor.java:208)
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.doResolveDependency(DefaultListableBeanFactory.java:1138)
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.resolveDependency(DefaultListableBeanFactory.java:1066)
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor$AutowiredFieldElement.inject(AutowiredAnnotationBeanPostProcessor.java:585)
```

```java

Error:Internal error: (java.io.IOException) 磁盘空间不足。
java.io.IOException: 磁盘空间不足。
	at java.io.FileOutputStream.writeBytes(Native Method)
	at java.io.FileOutputStream.write(FileOutputStream.java:326)
	at java.io.BufferedOutputStream.write(BufferedOutputStream.java:122)
	at com.intellij.util.io.CompressedAppendableFile.saveIncompleteChunk(CompressedAppendableFile.java:420)
	at com.intellij.util.io.CompressedAppendableFile.force(CompressedAppendableFile.java:468)
	at com.intellij.util.io.PersistentHashMapValueStorage$MyCompressedAppendableFile.force(PersistentHashMapValueStorage.java:911)
	at com.intellij.util.io.CompressedAppendableFile.dispose(CompressedAppendableFile.java:472)
	at com.intellij.util.io.PersistentHashMapValueStorage$MyCompressedAppendableFile.dispose(PersistentHashMapValueStorage.java:917)
	at com.intellij.util.io.PersistentHashMapValueStorage.dispose(PersistentHashMapValueStorage.java:720)
	at com.intellij.util.io.PersistentHashMap.doClose(PersistentHashMap.java:739)
	at com.intellij.util.io.PersistentHashMap.close(PersistentHashMap.java:718)
	at org.jetbrains.jps.incremental.storage.AbstractStateStorage.close(AbstractStateStorage.java:60)
	at org.jetbrains.jps.incremental.storage.CompositeStorageOwner.close(CompositeStorageOwner.java:59)
	at org.jetbrains.jps.incremental.storage.CompositeStorageOwner.close(CompositeStorageOwner.java:59)
	at org.jetbrains.jps.incremental.storage.BuildDataManager.close(BuildDataManager.java:247)
	at org.jetbrains.jps.cmdline.ProjectDescriptor.release(ProjectDescriptor.java:142)
	at org.jetbrains.jps.cmdline.BuildSession.saveData(BuildSession.java:352)
	at org.jetbrains.jps.cmdline.BuildSession.runBuild(BuildSession.java:313)
	at org.jetbrains.jps.cmdline.BuildSession.run(BuildSession.java:137)
	at org.jetbrains.jps.cmdline.BuildMain$MyMessageHandler.lambda$channelRead0$0(BuildMain.java:235)
	at org.jetbrains.jps.service.impl.SharedThreadPoolImpl.lambda$executeOnPooledThread$0(SharedThreadPoolImpl.java:42)
	at java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:511)
	at java.util.concurrent.FutureTask.run(FutureTask.java:266)
	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149)
	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624)
	at java.lang.Thread.run(Thread.java:748)
Please perform full project rebuild (Build | Rebuild Project)

```


[dubbo ReferenceConfig(null) is not DESTROYED when FINALIZE](https://github.com/apache/dubbo/issues/1164)

```java

java.lang.IllegalStateException: Duplicate application configs: <dubbo:application name="test-isomerization-proxy" id="test-isomerization-proxy" /> and <dubbo:application name="test-isomerization-proxy" id="test-isomerization-proxy2" />
	at com.alibaba.dubbo.config.spring.ServiceBean.afterPropertiesSet(ServiceBean.java:167)
	at com.alibaba.dubbo.config.spring.AnnotationBean.postProcessAfterInitialization(AnnotationBean.java:173)
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.applyBeanPostProcessorsAfterInitialization(AbstractAutowireCapableBeanFactory.java:423)
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.initializeBean(AbstractAutowireCapableBeanFactory.java:1633)
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.doCreateBean(AbstractAutowireCapableBeanFactory.java:555)
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.createBean(AbstractAutowireCapableBeanFactory.java:483)
	at org.springframework.beans.factory.support.AbstractBeanFactory$1.getObject(AbstractBeanFactory.java:306)
	at org.springframework.beans.factory.support.DefaultSingletonBeanRegistry.getSingleton(DefaultSingletonBeanRegistry.java:230)
	at org.springframework.beans.factory.support.AbstractBeanFactory.doGetBean(AbstractBeanFactory.java:302)
	at org.springframework.beans.factory.support.AbstractBeanFactory.getBean(AbstractBeanFactory.java:202)
	at org.springframework.beans.factory.config.DependencyDescriptor.resolveCandidate(DependencyDescriptor.java:208)
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.doResolveDependency(DefaultListableBeanFactory.java:1138)
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.resolveDependency(DefaultListableBeanFactory.java:1066)
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor$AutowiredFieldElement.inject(AutowiredAnnotationBeanPostProcessor.java:585)
	at org.springframework.beans.factory.annotation.InjectionMetadata.inject(InjectionMetadata.java:88)
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor.postProcessPropertyValues(AutowiredAnnotationBeanPostProcessor.java:366)
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.populateBean(AbstractAutowireCapableBeanFactory.java:1264)
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.doCreateBean(AbstractAutowireCapableBeanFactory.java:553)
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.createBean(AbstractAutowireCapableBeanFactory.java:483)
	at org.springframework.beans.factory.support.AbstractBeanFactory$1.getObject(AbstractBeanFactory.java:306)
	at org.springframework.beans.factory.support.DefaultSingletonBeanRegistry.getSingleton(DefaultSingletonBeanRegistry.java:230)
	at org.springframework.beans.factory.support.AbstractBeanFactory.doGetBean(AbstractBeanFactory.java:302)
	at org.springframework.beans.factory.support.AbstractBeanFactory.getBean(AbstractBeanFactory.java:197)
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.preInstantiateSingletons(DefaultListableBeanFactory.java:761)
	at org.springframework.context.support.AbstractApplicationContext.finishBeanFactoryInitialization(AbstractApplicationContext.java:867)
	at org.springframework.context.support.AbstractApplicationContext.refresh(AbstractApplicationContext.java:543)
	at org.springframework.web.servlet.FrameworkServlet.configureAndRefreshWebApplicationContext(FrameworkServlet.java:668)
	at org.springframework.web.servlet.FrameworkServlet.createWebApplicationContext(FrameworkServlet.java:634)
	at org.springframework.web.servlet.FrameworkServlet.createWebApplicationContext(FrameworkServlet.java:682)
	at org.springframework.web.servlet.FrameworkServlet.initWebApplicationContext(FrameworkServlet.java:553)
	at org.springframework.web.servlet.FrameworkServlet.initServletBean(FrameworkServlet.java:494)
	at org.springframework.web.servlet.HttpServletBean.init(HttpServletBean.java:171)
	at javax.servlet.GenericServlet.init(GenericServlet.java:244)
	at org.eclipse.jetty.servlet.ServletHolder.initServlet(ServletHolder.java:534)
	at org.eclipse.jetty.servlet.ServletHolder.doStart(ServletHolder.java:346)
	at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:64)
	at org.eclipse.jetty.servlet.ServletHandler.initialize(ServletHandler.java:786)
	at org.eclipse.jetty.servlet.ServletContextHandler.startContext(ServletContextHandler.java:265)
	at org.eclipse.jetty.webapp.WebAppContext.startContext(WebAppContext.java:1242)
	at org.eclipse.jetty.server.handler.ContextHandler.doStart(ContextHandler.java:717)
	at org.eclipse.jetty.webapp.WebAppContext.doStart(WebAppContext.java:494)
	at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:64)
	at org.eclipse.jetty.deploy.ContextDeployer.deploy(ContextDeployer.java:359)
	at org.eclipse.jetty.deploy.ContextDeployer.access$000(ContextDeployer.java:82)
	at org.eclipse.jetty.deploy.ContextDeployer$ScannerListener.fileAdded(ContextDeployer.java:107)
	at org.eclipse.jetty.util.Scanner.reportAddition(Scanner.java:615)
	at org.eclipse.jetty.util.Scanner.reportDifferences(Scanner.java:540)
	at org.eclipse.jetty.util.Scanner.scan(Scanner.java:403)
	at org.eclipse.jetty.util.Scanner$1.run(Scanner.java:353)
	at java.util.TimerThread.mainLoop(Timer.java:555)
	at java.util.TimerThread.run(Timer.java:505)

```

dubbo consumer直接调用dubbo provider
配置中心zk，调用zk的java框架是可选的

[dubbo注册中心介绍](https://www.cnblogs.com/frankyou/p/8417087.html)

[dubbo负载均衡是如何实现的](https://www.cnblogs.com/luozhiyun/p/10963116.html)

AbstractLoadBalance (com.alibaba.dubbo.rpc.cluster.loadbalance)
    RandomLoadBalance (com.alibaba.dubbo.rpc.cluster.loadbalance)
    LeastActiveLoadBalance (com.alibaba.dubbo.rpc.cluster.loadbalance)
    RoundRobinLoadBalance (com.alibaba.dubbo.rpc.cluster.loadbalance)
    ConsistentHashLoadBalance (com.alibaba.dubbo.rpc.cluster.loadbalance)


@Reference
com.alibaba.dubbo.config.annotation.Reference;

org.springframework.beans.factory.xml.NamespaceHandlerSupport

com.alibaba.dubbo.config.spring.schema.DubboNamespaceHandler





#### dubbo用法
本地服务 Spring 配置
local.xml:

```xml

<bean id=“xxxService” class=“com.xxx.XxxServiceImpl” />
<bean id=“xxxAction” class=“com.xxx.XxxAction”>
    <property name=“xxxService” ref=“xxxService” />
</bean>

```

远程服务 Spring 配置
在本地服务的基础上，只需做简单配置，即可完成远程化：

将上面的 local.xml 配置拆分成两份，将服务定义部分放在服务提供方 remote-provider.xml，将服务引用部分放在服务消费方 remote-consumer.xml。
并在提供方增加暴露服务配置 <dubbo:service>，在消费方增加引用服务配置 <dubbo:reference>。
remote-provider.xml:

```

<!-- 和本地服务一样实现远程服务 -->
<bean id=“xxxService” class=“com.xxx.XxxServiceImpl” /> 
<!-- 增加暴露远程服务配置 -->
<dubbo:service interface=“com.xxx.XxxService” ref=“xxxService” /> 

```

remote-consumer.xml:

```
<!-- 增加引用远程服务配置 -->
<dubbo:reference id=“xxxService” interface=“com.xxx.XxxService” />
<!-- 和本地服务一样使用远程服务 -->
<bean id=“xxxAction” class=“com.xxx.XxxAction”> 
    <property name=“xxxService” ref=“xxxService” />
</bean>
```

bean -> dubbo:reference(id) -> dubbo:service -> bean

### dubbo:reference必填项目
id		string	必填
interface		class	服务接口名

### dubbo:service
interface		class	服务接口名
ref		object	必填	服务对象实现引用	

Zookeeper 是 Apacahe Hadoop 的子项目，是一个树型的目录服务，支持变更推送



### dubbo:protocol

name	<protocol>	string	必填	dubbo	性能调优	协议名称

org.apache.dubbo.config.ProtocolConfig


- dubbo://
- rmi://
- hessian://
- http://
- webservice://
- thrift://
- memcached://
- redis://
- rest://

### dubbo:registry
address	<host:port>	string	必填		服务发现	注册中心服务器地址，如果地址没有端口缺省为9090，同一集群内的多个地址用逗号分隔，如：ip:port,ip:port，不同集群的注册中心，请配置多个<dubbo:registry>标签

### dubbo:application
name application	string	必填		服务治理	当前应用名称，用于注册中心计算应用间依赖关系，注意：消费者和提供者应用名不要一样，此参数不是匹配条件，你当前项目叫什么名字就填什么，和提供者消费者角色无关，比如：kylin应用调用了morgan应用的服务，则kylin项目配成kylin，morgan项目配成morgan，可能kylin也提供其它服务给别人使用，但kylin项目永远配成kylin，这样注册中心将显示kylin依赖于morgan



application registry protocol三个配置项

```shell
    <dubbo:application name="dubbospringprovider" />
    <!-- zookeeper注册中心 -->
    <dubbo:registry address="zookeeper://127.0.0.1:2181" />
    <dubbo:protocol name="dubbo" port="20880" />
```







API
Dubbo支持通过多种API方式启动:
Spring XMLSpring AnnotationPlain JavaSpring Boot
Registry
Dubbo支持以下注册中心:
ZookeeperRedisSimpleMulticastEtcd3
Cluster
Dubbo支持以下容错机制:
Fail overFail safeFail fastFail backForkingBroadcast
Load balance
Dubbo支持以下负载均衡策略:
RandomLeast ActiveRound RobinConsistent hash
Protocol
Dubbo支持以下协议:
DubboRMIHessianHTTPWebServiceThriftNative ThriftMemcachedRedisRestJsonRPCXmlRPCJmsRpc
Transport
Dubbo支持以下网络传输扩展:
Netty3 Netty4 Grizzly Jetty Mina P2P Zookeeper
Serialization
Dubbo支持以下序列化机制:
Hessian2JavaJSONFstKryoNative HessianAvro





[携程 Dubbo 连接超时问题的排查](https://www.infoq.cn/article/y5KYxYeVPXAlHI1Y8ylX)



Dubbo如何试下telnet





 https://blog.csdn.net/qq_27384769/article/details/80665512 



回到TelnetHandler的spi文件

```
clear=com.alibaba.dubbo.remoting.telnet.support.command.ClearTelnetHandler
exit=com.alibaba.dubbo.remoting.telnet.support.command.ExitTelnetHandler
help=com.alibaba.dubbo.remoting.telnet.support.command.HelpTelnetHandler
status=com.alibaba.dubbo.remoting.telnet.support.command.StatusTelnetHandler
log=com.alibaba.dubbo.remoting.telnet.support.command.LogTelnetHandler
ls=com.alibaba.dubbo.rpc.protocol.dubbo.telnet.ListTelnetHandler
ps=com.alibaba.dubbo.rpc.protocol.dubbo.telnet.PortTelnetHandler
cd=com.alibaba.dubbo.rpc.protocol.dubbo.telnet.ChangeTelnetHandler
pwd=com.alibaba.dubbo.rpc.protocol.dubbo.telnet.CurrentTelnetHandler
invoke=com.alibaba.dubbo.rpc.protocol.dubbo.telnet.InvokeTelnetHandler
trace=com.alibaba.dubbo.rpc.protocol.dubbo.telnet.TraceTelnetHandler
count=com.alibaba.dubbo.rpc.protocol.dubbo.telnet.CountTelnetHandler
```





dubbo

register center

provider

customer

monitor

架构图

注意初始化 

调用顺序

同步异步。只有invoke是同步，其他都是异步







Consumer

- 第 2 步，subscribe 向注册中心订阅服务。
  - 注意，只订阅使用到的服务。
  - 再注意，首次会拉取订阅的服务列表，缓存在本地。
- 【异步】第 3 步，notify 当服务发生变化时，获取最新的服务列表，更新本地缓存。





Consumer 直接发起对 Provider 的调用，无需经过注册中心。而对多个 Provider 的负载均衡，Consumer 通过 **cluster** 组件实现。重点，不经过注册中心。





## Dubbo 如何做参数校验







## Dubbo 如何实现分布式事务？

首先，关于分布式事务的功能，不是 Dubbo 作为服务治理框架需要去实现的，所以 Dubbo 本身并没有实现。所以在 [《Dubbo 用户指南 —— 分布式事务》](http://dubbo.apache.org/zh-cn/docs/user/demos/distributed-transaction.html) 也提到，目前并未实现。

说起分布式，理论的文章很多，落地的实践很少。笔者翻阅了各种分布式事务组件的选型，大体如下：

- TCC 模型：TCC-Transaction、Hmily
- XA 模型：Sharding Sphere、MyCAT
- 2PC 模型：raincat、lcn
- MQ 模型：RocketMQ
- BED 模型：Sharding Sphere
- Saga 模型：ServiceComb Saga

那怎么选择呢？目前社区对于分布式事务的选择，暂时没有定论，至少笔者没有看到。笔者的想法如下：

- 从覆盖场景来说，TCC 无疑是最优秀的，但是大家觉得相对复杂。实际上，复杂场景下，使用 TCC 来实现，反倒会容易很多。另外，TCC 模型，一直没有大厂开源，也是一大痛点。
- 从使用建议来说，MQ 可能是相对合适的( 不说 XA 的原因还是性能问题 )，并且基本轮询了一圈朋友，发现大多都是使用 MQ 实现最终一致性居多。
- 2PC 模型的实现，笔者觉得非常新奇，奈何隔离性是一个硬伤。
- Saga 模型，可以认为是 TCC 模型的简化版，所以在理解和编写的难度上，简单非常多。

所以结论是什么呢？

- TCC 模型：TCC-Transaction、Hmily 。
  - 已经提供了和 Dubbo 集成的方案，胖友可以自己去试试。
- XA 模型：Sharding Sphere、MyCAT 。
  - 无需和 Dubbo 进行集成。
- 2PC 模型：raincat、lcn 。
  - 已经提供了和 Dubbo 集成的方案，胖友可以自己去试试。
- MQ 模型：RocketMQ 。
  - 无需和 Dubbo 进行集成。
- BED 模型：Sharding Sphere 。
  - 无需和 Dubbo 进行集成。
- Saga 模型：ServiceComb Saga 。
  - **好像**已经提供了和 Dubbo 集成的方案，参见 [《Saga-dubbo-demo》](https://github.com/apache/servicecomb-pack/blob/64d8cfdfb9e0c8362e962eb17765b57ae2211c84/saga-demo/saga-dubbo-demo/README.md) 文档。
  - 😈 暂时没去深入研究。

另外，胖友在理解分布式事务时，一定要记住，分布式事务需要由多个**本地**事务组成。无论是上述的那种事务组件模型，它们都是扮演一个**协调者**，使多个**本地**事务达到最终一致性。而协调的过程中，就非常依赖每个方法操作可以被重复执行不会产生副作用，那么就需要：

- 幂等性！因为可能会被重复调用。如果调用两次退款，结果退了两次钱，那就麻烦大了。
- 本地事务！因为执行过程中可能会出错，需要回滚。

鉴于服务发现对服务化架构的重要性，再补充一点：Dubbo 实践通常以ZooKeeper 为注册中心（Dubbo 原生支持的Redis 方案需要服务器时间同步，且性能消耗过大）。针对分布式领域著名的CAP理论（C——数据一致性，A——服务可用性，P——服务对网络分区故障的容错性），Zookeeper保证的是CP ，但对于服务发现而言，可用性比数据一致性更加重要 ，而 Eureka 设计则遵循AP原则 。






https://www.zhihu.com/question/45413135







[分布式系列-dubbo服务telnet命令](https://www.cnblogs.com/feiqihang/p/4387330.html)



`telnet ip port`

中间是空格

不是：





dubbo源码分析6-telnet方式的管理实现
https://www.cnblogs.com/simoncook/p/5669159.html

https://blog.csdn.net/u012410733/article/details/80792479

~~~java
DubboServerHandler
~~~





<xsd:element name="annotation">



<dubbo:anotation




- application
- module
- registry
- service
- reference
- argument





http://dubbo.apache.org/zh-cn/docs/user/configuration/xml.html







dubbo入口类DubboNamespaceHandler
https://blog.csdn.net/peace_hehe/article/details/79288053


dubbo系列之xml解析原理NamespaceHandler
https://blog.csdn.net/u012394095/article/details/83009107





dubbo zk client包没有引入，是可选的

cursorframerowk

recipint







为什么dubbo使用ZkClient作为zookeeper的客户端

dubbo使用了zkClient而不是使用zookeeper本身的客户端与zookeeper进行交互，为什么呢？

```xml
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



 

先看看zookeeper本身自带的客户端的问题。

1）ZooKeeper的Watcher是一次性的，用过了需要再注册；

2） session的超时后没有自动重连，生产环境中如果网络出现不稳定情况，那么这种情况出现的更加明显；
3） 没有领导选举机制，集群情况下可能需要实现stand by，一个服务挂了，另一个需要接替的效果；
4） 客户端只提供了存储byte数组的接口，而项目中一般都会使用对象。

5）客户端接口需要处理的异常太多，并且通常，我们也不知道如何处理这些异常。

 

I0Itec这个zookeeper客户端基本上解决了上面的所有问题，主要有以下特性：

1) 提供了zookeeper重连的特性------能够在断链的时候,重新建立连接,无论session失效与否.

2) 持久的event监听器机制------ZKClient框架将事件重新定义分为了stateChanged、znodeChanged、dataChanged三种情况，用户可以注册这三种情况下的监听器（znodeChanged和dataChanged和路径有关），而不是注册Watcher。

3) zookeeper异常处理-------zookeeper中繁多的Exception,以及每个Exception所需要关注的事情各有不同，I0Itec简单的做了封装.

4) data序列化------简单的data序列化.(Serialzer/Deserialzer)

5）有默认的领导选举机制

 

**请注意使用I0Itect-zkClient暂时有几个方法仍需要重写:**

*1) create方法*:创建节点时,如果节点已经存在,仍然抛出NodeExistException,可是我期望它不在抛出此异常.

**2) retryUtilConnected:** 如果向zookeeper请求数据时(create,delete,setData等),此时链接不可用,那么调用者将会被阻塞直到链接建立成功;不过我仍然需要一些方法是非阻塞的,如果链接不可用,则抛出异常,或者直接返回.

**3) create方法:** 创建节点时,如果节点的父节点不存在,我期望同时也要创建父节点,而不是抛出异常.

4) **data监测:** 我需要提供一个额外的功能来补充watch的不足,开启一个线程,间歇性的去zk server获取指定的path的data,并缓存起来..归因与watch可能丢失,以及它不能持续的反应znode数据的每一次变化,所以只能手动去同步获取.





### dubbo admin



MonitorService



com.alibaba.dubbo.monitor.MonitorService







### 缺省依赖

通过mvn dependency:tree > dep.log命令分析，Dubbo缺省依赖以下三方库



