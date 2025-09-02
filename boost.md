# boost

https://www.boost.org/doc/libs/1_75_0/doc/html/

https://live.boost.org/doc/libs/1_75_0/doc/html/boost_asio/examples/cpp03_examples.html

如果仅仅是构建http message的话, boos/beast有比较好的抽象, 可以单独使用

要在Ubuntu 20上安装特定版本的libboost-dev（例如1.65版本），你可以考虑使用第三方APT源，因为Ubuntu官方仓库可能不提供旧版本。以下是一些推荐的第三方APT源：

阿里云开源镜像站：阿里云提供了广泛的开源软件镜像，包括Boost。你可以尝试添加阿里云的源到你的系统中。
清华大学开源软件镜像站：清华大学也提供了许多开源软件的镜像，包括Boost。
中科大开源镜像站：中国科学技术大学开源软件镜像站也是一个可靠的选择。
添加这些源之后，你可以使用类似以下的命令来安装特定版本的libboost-dev：

```bash
sudo apt-get update  
sudo apt-get install libboost-dev=1.65.1-1
```
请注意，你需要将上述命令中的版本号替换为你想要安装的确切版本。此外，由于使用第三方源可能会带来一些风险，如软件包的完整性和安全性，建议在使用之前仔细检查和验证源的可靠性。

支持Aix平台

模板
元编程

boost.test
https://blog.csdn.net/Betterc5/article/details/86291109

https://blog.csdn.net/weixin_33656634/article/details/86133362

Boost库系列：基于boost::asio的http、https serve实现方式总结

https://www.boost.org/doc/libs/1_67_0/doc/html/boost_asio/examples/cpp03_examples.html

1、http::server，简单的单线程服务器，只有一个主线程；
2、 http::server2  多个io_contex响应socket连接
3、 http::server3 一个io_context多个线程run()
4、 http::server4 单线程的协程

  boost.x86_64 0:1.53.0-28.el7                                          
  boost-atomic.x86_64 0:1.53.0-28.el7                                   
  boost-chrono.x86_64 0:1.53.0-28.el7                                   
  boost-context.x86_64 0:1.53.0-28.el7                                  
  boost-filesystem.x86_64 0:1.53.0-28.el7                               
  boost-graph.x86_64 0:1.53.0-28.el7                                    
  boost-iostreams.x86_64 0:1.53.0-28.el7                                
  boost-locale.x86_64 0:1.53.0-28.el7                                   
  boost-math.x86_64 0:1.53.0-28.el7                                     
  boost-program-options.x86_64 0:1.53.0-28.el7                          
  boost-python.x86_64 0:1.53.0-28.el7                                   
  boost-random.x86_64 0:1.53.0-28.el7                                   
  boost-regex.x86_64 0:1.53.0-28.el7                                    
  boost-serialization.x86_64 0:1.53.0-28.el7                            
  boost-signals.x86_64 0:1.53.0-28.el7                                  
  boost-test.x86_64 0:1.53.0-28.el7                                     
  boost-timer.x86_64 0:1.53.0-28.el7                                    
  boost-wave.x86_64 0:1.53.0-28.el7                                     

## boost版本
1.71
1.53
1.66

## ubuntu 20 gcc9编译boost 1.65失败

```shell
gcc.compile.c++ bin.v2/libs/python/build/gcc-9/release/threading-multi/converter/builtin_converters.o
libs/python/src/converter/builtin_converters.cpp: In function ‘void* boost::python::converter::{anonymous}::convert_to_cstring(PyObject*)’:
libs/python/src/converter/builtin_converters.cpp:51:35: error: invalid conversion from ‘const void*’ to ‘void*’ [-fpermissive]
   51 |       return PyUnicode_Check(obj) ? _PyUnicode_AsString(obj) : 0;

    "g++"   -O3 -finline-functions -Wno-inline -Wall -pthread -fPIC -m64  -DBOOST_ALL_NO_LIB=1 -DBOOST_PYTHON_SOURCE -DNDEBUG  -I"." -I"/usr/include/python3.8" -c -o "bin.v2/libs/python/build/gcc-9/release/threading-multi/converter/builtin_converters.o" "libs/python/src/converter/builtin_converters.cpp"

...failed gcc.compile.c++ bin.v2/libs/python/build/gcc-9/release/threading-multi/converter/builtin_converters.o...
```

b2 工具是 Boost C++ 库的构建工具，它是 Boost 库的一部分。Boost 是一个广泛使用的 C++ 库集合，提供了许多功能强大且经过广泛测试的组件，涵盖了从基本工具到高级功能的各个领域。

b2 工具主要用于构建和安装 Boost 库。它提供了一种简单而灵活的方式来配置、构建和安装 Boost 库，使开发人员能够轻松集成 Boost 到自己的项目中。

以下是 b2 工具的一些主要功能：

