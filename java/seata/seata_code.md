# seata



## 分包解析

 https://javadoc.dev/online/api/io.seata/seata-all/1.3.0/index.html





程序包

## io.seata.common



Constants

XID



### io.seata.common.exception





|  io.seata.common.exception      |      |      |
| -------------------------- | ---- | ---- |
| FrameworkErrorCode         |      |      |
|                            |      |      |
| 异常错误                   |      |      |
|                            |      |      |
| DataAccessException        |      |      |
| EurekaRegistryException    |      |      |
| FrameworkException         |      |      |
| NotSupportYetException     |      |      |
| ShouldNeverHappenException |      |      |
| StoreException             |      |      |



### io.seata.common.executor





Callback

Initialize



### io.seata.common.holder



ObjectHolder



### io.seata.common.loader



|                                  |      |      |
| -------------------------------- | ---- | ---- |
| EnhancedServiceLoader            |      |      |
|                                  |      |      |
| 枚举                             |      |      |
|                                  |      |      |
| Scope                            |      |      |
|                                  |      |      |
| 异常错误                         |      |      |
|                                  |      |      |
| EnhancedServiceNotFoundException |      |      |
|                                  |      |      |
| 注释类型                         |      |      |
|                                  |      |      |
| LoadLevel                        |      |      |





### io.seata.common.thread



NamedThreadFactory

PositiveAtomicCounter

RejectedPolicies



### io.seata.common.util



|                   |      |      |
| ----------------- | ---- | ---- |
| BlobUtils         |      |      |
| CollectionUtils   |      |      |
| CompressUtil      |      |      |
| DurationUtil      |      |      |
| IdWorker          |      |      |
| IOUtil            |      |      |
| LambdaUtils       |      |      |
| NetUtil           |      |      |
| NumberUtils       |      |      |
| ReflectionUtil    |      |      |
| StringFormatUtils |      |      |
| StringUtils       |      |      |



## io.seata.compressor
### io.seata.compressor.bzip2





BZip2Compressor

BZip2Util



### io.seata.compressor.gzip



GzipCompressor

GzipUtil





### io.seata.compressor.lz4



Lz4Compressor

Lz4Util



### io.seata.compressor.sevenz



SevenZCompressor

SevenZUtil



### io.seata.compressor.zip



ZipCompressor

ZipUtil



## io.seata.config



|                              |      |      |
| ---------------------------- | ---- | ---- |
| ConfigChangeListener         |      |      |
| Configuration                |      |      |
| ConfigurationChangeListener  |      |      |
| ConfigurationProvider        |      |      |
| ExtConfigurationProvider     |      |      |
|                              |      |      |
| 类                           |      |      |
|                              |      |      |
| AbstractConfiguration        |      |      |
| ConfigFuture                 |      |      |
| ConfigurationCache           |      |      |
| ConfigurationChangeEvent     |      |      |
| ConfigurationFactory         |      |      |
| ConfigurationKeys            |      |      |
| FileConfiguration            |      |      |
|                              |      |      |
| 枚举                         |      |      |
|                              |      |      |
| ConfigFuture.ConfigOperation |      |      |
| ConfigType                   |      |      |
| ConfigurationChangeType      |      |      |



### io.seata.config.apollo



ApolloConfiguration

ApolloConfigurationProvider



### io.seata.config.consul



ConsulConfiguration

ConsulConfiguration.ConsulListener

ConsulConfigurationProvider



### io.seata.config.custom



CustomConfigurationProvider



### io.seata.config.etcd3



EtcdConfiguration

EtcdConfigurationProvider



### io.seata.config.nacos



NacosConfiguration

NacosConfiguration.NacosListener

NacosConfigurationProvider



### io.seata.config.springcloud



|                                           |      |      |
| ----------------------------------------- | ---- | ---- |
| SpringApplicationContextProvider          |      |      |
| SpringApplicationContextProviderRegistrar |      |      |
| SpringCloudConfiguration                  |      |      |
| SpringCloudConfigurationProvider          |      |      |
|                                           |      |      |
| 注释类型                                  |      |      |
|                                           |      |      |
| EnableSeataSpringConfig                   |      |      |



### io.seata.config.zk



|                                   |      |      |
| --------------------------------- | ---- | ---- |
| DefaultZkSerializer               |      |      |
| ZookeeperConfiguration            |      |      |
| ZookeeperConfiguration.ZKListener |      |      |
| ZookeeperConfigurationProvider    |      |      |



## io.seata.core
### io.seata.core.compressor





| io.seata.core.compressor         |      |      |
| -------------------------------- | ---- | ---- |
| Compressor                       |      |      |
|                                  |      |      |
| 类                               |      |      |
|                                  |      |      |
| CompressorFactory                |      |      |
| CompressorFactory.NoneCompressor |      |      |
|                                  |      |      |
| 枚举                             |      |      |
|                                  |      |      |
| CompressorType                   |      |      |



### io.seata.core.constants



| io.seata.core.constants |      |      |
| ----------------------- | ---- | ---- |
| ClientTableColumnsName  |      |      |
| ConfigurationKeys       |      |      |
| DefaultValues           |      |      |
| DubboConstants          |      |      |
| ServerTableColumnsName  |      |      |
|                         |      |      |
| 枚举                    |      |      |
|                         |      |      |
| DBType                  |      |      |



### io.seata.core.context



|                            |      |      |
| -------------------------- | ---- | ---- |
| ContextCore                |      |      |
|                            |      |      |
| 类                         |      |      |
|                            |      |      |
| ContextCoreLoader          |      |      |
| FastThreadLocalContextCore |      |      |
| RootContext                |      |      |
| ThreadLocalContextCo       |      |      |



### io.seata.core.event



| io.seata.core.event    |      |      |
| ---------------------- | ---- | ---- |
| Event                  |      |      |
| EventBus               |      |      |
|                        |      |      |
| 类                     |      |      |
|                        |      |      |
| GlobalTransactionEvent |      |      |
| GuavaEventBus          |      |      |



### io.seata.core.exception



|                                           |      |      |
| ----------------------------------------- | ---- | ---- |
| AbstractExceptionHandler.Callback         |      |      |
|                                           |      |      |
| 类                                        |      |      |
|                                           |      |      |
| AbstractExceptionHandler                  |      |      |
| AbstractExceptionHandler.AbstractCallback |      |      |
|                                           |      |      |
| 枚举                                      |      |      |
|                                           |      |      |
| TransactionExceptionCode                  |      |      |
|                                           |      |      |
| 异常错误                                  |      |      |
|                                           |      |      |
| BranchTransactionException                |      |      |
| GlobalTransactionException                |      |      |
| RmTransactionException                    |      |      |
| TmTransactionException                    |      |      |
| TransactionException                      |      |      |



### io.seata.core.lock



|                |      |      |
| -------------- | ---- | ---- |
| Locker         |      |      |
|                |      |      |
| 类             |      |      |
|                |      |      |
| AbstractLocker |      |      |
| LocalDBLocker  |      |      |
| RowLock        |      |      |
|                |      |      |
| 枚举           |      |      |
|                |      |      |
| LockMode       |      |      |





