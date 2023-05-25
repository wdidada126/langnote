# redis

小林图解redis系列
https://xiaolincoding.com/redis/



redis源代码阅读
https://blog.huangz.me/diary/2014/how-to-read-redis-source-code.html

https://github.com/redis/redis/tree/7.0
支持Linux Unix freeBSD openBSD
makefile



Redis的并发竞争问题如何解决
Redis的并发竞争问题主要表现为多个客户端同时请求Redis服务器，可能会出现多个客户端同时对同一个键值进行读写操作，导致数据不一致的问题。

以下是几种解决Redis并发竞争问题的方式：

使用Redis事务：Redis事务可以将一组操作打包成一个原子性的操作，保证多个客户端操作的原子性。

使用Redis分布式锁：通过对需要进行互斥的代码块加锁的方式，保证同一时间只有一个客户端可以对其进行操作。

使用Redis乐观锁：通过使用Redis的CAS操作（compare and set），在每次更新操作时判断当前版本是否正确，如果正确则执行更新操作，否则返回失败。

使用Redis队列：通过将多个客户端对同一个键值的请求存入队列中，再通过单独的线程对队列中的请求进行操作，保证多个客户端对同一键值的操作按照先后顺序执行。

需要注意的是，以上方法并不是绝对可靠的，不同的并发场景下适用的解决方案也有所不同。因此，在设计应用时应该根据实际情况选择合适的并发解决方案。




redis实现消息队列

Redis可以通过List数据类型实现消息队列。具体实现方式如下：

将消息存储到List中：使用Redis的LPUSH命令将消息推入到List的左侧，表示这是一个最新的消息。

从消息队列中获取消息：使用Redis的RPOP命令从List的右侧弹出一条消息，表示这是最旧的消息。

处理消息：从消息队列中获取到消息后，对消息进行处理。

重复执行：在消息处理完成后，返回步骤2，从消息队列中获取下一条消息进行处理。

需要注意的是，在实现Redis消息队列时，需要考虑多个客户端同时对同一个消息队列进行读写操作的并发情况。可以使用Redis的BLPOP命令来实现多个客户端并发读取同一个消息队列的操作。

此外，Redis的消息队列也可以实现消息发布/订阅模式。当有消息需要发布时，可以将消息推入到指定的通道中，所有订阅该通道的客户端都会收到该消息。实现方式可以使用Redis的PUBLISH命令实现。



除了使用Redis的List数据类型实现消息队列，还可以使用ZSet（有序集合）数据类型来实现。

在使用ZSet实现消息队列时，可以将消息的时间戳作为ZSet的分值（score），将消息的内容作为ZSet的成员（member）。这样，可以通过ZSet的分值来对消息进行排序，保证消息按照时间顺序排列。

具体实现方式如下：
将消息存储到ZSet中：使用Redis的ZADD命令将消息添加到ZSet中，将消息的时间戳作为分值，消息内容作为成员。如果需要添加多个消息，可以一次性添加多个消息。
从消息队列中获取消息：使用Redis的ZRANGE命令从ZSet中获取分值最小的一条消息，并返回消息的成员（即消息内容）。
处理消息：从消息队列中获取到消息后，对消息进行处理。
重复执行：在消息处理完成后，返回步骤2，从消息队列中获取下一条消息进行处理。
需要注意的是，ZSet中同一个成员只能有一个分值，因此不能将同一条消息重复添加到ZSet中。如果需要保证同一个消息可以被多次处理，可以使用不同的标识符（如UUID）作为消息的成员，同时将消息的实际内容保存在另外的数据结构中，例如Hash表。
此外，与List实现消息队列类似，也需要考虑多个客户端同时对同一个ZSet进行读写操作的并发情况。可以使用Redis的ZPOPMIN命令来实现多个客户端并发读取同一个消息队列的操作。
使用ZSet实现消息队列的库有很多，以下是其中的几个：
Redisson：Redisson是一个基于Redis的分布式Java对象和服务框架，提供了ZSet实现消息队列的功能。Redisson封装了Redis的ZADD和ZRANGE命令，提供了丰富的ZSet操作方法，使得使用ZSet实现消息队列更加方便。
lettuce：lettuce是一个高性能的Java Redis客户端，也提供了ZSet实现消息队列的功能。lettuce使用了异步、非阻塞的I/O操作，可以实现高并发的读写操作。
Jedis：Jedis是一个Java Redis客户端，也可以使用ZSet实现消息队列。Jedis对Redis的ZADD和ZRANGE命令进行了封装，提供了类似于Java集合的操作方式，更加方便使用。
除了这些库之外，还可以直接使用Redis的ZADD、ZRANGE等命令，自己编写代码实现ZSet实现消息队列的功能。










