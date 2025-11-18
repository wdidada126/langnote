# OpenMP


OpenMP
https://github.com/llvm-mirror/openmp

OpenMP 是由 OpenMP Architecture Review Board 牵头提出的，并已被广泛接受的，用于共享内存并行系统的多线程程序设计的一套编译指令 (Compiler Directive)。OpenMP 支持的编程语言包括 C 语言、C++ 和 Fortran；而支持 OpenMP 的编译器包括 Sun Compiler，GNU Compiler 和 Intel Compiler 等。OpenMP 提供了对并行算法的高层的抽象描述，程序员通过在源代码中加入专用的 pragma 来指明自己的意图，由此编译器可以自动将程序进行并行化，并在必要之处加入同步互斥以及通信。当选择忽略这些 pragma，或者编译器不支持 OpenMP 时，程序又可退化为通常的程序 (一般为串行)，代码仍然可以正常运作，只是不能利用多线程来加速程序执行。

OpenMP 提供的这种对于并行描述的高层抽象降低了并行编程的难度和复杂度，这样程序员可以把更多的精力投入到并行算法本 身，而非其具体实现细节。对基于数据分集的多线程程序设计，OpenMP 是一个很好的选择。同时，使用 OpenMP 也提供了更强的灵活性，可以较容易的适 应不同的并行系统配置。线程粒度和负载平衡等是传统多线程程序设计中的难题，但在 OpenMP 中，OpenMP 库从程序员手中接管了部分这两方面的工作。

但是，作为高层抽象，OpenMP 并不适合需要复杂的线程间同步和互斥的场合。

OpenMP 的另一个缺点是不能在非共享内存系统 (如计算机集群) 上使用。在这样的系统上，MPI 使用较多。

