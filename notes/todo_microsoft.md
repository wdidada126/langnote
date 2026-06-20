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


jetty 部署原理 IDEA 设置war文件绝对路径

Jetty部署 https://blog.csdn.net/tomato__/article/details/28874805



IDEA jetty端口修改 https://my.oschina.net/pengzai/blog/130797

加大IT技术文档英语阅读量

拿社保卡，激活储蓄功能，搞定6位数查询密码

ltp4j
https://github.com/HIT-SCIR/ltp4j

JMX
Java Management Extensions (JMX)

多交流吧，毕竟自己不是最先进的了

JMS
https://en.wikipedia.org/wiki/Java_Message_Service
阿里云账号申请

Java8 接口，默认方法 Default Methods
https://ebnbin.com/2015/12/20/java-8-default-methods/

Servlet要搞清楚业务流程，然后再记类

lock free算法
CAS ABA



http://novoland.github.io/%E5%B9%B6%E5%8F%91/2014/07/26/Lock-Free%20%E7%AE%97%E6%B3%95.html

离散数学在计算机科学中的应用
离散数学在计算机科学中的应用



https://blog.csdn.net/xyisv/article/details/79245952

Log4j2架构图
Spring View 记子类  ViewResolve
判断一个整数是否是回文数。回文数是指正序（从左向右）和倒序（从右向左）读都是一样的整数。  示例 1:  输入: 121 输出: true 示例 2:  输入: -121 输出: false 解释: 从左向右读, 为 -121 。 从右向左读, 为 121- 。因此它不是一个回文数。 示例 3:  输入: 10 输出: false 解释: 从右向左读, 为 01 。因此它不是一个回文数。 进阶:  你能不将整数转为字符串来解决这个问题吗？

hc
熟悉MySQL数据库结构、数据结构设计、性能调优和日常故障解决方法

熟悉MySQL主从复制，读写分离、分库分表设计，熟悉mariadb等MySQL各分支的区别和特性



了解主流开源存储系统原理，如HBase，RocksDB，LevelDB，Ceph等，对源码有研究者优先

有线上高并发，高性能，低延迟系统开发经验者优先

有国际一流系统会议：ODSI，SOSP，USENIX ATC, USENIX FAST, VLDB，SIGMOD，EuroSys，



会计 CPA

cat 日志监控
https://github.com/dianping/cat

Jwt记不住，因为没跑例子
Redis要加强 基本数据类型 二进制 过期时间 哨兵模式
	消息中间件面试题：如何保证消息不被重复消费

消息中间件面试题：如何保证消息不被重复消费



https://blog.csdn.net/weixin_34111819/article/details/87770104



因为这问题通常不是 MQ 自己保证的，是由我们开发来保证的。挑一个 Kafka 来举个例子，说说怎么重复消费吧。

leetcode 121
https://mp.weixin.qq.com/s?__biz=MzA3MjU5NjU2NA==&mid=2455501947&idx=1&sn=dd08b2f7b955e4c4b5007f248b3ba6ca&chksm=88b4b140bfc338568ae56600f5e7ba22fb7d6bb694a700327eb637cc118b93edc6902ca48505&mpshare=1&scene=1&srcid=&sharer_sharetime=1564101539595&sharer_shareid=887d04566c34e5f38ff4fd051a5b689e&key=bc8c7e003d0328abc7ad8d28fc886876a41565ddfb346eec5ba570f3bd420c207fc3d8dde390226c0004bc30938cf101f2cd7c0cdb363b53a8a4f00bb4692a22fd3e0e3bab41301c260c47b80ea3160a&ascene=1&uin=MjY1MTA3MzYyMQ%3D%3D&devicetype=Windows+10&version=62060833&lang=zh_CN&pass_ticket=f6hmhg8QwiIjbur9EfvfTFJIFZ5g6opdM2V5meBJMhWFUJIkPdwS3awXQyOZXAWl

tpcc mysql测试
TPC(Tracsaction Processing Performance Council) 事务处理性能协会是一个评价大型数据库系统软硬件性能的非盈利的组织,TPC-C是TPC协会制定的，用来测试典型的复杂OLTP系统的性能。Tpcc-mysql是percona基于tpcc衍生出来的产品，专用于mysql基准测试，其源码放在bazaar上，因此需要先安装bazaar客户端。



https://yq.aliyun.com/articles/131187



https://github.com/Percona-Lab/tpcc-mysql

BAT如何处理相同的数据
MySQL 索引 B+树
https://mp.weixin.qq.com/s/fR1a6yu1MfoZLov2xSwgsQ



局部性原理与磁盘预读

消息中间件面试题：如何保证消息不被重复消费

aries算法
https://my.oschina.net/fileoptions/blog/2988622


人人都是 API 设计者：我对 RESTful API、GraphQL、RPC API 的思考
https://www.infoq.cn/article/ZgAAVBZZaoo4I0-pkgV8

mysql Jeremy Cole
mysql 索引有哪些？
https://blog.csdn.net/qq_27388039/article/details/79647887



https://blog.csdn.net/u012006689/article/details/73195837



https://blog.csdn.net/u012006689/article/details/73195837


关于InnoDB优化，在《高性能Mysql》里有更加全面的介绍
解决幂等 思路

mysql 索引有哪些？

Spring Cloud项目之间是如何是实现调用的
我感觉应该不用记调用链那些。tcp是协议，代码是协议实现，不是一个维度 个人推荐重点还是从tcp的那四个timer各自作用来理解tcp协议会比较没那么痛苦

