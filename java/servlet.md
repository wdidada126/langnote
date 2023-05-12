# servlet

官方文档
servlet-3_0-mrel-spec.pdf



<!--        <dependency>
            <groupId>javax.servlet</groupId>
            <artifactId>servlet-api</artifactId>
            <version>4.0.1</version>
            <scope>provided</scope>
        </dependency>-->
        <dependency>
            <groupId>javax.servlet</groupId>
            <artifactId>javax.servlet-api</artifactId>
            <version>4.0.1</version>
            <scope>provided</scope>
        </dependency>

 servlet api两个版本artifactId不一样       

### servlet api doc

https://docs.oracle.com/cd/E17802_01/products/products/servlet/2.5/docs/servlet-2_5-mr2/


https://tomcat.apache.org/tomcat-7.0-doc/servletapi/index.html


### servlet version
Servlet版本
要务必注意servlet-api的版本。4.0及之前的servlet-api由Oracle官方维护，引入的依赖项是javax.servlet:javax.servlet-api，编写代码时引入的包名为：
import javax.servlet.*;
而5.0及以后的servlet-api由Eclipse开源社区维护，引入的依赖项是jakarta.servlet:jakarta.servlet-api，编写代码时引入的包名为：
import jakarta.servlet.*;
教程采用最新的jakarta.servlet:5.0.0版本，但对于很多仅支持Servlet 4.0版本的框架来说，例如Spring 5，我们就只能使用javax.servlet:4.0.0版本，这一点针对不同项目要特别注意

Jakarta Servlet 6.0
5
4.0.3
4
3.1
3
2.5
2.4
2.3


[结合源码谈谈Servlet的实例化、变量以及多线程](https://www.iteye.com/blog/angelbill3-2374280)



- java规范servlet servlet版本
- web.xml配置文件内容 校验文件 重要参数
- maven package



<dependency>
    <groupId>javax.servlet</groupId>
    <artifactId>javax.servlet</artifactId>
    <version>3.0.0.v201103241009</version>
</dependency>
<dependency>
    <groupId>javax.servlet</groupId>
    <artifactId>javax.servlet-api</artifactId>
    <version>3.0.1</version>
    <scope>provided</scope>
</dependency>





maven

src/main/webapp



src/main/webapp/WEB-INF/web.xml



#### web.xml

如何查看Servlet版本

查看web.xml文件中<web-app>标签中的version字段即可。

首先 web.xml 是java web项目的一个重要的配置文件，但是web.xml文件并不是Java web工程必须的。

web.xml文件是用来配置：欢迎页、servlet、filter等的。当你的web工程没用到这些时，你可以不用web.xml文件来配置你的web工程。



web.xml文件详解

src\main\webapp\WEB-INF\web.xml

xml文件通过dtd校验的


```xml
<!DOCTYPE web-app PUBLIC
  "-//Sun Microsystems, Inc.//DTD Web Application 2.3//EN"
  "http://java.sun.com/dtd/web-app_2_3.dtd" >
<web-app>
    <context-param>
    <param-name>contextConfigLocation</param-name>
    <param-value>applicationContext.xml</param-value>
  </context-param>
  <listener>
    <listener-class>
          com.minis.web.context.ContextLoaderListener
      </listener-class>
  </listener>
    <!-- shiro过滤器定义 -->
  <filter>  
      <filter-name>shiroFilter</filter-name>  
      <filter-class>org.springframework.web.filter.DelegatingFilterProxy</filter-class>  
    <init-param>
      <!-- 该值缺省为false,表示生命周期由SpringApplicationContext管理,设置为true则表示由ServletContainer管理 -->
      <param-name>targetFilterLifecycle</param-name>
      <param-value>true</param-value>
    </init-param>
  </filter>
  <filter-mapping>  
          <filter-name>shiroFilter</filter-name>  
          <url-pattern>/*</url-pattern>  
  </filter-mapping>
  <servlet>
    <servlet-name>springMvc</servlet-name>
    <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
    <init-param>
      <param-name>contextConfigLocation</param-name>
      <param-value>classpath:spring/spring.xml</param-value>
    </init-param>
    <load-on-startup>1</load-on-startup>
  </servlet>
  <servlet-mapping>
    <servlet-name>springMvc</servlet-name>
    <url-pattern>/</url-pattern>
  </servlet-mapping>
</web-app>
```







servlet是java ee标准
http的



servlet-api



JavaEE就是提供了一堆API

Tomcat实现了servlet-api

SpringMVC扩展实现了



HttpServletBean是一个class直接实现了HttpServlet,这个类主要负责配置文件





```xml
        <dependency>
            <groupId>javax.servlet</groupId>
            <artifactId>javax.servlet-api</artifactId>
            <version>3.0.1</version>
            <scope>provided</scope>
        </dependency>
```



### source package

-  javax.servlet
- javax.servlet.annotation
- Javax.servlet.descriptor
- javax.servlet.http

###### 三个组件

Servlet

Listener

Filter



javax.servlet.http.HttpServlet

继承

javax.servlet.GenericServlet

javax.servlet.Servlet实现这两个接口

javax.servlet.ServletConfig

javax.servlet.ServletContext

含有

javax.servlet.RequestDispatcher




javax.servlet.http.HttpServletRequestWrapper
请求包装器 自定义继承这个类



```java
void forward(ServletRequest request, ServletResponse response)
```

```java
void include(ServletRequest request, ServletResponse response)
```

### servlet与Spring Boot

import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;



InterceptorRegistry
public InterceptorRegistration addInterceptor(HandlerInterceptor interceptor)


http插值器
org.springframework.web.servlet.HandlerInterceptor


### servlet与springmvc


