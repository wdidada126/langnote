# oauth

https://accounts.google.com/o/oauth2/auth/oauthchooseaccount?login_hint&prompt=login&response_type=code&redirect_uri=https%3A%2F%2Fauth0.openai.com%2Flogin%2Fcallback&scope=email%20profile&state=ZRFM0n5a9Zaa_gLCLJpjvmhdHT4XVseu&client_id=799222349882-ne3i0s9jdm5s0p7ll2d7tlsi1vc1halt.apps.googleusercontent.com&service=lso&o2v=1&flowName=GeneralOAuthFlow

openai_google_oauth.png


OAuth 2.0 是目前最流行的授权机制，用来授权第三方应用，获取用户数据。

http://www.ruanyifeng.com/blog/2019/04/oauth_design.html
https://datatracker.ietf.org/doc/html/rfc6749

简单说，OAuth 就是一种授权机制。数据的所有者告诉系统，同意授权第三方应用进入系统，获取这些数据。系统从而产生一个短期的进入令牌（token），用来代替密码，供第三方应用使用。
令牌（token）与密码（password）的作用是一样的，都可以进入系统，但是有三点差异。
（1）令牌是短期的，到期会自动失效，用户自己无法修改。密码一般长期有效，用户不修改，就不会发生变化。
（2）令牌可以被数据所有者撤销，会立即失效。以上例而言，屋主可以随时取消快递员的令牌。密码一般不允许被他人撤销。
（3）令牌有权限范围（scope），比如只能进小区的二号门。对于网络服务来说，只读令牌就比读写令牌更安全。密码一般是完整权限。

也就是说，OAuth 2.0 规定了四种获得令牌的流程。你可以选择最适合自己的那一种，向第三方应用颁发令牌。下面就是这四种授权方式。

授权码（authorization-code）
隐藏式（implicit）
密码式（password）：
客户端凭证（client credentials）



1、https://b.com/oauth/authorize?response_type=code
一共有4步，第三步会发送https://b.com/oauth/token?grant_type=authorization_code
2、https://b.com/oauth/authorize?response_type=token
3、https://oauth.b.com/token?grant_type=password
4、https://oauth.b.com/token?grant_type=client_credentials

https://www.ruanyifeng.com/blog/2019/04/oauth-grant-types.html


https://oauth.net/2/

https://tools.ietf.org/html/rfc6749

理解OAuth 2.0 https://www.ruanyifeng.com/blog/2014/05/oauth_2_0.html

https://github.com/oauth-xx/oauth2

https://www.digitalocean.com/community/tutorials/an-introduction-to-oauth-2



oauth2协议中文翻译

http://ifeve.com/oauth2-tutorial-all/



oauth

https://zhuanlan.zhihu.com/p/338815329





1. 微信怎么把“登录成功”这件事情告诉【支浩宇粉丝后援会】APP？
2. 微信怎么把“具体是哪个用户登录了”这个用户的值，传给【支浩宇粉丝后援会】APP？

**回调地址+code**解决的是第1个问题。**code+token**解决的是第二个问题。



code只能被消费一次

token会定时过期？





[oauth2 java 代码示例](https://www.cnblogs.com/cxygg/p/9504171.html)



有JWT为什么还要用oAuth2.0来做登入和权限认证呢？
oauth2是一个行业标准的授权协议, 包含一系列流程和标准
你把token的形式和授权认证协议二者搞混了
oauth2是一个行业标准的授权协议, 包含一系列流程和标准
jwt只是指Json web token,  只是一种token的形式
你可以在使用oauth2流程的时候授权一个jwt形式的token, 也可以使用其它形式的token, bearer token, mac token等等
你也可以不用oauth2流程, 在自己的授权流程里使用jwt

FavOAuth2



## github repo OAuth2-SSO

使用说明 
    http://localhost:19888/swagger-ui.html查看接口文档

1. 获取code  
    访问http://localhost:19888/oauth2/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&state={state}

2. 输入账号admin 密码!QAZ2wsx 提交    
3. 系统回调{redirect_uri}?code={code}&state={state}    
    >1 2 3 步骤示例：  
    访问 http://localhost:19888/oauth2/authorize?response_type=code&client_id=system&redirect_uri=http://baidu.com    这个参数写在数据库里面
    返回 http://baidu.com?code=****************   

   http://localhost:19888/oauth2/authorize?response_type=code&client_id=system123&redirect_uri=myweb.com&state=2 点击，返回
   http://localhost:19888/oauth2/myweb.com?code=d32e9483e09546f270290627bd3b4a18&state=2 这个是错误的例子

4. 获取token  
    根据回调返回code，post方式调用http://localhost:19888/oauth2/accessToken接口返回token信息  
    注意：Content-Type=application/x-www-form-urlencoded  
    >示例参数:  
    header配置Content-Type=application/x-www-form-urlencoded  
    [{"key":"client_id","value":"system","description":""},{"key":"client_secret","value":"system","description":""},{"key":"grant_type","value":"authorization_code","description":""},{"key":"code","value":"77c9c36b1d9ef13f366d20f47789c80b","description":""},{"key":"redirect_uri","value":"http://baidu.com","description":""}]        
5. 获取用户信息    
    get方式请求http://localhost:19888/user/info?access_token={access_token}获取用户信息    
    >示例:  
    http://localhost:19888/user/info?access_token=****************  
    或者  
    也可将token信息放入header中 设置Authorization=Bearer{access_token}  get请求http://localhost:19888/user/info  
6. 用户登出  
    访问http://localhost:19888/user/revoke 登出账号  



申请auth



oltu、cxf、spring security实现了oauth2

https://blog.csdn.net/u013435893/article/details/79735097



2013年之后，就没有oauth1了，用oauth2





不建议基于oatuh2实现sso. ??
sso可以使用cas实现



https://zhuanlan.zhihu.com/p/25007591