todo字节跳动 分布式 头条 三大算法
Mysql工具测ss
ss测试官方代码
https://github.com/OpenSharding/shardingsphere-acceptance-test

公司内部使用消息队列实现分布式事务，查相关资料，咨询阳哥

求数组中第k大的数的题
求数组中第k大的数的题

题目描述：

在未排序的数组中找到第 k 个最大的元素。请注意，你需要找的是数组排序后的第 k 个最大的元素，而不是第 k 个不同的元素。

示例 1:

输入: [3,2,1,5,6,4] 和 k = 2

输出: 5

示例 2:

输入: [3,2,3,1,2,4,5,5,6] 和 k = 4

输出: 4

说明:

你可以假设 k 总是有效的，且 1 ≤ k ≤ 数组的长度。

题目链接： https://leetcode-cn.com/problems/kth-largest-element-in-an-array/

false sharing(伪共享)

所谓的“广域网负载均衡”（跨地域负载均衡） >>这个是自己配置，还是依赖于运营商呢

Disruptor 无锁队列
http://lmax-exchange.github.io/disruptor/

java  如何打印当前程序运行堆栈信息


supervisor
http://liyangliang.me/posts/2015/06/using-supervisor/

学习无鼠标操作电脑
ShardingSphere微信1群讨论SPI
SPI ss是原生

Dubbo上是修改的

数据库 异地多活
OB
多活架构


数据库指标 RTO
https://blog.51cto.com/se7en/1085442

Leetcode链表总结
https://blog.csdn.net/wonner_/article/details/79766037

数据库 XA协议 分布式规范
XA协议包括两套函数，以xa_开头的及以ax_开头的

MySQL索引的创建、删除和查看
https://www.cnblogs.com/tianhuilove/archive/2011/09/05/2167795.html

Redis阻塞访问，非阻塞访问

Java Logger
https://bryantchang.github.io/2018/07/19/log4j2-code-1/

在查询语句后面增加for update，数据库会在查询过程中给数据库表增加排他锁（这里再多提一句，InnoDB引擎在加锁的时候，只有通过索引进行检索的时候才会使用行级锁，否则会使用表级锁。这里我们希望使用行级锁，就要给method_name添加索引，值得注意的是，这个索引一定要创建成唯一索引，否则会出现多个重载方法之间无法同时被访问的问题。重载方法的话建议把参数类型也加上。）

虽然我们对method_name 使用了唯一索引，并且显示使用for update来使用行级锁。但是，MySql会对查询进行优化，即便在条件中使用了索引字段，但是否使用索引来检索数据是由 MySQL 通过判断不同执行计划的代价来决定的，如果 MySQL 认为全表扫效率更高，比如对一些很小的表，它就不会使用索引，这种情况下 InnoDB 将使用表锁，而不是行锁。如果发生这种情况就悲剧了。

基于缓存实现分布式锁
JUnit Spring test testng原理
在本地开启了一个socket

ubuntu 16 ss命令行版本不工作了

再见linux kernel source，open jdk source code,android open source code，I try to love Java application code for ever!
Log4j2 多个文件怎么压缩
怎么配置输出格式

怎么



https://blog.csdn.net/u010597819/article/details/92429838


Log4j2 插件 spi优劣

tgockel-zookeeper-cpp
tgockel-zookeeper-cpp



https://www.findbestopensource.com/product/tgockel-zookeeper-cpp

没有保持好的读书习惯，阅读新书，复习读过的书籍 温故知新

多看书，分布式协议 dubbo序列化 ss代码

Mabatis Generator源码
美团线上有基础平台用zgc，直接上的12

Java 教程



http://how2j.cn/?p=81319/ 

Paxos，Raft，2PC，3PC等等，在这讲一种协议，ZAB 协议

如果你是技术岗，问你这些其实没啥问题。原理真不难，写出来难。理解多线程的底层实现(这个面试的时候很多人都是背博客，其实都是有问题的)和虚拟机原理是大有好处的。我觉得高阶程序员手撕一个依赖注入和虚拟机(不用对应所有jvm bytecode，有栈有算数逻辑跳转有GC就够了)应该是基本功。

大学体系结构课是用FPGA实现支持简单指令集的pipeline cpu.  但是我甚至不会用简单指令集实现快速排序… 我觉得挺正常的

写了五年代码了，还没见过用rb树的。c#的sorteddictionary里面用了rb树，但是基本不用这个数据结构啊

人脸识别，旷视。  语音识别，讯飞。  情感识别，依图。

推荐大家去读《A Tour of C++》第二版，英文版在2018年6月出版。（译注：Oreilly会员可以直接读）本书包括了C++17以及C++20的内容，是最近相当全面的C++17的特性指南。


Leetcode 个人题解
https://github.com/hqztrue/LeetCodeSolutions

https://github.com/azl397985856/leetcode

协程 cpp

Jdk8后续版本新特性
https://mp.weixin.qq.com/s/BDJhcoY0DK03cuCMfA-KAQ

mysql B +树源码

IsRoot isLeaf boolean值

两个指针

左右节点

孩子节点

Java io包需要强记

我们去更加深入的理解什么是计算机。给计算机建立模型。  所以，形式语言就应运而生了。其中最基础的就是自动机(automata)。它可以将很多的东西抽象话， 也让我们更加了解一些简单的程序。

