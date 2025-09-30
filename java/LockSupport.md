# LockSupport

LockSupport是一个线程阻塞工具类，所有的方法都是静态方法，可以让线程在任意位置阻塞，当然阻塞之后肯定得有唤醒的方法。主要有两类方法：`park`和`unpark`。park()英文意思为停车，unpark()就是让车启动然后跑起来。

java.util.concurrent.locks.LockSupport
