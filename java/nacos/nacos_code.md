# nacos code



## 源代码v1.4.2

自己编译java doc

跟rocketmq一样，修改

<maven.javadoc.skip>false</maven.javadoc.skip>



命令行编译





file:///C:/Users/admin/Documents/GitHub/nacos/api/target/apidocs/index.html







nacos-address

nacos-all

nacos-api

nacos-auth

nacos-auth-plugin                                        

nacos-client

nacos-cmdb

nacos-common

nacos-config

nacos-consistency

nacos-console

nacos-core

nacos-discovery

nacos-distribution                                        

nacos-encryption-plugin

nacos-example

nacos-istio

nacos-naming

nacos-plugin

nacos-sys

nacos-test





## nacos-address





### com.alibaba.nacos.address



AddressServer



### com.alibaba.nacos.address.auth



AddressServerAuthManager



### com.alibaba.nacos.address.component



AddressServerGeneratorManager

AddressServerManager



### com.alibaba.nacos.address.configuration



AddressServerSpringConfiguration



### com.alibaba.nacos.address.constant



AddressServerConstants





### com.alibaba.nacos.address.controller



AddressServerClusterController

ServerListController





### com.alibaba.nacos.address.misc

Loggers





## nacos-all

## nacos-api



### com.alibaba.nacos.api



|                            |      |      |
| -------------------------- | ---- | ---- |
| 接口                       |      |      |
|                            |      |      |
| SystemPropertyKeyConst     |      |      |
|                            |      |      |
| 类                         |      |      |
|                            |      |      |
| NacosFactory               |      |      |
| PropertyKeyConst           |      |      |
| PropertyKeyConst.SystemEnv |      |      |



### com.alibaba.nacos.api.annotation



NacosInjected

NacosProperties



### com.alibaba.nacos.api.cmdb.pojo





|                      |      |      |
| -------------------- | ---- | ---- |
| 类                   |      |      |
|                      |      |      |
| Entity               |      |      |
| EntityEvent          |      |      |
| Label                |      |      |
|                      |      |      |
| 枚举                 |      |      |
|                      |      |      |
| EntityEventType      |      |      |
| PreservedEntityTypes |      |      |



### com.alibaba.nacos.api.cmdb.spi



CmdbService



### com.alibaba.nacos.api.common



类

Constants

ResponseCode





### com.alibaba.nacos.api.config



|                    |      |      |
| ------------------ | ---- | ---- |
| 接口               |      |      |
|                    |      |      |
| ConfigService      |      |      |
|                    |      |      |
| 类                 |      |      |
|                    |      |      |
| ConfigChangeEvent  |      |      |
| ConfigChangeItem   |      |      |
| ConfigFactory      |      |      |
|                    |      |      |
| 枚举               |      |      |
|                    |      |      |
| ConfigType         |      |      |
| PropertyChangeType |      |      |





### com.alibaba.nacos.api.config.annotation



|                              |      |      |
| ---------------------------- | ---- | ---- |
| 注释类型                     |      |      |
|                              |      |      |
| NacosConfigListener          |      |      |
| NacosConfigurationProperties |      |      |
| NacosIgnore                  |      |      |
| NacosProperty                |      |      |
| NacosValue                   |      |      |





### com.alibaba.nacos.api.config.convert



NacosConfigConverter



### com.alibaba.nacos.api.config.filter





|                      |      |      |
| -------------------- | ---- | ---- |
| 接口                 |      |      |
|                      |      |      |
| IConfigContext       |      |      |
| IConfigFilter        |      |      |
| IConfigFilterChain   |      |      |
| IConfigRequest       |      |      |
| IConfigResponse      |      |      |
| IFilterConfig        |      |      |
|                      |      |      |
| 类                   |      |      |
|                      |      |      |
| AbstractConfigFilter |      |      |



### com.alibaba.nacos.api.config.listener



|                        |      |      |
| ---------------------- | ---- | ---- |
| 接口                   |      |      |
|                        |      |      |
| ConfigChangeParser     |      |      |
| Listener               |      |      |
|                        |      |      |
| 类                     |      |      |
|                        |      |      |
| AbstractListener       |      |      |
| AbstractSharedListener |      |      |



### com.alibaba.nacos.api.exception



NacosException



### com.alibaba.nacos.api.exception.runtime



|                               |      |      |
| ----------------------------- | ---- | ---- |
| 异常错误                      |      |      |
|                               |      |      |
| NacosDeserializationException |      |      |
| NacosRuntimeException         |      |      |
| NacosSerializationException   |      |      |



### com.alibaba.nacos.api.naming



|                       |      |      |
| --------------------- | ---- | ---- |
| 接口                  |      |      |
|                       |      |      |
| NamingMaintainService |      |      |
| NamingService         |      |      |
|                       |      |      |
| 类                    |      |      |
|                       |      |      |
| CommonParams          |      |      |
| NamingFactory         |      |      |
| NamingMaintainFactory |      |      |
| NamingResponseCode    |      |      |
| PreservedMetadataKeys |      |      |





### com.alibaba.nacos.api.naming.listener

|                       |      |      |
| --------------------- | ---- | ---- |
| 接口                  |      |      |
|                       |      |      |
| Event                 |      |      |
| EventListener         |      |      |
|                       |      |      |
| 类                    |      |      |
|                       |      |      |
| AbstractEventListener |      |      |
| NamingEvent           |      |      |



### com.alibaba.nacos.api.naming.pojo



|             |      |      |
| ----------- | ---- | ---- |
| 类          |      |      |
|             |      |      |
| Cluster     |      |      |
| Instance    |      |      |
| ListView    |      |      |
| Service     |      |      |
| ServiceInfo |      |      |



### com.alibaba.nacos.api.naming.pojo.healthcheck



|                            |      |      |
| -------------------------- | ---- | ---- |
| 类                         |      |      |
|                            |      |      |
| AbstractHealthChecker      |      |      |
| AbstractHealthChecker.None |      |      |
| HealthCheckerFactory       |      |      |
|                            |      |      |
| 枚举                       |      |      |
|                            |      |      |
| HealthCheckType            |      |      |



### com.alibaba.nacos.api.naming.pojo.healthcheck.impl



类

Http

Mysql

Tcp

### com.alibaba.nacos.api.naming.utils

类

NamingUtils



### com.alibaba.nacos.api.selector



|                    |      |      |
| ------------------ | ---- | ---- |
| 类                 |      |      |
|                    |      |      |
| AbstractSelector   |      |      |
| ExpressionSelector |      |      |
| NoneSelector       |      |      |
|                    |      |      |
| 枚举               |      |      |
|                    |      |      |
| SelectorType       |      |      |



### com.alibaba.nacos.api.utils

StringUtils





## nacos-auth



### com.alibaba.nacos.auth



AuthManager



### com.alibaba.nacos.auth.annotation



Secured



### com.alibaba.nacos.auth.common



AuthConfigs

枚举

ActionTypes

AuthSystemTypes





### com.alibaba.nacos.auth.exception



AccessException





### com.alibaba.nacos.auth.model



