spring-boot-autoconfigure

https://docs.spring.io/spring-boot/docs/2.3.x/api/


## 源代码分包解析


### springboot autoconfig
## org.springframework.boot.autoconfigure

| org.springframework.boot.autoconfigure                 | 类型       | 笔记 |
| ------------------------------------------------------ | ---------- | ---- |
| AutoConfigurationImportFilter                          |            |      |
| AutoConfigurationImportListener                        |            |      |
| AutoConfigurationMetadata                              |            |      |
|                                                        |            |      |
| Classes                                                |            |      |
|                                                        |            |      |
| AbstractDependsOnBeanFactoryPostProcessor              |            |      |
| AutoConfigurationExcludeFilter                         |            |      |
| AutoConfigurationImportEvent                           |            |      |
| AutoConfigurationImportSelector                        |            |      |
| AutoConfigurationImportSelector.AutoConfigurationEntry |            |      |
| AutoConfigurationPackages                              |            |      |
| AutoConfigurations                                     |            |      |
| BackgroundPreinitializer                               |            |      |
|                                                        |            |      |
| Annotation Types                                       |            |      |
|                                                        |            |      |
| AutoConfigurationPackage                               | @interface |      |
| AutoConfigureAfter                                     | @interface |      |
| AutoConfigureBefore                                    | @interface |      |
| AutoConfigureOrder                                     | @interface |      |
| EnableAutoConfiguration                                | @interface |      |
| ImportAutoConfiguration                                | @interface |      |
| SpringBootApplication                                  | @interface |      |



ApplicationContextInitializer
ApplicationListener





### org.springframework.boot.autoconfigure.admin



SpringApplicationAdminJmxAutoConfiguration



### org.springframework.boot.autoconfigure.amqp



| org.springframework.boot.autoconfigure.amqp            |      |      |
| ------------------------------------------------------ | ---- | ---- |
| RabbitRetryTemplateCustomizer                          |      |      |
|                                                        |      |      |
| Classes                                                |      |      |
|                                                        |      |      |
| AbstractRabbitListenerContainerFactoryConfigurer       |      |      |
| DirectRabbitListenerContainerFactoryConfigurer         |      |      |
| RabbitAutoConfiguration                                |      |      |
| RabbitAutoConfiguration.MessagingTemplateConfiguration |      |      |
| RabbitAutoConfiguration.RabbitConnectionFactoryCreator |      |      |
| RabbitAutoConfiguration.RabbitTemplateConfiguration    |      |      |
| RabbitProperties                                       |      |      |
| RabbitProperties.AmqpContainer                         |      |      |
| RabbitProperties.Cache                                 |      |      |
| RabbitProperties.Cache.Channel                         |      |      |
| RabbitProperties.Cache.Connection                      |      |      |
| RabbitProperties.DirectContainer                       |      |      |
| RabbitProperties.Listener                              |      |      |
| RabbitProperties.ListenerRetry                         |      |      |
| RabbitProperties.Retry                                 |      |      |
| RabbitProperties.SimpleContainer                       |      |      |
| RabbitProperties.Template                              |      |      |
| RabbitTemplateConfigurer                               |      |      |
| SimpleRabbitListenerContainerFactoryConfigurer         |      |      |
|                                                        |      |      |
| Enums                                                  |      |      |
|                                                        |      |      |
| RabbitProperties.ContainerType                         |      |      |
| RabbitRetryTemplateCustomizer.Target                   |      |      |



### org.springframework.boot.autoconfigure.aop



AopAutoConfiguration



### org.springframework.boot.autoconfigure.availability



ApplicationAvailabilityAutoConfiguration



### org.springframework.boot.autoconfigure.batch



| org.springframework.boot.autoconfigure.batch |      |      |
| -------------------------------------------- | ---- | ---- |
| BasicBatchConfigurer                         |      |      |
| BatchAutoConfiguration                       |      |      |
| BatchDataSourceInitializer                   |      |      |
| BatchProperties                              |      |      |
| BatchProperties.Job                          |      |      |
| JobExecutionEvent                            |      |      |
| JobExecutionExitCodeGenerator                |      |      |
| JobLauncherApplicationRunner                 |      |      |
| JobLauncherCommandLineRunner                 |      |      |
| JpaBatchConfigurer                           |      |      |
|                                              |      |      |
| Annotation Types                             |      |      |
|                                              |      |      |
| BatchDataSource                              |      |      |



### org.springframework.boot.autoconfigure.cache



