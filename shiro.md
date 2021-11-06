# shiro

testshiro gitee repo

shrio springboot



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
