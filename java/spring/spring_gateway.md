# spring_gateway


微服务开发的dubbo或者http接口，前端如何访问，通过域名dns系统实现负载均衡？
如何避免攻击？
pgsql是可以设置ip白名单的
mysql通过用户名密码访问
ftp也是


AbstractGatewayFilterFactory

`AbstractGatewayFilterFactory`是Spring Cloud Gateway中的一个抽象类，用于简化自定义过滤器的创建。它提供了一些基本的方法和属性，以便更轻松地创建自定义过滤器。

具体作用如下：
1. 提供了默认的构造函数和属性，简化了过滤器的创建和配置过程。
2. 定义了一些常用的过滤器属性，如name、order等，用于设置过滤器的名称和执行顺序。
3. 提供了`ShortcutType`枚举，用于定义过滤器的类型，如PRE、POST、ROUTE等。
4. 定义了抽象方法`shortcutType()`和`apply()`，用于子类实现具体的过滤器逻辑。
5. 可以通过继承`AbstractGatewayFilterFactory`并实现相应的方法，来创建自定义的过滤器。

总之，`AbstractGatewayFilterFactory`为开发者提供了一个基础框架，使得创建和配置自定义过滤器变得更加简单和灵活。

多个自定义AbstractGatewayFilterFactory的顺序

在 Spring Cloud Gateway 中，多个自定义的 `AbstractGatewayFilterFactory` 的顺序是根据它们在过滤器链中的顺序来决定的。具体而言，它们的顺序取决于它们在 `RouteLocator` 中的配置顺序和它们在 `GatewayFilterChain` 中的添加顺序。

在 `RouteLocator` 中，您可以通过 `route()` 方法配置路由规则，例如：

```java
@Bean
public RouteLocator customRouteLocator(RouteLocatorBuilder builder) {
    return builder.routes()
        .route("example_route", r -> r.path("/example")
            .filters(f -> f.filter(filter1()).filter(filter2()))
            .uri("http://example.com"))
        .build();
}
```

在上述例子中，`filter1()` 和 `filter2()` 分别表示两个自定义的 `AbstractGatewayFilterFactory`，它们被添加到了路由规则中，并按照顺序进行调用。

在 `GatewayFilterChain` 中，每个过滤器都会被添加到过滤器链中，并按照添加顺序进行调用。例如：

```java
public Mono<Void> filter(ServerWebExchange exchange, GatewayFilterChain chain) {
    // 调用自定义过滤器逻辑
    return chain.filter(exchange);
}
```

在上述例子中，`chain.filter(exchange)` 表示调用下一个过滤器，这样就能够保证过滤器按照添加顺序进行调用。

总之，多个自定义的 `AbstractGatewayFilterFactory` 的顺序取决于它们在过滤器链中的顺序，在 `RouteLocator` 和 `GatewayFilterChain` 中的配置方式都会影响它们的顺序。建议您根据具体的业务需求和过滤器的功能特点，来确定它们的顺序。




在 Spring Cloud Gateway 中，Predicate 和自定义的 `AbstractGatewayFilterFactory` 都是用于实现路由规则的重要组件。它们的主要区别和联系如下：

1. 区别：Predicate 是用于实现路由规则匹配的组件，它根据请求的条件，例如请求的 Host、Path、Header 等，判断请求是否符合路由规则。而自定义的 `AbstractGatewayFilterFactory` 则是用于实现过滤器的组件，它根据请求和响应的条件，例如请求和响应的 Header、Body 等，对请求进行过滤和转换。

2. 联系：Predicate 和自定义的 `AbstractGatewayFilterFactory` 都是可以根据实际业务需求进行自定义的组件。它们都可以通过编写 Java 代码来实现自定义逻辑，实现灵活、可扩展的路由规则和过滤器。

在 Spring Cloud Gateway 的路由规则中，Predicate 和自定义的 `AbstractGatewayFilterFactory` 都可以进行组合使用。例如，您可以使用 `PathRoutePredicateFactory` 实现基于请求 Path 的路由规则匹配，使用自定义的 `AbstractGatewayFilterFactory` 实现基于请求 Body 的过滤器逻辑。这样就能够实现更加灵活、高效、可扩展的路由规则和过滤器。