Leetcode题解
https://zhuanlan.zhihu.com/c_213492055

二叉树中序遍历，取最大的K个值
javap 查看class文件
多API支持：log4j2提供Log4j 1.2, SLF4J, Commons Logging and java.util.logging (JUL) 的API支持

插件架构： Log4j使用插件模式配置组件。因此，您无需编写代码来创建和配置Appender，Layout，Pattern Converter等。Log4j自动识别插件并在配置引用它们时使用它们。

微软 cpp library http

https://github.com/Microsoft/cpprestsdk 

ICML或CVPR ECCV、CVPR、AAAI、ICML

cpp代码 configure generate compiler
阿丙的博客园

https://www.cnblogs.com/acm-bingzi/category/468280.html

同感，spp框架是很不错，但是源码一坨翔
http://www.pianshen.com/article/4844349025/



https://blog.csdn.net/mijichui2153/article/details/89291390

收购奇妙清单之后，微软在几年前推出了这款全新的任务清单工具——Microsoft To-Do，现在，你可以在你的 Windows10 系统、苹果、安卓，以及网页端同时使用。

算法、自动机理论、形式语言、可计算性理论之间都是什么关系
矩阵 数学基础
矩阵 数学基础



https://www.zhihu.com/question/338548610/answer/796325582?hb_wx_block=1

http://mysqllover.com/

tidb



Slack

MySQL内核：InnoDB存储引擎 卷1

Write-Behind Logging 论文介绍 数据库相关

Write-Behind Logging 论文介绍



https://zhuanlan.zhihu.com/p/47369609

cmake小记 多个cmakefile.txt

https://zhuanlan.zhihu.com/p/51391675

Cmake 单元测试
二叉树 中序遍历 排序效果
主机有多个cpu
JVM回收机制
JMM 是围绕着在并发过程中如何处理原子性、可见性和有序性这 3 个特征来建立的
Happens-Before  JMM 为程序中所有的操作定义了一个偏序关系，称之为 Happens-Before。

Java内存模型
JVM内存结构，和Java虚拟机的运行时区域有关。 Java内存模型，和Java的并发编程有关。 Java对象模型，和Java对象在虚拟机中的表现形式有关。



https://www.zhihu.com/question/64586462/answer/576543433?hb_wx_block=1

Servlet同步阻塞模型 一个请求一个线程
db Schema 个人理解不透彻
Spring中解析xml格式配置文件使用的工具 dom org.w3c.dom.Element
Spring scope 范围 余地 视野
<bean id="role" class="spring.chapter2.maryGame.Role" scope="singleton"/>

这里的scope就是用来配置spring bean的作用域，它标识bean的作用域。

在spring2.0之前bean只有2种作用域即：singleton(单例)、non-singleton（也称 prototype）, Spring2.0以后，增加了session、request、global session三种专用于Web应用程序上下文的Bean。因此，默认情况下Spring2.0现在有五种类型的Bean。当然，Spring2.0对 Bean的类型的设计进行了重构，并设计出灵活的Bean类型支持，理论上可以有无数多种类型的Bean，用户可以根据自己的需要，增加新的Bean类 型，满足实际应用需求。

Spring注解处理器
https://www.jianshu.com/p/acd1565510e3

三年经验连表单校验都不知道是啥。这种人我都想抽他。
http://09x.ant.design/components/validation/

motan
https://github.com/weibocom/motan/issues/539

嵌套虚拟化
如何让junit的测试跑多次
https://blog.csdn.net/lantianjialiang/article/details/82811704

springmvc 定时任务
多线程 要测试熔断限流 如何实现在特定时间内执行任务多少次
https://zhuanlan.zhihu.com/p/67069088

分布式测试senselink resilinece4j
c++编译慢是事实，但是大规模项目不是应该分模块独立编译么？比如chromiun
你想的太简单了，做后端需要考虑的有很多，不只是Orm什么，你有了简单的Http后，你还要考虑是否支持REST，考虑CORS，考虑权限认证，考虑Health Check，考虑数据库连接池，考虑监控系统的集成，还有常见的工具集成，比如Swagger，常见中间件集成，比如Redis。这都还是只考虑你单机部署，如果你起成集群，或者做微服务什么的就更复杂了，而这些都是框架的工作，而不是你的工作，浪费时间去开发这些得不偿失

MyCat2
https://github.com/MyCatApache/MyCat2

高并发系统设计 40 问 极客时间

thesis.pdf zab raft
https://ramcloud.stanford.edu/~ongaro/thesis.pdf

http://www.tcs.hut.fi/Studies/T-79.5001/reports/2012-deSouzaMedeiros.pdf

C++ 的 std::string 有什么缺点



https://www.zhihu.com/question/35967887/answer/800711658?hb_wx_block=1

MQ解偶 异步 削峰 事务

系统可用性降低:

你想啊，本来其他系统只要运行好好的，那你的系统就是正常的。

现在你非要加个消息队列进去，那消息队列挂了，你的系统不是呵呵了。因此，系统可用性降低

系统复杂性增加:

要多考虑很多方面的问题，比如一致性问题、如何保证消息不被重复消费，如何保证保证消息可靠传输。

因此，需要考虑的东西更多，系统复杂性增大。

但是，我们该用还是要用的。



https://zhuanlan.zhihu.com/p/84007327

https://blog.csdn.net/weixin_43970890

交换机 隔离广播域 交换机 路由器 区别