Permission

Resource

User





### com.alibaba.nacos.auth.parser



接口

ResourceParser

类

DefaultResourceParser





### com.alibaba.nacos.auth.util

AuthHeaderUtil





## nacos-auth-plugin                                        

## nacos-client







## nacos-cmdb





### com.alibaba.nacos.cmdb

#### com.alibaba.nacos.cmdb.controllers

#### com.alibaba.nacos.cmdb.core

#### com.alibaba.nacos.cmdb.memory

#### com.alibaba.nacos.cmdb.service

#### com.alibaba.nacos.cmdb.utils





CmdbApp

CmdbExecutor

CmdbProvider

CmdbReader

CmdbWriter

Loggers

OperationController

SwitchAndOptions

UtilsAndCommons



## nacos-common







### com.alibaba.nacos.common

#### com.alibaba.nacos.common.codec

#### com.alibaba.nacos.common.constant

#### com.alibaba.nacos.common.executor

#### com.alibaba.nacos.common.http



| 接口                                     |      |      |
| ---------------------------------------- | ---- | ---- |
|                                          |      |      |
| Callback                                 |      |      |
| HttpClientFactory                        |      |      |
|                                          |      |      |
| 类                                       |      |      |
|                                          |      |      |
| AbstractApacheHttpClientFactory          |      |      |
| AbstractHttpClientFactory                |      |      |
| BaseHttpMethod.HttpDeleteWithEntity      |      |      |
| BaseHttpMethod.HttpGetWithEntity         |      |      |
| DefaultHttpClientFactory                 |      |      |
| HttpClientBeanHolder                     |      |      |
| HttpClientConfig                         |      |      |
| HttpClientConfig.HttpClientConfigBuilder |      |      |
| HttpRestResult                           |      |      |
| HttpUtils                                |      |      |
|                                          |      |      |
| 枚举                                     |      |      |
|                                          |      |      |
| BaseHttpMethod                           |      |      |



##### com.alibaba.nacos.common.http.client



|                               |      |      |
| ----------------------------- | ---- | ---- |
| 接口                          |      |      |
|                               |      |      |
| HttpClientRequestInterceptor  |      |      |
|                               |      |      |
| 类                            |      |      |
|                               |      |      |
| AbstractNacosRestTemplate     |      |      |
| InterceptingHttpClientRequest |      |      |
| NacosAsyncRestTemplate        |      |      |
| NacosRestTemplate             |      |      |
|                               |      |      |
|                               |      |      |
|                               |      |      |
|                               |      |      |
|                               |      |      |



###### com.alibaba.nacos.common.http.client.handler



|                           |      |      |
| ------------------------- | ---- | ---- |
| 接口                      |      |      |
|                           |      |      |
| ResponseHandler           |      |      |
|                           |      |      |
| 类                        |      |      |
|                           |      |      |
| AbstractResponseHandler   |      |      |
| BeanResponseHandler       |      |      |
| RestResultResponseHandler |      |      |
| StringResponseHandler     |      |      |



###### com.alibaba.nacos.common.http.client.request





|                               |      |      |
| ----------------------------- | ---- | ---- |
| 接口                          |      |      |
|                               |      |      |
| AsyncHttpClientRequest        |      |      |
| HttpClientRequest             |      |      |
|                               |      |      |
| 类                            |      |      |
|                               |      |      |
| DefaultAsyncHttpClientRequest |      |      |
| DefaultHttpClientRequest      |      |      |
| JdkHttpClientRequest          |      |      |



###### com.alibaba.nacos.common.http.client.response



接口

HttpClientResponse

类

DefaultClientHttpResponse

JdkHttpClientResponse



##### com.alibaba.nacos.common.http.handler



RequestHandler

ResponseHandler



##### com.alibaba.nacos.common.http.param



Header

MediaType

Query



#### com.alibaba.nacos.common.lifecycle



Closeable



#### com.alibaba.nacos.common.model





RequestHttpEntity

RestResult

RestResult.ResResultBuilder

RestResultUtils



##### com.alibaba.nacos.common.model.core



IResultCode



#### com.alibaba.nacos.common.notify



|                       |      |      |
| --------------------- | ---- | ---- |
| EventPublisher        |      |      |
|                       |      |      |
| 类                    |      |      |
|                       |      |      |
| DefaultPublisher      |      |      |
| DefaultSharePublisher |      |      |
| Event                 |      |      |
| NotifyCenter          |      |      |
| SlowEvent             |      |      |



##### com.alibaba.nacos.common.notify.listener



SmartSubscriber

Subscriber



#### com.alibaba.nacos.common.task



|                     |      |      |
| ------------------- | ---- | ---- |
| NacosTask           |      |      |
| NacosTaskProcessor  |      |      |
|                     |      |      |
| 类                  |      |      |
|                     |      |      |
| AbstractDelayTask   |      |      |
| AbstractExecuteTask |      |      |





##### com.alibaba.nacos.common.task.engine



|                                |      |      |
| ------------------------------ | ---- | ---- |
| NacosTaskExecuteEngine         |      |      |
|                                |      |      |
| 类                             |      |      |
|                                |      |      |
| AbstractNacosTaskExecuteEngine |      |      |
| NacosDelayTaskExecuteEngine    |      |      |
| NacosExecuteTaskExecuteEngine  |      |      |
| TaskExecuteWorker              |      |      |



#### com.alibaba.nacos.common.tls



|                                   |      |      |
| --------------------------------- | ---- | ---- |
| TlsFileWatcher.FileChangeListener |      |      |
|                                   |      |      |
| 类                                |      |      |
|                                   |      |      |
| SelfHostnameVerifier              |      |      |
| SelfTrustManager                  |      |      |
| TlsFileWatcher                    |      |      |
| TlsHelper                         |      |      |
| TlsSystemConfig                   |      |      |



#### com.alibaba.nacos.common.utils



|                   |      |      |
| ----------------- | ---- | ---- |
| 接口              |      |      |
|                   |      |      |
| BiConsumer        |      |      |
| BiFunction        |      |      |
| Observer          |      |      |
|                   |      |      |
| 类                |      |      |
|                   |      |      |
| ByteUtils         |      |      |
| ClassUtils        |      |      |
| CollectionUtils   |      |      |
| ConcurrentHashSet |      |      |
| ConvertUtils      |      |      |
| ExceptionUtil     |      |      |
| HttpMethod        |      |      |
| IoUtils           |      |      |
| IPUtil            |      |      |
| JacksonUtils      |      |      |
| LoggerUtils       |      |      |
| MapUtils          |      |      |
| MD5Utils          |      |      |
| NamespaceUtil     |      |      |
| Objects           |      |      |
| Observable        |      |      |
| Pair              |      |      |
| ResourceUtils     |      |      |
| StringUtils       |      |      |
| ThreadUtils       |      |      |
| UuidUtils         |      |      |
| VersionUtils      |      |      |





## nacos-config







### com.alibaba.nacos.config.server



Config







#### com.alibaba.nacos.config.server.aspect





CapacityManagementAspect

