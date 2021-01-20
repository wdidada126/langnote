# 深入理解Apache Dubbo与实战



商宗海，花名诣极，Apache Dubbo PMC。曾就职于阿里巴巴、有赞，担任Dubbo框架技术负责人，长期活跃在Dubbo社区。现就职于蚂蚁金服中间件团队，负责sofa-rpc和云原生方向的产品研发。
林琳，花名景竹，曾就职于华软集团、递四方等公司，担任技术经理、高级架构师等职位。现就职于蚂蚁金服支付宝事业群，负责工程平台架构工作。



先看官方文档



Hession好像是http层的东西，跟webservice差不多



[深入理解Apache Dubbo与实战](https://book.douban.com/subject/34455777/)

https://blog.csdn.net/shaolong1013/article/details/105582263

Dubbo在zk中的配置信息
telnet ip port 回车 记住要有回车

四大类

[Dubbo zk命令行](http://alibaba.github.io/dubbo-doc-static/Telnet+Command+Reference-zh-showComments=true&showCommentArea=true.htm)

20880 port

ExtensionLoader
classpath下面有三个位置
前置条件
Interface
@SPI注解

Filter
配置有两种，一种是注解，一种是spring xml配置文件

https://www.cnblogs.com/mumuxinfei/p/9305710.html
定义类，实现Filter接口，


```java
    @Override
    public Result invoke(Invoker<?> invoker, Invocation invocation) throws RpcException {
       return invoker.invoke(invocation);
    }
```

在META-INF/dubbo目录下, 添加com.alibaba.dubbo.rpc.Filter文件, 其内容为
statFilter=com.test.StatFilter

而对于每个需要用到该filter的dubbo provider/consumer, 都需要在xml申明中添加filter标签, 比如:
```xml
<dubbo:reference id="echoService" check="false" interface="com.test.EchoService" filter="statFilter" />
```


全局配置:
　　其实实现全局配置, 非常的简单, 一种方式是通过额外的配置, 一种通过指定@Activate的group实现.
　　1. 额外的配置方式
　　以上文的案例为例, 在resource目录下, 添加dubbo.properties文件, 然后配置如下:

invoker：指服务提供者provider列表
invocation：指服务rpc调用相关参数信息


4
# 如果该filter要作用于为provider
dubbo.provider.filter=com.test.StatFilter
# 如果该filter要作用于为consumer
dubbo.consumer.filter=com.test.StatFilter
　　具体的目录结果如下:
　　
　　2. 指定@Activate的group
　　这个方法, 就比较简单了, 而且也不需要额外的配置文件了

package com.test
 
import com.alibaba.dubbo.common.Constants;
import com.alibaba.dubbo.common.extension.Activate;
 
@Activate(
        group = {Constants.PROVIDER, Constants.CONSUMER},
        order = -2000
)
public class StatFilter implements Filter {
 
    @Override
    public Result invoke(Invoker<?> invoker, Invocation invocation) throws RpcException {
       return invoker.invoke(invocation);
    }
 
}
　　

总结:
　　权当做笔记吧, 确实dubbo filter给了开发者很大自由度和空间.


### Chap. 1 Dubbo——高性能RPC通信框架 

总体上认识dubbo





### Chap. 2 开发第一款Dubbo应用程序 

跑仓库自带的demo例子

调试源码

Zk支持推，拉

### Chap. 3 Dubbo注册中心

Zookeeper

Redis



重试机制？？



注册中心

Spi

Extendloader



### Chap. 4 Dubbo扩展点加载机制



git@github.com:edidada/java-spi-demo.git

java spi    把实现写在文件里，通过修改文件内容来达到更新的目的，应对软件更新

ExtensionLoader.getExtend()

ExtensionLoader.getAdaptiveExtension().   获取当前扩展的自适应实现

ExtensionLoader.getActivateExtension()      根据条件获取当前扩展可自动激活的实现

ExtendFactory

java_spi.md



[扩展点加载机制(ExtensionLoader)](https://blog.csdn.net/jdluojing/article/details/44947221)



看书看大纲，精读，粗读

4.4 扩展点动态编译的实现



Dubbo有三个编译器

JDK

Javassist javassist.md

AdaptiveComplier





dubbo定义源码编译器Compiler及实现类JdkCompiler、JavassistCompiler




### Chap. 5 Dubbo启停原理解析



配置



xsd文件

Spring容器

namespaceHandlersupport？？？



invoke

exporer dubbo 协议 rmi协议



优雅停机

不能kill -9





### 第6章 Dubbo远程调用



Dubbo协议详解


### 第7章 Dubbo集群容错



### 第8章 Dubbo扩展点
Dubbo核心扩展点概述


### 第9章 Dubbo高级特性

### 第10章 Dubbo过滤器

公司项目用
分为消费者过滤器 提供者过滤器


**Dubbo书籍第二章**

Zk支持推，拉



三四章

注册中心

Spi

Extendloader



**令牌桶限流**

水龙头放水

恒定的

Token

可以改变速率

Buck

AccessLogFilter
https://blog.csdn.net/u013160932/article/details/81074231