Banzai Cloud这家来自匈牙利的公司很有意思，我从2018年初就开始关注，他们的每次分享都能准确得戳中G点，这应该是他们在中国的首秀，明天上午10点云栖大会C101，How to fail with service mesh？分享的内容就是这篇博客Announcing Banzai Cloud automated service mesh, Backyards - Istio the easy way，https://banzaicloud.com/blog/istio-the-easy-way/

以实时游戏服务器的角度看，首先建议学习高性能网络库Raknet，这个库仅专注于高性能的传输协议，可以认为是一种“可靠UDP”协议，没有涉及其它方面。历史较久综合评价较高，值得推荐。  至今我觉得actor仍是高性能游戏服务器的王道思路，有了actor模型，对游戏服务器来说很多其它复杂的并发概念都可以不用看了。而且actor用很少的代码就可以做出相当完美的实现，强烈推荐skynet框架（用C+Lua编写）。

被loki库带坏的, 太学院派了

《领域驱动设计》作者 Eric Evans 在 Explore DDD 主题演讲会上呼吁与会者积极参与改进用于复杂系统的建模和设计语言。

8cc c编译器
https://github.com/rui314/8cc

苦归苦，但是我也特别感谢这四年，作为一个计算机的从业人员，这四年扎实的基础和磨练，真的是受益终身的，工作也有好几年了，这些年面试和招聘的新人有3位数了，我发现能够在大学期间帮学生打好这样的或者差不多点基础的学校，真是全中国都超不过10家。

ss的流量特征早就被识别了，然后依然没有不ban掉。这就是上边的态度了。最近换策略了，对ip间歇性的干扰，什么方案都是这样。无差别攻击的感觉

Dubbo admin 屏蔽一个节点

有两条路可以走，一条是学习一门函数式语言如Haskell，F#来感受函数式编程，另一条路则枯燥和深入一些，需要看一些专业的书籍和论文，比如从计算模型开始，如lambda演算，讲归约机的论文等，到类型论，域论，范畴论等，这个就深坑了。

中石油 60+核100G

通过了SUN Java（SCJP、SCWCD、SCBCD）及Oracle OCA等认证

InfoQ：我们知道阿里内部现在基本上没有在使用 Dubbo，而是用了 Dubbo 开发的第三代 RPC 服务框架 HSF（High-speed Service Framework），那现在还将 Dubbo 重启维护，大家不免疑惑。  罗毅：Dubbo 和 HSF 都是阿里巴巴集团自研的 RPC 服务框架，在不同时期都很好的支持了集团业务的发展。目前，HSF2 主要服务于集团内部业务，而 Dubbo2 主要以开源的形式服务社会，它们之间的关系与 Google 内部使用的 Stubby 和开源的 gRPC

深入理解Apache Dubbo与实战

ubuntu 16 连接企业wifi，总是提示输入账户密码，百度解决

Eclipse 基金会正努力使开发人员更容易构建云原生应用程序。为此，它成立了 Eclipse Cloud Development Tools 工作组。该小组是一个与供应商无关的开源组，将专注于云的开发工具。其创始成员包括 Broadcom、IBM、RedHat 和 SAP 等。

https://github.com/liqiangit/maven-in-action
https://github.com/spotify/dockerfile-maven  docker-maven-plugin弃用了


2016年，百度宣布PaddlePaddle开源，这标志着国内第一个开源深度学习平台的诞生。

跟国外比 不行
另外一篇比较新的论文Scotty: Efficient Window Aggregation for out-of-order Stream Processing，其在2018年柏林的Apache Flink Forward会议上面进行过presentation，网上可以找到相应的PPT和视频，讲得很好，未来可能会增加到Flink中，推荐了解了解！  IBM研究院发表了一篇相关的教程，类似于综述，非常推荐，链接为link，或者直接google：Tutorial: Sliding-Window Aggreg

动手学深度学习
https://github.com/d2l-ai/d2l-zh


激活码，激活码只用于尝试 VisualStudio 的使用，请不要在商业环境使用  Visual Studio 2019 Enterprise  BF8Y8-GN2QH-T84XB-QVY3B-RC4DF  Visual Studio 2019 Professional  NYWVH-HT4XC-R2WYW-9Y3CM-X4V3Y

java null的String变量和一个非nullstring变量相加 有个null在里面，需要写示例程序

gradle多模块打jar，上传本地仓库，并给本地其他项目使用
https://blog.csdn.net/cradle2006/article/details/95072540

整体架构还是DDD的四层架构：UserInterface-接口层，Application-应用层，Domain-领域层和Infrastructure-基础设施层。

基于 DDD 的微服务设计和开发实战
https://www.infoq.cn/article/s_LFUlU6ZQODd030RbH9

注释版muduo
https://github.com/chenyahui/AnnotatedCode/tree/master/muduo

Java日志框架演化历史
https://zhuanlan.zhihu.com/p/86249472

Cmake 分模块，静态库，动态库
Gradle，分模块，Spring源码是如何组织的

可以说都是代码静态分析工具，但侧重点不同。pmd：基于源代码分析，主要面向安全编码规则，如“避免声明同名变量”，包括风格类、类型使用等等，具备一定的数据流分析和路径分析能力。checkstyle：基于源代码，与pmd类似，但更侧重编码的语法风格，分析深度不及pmd。findbugs：基于字节码分析，大量使用数据流分析技术，侧重运行时错误检测，如空指针引用等，分析深度大于前述两个。sonar：定位是代码质量平台，本身不进行代码分析，但可以集成各个静态分析工具以及其他软件开发测试工具，并基于集成工具的结果数据

