# twemproxy

[twemproxy](https://github.com/twitter/twemproxy)

A fast, light-weight proxy for memcached and redis

支持k8s



twitter公司开源





redis集群方案，有两种

sharding

redis cluster





Twemproxy 又称nutcracker ，是一个memcache、Redis协议的轻量级代理，一个用于sharding 的中间件。有了Twemproxy，客户端不直接访问Redis服务器，而是通过twemproxy 代理中间件间接访问。 Twemproxy 为 Twitter 开源产品，简单来说，Twemproxy是Twitter开发的一个redis代理proxy，类似于nginx的反向代理或者mysql的代理工具，如amoeba。Twemproxy通过引入一个代理层，可以将其后端的多台Redis或Memcached实例进行统一管理与分配，使应用程序只需要在Twemproxy上进行操作，而不用关心后面具体有多少个真实的Redis或Memcached存储。