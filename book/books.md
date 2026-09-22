# books


dive into design patterns
https://book.douban.com/subject/26877699/
http://www.java1234.com/a/javabook/javabase/2019/0901/14465.html

微服务设计四个原则：AKF拆分原则

前后端分离
无状态服务
Restful通信风格

其中：
AKF扩展立方体(参考《The Art of Scalability》)，是一个叫AKF的公司的技术专家抽象总结的应用扩展的三个维度。理论上按照这三个扩展模式，可以将一个单体系统，进行无限扩展。

X 轴 ：指的是水平复制，很好理解，就是讲单体系统多运行几个实例，做个集群加负载均衡的模式。

Z 轴 ：是基于类似的数据分区，比如一个互联网打车应用突然或了，用户量激增，集群模式撑不住了，那就按照用户请求的地区进行数据分区，北京、上海、四川等多建几个集群。

Y 轴 ：就是我们所说的微服务的拆分模式，就是基于不同的业务拆分。

场景说明：比如打车应用，一个集群撑不住时，分了多个集群，后来用户激增还是不够用，经过分析发现是乘客和车主访问量很大，就将打车应用拆成了三个乘客服务、车主服务、支付服务。三个服务的业务特点各不相同，独立维护，各自都可以再次按需扩展。



https://book.douban.com/subject/20458253/

https://book.douban.com/subject/4160830/

https://zhuanlan.zhihu.com/p/79055107



AKF可扩展立方

Cube



https://github.com/dylanninin/dylanninin.github.com/issues/5/





联邦学习

金融







The Art of Scalability



Vp

Cto
architect 需要考虑的因素

cost effeict quality

The Art of Scalability

Chap. 12
RASCI模型

AKF的十二条架构设计原则


Chap. 13

JAd流程



Chap. 23



AKF扩展立方

Chap. 24

AKF扩展立方 数据库方向



Chap. 26
应用中的状态
消除状态
状态机
米利机
摩尔机





- Introduction to algorithms，作者首字母缩写 CLRS ，讲算法的。
- Structure and Interpretation of Computer Programs， 简称 SICP，一本有些被神化的书，不过的确值得一读。多数人初读此书，两章后会有眼前豁然开朗的感觉。虽然这书已经不再是教材了。封面是魔术师和 lamda 。什么是经典，这就是经典。计算机程序的构造和解释-SICP中文第2版
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







[10本经典书籍](https://mp.weixin.qq.com/s/oDWme4ZifffwB8-33IaGyw)




## 跨年摘录（2020–2026 日常笔记聚合，2026-09-23 整理）

### 2021-04
> 原理与设计：《大规模存储式系统》、《UNIX 网络编程 卷1:套接字联网 API》、《How Tomcat Works》。

