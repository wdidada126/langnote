# nginx


彻底搞懂反向代理神器Nginx Proxy Manager的配置和使用

除了DNS的A类型记录外，常见的还有以下类型：
1. AAAA记录（IPv6 Address Record）：用于将域名映射到IPv6地址，随着IPv6的广泛应用，它允许设备使用新的互联网协议版本进行通信，提供更多的地址空间和更好的安全性。
2. MX记录（Mail Exchanger Record）：即邮件交换记录，指向一个邮件服务器，用于电子邮件系统发邮件时根据收信人的地址后缀来定位邮件服务器。
3. CNAME记录（Canonical Name Record）：即别名记录，允许将多个名字映射到同一台计算机，也就是可以为一个主机设置多个别名，这些别名最终都指向同一个主机名。
4. NS记录（Name Server Record）：即域名服务器记录，用来指定该域名由哪个DNS服务器来进行解析。
5. TXT记录：可以存储任意文本信息，通常用于存储元数据或配置信息，如用于SPF（发送者策略框架）反垃圾邮件，向收信者表明哪些邮件服务器是经过某个域名认可会发送邮件的。
6. SRV记录（Service Record）：用于指定特定服务的服务器位置和端口号，比如指定一个LDAP服务器的地址和端口。
7. PTR记录（Pointer Record）：是A记录的逆向，将IP地址映射回域名，通常用于反向DNS查找，确定一个IP地址属于哪个域名。
8. SOA记录（Start of Authority Record）：标志着DNS区域的开始，并包含有关区域的信息，如主DNS服务器和区域的管理员联系信息。
9. DNSSEC记录：即DNS安全扩展记录，用于提供DNS数据的完整性和来源认证，包括DS（Delegation Signer）、DNSKEY（DNS密钥）和RRSIG（资源记录签名）等。
10. 其他记录：如LOC（地理位置）记录用于标识与域名相关的地理位置信息、NAPTR（名称服务器指针转换）记录用于处理电话号码映射等特定应用场景、SSHFP（SSH公钥指纹）记录用于验证SSH服务器的公钥等。

nginx可以映射到本地html文件，可以解析php
nginx可以http include其他配置文件
在Nginx的配置中，alias指令用于替换location匹配到的URI部分。具体到你的配置示例中，让我们逐步解析alias的作用：

nginx
```
location /salaryManager/index.html {
    alias /app/nginx-1.20.0/html/salaryManager/index.html;
    add_header Cache-Control "private, no-store, no-cache, must-revalidate, proxy-revalidate";
}
```

location匹配：
location /salaryManager/index.html 表示当请求的URI是/salaryManager/index.html时，这条规则会被匹配。
alias的作用：
alias指令后面跟着的路径/app/nginx-1.20.0/html/salaryManager/index.html是一个文件系统上的绝对路径。
当请求匹配到location /salaryManager/index.html时，Nginx不会简单地基于请求的URI去寻找文件（即不会去找/salaryManager/index.html这样的相对路径下的文件），而是直接使用alias指定的路径去服务文件。
重要的是，alias替换的是整个匹配的location部分（在这个例子中是/salaryManager/index.html），而不是仅仅替换location中的某个部分。因此，这里的alias直接指向了一个具体的文件，而不是一个目录。
注意事项：
在你的配置中，alias直接指向了一个具体的HTML文件。这通常用于特定文件的重定向，但在大多数情况下，我们可能更希望alias指向一个目录，然后通过请求的URI来确定具体的文件。例如，如果希望/salaryManager/下的所有请求都映射到某个目录下的文件，可以这样配置：
```nginx
location /salaryManager/ {
    alias /app/nginx-1.20.0/html/salaryManager/;
    # 其他指令
}
```
这样，请求/salaryManager/somefile.html会映射到/app/nginx-1.20.0/html/salaryManager/somefile.html。
由于alias直接指向了一个文件，这意味着所有匹配到location /salaryManager/index.html的请求都会返回同一个文件，不论请求的路径或查询参数如何变化。
缓存控制：
add_header Cache-Control "private, no-store, no-cache, must-revalidate, proxy-revalidate";这条指令是用来控制缓存的，它告诉浏览器和中间缓存（如代理服务器）不要存储这个页面的任何版本，每次都需要从服务器重新验证。
综上所述，alias在这个配置中的作用是直接将/salaryManager/index.html的请求映射到文件系统中的/app/nginx-1.20.0/html/salaryManager/index.html文件。

