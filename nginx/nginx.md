# nginx

ng对比apache httpd
https://zhuanlan.zhihu.com/p/633063330

PCRE库
PCRE（Perl Compatible Regular Expressions，Perl兼容正则表达式）是由Philip Hazel开发
的函数库，目前为很多软件所使用，该库支持正则表达式。它由RegEx演化而来，实际上，
Perl正则表达式也是源自于Henry Spencer写的RegEx。
如果我们在配置文件nginx.conf里使用了正则表达式，那么在编译Nginx时就必须把PCRE
库编译进Nginx，因为Nginx的HTTP模块要靠它来解析正则表达式。当然，如果你确认不会使
用正则表达式，就不必安装它。

部署Nginx时都是使用一个master进程来管理多个worker
进程，一般情况下，worker进程的数量与服务器上的CPU核心数相等。每一个worker进程都
是繁忙的，它们在真正地提供互联网服务，master进程则很“清闲”，只负责监控管理worker
进程。worker进程之间通过共享内存、原子操作等一些进程间通信机制来实现负载均衡等功
能

屹通nginx.conf

    #多租户场景文件引入
    #宁波银行租户:9083
    include /app/nginx-1.20.0/conf/nbcb.conf;
    #薪享通租户:9084
    include /app/nginx-1.20.0/conf/xxt.conf;

    include /app/nginx-1.20.0/conf/zwb.conf;

在Nginx的配置文件nginx.conf中，worker_processes 指令用于定义Nginx启动的工作进程数。当你设置worker_processes 4; 时，你告诉Nginx启动4个工作进程来处理连接。

这里的每个工作进程都是独立的，并且它们都可以处理多个连接。Nginx 使用事件驱动和非阻塞 I/O 来处理这些连接，这意味着每个工作进程都可以有效地处理数千个并发连接。

设置 worker_processes 的值通常取决于你的服务器的硬件配置，特别是 CPU 的核心数。以下是一些常见的设置建议：

如果你有一个单核 CPU，那么设置 worker_processes 1; 通常是足够的。
如果你有一个多核 CPU，那么你可以将 worker_processes 的值设置为与 CPU 核心数相同，以便充分利用多核优势。例如，如果你的服务器有 4 个 CPU 核心，那么设置 worker_processes 4; 是合适的。
在某些情况下，你可能还想考虑使用超线程或逻辑核心。但是，请注意，超线程并不总是能带来性能提升，因此你可能需要进行一些基准测试来确定最佳的设置。
除了 worker_processes 之外，还有其他一些指令（如 worker_connections 和 events 块中的指令）也可以影响 Nginx 的性能和工作方式。因此，在调整 Nginx 的配置时，最好考虑整个配置文件，并确保所有的设置都是相互协调的。



events {
    worker_connections 51200;
    use epoll;
    multi_accept on;
}


在 Nginx 的配置文件中，events 块用于定义与事件处理相关的指令。下面是你给出的 events 块配置的详解：

worker_connections 51200;
这个指令设置了每个工作进程（worker process）可以打开的最大连接数。需要注意的是，这个数值并不是 Nginx 可以处理的并发连接总数，而是每个工作进程可以处理的连接数。因此，Nginx 可以处理的并发连接总数是 worker_processes（工作进程数）乘以 worker_connections（每个工作进程的连接数）。

在这个例子中，每个工作进程可以打开的最大连接数是 51200。但是，实际上你可能需要根据服务器的实际情况来调整这个值，因为打开过多的连接可能会消耗大量的系统资源。
2. use epoll;

这个指令指定了 Nginx 使用哪种事件驱动模型。在 Linux 系统上，Nginx 支持多种事件驱动模型，如 select、poll、kqueue、epoll 等。epoll 是 Linux 上的一种高效的事件通知机制，特别适合于高并发的场景。使用 epoll 可以提高 Nginx 的性能和可扩展性。

注意：在 Windows 系统上，Nginx 不支持 epoll，而是使用 iocp 作为事件驱动模型。
3. multi_accept on;

这个指令决定了 Nginx 是否应该尝试同时接受多个新连接。当设置为 on 时，Nginx 会尝试在一个工作进程中同时接受多个新连接，这样可以减少系统的上下文切换次数，提高性能。但是，这也可能会增加资源竞争的风险，因此需要根据你的应用场景和服务器配置来权衡利弊。

