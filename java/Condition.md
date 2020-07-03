# Condition



详解Condition的await和signal等待/通知机制

https://www.jianshu.com/p/28387056eeb4





--> UnSafe

Lock







Condition在Concurrent包中，主要用于替代以前对象Object上的wait()、notify()等方法实现线程间的协作。

相比wait()、notify()，Condition根据和Lock的结合，可以实现更复杂和精细的线程协同和等待。

Condition包含了接口和在AbstractQueuedSynchronizer类中的ConditionObject类的实现



原来趣分期在考我并发