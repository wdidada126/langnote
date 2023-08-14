# httpcomponents





```xml
<dependency>
    <groupId>org.apache.httpcomponents</groupId>
    <artifactId>httpclient</artifactId>
    <version>4.5.13</version>
</dependency>
```



http-client依赖http-core



```xml
    <dependency>
      <groupId>org.apache.httpcomponents</groupId>
      <artifactId>httpcore</artifactId>
    </dependency>
    <dependency>
      <groupId>org.apache.httpcomponents</groupId>
      <artifactId>httpcore-nio</artifactId>
    </dependency>
    <dependency>
```

http-client 4.5 依赖http-core 4.4



http://hc.apache.org/httpcomponents-client

[Overview (Apache HttpCore 4.4.16 API)](https://hc.apache.org/httpcomponents-core-4.4.x/current/httpcore/apidocs/)





[Overview (Apache HttpClient 4.5.14 API)](https://hc.apache.org/httpcomponents-client-4.5.x/current/httpclient/apidocs/)



httpcomponents.xlsx



## org.apache.http.auth

### org.apache.http.auth.params



## org.apache.http.client





| org.apache.http.client          |           |         |
| ------------------------------- | --------- | ------- |
| AuthCache                       |           |         |
| AuthenticationHandler           |           |         |
| AuthenticationStrategy          |           |         |
| BackoffManager                  |           |         |
| ConnectionBackoffStrategy       |           |         |
| CookieStore                     |           |         |
| CredentialsProvider             |           |         |
| HttpClient                      | interface | 核心api |
| HttpRequestRetryHandler         |           |         |
| RedirectHandler                 |           |         |
| RedirectStrategy                |           |         |
| RequestDirector                 |           |         |
| ResponseHandler                 |           |         |
| ServiceUnavailableRetryStrategy |           |         |
| UserTokenHandler                |           |         |
|                                 |           |         |
| Exceptions                      |           |         |
|                                 |           |         |
| CircularRedirectException       |           |         |
| ClientProtocolException         |           |         |
| HttpResponseException           |           |         |
| NonRepeatableRequestException   |           |         |
| RedirectException               |           |         |



### org.apache.http.client.config





| org.apache.http.client.config |      |      |
| ----------------------------- | ---- | ---- |
| AuthSchemes                   |      |      |
| CookieSpecs                   |      |      |
| RequestConfig                 |      |      |
| RequestConfig.Builder         |      |      |



### org.apache.http.client.entity



### org.apache.http.client.methods



### org.apache.http.client.params



### org.apache.http.client.protocol





### org.apache.http.client.utils





## org.apache.http.conn

org.apache.http.conn.params

org.apache.http.conn.routing

org.apache.http.conn.scheme

org.apache.http.conn.socket

org.apache.http.conn.ssl

org.apache.http.conn.util

## org.apache.http.cookie

org.apache.http.cookie.params



## org.apache.http.impl



org.apache.http.impl.auth

### org.apache.http.impl.client



| org.apache.http.impl.client            |      |      |
| -------------------------------------- | ---- | ---- |
| AbstractAuthenticationHandler          |      |      |
| AbstractHttpClient                     |      |      |
| AbstractResponseHandler                |      |      |
| AIMDBackoffManager                     |      |      |
| AutoRetryHttpClient                    |      |      |
| BasicAuthCache                         |      |      |
| BasicCookieStore                       |      |      |
| BasicCredentialsProvider               |      |      |
| BasicResponseHandler                   |      |      |
| ClientParamsStack                      |      |      |
| CloseableHttpClient                    |      |      |
| ContentEncodingHttpClient              |      |      |
| CookieSpecRegistries                   |      |      |
| DecompressingHttpClient                |      |      |
| DefaultBackoffStrategy                 |      |      |
| DefaultClientConnectionReuseStrategy   |      |      |
| DefaultConnectionKeepAliveStrategy     |      |      |
| DefaultHttpClient                      |      |      |
| DefaultHttpRequestRetryHandler         |      |      |
| DefaultProxyAuthenticationHandler      |      |      |
| DefaultRedirectHandler                 |      |      |
| DefaultRedirectStrategy                |      |      |
| DefaultRequestDirector                 |      |      |
| DefaultServiceUnavailableRetryStrategy |      |      |
| DefaultTargetAuthenticationHandler     |      |      |
| DefaultUserTokenHandler                |      |      |
| EntityEnclosingRequestWrapper          |      |      |
| FutureRequestExecutionMetrics          |      |      |
| FutureRequestExecutionService          |      |      |
| HttpAuthenticator                      |      |      |
| HttpClientBuilder                      |      |      |
| HttpClients                            |      |      |
| HttpRequestFutureTask                  |      |      |
| IdleConnectionEvictor                  |      |      |
| LaxRedirectStrategy                    |      |      |
| NoopUserTokenHandler                   |      |      |
| NullBackoffStrategy                    |      |      |
| ProxyAuthenticationStrategy            |      |      |
| ProxyClient                            |      |      |
| RedirectLocations                      |      |      |
| RequestWrapper                         |      |      |
| RoutedRequest                          |      |      |
| StandardHttpRequestRetryHandler        |      |      |
| SystemDefaultCredentialsProvider       |      |      |
| SystemDefaultHttpClient                |      |      |
| TargetAuthenticationStrategy           |      |      |
|                                        |      |      |
| TunnelRefusedException                 |      |      |









org.apache.http.impl.conn

org.apache.http.impl.conn.tsccm

org.apache.http.impl.cookie

org.apache.http.impl.execchain
