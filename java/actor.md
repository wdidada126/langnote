# actor

[了解 Actor 模型](https://www.jianshu.com/p/449850aa8e82)

<<<<<<< HEAD
并行

并不擅长密集计算



akka

https://github.com/guobinhit/akka-guide

scala

https://github.com/guobinhit/akka-guide/blob/master/articles/qucikstart-akka-java.md

=======
>>>>>>> afe522da082020e5ece0b75c43067644b2edb768


Actors

一个Actor指的是一个最基本的计算单元。它能接收一个消息并且基于其执行计算。
这个理念很像面向对象语言，一个对象接收一条消息（方法调用），然后根据接收的消息做事（调用了哪个方法）。
Actors一大重要特征在于actors之间相互隔离，它们并不互相共享内存。这点区别于上述的对象。也就是说，一个actor能维持一个私有的状态，并且这个状态不可能被另一个actor所改变。



为什么Actor模型是高并发事务的终极解决方案





threads并不是获取并发性的好方法，往往会带来难以查找的bug



今天我们有很多其他方法来获得易用的并发性，比如我们接下来介绍的Actor模型。



使用这套规则的编程语言是Erlang







使用Disruptor这样无锁队列也可以自己实现Actor模型，让一个普通对象与外界的交互调用通过Disruptor消息队列实现，比如LMAX架构就是这样实现高频交易，从2009年成功运行至今，被Martin Fowler推崇。



<<<<<<< HEAD
### ECUP



Effective Cloud User Group





Skynet



https://www.jianshu.com/p/c69e69c9c0a9



vert.x



=======
>>>>>>> afe522da082020e5ece0b75c43067644b2edb768