redis list底层数据结构

Redis List底层数据结构是双向链表，它是由多个列表节点（List Node）组成的链表。每个列表节点包含了三个属性：

前置节点指针（prev）：指向前置节点的指针，如果当前节点是头节点，则前置节点为NULL。
后置节点指针（next）：指向后置节点的指针，如果当前节点是尾节点，则后置节点为NULL。
节点值（value）：列表节点保存的值。
Redis List的实现是一个双向链表，这个链表的每个节点都包含了一个列表项（listNode）和两个指针（prev和next），这个链表既可以从头部遍历，也可以从尾部遍历。在Redis中，每个List对应一个链表，List中的每个元素都对应着一个节点。Redis使用双向链表而不是数组的好处在于，在进行添加、删除操作时可以更加高效，不需要像数组那样重新分配内存和移动数据。

redis list压缩表
Redis List的底层数据结构可以使用压缩列表（ziplist）实现。压缩列表是一种紧凑的、连续的、可压缩的顺序数据结构，它的内存占用更小、访问速度更快，适合存储一些较小的数据。Redis中，当List满足一定条件时，就会将其转换为压缩列表，从而降低内存使用。

Redis的压缩列表的结构与普通的双向链表不同，它将多个节点的数据连续存放在一段连续的内存区域中，每个节点的结构如下：

zlbytes	zltail	entry1	entry2	...	entryN	zlend
其中：

zlbytes：压缩列表的长度（以字节为单位）。
zltail：最后一个元素的偏移量（以字节为单位），即压缩列表的尾部。
entryX：列表中的元素，其大小和类型由具体的实现决定。
zlend：标识压缩列表的结束位置。
压缩列表在进行插入、删除等操作时，会进行动态扩容和缩容，其原理类似于动态数组。在扩容时，压缩列表会先预留一些空间，当列表中的元素个数超过了预留空间时，就会自动扩容。在缩容时，压缩列表会检查是否有多余的空间，如果有，则会自动缩容。

在Redis中，可以通过CONFIG SET命令的list-max-ziplist-entries选项来设置当List转换为压缩列表时的最大元素数量，以及通过list-max-ziplist-value选项来设置单个元素的最大值。


redisinsight 最好用的redis图形工具

https://spring.io/projects/spring-data-redis





从单机到2000万QPS: 知乎Redis平台发展与演进之路

https://zhuanlan.zhihu.com/p/48694169





redis深度探险

布隆过滤器

管道

事务



Redis 延迟 面试题 纯技术的

https://zhuanlan.zhihu.com/p/108212058

延迟（Latency）是指从客户端发送命令到客户端接收到命令返回值的时间间隔。所以我们先来看一下 Redis 一条命令执行的步骤，其中每个步骤出问题都可能导致高延迟。



remote dictionary service 首字母缩写

codis

redis最新版安装 centos平台
https://computingforgeeks.com/how-to-install-latest-redis-on-centos-7/

yum -y install http://rpms.remirepo.net/enterprise/remi-release-7.rpm
yum --enablerepo=remi install redis -y


Redis协议里有大量冗余的回车换行符，但是这不影响它成为互联网技术领域非常受欢迎的一个文本协议。有很多开源项目使用阻SP作为它的通讯协议


- Redis深度历险 书籍
- Redis实战
- Redis权威指南
- Redis设计与实现
- Redis5设计与源码分析

ltamar Haber

Redis图形客户端
rdm windows 自己编译的版本

redis 6支持自定义用户名


https://www.runoob.com/redis/redis-sorted-sets.html

http://doc.redisfans.com/

Key（键）
DEL
DUMP
EXISTS
EXPIRE
EXPIREAT
KEYS
MIGRATE
MOVE
OBJECT
PERSIST
PEXPIRE
PEXPIREAT
PTTL
RANDOMKEY
RENAME
RENAMENX
RESTORE
SORT
TTL
TYPE
SCAN


String（字符串）
APPEND
BITCOUNT
BITOP
DECR
DECRBY
GET
GETBIT
GETRANGE
GETSET
INCR
INCRBY
INCRBYFLOAT
MGET
MSET
MSETNX
PSETEX
SET
SETBIT
SETEX
SETNX
SETRANGE
STRLEN


Hash（哈希表）
HDEL
HEXISTS
HGET
HGETALL
HINCRBY
HINCRBYFLOAT
HKEYS
HLEN
HMGET
HMSET
HSET
HSETNX
HVALS
HSCAN