Office 2019 for Mac 下载和激活
https://zhuanlan.zhihu.com/p/62981751

TeamView也是使用x11协议

推荐系统有哪些比较好的论文
https://www.zhihu.com/question/25566638/answer/859024541

https://hyperledgercn.github.io/hyperledgerDocs/blockchain_zh/
怎么没有打价格战？我现在双卡，移动18的淘宝，电信卡就用来上网，20元无限流量。

自制编译器
https://m.ituring.com.cn/book/1308


sofa-mesh

https://github.com/youzan/gatling-dubbo

Vcpkg 是一款开源的 VC++ 打包工具。该项目于 2016 年首次在 CppCon 上发布，以满足开发人员的需求。

brpc + folly

从物理机到虚拟化再到容器化、微服务和DevOps，更加灵活的IT架构、更加便捷高效的开发流程，这就是云原生，并不存在什么难以逾越的鸿沟。

/etc/fastdb 挂载点

开源cpp库列表
https://zh.cppreference.com/w/cpp/links/libs

C++实现轻量级极简httpserver和httpclient
https://blog.csdn.net/u012234115/article/details/79596826

by ex-googlers, for ex-googler
https://github.com/jhuangtw-dev/xg2xg


定期更新chinadns 文件列表

http://phyer.click/2016/06/23/update-ignore-list-of-chinadns/

AMD 被称为农企
https://www.zhihu.com/question/21683232

南京it公司
https://www.zhihu.com/question/22524282/answer/803267480

https://www.zhihu.com/question/22524282/answer/803267480

如何看待语音识别大牛、Kaldi 之父 Daniel Povey 加入小米？
https://www.zhihu.com/question/351137894/answer/861767125

没用过，看起来貌似不错。和zero ice相比，除了license以外，有什么其他优势吗？

cpp 库 zeroc-ice

https://github.com/zeroc-ice/ice

curl 有提供三方库 libcurl
Mongoose Embedded Web Server Library
https://github.com/cesanta/mongoose

boost Windows
https://www.boost.org/doc/libs/1_71_0/more/getting_started/windows.html

网易互娱的数据库选型和 TiDB 应用实践

https://mp.weixin.qq.com/s/prQ3EKkcv-eZR4nDhHWWZA

如果是公募基金，你可以看到基金都持仓了什么股票，这钱你是放心的，只要股票没崩盘，你的钱就一定还在那儿。  如果是货币基金，就跟存银行差不多，还有的是债券投资，你知道投的标的是什么，只要你投的标的没有出现系统性金融风险，你的钱也是安全的。

很明显你不是没学好C++，是没学好C#。。  论高性能编程，C#静态编译有多麻烦？怎么处理内存非托管和托管资源的关系？怎么解决反射元数据量大的问题？Lambda怎么能像C++一样生成纯值类型匿名类？指针和泛型怎么兼容？  但凡考虑过以上任何一个问题，你都不会这么问。

如果换做今天，我可能会被层出不穷的框架、库和换汤不换药的技术名词压得喘不过气来，满脑子就是一堆编程语言十几个前端后端框架和linux docker kubernetes mapreduce spark, 电脑在我眼中就会是个无法感知无法控制的神奇黑盒。

图灵机


如何愉快地写个小parser
https://zhuanlan.zhihu.com/p/20178871


Cpp 依赖头文件 不分模块
《数据库系统概念》8-选择、投影等关系运算

https://www.cnblogs.com/zhixin9001/p/7912572.html

形式语言总结
https://www.jianshu.com/p/575add9b80c3

mysql如何使用bison flex
http://www.orczhou.com/index.php/2012/11/mysql-innodb-source-code-optimization-1/

架构设计 考虑实时，非实时
brpc属于分布式RPC框架， 而dubbo是分布式服务框架。 所以这个问题也可以看做是分布式RPC框架和分布式服务框架的异同。从功能上看，可以简单将分布式服务框架看做是分布式RPC框架的升级，二者的核心部分基本是相似的。分布式RPC框架核心功能： 网络通信、序列化/反序列化、协议封装。分布式服务框架核心功能， 在分布式RPC基础上，增加了服务发现和服务治理的功能

spring 中英文文档
https://www.docs4dev.com/docs/zh/spring-framework/4.3.21.RELEASE/reference

思考一个问题，如何从0新建一个项目

十年后，随着虚拟化技术的进步以及硬件的进步，量变引起了质变，云计算在成本控制、性能和稳定性等方面都体现出了巨大的优势。另一方面，随着互联网的持续发展和传统企业的数字化，市场对于成本低、灵活性强、功能全面的互联网基础设施服务的需求越来跃强劲。两个因素共同作用，催生了一场云计算革命。

spring http参数接收
https://blog.csdn.net/yh_zeng2/article/details/75172990

问丁旺 小环，生产哪些宁静可以执行
假如不需要基础镜像，可以使用空白镜像 scratch 作为基础镜像。scratch 这个镜像是虚拟的，实际并不存在。

flex 可执行文件 flex-dev 编程用到库文件
线程模型 posix freebsd
卸载chrome企业插件Symantec Extension
https://malwaretips.com/blogs/installed-enterprise-policy-removal/#removal

阿里巴巴中间件
http://jm.taobao.org/