RequestLogAspect

枚举

CapacityManagementAspect.LimitType



#### com.alibaba.nacos.config.server.auth



| com.alibaba.nacos.config.server.auth |      |      |
| ------------------------------------ | ---- | ---- |
| PermissionPersistService             |      |      |
| RolePersistService                   |      |      |
| UserPersistService                   |      |      |
|                                      |      |      |
| 类                                   |      |      |
|                                      |      |      |
| ConfigResourceParser                 |      |      |
| EmbeddedPermissionPersistServiceImpl |      |      |
| EmbeddedRolePersistServiceImpl       |      |      |
| EmbeddedUserPersistServiceImpl       |      |      |
| ExternalPermissionPersistServiceImpl |      |      |
| ExternalRolePersistServiceImpl       |      |      |
| ExternalUserPersistServiceImpl       |      |      |
| PermissionInfo                       |      |      |
| RoleInfo                             |      |      |





#### com.alibaba.nacos.config.server.configuration



ConditionDistributedEmbedStorage

ConditionOnEmbeddedStorage

ConditionOnExternalStorage

ConditionStandaloneEmbedStorage

NacosConfigConfiguration



#### com.alibaba.nacos.config.server.constant



Constants

枚举

CounterMode



#### com.alibaba.nacos.config.server.controller



| com.alibaba.nacos.config.server.controller |      |      |
| ------------------------------------------ | ---- | ---- |
| CapacityController                         |      |      |
| CommunicationController                    |      |      |
| ConfigController                           |      |      |
| ConfigOpsController                        |      |      |
| ConfigServletInner                         |      |      |
| HealthController                           |      |      |
| HistoryController                          |      |      |
| ListenerController                         |      |      |



##### com.alibaba.nacos.config.server.controller.parameters



SameNamespaceCloneConfigBean



#### com.alibaba.nacos.config.server.enums



FileTypeEnum



#### com.alibaba.nacos.config.server.exception



GlobalExceptionHandler

异常错误

NacosConfigException

NJdbcException



#### com.alibaba.nacos.config.server.filter



CurcuitFilter

NacosWebFilter



#### com.alibaba.nacos.config.server.manager



TaskManagerMBean

类

TaskManager



#### com.alibaba.nacos.config.server.model



| com.alibaba.nacos.config.server.model |      |      |
| ------------------------------------- | ---- | ---- |
| AclInfo                               |      |      |
| CacheItem                             |      |      |
| ConfigAdvanceInfo                     |      |      |
| ConfigAllInfo                         |      |      |
| ConfigHistoryInfo                     |      |      |
| ConfigInfo                            |      |      |
| ConfigInfo4Beta                       |      |      |
| ConfigInfo4Tag                        |      |      |
| ConfigInfoAggr                        |      |      |
| ConfigInfoBase                        |      |      |
| ConfigInfoBaseEx                      |      |      |
| ConfigInfoBetaWrapper                 |      |      |
| ConfigInfoChanged                     |      |      |
| ConfigInfoEx                          |      |      |
| ConfigInfoTagWrapper                  |      |      |
| ConfigInfoWrapper                     |      |      |
| ConfigKey                             |      |      |
| ConfigMetadata                        |      |      |
| ConfigMetadata.ConfigExportItem       |      |      |
| GroupInfo                             |      |      |
| GroupkeyListenserStatus               |      |      |
| HistoryContext                        |      |      |
| Page                                  |      |      |
| RestPageResult                        |      |      |
| SampleResult                          |      |      |
| SubInfo                               |      |      |
| SubscriberStatus                      |      |      |
| TenantInfo                            |      |      |
| User                                  |      |      |
|                                       |      |      |
| 枚举                                  |      |      |
|                                       |      |      |
| AuthType                              |      |      |
| SameConfigPolicy                      |      |      |



##### com.alibaba.nacos.config.server.model.app



ApplicationInfo

ApplicationPublishRecord

GroupKey

MonitorInfo



##### com.alibaba.nacos.config.server.model.capacity



Capacity

GroupCapacity

TenantCapacity



##### com.alibaba.nacos.config.server.model.event



| com.alibaba.nacos.config.server.model.event |      |      |
| ------------------------------------------- | ---- | ---- |
| ConfigDataChangeEvent                       |      |      |
| ConfigDumpEvent                             |      |      |
| ConfigDumpEvent.ConfigDumpEventBuilder      |      |      |
| DerbyImportEvent                            |      |      |
| DerbyLoadEvent                              |      |      |
| LocalDataChangeEvent                        |      |      |
| RaftDbErrorEvent                            |      |      |
| RaftDbErrorRecoverEvent                     |      |      |



#### com.alibaba.nacos.config.server.monitor



| com.alibaba.nacos.config.server.monitor |      |      |
| --------------------------------------- | ---- | ---- |
| MemoryMonitor                           |      |      |
| MetricsMonitor                          |      |      |
| NotifyTaskQueueMonitorTask              |      |      |
| PrintGetConfigResponeTask               |      |      |
| PrintMemoryTask                         |      |      |
| ResponseMonitor                         |      |      |

#### com.alibaba.nacos.config.server.result

##### com.alibaba.nacos.config.server.result.code



ResultCodeEnum





#### com.alibaba.nacos.config.server.service



| com.alibaba.nacos.config.server.service |      |      |
| --------------------------------------- | ---- | ---- |
| AggrWhitelist                           |      |      |
| ClientIpWhiteList                       |      |      |
| ClientRecord                            |      |      |
| ClientTrackService                      |      |      |
| ConfigCacheService                      |      |      |
| ConfigChangePublisher                   |      |      |
| ConfigSubService                        |      |      |
| LongPollingService                      |      |      |
| SwitchService                           |      |      |



##### com.alibaba.nacos.config.server.service.capacity



CapacityService

GroupCapacityPersistService

TenantCapacityPersistService





##### com.alibaba.nacos.config.server.service.datasource



| com.alibaba.nacos.config.server.service.datasource |      |      |
| -------------------------------------------------- | ---- | ---- |
| DataSourceService                                  |      |      |
|                                                    |      |      |
| 类                                                 |      |      |
|                                                    |      |      |
| DataSourcePoolProperties                           |      |      |
| DynamicDataSource                                  |      |      |
| ExternalDataSourceProperties                       |      |      |
| ExternalDataSourceServiceImpl                      |      |      |
| LocalDataSourceServiceImpl                         |      |      |



##### com.alibaba.nacos.config.server.service.dump



DumpConfigHandler

DumpService

EmbeddedDumpService

ExternalDumpService





###### com.alibaba.nacos.config.server.service.dump.processor



| com.alibaba.nacos.config.server.service.dump.processor |      |      |
| ------------------------------------------------------ | ---- | ---- |
| DumpAllBetaProcessor                                   |      |      |
| DumpAllProcessor                                       |      |      |
| DumpAllTagProcessor                                    |      |      |
| DumpChangeProcessor                                    |      |      |
| DumpProcessor                                          |      |      |



##### com.alibaba.nacos.config.server.service.dump.task