List（列表）
BLPOP
BRPOP
BRPOPLPUSH
LINDEX
LINSERT
LLEN
LPOP
LPUSH
LPUSHX
LRANGE
LREM
LSET
LTRIM
RPOP
RPOPLPUSH
RPUSH
RPUSHX


Set（集合）
SADD
SCARD
SDIFF
SDIFFSTORE
SINTER
SINTERSTORE
SISMEMBER
SMEMBERS
SMOVE
SPOP
SRANDMEMBER
SREM
SUNION
SUNIONSTORE
SSCAN


SortedSet（有序集合）
ZADD
ZCARD
ZCOUNT
ZINCRBY
ZRANGE
ZRANGEBYSCORE
ZRANK
ZREM
ZREMRANGEBYRANK
ZREMRANGEBYSCORE
ZREVRANGE
ZREVRANGEBYSCORE
ZREVRANK
ZSCORE
ZUNIONSTORE
ZINTERSTORE
ZSCAN


Pub/Sub（发布/订阅）
PSUBSCRIBE
PUBLISH
PUBSUB
PUNSUBSCRIBE
SUBSCRIBE
UNSUBSCRIBE


Transaction（事务）
DISCARD
EXEC
MULTI
UNWATCH
WATCH


Script（脚本）
EVAL
EVALSHA
SCRIPT EXISTS
SCRIPT FLUSH
SCRIPT KILL
SCRIPT LOAD


Connection（连接）
AUTH
ECHO
PING
QUIT
SELECT


Server（服务器）
BGREWRITEAOF
BGSAVE
CLIENT GETNAME
CLIENT KILL
CLIENT LIST
CLIENT SETNAME
CONFIG GET
CONFIG RESETSTAT
CONFIG REWRITE
CONFIG SET
DBSIZE
DEBUG OBJECT
DEBUG SEGFAULT
FLUSHALL
FLUSHDB
INFO
LASTSAVE
MONITOR
PSYNC
SAVE
SHUTDOWN
SLAVEOF
SLOWLOG
SYNC
TIME




systemctl disable redis.service

https://forum.redislabs.com/

#### sentinel 2.8支持

/etc/redis-sentinel.conf


##### redis 3.2 master slave 配置
https://www.cnblogs.com/chenmh/p/5121849.html
从redis2.6版本开始，slave支持只读模式
https://segmentfault.com/a/1190000006619753

slave of节点需要配置master密码
https://blog.csdn.net/weixin_30949361/article/details/95011761

Lua 脚本的最大执行时间，毫秒为单位
lua-time-limit 5000

Redis慢查询日志可以记录超过指定时间的查询
slowlog-log-slower-than 10000

这个长度没有限制。只是要主要会消耗内存。你可以通过 SLOWLOG RESET 来回收内存。
slowlog-max-len 128



Redis Dbsize 命令用于返回当前数据库的 key 的数量。




redis 3.2 protect mode，限定特定网卡/ip的地址才能访问
redis-cli登录之后，
auth


#### Redis 分区

#### 性能测试
https://www.runoob.com/redis/redis-benchmarks.html
monotor监控

```
redis-benchmark -n 10000  -q
PING_INLINE: 63694.27 requests per second
PING_BULK: 69444.45 requests per second
SET: 56497.18 requests per second
GET: 69930.07 requests per second
INCR: 66666.66 requests per second
LPUSH: 64935.07 requests per second
LPOP: 68965.52 requests per second
SADD: 63694.27 requests per second
SPOP: 69444.45 requests per second
LPUSH (needed to benchmark LRANGE): 65359.48 requests per second
LRANGE_100 (first 100 elements): 28735.63 requests per second
LRANGE_300 (first 300 elements): 15151.51 requests per second
LRANGE_500 (first 450 elements): 10559.66 requests per second
LRANGE_600 (first 600 elements): 8271.30 requests per second
MSET (10 keys): 42735.04 requests per second
```


```shell
redis-benchmark -n 10000  -q -h 60.205.225.118 -a 5%Edidada
PING_INLINE: 1992.03 requests per second
PING_BULK: 2007.63 requests per second
SET: 1980.59 requests per second
GET: 1954.27 requests per second
INCR: 1963.86 requests per second
LPUSH: 1984.52 requests per second
LPOP: 1953.89 requests per second
SADD: 1967.34 requests per second
SPOP: 1977.85 requests per second
LPUSH (needed to benchmark LRANGE): 1844.68 requests per second
LRANGE_100 (first 100 elements): 75.52 requests per second
LRANGE_300 (first 300 elements): 31.75 requests per second
LRANGE_500 (first 450 elements): 25.80 requests per second
LRANGE_600 (first 600 elements): 19.79 requests per second
MSET (10 keys): 1910.95 requests per second
```

