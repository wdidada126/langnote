# libevent

rest_libevent

在使用 libevent 创建 HTTP 服务器时，如果你想返回 JSON 格式的数据并设置 `Content-Type` 为 `application/json`，你可以按照以下步骤操作。

### 代码示例

假设你已经设置好了 HTTP 服务器，并且正在处理一个请求：

```c
#include <event2/event.h>
#include <event2/http.h>
#include <event2/buffer.h>
#include <jansson.h>

void handle_request(struct evhttp_request *req, void *arg) {
    // 创建一个 JSON 响应对象
    json_t *json_resp = json_object();
    json_object_set_new(json_resp, "message", json_string("Hello, World!"));
    json_object_set_new(json_resp, "status", json_integer(200));

    // 将 JSON 对象转换为字符串
    char *response_data = json_dumps(json_resp, JSON_COMPACT);
    
    // 设置响应头中的 Content-Type 为 application/json
    struct evbuffer *evb = evbuffer_new();
    evhttp_add_header(evhttp_request_get_output_headers(req), "Content-Type", "application/json");
    
    // 添加响应数据
    evbuffer_add_printf(evb, "%s", response_data);
    
    // 发送响应
    evhttp_send_reply(req, 200, "OK", evb);

    // 清理资源
    evbuffer_free(evb);
    json_decref(json_resp);
    free(response_data);
}

int main(int argc, char **argv) {
    struct event_base *base = event_base_new();
    struct evhttp *http = evhttp_new(base);

    // 绑定请求处理函数
    evhttp_set_gencb(http, handle_request, NULL);

    // 监听指定端口
    evhttp_bind_socket(http, "0.0.0.0", 8080);

    // 启动事件循环
    event_base_dispatch(base);

    // 释放资源
    evhttp_free(http);
    event_base_free(base);

    return 0;
}
```

### 关键步骤

1. 创建 JSON 响应对象：
   使用 `jansson` 库来创建 JSON 数据。`json_object_set_new()` 函数可以为对象设置键值对。

2. 转换 JSON 对象为字符串：
   使用 `json_dumps()` 将 `json_t` 对象转换为 JSON 字符串。

3. 设置 `Content-Type` 为 `application/json`：
   调用 `evhttp_add_header()`，将 `Content-Type` 设置为 `application/json`。

4. 发送响应：
   使用 `evhttp_send_reply()` 将响应数据发送回客户端。

5. 清理资源：
   在完成响应后，释放分配的内存和对象。

### 运行效果

当客户端发起请求时，服务器将返回如下格式的 JSON 响应：

```json
{
    "message": "Hello, World!",
    "status": 200
}
```

同时，HTTP 响应头中的 `Content-Type` 被正确设置为 `application/json`。

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
https://gitee.com/Gendron/libevent

libevent 2.1.12
release-2.1.8-stable

sudo apt install libevent-dev -y
sudo yum install libevent-devel -y

2.1.11

dpkg -L libevent-dev
/.
/usr
/usr/include
/usr/include/evdns.h
/usr/include/event.h
/usr/include/event2
/usr/include/event2/buffer.h
/usr/include/event2/buffer_compat.h
/usr/include/event2/bufferevent.h
/usr/include/event2/bufferevent_compat.h
/usr/include/event2/bufferevent_ssl.h
/usr/include/event2/bufferevent_struct.h
/usr/include/event2/dns.h
/usr/include/event2/dns_compat.h
/usr/include/event2/dns_struct.h
/usr/include/event2/event-config.h
/usr/include/event2/event.h
/usr/include/event2/event_compat.h
/usr/include/event2/event_struct.h
/usr/include/event2/http.h
/usr/include/event2/http_compat.h
/usr/include/event2/http_struct.h
/usr/include/event2/keyvalq_struct.h
/usr/include/event2/listener.h
/usr/include/event2/rpc.h
/usr/include/event2/rpc_compat.h
/usr/include/event2/rpc_struct.h
/usr/include/event2/tag.h
/usr/include/event2/tag_compat.h
/usr/include/event2/thread.h
/usr/include/event2/util.h
/usr/include/event2/visibility.h
/usr/include/evhttp.h
/usr/include/evrpc.h
/usr/include/evutil.h
/usr/lib
/usr/lib/x86_64-linux-gnu
/usr/lib/x86_64-linux-gnu/libevent.a
/usr/lib/x86_64-linux-gnu/libevent_core.a
/usr/lib/x86_64-linux-gnu/libevent_extra.a
/usr/lib/x86_64-linux-gnu/libevent_openssl.a
/usr/lib/x86_64-linux-gnu/libevent_pthreads.a
/usr/lib/x86_64-linux-gnu/pkgconfig
/usr/lib/x86_64-linux-gnu/pkgconfig/libevent.pc
/usr/lib/x86_64-linux-gnu/pkgconfig/libevent_core.pc
/usr/lib/x86_64-linux-gnu/pkgconfig/libevent_extra.pc
/usr/lib/x86_64-linux-gnu/pkgconfig/libevent_openssl.pc
/usr/lib/x86_64-linux-gnu/pkgconfig/libevent_pthreads.pc
/usr/share
/usr/share/doc
/usr/share/doc/libevent-dev
/usr/share/doc/libevent-dev/TODO.Debian
/usr/share/doc/libevent-dev/copyright
/usr/share/doc/libevent-dev/examples
/usr/share/doc/libevent-dev/examples/Makefile.sample
/usr/share/doc/libevent-dev/examples/dns-example.c
/usr/share/doc/libevent-dev/examples/event-read-fifo.c
/usr/share/doc/libevent-dev/examples/hello-world.c
/usr/share/doc/libevent-dev/examples/hostcheck.c
/usr/share/doc/libevent-dev/examples/http-connect.c
/usr/share/doc/libevent-dev/examples/http-server.c
/usr/share/doc/libevent-dev/examples/https-client.c
/usr/share/doc/libevent-dev/examples/le-proxy.c
/usr/share/doc/libevent-dev/examples/openssl_hostname_validation.c
/usr/share/doc/libevent-dev/examples/signal-test.c
/usr/share/doc/libevent-dev/examples/time-test.c
/usr/share/doc/libevent-dev/whatsnew-2.0.txt.gz
/usr/share/doc/libevent-dev/whatsnew-2.1.txt.gz
/usr/lib/x86_64-linux-gnu/libevent.so
/usr/lib/x86_64-linux-gnu/libevent_core.so
/usr/lib/x86_64-linux-gnu/libevent_extra.so
/usr/lib/x86_64-linux-gnu/libevent_openssl.so
/usr/lib/x86_64-linux-gnu/libevent_pthreads.so
/usr/share/doc/libevent-dev/changelog.Debian.gz

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