| com.alibaba.nacos.config.server.service.dump.task |      |      |
| ------------------------------------------------- | ---- | ---- |
| DumpAllBetaTask                                   |      |      |
| DumpAllTagTask                                    |      |      |
| DumpAllTask                                       |      |      |
| DumpChangeTask                                    |      |      |
| DumpTask                                          |      |      |



##### com.alibaba.nacos.config.server.service.merge



MergeDatumService

MergeTaskProcessor





##### com.alibaba.nacos.config.server.service.notify



| com.alibaba.nacos.config.server.service.notify |      |      |
| ---------------------------------------------- | ---- | ---- |
| AsyncNotifyService                             |      |      |
| HttpClientManager                              |      |      |
| NotifyService                                  |      |      |
| NotifySingleService                            |      |      |
| NotifyTask                                     |      |      |
| NotifyTaskProcessor                            |      |      |





##### com.alibaba.nacos.config.server.service.repository



| com.alibaba.nacos.config.server.service.repository |      |      |
| -------------------------------------------------- | ---- | ---- |
| PaginationHelper                                   |      |      |
| PersistService                                     |      |      |
|                                                    |      |      |
| 类                                                 |      |      |
|                                                    |      |      |
| RowMapperManager                                   |      |      |
| RowMapperManager.ConfigAdvanceInfoRowMapper        |      |      |
| RowMapperManager.ConfigAllInfoRowMapper            |      |      |
| RowMapperManager.ConfigHistoryDetailRowMapper      |      |      |
| RowMapperManager.ConfigHistoryRowMapper            |      |      |
| RowMapperManager.ConfigInfo4BetaRowMapper          |      |      |
| RowMapperManager.ConfigInfo4TagRowMapper           |      |      |
| RowMapperManager.ConfigInfoAggrRowMapper           |      |      |
| RowMapperManager.ConfigInfoBaseRowMapper           |      |      |
| RowMapperManager.ConfigInfoBetaWrapperRowMapper    |      |      |
| RowMapperManager.ConfigInfoChangedRowMapper        |      |      |
| RowMapperManager.ConfigInfoRowMapper               |      |      |
| RowMapperManager.ConfigInfoTagWrapperRowMapper     |      |      |
| RowMapperManager.ConfigInfoWrapperRowMapper        |      |      |
| RowMapperManager.ConfigKeyRowMapper                |      |      |
| RowMapperManager.MapRowMapper                      |      |      |
| RowMapperManager.PermissionRowMapper               |      |      |
| RowMapperManager.RoleInfoRowMapper                 |      |      |
| RowMapperManager.TenantInfoRowMapper               |      |      |
| RowMapperManager.UserRowMapper                     |      |      |





##### com.alibaba.nacos.config.server.service.repository.embedded



| com.alibaba.nacos.config.server.service.repository.embedded |      |      |
| ----------------------------------------------------------- | ---- | ---- |
| BaseDatabaseOperate                                         |      |      |
| DatabaseOperate                                             |      |      |
|                                                             |      |      |
| 类                                                          |      |      |
|                                                             |      |      |
| DerbySnapshotOperation                                      |      |      |
| DistributedDatabaseOperateImpl                              |      |      |
| EmbeddedStoragePersistServiceImpl                           |      |      |
| StandaloneDatabaseOperateImpl                               |      |      |

EmbeddedStoragePersistServiceImpl derby对应的数据源

##### com.alibaba.nacos.config.server.service.repository.extrnal



ExternalStoragePersistServiceImpl



##### com.alibaba.nacos.config.server.service.sql



| com.alibaba.nacos.config.server.service.sql |      |      |
| ------------------------------------------- | ---- | ---- |
| EmbeddedStorageContextUtils                 |      |      |
| ModifyRequest                               |      |      |
| QueryType                                   |      |      |
| SelectRequest                               |      |      |
| SelectRequest.SelectRequestBuilder          |      |      |



##### com.alibaba.nacos.config.server.service.trace



ConfigTraceService



#### com.alibaba.nacos.config.server.utils



| com.alibaba.nacos.config.server.utils      |      |      |
| ------------------------------------------ | ---- | ---- |
| AccumulateStatCount                        |      |      |
| AppNameUtils                               |      |      |
| ConfigExecutor                             |      |      |
| ContentUtils                               |      |      |
| DerbyUtils                                 |      |      |
| DiskUtil                                   |      |      |
| GroupKey                                   |      |      |
| GroupKey2                                  |      |      |
| LogUtil                                    |      |      |
| MD5Util                                    |      |      |
| ParamUtils                                 |      |      |
| PropertyUtil                               |      |      |
| Protocol                                   |      |      |
| RegexParser                                |      |      |
| RequestUtil                                |      |      |
| ResponseUtil                               |      |      |
| SimpleCache                                |      |      |
| SimpleFlowData                             |      |      |
| SimpleIpFlowData                           |      |      |
| SimpleReadWriteLock                        |      |      |
| SingletonRepository                        |      |      |
| SingletonRepository.DataIdGroupIdCache     |      |      |
| StatConstants                              |      |      |
| SystemConfig                               |      |      |
| TimeoutUtils                               |      |      |
| TimeUtils                                  |      |      |
| TraceLogUtil                               |      |      |
| UrlAnalysisUtils                           |      |      |
| YamlParserUtil                             |      |      |
| YamlParserUtil.ConstructYamlConfigMetadata |      |      |
| YamlParserUtil.YamlParserConstructor       |      |      |
| ZipUtils                                   |      |      |
| ZipUtils.UnZipResult                       |      |      |
| ZipUtils.ZipItem                           |      |      |





## nacos-consistency



### com.alibaba.nacos.consistency





|                            |      |      |
| -------------------------- | ---- | ---- |
| CommandOperations          |      |      |
| Config                     |      |      |
| ConsistencyProtocol        |      |      |
| IdGenerator                |      |      |
| Serializer                 |      |      |
|                            |      |      |
| 类                         |      |      |
|                            |      |      |
| ProtocolMetaData           |      |      |
| ProtocolMetaData.MetaData  |      |      |
| ProtocolMetaData.ValueItem |      |      |
| ProtoMessageUtil           |      |      |
| RequestProcessor           |      |      |
| SerializeFactory           |      |      |
|                            |      |      |
| 枚举                       |      |      |
|                            |      |      |
| DataOperation              |      |      |







#### com.alibaba.nacos.consistency.ap



APProtocol

类

RequestProcessor4AP





#### com.alibaba.nacos.consistency.cp



CPProtocol

类

MetadataKey

RequestProcessor4CP





#### com.alibaba.nacos.consistency.entity



|                       |      |      |
| --------------------- | ---- | ---- |
| 接口                  |      |      |
|                       |      |      |
| GetRequestOrBuilder   |      |      |
| LogOrBuilder          |      |      |
| ReadRequestOrBuilder  |      |      |
| ResponseOrBuilder     |      |      |
| WriteRequestOrBuilder |      |      |
|                       |      |      |
| 类                    |      |      |
|                       |      |      |
| Consistency           |      |      |
| Data                  |      |      |
| GetRequest            |      |      |
| GetRequest.Builder    |      |      |
| Log                   |      |      |
| Log.Builder           |      |      |
| ReadRequest           |      |      |
| ReadRequest.Builder   |      |      |
| Response              |      |      |
| Response.Builder      |      |      |
| WriteRequest          |      |      |
| WriteRequest.Builder  |      |      |





