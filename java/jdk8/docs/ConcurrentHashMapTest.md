# ConcurrentHashMapTest
有Map必有Map.Entry


ConcurrentHashMap

|

java.util.concurrent.ConcurrentMap接口

|


java.util.Map接口


类路径

java.util.AbstractMap



https://docs.oracle.com/javase/8/docs/technotes/guides/collections/overview.html

### Collections Framework Overview

- #### Collection Interfaces
- #### Collection Implementations
- #### Concurrent Collections
- #### Design Goals


#### Collection Interfaces

java.util.Collection, has the following descendants:

java.util.Set
java.util.SortedSet
java.util.NavigableSet
java.util.Queue
java.util.concurrent.BlockingQueue
java.util.concurrent.TransferQueue
java.util.Deque
java.util.concurrent.BlockingDeque


java.util.Map, has the following descendants:

java.util.SortedMap
java.util.NavigableMap
java.util.concurrent.ConcurrentMap
java.util.concurrent.ConcurrentNavigableMap


concurrent-aware interfaces are available:

BlockingQueue
TransferQueue
BlockingDeque
ConcurrentMap
ConcurrentNavigableMap

concurrent-aware classes are available:

LinkedBlockingQueue
ArrayBlockingQueue
PriorityBlockingQueue
DelayQueue
SynchronousQueue
LinkedBlockingDeque
LinkedTransferQueue
CopyOnWriteArrayList
CopyOnWriteArraySet
ConcurrentSkipListSet
ConcurrentHashMap
ConcurrentSkipListMap   


- java.util.AbstractMap  继承Map
- java.util.AbstractCollection 继承Collection



ConcurrentHashMap 类中包含两个静态内部类 HashEntry 和 Segment。
锁分段技术
HashTable容器在竞争激烈的并发环境下表现出效率低下的原因，是因为所有访问HashTable的线程都必须竞争同一把锁，
那假如容器里有多把锁，每一把锁用于锁容器其中一部分数据，那么当多线程访问容器里不同数据段的数据时，线程间就不会存在锁竞争，
从而可以有效的提高并发访问效率，这就是ConcurrentHashMap所使用的锁分段技术。
首先将数据分成一段一段的存储，然后给每一段数据配一把锁，当一个线程占用锁访问其中一个段数据的时候，其他段的数据也能被其他线程访问。
有些方法需要跨段，比如size()和containsValue()，它们可能需要锁定整个表而而不仅仅是某个段，这需要按顺序锁定所有段，操作完毕后，又按顺序释放所有段的锁。
这里“按顺序”是很重要的，否则极有可能出现死锁，在ConcurrentHashMap内部，段数组是final的，并且其成员变量实际上也是final的，
但是，仅仅是将数组声明为final的并不保证数组成员也是final的，这需要实现上的保证。这可以确保不会出现死锁，因为获得锁的顺序是固定的。

ConcurrentHashMap中的读方法不需要加锁，所有的修改操作在进行结构修改时都会在最后一步写count 变量，通过这种机制保证get操作能够得到几乎最新的结构更新。

### size()
我们要统计整个ConcurrentHashMap里元素的大小，就必须统计所有Segment里元素的大小后求和。
Segment里的全局变量count是一个volatile变量，那么在多线程场景下，我们是不是直接把所有Segment的count相加就可以得到整个ConcurrentHashMap大小了呢？
不是的，虽然相加时可以获取每个Segment的count的最新值，但是拿到之后可能累加前使用的count发生了变化，那么统计结果就不准了。
所以最安全的做法，是在统计size的时候把所有Segment的put，remove和clean方法全部锁住，但是这种做法显然非常低效。
因为在累加count操作过程中，之前累加过的count发生变化的几率非常小，所以ConcurrentHashMap的做法是先尝试2次通过不锁住Segment的方式来统计各个Segment大小，如果统计的过程中，容器的count发生了变化，则再采用加锁的方式来统计所有Segment的大小。


### ConcurrentHashMap 的高并发性主要来自于三个方面：

用分离锁实现多个线程间的更深层次的共享访问。
用 HashEntery 对象的不变性来降低执行读操作的线程在遍历链表期间对加锁的需求。
通过对同一个 Volatile 变量的写 / 读访问，协调不同线程间读 / 写操作的内存可见性。
使用分离锁，减小了请求同一个锁的频率。

https://blog.csdn.net/dingjianmin/article/details/79776646