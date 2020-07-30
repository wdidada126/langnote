当应用了IoC，一个对象依赖的其它对象会通过被动的方式传递进来，而不是这个对象自己创建或者查找依赖对象。你可以认为IoC与JNDI相反——不是对象从容器中查找依赖，而是容器在对象初始化时不等对象请求就主动将依赖传递给它。



同时同步多个git仓库的功能，有现成的脚本可用吗？

Android repo



SS写SC模块

近日，Sentinel 贡献的 spring-cloud-circuitbreaker-sentinel 模块正式被Spring Cloud社区合并至 Spring Cloud Circuit Breaker，由此，Sentinel 加入了 Spring Cloud Circuit Breaker 俱乐部，成为 Spring Cloud 官方的主流推荐选择之一。这意味着，Spring Cloud 微服务的开发者在熔断降级领域有了更多的选择，可以更方便地利用 Sentinel 来保障微服务的稳定性。





SC整合Spring 和其他框架，消除了配置代码，提供了默认配置，默认配置在jar包里面



Jmeter 脚本开发



「测试」 - 性能测试 & JMeter脚本开发



https://zhuanlan.zhihu.com/p/60502516



http2开源中国文章  甜橙金融



https://my.oschina.net/u/861562/blog/1823472





http2支持 包头压缩 多路复用 请求优先级 server推送 



iOS Android 如何封装sqlite



dependencies与dependencyManagement的区别



https://blog.csdn.net/liutengteng130/article/details/46991829



 在我们项目顶层的POM文件中，我们会看到dependencyManagement元素。通过它元素来管理jar包的版本，让子项目中引用一个依赖而不用显示的列出版本号。Maven会沿着父子层次向上走，直到找到一个拥有dependencyManagement元素的项目，然后它就会使用在这个dependencyManagement元素中指定的版本号。







dependencyManagement 比dependencies支持更多的功能



重点 AQS详解-CLH队列，线程等待状态



https://donald-draper.iteye.com/blog/2360256



CLH



https://blog.csdn.net/aesop_wubo/article/details/7533186



https://www.cnblogs.com/llkmst/p/4895478.html



锁持有者管理器AbstractOwnableSynchronizer

枚举值



xutils dbutils  报错 原因 深究下

锁的原因 并发

releas

close



关注推特 脸书 开发者

http://blog.didispace.com/Springboot-2-0-HikariCP-default-reason/



toml 配置文件格式



微软新项目minalloc



https://github.com/microsoft/mimalloc



ansj_seg 中文分词



Redis入门指南2



计算机程序的结构和解释



https://github.com/DeathKing/Learning-SICP



debug多线程

日志



知乎 paxos 理解

https://zhuanlan.zhihu.com/p/70439273



后端图谱

https://github.com/xingshaocheng/architect-awesome



微服务动态配置组件netflix archaius



http://techblog.ppdai.com/2018/05/08/20180508/



Java 源码 面试题

1、你看过那些源码吗？

2、那你能讲讲HashMap的实现原理吗？

3、HashMap什么时候会进行rehash？

4、HashMap什么时候会进行扩容？

5、那HashMap的初始容量设置成多少比较合适呢？

6、结合源码说说HashMap在高并发场景中为什么会出现死循环？

7、JDK1.8中对HashMap做了哪些性能优化？

8、HashMap和HashTable有何不同？

9、HashMap 和 ConcurrentHashMap 的区别？

10、ConcurrentHashMap和LinkedHashMap有什么区别？

11、为什么ConcurrentHashMap中的链表转红黑树的阀值是8？

12、什么是ConcurrentSkipListMap？他和ConcurrentHashMap有什么区别？

13、还看过其他的源码吗？Spring的源码有了解吗？

14、SpringBoot的源码呢？知道starter是怎么实现的吗？



apache common源码分析

deploy android ios app

https://fastlane.tools

TiKV用于存储真正的数据，TiKV由分布在不同机器上的RocksDB实例组成。

泛型的几种写法

https://blog.csdn.net/ShierJun/article/details/51253870



