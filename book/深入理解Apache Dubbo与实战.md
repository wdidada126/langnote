# 深入理解Apache Dubbo与实战



商宗海，花名诣极，Apache Dubbo PMC。曾就职于阿里巴巴、有赞，担任Dubbo框架技术负责人，长期活跃在Dubbo社区。现就职于蚂蚁金服中间件团队，负责sofa-rpc和云原生方向的产品研发。

林琳，花名景竹，曾就职于华软集团、递四方等公司，担任技术经理、高级架构师等职位。现就职于蚂蚁金服支付宝事业群，负责工程平台架构工作。



[深入理解Apache Dubbo与实战](https://book.douban.com/subject/34455777/)



Dubbo在zk中的配置信息
四大类

[Dubbo zk命令行](http://alibaba.github.io/dubbo-doc-static/Telnet+Command+Reference-zh-showComments=true&showCommentArea=true.htm)

20880 port

ExtensionLoader

classpath下面有三个位置
前置条件
Interface
@SPI注解





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

