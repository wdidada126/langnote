# clion



cmake

[CLion开发编译调试Makefile项目](https://blog.csdn.net/lylwo317/article/details/86673912)



完成RPC 需要两个协议： 对象序列化协议  和 调用控制协议

常见例子举例：

1.zeroC ICE，拥有自己的网络通信框架 + ICE 调用控制协议和对象序列化协议,同时也涵盖了服务组件的抽象部署等功能。

2.thrift，有自己的网络通信框架+thrift 对象序列化协议+thrift 调用控制协议

3.probuff，只是 对象序列化协议

4.XMLRPC ，jsonRPC，常见的语境是利用HTTP协议作为调用控制协议,XML 和 JSON 作为对象序列化之后的格式。





云原声的rpc协议 grpc







后端前景

云服务把标准化的后端比如数据库／缓存／邮件／监控都给你做好了，后端业务代码还得写啊，云厂家又不可能帮你写出一个在线支付程序。

Clion支持makefile



ThoughtWorks
如何评价 TAPIR 分布式事务协议

论文地址：[http://syslab.cs.washington.edu/papers/tapir-tr14.pdf](http://syslab.cs.washington.edu/papers/tapir-tr14.pdf)
通过区分 inconsistent 和 consensus 两种操作来放宽对事务中操作顺序的要求，另外通过一个 sync 过程来同步各副本间的记录。似乎有很多的限制条件，有很多 corner case 需要考虑。

有没有哪个已知生产系统使用了这个协议？





https://www.youtube.com/watch?v=yE3eMxYJDiE

我个人是这么理解的, 没 leader 的强一致复制协议(如经典 Paxos)是不保证多少次 RTT 才能达成一致的, 好巧, 分布式事务也是不保证的. 那么无穷大 + 无穷大还是等于无穷大.

那么就干脆别搞强一致了, client 直接广播请求到那个 shard 下所有 replicas, 让分布式事务层辛苦点可能要多重试几次. 确定性的收益是最优情况下, RTT 从 2 降低到了 1, 最差情况反正是无穷大, 不差再多几个 RTT.

没想得很明白的是 abort 要怎么做, 总感觉哪里有问题. 求教



作者：匿名用户
链接：https://www.zhihu.com/question/56763641/answer/1016947765
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。





ThoughtWorks