dfs

非递归还是有点麻烦，一般要用到栈或者队列……有些递归实现easy的，非递归就改hard了

保存中间状态



VirtualXposed，让你无需Root也能使用Xposed框架！



https://blog.csdn.net/moon_nife/article/details/91346067



mysql Communications link failure

mysql 连接错误





自定义注解 开发

Hystrix提供的断路器具有自我反馈和自我恢复的功能，Hystrix会根据接口调用的情况，让断路器在closed,open,half-open三种状态之间自动切换。  open状态表示打开熔断，即服务消费者执行本地设置的降级策略，不再调用服务消费者。 closed状态表示关闭熔断，此时服务消费者直接调用服务提供者。 half-open状态，这是一个中间状态，当断路器处于该状态时，服务消费者直接调用服务提供者。



Guide to Assembly Language Programming in Linux - X-Files

复习谢龙学习路线

远程调试 debug



shell



Leetcode每日一题 有序矩阵

https://blog.csdn.net/arkblue/article/details/50974957



**maven跳过单元测试-maven.test.skip和skiptests的区别**

-DskipTests，不执行测试用例，但编译测试用例类生成相应的class文件至target/test-classes下。



-Dmaven.test.skip=true，不执行测试用例，也不编译测试用例类。





Spring读取properties文件作为环境变量



https://dacoolbaby.iteye.com/blog/2047579



sum-root-to-leaf-numbers

https://www.cnblogs.com/springfor/p/3884038.html





复习mysql语法

https://dev.mysql.com/doc/refman/5.7/en/alter-database.html



https://dev.mysql.com/doc/refman/5.7/en/entering-queries.html



用正则表达式如何获取一篇文章某个单词是否只出现一次，如果出现2次，那么代表不匹配 请指教



delay ack



https://en.wikipedia.org/wiki/TCP_delayed_acknowledgment



画活动图



github算法项目

https://zhuanlan.zhihu.com/p/72740942

https://github.com/algorithm-visualizer/algorithm-visualizer



头条 java面试

https://mp.weixin.qq.com/s?__biz=MzUzMTA2NTU2Ng==&mid=2247487240&idx=1&sn=fccd13db7146ccf9304a25c2012498a2&pass_ticket=25hIANlGbBIXI%2FY6LGoLl0aIpizEUYQ4%2FeWB36q7jS3c8inYNcvCcGO3aOH3L%2B71





干货总结下



数据库范式的存在,是为了关系运算的



开源网关实现?内网,公网,测试,生产网络,是不是网关在起作用?



2019 最前沿的几个 Flutter 实践：微信、咸鱼、美团

https://mp.weixin.qq.com/s?timestamp=1562813570&src=3&ver=1&signature=vAVg9KHAKy5bkgZgLs8I9ihYX5a0sge7I*qxpNnRoxDmMGkuVwQ3hLVXEFZGf0LpFt7QOhHK0PeqWRrDyKQZy*-CZHoVGoBTZToyQtK8gsPLqD3h68hHobpeYzQnBZ8iEyNNNj9HudYXk75jxuPRepc9PIUxKzj7sxeJ0wNDRY0=





多参加IT比赛



Java github page

wangkuiwu.github.io



上海2019下半年软考报名



8月13日至8月28日



互联网场景下的网关

知道一个gateway

还有啥，忘了

zuul

kong



真正大公司的一线产品，移动端就是移动端，PC端就是PC端，WEB端就是WEB端

leetcode maximal-square

题号 [221] Maximal Square

题目描述：

在一个由 0 和 1 组成的二维矩阵内，找到只包含 1 的最大正方形，并返回其面积。

示例:

输入: 

1 0 1 0 0

1 0 1 1 1

1 1 1 1 1

1 0 0 1 0

输出: 4



https://leetcode-cn.com/problems/maximal-square/



processon帮助中心

https://www.processon.com/support/question/5b190327e4b0e2754666eb83



甜橙金融后端产品

https://www.jianshu.com/p/d1d5c50a90f6

数据分析



