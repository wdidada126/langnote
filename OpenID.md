# OpenID

OIDC基础
简要而言，OIDC是一种安全机制，用于应用连接到身份认证服务器（Identity Service）获取用户信息，并将这些信息以安全可靠的方法返回给应用。

在最初，因为OpenID1/2经常和OAuth协议（一种授权协议）一起提及，所以二者经常被搞混。

OpenID是Authentication，即认证，对用户的身份进行认证，判断其身份是否有效，也就是让网站知道“你是你所声称的那个用户”；
OAuth是Authorization，即授权，在已知用户身份合法的情况下，经用户授权来允许某些操作，也就是让网站知道“你能被允许做那些事情”。
由此可知，授权要在认证之后进行，只有确定用户身份只有才能授权。
(身份验证)+ OAuth 2.0 = OpenID Connect


链接：https://www.jianshu.com/p/be7cc032a4e9


https://zhuanlan.zhihu.com/p/95064385