备份
save
bgsave
listsave

MONITOR monitor
实时打印出 Redis 服务器接收到的命令，调试用

CONFIG get requirepass

常用数据类型 5种
String（字符串）
Hash（哈希）
List（列表）
Set（集合）
zset(sorted set：有序集合)



Redis数据结构(9种)
String：二进制安全的字符串
Lists：安插入顺序排序的字符串元素集合。基本是链表。
Sets：无序不重复集合。
Sorted sets(zset)：里面的元素总是通过score进行排序。有序集合。
Hashes：键值都是字符串的哈希表。
Bit arrays：位集合（可以实现类似布隆过滤器的功能结构）
HyperLogLog：是用来做基数统计的算法。用于估计一个set中元素数量的概率性的数据结构。
Geospatial Indexes：地理空间索引
Streams：流信息

https://blog.csdn.net/chenhailonghp/article/details/105388802



add sadd zadd

HMSET
hget

lpush lrange

del
lrange xxx 0 10
lrem


sadd
smembers


exist key


#### redis pub sub
SUBSCRIBE runoobChat
https://www.runoob.com/redis/redis-pub-sub.html

PUBLISH runoobChat "Learn redis by runoob.com"
#### transaction

MULTI
EXEC

Redis 事务可以一次执行多个命令， 并且带有以下三个重要的保证：
批量操作在发送 EXEC 命令前被放入队列缓存。
收到 EXEC 命令后进入事务执行，事务中任意命令执行失败，其余的命令依然被执行。
在事务执行过程，其他客户端提交的命令请求不会插入到事务执行命令序列中。



AUTH password
验证密码是否正确

ECHO message
打印字符串

PING
查看服务是否运行

QUIT
关闭当前连接

SELECT index
切换到指定的数据库


INFO



redis


配置redis 跟MySQL对比
- 临时生效 命令行
- 永久生效 配置文件


https://www.cnblogs.com/woshimrf/p/5208072.html

CONFIG SET loglevel "verbose"
https://www.runoob.com/redis/redis-conf.html
指定日志记录级别，Redis总共支持四个级别：debug、verbose、notice、warning

https://www.runoob.com/redis/redis-install.html


```shell
redis-cli -a 5%Edidada
127.0.0.1:6379> CONFIG GET dir
1) "dir"
2) "/var/lib/redis"
127.0.0.1:6379> exit
[root@iZ2ze9f7g12pq4tby7ewz2Z ~]# cd /var/lib/redis
[root@iZ2ze9f7g12pq4tby7ewz2Z redis]# ll
total 8
-rw-r--r-- 1 root root   0 Aug 11  2018 appendonly.aof
-rw-r--r-- 1 root root 251 Mar  2 14:44 dump.rdb
-rw-r--r-- 1 root root 112 Aug 11  2018 nodes-6379.conf
```


redis-cli -h host -p port -a password  可以直接输入密码 不是-p，是-a
```shell
redis-cli 60.205.225.118
(error) ERR unknown command '60.205.225.118'
PS C:\Users\chengwu2> redis-cli -h 60.205.225.118
60.205.225.118:6379> auth 5%Edidada
OK
60.205.225.118:6379> ping
PONG
60.205.225.118:6379> exit
PS C:\Users\chengwu2> redis-cli -h 60.205.225.118
60.205.225.118:6379> ping
(error) NOAUTH Authentication required.
60.205.225.118:6379> auth 5%Edidada
OK
60.205.225.118:6379> ping
PONG
60.205.225.118:6379>
```

redis 设置密码
https://redis.io/topics/security
https://www.cnblogs.com/keystone/p/10653836.html

https://redis.io/documentation