在Nginx中配置以支持PHP文件的处理通常涉及安装PHP-FPM（FastCGI Process Manager）服务，并在Nginx配置文件中设置适当的指令以将PHP请求传递给PHP-FPM处理。以下是一个基本的指南，帮助你在Nginx服务器上配置PHP支持：

1. 安装PHP和PHP-FPM
首先，你需要在你的服务器上安装PHP和PHP-FPM。安装方法取决于你的操作系统。

在Ubuntu/Debian上：
```bash
sudo apt update
sudo apt install php php-fpm php-mysql
```
这里的php-fpm是FastCGI Process Manager，它允许Nginx将PHP请求传递给PHP解释器处理。php-mysql是PHP的MySQL扩展（根据你的需要，你可能想安装其他数据库扩展）。

在CentOS/RHEL上：
```bash
sudo yum install epel-release
sudo yum install php php-fpm php-mysqlnd
```
对于CentOS/RHEL，你需要确保php-fpm服务被安装并启动。
2. 配置PHP-FPM
安装PHP-FPM后，你可能需要编辑其配置文件（通常位于/etc/php-fpm.d/或/etc/php-fpm.conf及包含的池配置文件，如www.conf），以根据你的需求进行调整。例如，你可以更改监听地址、池名称、用户/组等。
3. 修改Nginx配置文件
接下来，你需要修改Nginx的配置文件，以添加对PHP文件的支持。这通常涉及编辑Nginx的主配置文件（如/etc/nginx/nginx.conf）或站点特定的配置文件（如/etc/nginx/sites-available/default，然后创建一个符号链接到/etc/nginx/sites-enabled/）。
你需要在server块中添加一个location块，用于匹配PHP文件，并将请求传递给PHP-FPM处理。例如：
nginx
```
server {
    listen 80;
    server_name yourdomain.com;
    root /var/www/yourdomain;
    index index.php index.html index.htm;
 
    location / {
        try_files $uri $uri/ =404;
    }
 
    location ~ \.php$ {
        include snippets/fastcgi-php.conf;
        fastcgi_pass unix:/var/run/php/php7.4-fpm.sock; # 根据你的PHP-FPM配置调整此路径
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include fastcgi_params;
    }
 
    # 其他配置...
}
```
注意：fastcgi_pass指令的值应该与你的PHP-FPM配置中的监听地址相匹配。在某些系统上，它可能是一个TCP端口（如127.0.0.1:9000），而在其他系统上，它可能是一个Unix套接字（如上面的示例所示）。
4. 重启Nginx和PHP-FPM
修改配置文件后，你需要重启Nginx和PHP-FPM服务以使更改生效：
```bash
sudo systemctl restart nginx
sudo systemctl restart php7.4-fpm  # 根据你的PHP版本调整服务名称
```
或者，如果你的系统使用systemd但不遵循上述命名约定：

```bash
sudo systemctl restart php-fpm
```
5. 测试PHP安装
为了验证PHP是否已正确安装和配置，你可以创建一个简单的PHP文件，如info.php，并将其放在你的网站根目录中：

```php
<?php
phpinfo();
?>
```
然后，在浏览器中访问http://yourdomain.com/info.php。你应该会看到一个PHP信息页面，显示PHP的配置和已安装的扩展。

6. 配置PHP（可选）
根据你的需要，你可能还需要编辑PHP的配置文件（通常是/etc/php/7.4/fpm/php.ini或/etc/php.ini，取决于你的安装和PHP版本），以更改PHP的设置，如时区、内存限制、上传文件大小等。

完成这些步骤后，你的Nginx服务器应该能够处理PHP文件了。

