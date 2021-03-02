# redis_sentinel

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