总结：你给出的 events 块配置是一个针对高并发场景的优化配置，其中使用了高效的 epoll 事件驱动模型和 multi_accept 功能来提高 Nginx 的性能和可扩展性。但是，请注意，具体的配置值需要根据你的服务器和应用场景来进行调整。


nginx开发出来之前，直接servlet

互联网公司，nginx用

反向代理，负载均衡，代理缓存，限流

http://nginx.org/en/docs/

nginx中文翻译

blog

https://www.nginx.com/blog/

校验nginx配置文件的项目
nginx -t

https://blog.redis.com.cn/doc/


Tengine

章亦春
lua

openresty

[ng load blance](http://nginx.org/en/docs/http/load_balancing.html)

[Nginx负载均衡health_check分析](https://www.onmpw.com/tm/xwzj/network_132.html)

- round-robin
- least-connected
- ip-hash


```shell
nginx -V
nginx version: nginx/1.12.2
built by gcc 4.8.5 20150623 (Red Hat 4.8.5-16) (GCC) 
built with OpenSSL 1.0.2k-fips  26 Jan 2017
TLS SNI support enabled
configure arguments: --prefix=/usr/share/nginx --sbin-path=/usr/sbin/nginx --modules-path=/usr/lib64/nginx/modules --conf-path=/etc/nginx/nginx.conf --error-log-path=/var/log/nginx/error.log --http-log-path=/var/log/nginx/access.log --http-client-body-temp-path=/var/lib/nginx/tmp/client_body --http-proxy-temp-path=/var/lib/nginx/tmp/proxy --http-fastcgi-temp-path=/var/lib/nginx/tmp/fastcgi --http-uwsgi-temp-path=/var/lib/nginx/tmp/uwsgi --http-scgi-temp-path=/var/lib/nginx/tmp/scgi --pid-path=/run/nginx.pid --lock-path=/run/lock/subsys/nginx --user=nginx --group=nginx --with-file-aio --with-ipv6 --with-http_auth_request_module --with-http_ssl_module --with-http_v2_module --with-http_realip_module --with-http_addition_module --with-http_xslt_module=dynamic --with-http_image_filter_module=dynamic --with-http_geoip_module=dynamic --with-http_sub_module --with-http_dav_module --with-http_flv_module --with-http_mp4_module --with-http_gunzip_module --with-http_gzip_static_module --with-http_random_index_module --with-http_secure_link_module --with-http_degradation_module --with-http_slice_module --with-http_stub_status_module --with-http_perl_module=dynamic --with-mail=dynamic --with-mail_ssl_module --with-pcre --with-pcre-jit --with-stream=dynamic --with-stream_ssl_module --with-google_perftools_module --with-debug --with-cc-opt='-O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector-strong --param=ssp-buffer-size=4 -grecord-gcc-switches -specs=/usr/lib/rpm/redhat/redhat-hardened-cc1 -m64 -mtune=generic' --with-ld-opt='-Wl,-z,relro -specs=/usr/lib/rpm/redhat/redhat-hardened-ld -Wl,-E'
```

### Ngix安装(Linux) 

[官方下载地址](http://nginx.org/en/download.html)

### 安装与启动

#### rpm源码编译
wget http://nginx.org/download/nginx-1.8.1.tar.gz

1. gcc环境 `yum install gcc-c++`
2. 第三方的开发包
    - PCRE `yum install -y pcre pcre-devel`
    - zlib `yum install -y zlib zlib-devel`
    - openssl `yum install -y openssl openssl-devel`
3. 安装
    - 解压 `[root@localhost ~]# tar zxf nginx-1.8.0.tar.gz`
    - 进入解压后文件夹复制执行以下命令
    `./configure  --prefix=/usr/local/nginx  --sbin-path=/usr/local/nginx/sbin/nginx --conf-path=/usr/local/nginx/conf/nginx.conf --error-log-path=/var/log/nginx/error.log  --http-log-path=/var/log/nginx/access.log  --pid-path=/var/run/nginx/nginx.pid --lock-path=/var/lock/nginx.lock  --user=nginx --group=nginx --with-http_ssl_module --with-http_stub_status_module --with-http_gzip_static_module --http-client-body-temp-path=/var/tmp/nginx/client/ --http-proxy-temp-path=/var/tmp/nginx/proxy/ --http-fastcgi-temp-path=/var/tmp/nginx/fcgi/ --http-uwsgi-temp-path=/var/tmp/nginx/uwsgi --http-scgi-temp-path=/var/tmp/nginx/scgi --with-pcre`
    - `[root@localhost nginx-1.8.0]# make`
    - `[root@localhost nginx-1.8.0]# make install`
    - `[root@localhost sbin]# mkdir /var/temp/nginx/client -p`
    - 进入目录 `cd /usr/local/nginx/` 
    - 启动 `[root@localhost sbin]# ./nginx`
4. 配置文件目录 
`nginx/conf/nginx.conf`
5. 重新加载配置文件 避免重启
`sbin/nginx -s reload`

### 配置

- 配置虚拟主机与反向代理
```
worker_processes  1;

events {
    worker_connections  1024;
}

http {
    include       mime.types;
    default_type  application/octet-stream;

    sendfile        on;
    #tcp_nopush     on;

    #keepalive_timeout  0;
    keepalive_timeout  65;

    #gzip  on;

    upstream resume{
	server 123.207.121.135:8080;
    }

    server {
        listen       80;
        server_name  localhost;

        location / {
            proxy_pass   http://resume;
            index  index.html index.htm;
        }

        #error_page  404              /404.html;

        # redirect server error pages to the static page /50x.html
        #
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }
    }

    server {
        listen       80;
        server_name  www.img.exrick.cn;

        #charset koi8-r;

        #access_log  logs/host.access.log  main;

        location / {
            root   html81;
            index  index.html index.htm;
        }

        #error_page  404              /404.html;

        # redirect server error pages to the static page /50x.html
        #
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }
    }

    server {
        listen       80;
        server_name  www.xmall.exrick.cn;

        #charset koi8-r;

        #access_log  logs/host.access.log  main;

        location / {
            root   html;
            index  index.html index.htm;
        }

        #error_page  404              /404.html;

        # redirect server error pages to the static page /50x.html
        #
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }
    }
}
```

- 负载均衡（直接添加server即可）
```
...
http {
    ...
    upstream resume{
        server 123.207.121.135:8080;
        server 123.207.121.135:8081;
    } 
    ...
}
```
权重调节（weight）
```
...
http {
    ...
    upstream resume{
        server 123.207.121.135:8080;
        server 123.207.121.135:8081 weight=2;
    } 
    ...
}
```

- 压缩文件
```
    gzip  on;
    gzip_min_length 1k;
    gzip_buffers 4 16k;
    gzip_comp_level 9;
    gzip_types text/plain application/x-javascript application/javascript text/css application/xml text/javascript application/x-httpd-php image/jpeg image/gif image/png eventsource script png;
```

- 解决代理IP地址
```
server {
        listen       80;
        server_name  xmall.exrick.cn;

        location / {
            proxy_pass   http://xmall;
            index  index.html index.htm;
	        proxy_set_header Host $host;
	        proxy_set_header X-Real-IP $remote_addr;
	        proxy_set_header REMOTE-HOST $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }

        error_page  404              /50x.html;

        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }

    }
```

### 踩坑解决问题
- [emerg]: getpwnam("nginx") failed

    - 解决方法1：
      在nginx.conf中 把user nobody的注释去掉既可
    - 解决方法2：
      错误的原因是没有创建nginx这个用户，应该在服务器系统中添加nginx用户组和用户nginx，如下命令：
`/usr/sbin/groupadd -f nginx`
`/usr/sbin/useradd -g nginx nginx`
- [emerg] mkdir() "/var/temp/nginx/client" failed (2: No such file or directory)
root下手动创建即可：`mkdir -p /var/temp/nginx/client`
- 重启服务器后启动提示/var/run/nginx找不到

```
nginx: [error] open() "/var/run/nginx.pid" failed (2: No such file or directory)
```

进入`/var/run`新建`nginx`文件夹：`mkdir nginx`

ngx里面红黑树实现得多漂亮，简直是c的典范