|                                        |      |      |
| -------------------------------------- | ---- | ---- |
| CacheManagerCustomizer                 |      |      |
| CouchbaseCacheManagerBuilderCustomizer |      |      |
| JCacheManagerCustomizer                |      |      |
| RedisCacheManagerBuilderCustomizer     |      |      |
|                                        |      |      |
| Classes                                |      |      |
|                                        |      |      |
| CacheAutoConfiguration                 |      |      |
| CacheManagerCustomizers                |      |      |
| CacheProperties                        |      |      |
| CacheProperties.Caffeine               |      |      |
| CacheProperties.Couchbase              |      |      |
| CacheProperties.EhCache                |      |      |
| CacheProperties.Infinispan             |      |      |
| CacheProperties.JCache                 |      |      |
| CacheProperties.Redis                  |      |      |
| CouchbaseCacheConfiguration            |      |      |
| InfinispanCacheConfiguration           |      |      |
|                                        |      |      |
| Enums                                  |      |      |
|                                        |      |      |
| CacheType                              |      |      |



### org.springframework.boot.autoconfigure.cassandra



|                                     |      |      |
| ----------------------------------- | ---- | ---- |
| CqlSessionBuilderCustomizer         |      |      |
| DriverConfigLoaderBuilderCustomizer |      |      |
|                                     |      |      |
| Classes                             |      |      |
|                                     |      |      |
| CassandraAutoConfiguration          |      |      |
| CassandraProperties                 |      |      |
| CassandraProperties.Connection      |      |      |
| CassandraProperties.Pool            |      |      |
| CassandraProperties.Request         |      |      |
| CassandraProperties.Throttler       |      |      |
|                                     |      |      |
| Enums                               |      |      |
|                                     |      |      |
| CassandraProperties.Compression     |      |      |
| CassandraProperties.ThrottlerType   |      |      |



### org.springframework.boot.autoconfigure.codec



CodecProperties



### org.springframework.boot.autoconfigure.condition



|                                                |      |      |
| ---------------------------------------------- | ---- | ---- |
| AbstractNestedCondition                        |      |      |
| AbstractNestedCondition.MemberMatchOutcomes    |      |      |
| AllNestedConditions                            |      |      |
| AnyNestedCondition                             |      |      |
| ConditionEvaluationReport                      |      |      |
| ConditionEvaluationReport.ConditionAndOutcome  |      |      |
| ConditionEvaluationReport.ConditionAndOutcomes |      |      |
| ConditionMessage                               |      |      |
| ConditionOutcome                               |      |      |
| NoneNestedConditions                           |      |      |
| OnPropertyListCondition                        |      |      |
| ResourceCondition                              |      |      |
| SpringBootCondition                            |      |      |
|                                                |      |      |
| Enums                                          |      |      |
|                                                |      |      |
| ConditionalOnJava.Range                        |      |      |
| ConditionalOnWebApplication.Type               |      |      |
| ConditionMessage.Style                         |      |      |
| SearchStrategy                                 |      |      |
|                                                |      |      |
| Annotation Types                               |      |      |
|                                                |      |      |
| ConditionalOnBean                              |      |      |
| ConditionalOnClass                             |      |      |
| ConditionalOnCloudPlatform                     |      |      |
| ConditionalOnExpression                        |      |      |
| ConditionalOnJava                              |      |      |
| ConditionalOnJndi                              |      |      |
| ConditionalOnMissingBean                       |      |      |
| ConditionalOnMissingClass                      |      |      |
| ConditionalOnNotWebApplication                 |      |      |
| ConditionalOnProperty                          |      |      |
| ConditionalOnResource                          |      |      |
| ConditionalOnSingleCandidate                   |      |      |
| ConditionalOnWarDeployment                     |      |      |
| ConditionalOnWebApplication                    |      |      |



### org.springframework.boot.autoconfigure.context

### org.springframework.boot.autoconfigure.couchbase

### org.springframework.boot.autoconfigure.dao

### org.springframework.boot.autoconfigure.data

#### org.springframework.boot.autoconfigure.data.cassandra

#### org.springframework.boot.autoconfigure.data.couchbase

#### org.springframework.boot.autoconfigure.data.elasticsearch

#### org.springframework.boot.autoconfigure.data.jdbc

#### org.springframework.boot.autoconfigure.data.jpa

#### org.springframework.boot.autoconfigure.data.ldap

#### org.springframework.boot.autoconfigure.data.mongo

#### org.springframework.boot.autoconfigure.data.neo4j

#### org.springframework.boot.autoconfigure.data.r2dbc

#### org.springframework.boot.autoconfigure.data.redis

#### org.springframework.boot.autoconfigure.data.rest

#### org.springframework.boot.autoconfigure.data.solr

#### org.springframework.boot.autoconfigure.data.web

### org.springframework.boot.autoconfigure.domain

### org.springframework.boot.autoconfigure.elasticsearch

#### org.springframework.boot.autoconfigure.elasticsearch.rest

### org.springframework.boot.autoconfigure.flyway

### org.springframework.boot.autoconfigure.freemarker

#### org.springframework.boot.autoconfigure.groovy.template

### org.springframework.boot.autoconfigure.gson

### org.springframework.boot.autoconfigure.h2

### org.springframework.boot.autoconfigure.hateoas

### org.springframework.boot.autoconfigure.hazelcast