```shell
rpm -pql remi-release-8.rpm
warning: remi-release-8.rpm: Header V4 RSA/SHA256 Signature, key ID 5f11735a: NOKEY
/etc/pki/rpm-gpg/RPM-GPG-KEY-remi
/etc/pki/rpm-gpg/RPM-GPG-KEY-remi.el8
/etc/pki/rpm-gpg/RPM-GPG-KEY-remi2017
/etc/pki/rpm-gpg/RPM-GPG-KEY-remi2018
/etc/pki/rpm-gpg/RPM-GPG-KEY-remi2019
/etc/pki/rpm-gpg/RPM-GPG-KEY-remi2020
/etc/pki/rpm-gpg/RPM-GPG-KEY-remi2021
/etc/yum.repos.d/remi-modular.repo
/etc/yum.repos.d/remi-safe.repo
/etc/yum.repos.d/remi.repo
[root@iZ2ze9f7g12pq4tby7ewz2Z ~]# rpm -ivh remi-release-8.rpm
warning: remi-release-8.rpm: Header V4 RSA/SHA256 Signature, key ID 5f11735a: NOKEY
error: Failed dependencies:
	epel-release = 8 is needed by remi-release-8.3-1.el8.remi.noarch
	redhat-release >= 8.3 is needed by remi-release-8.3-1.el8.remi.noarch
	system-release(releasever) = 8 is needed by remi-release-8.3-1.el8.remi.noarch




rpm -pql remi-release-7.rpm
rpm -ivh remi-release-7.rpm
```


```shell
yum install kernel-devel -y
```

kernel-devel-3.10.0-1160.15.2.el7.x86_64






```shell
yum install libodb-mysql-devel.x86_64
Downloading packages:
(1/3): libodb-mysql-2.3.0-1.el7.x86_64.rpm                                                                                                 |  66 kB  00:00:00     
(2/3): libodb-2.3.0-1.el7.x86_64.rpm                                                                                                       |  51 kB  00:00:00     
(3/3): libodb-mysql-devel-2.3.0-1.el7.x86_64.rpm                                                                                           |  46 kB  00:00:00     
------------------------------------------------------------------------------------------------------------------------------------------------------------------
Total                                                                                                                             412 kB/s | 163 kB  00:00:00     
Running transaction check
Running transaction test
Transaction test succeeded
Running transaction
Warning: RPMDB altered outside of yum.
  Installing : libodb-2.3.0-1.el7.x86_64                                                                                                                      1/3 
  Installing : libodb-mysql-2.3.0-1.el7.x86_64                                                                                                                2/3 
  Installing : libodb-mysql-devel-2.3.0-1.el7.x86_64
```

cenntos 7 镜像 rpms.remirepo.net

https://centos.pkgs.org/7/remi-x86_64/redis-5.0.11-1.el7.remi.x86_64.rpm.html
redis 5

windows 微软维护 3.0








从2010年3月15日起，Redis的开发工作由VMware主持。从2013年5月开始，Redis的开发由Pivotal赞助。
redis的作者，叫Salvatore Sanfilippo，来自意大利的西西里岛，居住在卡塔尼亚。目前供职于Pivotal公司。他使用的网名是antirez。



3.2.12
4.0.8

redis-3.2.12-2.el7.x86_64.rpm       A persistent key-value database
redis-trib-3.2.12-2.el7.noarch.rpm    Cluster management script for Redis


https://centos.pkgs.org/7/epel-x86_64/redis-3.2.12-2.el7.x86_64.rpm.html

/etc/redis-sentinel.conf
/etc/redis.conf