#### com.alibaba.nacos.consistency.exception



ConsistencyException

NoSuchLogProcessorException



com.alibaba.nacos.consistency.serialize



HessianSerializer

JacksonSerializer





#### com.alibaba.nacos.consistency.snapshot



SnapshotOperation

类

LocalFileMeta

Reader

Writer



## nacos-console





### com.alibaba.nacos

#### com.alibaba.nacos.console.config

#### com.alibaba.nacos.console.controller

#### com.alibaba.nacos.console.exception

#### com.alibaba.nacos.console.filter

#### com.alibaba.nacos.console.model

##### com.alibaba.nacos.console.security.nacos

##### com.alibaba.nacos.console.security.nacos.roles

#### com.alibaba.nacos.console.security.nacos.users

#### com.alibaba.nacos.console.utils



ConsoleConfig

ConsoleExceptionHandler

CustomAuthenticationProvider

HealthController

JwtAuthenticationEntryPoint

JwtAuthenticationTokenFilter

JwtTokenManager

Nacos

NacosAuthConfig

NacosAuthManager

NacosRoleServiceImpl

NacosUser

NacosUserDetails

NacosUserDetailsServiceImpl

Namespace

NamespaceAllInfo

NamespaceController

PasswordEncoderUtil

PermissionController

RoleController

ServerStateController

UserController





## nacos-core

### com.alibaba.nacos.core.auth





| 类                                              | 说明                                                         |      |
| ----------------------------------------------- | ------------------------------------------------------------ | ---- |
| AuthConfig                                      | auth filter config.                                          |      |
| AuthFilter                                      | Unified filter to handle authentication and authorization.   |      |
| RequestMappingInfo                              | Request mapping information. to find the matched method by request |      |
| RequestMappingInfo.RequestMappingInfoComparator |                                                              |      |





#### com.alibaba.nacos.core.auth.condition





| 类                    |      | 说明                                                         |
| --------------------- | ---- | ------------------------------------------------------------ |
| ParamRequestCondition |      | request param info.                                          |
| PathRequestCondition  |      | request path info. method:RequestMapping.method() path: RequestMapping.value() or RequestMapping.value() |
|                       |      |                                                              |



### com.alibaba.nacos.core.cluster





| 接口                                        | 说明                                                         |      |
| ------------------------------------------- | ------------------------------------------------------------ | ---- |
| MemberLookup                                | Member node addressing mode.                                 |      |
|                                             |                                                              |      |
| 类                                          | 说明                                                         |      |
| AbstractMemberLookup                        | Addressable pattern base class.                              |      |
| Member                                      | Cluster member node.                                         |      |
| Member.MemberBuilder                        |                                                              |      |
| MemberChangeListener                        | Node change listeners.                                       |      |
| MemberMetaDataConstants                     | The necessary metadata information for the node.             |      |
| MembersChangeEvent                          | Publish this event when the node list changes，All interested in the node list change event can listen to this event. |      |
| MembersChangeEvent.MemberChangeEventBuilder |                                                              |      |
| MemberUtil                                  | Member node tool class.                                      |      |
| ServerMemberManager                         | Cluster node management in Nacos.                            |      |
| Task                                        | task.                                                        |      |
|                                             |                                                              |      |
| 枚举                                        | 说明                                                         |      |
| NodeState                                   | The life cycle state of a node plays an important role.      |      |

#### com.alibaba.nacos.core.cluster.lookup



| 类                        | 说明                                                         |
| ------------------------- | ------------------------------------------------------------ |
| AddressServerMemberLookup | Cluster member addressing mode for the address server.       |
| FileConfigMemberLookup    | Cluster.conf file managed cluster member node addressing pattern. |
| LookupFactory             | An addressing pattern factory, responsible for the creation of all addressing patterns. |
| StandaloneMemberLookup    | Member node addressing mode in stand-alone mode.             |
| LookupFactory.LookupType  |                                                              |



### com.alibaba.nacos.core.code



| 类                                   | 说明                                                         |      |
| ------------------------------------ | ------------------------------------------------------------ | ---- |
| ControllerMethodsCache               | Method cache.                                                |      |
| SpringApplicationRunListener         | SpringApplicationRunListener before EventPublishingRunListener execution. |      |
| StandaloneProfileApplicationListener | Standalone Profile ApplicationListener for ApplicationEnvironmentPreparedEvent. |      |



### com.alibaba.nacos.core.controller





| 类                     | 说明                                                 |      |
| ---------------------- | ---------------------------------------------------- | ---- |
| CoreOpsController      | Kernel modules operate and maintain HTTP interfaces. |      |
| NacosClusterController | Cluster communication interface.                     |      |



### com.alibaba.nacos.core.distributed



| 类                                                           | 说明                                                         |      |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ---- |
| AbstractConsistencyProtocol<T extends com.alibaba.nacos.consistency.Config,L extends com.alibaba.nacos.consistency.RequestProcessor> | Consistent protocol base class.                              |      |
| ConsistencyConfiguration                                     | consistency configuration.                                   |      |
| ProtocolExecutor                                             | ProtocolExecutor.                                            |      |
| ProtocolManager                                              | Conformance protocol management, responsible for managing the lifecycle of conformance protocols in Nacos. |      |





#### com.alibaba.nacos.core.distributed.distro



| 类                                    | 说明                  |
| :------------------------------------ | :-------------------- |
| [DistroConfig](DistroConfig.html)     | Distro configuration. |
| [DistroProtocol](DistroProtocol.html) | Distro protocol.      |





##### com.alibaba.nacos.core.distributed.distro.component





| 接口                    | 说明                        |      |
| ----------------------- | --------------------------- | ---- |
| DistroCallback          | Distro callback.            |      |
| DistroDataProcessor     | Distro data processor.      |      |
| DistroDataStorage       | Distro data storage.        |      |
| DistroFailedTaskHandler | Distro failed task handler. |      |
| DistroTransportAgent    | Distro transport agent.     |      |
| 类概要                  |                             |      |
| 类                      | 说明                        |      |
| DistroComponentHolder   | Distro component holder.    |      |





##### com.alibaba.nacos.core.distributed.distro.entity



| 类         | 说明         |      |
| ---------- | ------------ | ---- |
| DistroData | Distro data. |      |
| DistroKey  | Distro key.  |      |





##### com.alibaba.nacos.core.distributed.distro.exception



DistroException





##### com.alibaba.nacos.core.distributed.distro.task



DistroTaskEngineHolder



###### com.alibaba.nacos.core.distributed.distro.task.delay