需要注意的是，在使用 Predicate 和自定义的 `AbstractGatewayFilterFactory` 时，要根据具体业务需求选择合适的实现方式，并进行充分的测试和验证，确保其满足实际的性能和安全要求。同时，也要注意路由规则和过滤器的顺序，以确保其按照预期的顺序进行调用。


GlobalFilter作用
自定义类，实现GlobalFilter



日志打印RouteDefinitionRouteLocator

```shell
2023-05-25 09:36:23.238 [main] INFO  o.s.c.g.r.RouteDefinitionRouteLocator 139 - Loaded RoutePredicateFactory [After]
2023-05-25 09:36:23.238 [main] INFO  o.s.c.g.r.RouteDefinitionRouteLocator 139 - Loaded RoutePredicateFactory [Before]
2023-05-25 09:36:23.238 [main] INFO  o.s.c.g.r.RouteDefinitionRouteLocator 139 - Loaded RoutePredicateFactory [Between]
2023-05-25 09:36:23.238 [main] INFO  o.s.c.g.r.RouteDefinitionRouteLocator 139 - Loaded RoutePredicateFactory [Cookie]
2023-05-25 09:36:23.238 [main] INFO  o.s.c.g.r.RouteDefinitionRouteLocator 139 - Loaded RoutePredicateFactory [Header]
2023-05-25 09:36:23.238 [main] INFO  o.s.c.g.r.RouteDefinitionRouteLocator 139 - Loaded RoutePredicateFactory [Host]
2023-05-25 09:36:23.238 [main] INFO  o.s.c.g.r.RouteDefinitionRouteLocator 139 - Loaded RoutePredicateFactory [Method]
2023-05-25 09:36:23.239 [main] INFO  o.s.c.g.r.RouteDefinitionRouteLocator 139 - Loaded RoutePredicateFactory [Path]
2023-05-25 09:36:23.239 [main] INFO  o.s.c.g.r.RouteDefinitionRouteLocator 139 - Loaded RoutePredicateFactory [Query]
2023-05-25 09:36:23.239 [main] INFO  o.s.c.g.r.RouteDefinitionRouteLocator 139 - Loaded RoutePredicateFactory [ReadBodyPredicateFactory]
2023-05-25 09:36:23.239 [main] INFO  o.s.c.g.r.RouteDefinitionRouteLocator 139 - Loaded RoutePredicateFactory [RemoteAddr]
2023-05-25 09:36:23.239 [main] INFO  o.s.c.g.r.RouteDefinitionRouteLocator 139 - Loaded RoutePredicateFactory [Weight]
2023-05-25 09:36:23.240 [main] INFO  o.s.c.g.r.RouteDefinitionRouteLocator 139 - Loaded RoutePredicateFactory [CloudFoundryRouteService]
```




内置RouteToRequestUrlFilter
Spring Cloud Gateway是Spring Cloud官方推出的第二代网关框架，取代Netflix Zuul网关。
路由中的断言可以看做是一种规则或条件，用来匹配用户的请求是否符合我们所设定的路由规则。
在Spring Cloud Gateway中，路由配置可以包含一个或多个断言（Predicate），用于匹配请求是否符合当前路由规则。如果请求匹配成功，Gateway就会将请求路由到目标微服务，否则会返回404 Not Found错误。
断言通常用于检查HTTP请求的特定属性，例如请求的URI、HTTP方法、请求头、查询参数等。以下是一些常用的断言：
Path断言：根据请求的URI匹配路由规则，可以使用Ant风格的通配符。
Method断言：根据HTTP方法匹配路由规则，例如GET、POST、PUT、DELETE等。
Header断言：根据请求头匹配路由规则，例如Content-Type、User-Agent等。
Query断言：根据查询参数匹配路由规则，例如id、name等。