centos 7 安装redis yum
```shell
yum install redis -y
Loaded plugins: fastestmirror, langpacks
Repository epel is listed more than once in the configuration
Determining fastest mirrors
 * centos-sclo-rh: mirrors.aliyun.com
 * centos-sclo-sclo: mirrors.aliyun.com
centos-sclo-rh                                                                                                                             | 3.0 kB  00:00:00     
centos-sclo-sclo                                                                                                                           | 3.0 kB  00:00:00     
copr:copr.fedorainfracloud.org:carlwgeorge:ripgrep                                                                                         | 3.3 kB  00:00:00     
docker-ce-stable                                                                                                                           | 3.5 kB  00:00:00     
epel                                                                                                                                       | 4.7 kB  00:00:00     
extras                                                                                                                                     | 2.9 kB  00:00:00     
ius                                                                                                                                        | 1.3 kB  00:00:00     
kubernetes                                                                                                                                 | 2.9 kB  00:00:00     
mysql-connectors-community                                                                                                                 | 2.6 kB  00:00:00     
mysql-tools-community                                                                                                                      | 2.6 kB  00:00:00     
mysql57-community                                                                                                                          | 2.6 kB  00:00:00     
os                                                                                                                                         | 3.6 kB  00:00:00     
pgdg-common                                                                                                                                | 2.9 kB  00:00:00     
pgdg10                                                                                                                                     | 3.6 kB  00:00:00     
pgdg11                                                                                                                                     | 3.6 kB  00:00:00     
pgdg12                                                                                                                                     | 3.6 kB  00:00:00     
pgdg95                                                                                                                                     | 3.6 kB  00:00:00     
pgdg96                                                                                                                                     | 3.6 kB  00:00:00     
updates                                                                                                                                    | 2.9 kB  00:00:00     
wandisco-git                                                                                                                               | 2.9 kB  00:00:00     
(1/12): extras/7/x86_64/primary_db                                                                                                         | 225 kB  00:00:00     
(2/12): epel/7/x86_64/updateinfo                                                                                                           | 1.0 MB  00:00:00     
(3/12): epel/7/x86_64/primary_db                                                                                                           | 6.9 MB  00:00:00     
(4/12): docker-ce-stable/x86_64/primary_db                                                                                                 |  56 kB  00:00:01     
(5/12): ius/x86_64/primary                                                                                                                 | 104 kB  00:00:02     
(6/12): kubernetes/x86_64/primary_db                                                                                                       | 164 kB  00:00:03     
(7/12): pgdg-common/7/x86_64/primary_db                                                                                                    | 155 kB  00:00:03     
(8/12): updates/7/x86_64/primary_db                                                                                                        | 5.6 MB  00:00:00     
(9/12): pgdg11/7/x86_64/primary_db                                                                                                         | 318 kB  00:00:03     
(10/12): pgdg12/7/x86_64/primary_db                                                                                                        | 180 kB  00:00:03     
(11/12): pgdg96/7/x86_64/primary_db                                                                                                        | 298 kB  00:00:03     
(12/12): pgdg10/7/x86_64/primary_db                                                                                                        | 305 kB  00:00:07     
ius                                                                                                                                                       460/460
Resolving Dependencies
--> Running transaction check
---> Package redis.x86_64 0:3.2.12-2.el7 will be installed
--> Processing Dependency: libjemalloc.so.1()(64bit) for package: redis-3.2.12-2.el7.x86_64
--> Running transaction check
---> Package jemalloc.x86_64 0:3.6.0-1.el7 will be installed
--> Finished Dependency Resolution

Dependencies Resolved

==================================================================================================================================================================
 Package                                Arch                                 Version                                     Repository                          Size
==================================================================================================================================================================
Installing:
 redis                                  x86_64                               3.2.12-2.el7                                epel                               544 k
Installing for dependencies:
 jemalloc                               x86_64                               3.6.0-1.el7                                 epel                               105 k

Transaction Summary
==================================================================================================================================================================
Install  1 Package (+1 Dependent package)

Total download size: 648 k
Installed size: 1.7 M
Downloading packages:
(1/2): jemalloc-3.6.0-1.el7.x86_64.rpm                                                                                                     | 105 kB  00:00:00     
(2/2): redis-3.2.12-2.el7.x86_64.rpm                                                                                                       | 544 kB  00:00:00     
------------------------------------------------------------------------------------------------------------------------------------------------------------------
Total                                                                                                                             2.7 MB/s | 648 kB  00:00:00     
Running transaction check
Running transaction test
Transaction test succeeded
Running transaction
Warning: RPMDB altered outside of yum.
  Installing : jemalloc-3.6.0-1.el7.x86_64                                                                                                                    1/2 
  Installing : redis-3.2.12-2.el7.x86_64                                                                                                                      2/2 
  Verifying  : redis-3.2.12-2.el7.x86_64                                                                                                                      1/2 
  Verifying  : jemalloc-3.6.0-1.el7.x86_64                                                                                                                    2/2 

Installed:
  redis.x86_64 0:3.2.12-2.el7                                                                                                                                     

Dependency Installed:
  jemalloc.x86_64 0:3.6.0-1.el7                                                                                                                                   

Complete!
```


systemctl status redis



查看端口
netstat -lnp|grep 6379

26379 redis-sentinel

先执行命令 yum install net-tools 和 yum search ifconfig下载依赖插件


设置开机自启动
systemctl enable redis

systemctl start redis


journalctl -xe


journalctl - Query the systemd journal



