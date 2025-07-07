# libevent

linux高性能编程，书记上有libevent 例子，Chap. 12
如果你使用的是较新版本的 libevent（比如 libevent 2.x），推荐使用 event_base_new() 替代 event_init()（后者已废弃）。

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
```shell
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
```

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


## 接口列表 Data Structure Index
commit 5df3037d10556bfcb675bc73e516978b75fc7bc7 (HEAD, tag: release-2.1.12-stable, origin/patches-2.1)

### A
alerted_record
arc4_stream

### B
basic_cb_args
basic_test_data
be_conn_hostname_result
bio_data_counts
both
bufferevent
bufferevent_async
bufferevent_ctrl_data
bufferevent_filter_data_stuck
bufferevent_filtered
bufferevent_openssl
bufferevent_ops
bufferevent_pair
bufferevent_private
bufferevent_rate_limit
bufferevent_rate_limit_group

### C
chunk_req_state
client_state
common_timeout_info
common_timeout_list
cond_wait
connect_base
cpu_usage_timer

### D
data_buffer
debug_lock
deferred_reply_callback
deferred_test_data
dnslabel_entry
dnslabel_table
dummy_overlapped

### E
ev_token_bucket
ev_token_bucket_cfg
evbuffer
evbuffer_cb_entry
evbuffer_cb_info
evbuffer_chain
evbuffer_chain_file_segment
evbuffer_chain_reference
evbuffer_file_segment
evbuffer_iovec
evbuffer_multicast_parent
evbuffer_overlapped
evbuffer_ptr
evconnlistener
evconnlistener_event
evconnlistener_ops
evdns_base
evdns_getaddrinfo_request
evdns_request
evdns_server_port
evdns_server_question
evdns_server_request
event
event_and_count
event_base
event_callback
event_change
event_changelist
event_changelist_fdinfo
event_config
event_config_entry
event_debug_entry
event_once
event_overlapped
event_signal_map
event_watermark
eventop
evhttp
evhttp_bound_socket
evhttp_cb
evhttp_connection
evhttp_request
evhttp_server_alias
evhttp_uri
evkeyval
evmap_foreach_event_helper
evmap_io
evmap_signal
evrpcevrpc_base
evrpc_hook
evrpc_hook_ctx
evrpc_hook_meta
evrpc_hooks_
evrpc_meta
evrpc_pool
evrpc_req_generic
evrpc_request_wrapper
evrpc_status
evsig_info
evthread_condition_callbacks
evthread_lock_callbacks
evthread_win32_cond
evutil_addrinfo
evutil_monotonic_timer
evutil_weakrand_state
example_struct

### F
foreach_helper

### G
gai_outcome
gaic_request_status
generic_dns_callback_result
getaddrinfo_subrequest

### H
hosts_entry
http_server

### I
in6_addr

### M
min_heap

### N
nameserver

### O
options

### P
persist_active_timeout_called

### R
read_not_timeout_param
regress_dns_server_table
reply
request
request_info
response_class
rpc_hook_ctx_
rwcount

### S
search_domain
search_state
server_reply_item
server_request
sockaddr_in6
sockaddr_storage

### T
terminate_state
test_pri_event
testcase_setup_t
testcase_t
testgroup_t
testlist_alias_t
timeout_cb_result

### W
wm_context

