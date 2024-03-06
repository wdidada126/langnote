# asio

1、asio有独立版本，不需要boost，我一直都用独立版本；2、asio已经进不了标准库了。

其实C++里面功能强大的网络库有很多，asio
这和C++的用户生态有关。1、C++用户很多人不仅仅会调库而且会写库；
2、C++的玩家不喜欢臃肿的全家桶，所以那些所谓的大框架在C++里面并不受欢迎。
qt
opencv

https://think-async.com/Asio/
？

有两个版本，一个依赖boost
一个不依赖boost

https://think-async.com/Asio/asio-1.28.0/doc/

https://think-async.com/Asio/asio-1.28.0/doc/asio/reference.html

https://github.com/chriskohlhoff/asio/

## github action编译

Asio is a header-only library.

Asio库是一个跨平台的C++网络库，它是Boost库的一部分，主要用于实现异步I/O操作。以下是Asio库的主要功能：
1. 异步I/O操作：Asio库提供了一组异步的I/O操作，包括TCP和UDP的socket、定时器、串口等。它使用异步模式，使得应用程序可以在等待I/O操作完成时执行其他任务，提高了程序的效率和响应性。
2. 事件循环：Asio的核心是一个事件循环，它使用epoll、kqueue、IOCP等系统调用来实现异步I/O操作。通过事件循环，Asio可以监听多个I/O事件，并对其进行统一的处理和管理。
3. 多线程支持：Asio库并不要求使用多线程和锁，有效地避免了多线程编程带来的诸多有害副作用（如条件竞争、死锁等)。它通过异步模式实现多线程的并发操作，避免了线程间的同步问题。
4. 定时器：Asio库提供了一个定时器类，可以用于在指定的时间间隔内触发事件或执行任务。这使得应用程序可以在指定的时间间隔内进行任务调度或监控系统的状态。
5. 串口通信：Asio库还提供了对串口通信的支持，可以用于读取和写入串口数据。这使得应用程序可以通过串口与其他设备或硬件进行通信。

总的来说，Asio库是一个功能强大且灵活的C++网络库，它提供了异步I/O操作、事件循环、多线程支持、定时器和串口通信等功能，使得应用程序可以更加高效地处理网络和I/O操作。

head only，不需要编译
也可以用
./configure

## 更新情况
https://think-async.com/Asio/asio-1.28.0/doc/asio/history.html


## 库
### 版本 version
1.28.0

### conan
#### conan2

class io_context

### vcpkg
### cmake 