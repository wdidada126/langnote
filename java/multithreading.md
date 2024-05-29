# multithreading

JAVA多线程实现方式主要有三种：

- 继承Thread类
- 实现Runnable接口
- 使用ExecutorService、Callable、Future实现有返回结果的多线程。

其中前两种方式线程执行完后都没有返回值，只有最后一种是带返回值的。

jdk7
ForkJoinPool

java.util.concurrent.ForkJoinPool 是es接口的实现类
