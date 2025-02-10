# springboot_actuator

spring actuator提供接口，k8s去调用接口查看应用状态

spring actuator 就绪 存活url搞反了
在Spring Boot应用中，Actuator是一个用于监控和管理应用的工具，它提供了多种端点（endpoints），比如 /actuator/health（健康检查）和 /actuator/readiness（就绪状态）等。如果你提到“就绪”和“存活”的 URL 搞反了，这可能是因为对这些端点的作用和默认路径理解有误。
1. Spring Actuator 的健康检查（存活状态）
/actuator/health 是用于检查应用的“存活状态”（Liveness）的端点。它主要用来判断应用是否正在运行，是否能够正常响应请求。通常，这个端点返回的状态码为 200 OK，表示应用是存活的。
2. Spring Actuator 的就绪状态
/actuator/readiness 是用于检查应用的“就绪状态”（Readiness）的端点。它不仅检查应用是否存活，还会检查应用是否已经准备好接受流量（比如数据库连接是否正常、依赖服务是否可用等）。如果应用尚未准备好，这个端点可能会返回 503 Service Unavailable 状态码。
3. 可能的原因
如果你提到“就绪”和“存活”的 URL 搞反了，可能是因为以下原因：
配置错误：你可能在配置文件中错误地设置了 Actuator 的端点路径。
理解错误：你可能混淆了 /actuator/health 和 /actuator/readiness 的作用。


Spring Boot Actuator 提供了多种端点用于监控和管理应用状态。关于 /actuator/health/liveness 和 /actuator/health/readiness 的问题

https://docs.spring.io/spring-boot/reference/actuator/endpoints.html


