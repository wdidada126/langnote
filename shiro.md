# shiro

testshiro gitee repo

shrio springboot



relam 相当于数据源
Realm即领域，相当于datasource数据源，可以是JDBC实现，也可以是LDAP实现，或者内存实现等等，securityManager进行安全认证需要通过Realm获取用户权限数据


shiro_filter.jpeg

LDAP，Lightweight Directory Access Protocol，轻量级目录访问协议
用户认证
基于 LDAP 做一个认证同样也需要用户名和密码，在这个案例描述中用户名就是 LDAP 中的 DN，因此，假设用户 Tom Riddle 的密码为 123456，你将使用如下方式认证成功：
username: cn=triddle, ou=users, dc=hogwarts, dc=com
password: 123456



Authenticator（认证）
Authorizer（授权）




shiro authc和user的区别
前者是认证过，后者是登录过，如果开启了Readmemberme功能的话，后者也是可以通过的，而前者通过不了。


需要写一个user权限接口的例子





web
认证
Authrization

token
jwt
auth0.

Shiro的AOP横切模式-注解权限控制
https://www.cnblogs.com/BINGJJFLY/p/9066524.html


RequiresPermissions注解
org.apache.shiro.authz.annotation.RequiresPermissions

RequiresAuthentication
RequiresGuest
RequiresPermissions
RequiresRoles
RequiresUser

org.apache.shiro.authz.aop
org.apache.shiro.authz.aop.AnnotationsAuthorizingMethodInterceptor

原理 aop


Spring Security


org.apache.shiro.realm.AuthorizingRealm

doGetAuthorizationInfo
doGetAuthenticationInfo


SimpleAuthenticationInfo   读写权限 在ca之后
SimpleAuthorizationInfo    能否访问系统

核心类Subject
http://shiro.apache.org/static/1.3.2/apidocs/org/apache/shiro/subject/Subject.html

        Subject subject = SecurityUtils.getSubject();





shiro使用了cookie jsessionid