RocketMQ 不支持多点之间自动同步
多看几遍架构师的文章
Antlr 生成的java代码，如何添加package
短网址
https://www.infoq.cn/article/2v4QjIYziuj5Wf59rLs2

2019 腾讯区块链白皮书
Uber 正式开源 Go 语言编程规范，内部已使用多年
GSoC，如果你没有被选上可以再算进JSoC
Centos的包，是不是类似maven
数据库分表，对数据库操作

想使用消息队列，先考虑下这些问题！
https://mp.weixin.qq.com/s/LpN_OcEJEJBw38xxQzOtgA


千亿级数量下日志分析系统的技术架构选型
https://mp.weixin.qq.com/s/7jKABLwsxdm5ZR7imNhhFQ

预处理SQL  普通SQL：即使用Statement接口执行SQL 预处理SQL：即使用PreparedStatement接口执行SQL 使用PreparedStatement接口允许数据库预编译SQL语句，以后只需传入参数，避免了数据库每次都编译SQL语句，因此性能更好。

Spring Security、Session 和 LDAP 项目负责人 ROB WINCH 指出

Mybatis 讲解的点
Spring aop查看注解了哪些方法的工具

整理常用中间件用法

亚军 302网址跳转
infoq 短网址 写文档 借鉴
https://www.infoq.cn/article/2v4QjIYziuj5Wf59rLs2

springmvc redirect原理分析

Spring jar包 作用
https://www.docs4dev.com/docs/zh/spring-framework/4.3.21.RELEASE/reference/overview.html#overview-core-container

Dubbo书籍 telnet invoke
Dubbo zk分组 有四个

这本O'Reilly的免费电子书只有不到200页，相信可以帮助你入门BPF，。如果你听过Cilium的话那么一定知道BPF，这是类Unix系统上数据链路层的一种原始接口，可以用在Service Mesh中的透明流量劫持，https://www.servicemesher.com/blog/cilium-intro

dubbo zk 自定义命令行
http://alibaba.github.io/dubbo-doc-static/Telnet+Command+Reference-zh-showComments=true&showCommentArea=true.htm

Mbg是典型的ddd对立面
tidb是兼容mysql协议的

Redis适合存放小并且经常写的数据
Cpp 库文件依赖关系怎么定
IDEA使用三方库套路 idea插件 maven插件 配置文件
Spring cloud的ip问题，可以通过动态ip解决

Pivotal公司是由EMC和VMware联合成立的一家公司。spring是他下面的一个team在维护

Maven optional 例子
https://www.zhihu.com/question/318377502/answer/639574906

亚军 金融系统分为账单 账户 交易等等
dubbo云原生 k8s
https://mp.weixin.qq.com/s?__biz=MzUzNzYxNjAzMg==&mid=2247487207&idx=1&sn=e185d620c6b821614ec621529b75ed1e&chksm=fae50528cd928c3e5563236193a59601cae403968c3e34c21520ca56240140c451f5c46bee78&mpshare=1&scene=1&srcid=&sharer_sharetime=1572352478294&sharer_shareid=02e3c79169caf3429aa8f00c9f73608f&key=f9d17ab3d743a978fb49ab8939166c522da437621f9d3c08aa699346f7ad15f0d70bd71f681d7b88987f75a638b5093a3b59f3996d5641c263c64928ed525a23fb720f9d9a3233d77206c3327a4df545&ascene=1&uin=MjY1MTA3MzYyMQ%3D%3D&devicetype=Windows+10&version=62060844&lang=zh_CN&pass_ticket=%2BGo8sDEUEg6W6AuObCiENdFpHai%2BQgd%2BXp%2Bxw4Q%2FWGfx6Ga%2Bp5RMjda72LE3fhCN

金数据
https://jinshuju.net/

.net rpc
https://www.cnblogs.com/Leo_wl/p/10531496.html?utm_medium=referral&utm_source=itdadao

中华石杉的两万架构师培训

Apollo配置中心部署
https://blog.csdn.net/luhong327/article/details/81453001

Shell的本质
Zsh bash
mysql 命令行 redis命令行

单元测试框架含有main函数
填充一部分代码，这些填充的代码包含要测试的内容

控制台上如何运行junit，如何查看单元测试结果
对http body不熟悉
https://blog.csdn.net/u010244522/article/details/79385502


整理Spring Springmvc配置文件先顺序

字节全是go

视频流媒体 ，大部分也是C++

存储也用C++

c++主要用于高性能实时性强的部分

c++一线今年也不好了 大厂 打着招人招牌 其实也不怎么想招

Dubbo qos telenet登陆

rpc是什么？php中流行的rpc框架有哪些

建议找大型PHP团队练练手,技术只看不动手不深入场景,很难悟出道道.

另外多学学自然语言处理、推荐系统、智能客服之类这些和web方面结合比较紧密的人工智能。数学思维很重要。

spring动态变量 properties

Chubby
Zookeep 谷歌论文Chubby的开源实现

系统设计 北美IT面试
初中开始写代码，一天12小时，不能间断，不断突破舒适区，先用别人轮子，然后迅速自己造轮子，首先写一个2d rpg游戏，再写一个2d游戏引擎，然后写一个静态语言，再写一个jit语言,然后把Java,c,c++,Haskell,python,ocaml啥的语言都学会了，然后大学没毕业去面试msra，并在实习的时候认识一个谷歌的妹子，然后去西雅图写office，如果你卡在某一步了，记得多关注几个知乎妹子

