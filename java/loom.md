# loom

https://github.com/openjdk/loom

Loom在JDK中是一个创新项目，旨在改进Java虚拟机（JVM）的执行模型，以支持轻量级线程（也称为Virtual Threads），从而提高Java在处理并发和并行编程方面的性能和可伸缩性。以下是关于Loom项目的详细解释：

项目目标：
Loom项目的主要目标是改进Java中的多线程编程模型，通过引入轻量级的线程实现，来简化并提升Java应用程序的并发性能。
核心特性：
Fibers（纤程）：Fibers是Loom项目中的关键特性，它们是一种轻量级的、用户态的线程实现，允许在同一操作系统线程内运行大量Fibers，减少内存消耗和提高性能。与传统的操作系统线程相比，Fibers的创建和销毁成本较低。
Continuations（续体）：它允许在Fiber被挂起时保存其执行状态，并在需要时恢复到挂起的状态。这为Fibers的挂起和恢复提供了一种高效的机制，避免了传统线程上下文切换的开销。
Virtual Threads（虚拟线程）：Virtual Threads是对Fibers进行透明封装的机制，允许开发者使用简单的编程模型处理大规模并发而无需担心线程管理细节。
Scoped Threads（作用域线程）：允许Fibers在有限的作用域内运行。
实现方式：
Loom项目通过引入轻量级的Fibers，使得Java应用程序可以更高效地处理大量并发任务，提供更高的并发性能和更好的可伸缩性。
由于Fibers不再需要映射到操作系统的本地线程，Java应用程序的内存消耗将显著降低，这对于资源有限的环境和云计算平台尤为重要。
Loom项目还提供了对并发编程的简化，使开发者能够更专注于业务逻辑而无需过多关注底层线程管理。
当前状态：
在当前版本的JDK中，Loom项目的某些功能（如VirtualThread）并未完全公开。例如，虽然VirtualThread类存在，但它使用default修饰符隐藏在java.lang包中，并且是Thread的子类。
协程的创建API位于Thread类中，开发者可以使用类似Thread.startVirtualThread()的方法来创建协程。
综上所述，Loom在JDK中是一个重要的项目，它通过引入轻量级的线程实现和其他并发原语，显著改进了Java的并发编程模型，使得开发者能够更高效地处理大量并发任务，同时保持较低的系统资源消耗。