PHP-FPM（FastCGI Process Manager）是一个实现了FastCGI协议的PHP FastCGI管理器，它是PHP的一个FastCGI管理器，旨在提高网站的性能和可靠性。PHP-FPM将传统的CGI（Common Gateway Interface）或FastCGI处理大量并发请求的方式进行了优化，通过管理多个PHP进程来有效地处理请求。

以下是PHP-FPM的一些主要功能和优点：

多进程管理：
PHP-FPM通过创建多个PHP子进程来处理并发请求，这些子进程可以独立运行，互不影响。当请求到来时，PHP-FPM会将请求分配给可用的子进程进行处理。
平滑化请求处理：
PHP-FPM能够智能地管理PHP进程的生命周期，包括进程的启动、运行和终止。它还可以根据服务器的负载情况动态调整进程数量，以优化资源使用。
提高性能和响应速度：
由于PHP-FPM采用了多进程模型，并且能够有效地管理这些进程，因此它能够显著提高PHP应用程序的性能和响应速度。
增强稳定性和安全性：
PHP-FPM通过分离每个请求的处理过程，减少了因单个请求导致的整个服务器崩溃的风险。同时，它还提供了更细粒度的权限控制，增强了系统的安全性。
丰富的配置选项：
PHP-FPM提供了丰富的配置选项，允许管理员根据实际需求对PHP进程进行精细控制。这些配置选项包括进程数量、进程优先级、内存限制等。
支持慢日志和错误日志：
PHP-FPM可以记录慢日志和错误日志，帮助开发人员和运维人员快速定位和解决性能瓶颈和错误。
与Nginx等Web服务器的无缝集成：
PHP-FPM与Nginx等现代Web服务器有着良好的兼容性，可以轻松实现PHP应用程序的快速部署和高效运行。
总之，PHP-FPM是一个功能强大且灵活的PHP FastCGI管理器，它能够帮助开发人员和运维人员提高PHP应用程序的性能、稳定性和安全性。在现代Web开发中，PHP-FPM已经成为处理PHP请求的标准方式之一。

https://docs.konghq.com/

https://www.meetup.com/topics/kong/all/

Products
Kong Konnect
Kong Gateway Enterprise
Kong Gateway
Kong Mesh
Kong Ingress Controller
Kong Insomnia

以下是 Kong 系列产品 的核心功能与区别对比，帮助您根据场景选择合适的产品：

### 1. Kong Gateway  
- 定位：开源版 API 网关  
- 核心功能：  
  - API 路由、负载均衡、认证（Key Auth、JWT 等）、限流、日志集成。  
  - 支持插件扩展（如社区插件）。  
- 适用场景：  
  - 中小型企业或开发者，需要轻量级 API 网关管理。  
  - 无企业级功能需求，依赖开源生态。  

### 2. Kong Gateway Enterprise  
- 定位：企业级增强版 API 网关  
- 核心功能（在开源版基础上增加）：  
  - 高级插件：Bot Detection、RBAC、动态证书管理、GraphQL 防护等。  
  - 可视化分析：实时监控、流量报表、API 性能分析。  
  - 开发者门户：自助式 API 文档发布与订阅。  
  - 高可用性：企业级 SLA、技术支持。  
- 适用场景：  
  - 中大型企业，需要安全、合规、高可用的 API 管理平台。  

### 3. Kong Konnect  
- 定位：全托管云原生 API 管理平台（SaaS）  
- 核心功能：  
  - 集成 Kong Gateway Enterprise 的所有功能。  
  - 统一控制平面：跨多云、混合环境的集中式 API 管理。  
  - 服务网格集成：与 Kong Mesh 无缝协作。  
  - 自动化治理：CI/CD 流水线集成、API 生命周期管理。  
- 适用场景：  
  - 需要快速构建云原生 API 架构，减少运维负担。  
  - 混合云或多云环境下的统一 API 治理。  