```shell
journalctl -xe
Mar 01 16:30:01 iZ2ze9f7g12pq4tby7ewz2Z systemd[1]: Started Session 48461 of user root.
-- Subject: Unit session-48461.scope has finished start-up
-- Defined-By: systemd
-- Support: http://lists.freedesktop.org/mailman/listinfo/systemd-devel
-- 
-- Unit session-48461.scope has finished starting up.
-- 
-- The start-up result is done.
Mar 01 16:30:01 iZ2ze9f7g12pq4tby7ewz2Z CROND[8736]: (root) CMD (/usr/lib64/sa/sa1 1 1)
Mar 01 16:30:01 iZ2ze9f7g12pq4tby7ewz2Z systemd[1]: Starting Session 48461 of user root.
-- Subject: Unit session-48461.scope has begun start-up
-- Defined-By: systemd
-- Support: http://lists.freedesktop.org/mailman/listinfo/systemd-devel
-- 
-- Unit session-48461.scope has begun starting up.
Mar 01 16:35:30 iZ2ze9f7g12pq4tby7ewz2Z polkitd[460]: Registered Authentication Agent for unix-process:9427:2404043761 (system bus name :1.96973 [/usr/bin/pkttyag
Mar 01 16:35:30 iZ2ze9f7g12pq4tby7ewz2Z systemd[1]: Starting Redis persistent key-value database...
-- Subject: Unit redis.service has begun start-up
-- Defined-By: systemd
-- Support: http://lists.freedesktop.org/mailman/listinfo/systemd-devel
-- 
-- Unit redis.service has begun starting up.
Mar 01 16:35:30 iZ2ze9f7g12pq4tby7ewz2Z redis-server[9433]: *** FATAL CONFIG FILE ERROR ***
Mar 01 16:35:30 iZ2ze9f7g12pq4tby7ewz2Z redis-server[9433]: Reading the configuration file, at line 163
Mar 01 16:35:30 iZ2ze9f7g12pq4tby7ewz2Z redis-server[9433]: >>> 'logfile /var/log/redis/redis.log'
Mar 01 16:35:30 iZ2ze9f7g12pq4tby7ewz2Z redis-server[9433]: Can't open the log file: Permission denied
Mar 01 16:35:30 iZ2ze9f7g12pq4tby7ewz2Z systemd[1]: redis.service: main process exited, code=exited, status=1/FAILURE
Mar 01 16:35:30 iZ2ze9f7g12pq4tby7ewz2Z redis-shutdown[9434]: Could not connect to Redis at 127.0.0.1:6379: Connection refused
Mar 01 16:35:30 iZ2ze9f7g12pq4tby7ewz2Z systemd[1]: redis.service: control process exited, code=exited status=1
Mar 01 16:35:30 iZ2ze9f7g12pq4tby7ewz2Z systemd[1]: Failed to start Redis persistent key-value database.
-- Subject: Unit redis.service has failed
-- Defined-By: systemd
-- Support: http://lists.freedesktop.org/mailman/listinfo/systemd-devel
-- 
-- Unit redis.service has failed.
-- 
-- The result is failed.
Mar 01 16:35:30 iZ2ze9f7g12pq4tby7ewz2Z systemd[1]: Unit redis.service entered failed state.
Mar 01 16:35:30 iZ2ze9f7g12pq4tby7ewz2Z polkitd[460]: Unregistered Authentication Agent for unix-process:9427:2404043761 (system bus name :1.96973, object path /o
Mar 01 16:35:30 iZ2ze9f7g12pq4tby7ewz2Z systemd[1]: redis.service failed.
[root@iZ2ze9f7g12pq4tby7ewz2Z redis]# man journalctl
[root@iZ2ze9f7g12pq4tby7ewz2Z redis]# journalctl -xe
-- Subject: Unit session-48461.scope has finished start-up
-- Defined-By: systemd
-- Support: http://lists.freedesktop.org/mailman/listinfo/systemd-devel
-- 
-- Unit session-48461.scope has finished starting up.
-- 
-- The start-up result is done.
Mar 01 16:30:01 iZ2ze9f7g12pq4tby7ewz2Z CROND[8736]: (root) CMD (/usr/lib64/sa/sa1 1 1)
Mar 01 16:30:01 iZ2ze9f7g12pq4tby7ewz2Z systemd[1]: Starting Session 48461 of user root.
-- Subject: Unit session-48461.scope has begun start-up
-- Defined-By: systemd
-- Support: http://lists.freedesktop.org/mailman/listinfo/systemd-devel
-- 
-- Unit session-48461.scope has begun starting up.
Mar 01 16:35:30 iZ2ze9f7g12pq4tby7ewz2Z polkitd[460]: Registered Authentication Agent for unix-process:9427:2404043761 (system bus name :1.96973 [/usr/bin/pkttyag
Mar 01 16:35:30 iZ2ze9f7g12pq4tby7ewz2Z systemd[1]: Starting Redis persistent key-value database...
-- Subject: Unit redis.service has begun start-up
-- Defined-By: systemd
-- Support: http://lists.freedesktop.org/mailman/listinfo/systemd-devel
-- 
-- Unit redis.service has begun starting up.
Mar 01 16:35:30 iZ2ze9f7g12pq4tby7ewz2Z redis-server[9433]: *** FATAL CONFIG FILE ERROR ***
Mar 01 16:35:30 iZ2ze9f7g12pq4tby7ewz2Z redis-server[9433]: Reading the configuration file, at line 163
Mar 01 16:35:30 iZ2ze9f7g12pq4tby7ewz2Z redis-server[9433]: >>> 'logfile /var/log/redis/redis.log'
Mar 01 16:35:30 iZ2ze9f7g12pq4tby7ewz2Z redis-server[9433]: Can't open the log file: Permission denied
Mar 01 16:35:30 iZ2ze9f7g12pq4tby7ewz2Z systemd[1]: redis.service: main process exited, code=exited, status=1/FAILURE
Mar 01 16:35:30 iZ2ze9f7g12pq4tby7ewz2Z redis-shutdown[9434]: Could not connect to Redis at 127.0.0.1:6379: Connection refused
Mar 01 16:35:30 iZ2ze9f7g12pq4tby7ewz2Z systemd[1]: redis.service: control process exited, code=exited status=1
Mar 01 16:35:30 iZ2ze9f7g12pq4tby7ewz2Z systemd[1]: Failed to start Redis persistent key-value database.
-- Subject: Unit redis.service has failed
-- Defined-By: systemd
-- Support: http://lists.freedesktop.org/mailman/listinfo/systemd-devel
-- 
-- Unit redis.service has failed.
-- 
-- The result is failed.
Mar 01 16:35:30 iZ2ze9f7g12pq4tby7ewz2Z systemd[1]: Unit redis.service entered failed state.
Mar 01 16:35:30 iZ2ze9f7g12pq4tby7ewz2Z polkitd[460]: Unregistered Authentication Agent for unix-process:9427:2404043761 (system bus name :1.96973, object path /o
Mar 01 16:35:30 iZ2ze9f7g12pq4tby7ewz2Z systemd[1]: redis.service failed.
```


