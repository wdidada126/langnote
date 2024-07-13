# java_atomic

Number (java.lang)
    Striped64 (java.util.concurrent.atomic)
        LongAdder (java.util.concurrent.atomic)
        LongAccumulator (java.util.concurrent.atomic)
        DoubleAdder (java.util.concurrent.atomic)
        DoubleAccumulator (java.util.concurrent.atomic)

Striped64中的"64"主要指的是该组件支持的数值类型及其位大小。具体来说，它表示Striped64是用来处理64位数值的累加操作的，这里的64位数值主要指的是Long类型和Double类型的数。

详细解释
数值类型：
Long类型：在Java中，Long类型是一个64位的整数类型，可以表示非常大的整数。Striped64提供了对Long类型数值的并发累加操作。
Double类型：虽然Double类型在Java中也是以64位存储的（遵循IEEE 754标准），但它表示的是浮点数而非整数。Striped64同样支持对Double类型数值的并发累加操作，尽管这种累加在浮点数上可能不如整数直观或精确。
并发性能：
Striped64的设计目的是为了在高并发环境下提供高效的累加操作。它通过内部的分散机制来避免多线程之间的竞争，从而提高累加操作的性能。
内部实现：
Striped64内部维护了一个基础值（base）和一个Cell数组。基础值用于在没有竞争时的累加操作，而Cell数组则用于分散竞争时的累加操作。每个Cell都可以看作是一个独立的累加器，用于存储和更新特定线程的累加值。
哈希映射：
Striped64使用每个线程的哈希值来映射到Cell数组的特定位置。这种映射方式使得不同线程能够分散到不同的Cell上进行操作，从而避免了多线程对同一个Cell的竞争。
综上所述，Striped64中的"64"指的是它所支持的数值类型（Long和Double）的位大小，即64位。这一设计使得Striped64能够在高并发环境下提供高效的64位数值累加操作。


Striped64是Java 8中引入的一个并发计数组件，其作用主要是在高并发环境下提供高效的累加器（accumulator）功能。Striped64的设计思路是通过内部的分散计算来避免多线程竞争，从而提高并发性能。具体来说，Striped64的作用和特点可以归纳如下：

1. 并发计数
Striped64可以在高并发环境下对数值进行累加（或累减）操作，支持Long类型和Double类型的计数。它通过内部维护的一个基础值（base）和一个单元哈希表（Cell数组）来实现并发计数。在没有竞争的情况下，累加操作会直接在基础值上进行；当竞争激烈时，则会将累加操作分散到不同的Cell中进行，以降低CAS（Compare-And-Swap）操作的竞争。

2. 分散竞争
Striped64的核心思想是通过分散计算来分散竞争。每个线程都会通过计算哈希值来映射到Cell数组的某个位置，然后对该位置的Cell进行CAS操作。由于不同线程的哈希值可能不同，因此它们会分散到不同的Cell上进行操作，从而避免了多线程对同一个资源的竞争。

3. 高性能
由于Striped64能够有效地分散竞争，因此在高并发环境下能够提供较高的性能。与传统的同步机制（如synchronized）和原子类（如AtomicLong）相比，Striped64在并发计数方面通常具有更好的性能表现。

4. 灵活性
Striped64提供了灵活的累加操作接口，如longAccumulate和doubleAccumulate方法。这些方法允许用户自定义累加操作，从而满足不同的业务需求。

5. 实现细节
内部数据结构：Striped64内部包含一个基础值（base）和一个Cell数组。基础值用于在没有竞争时的累加操作，而Cell数组则用于分散竞争时的累加操作。
哈希映射：Striped64使用每个线程的探针字段（probe）作为哈希码来映射到Cell数组的指定位置。这种映射方式使得不同线程能够分散到不同的Cell上进行操作。
CAS操作：Striped64在Cell中使用了CAS操作来保证并发更新时的原子性。
6. 应用场景
Striped64适用于需要高并发计数的场景，如性能监控、日志统计等。在高并发环境下，Striped64能够提供比传统同步机制和原子类更高的性能表现。

综上所述，Striped64是Java 8中引入的一个高效并发计数组件，它通过分散计算来避免多线程竞争，从而在高并发环境下提供高性能的累加器功能。