Soloπ 自动化测试工具

https://github.com/alipay/SoloPi



考虑一个双人游戏。游戏在一个圆桌上进行。每个游戏者都有足够多的硬币。他们需要在桌子上轮流放置硬币，每次必需且只能放置一枚硬币，要求硬币完全置于桌面内（不能有一部分悬在桌子外面），并且不能与原来放过的硬币重叠。谁没有地方放置新的硬币，谁就输了。游戏的先行者还是行者有必胜策略？这种策略是什么？



curl argument list too long

https://stackoverflow.com/questions/54090784/curl-argument-list-too-long



rz,sz

Facebook 于前日发布了新的 JavaScript 引擎：Hermes，专注于提高 React Native 应用的性能

tail -f



logging打印日志需要设置格式

pdb python db

SpringMVC接收参数的几种方式

跨语言id追踪

网络协议？



Docker分布式部署，日志在一个文件

刷leetcode

Beyond Compare软件比较两个文件夹的差异



Duilib是一个Windows下免费开源的DirectUI界面库



Project和Module的区别是：Project相当于是Eclipse中的Workspace，Module相当于是我们Eclipse中的工程。

Project pom



二进制文件格式，如何读写二进制文件



java导出pdf xlsx



百亿流量微服务网关的设计与实现

https://www.infoq.cn/article/EeE1xZeic4UdpbmR*03t



Jira项目管理的

524.longest-word-in-dictionary-through-deleting



MySQL索引及其SQL优化

https://blog.csdn.net/weixin_39704652/article/details/92020129



如何保证消息不被重复消费？或者说，如何保证消息消费的幂等性

幂等



执行一次和N次没有区别



例子

*1

*0



graphql论文

是在http的基础上加语义



mysql源码阅读

没看过MySQL，但是看过PostgreSQL，说一点经历吧。

首先，一定要对SQL语法语义熟练。比如除了select，update，insert，delete，create以外，还要熟悉with 语句的语义与使用场景，各种join的语义，view与table的区别与联系，等等。因为源码里有些变量名字是缩写，不懂语义是完全记不清的。这一条很重要，但学习方法也很简单，找本书敲例子就行，或者跟踪官网例子敲一遍。

其次，要有架构感。一，如果不存在并发，一条SQL语句，是如何经历语法解析，语义检测，语义优化后得到怎样的执行树，然后执行树是怎样执行，如何存取文件（文件格式，行数据如何解析等）；二，再考虑是如何实现并发执行时候的ACID。把并发单独抽取出来好处是不容易被绕晕头。

还有，要带着目标去研究。不要为了学习而看开源代码，看源码是很枯燥的事情，特别是C/CPP写的开源软件都带了很多底层实现细节，很容易就绕进去暗无天日。可以带着独立的问题去研究，比如数据是怎么在磁盘存储的，存储格式是怎样，怎样解析一条记录；比如SQL是解析成什么样的语法树节点，语法树又是如何进行语义检测，语义检测之后都做了什么语义优化；执行树是如何表示的，怎样执行的；ACID是怎样实现的，都提供了几种隔离级别，版本控制在内存或者磁盘数据上是如何表示以及实现的，redo，undo是怎样实现的，是怎样利用日志来完成持久性以及数据恢复的等等。

再补充一点吧，要是有源码分析的书籍，可以先看一遍，挑一个论题深入看透，然后看源码做笔记，再使用debug工具（最好是可视化IDE，gdb 很容易就搞得屏幕花脸，虽然我习惯gdb了）跟踪。



如何以最快的速度找到链表中倒数第N个元素



DisposableBean



beans包



随意丢弃的



Destory()方法



ThreadLocal

面试题



https://www.jianshu.com/p/377bb840802f



key是ThreadLocal对象 value值



内存泄漏



强引用



remove



tidb 美国办事处

HotDB Server

兼容主流数据库协议和 SQL92/SQL99标准语法



如何快速学习新的中间件？

先用，看文档，编译，修改，订阅开发者邮件



CephFS

docs..com/docs/master/cephfs/