javaee标准 jcp社区维护 提供标准api 不同厂商实现，开源闭源都有

javaee的收费产品，受到云计算产品的冲击

tomcat HTTP2 alpn
https://www.cnblogs.com/haore147/p/5508287.html



https://http2.akamai.com/demo



http2 二进制打包 多路复用

web.xml  是javaee servlet标准

https://blog.csdn.net/m751075306/article/details/9452893



https://docs.oracle.com/cd/E24329_01/web.1211/e21049/web_xml.htm#WBAPP547



tomcat jetty jboss websperer都有实现

华泰证券 it es建设
http://www.itdks.com/Course/detail?id=12972

spi 阿里中间件开发个人笔记
https://www.cnkirito.moe/spi/

讲数据库中间件现状国外的情况，做数据库中间件的多吗？貌似不多，因为直接跨过中间件搞数据库本身去

ReactiveX是Reactive Extensions的缩写，一般简写为Rx。Rx是一个编程模型，目标是提供一致的编程接口，帮助开发者更方便的处理异步数据流，Rx库支持.NET、JavaScript和C++，Rx近几年越来越流行了，现在已经支持几乎全部的流行编程语言了。社区网站是 ReactiveX 。

头条OLAP招聘要求
对市面上常见的 OLAP 系统设计与源码有深入研究；

给 Hive/Kylin/Presto/Spark/Druid 等项目提交过 patch 者优先；

在PB以上级生产环境经验者优先

Google利器之Chubby
https://blog.csdn.net/historyasamirror/article/details/3870168

Dubbo看书要查资料
@Gome 兄弟 不和你争了 你可以参照一下rust mod的设计，然后看看cocoapods 是不是完善，cocoapods 解决不了 不能用carthage吗？我心目中完善的包管理工具是npm 和 gradle，cocoapods还是不完整的

Mysql 连接数
show processlists

返回结果的行数就是当前用户的连接数

dubbo引入Spring配置，使用了BeanDefinationParseDelegate#parseCustomerElement方法

沪江有两套文件存储系统，一套是基于Ceph自建的内部存储系统。另一套是基于云厂商的外部存储(DFS)。本次分享主要介绍两套文件系统的适用场景及构建思路，包括： 存储模式的选择， 对象存储 OR 块存储 为什么需要搭建内部存储系统 为什么选择Ceph， Ceph与Swfit、HDFS、fastDFS的对比。 有了Ceph，为什么还需要DFS 如何在享受云厂商的便利性的同时，最大限度的规避相应的各种不可控因素

沪江网 存储系统 fastdfs 转换到ceph

fastdfs问题多，不符合云存储理念


Kubernetes 是从 Google 的 Borg 系统演变而来，Prometheus 同样受到 Google 的 Borgmon 监控系统的启发

Zabbix, Nagios

bind9
现在CDN厂商也就cloudflare和akamai技术上革新比较积极吧。。

https://renderdoc.org/  vulkan windows安装时会安装

把代理服务器地址写入shell配置文件.bashrc或者.zshrc
利用proxychains在终端使用socks5代理

补充：

如果代理服务器需要登陆，这时可以直接把用户名和密码写进去



http_proxy=http://userName:password@proxyAddress:port

期待。之前做压测时候有些问题比较困惑，希望写文章时候如果可能顺带提一下。 典型配置下的一些经验数据，比如4核8G服务器大概可以扛到的并发，mysql连接数多少正常，time_wait数目多少是正常范围。
termux 更换源
https://www.jianshu.com/p/5c8678cef499


但人家Rosen写离散数学及其应用的初衷，是给学计算机的同学入门用的，如果无论你是应付期末考试，还是为了考研，看这本书我敢保证没好果子吃。
离散数学及其应用
看书，看笔记时需要思考

没有哪家银行是用java写的核心，交易系统都是用C

联通王卡 dubxbo
ubuntu 16 systemd 企业wifi
https://askubuntu.com/questions/279762/how-to-connect-to-wpa2-peap-mschapv2-enterprise-wifi-networks-that-dont-use-a-c

谷歌密码在苹果手机上

leveldb 思想牛逼 代码就那样
cpp编译，带上头文件和编译好的文件
vs就是这样干的

C++模板
https://zhuanlan.zhihu.com/p/97907193


开课吧 课程
conans
https://blog.csdn.net/qqqq123qqqqqqq/article/details/79421686



https://blog.csdn.net/h511555/article/details/8904143

Comments:

Cheng Wu: https://conan.io/

济南平安作为平安8个区域
死磕源码系列
mybatis 不开启事务 如何

sentinel集群部署方案
集群

如何评价首发价4499起步的联想小新Pro13锐龙版 因特尔版6千多

20191124 netty 线程 17个？cpu个数*2




对比下配置中心
https://mp.weixin.qq.com/s?__biz=MzI4NTA1MDEwNg==&mid=2650778104&idx=2&sn=d069efc206e5312f6b2d5360196bae7f&chksm=f3f91c6dc48e957b22a38fbb49521273d2582dd26fe6496e138e1af159a55bdbd203d0bd4620&scene=21#wechat_redirect

图形化显示sql慢日志
https://mp.weixin.qq.com/s?__biz=MzI4NTA1MDEwNg==&mid=2650776064&idx=1&sn=3413111ad786a9264a8747857323f102&chksm=f3f91795c48e9e839a5e7e4e2e13ec27f3f8806a465358ab89ef0b1f7e283f2506ca54d97390&scene=21#wechat_redirect