### io.seata.core.logger



StackTraceLogger



### io.seata.core.model



| io.seata.core.model     |      |      |
| ----------------------- | ---- | ---- |
| Resource                |      |      |
| ResourceManager         |      |      |
| ResourceManagerInbound  |      |      |
| ResourceManagerOutbound |      |      |
| TransactionManager      |      |      |
|                         |      |      |
| 类                      |      |      |
|                         |      |      |
| Result                  |      |      |
|                         |      |      |
| 枚举                    |      |      |
|                         |      |      |
| BranchStatus            |      |      |
| BranchType              |      |      |
| GlobalStatus            |      |      |



### io.seata.core.protocol



| io.seata.core.protocol       |      |      |
| ---------------------------- | ---- | ---- |
| MergeMessage                 |      |      |
| MessageTypeAware             |      |      |
|                              |      |      |
| 类                           |      |      |
|                              |      |      |
| AbstractIdentifyRequest      |      |      |
| AbstractIdentifyResponse     |      |      |
| AbstractMessage              |      |      |
| AbstractResultMessage        |      |      |
| HeartbeatMessage             |      |      |
| MergedWarpMessage            |      |      |
| MergeResultMessage           |      |      |
| MessageFuture                |      |      |
| MessageType                  |      |      |
| ProtocolConstants            |      |      |
| RegisterRMRequest            |      |      |
| RegisterRMResponse           |      |      |
| RegisterTMRequest            |      |      |
| RegisterTMResponse           |      |      |
| RpcMessage                   |      |      |
| Version                      |      |      |
|                              |      |      |
| 枚举                         |      |      |
|                              |      |      |
| ResultCode                   |      |      |
|                              |      |      |
| 异常错误                     |      |      |
|                              |      |      |
| IncompatibleVersionException |      |      |



### io.seata.core.protocol.transaction



| io.seata.core.protocol.transaction |      |      |
| ---------------------------------- | ---- | ---- |
| RMInboundHandler                   |      |      |
| TCInboundHandler                   |      |      |
|                                    |      |      |
| 类                                 |      |      |
|                                    |      |      |
| AbstractBranchEndRequest           |      |      |
| AbstractBranchEndResponse          |      |      |
| AbstractGlobalEndRequest           |      |      |
| AbstractGlobalEndResponse          |      |      |
| AbstractTransactionRequest         |      |      |
| AbstractTransactionRequestToRM     |      |      |
| AbstractTransactionRequestToTC     |      |      |
| AbstractTransactionResponse        |      |      |
| BranchCommitRequest                |      |      |
| BranchCommitResponse               |      |      |
| BranchRegisterRequest              |      |      |
| BranchRegisterResponse             |      |      |
| BranchReportRequest                |      |      |
| BranchReportResponse               |      |      |
| BranchRollbackRequest              |      |      |
| BranchRollbackResponse             |      |      |
| GlobalBeginRequest                 |      |      |
| GlobalBeginResponse                |      |      |
| GlobalCommitRequest                |      |      |
| GlobalCommitResponse               |      |      |
| GlobalLockQueryRequest             |      |      |
| GlobalLockQueryResponse            |      |      |
| GlobalReportRequest                |      |      |
| GlobalReportResponse               |      |      |
| GlobalRollbackRequest              |      |      |
| GlobalRollbackResponse             |      |      |
| GlobalStatusRequest                |      |      |
| GlobalStatusResponse               |      |      |
| UndoLogDeleteRequest               |      |      |



### io.seata.core.rpc



| io.seata.core.rpc                |      |      |
| -------------------------------- | ---- | ---- |
| ClientMessageListener            |      |      |
| ClientMessageSender              |      |      |
| Disposable                       |      |      |
| RegisterCheckAuthHandler         |      |      |
| RemotingBootstrap                |      |      |
| RemotingClient                   |      |      |
| RemotingServer                   |      |      |
| RemotingService                  |      |      |
| ServerMessageListener            |      |      |
| ServerMessageSender              |      |      |
| TransactionMessageHandler        |      |      |
|                                  |      |      |
| 类                               |      |      |
|                                  |      |      |
| DefaultServerMessageListenerImpl |      |      |
| RpcContext                       |      |      |
| ShutdownHook                     |      |      |
|                                  |      |      |
| 枚举                             |      |      |
|                                  |      |      |
| ClientType                       |      |      |
| TransportProtocolType            |      |      |
| TransportServerType              |      |      |



### io.seata.core.rpc.netty



| io.seata.core.rpc.netty        |      |      |
| ------------------------------ | ---- | ---- |
| ChannelAuthHealthChecker       |      |      |
| ChannelEventListener           |      |      |
| RegisterMsgListener            |      |      |
| RpcEventLoopGroup              |      |      |
|                                |      |      |
| 类                             |      |      |
|                                |      |      |
| AbstractNettyRemoting          |      |      |
| AbstractNettyRemotingClient    |      |      |
| AbstractNettyRemotingServer    |      |      |
| ChannelManager                 |      |      |
| ChannelUtil                    |      |      |
| NettyBaseConfig                |      |      |
| NettyClientBootstrap           |      |      |
| NettyClientConfig              |      |      |
| NettyPoolableFactory           |      |      |
| NettyPoolKey                   |      |      |
| NettyRemotingServer            |      |      |
| NettyServerBootstrap           |      |      |
| NettyServerConfig              |      |      |
| RmNettyRemotingClient          |      |      |
| TmNettyRemotingClient          |      |      |
|                                |      |      |
| 枚举                           |      |      |
|                                |      |      |
| NettyBaseConfig.WorkThreadMode |      |      |
| NettyPoolKey.TransactionRole   |      |      |



### io.seata.core.rpc.netty.v1



HeadMapSerializer

ProtocolV1Decoder

ProtocolV1Encoder



### io.seata.core.rpc.processor



RemotingProcessor

类

Pair



#### io.seata.core.rpc.processor.client



| io.seata.core.rpc.processor.client |      |      |
| ---------------------------------- | ---- | ---- |
| ClientHeartbeatProcessor           |      |      |
| ClientOnResponseProcessor          |      |      |
| RmBranchCommitProcessor            |      |      |
| RmBranchRollbackProcessor          |      |      |
| RmUndoLogProcessor                 |      |      |



#### io.seata.core.rpc.processor.server



| io.seata.core.rpc.processor.server |      |      |
| ---------------------------------- | ---- | ---- |
| BatchLogHandler                    |      |      |
| RegRmProcessor                     |      |      |
| RegTmProcessor                     |      |      |
| ServerHeartbeatProcessor           |      |      |
| ServerOnRequestProcessor           |      |      |
| ServerOnResponseProcessor          |      |      |



### io.seata.core.serializer



| io.seata.core.serializer |      |      |
| ------------------------ | ---- | ---- |
| Serializer               |      |      |
|                          |      |      |
| 类                       |      |      |
|                          |      |      |
| SerializerClassRegistry  |      |      |
| SerializerFactory        |      |      |
|                          |      |      |
| 枚举                     |      |      |
|                          |      |      |
| SerializerType           |      |      |



