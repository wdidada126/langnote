# valgrind

Valgrind 是一个用于构建动态分析工具的仪器框架。 Valgrind 工具可以自动检测许多内存管理和线程错误，并对程序进行详细剖析。 目前，Valgrind 发行版包括七种高质量工具：一个内存错误检测器、两个线程错误检测器、一个高速缓存和分支预测剖析器、一个生成调用图的高速缓存和分支预测剖析器以及两个不同的堆剖析器。 它还包括一个实验性的 SimPoint 基本块向量生成器。 它可在以下平台上运行 X86/Linux、AMD64/Linux、ARM/Linux、ARM64/Linux、PPC32/Linux、PPC64/Linux、PPC64LE/Linux、S390X/Linux、MIPS32/Linux、MIPS64/Linux、X86/Solaris、AMD64/Solaris、ARM/Android（2.3.x 及更高版本）、ARM64/Android、X86/Android（4.0 及更高版本）、MIPS32/Android、X86/FreeBSD、AMD64/FreeBSD、ARM64/FreeBSD、X86/Darwin 和 AMD64/Darwin (Mac OS X 10.12)。

## 官网
https://valgrind.org/

[内存、性能问题分析的利器](https://blog.csdn.net/breaksoftware/article/details/79429330)

## 版本

valgrind 3.4.1
valgrind 3.4.0
valgrind 3.3.1
valgrind 3.3.0
valgrind 3.2.3
valgrind 3.2.2
valgrind 3.2.1
valgrind 3.2.0
valgrind 3.1.1
valgrind 3.1.0
valgrind 3.0.1
valgrind 3.0.0
valgrind 2.4.1
valgrind 2.2.0
valgrind 2.1.2
valgrind 2.1.1
valgrind 2.1.0
valgrind 2.0.0
valgrind 1.9.6

## 安装

git clone https://sourceware.org/git/valgrind.git
cd valgrind
./autogen.sh
./configure
make


sudo apt install -y valgrind valgrind-dbg valgrind-mpi

valgrind --leak-check=full --track-origins=yes ./my_program


Valgrind 允许你将输出或报错信息保存到文件中，而不是直接显示在终端上。这在你需要稍后分析输出或在不方便查看终端输出的环境中运行 Valgrind 时非常有用。

要将 Valgrind 的输出保存到文件中，你可以使用重定向操作符（>）或 --log-file 选项。以下是两种方法的示例：

使用重定向操作符
在 Unix-like 系统中，你可以使用重定向操作符 > 将 Valgrind 的输出重定向到文件中。例如：

bash
valgrind --leak-check=full ./your_program > valgrind_output.txt
但是，请注意，这种方法只会将标准输出（stdout）重定向到文件中，而 Valgrind 的错误和警告信息（包括内存泄露报告）通常是通过标准错误（stderr）输出的。为了同时捕获标准输出和标准错误，你可以使用 &>（在某些 shell 中是 2>&1）：

bash
valgrind --leak-check=full ./your_program &> valgrind_output.txt  
# 或者  
valgrind --leak-check=full ./your_program 2>&1 > valgrind_output.txt
注意：&> 是 Bash 和一些其他 shell 的语法糖，用于同时重定向标准输出和标准错误。如果你使用的是较旧的 shell 或脚本需要在不同的环境中运行，最好使用 2>&1。

使用 --log-file 选项
Valgrind 提供了 --log-file 选项，允许你指定一个文件来保存其输出。使用此选项时，Valgrind 会将所有输出（包括标准输出和标准错误）写入指定的文件，而不会在终端上显示任何内容。例如：

bash
valgrind --leak-check=full --log-file=valgrind_output.txt ./your_program
这种方法更加直接和方便，特别是当你只关心将 Valgrind 的输出保存到文件时。

总结
使用重定向操作符（&> 或 2>&1 >）可以捕获 Valgrind 的标准输出和标准错误。
使用 --log-file 选项可以将 Valgrind 的所有输出保存到指定的文件中，而不会在终端上显示任何内容。
根据你的具体需求选择合适的方法。


blog_rest_valgrind_output.txt

valgrind_output.txt

sudo apt install valgrind
valgrind --leak-check=full --track-origins=yes --log-file=valgrind_rest_poco.log --leak-check=full --show-leak-kinds=all ./blog_rest



==1255== Process terminating with default action of signal 2 (SIGINT)
==1255==    at 0x4E26117: __futex_abstimed_wait_common64 (futex-internal.c:57)
==1255==    by 0x4E26117: __futex_abstimed_wait_common (futex-internal.c:87)
==1255==    by 0x4E26117: __futex_abstimed_wait_cancelable64 (futex-internal.c:139)
==1255==    by 0x4E28A40: __pthread_cond_wait_common (pthread_cond_wait.c:503)
==1255==    by 0x4E28A40: pthread_cond_wait@@GLIBC_2.3.2 (pthread_cond_wait.c:627)
==1255==    by 0x85C2B6: Poco::EventImpl::waitImpl() (Event_POSIX.cpp:109)
==1255==    by 0x74ED83: Poco::Event::wait() (Event.h:107)
==1255==    by 0x8A5E0D: Poco::PooledThread::run() (ThreadPool.cpp:191)
==1255==    by 0x8A280C: Poco::(anonymous namespace)::RunnableHolder::run() (Thread.cpp:56)
==1255==    by 0x8A242E: Poco::ThreadImpl::runnableEntry(void*) (Thread_POSIX.cpp:358)
==1255==    by 0x4E29AC2: start_thread (pthread_create.c:442)
==1255==    by 0x4EBAA03: clone (clone.S:100)
==1255==
==1255== HEAP SUMMARY:
==1255==     in use at exit: 789,065 bytes in 8,077 blocks
==1255==   total heap usage: 18,652 allocs, 10,575 frees, 3,400,320 bytes allocated
==1255==
==1255== 144 bytes in 1 blocks are definitely lost in loss record 1,043 of 1,362
==1255==    at 0x4848899: malloc (in /usr/libexec/valgrind/vgpreload_memcheck-amd64-linux.so)
==1255==    by 0x3B00D9: redirecting_allocator(unsigned long, int) (my_malloc.cc:279)
==1255==    by 0x3B0391: void* my_raw_malloc<&(redirecting_allocator(unsigned long, int))>(unsigned long, int) (my_malloc.cc:322)
==1255==    by 0x3B014A: my_malloc(unsigned int, unsigned long, int) (my_malloc.cc:475)
==1255==    by 0x3AB0BB: MEM_ROOT::AllocBlock(unsigned long, unsigned long) (my_alloc.cc:89)
==1255==    by 0x3AB391: MEM_ROOT::ForceNewBlock(unsigned long) (my_alloc.cc:156)
==1255==    by 0x3AB2DB: MEM_ROOT::AllocSlow(unsigned long) (my_alloc.cc:143)
==1255==    by 0x350BB0: MEM_ROOT::Alloc(unsigned long) (my_alloc.h:164)
==1255==    by 0x3ABBF7: memdup_root(MEM_ROOT*, void const*, unsigned long) (my_alloc.cc:296)
==1255==    by 0x374D87: do_add_plugin(MYSQL*, st_mysql_client_plugin*, void*, int, __va_list_tag*) (client_plugin.cc:229)
==1255==    by 0x374FC7: add_plugin_noargs(MYSQL*, st_mysql_client_plugin*, void*, int, ...) (client_plugin.cc:277)
==1255==    by 0x375251: mysql_client_plugin_init (client_plugin.cc:359)
==1255==
==1255== 304 bytes in 1 blocks are possibly lost in loss record 1,132 of 1,362
==1255==    at 0x484DA83: calloc (in /usr/libexec/valgrind/vgpreload_memcheck-amd64-linux.so)
==1255==    by 0x40147D9: calloc (rtld-malloc.h:44)
==1255==    by 0x40147D9: allocate_dtv (dl-tls.c:375)
==1255==    by 0x40147D9: _dl_allocate_tls (dl-tls.c:634)
==1255==    by 0x4E2A7B4: allocate_stack (allocatestack.c:430)
==1255==    by 0x4E2A7B4: pthread_create@@GLIBC_2.34 (pthread_create.c:647)
==1255==    by 0x8A1889: Poco::ThreadImpl::startImpl(Poco::SharedPtr<Poco::Runnable, Poco::ReferenceCounter, Poco::ReleasePolicy<Poco::Runnable> >) (Thread_POSIX.cpp:206)
==1255==    by 0x8A2BBF: Poco::Thread::start(Poco::Runnable&) (Thread.cpp:129)
==1255==    by 0x69FED7: Poco::Net::TCPServer::start() (TCPServer.cpp:111)
==1255==    by 0x23164F: BlogRestServerApp::main(std::vector<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, std::allocator<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > > > const&) (blog_rest.cpp:291)
==1255==    by 0x2F2CAD: Poco::Util::Application::run() (Application.cpp:358)
==1255==    by 0x30D1F5: Poco::Util::ServerApplication::run() (ServerApplication.cpp:95)
==1255==    by 0x30D374: Poco::Util::ServerApplication::run(int, char**) (ServerApplication.cpp:585)
==1255==    by 0x22D4E2: main (blog_rest.cpp:302)
==1255==
==1255== 304 bytes in 1 blocks are possibly lost in loss record 1,133 of 1,362
==1255==    at 0x484DA83: calloc (in /usr/libexec/valgrind/vgpreload_memcheck-amd64-linux.so)
==1255==    by 0x40147D9: calloc (rtld-malloc.h:44)
==1255==    by 0x40147D9: allocate_dtv (dl-tls.c:375)
==1255==    by 0x40147D9: _dl_allocate_tls (dl-tls.c:634)
==1255==    by 0x4E2A7B4: allocate_stack (allocatestack.c:430)
==1255==    by 0x4E2A7B4: pthread_create@@GLIBC_2.34 (pthread_create.c:647)
==1255==    by 0x8A1889: Poco::ThreadImpl::startImpl(Poco::SharedPtr<Poco::Runnable, Poco::ReferenceCounter, Poco::ReleasePolicy<Poco::Runnable> >) (Thread_POSIX.cpp:206)
==1255==    by 0x8A2BBF: Poco::Thread::start(Poco::Runnable&) (Thread.cpp:129)
==1255==    by 0x8A58D6: Poco::PooledThread::start() (ThreadPool.cpp:85)
==1255==    by 0x8A707D: Poco::ThreadPool::getThread() (ThreadPool.cpp:461)
==1255==    by 0x8A6838: Poco::ThreadPool::startWithPriority(Poco::Thread::Priority, Poco::Runnable&, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&) (ThreadPool.cpp:365)
==1255==    by 0x6A13AB: Poco::Net::TCPServerDispatcher::enqueue(Poco::Net::StreamSocket const&) (TCPServerDispatcher.cpp:150)
==1255==    by 0x6A005D: Poco::Net::TCPServer::run() (TCPServer.cpp:148)
==1255==    by 0x8A280C: Poco::(anonymous namespace)::RunnableHolder::run() (Thread.cpp:56)
==1255==    by 0x8A242E: Poco::ThreadImpl::runnableEntry(void*) (Thread_POSIX.cpp:358)
==1255==
==1255== 608 bytes in 2 blocks are possibly lost in loss record 1,216 of 1,362
==1255==    at 0x484DA83: calloc (in /usr/libexec/valgrind/vgpreload_memcheck-amd64-linux.so)
==1255==    by 0x40147D9: calloc (rtld-malloc.h:44)
==1255==    by 0x40147D9: allocate_dtv (dl-tls.c:375)
==1255==    by 0x40147D9: _dl_allocate_tls (dl-tls.c:634)
==1255==    by 0x4E2A7B4: allocate_stack (allocatestack.c:430)
==1255==    by 0x4E2A7B4: pthread_create@@GLIBC_2.34 (pthread_create.c:647)
==1255==    by 0x8A1889: Poco::ThreadImpl::startImpl(Poco::SharedPtr<Poco::Runnable, Poco::ReferenceCounter, Poco::ReleasePolicy<Poco::Runnable> >) (Thread_POSIX.cpp:206)
==1255==    by 0x8A2BBF: Poco::Thread::start(Poco::Runnable&) (Thread.cpp:129)
==1255==    by 0x8A58D6: Poco::PooledThread::start() (ThreadPool.cpp:85)
==1255==    by 0x8A6299: Poco::ThreadPool::ThreadPool(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, int, int, int, int) (ThreadPool.cpp:276)
==1255==    by 0x8A771E: Poco::ThreadPoolSingletonHolder::pool() (ThreadPool.cpp:502)
==1255==    by 0x8A730C: Poco::ThreadPool::defaultPool() (ThreadPool.cpp:523)
==1255==    by 0x8A9B9C: Poco::Timer::start(Poco::AbstractTimerCallback const&) (Timer.cpp:49)
==1255==    by 0x73C04B: Poco::Data::SessionPool::SessionPool(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, int, int, int, int) (SessionPool.cpp:37)
==1255==    by 0x230974: BlogRestServerApp::initialize(Poco::Util::Application&) (blog_rest.cpp:204)
==1255==
==1255== LEAK SUMMARY:
==1255==    definitely lost: 144 bytes in 1 blocks
==1255==    indirectly lost: 0 bytes in 0 blocks
==1255==      possibly lost: 1,216 bytes in 4 blocks
==1255==    still reachable: 787,705 bytes in 8,072 blocks
==1255==         suppressed: 0 bytes in 0 blocks
==1255== Reachable blocks (those to which a pointer was found) are not shown.
==1255== To see them, rerun with: --leak-check=full --show-leak-kinds=all
==1255==
==1255== For lists of detected and suppressed errors, rerun with: -s
==1255== ERROR SUMMARY: 4 errors from 4 contexts (suppressed: 0 from 0)