在 Spring Cloud Gateway 中,可以使用 Path 断言来匹配具体的 URL 路径。
一个简单的 Path 断言示例:
```yaml
- id: path_route
  uri: https://example.com
  predicates:
    - Path=/foo/**  
```
这里我们使用 Path=/foo/** 来匹配所有以 /foo 开头的路径。

还可以使用正则表达式匹配路径:
```yaml
- id: regex_route  
  uri: https://example.com
  predicates:
    - Path= /foo/bar, /abc/.*   
```
这里我们使用了 Path= /foo/bar, /abc/.* 模式来匹配 /foo/bar 和所有以 /abc 开头的路径。

Path 断言还支持匹配 HTTP 方法,例如:
```yaml  
- id: method_route
  uri: https://example.com
  predicates:
    - Path=/api/foo/** 
    - Method=GET
```
这里只有 GET 请求并且路径以 /api/foo 开头时,路由才会匹配。

除了 Path 断言外,Spring Cloud Gateway 还支持很多其他断言:
- Cookie
- Header
- Host
- Method
- Query
- RemoteAddr

希望这有助于理解 Path 断言在 Spring Cloud Gateway 的使用。


DefaultServerWebExchange


https://gitee.com/edidada/my-gateway

lb标签负载均衡原理

lb:erp-fi标签代表使用erp-fi作为负载均衡策略。

其负载均衡原理为:
1. 维护一个各机器访问权重的权重表,初始时各机器的权重相同。
2. 当有新的访问请求到来时,会根据各机器的权重比例,选择一个机器来处理该请求。
3. 在处理完一个请求后,会根据服务到达时间进行调整:
   - 如果响应时间短于平均响应时间,则该机器的权重增加
   - 如果响应时间长于平均响应时间,则该机器的权重减少
4. 通过这样的负反馈机制,可以动态调整各机器的工作压力,使高压力的机器的权重下降,低压力的机器的权重增加。 
达到一种动态的负载均衡。

具体步骤为:
1. 获取所有服务实例及其初始权重;
2. 客户端来请求时,根据权重分配给一个服务实例;
3. 服务实例响应后,根据响应时间调整该实例的权重;
4. 重复步骤2和3。
基于这样的机制,可以实现动态的负载均衡,高压力的实例压力会降低,低压力的实例压力会增加,从而最终达到整体上的负载均衡。




Spring Cloud Gateway和Zuul都是Spring Cloud提供的API网关组件，用于实现请求路由、负载均衡、过滤器等功能。它们在功能上有一些区别和特点：
1. 基于不同的技术栈：Spring Cloud Gateway使用Spring WebFlux作为底层，而Zuul是基于Servlet技术实现的。
2. 响应式与阻塞式：Spring Cloud Gateway基于响应式编程模型，利用非阻塞I/O实现高性能，适用于处理大量并发请求。而Zuul采用阻塞式I/O，适用于传统的同步请求处理。
3. 网关过滤器：Spring Cloud Gateway采用基于过滤器链的方式，可以通过过滤器进行请求的预处理和后处理。Zuul也支持过滤器，但其过滤器是基于Servlet Filter的，使用起来略显复杂。
4. 动态路由配置：Spring Cloud Gateway支持动态路由配置，可以使用动态路由断言和过滤器工厂来动态定义路由规则。Zuul的路由配置需要在启动时静态配置，不支持动态刷新。
5. 生态系统支持：由于Spring Cloud Gateway基于Spring WebFlux，它能够与Spring生态系统中的其他组件（如Spring Security、Spring Cloud Sleuth等）无缝集成。而Zuul在一些新的功能和扩展上可能相对较少。
总体而言，Spring Cloud Gateway更适合构建高性能、响应式的微服务架构，而Zuul则更适合传统的阻塞式请求处理和与传统Spring生态系统的集成。选择使用哪个网关组件取决于项目需求和技术栈的选择。

Spring Cloud Gateway 并没有依赖 Tomcat，而是用 NettyWebServer 来启动服务监听（从启动日志可以看到）


https://docs.spring.io/spring-cloud-gateway/docs/current/reference/html/
https://cloud.spring.io/spring-cloud-gateway/reference/html/
三个核心概念
Route
Predicate
Filter



5.1. The After Route Predicate Factory
5.2. The Before Route Predicate Factory
5.3. The Between Route Predicate Factory
5.4. The Cookie Route Predicate Factory
5.5. The Header Route Predicate Factory
5.6. The Host Route Predicate Factory
5.7. The Method Route Predicate Factory
5.8. The Path Route Predicate Factory
5.9. The Query Route Predicate Factory
5.10. The RemoteAddr Route Predicate Factory
5.11. The Weight Route Predicate Factory




6.1. The AddRequestHeader GatewayFilter Factory
6.2. The AddRequestParameter GatewayFilter Factory
6.3. The AddResponseHeader GatewayFilter Factory
6.4. The DedupeResponseHeader GatewayFilter Factory
6.5. Spring Cloud CircuitBreaker GatewayFilter Factory
6.6. The FallbackHeaders GatewayFilter Factory
6.7. The MapRequestHeader GatewayFilter Factory
6.8. The PrefixPath GatewayFilter Factory
6.9. The PreserveHostHeader GatewayFilter Factory
6.10. The RequestRateLimiter GatewayFilter Factory
6.11. The RedirectTo GatewayFilter Factory
6.12. The RemoveRequestHeader GatewayFilter Factory
6.13. RemoveResponseHeader GatewayFilter Factory
6.14. The RemoveRequestParameter GatewayFilter Factory
6.15. The RewritePath GatewayFilter Factory
6.16. RewriteLocationResponseHeader GatewayFilter Factory
6.17. The RewriteResponseHeader GatewayFilter Factory
6.18. The SaveSession GatewayFilter Factory
6.19. The SecureHeaders GatewayFilter Factory
6.20. The SetPath GatewayFilter Factory
6.21. The SetRequestHeader GatewayFilter Factory
6.22. The SetResponseHeader GatewayFilter Factory
6.23. The SetStatus GatewayFilter Factory
6.24. The StripPrefix GatewayFilter Factory
6.25. The Retry GatewayFilter Factory
6.26. The RequestSize GatewayFilter Factory
6.27. The SetRequestHost GatewayFilter Factory
6.28. Modify a Request Body GatewayFilter Factory
6.29. Modify a Response Body GatewayFilter Factory
6.30. Default Filters



7.1. Combined Global Filter and GatewayFilter Ordering
7.2. Forward Routing Filter
7.3. The LoadBalancerClient Filter
7.4. The ReactiveLoadBalancerClientFilter
7.5. The Netty Routing Filter
7.6. The Netty Write Response Filter
7.7. The RouteToRequestUrl Filter
7.8. The Websocket Routing Filter
7.9. The Gateway Metrics Filter
7.10. Marking An Exchange As Routed



org.springframework.cloud.gateway.route.Route


`org.springframework.cloud.gateway.route.Route` 是 Spring Cloud Gateway 中的一个重要类，它表示一个路由规则，用于将客户端的请求转发到后端的服务实例。

具体而言，`Route` 类主要包含以下属性：

- `id`：路由规则的唯一标识符，通常使用字符串类型表示。
- `uri`：后端服务的 URI 地址，可以是 `http` 或 `https` 协议，也可以是 `lb`（负载均衡器）协议。
- `predicates`：路由规则的匹配条件，例如请求路径、请求头、请求参数等。
- `filters`：路由规则的过滤器，用于对请求进行拦截、转换、限流等操作。
- `metadata`：路由规则的元数据，用于描述路由规则的更多信息，例如服务名称、版本号、负责人等。

在 Spring Cloud Gateway 中，`Route` 类的实例通常通过 `RouteLocator` 接口来加载和管理，例如通过 `PropertiesRouteLocator` 加载配置文件中的路由规则，或通过 `DiscoveryClientRouteLocator` 加载注册中心中的服务实例。一旦加载完成，`Route` 对象就可以被用于将客户端的请求转发到对应的后端服务实例，实现微服务的动态路由和负载均衡。

需要注意的是，`Route` 类的使用要遵循 Spring Cloud Gateway 的设计原则和最佳实践，例如避免在路由规则中使用全局过滤器、使用合适的路由规则匹配条件、避免在路由规则中硬编码 IP 地址等。同时，也要注意 `Route` 类的生命周期和线程安全性，以确保其在高并发场景下的性能和可靠性。

`RouteDefinitionRouteLocator` 是 Spring Cloud Gateway 中的一个 `RouteLocator` 实现类，用于从配置文件或数据库中加载路由规则，并根据规则创建对应的 `Route` 对象，以实现动态路由和负载均衡的功能。

具体而言，`RouteDefinitionRouteLocator` 通过 `RouteDefinitionLocator` 接口来加载 `RouteDefinition` 对象，每个 `RouteDefinition` 对象包含了一条路由规则，包括 `id`、`uri`、`predicates`、`filters` 等属性。`RouteDefinitionRouteLocator` 在加载 `RouteDefinition` 对象后，会将其转换为对应的 `Route` 对象，并将 `Route` 对象添加到路由表中，以供客户端请求时匹配和转发。

`RouteDefinitionRouteLocator` 的使用非常灵活，您可以通过 Spring Boot 的配置文件（如 `application.yml` 或 `application.properties`）或通过编程的方式来加载 `RouteDefinition` 对象，例如：

```yaml
spring:
  cloud:
    gateway:
      routes:
        - id: myservice
          uri: http://localhost:8080
          predicates:
            - Path=/myservice/**
```

在上述例子中，`RouteDefinitionRouteLocator` 会根据配置文件中的路由规则，创建一个 ID 为 `myservice`、URI 为 `http://localhost:8080`、匹配条件为 `/myservice/**` 的 `Route` 对象。

需要注意的是，`RouteDefinitionRouteLocator` 可以与其他 `RouteLocator` 实现类组合使用，例如与 `DiscoveryClientRouteLocator` 结合使用，实现更加灵活和强大的路由功能。同时，您也可以自定义 `RouteLocator` 实现类，以满足更加特殊和定制化的路由需求。



在 Spring Cloud Gateway 中，`ServerWebExchangeUtils.GATEWAY_ROUTE_ATTR` 是一个关键的属性，它用于存储当前请求所匹配的路由规则，即 `Route` 对象。当请求进入 Gateway 后，通过一系列的过滤器和路由匹配器，Gateway 会根据请求的路径、请求头、请求参数等信息，匹配出所对应的路由规则，然后将路由规则存储在 `ServerWebExchange` 对象中的 `GATEWAY_ROUTE_ATTR` 属性中。

具体而言，当匹配到合适的路由规则后，Gateway 会创建一个新的 `Route` 对象，并将该对象设置为 `ServerWebExchange` 中的 `GATEWAY_ROUTE_ATTR` 属性值，以便后续的过滤器和处理器可以使用该对象来进行请求转发和负载均衡。例如，当请求进入 Gateway 后，可以通过以下代码获取当前请求所匹配的路由规则：

```java
Route route = exchange.getAttribute(ServerWebExchangeUtils.GATEWAY_ROUTE_ATTR);
```

在某些情况下，您可能需要重新构建 `Route` 对象，并将其设置为 `GATEWAY_ROUTE_ATTR` 属性值，以便后续的过滤器和处理器可以使用新的路由规则。例如，在某些动态路由的场景中，您可能需要根据请求的特定条件重新构建路由规则，以实现更加灵活和个性化的路由策略。此时，您可以通过以下代码来设置 `GATEWAY_ROUTE_ATTR` 属性值：

```java
exchange.getAttributes().put(ServerWebExchangeUtils.GATEWAY_ROUTE_ATTR, rebuildRoute);
```

其中，`rebuildRoute` 表示重新构建的 `Route` 对象。这样一来，后续的过滤器和处理器就可以使用新的路由规则来进行请求转发和负载均衡。

总之，`ServerWebExchangeUtils.GATEWAY_ROUTE_ATTR` 属性是 Spring Cloud Gateway 中非常重要的一个属性，它存储了当前请求所匹配的路由规则，可以帮助 Gateway 实现动态路由和负载均衡的功能。同时，您也可以根据实际需求重新构建路由规则，并将其设置为 `GATEWAY_ROUTE_ATTR` 属性值，以实现更加灵活和个性化的路由策略。



在 Spring Cloud Gateway 中，`Router` 是一个用于将客户端请求转发到后端服务实例的组件。`Router` 通常包含一个或多个 `Predicate` 条件和一个 `URI` 地址，用于匹配请求并将其转发到对应的后端服务实例。其中，`URI` 地址可以是一个具体的地址，也可以是一个 `lb` 开头的地址，用于实现负载均衡的功能。

具体而言，当 `URI` 地址以 `lb` 开头时，Spring Cloud Gateway 会将其解析为一个负载均衡器地址，并根据负载均衡策略将请求转发到对应的后端服务实例。例如，当 `URI` 地址为 `lb:erp-fi` 时，Gateway 会将其解析为一个名称为 `erp-fi` 的负载均衡器地址，并根据负载均衡策略选择一个可用的后端服务实例进行转发。

在实际使用中，您可以通过配置 Spring Cloud 的服务注册与发现功能，将多个后端服务实例注册到注册中心，并使用 `lb` 开头的 `URI` 地址来实现动态负载均衡的功能。例如，可以通过以下方式将服务实例注册到注册中心：

```yaml
spring:
  cloud:
    discovery:
      client:
        simple:
          instances:
            erp-fi:
              - uri: http://localhost:8081
              - uri: http://localhost:8082
```

在上述例子中，我们将名称为 `erp-fi` 的服务注册到了注册中心，并指定了两个后端服务实例，分别对应 `http://localhost:8081` 和 `http://localhost:8082` 两个地址。此时，我们可以通过以下方式来将客户端请求转发到 `erp-fi` 服务实例：

```java
@Bean
public RouteLocator customRouteLocator(RouteLocatorBuilder builder) {
    return builder.routes()
            .route("erp-fi", r -> r.path("/erp-fi/**")
                    .uri("lb:erp-fi"))
            .build();
}
```

在上述例子中，我们创建了一个名为 `erp-fi` 的路由规则，其中 `path` 属性用于匹配请求路径，`uri` 属性用于指定 `lb:erp-fi` 的负载均衡器地址。此时，Gateway 就可以根据负载均衡策略，将客户端请求转发到 `erp-fi` 服务实例中的任意一个可用实例上，实现动态负载均衡的功能。

总之，`Router` 中的 `URI` 地址可以是一个具体的地址，也可以是一个 `lb` 开头的地址，用于实现负载均衡的功能。您可以通过配置服务注册与发现功能，将多个后端服务实例注册到注册中心，并使用 `lb` 开头的 `URI` 地址来实现动态负载均衡的功能。


GatewayFilter
AddRequestParameterGatewayFilterFactory，为请求添加一个查询参数

spring:
  cloud:
    gateway:
      routes:
        - id: ${serviceId}
          filters:
            - AddRequestParameter=foo, bar        # 请求增加 foo=bar 这个参数

AddResponseHeaderGatewayFilterFactory，为请求的返回的 Header 中添加数据

spring:
  cloud:
    gateway:
      routes:
        - id: ${serviceId}
          filters:
            - AddResponseHeader=X-Response-Foo, bar   
            # Response Header 添加 key=X-Response-Foo, Valuebar

RetryGatewayFilterFactory，请求重试过滤器，当后端服务不可用时，根据配置参数发起重试请求

spring:
  cloud:
    gateway:
      routes:
        - id: ${serviceId}
          filters:
            - name: Retry
              args: 
                retries: 3				# 重试次数
                status: 503				# 针对 HTTP 请求返回状态码进行重试

RequestRateLimiterGatewayFilterFactory，对请求进行限流（被限流的请求会收到 Too Many Request）

由 org.springframework.cloud.gateway.filter.ratelimit.RedisRateLimiter 实现，其他参数参考实现类
spring:
  cloud:
    gateway:
      routes:
        - id: ${serviceId}
          filters:
            - name: RequestRateLimiter
              args: 
                redis-rate-limiter.replenishRate: 10				
                   # 令牌桶的令牌填充速度，代表允许每秒执行的请求数
                redis-rate-limiter.burstCapacity: 20				
                   # 令牌桶的容量，表示每秒用户最大能够执行的请求数量

jar包

- spring-cloud-starter-gateway
- spring-cloud-starter-core



org.springframework.cloud.gateway.filter.factory.RequestRateLimiterGatewayFilterFactory


org.springframework.cloud.gateway.route.builder.RouteLocatorBuilder


spring-web里面的类
org.springframework.web.server.ServerWebExchange