| com.alibaba.nacos.core.distributed.distro.task.delay |                                   |      |
| ---------------------------------------------------- | --------------------------------- | ---- |
| DistroDelayTask                                      | Distro delay task.                |      |
| DistroDelayTaskExecuteEngine                         | Distro delay task execute engine. |      |
| DistroDelayTaskProcessor                             | Distro delay task processor.      |      |





###### com.alibaba.nacos.core.distributed.distro.task.execute



| com.alibaba.nacos.core.distributed.distro.task.execute |                                     |      |
| ------------------------------------------------------ | ----------------------------------- | ---- |
| AbstractDistroExecuteTask                              | Abstract distro execute task.       |      |
| DistroExecuteTaskExecuteEngine                         | Distro execute task execute engine. |      |
| DistroSyncChangeTask                                   | Distro sync change task.            |      |





###### com.alibaba.nacos.core.distributed.distro.task.load



DistroLoadDataTask



###### com.alibaba.nacos.core.distributed.distro.task.verify



DistroVerifyTask



#### com.alibaba.nacos.core.distributed.id



| com.alibaba.nacos.core.distributed.id |                                                              |
| ------------------------------------- | ------------------------------------------------------------ |
| IdGeneratorManager                    | Id generator manager.                                        |
| SnowFlowerIdGenerator                 | copy from http://www.cluozy.com/home/hexo/2018/08/11/shariding-JDBC-snowflake/. |



#### com.alibaba.nacos.core.distributed.raft





| 类                         | 说明                                                         |
| -------------------------- | ------------------------------------------------------------ |
| JRaftMaintainService       | JRaft operations interface.                                  |
| JRaftProtocol              | A concrete implementation of CP protocol: JRaft.             |
| JRaftServer                | JRaft server instance, away from Spring IOC management.      |
| JRaftServer.RaftGroupTuple |                                                              |
| NacosClosure               | implement jraft closure.                                     |
| NacosClosure.NacosStatus   |                                                              |
| RaftConfig                 | raft config.                                                 |
| RaftErrorEvent             | The RAFT protocol runs an exception event.                   |
| RaftEvent                  | Changes to metadata information during the raft protocol run. |
| RaftEvent.RaftEventBuilder |                                                              |
| RaftSysConstants           | jraft system constants.                                      |



##### com.alibaba.nacos.core.distributed.raft.exception



| 异常错误                    | 说明                                                         |      |
| --------------------------- | ------------------------------------------------------------ | ---- |
| DuplicateRaftGroupException | Duplicate groupId when creating Raft Group throws this exception. |      |
| JRaftException              | Abnormal JRaft.                                              |      |
| NoLeaderException           | This exception is thrown if the current Raft Group Cluster does not elect a leader. |      |
| NoSuchRaftGroupException    | no this raft group exception.                                |      |



##### com.alibaba.nacos.core.distributed.raft.processor



| 类                         | 说明                                      |      |
| -------------------------- | ----------------------------------------- | ---- |
| AbstractProcessor          | abstract rpc processor.                   |      |
| NacosGetRequestProcessor   | 已过时。                                  |      |
| NacosLogProcessor          | 已过时。                                  |      |
| NacosReadRequestProcessor  | nacos request processor for ReadRequest.  |      |
| NacosWriteRequestProcessor | nacos request processor for WriteRequest. |      |





##### com.alibaba.nacos.core.distributed.raft.utils





| 接口                | 说明                                                    |      |
| ------------------- | ------------------------------------------------------- | ---- |
| FailoverClosure     | Failure callback based on Closure.                      |      |
| RetryRunner         | Retry function.                                         |      |
| 类概要              |                                                         |      |
| 类                  | 说明                                                    |      |
| FailoverClosureImpl | Closure with internal retry mechanism.                  |      |
| JRaftConstants      | constant.                                               |      |
| JRaftLogOperation   | JRaft for additional information on logging operations. |      |
| JRaftUtils          | JRaft utils.                                            |      |
| RaftExecutor        | raft executor.                                          |      |
| RaftOptionsBuilder  | build RaftOptions.                                      |      |
| 枚举概要            |                                                         |      |
| 枚举                | 说明                                                    |      |
| JRaftOps            | jraft maintain service.                                 |      |



### com.alibaba.nacos.core.exception



| 枚举                | 说明                                |      |
| ------------------- | ----------------------------------- | ---- |
| ErrorCode           | Core module code starts with 40001. |      |
| 异常错误概要        |                                     |      |
| 异常错误            | 说明                                |      |
| KvStorageException  | RocksDB Exception.                  |      |
| SnakflowerException | SnakflowerException.                |      |

### com.alibaba.nacos.core.listener



| 接口                        | 说明                                              |      |
| --------------------------- | ------------------------------------------------- | ---- |
| NacosApplicationListener    | Nacos Application Listener, execute init process. |      |
| 类概要                      |                                                   |      |
| 类                          | 说明                                              |      |
| LoggingApplicationListener  | For init logging configuration.                   |      |
| StartingApplicationListener | init environment config.                          |      |





### com.alibaba.nacos.core.monitor



| 类                 | 说明                          |      |
| ------------------ | ----------------------------- | ---- |
| MetricsMonitor     | The Metrics center.           |      |
| NacosMeterRegistry | Metrics unified usage center. |      |



### com.alibaba.nacos.core.storage



StorageFactory





#### com.alibaba.nacos.core.storage.kv





| com.alibaba.nacos.core.storage.kv |                                                              |      |
| --------------------------------- | ------------------------------------------------------------ | ---- |
| 接口                              | 说明                                                         |      |
| KvStorage                         | Universal KV storage interface.                              |      |
| 类概要                            |                                                              |      |
| 类                                | 说明                                                         |      |
| FileKvStorage                     | Kv storage based on file system. // TODO 写文件的方式需要优化 |      |
| MemoryKvStorage                   | Realization of KV storage based on memory.                   |      |
| 枚举概要                          |                                                              |      |
| 枚举                              | 说明                                                         |      |
| KvStorage.KvType                  |                                                              |      |

### com.alibaba.nacos.core.utils





| com.alibaba.nacos.core.utils      | 说明                                                         |      |
| --------------------------------- | ------------------------------------------------------------ | ---- |
| ReuseHttpRequest                  | ReuseHttpRequest.                                            |      |
| 类概要                            |                                                              |      |
| 类                                | 说明                                                         |      |
| ClassUtils                        | class operation utils.                                       |      |
| Commons                           | Constants.                                                   |      |
| GenericType<T>                    | Encapsulates third party tools for generics acquisition.     |      |
| GlobalExecutor                    | core module global executor.                                 |      |
| Loggers                           | Loggers for core.                                            |      |
| OverrideParameterRequestWrapper   | A request wrapper to override the parameters.                |      |
| ReuseHttpServletRequest           | httprequest wrapper.                                         |      |
| ReuseUploadFileHttpServletRequest | httprequest wrapper.                                         |      |
| TimerContext                      | Simple task time calculation，Currently only the task time statistics task that supports synchronizing code blocks is supported. |      |
| WebUtils                          | web utils.                                                   |      |



## nacos-discovery

## nacos-distribution                                        

