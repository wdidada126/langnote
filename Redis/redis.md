# redis



常用的消息队列有RabbitMQ,ActiveMQ，个人觉得这种消息队列太大太重，本文介绍下基于redis的轻量级消息队列服务。 

一般来说，消息队列有两种模式，一种是发布者订阅模式，另外一种是生产者和消费者模式。Redis的消息队列，也是基于这2种原理的实现。 
发布者和订阅者模式：发布者发送消息到队列，每个订阅者都能收到一样的消息。 
生产者和消费者模式：生产者将消息放入队列，多个消费者共同监听，谁先抢到资源，谁就从队列中取走消息去处理。注意，每个消息只能最多被一个消费者接收。

![redis windows](images/redis_windows.png)

dump.rdb

Redis cluster是gossip协议

Redis 集群和sentinal模式的区别
数据集中存储，所有节点都有

windows图形客户端

https://blog.csdn.net/qq_38709953/article/details/80914965

不能执行命令



Redis，单线程，同一台服务器部署多台

由于redisson不光是针对锁，提供了很多客户端操作redis的方法，所以会依赖一些其它的框架，比如netty，如果只是简单的使用锁也可以自己去实现。


redisson实现分布式锁原理
https://m.jb51.net/article/105186.htm

Redid lua是原子操作，要么全执行，要么全部不执行，执行到一半，回滚？

WAL

因此业界常用的解决方案通常是借助于一个第三方组件并利用它自身的排他性来达到多进程的互斥。如：  基于 DB 的唯一索引。  基于 ZK 的临时有序节点。  基于 Redis 的 NX EX 参数。

基于 Redis 的分布式锁、日志系统、消息队列、数据清洗等，各种各样的功能不断上线，从而引发各种各样的问题。运维天天疲于奔命，到处处理着 Redis 堵塞、网卡打爆、连接数爆表……”

ntp时间同步，时差0.2mm，如何解决



redis 3 cluster

zset实现

https://blog.csdn.net/Androidlushangderen/article/details/39803337

redis zset内部实现
https://zsr.github.io/2017/07/03/redis-zset%E5%86%85%E9%83%A8%E5%AE%9E%E7%8E%B0/

`redis-cli -h 172.16.0.2 -p 6379 -a 5@Edidada`

hash

hset 路径 key value

路径如何分文件夹 redis-session就分了

0616:12

setbit
getbit
bitcount