### io.seata.core.store



| io.seata.core.store |      |      |
| ------------------- | ---- | ---- |
| LockStore           |      |      |
| LogStore            |      |      |
|                     |      |      |
| 类                  |      |      |
|                     |      |      |
| BranchTransactionDO |      |      |
| GlobalTransactionDO |      |      |
| LockDO              |      |      |
|                     |      |      |
| 枚举                |      |      |
|                     |      |      |
| StoreMode           |      |      |



### io.seata.core.store.db



DataSourceProvider

类

AbstractDataSourceProvider



#### io.seata.core.store.db.sql.lock



| io.seata.core.store.db.sql.lock |      |      |
| ------------------------------- | ---- | ---- |
| LockStoreSql                    |      |      |
|                                 |      |      |
| 类                              |      |      |
|                                 |      |      |
| AbstractLockStoreSql            |      |      |
| H2LockStoreSql                  |      |      |
| LockStoreSqlFactory             |      |      |
| MysqlLockStoreSql               |      |      |
| OceanbaseLockStoreSql           |      |      |
| OracleLockStoreSql              |      |      |
| PostgresqlLockStoreSql          |      |      |



#### io.seata.core.store.db.sql.log



|                        |      |      |
| ---------------------- | ---- | ---- |
| LogStoreSqls           |      |      |
|                        |      |      |
| 类                     |      |      |
|                        |      |      |
| AbstractLogStoreSqls   |      |      |
| H2LogStoreSqls         |      |      |
| LogStoreSqlsFactory    |      |      |
| MysqlLogStoreSqls      |      |      |
| OceanbaseLogStoreSqls  |      |      |
| OracleLogStoreSqls     |      |      |
| PostgresqlLogStoreSqls |      |      |



## io.seata.discovery
### io.seata.discovery.loadbalance



| io.seata.discovery.loadbalance |      |      |
| ------------------------------ | ---- | ---- |
| LoadBalance                    |      |      |
|                                |      |      |
| 类                             |      |      |
|                                |      |      |
| AbstractLoadBalance            |      |      |
| LoadBalanceFactory             |      |      |
| RandomLoadBalance              |      |      |
| RoundRobinLoadBalance          |      |      |



### io.seata.discovery.registry



| io.seata.discovery.registry |      |      |
| --------------------------- | ---- | ---- |
| RegistryProvider            |      |      |
| RegistryService             |      |      |
|                             |      |      |
| 类                          |      |      |
|                             |      |      |
| FileRegistryServiceImpl     |      |      |
| RegistryFactory             |      |      |
|                             |      |      |
| 枚举                        |      |      |
|                             |      |      |
| RegistryType                |      |      |



#### io.seata.discovery.registry.consul



ConsulListener

类

ConsulRegistryProvider

ConsulRegistryServiceImpl



#### io.seata.discovery.registry.custom



CustomRegistryProvider



#### io.seata.discovery.registry.etcd3



EtcdRegistryProvider

EtcdRegistryServiceImpl



#### io.seata.discovery.registry.eureka



CustomEurekaInstanceConfig

EurekaRegistryProvider

EurekaRegistryServiceImpl



#### io.seata.discovery.registry.nacos



NacosRegistryProvider

NacosRegistryServiceImpl



#### io.seata.discovery.registry.redis



RedisListener

类

RedisRegistryProvider

RedisRegistryServiceImpl



#### io.seata.discovery.registry.sofa



SofaRegistryProvider

SofaRegistryServiceImpl





#### io.seata.discovery.registry.zk



ZookeeperRegisterServiceImpl

ZookeeperRegistryProvider





## io.seata.integration
### io.seata.integration.dubbo

### io.seata.integration.dubbo.alibaba

### io.seata.integration.grpc.interceptor

### io.seata.integration.grpc.interceptor.client

### io.seata.integration.grpc.interceptor.server

### io.seata.integration.http

### io.seata.integration.motan

### io.seata.integration.sofa.rpc

## io.seata.rm





| io.seata.rm             |      |      |
| ----------------------- | ---- | ---- |
| AbstractResourceManager |      |      |
| AbstractRMHandler       |      |      |
| BaseDataSourceResource  |      |      |
| DefaultResourceManager  |      |      |
| DefaultRMHandler        |      |      |
| GlobalLockTemplate      |      |      |
| RMClient                |      |      |
| RMHandlerAT             |      |      |
| RMHandlerXA             |      |      |



### io.seata.rm.datasource



| io.seata.rm.datasource                 |      |      |
| -------------------------------------- | ---- | ---- |
| AbstractConnectionProxy                |      |      |
| AbstractDataSourceCacheResourceManager |      |      |
| AbstractDataSourceProxy                |      |      |
| AbstractPreparedStatementProxy         |      |      |
| AbstractStatementProxy                 |      |      |
| AsyncWorker                            |      |      |
| ColumnUtils                            |      |      |
| ConnectionContext                      |      |      |
| ConnectionProxy                        |      |      |
| ConnectionProxy.LockRetryPolicy        |      |      |
| DataCompareUtils                       |      |      |
| DataSourceManager                      |      |      |
| DataSourceProxy                        |      |      |
| PreparedStatementProxy                 |      |      |
| SqlGenerateUtils                       |      |      |
| StatementProxy                         |      |      |
|                                        |      |      |
| 枚举                                   |      |      |
|                                        |      |      |
| ColumnUtils.Escape                     |      |      |



#### io.seata.rm.datasource.exec



| io.seata.rm.datasource.exec |      |      |
| --------------------------- | ---- | ---- |
| Executor                    |      |      |
| InsertExecutor              |      |      |
| StatementCallback           |      |      |
|                             |      |      |
| 类                          |      |      |
|                             |      |      |
| AbstractDMLBaseExecutor     |      |      |
| BaseInsertExecutor          |      |      |
| BaseTransactionalExecutor   |      |      |
| DeleteExecutor              |      |      |
| ExecuteTemplate             |      |      |
| LockRetryController         |      |      |
| MultiDeleteExecutor         |      |      |
| MultiExecutor               |      |      |
| MultiUpdateExecutor         |      |      |
| PlainExecutor               |      |      |
| SelectForUpdateExecutor     |      |      |
| UpdateExecutor              |      |      |
|                             |      |      |
| 异常错误                    |      |      |
|                             |      |      |
| LockConflictException       |      |      |
| LockWaitTimeoutException    |      |      |



#### io.seata.rm.datasource.exec.mysql

MySQLInsertExecutor



io.seata.rm.datasource.exec.oracle



OracleInsertExecutor



#### io.seata.rm.datasource.exec.postgresql





PostgresqlInsertExecutor





### io.seata.rm.datasource.sql



SQLVisitorFactory



#### io.seata.rm.datasource.sql.serial



SerialArray



#### io.seata.rm.datasource.sql.struct



