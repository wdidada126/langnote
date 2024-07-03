# java7

Java 7引入了Fork/Join框架，是一种基于工作窃取算法的任务执行框架，用于处理递归式的并行问题。其核心是在一个大任务中递归地将其拆分成小任务，然后将每个小任务加入到一个队列中等待处理。当一个工作线程处理完自己的任务后，会从其它工作线程的队列中随机挑选一个任务进行处理，这个过程就是工作线程的“窃取”行为。这种工作线程之间的任务相互窃取的算法能够确保各个工作线程的负载基本平衡，提高并发处理能力。 Fork/Join框架主要由下面几个类组成：

ForkJoinTask：任务抽象类，实现了future和work-stealing算法；
RecursiveTask：继承ForkJoinTask，有返回值的任务；
RecursiveAction：继承ForkJoinTask，没有返回值的任务；
ForkJoinPool：工作线程的线程池；
ForkJoinWorkerThread：工作线程。
Fork/Join框架的使用步骤大致如下：

创建ForkJoinPool；
创建ForkJoinTask（RecursiveTask或RecursiveAction）；
调用ForkJoinPool的submit()方法将任务提交给线程池；
调用ForkJoinTask的join()方法等待任务执行完毕并获取执行结果。