### org.springframework.boot.autoconfigure.http

#### org.springframework.boot.autoconfigure.http.codec

### org.springframework.boot.autoconfigure.influx

### org.springframework.boot.autoconfigure.info

### org.springframework.boot.autoconfigure.integration

### org.springframework.boot.autoconfigure.jackson



### org.springframework.boot.autoconfigure.jdbc



| org.springframework.boot.autoconfigure.jdbc               |      |      |
| --------------------------------------------------------- | ---- | ---- |
| DataSourceAutoConfiguration                               |      |      |
| DataSourceAutoConfiguration.EmbeddedDatabaseConfiguration |      |      |
| DataSourceAutoConfiguration.PooledDataSourceConfiguration |      |      |
| DataSourceProperties                                      |      |      |
| DataSourceProperties.Xa                                   |      |      |
| DataSourceSchemaCreatedEvent                              |      |      |
| DataSourceTransactionManagerAutoConfiguration             |      |      |
| EmbeddedDataSourceConfiguration                           |      |      |
| JdbcOperationsDependsOnPostProcessor                      |      |      |
| JdbcProperties                                            |      |      |
| JdbcProperties.Template                                   |      |      |
| JdbcTemplateAutoConfiguration                             |      |      |
| JndiDataSourceAutoConfiguration                           |      |      |
| NamedParameterJdbcOperationsDependsOnPostProcessor        |      |      |
| XADataSourceAutoConfiguration                             |      |      |



org.mybatis.spring.boot.autoconfigure.MybatisAutoConfiguration
使用DataSourceAutoConfiguration




#### org.springframework.boot.autoconfigure.jdbc.metadata

### org.springframework.boot.autoconfigure.jersey

### org.springframework.boot.autoconfigure.jms

#### org.springframework.boot.autoconfigure.jms.activemq

#### org.springframework.boot.autoconfigure.jms.artemis

### org.springframework.boot.autoconfigure.jmx

### org.springframework.boot.autoconfigure.jooq

### org.springframework.boot.autoconfigure.jsonb

### org.springframework.boot.autoconfigure.kafka

### org.springframework.boot.autoconfigure.ldap

#### org.springframework.boot.autoconfigure.ldap.embedded

### org.springframework.boot.autoconfigure.liquibase

### org.springframework.boot.autoconfigure.logging

### org.springframework.boot.autoconfigure.mail

### org.springframework.boot.autoconfigure.mongo

#### org.springframework.boot.autoconfigure.mongo.embedded

### org.springframework.boot.autoconfigure.mustache

### org.springframework.boot.autoconfigure.orm.jpa

### org.springframework.boot.autoconfigure.quartz

### org.springframework.boot.autoconfigure.r2dbc

### org.springframework.boot.autoconfigure.rsocket

### org.springframework.boot.autoconfigure.security
#### org.springframework.boot.autoconfigure.security.oauth2
##### org.springframework.boot.autoconfigure.security.oauth2.client

##### org.springframework.boot.autoconfigure.security.oauth2.client.reactive

##### org.springframework.boot.autoconfigure.security.oauth2.client.servlet

##### org.springframework.boot.autoconfigure.security.oauth2.resource

##### org.springframework.boot.autoconfigure.security.oauth2.resource.reactive

##### org.springframework.boot.autoconfigure.security.oauth2.resource.servlet

#### org.springframework.boot.autoconfigure.security.reactive

#### org.springframework.boot.autoconfigure.security.rsocket

#### org.springframework.boot.autoconfigure.security.saml2

#### org.springframework.boot.autoconfigure.security.servlet

### org.springframework.boot.autoconfigure.sendgrid

### org.springframework.boot.autoconfigure.session

### org.springframework.boot.autoconfigure.solr

### org.springframework.boot.autoconfigure.task

### org.springframework.boot.autoconfigure.template

### org.springframework.boot.autoconfigure.thymeleaf

### org.springframework.boot.autoconfigure.transaction

#### org.springframework.boot.autoconfigure.transaction.jta

### org.springframework.boot.autoconfigure.validation

### org.springframework.boot.autoconfigure.web

#### org.springframework.boot.autoconfigure.web.client

#### org.springframework.boot.autoconfigure.web.embedded

### org.springframework.boot.autoconfigure.web.format

### org.springframework.boot.autoconfigure.web.reactive

#### org.springframework.boot.autoconfigure.web.reactive.error

#### org.springframework.boot.autoconfigure.web.reactive.function.client

### org.springframework.boot.autoconfigure.web.servlet

#### org.springframework.boot.autoconfigure.web.servlet.error

### org.springframework.boot.autoconfigure.webservices

#### org.springframework.boot.autoconfigure.webservices.client
### org.springframework.boot.autoconfigure.websocket
#### org.springframework.boot.autoconfigure.websocket.reactive

#### org.springframework.boot.autoconfigure.websocket.servlet

### org.springframework.boot.autoconfigureprocessor