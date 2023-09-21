# algorithm



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