# HTTP权威指南

[HTTP权威指南](https://book.douban.com/subject/10746113/)

http实验

chrome浏览器 开发者模式，看接口
Postman工具发起http请求
Wireshark抓包

sessionid
重点看http是如何基于tcp这一可靠连接来进行通信的

request/reponse来的

## 第一部分　HTTP：Web 的基础
### 第1 章　HTTP 概述

URI

URL

URN

### 第2 章　URL 与资源


### 第3 章　HTTP 报文





### 第4章 　连接管理 

TCP


keep-alive?


## 第二部分　HTTP 结构

### 第5 章　Web 服务器





### 第6 章　代理

Via 首部

TRACE 方法

Allow 首部



### 第7 章　缓存
etag
缓存是指将经常访问的数据保存在临时存储器中，以便下次访问时能够更快地获取数据的过程。缓存可以有效地提高应用程序的性能，减少对后端资源的访问，降低系统的负载压力。

在 Web 应用程序中，缓存机制是通过 HTTP 协议中的缓存头来实现的。其中，ETag 是一种常用的缓存头之一，它用于标识资源的版本号，可以帮助客户端判断资源是否发生了变化，从而决定是否需要重新获取资源。

ETag（Entity Tag）是一个字符串，用于标识资源的版本号。服务器在响应客户端请求时，会将资源的 ETag 值作为响应头返回。客户端在下一次请求同一资源时，可以将上一次获取到的 ETag 值作为请求头中的 If-None-Match 字段发送给服务器，服务器会根据该值判断资源是否发生了变化。如果资源未发生变化，服务器会返回 304 Not Modified 响应码，告诉客户端可以使用缓存的资源；如果资源已发生变化，服务器会返回新的资源和新的 ETag 值，客户端会使用新的资源并更新缓存。

下面是一个使用 ETag 缓存的示例代码：

```java
@RequestMapping("/api/user/{id}")
@ResponseBody
public User getUser(@PathVariable("id") Long id, HttpServletRequest request, HttpServletResponse response) {
    User user = userService.getUserById(id);
    String etag = "\"" + user.getVersion() + "\""; // 使用版本号生成 ETag 值
    response.setHeader("ETag", etag); // 设置响应头中的 ETag
    String ifNoneMatch = request.getHeader("If-None-Match"); // 获取请求头中的 If-None-Match
    if (ifNoneMatch != null && ifNoneMatch.equals(etag)) {
        response.setStatus(HttpStatus.NOT_MODIFIED.value()); // 如果资源未变化，返回 304 Not Modified
        return null;
    }
    return user;
}
```

在上面的代码中，我们在控制器中定义了一个 getUser() 方法，用于获取指定用户的信息。在方法中，我们通过调用 userService.getUserById() 方法获取用户信息，并使用版本号生成 ETag 值。然后，我们将 ETag 值设置到响应头中，并获取请求头中的 If-None-Match 值。如果 If-None-Match 和当前的 ETag 值相同，说明资源未发生变化，我们返回 304 Not Modified 响应码；否则，我们返回用户信息并更新 ETag 值。

需要注意的是，使用 ETag 缓存可以有效地减少网络流量和服务器负载，但也会增加一定的计算和存储开销。因此，需要根据实际情况权衡使用 ETag 缓存的利弊，并结合其他缓存机制一起使用，以达到最佳的性能和可靠性的平衡。



### 第8 章　集成点：网关隧道及中继



### 第9 章　Web 机器人





### 第10 章　HTTP-NG





## 第三部分　识别、认证与安全
### 第11 章　客户端识别与cookie 机制

### 第13 章　摘要认证



### 第14 章　安全HTTP



## 第四部分　实体、编码和国际化


### 第15章 　实体和编码 





### 第16 章　国际化



### 第17 章　内容协商与转码



## 第五部分　内容发布与分发
### 第18 章　Web 主机托管



### 第19 章　发布系统



### 第20 章　重定向与负载均衡



### 第21 章　日志记录与使用情况跟踪
