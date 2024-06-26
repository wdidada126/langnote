# system design

SELECT name, birth, CURDATE(),
       TIMESTAMPDIFF(YEAR,birth,CURDATE()) AS age
       FROM pet;

年龄，跟当前时间有关
所以不能直接存数据库，需要获取当前时间，使用时间函数
       TIMESTAMPDIFF(YEAR,birth,CURDATE()) AS age

学习系统设计最好的几个站点
1. Educative - bit.ly/3Mnh6UR
2. Udemy - bit.ly/3vFNPid
3. ByteByteGo - bit.ly/3P3eqMN
4. Exponent - bit.ly/3cNF0vw
5. ZTM - bit.ly/3zEPZ3j
6. Coursera - bit.ly/3BxMXzr

系统扩展方式
https://blog.csdn.net/kepa520/article/details/82791470

哪种Scale out架构能更有效满足分布式计算

https://baijiahao.baidu.com/s?id=1611494409859582577&wfr=spider&for=pc

[横向扩展存储](https://baike.baidu.com/item/横向扩展存储/17583162?fr=aladdin)

https://www.sohu.com/a/206625689_165716

https://github.com/xingshaocheng/architect-awesome

https://github.com/sorenduan/awesome-java-books

##### 电商系统

SKU

[商品规格SKU算法实现](https://www.toutiao.com/i6760837222372475405/)

##### Consistency Model

[面试必问：怎么保证缓存与数据库的双写一致性](https://mp.weixin.qq.com/s?__biz=MzAxODcyNjEzNQ==&mid=2247488169&idx=2&sn=fa362cbb3fa97e97283e42d7cffde243&chksm=9bd0bf31aca73627fee22c0fff950e2492f8fce243c95de73a23ba068f7179872bd31894a091&scene=21#wechat_redirect)

##### Cache Aside Pattern

最经典的缓存+数据库读写的模式，就是 Cache Aside Pattern。

读的时候，先读缓存，缓存没有的话，就读数据库，然后取出数据后放入缓存，同时返回响应。

更新的时候，先更新数据库，然后再删除缓存。

为什么是删除缓存，而不是更新缓存？

原因很简单，很多时候，在复杂点的缓存场景，缓存不单单是数据库中直接取出来的值。

比如可能更新了某个表的一个字段，然后其对应的缓存，是需要查询另外两个表的数据并进行运算，才能计算出缓存最新的值的。

另外更新缓存的代价有时候是很高的。是不是说，每次修改数据库的时候，都一定要将其对应的缓存更新一份？也许有的场景是这样，但是对于比较复杂的缓存数据计算的场景，就不是这样了。如果你频繁修改一个缓存涉及的多个表，缓存也频繁更新。但是问题在于，这个缓存到底会不会被频繁访问到？



- Strict Consistency Strict Consistency是最强的一致性模型，要求任何读取操作都能读取到最新的值，换句话说，要求任何写入操作立即同步给所有进程。在分布式系统中，数据的同步是需要时间的，因此在分布式系统下无法严格实现Strict Consistency。除非让所有的读写操作都只在一个进程的一个线程中执行或者，读写操作被锁保护起来。(根据CAP的原理，这个一致性模型在没有牺牲可用性的前提下是不能得到满足的。 性能也是不可接受的：所有的写操作需要同步到所有节点之后再返回给客户端。)

- Sequential Consistency Sequential Consistency是比Strict Consistency弱一些的一致性模型，要求：
1. 进程内，对同一个变量的读写保持顺序
  2. 进程间，“看到”的变量的变更顺序是一致的（不要求和“物理时间”下的顺序保持一致）

- Linearizable Consistency Linearizable Consistency比Sequential Consistency更严格一些：
1. 进程内，对同一个变量的读写操作保持顺序
  2. 进程间，“看到”的变量的变更顺序和全局“物理时钟”下的顺序是一致的


[etcd raft如何实现Linearizable Read](https://www.cnblogs.com/foxmailed/p/7161878.html)


https://zhuanlan.zhihu.com/p/81953907



其实系统设计的本质是，在考察的领域中将functional/non-functional requirements转化为可落地实现的技术描述。

所以paper看与不看都是有可能的，和你具体面试的方向有关系。

如果你去做infra，我讲FLP你不懂，linearizable你也不懂，consensus一知半解，设计个简单的数据库也没谱，那还是回去看看paper再来吧……

如果做应用层，那这些概念又不重要了，linearizability是啥？我只要知道strong consistency就行。甚至有所谓senior eng把cap的c和acid的c混为一谈人家照样出活。做应用要对产品有大局观，细节上对工具特性吃得透，做出系统对ops，analytics和扩展性支持好。搭积木也不是人人都能搭得出彩的。

也可以做计算啊……客户端啊……要的知识都不一样。





系统设计题

https://github.com/donnemartin/system-design-primer/blob/master/README-zh-Hans.md


SOA----面向服务架构，实际上强调的是软件的一种架构，一种支撑软件运行的相对稳定的结构，表面含义如此，其实SOA是一种通过服务整合来解决系统集成的一种思想。不是具体的技术，本质上是一种策略、思想。
ESB----企业服务总线，像一根“聪明”的管道，用来连接各个“愚笨”的节点。为了集成不同系统，不同协议的服务，ESB做了消息的转换解释与路由等工作，让不同的服务互联互通。


异地多活架构的应用场景

备份系统平常没有流量，如果直接上线可能触发平常测试不到的故障。
再实时的系统也会有数据延时，如果涉及到金融这种系统，仍然是不敢直接切换的。
系统运行过程中会有很多中间数据，缓存数据等。系统不经过预热直接把流量倒过来，大流量会直接把系统拖垮

例如，广州机房到北京机房，正常情况下 RTT 大约是 50 毫秒左右，遇到网络波动之类的情况，RTT 可能飙升到 500 毫秒甚至 1 秒，更不用说经常发生的线路丢包问题，那延迟可能就是几秒几十秒了。

回到软件架构设计领域，FMEA 并不能指导我们如何做架构设计，而是当我们设计出一个架构后，再使用 FMEA 对这个架构进行分析，看看架构是否还存在某些可用性的隐患。
FMEA 方法
在架构设计领域，FMEA 的具体分析方法是：
给出初始的架构设计图。
假设架构中某个部件发生故障。
分析此故障对系统功能造成的影响。
根据分析结果，判断架构是否需要进行优化。
FMEA 分析的方法其实很简单，就是一个 FMEA 分析表，常见的 FMEA 分析表格包含下面部分。


今天我要问你的是有关集合框架方面的问题，对比 Vector、ArrayList、LinkedList 有何区别？
典型回答
这三者都是实现集合框架中的 List，也就是所谓的有序集合，因此具体功能也比较近似，比如都提供按照位置进行定位、添加或者删除的操作，都提供迭代器以遍历其内容等。但因为具体的设计区别，在行为、性能、线程安全等方面，表现又有很大不同。
Vector 是 Java 早期提供的线程安全的动态数组，如果不需要线程安全，并不建议选择，毕竟同步是有额外开销的。Vector 内部是使用对象数组来保存数据，可以根据需要自动的增加容量，当数组已满时，会创建新的数组，并拷贝原有数组数据。
ArrayList 是应用更加广泛的动态数组实现，它本身不是线程安全的，所以性能要好很多。与 Vector 近似，ArrayList 也是可以根据需要调整容量，不过两者的调整逻辑有所区别，Vector 在扩容时会提高 1 倍，而 ArrayList 则是增加 50%。
LinkedList 顾名思义是 Java 提供的双向链表，所以它不需要像上面两种那样调整容量，它也不是线程安全的。

今天，我要问你的是一个经典的 Java 基础题目，谈谈 final、finally、 finalize 有什么不同？
典型回答
final 可以用来修饰类、方法、变量，分别有不同的意义，final 修饰的 class 代表不可以继承扩展，final 的变量是不可以修改的，而 final 的方法也是不可以重写的（override）。
finally 则是 Java 保证重点代码一定要被执行的一种机制。我们可以使用 try-finally 或者 try-catch-finally 来进行类似关闭 JDBC 连接、保证 unlock 锁等动作。
finalize 是基础类 java.lang.Object 的一个方法，它的设计目的是保证对象在被垃圾收集前完成特定资源的回收。finalize 机制现在已经不推荐使用，并且在 JDK 9 开始被标记为 deprecated。





知乎live

互联网面试攻略：系统设计篇



知乎专栏

微服务应用开发和API管理



##### 经典系统设计面试题解析：如何设计TinyURL（三）

APE灵长科技

Grokking the System Design Interview

https://www.1point3acres.com/bbs/forum.php?mod=viewthread&tid=456546&extra=

https://www.1point3acres.com/bbs/thread-404097-1-1.html





##### Designing a URL Shortening service like TinyURL

Let's design a URL shortening service like TinyURL. This service will provide short aliases redirecting to long URLs. Similar services: bit.ly, goo.gl, qlink.me, etc. Difficulty Level: Easy



### 1. Why do we need URL shortening?
###  2. Requirements and Goals of the System
### 3.Capacity Estimation and Constraints
### 4. System APIs

### 5. Database Design

### 6. Basic System Design and Algorithm

##### a. Encoding actual URL

##### b. Generating keys offline 

7. Data Partitioning and Replication
8. Cache
9. Load Balancer (LB)
10. Purging or DB cleanup
11. Telemetry


### 12. Security and Permissions

# Designing Instagram

Let's design a photo-sharing service like Instagram, where users can upload photos to share them with other users. Similar Services: Flickr, Picasa Difficulty Level: Medium

### 1. What is Instagram?

2. Requirements and Goals of the System

Functional Requirements

Non-functional Requirements

### 3.Some Design Considerations

### 4. Capacity Estimation and Constraints

5. High Level System Design

### 6. Database Schema
### 7. Data Size Estimation
### 8. Component Design
### 9. Reliability and Redundancy
### 10. Data Sharding
### 11. Ranking and News Feed Generation
### 12. News Feed Creation with Sharded Data
### 13. Cache and Load balancing



