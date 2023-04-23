# jwt



token，是一个字符串
例子：eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJKb2UifQ.1KP0SsvENi7Uz1oQc07aXTL7kpQG5jBNIybqr60AlD4


### jwt vs redis+token
JWT: 生成并发给客户端之后，后台是不用存储，客户端访问时会验证其签名、过期时间等再取出里面的信息（如username），再使用该信息直接查询用户信息完成登录验证。jwt自带签名、过期等校验，后台不用存储，缺陷是一旦下发，服务后台无法拒绝携带该jwt的请求（如踢除用户）；
token+redis： 是自己生成个32位的key，value为用户信息，访问时判断redis里是否有该token，如果有，则加载该用户信息完成登录。服务需要存储下发的每个token及对应的value，维持其过期时间，好处是随时可以删除某个token，阻断该token继续使用
JWT 适用场景：无状态的 API：JWT 在无状态的 API 上非常有用，因为服务器不需要存储任何会话信息，这可以轻松地扩展系统。跨域身份验证：由于 JWT 是通过客户端传递的，因此它可以轻松实现跨域身份验证，避免了 CORS 问题。微服务架构：在微服务架构中，各个服务可以相互独立验证 JWT，减少了内部服务通信的复杂性。JWT 不适用场景：需要立即废弃访问权限的场景：由于 JWT 的生命周期无法由服务器控制，因此在需要立即废弃某个用户的访问权限时（例如：踢除用户、安全漏洞等），JWT 不是最佳选择。Token+Redis 适用场景：需要实时控制会话状态的系统：由于服务器存储了每个 token，可以随时废弃或修改某个 token，因此在需要实时控制会话状态的系统中，Token+Redis 更为合适。需要缓存用户信息：在某些系统中，为了减少对数据库的访问，可以将用户信息存储在 Redis 中，这种情况下，Token+Redis 方案更具优势。

https://www.zhihu.com/question/274566992/answer/2994761733



JWS 也就是 Json Web Signature，是构造 JWT 的基础结构（JWT 其实涵盖了 JWS 和 JWE 两类，其中 JWT 的载荷还可以是嵌套的 JWT
https://www.cnblogs.com/read-the-spring-and-autumn-annals-in-night/p/12041911.html


```java
     byte[] header = java.util.Base64.getDecoder().decode("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9");
     System.out.println(new String(header));
```

```shell
{"alg":"HS256","typ":"JWT"}
```

Base64 有三个字符`+`、`/`和`=`，在 URL 里面有特殊含义，所以要被替换掉：`=`被省略、`+`替换成`-`，`/`替换成`_` 。这就是 Base64URL 算法。

http://www.ruanyifeng.com/blog/2018/07/json_web_token-tutorial.html



https://github.com/Thalhammer/jwt-cpp

JJWT是纯Java实现 android的
https://www.jianshu.com/p/b5e63a859a30

https://github.com/jwtk/jjwt



Python 生成 JWT(json web token) 及 解析方式
https://www.cnblogs.com/lowmanisbusy/p/10930856.html
itsdangerous

https://gitee.com/edidada/itsdangerous-test


jwtdemo git repo java

跨语言incode/decode

HMSC	RSA	ECDSA	PSS	EdDSA
HS256	RS256	ES256	PS256	Ed25519
HS384	RS384	ES384	PS384	Ed448
HS512	RS512	ES512	PS512	


https://stackoverflow.com/questions/26881296/spring-security-oauth2-full-authentication-is-required-to-access-this-resource

https://segmentfault.com/q/1010000019185053/a-1020000019185166

Authorization: Bearer eyJhbGciOiJIUzI1NiIsI.eyJpc3MiOiJodHRwczotcGxlL.mFrs3Zo8eaSNcxiNfvRh9dqKP4F1cB

HTTP头
Authorization: Bearer 

没有什么为什么，这就是JWT定义的规范: https://jwt.io/introduction/
建议详读上述官方文档。Bearer代表Authorization头定义的schema，https://developer.mozilla.org/en-US/docs/Web/HTTP/Authentication#Authentication_schemes


JWT 的三个部分依次如下。

Header（头部）
Payload（负载）
Signature（签名）

类比http协议

Header
Header 部分是一个 JSON 对象，描述 JWT 的元数据，通常是下面的样子。
`{ "alg": "HS256", "typ": "JWT" }`
上面代码中，alg属性表示签名的算法（algorithm），默认是 HMAC SHA256（写成 HS256）；typ属性表示这个令牌（token）的类型（type），JWT 令牌统一写为JWT。

最后，将上面的 JSON 对象使用 Base64URL 算法转成字符串。

payload可以自定义用户数据

Payload 部分也是一个 JSON 对象，用来存放实际需要传递的数据。JWT 规定了7个官方字段，供选用。
iss (issuer)：签发人
exp (expiration time)：过期时间
sub (subject)：主题
aud (audience)：受众
nbf (Not Before)：生效时间
iat (Issued At)：签发时间
jti (JWT ID)：编号
除了官方字段，你还可以在这个部分定义私有字段，下面就是一个例子。
`{ "sub": "1234567890", "name": "John Doe", "admin": true }`
注意，JWT 默认是不加密的，任何人都可以读到，所以不要把秘密信息放在这个部分。
这个 JSON 对象也要使用 Base64URL 算法转成字符串。

https://github.com/auth0/java-jwt

https://jwt.io/libraries?language=Java




jwt字符串生成 逆向
字符串过期时间 加盐 算法（

字符串例子
eyJ0eXBlIjoiSldUIiwiYWxnIjoiSFMyNTYiLCJ0eXAiOiJKV1QifQ.eyJwYXlsb2FkIjoie1wibmFtZVwiOlwi5byg5LiJXCIsXCJhZ2VcIjpcIjIwXCJ9IiwiZXhwIjoxNjE5Njc3MjU1fQ.OEmfLC4_5qNv_q7wf0-ASMLjk34XeoBkpQaW4xIntY0

有两个符号 .

```shell
com.auth0.jwt.exceptions.TokenExpiredException: The Token has expired on Thu Apr 29 14:20:55 CST 2021.
	at com.auth0.jwt.JWTVerifier.assertDateIsFuture(JWTVerifier.java:441)
	at com.auth0.jwt.JWTVerifier.assertValidDateClaim(JWTVerifier.java:432)
	at com.auth0.jwt.JWTVerifier.verifyClaims(JWTVerifier.java:373)
	at com.auth0.jwt.JWTVerifier.verify(JWTVerifier.java:355)
	at cn.wdidada.test.jwtdemo.JWTKit.unsign(JWTKit.java:57)
	at cn.wdidada.test.jwtdemo.JWTKit.main(JWTKit.java:79)
```


eyJ0eXBlIjoiSldUIiwiYWxnIjoiSFMyNTYiLCJ0eXAiOiJKV1QifQ.eyJwYXlsb2FkIjoie1wibmFtZVwiOlwi5byg5LiJXCIsXCJhZ2VcIjpcIjIwXCJ9IiwiZXhwIjo2MTU4MDQ0ODAwMH0.FGjDDAn6PvJdJRBUXbIFqKvEg48wOnsdbHCkdIZd_fA


no suitable constructor found, can not deserialize from Object value (missing default constructor or

User 是内部类







https://www.codenong.com/cs106759642/



https://www.cnblogs.com/shihaiming/p/9565835.html



典型用法

实用场景
