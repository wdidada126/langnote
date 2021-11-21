# shiro

shiro netty项目，或者爬虫项目，大数据处理项目，如何鉴权？
数据拿去校验

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



https://shiro.apache.org/

https://blog.csdn.net/lei_1994/article/details/80504075

- IniSecurityManagerFactory ini纯文件保存用户名密码
- SecurityManager
- Factory

SecurityUtils

Realm

```shell
CachingRealm (org.apache.shiro.realm)
    AuthenticatingRealm (org.apache.shiro.realm)
        AuthorizingRealm (org.apache.shiro.realm)
            SimpleAccountRealm (org.apache.shiro.realm)
                TextConfigurationRealm (org.apache.shiro.realm.text)
                    IniRealm (org.apache.shiro.realm.text)
                    PropertiesRealm (org.apache.shiro.realm.text)
            AbstractLdapRealm (org.apache.shiro.realm.ldap)
                ActiveDirectoryRealm (org.apache.shiro.realm.activedirectory)
            JdbcRealm (org.apache.shiro.realm.jdbc)
            DefaultLdapRealm (org.apache.shiro.realm.ldap)
                JndiLdapRealm (org.apache.shiro.realm.ldap)
```


Subject
- login()
- logout()
- hasRole()
- hasRoles()
- checkRole()

shrio

shiro用户角色
https://www.jianshu.com/p/6a43af2ad044


