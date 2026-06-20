# algorithm
算法可视化网站
https://algorithm-visualizer.org/

[线性表之链表_单向循环链表&约瑟夫环问题](https://blog.csdn.net/yangshangwei/article/details/103864131)

## 布隆过滤器 Bloom filter
[Bloom filter](https://blog.csdn.net/she_lock/article/details/103856260)

算法分析

## 洗牌算法（Fisher-Yates Shuffle Algorithm）
给一堆学号，乱序排座位，用什么算法保证排座位的结果每次都不一样尽量随机

可以使用洗牌算法（Fisher-Yates Shuffle Algorithm）来实现随机排座位。具体步骤如下：
1. 从最后一个学号开始，依次向前遍历所有学号。
2. 对于当前遍历到的学号，将其与一个随机生成的整数（范围在0到当前遍历位置之间）进行交换。
3. 重复步骤2，直到遍历完所有学号。

这样，每次执行洗牌算法得到的座位顺序都会不一样，尽量满足随机性要求。

推荐一个Java开源库：Apache Commons Lang，它提供了一个工具类`CollectionsUtils`，其中包含了洗牌算法的实现。使用方法如下：

```java
import org.apache.commons.lang3.RandomUtils;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class ShuffleDemo {
    public static void main(String[] args) {
        List<Integer> ids = new ArrayList<>();
        for (int i = 1; i <= 10; i++) {
            ids.add(i);
        }

        // 使用Apache Commons Lang提供的洗牌算法
        Collections.shuffle(ids, RandomUtils.nextInt());

        System.out.println("洗牌后的结果：" + ids);
    }
}
```

在这个示例中，我们创建了一个包含1到10的整数列表，然后使用`Collections.shuffle()`方法和`RandomUtils.nextInt()`方法进行洗牌。最后输出洗牌后的结果。

Apache Commons Lang是一个Java开源库，提供了许多有用的工具类和方法。以下是Apache Commons Lang的Maven坐标：

```xml
<dependency>
    <groupId>org.apache.commons</groupId>
    <artifactId>commons-lang3</artifactId>
    <version>3.12.0</version>
</dependency>
```

在Maven项目的pom.xml文件中，只需要将以上代码添加到`<dependencies>`标签中即可引入Apache Commons Lang库。注意要使用最新版本的3.12.0版本。

## COPS算法
COPS是保序系统的集群(Clusters of Order Preserving System)
COPS算法是一种分布式系统中的因果一致性算法。它设计为支持复杂的在线应用，这些应用托管在少量的大规模数据中心，每个应用都有前端服务器（COPS客户端）以及后端key-value数据存储。

COPS算法通过在本地数据中心以线性化方式执行所有的put写操作和get读操作，然后会跨数据中心以因果一致性的顺序在后台进行复制。这样可以确保数据的一致性以及操作的因果关系。

该算法基于因果一致性，假设一个key-value数据存储有两个基本操作：put(key,val)和get(key)。类似于在单机的共享内存系统中的读操作和写操作。同时，它遵循三个规则来表达潜在一致性：

如果a和b是执行线程中的两个操作，如果操作a发生在操作b之前，那么a ->b。
如果a是一个put放入操作，且b是一个获得操作，能返回被a放入的写操作结果值，那么a->b。
在同一执行线程，如果a ->b，则a->b。
通过这些规则，COPS算法在分布式系统中实现了因果一致性，为在线应用提供了高可用性、低延迟、分区容错和可扩展性的保证。

分布式系统因果一致性与COPS算法.mhtml