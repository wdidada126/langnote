# Java标准库

map foreach

(k,v) -> {
  
}


java 命令行程序
```shell
java -h
用法: java [-options] class [args...]
           (执行类)
   或  java [-options] -jar jarfile [args...]
           (执行 jar 文件)
其中选项包括:
    -d32          使用 32 位数据模型 (如果可用)
    -d64          使用 64 位数据模型 (如果可用)
    -client       选择 "client" VM
    -server       选择 "server" VM
                  默认 VM 是 client.

    -cp <目录和 zip/jar 文件的类搜索路径>
    -classpath <目录和 zip/jar 文件的类搜索路径>
                  用 ; 分隔的目录, JAR 档案
                  和 ZIP 档案列表, 用于搜索类文件。
    -D<名称>=<值>
                  设置系统属性
    -verbose:[class|gc|jni]
                  启用详细输出
    -version      输出产品版本并退出
    -version:<值>
                  警告: 此功能已过时, 将在
                  未来发行版中删除。
                  需要指定的版本才能运行
    -showversion  输出产品版本并继续
    -jre-restrict-search | -no-jre-restrict-search
                  警告: 此功能已过时, 将在
                  未来发行版中删除。
                  在版本搜索中包括/排除用户专用 JRE
    -? -help      输出此帮助消息
    -X            输出非标准选项的帮助
    -ea[:<packagename>...|:<classname>]
    -enableassertions[:<packagename>...|:<classname>]
                  按指定的粒度启用断言
    -da[:<packagename>...|:<classname>]
    -disableassertions[:<packagename>...|:<classname>]
                  禁用具有指定粒度的断言
    -esa | -enablesystemassertions
                  启用系统断言
    -dsa | -disablesystemassertions
                  禁用系统断言
    -agentlib:<libname>[=<选项>]
                  加载本机代理库 <libname>, 例如 -agentlib:hprof
                  另请参阅 -agentlib:jdwp=help 和 -agentlib:hprof=help
    -agentpath:<pathname>[=<选项>]
                  按完整路径名加载本机代理库
    -javaagent:<jarpath>[=<选项>]
                  加载 Java 编程语言代理, 请参阅 java.lang.instrument
    -splash:<imagepath>
                  使用指定的图像显示启动屏幕
有关详细信息, 请参阅 http://www.oracle.com/technetwork/java/javase/documentation/index.html。
```



