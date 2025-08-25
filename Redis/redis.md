# redis

Redis 5.0 及之后的版本（如 Redis 6.0）中，其核心 5 种数据类型（String, List, Hash, Set, Sorted Set）在底层使用了多种 高效的数据结构 来实现。这些内部数据结构的选择基于 空间效率、时间复杂度和使用场景 的权衡。

我们将基于 Redis 6.0 的源码（[https://github.com/redis/redis](https://github.com/redis/redis)）来深入解析每种数据类型的内部编码（encoding）和对应的数据结构。

##  Redis 5 大数据类型与内部编码总览

| Redis 数据类型 | 内部编码 (encoding) | 对应的数据结构 | 触发条件（何时使用） |
|----------------|---------------------|----------------|------------------------|
| String     | `OBJ_ENCODING_INT`  | `long` 类型整数 | 值是整数且可 fit 到 long |
|                | `OBJ_ENCODING_EMBSTR` | `sdshdr8/sdshdr16` + 字符串 | 小字符串（≤ 44 字节） |
|                | `OBJ_ENCODING_RAW`  | `sds`（动态字符串） | 大字符串 |
| List       | `OBJ_ENCODING_ZIPLIST` (Redis 3.2-) | `ziplist` | 元素少且小（旧版本） |
|                | `OBJ_ENCODING_QUICKLIST` | `quicklist` | Redis 3.2+ 默认（所有 List） |
| Hash       | `OBJ_ENCODING_ZIPLIST` | `ziplist` | 字段少且值小 |
|                | `OBJ_ENCODING_HT`   | `dict`（哈希表） | 字段多或值大 |
| Set        | `OBJ_ENCODING_INTSET` | `intset` | 元素全是整数且少 |
|                | `OBJ_ENCODING_HT`   | `dict` | 元素为字符串或数量多 |
| Sorted Set | `OBJ_ENCODING_ZIPLIST` | `ziplist` | 元素少且小 |
|                | `OBJ_ENCODING_SKIPLIST` | `zset`（`dict` + `skiplist`） | 元素多或大 |

>  注意：从 Redis 3.2 开始，`list` 的底层已从 `ziplist` 和 `linkedlist` 迁移到 `quicklist`，它本质上是 ziplist 的双向链表，兼顾了内存和性能。

##  一、String 类型

### 1. `OBJ_ENCODING_INT`
- 结构：直接将整数存储在 `redisObject` 的 `ptr` 指针中。
- 源码位置：`object.c` 中 `createStringObject()`。
- 优点：零内存碎片，最快访问。
- 条件：`value` 是整数且 `lval` 可 fit 到 `long`。

```c
// redisObject.h
typedef struct redisObject {
    unsigned type:4;
    unsigned encoding:4;
    void *ptr; // 当 encoding=INT 时，ptr = (void*)value
    // ...
} robj;
```

### 2. `OBJ_ENCODING_EMBSTR` 和 `OBJ_ENCODING_RAW`
- 底层结构：`sds`（Simple Dynamic String）。
- 源码文件：`sds.h`, `sds.c`

#### SDS 结构（以 `sdshdr8` 为例）：
```c
// sds.h
struct __attribute__ ((__packed__)) sdshdr8 {
    uint8_t len;      // 当前字符串长度
    uint8_t alloc;    // 分配的总空间（不包括 header）
    unsigned char flags; // 编码类型（低 3 位）
    char buf[];       // 变长数组，存储字符串
};
```

- `embstr`：使用 一次 `malloc` 分配 `redisObject` + `sdshdr` + 字符串空间，适合小字符串（≤ 44 字节），减少内存碎片。
- `raw`：`redisObject` 和 `sds` 分开 `malloc`，适合大字符串。


##  二、List 类型（Redis 6.0 使用 `quicklist`）

### `OBJ_ENCODING_QUICKLIST`
- 结构：`quicklist` 是 ziplist 的双向链表。
- 源码文件：`quicklist.h`, `quicklist.c`

#### 核心结构：
```c
// quicklist.h
typedef struct quicklist {
    quicklistNode *head;
    quicklistNode *tail;
    unsigned long count;        // 所有节点中元素总数
    int nodes;                  // ziplist 节点数量
    int compress;               // LZF 压缩深度
    // ...
} quicklist;

typedef struct quicklistNode {
    struct quicklistNode *prev;
    struct quicklistNode *next;
    unsigned char *zl;          // 指向 ziplist
    unsigned int sz;            // ziplist 占用字节数
    unsigned int count : 16;    // 该节点中元素个数
    unsigned int encoding : 2;  // RAW=1 or LZF=2
    unsigned int container : 2; // NONE=1 or ZIPLIST=2
    unsigned int recompress : 1;// 是否被解压过
    // ...
} quicklistNode;
```

#### 为什么用 `quicklist`？
- `ziplist` 插入/删除慢（O(N)），且不能太大（否则 `realloc` 成本高）。
- `quicklist` 将大 list 拆成多个小 `ziplist`，每个 `ziplist` 大小可控（通过 `list-max-ziplist-size` 配置）。
- 支持 LZF 压缩（`compress` 字段），节省内存。

>  Redis 3.2+ 所有 List 都用 `quicklist`，`ziplist` 和 `linkedlist` 已废弃。


##  三、Hash 类型

### 1. `OBJ_ENCODING_ZIPLIST`
- 结构：压缩列表，连续内存存储 `field1, value1, field2, value2, ...`。
- 优点：内存紧凑。
- 缺点：查 `field` 需遍历，O(N)。
- 触发条件（默认）：
  - 元素个数 < `hash-max-ziplist-entries`（默认 512）
  - 所有 `value` 长度 < `hash-max-ziplist-value`（默认 64 字节）

### 2. `OBJ_ENCODING_HT`
- 结构：`dict`（哈希表），即 `hashtable`。
- 源码文件：`dict.h`, `dict.c`

#### `dict` 结构：
```c
// dict.h
typedef struct dict {
    dictType *type;
    dictht ht[2];               // 两个哈希表，用于渐进式 rehash
    long rehashidx;             // rehash 状态
    // ...
} dict;

typedef struct dictht {
    dictEntry table;          // 桶数组
    unsigned long size;         // 数组大小
    unsigned long used;         // 已用桶数
    // ...
} dictht;

typedef struct dictEntry {
    void *key;
    union {
        void *val;
        uint64_t u64;
        int64_t s64;
        double d;
    } v;
    struct dictEntry *next;     // 链地址法解决冲突
} dictEntry;
```

- 优点：查找 O(1)。
- 缺点：内存开销大（指针、桶）。
- 触发条件：超过 ziplist 限制时自动转为 `HT`。


##  四、Set 类型

### 1. `OBJ_ENCODING_INTSET`
- 结构：整数集合，有序数组。
- 源码文件：`intset.h`, `intset.c`

#### 结构：
```c
// intset.h
typedef struct intset {
    uint32_t encoding;          // INTSET_ENC_INT16, _32, _64
    uint32_t length;            // 元素个数
    int8_t contents[];          // 变长数组，存储整数（紧凑）
} intset;
```

- 优点：内存极省，查找用二分 O(log N)。
- 触发条件：
  - 所有元素是整数。
  - 元素个数 < `set-max-intset-entries`（默认 512）。

### 2. `OBJ_ENCODING_HT`
- 结构：`dict`，`key=member`, `val=NULL`。
- 触发条件：有非整数元素或元素太多。

##  五、Sorted Set（ZSet）类型

### 1. `OBJ_ENCODING_ZIPLIST`
- 结构：`member1, score1, member2, score2, ...`，按 score 排序。
- 触发条件：
  - 元素个数 < `zset-max-ziplist-entries`（默认 128）
  - 所有 `member` 长度 < `zset-max-ziplist-value`（默认 64 字节）

### 2. `OBJ_ENCODING_SKIPLIST`
- 结构：双结构体 —— `zset`，包含：
  - `dict`：`member → score` 映射，用于 O(1) 查 score。
  - `skiplist`：按 score 排序的跳表，用于范围查询。
- 源码文件：`server.h`, `t_zset.c`

#### `zset` 结构：
```c
// server.h
typedef struct zset {
    dict *dict;                 // member -> double score
    zskiplist *zsl;             // score -> member (ordered)
} zset;
```

#### 跳表节点：
```c
// server.h
typedef struct zskiplistNode {
    sds ele;                    // member
    double score;               // score
    struct zskiplistNode *backward; // 后向指针
    struct zskiplistLevel {
        struct zskiplistNode *forward;
        unsigned int span;      // 到下一个节点的跨度
    } level[];
} zskiplistNode;
```

>  为什么用跳表而不是红黑树？
> - 跳表实现简单，支持高效的范围查询（`ZRANGE`）。
> - Redis 更看重实现简洁和范围操作，跳表足够好。


##  总结表（Redis 6.0）

| 类型 | 编码 | 数据结构 | 优点 | 缺点 | 典型场景 |
|------|------|----------|------|------|----------|
| String | `INT` | `long` | 零开销 | 仅整数 | 计数器 |
| | `EMBSTR` | `sds` (小) | 内存紧凑 | ≤44字节 | 小字符串 |
| | `RAW` | `sds` (大) | 动态扩容 | 有指针开销 | 大文本 |
| List | `QUICKLIST` | `quicklist` (ziplist 链表) | 内存+性能平衡 | - | 所有 List |
| Hash | `ZIPLIST` | 压缩列表 | 内存省 | O(N) 查找 | 小对象 |
| | `HT` | `dict` | O(1) 查找 | 内存大 | 大对象 |
| Set | `INTSET` | 整数数组 | 内存极省 | 仅整数 | 标签、ID 集合 |
| | `HT` | `dict` | 通用 | 内存大 | 字符串集合 |
| Sorted Set | `ZIPLIST` | 压缩列表 | 内存省 | O(N) | 小有序集 |
| | `SKIPLIST` | `dict` + `skiplist` | O(1) 查, O(log N) 范围 | 内存大 | 排行榜、优先队列 |

##  关键设计思想

1. 空间换时间：小对象用紧凑结构（ziplist, intset），大对象用高效结构（dict, skiplist）。
2. 渐进式转换：当数据增长超过阈值时，自动从 ziplist → dict/quicklist。
3. 避免外部依赖：所有数据结构均为 Redis 自研，控制力强。
4. 内存友好：`embstr`, `quicklist`, `intset` 都是为了减少内存碎片和开销。

如果你想看某个数据结构的 具体源码实现（如 `ziplistPush`, `dictAdd`, `zslInsert`），我可以继续深入分析。

在 Redis 6.0 的源代码中，`OBJ_ENCODING_INT` 这个常量的定义以及它被使用的逻辑主要分布在以下几个关键文件中：

### 1. `server.h` - 常量定义

这是 `OBJ_ENCODING_INT` 的定义所在文件。

```c
// src/server.h
#define OBJ_ENCODING_RAW 0     /* Raw representation */
#define OBJ_ENCODING_INT 1     /* Encoded as integer */
#define OBJ_ENCODING_HT 2      /* Encoded as hash table */
#define OBJ_ENCODING_ZIPMAP 3  /* No longer used: old hash encoding. */
#define OBJ_ENCODING_LINKEDLIST 4 /* No longer used: old list encoding. */
#define OBJ_ENCODING_ZIPLIST 5 /* No longer used: old list/hash/zset encoding. */
#define OBJ_ENCODING_INTSET 6  /* Encoded as intset */
#define OBJ_ENCODING_SKIPLIST 7/* Encoded as skiplist */
#define OBJ_ENCODING_EMBSTR 8  /* Embedded string encoding */
#define OBJ_ENCODING_QUICKLIST 9/* Encoded as linked list of ziplists */
#define OBJ_ENCODING_STREAM 10 /* Encoded as a radix tree of listpacks */
```

>  文件：`src/server.h`
>
>  作用：定义了所有 `redisObject` 可能的 `encoding` 值，`OBJ_ENCODING_INT` 被定义为 `1`。

### 2. `object.c` - 创建和管理字符串对象（核心逻辑）

这是 `OBJ_ENCODING_INT` 被创建和使用的最主要文件。当你设置一个整数字符串时，Redis 会尝试将其编码为 `INT`。

#### 关键函数：`createStringObject()`

```c
// src/object.c
robj *createStringObject(const char *ptr, size_t len) {
    if (len <= OBJ_ENCODING_EMBSTR_SIZE_LIMIT) {
        return createEmbeddedStringObject(ptr,len);
    } else {
        return createRawStringObject(ptr,len);
    }
}
```

这个函数会根据字符串长度决定是用 `embstr` 还是 `raw`。但真正判断是否用 `INT` 编码的逻辑在 `tryObjectEncoding()` 中。

#### 核心函数：`tryObjectEncoding()` - 尝试优化编码

```c
// src/object.c
robj *tryObjectEncoding(robj *o) {
    long value;
    sds s = o->ptr;
    size_t len;

    // 只有字符串对象才可能被编码为 INT
    if (o->type != OBJ_STRING) return o;

    // 检查是否可以转换为 long 整数
    if (sdsEncodedObject(o)) {
        len = sdslen(s);
        if (len <= 21 && string2l(s,len,&value)) {
            // 释放原来的 SDS
            if (o->refcount > 1) return o;
            o->encoding = OBJ_ENCODING_INT;
            o->ptr = (void*) value;  // 直接将整数存入 ptr 指针
            return o;
        }
    }

    // ... 其他编码尝试（如 EMBSTR）
    return o;
}
```

>  文件：`src/object.c`
>
>  作用：
> - `tryObjectEncoding()` 是决定是否将字符串对象转为 `OBJ_ENCODING_INT` 的核心函数。
> - 它调用 `string2l()` 尝试将字符串解析为 `long`。
> - 如果成功且长度 ≤ 21 字符，就将 `redisObject` 的 `encoding` 设为 `OBJ_ENCODING_INT`，并把整数值直接存入 `ptr` 指针（利用指针的高位存储数据）。


### 3. `t_string.c` - SET 命令的实现

当你执行 `SET mykey 123` 时，最终会调用这个文件中的函数，它会触发 `tryObjectEncoding()`。

```c
// src/t_string.c
void setGenericCommand(client *c, int flags, robj *key, robj *val, robj *expire, int unit, robj *ok_reply, robj *abort_reply) {
    // ... 逻辑
    val = getDecodedObject(val); // 解码
    // 尝试优化编码（可能转为 INT）
    if (o) o = tryObjectEncoding(o);
    // ... 存入数据库
}
```

>  文件：`src/t_string.c`
>
>  作用：`SET` 命令的处理逻辑中会调用 `tryObjectEncoding()`，这是 `OBJ_ENCODING_INT` 被触发的常见入口。

### 4. `object.c` - 获取对象值时的处理

当从 `OBJ_ENCODING_INT` 对象中读取值时，需要特殊处理：

```c
// src/object.c
char *get原创内容，此处为示意
// 实际上在命令实现中，会检查 encoding 并从 ptr 读取整数
```

虽然没有一个单独的 `getIntValueFromObject` 函数，但在很多命令（如 `INCR`, `GET`）中，都会先检查 `encoding == OBJ_ENCODING_INT`，然后直接 `(long)o->ptr` 获取值。


###  总结

| 作用 | 文件 | 说明 |
|------|------|------|
| 定义 `OBJ_ENCODING_INT` | `src/server.h` | 宏定义，值为 `1` |
| 创建/转换为 `INT` 编码 | `src/object.c` | `tryObjectEncoding()` 函数是核心 |
| `SET` 命令触发 | `src/t_string.c` | 调用 `tryObjectEncoding()` |
| 对象创建辅助 | `src/object.c` | `createStringObject()` 等 |

所以，如果你想看 `OBJ_ENCODING_INT` 是如何被应用的，重点看：

 `src/object.c` 中的 `tryObjectEncoding()` 函数

这是 Redis 实现“小整数字符串自动转为整数存储”这一优化的关键逻辑。

## 自己写redis
Rust
https://github.com/tokio-rs/mini-redis

Go
https://github.com/alicebob/miniredis

Redis选择用C语言而不是C++语言编写，背后有几个关键的原因，这些原因涉及到性能、语言的特性、开发效率以及社区支持等方面。以下是一些主要的考虑因素：

性能优化：
C语言非常接近硬件，能够提供更低的系统开销和更高的执行效率。Redis作为一个高性能的键值存储系统，对性能有极高的要求。C语言允许开发者直接操作内存，减少中间层的开销，如自动内存管理（垃圾回收）等。
C++虽然也提供了高性能编程的能力，但其标准库（如STL）和某些特性（如模板元编程）可能会引入额外的运行时开销，这可能会影响Redis的性能。
内存管理：
Redis需要精细地控制内存使用，以最大化存储效率和响应速度。C语言允许开发者直接管理内存（例如，使用malloc和free），这在Redis中是非常关键的。
C++虽然提供了智能指针等自动内存管理工具，但这些工具可能会引入额外的性能开销，并且可能不如直接内存管理那样灵活和高效。
简洁性和可维护性：
Redis的代码库相对较小且专注于其核心功能。C语言的简洁性有助于保持代码的清晰和可维护性。
C++虽然提供了更多的抽象和面向对象编程的能力，但这些特性在Redis的应用场景中可能并不总是必要的，而且可能会增加代码的复杂性。
开发效率和兼容性：
C语言是一种广泛使用的编程语言，有着庞大的开发者社区和丰富的文档资源。使用C语言可以更容易地吸引和留住开发者。
Redis的目标是跨平台兼容，C语言在这方面具有天然的优势，因为它被设计成一种可移植的语言。
历史原因和社区决策：
Redis的原始开发者可能基于上述原因（或其他个人偏好）选择了C语言。随着项目的发展和社区的壮大，这种选择也得到了广泛的认可和支持。
总的来说，Redis选择用C语言编写是出于性能、内存管理、简洁性、开发效率和兼容性等多方面的考虑。这些决策使得Redis能够成为一个高效、可靠且易于维护的键值存储系统。

## c语言 redis客户端
好的,我来为您介绍一下C语言中常用的Redis客户端库。

在C语言中,有几个比较流行的Redis客户端库,包括:
1. hiredis
   - 这是Redis官方推荐的C语言客户端库。
   - 支持同步和异步两种操作模式。
   - 提供了简单易用的API,可以方便地执行Redis命令。
   - 项目地址: https://github.com/redis/hiredis
2. credis
   - 这是另一个流行的C语言Redis客户端库。
   - 提供了与hiredis类似的API,但增加了一些额外的功能,如连接池管理等。
   - 项目地址: https://github.com/chusiang/credis
3. predis
   - 这是一个基于phpredis的C语言Redis客户端库。
   - 支持同步和异步两种操作模式。
   - 提供了丰富的Redis命令支持。
   - 项目地址: https://github.com/nrk/predis
4. libredis
   - 这是一个轻量级的C语言Redis客户端库。
   - 提供了基本的Redis命令执行功能。
   - 项目地址: https://github.com/gerasimou/libredis

以上是 C 语言中常用的几个 Redis 客户端库,它们各有自己的特点和优势。您可以根据项目需求和使用习惯,选择合适的库进行开发。

从社招面试来看，很多小伙伴分不清redis的内存淘汰机制和过期键值清理机制，不管问什么，开口就是LRU。
记英文不舒服么，eviction和expiration

redis map filed是否可以设置过期时间
list是单向链表还是双向链表

什么是Redis Module？有什么用？
Redis从4.0 版本开始，支持通过Module 来扩展其功能以满足特殊的需求。这些Module 以动态链接库（so 文件）的形式被加载到Redis中，这是一种非常灵活的动态扩展功能的实现方式，值得借鉴学习！
我们每个人都可以基于Redis去定制化开发自己的Module，比如实现搜索引擎功能、自定义分布式锁和分布式限流。
目前，被Redis官方推荐的Module有：
* RediSearchopen in new window：用于实现搜索引擎的模块。
* RedisJSONopen in new window：用于处理 JSON 数据的模块。
* RedisGraphopen in new window：用于实现图形数据库的模块。
* RedisTimeSeriesopen in new window：用于处理时间序列数据的模块。
* RedisBloomopen in new window：用于实现布隆过滤器的模块。
* RedisAIopen in new window：用于执行深度学习/机器学习模型并管理其数据的模块。
* RedisCellopen in new window：用于实现分布式限流的模块。

关于Redis模块的详细介绍，可以查看官方文档：https://redis.io/modulesopen in new window。

redis使用场景
共同关注

自增 分布式id
计数

消息队列 看门狗 延迟队列

Redis HyperLogLog是一种用于统计基数（cardinality）的数据结构，主要用于解决大数据集合中基数的估算问题。它的主要使用场景包括：
1. 实时访问统计：例如网站实时访问量、页面浏览量等，可以使用HyperLogLog来存储每个IP地址的访问次数，从而快速估算出总访问量。
2. 用户画像分析：在用户画像分析中，需要对用户的兴趣标签进行统计。由于用户可能拥有多个兴趣标签，因此可以使用HyperLogLog来统计每个用户的兴趣标签数量。
3. 推荐系统：在推荐系统中，需要对用户的历史行为进行统计，以便为用户推荐相似的内容。可以使用HyperLogLog来统计每个用户的行为次数，从而快速估算出用户的偏好。
4. 广告投放：在广告投放中，需要对广告的曝光量进行统计。可以使用HyperLogLog来存储每个广告的曝光次数，从而快速估算出广告的总曝光量。
5. 社交网络：在社交网络中，需要对用户的好友关系进行统计。可以使用HyperLogLog来统计每个用户的好友数量，从而快速估算出社交网络的规模。

在Redis Lettuce中，可以通过以下方式设置Sentinel的IP地址：
1. 首先，创建一个`RedisURIBuilder`对象，并设置Sentinel的IP地址。例如：

```java
import io.lettuce.core.RedisURI;
import io.lettuce.core.sentinel.api.RedisSentinelClient;
import io.lettuce.core.sentinel.api.SentinelEndpoint;
import io.lettuce.core.sentinel.api.builder.SentinelClientConfigurationBuilder;

public class RedisLettuceSentinelExample {
    public static void main(String[] args) {
        // 设置Sentinel的IP地址
        List<String> sentinelAddresses = Arrays.asList("127.0.0.1:26379", "127.0.0.1:26380", "127.0.0.1:26381");

        // 创建RedisURIBuilder对象
        RedisURIBuilder redisURIBuilder = RedisURI.SENTINEL_URI.builder()
                .withSentinelAddresses(sentinelAddresses);

        // 构建RedisURI对象
        RedisURI redisURI = redisURIBuilder.build();

        // 创建Sentinel客户端配置构建器
        SentinelClientConfigurationBuilder builder = SentinelClientConfiguration.builder()
                .masterName("mymaster")
                .sentinelAddresses(sentinelAddresses);

        // 创建RedisSentinelClient对象
        RedisSentinelClient sentinelClient = RedisSentinelClient.create(builder.build(), redisURI);

        // 使用RedisSentinelClient对象进行操作...
    }
}
```

在这个例子中，我们设置了三个Sentinel节点的IP地址（127.0.0.1:26379、127.0.0.1:26380和127.0.0.1:26381）。然后，我们创建了一个`RedisURIBuilder`对象，并使用`withSentinelAddresses()`方法设置了Sentinel的IP地址。接下来，我们构建了一个`RedisURI`对象，用于连接到Redis集群。最后，我们创建了一个`SentinelClientConfigurationBuilder`对象，并设置了主节点名称和Sentinel节点的IP地址。最后，我们使用这些配置创建了一个`RedisSentinelClient`对象，可以用于与Redis集群进行通信。

尽量不做分片集群。因为集群维护起来比较麻烦，并且集群之间的心跳检测和数据通信会消耗大量的网络带宽，也没有办法使用lua脚本和事务

bgsave
bgrewriteaof

## b站黑马程序员
Redis的数据持久化策略有哪些
什么是缓存穿透，怎么解决
什么是布隆过滤器
什么是缓存击穿，怎么解决
什么是缓存雪崩，怎么解决
redis双写问题
Redis分布式锁如何实现
Redis实现分布式锁如何合理的控制锁的有效时长
Redis的数据过期策略有哪些
Redis的数据淘汰策略有哪些

Redis的数据持久化策略有哪些
什么是缓存穿透，怎么解决
什么是布隆过滤器
什么是缓存击穿，怎么解决
什么是缓存雪崩，怎么解决
redis双写问题
Redis分布式锁如何实现
Redis实现分布式锁如何合理的控制锁的有效时长
Redis的数据过期策略有哪些
Redis的数据淘汰策略有哪些

缓存穿透：查询一个不存在的数据，mysql查询不到数据也不会直接写入缓存，就会导致每次请求都查数据库
解决方案一：缓存空数据，查询返回的数据为空，仍把这个空结果进行缓存
优点：简单
缺点：消耗内存，可能会发生不一致的问题

解决方案二：布隆过滤器
优点：内存占用较少，没有多余key
缺点：实现复杂，存在误判
bitmap（位图）：相当于是一个以（bit）位为单位的数组，数组中每个单元只能存储二进制数0或1
布隆过滤器作用：布隆过滤器可以用于检索一个元素是否在一个集合中。

https://zhuanlan.zhihu.com/p/662883241

## redis高级数据结构
hyperloglog

## redis底层数据结构
redis设计与实现 书籍

动态字符串 sds
链表 list listNode
字典 符号表 map dictht dictEntry
跳表 skipList
整数集合
压缩列表
对象

ziplist

## redis分布式锁
Redisson是一个在Java中实现的Redis客户端，它提供了很多高级功能，包括分布式锁，信号量，队列等等。

在Redis中，可以使用字节流（byte stream）来存储图片。以下是一个使用Java API存储图片的示例代码：
```java
// 创建Redis客户端  
Jedis jedis = new Jedis("localhost", 6379);  

// 读取图片文件  
File file = new File("path/to/image.jpg");  
byte[] imageData = Files.readAllBytes(file.toPath());  

// 将图片数据存储到Redis中  
jedis.set("image:1", imageData);  

// 关闭Redis客户端  
jedis.close();
```
在这个示例中，我们首先创建了一个Jedis客户端，指定了Redis服务器的地址和端口号。然后，我们使用Java的文件读取API将图片文件读取到字节数组中。最后，我们使用Jedis客户端的set命令将图片数据存储到Redis中，其中"image:1"是键，imageData是值。

需要注意的是，在存储图片数据时，应该使用字节流（byte stream）而不是字符串（string）。如果使用字符串来存储二进制数据，可能会导致数据损坏或编码问题。

## Redis之各版本特性
redis 7.2 上线了向量检索

### 1.Redis2.6

Redis2.6在2012年正是发布，经历了17个版本，到2.6.17版本，相对于Redis2.4，主要特性如下：
1）服务端支持Lua脚本。
2）去掉虚拟内存相关功能。
3）放开对客户端连接数的硬编码限制。
4）键的过期时间支持毫秒。
5）从节点支持只读功能。
6）两个新的位图命令：bitcount和bitop。
7）增强了redis-benchmark的功能：支持定制化的压测，CSV输出等功能。
8）基于浮点数自增命令：incrbyfloat和hincrbyfloat。
9）redis-cli可以使用--eval参数实现Lua脚本执行。
10）shutdown命令增强。
11）重构了大量的核心代码，所有集群相关的代码都去掉了，cluster功能将会是3.0版本最大的亮点。
12）info可以按照section输出，并且添加了一些统计项
13）sort命令优化

### 2.Redis2.8

Redis2.8在2013年11月22日正式发布，经历了24个版本，到2.8.24版本，相比于Redis2.6，主要特性如下：
1）添加部分主从复制的功能，在一定程度上降低了由于网络问题，造成频繁全量复制生成RDB对系统造成的压力。
2）尝试性的支持IPv6.
3）可以通过config set命令设置maxclients。
4）可以用bind命令绑定多个IP地址。
5）Redis设置了明显的进程名，方便使用ps命令查看系统进程。
6）config rewrite命令可以将config set持久化到Redis配置文件中。
7）发布订阅添加了pubsub。
8）Redis Sentinel第二版，相比于Redis2.6的Redis Sentinel，此版本已经变成生产可用。

### 3.Redis3.0（里程碑）

Redis3.0在2015年4月1日正式发布，相比于Redis2.8主要特性如下：
Redis最大的改动就是添加Redis的分布式实现Redis Cluster。

1）Redis Cluster：Redis的官方分布式实现。
2）全新的embedded string对象编码结果，优化小对象内存访问，在特定的工作负载下载速度大幅提升。
3）Iru算法大幅提升。
4）migrate连接缓存，大幅提升键迁移的速度。
5）migrate命令两个新的参数copy和replace。
6）新的client pause命令，在指定时间内停止处理客户端请求。
7）bitcount命令性能提升。
8）cinfig set设置maxmemory时候可以设置不同的单位（之前只能是字节）。
9）Redis日志小做调整：日志中会反应当前实例的角色（master或者slave）。
10）incr命令性能提升。

### 4.Redis3.2

Redis3.2在2016年5月6日正式发布，相比于Redis3.0主要特征如下：

1）添加GEO相关功能。
2）SDS在速度和节省空间上都做了优化。
3）支持用upstart或者systemd管理Redis进程。
4）新的List编码类型：quicklist。
5）从节点读取过期数据保证一致性。
6）添加了hstrlen命令。
7）增强了debug命令，支持了更多的参数。
8）Lua脚本功能增强。
9）添加了Lua Debugger。
10）config set 支持更多的配置参数。
11）优化了Redis崩溃后的相关报告。
12）新的RDB格式，但是仍然兼容旧的RDB。
13）加速RDB的加载速度。
14）spop命令支持个数参数。
15）cluster nodes命令得到加速。
16）Jemalloc更新到4.0.3版本。

### 5.Redis4.0

可能出乎很多的意料，Redis3.2之后的版本是4.0，而不是3.4、3.6、3.8。
一般这种重大版本号的升级也意味着软件或者工具本身发生了重大改革。下面是Redis4.0的新特性：

1）提供了模块系统，方便第三方开发者拓展Redis的功能。
2）PSYNC2.0：优化了之前版本中，主从节点切换必然引起全量复制的问题。
3）提供了新的缓存剔除算法：LFU（Last Frequently Used），并对已有算法进行了优化。
4）提供了非阻塞del和flushall/flushdb功能，有效解决删除了bigkey可能造成的Redis阻塞。
5）提供了memory命令，实现对内存更为全面的监控统计。
6）提供了交互数据库功能，实现Redis内部数据库的数据置换。
7）提供了RDB-AOF混合持久化格式，充分利用了AOF和RDB各自优势。
8）Redis Cluster 兼容NAT和Docker。

### 6.Redis5.0
1.新的Stream数据类型。[1]5.0
2.新的Redis模块API：Timers and Cluster API。
3. RDB现在存储LFU和LRU信息。
4.集群管理器从Ruby（redis-trib.rb）移植到C代码。可以在redis-cli中。查看`redis-cli —cluster help`了解更多信息。
5.新sorted set命令：ZPOPMIN / MAX和阻塞变量。
6.主动碎片整理V2。
7.增强HyperLogLog实现。
8.更好的内存统计报告。
9.许多带有子命令的命令现在都有一个HELP子命令。
10.客户经常连接和断开连接时性能更好。
11.错误修复和改进。
12. Jemalloc升级到5.1版

浅析Redis 4.0新特性之LazyFree
Redis 4.0引入了一个新的特性：lazy free，这个特性主要解决了一个问题，那就是在删除大型数据元素（Big Key）时可能带来的性能和可用性问题。
首先，我们需要理解一下什么是lazy free。在Redis中，当你删除一个键值对时，通常会立即释放该键占用的内存。然而，对于大型键值对，这可能会导致Redis主线程的阻塞，从而降低性能甚至引发故障转移。为了解决这个问题，Redis 4.0引入了lazy free特性，即在删除键时，将键的内存释放操作放在后台的I/O线程中处理，从而避免了删除大型键值对时对主线程的阻塞。
在实际操作中，如果你删除了一个非常大的键值对，Redis会将其放入一个待删除的队列中，然后在后台I/O线程中异步地处理这些待删除的键值对。这样一来，即使删除大型数据元素，Redis主线程也可以继续处理其他任务，从而提高了整体性能。
总的来说，Redis 4.0的lazy free特性是一个非常实用的功能。它有效地避免了删除大型键值对时可能带来的性能和可用性问题。当然，这也需要我们在使用时注意内存的使用和数据的完整性。如在使用过程中发现内存占用过大或者数据出现异常，应及时检查和处理。

## 图形化工具
another redis desktop manager
AnotherRedisDesktopManager
https://github.com/qishibo/AnotherRedisDesktopManager

支持windows
linux
mac
支持redis版本？
支持redis cluster？

## 缓存中间件大比拼
ecache

redis支持多种数据结构
其他，mongodb

redis是内存型，读写快

磁盘，io，效率相对慢
redis集群
redis sentinel 支持高可用

五高即：高可用、高可扩展、高性能、高安全、高可管理。
其中，高可用即应用全年的停机时长要在标准范围内，经常说的高并发并不是五高之一，高并发即通过设计保证系统能够同时并行处理很多请求。当系统面临高可用要求时，需要采取冗余设计、容灾备份、自动化运维等措施，以确保系统的稳定性和可靠性。

redis存哪些数据
不变的数据
web session

Redis 缓存写入策略可以根据具体的应用场景和需求进行选择。以下是一些常用的 Redis 缓存写入策略：

缓存穿透：对于空数据的请求，缓存不起作用，每次都会直接请求数据库。为了避免这种情况，可以采用缓存穿透策略，即将空数据也缓存起来，这样当再次请求时，就可以直接从缓存中获取。
缓存雪崩：在某一时间段内，大量的缓存同时过期，导致缓存失效，请求全部落到数据库上，造成数据库压力过大。为了避免这种情况，可以采用缓存雪崩策略，即将缓存的过期时间分散开来，避免同时过期。
缓存预热：在系统启动时，提前将热点数据加载到缓存中，避免在用户请求时再进行加载，提高系统的响应速度。
缓存更新：当数据库中的数据发生变化时，需要及时更新缓存中的数据，以保证缓存中的数据与数据库中的数据一致。可以采用定时任务或者消息队列等方式来实现缓存更新。
缓存降级：在系统压力过大时，可以降低缓存的精度或者减少缓存的容量，以减轻系统的压力。
缓存淘汰：当缓存容量已满时，需要根据一定的策略淘汰掉一些数据，以释放缓存空间。常见的策略包括 LRU（Least Recently Used）和 LFU（Least Frequently Used）等。


缓存雪崩策略是一种用于处理缓存失效问题的方法，主要涉及两个方面：缓存数据的批量失效和查询数据的批量请求。
在批量失效方面，一种策略是在缓存数据过期时间到达时，逐个逐批地删除缓存数据，而不是一次性全部删除。这样可以减少对数据库的集中压力，避免造成数据库过载甚至崩溃的情况。
在批量请求方面，当有大量查询请求到达时，可以根据一定的策略将查询请求分批处理，例如采用队列或者限流等方式，减少对数据库的并发请求，避免数据库在短时间内承受过大的压力。
具体实现可以根据实际应用场景和需求，采用适当的策略和工具进行优化和治理。

Feature Log
2023-06-22: Export\Import keys support
2023-05-26: Search support in Stream && Slow log support
2023-04-01: Search support in List && Deflate raw support
2022-10-07: Arrow Keys support in key list && Memory Analysis in folder
2022-08-05: Clone Connection && Tabs Contextmenu\Mousewheel Support
2022-04-01: Protobuf Support && Memory Analysis
2022-03-03: Readonly Mode && Mointor Support
2022-01-24: Command Dump Support
2022-01-05: Support To Load All Keys
2022-01-01: Brotli\Gzip\Deflate Support && RedisJSON Support
2021-11-26: JSON Editable && Subscribe Support
2021-08-30: Execution log Support && Add Hot Keys
2021-08-16: Custom Formatter View Support!
2021-06-30: Sentinel Support!!
2021-06-24: ACL Support
2021-05-03: Stream Support && Cli Command Tips Support
2021-02-28: Connection Color Tag && Search History Support
2021-02-03: Multiple Select\Delete && Msgpack Viewer Support
2020-12-30: Tree View Support!!!
2020-11-03: Binary View Support && SSH Passparse\Timeout Support
2020-09-04: SSH Cluster Support && Extension Commands Support
2020-06-18: SSL/TLS Support!!!
2020-04-28: Page Zoom && Big Key Loads With Scan && Auto Json
2020-04-18: Unvisible Key\Value Format Support
2020-04-04: Cluster Support!!!
2020-03-13: Dark Mode Support!!! && JsonView In Other Place
2020-02-16: SSH Private Key Support
2020-02-13: Open Cli Console In Tabs
2019-06-14: Custom Font-Family Support
2019-05-28: Key List Resizable
2019-05-09: Search Support In Hash List Set Zset
2019-04-26: Auto Updater
2019-04-09: SSH Tunnel Connection Support
2019-04-01: Extract Search Support
2019-02-22: Single Connection Support
2019-01-08: Project Start

redis redisson分布式锁

### 分布式锁redis实现

分布式锁的常见使用方法： 
1：利用 ThreadLocal + mysql 主键冲突 
2：手写redis锁 
3：利用Redisson封装的锁 
4：利用多个独立的redis,实现红锁 
5：curator封装zookeeper实现分布式锁 
ps:还有其他的分布式锁，利用zookeeper单独实现分布式锁

https://gitee.com/jiang-qikun/distributed-lock

Redis中清除某个库中的所有数据

- 进入redis ：redis-cli -h 192.168.233.132 -p 6380
- 选择其中某个库(比如2号库)：select 2
- 输入命令：flushdb

Redis之各版本特性

1.Redis2.6

Redis2.6在2012年正是发布，经历了17个版本，到2.6.17版本，相对于Redis2.4，主要特性如下：
1）服务端支持Lua脚本。
2）去掉虚拟内存相关功能。
3）放开对客户端连接数的硬编码限制。
4）键的过期时间支持毫秒。
5）从节点支持只读功能。
6）两个新的位图命令：bitcount和bitop。
7）增强了redis-benchmark的功能：支持定制化的压测，CSV输出等功能。
8）基于浮点数自增命令：incrbyfloat和hincrbyfloat。
9）redis-cli可以使用--eval参数实现Lua脚本执行。
10）shutdown命令增强。
11）重构了大量的核心代码，所有集群相关的代码都去掉了，cluster功能将会是3.0版本最大的亮点。
12）info可以按照section输出，并且添加了一些统计项
13）sort命令优化

2.Redis2.8

Redis2.8在2013年11月22日正式发布，经历了24个版本，到2.8.24版本，相比于Redis2.6，主要特性如下：
1）添加部分主从复制的功能，在一定程度上降低了由于网络问题，造成频繁全量复制生成RDB对系统造成的压力。
2）尝试性的支持IPv6.
3）可以通过config set命令设置maxclients。
4）可以用bind命令绑定多个IP地址。
5）Redis设置了明显的进程名，方便使用ps命令查看系统进程。
6）config rewrite命令可以将config set持久化到Redis配置文件中。
7）发布订阅添加了pubsub。
8）Redis Sentinel第二版，相比于Redis2.6的Redis Sentinel，此版本已经变成生产可用。

3.Redis3.0（里程碑）

Redis3.0在2015年4月1日正式发布，相比于Redis2.8主要特性如下：
Redis最大的改动就是添加Redis的分布式实现Redis Cluster。

1）Redis Cluster：Redis的官方分布式实现。
2）全新的embedded string对象编码结果，优化小对象内存访问，在特定的工作负载下载速度大幅提升。
3）Iru算法大幅提升。
4）migrate连接缓存，大幅提升键迁移的速度。
5）migrate命令两个新的参数copy和replace。
6）新的client pause命令，在指定时间内停止处理客户端请求。
7）bitcount命令性能提升。
8）cinfig set设置maxmemory时候可以设置不同的单位（之前只能是字节）
9）Redis日志小做调整：日志中会反应当前实例的角色（master或者slave）。
10）incr命令性能提升。

4.Redis3.2
Redis3.2在2016年5月6日正式发布，相比于Redis3.0主要特征如下：
1）添加GEO相关功能。
2）SDS在速度和节省空间上都做了优化。
3）支持用upstart或者systemd管理Redis进程。
4）新的List编码类型：quicklist。
5）从节点读取过期数据保证一致性。
6）添加了hstrlen命令。
7）增强了debug命令，支持了更多的参数。
8）Lua脚本功能增强。
9）添加了Lua Debugger。
10）config set 支持更多的配置参数。
11）优化了Redis崩溃后的相关报告。
12）新的RDB格式，但是仍然兼容旧的RDB。
13）加速RDB的加载速度。
14）spop命令支持个数参数。
15）cluster nodes命令得到加速。
16）Jemalloc更新到4.0.3版本。


5.Redis4.0
可能出乎很多的意料，Redis3.2之后的版本是4.0，而不是3.4、3.6、3.8。
一般这种重大版本号的升级也意味着软件或者工具本身发生了重大改革。下面是Redis4.0的新特性：
1）提供了模块系统，方便第三方开发者拓展Redis的功能。
2）PSYNC2.0：优化了之前版本中，主从节点切换必然引起全量复制的问题。
3）提供了新的缓存剔除算法：LFU（Last Frequently Used），并对已有算法进行了优化。
4）提供了非阻塞del和flushall/flushdb功能，有效解决删除了bigkey可能造成的Redis阻塞。
5）提供了memory命令，实现对内存更为全面的监控统计。
6）提供了交互数据库功能，实现Redis内部数据库的数据置换。
7）提供了RDB-AOF混合持久化格式，充分利用了AOF和RDB各自优势。
8）Redis Cluster 兼容NAT和Docker。

6.Redis5.0

1.新的Stream数据类型。[1]5.0
2.新的Redis模块API：Timers and Cluster API。
3. RDB现在存储LFU和LRU信息。
4.集群管理器从Ruby（redis-trib.rb）移植到C代码。可以在redis-cli中。查看`redis-cli —cluster help`了解更多信息。
5.新sorted set命令：ZPOPMIN / MAX和阻塞变量。
6.主动碎片整理V2。
7.增强HyperLogLog实现。
8.更好的内存统计报告。
9.许多带有子命令的命令现在都有一个HELP子命令。
10.客户经常连接和断开连接时性能更好。
11.错误修复和改进。
12. Jemalloc升级到5.1版

https://github.com/redis/redis/releases/tag/7.4.0
7 29, 2024

https://github.com/redis/redis/releases/tag/7.2.0
8 15, 2023

https://github.com/redis/redis/releases/tag/7.0.0
4 27, 2022

https://github.com/redis/redis/releases/tag/6.2.0
2 23, 2021

https://github.com/redis/redis/releases/tag/6.0.0
4 30, 2020

5.0.14
10 4, 2021
https://github.com/redis/redis/releases/tag/5.0.14

5.0.0
10 17, 2018
https://github.com/redis/redis/releases/tag/5.0.0

浅析Redis 4.0新特性之LazyFree

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

## 书籍
- Redis深度历险 
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
Mar 01 16:35:30 iZ2ze9f7g12pq4tby7ewz2Z redis-server[9433]: * FATAL CONFIG FILE ERROR *
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
Mar 01 16:35:30 iZ2ze9f7g12pq4tby7ewz2Z redis-server[9433]: * FATAL CONFIG FILE ERROR *
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

Redis 集群和sentinel模式的区别
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

https://gitee.com/edidada/testspringbootredis

### 图形化工具
Another Redis Desktop Manager

免费开源，支持集群