|                                |      |      |
| ------------------------------ | ---- | ---- |
| TableMetaCache                 |      |      |
|                                |      |      |
| 类                             |      |      |
|                                |      |      |
| ColumnMeta                     |      |      |
| Field                          |      |      |
| IndexMeta                      |      |      |
| Row                            |      |      |
| TableMeta                      |      |      |
| TableMetaCacheFactory          |      |      |
| TableRecords                   |      |      |
| TableRecords.EmptyTableRecords |      |      |
|                                |      |      |
| 枚举                           |      |      |
|                                |      |      |
| IndexType                      |      |      |
| KeyType                        |      |      |



#### io.seata.rm.datasource.sql.struct.cache



AbstractTableMetaCache

MysqlTableMetaCache

OracleTableMetaCache

PostgresqlTableMetaCache



### io.seata.rm.datasource.undo



| io.seata.rm.datasource.undo  |      |      |
| ---------------------------- | ---- | ---- |
| KeywordChecker               |      |      |
| UndoExecutorHolder           |      |      |
| UndoLogManager               |      |      |
| UndoLogParser                |      |      |
|                              |      |      |
| 类                           |      |      |
|                              |      |      |
| AbstractUndoExecutor         |      |      |
| AbstractUndoLogManager       |      |      |
| BranchUndoLog                |      |      |
| KeywordCheckerFactory        |      |      |
| SQLUndoLog                   |      |      |
| UndoExecutorFactory          |      |      |
| UndoExecutorHolderFactory    |      |      |
| UndoLogConstants             |      |      |
| UndoLogManagerFactory        |      |      |
| UndoLogParserFactory         |      |      |
|                              |      |      |
| 枚举                         |      |      |
|                              |      |      |
| AbstractUndoLogManager.State |      |      |



#### io.seata.rm.datasource.undo.mysql



| io.seata.rm.datasource.undo.mysql |      |      |
| --------------------------------- | ---- | ---- |
| MySQLUndoDeleteExecutor           |      |      |
| MySQLUndoExecutorHolder           |      |      |
| MySQLUndoInsertExecutor           |      |      |
| MySQLUndoLogManager               |      |      |
| MySQLUndoUpdateExecutor           |      |      |



#### io.seata.rm.datasource.undo.mysql.keyword



MySQLKeywordChecker



#### io.seata.rm.datasource.undo.oracle



OracleUndoDeleteExecutor

OracleUndoExecutorHolder

OracleUndoInsertExecutor

OracleUndoLogManager

OracleUndoUpdateExecutor



##### io.seata.rm.datasource.undo.oracle.keyword



OracleKeywordChecker



#### io.seata.rm.datasource.undo.parser



| io.seata.rm.datasource.undo.parser        |      |      |
| ----------------------------------------- | ---- | ---- |
| FastjsonUndoLogParser                     |      |      |
| JacksonUndoLogParser                      |      |      |
| KryoSerializer                            |      |      |
| KryoSerializerFactory                     |      |      |
| KryoUndoLogParser                         |      |      |
| ProtostuffUndoLogParser                   |      |      |
| ProtostuffUndoLogParser.DateDelegate      |      |      |
| ProtostuffUndoLogParser.SqlDateDelegate   |      |      |
| ProtostuffUndoLogParser.TimeDelegate      |      |      |
| ProtostuffUndoLogParser.TimestampDelegate |      |      |



#### io.seata.rm.datasource.undo.postgresql



| io.seata.rm.datasource.undo.postgresql |      |      |
| -------------------------------------- | ---- | ---- |
| PostgresqlUndoDeleteExecutor           |      |      |
| PostgresqlUndoExecutorHolder           |      |      |
| PostgresqlUndoInsertExecutor           |      |      |
| PostgresqlUndoLogManager               |      |      |
| PostgresqlUndoUpdateExecutor           |      |      |



##### io.seata.rm.datasource.undo.postgresql.keyword



PostgresqlKeywordChecker



### io.seata.rm.datasource.util



JdbcUtils

XAUtils



### io.seata.rm.datasource.xa



| io.seata.rm.datasource.xa |      |      |
| ------------------------- | ---- | ---- |
| Holdable                  |      |      |
| Holder                    |      |      |
| XAXid                     |      |      |
|                           |      |      |
| 类                        |      |      |
|                           |      |      |
| AbstractConnectionProxyXA |      |      |
| AbstractDataSourceProxyXA |      |      |
| ConnectionProxyXA         |      |      |
| DataSourceProxyXA         |      |      |
| DataSourceProxyXANative   |      |      |
| ExecuteTemplateXA         |      |      |
| PreparedStatementProxyXA  |      |      |
| ResourceManagerXA         |      |      |
| StatementProxyXA          |      |      |
| XABranchXid               |      |      |
| XAXidBuilder              |      |      |



### io.seata.rm.tcc



RMHandlerTCC

TCCResource

TCCResourceManager

TwoPhaseResult



#### io.seata.rm.tcc.api



| io.seata.rm.tcc.api            |      |      |
| ------------------------------ | ---- | ---- |
| BusinessActionContext          |      |      |
| BusinessActivityContext        |      |      |
|                                |      |      |
| 注释类型                       |      |      |
|                                |      |      |
| BusinessActionContextParameter |      |      |
| LocalTCC                       |      |      |
| TwoPhaseBusinessAction         |      |      |



#### io.seata.rm.tcc.interceptor



ActionContextFilter

类

ActionContextUtil

ActionInterceptorHandler



#### io.seata.rm.tcc.remoting

RemotingParser

类

Protocols

RemotingDesc



##### io.seata.rm.tcc.remoting.parser



| io.seata.rm.tcc.remoting.parser |      |      |
| ------------------------------- | ---- | ---- |
| AbstractedRemotingParser        |      |      |
| DefaultRemotingParser           |      |      |
| DubboRemotingParser             |      |      |
| DubboUtil                       |      |      |
| HSFRemotingParser               |      |      |
| LocalTCCRemotingParser          |      |      |
| SofaRpcRemotingParser           |      |      |



## io.seata.saga
### io.seata.saga.engine



AsyncCallback

StateMachineConfig

StateMachineEngine



#### io.seata.saga.engine.config



DbStateMachineConfig



#### io.seata.saga.engine.evaluation



Evaluator

EvaluatorFactory

类

EvaluatorFactoryManager



##### io.seata.saga.engine.evaluation.exception



ExceptionMatchEvaluator

ExceptionMatchEvaluatorFactory



##### io.seata.saga.engine.evaluation.expression



ExpressionEvaluator

ExpressionEvaluatorFactory



#### io.seata.saga.engine.exception



EngineExecutionException

ForwardInvalidException



#### io.seata.saga.engine.expression



Expression

ExpressionFactory

类

ExpressionFactoryManager



##### io.seata.saga.engine.expression.seq



SequenceExpression

SequenceExpressionFactory



##### io.seata.saga.engine.expression.spel



SpringELExpression

SpringELExpressionFactory



#### io.seata.saga.engine.impl



DefaultStateMachineConfig