google search

windows redis ui client sentinel




图形客户端 windows
https://github.com/cinience/RedisStudio/releases  2015最新更新

2014
https://github.com/uglide/RedisDesktopManager/releases
https://www.cnblogs.com/zxtceq/p/7676862.html


redisinsight redislab提供的

https://docs.redislabs.com/latest/ri/installing/install-redis-desktop/

redisinsight-win.msi
http://localhost:8001/  ui是网页的

AnotherRedisDesktopManager 国人维护的
https://gitee.com/qishibo/AnotherRedisDesktopManager/releases
https://github.com/qishibo/AnotherRedisDesktopManager


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

因此业界常用的解决方案通常是借助于一个第三方组件并利用它自身的排他性来达到多进程的互斥。如：基于DB的唯一索引。基于ZK的临时有序节点。基于Redis的NX EX参数。

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

2021 Redis 7

git clone https://github.com/redis/redis.git
cd redis
git checkout 7.0
make -j4 2>&1 | tee out.txt

不支持doxygen，c项目，没有函数列表
makefile 组织的

新增单元测试
测试动态字符串 跳表


ansi c写的

https://github.com/redis/redis/issues/11630


https://github.com/antirez/redis/tree/6.0



一、对用户使用有直接影响的功能

1. ACL用户权限控制功能
2. RESP3：新的 Redis 通信协议
3. Cluster 管理工具
4. SSL 支持

二、Redis 内部的优化

1. IO多线程支持
2. 新的Module API
3. 新的 Expire 算法

三、外部工具

1. Redis Cluster Proxy
2. Disque



[Redis Day New York 上的分享在YouTube ](https://www.youtube.com/watch?v=lo-Pgf_l7_M)



问：如何熟悉Redis
先学会用，然后会用了自然想去了解细节



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


```





redis-stat is a simple Redis monitoring tool written in Ruby.

https://github.com/junegunn/redis-stat



zabbix也提供了相关的插件对redis服务进行监控



Redis几个重要的健康指标 zotero





MemAdmin

通过一些开源的第三方工具对整个memcached集群进行监控，显示会更直观
https://www.cnblogs.com/dinglang/p/6117309.html


redis 编译环境
redis 核心维护者沟通渠道

https://redis.io/community/


https://groups.google.com/g/redis-db/c/tFldUlOt8D8/m/HrZAfUB0AgAJ



https://blog.csdn.net/gig886/article/details/123231156


### 客户端
redisson.md



### java访问redis

		<dependency>
			<groupId>org.springframework.boot</groupId>
			<artifactId>spring-boot-starter-data-redis</artifactId>
		</dependency>