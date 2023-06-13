# spring security

Spring Security 提供了诸多的 TokenStore 实现，如存在内存中的 InMemoryTokenStore 、存在数据库中的 JdbcTokenStore、存在 Redis 中的 RedisTokenStore

https://www.jianshu.com/p/64f2ee59acd9


https://www.oschina.net/p/spring+security?hmsr=aladdin1e1
Spring Security 是一个功能强大且高度可定制的身份验证和访问控制框架。它是用于保护基于Spring的应用程序的实际标准。

Spring Security 致力于为Java应用程序提供身份验证和授权。与所有Spring项目一样，Spring Security的真正强大之处在于可以轻松扩展以满足自定义要求
特性：
全面和可扩展的身份验证和授权支持
防止会话固定、点击劫持、跨网站请求伪造等攻击

Servlet API集成

与Spring Web MVC的可选集成

git repo springsecuritytest
https://gitee.com/edidada/springsecuritytest



https://github.com/spring-projects/spring-security-samples/tree/main/servlet/spring-boot/java/hello-security

```shell
org.springframework.ldap.CommunicationException: localhost:389; nested exception is javax.naming.CommunicationException: localhost:389 [Root exception is java.net.ConnectException: Connection refused: connect]
```


有几个流行的LDAP服务器可供选择，具体选择哪个取决于您的需求和偏好。以下是一些常见的LDAP服务器：

1. OpenLDAP：OpenLDAP 是一个免费的开源LDAP服务器，广泛用于企业和组织中。它具有稳定性和可靠性，并且支持广泛的LDAP协议功能。

2. Microsoft Active Directory：对于Windows环境，Microsoft Active Directory 是一个常用的LDAP服务器选项。它提供了丰富的功能和集成性，并且与其他Microsoft产品和服务紧密集成。

3. Apache Directory Server：Apache Directory Server 是一个基于Java的开源LDAP服务器，由Apache软件基金会开发和维护。它具有良好的性能和可扩展性，并提供了易于使用的管理界面。

4. Novell eDirectory：Novell eDirectory 是一个功能强大的LDAP服务器，具有高度可伸缩性和安全性。它适用于大型企业和组织，并提供了许多高级功能和集成选项。

这些LDAP服务器都具有各自的特点和优势，您可以根据自己的需求进行评估和选择。此外，还可以考虑其他LDAP服务器，如IBM Security Directory Server、Oracle Directory Server Enterprise Edition等，根据您的具体情况选择适合的服务器。


访问
http://127.0.0.1:8080
跳转到
http://127.0.0.1:8080/login


```shell

Using generated security password: 311e43dd-86d7-4b12-8937-d3e266bf06b4

2023-06-12 11:46:04.998  INFO 61620 --- [           main] o.s.s.web.DefaultSecurityFilterChain     : Will secure any request with [org.springframework.security.web.context.request.async.WebAsyncManagerIntegrationFilter@cfbc8e8, org.springframework.security.web.context.SecurityContextPersistenceFilter@3eee3e2b, org.springframework.security.web.header.HeaderWriterFilter@314ed053, org.springframework.security.web.csrf.CsrfFilter@67e28be3, org.springframework.security.web.authentication.logout.LogoutFilter@2f61f937, org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter@64c4c01, org.springframework.security.web.authentication.ui.DefaultLoginPageGeneratingFilter@1d96d872, org.springframework.security.web.authentication.ui.DefaultLogoutPageGeneratingFilter@3bead518, org.springframework.security.web.authentication.www.BasicAuthenticationFilter@16073fa8, org.springframework.security.web.savedrequest.RequestCacheAwareFilter@59532566, org.springframework.security.web.servletapi.SecurityContextHolderAwareRequestFilter@421a4ee1, org.springframework.security.web.authentication.AnonymousAuthenticationFilter@14bf57b2, org.springframework.security.web.session.SessionManagementFilter@486bc9a4, org.springframework.security.web.access.ExceptionTranslationFilter@2ff95fc6, org.springframework.security.web.access.intercept.FilterSecurityInterceptor@dcc6211]
```

