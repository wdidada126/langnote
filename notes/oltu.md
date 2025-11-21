# oltu

springboot_oltu_oauth2

github repo

Oltu在Jersey框架上实现oauth2.0授权模块

https://oltu.apache.org/
https://attic.apache.org/projects/oltu.html
2018 oltu move to Attic

Apache Oltu moved into the Attic in April 2018. Apache Oltu is an OAuth protocol implementation in Java. It also covers others "OAuth family" related implementations such as JWT, JWS and OpenID Connect

OAuth 2实战


https://cwiki.apache.org/confluence/display/OLTU/OAuth+2.0+Client+Demo

windows 10电脑下载了

oltu_demo_urls.png


https://www.cnblogs.com/huanglin101/p/8334208.html


/login：登录接口
/Oauth/authorize:获取授权码的接口
/Oauth/getCode:这个其实就是授权码接口，只是例子中后端没有存储登录状态，做了个中转
/Oauth/accesstoken:获取访问令牌


https://www.cnblogs.com/jdluojing/p/4201729.html

认证服务器的返回是通过重定向实现的

为什么oauth2中的授权码模式 在获取token之前非要先到资源服务器获取一个code 然后才使用资源服务器的code去资源服务器去申请token?
看了很多资料说是因为 用户在确认授权之后 资源服务器会跳转到我们指定的一个回调url, 如果直接返回token的话，谁都可以在浏览器中看到这个token 那就没有安全性可言了

OAuth全称Open Authentication
qq登录是不是用Oauth 2

https://blog.csdn.net/Fishermen_sail/article/details/128850396


授权码模式（Authorization Code）是 OAuth 功能最齐全、流程最严谨，也是最常用的授权模式。假设我们要用微信账号登录网易云音乐，需要以下五步： 1. 访问网易云音乐客户端，客户端跳转到微信授权页面，询问用户是否同意授权，微信会提供授权的URL。用户选择是否同意授权假设用户同意授权，微信端将向网易云音乐跳转重定向 URL，同时附上授权码（code）网易云音乐收到授权码后，附上重定向 URL，向微信端申请令牌（token）微信端传回网易云音乐令牌，由此网易云音乐就可以拿着访问令牌访问微信用户信息在用户将微信信息授权给网易云音乐登录后，此时后端开始处理，前端不再参与。此时需要微信的服务器将 token 传给网易云音乐的后端，后端携带 token 去访问被授权的微信信息。在授权成功后，需要重定向 URL 通知用户授权成功，也就是说，建立起微信前端和网易云音乐前端的关联。 code 的作用在于让 token 不经过用户的浏览器直接传递，保护了 token 的安全。因为 code 只能用一次，且有时间限制，超时会失效，所以即使被截也未必能用。 其次，要获得 token，除了需要 code，还需要 client id/client secret。所以即使 code 被盗，也是无法获得 token 的。

总结：一个code授权码，一个token令牌

client_id client_sercurite


oltu 简介:
Apache Oltu是OAuth协议的Java语言实现。它也包含其他oauth 的协议如JWT JWS OpenID ,是apache 基金会提供的开源项目 官网:http://oltu.apache.org/
https://blog.csdn.net/lipingping951462/article/details/53098866

