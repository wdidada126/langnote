# jvm



```shell
mvn clean install -DskipTests
Error occurred during initialization of VM
Unable to allocate 8192KB card tables for parallel garbage collection for the requested 4173824KB heap.
Error: Could not create the Java Virtual Machine.
Error: A fatal exception has occurred. Program will exit.
```




马士兵

第一天：Jvm垃圾回收快速入门

1、什么是垃圾？

2、如何定位垃圾？

3、常用垃圾回收算法

4、常用垃圾回收器

5、系统上线前预估系统的内存占用情况

6、系统上线前预估系统的并发访问情况

7、根据预估值设定JVM初始参数

8、压力测试方法论

9、根据压测结果调整参数值

10、系统上线后设定日志参数

11、定期观察日志情况

12、根据日志解决实战问题

 

 

第二天：生产环境中的垃圾回收方法理论与动手实战

13、为什么一个百万级TPS系统会频繁GC？

14、定位JVM问题的实用参数设置

15、用top命令观察系统运行情况

16、用jps定位虚拟机进程

17、用jstat定位JVM问题

18、用jmap导出内存转储文件

19、用jstack定位问题线程

20、用jhat分析转储文件

21、其他给力的工具visual VM，MAT，Arthas介绍

22、动手实战

23、集中答疑，解决同学们学习中的问题

24、面向未来，学习路线指引与职业规划


JVM中的堆外内存（off-heap memory）与堆内内存（on-heap memory）

https://blog.csdn.net/khxu666/article/details/80775635



链接：https://www.nowcoder.com/questionTerminal/7a0dadaccd364f68a41cca5d22d2e09e
来源：牛客网

off-heap叫做堆外内存，将你的对象从堆中脱离出来序列化，然后存储在一大块内存中，这就像它存储到磁盘上一样，但它仍然在RAM中。对象在这种状态下不能直接使用，它们必须首先反序列化，也不受垃圾收集。序列化和反序列化将会影响部分性能（所以可以考虑使用FST-serialization）使用堆外内存能够降低GC导致的暂停。堆外内存不受垃圾收集器管理，也不属于老年代，新生代。



Statement 对象用于将 SQL 语句发送到数据库中。实际上有三种 Statement 对象，它们都作为在给定连接上执行 SQL 语句的包容器:Statement、PreparedStatement(它从 Statement 继承而来)和 CallableStatement(它从 PreparedStatement 继承而来)。它们都专用于发送特定类型的 SQL 语句: **Statement** 对象用于执行不带参数的简单 SQL 语句;**PreparedStatement** 对象用于执行带或不带 IN 参数的预编译 SQL 语句;**CallableStatement** 对象用于执行对数据库已存在的存储过程的调用。



jvm是宇宙第一虚拟机。gc，monitor，还有动态性都已经很成熟了，围绕着jvm还有一群设计精良的语言：java，scala。这些组成了庞大的生态系统：spark，kafka，ssh，ibatis，tomcat，play，netty，akka等等。现代系统，只要是打算用虚拟机的，性能最好+招聘成本最低毫无疑问是java，各种监测工具，甚至允许运行期改动子节码立即生效找错。osgi的引入甚至将oo的结构提升到前所未有的层次，这些都不是号称有模块化功能的语言（node）可以比的。大数据你绕不开spark。。。。。等等。所以何来java没人用之说？至于swing，在商业上叫产品完整性。作为一个dk所必需要有的完整和体系。

Oracle JDK是Oracle公司给出的JAVASE参考实现,同理GlassFish是Oralce给出的JAVAEE参考实现

javaconfigurationblogexample_{0..1}.t_blog

