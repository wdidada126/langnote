# redis_sentinel

http://ifeve.com/spring-boot-%e5%a6%82%e4%bd%95%e5%bf%ab%e9%80%9f%e9%9b%86%e6%88%90-redis-%e5%93%a8%e5%85%b5%ef%bc%9f/
没有 Redis Sentinel 架构之前，如果主节点挂了，需要运维人员手动进行主从切换，然后更新所有用到的 Redis IP 地址参数再重新启动系统，所有恢复操作都需要人为干预，如果半夜挂了，如果系统很多，如果某个操作搞错了，等等，这对运维人员来说简直就是恶梦。
有了 Redis Sentinel，主从节点故障都是自动化切换，应用程序参数什么也不用改，对于客户端来说都是透明无缝切换的，运维人员再也不用担惊受怕了。

https://www.jianshu.com/p/0e6fa34d07ad
cp /etc/redis-sentinel.conf  /etc/redis-sentinel_26380.conf

port 26380

mymaster password
pidfile
logfile
mymaster ip 端口

redis-sentinel /etc/redis-sentinel.conf &
redis-sentinel /etc/redis-sentinel_26380.conf &

sentinel配置之后，jedis，rediscli,图形工具连接sentinel的ip和端口，不是连接redis-server的

https://www.cnblogs.com/kevingrace/p/9004460.html
https://blog.csdn.net/guying4875/article/details/79045075

http://redisdoc.com/topic/sentinel.html


jedis连接redis master slave sentinel
https://blog.csdn.net/guying4875/article/details/79045075


```shell
redis-sentinel -h
Usage: ./redis-server [/path/to/redis.conf] [options]
       ./redis-server - (read config from stdin)
       ./redis-server -v or --version
       ./redis-server -h or --help
       ./redis-server --test-memory <megabytes>

Examples:
       ./redis-server (run the server with default conf)
       ./redis-server /etc/redis/6379.conf
       ./redis-server --port 7777
       ./redis-server --port 7777 --slaveof 127.0.0.1 8888
       ./redis-server /etc/myredis.conf --loglevel verbose

Sentinel mode:
       ./redis-server /etc/sentinel.conf --sentinel
```

sentinel是主从模式基础上改进的
https://blog.csdn.net/qq_28410283/article/details/89197156


在Redis支持集群(3.0)之前，官方推荐高可用解决方案为Redis-sentinel，使用起来也比较简单。
https://www.jianshu.com/p/cbd40a188226