我有bgp，未来还会部署iplc



dfs 深度优先 非递归



sourcegraph github辅助插件 cpp 类定义直接跳转



p-impl 编程范式 tc++pl 书籍



冒号课堂 编程范式

https://book.douban.com/subject/4031906/



十大经典排序算法动画与解析，看我就够了



https://mp.weixin.qq.com/s/vn3KiV-ez79FmbZ36SX9lg





LeetCodeAnimation



https://github.com/MisterBooo/LeetCodeAnimation



https://dev.mysql.com/doc/refman/5.7/en/optimizing-innodb-bulk-data-loading.html



确实，但更多的东西（eda工具，工业系统这些）还没人贡献出来



CountDownLatch构造函数



MySQL date相关内置函数



逻辑题  题目描述:  房子有三盏灯，屋外有三个开关，分别控制这三盏灯，只有进去房间，才能看到哪一个灯是亮的。请问如何只进一次房间，就能指明哪一个开关控制哪一个灯？



十大经典排序算法动画与解析，看我就够了





https://mp.weixin.qq.com/s/vn3KiV-ez79FmbZ36SX9lg



分布式事务



分布式存储

分布式计算

MAC压缩就是zip

**秒杀系统设计与实现.互联网工程师进阶与分析**



一款入门级的人脸、视频、文字检测以及识别的项目

https://github.com/vipstone/faceai



MySQL Select 正则表达式

walle 安卓渠道打包

https://github.com/Meituan-Dianping/walle



Scripting for the Java™ Platform jsr233



ACTS 测试工具包

https://github.com/sofastack/sofa-acts



spring boot redis分布式锁



spring boot redis分布式锁

https://zhuanlan.zhihu.com/p/32660563



git删除分支

首先使用 git branch -d bugfix01对分支 bugfix01 进行删除。

然后使用 git branch -d bugfix02 对分支 bugfix02 进行删除。

操作上来看对分支的删除只是删除的指向该commit号的指针，并不会删除其相关的提交号, 在日志中仍然可以找到之前的commit记录，也仍然可以在该commit上创建新的分支。如果你想删除远端的分支的话，那么得使用 $ git push origin --delete <分支名> 了。



dachengxi个人github主页



https://github.com/dachengxi/dachengxi.github.com



Dubbo开发调试方法



本地直连，不经过zk等注册中心



multify



dubbo-resolve.properties 本地调试

https://blog.csdn.net/blissnmx/article/details/52808858





https://blog.csdn.net/hardworking0323/article/details/51166113



编译原理之美 手把手教你实现一个编译器 宫文学 北京物演科技CEO

Jetty8 网页编码



text/html = ISO-8859-1

text/plain = ISO-8859-1

text/xml = UTF-8

text/json = UTF-8



https://www.cnblogs.com/fairjm/p/jetty-8-default-character-encoding.html



测试json好像也不对



为什么这些年网线不直接是光纤而是rj45呢?

光纤易折



Apache ShardingSphere 数据脱敏全解决方案详解

https://www.infoq.cn/article/tk9gMjP6geOKOy-BTisX



Yandex 邮件服务提供商

老牌产品：sendmail 或新秀：postfix



MySQL性能优化之max_connections配置参数浅析

https://blog.csdn.net/dyf511860475/article/details/52710181



Caffeine java缓存



潘娟 ss 加密功能实现 需要仔细看

感谢 gitHub ID @betterjava 贡献的优秀Pr, 主要对脱敏数据源的元数据信息展示进行了修复和优化🎉

https://github.com/apache/incubator-shardingsphere/pull/2934



🎁 欢迎大家有空做社区任务练手~



内置 预置app 安卓 区别

说到人工智能技术，人们首先会联想到深度学习、机器学习技术；谈到人工智能应用，人们很可能会马上想起语音助理、自动驾驶等等，各行各业都在研发底层技术和寻求AI场景，却忽视了当下最时髦也很重要的AI技术：知识图谱。  当我们进行搜索时，搜索结果右侧的联想，来自于知识图谱技术的应用。我们几乎每天都会接收到各种各样的推荐信息，从新闻、购物到吃饭、娱乐。