```
jps -v
5808 TokenServerStart -Djava.awt.headless=true -Djava.net.preferIPv4Stack=true -Xmx2g -Xms2g -Dfastjson.parser.safeMode=true -XX:+DisableExplicitGC -XX:+UseConcMarkSweepGC -XX:+CMSParallelRemarkEnabled -XX:+UseCMSCompactAtFullCollection -XX:LargePageSizeInBytes=128m -XX:+UseFastAccessorMethods -XX:+UseCMSInitiatingOccupancyOnly -XX:CMSInitiatingOccupancyFraction=70


10961 StartupMain -Djava.awt.headless=true -Djava.net.preferIPv4Stack=true -Xmx2g -Xms2g -Dfastjson.parser.safeMode=true -XX:+DisableExplicitGC -XX:+UseConcMarkSweepGC -XX:+CMSParallelRemarkEnabled -XX:+UseCMSCompactAtFullCollection -XX:LargePageSizeInBytes=128m -XX:+UseFastAccessorMethods -XX:+UseCMSInitiatingOccupancyOnly -XX:CMSInitiatingOccupancyFraction=70
26131 StartupMain -Djava.awt.headless=true -Djava.net.preferIPv4Stack=true -Xmx2g -Xms2g -Dfastjson.parser.safeMode=true -XX:+DisableExplicitGC -XX:+UseConcMarkSweepGC -XX:+CMSParallelRemarkEnabled -XX:+UseCMSCompactAtFullCollection -XX:LargePageSizeInBytes=128m -XX:+UseFastAccessorMethods -XX:+UseCMSInitiatingOccupancyOnly -XX:CMSInitiatingOccupancyFraction=70
17748 StartupMain -Djava.awt.headless=true -Djava.net.preferIPv4Stack=true -Xmx2g -Xms2g -Xss256k -Dfastjson.parser.safeMode=true -XX:+DisableExplicitGC -XX:+UseConcMarkSweepGC -XX:+CMSParallelRemarkEnabled -XX:+UseCMSCompactAtFullCollection -XX:LargePageSizeInBytes=128m -XX:+UseFastAccessorMethods -XX:+UseCMSInitiatingOccupancyOnly -XX:CMSInitiatingOccupancyFraction=70
30824 QuorumPeerMain -Dzookeeper.log.dir=. -Dzookeeper.root.logger=INFO,CONSOLE -Dcom.sun.management.jmxremote -Dcom.sun.management.jmxremote.local.only=false
23065 StartupMain -Djava.awt.headless=true -Djava.net.preferIPv4Stack=true -Xmx2g -Xms2g -Dfastjson.parser.safeMode=true -XX:+DisableExplicitGC -XX:+UseConcMarkSweepGC -XX:+CMSParallelRemarkEnabled -XX:+UseCMSCompactAtFullCollection -XX:LargePageSizeInBytes=128m -XX:+UseFastAccessorMethods -XX:+UseCMSInitiatingOccupancyOnly -XX:CMSInitiatingOccupancyFraction=70
25515 ResDataStartup -Djava.awt.headless=true -Djava.net.preferIPv4Stack=true -Xmx22g -Xms22g -Dfastjson.parser.safeMode=true -XX:+DisableExplicitGC -XX:+UseConcMarkSweepGC -XX:+CMSParallelRemarkEnabled -XX:+UseCMSCompactAtFullCollection -XX:LargePageSizeInBytes=128m -XX:+UseFastAccessorMethods -XX:+UseCMSInitiatingOccupancyOnly -XX:CMSInitiatingOccupancyFraction=70
10491 OrderServerStart -Djava.awt.headless=true -Djava.net.preferIPv4Stack=true -Xmx2g -Xms2g -Xss256k -Dfastjson.parser.safeMode=true -XX:+DisableExplicitGC -XX:+UseConcMarkSweepGC -XX:+CMSParallelRemarkEnabled -XX:+UseCMSCompactAtFullCollection -XX:LargePageSizeInBytes=128m -XX:+UseFastAccessorMethods -XX:+UseCMSInitiatingOccupancyOnly -XX:CMSInitiatingOccupancyFraction=70
18284 SpsServerStart -Djava.awt.headless=true -Djava.net.preferIPv4Stack=true -Xmx2g -Xms2g -Dfastjson.parser.safeMode=true -XX:+DisableExplicitGC -XX:+UseConcMarkSweepGC -XX:+CMSParallelRemarkEnabled -XX:+UseCMSCompactAtFullCollection -XX:LargePageSizeInBytes=128m -XX:+UseFastAccessorMethods -XX:+UseCMSInitiatingOccupancyOnly -XX:CMSInitiatingOccupancyFraction=70
19005 Jps -Denv.class.path=.:/lib/dt.jar:/lib/tools.jar -Dapplication.home=/data/yyy40/lib/java/jdk1.8.0_181 -Xms8m
18479 DataStatisticsApplication -Djava.awt.headless=true -Djava.net.preferIPv4Stack=true -Xmx2g -Xms2g -Xmn256m -Xss256k -XX:+DisableExplicitGC -XX:+UseConcMarkSweepGC -XX:+CMSParallelRemarkEnabled -XX:+UseCMSCompactAtFullCollection -XX:LargePageSizeInBytes=128m -XX:+UseFastAccessorMethods -XX:+UseCMSInitiatingOccupancyOnly -XX:CMSInitiatingOccupancyFraction=70
```

观察zk car tomcat jetty idea



jvm参数有哪些，在哪儿输入的？

-Xms

-X -D输入jvm参数


getResourceAsStream返回NULL

A.class.getResourceAsStream("/config.properties")



https://blog.csdn.net/qudany10061700/article/details/86590373



common-codec

bouncycastle



Java容器类api要记住



校招Java也考Jvm参数了



Java

自定义hashmap

