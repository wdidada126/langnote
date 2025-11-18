# muduo
https://github.com/vbhsjd/mymuduo
看我改的全用c++,不用boost

先导课程
https://github.com/yuesong-feng/30dayMakeCppServer

export BUILD_TYPE=Debug

https://github.com/chenshuo/muduo-tutorial

知乎网友评价muduo

当然差，虽然使用了一些c++的新东西，如function取代虚函数之外，其实不如ace，因为设计有问题，随便说说吧
比如用户无法感知队头阻塞（收发窗口）而可能会导致爆内存，所以有一定使用场景限制；
比如复制用户数据到库内部，比如使用LT而不是ET（这个不算什么大问题，只是使用ET较为主流）；
比如多线程模型设计很糟糕（优秀的参考asio的io_contex，可轻松使用不同多线程模型，如以下组合：multithreads/contex, onethread/contex, mutlithreads/multicontex）；
比如使用reactor模型也是一个败笔，很难转换成现代协程模型。
代码水平写的也一般吧，不是很规范较为随意，好代码会像混然天成一样，风格错落有致，极为规范，国外那些优秀的开源项目基本都如此，差的很少。

Boost.Asio 的 io_context 是其异步操作的核心，它负责处理所有 I/O 事件和任务调度。你提到的几种多线程模型，本质上都是围绕如何运行 io_context::run() 来组织的。下面我将用一个表格概括这几种模型的核心思想，并提供相应的代码示例。

模型名称 核心思想 优点 缺点 适用场景

单线程单 io_context 单个线程运行一个 io_context，所有操作都在该线程中完成。 简单，无需考虑线程安全。 无法利用多核，性能受限。 连接数少、任务轻量的场景。

多线程单 io_context 多个线程共同运行同一个 io_context。 实现相对简单，能利用多核处理 I/O 事件。 回调可能在任何线程触发，必须用 strand 等手段保证线程安全。 I/O 密集型任务，且回调处理逻辑本身不重。

多线程多 io_context 每个线程运行自己独立的 io_context，连接可以均匀分配到不同的 io_context。 连接级的线程安全（同一连接的回调总在同一线程），性能高。 不同 io_context 上的连接若需交互，仍需额外线程同步。 高性能服务器，需要良好利用多核且连接间交互较少。

混合模式 (你的组合需求) 例如，用一个专用 io_context 处理接受连接，用一个 io_context 池处理 I/O。 灵活，可根据任务类型选择最优模型。 设计和实现更复杂。 复杂的高并发应用，不同任务有不同特性。

下面我们来看各种模型的代码实现。

1. 单线程单 io_context (Onethread/Contex)

这是最基础的模型，所有操作都在一个线程中完成。
#include <boost/asio.hpp>
#include <iostream>

int main() {
    boost::asio::io_context io_context;

    // 创建一个定时器，模拟异步操作
    boost::asio::steady_timer timer(io_context, std::chrono::seconds(1));
    timer.async_wait([](const boost::system::error_code& ec) {
        if (!ec) {
            std::cout << "Timer expired! Thread ID: " 
                      << std::this_thread::get_id() << std::endl;
        }
    });

    // 单线程运行事件循环
    std::cout << "Main Thread ID: " << std::this_thread::get_id() << std::endl;
    io_context.run(); // 会阻塞，直到所有异步操作完成且没有更多工作

    return 0;
}

输出示例：

Main Thread ID: 0x7f7a8c2d5740
Timer expired! Thread ID: 0x7f7a8c2d5740

注意：所有回调都在同一个主线程中执行。

2. 多线程单 io_context (Multithreads/One Contex)

多个线程共同调用同一个 io_context 的 run() 方法。
#include <boost/asio.hpp>
#include <iostream>
#include <vector>
#include <thread>

