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

### 第2 章　URL与资源


### 第3 章　HTTP报文





### 第4章 连接管理

## 第二部分　HTTP结构

### 第5章　Web服务器





### 第6章 代理


### 第7章 缓存

### 第8章　集成点：网关隧道及中继



### 第9章 Web机器人

### 第10章 HTTP-NG

## 第三部分　识别、认证与安全
### 第11章　客户端识别与cookie 机制
### 第12章　基本认证机制
### 第13章 摘要认证

### 第14章 安全HTTP

## 第四部分 实体、编码和国际化

### 第15章 　实体和编码

### 第16章　国际化

### 第17章　内容协商与转码

## 第五部分　内容发布与分发
### 第18章　Web 主机托管

### 第19章　发布系统

### 第20章　重定向与负载均衡

### 第21章　日志记录与使用情况跟踪


## 笔记
## 第一部分　HTTP：Web 的基础
### 第1 章　HTTP 概述

URI

URL

URN

### 第2 章　URL与资源


### 第3 章　HTTP报文





### 第4章 连接管理 

TCP


keep-alive?


## 第二部分　HTTP结构

### 第5章　Web服务器





### 第6章 代理

Via 首部

TRACE 方法

Allow 首部



### 第7章 缓存
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



### 第8章　集成点：网关隧道及中继



### 第9章 Web机器人





### 第10章 HTTP-NG





## 第三部分　识别、认证与安全
### 第11章　客户端识别与cookie 机制
### 第12章　基本认证机制
### 第13章 摘要认证



### 第14章 安全HTTP



## 第四部分 实体、编码和国际化


### 第15章 　实体和编码 





### 第16章　国际化



### 第17章　内容协商与转码



## 第五部分　内容发布与分发
### 第18章　Web 主机托管



### 第19章　发布系统



### 第20章　重定向与负载均衡



### 第21章　日志记录与使用情况跟踪

## 跨年摘录（2020–2026 日常笔记聚合，2026-09-23 整理）

### 2025-04
> 学习antlr这个话题很大，你的需求不同，学习的深度也不一样。antlr是一个cc(compiler compiler)，你需要有一点点的编译原理知识，但是相信我真的不需要很多。如果你的文本是确定性的，完全没有语法错误的文本。那么你要做的大概率就是一个反序列化的过程，即把文本变成一个结构化的内存数据。这种情况下，你只需要保证语法、词法的定义即可。如果你是要做一个类似编译器的东西，希望可以像rust一样有比较丰富的报错信息，那么你就需要处理报错相关的内容了，这个时候可以看一下 @zxh404 大佬推荐的《ANTLR 4权威指南》。这本书里面就有介绍，在报错时如何处理（关键词 ErrorListener）

### 2025-10
> ANTLR作者写过两本书，都是很好的学习资料。一本是《编程语言实现模式》，另外一本是《ANTLR 4权威指南》。