最好能解决多线程下循环引用、数据丢失和1.8版本下的数据覆盖问题



java可以看作c++的一门脚本？

jvm



jar包截图



imgs/java_jar.png



扰动函数 hash



https://blog.csdn.net/qq_28523617/article/details/77533097

https://www.zhihu.com/question/20733617





JDK 自带的 JAXB xml


Java Architecture for XML Binding (JAXB)
https://www.oracle.com/technical-resources/articles/javase/jaxb.html



Java14 scp 

[在JDK 14中，共有16个新特性](https://zhuanlan.zhihu.com/p/114760294?utm_source=wechat_session&utm_medium=social&utm_oi=30429583245312)

DTO





java远程调用之RMI
https://zhuanlan.zhihu.com/p/80686193

把你的设计、思路、总结都写到日记里（我用evernote），便于你自己思路的整理，很多时候人脑的缓存是真不够用，后面回来找思路的时候，细节也都在笔记里面







Java大数据、云计算、微服务、分布式系统等这些都是薪资待遇很好的岗位





虚拟化技术(CloudStack)（比openstack易用）





java.lang.Void


### java学习方向
进阶
netty高并发

java8 函数式




```java
int a =2;

if("1".equals(a)){

}
```




[Java中的Comparable和Comparator](https://blog.csdn.net/qing_gee/article/details/103884684)



## java命令行工具

java -cp xxx.jar xxx.xxx.xx.MainClass

java.util.concurrent.SynchronousQueue

需要写例子

java log 分析java xml方式

Java监控线程池


java agent


指令重排 编议原理
Java多线程的场合需要禁用

Java后端开发调试方式
日志
断点
Debug

logback
1.4.2

队列1024

换成log4j2

Java基本类型共有八种，基本类型可以分为三类，字符类型char，布尔类型boolean以及数值类型byte、short、int、long、float、double。数值类型又可以分为整数类型byte、short、int、long和浮点数类型float、double。JAVA中的数值类型不存在无符号的，它们的取值范围是固定的，不会随着机器硬件环境或者操作系统的改变而改变。实际上，JAVA中还存在另外一种基本类型void，它也有对应的包装类 java.lang.Void，不过我们无法直接对它们进行操作。8 中类型表示范围如下：
byte：8位，最大存储数据量是255，存放的数据范围是-128~127之间。
short：16位，最大数据存储量是65536，数据范围是-32768~32767之间。
int：32位，最大数据存储容量是2的32次方减1，数据范围是负的2的31次方到正的2的31次方减1。
long：64位，最大数据存储容量是2的64次方减1，数据范围为负的2的63次方到正的2的63次方减1。
float：32位，数据范围在3.4e-45~1.4e38，直接赋值时必须在数字后加上f或F。
double：64位，数据范围在4.9e-324~1.8e308，赋值时可以加d或D也可以不加。
boolean：只有true和false两个取值。
char：16位，存储Unicode码，用单引号赋值。


ngrinder



javaagent 日志收集

https://github.com/dingjs/javaagent

JavaAgent 简单例子

https://blog.csdn.net/catoop/article/details/51034739

https://docs.oracle.com/javase/7/docs/api/java/lang/instrument/package-summary.html

`javap -v XXX.class`


一定程度上考虑边界条件和性能问题



SQL规范与性能优化

1.2.1、先提前声明，博主工作用到是MySQL，可能有些场景只针对MySQL。说到SQL优化，一些概念必须要理解，不然死记硬背一两天就忘记了。特别是执行计划的概念。

1.2.2、什么是执行计划：a.决定如何访问表数据，是否通过索引，是否排序等。b.多表关联是先访问哪个表。c.多表关联时，使用哪种连接方式，不过现在MySQL只有嵌套连接（嵌套循环，顾名思义就是将一个表为出发点，将该表全部记录逐条去遍历另外一张表的记录）。

1.2.3、SQL执行顺序：a.检查语法是否正确。b.检查表是否存在、权限是否满足等。c.根据统计信息(如data length,rows,index length、索引唯一度)，生成较优的执行计划。d.根据执行计划，进行数据检索、过滤、合并、排序等操作。访问数据时，内存中如存在表数据，则直接进行操作；否则，从磁带读取表数据，放入内存，再进行操作；如内存不足，则内存中较冷数据涮出内存，再从内存中读取数据。

1.2.4、索引：查询的时候如果使用上了索引，可以提高效率，因为建立了索引后，可以理解为数据字典的结构存储，因此根据条件查询的时候更加高效。下面看一下MySQL常用的索引类型的概念。 

a．普通索引：在创建普通索引时，不附加任何限制条件。这类索引可以创建在任何数据类型中，其值是否唯一和非空由字段本身的完整性约束条件决定。建立索引以后，查询时可以通过索引进行查询。例如，在student表的stu_id字段上建立一个普通索引。查询记录时，就可以根据该索引进行查询。

b．唯一性索引:使用UNIQUE参数可以设置索引为唯一性索引。在创建唯一性索引时，限制该索引的值必须是唯一的。例如，在student表的stu_name字段中创建唯一性索引，那么stu_name字段的值就必需是唯一的。通过唯一性索引，可以更快速地确定某条记录。主键就是一种特殊唯一性索引。
c．单列索引:在表中的单个字段上创建索引。单列索引只根据该字段进行索引。单列索引可以是普通索引，也可以是唯一性索引，还可以是全文索引。只要保证该索引只对应一个字段 即可。
d．多列索引：多列索引是在表的多个字段上创建一个索引。该索引指向创建时对应的多个字段，可以通过这几个字段进行查询。但是，只有查询条件中使用了这些字段中第一个字段时，索引才会被使用。例如，在表中的id、name和sex字段上建立一个多列索引，那么，只有查询条件使用了id字段时该索引才会被使用。
e . 全文索引：使用FULLTEXT参数可以设置索引为全文索引。全文索引只能创建在CHAR、VARCHAR或TEXT类型的字段上。查询数据量较大的字符串类型的字段时，使用全文索引可以提高查询速度。例如，student表的information字段是TEXT类型，该字段包含了很多的文字信息。在information字段上建立全文索引后，可以提高查询information字段的速度。MySQL数据库从3.23.23版开始支持全文索引，但只有MyISAM存储引擎支持全文检索。在默认情况下，全文索引的搜索执行方式不区分大小写。但索引的列使用二进制排序后，可以执行区分大小写的全文索引。

还有空间索引，平时也比较少用。目前只有MyISAM存储引擎支持空间检索。目前博主也只接触过InnoDB存储引擎。
1.2.5、一般一张表索引不要超过5个，而且避免重复索引，而且也不是建了索引，根据索引字段条件查询，索引就会起作用。
1.2.6、一般哪些场景会导致索引失效：a.使用like关键字匹配字符串第一个为”%”的场景。b.条件中包含or、in、not in、<>关键字，默认不走索引的。c.访问表上的数据行超出表总记录数30%，变成全表扫描。d.查询条件使用函数在索引列上，或者对索引列进行运算。e.多列索引中，第一个索引列使用范围查询，只能用到部份或无法使用索引。f.多列索引中，第一个查询条件不是最左索引列，上面多列索引概念中也有提到。肯定还有更多的场景，但是博主现在能想到的场景就这些了。
1.2.7、不能同时使用两个索引，一个过滤数据，一个用于排序（主键除外）。
1.2.8、DML语句如果使用索引，会导致lock全表；如果使用了非唯一索引，可能只是锁住一定范围。对此，建议更新/删除数据尽量用上索引，如果可以最好用上主键或唯一索引，另外事务要及时提交。
1.2.9、最后一点，如何看执行计划，分析SQL的性能。这个吧，三言两语说不清楚，直接看其他博主的博文吧：[mysql explain执行计划详解](https://link.zhihu.com/?target=http%3A//www.cnblogs.com/xiaoboluo768/p/5400990.html)。一定要看！！！





习惯查阅 Java API Doc


- Introduction to algorithms，作者首字母缩写 CLRS ，讲算法的。
- Structure and Interpretation of Computer Programs， 简称 SICP，一本有些被神化的书，不过的确值得一读。多数人初读此书，两章后会有眼前豁然开朗的感觉。虽然这书已经不再是教材了。封面是魔术师和 lamda 。什么是经典，这就是经典。
- Computer architecture: a quantitative approach，此书我还没看，因为我自己也不是科班出身，而且此前对硬件毫无兴趣（Dijkstra 说过 computer science is no more about computers than astronomy is about telescopes），不过据说讲计算机架构的书里这本很好。
- Concrete Mathematics: A Foundation for Computer Science，高德纳出品，讲述与计算机相关的数学知识。如果数学书只想看一本，这个应该差不多够了。
- Computer Networks，作者Tanenbaum。
- 一本讲数字电路基础的书……可以省略，不过还是挺有趣的。
- TAOCP，若能看下去就看吧，看不下去也没啥，科班的都未必看得去。
- The Art of UNIX Programming，The Cathedral and the Bazaar，这两本是传道书，有些内容现在看来已经是常识了，不过仍旧值得一读。



- Code Complete (2nd Ed) by Steve McConnell，比较系统的软件工业流程认知和编程常识读本。
- The Pragmatic Programmer, 这本书讲授编程实作中的基本套路，过一遍有助于扫清盲点。
- 《人月神话》（*The Mythical Man-Month*），中文版还不错。
- 《最后期限》（*The Deadline*），中文版也还不错。
- Refactoring: Improving the Design of Existing Code，“重构”理论的集大成者。
- Design Patterns，“设计模式”的集大成者，作者四人帮，封面是埃舍尔的画。什么是经典，这就是经典。
- Programming Pearls，《编程珠玑》，茶余饭后的鉴赏小品，虽然说不定哪天就用到了。


Java设计模式
https://github.com/iluwatar/java-design-patterns

Enumeration

https://www.zhihu.com/question/276361636/answer/388370036


作者：wuxinliulei
链接：https://www.zhihu.com/question/276361636/answer/388370036
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。


1.class文件是二进制形式，是紧凑的，不想xml那样各个属性见有明显的分隔符2.每个class文件的开头都是4个字节的魔数(Magic Number),它的唯一作用是确定这个文件是否为一个能被虚拟机接受的Class文件。其实很多文件存储标准中都使用魔数来进行身份识别，
比如图片格式的gif或者jpeg文件头中都存在有魔数。使用魔数而不是扩展名来进行识别主要是基于安全方面的考虑，
因为文件扩展名是可以随意改动的。3.紧接着魔数，后面的4个字节存储的是Class文件的版本号，第5和第6个字节是次版本号(Minor Version),
第7和第8个字节是主版本号(Major Version).高版本的JDK能向下兼容以前的Class文件，但不能运行以后版本的Class文件，
即使文件格式并未发生任何变化，虚拟机也必须拒绝执行超过其版本号的Class文件。4.紧接着主次版本号的是常量池入口。常量池的常亮数目是不固定的，
所以常量池的入口放置了两个字节的数据代表常量池容量计数值.
5.其后是访问标志6.其后是类索引、父类索引、接口索引集合7.字段表集合8.方法表集合对于方法的参数为什么不能超过255个，
重点在方法表集合当中；attribute是什么？可以是int long 也可以是Class对象，就是方法的参数，而attributes_count是一个一字节的数据，
我们知道1个字节可以表示从1到255，所以方法参数不能超过255个9.属性表集合

for循环必须加大括号

HashMap是使用链表法来处理Hash冲突的；
threadlocal另一种处理Hash冲突的方法-----开放地址法

java.lang.ThreadLocal.ThreadLocalMap

java.lang.ThreadLocal.ThreadLocalMap.Entry
java.lang.ref.WeakReference


父级package不能引用子目录下的public class?

- ThreadLocalRandom

annotation的持久策略如果保存到class文件，如果用类似bytecodeviewer查看的话，怎么才能查看到

javax.annotation.PostConstruct
javax.annotation.Resource
Generated
Resources


https://blog.csdn.net/dh_chao/article/details/79001016

https://blog.csdn.net/tjcyjd/article/details/11111401


Java RESTful

https://www.gajotres.net/best-available-java-restful-micro-frameworks/
https://www.jdon.com/soa/6-restful.html
https://github.com/smallnest/Jax-RS-Performance-Comparison
https://cloud.tencent.com/developer/article/1031616






···

// 校验订单号
if (order.getOrderId() == null) {
    throw new RuntimeException("订单编号不能为空");
}
if (order.getOrderId() < 2019000000L) {
    throw new RuntimeException
        ("订单编号最小不能小于本年度初始值");
}
// 校验客户编号
if (order.getCustomerId() == null) {
    throw new RuntimeException("客户编号不能为空");
}
if (order.getCustomerId().length() < 10 ||
    order.getCustomerId().length() > 20) {
    throw new RuntimeException
        ("客户编号长度最小10位，最大20位");
}

···

那真的应该尽快了解一下Validation验证框架，它能够消除散落在各层的重复性校验逻辑。

http://www.imooc.com/article/292304

Java 字符串 多行变一行

javax.imageio.ImageIO

throws new RuntimeException("");可以
throws new Exception("");不可以

Java package不能是enum
可以是enums

jucl java自带的日志库

package name包名区分大小写

```java
NamespaceHandlerSupport (org.springframework.beans.factory.xml)
    DruidStatNamespaceHandler (com.alibaba.druid.support.spring.stat.config)
    JeeNamespaceHandler (org.springframework.ejb.config)
    AopNamespaceHandler (org.springframework.aop.config)
    LangNamespaceHandler (org.springframework.scripting.config)
    OxmNamespaceHandler (org.springframework.oxm.config)
    JdbcNamespaceHandler (org.springframework.jdbc.config)
    RepositoryNameSpaceHandler (org.springframework.data.repository.config)
    TxNamespaceHandler (org.springframework.transaction.config)
    RedisNamespaceHandler (org.springframework.data.redis.config)
    DubboNamespaceHandler (com.alibaba.dubbo.config.spring.schema)
    ContextNamespaceHandler (org.springframework.context.config)
    NamespaceHandler (org.mybatis.spring.config)
    UtilNamespaceHandler (org.springframework.beans.factory.xml)
    MvcNamespaceHandler (org.springframework.web.servlet.config)
    TaskNamespaceHandler (org.springframework.scheduling.config)
    CacheNamespaceHandler (org.springframework.cache.config)
```

`dubbo:application`

```shell
    public void init() {
        registerBeanDefinitionParser("application", new DubboBeanDefinitionParser(ApplicationConfig.class, true));
        registerBeanDefinitionParser("module", new DubboBeanDefinitionParser(ModuleConfig.class, true));
        registerBeanDefinitionParser("registry", new DubboBeanDefinitionParser(RegistryConfig.class, true));
        registerBeanDefinitionParser("monitor", new DubboBeanDefinitionParser(MonitorConfig.class, true));
        registerBeanDefinitionParser("provider", new DubboBeanDefinitionParser(ProviderConfig.class, true));
        registerBeanDefinitionParser("consumer", new DubboBeanDefinitionParser(ConsumerConfig.class, true));
        registerBeanDefinitionParser("protocol", new DubboBeanDefinitionParser(ProtocolConfig.class, true));
        registerBeanDefinitionParser("service", new DubboBeanDefinitionParser(ServiceBean.class, true));
        registerBeanDefinitionParser("reference", new DubboBeanDefinitionParser(ReferenceBean.class, false));
        registerBeanDefinitionParser("annotation", new DubboBeanDefinitionParser(AnnotationBean.class, true));
    }
```


LinkedHashMap
protected boolean removeEldestEntry(Map.Entry<K,V> eldest)

AutoCloseable

```java
AutoCloseable接口位于java.lang包下，从JDK1.7开始引入。
1.在1.7之前，我们通过try{} finally{} 在finally中释放资源。
在finally中关闭资源存在以下问题：
1、自己要手动写代码做关闭的逻辑；
2、有时候还会忘记关闭一些资源；
3、关闭代码的逻辑比较冗长，不应该是正常的业务逻辑需要关注的；
2.对于实现AutoCloseable接口的类的实例，将其放到try后面（我们称之为：带资源的try语句），在try结束的时候，会自动将这些资源关闭（调用close方法）。

```


[javap的基本用法](https://blog.csdn.net/hantiannan/article/details/7659904)

关于System.err和System.out的使用区别
https://blog.csdn.net/captainCZY/article/details/79496959

log4j2中使用InheritableThreadLocal

[InheritableThreadLocal](https://docs.oracle.com/javase/6/docs/api/java/lang/InheritableThreadLocal.html)

```java

	import java.io.FileNotFoundException;
	import java.io.PrintWriter;
	import java.io.UnsupportedEncodingException;
	try {
	  PrintWriter writer = new PrintWriter("the-file-namess.txt", "UTF-8");
	  writer.println("access HttpPostRawAccessDto"+System.currentTimeMillis());
	  writer.println("The second line");
	  writer.close();
	} catch (FileNotFoundException e) {
	  e.printStackTrace();
	} catch (UnsupportedEncodingException e) {
	  e.printStackTrace();
	} finally {
	}

```

annotation中方法不能有访问权限修饰符（public private protected default）

[idea打印gc日志的2种方法](https://blog.csdn.net/bear_lam/article/details/79648701)

gc什么时候进行？
查看使用什么cms ？

枚举类型
Enum
也需要有构造函数
枚举类列表
，
，
；


Object

.wait()
Causes the current thread to wait until another thread invokes

[java关键字transient和volatile](https://www.iteye.com/blog/dongruan00-2090116)

[Java的四种引用](https://www.cnblogs.com/huajiezh/p/5835618.html)

强引用，软引用，弱引用，虚引用


access level


show variables like '%connect%';  查看链接参数
show status like '%connect%'  查看链接状态


java.lang.Enum是所有emun的父类

[Java并发编程实战----- AQS(四)：CLH同步队列](https://www.cnblogs.com/chenssy/p/5087652.html)

ResultSet
getBoolean()
getString()
getBlob(int columnIndex)

```java
       Statement stmt = con.createStatement(
                                      ResultSet.TYPE_SCROLL_INSENSITIVE,
                                      ResultSet.CONCUR_UPDATABLE);
       ResultSet rs = stmt.executeQuery("SELECT a, b FROM TABLE2");
```

statement 声明 陈述

DataSource
```java
Connection	getConnection(String username, String password)
```

[Java中Map遍历](https://www.cnblogs.com/fqfanqi/p/6187085.html)

[java static code block](https://stackoverflow.com/questions/2420389/static-initialization-blocks)

The non-static block:

{
    // Do Something...
}
Gets called every time an instance of the class is constructed. The static block only gets called once, when the class itself is initialized, no matter how many objects of that type you create.

Example:

public class Test {

    static{
        System.out.println("Static");
    }
    
    {
        System.out.println("Non-static block");
    }
    
    public static void main(String[] args) {
        Test t = new Test();
        Test t2 = new Test();
    }
}
This prints:

Static
Non-static block

[java enum 实现接口](https://blog.csdn.net/whl825/article/details/54582715)

[Java枚举实现接口](https://blog.csdn.net/qq_21508059/article/details/78806610)

[rsa-encryption-decryption-java](https://www.devglan.com/java8/rsa-encryption-decryption-java)

java enum 实现接口

https://blog.csdn.net/whl825/article/details/54582715

https://blog.csdn.net/qq_21508059/article/details/78806610



Reactive

Vert.x

Spring

Netty



GlassFish

WebLogic

Servlet不是nio，是bio，性能不高
以前高性能领域都是c cpp
现在用Netty



java字节码的安全 魔术





java 多进程

支持

https://www.cnblogs.com/chanshuyi/p/5331094.html





Java并发ConcurrentNavigableMap接口
https://www.yiibai.com/java_concurrency/concurrency_concurrentnavigablemap.html



http://dblab.xmu.edu.cn/post/google-bigtable/





**手写HashMap核心源码**

https://juejin.im/post/5d5cf60af265da03ec2e681a

构造方法
get
put
数组+链表红黑树


http://dblab.xmu.edu.cn/post/google-bigtable/





https://docs.oracle.com/en/java/javase/14/