int main() {
    boost::asio::io_context io_context;
    
    // 使用 work_guard 防止 io_context 在没有待处理事件时退出
    auto work_guard = std::make_unique<boost::asio::executor_work_guard<boost::asio::io_context::executor_type>>(io_context.get_executor());

    // 创建多个定时器，模拟多个异步操作
    for (int i = 0; i < 3; ++i) {
        auto timer = std::make_shared<boost::asio::steady_timer>(io_context, std::chrono::seconds(1 + i));
        timer->async_wait([i, timer](const boost::system::error_code& ec) {
            if (!ec) {
                std::cout << "Timer " << i << " expired! Thread ID: " 
                          << std::this_thread::get_id() << std::endl;
            }
        });
    }

    // 创建线程池并运行 io_context
    std::vector<std::thread> threads;
    int num_threads = 4; // 线程数通常设置为CPU核数
    for (int i = 0; i < num_threads; ++i) {
        threads.emplace_back([&io_context]() {
            std::cout << "Thread " << std::this_thread::get_id() << " started running io_context." << std::endl;
            io_context.run();
            std::cout << "Thread " << std::this_thread::get_id() << " finished running io_context." << std::endl;
        });
    }

    // 等待所有线程完成（在实际服务器中，可能长期运行，这里为了演示）
    std::this_thread::sleep_for(std::chrono::seconds(5));
    work_guard.reset(); // 允许 io_context 退出
    io_context.stop(); // 通知所有线程停止

    for (auto& t : threads) {
        if (t.joinable()) t.join();
    }

    return 0;
}

输出示例（线程ID每次运行都不同）：

Thread 0x7f7a8c2d5740 started running io_context.
Thread 0x7f7a8c1d4700 started running io_context.
Thread 0x7f7a8c0d3700 started running io_context.
Thread 0x7f7a8bfd2700 started running io_context.
Timer 0 expired! Thread ID: 0x7f7a8c2d5740
Timer 1 expired! Thread ID: 0x7f7a8c1d4700
Timer 2 expired! Thread ID: 0x7f7a8c0d3700
... (等待5秒)
Thread 0x7f7a8c2d5740 finished running io_context.
...

注意：回调函数可能被任何一个运行 io_context.run() 的线程执行，这意味着对共享数据的访问需要额外的同步措施（如互斥锁或 strand）。

3. 多线程多 io_context (Multithreads/Multicontex) - IOServicePool

每个线程都有自己的 io_context，形成一个 io_context 池。新连接可以以轮询或其他策略分配到不同的 io_context 上。
#include <boost/asio.hpp>
#include <iostream>
#include <vector>
#include <thread>
#include <atomic>

class IOServicePool {
public:
    using IOService = boost::asio::io_context;
    using WorkGuard = boost::asio::executor_work_guard<IOService::executor_type>;
    using WorkGuardPtr = std::unique_ptr<WorkGuard>;

    explicit IOServicePool(std::size_t pool_size = std::thread::hardware_concurrency())
        : next_io_service_(0) {
        if (pool_size == 0) pool_size = 1;
        
        work_guards_.reserve(pool_size);
        for (std::size_t i = 0; i < pool_size; ++i) {
            io_services_.emplace_back();
            work_guards_.push_back(std::make_unique<WorkGuard>(io_services_.back().get_executor()));
        }
    }

    void run() {
        threads_.reserve(io_services_.size());
        for (std::size_t i = 0; i < io_services_.size(); ++i) {
            threads_.emplace_back([this, i]() {
                std::cout << "Thread " << std::this_thread::get_id() 
                          << " running io_service " << i << std::endl;
                io_services_[i].run();
                std::cout << "Thread " << std::this_thread::get_id() 
                          << " finished io_service " << i << std::endl;
            });
        }
    }

    void stop() {
        for (auto& work_guard : work_guards_) {
            work_guard.reset();
        }
        for (auto& io_service : io_services_) {
            io_service.stop();
        }
        for (auto& t : threads_) {
            if (t.joinable()) t.join();
        }
    }

    boost::asio::io_context& get_io_service() {
        auto& service = io_services_[next_io_service_++];
        if (next_io_service_ >= io_services_.size()) {
            next_io_service_ = 0;
        }
        return service;
    }

private:
    std::vector<IOService> io_services_;
    std::vector<WorkGuardPtr> work_guards_;
    std::vector<std::thread> threads_;
    std::atomic<std::size_t> next_io_service_;
};

