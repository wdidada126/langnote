# jwt

https://stackoverflow.com/questions/26881296/spring-security-oauth2-full-authentication-is-required-to-access-this-resource

https://segmentfault.com/q/1010000019185053/a-1020000019185166

Authorization: Bearer eyJhbGciOiJIUzI1NiIsI.eyJpc3MiOiJodHRwczotcGxlL.mFrs3Zo8eaSNcxiNfvRh9dqKP4F1cB


没有什么为什么，这就是JWT定义的规范: https://jwt.io/introduction/
建议详读上述官方文档。Bearer代表Authorization头定义的schema，https://developer.mozilla.org/en-US/docs/Web/HTTP/Authentication#Authentication_schemes


JWT 的三个部分依次如下。

Header（头部）
Payload（负载）
Signature（签名）

类比http协议

Header
Header 部分是一个 JSON 对象，描述 JWT 的元数据，通常是下面的样子。
`javascript { "alg": "HS256", "typ": "JWT" }`
上面代码中，alg属性表示签名的算法（algorithm），默认是 HMAC SHA256（写成 HS256）；typ属性表示这个令牌（token）的类型（type），JWT 令牌统一写为JWT。

最后，将上面的 JSON 对象使用 Base64URL 算法（详见后文）转成字符串。

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
javascript { "sub": "1234567890", "name": "John Doe", "admin": true }
注意，JWT 默认是不加密的，任何人都可以读到，所以不要把秘密信息放在这个部分。
这个 JSON 对象也要使用 Base64URL 算法转成字符串。

