# 狂神说JUC


Object wait

Lock
await()



Java默认有几个线程？ 2 个 mian、GC

Runnable、Callable



并发（多线程操作同一个资源）
CPU 一核 ，模拟出来多条线程，天下武功，唯快不破，快速交替
并行（多个人一起行走）
CPU 多核 ，多个线程可以同时执行； 线程池
并



wait/sleep 区别

1、来自不同的类
wait => Object
sleep => Thread
2、关于锁的释放
wait 会释放锁，sleep 睡觉了，抱着锁睡觉，不会释放！
3、使用的范围是不同的
wait
synchronized
sleep 可以再任何地方
4、是否需要捕获异常
wait 不需要捕获异常
sleep 必须要捕获异常


Lock锁

传统 Synchronized


ReentrantLock
构造函数有一个参数boolean，引出公平锁和非公平锁



Synchronized 和 Lock 区别
1、Synchronized 内置的Java关键字， Lock 是一个Java类
2、Synchronized 无法判断获取锁的状态，Lock 可以判断是否获取到了锁（？
3、Synchronized 会自动释放锁，lock 必须要手动释放锁！如果不释放锁，死锁
4、Synchronized 线程 1（获得锁，阻塞）、线程2（等待，傻傻的等）；Lock锁就不一定会等待下
去；
5、Synchronized 可重入锁，不可以中断的，非公平；Lock ，可重入锁，可以 判断锁，非公平（可以
自己设置）；
6、Synchronized 适合锁少量的代码同步问题，Lock 适合锁大量的同步代码！



##### 9.ReadWriteLock
ReentrantReadWriteLock
ReadWriteLock readWriteLock = new ReentrantReadWriteLock();
readWriteLock.ReadLock()
readWriteLock.WriteLock()




10

BlockingQueue

LinkedBlockingQueue

ArrayBlockingQueue

方式    抛出异常 有返回值，不抛出异常    阻塞 等待    超时等待
添加    add         offer()                               put()             offer(,,)
移除   remove   poll()                                 take()            poll(,)
检测队首元素element peek - -