int main() {
    try {
        IOServicePool pool(4); // 创建一个包含4个io_context的池

        // 模拟多个异步操作分配到不同的io_context
        for (int i = 0; i < 8; ++i) {
            auto& io_context = pool.get_io_service(); // 轮询获取io_context
            auto timer = std::make_shared<boost::asio::steady_timer>(io_context, std::chrono::seconds(1 + i % 3));
            timer->async_wait([i, timer](const boost::system::error_code& ec) {
                if (!ec) {
                    std::cout << "Timer " << i << " expired! Thread ID: " 
                              << std::this_thread::get_id() << std::endl;
                }
            });
        }

        pool.run(); // 启动所有线程运行各自的io_context

        std::cout << "Press Enter to exit..." << std::endl;
        std::cin.get();

        pool.stop();
    } catch (const std::exception& e) {
        std::cerr << "Exception: " << e.what() << std::endl;
    }
    return 0;
}

输出示例：

Thread 0x7f7a8c2d5740 running io_service 0
Thread 0x7f7a8c1d4700 running io_service 1
Thread 0x7f7a8c0d3700 running io_service 2
Thread 0x7f7a8bfd2700 running io_service 3
Timer 0 expired! Thread ID: 0x7f7a8c2d5740 // 属于io_service 0
Timer 1 expired! Thread ID: 0x7f7a8c1d4700 // 属于io_service 1
Timer 2 expired! Thread ID: 0x7f7a8c0d3700 // 属于io_service 2
Timer 3 expired! Thread ID: 0x7f7a8bfd2700 // 属于io_service 3
Timer 4 expired! Thread ID: 0x7f7a8c2d5740 // 再次轮到io_service 0
...
Press Enter to exit...

注意：每个 io_context 都在其自己专属的线程中运行。分配给同一个 io_context 的所有异步操作的回调都会在同一个线程中被执行，这在连接级别提供了线程安全性。

4. 使用 strand 保证线程安全

在多线程单 io_context 模型中，必须使用 strand 来确保特定操作的顺序执行和线程安全。
#include <boost/asio.hpp>
#include <iostream>
#include <vector>
#include <thread>

int main() {
    boost::asio::io_context io_context;
    auto work_guard = std::make_unique<boost::asio::executor_work_guard<boost::asio::io_context::executor_type>>(io_context.get_executor());

    // 创建一个 strand
    boost::asio::strand<boost::asio::io_context::executor_type> my_strand(io_context.get_executor());

    // 模拟需要线程安全的共享资源
    int shared_counter = 0;

    // 启动多个异步操作，它们都通过 strand 来访问共享资源
    for (int i = 0; i < 5; ++i) {
        // 使用 post 通过 strand 提交任务
        boost::asio::post(my_strand, [i, &shared_counter]() {
            std::cout << "Task " << i << " (via post) is modifying shared_counter on Thread: " 
                      << std::this_thread::get_id() << std::endl;
            shared_counter += i;
            std::cout << "shared_counter is now: " << shared_counter << std::endl;
        });

        // 或者在异步操作中直接绑定 strand (更常见于socket async_read/async_write)
        auto timer = std::make_shared<boost::asio::steady_timer>(io_context, std::chrono::milliseconds(100 * i));
        timer->async_wait(boost::asio::bind_executor(my_strand, [i, timer, &shared_counter](const boost::system::error_code& ec) {
            if (!ec) {
                std::cout << "Timer " << i << " (via bind_executor) is modifying shared_counter on Thread: " 
                          << std::this_thread::get_id() << std::endl;
                shared_counter -= 1;
                std::cout << "shared_counter is now: " << shared_counter << std::endl;
            }
        }));
    }

    // 运行 io_context 的多线程
    std::vector<std::thread> threads;
    for (int i = 0; i < 2; ++i) {
        threads.emplace_back([&io_context]() { io_context.run(); });
    }

    std::this_thread::sleep_for(std::chrono::seconds(2));
    work_guard.reset();
    io_context.stop();

    for (auto& t : threads) {
        t.join();
    }

    std::cout << "Final shared_counter: " << shared_counter << std::endl;
    return 0;
}

输出示例：