1. 构建 Boost 库：b2 工具可以根据你的需求构建特定的 Boost 库。你可以选择要构建的库组件、库类型（静态库或共享库）、目标平台和编译器等配置选项。b2 工具会自动处理依赖关系，并根据你的配置生成所需的库文件。
2. 安装 Boost 库：b2 工具可以将构建好的 Boost 库安装到指定位置，以便你的项目可以使用这些库。安装过程会将库文件和相关的头文件复制到指定的目录中，并生成相应的构建配置文件，以便你的项目可以正确地链接和使用 Boost 库。
3. 自定义配置：b2 工具提供了丰富的配置选项，可以根据你的需求进行自定义配置。你可以指定编译器选项、目标平台、库的版本、调试选项等。
4. 构建变体：b2 工具支持构建不同的 Boost 库变体，如调试版本和发布版本、动态链接库和静态库等。你可以根据需要选择所需的构建变体，以满足特定的项目需求。
5. 依赖管理：b2 工具可以自动处理 Boost 库的依赖关系。当你选择构建特定的 Boost 库时，b2 工具会自动处理该库所依赖的其他 Boost 组件，并确保它们被正确构建和链接。

总之，b2 工具是 Boost C++ 库的构建工具，它简化了 Boost 库的配置、构建和安装过程，使开发人员能够轻松地集成 Boost 库到他们的 C++ 项目中。

希望这个解答能够帮助你理解 b2 工具的作用。如有任何进一步的问题，请随时提问！

## 源代码安装

zip/gz格式代码下载

https://www.boost.org/doc/libs/1_65_0/doc/html/bbv2.html#bbv2.installation

https://www.baeldung.com/linux/boost-install-on-ubuntu

https://www.boost.org/users/history/version_1_65_0.html

https://boostorg.jfrog.io/ui/packages

## io_context
你提到的这句话非常精准：

> “多线程模型设计很糟糕（优秀的参考 asio 的 `io_context`，可轻松使用不同多线程模型，如：`multithread/context`、`onethread/context`、`multithread/multicontext`）”

这正是现代高性能网络编程的核心思想。下面我们来深入详解 Boost.Asio 的 `io_context` 概念，并通过代码示例展示它如何支持多种多线程模型。

#  Boost.Asio 的 `io_context` 概念详解

## 一、什么是 `io_context`？

`io_context` 是 Boost.Asio 库的核心调度器（I/O Scheduler），它是所有异步操作的“中枢神经”。

###  核心职责：
- 管理 I/O 事件循环（Event Loop）
- 调度 异步操作（如 async_read, async_write）
- 分发 完成处理器（Completion Handlers）
- 绑定 I/O 对象（如 `tcp::socket`, `timer`）

>  可以把 `io_context` 理解为：
> - Linux 下的 epoll / io_uring 事件循环封装
> - Windows 下的 IOCP（I/O Completion Ports）调度器
> - 类似 Node.js 的 event loop

---

## 二、`io_context` 的基本结构

```cpp
#include <boost/asio.hpp>
using boost::asio::io_context;

int main() {
    boost::asio::io_context io;  // 创建一个 io_context

    // 所有异步操作都绑定到这个 io 上
    // io.run();  // 启动事件循环
}
```

---

## 三、`io_context` 支持的多线程模型

Asio 的强大之处在于：同一个 `io_context` 可以灵活适配多种线程模型，无需修改业务逻辑。

| 模型 | 描述 | 适用场景 |
|------|------|---------|
|  Single Thread / Single Context | 一个线程运行 `io_context::run()` | 简单服务、低并发 |
|  Multi Thread / Single Context | 多个线程调用同一个 `io_context::run()` | 高并发、负载均衡 |
|  Multi Thread / Multi Context | 每个线程有自己的 `io_context` | CPU 绑核、极致性能 |

下面我们逐一用代码说明。

---

##  模型 1：Single Thread / Single Context（单线程模型）

一个线程运行一个 `io_context`，所有 I/O 和回调都在该线程执行。

```cpp
#include <boost/asio.hpp>
#include <iostream>
#include <thread>

int main() {
    boost::asio::io_context io;

    // 添加一个定时器异步操作
    boost::asio::steady_timer timer(io, std::chrono::seconds(1));
    timer.async_wait([](const boost::system::error_code& ec) {
        std::cout << "[Thread " << std::this_thread::get_id() 
                  << "] Timer expired!" << std::endl;
    });

    std::cout << "[Main] Starting io_context in single thread..." << std::endl;
    io.run();  // 阻塞，直到所有任务完成

    std::cout << "io_context stopped." << std::endl;
    return 0;
}
```

>  所有回调都在主线程执行，线程安全简单，但吞吐量受限。


##  模型 2：Multi Thread / Single Context（多线程共享一个 io_context）

多个工作线程调用同一个 `io_context::run()`，Asio 自动在这些线程中分发事件和回调。

这是最常用的高性能模型。

