# cas


利用CAS操作（Compare & Set）实现无锁队列


https://zhuanlan.zhihu.com/p/80727111

无锁队列的链表实现
下面的东西主要来自John D. Valois 1994年10月在拉斯维加斯的并行和分布系统系统国际大会上的一篇论文——《Implementing Lock-Free Queues》。

我们先来看一下进队列用CAS实现的方式：
https://blog.csdn.net/syzcch/article/details/8075830