记得写日报

上周 curl 的首席开发人员 Daniel Stenberg 在个人博客上发布：他首次通过 HTTP/3，用 curl 命令成功发送了一个文件。



详细信息请查阅： https://daniel.haxx.se/blog/2019/08/05/first-http-3-with-curl/



go分包

https://github.com/golang-standards/project-layout



Http协议 req rep一对一，其他协议不是的

raft cn

https://github.com/maemual/raft-zh_cn



Jvm classloader 父类子类不一样

https://blog.csdn.net/hbyxly/article/details/33361663



dubbo与spring整合 只有一个jar包，但是有相关代码



https://blog.csdn.net/chinabestchina/article/details/76166948



四、dubbo服务在zookeeper存储格式



1、/dubbo



这是dubbo在zookeeper上的根节点



2、/dubbo/com.dragon.study.dubboService.service.HelloService



这是服务节点，代表一个服务，这里即是自定义的HelloService服务



3、/dubbo/com.dragon.study.dubboService.service.HelloService/providers



服务提供者的节点，子节点代码服务真正的提供者



4、/dubbo/com.dragon.study.dubboService.service.HelloService/consumers



服务消费者的节点，子节点代码服务真正的消费者



https://blog.csdn.net/chinabestchina/article/details/76166948



聚集索引 innodb

https://blog.csdn.net/u012006689/article/details/73195837



Innodb自动维护

有主键用主键，没主键，用非空，没非空，自建列



数据全部存在跟节点



Log4j2 利用插件系统，使得扩展新的appender,filter,layout等变得容易

两个线程，交替打印奇偶数

Object synchronized wait nitifyAll



华为方舟编译器 俄罗斯人开发

上周，搜狗在GitHub低调发布了机器阅读理解工具包SMRC（Sogou Machine Reading Comprehension）。 这是目前业内最全的TensorFlow版本的阅读理解工具集合，从相关数据集的下载到最后模型的训练和测试，一应俱全。 搜狗此次开源的目的也是为了帮助NLP从业人员快速实现已有的机器理解模型，从而更高效地开发新模型。 近两年来，NLP领域取得了许多突破性进展。但是在机器阅读理解方面开源的资源还是非常少。目前在CoQA上“打榜”的选手中，只有搜狗和微软公开了源代码。

spring 源码分析

https://github.com/seaswalker/spring-analysis



面试题：JAVA Hashmap的死循环及Java8的修复

面试题：JAVA Hashmap的死循环及Java8的修复



https://mp.weixin.qq.com/s?__biz=MzI3MjUxNzkxMw==&mid=2247483769&idx=1&sn=7ea154f52cbf19777f44ad23002f06e6&chksm=eb301f0fdc4796196e3d2df5adf80ddb195a9efef134cfb38e4e05df66c9fbc5a867a6469af1&scene=21#wechat_redirect



防止破解，用c cpp开发 授权文件

Cmu

Lincense key



code academy 的python课程蛮好

极客时间 shell编程

应该得ldconfig一下吧

贴个错误信息出来看看吧，实在不行像 LaTex 那样提供一个 MWE。有个具体的错误输出可能会更好一点。



javah

dubbo负载均衡是如何实现的

https://www.cnblogs.com/luozhiyun/p/10963116.html



Dubbo group分组

对接多类型的个provider，提供一样的接口，但是不同的数据源



fastdfs 客户端

<dependency>

 <groupId>org.csource</groupId>

 <artifactId>fastdfs</artifactId>

 <version>1.2.4</version>

 </dependency>



mybatis 开发 “三剑客”

https://blog.csdn.net/wuseyukui/article/details/79497723

Java function 异构语言用到了

SPI 详解
阿里熔断限流Sentinel研究
https://www.hellojava.com/a/82317.html



需要考虑跟dubbo结合

Kfaka异步
rpc rmi区别


基于 Redis 的分布式锁
https://segmentfault.com/a/1190000014128432