```cpp
#include <boost/asio.hpp>
#include <iostream>
#include <thread>
#include <vector>

int main() {
    boost::asio::io_context io;
    boost::asio::executor_work_guard<boost::asio::io_context::executor_type> 
        work(io.get_executor());  // 防止 io.run() 立即退出

    // 启动多个定时器（模拟异步任务）
    for (int i = 0; i < 10; ++i) {
        boost::asio::steady_timer* timer = new boost::asio::steady_timer(
            io, std::chrono::milliseconds(100 * (i + 1))
        );
        timer->async_wait([i](const boost::system::error_code&) {
            std::cout << "[Thread " << std::this_thread::get_id()
                      << "] Task " << i << " completed." << std::endl;
            delete timer;
        });
    }

    // 创建多个线程运行同一个 io_context
    std::vector<std::thread> threads;
    int thread_count = 4;
    for (int i = 0; i < thread_count; ++i) {
        threads.emplace_back([&io]() {
            std::cout << "[Worker] Thread " << std::this_thread::get_id() 
                      << " started." << std::endl;
            io.run();
            std::cout << "[Worker] Thread " << std::this_thread::get_id() 
                      << " stopped." << std::endl;
        });
    }

    // 等待所有线程结束
    for (auto& t : threads) {
        t.join();
    }

    return 0;
}
```

###  优势：
- 自动负载均衡：Asio 内部使用线程安全队列分发回调
- 高效：避免线程频繁创建/销毁
- 简单：开发者无需手动同步

###  注意：
- 回调可能在任意一个调用 `io.run()` 的线程中执行，所以共享数据必须加锁。

##  模型 3：Multi Thread / Multi Context（每个线程独立 io_context）
每个线程拥有自己的 `io_context`，通常用于CPU绑核（CPU Affinity） 或极致性能优化。

```cpp
#include <boost/asio.hpp>
#include <iostream>
#include <thread>
#include <vector>

void worker_thread(int id) {
    boost::asio::io_context io;
    boost::asio::executor_work_guard<boost::asio::io_context::executor_type> 
        work(io.get_executor());

    // 每个线程创建自己的定时器
    boost::asio::steady_timer timer(io, std::chrono::seconds(2));
    timer.async_wait([id](const boost::system::error_code&) {
        std::cout << "[Thread " << id << "] Dedicated io_context task done."
                  << std::endl;
    });

    std::cout << "[Thread " << id << "] Starting dedicated io_context..." << std::endl;
    io.run();
}

int main() {
    std::vector<std::thread> threads;
    int num_threads = 3;

    for (int i = 0; i < num_threads; ++i) {
        threads.emplace_back(worker_thread, i);
    }

    for (auto& t : threads) {
        t.join();
    }

    return 0;
}
```

###  优势：
- 无锁设计：每个线程独立，避免上下文切换和锁竞争
- 可绑定 CPU 核心：适合高性能服务器、DPDK 类应用
- 隔离性好：一个线程崩溃不影响其他

###  适用场景：
- 高频交易系统
- 游戏服务器
- 网络协议栈优化

##  `io_context` 的核心机制

### 1. Proactor 模式
Asio 使用 Proactor 模式（而非 Reactor）：
- 异步发起 I/O 操作
- 操作完成后，系统通知 Asio
- Asio 调用用户提供的回调函数（Completion Handler）

### 2. Completion Handler 的执行
- 回调不是在 I/O 完成的“系统线程”中执行
- 而是被放入 `io_context` 的任务队列，由调用 `io.run()` 的线程执行

### 3. 线程安全
- `io_context::post()` 和 `dispatch()` 是线程安全的
- 可以从任意线程向 `io_context` 投递任务：

```cpp
io.post([]() { std::cout << "This runs in io_context thread"; });
```

##  总结：Asio 的设计哲学

| 特性 | 说明 |
|------|------|
| 解耦 I/O 与线程模型 | `io_context` 是抽象调度器，不绑定线程数 |
| 灵活适配 | 同一套代码可运行在单线程、多线程、多 context 模型下 |
| 高性能 | 基于操作系统原生异步 I/O（epoll, kqueue, IOCP） |
| 可扩展 | 支持自定义 Executor、Strand（线程安全序列化） |

##  为什么说“多线程模型设计很糟糕”？

很多传统网络库（如原始的pthread + socket）：
- 线程模型硬编码（如“一个连接一个线程”）
- 难以扩展
- 容易死锁、资源浪费

而 Asio 的 `io_context`：
- 让开发者专注于业务逻辑
- 线程模型由部署决定，而非代码决定
- 轻松切换模型，无需重写

>  这就是“优秀的多线程模型设计”。

##  推荐学习资源

- 官方文档：[https://www.boost.org/doc/libs/release/libs/asio/](https://www.boost.org/doc/libs/release/libs/asio/)
- 书籍：《Boost.Asio C++ Network Programming》
- 示例代码：[Boost.Asio Examples](https://github.com/boostorg/asio/tree/develop/example)


掌握 `io_context`，你就掌握了现代 C++ 高性能网络编程的“心脏”。