Task 0 (via post) is modifying shared_counter on Thread: 0x7f7a8c2d5740
shared_counter is now: 0
Task 1 (via post) is modifying shared_counter on Thread: 0x7f7a8c2d5740
shared_counter is now: 1
Timer 0 (via bind_executor) is modifying shared_counter on Thread: 0x7f7a8c2d5740
shared_counter is now: 0
Task 2 (via post) is modifying shared_counter on Thread: 0x7f7a8c2d5740
shared_counter is now: 2
Timer 1 (via bind_executor) is modifying shared_counter on Thread: 0x7f7a8c2d5740
shared_counter is now: 1
...
Final shared_counter: -5

注意：所有通过 my_strand 提交或绑定的任务，即使 io_context 有多个线程在运行，这些任务也会被串行化执行，从而安全地访问 shared_counter，无需额外的互斥锁。

5. 混合模式示例（接受连接与I/O处理分离）

这是一种常见的高性能服务器模式，使用独立的 io_context 分别处理连接接受和连接上的数据I/O。
#include <boost/asio.hpp>
#include <iostream>
#include <thread>
#include <vector>

int main() {
    try {
        // 1. 一个专门的 io_context 用于接受连接 (通常单线程就够了)
        boost::asio::io_context accept_io_context;
        boost::asio::executor_work_guard<boost::asio::io_context::executor_type> accept_work_guard(accept_io_context.get_executor());

        // 2. 一个 io_context 池用于处理所有连接的 I/O 操作 (多线程)
        IOServicePool io_pool(4); // 使用前面定义的 IOServicePool

        // ... 这里需要设置 acceptor，绑定端口等 ...
        // boost::asio::ip::tcp::acceptor acceptor(accept_io_context, endpoint);
        // void start_accept() {
        //     auto& io_service_for_connection = io_pool.get_io_service(); // 从池中取一个io_context给新连接
        //     auto new_session = std::make_shared<Session>(io_service_for_connection, ...);
        //     acceptor.async_accept(new_session->socket(), [this, new_session](...) { ... });
        // }

        // 3. 启动线程运行 accept_io_context
        std::thread accept_thread([&accept_io_context]() {
            std::cout << "Accept thread started: " << std::this_thread::get_id() << std::endl;
            accept_io_context.run();
            std::cout << "Accept thread finished." << std::endl;
        });

        // 4. 启动线程池运行 I/O io_contexts
        io_pool.run();

        std::cout << "Server started. Press Enter to stop..." << std::endl;
        std::cin.get();

        // 5. 优雅停止
        accept_io_context.stop();
        accept_work_guard.reset();
        io_pool.stop();
        accept_thread.join();

    } catch (const std::exception& e) {
        std::cerr << "Exception: " << e.what() << std::endl;
    }
    return 0;
}

这种架构将接受连接的负担与处理连接数据I/O的负担分离，允许更精细的资源控制和更好的性能。
核心建议
1.  简单应用：从单线程单 io_context 开始。
2.  I/O 密集型：使用多线程单 io_context，并务必为所有共享数据使用 strand 或其他同步机制。
3.  高性能、高并发：使用多线程多 io_context (IOServicePool)，这通常能提供更好的性能，因为减少了线程间的竞争。
4.  复杂应用：考虑混合模式，例如用单独的 io_context 处理接受连接和信号，用池处理连接I/O。
5.  始终注意线程安全：明确每个回调函数在哪个线程中执行，并对共享数据采取适当的保护措施。
6.  优雅关闭：使用 work_guard 防止 io_context 意外退出，并通过 signal_set 捕获信号（如 SIGINT, SIGTERM）来实现优雅关闭。

希望这些详细的解释和代码示例能帮助你更好地设计和实现基于 Boost.Asio 的多线程网络应用。


有tag

ubuntu 20有编译

cmake组织
依赖boost probobuf

https://www.zhihu.com/question/24590359/answer/34834484

