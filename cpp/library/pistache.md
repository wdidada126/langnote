# Pistache

## doc
https://pistacheio.github.io/pistache/docs/

### head files
#include <pistache/pistache.h>
#include <pistache/endpoint.h>

https://pistacheio.github.io/pistache/docs/

## c++标准
貌似要c++17了

## 源代码托管仓库
https://github.com/pistacheio/pistache


源码分析
https://zhuanlan.zhihu.com/p/389151428

Restful
## testpistache

travis编译不通过
https://github.com/edidada/testpistache
20210207 编译通过

nohup和&后台运行，进程查看及终止
https://www.cnblogs.com/baby123/p/6477429.html

## debian/ubuntu安装
$ sudo add-apt-repository ppa:pistache+team/stable
$ sudo apt update
$ sudo apt install libpistache-dev


sudo add-apt-repository ppa:pistache+team/stable
sudo apt update
sudo apt install libpistache-dev

ubuntu github codespace尝试了，安装不了


对pistache的源码分析和竞品可以概括如下:
Pistache源码分析:
- Pistache是一个用C++写的开源高性能REST框架。它使用了一些现代C++特性,如coroutine和线程池等。

- Pistache的主要组件包括:
  - Router: 用于注册路由和请求分发
  - Endpoint: 表示一个端点,接收连接并处理请求
  - Http::Request/Response: 封装了请求和响应
  - Transport: 处理底层的socket连接
  - Thread pool: 用于异步处理请求

- Pistache使用了reactor模式,当请求到来时,会交给线程池进行异步处理,而不是为每个请求创建新线程。
- Pistache还使用了一些优化技术,比如预先分配内存减少堆分配,io队列避免锁竞争等。

竞品:
- drogon: 另一个用C++编写的高性能Web应用框架,采用协程实现异步非阻塞,也支持HTTP2。
- cpp-netlib: 一个较早的C++网络库项目,提供了对HTTP、URI、 序列化、服务器等方面的封装。
- Restbed: 一个模型简单的C++ REST框架,易于嵌入已有项目。
- Beast: C++的增强型网络和应用程序库,由Boost提供,可以用来构建REST服务。

所以Pistache在性能、api设计和使用C++新特性方面做得不错,是C++创建REST服务不错的选择。