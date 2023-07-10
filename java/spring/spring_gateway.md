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