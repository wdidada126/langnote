# OkHTTP



testokhttp


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
- 
- 
- 


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
