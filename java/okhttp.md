# OkHTTP

okhttp api doc
https://square.github.io/okhttp/4.x/okhttp/okhttp3/

okhttp example

https://github.com/edidada/testokhttp

Platform.get().log(INFO, "Callback failure for " + toLoggableString(), e);

JakeWharton

[插值器 interceptor](https://www.cnblogs.com/hankzhouAndroid/p/8710284.html)

线程池

http的UA是什么

### okio
- Okio

其他类分为读写两类
Input Reader
Output Writer

读

- Source
- BufferedSource
- okio.BufferedSource.readUtf8()

写

- Sink
- BufferedSink
- okio.BufferedSink.writeUtf8(java.lang.String)



AsyncTimeout
Base64
Buffer
BufferedSink
BufferedSource
ByteString
DeflaterSink
ForwardingSink
ForwardingSource
ForwardingTimeout
GzipSink
GzipSource
HashingSink
HashingSource
InflaterSource
Okio
Options
package-info
PeekSource
Pipe
PushableTimeout
RealBufferedSink
RealBufferedSource
Segment
Segmented ByteString
SegmentPool
Sink
Source
Timeout
Utf8
Util

https://www.cnblogs.com/could-deng/p/8378796.html

### java 自带log 写进testjdk8

Level

```shell
    Logger logger = Logger.getLogger(LoggerTest.class.getSimpleName());
    logger.log(Level.WARNING, "Failed to close timed out socket ", e);
```

sink 下沉
deflater 放气阀

Timeout (okio)
    AsyncTimeout (okio)
    ForwardingTimeout (okio)
    PushableTimeout (okio)

- Base64 final类
- Utf8   final类

Pipe

https://blog.csdn.net/p892848153/article/details/51214054

okio 跟nio区别

Netty
https://blog.csdn.net/p892848153/article/details/51214054
https://www.jianshu.com/p/ea3ef6d7f01b
https://www.ctolib.com/okio.html
https://juejin.cn/post/6844903785236545549
https://juejin.cn/post/6844903637668331528
https://www.ucloud.cn/yun/68256.html

https://blog.csdn.net/dmy17356716992/article/details/88690640

java.nio.charset.Charset

```java
MediaType mediaType = MediaType.get("text/plain");
MediaType mediaType = MediaType.parse("text/plain");
```

https://www.w3school.com.cn/media/media_mimeref.asp

RequestBody静态创建方法 本身是抽象方法
okhttp3.RequestBody.create(okhttp3.MediaType, java.io.File)


```shell
java.net.ConnectException: Failed to connect to /192.168.1.228:8101
    at okhttp3.internal.connection.RealConnection.connectSocket(RealConnection.java:265)
    at okhttp3.internal.connection.RealConnection.connect(RealConnection.java:183)
    at okhttp3.internal.connection.ExchangeFinder.findConnection(ExchangeFinder.java:224)
    at okhttp3.internal.connection.ExchangeFinder.findHealthyConnection(ExchangeFinder.java:107)
    at okhttp3.internal.connection.ExchangeFinder.find(ExchangeFinder.java:87)
    at okhttp3.internal.connection.Transmitter.newExchange(Transmitter.java:162)
    at okhttp3.internal.connection.ConnectInterceptor.intercept(ConnectInterceptor.java:41)
    at okhttp3.internal.http.RealInterceptorChain.proceed(RealInterceptorChain.java:142)
    at okhttp3.internal.http.RealInterceptorChain.proceed(RealInterceptorChain.java:117)
    at okhttp3.internal.cache.CacheInterceptor.intercept(CacheInterceptor.java:94)
    at okhttp3.internal.http.RealInterceptorChain.proceed(RealInterceptorChain.java:142)
    at okhttp3.internal.http.RealInterceptorChain.proceed(RealInterceptorChain.java:117)
    at okhttp3.internal.http.BridgeInterceptor.intercept(BridgeInterceptor.java:93)
    at okhttp3.internal.http.RealInterceptorChain.proceed(RealInterceptorChain.java:142)
    at okhttp3.internal.http.RetryAndFollowUpInterceptor.intercept(RetryAndFollowUpInterceptor.java:88)
    at okhttp3.internal.http.RealInterceptorChain.proceed(RealInterceptorChain.java:142)
    at okhttp3.internal.http.RealInterceptorChain.proceed(RealInterceptorChain.java:117)
    at okhttp3.RealCall.getResponseWithInterceptorChain(RealCall.java:221)
    at okhttp3.RealCall.execute(RealCall.java:81)
    at cn.wdidada.test.okhttp.Main.main(Main.java:33)
Caused by: java.net.ConnectException: Connection timed out: connect
    at java.net.DualStackPlainSocketImpl.waitForConnect(Native Method)
    at java.net.DualStackPlainSocketImpl.socketConnect(DualStackPlainSocketImpl.java:85)
    at java.net.AbstractPlainSocketImpl.doConnect(AbstractPlainSocketImpl.java:350)
    at java.net.AbstractPlainSocketImpl.connectToAddress(AbstractPlainSocketImpl.java:206)
    at java.net.AbstractPlainSocketImpl.connect(AbstractPlainSocketImpl.java:188)
    at java.net.PlainSocketImpl.connect(PlainSocketImpl.java:172)
    at java.net.SocksSocketImpl.connect(SocksSocketImpl.java:392)
    at java.net.Socket.connect(Socket.java:606)
    at okhttp3.internal.platform.Platform.connectSocket(Platform.java:130)
    at okhttp3.internal.connection.RealConnection.connectSocket(RealConnection.java:263)
```


get
url带参数的

get
body的

post
- raw
- form-data
File
Text

url-encoded

bin


[HTTP上传数据的方式和OKHttp的实现](https://blog.csdn.net/weixin_40763897/article/details/106806721)


multipart/form-data与x-www-form-urlencoded区别：

multipart/form-data：既可以上传文件等二进制数据，也可以上传表单键值对，只是最后会转化为一条信息；
x-www-form-urlencoded：只能上传键值对，并且键值对都是间隔分开的。



FormBody
对应
    private static final MediaType CONTENT_TYPE = MediaType.parse("application/x-www-form-urlencoded");


只能写入kv对

38
61 对应的ascii码

ExecuterService
ThreadPollExecutor
有自定义线程池

java.util.concurrent.SynchronousQueue

Synchronous
同时发生(或存在)的; 同步的; 共时的;


okhttp3.RealCall.getResponseWithInterceptorChain()

okhttp3.Dispatcher.executorService

- Request
- OkHttpClient
- RequestBody
- Response
- Call
- RealCall
- Transmitter
- Dispatcher

OkHttp是一个开源的HTTP客户端库，它可以用于发送HTTP请求和处理HTTP响应。在OkHttp中，Transmitter是一个关键组件，它负责处理HTTP请求和响应的发送和接收。

具体来说，Transmitter有以下作用：

1. 处理HTTP请求：Transmitter负责将HTTP请求发送到服务器。它负责建立连接、发送请求头和请求体、处理重定向、处理连接池等问题。
2. 处理HTTP响应：Transmitter负责从服务器接收HTTP响应。它会读取响应头和响应体，处理重定向、缓存等问题。
3. 连接池管理：Transmitter维护了一个连接池，用于管理和重用HTTP连接。它可以复用已经建立的连接，从而提高性能。
4. 异步请求处理：Transmitter可以处理异步请求，它会将异步请求加入到异步请求队列中，等待响应结果。
5. 请求取消处理：Transmitter可以处理请求取消操作，它会中断正在进行的请求，并释放相关资源。
总之，Transmitter是OkHttp中负责处理HTTP请求和响应的关键组件，它可以处理HTTP请求和响应、连接池管理、异步请求处理、请求取消处理等问题，是OkHttp的核心组件之一。


BridgeInterceptor (okhttp3.internal.http)
CacheInterceptor (okhttp3.internal.cache)
ConnectInterceptor (okhttp3.internal.connection)
RetryAndFollowUpInterceptor (okhttp3.internal.http)
CallServerInterceptor (okhttp3.internal.http)


okhttp3.Interceptor
    Response intercept(Chain chain) throws IOException;



okhttp3.Interceptor.Chain
    Request request();
    Response proceed(Request request) throws IOException;
    @Nullable Connection connection();
    Call call();
    int connectTimeoutMillis();
    Chain withConnectTimeout(int timeout, TimeUnit unit);
    int readTimeoutMillis();
    Chain withReadTimeout(int timeout, TimeUnit unit);
    int writeTimeoutMillis();
    Chain withWriteTimeout(int timeout, TimeUnit unit);





### Dispatcher类
具体来说，Dispatcher有以下作用：
控制同时执行的请求数量：Dispatcher可以控制同时执行的请求数量，并发控制可以在一定程度上控制网络流量和资源使用。在Dispatcher中，可以通过setMaxRequests()方法设置最大请求数量，通过setMaxRequestsPerHost()方法设置每个主机允许的最大请求数量。
管理异步请求队列：Dispatcher可以管理异步请求队列，它会将异步请求加入到请求队列中，并在空闲连接池时自动启动新请求。当请求队列已满时，Dispatcher会将多余的请求加入到等待队列中，等待其他请求完成后再执行。
处理请求取消操作：Dispatcher可以处理请求取消操作，当请求被取消时，Dispatcher会从等待队列和请求队列中移除该请求，并释放相关资源。


Dispatcher类在

- OkHttpClient.Builder
- RealCall
- WebSocketEcho
- TestTls13Request

中使用






