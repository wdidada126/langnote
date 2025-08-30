# StampedLock

java.util.concurrent.locks.StampedLock
StampedLock类是Java 8中引入的一个用于替代synchronized关键字的锁机制，它提供了更高的并发性能和更灵活的锁定操作。StampedLock的主要作用是在多线程环境下实现读写锁的功能，同时避免了synchronized关键字带来的性能开销。

StampedLock

writeLock();

unlockWrite(long stamp);

readLock();

unlockRead(long stamp);

## 内部原理

使用clh队列

内部类

WNode
ReadLockView
WriteLockView
ReadWriteLockView