补充说明一下我对那位水木网友的看法的看法，我认为他关于timer的批判是站得住脚的---如果他说的属实的话，关于signal 的看法有待商榷，实屏蔽大部分signal（只留一个做启停）是实践上很实用的做法，一般也不特别需要网络框架去处理。
-------------------------------这是那位水木网友的文章：  hurricanelee (风的影子) 于  (Tue Sep 25 13:57:06 2012)  提到:muduo适用于什么环境？muduo的官方一句话自我介绍是：A C++ non-blocking multi-threaded networklibrary for Linux。在其readme和wiki中均未提及此lib是否适用于实际场景，于是我花了些时间翻看了一下，得出的结论是此lib仅限于展示epoll/poll的基本用法，对网络编程初学者是否有参考价值还有待进一步考察。任何一个网络产品除了要支持网络event之外，还必须处理另外两种事件：signal和timer。muduo也毫无例外。但近看一下就发现muduo对single和timer的支持很有喜感。除了SIGPIPE被mask之外，muduo没有接管signal。当然muduo这么做是有借口的，反正有signalfd嘛。在此我想问问各位做网络应用的同学，在你的实际项目中，不用POSIX的signal接口而用signalfd的，有几个？而如果是从编程初学者教育的角度来看，是介绍POSIX重要，还是介绍2.6.22引入的一个new feature重要？而抛弃signal的处理之后，muduo自然轻松了许多，还顺带可以说一句：muduo支持高级特性signalfd。--嗯，听起来很高级，不过signalfd不是muduo支持的，而是kernel支持的。一个网络编程库，timer是重中之重，比到底是用epoll还是select都重要。当然，话说回来，再吊的库无非也就是个heap为本的数据结构在支持，无非是有些库喜欢说自己的heap实现比别人都高效，比如haproxy。但muduo却独辟蹊径，用timerfd，泥玛又是一个高级特性啊，很唬人的。由kernel帮你管理timer，是不是很吊。不仅采用了timerfd，muduo还采用了set来保存event，每个big loop里要查超时的时候，再iterate一遍这个set。再然后，每次加一个timer，就要冒着一次settime的syscall的风险--这还不够，还得要一次gettimeofday。别不把syscall当不要钱的可以吗？你也许可以跑10万个连接，但你敢加上超时的特性吗？muduo如果有做过细致的benchmark就会知道，一个loop里最花时间的就是timer的处理。关于muduo的timer处理，槽点太多，我就不一一细述了。回头看看timer，很显然不适合工业应用，而给初学者做参考。嗯，负面参考价值很大。嗯，今天先说这么多吧。吐槽点还很多，比如那个全功能的http范例，比如对pthread/fork的支持，比如对内存的使用等等等等。都要一一吐过也不是不可以，不过就要耐下性子来慢慢写就是。

别的不多说，gettimeofday在64位linux上不是系统调用了
在 x86-64 平台上,gettimeofday 不是系统调用,而是在用户态实现的(搜
vsyscall),没有上下文切换和陷入内核的开销。
喷 signalfd 和 timerfd 站不住脚，内核提供新的接口显然是让人用的。如果内核比较老或者不用 linux，那大可不必使用 muduo。就像写 win10 的应用程序不必兼容 xp 一样。

1、std::set内部使用的红黑树
2、至于用不用timerfd，引用下stackoverflow上的回答：
When you use timerfd, it takes 3 system calls (timerfd_create(), timerfd_settime() and epoll_ctl()) just to create a timer.
And every time it expires you need to read() from that file descriptor.
timerfd could be useful for applications without an event loop, but for ones that already use a decent event loop it is pretty much useless.

看到timer比epoll或者select更重要我就不想往下看了

自己项目用timerfd还是很爽的，但是作为通用库，兼容性也是非常重要的。
libuv的timer也是红黑树实现，不过只是在windows上，Linux下还是最小堆
可试试corelooper，没有这些问题
大哥人家timer的做法有什么不对的吗？nginx也是用set管理timer的，你黑别人之前也要了解一下好吗？
nginx 又不是天王老子，nginx 做得就一定是对的？你只要手工管理过超时器，一定知道为什么有必要用优先队列或者最小堆。而且这又不是我说的，而且我也不能确定你关于 nginx 的说法对不对。

## muduo依赖
boost
protoc

## muduo安装
https://github.com/chenshuo/muduo

```shell

git clone https://github.com/chenshuo/muduo.git
sudo apt update
sudo apt install libboost-all-dev -y
sudo apt install protobuf-compiler -y
export Boost_INCLUDE_DIR=/usr/include
cd muduo
chmod +x ./build.sh
./build.sh
```

## api
