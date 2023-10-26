# redisson

## 测试代码
https://gitee.com/edidada/testredision

分布式Redis解决方案之Redisson
https://www.cnblogs.com/zys2019/p/16401233.html

分布式锁 看门狗，默认延时时长10s


### redisson vs jedis vs lettuce

Redisson、Jedis和Lettuce都是Java语言中常用的Redis客户端库，它们都提供了丰富的Redis操作功能。下面是它们的竞品分析：

1. Redisson

优点：
- 支持单机、主从、哨兵和集群模式；
- 提供了丰富的Redis API，包括String、List、Set、Map等数据结构的操作；
- 支持异步编程和分布式锁等功能；
- 社区活跃，更新迭代快。

缺点：
- 相对较重，对系统资源消耗较大；
- 配置较为复杂，需要手动配置连接池、序列化器等参数。

2. Jedis

优点：
- 简单易用，API设计清晰明了；
- 支持单机、主从模式；
- 提供了丰富的Redis API，包括String、List、Set、Map等数据结构的操作；
- 社区活跃，更新迭代快。

缺点：
- 不支持集群模式；
- 不支持异步编程和分布式锁等功能；
- 对系统资源消耗较大。

3. Lettuce

优点：
- 基于Netty框架实现，支持高并发场景下的快速响应；
- 支持单机、主从、哨兵和集群模式；
- 提供了丰富的Redis API，包括String、List、Set、Map等数据结构的操作；
- 支持异步编程和分布式锁等功能；
- 配置简单，自动适配各种序列化器。

缺点：
- API设计较为繁琐，使用起来不如Jedis直观；
- 社区相对较小，更新迭代较慢。

## 官网
https://redisson.org/

## 源代码
https://github.com/redisson/redisson
https://mavenlibs.com/maven/dependency/org.redisson/redisson

C:/Users/edidada/Downloads/redisson-3.23.3-javadoc/index.html


https://mavenlibs.com/maven/dependency/org.redisson/redisson-spring-boot-starter


```xml
<dependency>
    <groupId>org.redisson</groupId>
    <artifactId>redisson-spring-boot-starter</artifactId>
    <version>3.23.3</version>
</dependency>
```


https://mavenlibs.com/

## api doc

### org.redisson





Class

Description

ElementsSubscribeService

 

JndiRedissonFactory

Redisson object factory used to register instance in JNDI registry.

LongSlotCallback

 

MapWriteBehindTask

 

MapWriterTask

 

MapWriterTask.Add

 

MapWriterTask.Remove

 

PubSubEntry<E>

Nikita Koksharov

PubSubMessageListener<V>

 

PubSubPatternMessageListener<V>

 

PubSubPatternStatusListener

 

PubSubStatusListener

 

QueueTransferService

 

QueueTransferTask

 

QueueTransferTask.TimeoutTask

 

RedisClusterNodes

Deprecated.

RedisNodes<N extends Node>

Deprecated.

Redisson

Main infrastructure class allows to get access to all Redisson objects on top of Redis server.

RedissonAtomicDouble

Distributed alternative to the AtomicLong

RedissonAtomicLong

Distributed alternative to the AtomicLong

RedissonBaseAdder<T extends Number>

 

RedissonBaseLock

Base class for implementing distributed locks

RedissonBaseLock.ExpirationEntry

 

RedissonBatch

 

RedissonBinaryStream

 

RedissonBitSet

 

RedissonBlockingDeque<V>

Distributed and concurrent implementation of BlockingDeque.

RedissonBlockingQueue<V>

Distributed and concurrent implementation of BlockingQueue.

RedissonBloomFilter<T>

Bloom filter based on Highway 128-bit hash.

RedissonBoundedBlockingQueue<V>

Distributed and concurrent implementation of bounded BlockingQueue.

RedissonBucket<V>

 

RedissonBuckets

 

RedissonCountDownLatch

Distributed alternative to the CountDownLatch It has a advantage over CountDownLatch -- count can be reset via RedissonCountDownLatch.trySetCount(long).

RedissonCountDownLatchEntry

 

RedissonDelayedQueue<V>

 

RedissonDeque<V>

Distributed and concurrent implementation of Queue

RedissonDoubleAdder

 

RedissonExecutorService

 

RedissonExecutorService.ClassBody

 

RedissonFairLock

Distributed implementation of Lock Implements reentrant lock.

Lock will be removed automatically if client disconnects.

RedissonFencedLock

Redis based implementation of Fenced Lock with reentrancy support.

RedissonFuction

 

RedissonGeo<V>

Geospatial items holder

RedissonHyperLogLog<V>

 

RedissonIdGenerator

 

RedissonJsonBucket<V>

Json data holder

RedissonKeys

 

RedissonLexSortedSet

Sorted set contained values of String type

RedissonList<V>

Distributed and concurrent implementation of List

RedissonListMultimap<K,V>

 

RedissonListMultimapCache<K,V>

 

RedissonListMultimapIterator<K,V,M>

 

RedissonListMultimapValues<V>

List based Multimap Cache values holder

RedissonLiveObjectService

 

RedissonLocalCachedMap<K,V>

 

RedissonLock

Distributed implementation of Lock Implements reentrant lock.

Lock will be removed automatically if client disconnects.

RedissonLockEntry

 

RedissonLongAdder

 

RedissonMap<K,V>

