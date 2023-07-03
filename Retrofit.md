# Retrofit



Java doc

https://square.github.io/retrofit/2.x/retrofit/


Body
Call
CallAdapter
CallAdapter.Factory
Callback
Converter
Converter.Factory
DELETE
Field
FieldMap
FormUrlEncoded
GET
HEAD
Header
HeaderMap
Headers
HTTP
HttpException
Invocation
Multipart
OPTIONS
Part
PartMap
PATCH
Path
POST
PUT
Query
QueryMap
QueryName
Response
Retrofit
Retrofit.Builder
SkipCallbackExecutor
Streaming
Tag
Url


retrofit是基于OkHttp 的封装


转换器
http request body
response body
retrofit2.Converter 接口 

主要分析以下几个框架
HttpClient
HttpURLConnection
Volley
OkHttp
Retrofit

RxJava+Retrofit+OkHttp

https://github.com/square/retrofit

Retrofit requires at minimum Java 8+ or Android API 21+.

### 用法
新建接口
public interface IBeanService {
    @GET("show")
    Call<Bean> getMenuById(@Query("id") String id);
}


retrofit2.Retrofit retrofit = new retrofit2.Retrofit.Builder()
                .baseUrl("http://www.tngou.net/api/food/")
                .addConverterFactory(GsonConverterFactory.create())
                .build();
         IBeanService service = retrofit.create(IBeanService.class);



### Retrofit VS feign


https://blog.csdn.net/choi2016/article/details/54974137



https://zhuanlan.zhihu.com/p/384451261

Feign 通过给我们定义的目标接口（比如例子中的 GitHub）生成一个 HardCodedTarget 类型的代理对象，由 JDK 动态代理实现，生成代理的时候会根据注解来生成一个对应的 Map<Method, MethodHandler>，这个 Map 被 InvocationHandler 持有，接口方法调用的时候，进入 InvocationHandler 的 invoke 方法（为什么会进入这里？JDK 动态代理的基础知识）。

然后根据调用的方法从 Map<Method, MethodHandler> 获取对应的 MethodHandler，然后通过 MethodHandler 根据指定的 client 来完成对应处理， MethodHandler 中的实现类 DefaultMethodHandler 处理默认方法（接口的默认方法）的请求处理的，SynchronousMethodHandler 实现类是完成其它方法的 HTTP 请求的实现，这就是 Feign 的主要核心流程


spring boot与retrofit

https://gitee.com/edidada/testspringbootretrofit