```shell
2021-10-29 13:16:49,747 DEBUG [org.apache.shiro.io.ResourceUtils] - Opening resource from class path [shiro-permission.ini] 
2021-10-29 13:16:49,761 DEBUG [org.apache.shiro.config.Ini] - Parsing [users] 
2021-10-29 13:16:49,763 TRACE [org.apache.shiro.config.Ini] - Discovered key/value pair: zhangsan = 666,role1,role2 
2021-10-29 13:16:49,763 TRACE [org.apache.shiro.config.Ini] - Discovered key/value pair: lisi = 888,role2 
2021-10-29 13:16:49,763 DEBUG [org.apache.shiro.config.Ini] - Parsing [roles] 
2021-10-29 13:16:49,764 TRACE [org.apache.shiro.config.Ini] - Discovered key/value pair: role1 = user:create,user:update 
2021-10-29 13:16:49,764 TRACE [org.apache.shiro.config.Ini] - Discovered key/value pair: role2 = user:create,user:delete 
2021-10-29 13:16:49,764 TRACE [org.apache.shiro.config.Ini] - Discovered key/value pair: role3 = user:create 
2021-10-29 13:16:49,765 DEBUG [org.apache.shiro.config.IniFactorySupport] - Creating instance from Ini [sections=users,roles] 
2021-10-29 13:16:49,765 TRACE [org.apache.shiro.config.Ini] - Specified name was null or empty.  Defaulting to the default section (name = "") 
2021-10-29 13:16:49,873 DEBUG [org.apache.shiro.realm.text.IniRealm] - Discovered the [roles] section.  Processing... 
2021-10-29 13:16:49,876 DEBUG [org.apache.shiro.realm.text.IniRealm] - Discovered the [users] section.  Processing... 
2021-10-29 13:16:49,899 TRACE [org.apache.shiro.mgt.DefaultSecurityManager] - Context already contains a SecurityManager instance.  Returning. 
2021-10-29 13:16:49,899 TRACE [org.apache.shiro.mgt.DefaultSecurityManager] - No identity (PrincipalCollection) found in the context.  Looking for a remembered identity. 
2021-10-29 13:16:49,899 TRACE [org.apache.shiro.mgt.DefaultSecurityManager] - No remembered identity found.  Returning original context. 
2021-10-29 13:16:49,904 TRACE [org.apache.shiro.subject.support.DelegatingSubject] - attempting to get session; create = false; session is null = true; session has id = false 
2021-10-29 13:16:49,904 TRACE [org.apache.shiro.subject.support.DelegatingSubject] - attempting to get session; create = false; session is null = true; session has id = false 
2021-10-29 13:16:49,905 TRACE [org.apache.shiro.subject.support.DelegatingSubject] - attempting to get session; create = false; session is null = true; session has id = false 
2021-10-29 13:16:49,905 TRACE [org.apache.shiro.subject.support.DelegatingSubject] - attempting to get session; create = false; session is null = true; session has id = false 
2021-10-29 13:16:49,905 TRACE [org.apache.shiro.subject.support.DelegatingSubject] - attempting to get session; create = false; session is null = true; session has id = false 
2021-10-29 13:16:49,906 TRACE [org.apache.shiro.subject.support.DelegatingSubject] - attempting to get session; create = false; session is null = true; session has id = false 
2021-10-29 13:16:49,906 TRACE [org.apache.shiro.authc.AbstractAuthenticator] - Authentication attempt received for token [org.apache.shiro.authc.UsernamePasswordToken - zhangsan, rememberMe=false] 
2021-10-29 13:16:49,906 DEBUG [org.apache.shiro.realm.AuthenticatingRealm] - Looked up AuthenticationInfo [zhangsan] from doGetAuthenticationInfo 
2021-10-29 13:16:49,907 DEBUG [org.apache.shiro.realm.AuthenticatingRealm] - AuthenticationInfo caching is disabled for info [zhangsan].  Submitted token: [org.apache.shiro.authc.UsernamePasswordToken - zhangsan, rememberMe=false]. 
2021-10-29 13:16:49,907 DEBUG [org.apache.shiro.authc.credential.SimpleCredentialsMatcher] - Performing credentials equality check for tokenCredentials of type [[C and accountCredentials of type [java.lang.String] 
2021-10-29 13:16:49,907 DEBUG [org.apache.shiro.authc.credential.SimpleCredentialsMatcher] - Both credentials arguments can be easily converted to byte arrays.  Performing array equals comparison 
2021-10-29 13:16:49,908 DEBUG [org.apache.shiro.authc.AbstractAuthenticator] - Authentication successful for token [org.apache.shiro.authc.UsernamePasswordToken - zhangsan, rememberMe=false].  Returned account [zhangsan] 
2021-10-29 13:16:49,909 DEBUG [org.apache.shiro.subject.support.DefaultSubjectContext] - No SecurityManager available in subject context map.  Falling back to SecurityUtils.getSecurityManager() lookup. 
2021-10-29 13:16:49,909 TRACE [org.apache.shiro.mgt.DefaultSecurityManager] - Context already contains a SecurityManager instance.  Returning. 
2021-10-29 13:16:49,909 TRACE [org.apache.shiro.subject.support.DelegatingSubject] - attempting to get session; create = false; session is null = true; session has id = false 
2021-10-29 13:16:49,909 DEBUG [org.apache.shiro.subject.support.DefaultSubjectContext] - No SecurityManager available in subject context map.  Falling back to SecurityUtils.getSecurityManager() lookup. 
2021-10-29 13:16:49,909 TRACE [org.apache.shiro.subject.support.DelegatingSubject] - attempting to get session; create = false; session is null = true; session has id = false 
2021-10-29 13:16:49,909 TRACE [org.apache.shiro.subject.support.DelegatingSubject] - attempting to get session; create = false; session is null = true; session has id = false 
2021-10-29 13:16:49,909 TRACE [org.apache.shiro.subject.support.DelegatingSubject] - attempting to get session; create = false; session is null = true; session has id = false 
2021-10-29 13:16:49,909 TRACE [org.apache.shiro.subject.support.DelegatingSubject] - attempting to get session; create = false; session is null = true; session has id = false 
2021-10-29 13:16:49,909 TRACE [org.apache.shiro.subject.support.DelegatingSubject] - attempting to get session; create = false; session is null = true; session has id = false 
2021-10-29 13:16:49,909 TRACE [org.apache.shiro.subject.support.DelegatingSubject] - attempting to get session; create = false; session is null = true; session has id = false 
2021-10-29 13:16:49,909 TRACE [org.apache.shiro.subject.support.DelegatingSubject] - attempting to get session; create = true; session is null = true; session has id = false 
2021-10-29 13:16:49,909 TRACE [org.apache.shiro.subject.support.DelegatingSubject] - Starting session for host null 
2021-10-29 13:16:49,910 DEBUG [org.apache.shiro.session.mgt.AbstractValidatingSessionManager] - No sessionValidationScheduler set.  Attempting to create default instance. 
2021-10-29 13:16:49,911 TRACE [org.apache.shiro.session.mgt.AbstractValidatingSessionManager] - Created default SessionValidationScheduler instance of type [org.apache.shiro.session.mgt.ExecutorServiceSessionValidationScheduler]. 
2021-10-29 13:16:49,911 INFO [org.apache.shiro.session.mgt.AbstractValidatingSessionManager] - Enabling session validation scheduler... 
2021-10-29 13:16:49,919 TRACE [org.apache.shiro.session.mgt.DefaultSessionManager] - Creating session for host null 
2021-10-29 13:16:49,920 DEBUG [org.apache.shiro.session.mgt.DefaultSessionManager] - Creating new EIS record for new session instance [org.apache.shiro.session.mgt.SimpleSession,id=null] 
2021-10-29 13:16:50,542 TRACE [org.apache.shiro.session.mgt.AbstractValidatingSessionManager] - Attempting to retrieve session with key org.apache.shiro.session.mgt.DefaultSessionKey@50f8360d 
2021-10-29 13:16:50,542 TRACE [org.apache.shiro.subject.support.DelegatingSubject] - attempting to get session; create = false; session is null = false; session has id = true 
2021-10-29 13:16:50,542 TRACE [org.apache.shiro.session.mgt.AbstractValidatingSessionManager] - Attempting to retrieve session with key org.apache.shiro.session.mgt.DefaultSessionKey@50f8360d 
2021-10-29 13:16:50,543 TRACE [org.apache.shiro.session.mgt.AbstractValidatingSessionManager] - Attempting to retrieve session with key org.apache.shiro.session.mgt.DefaultSessionKey@50f8360d 
2021-10-29 13:16:50,543 TRACE [org.apache.shiro.mgt.DefaultSecurityManager] - This org.apache.shiro.mgt.DefaultSecurityManager instance does not have a [org.apache.shiro.mgt.RememberMeManager] instance configured.  RememberMe services will not be performed for account [zhangsan]. 
2021-10-29 13:16:50,543 TRACE [org.apache.shiro.subject.support.DelegatingSubject] - attempting to get session; create = false; session is null = false; session has id = true 
2021-10-29 13:16:50,543 TRACE [org.apache.shiro.subject.support.DelegatingSubject] - attempting to get session; create = false; session is null = false; session has id = true 
2021-10-29 13:16:50,543 TRACE [org.apache.shiro.session.mgt.AbstractValidatingSessionManager] - Attempting to retrieve session with key org.apache.shiro.session.mgt.DefaultSessionKey@50f8360d 
2021-10-29 13:16:50,544 TRACE [org.apache.shiro.subject.support.DelegatingSubject] - attempting to get session; create = false; session is null = false; session has id = true 
2021-10-29 13:16:50,544 TRACE [org.apache.shiro.session.mgt.AbstractValidatingSessionManager] - Attempting to retrieve session with key org.apache.shiro.session.mgt.DefaultSessionKey@50f8360d 
2021-10-29 13:16:50,544 TRACE [org.apache.shiro.realm.AuthorizingRealm] - Retrieving AuthorizationInfo for principals [zhangsan] 
true
2021-10-29 13:16:50,544 TRACE [org.apache.shiro.subject.support.DelegatingSubject] - attempting to get session; create = false; session is null = false; session has id = true 
2021-10-29 13:16:50,544 TRACE [org.apache.shiro.session.mgt.AbstractValidatingSessionManager] - Attempting to retrieve session with key org.apache.shiro.session.mgt.DefaultSessionKey@50f8360d 
2021-10-29 13:16:50,544 TRACE [org.apache.shiro.subject.support.DelegatingSubject] - attempting to get session; create = false; session is null = false; session has id = true 
2021-10-29 13:16:50,544 TRACE [org.apache.shiro.session.mgt.AbstractValidatingSessionManager] - Attempting to retrieve session with key org.apache.shiro.session.mgt.DefaultSessionKey@50f8360d 
2021-10-29 13:16:50,544 TRACE [org.apache.shiro.realm.AuthorizingRealm] - Retrieving AuthorizationInfo for principals [zhangsan] 
2021-10-29 13:16:50,545 TRACE [org.apache.shiro.realm.AuthorizingRealm] - Retrieving AuthorizationInfo for principals [zhangsan] 
[Z@12843fce
2021-10-29 13:16:50,545 TRACE [org.apache.shiro.subject.support.DelegatingSubject] - attempting to get session; create = false; session is null = false; session has id = true 
2021-10-29 13:16:50,546 TRACE [org.apache.shiro.session.mgt.AbstractValidatingSessionManager] - Attempting to retrieve session with key org.apache.shiro.session.mgt.DefaultSessionKey@50f8360d 
2021-10-29 13:16:50,546 TRACE [org.apache.shiro.subject.support.DelegatingSubject] - attempting to get session; create = false; session is null = false; session has id = true 
2021-10-29 13:16:50,546 TRACE [org.apache.shiro.session.mgt.AbstractValidatingSessionManager] - Attempting to retrieve session with key org.apache.shiro.session.mgt.DefaultSessionKey@50f8360d 
2021-10-29 13:16:50,546 TRACE [org.apache.shiro.realm.AuthorizingRealm] - Retrieving AuthorizationInfo for principals [zhangsan] 
````



```java
//1.创建SecurityManager工厂对象：加载配置文件，创建工厂对象

  Factory<SecurityManager> factory =  new IniSecurityManagerFactory("classpath:shiro-permission.ini");

  //2.创建工厂对象，创建SecurityManager对象

  SecurityManager securityManager = (SecurityManager) factory.getInstance();

  //3.将securityManager绑定到当前运行环境中，让系统随时都可以访问SecurityManager对象

  SecurityUtils.setSecurityManager((org.apache.shiro.mgt.SecurityManager) securityManager);

  //4.创建当前登录的主体，注意：此时主体没有经验证

  Subject subject = SecurityUtils.getSubject();

  //5.绑定主体登录的身份/凭证，即账号密码

  //参数1：将要登录的用户名，参数2：登录用户的密码

  UsernamePasswordToken token = new UsernamePasswordToken("zhangsan","666");

  subject.login(token);

  //进行授权操作时前提：用户必须通过认证

  //判断当前用户手否拥有某个角色

  System.out.println(subject.hasRole("role1"));

  System.out.println(subject.hasRoles(Arrays.asList("role1","role2")));

  //判断当前用户是否拥有某个角色：没有返回值，如果有角色不做任何操作，没有报一个异常

  subject.checkRole("role4");
```

如果身份验证失败请捕获AuthenticationException 或其子类，常见的如：
DisabledAccountException（禁用的帐号）、LockedAccountException（锁定的帐号）、
UnknownAccountException（错误的帐号）、ExcessiveAttemptsException（登录失败次数过
多）、IncorrectCredentialsException （错误的凭证）、ExpiredCredentialsException（过期的
凭证）等


spring-springmvc-mybatis-shiro项目介绍 https://segmentfault.com/a/1190000011001391

AopAllianceAnnotationsAuthorizingMethodInterceptor


shiro web支持多节点部署吗？

https://blog.csdn.net/lgxzzz/article/details/102632667

Shiro-redis插件版本:3.1.0
https://my.oschina.net/linwl/blog/1813441


shiro使用了cookie jsessionid