[HyperLogLog](https://en.wikipedia.org/wiki/HyperLogLog)

PFADD
PFCOUNT

Redis

 Redis 崩溃后数据处理？

序列化到本地

aof



手写Redis客户端-实现自己的Jedis

 https://blog.csdn.net/ljheee/article/details/103882807



 https://blog.csdn.net/she_lock/article/details/103859781 



 https://blog.csdn.net/breaksoftware/article/details/53393191 



 https://blog.csdn.net/breaksoftware/category_9272302.html 



https://www.runoob.com/redis/redis-tutorial.html



http://try.redis.io/



[Redis 常用命令](https://blog.csdn.net/weixin_30498807/article/details/98350192)



redis理解key

```
redis-cli -p 5566 -a password
EXISTS key//
KSYS *4//
TYPE key
set a b;
get a;
del a;
get a;
set one 1;
set two 2;
mget one two;



hmset key valueKey value//如何设置多个？
HGETALL key//获取所有的
获取hash所有key HKEYS key
获取hash所有key的value HVALS key
获取hash内键值对的长度 HLEN key
给一个hash的某个键值对赋值 HSET key valueKey value
当hash中valueKey不存在时赋值 HSETNX key valueKey value








List
给list赋值 LPUSH listName value
按照索引取值 LINDEX listName 1
```





一、Redis之Set简介
1. Set是String类型的无序集合（元素成员唯一）。
2. Set是通过hash表实现的，添加、删除、查找的复杂度都是O(1)。
3. 每个集合最大成员数为232-1（40多亿）个。

 

二、Redis之Set命令行操作
Sadd：将一个或多个元素加入集合，已经存在集合中的元素则忽略。若集合不存在则先创建，若key不是集合类型则返回错误。
Smembers：返回集合中所有成员。
Sismember：判断指定元素是否是指定集合的成员，是返回1，否则返回0。
Scard：返回集合中元素的数量。



redis防穿透设计


补充一点，对于每次都查询key不同的数据，如果缓存中不存在数据，则每次查询都会落到DB上面，仍然会造成缓存穿透。

对于这种情况，可以考虑进一步增强健壮性。

方法一：判断key是否存在。比如说先把key放在缓存中，存在再去查数据。缺点是数据量一旦比较大，代价很高，而且新增了key还要维护这个集合。

方法二：依照某种规则设计key，查询之前根据规则校验key的合法性，如果不合法直接返回。

可以引入布隆过滤器配合解决缓存穿透的问题






Redis防穿透设计





微信大神群



redis

序列化到磁盘的时候 超时



在使用redis-cluster集群的时候，禁用主节点的持久化有没有啥风险

现在发现主节点做持久化，fork子进程的时候，会阻塞

抢购的时候就出事了

只有抢购接口能用这个集群吗

不是所有的都用，集群里面都是缓存数据

噢，开的aof？

rdb

每次刷盘都会fork啊这是，很多应用都去一个集群挤，可能数据量就大了，而且还用的是 rdb，每次都要刷完整快照，超过百兆那个延迟可能就受不了，我理解耗时在fork操作，后面刷盘是子进程做的，主进程查询依然不受影响，这个理解有没有啥问题，老哥，不是的，fork的时候子进程要拿到当前redis数据库的状态，这个数据复制是需要时间的，而且你会看到内存暴增，因为大概是两倍的用量，一个物理机可以考虑多redis进程，用不同端口，分应用连接，管理下就好了。这样可以rdb 和 aof 分开用



fork的时候还需要复制数据，我们都是一台机器一个redis实例，资源可以浪费，服务不能挂，反正就多几个实例吧，之前在哪看的来着，有大手子建议redis一个实例内存占用限到2g，然后起多实例用...还有一个，fork复制的时候，是复制全量数据吗，rdb 是啊，全量快照，还是类似做分页，标记dirty页，然后复制dirty页






redis 某某公司是用sentinel，没上cluster



2020 Redis 6



https://github.com/antirez/redis/tree/6.0



**一、对用户使用有直接影响的功能**

1. ACL用户权限控制功能
2. RESP3：新的 Redis 通信协议
3. Cluster 管理工具
4. SSL 支持

**二、Redis 内部的优化**

1. IO多线程支持
2. 新的Module API
3. 新的 Expire 算法

**三、外部工具**

1. Redis Cluster Proxy
2. Disque



[Redis Day New York 上的分享在YouTube ](https://www.youtube.com/watch?v=lo-Pgf_l7_M)



问：如何熟悉Redis

先学会用   然后会用了自然想去了解细节



### changelog

6 2020

5 2018

4 2017

3 2015



### mail list



https://redis.io/community

https://groups.google.com/forum/#!topic/redis-db/

```
redis



info



info

# Server

redis_version:3.2.100

redis_git_sha1:00000000

redis_git_dirty:0

redis_build_id:dd26f1f93c5130ee

redis_mode:standalone

os:Windows

arch_bits:64

multiplexing_api:WinSock_IOCP

process_id:5304

run_id:f8eba9288a0216030c2d5e923a4743d94f774278

tcp_port:6379

uptime_in_seconds:523316

uptime_in_days:6

hz:10

lru_clock:4401641

executable:D:\Program\Redis\"D:\Program\Redis\redis-server.exe"

config_file:D:\Program\Redis\redis.windows-service.conf



# Clients

connected_clients:1

client_longest_output_list:0

client_biggest_input_buf:0

blocked_clients:0



# Memory

used_memory:690424

used_memory_human:674.24K

used_memory_rss:652512

used_memory_rss_human:637.22K

used_memory_peak:766536

used_memory_peak_human:748.57K

total_system_memory:0

total_system_memory_human:0B

used_memory_lua:37888

used_memory_lua_human:37.00K

maxmemory:0

maxmemory_human:0B

maxmemory_policy:noeviction

mem_fragmentation_ratio:0.95

mem_allocator:jemalloc-3.6.0



# Persistence

loading:0

rdb_changes_since_last_save:0

rdb_bgsave_in_progress:0

rdb_last_save_time:1597713845

rdb_last_bgsave_status:ok

rdb_last_bgsave_time_sec:-1

rdb_current_bgsave_time_sec:-1

aof_enabled:0

aof_rewrite_in_progress:0

aof_rewrite_scheduled:0

aof_last_rewrite_time_sec:-1

aof_current_rewrite_time_sec:-1

aof_last_bgrewrite_status:ok

aof_last_write_status:ok



# Stats

total_connections_received:1

total_commands_processed:1

instantaneous_ops_per_sec:0

total_net_input_bytes:43

total_net_output_bytes:5889929

instantaneous_input_kbps:0.01

instantaneous_output_kbps:0.02

rejected_connections:0

sync_full:0

sync_partial_ok:0

sync_partial_err:0

expired_keys:0

evicted_keys:0

keyspace_hits:0

keyspace_misses:0

pubsub_channels:0

pubsub_patterns:0

latest_fork_usec:0

migrate_cached_sockets:0



# Replication

role:master

connected_slaves:0

master_repl_offset:0

repl_backlog_active:0

repl_backlog_size:1048576

repl_backlog_first_byte_offset:0

repl_backlog_histlen:0



# CPU

used_cpu_sys:0.23

used_cpu_user:0.27

used_cpu_sys_children:0.00

used_cpu_user_children:0.00



# Cluster

cluster_enabled:0



# Keyspace













redis



info

# Server

redis_version:4.0.9

redis_git_sha1:00000000

redis_git_dirty:0

redis_build_id:9435c3c2879311f3

redis_mode:standalone

os:Linux 4.4.0-18362-Microsoft x86_64

arch_bits:64

multiplexing_api:epoll

atomicvar_api:atomic-builtin

gcc_version:7.4.0

process_id:26042

run_id:331aafdd90fff400a457d626345973ff5ef00511

tcp_port:6379

uptime_in_seconds:5

uptime_in_days:0

hz:10

lru_clock:4401729

executable:/usr/bin/redis-server

config_file:/etc/redis/redis.conf



# Clients

connected_clients:1

client_longest_output_list:0

client_biggest_input_buf:0

blocked_clients:0



# Memory

used_memory:842296

used_memory_human:822.55K

used_memory_rss:2306048

used_memory_rss_human:2.20M

used_memory_peak:842296

used_memory_peak_human:822.55K

used_memory_peak_perc:100.13%

used_memory_overhead:832486

used_memory_startup:782480

used_memory_dataset:9810

used_memory_dataset_perc:16.40%

total_system_memory:8500387840

total_system_memory_human:7.92G

used_memory_lua:37888

used_memory_lua_human:37.00K

maxmemory:0

maxmemory_human:0B

maxmemory_policy:noeviction

mem_fragmentation_ratio:2.74

mem_allocator:jemalloc-3.6.0

active_defrag_running:0

lazyfree_pending_objects:0



# Persistence

loading:0

rdb_changes_since_last_save:0

rdb_bgsave_in_progress:0

rdb_last_save_time:1598237244

rdb_last_bgsave_status:ok

rdb_last_bgsave_time_sec:-1

rdb_current_bgsave_time_sec:-1

rdb_last_cow_size:0

aof_enabled:0

aof_rewrite_in_progress:0

aof_rewrite_scheduled:0

aof_last_rewrite_time_sec:-1

aof_current_rewrite_time_sec:-1

aof_last_bgrewrite_status:ok

aof_last_write_status:ok

aof_last_cow_size:0



# Stats

total_connections_received:1

total_commands_processed:1

instantaneous_ops_per_sec:0

total_net_input_bytes:31

total_net_output_bytes:10163

instantaneous_input_kbps:0.00

instantaneous_output_kbps:0.00

rejected_connections:0

sync_full:0

sync_partial_ok:0

sync_partial_err:0

expired_keys:0

expired_stale_perc:0.00

expired_time_cap_reached_count:0

evicted_keys:0

keyspace_hits:0

keyspace_misses:0

pubsub_channels:0

pubsub_patterns:0

latest_fork_usec:0

migrate_cached_sockets:0

slave_expires_tracked_keys:0

active_defrag_hits:0

active_defrag_misses:0

active_defrag_key_hits:0

active_defrag_key_misses:0



# Replication

role:master

connected_slaves:0

master_replid:86b3b60425334c899af4f9ea85a9891c7c17f777

master_replid2:0000000000000000000000000000000000000000

master_repl_offset:0

second_repl_offset:-1

repl_backlog_active:0

repl_backlog_size:1048576

repl_backlog_first_byte_offset:0

repl_backlog_histlen:0



# CPU

used_cpu_sys:0.02

used_cpu_user:0.00

used_cpu_sys_children:0.00

used_cpu_user_children:0.00



# Cluster

cluster_enabled:0



# Keyspace

db0:keys=7,expires=0,avg_ttl=0







redis-stat is a simple Redis monitoring tool written in Ruby.

https://github.com/junegunn/redis-stat



zabbix也提供了相关的插件对redis服务进行监控



Redis几个重要的健康指标 zotero





MemAdmin

通过一些开源的第三方工具对整个memcached集群进行监控，显示会更直观

https://www.cnblogs.com/dinglang/p/6117309.html


```

