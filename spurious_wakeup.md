# spurious wakeup



虚假唤醒

java线程

假唤醒（spurious wakeups）

http://ifeve.com/thread-signaling/

https://juejin.im/post/5d32a6545188257f3850d514

https://www.zhihu.com/question/271521213

为什么条件锁会产生虚假唤醒现象（spurious wakeup）





举个例子来说：

pthread 的条件变量等待 `pthread_cond_wait` 是使用阻塞的系统调用实现的（比如 Linux 上的 `futex`），这些阻塞的系统调用在进程被信号中断后，通常会中止阻塞、直接返回 EINTR 错误。

同样是阻塞系统调用，你从 `read` 拿到 EINTR 错误后可以直接决定重试，因为这通常不影响它本身的语义。而条件变量等待则不能，因为本线程拿到 EINTR 错误和重新调用 `futex` 等待之间，可能别的线程已经通过 `pthread_cond_signal` 或者 `pthread_cond_broadcast`发过通知了。 

所以，虚假唤醒的一个可能性是条件变量的等待被信号中断。

不过，把等待放到循环里的另一个原因是还可能有这样的情况（有人觉得它是虚假唤醒的一种，有人觉得不是）：明明有对应的唤醒，但条件不成立。这是因为可能由于线程调度的原因，被条件变量唤醒的线程在本线程内真正执行「加锁并返回」前，另一个线程插了进来，完整地进行了一套「拿锁、改条件、还锁」的操作。

比如 Windows 下 `SleepConditionVariableCS` 的文档中就明确指出了可能出现这种情况。（pthread 里的情况则有点区别，人家的 `pthread_cond_signal` 本来就可能唤醒多个正在等待的线程。）



https://en.wikipedia.org/wiki/Spurious_wakeup



condition variables



- pthread_cond_timedwait()
- pthread_cond_wait
- pthread_mutex_lock



https://stackoverflow.com/questions/8594591/why-does-pthread-cond-wait-have-spurious-wakeups

Spurious wakeup describes a complication in the use of condition variables as provided by certain multithreading APIs such as POSIX Threads and the Windows API.



[Be Aware of the Traps of Condition Variables](https://www.modernescpp.com/index.php/c-core-guidelines-be-aware-of-the-traps-of-condition-variables)



