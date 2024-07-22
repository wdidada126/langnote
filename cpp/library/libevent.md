# libevent
an event notification library

## 官方文档
https://libevent.org/doc

## 参考书籍
Linux高性能服务器编程 游双

## 源代码
https://libevent.org/

eventop结构体
event_base结构体

libevent
ubuntu20上面有项目

创建httpserver 

libevent项目源码可以在GitHub上找到，地址为：https://github.com/libevent/libevent

https://gitee.com/edidada/libevent_test
https://github.com/downloads/libevent/libevent/libevent-2.0.20-stable.tar.gz

### sample例子 example
https://github.com/libevent/libevent/tree/master/sample

### cmake 构建 autoconf（截止2.2）

```cmake
git clone https://github.com/libevent/libevent.git
cd libevent
git checkout release-2.1.12-stable
mkdir build && cd build
cmake ..
make
sudo make install
make verify
```

```shell
./configure
make
make verify   # (optional)
sudo make install
```

### 例子模块
dns
http
rpc

跟brpc好像

## 版本历史
libevent-2.1.12-stable.tar.gz [GPG Sig] ChangeLog
PR
Released 2020-07-05

libevent-2.1.11-stable.tar.gz [GPG Sig] ChangeLog
Released 2019-08-01 (ABI changed)
libevent-2.1.10-stable.tar.gz [GPG Sig] ChangeLog
Released 2019-05-26
libevent-2.1.8-stable.tar.gz [GPG Sig] ChangeLog
Released 2017-01-22
Changelog to follow
libevent-2.0.22-stable.tar.gz [GPG Sig] ChangeLog
Released 2014-01-05
Changelog to follow
libevent-2.0.21-stable.tar.gz [GPG Sig] ChangeLog
Released 2012-11-18
Several SSL correctness and performance fixes.
Build fixes for mingw64
Avoid a few resource leaks
and more...
libevent-2.0.20-stable.tar.gz [GPG Sig] ChangeLog
Released 2012-08-23
Fix a crash on windows.
Make event_pending() threadsafe.
Another SSL callback behavior fixes
Avoid an evdns segfault (Greg Hazel)
and more...
libevent-1.4.15-stable.tar.gz ChangeLog
Released 2015-01-05
Changelog to follow
libevent-1.4.14b-stable.tar.gz [GPG Sig] ChangeLog
Released 2010-06-07

https://github.com/edidada/testlibevent
源代码调试libevent

https://libevent.org/

https://github.com/libevent/libevent/tags


libevent 2.1.12
release-2.1.8-stable

sudo apt install libevent-dev -y
sudo yum install libevent-devel -y

## reference
http://www.wangafu.net/~nickm/libevent-2.1/doxygen/html/


http://www.wangafu.net/~nickm/libevent-2.1/doxygen/html/event_8h.html


`#define SENDFILE_IS_LINUX 1` 这个宏定义是 libevent 库中的一部分,它与 Linux 操作系统的 `sendfile()` 系统调用有关。

libevent 是一个开源的跨平台事件调度库,广泛用于构建网络应用程序。它提供了统一的事件处理接口,并在不同的操作系统上使用最佳的方法进行实现。
在 libevent 中,`SENDFILE_IS_LINUX` 宏的作用如下:
1. 操作系统检测: 该宏用于检测当前使用的操作系统是否为 Linux。在 Linux 系统上,该宏的值被定义为 1,而在其他操作系统上则为 0。
2. 优化网络传输: Linux 操作系统提供了 `sendfile()` 系统调用,可以在内核空间直接将文件数据传输到套接字,而无需在用户空间进行复制。libevent 会根据 `SENDFILE_IS_LINUX` 的值,选择使用 `sendfile()` 还是其他的传输方式,以优化网络数据传输的性能。
在 libevent 的实现中,当 `SENDFILE_IS_LINUX` 为 1 时,libevent 会使用 `sendfile()` 系统调用来高效地传输文件数据。这可以减少内存复制操作,提高网络传输性能,特别是在大文件传输的场景下。

总的来说, `#define SENDFILE_IS_LINUX 1` 这个宏定义是 libevent 库用于检测当前操作系统是否为 Linux,并优化网络传输性能的一个重要标识。它体现了 libevent 在不同平台上进行针对性优化的设计思想。

## book

https://libevent.org/libevent-book/Ref10_http_server.html

git clone git://github.com/libevent/libevent-book.git

