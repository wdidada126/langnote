# spring_gateway

AbstractGatewayFilterFactory



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


DefaultServerWebExchange


https://gitee.com/edidada/my-gateway

lb标签负载均衡原理
