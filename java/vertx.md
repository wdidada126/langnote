# Vert.x框架


http://vertxchina.github.io/vertx-translation-chinese/
https://www.zhihu.com/question/277219881
https://blog.teemo.co/vertx-in-production-d5ca9e89d7c6

跟Spring Cloud对比的
https://quarkus.io/

https://www.zhihu.com/question/277219881/answer/1026585089


如果真的要比较的话，需要看你到底是要做一般性的快速项目开发，还是高并发系统的开发。如果做快速开发的话，我的推荐其实是Nutz，一个国内的框架。基本思路和Spring系列一致，但是上手难度更小。如果你需要应对复杂、业务规模庞大、不断变动和扩张的应用，那么暂时spring的地位还是难以撼动的。如果你开发的是一个高并发的系统，那我建议Vert.X是优先之选。Vert.X强的地方在于它的方法论。多处理器、高并发的需求，多数人都知道是要处理好同步、资源竞争、线程调度的问题。少部分人意识到异步是解决高并发的良好方案，但依然不够解决问题。只有在Akka/Actor这类方案出来之后，异步IO框架才逐渐认识到解决同步、资源竞争、线程调度的最好方法就是让它干脆不要出现。而在所有这类方案中，Vert.X是决心最大动作最彻底的。别的方案主要是基本核心等其他人扩充，Vert.X几乎是全家桶。举个例子，拿Vert.X和异步高并发界的知名前辈Nginx比较：Nginx大思路主要采用单线程模型，但是在会话秘钥等方面还是会需要内存共享。所以Nginx提供了专门的函数来处理共享内存，以及严禁复杂内存对象的共享。假如你在上面做研发，有些需求就没法实现。Vert.X则是从解决这个问题的思路就开始了重构，不是怎么去做内存共享，而是怎么让这个内存对象的访问都集中到同一线程，让内存共享的问题根本不出现。所以出现类似的情况，极少有需求用Vert.X不能实现，多半都是你没按照它的思路来理解问题。Vert.X的另外一个优点是，它没有象以前的NIO框架那样整出一套与常规编程逻辑大不相同的规范，它着力构造的是系统本身的运作方式，但尽量少干扰应用的编写。也就是说程序员需要学习的主要是解题思路，而不是解题写法。我个人觉得，Vert.X实际综合吸收了nodejs的单线程调度、netty的多处理器协同、Akka/Actor模型的优点，用它来解决高并发问题是非常优雅的，绝对不仅仅是XX版的node。但是从另外一方面来说，它的方法论太干净，很难与不一致的模块共处。要让程序员放弃自己熟悉的很多类库，或用全新的方法论来构造一个复杂的系统，都是有高度风险的选择。所以比较合理的方案是用Vert.X来构造系统中有高并发要求的微服务，其它复杂或者是没什么要求的部分还是采取传统方案。当然，对于单个人而言，同时掌握和应用两套思路完全不同的框架，确实会有更大的挑战。但这应该是很多程序猿的乐趣所在吧。


vert.x actor

[vertx github repo](https://github.com/eclipse-vertx/vert.x)

vertx是二进制可执行程序

[vertx examples](https://github.com/vert-x3/vertx-examples)

[创建并运行maven项目](https://blog.csdn.net/zhangzeyuaaa/article/details/39698479)

js demo vertx 3.7


server.js
```somecode

vertx.createHttpServer().requestHandler(function(req) {
  req.response.end("Hello World!");
}).listen(8280, 'localhost');

```

vertx run server.js

# Ver.x框架

[vertx github repo](https://github.com/eclipse-vertx/vert.x)

# vert



actor



天然分布式



JavaEE

限制多



actor模型

https://www.jianshu.com/p/d803e2a7de8e



https://blog.csdn.net/ieflex/article/details/98875107


### 测试 vert.x的仓库

https://gitee.com/edidada/testvertx

打印日志

slf4j log4j2
idea vm设置
-Dvertx.logger-delegate-factory-class-name=io.vertx.core.logging.SLF4JLogDelegateFactory

127.0.0.1:8080/shop

io.vertx.ext.web.impl.RoutingContextImplBase#routes
routes 是ConcurrentSkipListSet对象