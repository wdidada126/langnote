transient 作用 禁止序列化
volatile 共享内存 
https://github.com/crossoverJie/JCSprout/blob/master/MD/concurrent/volatile.md
这里要重点强调，volatile 并不能保证线程安全性！


Object
wait()
join()

当对象中自定义了 writeObject 和 readObject 方法时，JVM 会调用这两个自定义方法来实现序列化与反序列化。

HashMap 扩容策略？

https://github.com/crossoverJie/JCSprout/blob/master/MD/collection/HashSet.md

HashSet 的成员变量:
private transient HashMap<E,Object> map;  //用于存放最终数据的
// Dummy value to associate with an Object in the backing Map
private static final Object PRESENT = new Object();  //所有写入 map 的 value 值

ThreadPoolExecutor(int corePoolSize, int maximumPoolSize, long keepAliveTime, TimeUnit unit, BlockingQueue<Runnable> workQueue, RejectedExecutionHandler handler) 


