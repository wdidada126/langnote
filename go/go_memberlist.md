# memberlist



https://github.com/hashicorp/memberlist



Golang package for gossip based membership and failure detection



go get -u github.com/hashicorp/memberlist



[结合consul serf理解gossip](https://www.jianshu.com/p/10f8743552ad)



[开源代码memberlist源码分析](https://blog.csdn.net/screscent/article/details/91984420)







实际上Gossip可以用于众多能接受“最终一致性”的领域：失败检测、路由同步、Pub/Sub、动态负载均衡。

但Gossip的缺点也很明显，冗余通信会对网路带宽、CUP资源造成很大的负载，而这些负载又受限于通信频率，该频率又影响着算法收敛的速度，后面我们会讲在各种场合下的优化方法。
————————————————
版权声明：本文为CSDN博主「纯粹的码农」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/chen77716/article/details/6275762

# 健壮性

Gossip协议下，没有任何扮演特殊角色的节点（比如leader等）。任何一个节点无论什么时候下线或者加入，并不会破坏整个系统的服务质量。

然而，Gossip协议也有不完美的地方，例如，**拜占庭**问题（Byzantine）。即，如果有一个恶意传播消息的节点，Gossip协议的分布式系统就会出问题。



作者：阿飞的博客
链接：https://www.jianshu.com/p/54eab117e6ae
来源：简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。



Gossip协议是一个通信协议，一种传播消息的方式，灵感来自于：瘟疫、社交网络等。使用Gossip协议的有：Redis Cluster、Consul、Apache Cassandra等。



https://zhuanlan.zhihu.com/p/41228196



https://blog.csdn.net/b6ecl1k7BS8O/article/details/86653449



https://www.iteblog.com/archives/2505.html



