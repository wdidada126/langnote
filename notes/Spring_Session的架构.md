Spring Session的架构
Spring Session定义了一组标准的接口，可以通过实现这些接口间接访问底层的数据存储。
Spring Session定义了如下核心接口：Session、ExpiringSession以及SessionRepository，针对不同的数据存储，它们需要分别实现。
org.springframework.session.Session接口定义了session的基本功能，如设置和移除属性。
这个接口并不关心底层技术，因此能够比servlet HttpSession适用于更为广泛的场景中。
org.springframework.session.ExpiringSession扩展了Session接口，它提供了判断session是否过期的属性。
RedisSession是这个接口的一个样例实现。
org.springframework.session.SessionRepository定义了创建、保存、删除以及检索session的方法。
将Session实例真正保存到数据存储的逻辑是在这个接口的实现中编码完成的。
例如，RedisOperationsSessionRepository就是这个接口的一个实现，它会在Redis中创建、存储和删除session。
在请求/响应周期中，客户端和服务器之间需要协商同意一种传递session id的方式。
例如，如果请求是通过HTTP传递进来的，那么session可以通过HTTP cookie或HTTP Header信息与请求进行关联。



对于HTTP协议来说，Spring Session定义了HttpSessionStrategy接口以及两个默认实现，
即CookieHttpSessionStrategy和HeaderHttpSessionStrategy，其中前者使用HTTP cookie将请求与session id关联，
而后者使用HTTP header将请求与session关联。



核心思想：
通过org.springframework.session.web.http.SessionRepositoryFilter的
doFilterInternal(HttpServletRequest request,HttpServletResponse response,FilterChain filterChain)
对所有的请求进行拦截，使用包装（Wrapper）或者说是装饰（Decorator）模式对request,
response进行包装并重写HttpServletRequest 的 getSession方法，然后通过 filterChain向后传递。


Java内存模型
https://www.cnblogs.com/nexiyi/p/java_memory_model_and_thread.html



Java内存模型 vs JVM内存模型




volitale     只保证可见性
synchronized   既保证可见性，又保证原子性



有序性
redis-cli del spring:session:sessions:7e8383a4-082c-4ffe-a4bc-c40fd3363c5e

SpringMVC ContextLoaderListener

The ContextLoaderListener reads the contextConfigLocation and picks up our session.xml configuration.

The DelegatingFilterProxy will look up a Bean by the name of springSessionRepositoryFilter and cast it to a Filter.
For every request that DelegatingFilterProxy is invoked, the springSessionRepositoryFilter will be invoked.

<filter>
    <filter-name>springSessionRepositoryFilter</filter-name>
    <filter-class>org.springframework.web.filter.DelegatingFilterProxy</filter-class>
</filter>
<filter-mapping>
    <filter-name>springSessionRepositoryFilter</filter-name>
    <url-pattern>/*</url-pattern>
    <dispatcher>REQUEST</dispatcher>
    <dispatcher>ERROR</dispatcher>
</filter-mapping>




web.xml中 
filter
init-param的作用
filter 可以接受一些参数。init-param 的param-name 就是参数名param-value就是参数值，支持多个参数
每一个filter都有一个init方法，可以再这个方法中通过getInitParamter("key")；key就是param-name的值，来获取对应的参数值
常用的就是设置编码过滤器，例如：
<init-param>
	<param-name>encoding</param-name>
	<parma-value>UTF-8</param-vaue>
</init-param>


OncePerRequestFilter的作用
在Spring中，filter默认继承OncePerRequestFilter，OncePerRequestFilter，顾名思义，
它能够确保在一次请求中只通过一次filter，而需要重复的执行。
大家常识上都认为，一次请求本来就只filter一次，为什么还要由此特别限定呢，
往往我们的常识和实际的实现并不真的一样，经过一番资料的查阅，此方法是为了兼容不同的web container，
也就是说并不是所有的container都入我们期望的只过滤一次，servlet版本不同，执行过程也不同
如：servlet2.3与servlet2.4也有一定差异：
在servlet2.3中，Filter会经过一切请求，包括服务器内部使用的forward转发请求和<%@ include file=”/login.jsp”%>的情况
servlet2.4中的Filter默认情况下只过滤外部提交的请求，forward和include这些内部转发都不会被过滤，
因此，为了兼容各种不同运行环境和版本，默认filter继承OncePerRequestFilter是一个比较稳妥的选择


Lettuce


Spring for Apache Kafka 2.2.0

Spring Session


spring.cloud.inetutils.preferred-networks

java -jar E:\SpringCloudProducer\target\spring-cloud-producer-0.0.6.jar  --spring.cloud.inetutils.preferred-networks=180.172.0.20

180.172.0.20:8090/info

docker run -d -it -p 8089:8089 edidada/spring-cloud-eureka


application.properties

eureka.client.register-with-eureka ：表示是否将自己注册到Eureka Server，默认为true。
eureka.client.fetch-registry ：表示是否从Eureka Server获取注册信息，默认为true。
eureka.client.serviceUrl.defaultZone ：设置与Eureka Server交互的地址，查询服务和注册服务都需要依赖这个地址。
默认是http://localhost:8761/eureka ；多个地址可使用 , 分隔。

spring:
  cloud:
    config:
      server:
        git:
          uri: https://github.com/ityouknow/spring-cloud-starter/     # 配置git仓库的地址
          search-paths: config-repo                             # git仓库地址下的相对地址，可以配置多个，用,分割。
          username:                                             # git仓库的账号
          password:                                             # git仓库的密码


Consul 客户端、服务端还支持跨中心访问
1、当 Producer 启动的时候，会向 Consul 发送一个 post 请求，告诉 Consul 自己的 IP 和 Port
2、Consul 接收到 Producer 的注册后，每隔10s（默认）会向 Producer 发送一个健康检查的请求，检验Producer是否健康
3、当 Consumer 发送 GET 方式请求 /api/address 到 Producer 时，会先从 Consul 中拿到一个存储服务 IP 和 Port 的临时表，从表中拿到 Producer 的 IP 和 Port 后再发送 GET 方式请求 /api/address
4、该临时表每隔10s会更新，只包含有通过了健康检查的 Producer