ProcessCtrlStateMachineEngine



#### io.seata.saga.engine.invoker



ServiceInvoker

类

ServiceInvokerManager



##### io.seata.saga.engine.invoker.impl



SpringBeanServiceInvoker



#### io.seata.saga.engine.pcext



|                            |      |      |
| -------------------------- | ---- | ---- |
| InterceptableStateHandler  |      |      |
| InterceptableStateRouter   |      |      |
| StateHandler               |      |      |
| StateHandlerInterceptor    |      |      |
| StateRouter                |      |      |
| StateRouterInterceptor     |      |      |
|                            |      |      |
| 类                         |      |      |
|                            |      |      |
| StateInstruction           |      |      |
| StateMachineProcessHandler |      |      |
| StateMachineProcessRouter  |      |      |



##### io.seata.saga.engine.pcext.handlers



|                                 |      |      |
| ------------------------------- | ---- | ---- |
| ChoiceStateHandler              |      |      |
| CompensationTriggerStateHandler |      |      |
| FailEndStateHandler             |      |      |
| ScriptTaskStateHandler          |      |      |
| ServiceTaskStateHandler         |      |      |
| SubStateMachineHandler          |      |      |
| SucceedEndStateHandler          |      |      |



##### io.seata.saga.engine.pcext.interceptors



EndStateRouterInterceptor

ScriptTaskHandlerInterceptor

ServiceTaskHandlerInterceptor



##### io.seata.saga.engine.pcext.routers



EndStateRouter

TaskStateRouter



#### io.seata.saga.engine.pcext.utils



CompensationHolder

EngineUtils

ParameterUtils



#### io.seata.saga.engine.repo



StateLogRepository

StateMachineRepository



##### io.seata.saga.engine.repo.impl



StateLogRepositoryImpl

StateMachineRepositoryImpl



#### io.seata.saga.engine.sequence



SeqGenerator

类

SpringJvmUUIDSeqGenerator



#### io.seata.saga.engine.serializer



Serializer



##### io.seata.saga.engine.serializer.impl



ExceptionSerializer

ParamsSerializer



#### io.seata.saga.engine.store



StateLangStore

StateLogStore



##### io.seata.saga.engine.store.db





|                                 |      |      |
| ------------------------------- | ---- | ---- |
| AbstractStore.ObjectToStatement |      |      |
| AbstractStore.ResultSetToObject |      |      |
|                                 |      |      |
| 类                              |      |      |
|                                 |      |      |
| AbstractStore                   |      |      |
| DbAndReportTcStateLogStore      |      |      |
| DbStateLangStore                |      |      |
| StateLangStoreSqls              |      |      |
| StateLogStoreSqls               |      |      |



##### io.seata.saga.engine.store.utils



BeanUtils



#### io.seata.saga.engine.strategy



StatusDecisionStrategy



##### io.seata.saga.engine.strategy.impl



DefaultStatusDecisionStrategy



#### io.seata.saga.engine.utils



ExceptionUtils

ProcessContextBuilder

枚举

ExceptionUtils.NetExceptionType



### io.seata.saga.proctrl



|                            |      |      |
| -------------------------- | ---- | ---- |
| HierarchicalProcessContext |      |      |
| Instruction                |      |      |
| ProcessContext             |      |      |
| ProcessController          |      |      |
| ProcessRouter              |      |      |
|                            |      |      |
| 枚举                       |      |      |
|                            |      |      |
| ProcessType                |      |      |



#### io.seata.saga.proctrl.eventing



EventBus

EventConsumer

EventPublisher



##### io.seata.saga.proctrl.eventing.impl





|                           |      |      |
| ------------------------- | ---- | ---- |
| AbstractEventBus          |      |      |
| AsyncEventBus             |      |      |
| DirectEventBus            |      |      |
| ProcessCtrlEventConsumer  |      |      |
| ProcessCtrlEventPublisher |      |      |



##### io.seata.saga.proctrl.handler



|                      |      |      |
| -------------------- | ---- | ---- |
| ProcessHandler       |      |      |
| RouterHandler        |      |      |
|                      |      |      |
| 类                   |      |      |
|                      |      |      |
| DefaultRouterHandler |      |      |



#### io.seata.saga.proctrl.impl



ProcessContextImpl

ProcessControllerImpl



#### io.seata.saga.proctrl.process



BusinessProcessor



##### io.seata.saga.proctrl.process.impl



CustomizeBusinessProcessor



### io.seata.saga.rm



|                          |      |      |
| ------------------------ | ---- | ---- |
| RMHandlerSaga            |      |      |
| SagaResource             |      |      |
| SagaResourceManager      |      |      |
| StateMachineEngineHolder |      |      |


## io.seata.saga.statelang
### io.seata.saga.statelang.domain



|                                |      |      |
| ------------------------------ | ---- | ---- |
| ChoiceState                    |      |      |
| ChoiceState.Choice             |      |      |
| CompensateSubStateMachineState |      |      |
| CompensationTriggerState       |      |      |
| EndState                       |      |      |
| FailEndState                   |      |      |
| ScriptTaskState                |      |      |
| ServiceTaskState               |      |      |
| State                          |      |      |
| StateInstance                  |      |      |
| StateMachine                   |      |      |
| StateMachineInstance           |      |      |
| SubStateMachine                |      |      |
| SucceedEndState                |      |      |
| TaskState                      |      |      |
| TaskState.ExceptionMatch       |      |      |
| TaskState.Retry                |      |      |
| TaskState.StatusMatch          |      |      |
|                                |      |      |
| 类                             |      |      |
|                                |      |      |
| DomainConstants                |      |      |
|                                |      |      |
| 枚举                           |      |      |
|                                |      |      |
| ExecutionStatus                |      |      |
| RecoverStrategy                |      |      |
| StateMachine.Status            |      |      |



#### io.seata.saga.statelang.domain.impl



|                                      |      |      |
| ------------------------------------ | ---- | ---- |
| AbstractTaskState                    |      |      |
| AbstractTaskState.ExceptionMatchImpl |      |      |
| AbstractTaskState.RetryImpl          |      |      |
| BaseState                            |      |      |
| ChoiceStateImpl                      |      |      |
| ChoiceStateImpl.ChoiceImpl           |      |      |
| CompensateSubStateMachineStateImpl   |      |      |
| CompensationTriggerStateImpl         |      |      |
| FailEndStateImpl                     |      |      |
| ScriptTaskStateImpl                  |      |      |
| ServiceTaskStateImpl                 |      |      |
| StateInstanceImpl                    |      |      |
| StateMachineImpl                     |      |      |
| StateMachineInstanceImpl             |      |      |
| SubStateMachineImpl                  |      |      |
| SucceedEndStateImpl                  |      |      |



### io.seata.saga.statelang.parser



|                           |      |      |
| ------------------------- | ---- | ---- |
| JsonParser                |      |      |
| StateMachineParser        |      |      |
| StateParser               |      |      |
|                           |      |      |
| 类                        |      |      |
|                           |      |      |
| JsonParserFactory         |      |      |
| StateMachineParserFactory |      |      |
| StateParserFactory        |      |      |