“SpringSecurity默认的用户名是user,密码在项目启动的时候在控制台会打印,注意每次启动的时候密码都回发生变化!


Spring Security在启动时打印密码的源代码位于`org.springframework.security.web.authentication.ui.DefaultLoginPageGeneratingFilter`类的`generateLoginPageHtml`方法中。在该方法中，会生成登录页面的HTML代码，并在控制台输出用户名和密码信息。

具体来说，打印密码信息的代码位于该方法的第184行，如下所示：

```
logger.info("Using generated security password: " + password);
```

其中，`logger`是该类中声明的一个日志记录器。密码信息会被记录在日志中，并在控制台中输出。需要注意的是，这里的日志级别默认为INFO级别，如果您的应用程序的日志级别高于INFO级别，则可能无法在控制台中看到该信息。

文档不好，不如k8s文档全

新手不知道文档写的啥，需要找培训班视频去入门
老手觉得没有深入底层，有些问题光看文档没办法解决


需要有oauth2基础

深入浅出spring security作者，江南一点雨
SpringSecurity快速入门.pdf windows电脑上    有

https://github.com/lenve/spring-security-samples
https://gitee.com/edidada/spring-security-samples

### 初识Spring Security


Spring Security官方提供了很多示例代码，以帮助您了解和使用Spring Security的各种功能。以下是一些常见的Spring Security官方示例代码：
1. Spring Security Samples Repository：官方维护了一个GitHub仓库，其中包含了多个示例项目，涵盖了不同的使用场景和功能。您可以在该仓库中查看示例代码，并按照说明进行配置和运行。
GitHub链接：[https://github.com/spring-projects/spring-security-samples](https://github.com/spring-projects/spring-security-samples)
2. Spring Security Guides：官方提供了一系列的指南（guides），涵盖了Spring Security的不同方面和用法。这些指南提供了详细的说明、示例代码和配置示例，帮助您了解和应用Spring Security的功能。
官方指南链接：[https://docs.spring.io/spring-security/site/docs/current/guides/](https://docs.spring.io/spring-security/site/docs/current/guides/)
3. Spring Security OAuth Samples：如果您希望了解和使用Spring Security OAuth相关的功能，官方也提供了一些示例代码，用于演示OAuth 2.0和OpenID Connect等认证和授权场景的实现。
GitHub链接：[https://github.com/spring-projects/spring-security-oauth-samples](https://github.com/spring-projects/spring-security-oauth-samples)
这些示例代码和指南将帮助您快速入门并理解Spring Security的用法和配置方式。您可以根据自己的需求选择适合的示例，并根据官方文档进行配置和定制化。


### security与shiro结合使用？
有说法是不能结合，二者是竞品
todo

jar
spring-boot-starter-security 2.3.10.RELEASE
spring-cloud-starter-security 2.2.5.RELEASE



在Spring Security中，你可以通过配置来给登录的用户赋予角色。下面是一种常见的方式：

首先，你需要创建一个实现了`UserDetailsService`接口的类，用于加载用户信息和角色信息。在该类中，你可以从数据库、内存或其他数据源中获取用户信息，并将用户的角色信息添加到`UserDetails`对象中。

```java
import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;

public class UserDetailsServiceImpl implements UserDetailsService {
    
    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        // 从数据源中获取用户信息和角色信息
        // 示例中使用硬编码的方式添加角色信息，你可以根据实际情况从数据库或其他地方获取角色信息
        UserDetails user = User.withUsername(username)
                .password("password")
                .roles("ROLE_USER") // 添加用户角色
                .build();
        
        return user;
    }
}
```

然后，在配置类中使用`UserDetailsService`将其注入到`AuthenticationManagerBuilder`中，并配置登录的URL和角色相关的权限。

```java
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.authentication.builders.AuthenticationManagerBuilder;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configuration.WebSecurityConfigurerAdapter;

@Configuration
@EnableWebSecurity
public class SecurityConfig extends WebSecurityConfigurerAdapter {

    @Autowired
    private UserDetailsService userDetailsService;

    @Override
    protected void configure(AuthenticationManagerBuilder auth) throws Exception {
        auth.userDetailsService(userDetailsService);
    }

    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http.authorizeRequests()
            .antMatchers("/admin/**").hasRole("ADMIN") // 需要ADMIN角色才能访问
            .anyRequest().authenticated()
            .and()
            .formLogin()
            .loginPage("/login") // 登录页面的URL
            .permitAll()
            .and()
            .logout()
            .permitAll();
    }
}
```

在上述示例中，`UserDetailsServiceImpl`实现了`UserDetailsService`接口，并在`loadUserByUsername`方法中为用户添加了角色信息。在`SecurityConfig`配置类中，我们将`UserDetailsService`注入到`AuthenticationManagerBuilder`中，并使用`.hasRole("ROLE_NAME")`配置了需要具有指定角色的权限。

这样，当用户成功登录后，Spring Security会根据用户的角色信息进行权限验证，以决定用户是否具有访问受限资源的权限。


spring security

UserDetails信息如何支持集群中不同节点访问的

```java
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;

public class MyService {
    public boolean hasRole(String role) {
        Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
        return authentication.getAuthorities().stream()
                .anyMatch(authority -> authority.getAuthority().equals(role));
    }
}
```

login页面的用户名密码设置
```yml
spring:
  security:
    user:
      name: user
      password: 123456
```



https://gitee.com/edidada/spring-security-samples-5.6.x

### todo

GET /login
POST /login


org.springframework.boot.autoconfigure.security.servlet.UserDetailsServiceAutoConfiguration#getOrDeducePassword
打印spring security生成的密码

两种非主流的用户名/密码配置方案。
Spring Security 提供了多种密码加密方案，官方推荐使用 BCryptPasswordEncoder，BCryptPasswordEncoder 使用 BCrypt 强哈希函数，开发者在使用时可以选择提供 strength 和 SecureRandom 实例。strength 越大，密钥的迭代次数越多，密钥迭代次数为 2^strength。strength 取值在 4~31 之间，默认为 10。
不同于 Shiro 中需要自己处理密码加盐，在 Spring Security 中，BCryptPasswordEncoder 就自带了盐，处理起来非常方便。
而 BCryptPasswordEncoder 就是 PasswordEncoder 接口的实现类。
定义类，实现，注入spring ioc容器
org.springframework.security.config.annotation.web.configuration.WebSecurityConfigurerAdapter


`WebSecurityConfigurerAdapter`是Spring Security框架提供的一个方便的类，用于简化Web应用程序的安全配置。

它的主要作用如下：

1. 提供默认的安全配置：`WebSecurityConfigurerAdapter`定义了一系列方法，可以用于配置Web应用程序的安全性。它提供了一组默认的安全配置，例如禁用CSRF保护、启用HTTP基本身份验证、配置表单登录、配置注销等。通过继承`WebSecurityConfigurerAdapter`，可以轻松地启用和配置这些默认的安全设置。
2. 自定义安全配置：除了提供默认的安全配置外，`WebSecurityConfigurerAdapter`还允许开发人员自定义安全配置以满足特定的应用程序需求。通过重写`WebSecurityConfigurerAdapter`的方法，可以定制安全规则、配置认证管理器、定义登录和注销行为、配置访问权限等。这样，开发人员可以根据应用程序的具体要求来设计和配置安全性。
3. 组合多个安全配置类：`WebSecurityConfigurerAdapter`支持通过组合多个安全配置类的方式实现复杂的安全配置。通过创建多个继承自`WebSecurityConfigurerAdapter`的配置类，并将它们注入到主配置类中，可以实现按模块划分、分层次的安全配置。这样，每个配置类可以专注于特定的安全需求，提高了安全配置的可维护性和可扩展性。
总的来说，`WebSecurityConfigurerAdapter`是Spring Security框架提供的一个便捷的类，用于简化Web应用程序的安全配置。它提供了默认的安全设置和可扩展的配置选项，使开发人员能够快速搭建和定制应用程序的安全性。

spring security源代码，哪儿用抽象类WebSecurityConfigurerAdapter

chatgpt回答不是我想问的

实现了接口org.springframework.security.config.annotation.SecurityConfigurer

org.springframework.security.config.annotation.web.WebSecurityConfigurer

