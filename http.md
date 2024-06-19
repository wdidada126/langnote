# http

统一资源标识符（URI）和统一资源定位符（URL）在定义、用途和结构上存在一定的区别。以下是关于它们之间区别的详细解释和举例：

定义和用途：
URI（Uniform Resource Identifier）：统一资源标识符是用于标识互联网上的资源的字符串序列。URI是一个更广义的概念，它不仅涵盖了URL，还包括了用于标识资源的其他形式，如URN（统一资源名称）。URI的目标是通过唯一标识符来命名和定位资源，而不管它们的位置。
URL（Uniform Resource Locator）：统一资源定位符，也称为网址，是URI的一种特殊类型，用于定位互联网上的资源。URL提供了关于资源在互联网上位置的详细信息，通过协议、域名或IP地址、端口以及资源路径等信息，URL能够唯一确定互联网上的一个资源的位置。
结构和组成：
URI：URI一般由三部分组成，包括①访问资源的命名机制（如URN），②存放资源的主机名，③资源自身的名称，由路径表示。虽然URI包括URL和URN，但URN在实际应用中并未广泛流行，因此目前几乎所有的URI都是URL。
URL：URL由多个部分组成，具体包括①协议（例如HTTP或HTTPS），它指示了网络访问的方式；②域名或IP地址，指示了要访问的目标服务器地址；③端口（有时也包括），它指定了访问服务器上的哪个端口；④资源路径，指示了资源的具体位置和名称。例如，"https://www.example.com/index.html"就是一个URL，它指向了位于"www.example.com"域名下根目录的一个名为"index.html"的文件。
举例说明：
URI例子：由于URN在实际中不常用，这里我们以一个假设的URN为例："urn:isbn:1234567890"。这个URI只提供了关于一本书的国际标准书号（ISBN）的信息，而没有提供该书在互联网上的具体位置。
URL例子："https://www.example.com/index.html"。这个URL明确指出了要访问的协议是HTTPS，服务器地址是"www.example.com"，并且请求的资源位于该服务器的根目录下，名为"index.html"。
总结来说，URI是一个更广泛的概念，用于标识互联网上的资源，而URL则是URI的一种特殊类型，专门用于定位这些资源。在实际应用中，URL更为常见和实用。

Origin refer
Host

Access-Control-Allow-Headers，并且不能为 *
Access-Control-Allow-Origin，并且不能为 *
Access-Control-Allow-Credentials 为 true
Access-Control-Allow-
ACA

请求方法有多种，各方法的作用如下。
GET：请求获取Request-URI所标识的资源；
POST：在Request-URI所标识的资源后附加新的提交数据；
HEAD：请求获取由Request-URI所标识的资源的响应消息报头；
PUT：请求服务器存储一个资源，并用Request・URI作为其标识；
DELETE：请求服务器删除Request-URI所标识的资源；
TRACE：请求服务器回送收到的请求信息，主要用于测试或诊断：
CONNECT：保留将来使用；
OPTIONS：请求查询服务器的性能，或者查询与资源相关的选项和需求。



### http rfc

好几个rfc文档吧
鉴权 授权


apache http client
https://hc.apache.org/httpcomponents-client-5.1.x/index.html

Set-Cookie

返回响应头



Content-Type application/octet-stream


application/imgs?



Content-disposition 是 MIME 协议的扩展，MIME 协议指示 MIME 用户代理如何显示附加的文件。Content-disposition其实可以控制用户请求所得的内容存为一个文件的时候提供一个默认的文件名，文件直接在浏览器上显示或者在访问时弹出文件下载对话框。
格式说明： content-disposition = "Content-Disposition" ":" disposition-type *( ";" disposition-parm ) 
字段说明：Content-Disposition为属性名disposition-type是以什么方式下载，如attachment为以附件方式下载disposition-parm为默认保存时的文件名服务端向客户端游览器发送文件时，如果是浏览器支持的文件类型，一般会默认使用浏览器打开，比如txt、jpg等，会直接在浏览器中显示，如果需要提示用户保存，就要利用Content-Disposition进行一下处理，关键在于一定要加上attachment：



```java
        response.setHeader("Content-Type", "application/octet-stream");
        response.setHeader("Content-Disposition","attachment;filename="+s);
```



在电脑领域里，一个octet是指八个比特（bit）为一组的单位，中文称作八字节。
octet-stream指任意类型的二进制流数据。



HTTP origin refer

1. Host
描述请求将被发送的目的地，包括，且仅仅包括域名和端口号。
在任何类型请求中，request都会包含此header信息。
2. Origin
用来说明请求从哪里发起的，包括，且仅仅包括协议和域名。
这个参数一般只存在于CORS跨域请求中，可以看到response有对应的header：Access-Control-Allow-Origin。
3. Referer
告知服务器请求的原始资源的URI，其用于所有类型的请求，并且包括：协议+域名+查询参数（注意，不包含锚点信息）。
因为原始的URI中的查询参数可能包含ID或密码等敏感信息，如果写入referer，则可能导致信息泄露。


https://developer.mozilla.org/zh-CN/docs/Web/HTTP/CORS

