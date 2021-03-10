# UnixLinux编程实践教程

Unix Linux编程实践教程

读书笔记

很多都是Linux接口的

[WebService的几种框架 比较](https://blog.csdn.net/dzq_boyka/article/details/80360297)



目前[三种主流的web服务](http://www.zelinonline.com/news_detail.asp?id=1692)实现方法： 

[REST](http://baike.baidu.com/view/1077487.htm)（新型）：表象化状态转变 (软件[架构](http://lib.csdn.net/base/16)风格）RESTEasy、Wink、CXF、Axis2…….

[SOAP](http://www.baike.com/wiki/SOAP)（比较成熟）：简单对象访问协议 Xfire、Axis2、CXF、Axis1

[XML-RPC](http://baike.baidu.com/view/643379.htm)（淘汰）：远程过程调用协议（慢慢被soap 所取代）





线程
Java接口

Fastjson druid 开源
温少


spring是通过设置target-class是否为true，来决定是否强制使用cglib。

RPC使用了动态代理

Dubbo:reference使用了动态代理？






为什么JDK Proxy是基于反射实现的呢？这其中有啥考量呢？


我的理解，核心功能需要最小依赖关系，性能也不错


内部排序，至少掌握基础算法如归并排序、交换排序（冒泡、快排）、选择排序、插入排序等。
外部排序，掌握利用内存和外部存储处理超大数据集，至少要理解过程和思路。

双向琏表排序



mmap
Io效率高

占用连续内存，
写入连续内存不阻塞
内存信息一次性保存到本地磁盘
而不是写一次就更新一次到硬盘


特斯拉的自动驾驶本来就很落后，自动驾驶领域一军事waymo、福特、通用，二军是丰田，大众、博世、mobileyes等，特斯拉勉强排进三军吧，不过架不住他能吹[捂脸]



后端架构师技术图谱


https://github.com/xingshaocheng/architect-awesome



随着硬件计算能力的增强，以及大数据的爆发式增长，AI技术的潜力得到前所未有的挖掘，再一次掀起人工智能的新高潮。结合不同场景的业务特点，AI在搜索、推荐、计算广告、风控、图像处理等领域都有不断突破。
本次技术沙龙，美团外卖技术部的专家深入介绍AI在对话系统、图像处理、个性化推荐、智能营销等方向在外卖业务中的实践，希望与业界技术同学一起交流学习。


想学C# 的同学可以追一下这个视频列表，微软.NET 组大佬Immo 直播写编译器。此大佬目前掌管.NET 全部的API 设计，身为Principal PM还能写这么溜地写代码。http://www.youtube.com/playlist?list=PLRAdsfhKI4OWNOSfS7EUu5GRAVmze1t2y



还行。我还是推荐The Implementation of Functional Programming Languages。初学者入门编译原理必读之一（剩下的还有虎书和Parsing Techniques，都看完保证成为合格的二本毕业生）

《C语言经典编程282例》


spring aop 查看匹配了哪些方法

System call


https://blog.csdn.net/wwwdc1012/article/details/78759326


综上源码，在进行阻塞的时候，底层并没有（并不一定）要用 while 死循环来阻塞，更多的是借助于操作系统的实现来进行阻塞的。当然，这也更符合大家的猜想！
从上的代码我们也发现一点，底层在做许多事的时候，都不忘考虑线程中断，也就是说，即使在阻塞状态也是可以接收中断信号的，这为上层语言打开了方便之门。

是调用操作系统的底层操作原语，可以认为是操作系统内核


C++，JAVA刚出来我就用了，你如果真的了解的花，这些还是01010那一套。但是我从来没写过01010。我2000年毕业，从07年前后就没直接写过Servlet了。软件开发不变的方向就是抽象和透明化！让人不断的站在更高层级上去完成开发工作。Typescript刚出来，我就用了，如果你真的了解的话，最后Typescript会编译成JS。Less/SASS刚出来，我就用了，如果你真的了解的话，最后都会编译成CSS。


Java的服务器端演进的太慢了，Akka都出现了N年了，同样基于Actor Model的Vert.X的流行度依然不如Spring系列。

Python Prof 强制我oop 蛋疼


小米开源编译器

https://github.com/xiaomi/mace

MACE is a deep learning inference framework 


https://github.com/ronaldo8210/brpc_source_code_analysis

写了一些brpc的源码分析，供参考


程序员逐步升级的过程。
第一阶段，首先要保证基本功扎实，最简单的说，要做到语法熟练、基本框架熟练，成为一个功夫精熟的“码农”。
第二阶段，从“技”到“术”，从“码农”到“工程师”。这个阶段的关键技术是设计模式。在局部上，不仅追求实现功能，更关注实现的好，关注功能之外的维度，例如健壮性、低耦合、可扩展等指标。对主流框架（例如Spring），不仅会用，更有深刻的理解。
第三阶段，从“术”到“道”。
这个阶段，不仅在局部上追求一个模块的好坏，而且还要从整个系统层面去掌控程序，例如保证整个程序不出现系统腐败，如何安排资源的优先级等。这个时候就不是单一的维度，单一的技术能够保证了。


《代码大全》、
《重构：改善既有代码的设计》
《设计原本》
《大型网站技术架构核心原理与案例分析》



IBM
作为一个学过Wason架构，参与过部分医疗方面扩展的人，表示至少在医疗方面并不乐观。
IBM现在主要产业是low到爆的IT外包，用创新改变世界那个公司已经不在了
1911年IBM成立



VS Code 的核心组件
Electron
Monaco Editor
Language Server Protocol
Debug Adapter Protocol


龙书对前端词法、语法分析讲的过多，理论很深。实际中一般不会用到—除了考试，一般到会用工具如flex&yacc 和antlr即可。
龙书后面的数据流分析很好，实际中会用。
因此，建议直接上工具书学习编译器前端，建议使用antlr，书籍推荐
Language Implementation Patterns: Create Your Own Domain-Specific and General Programming Languages
这本书中也讲了编译器前端的知识，结合工具中的例子学习更快。
之后数据流分析可以看看龙书， 虎书。



系统设计题
https://github.com/donnemartin/system-design-primer/blob/master/README-zh-Hans.md



SOA----面向服务架构，实际上强调的是软件的一种架构，一种支撑软件运行的相对稳定的结构，表面含义如此，其实SOA是一种通过服务整合来解决系统集成的一种思想。不是具体的技术，本质上是一种策略、思想。
ESB----企业服务总线，像一根“聪明”的管道，用来连接各个“愚笨”的节点。为了集成不同系统，不同协议的服务，ESB做了消息的转换解释与路由等工作，让不同的服务互联互通。


termux install htttp2 server
https://github.com/caddyserver/caddy/wiki/Running-Caddy-on-Android


 单纯从上面的对比来看，似乎微服务大大优于 SOA，这也导致了很多团队在实践时不加思考地采用微服务——既不考虑团队的规模，也不考虑业务的发展，也没有考虑基础技术的支撑，只是觉得微服务很牛就赶紧来实施，以为实施了微服务后就什么问题都解决了，而一旦真正实施后才发现掉到微服务的坑里面去了。


 异地多活架构的应用场景

备份系统平常没有流量，如果直接上线可能触发平常测试不到的故障。
再实时的系统也会有数据延时，如果涉及到金融这种系统，仍然是不敢直接切换的。
系统运行过程中会有很多中间数据，缓存数据等。系统不经过预热直接把流量倒过来，大流量会直接把系统拖垮


例如，广州机房到北京机房，正常情况下 RTT 大约是 50 毫秒左右，遇到网络波动之类的情况，RTT 可能飙升到 500 毫秒甚至 1 秒，更不用说经常发生的线路丢包问题，那延迟可能就是几秒几十秒了。


即可时间

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



NoClassDefFoundError是一个错误(Error)，而ClassNOtFoundException是一个异常，在Java中对于错误和异常的处理是不同的，我们可以从异常中恢复程序但却不应该尝试从错误中恢复程序。
ClassNotFoundException的产生原因：

Java支持使用Class.forName方法来动态地加载类，任意一个类的类名如果被作为参数传递给这个方法都将导致该类被加载到JVM内存中，如果这个类在类路径中没有被找到，那么此时就会在运行时抛出ClassNotFoundException异常。
ClassNotFoundException的产生原因主要是：
Java支持使用反射方式在运行时动态加载类，例如使用Class.forName方法来动态地加载类时，可以将类名作为参数传递给上述方法从而将指定类加载到JVM内存中，如果这个类在类路径中没有被找到，那么此时就会在运行时抛出ClassNotFoundException异常。
解决该问题需要确保所需的类连同它依赖的包存在于类路径中，常见问题在于类名书写错误。
另外还有一个导致ClassNotFoundException的原因就是：当一个类已经某个类加载器加载到内存中了，此时另一个类加载器又尝试着动态地从同一个包中加载这个类。通过控制动态类加载过程，可以避免上述情况发生。

NoClassDefFoundError产生的原因在于：
如果JVM或者ClassLoader实例尝试加载（可以通过正常的方法调用，也可能是使用new来创建新的对象）类的时候却找不到类的定义。要查找的类在编译的时候是存在的，运行的时候却找不到了。这个时候就会导致NoClassDefFoundError.
造成该问题的原因可能是打包过程漏掉了部分类，或者jar包出现损坏或者篡改。解决这个问题的办法是查找那些在开发期间存在于类路径下但在运行期间却不在类路径下的类。