Distributed and concurrent implementation of ConcurrentMap and Map

RedissonMapCache<K,V>

Map-based cache with ability to set TTL for each entry via RedissonMapCache.put(Object, Object, long, TimeUnit) or RedissonMapCache.putIfAbsent(Object, Object, long, TimeUnit) methods.

RedissonMapEntry<K,V>

 

RedissonMultiLock

Groups multiple independent locks and manages them as one lock.

RedissonMultimap<K,V>

 

RedissonMultimapCache<K>

 

RedissonNode

 

RedissonObject

Base Redisson object

RedissonPatternTopic

Distributed topic implementation.

RedissonPermitExpirableSemaphore

 

RedissonPriorityBlockingDeque<V>

Distributed and concurrent implementation of priority blocking deque.

RedissonPriorityBlockingQueue<V>

Distributed and concurrent implementation of PriorityBlockingQueue.

RedissonPriorityDeque<V>

Distributed and concurrent implementation of Queue

RedissonPriorityQueue<V>

 

RedissonPriorityQueue.BinarySearchResult<V>

 

RedissonQueue<V>

Distributed and concurrent implementation of Queue

RedissonQueueSemaphore

 

RedissonRateLimiter

 

RedissonReactive

Main infrastructure class allows to get access to all Redisson objects on top of Redis server.

RedissonReadLock

Lock will be removed automatically if client disconnects.

RedissonReadWriteLock

A ReadWriteLock maintains a pair of associated locks, one for read-only operations and one for writing.

RedissonRedLock

RedLock locking algorithm implementation for multiple locks.

RedissonReference

 

RedissonReference.ReferenceType

 

RedissonReliableTopic

 

RedissonRemoteService

 

RedissonRemoteService.Entry

 

RedissonRingBuffer<V>

 

RedissonRx

Main infrastructure class allows to get access to all Redisson objects on top of Redis server.

RedissonScoredSortedSet<V>

 

RedissonScript

 

RedissonSearch

 

RedissonSemaphore

Distributed and concurrent implementation of Semaphore.

RedissonSet<V>

Distributed and concurrent implementation of Set

RedissonSetCache<V>

Set-based cache with ability to set TTL for each entry via RSetCache.add(Object, long, TimeUnit) method.

RedissonSetMultimap<K,V>

 

RedissonSetMultimapCache<K,V>

 

RedissonSetMultimapIterator<K,V,M>

 

RedissonSetMultimapValues<V>

Set based Multimap Cache values holder

RedissonShardedTopic

Sharded Topic for Redis Cluster.

RedissonShutdownException

 

RedissonSortedSet<V>

 

RedissonSortedSet.BinarySearchResult<V>

 

RedissonSpinLock

Distributed implementation of Lock Implements reentrant lock.

Lock will be removed automatically if client disconnects.

RedissonStream<K,V>

 

RedissonSubList<V>

Distributed and concurrent implementation of List

RedissonTimeSeries<V,L>

 

RedissonTopic

Distributed topic implementation.

RedissonTransferQueue<V>

 

RedissonTransferQueue.TransferQueueService

 

RedissonTransferQueue.TransferQueueServiceAsync

 

RedissonTransferQueue.TransferQueueServiceImpl

 

RedissonWriteLock

Lock will be removed automatically if client disconnects.

ScanIterator

 

ScanResult<R>

 

SlotCallback<T,R>

 

Version

 

WriteBehindService

 



#### org.redisson.api

org.redisson.api.annotation

org.redisson.api.condition

org.redisson.api.executor

org.redisson.api.geo

org.redisson.api.listener

org.redisson.api.map

org.redisson.api.map.event

org.redisson.api.mapreduce

org.redisson.api.queue

org.redisson.api.redisnode

org.redisson.api.search

org.redisson.api.search.aggregate

org.redisson.api.search.index

org.redisson.api.search.query

org.redisson.api.stream

#### org.redisson.cache

#### org.redisson.client

org.redisson.client.codec

org.redisson.client.handler

org.redisson.client.protocol

org.redisson.client.protocol.convertor

org.redisson.client.protocol.decoder

org.redisson.client.protocol.pubsub

#### org.redisson.cluster

#### org.redisson.codec

#### org.redisson.command

#### org.redisson.config

#### org.redisson.connection

org.redisson.connection.balancer

org.redisson.connection.decoder

org.redisson.connection.pool

#### org.redisson.eviction

#### org.redisson.executor

org.redisson.executor.params

#### org.redisson.iterator

#### org.redisson.jcache

org.redisson.jcache.bean

org.redisson.jcache.configuration

#### org.redisson.liveobject

org.redisson.liveobject.condition

org.redisson.liveobject.core

org.redisson.liveobject.misc

org.redisson.liveobject.resolver

#### org.redisson.mapreduce

#### org.redisson.misc

#### org.redisson.pubsub

#### org.redisson.reactive

#### org.redisson.redisnode

#### org.redisson.remote

#### org.redisson.rx

#### org.redisson.spring
org.redisson.spring.cache

org.redisson.spring.misc

org.redisson.spring.session

org.redisson.spring.session.config

org.redisson.spring.support

org.redisson.spring.transaction

#### org.redisson.transaction

org.redisson.transaction.operation

org.redisson.transaction.operation.bucket

org.redisson.transaction.operation.map

org.redisson.transaction.operation.set