#### io.seata.saga.statelang.parser.impl



|                                      |      |      |
| ------------------------------------ | ---- | ---- |
| AbstractTaskStateParser              |      |      |
| BaseStatePaser                       |      |      |
| ChoiceStateParser                    |      |      |
| CompensateSubStateMachineStateParser |      |      |
| CompensationTriggerStateParser       |      |      |
| FailEndStateParser                   |      |      |
| FastjsonParser                       |      |      |
| JacksonJsonParser                    |      |      |
| ScriptTaskStateParser                |      |      |
| ServiceTaskStateParser               |      |      |
| StateMachineParserImpl               |      |      |
| SubStateMachineParser                |      |      |
| SucceedEndStateParser                |      |      |



#### io.seata.saga.statelang.parser.utils



DesignerJsonTransformer

IOUtils



### io.seata.saga.tm



SagaTransactionalTemplate

类

DefaultSagaTransactionalTemplate



## io.seata.serializer
### io.seata.serializer.hessian



HessianSerializer

HessianSerializerFactory



### io.seata.serializer.kryo



KryoInnerSerializer

KryoSerializer

KryoSerializerFactory



### io.seata.serializer.protobuf



ProtobufHelper

ProtobufInnerSerializer

ProtobufSerializer



#### io.seata.serializer.protobuf.convertor



|                                  |      |      |
| -------------------------------- | ---- | ---- |
| PbConvertor                      |      |      |
|                                  |      |      |
| 类                               |      |      |
|                                  |      |      |
| BranchCommitRequestConvertor     |      |      |
| BranchCommitResponseConvertor    |      |      |
| BranchRegisterRequestConvertor   |      |      |
| BranchRegisterResponseConvertor  |      |      |
| BranchReportRequestConvertor     |      |      |
| BranchReportResponseConvertor    |      |      |
| BranchRollbackRequestConvertor   |      |      |
| BranchRollbackResponseConvertor  |      |      |
| GlobalBeginRequestConvertor      |      |      |
| GlobalBeginResponseConvertor     |      |      |
| GlobalCommitRequestConvertor     |      |      |
| GlobalCommitResponseConvertor    |      |      |
| GlobalLockQueryRequestConvertor  |      |      |
| GlobalLockQueryResponseConvertor |      |      |
| GlobalReportRequestConvertor     |      |      |
| GlobalReportResponseConvertor    |      |      |
| GlobalRollbackRequestConvertor   |      |      |
| GlobalRollbackResponseConvertor  |      |      |
| GlobalStatusRequestConvertor     |      |      |
| GlobalStatusResponseConvertor    |      |      |
| HeartbeatMessageConvertor        |      |      |
| MergedWarpMessageConvertor       |      |      |
| MergeResultMessageConvertor      |      |      |
| RegisterRMRequestConvertor       |      |      |
| RegisterRMResponseConvertor      |      |      |
| RegisterTMRequestConvertor       |      |      |
| RegisterTMResponseConvertor      |      |      |
| UndoLogDeleteRequestConvertor    |      |      |



#### io.seata.serializer.protobuf.generated



