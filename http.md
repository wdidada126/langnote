# http

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