## nacos-encryption-plugin

## nacos-example

## nacos-istio







### com.alibaba.nacos.istio

### com.alibaba.nacos.istio.mcp

### com.alibaba.nacos.istio.misc

### com.alibaba.nacos.istio.model

#### com.alibaba.nacos.istio.model.mcp







IstioApp





CollectionTypes

McpServerIntercepter

NacosMcpServer

NacosMcpService



IstioConfig

Loggers





GatewayOrBuilder

PortOrBuilder

Server.TLSOptionsOrBuilder

ServerOrBuilder

类

Gateway

Gateway.Builder

GatewayOuterClass

Port

Port.Builder

Server

Server.Builder

Server.TLSOptions

Server.TLSOptions.Builder

枚举

Server.TLSOptions.TLSmode

Server.TLSOptions.TLSProtocol

#### com.alibaba.nacos.istio.model.mcp

| com.alibaba.nacos.istio.model.mcp                            |      |      |
| ------------------------------------------------------------ | ---- | ---- |
|                                                              |      |      |
| 接口                                                         |      |      |
|                                                              |      |      |
| IncrementalMeshConfigRequestOrBuilder                        |      |      |
| IncrementalMeshConfigResponseOrBuilder                       |      |      |
| MeshConfigRequestOrBuilder                                   |      |      |
| MeshConfigResponseOrBuilder                                  |      |      |
| MetadataOrBuilder                                            |      |      |
| RequestResourcesOrBuilder                                    |      |      |
| ResourceOrBuilder                                            |      |      |
| ResourcesOrBuilder                                           |      |      |
| SinkNodeOrBuilder                                            |      |      |
|                                                              |      |      |
| 类                                                           |      |      |
|                                                              |      |      |
| AggregatedMeshConfigServiceGrpc                              |      |      |
| AggregatedMeshConfigServiceGrpc.AggregatedMeshConfigServiceBlockingStub |      |      |
| AggregatedMeshConfigServiceGrpc.AggregatedMeshConfigServiceFutureStub |      |      |
| AggregatedMeshConfigServiceGrpc.AggregatedMeshConfigServiceImplBase |      |      |
| AggregatedMeshConfigServiceGrpc.AggregatedMeshConfigServiceStub |      |      |
| IncrementalMeshConfigRequest                                 |      |      |
| IncrementalMeshConfigRequest.Builder                         |      |      |
| IncrementalMeshConfigResponse                                |      |      |
| IncrementalMeshConfigResponse.Builder                        |      |      |
| Mcp                                                          |      |      |
| MeshConfigRequest                                            |      |      |
| MeshConfigRequest.Builder                                    |      |      |
| MeshConfigResponse                                           |      |      |
| MeshConfigResponse.Builder                                   |      |      |
| Metadata                                                     |      |      |
| Metadata.Builder                                             |      |      |
| MetadataOuterClass                                           |      |      |
| RequestResources                                             |      |      |
| RequestResources.Builder                                     |      |      |
| Resource                                                     |      |      |
| Resource.Builder                                             |      |      |
| ResourceOuterClass                                           |      |      |
| Resources                                                    |      |      |
| Resources.Builder                                            |      |      |
| ResourceSinkGrpc                                             |      |      |
| ResourceSinkGrpc.ResourceSinkBlockingStub                    |      |      |
| ResourceSinkGrpc.ResourceSinkFutureStub                      |      |      |
| ResourceSinkGrpc.ResourceSinkImplBase                        |      |      |
| ResourceSinkGrpc.ResourceSinkStub                            |      |      |
| ResourceSourceGrpc                                           |      |      |
| ResourceSourceGrpc.ResourceSourceBlockingStub                |      |      |
| ResourceSourceGrpc.ResourceSourceFutureStub                  |      |      |
| ResourceSourceGrpc.ResourceSourceImplBase                    |      |      |
| ResourceSourceGrpc.ResourceSourceStub                        |      |      |
| SinkNode                                                     |      |      |
| SinkNode.Builder                                             |      |      |







#### com.alibaba.nacos.istio.model.naming

| com.alibaba.nacos.istio.model.naming |      |      |
| ------------------------------------ | ---- | ---- |
| ServiceEntry.EndpointOrBuilder       |      |      |
| ServiceEntryOrBuilder                |      |      |
|                                      |      |      |
| 类                                   |      |      |
|                                      |      |      |
| ServiceEntry                         |      |      |
| ServiceEntry.Builder                 |      |      |
| ServiceEntry.Endpoint                |      |      |
| ServiceEntry.Endpoint.Builder        |      |      |
| ServiceEntryOuterClass               |      |      |
|                                      |      |      |
| 枚举                                 |      |      |
|                                      |      |      |
| ServiceEntry.Location                |      |      |
| ServiceEntry.Resolution              |      |      |



## nacos-naming







### com.alibaba.nacos.naming



NamingApp



### com.alibaba.nacos.naming.cluster





类

ServerListManager

ServerStatusManager

枚举

ServerStatus



#### com.alibaba.nacos.naming.cluster.transport





接口

Serializer

类

JacksonSerializer



### com.alibaba.nacos.naming.consistency



|                                          |      |      |
| ---------------------------------------- | ---- | ---- |
| 接口                                     |      |      |
|                                          |      |      |
| ConsistencyService                       |      |      |
| RecordListener                           |      |      |
|                                          |      |      |
| 类                                       |      |      |
|                                          |      |      |
| Datum                                    |      |      |
| DelegateConsistencyServiceImpl           |      |      |
| KeyBuilder                               |      |      |
| ValueChangeEvent                         |      |      |
| ValueChangeEvent.ValueChangeEventBuilder |      |      |



#### com.alibaba.nacos.naming.consistency.ephemeral



EphemeralConsistencyService





#### com.alibaba.nacos.naming.consistency.ephemeral.distro



|                              |      |      |
| ---------------------------- | ---- | ---- |
| 类                           |      |      |
|                              |      |      |
| DataStore                    |      |      |
| DistroConsistencyServiceImpl |      |      |
| DistroHttpData               |      |      |
| DistroHttpRegistry           |      |      |



#### com.alibaba.nacos.naming.consistency.ephemeral.distro.combined



|                                        |      |      |
| -------------------------------------- | ---- | ---- |
| 类                                     |      |      |
|                                        |      |      |
| DistroHttpCombinedKey                  |      |      |
| DistroHttpCombinedKeyDelayTask         |      |      |
| DistroHttpCombinedKeyExecuteTask       |      |      |
| DistroHttpCombinedKeyTaskFailedHandler |      |      |
| DistroHttpDelayTaskProcessor           |      |      |



#### com.alibaba.nacos.naming.consistency.ephemeral.distro.component





DistroDataStorageImpl

DistroHttpAgent



#### com.alibaba.nacos.naming.consistency.persistent



|                                          |      |      |
| ---------------------------------------- | ---- | ---- |
| 接口                                     |      |      |
|                                          |      |      |
| PersistentConsistencyService             |      |      |
|                                          |      |      |
| 类                                       |      |      |
|                                          |      |      |
| ClusterVersionJudgement                  |      |      |
| PersistentConsistencyServiceDelegateImpl |      |      |
| PersistentNotifier                       |      |      |