|                                           |      |      |
| ----------------------------------------- | ---- | ---- |
| 接口                                      |      |      |
|                                           |      |      |
| AbstractBranchEndRequestProtoOrBuilder    |      |      |
| AbstractBranchEndResponseProtoOrBuilder   |      |      |
| AbstractGlobalEndRequestProtoOrBuilder    |      |      |
| AbstractGlobalEndResponseProtoOrBuilder   |      |      |
| AbstractIdentifyRequestProtoOrBuilder     |      |      |
| AbstractIdentifyResponseProtoOrBuilder    |      |      |
| AbstractMessageProtoOrBuilder             |      |      |
| AbstractResultMessageProtoOrBuilder       |      |      |
| AbstractTransactionRequestProtoOrBuilder  |      |      |
| AbstractTransactionResponseProtoOrBuilder |      |      |
| BranchCommitRequestProtoOrBuilder         |      |      |
| BranchCommitResponseProtoOrBuilder        |      |      |
| BranchRegisterRequestProtoOrBuilder       |      |      |
| BranchRegisterResponseProtoOrBuilder      |      |      |
| BranchReportRequestProtoOrBuilder         |      |      |
| BranchReportResponseProtoOrBuilder        |      |      |
| BranchRollbackRequestProtoOrBuilder       |      |      |
| BranchRollbackResponseProtoOrBuilder      |      |      |
| GlobalBeginRequestProtoOrBuilder          |      |      |
| GlobalBeginResponseProtoOrBuilder         |      |      |
| GlobalCommitRequestProtoOrBuilder         |      |      |
| GlobalCommitResponseProtoOrBuilder        |      |      |
| GlobalLockQueryRequestProtoOrBuilder      |      |      |
| GlobalLockQueryResponseProtoOrBuilder     |      |      |
| GlobalReportRequestProtoOrBuilder         |      |      |
| GlobalReportResponseProtoOrBuilder        |      |      |
| GlobalRollbackRequestProtoOrBuilder       |      |      |
| GlobalRollbackResponseProtoOrBuilder      |      |      |
| GlobalStatusRequestProtoOrBuilder         |      |      |
| GlobalStatusResponseProtoOrBuilder        |      |      |
| HeartbeatMessageProtoOrBuilder            |      |      |
| MergedResultMessageProtoOrBuilder         |      |      |
| MergedWarpMessageProtoOrBuilder           |      |      |
| RegisterRMRequestProtoOrBuilder           |      |      |
| RegisterRMResponseProtoOrBuilder          |      |      |
| RegisterTMRequestProtoOrBuilder           |      |      |
| RegisterTMResponseProtoOrBuilder          |      |      |
| UndoLogDeleteRequestProtoOrBuilder        |      |      |
|                                           |      |      |
| 类                                        |      |      |
|                                           |      |      |
| AbstractBranchEndRequest                  |      |      |
| AbstractBranchEndRequestProto             |      |      |
| AbstractBranchEndRequestProto.Builder     |      |      |
| AbstractBranchEndResponse                 |      |      |
| AbstractBranchEndResponseProto            |      |      |
| AbstractBranchEndResponseProto.Builder    |      |      |
| AbstractGlobalEndRequest                  |      |      |
| AbstractGlobalEndRequestProto             |      |      |
| AbstractGlobalEndRequestProto.Builder     |      |      |
| AbstractGlobalEndResponse                 |      |      |
| AbstractGlobalEndResponseProto            |      |      |
| AbstractGlobalEndResponseProto.Builder    |      |      |
| AbstractIdentifyRequest                   |      |      |
| AbstractIdentifyRequestProto              |      |      |
| AbstractIdentifyRequestProto.Builder      |      |      |
| AbstractIdentifyResponse                  |      |      |
| AbstractIdentifyResponseProto             |      |      |
| AbstractIdentifyResponseProto.Builder     |      |      |
| AbstractMessage                           |      |      |
| AbstractMessageProto                      |      |      |
| AbstractMessageProto.Builder              |      |      |
| AbstractResultMessage                     |      |      |
| AbstractResultMessageProto                |      |      |
| AbstractResultMessageProto.Builder        |      |      |
| AbstractTransactionRequest                |      |      |
| AbstractTransactionRequestProto           |      |      |
| AbstractTransactionRequestProto.Builder   |      |      |
| AbstractTransactionResponse               |      |      |
| AbstractTransactionResponseProto          |      |      |
| AbstractTransactionResponseProto.Builder  |      |      |
| BranchCommitRequest                       |      |      |
| BranchCommitRequestProto                  |      |      |
| BranchCommitRequestProto.Builder          |      |      |
| BranchCommitResponse                      |      |      |
| BranchCommitResponseProto                 |      |      |
| BranchCommitResponseProto.Builder         |      |      |
| BranchRegisterRequest                     |      |      |
| BranchRegisterRequestProto                |      |      |
| BranchRegisterRequestProto.Builder        |      |      |
| BranchRegisterResponse                    |      |      |
| BranchRegisterResponseProto               |      |      |
| BranchRegisterResponseProto.Builder       |      |      |
| BranchReportRequest                       |      |      |
| BranchReportRequestProto                  |      |      |
| BranchReportRequestProto.Builder          |      |      |
| BranchReportResponse                      |      |      |
| BranchReportResponseProto                 |      |      |
| BranchReportResponseProto.Builder         |      |      |
| BranchRollbackRequest                     |      |      |
| BranchRollbackRequestProto                |      |      |
| BranchRollbackRequestProto.Builder        |      |      |
| BranchRollbackResponse                    |      |      |
| BranchRollbackResponseProto               |      |      |
| BranchRollbackResponseProto.Builder       |      |      |
| BranchStatus                              |      |      |
| BranchType                                |      |      |
| GlobalBeginRequest                        |      |      |
| GlobalBeginRequestProto                   |      |      |
| GlobalBeginRequestProto.Builder           |      |      |
| GlobalBeginResponse                       |      |      |
| GlobalBeginResponseProto                  |      |      |
| GlobalBeginResponseProto.Builder          |      |      |
| GlobalCommitRequest                       |      |      |
| GlobalCommitRequestProto                  |      |      |
| GlobalCommitRequestProto.Builder          |      |      |
| GlobalCommitResponse                      |      |      |
| GlobalCommitResponseProto                 |      |      |
| GlobalCommitResponseProto.Builder         |      |      |
| GlobalLockQueryRequest                    |      |      |
| GlobalLockQueryRequestProto               |      |      |
| GlobalLockQueryRequestProto.Builder       |      |      |
| GlobalLockQueryResponse                   |      |      |
| GlobalLockQueryResponseProto              |      |      |
| GlobalLockQueryResponseProto.Builder      |      |      |
| GlobalReportRequest                       |      |      |
| GlobalReportRequestProto                  |      |      |
| GlobalReportRequestProto.Builder          |      |      |
| GlobalReportResponse                      |      |      |
| GlobalReportResponseProto                 |      |      |
| GlobalReportResponseProto.Builder         |      |      |
| GlobalRollbackRequest                     |      |      |
| GlobalRollbackRequestProto                |      |      |
| GlobalRollbackRequestProto.Builder        |      |      |
| GlobalRollbackResponse                    |      |      |
| GlobalRollbackResponseProto               |      |      |
| GlobalRollbackResponseProto.Builder       |      |      |
| GlobalStatus                              |      |      |
| GlobalStatusRequest                       |      |      |
| GlobalStatusRequestProto                  |      |      |
| GlobalStatusRequestProto.Builder          |      |      |
| GlobalStatusResponse                      |      |      |
| GlobalStatusResponseProto                 |      |      |
| GlobalStatusResponseProto.Builder         |      |      |
| HeartbeatMessage                          |      |      |
| HeartbeatMessageProto                     |      |      |
| HeartbeatMessageProto.Builder             |      |      |
| MergedResultMessage                       |      |      |
| MergedResultMessageProto                  |      |      |
| MergedResultMessageProto.Builder          |      |      |
| MergedWarpMessage                         |      |      |
| MergedWarpMessageProto                    |      |      |
| MergedWarpMessageProto.Builder            |      |      |
| MessageType                               |      |      |
| RegisterRMRequest                         |      |      |
| RegisterRMRequestProto                    |      |      |
| RegisterRMRequestProto.Builder            |      |      |
| RegisterRMResponse                        |      |      |
| RegisterRMResponseProto                   |      |      |
| RegisterRMResponseProto.Builder           |      |      |
| RegisterTMRequest                         |      |      |
| RegisterTMRequestProto                    |      |      |
| RegisterTMRequestProto.Builder            |      |      |
| RegisterTMResponse                        |      |      |
| RegisterTMResponseProto                   |      |      |
| RegisterTMResponseProto.Builder           |      |      |
| ResultCode                                |      |      |
| TransactionExceptionCode                  |      |      |
| UndoLogDeleteRequest                      |      |      |
| UndoLogDeleteRequestProto                 |      |      |
| UndoLogDeleteRequestProto.Builder         |      |      |
|                                           |      |      |
| 枚举                                      |      |      |
|                                           |      |      |
| BranchStatusProto                         |      |      |
| BranchTypeProto                           |      |      |
| GlobalStatusProto                         |      |      |
| MessageTypeProto                          |      |      |
| ResultCodeProto                           |      |      |
| TransactionExceptionCodeProto             |      |      |



#### io.seata.serializer.protobuf.manager



ProtobufConvertManager



### io.seata.serializer.seata



MessageSeataCodec

类

MessageCodecFactory

SeataSerializer



#### io.seata.serializer.seata.protocol



|                               |      |      |
| ----------------------------- | ---- | ---- |
| AbstractIdentifyRequestCodec  |      |      |
| AbstractIdentifyResponseCodec |      |      |
| AbstractMessageCodec          |      |      |
| AbstractResultMessageCodec    |      |      |
| MergedWarpMessageCodec        |      |      |
| MergeResultMessageCodec       |      |      |
| RegisterRMRequestCodec        |      |      |
| RegisterRMResponseCodec       |      |      |
| RegisterTMRequestCodec        |      |      |
| RegisterTMResponseCodec       |      |      |
|                               |      |      |
|                               |      |      |



#### io.seata.serializer.seata.protocol.transaction