[大型跨境电商JVM调优总结](https://blog.csdn.net/lingbo229/article/details/84999732)



**Jvm slot**





19年开始搞zgc，有一起的吗？g1



最近在看zgc，发现在进行dump时候，如果没指定-all，依然不会进行gc，不过整个过程还是会stw。





https://www.jianshu.com/p/4e4fd0dd5d25





3.。。。。。。。



<<<<<<< HEAD
阿里巴巴即将重磅开源OpenJDK长期支持版本Alibaba Dragonwell
=======
**阿里巴巴即将重磅开源** **OpenJDK** **长期支持版本** **Alibaba Dragonwell**
>>>>>>> a37e32040eec40d601569c731c313a398efb2dec

AWS 开源的 OpenJDK 长期支持版本 Corretto 项目





Java HotSpot(TM) 64-Bit Server VM warning: ignoring option MaxPermSize=256m; support was removed in 8.0

没有固定的jvm参数规范，只有合适业务的


你假笨

<<<<<<< HEAD
[JVM 源码解读之 CMS GC 触发条件](https://mp.weixin.qq.com/s?__biz=MzUyMDE1ODQ3NQ==&mid=2247483851&idx=1&sn=8cb444039449848531b7ca72c396e07e&chksm=f9efedafce9864b9dbb645863d7d3c8b34e83888d07e175dd9c931576db2ecc0aa90835fcf50&mpshare=1&scene=1&srcid=&key=934cca182998c288c821744645ddf2abe9f1f1754543521660280cc6fdf86d21a8632a2a4e54ea2201159f76f65ca38dbc010a875d1e7f100a58d6a615b9869a72278ab94abf6a2dae104bedaaca154d&ascene=1&uin=MjY1MTA3MzYyMQ%3D%3D&devicetype=Windows+10&version=62060833&lang=zh_CN&pass_ticket=7KLf9b9yLXLeuk0HnBlu%2BN9tmKg%2BEfXwrAWUCAPR0nEEjSroYcrsrBNjoMJYurWr)

涤生的博客

disheng_yq



深入理解java虚拟机第三版本



Jvm vs CLR

虚拟机规范

Java语言规范

Spec

Kotlin 函数式

垃圾回收算法

Cms g1zgc是？

标记清除算法

Java内存区域

方法区

堆

栈

寄存器

线程私有的划分
=======
<<<<<<< HEAD
[JVM 源码解读之 CMS GC 触发条件](https://mp.weixin.qq.com/s?__biz=MzUyMDE1ODQ3NQ==&mid=2247483851&idx=1&sn=8cb444039449848531b7ca72c396e07e&chksm=f9efedafce9864b9dbb645863d7d3c8b34e83888d07e175dd9c931576db2ecc0aa90835fcf50&mpshare=1&scene=1&srcid=&key=934cca182998c288c821744645ddf2abe9f1f1754543521660280cc6fdf86d21a8632a2a4e54ea2201159f76f65ca38dbc010a875d1e7f100a58d6a615b9869a72278ab94abf6a2dae104bedaaca154d&ascene=1&uin=MjY1MTA3MzYyMQ%3D%3D&devicetype=Windows+10&version=62060833&lang=zh_CN&pass_ticket=7KLf9b9yLXLeuk0HnBlu%2BN9tmKg%2BEfXwrAWUCAPR0nEEjSroYcrsrBNjoMJYurWr)
=======
https://mp.weixin.qq.com/s?__biz=MzUyMDE1ODQ3NQ==&mid=2247483851&idx=1&sn=8cb444039449848531b7ca72c396e07e&chksm=f9efedafce9864b9dbb645863d7d3c8b34e83888d07e175dd9c931576db2ecc0aa90835fcf50&mpshare=1&scene=1&srcid=&key=934cca182998c288c821744645ddf2abe9f1f1754543521660280cc6fdf86d21a8632a2a4e54ea2201159f76f65ca38dbc010a875d1e7f100a58d6a615b9869a72278ab94abf6a2dae104bedaaca154d&ascene=1&uin=MjY1MTA3MzYyMQ%3D%3D&devicetype=Windows+10&version=62060833&lang=zh_CN&pass_ticket=7KLf9b9yLXLeuk0HnBlu%2BN9tmKg%2BEfXwrAWUCAPR0nEEjSroYcrsrBNjoMJYurWr
>>>>>>> afe522da082020e5ece0b75c43067644b2edb768

>>>>>>> a37e32040eec40d601569c731c313a398efb2dec