https://spring.io/guides/gs/actuator-service/

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
```

/actuator/health和/actuator/info

endpoint

监控es
rabbit
mysql
web




## 源码 2.3.12

[Overview (Spring Boot 2.3.12.RELEASE API)](https://docs.spring.io/spring-boot/docs/2.3.x/api/)



## org.springframework.boot.actuate.amqp



RabbitHealthIndicator



## org.springframework.boot.actuate.audit



| org.springframework.boot.actuate.audit    |      |      |
| ----------------------------------------- | ---- | ---- |
| AuditEventRepository                      |      |      |
|                                           |      |      |
| Classes                                   |      |      |
|                                           |      |      |
| AuditEvent                                |      |      |
| AuditEventsEndpoint                       |      |      |
| AuditEventsEndpoint.AuditEventsDescriptor |      |      |
| InMemoryAuditEventRepository              |      |      |







### org.springframework.boot.actuate.audit.listener

AbstractAuditListener

AuditApplicationEvent

AuditListener



### org.springframework.boot.actuate.availability



Interfaces

AvailabilityStateHealthIndicator.StatusMappings

Classes

AvailabilityStateHealthIndicator

LivenessStateHealthIndicator

ReadinessStateHealthIndicator





### org.springframework.boot.actuate.beans



BeansEndpoint

BeansEndpoint.ApplicationBeans

BeansEndpoint.BeanDescriptor

BeansEndpoint.ContextBeans



## org.springframework.boot.actuate.cache



| org.springframework.boot.actuate.cache |      |      |
| -------------------------------------- | ---- | ---- |
| CachesEndpoint                         |      |      |
| CachesEndpoint.CacheDescriptor         |      |      |
| CachesEndpoint.CacheEntry              |      |      |
| CachesEndpoint.CacheManagerDescriptor  |      |      |
| CachesEndpoint.CachesReport            |      |      |
| CachesEndpointWebExtension             |      |      |
|                                        |      |      |
| Exceptions                             |      |      |
|                                        |      |      |
| NonUniqueCacheException                |      |      |







## org.springframework.boot.actuate.cassandra



|                                  |      |      |
| -------------------------------- | ---- | ---- |
| CassandraHealthIndicator         |      |      |
| CassandraReactiveHealthIndicator |      |      |





## org.springframework.boot.actuate.context



​	ShutdownEndpoint



### org.springframework.boot.actuate.context.properties



|                                                              |      |      |
| ------------------------------------------------------------ | ---- | ---- |
| ConfigurationPropertiesReportEndpoint                        |      |      |
| ConfigurationPropertiesReportEndpoint.ApplicationConfigurationProperties |      |      |
| ConfigurationPropertiesReportEndpoint.ConfigurationPropertiesBeanDescriptor |      |      |
| ConfigurationPropertiesReportEndpoint.ContextConfigurationProperties |      |      |
| ConfigurationPropertiesReportEndpoint.GenericSerializerModifier |      |      |





## org.springframework.boot.actuate.couchbase





## CouchbaseHealth



CouchbaseHealthIndicator

CouchbaseReactiveHealthIndicator



## org.springframework.boot.actuate.elasticsearch



ElasticsearchReactiveHealthIndicator

ElasticsearchRestHealthIndicator



## org.springframework.boot.actuate.endpoint



| org.springframework.boot.actuate.endpoint |      |      |
| ----------------------------------------- | ---- | ---- |
| EndpointFilter                            |      |      |
| EndpointsSupplier                         |      |      |
| ExposableEndpoint                         |      |      |
| Operation                                 |      |      |
| SecurityContext                           |      |      |
|                                           |      |      |
| Classes                                   |      |      |
|                                           |      |      |
| AbstractExposableEndpoint                 |      |      |
| EndpointId                                |      |      |
| InvocationContext                         |      |      |
| Sanitizer                                 |      |      |
|                                           |      |      |
| Enums                                     |      |      |
|                                           |      |      |
| OperationType                             |      |      |
|                                           |      |      |
| Exceptions                                |      |      |
|                                           |      |      |
| InvalidEndpointRequestException           |      |      |





org.springframework.boot.actuate.endpoint.annotation





| org.springframework.boot.actuate.endpoint.annotation |      |      |
| ---------------------------------------------------- | ---- | ---- |
| DiscoveredEndpoint                                   |      |      |
|                                                      |      |      |
| Classes                                              |      |      |
|                                                      |      |      |
| AbstractDiscoveredEndpoint                           |      |      |
| AbstractDiscoveredOperation                          |      |      |
| DiscoveredOperationMethod                            |      |      |
| DiscovererEndpointFilter                             |      |      |
| EndpointDiscoverer                                   |      |      |
| EndpointDiscoverer.OperationKey                      |      |      |
|                                                      |      |      |
| Enums                                                |      |      |
|                                                      |      |      |
| Selector.Match                                       |      |      |
|                                                      |      |      |
| Annotation Types                                     |      |      |
|                                                      |      |      |
| DeleteOperation                                      |      |      |
| Endpoint                                             |      |      |
| EndpointConverter                                    |      |      |
| EndpointExtension                                    |      |      |
| FilteredEndpoint                                     |      |      |
| ReadOperation                                        |      |      |
| Selector                                             |      |      |
| WriteOperation                                       |      |      |



org.springframework.boot.actuate.endpoint.http



ActuatorMediaType

Enums

ApiVersion



org.springframework.boot.actuate.endpoint.invoke



| org.springframework.boot.actuate.endpoint.invoke |      |      |
| ------------------------------------------------ | ---- | ---- |
| OperationInvoker                                 |      |      |
| OperationInvokerAdvisor                          |      |      |
| OperationParameter                               |      |      |
| OperationParameters                              |      |      |
| ParameterValueMapper                             |      |      |
|                                                  |      |      |
| Exceptions                                       |      |      |
|                                                  |      |      |
| MissingParametersException                       |      |      |
| ParameterMappingException                        |      |      |



org.springframework.boot.actuate.endpoint.invoke.convert



ConversionServiceParameterValueMapper

IsoOffsetDateTimeConverter



org.springframework.boot.actuate.endpoint.invoke.reflect



OperationMethod

ReflectiveOperationInvoker



org.springframework.boot.actuate.endpoint.invoker.cache



CachingOperationInvoker

CachingOperationInvokerAdvisor



org.springframework.boot.actuate.endpoint.jmx



| org.springframework.boot.actuate.endpoint.jmx |      |      |
| --------------------------------------------- | ---- | ---- |
| EndpointObjectNameFactory                     |      |      |
| ExposableJmxEndpoint                          |      |      |
| JmxEndpointsSupplier                          |      |      |
| JmxOperation                                  |      |      |
| JmxOperationParameter                         |      |      |
| JmxOperationResponseMapper                    |      |      |
|                                               |      |      |
| Classes                                       |      |      |
|                                               |      |      |
| EndpointMBean                                 |      |      |
| JacksonJmxOperationResponseMapper             |      |      |
| JmxEndpointExporter                           |      |      |



org.springframework.boot.actuate.endpoint.jmx.annotation



JmxEndpointDiscoverer

Annotation Types

EndpointJmxExtension

JmxEndpoint



org.springframework.boot.actuate.endpoint.web



| org.springframework.boot.actuate.endpoint.web |      |      |
| --------------------------------------------- | ---- | ---- |
| ExposableServletEndpoint                      |      |      |
| ExposableWebEndpoint                          |      |      |
| PathMappedEndpoint                            |      |      |
| PathMapper                                    |      |      |
| WebEndpointsSupplier                          |      |      |
| WebOperation                                  |      |      |
|                                               |      |      |
| Classes                                       |      |      |
|                                               |      |      |
| EndpointLinksResolver                         |      |      |
| EndpointMapping                               |      |      |
| EndpointMediaTypes                            |      |      |
| EndpointServlet                               |      |      |
| Link                                          |      |      |
| PathMappedEndpoints                           |      |      |
| ServletEndpointRegistrar                      |      |      |
| WebEndpointResponse                           |      |      |
| WebOperationRequestPredicate                  |      |      |
|                                               |      |      |
| Enums                                         |      |      |
|                                               |      |      |
| WebEndpointHttpMethod                         |      |      |





org.springframework.boot.actuate.endpoint.web.annotation



| org.springframework.boot.actuate.endpoint.web.annotation |      |      |
| -------------------------------------------------------- | ---- | ---- |
| ControllerEndpointsSupplier                              |      |      |
| ExposableControllerEndpoint                              |      |      |
| ServletEndpointsSupplier                                 |      |      |
|                                                          |      |      |
| Classes                                                  |      |      |
|                                                          |      |      |
| ControllerEndpointDiscoverer                             |      |      |
| ServletEndpointDiscoverer                                |      |      |
| WebEndpointDiscoverer                                    |      |      |
|                                                          |      |      |
| Annotation Types                                         |      |      |
|                                                          |      |      |
| ControllerEndpoint                                       |      |      |
| EndpointWebExtension                                     |      |      |
| RestControllerEndpoint                                   |      |      |
| ServletEndpoint                                          |      |      |
| WebEndpoint                                              |      |      |





org.springframework.boot.actuate.endpoint.web.jersey



JerseyEndpointResourceFactory



org.springframework.boot.actuate.endpoint.web.reactive



| org.springframework.boot.actuate.endpoint.web.reactive       |      |      |
| ------------------------------------------------------------ | ---- | ---- |
| AbstractWebFluxEndpointHandlerMapping.LinksHandler           |      |      |
| AbstractWebFluxEndpointHandlerMapping.ReactiveWebOperation   |      |      |
|                                                              |      |      |
| Classes                                                      |      |      |
|                                                              |      |      |
| AbstractWebFluxEndpointHandlerMapping                        |      |      |
| AbstractWebFluxEndpointHandlerMapping.ElasticSchedulerInvoker |      |      |
| ControllerEndpointHandlerMapping                             |      |      |
| WebFluxEndpointHandlerMapping                                |      |      |



org.springframework.boot.actuate.endpoint.web.servlet

| org.springframework.boot.actuate.endpoint.web.servlet    |      |      |
| -------------------------------------------------------- | ---- | ---- |
| AbstractWebMvcEndpointHandlerMapping.LinksHandler        |      |      |
| AbstractWebMvcEndpointHandlerMapping.ServletWebOperation |      |      |
|                                                          |      |      |
| Classes                                                  |      |      |
|                                                          |      |      |
| AbstractWebMvcEndpointHandlerMapping                     |      |      |
| ControllerEndpointHandlerMapping                         |      |      |
| WebMvcEndpointHandlerMapping                             |      |      |





## org.springframework.boot.actuate.env



EnvironmentEndpoint

EnvironmentEndpointWebExtension



## org.springframework.boot.actuate.flyway





| org.springframework.boot.actuate.flyway |      |      |
| --------------------------------------- | ---- | ---- |
| FlywayEndpoint                          |      |      |
| FlywayEndpoint.ApplicationFlywayBeans   |      |      |
| FlywayEndpoint.ContextFlywayBeans       |      |      |
| FlywayEndpoint.FlywayDescriptor         |      |      |
| FlywayEndpoint.FlywayMigration          |      |      |



## org.springframework.boot.actuate.hazelcast



HazelcastHealthIndicator



## org.springframework.boot.actuate.health



|                                          |      |      |
| ---------------------------------------- | ---- | ---- |
| CompositeHealthContributor               |      |      |
| CompositeReactiveHealthContributor       |      |      |
| ContributorRegistry                      |      |      |
| HealthAggregator                         |      |      |
| HealthContributor                        |      |      |
| HealthContributorRegistry                |      |      |
| HealthEndpointGroup                      |      |      |
| HealthEndpointGroups                     |      |      |
| HealthEndpointGroupsPostProcessor        |      |      |
| HealthIndicator                          |      |      |
| HealthIndicatorRegistry                  |      |      |
| HttpCodeStatusMapper                     |      |      |
| NamedContributor                         |      |      |
| NamedContributors                        |      |      |
| ReactiveHealthContributor                |      |      |
| ReactiveHealthContributorRegistry        |      |      |
| ReactiveHealthIndicator                  |      |      |
| ReactiveHealthIndicatorRegistry          |      |      |
| StatusAggregator                         |      |      |
|                                          |      |      |
| Classes                                  |      |      |
|                                          |      |      |
| AbstractHealthAggregator                 |      |      |
| AbstractHealthIndicator                  |      |      |
| AbstractReactiveHealthIndicator          |      |      |
| CompositeHealth                          |      |      |
| CompositeHealthIndicator                 |      |      |
| CompositeReactiveHealthIndicator         |      |      |
| DefaultHealthContributorRegistry         |      |      |
| DefaultHealthIndicatorRegistry           |      |      |
| DefaultReactiveHealthContributorRegistry |      |      |
| DefaultReactiveHealthIndicatorRegistry   |      |      |
| Health                                   |      |      |
| Health.Builder                           |      |      |
| HealthComponent                          |      |      |
| HealthContributorNameFactory             |      |      |
| HealthEndpoint                           |      |      |
| HealthEndpointWebExtension               |      |      |
| HealthIndicatorNameFactory               |      |      |
| HealthIndicatorReactiveAdapter           |      |      |
| HealthIndicatorRegistryFactory           |      |      |
| OrderedHealthAggregator                  |      |      |
| PingHealthIndicator                      |      |      |
| ReactiveHealthEndpointWebExtension       |      |      |
| ReactiveHealthIndicatorRegistryFactory   |      |      |
| SimpleHttpCodeStatusMapper               |      |      |
| SimpleStatusAggregator                   |      |      |
| Status                                   |      |      |
| SystemHealth                             |      |      |





## org.springframework.boot.actuate.influx



InfluxDbHealthIndicator



| org.springframework.boot.actuate.influx |      |      |
| --------------------------------------- | ---- | ---- |
| InfoContributor                         |      |      |
|                                         |      |      |
| Classes                                 |      |      |
|                                         |      |      |
| BuildInfoContributor                    |      |      |
| EnvironmentInfoContributor              |      |      |
| GitInfoContributor                      |      |      |
| Info                                    |      |      |
| Info.Builder                            |      |      |
| InfoEndpoint                            |      |      |
| InfoPropertiesInfoContributor           |      |      |
| MapInfoContributor                      |      |      |
| SimpleInfoContributor                   |      |      |
|                                         |      |      |
| Enums                                   |      |      |
|                                         |      |      |
| InfoPropertiesInfoContributor.Mode      |      |      |





## org.springframework.boot.actuate.integration



IntegrationGraphEndpoint

org.springframework.boot.actuate.jdbc



DataSourceHealthIndicator



org.springframework.boot.actuate.jms



JmsHealthIndicator

org.springframework.boot.actuate.ldap



LdapHealthIndicator



org.springframework.boot.actuate.liquibase



LiquibaseEndpoint

LiquibaseEndpoint.ApplicationLiquibaseBeans

LiquibaseEndpoint.ChangeSet

LiquibaseEndpoint.ContextExpression

LiquibaseEndpoint.ContextLiquibaseBeans

LiquibaseEndpoint.LiquibaseBean



org.springframework.boot.actuate.logging



LogFileWebEndpoint

LoggersEndpoint

LoggersEndpoint.GroupLoggerLevels

LoggersEndpoint.LoggerLevels

LoggersEndpoint.SingleLoggerLevels



org.springframework.boot.actuate.mail



MailHealthIndicator



org.springframework.boot.actuate.management



|                                                       |      |      |
| ----------------------------------------------------- | ---- | ---- |
| HeapDumpWebEndpoint.HeapDumper                        |      |      |
|                                                       |      |      |
| Classes                                               |      |      |
|                                                       |      |      |
| HeapDumpWebEndpoint                                   |      |      |
| HeapDumpWebEndpoint.HotSpotDiagnosticMXBeanHeapDumper |      |      |
| ThreadDumpEndpoint                                    |      |      |
| ThreadDumpEndpoint.ThreadDumpDescriptor               |      |      |
|                                                       |      |      |
| Exceptions                                            |      |      |
|                                                       |      |      |
| HeapDumpWebEndpoint.HeapDumperUnavailableException    |      |      |



org.springframework.boot.actuate.metrics

|                                   |      |      |
| --------------------------------- | ---- | ---- |
| AutoTimer                         |      |      |
|                                   |      |      |
| Classes                           |      |      |
|                                   |      |      |
| MetricsEndpoint                   |      |      |
| MetricsEndpoint.AvailableTag      |      |      |
| MetricsEndpoint.ListNamesResponse |      |      |
| MetricsEndpoint.MetricResponse    |      |      |
| MetricsEndpoint.Sample            |      |      |
|                                   |      |      |
|                                   |      |      |
|                                   |      |      |



org.springframework.boot.actuate.metrics.amqp



RabbitMetrics



org.springframework.boot.actuate.metrics.cache



| org.springframework.boot.actuate.metrics.cache |      |      |
| ---------------------------------------------- | ---- | ---- |
| CacheMeterBinderProvider                       |      |      |
|                                                |      |      |
| Classes                                        |      |      |
|                                                |      |      |
| CacheMetricsRegistrar                          |      |      |
| CaffeineCacheMeterBinderProvider               |      |      |
| EhCache2CacheMeterBinderProvider               |      |      |
| HazelcastCacheMeterBinderProvider              |      |      |
| JCacheCacheMeterBinderProvider                 |      |      |



org.springframework.boot.actuate.metrics.export.prometheus



PrometheusPushGatewayManager

PrometheusScrapeEndpoint

Enums

PrometheusPushGatewayManager.ShutdownOperation



org.springframework.boot.actuate.metrics.http



Outcome



org.springframework.boot.actuate.metrics.jdbc



DataSourcePoolMetrics



org.springframework.boot.actuate.metrics.r2dbc



ConnectionPoolMetrics



org.springframework.boot.actuate.metrics.web.client



| org.springframework.boot.actuate.metrics.web.client |      |      |
| --------------------------------------------------- | ---- | ---- |
| RestTemplateExchangeTagsProvider                    |      |      |
|                                                     |      |      |
| Classes                                             |      |      |
|                                                     |      |      |
| DefaultRestTemplateExchangeTagsProvider             |      |      |
| MetricsRestTemplateCustomizer                       |      |      |
| RestTemplateExchangeTags                            |      |      |



org.springframework.boot.actuate.metrics.web.jetty



JettyServerThreadPoolMetricsBinder



org.springframework.boot.actuate.metrics.web.reactive.client



| org.springframework.boot.actuate.metrics.web.reactive.client |      |      |
| ------------------------------------------------------------ | ---- | ---- |
| WebClientExchangeTagsProvider                                |      |      |
|                                                              |      |      |
| Classes                                                      |      |      |
|                                                              |      |      |
| DefaultWebClientExchangeTagsProvider                         |      |      |
| MetricsWebClientCustomizer                                   |      |      |
| MetricsWebClientFilterFunction                               |      |      |
| WebClientExchangeTags                                        |      |      |



org.springframework.boot.actuate.metrics.web.reactive.server



| org.springframework.boot.actuate.metrics.web.reactive.server |      |      |
| ------------------------------------------------------------ | ---- | ---- |
| WebFluxTagsContributor                                       |      |      |
| WebFluxTagsProvider                                          |      |      |
|                                                              |      |      |
| Classes                                                      |      |      |
|                                                              |      |      |
| DefaultWebFluxTagsProvider                                   |      |      |
| MetricsWebFilter                                             |      |      |
| WebFluxTags                                                  |      |      |



org.springframework.boot.actuate.metrics.web.servlet



|                                  |      |      |
| -------------------------------- | ---- | ---- |
| WebMvcTagsContributor            |      |      |
| WebMvcTagsProvider               |      |      |
|                                  |      |      |
| Classes                          |      |      |
|                                  |      |      |
| DefaultWebMvcTagsProvider        |      |      |
| LongTaskTimingHandlerInterceptor |      |      |
| WebMvcMetricsFilter              |      |      |
| WebMvcTags                       |      |      |



org.springframework.boot.actuate.metrics.web.tomcat



TomcatMetricsBinder



org.springframework.boot.actuate.mongo



MongoHealthIndicator

MongoReactiveHealthIndicator





## org.springframework.boot.actuate.neo4j

Neo4jHealthIndicator





## org.springframework.boot.actuate.r2dbc



ConnectionFactoryHealthIndicator





## org.springframework.boot.actuate.redis



RedisHealthIndicator

RedisReactiveHealthIndicator



## org.springframework.boot.actuate.scheduling



| org.springframework.boot.actuate.scheduling         |      |      |
| --------------------------------------------------- | ---- | ---- |
| ScheduledTasksEndpoint                              |      |      |
| ScheduledTasksEndpoint.CronTaskDescription          |      |      |
| ScheduledTasksEndpoint.CustomTriggerTaskDescription |      |      |
| ScheduledTasksEndpoint.FixedDelayTaskDescription    |      |      |
| ScheduledTasksEndpoint.FixedRateTaskDescription     |      |      |
| ScheduledTasksEndpoint.IntervalTaskDescription      |      |      |
| ScheduledTasksEndpoint.RunnableDescription          |      |      |
| ScheduledTasksEndpoint.ScheduledTasksReport         |      |      |
| ScheduledTasksEndpoint.TaskDescription              |      |      |
|                                                     |      |      |



## org.springframework.boot.actuate.security



| org.springframework.boot.actuate.security |      |      |
| ----------------------------------------- | ---- | ---- |
| AbstractAuthenticationAuditListener       |      |      |
| AbstractAuthorizationAuditListener        |      |      |
| AuthenticationAuditListener               |      |      |
| AuthorizationAuditListener                |      |      |





## org.springframework.boot.actuate.session

| org.springframework.boot.actuate.session |      |      |
| ---------------------------------------- | ---- | ---- |
| SessionsEndpoint                         |      |      |
| SessionsEndpoint.SessionDescriptor       |      |      |
| SessionsEndpoint.SessionsReport          |      |      |





## org.springframework.boot.actuate.solr



| org.springframework.boot.actuate.solr         |      |      |
| --------------------------------------------- | ---- | ---- |
| SolrHealthIndicator                           |      |      |
| SolrHealthIndicator.ParticularCoreStatusCheck |      |      |
| SolrHealthIndicator.RootStatusCheck           |      |      |
| SolrHealthIndicator.StatusCheck               |      |      |



## org.springframework.boot.actuate.system



DiskSpaceHealthIndicator



## org.springframework.boot.actuate.trace.http



| org.springframework.boot.actuate.trace.http |      |      |
| ------------------------------------------- | ---- | ---- |
| HttpTraceRepository                         |      |      |
| TraceableRequest                            |      |      |
| TraceableResponse                           |      |      |
|                                             |      |      |
| Classes                                     |      |      |
|                                             |      |      |
| HttpExchangeTracer                          |      |      |
| HttpTrace                                   |      |      |
| HttpTrace.Principal                         |      |      |
| HttpTrace.Request                           |      |      |
| HttpTrace.Response                          |      |      |
| HttpTrace.Session                           |      |      |
| HttpTraceEndpoint                           |      |      |
| HttpTraceEndpoint.HttpTraceDescriptor       |      |      |
| InMemoryHttpTraceRepository                 |      |      |
|                                             |      |      |
| Enums                                       |      |      |
|                                             |      |      |
| Include                                     |      |      |