腾讯云 mysql源码涉及到
https://mp.weixin.qq.com/s?__biz=MzI4NTA1MDEwNg==&mid=2650782428&idx=2&sn=e9c90b1eba3307a62f064c1d5967df0c&chksm=f3f90f49c48e865f138c8846f3d6cafd7a63a53ce44fc71169c1226ec5d8ed51ffaddfa2da73&scene=21#wechat_redirect

OpenResty  Scalable Web Platform by Extending NGINX with Lua
算法动态演示
https://visualgo.net/zh

maven内置变量
${basedir} 项目根目录(即pom.xml文件所在目录)

${project.build.directory} 构建目录，缺省为target目录

${project.build.outputDirectory} 构建过程输出目录，缺省为target/classes

${project.build.finalName} 产出物名称，缺省为${project.artifactId}-${project.version}

${project.packaging} 打包类型，缺省为jar

${project.xxx} 当前pom文件的任意节点的内容

${env.xxx} 获取系统环境变量。例如,"env.PATH"指代了$path环境变量（在Windows上是%PATH%）。

${settings.xxx} 指代了settings.xml中对应元素的值。例如：<settings><offline>false</offline></settings>通过 ${settings.offline}获得offline的值。

Java System Properties: 所有可通过java.lang.System.getProperties()访问的属性都能在POM中使用，例如 ${JAVA_HOME}。

c++有个开源库spdlog，可以格式化输出日志
可能就搜索 和 广告引擎用c++ 了
搜索es满足大部分需求

Mybatis generator也是idea插件 maven插件，自身jar包
不过，Java的确可以写出性能很强大的程序，个人认为比较优秀的例子就是kafka，渣机都能跑出十万并发

Meituan-Dianping Zebra  ss竞品
中国安防领域的芯片大部分使用的是海思的芯片，未来的ARM cpu绝对会继续百花齐放的
2018年，手机CPU没有百花齐放。除了苹果华为三星三家CPU专供。就剩下高通和联发科了。
CPU开启虚拟化支持
icc -S 输出出来的汇编都是att风格的
gas是gnu出的，masm是ms出的，nasm和yasm是……嗯……奇奇怪怪的人出的。

gas用的AT&T风格汇编“甚至可以是平台无关的”。

intel倒是出过icc。贵到正常人不会去用的那种。
RPO一般按客户公司职级收费，比如8级以上是猎头收费，8级以下是RPO收费，收费标准比如6-7级收1.5倍月薪，6级以下1倍月薪。比如你为客户招到一个候选人 薪资是2万/月，如果定7级，就收3万，如果5级，就收2万

grpc和thrift区别真心不太大，差的最多的是你自己要填坑的那些东西：连接池、服务框架、服务发现、服务治理、trace、打点、context日志
一般应用来说，并发估算公式如下：qps = 5 * 日pv / 864005是通用峰值倍数，如果你有高峰值特性自行调整，比如秒杀功能。mysql通常在实体机的读写综合qps在几千左右，具体你可以自己压测一下，跟机器配置有关。所以首先你需要通过收集日志得到日pv，然后通过估算得到当前qps，再根据未来一段时间的用户量和场景看看够不够。比如你每天数据库访问次数是100万，可估算峰值qps为60左右，比如数据库qps可达3000，那么可估算你的服务器还能撑同等场景50倍增长。以上方法都是通用方法 作者：大雄

clinet为什么不rpc
sso header读写 文件



优势是io性能好，从根源上做到了io异步化。我可以告诉你为什么我们不用go语言做业务了，因为生态与java差太远，因为基础库质量太差，因为依赖比较坑，因为人比机器贵。性能？作为acmer，我是爱性能的，但绝大部分所谓性能问题都是代码写sb了。在坐的绝大部分互联网公司的业务，都谈不上语言与io的极限优化。正常的服务端语言，再差5w qps总有了吧？啥概念？单机40亿请求每天，你那破业务做到了吗？做不到扯什么性能。省10台机器，不够一个码农年薪的，而挖的坑造成的用户流失，就更不计其数了。用技术做业务与用业务做技术，是两种不同的价值观，其实说白了就这么回事。

ssdb pika这种也是有适用场景的
手写递归下降分析器
感觉记忆力是智商的基础


所以男人还是非常非常非常有必要找个处 否则你岂知道别人以前是人是鬼？所以我努力买房买车 就是不想以后新房新车新家具 新娘却是n手的

笛卡尔积  集合做交集
比如OI知识点：  树套树，树形DP，状态压缩DP，AC自动机，最小费用最大流，快速傅里叶变换。

比如LeetCode考点：  哈希表，动态规划，图，二叉树，堆栈

真正的央企有自己的电厂、电视台、电话站或局，有自己的医院、银行、派出所、幼儿园、从小学到大学的不同等级的学校，有自己的房产公司、物业公司、热力公司，有自己不同的养殖厂，有自己的农场，有自己的商场、酒店，地方有的企业都有，地方没有的，企业也有。

这得看情况了，很多公司实际项目全是写业务逻辑，其他你什么都不用管，需要什么直接公司出钱买。这样干个5年，你从实际项目中学会了啥？学会了怎么写业务逻辑，怎么使用各种商业软件服务？  脑子是个好东西，不用脑子永远只有被忽悠的份。