### 4. Kong Mesh  
- 定位：基于 Kuma 的服务网格  
- 核心功能：  
  - 跨环境通信：支持 Kubernetes、VM、裸机等多运行时统一管理。  
  - 流量治理：金丝雀发布、熔断、重试、超时控制。  
  - 零信任安全：自动 mTLS 加密、服务间 ACL。  
  - 可观测性：集成 Prometheus、Grafana、Jaeger。  
- 适用场景：  
  - 微服务架构中需要细粒度服务间流量控制与安全策略。  
  - 替代或补充 Istio，支持多集群、多环境统一管理。  

### 5. Kong Ingress Controller  
- 定位：Kubernetes 原生入口流量管理  
- 核心功能：  
  - 作为 Kubernetes Ingress Controller，管理集群入口流量。  
  - 集成 Kong Gateway 功能：认证、限流、路由规则等。  
  - 支持 CRD（Kubernetes 原生资源定义），与 Helm 集成。  
- 适用场景：  
  - 在 Kubernetes 环境中替代 Nginx Ingress，增强 API 网关能力。  
  - 需要将 API 管理与 K8s 生态深度结合。  

### 6. Kong Insomnia  
- 定位：API 设计与测试工具  
- 核心功能：  
  - API 设计：支持 OpenAPI、GraphQL 规范编写与调试。  
  - 自动化测试：生成测试用例、Mock 服务器、性能压测。  
  - 协作功能：团队共享 API 定义、版本控制。  
- 适用场景：  
  - 开发者或测试人员设计、调试和文档化 API。  
  - 替代 Postman，提供更轻量化的本地开发体验。  

### 对比总结  
| 产品                  | 核心能力               | 适用场景                     | 部署形态           |  
|-----------------------|------------------------|------------------------------|--------------------|  
| Kong Gateway       | 基础 API 网关功能      | 轻量级 API 管理              | 开源、自托管       |  
| Kong Gateway Enterprise | 企业级 API 治理       | 中大型企业合规需求           | 企业版、自托管     |  
| Kong Konnect       | 全托管 API 平台        | 多云/混合云统一管理          | SaaS 云服务        |  
| Kong Mesh          | 服务网格               | 微服务间流量与安全治理       | 自托管、K8s/VM     |  
| Kong Ingress Controller | Kubernetes 入口管理 | K8s 环境 API 网关集成        | K8s 原生部署       |  
| Kong Insomnia      | API 开发与测试工具     | 开发者本地调试与协作         | 桌面应用/CLI       |  

### 选型建议  
- API 网关需求：  
  - 开源轻量 → Kong Gateway  
  - 企业级功能 → Kong Gateway Enterprise 或 Kong Konnect（如需云托管）。  
- 服务网格需求 → Kong Mesh。  
- Kubernetes 入口管理 → Kong Ingress Controller。  
- API 开发测试 → Kong Insomnia。  

通过上述对比，可根据实际架构需求（云原生、微服务、K8s 等）选择组合使用 Kong 产品。

`@EnableRedisHttpSession`注解的作用是启用基于 Redis 的分布式会话管理功能，具体作用如下：

1.启用 Redis 作为会话存储
通过该注解，Spring Boot 应用程序会将`HttpSession`数据存储到 Redis 中，而不是存储在本地内存中。这使得会话数据可以在多个应用程序实例之间共享，解决了传统会话管理在分布式环境下的局限性。

2.注册 SessionRepositoryFilter
该注解会注册一个`SessionRepositoryFilter`，它会拦截所有请求，并对会话数据进行操作。这个过滤器会将请求和响应包装成`SessionRepositoryRequestWrapper`和`SessionRepositoryResponseWrapper`，从而实现对会话数据的统一管理。

3.配置会话管理相关参数
• `maxInactiveIntervalInSeconds`：设置会话的失效时间，默认值为 1800 秒（30 分钟），可以通过该属性自定义会话的超时时间。
• `redisNamespace`：设置 Redis 中会话数据的命名空间，默认为`spring:session`。
• `redisFlushMode`：设置 Redis 数据的同步模式，默认为`ON_SAVE`，即在会话保存时同步到 Redis。
• `cleanupCron`：设置清理过期会话的定时任务的 Cron 表达式。

