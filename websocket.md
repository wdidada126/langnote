# WebSocket



- javawebsocketserver
- javawebsocketclient





```js
var wsUri = "ws://${pageContext.request.serverName}:${pageContext.request.localPort}/wscpu.ws";
```


#### 拥抱HTTP2.0





[七种WebSocket框架的性能比较](https://www.sohu.com/a/134240630_466839)





Netty：http://netty.io/

Undertow：http://undertow.io/





基于netty搭建websocket，实现消息的主动推送

https://www.jianshu.com/p/56216d1052d7


Nginx支持WebSocket反向代理-学习小结

https://www.cnblogs.com/kevingrace/p/9512287.html

https://github.com/facundofarias/awesome-websockets


Java
Project Tyrus - JSR 356: Java API for WebSocket - Reference Implementation.
Java-WebSocket - Barebones WebSocket client and server implementation written in 100% Java.
Atmosphere - Realtime Client Server Framework for the JVM, supporting WebSockets with Cross-Browser Fallbacks.
Webbit - Java event based WebSocket and HTTP server.



websocket http区别

https://www.cnblogs.com/goeasycloud/p/9355164.html





curl --include \
     --no-buffer \
     --header "Connection: Upgrade" \
     --header "Upgrade: websocket" \
     --header "Host: http://127.0.0.1:8030/" \
     --header "Origin: http://127.0.0.1:8030/" \
     --header "Sec-WebSocket-Key: SGVsbG8sIHdvcmxkIQ==" \
     --header "Sec-WebSocket-Version: 13" \
     http://127.0.0.1:8030/





spring-websocket




[No suitable default RequestUpgradeStrategy found](https://blog.csdn.net/u013630932/article/details/76030271)



Spring-websocket github repo运行

ws路径没注册



web网页登录正常



以前并发量不大，http这种严格client发起，server响应的模式可以满足需要

现在访问量大

所以重复使用网络连接，server client相互通信，产生websocket


