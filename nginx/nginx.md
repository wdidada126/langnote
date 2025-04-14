# nginx

server_token on/off
nginx配置中的server_token指令用于控制nginx服务器在响应HTTP请求时是否显示服务器的版本信息。默认情况下，nginx会在响应头中包含服务器的版本号，例如Server: nginx/1.18.0。这个信息可能会被潜在的攻击者用来了解服务器的漏洞和弱点，从而增加服务器被攻击的风险
。

通过配置server_token off，可以禁止在响应头中显示服务器的版本信息，只显示服务名称而不显示具体的版本号。这样，攻击者就难以通过版本号来识别服务器的具体版本，进而难以利用已知漏洞进行针对性攻击。具体来说，当在nginx的配置文件中设置server_token off后，nginx在返回HTTP响应头时，将不再包含服务器的版本信息，从而增加服务器的安全性
。

要在nginx中配置server_token off，需要编辑nginx的配置文件（通常是nginx.conf），在http、server或location节点下添加server_token off;指令。完成配置后，需要重新加载nginx的配置，使更改生效


`nginx.conf` 是Nginx服务器的主配置文件，它包含了Nginx服务器的全局配置、事件模块配置以及HTTP、Mail、Stream等核心模块的配置信息。下面详细介绍其常见包含内容：

### 全局块
全局块是 `nginx.conf` 文件中从开始到 `events` 块之间的部分，主要用于设置影响Nginx服务器整体运行的全局配置指令。
```nginx
# 定义Nginx工作进程的用户和用户组
user nginx;
# 指定Nginx工作进程的数量，通常设置为CPU核心数
worker_processes auto;
# 错误日志的路径和日志级别
error_log /var/log/nginx/error.log warn;
# 指定进程ID文件的路径
pid /var/run/nginx.pid;
```

### events块
`events` 块主要用于配置Nginx服务器与用户的网络连接，控制Nginx的连接处理方式。
```nginx
events {
    # 每个工作进程允许同时连接的最大客户端数量
    worker_connections 1024;
    # 使用的事件驱动模型，如epoll（Linux）、kqueue（FreeBSD）等
    use epoll; 
}
```

### HTTP块
`http` 块是Nginx配置中最核心的部分，包含了代理、缓存、日志记录、虚拟主机等众多功能的配置。
```nginx
http {
    # 设置文件扩展名与文件类型的映射关系
    include /etc/nginx/mime.types;
    # 默认的文件类型
    default_type application/octet-stream;
    # 日志格式
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';
    # 访问日志的路径和使用的日志格式
    access_log /var/log/nginx/access.log main;
    # 开启高效文件传输模式
    sendfile on;
    # 防止网络阻塞
    tcp_nopush on;
    # 保持连接的超时时间
    keepalive_timeout 65;
    # 包含其他配置文件
    include /etc/nginx/conf.d/*.conf;
    # 虚拟主机配置
    server {
        # 监听的端口
        listen 80;
        # 服务器名称，可以是域名或IP地址
        server_name example.com;
        # 网站根目录
        root /var/www/html;
        # 默认的索引文件
        index index.html index.htm;
        # 处理请求的位置块
        location / {
            try_files $uri $uri/ /index.html;
        }
        # 错误页面配置
        error_page 500 502 503 504 /50x.html;
        location = /50x.html {
            root /var/www/html;
        }
    }
}
```

### mail块（可选）
如果Nginx用于邮件代理，可使用 `mail` 块进行相关配置。
```nginx
mail {
    # 监听的邮件服务端口
    server {
        listen     25;
        protocol   smtp;
        # 邮件服务器的认证方式
        smtp_auth  login plain;
    }
    server {
        listen     110;
        protocol   pop3;
        # 启用POP3的APOP认证
        pop3_auth  apop;
    }
}
```

### stream块（可选）
`stream` 块用于配置Nginx的TCP和UDP代理功能。
```nginx
stream {
    # 监听的TCP端口
    server {
        listen     3306;
        # 转发的目标服务器地址和端口
        proxy_pass mysql_backend;
    }
    # 定义上游服务器组
    upstream mysql_backend {
        server 192.168.1.100:3306;
        server 192.168.1.101:3306;
    }
}
```

以上是 `nginx.conf` 文件常见的配置内容，不同的使用场景和需求可能会导致配置文件有所差异。 

根据您的请求，以下是一些Nginx配置项图形化界面的工具：

1. Nginx UI
   - Nginx UI是一款开源的Nginx可视化管理界面，它简化了Nginx的配置与管理过程，提供了实时监控功能，可以显示Nginx服务器的关键指标，如连接数、请求处理时间等。[CSDN博客](https://blog.csdn.net/leeit/article/details/143420722)
   - 项目地址：[https://github.com/0xJacky/nginx-ui](https://github.com/0xJacky/nginx-ui)
2. nginxWebUI
   - nginxWebUI是一款图形化管理nginx配置的工具，可以使用网页来快速配置nginx的各项功能，包括http协议转发、tcp协议转发、反向代理、负载均衡、静态html服务器、ssl证书自动申请、续签、配置等。[CSDN博客](https://blog.csdn.net/mopmgerg54mo/article/details/141356440)
   - 开源地址：[https://gitee.com/cym1102/nginxWebUI](https://gitee.com/cym1102/nginxWebUI)
3. Nginx GUI Manager
   - Nginx GUI Manager是一个开源项目，提供了一个图形用户界面来管理和配置Nginx服务器，使得用户无需直接编辑配置文件即可完成服务器的设置。[CSDN博客](https://blog.csdn.net/gitblog_00578/article/details/144080381)

这些工具可以帮助您通过图形化界面来管理和配置Nginx服务器，提高工作效率并降低配置难度。您可以访问上述链接了解更多详情和下载使用。


ng中文社区
https://www.f5chinanetworks.com/

## 模块
https://github.com/gnosek/nginx-upstream-fair
c语言写的

这个问题的原因可能是由于location匹配顺序和规则导致的。在Nginx中，location的匹配规则如下：

精确匹配（使用=）。
前缀匹配（最长匹配，使用^~）。
正则表达式匹配（使用~和~*）。
非前缀匹配（使用无修饰符的URI）。
在您的情况下，由于没有使用^~、=、~或~*修饰符，Nginx将按照最长前缀匹配规则来处理。这意味着如果有其他更具体的location配置与请求的URI前缀匹配，那么这些配置将优先于您当前的location配置。

https://nginx.org/en/docs/http/ngx_http_core_module.html#var_remote_addr

$remote_addr
client address

x_forwarded_for
https://www.cnblogs.com/kuracola/p/7482939.html

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