4.实现会话的持久化和共享
使用 Redis 存储会话数据后，会话信息可以在多个应用程序实例之间共享，解决了分布式系统中会话同步的问题。同时，Redis 的持久化功能也保证了会话数据的安全性。

5.简化配置
通过在配置类上添加`@EnableRedisHttpSession`注解，Spring Boot 会自动完成大部分配置工作，包括创建 Redis 连接工厂、配置会话存储等。开发者只需添加注解并配置相关参数即可实现分布式会话管理。

示例
以下是一个简单的配置示例：
```java
@Configuration
@EnableRedisHttpSession(maxInactiveIntervalInSeconds = 86400 * 30) // 设置会话超时时间为 30 天
public class RedisSessionConfig {
    // 可以在此配置其他相关 Bean，如 RedisTemplate
}
```

在上述代码中，`maxInactiveIntervalInSeconds`属性被设置为 30 天，表示会话的超时时间为 30 天。

在Nginx中实现类似Spring Cloud Gateway的限流和授权功能，可以通过以下方式配置：

1.限流功能
Nginx提供了两个核心模块用于限流：
• `ngx_http_limit_req_module`：基于请求速率的限流。
• `ngx_http_limit_conn_module`：基于并发连接数的限流。

示例配置
以下是一个综合的限流配置示例，限制请求速率和并发连接数：

```nginx
http {
    # 定义请求速率限制区域
    limit_req_zone $binary_remote_addr zone=req_limit:10m rate=10r/s;

    # 定义并发连接限制区域
    limit_conn_zone $binary_remote_addr zone=conn_limit:10m;

    server {
        listen 80;
        server_name example.com;

        location / {
            # 应用请求速率限制
            limit_req zone=req_limit burst=20 nodelay;

            # 应用并发连接限制
            limit_conn conn_limit 5;

            proxy_pass http://backend_server;
        }
    }
}
```

• `rate=10r/s`：每秒最多允许10个请求。
• `burst=20`：允许突发请求的最大数量为20。
• `limit_conn conn_limit 5`：每个IP地址最多允许5个并发连接。

2.授权功能
Nginx 可以通过`auth_request`模块实现授权功能，通常结合后端服务（如 Spring Security）进行鉴权。

示例配置
以下是一个基于 JWT 的授权配置示例：

```nginx
http {
    # 启用 auth_request 模块
    server {
        listen 80;
        server_name example.com;

        location / {
            # 调用后端授权服务
            auth_request /auth;

            proxy_pass http://backend_server;
        }

        # 配置授权服务
        location = /auth {
            internal;  # 内部接口，不允许外部直接访问
            proxy_pass http://auth_server;  # 后端授权服务地址
            proxy_pass_request_body off;  # 不转发请求体
            proxy_set_header Content-Length "";
            proxy_set_header X-Original-URI $request_uri;
        }
    }
}
```

• `auth_request /auth`：将所有请求转发到`/auth`路径进行授权。
• `proxy_pass http://auth_server`：授权服务的地址，通常是一个验证JWT的服务。

3.综合配置
将限流和授权功能结合在一起，可以实现更全面的流量控制和安全保护：

```nginx
http {
    limit_req_zone $binary_remote_addr zone=req_limit:10m rate=10r/s;
    limit_conn_zone $binary_remote_addr zone=conn_limit:10m;

    server {
        listen 80;
        server_name example.com;

        location / {
            auth_request /auth;
            limit_req zone=req_limit burst=20 nodelay;
            limit_conn conn_limit 5;

            proxy_pass http://backend_server;
        }

        location = /auth {
            internal;
            proxy_pass http://auth_server;
            proxy_pass_request_body off;
            proxy_set_header Content-Length "";
            proxy_set_header X-Original-URI $request_uri;
        }
    }
}
```

通过上述配置，Nginx可以实现与Spring Cloud Gateway类似的限流和授权功能，保护后端服务免受过多请求压力和未授权访问。

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