[Http请求中Content-Type](https://www.cnblogs.com/klb561/p/10090540.html)

[ietf http 2.0 翻译](https://blog.csdn.net/violet_chengxiao/article/details/45335905)


https://www.ietf.org/blog/http-20/


对比起算法和数据结构来说，前端忽略 HTTP 的后果更严重。有时间的话，建议读 RFC 2616，至少挑重点来读。还有时间可以看看 Roy Fielding 那篇关于 REST 的论文


```
<html>
119524-<head><title>413 Request Entity Too Large</title></head>
119525-<body bgcolor="white">
119526-<center><h1>413 Request Entity Too Large</h1></center>
119527-<hr><center>nginx</center>
119528-</body>
119529-</html>
```

实际上从 2013 年底起，携程内主要使用的就是基于 HTTP 协议的 SOA 微服务框架。这个框架是携程内部自行研发的，整体架构在这近 6 年中没有进行大的重构。受到当初设计的限制，框架本身的扩展性不是很好，使得用户要想自己扩展一些功能就会比较困难。另外，由于 HTTP 协议一个连接同时只能处理一个请求。在高并发的情况下，服务端的连接数和线程池等资源都会比较紧张，影响到请求处理的性能。



HTTP 协议一个连接同时只能处理一个请求

连接-请求-连接断开
处理完请求之后连接就会断开



[携手Chrome与Firefox：Cloudflare宣布全力支持HTTP/3新协议](https://www.cnbeta.com/articles/tech/894021.htm)

port 80001超过范围
http port 80001超过范围，正常范围是多少？
在 TCP/IP 协议中，端口号是用于标识进程或应用程序的一个 16 位无符号整数。在 HTTP 协议中，默认的端口号是 80，也可以使用其他端口号来访问 Web 服务器。
在常见的操作系统中，端口号的取值范围是从 0 到 65535。其中，0 到 1023 的端口号被称为系统端口或者知名端口，一般被用于标准服务的协议，如 HTTP（80）、FTP（21）、SSH（22）等。1024 到 49151 的端口号被称为注册端口或者用户端口，一般被用于网络应用程序。49152 到 65535 的端口号被称为动态端口或者私有端口，一般被用于客户端程序或者临时服务。
因此，端口号 80001 超出了合法的端口号取值范围，不是一个合法的端口号。如果需要使用端口号来标识 Web 服务器，建议使用合法的端口号，如 80 或者其他未被占用的用户端口。

通过Netty学习http2 http3

http get传参
localhost:3000/?query=a&a=b



http post ?query=a&a=b 用法也是可以的



url encoded



http response
head

Set-Cookie-----AUTHSESSID=8ee39f094483; HttpOnly;Secure;


https://blog.csdn.net/HeatDeath/article/details/79186209
Referer的正确英语拼法是referrer
HTTP来源地址（referer，或 HTTP referer）是HTTP表头的一个字段，用来表示从哪儿链接到目前的网页，采用的格式是URL。换句话说，借着HTTP来源地址，目前的网页可以检查访客从哪里而来，这也常被用来对付伪造的跨网站请求。

Referer: http://192.168.159.166/ac_portal/addisclaimer/pc.html?template=addisclaimer&tabs=pwd&vlanid=0&urlip=192.168.1.174&_ID_=6106&switch_url=&url=http://qq.com/&tdsourcetag=s_pctim_aiomsg

multipart/form-data
boundary

```

POST / HTTP/1.1
User-Agent: PostmanRuntime/7.19.0
Accept: */*
Cache-Control: no-cache
Postman-Token: 6488f7fd-2584-40e3-a303-fb666b2a7e64
Host: 127.0.0.1:8010
Content-Type: multipart/form-data; boundary=--------------------------563248598015743970708403
Accept-Encoding: gzip, deflate
Content-Length: 265
Connection: keep-alive

----------------------------563248598015743970708403
Content-Disposition: form-data; name="q"

q
----------------------------563248598015743970708403
Content-Disposition: form-data; name="a"

aaaaaaaa
----------------------------563248598015743970708403--



```



先有rpc，再有http

rpc在内网网络调用

http用于web

restful graphql 基于http

http2增强



http返回参数key

server



http协议实现框架：

java spingmvc webx

python fingle

c++ pistache

go 

rust 



有测试的，针对不同语言的web框架

web是计算机程序的对外接口


Bearer Token、JWT Bearer、Basic Auth 和 Digest Auth 都是在 Web 应用程序中进行身份验证的常见方式，它们之间有以下区别：

1. Bearer Token：Bearer Token 是一种用于 OAuth 2.0 授权的身份验证机制，它使用一个访问令牌来验证用户身份。Bearer Token 通常用于客户端与服务器之间的身份验证，它使用 HTTP 头部字段 `Authorization` 带上访问令牌进行身份验证。Bearer Token 机制相对简单，但安全性较低，因为访问令牌可以被截获并被恶意使用。
2. JWT Bearer：JWT Bearer 是一种使用 JSON Web Token（JWT）进行身份验证的机制。JWT Bearer 机制使用 JWT 作为访问令牌，并使用 HTTP 头部字段 `Authorization` 带上 JWT 进行身份验证。相对于 Bearer Token，JWT Bearer 机制更加安全，因为 JWT 可以被加密和签名，从而确保令牌不会被篡改或伪造。
3. Basic Auth：Basic Auth 是一种使用用户名和密码进行身份验证的机制。当使用 Basic Auth 时，客户端将用户名和密码进行 Base64 编码，并将编码后的字符串作为 HTTP 头部字段 `Authorization` 的值传递到服务器进行身份验证。Basic Auth 机制相对简单，但安全性较低，因为用户名和密码是以明文形式传输的，容易被截获并被恶意使用。
4. Digest Auth：Digest Auth 是一种使用摘要算法进行身份验证的机制。当使用 Digest Auth 时，客户端将用户名和密码进行 MD5 摘要，并将摘要结果作为 HTTP 头部字段 `Authorization` 的值传递到服务器进行身份验证。Digest Auth 相对于 Basic Auth 更加安全，因为密码是以摘要形式传输的，而不是以明文形式传输。但 Digest Auth 的实现相对较复杂，并且在某些情况下可能会导致性能问题。