## 函数
### a
a : example_struct, min_heap, reply
aaaa : reply
accept4_flags : evconnlistener
active_later_queue : event_base
activequeues : event_base
add : eventop
additional : server_request
addr : hosts_entry, server_request
addrcount : reply
address : evhttp_connection, nameserver
addresses : reply
addrlen : hosts_entry, nameserver, server_request
addrs : generic_dns_callback_result
addrs_buf : generic_dns_callback_result
addrs_len : generic_dns_callback_result
adj_timeouts : bufferevent_ops
adjust_monotonic_clock : evutil_monotonic_timer
ai : gai_outcome
ai_addr : evutil_addrinfo
ai_addrlen : evutil_addrinfo
ai_canonname : evutil_addrinfo
ai_family : evhttp_connection, evutil_addrinfo
ai_flags : evutil_addrinfo
ai_next : evutil_addrinfo
ai_protocol : evutil_addrinfo
ai_socktype : evutil_addrinfo
alerted_at : alerted_record
alias : evhttp_server_alias
alloc : evthread_lock_callbacks
alloc_condition : evthread_condition_callbacks
allow_dirty_shutdown : bufferevent_openssl
allowed_methods : evhttp
ans : regress_dns_server_table
anstype : regress_dns_server_table
answer : server_request
arg : event_once, evmap_foreach_event_helper
authority : server_request
avoid_method : event_config_entry

### b
b : example_struct
base : basic_test_data, chunk_req_state, common_timeout_list, evconnlistener_event, evdns_request, evhttp, evhttp_connection, evrpc, evrpc_pool, gaic_request_status, nameserver, request, server_request, terminate_state
be_ops : bufferevent
bev : bufferevent_async, bufferevent_filtered, bufferevent_openssl, bufferevent_pair, bufferevent_private, terminate_state, wm_context
bevcb : evhttp
bevcbarg : evhttp
bind_address : evhttp_connection
bind_port : evhttp_connection
body_size : evhttp_request
bufev : evhttp_connection
buffer : evbuffer_chain, evbuffer_overlapped
buffer1 : data_buffer
buffer2 : data_buffer
buffer_len : evbuffer_chain
buffers : evbuffer_overlapped


c : example_struct
call_count : dummy_overlapped
callcount : basic_cb_args
called_at : common_timeout_info
can_sendfile : evbuffer_file_segment
cancel_event : gaic_request_status
canceled : gaic_request_status
cases : testgroup_t
cb : evbuffer_cb_entry, evconnlistener, event_once, event_overlapped, evhttp_cb, evhttp_connection, evhttp_request, evrpc, evrpc_hook_ctx, evrpc_request_wrapper
cb_arg : evhttp_connection, evhttp_request, evrpc, evrpc_request_wrapper
cb_func : evbuffer_cb_entry
cb_obsolete : evbuffer_cb_entry
cb_queue : evbuffer
cbarg : bufferevent, evbuffer_cb_entry, evhttp_cb
cbs : deferred_test_data
cfg : bufferevent_rate_limit
chain : evbuffer_ptr
changelist : event_base
changes : event_changelist
changes_size : event_changelist
choked : evdns_server_port, nameserver
chunk_cb : evhttp_request
chunked : evhttp_request
class : evdns_server_question, server_reply_item
cleanup_cb : evbuffer_file_segment
cleanup_cb_arg : evbuffer_file_segment
cleanup_fn : testcase_setup_t
cleanupfn : evbuffer_chain_reference
close_change : event_change
closecb : evhttp_connection
closecb_arg : evhttp_connection
closing : evdns_server_port
cname_result : evdns_getaddrinfo_request
common : evrpc_base, evrpc_pool
common_timeout_queues : event_base
cond : alerted_record, cond_wait
condition_api_version : evthread_condition_callbacks
configured_min_share : bufferevent_rate_limit_group
conn_address : bufferevent_private
connect_overlapped : bufferevent_async
connecting : bufferevent_private
connection_refused : bufferevent_private
connections : evhttp, evrpc_pool
contents : evbuffer_file_segment
context : bufferevent_filtered
count : common_timeout_info, debug_lock, event_and_count, foreach_helper, generic_dns_callback_result, read_not_timeout_param, test_pri_event
counts : bufferevent_openssl
ctrl : bufferevent_ops
ctx : evrpc_hook_ctx, rpc_hook_ctx_
current_event : event_base
current_event_cond : event_base
current_event_waiters : event_base
current_req : evdns_request
