# servlet



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

首先 web.xml 是java web 项目的一个重要的配置文件，但是web.xml文件并不是Java web工程必须的。

web.xml文件是用来配置：欢迎页、servlet、filter等的。当你的web工程没用到这些时，你可以不用web.xml文件来配置你的web工程。



web.xml文件详解

src\main\webapp\WEB-INF\web.xml



```xml
<!DOCTYPE web-app PUBLIC
  "-//Sun Microsystems, Inc.//DTD Web Application 2.3//EN"
  "http://java.sun.com/dtd/web-app_2_3.dtd" >
<web-app>
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







servlet是java标准

http的



servlet-api



JavaEE就是提供了一堆API

Tomcat实现了

SpringMVC实现了



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


