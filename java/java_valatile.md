# java volatile



volatile

原子性

可见性

有序性



深度解析volatile—底层实现

https://www.jianshu.com/p/2643c9ea1b82

通过使用-XX:+UnlockDiagnosticVMOptions -XX:+PrintAssembly

IDEA打印出了源代码的汇编指令。

加入volatile关键字和没有加入volatile关键字时所生成的汇编代码发现，加入volatile关键字时，会多出一个lock前缀指令。我们发现，volatile变量在字节码级别没有任何区别，在汇编级别使用了lock指令前缀。

lock是一个指令前缀，Intel的手册上对其的解释是：

简单理解也就是说，lock后就是一个原子操作。原子操作是指不会被线程调度机制打断的操作；这种操作一旦开始，就一直运行到结束，中间不会有任何 context switch （切换到另一个线程）。

当使用 LOCK 指令前缀时，它会使 CPU 宣告一个 LOCK# 信号，这样就能确保在多处理器系统或多线程竞争的环境下互斥地使用这个内存地址。当指令执行完毕，这个锁定动作也就会消失。



