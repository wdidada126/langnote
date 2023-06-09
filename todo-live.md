# todo live



看小专栏 v大 quic

看占小狼博客 美团 有赞 阿里



看阿里 sential源码



spring cloud alibaba

研究Spring ClassUtils



Spring中的后置处理器BeanPostProcessor讲解



org.springframework.session.web.context.AbstractHttpSessionApplicationInitializer



Lettuce java redis client



jboss doc servlet



Spring Bean生命周期 记忆



feign http clinet java



ribbon



学习go

暂停



学习erlang 分布式



使用tars mesos



Tars集群部署 官方有文档



Tars c++ Java demo



Tars源码分析，先简单的，后难的，放一放



hbase 分布式列数据库



列式数据库



王珊 数据库 中国mooc



cloudera hadoop版本

Hadoop三大版本



k8s管理容器应用的



挑战 旧系统 调试



云原生应用



istio 提供代理，负载均衡



网易juc课程

b站狂神juc



看论文的步骤 先粗后细，公式推理



zotero



OLAP



it大咖说 视频文件



链家网 Spark 大数据分析



CNI k8s



[
https://blog.csdn.net/zhonglinzhang/article/details/82697524](https://blog.csdn.net/zhonglinzhang/article/details/82697524)

CNI是Container Network Interface的是一个标准的，通用的接口。现在容器平台：docker，kubernetes，mesos，容器网络解决方案：flannel，calico，weave。只要提供一个标准的接口，就能为同样满足该协议的所有容器平台提供网络功能，而CNI正是这样的一个标准接口协议。



Logon mmap





Mysql 主从架构搭建 系统自带

Slaver订阅Master的Binlog，读从Slaver，非读 Master



《Redis持久化方式》  RDB方式：定期备份快照，常用于灾难恢复。优点：通过fork出的进程进行备份，不影响主进程、RDB 在恢复大数据集时的速度比 AOF 的恢复速度要快。缺点：会丢数据。 AOF方式：保存操作日志方式。优点：恢复时数据丢失少，缺点：文件大，回复慢。 也可以两者结合使用。



后端技术博客一个站点

http://yalunwang.com



https://m.baidu.com/sf_bk/item/SRE/1141123?fr=aladdin&ms=1&rid=10176948610001659928

Site Reliability Engineer (网站可靠性工程师)





JVM参数整理进入anki

-Xms(最小堆),-Xmx(最大堆)



https://www.paperweekly.site/papers/2749



sql 92标准 文档



基础组件团队各个互联网公司也开始重视了



https://baike.baidu.com/item/CMDB/5403317?fr=aladdin



CMDB存储与管理企业IT架构中设备的各种配置信息，它与所有服务支持和服务交付流程都紧密相联，支持这些流程的运转、发挥配置信息的价值，同时依赖于相关流程保证数据的准确性。



String类为什么要被设计为是final的？



 1.不可变性支持线程安全。

 2.不可变性支持字符串常量池，提升性能。

 3.String字符串作为最常用数据类型之一，不可变防止了随意修改，保证了数据的安全性。





Wireshark tcpdump抓包，解决odb libmysqlclient往阿里云插入汉字乱码

考虑是url 编码的问题，不要以为是mysql字符串乱码 现在看来，真是乱码问题，不是url encoding





现在要学C#我推荐的方向就两个：  .NET Core做Web开发,多学习些分布式微服务中间件等内容。 Unity游戏开发





Netty 有个重庆的开发者为了学习Netty写了个http协议的解析器，可以参考



Fork and join框架

https://www.cnblogs.com/wkzhao/p/10263753.html



Fork/Join框架是Java并发工具包中的一种可以将一个大任务拆分为很多小任务来异步执行的工具，自JDK1.7引入。
Fork/Join框架主要包含三个模块：
1、任务对象：ForkJoinTask
2、执行Fork/Join任务的线程：ForkJoinWorkerThread
3、线程池：ForkJoinPool



https://blog.csdn.net/abc123lzf/article/details/82873181



shiro单体应用鉴权，不能直接用于分布式应用



xml dtd xsd文件配置



Intel i9发烧平台今夏升级：仍是最多18核心



受工艺和架构限制，Intel HEDT发烧级桌面平台面对AMD早已经优势不再，但升级仍然在继续。去年10月份，Intel一方面发布了第二代酷睿i9 X系列，仍然基于14nm Skylake-X架构，最多18核心36线程，延续LGA2066接口。

另一方面推出了特殊的至强Xeon-W3175X，架构也是14nm Skylake-X，但是多达28核心56线程，并有六通道内存，但因为借用了服务器上的LGA3647平台，需要特殊主板、内存支持，其中板子只有华硕、技嘉才能做到。

根据规划路线图，Intel将在今年上半年推出下一代服务器平台Cascade Lake(去年底已发货)，工艺还是14nm，但是会支持傲腾一致性内存、VNNI指令集和DLBOOST机器学习加速、修复部分熔断和幽灵安全漏洞。

它也会有个桌面发烧版“Cascade Lake-X”，从目前得到的消息看如无意外将在今年5月底开始的新一届Computex上正式发布。

它自然还是14nm工艺，具体规格暂时不详，据说最多依然只有18核心36线程，毕竟架构摆在那里，只是如此频繁连续的升级，似乎意义并不是很大，尤其是AMD的锐龙线程撕裂者已经做到了32核心64线程，而且近日还确认今年就会公布第三代。

另外在主流领域，Intel下一代很可能会升级到10核心20线程，AMD则有望提高到12核心24线程，而且有7nm工艺和Zen 2架构加持。

至于服务器领域，AMD EPYC霄龙已经奔向64核心，Intel明年的Copper Lake则依然是14nm工艺和老架构，只能通过双芯片胶水堆叠增加核心数，预计最多48个，而且很可能会换新接口，兼容后年的10nm Ice Lake。



没有上7nm制程



分布式一致性协议（Paxos/Raft/viewstamp）

[
https://blog.csdn.net/zhushuai1221/article/details/52345966](https://blog.csdn.net/zhushuai1221/article/details/52345966)

Viewstamps算法是Oki和Liskov于1988年发表的论文，Liskov是一位计算机世界中杰出的女性，08年图灵奖得主、著名面向对象五原则中“Liskov可替换原则”的提出者。我们已无精力考证Viewstamps是否是第一个多数派表决的算法，但知道其比Paxos（1998）整整早了10年，杯具的是，随着06年google chubby论文发表，Paxos迅速闻名于世，而Viewstamps依旧寂寂无闻。

ZooKeeper是一个分布式的，开放源码的分布式应用程序协调服务，是Google的Chubby一个开源的实现



﻿阿里巴巴来源自己维护的Blink(源自Flink

是分支，不是新项目



javaee的部分技术是为了跨JVM的

RMI ear包



Engineering a Compiler, Second Edition 书籍阅读

靠后面的内容不熟悉

需要学习



Guava书籍阅读

有哪些类，写demo，写笔记，记api，shardingsphere也有用



k2p无线驱动源码

https://www.right.com.cn/forum/thread-334561-1-1.html



总结ss源码进anki



shardingsphere 在win 10电脑上的资料整理



xv6



域名注册 仅供参考

https://www.hostloc.com/thread-513615-1-1.html



Vultr 家不让搭 Tor 出口节点。

大部分商家把tor节点当做滥用

vultr 大陆ip已经基本开不出能用的机器了，得用非大陆机器当跳板





MGR

MySQL Group Replication（MGR）是官方最新推出的数据复制解决方案



String是否有长度限制？

Java String类没有append方法





一种是对系统进行加密，比如引导时输入密码完成解密。另一种是对某个分区或硬盘加密，访问此分区/硬盘时，输入密码解密。所谓全盘加密的两种情形。



SIMBL hook





Dubbo可以跨局域网调用吗？

本质ip port tcp通信



Nginx如何配置白名单，配置白名单后非白名单用户访问报什么错误

分布式应用架构技术能力要求第一部分：微服务平台



cloudfoundry



xsd dtd w3c

http://www.w3school.com.cn/schema/schema_schema.asp



neofetch  A command-line system information tool

分布式事务 Seata 社区 Contributor





Cloudatcost vpn



SATA硬盘接口



豆瓣书单



看这本书之前，可以先看另外一本书《编码:隐匿在计算机软硬件背后的语言》，我也是零基础，看完这本书，再看汇编我感觉很通畅了。



这个可以看为什么java8的升级带来了interface的default method）。我觉得隐式继承在超大型的monorepo项目中是非常有帮助的，当然小型的项目可能好处不是很明显



阿里开发确实是最惨的，经常为运营和pd买单...我一直觉得，大家在计算熬不熬的时候，总是把时间这个最值钱的东西给忘记计算了...过了就是真的过了，怎么都赚不回来



技术面试，HashMap源码，支持多线程的Map有哪些？多线程用法，拒绝策略，返回值



对Spring SpringMVC源码熟悉吗？数据库索引，优化

Lock synchronized区别？



源码里面的类，要记作用，方法，最好有例子





Aop实现原理



动态生成字节码 cglib asm

spring-context包





Anki 整理关键类的使用例子



考虑一个java程序在运行的时候，是否有类图，是否能获取。



Pinpoint如何做到无入侵链路追踪，搜集了哪些信息



SVN 协议动态代理服务器

SVN 协议动态代理服务器



https://m.gitee.com/oschina/svnsrv



HashMap红黑树 jdk8，看，自己实现

先了解普通的二叉查找树和平衡查找树（AVL）树、2-3-4树



tail sed  awk more  less cat

基础不好，大厂面试都过不了





OSC源创会 / 2018讲师PPT

https://gitee.com/OSCYuanChuangHui/2018_lecturer_ppt/tree/master



mybatis generator 需要学习

UIViewController控制器

UIViewController控制器

UIViewController类包含如下常见的需要重写的方法： 

\1. - (void)viewDidLoad：——控制器管理的视图被装载完成后,系统自动调用该方法。注意：重写该方法时,记得用[super viewDidLoad]; 代码调用UIViewController基类的viewDidLoad方法。 

\2. - (void)didReceiveMemoryWarning——该方法不需程序员自己调用。如果需要在系统内存紧张时释放部分内存,可通过重写该方法来释放那些暂时不用的内存。——重写时不要忘记通过[super didReceiveMemoryWarning]方法。 

\3. - (void)viewWillAppear:(BOOL)animated——视图要显示出来时,系统自动调用该方法;重写该方法的格式注意点看下面的重要说明。 

\4. - (void)viewDidAppear:(BOOL)animated——视图显示出来后,自动调用该方法。重写该方法的格式注意点看下面的重要说明。 

\5. - (void)viewWillDisappear:(BOOL)animated——当控制器管理的视图将要隐藏或被移出窗口时,系统自动调用该方法。重写该方法的格式注意点看下面的重要说明。 

\6. - (void)viewDidDisappear:(BOOL)animated——当控制器管理的视图已经隐藏或被移出窗口时,系统自动调用该方法。重写该方法的格式注意点看下面的重要说明。 

\7. - (void)viewWillLayoutSubviews——当控制器管理的视图将要排列它包含 的所有子视图时,系统自动调用该方法。重写该方法的格式注意点看下面的重要说明。 

\8. - (void)viewDidLayoutSubviews——当控制器管理的视图已经排列它包含 的所有子视图时,系统自动调用该方法。重写该方法的格式注意点看下面的重要说明。



wrk ab htpp测试工具

安装和配置AFNetworking框架 iOS



腾讯 大连 安卓测试 充值了一百元

感觉学习没有规划，需要一份大纲

学习源码，了解原理，掌握业务 资源要close 数据库连接池



设计模式45种，六大原则

https://github.com/guanguans/notes/blob/master/%E8%AE%BE%E8%AE%A1%E6%A8%A1%E5%BC%8F%EF%BC%8845%E7%A7%8D%EF%BC%89.md



iOS委托模式 Delegate



Java rmi 继承Remote接口



Spring 深度解析例子 自定义xsd文件 有什么用？



Rust 跨文件函数调用解决了，iron绑定多个http路径，传参数 怎么解决？



Java标准库要熟悉

反射 注解 sax Collection





创建型模式 结构型模式 45种设计模式 6种原则

看书贪多嚼不烂



Java 8 接口有静态方法 接口跟抽象类对比



SPI java 1.6开始的

ServiceLoader



领域驱动模型 github 例子

架构设计方法

https://zhuanlan.zhihu.com/p/30877742





Tcp状态转换，加强记忆



二分查找需要待查找数据有序



Spring源码深度分析 Chap.5

Bean的创建过程sscope request

Redis vs code源码调试

复习redis 需要有大纲，完整的计划

https://zhuanlan.zhihu.com/p/67205845



lua脚本实现限流

redis doc

jedis

key可以是jpeg图片



jndi spi

https://docs.oracle.com/javase/7/docs/technotes/guides/jndi/index.html

jndi 容器实现mysql或者oracle 应用代码通过jdbc访问



SpringMVC配置的例子

SimpleUrlHandlerMap bean jstl引用 例子

web.xml

配置servlet listener servlet-map



redis的cluster 哨兵模式有什么区别？

https://blog.csdn.net/huang_wu_yao_xin/article/details/83988728

master-slave 避免单点故障

redis-server --port 6379 

redis-server --port 6380 --slaveof 192.168.0.167 6379 

redis-server --port 6381 --slaveof 192.168.0.167 6379

集群 slot 分布





Dubbo使用了扩展的SPI



Java.bean包



怎样查看分布式应用网络连接数，数据库连接数

Spring注解处理器

https://blog.csdn.net/jack_wang001/article/details/78781588

https://blog.csdn.net/chjttony/article/details/6301523

https://www.cnblogs.com/caogen1991/p/7911857.html



看源码，先找例子



同类型工具还有vc-mysql-sniffer，以及 tshark 的 -e mysql.query 参数来解析 MySQL 协议。



Mysql事务，数据库抓包

https://www.colabug.com/3731299.html

ngrep 源码安装

ngrep -d eth0 -W single -l port 3306|grep -E -i -w "selectegin|commit"

T 180.167.148.2:39205 -> 172.17.95.55:3306 [AP] …..begin

T 180.167.148.2:39205 -> 172.17.95.55:3306 [AP] +….select id title from t_blog where id > 134

T 180.167.148.2:39205 -> 172.17.95.55:3306 [AP] …..commit





maven 使用 BOM （bill of material）后，当依赖 Spring Framework 组件后，无需指定<version> 属性





注解的继承

@Service 继承@Compont

本文从三个方面介绍java注解的**“继承性”**：

1. 基于元注解@Inherited，类上注解的继承性
2. 基于类的继承，方法/属性上注解的继承性
3. 基于接口的继承/实现，方法/属性上注解的继承性





cpp cin cout是对象 捂脸 对应的类呢？ << >> 运算符重载了





Spring 构造器依赖



odb vs mybatis odb用法 save query？

如何处理多数据源，多个表？



Dubbo是如何把数据存在zk的

dubbo zk 客户端

Dubbo 支持 zkclient 和 curator 两种 Zookeeper 客户端实现：



注意:在2.7.x的版本中已经移除了zkclient的实现,如果要使用zkclient客户端,需要自行拓展



Spring配置文件有哪些配置项 bean

doc文档应该有 aop的配置都有



id leaf

BeanFactory vs ApplicationContext

The BeanFactory interface provides an advanced configuration mechanism capable of managing any type of object. ApplicationContext is a sub-interface of BeanFactory. It adds:

Easier integration with Spring’s AOP features

Message resource handling (for use in internationalization)

Event publication

Application-layer specific contexts such as the WebApplicationContext for use in web applications.





通过Factory 对象实例 的静态方法来创建bean

git PR其实是跟git pull类似，是合并两个仓库的信息

MySQL binlog，业务系统监控也可以基于日志

Elk也是日志





aspectj aspect关键字 IDEA如何设置

aspectj**.jar

aspectj*tools*jar



The AspectJ Language [也是一种语言，源文件缀是.aj或者是.java](https://xn--%2C-zn6aul0uu61gz2aea172o00xo2l5o3a92e.xn--aj-ng5dy3m3y4b.java/)



美团 js写iOS Android代码，写一套，兼容另外一个

python





.aj 是源文件 编译器是哪种？



Aspect4 现在是5？



SpEL是一种表达式 SS的Hint也是一种表达式



表达式语义丰富



java程序性能监控 jmc jvisualvm jps -lv



jmc 飞行记录

https://docs.oracle.com/javacomponents/jmc-5-4/jfr-runtime-guide/run.htm#JFRUH164