#### com.alibaba.nacos.naming.consistency.persistent.impl



|                                      |      |      |
| ------------------------------------ | ---- | ---- |
| 类                                   |      |      |
|                                      |      |      |
| BasePersistentServiceProcessor       |      |      |
| BatchReadResponse                    |      |      |
| BatchWriteRequest                    |      |      |
| NamingKvStorage                      |      |      |
| NamingSnapshotOperation              |      |      |
| PersistentServiceProcessor           |      |      |
| StandalonePersistentServiceProcessor |      |      |





#### com.alibaba.nacos.naming.consistency.persistent.raft



|                            |      |      |
| -------------------------- | ---- | ---- |
| 类                         |      |      |
|                            |      |      |
| BaseRaftEvent              |      |      |
| LeaderElectFinishedEvent   |      |      |
| MakeLeaderEvent            |      |      |
| RaftConsistencyServiceImpl |      |      |
| RaftCore                   |      |      |
| RaftListener               |      |      |
| RaftPeer                   |      |      |
| RaftPeerSet                |      |      |
| RaftProxy                  |      |      |
| RaftStore                  |      |      |
|                            |      |      |
| 枚举                       |      |      |
|                            |      |      |
| RaftPeer.State             |      |      |



### com.alibaba.nacos.naming.controllers



| com.alibaba.nacos.naming.controllers |      |      |
| ------------------------------------ | ---- | ---- |
| 类                                   |      |      |
|                                      |      |      |
| ApiController                        |      |      |
| CatalogController                    |      |      |
| ClusterController                    |      |      |
| DistroController                     |      |      |
| HealthController                     |      |      |
| InstanceController                   |      |      |
| OperatorController                   |      |      |
| RaftController                       |      |      |
| ServiceController                    |      |      |





### com.alibaba.nacos.naming.core



|    com.alibaba.nacos.naming.core           |      |      |
| ------------------------------ | ---- | ---- |
| 类                             |      |      |
|                                |      |      |
| Cluster                        |      |      |
| DistroMapper                   |      |      |
| Instance                       |      |      |
| Instances                      |      |      |
| Service                        |      |      |
| ServiceManager                 |      |      |
| ServiceManager.ServiceChecksum |      |      |
| SubscribeManager               |      |      |



### com.alibaba.nacos.naming.exception



ResponseExceptionHandler



### com.alibaba.nacos.naming.healthcheck



|                              |      |      |
| ---------------------------- | ---- | ---- |
| 接口                         |      |      |
|                              |      |      |
| HealthCheckProcessor         |      |      |
|                              |      |      |
| 类                           |      |      |
|                              |      |      |
| ClientBeatCheckTask          |      |      |
| ClientBeatProcessor          |      |      |
| HealthCheckCommon            |      |      |
| HealthCheckProcessorDelegate |      |      |
| HealthCheckReactor           |      |      |
| HealthCheckStatus            |      |      |
| HealthCheckTask              |      |      |
| HttpHealthCheckProcessor     |      |      |
| MysqlHealthCheckProcessor    |      |      |
| NoneHealthCheckProcessor     |      |      |
| RsInfo                       |      |      |
| TcpSuperSenseProcessor       |      |      |



#### com.alibaba.nacos.naming.healthcheck.events



InstanceHeartbeatTimeoutEvent



#### com.alibaba.nacos.naming.healthcheck.extend



HealthCheckExtendProvider



### com.alibaba.nacos.naming.misc



|                                |      |      |
| ------------------------------ | ---- | ---- |
| 接口                           |      |      |
|                                |      |      |
| SwitchDomain.HealthParams      |      |      |
| Synchronizer                   |      |      |
|                                |      |      |
| 类                             |      |      |
|                                |      |      |
| GlobalConfig                   |      |      |
| GlobalExecutor                 |      |      |
| HttpClient                     |      |      |
| HttpClientManager              |      |      |
| Loggers                        |      |      |
| Message                        |      |      |
| NamingProxy                    |      |      |
| NamingProxy.Request            |      |      |
| NetUtils                       |      |      |
| ServerStatusSynchronizer       |      |      |
| ServiceStatusSynchronizer      |      |      |
| SwitchDomain                   |      |      |
| SwitchDomain.HttpHealthParams  |      |      |
| SwitchDomain.MysqlHealthParams |      |      |
| SwitchDomain.TcpHealthParams   |      |      |
| SwitchEntry                    |      |      |
| SwitchManager                  |      |      |
| UtilsAndCommons                |      |      |



### com.alibaba.nacos.naming.monitor



MetricsMonitor

PerformanceLoggerThread



### com.alibaba.nacos.naming.pojo



|                          |      |      |
| ------------------------ | ---- | ---- |
| 接口                     |      |      |
|                          |      |      |
| Record                   |      |      |
|                          |      |      |
| 类                       |      |      |
|                          |      |      |
| ClusterInfo              |      |      |
| ClusterStateView         |      |      |
| InstanceOperationContext |      |      |
| InstanceOperationInfo    |      |      |
| IpAddressInfo            |      |      |
| ServiceDetailInfo        |      |      |
| ServiceDetailView        |      |      |
| ServiceView              |      |      |
| Subscriber               |      |      |
| Subscribers              |      |      |



### com.alibaba.nacos.naming.push



|                                  |      |      |
| -------------------------------- | ---- | ---- |
| DataSource                       |      |      |
|                                  |      |      |
| 类                               |      |      |
|                                  |      |      |
| ClientInfo                       |      |      |
| ClientInfo.ClientTypeDescription |      |      |
| PushService                      |      |      |
| PushService.Receiver             |      |      |
| PushService.Receiver.AckEntry    |      |      |
| PushService.Receiver.AckPacket   |      |      |
| PushService.Retransmitter        |      |      |
| ServiceChangeEvent               |      |      |
|                                  |      |      |
| 枚举                             |      |      |
|                                  |      |      |
| ClientInfo.ClientType            |      |      |



### com.alibaba.nacos.naming.selector





|                                     |      |      |
| ----------------------------------- | ---- | ---- |
| Selector                            |      |      |
|                                     |      |      |
| 类                                  |      |      |
|                                     |      |      |
| LabelSelector                       |      |      |
| LabelSelector.ExpressionInterpreter |      |      |
| NoneSelector                        |      |      |



### com.alibaba.nacos.naming.utils



Constants



### com.alibaba.nacos.naming.web



| com.alibaba.nacos.naming.web |      |      |
| ---------------------------- | ---- | ---- |
| 类                           |      |      |
|                              |      |      |
| DistroFilter                 |      |      |
| NamingConfig                 |      |      |
| NamingResourceParser         |      |      |
| TrafficReviseFilter          |      |      |
|                              |      |      |
| 注释类型                     |      |      |
|                              |      |      |
| CanDistro                    |      |      |







## nacos-plugin

## nacos-sys

## nacos-test