|                                     |      |      |
| ----------------------------------- | ---- | ---- |
| AbstractBranchEndRequestCodec       |      |      |
| AbstractBranchEndResponseCodec      |      |      |
| AbstractGlobalEndRequestCodec       |      |      |
| AbstractGlobalEndResponseCodec      |      |      |
| AbstractTransactionRequestCodec     |      |      |
| AbstractTransactionRequestToRMCodec |      |      |
| AbstractTransactionRequestToTCCodec |      |      |
| AbstractTransactionResponseCodec    |      |      |
| BranchCommitRequestCodec            |      |      |
| BranchCommitResponseCodec           |      |      |
| BranchRegisterRequestCodec          |      |      |
| BranchRegisterResponseCodec         |      |      |
| BranchReportRequestCodec            |      |      |
| BranchReportResponseCodec           |      |      |
| BranchRollbackRequestCodec          |      |      |
| BranchRollbackResponseCodec         |      |      |
| GlobalBeginRequestCodec             |      |      |
| GlobalBeginResponseCodec            |      |      |
| GlobalCommitRequestCodec            |      |      |
| GlobalCommitResponseCodec           |      |      |
| GlobalLockQueryRequestCodec         |      |      |
| GlobalLockQueryResponseCodec        |      |      |
| GlobalReportRequestCodec            |      |      |
| GlobalReportResponseCodec           |      |      |
| GlobalRollbackRequestCodec          |      |      |
| GlobalRollbackResponseCodec         |      |      |
| GlobalStatusRequestCodec            |      |      |
| GlobalStatusResponseCodec           |      |      |
| UndoLogDeleteRequestCodec           |      |      |



## io.seata.spring
### io.seata.spring.annotation



|                                |      |      |
| ------------------------------ | ---- | ---- |
| GlobalTransactionalInterceptor |      |      |
| GlobalTransactionScanner       |      |      |
| MethodDesc                     |      |      |
|                                |      |      |
| 注释类型                       |      |      |
|                                |      |      |
| GlobalLock                     |      |      |
| GlobalTransactional            |      |      |



#### io.seata.spring.annotation.datasource



|                                 |      |      |
| ------------------------------- | ---- | ---- |
| SeataProxy                      |      |      |
|                                 |      |      |
| 类                              |      |      |
|                                 |      |      |
| AutoDataSourceProxyRegistrar    |      |      |
| DataSourceProxyHolder           |      |      |
| SeataAutoDataSourceProxyAdvice  |      |      |
| SeataAutoDataSourceProxyCreator |      |      |
|                                 |      |      |
| 注释类型                        |      |      |
|                                 |      |      |
| EnableAutoDataSourceProxy       |      |      |



### io.seata.spring.event



类

DegradeCheckEvent



### io.seata.spring.tcc



TccActionInterceptor

TccAnnotationProcessor



### io.seata.spring.util



SpringProxyUtils

TCCBeanParserUtils



## io.seata.sqlparser





|                      |      |      |
| -------------------- | ---- | ---- |
| ParametersHolder     |      |      |
| SQLDeleteRecognizer  |      |      |
| SQLInsertRecognizer  |      |      |
| SQLRecognizer        |      |      |
| SQLRecognizerFactory |      |      |
| SQLSelectRecognizer  |      |      |
| SQLUpdateRecognizer  |      |      |
| WhereRecognizer      |      |      |
|                      |      |      |
| 类                   |      |      |
|                      |      |      |
| SqlParserType        |      |      |
|                      |      |      |
| 枚举                 |      |      |
|                      |      |      |
| SQLType              |      |      |
|                      |      |      |
| 异常错误             |      |      |
|                      |      |      |
| SQLParsingException  |      |      |



### io.seata.sqlparser.druid



|                                     |      |      |
| ----------------------------------- | ---- | ---- |
| SQLOperateRecognizerHolder          |      |      |
|                                     |      |      |
| 类                                  |      |      |
|                                     |      |      |
| BaseRecognizer                      |      |      |
| BaseRecognizer.VMarker              |      |      |
| DruidDelegatingDbTypeParser         |      |      |
| DruidDelegatingSQLRecognizerFactory |      |      |
| SQLOperateRecognizerHolderFactory   |      |      |





#### io.seata.sqlparser.druid.mysql



|                                |      |      |
| ------------------------------ | ---- | ---- |
| 类                             |      |      |
|                                |      |      |
| BaseMySQLRecognizer            |      |      |
| MySQLDeleteRecognizer          |      |      |
| MySQLInsertRecognizer          |      |      |
| MySQLOperateRecognizerHolder   |      |      |
| MySQLSelectForUpdateRecognizer |      |      |
| MySQLUpdateRecognizer          |      |      |



#### io.seata.sqlparser.druid.oracle



|                                 |      |      |
| ------------------------------- | ---- | ---- |
| BaseOracleRecognizer            |      |      |
| OracleDeleteRecognizer          |      |      |
| OracleInsertRecognizer          |      |      |
| OracleOperateRecognizerHolder   |      |      |
| OracleSelectForUpdateRecognizer |      |      |
| OracleUpdateRecognizer          |      |      |
|                                 |      |      |



#### io.seata.sqlparser.druid.postgresql



|                                     |      |      |
| ----------------------------------- | ---- | ---- |
| BasePostgresqlRecognizer            |      |      |
| PostgresqlDeleteRecognizer          |      |      |
| PostgresqlInsertRecognizer          |      |      |
| PostgresqlOperateRecognizerHolder   |      |      |
| PostgresqlSelectForUpdateRecognizer |      |      |
| PostgresqlUpdateRecognizer          |      |      |



### io.seata.sqlparser.struct



|                    |      |      |
| ------------------ | ---- | ---- |
| Defaultable        |      |      |
| Sequenceable       |      |      |
|                    |      |      |
| 类                 |      |      |
|                    |      |      |
| NotPlaceholderExpr |      |      |
| Null               |      |      |
| SqlDefaultExpr     |      |      |
| SqlMethodExpr      |      |      |
| SqlSequenceExpr    |      |      |



### io.seata.sqlparser.util



DbTypeParser

JdbcConstants



## io.seata.tm



DefaultTransactionManager

TMClient

TransactionManagerHolder



### io.seata.tm.api



|                                          |      |      |
| ---------------------------------------- | ---- | ---- |
| FailureHandler                           |      |      |
| GlobalTransaction                        |      |      |
| TransactionalExecutor                    |      |      |
|                                          |      |      |
| 类                                       |      |      |
|                                          |      |      |
| DefaultFailureHandlerImpl                |      |      |
| DefaultGlobalTransaction                 |      |      |
| GlobalTransactionContext                 |      |      |
| TransactionalTemplate                    |      |      |
|                                          |      |      |
| 枚举                                     |      |      |
|                                          |      |      |
| GlobalTransactionRole                    |      |      |
| TransactionalExecutor.Code               |      |      |
|                                          |      |      |
| 异常错误                                 |      |      |
|                                          |      |      |
| TransactionalExecutor.ExecutionException |      |      |



#### io.seata.tm.api.transaction



|                          |      |      |
| ------------------------ | ---- | ---- |
| TransactionHook          |      |      |
|                          |      |      |
| 类                       |      |      |
|                          |      |      |
| NoRollbackRule           |      |      |
| RollbackRule             |      |      |
| SuspendedResourcesHolder |      |      |
| TransactionHookAdapter   |      |      |
| TransactionHookManager   |      |      |
| TransactionInfo          |      |      |
|                          |      |      |
| 枚举                     |      |      |
|                          |      |      |
| Propagation              |      |      |