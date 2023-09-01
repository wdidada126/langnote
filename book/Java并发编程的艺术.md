# Java并发编程的艺术

https://book.douban.com/subject/26591326/

方腾飞 ifeve
魏鹏
程晓明 IBM developerWorks

jvm
cpu

cpu
L123 缓存

手册
intel



栅栏 锁 内存屏



翻译的不错.大部分内容来自于jsr-133和Doug Lea的jsr-133 Cookbook,如果想深入研究这方面的问题,推荐仔细研究一下上面的两个文献和本书里提及到的引用文献(当然还有Lea的另外两本书),本书文献的引用只提及于书的正文,末尾并没有参考文献.也许是书名的"著"导致的这个问题.



### 第1章　并发编程的挑战



### 第2章　Java并发机制的底层实现原理

volatile、synchronized和原子操作的实现原理



### 第3章　Java内存模型



### 第4章　Java并发编程基础

volitale cas更新一个标量

### 第5章　Java中的锁



### 第6章　Java并发容器和框架

ConcurrentHashMap

HashTable容器使用synchronized来保证线程安全





JDK 7提供了7个阻塞队列，如下。
·ArrayBlockingQueue：一个由数组结构组成的有界阻塞队列。
·LinkedBlockingQueue：一个由链表结构组成的有界阻塞队列。
·PriorityBlockingQueue：一个支持优先级排序的无界阻塞队列。
·DelayQueue：一个使用优先级队列实现的无界阻塞队列。
·SynchronousQueue：一个不存储元素的阻塞队列。
·LinkedTransferQueue：一个由链表结构组成的无界阻塞队列。
·LinkedBlockingDeque：一个由链表结构组成的双向阻塞队列。





工作窃取（work-stealing）算法

### 第7章　Java中的13个原子操作类

Atomic包里的类基本都是使用Unsafe实现的包装类。

### 第8章　Java中的并发工具类

CountDownLatch、CyclicBarrier和

Semaphore工具类提供了一种并发流程控制的手段，Exchanger工具类则提供了在线程间交换数

据的一种手段



`CountDownLatch`和`CyclicBarrier`都是Java中用于多线程协作的工具类，它们的作用是在多个线程之间同步执行，以实现一些复杂的场景。虽然它们的作用有些相似，但它们的实现方式和使用场景有很大的区别。

1. `CountDownLatch`

`CountDownLatch`是一种简单的同步工具，它用于等待一个或多个线程完成某些操作后再继续执行。具体来说，`CountDownLatch`维护一个计数器，该计数器初始化为一个正整数，当一个或多个线程调用`countDown()`方法时，计数器的值减1，当计数器的值变为0时，等待的线程将被唤醒继续执行。

`CountDownLatch`的主要作用是在多个线程之间协调执行顺序。例如，可以使用`CountDownLatch`来等待多个线程完成初始化操作后再开始执行其他操作。`CountDownLatch`的使用场景比较单一，它适用于一次性等待多个线程完成某个操作，而且这些线程之间的协作方式比较简单。

1. `CyclicBarrier`

`CyclicBarrier`也是一种同步工具，它用于等待多个线程到达某个屏障点后再继续执行。具体来说，`CyclicBarrier`维护一个计数器和一个屏障点，当多个线程都调用`await()`方法时，计数器的值增加1，当计数器的值达到屏障点时，所有等待的线程将被唤醒继续执行。

`CyclicBarrier`的主要作用是在多个线程之间协调执行顺序，并且这些线程之间的协作方式比较复杂。例如，可以使用`CyclicBarrier`来等待多个线程执行完某个阶段的任务后再开始执行下一个阶段的任务。`CyclicBarrier`还支持自定义回调函数，在所有线程到达屏障点后执行特定的操作。

1. 区别

`CountDownLatch`和`CyclicBarrier`的主要区别可以总结如下：

- 计数器的初始值不同：`CountDownLatch`的计数器初始值为一个正整数，`CyclicBarrier`的计数器初始值为一个正整数和一个屏障点。
- 计数器的变化方式不同：`CountDownLatch`的计数器通过`countDown()`方法递减，`CyclicBarrier`的计数器通过`await()`方法递增。
- 等待的线程数量不同：`CountDownLatch`可以等待一个或多个线程完成某个操作，`CyclicBarrier`必须等待多个线程到达屏障点。
- 作用的场景不同：`CountDownLatch`适用于一次性等待多个线程完成某个操作，`CyclicBarrier`适用于多个线程之间协调执行顺序，并且这些线程之间的协作方式比较复杂。

需要注意的是，`CountDownLatch`和`CyclicBarrier`都是一次性的同步工具，一旦计数器的值变为0，就不能再用它们来等待其他线程的到来或执行。如果需要多次等待，则需要使用`Semaphore`或`ReentrantLock`等可重入的同步工具。



### 第9章　Java中的线程池

全局锁



### 第10章　Executor框架



### 第11章　Java并发编程实践