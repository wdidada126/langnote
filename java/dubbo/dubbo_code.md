# 类型dubbo源码挨个.java文件分析


https://javadoc.dev/online/api/org.apache.dubbo/dubbo/2.7.8/index.html








https://cn.dubbo.apache.org/zh-cn/docs/v2.7.8/user/quick-start.html

http://dubbo.apache.org/zh/docs/v2.7.8/javadoc/

https://cn.dubbo.apache.org/zh-cn/docs/references/api/











com.alibaba.com.caucho.hessian
com.alibaba.com.caucho.hessian.io
com.alibaba.com.caucho.hessian.io.java8
com.alibaba.com.caucho.hessian.security
com.alibaba.com.caucho.hessian.util
com.alibaba.dubbo.cache
com.alibaba.dubbo.cache.support
com.alibaba.dubbo.common
com.alibaba.dubbo.common.compiler
com.alibaba.dubbo.common.extension
com.alibaba.dubbo.common.logger
com.alibaba.dubbo.common.serialize
com.alibaba.dubbo.common.status
com.alibaba.dubbo.common.store
com.alibaba.dubbo.common.threadpool
com.alibaba.dubbo.common.utils
com.alibaba.dubbo.config
com.alibaba.dubbo.config.annotation
com.alibaba.dubbo.config.spring.context.annotation
com.alibaba.dubbo.container
com.alibaba.dubbo.monitor
com.alibaba.dubbo.qos.command
com.alibaba.dubbo.registry
com.alibaba.dubbo.registry.support
com.alibaba.dubbo.remoting
com.alibaba.dubbo.remoting.exchange
com.alibaba.dubbo.remoting.http
com.alibaba.dubbo.remoting.p2p
com.alibaba.dubbo.remoting.telnet
com.alibaba.dubbo.remoting.zookeeper
com.alibaba.dubbo.rpc
com.alibaba.dubbo.rpc.cluster
com.alibaba.dubbo.rpc.cluster.loadbalance
com.alibaba.dubbo.rpc.protocol.dubbo
com.alibaba.dubbo.rpc.protocol.rest.support
com.alibaba.dubbo.rpc.protocol.rmi
com.alibaba.dubbo.rpc.protocol.thrift
com.alibaba.dubbo.rpc.service
com.alibaba.dubbo.rpc.support
com.alibaba.dubbo.validation
org.apache.dubbo.cache
org.apache.dubbo.cache.filter
org.apache.dubbo.cache.support
org.apache.dubbo.cache.support.expiring
org.apache.dubbo.cache.support.jcache
org.apache.dubbo.cache.support.lfu
org.apache.dubbo.cache.support.lru
org.apache.dubbo.cache.support.threadlocal
org.apache.dubbo.common
org.apache.dubbo.common.beanutil
org.apache.dubbo.common.bytecode
org.apache.dubbo.common.compiler
org.apache.dubbo.common.compiler.support
org.apache.dubbo.common.config
org.apache.dubbo.common.config.configcenter
org.apache.dubbo.common.config.configcenter.file
org.apache.dubbo.common.config.configcenter.nop
org.apache.dubbo.common.config.configcenter.wrapper
org.apache.dubbo.common.constants
org.apache.dubbo.common.context
org.apache.dubbo.common.convert
org.apache.dubbo.common.convert.multiple
org.apache.dubbo.common.extension
org.apache.dubbo.common.extension.factory
org.apache.dubbo.common.extension.support
org.apache.dubbo.common.function
org.apache.dubbo.common.infra
org.apache.dubbo.common.infra.support
org.apache.dubbo.common.io
org.apache.dubbo.common.json
org.apache.dubbo.common.lang
org.apache.dubbo.common.logger
org.apache.dubbo.common.logger.jcl
org.apache.dubbo.common.logger.jdk
org.apache.dubbo.common.logger.log4j
org.apache.dubbo.common.logger.log4j2
org.apache.dubbo.common.logger.slf4j
org.apache.dubbo.common.logger.support
org.apache.dubbo.common.serialize
org.apache.dubbo.common.serialize.avro
org.apache.dubbo.common.serialize.fastjson
org.apache.dubbo.common.serialize.fst
org.apache.dubbo.common.serialize.gson
org.apache.dubbo.common.serialize.hessian2
org.apache.dubbo.common.serialize.hessian2.dubbo
org.apache.dubbo.common.serialize.java
org.apache.dubbo.common.serialize.kryo
org.apache.dubbo.common.serialize.kryo.optimized
org.apache.dubbo.common.serialize.kryo.utils
org.apache.dubbo.common.serialize.nativejava
org.apache.dubbo.common.serialize.protobuf.support
org.apache.dubbo.common.serialize.protobuf.support.wrapper
org.apache.dubbo.common.serialize.protostuff
org.apache.dubbo.common.serialize.protostuff.delegate
org.apache.dubbo.common.serialize.protostuff.utils
org.apache.dubbo.common.serialize.support
org.apache.dubbo.common.status
org.apache.dubbo.common.status.support
org.apache.dubbo.common.store
org.apache.dubbo.common.store.support
org.apache.dubbo.common.threadlocal
org.apache.dubbo.common.threadpool
org.apache.dubbo.common.threadpool.concurrent
org.apache.dubbo.common.threadpool.event
org.apache.dubbo.common.threadpool.manager
org.apache.dubbo.common.threadpool.support
org.apache.dubbo.common.threadpool.support.cached
org.apache.dubbo.common.threadpool.support.eager
org.apache.dubbo.common.threadpool.support.fixed
org.apache.dubbo.common.threadpool.support.limited
org.apache.dubbo.common.timer
org.apache.dubbo.common.utils



## dubbo jar分包分析



### org.apache.dubbo.cache



| org.apache.dubbo.cache | 类型      |      |
| ---------------------- | --------- | ---- |
|                        |           |      |
| Cache                  | interface |      |
| CacheFactory           | interface |      |



#### org.apache.dubbo.cache.filter



| org.apache.dubbo.cache.filter   | 类型 |      |
| ------------------------ | ---- | ---- |
| CacheFilter              |      |      |
| CacheFilter.ValueWrapper |      |      |
|                          |      |      |



#### org.apache.dubbo.cache.support

| org.apache.dubbo.cache.support | 类型 |      |
| ------------------------------ | ---- | ---- |
| AbstractCacheFactory           |      |      |
|                                |      |      |
|                                |      |      |

##### org.apache.dubbo.cache.support.expiring


| org.apache.dubbo.cache.support.expiring | 类型 |      |
| --------------------------------------- | ---- | ---- |
| ExpiringCache                           |      |      |
| ExpiringCacheFactory                    |      |      |
| ExpiringMap<K, V>                       |      |      |
| ExpiringMap<K, V>.ExpireThread          |      |      |
| ExpiringMap<K, V>.ExpireThread          |      |      |

##### org.apache.dubbo.cache.support.jcache


| org.apache.dubbo.cache.support.jcache | 类型 |      |
| ------------------------------ | ---- | ---- |
|       JCache                         |      |      |
|         JCacheFactory                       |      |      |
|                                |      |      |

##### org.apache.dubbo.cache.support.lfu


| org.apache.dubbo.cache.support.lfu | 类型 |      |
| ------------------------------ | ---- | ---- |
|        LfuCache                        |      |      |
|        LfuCacheFactory                        |      |      |
|                                |      |      |

##### org.apache.dubbo.cache.support.lru


| org.apache.dubbo.cache.support.lru | 类型 |      |
| ------------------------------ | ---- | ---- |
|         LruCache                       |      |      |
|         LruCacheFactory                       |      |      |
|                                |      |      |



##### org.apache.dubbo.cache.support.threadlocal


| org.apache.dubbo.cache.support.threadlocal | 类型 |      |
| ------------------------------------------ | ---- | ---- |
| ThreadLocalCache                           |      |      |
| ThreadLocalCacheFactory                    |      |      |
|                                            |      |      |



### org.apache.dubbo.common







| org.apache.dubbo.common | 类型 |      |
| ----------------------- | ---- | ---- |
|                         |      |      |
| Node                    |      |      |
| Resetable               |      |      |
|                         |      |      |
| 类                      |      |      |
|                         |      |      |
| BaseServiceMetadata     |      |      |
| Parameters              |      |      |
| URL                     |      |      |
| URLBuilder              |      |      |
| URLStrParser            |      |      |
| Version                 |      |      |
|                         |      |      |
| 注释类型                |      |      |
|                         |      |      |
| Experimental            |      |      |
| Extension               |      |      |





#### org.apache.dubbo.common.beanutil

| org.apache.dubbo.common.beanutil | 类型 |      |
| ------------------------------ | ---- | ---- |
|       JavaBeanAccessor                         |  enum    |      |
|      JavaBeanDescriptor                          |      |      |
|      JavaBeanSerializeUtil                          |      |      |

#### org.apache.dubbo.common.bytecode

| org.apache.dubbo.common.bytecode | 类型 |      |
| ------------------------------ | ---- | ---- |
|     ClassGenerator                           |      |      |
|     ClassGenerator  DC                         |      |      |
|      Mixin                          | abstract     |      |
|     Mixin MixinAware                           |   interface   |      |
|     NoSuchMethodException                           |      |      |
|     NoSuchPropertyException                           |      |      |
|     Proxy                           |  abstract    |      |
|    Wrapper                            |      |      |


#### org.apache.dubbo.common.compiler	 

| org.apache.dubbo.common.compiler | 类型 |      |
| ------------------------------ | ---- | ---- |
|        Compiler                        |  interface    |      |
|                                |      |      |
|                                |      |      |
##### org.apache.dubbo.common.compiler.support

| org.apache.dubbo.common.compiler.support | 类型 |      |
| ------------------------------ | ---- | ---- |
|        AbstractCompiler                        |   abstract   |      |
|        AdaptiveCompiler                        |      |      |
|         ClassUtils                       |      |      |
|        CtClassBuilder                        |      |      |
|       JavassistCompiler                         |      |      |
|      JdkCompiler                          |      |      |
|      JdkCompiler.ClassLoaderImpl                          |      |      |
|      JdkCompiler.JavaFileManagerImpl                          |      |      |
|      JdkCompiler.JavaFileObjectImpl                          |      |      |

#### org.apache.dubbo.common.config

| org.apache.dubbo.common.config | 类型 |      |
| ------------------------------ | ---- | ---- |
|        CompositeConfiguration              |      |      |
|      Configuration             |  interface    |      |
|      ConfigurationUtils    |      |      |
|       Environment                         |      |      |
|       EnvironmentConfiguration                         |      |      |
|       InmemoryConfiguration                         |      |      |
|          OrderedPropertiesProvider            | interface     |      |
|      PropertiesConfiguration      |      |      |
|     SystemConfiguration            |      |      |

##### org.apache.dubbo.common.config.configcenter	 

| org.apache.dubbo.common.config.configcenter | 类型 |      |
| ------------------------------------------- | ---- | ---- |
|                                             |      |      |
| 接口                                        |      |      |
|                                             |      |      |
| ConfigurationListener                       |      |      |
| Constants                                   |      |      |
| DynamicConfiguration                        |      |      |
| DynamicConfigurationFactory                 |      |      |
|                                             |      |      |
| 类                                          |      |      |
|                                             |      |      |
| AbstractDynamicConfiguration                |      |      |
| AbstractDynamicConfigurationFactory         |      |      |
| ConfigChangedEvent                          |      |      |
| TreePathDynamicConfiguration                |      |      |
|                                             |      |      |
| 枚举                                        |      |      |
|                                             |      |      |
| ConfigChangeType                            |      |      |


org.apache.dubbo.common.config.configcenter.file

| org.apache.dubbo.common.config.configcenter.file | 类型 |      |
| ------------------------------------------------ | ---- | ---- |
| FileSystemDynamicConfiguration                   |      |      |
| FileSystemDynamicConfigurationFactory            |      |      |
|                                                  |      |      |

org.apache.dubbo.common.config.configcenter.nop
过期

org.apache.dubbo.common.config.configcenter.wrapper
CompositeDynamicConfiguration


#### org.apache.dubbo.common.constants
| org.apache.dubbo.common.constants | 类型 |      |
| --------------------------------- | ---- | ---- |
| 接口                              |      |      |
| CommonConstants                   |      |      |
| FilterConstants                   |      |      |
| QosConstants                      |      |      |
| RegistryConstants                 |      |      |
| RemotingConstants                 |      |      |
|                                   |      |      |


#### org.apache.dubbo.common.context	
| org.apache.dubbo.common.constants | 类型 |  |
|-----------------------------------|-----------------------------------|-----------------------------------|
|   FrameworkExt        | interface |           |
|  Lifecycle               |  interface      |                 |
|    LifecycleAdapter                               |    abstract                       |                                   |

#### org.apache.dubbo.common.convert

| org.apache.dubbo.common.convert | 类型 |      |
| ------------------------------- | ---- | ---- |
|                                 |      |      |
| 接口                            |      |      |
|                                 |      |      |
| Converter                       |      |      |
| StringConverter                 |      |      |
|                                 |      |      |
| 类                              |      |      |
|                                 |      |      |
| StringToBooleanConverter        |      |      |
| StringToCharacterConverter      |      |      |
| StringToCharArrayConverter      |      |      |
| StringToDoubleConverter         |      |      |
| StringToFloatConverter          |      |      |
| StringToIntegerConverter        |      |      |
| StringToLongConverter           |      |      |
| StringToOptionalConverter       |      |      |
| StringToShortConverter          |      |      |
| StringToStringConverter         |      |      |


##### org.apache.dubbo.common.convert.multiple

| org.apache.dubbo.common.convert.multiple | 类型 |      |
| ---------------------------------------- | ---- | ---- |
|                                          |      |      |
| 接口                                     |      |      |
|                                          |      |      |
| MultiValueConverter                      |      |      |
| StringToMultiValueConverter              |      |      |
|                                          |      |      |
| 类                                       |      |      |
|                                          |      |      |
| StringToArrayConverter                   |      |      |
| StringToBlockingDequeConverter           |      |      |
| StringToBlockingQueueConverter           |      |      |
| StringToCollectionConverter              |      |      |
| StringToDequeConverter                   |      |      |
| StringToIterableConverter                |      |      |
| StringToListConverter                    |      |      |
| StringToNavigableSetConverter            |      |      |
| StringToQueueConverter                   |      |      |
| StringToSetConverter                     |      |      |
| StringToSortedSetConverter               |      |      |
| StringToTransferQueueConverter           |      |      |


#### org.apache.dubbo.common.extension	
| org.apache.dubbo.common.extension | 类型 |      |
| --------------------------------- | ---- | ---- |
|                                   |      |      |
| 接口                              |      |      |
|                                   |      |      |
| ExtensionFactory                  |      |      |
| LoadingStrategy                   |      |      |
|                                   |      |      |
| 类                                |      |      |
|                                   |      |      |
| AdaptiveClassCodeGenerator        |      |      |
| DubboInternalLoadingStrategy      |      |      |
| DubboLoadingStrategy              |      |      |
| ExtensionLoader                   |      |      |
| ServicesLoadingStrategy           |      |      |
|                                   |      |      |
| 注释类型                          |      |      |
|                                   |      |      |
| Activate                          |      |      |
| Adaptive                          |      |      |
| DisableInject                     |      |      |
| SPI                               |      |      |
| Wrapper                           |      |      |

##### org.apache.dubbo.common.extension.factory

类
AdaptiveExtensionFactory
SpiExtensionFactory

##### org.apache.dubbo.common.extension.support	

类
ActivateComparator
WrapperComparator


#### org.apache.dubbo.common.function
| org.apache.dubbo.common.function | 类型 |      |
| -------------------------------- | ---- | ---- |
|                                  |      |      |
| 接口                             |      |      |
|                                  |      |      |
| Predicates                       |      |      |
| Streams                          |      |      |
| ThrowableAction                  |      |      |
| ThrowableConsumer                |      |      |
| ThrowableFunction                |      |      |

#### org.apache.dubbo.common.infra
InfraAdapter

##### org.apache.dubbo.common.infra.support

CmdbAdapter
EnvironmentAdapter

#### org.apache.dubbo.common.io
| org.apache.dubbo.common.io  | 类型 |      |
| --------------------------- | ---- | ---- |
|                             |      |      |
| 类                          |      |      |
|                             |      |      |
| Bytes                       |      |      |
| StreamUtils                 |      |      |
| UnsafeByteArrayInputStream  |      |      |
| UnsafeByteArrayOutputStream |      |      |
| UnsafeStringReader          |      |      |
| UnsafeStringWriter          |      |      |



#### org.apache.dubbo.common.json
过期类

#### org.apache.dubbo.common.lang	 

Prioritized
ShutdownHookCallback
ShutdownHookCallbacks

#### org.apache.dubbo.common.logger
Level
Logger
LoggerAdapter
LoggerFactory

org.apache.dubbo.common.logger.jcl
JclLogger
JclLoggerAdapter

org.apache.dubbo.common.logger.jdk
JdkLogger
JdkLoggerAdapter

org.apache.dubbo.common.logger.log4j	 
Log4jLogger
Log4jLoggerAdapter

org.apache.dubbo.common.logger.log4j2
Log4j2Logger
Log4j2LoggerAdapter

org.apache.dubbo.common.logger.slf4j
Slf4jLogger
Slf4jLoggerAdapter

org.apache.dubbo.common.logger.support
FailsafeLogger


#### org.apache.dubbo.common.serialize
| org.apache.dubbo.common.serialize | 类型 |      |
| --------------------------------- | ---- | ---- |
|                                   |      |      |
| 接口                              |      |      |
|                                   |      |      |
| Cleanable                         |      |      |
| Constants                         |      |      |
| DataInput                         |      |      |
| DataOutput                        |      |      |
| ObjectInput                       |      |      |
| ObjectOutput                      |      |      |
| Serialization                     |      |      |



##### org.apache.dubbo.common.serialize.avro	 

AvroObjectInput
AvroObjectOutput
AvroSerialization

##### org.apache.dubbo.common.serialize.fastjson
FastJsonObjectInput
FastJsonObjectOutput
FastJsonSerialization

##### org.apache.dubbo.common.serialize.fst	 
FstFactory
FstObjectInput
FstObjectOutput
FstSerialization

##### org.apache.dubbo.common.serialize.gson	 
GsonJsonObjectInput
GsonJsonObjectOutput
GsonSerialization

##### org.apache.dubbo.common.serialize.hessian2	 
Hessian2ObjectInput
Hessian2ObjectOutput
Hessian2Serialization
Hessian2SerializerFactory

##### org.apache.dubbo.common.serialize.hessian2.dubbo	 
AbstractHessian2FactoryInitializer
DefaultHessian2FactoryInitializer
Hessian2FactoryInitializer
WhitelistHessian2FactoryInitializer

##### org.apache.dubbo.common.serialize.java	 
CompactedJavaSerialization
CompactedObjectInputStream
CompactedObjectOutputStream
JavaObjectInput
JavaObjectOutput
JavaSerialization

##### org.apache.dubbo.common.serialize.kryo	 
CompatibleKryo
KryoObjectInput
KryoObjectOutput
KryoSerialization

###### org.apache.dubbo.common.serialize.kryo.optimized	 
KryoObjectInput2
KryoObjectOutput2
KryoSerialization2
###### org.apache.dubbo.common.serialize.kryo.utils	 
AbstractKryoFactory
KryoUtils
PooledKryoFactory
PrototypeKryoFactory
ReflectionUtils
ThreadLocalKryoFactory

##### org.apache.dubbo.common.serialize.nativejava



| org.apache.dubbo.common.serialize.nativejava | 类型 |      |
| -------------------------------------------- | ---- | ---- |
|                                              |      |      |
| NativeJavaObjectInput                        |      |      |
| NativeJavaObjectOutput                       |      |      |
| NativeJavaSerialization                      |      |      |



###### org.apache.dubbo.common.serialize.protobuf.support



| org.apache.dubbo.common.serialize.protobuf.support | 类型 |      |
| -------------------------------------------------- | ---- | ---- |
| 类                                                 |      |      |
|                                                    |      |      |
| GenericProtobufJsonObjectInput                     |      |      |
| GenericProtobufJsonObjectOutput                    |      |      |
| GenericProtobufJsonSerialization                   |      |      |
| GenericProtobufObjectInput                         |      |      |
| GenericProtobufObjectOutput                        |      |      |
| GenericProtobufSerialization                       |      |      |
| ProtobufUtils                                      |      |      |
|                                                    |      |      |
| 异常错误                                           |      |      |
|                                                    |      |      |
| ProtobufWrappedException                           |      |      |





###### org.apache.dubbo.common.serialize.protobuf.support.wrapper	 





|                                             | 类型 |      |
| ------------------------------------------- | ---- | ---- |
| 接口                                        |      |      |
|                                             |      |      |
| MapValue.MapOrBuilder                       |      |      |
| ThrowablePB.StackTraceElementProtoOrBuilder |      |      |
| ThrowablePB.ThrowableProtoOrBuilder         |      |      |
|                                             |      |      |
| 类                                          |      |      |
|                                             |      |      |
| MapValue                                    |      |      |
| MapValue.Map                                |      |      |
| MapValue.Map.Builder                        |      |      |
| ThrowablePB                                 |      |      |
| ThrowablePB.StackTraceElementProto          |      |      |
| ThrowablePB.StackTraceElementProto.Builder  |      |      |
| ThrowablePB.ThrowableProto                  |      |      |
| ThrowablePB.ThrowableProto.Builder          |      |      |



##### org.apache.dubbo.common.serialize.protostuff





| org.apache.dubbo.common.serialize.protostuff | 类型 |      |
| -------------------------------------------- | ---- | ---- |
| 类                                           |      |      |
|                                              |      |      |
| ProtostuffObjectInput                        |      |      |
| ProtostuffObjectOutput                       |      |      |
| ProtostuffSerialization                      |      |      |
| Wrapper                                      |      |      |



###### org.apache.dubbo.common.serialize.protostuff.delegate



| org.apache.dubbo.common.serialize.protostuff.delegate | 类型 |      |
| ----------------------------------------------------- | ---- | ---- |
| 类                                                    |      |      |
|                                                       |      |      |
| SqlDateDelegate                                       |      |      |
| TimeDelegate                                          |      |      |
| TimestampDelegate                                     |      |      |



###### org.apache.dubbo.common.serialize.protostuff.utils





##### org.apache.dubbo.common.serialize.support



| org.apache.dubbo.common.serialize.support | 类型 |      |
| ----------------------------------------- | ---- | ---- |
| 接口                                      |      |      |
|                                           |      |      |
| SerializationOptimizer                    |      |      |
|                                           |      |      |
| 类                                        |      |      |
|                                           |      |      |
| SerializableClassRegistry                 |      |      |



#### org.apache.dubbo.common.status



| rg.apache.dubbo.common.status | 类型 |      |
| ----------------------------- | ---- | ---- |
| 接口                          |      |      |
|                               |      |      |
| StatusChecker                 |      |      |
|                               |      |      |
| 类                            |      |      |
|                               |      |      |
| Status                        |      |      |
|                               |      |      |
| 枚举                          |      |      |
|                               |      |      |
| Status.Level                  |      |      |



##### org.apache.dubbo.common.status.support



| org.apache.dubbo.common.status.support | 类型 |      |
| -------------------------------------- | ---- | ---- |
| 类                                     |      |      |
|                                        |      |      |
| LoadStatusChecker                      |      |      |
| MemoryStatusChecker                    |      |      |
| StatusUtils                            |      |      |



#### org.apache.dubbo.common.store

|                     | 类型 |      |
| ------------------- | ---- | ---- |
| 类                  |      |      |
|                     |      |      |
| LoadStatusChecker   |      |      |
| MemoryStatusChecker |      |      |
| StatusUtils         |      |      |



##### org.apache.dubbo.common.store.support

|                 | 类型 |      |
| --------------- | ---- | ---- |
| 类              |      |      |
|                 |      |      |
| SimpleDataStore |      |      |





#### org.apache.dubbo.common.threadlocal



|                            | 类型 |      |
| -------------------------- | ---- | ---- |
| 类                         |      |      |
|                            |      |      |
| InternalThread             |      |      |
| InternalThreadLocal        |      |      |
| InternalThreadLocalMap     |      |      |
| NamedInternalThreadFactory |      |      |



#### org.apache.dubbo.common.threadpool



|                    | 类型 |      |
| ------------------ | ---- | ---- |
| 接口               |      |      |
|                    |      |      |
| ThreadPool         |      |      |
|                    |      |      |
| 类                 |      |      |
|                    |      |      |
| ThreadlessExecutor |      |      |



##### org.apache.dubbo.common.threadpool.concurrent

ScheduledCompletableFuture





##### org.apache.dubbo.common.threadpool.event

| org.apache.dubbo.common.threadpool.event | 类型 |      |
| ---------------------------------------- | ---- | ---- |
| ThreadPoolExhaustedEvent                 |      |      |





##### org.apache.dubbo.common.threadpool.manager



| org.apache.dubbo.common.threadpool.manager | 类型 |      |
| ------------------------------------------ | ---- | ---- |
| 接口                                       |      |      |
|                                            |      |      |
| ExecutorRepository                         |      |      |
|                                            |      |      |
| 类                                         |      |      |
|                                            |      |      |
| DefaultExecutorRepository                  |      |      |
| Ring                                       |      |      |



##### org.apache.dubbo.common.threadpool.support



AbortPolicyWithReport



##### org.apache.dubbo.common.threadpool.support.cached



CachedThreadPool



##### org.apache.dubbo.common.threadpool.support.eager



|                         | 类型 |      |
| ----------------------- | ---- | ---- |
| 类                      |      |      |
|                         |      |      |
| EagerThreadPool         |      |      |
| EagerThreadPoolExecutor |      |      |
| TaskQueue               |      |      |



##### org.apache.dubbo.common.threadpool.support.fixed



FixedThreadPool



##### org.apache.dubbo.common.threadpool.support.limited



LimitedThreadPool



#### org.apache.dubbo.common.timer



|                  | 类型 |      |
| ---------------- | ---- | ---- |
| 接口             |      |      |
|                  |      |      |
| Timeout          |      |      |
| Timer            |      |      |
| TimerTask        |      |      |
|                  |      |      |
| 类               |      |      |
|                  |      |      |
| HashedWheelTimer |      |      |



#### org.apache.dubbo.common.utils





|                                   | 类型 |      |
| --------------------------------- | ---- | ---- |
| 接口                              |      |      |
|                                   |      |      |
| AnnotationUtils                   |      |      |
| FieldUtils                        |      |      |
| MemberUtils                       |      |      |
| MethodUtils                       |      |      |
| Page                              |      |      |
| PathUtils                         |      |      |
| TypeUtils                         |      |      |
|                                   |      |      |
| 类                                |      |      |
|                                   |      |      |
| ArrayUtils                        |      |      |
| Assert                            |      |      |
| AtomicPositiveInteger             |      |      |
| CharSequenceComparator            |      |      |
| CIDRUtils                         |      |      |
| ClassHelper                       |      |      |
| ClassUtils                        |      |      |
| CollectionUtils                   |      |      |
| CompatibleTypeUtils               |      |      |
| ConcurrentHashSet                 |      |      |
| ConfigUtils                       |      |      |
| DefaultPage                       |      |      |
| DubboAppender                     |      |      |
| ExecutorUtil                      |      |      |
| Holder                            |      |      |
| IOUtils                           |      |      |
| JVMUtil                           |      |      |
| LFUCache                          |      |      |
| Log                               |      |      |
| LogHelper                         |      |      |
| LogUtil                           |      |      |
| LRUCache                          |      |      |
| MethodComparator                  |      |      |
| NamedThreadFactory                |      |      |
| NetUtils                          |      |      |
| PojoUtils                         |      |      |
| ReflectUtils                      |      |      |
| ServiceAnnotationResolver         |      |      |
| Stack                             |      |      |
| StringConstantFieldValuePredicate |      |      |
| StringUtils                       |      |      |
| UrlUtils                          |      |      |
| Utf8Utils                         |      |      |



### org.apache.dubbo.config



| org.apache.dubbo.config | 类型 |      |
| ----------------------- | ---- | ---- |
| 接口                    |      |      |
|                         |      |      |
| ConfigInitializer       |      |      |
| ConfigPostProcessor     |      |      |
| Constants               |      |      |
|                         |      |      |
| 类                      |      |      |
|                         |      |      |
| AbstractConfig          |      |      |
| AbstractInterfaceConfig |      |      |
| AbstractMethodConfig    |      |      |
| AbstractReferenceConfig |      |      |
| AbstractServiceConfig   |      |      |
| ApplicationConfig       |      |      |
| ArgumentConfig          |      |      |
| ConfigCenterConfig      |      |      |
| ConsumerConfig          |      |      |
| DubboShutdownHook       |      |      |
| MetadataReportConfig    |      |      |
| MethodConfig            |      |      |
| MetricsConfig           |      |      |
| ModuleConfig            |      |      |
| MonitorConfig           |      |      |
| ProtocolConfig          |      |      |
| ProviderConfig          |      |      |
| ReferenceConfig         |      |      |
| ReferenceConfigBase     |      |      |
| RegistryConfig          |      |      |
| ServiceConfig           |      |      |
| ServiceConfigBase       |      |      |
| SslConfig               |      |      |



#### org.apache.dubbo.config.annotation

| org.apache.dubbo.config.annotation | 类型       |  解释    |
| ---------------------------------- | ---------- | ---- |
| Argument                           | @interface |      |
| DubboReference                     | @interface |      |
| DubboService                       | @interface |      |
| Reference                          | @interface |      |
| Service                            | @interface |      |







#### org.apache.dubbo.config.bootstrap


| org.apache.dubbo.config.bootstrap | 类型 |      |
| ------------------------------ | ---- | ---- |
|       DubboBootstrap                         |      |      |


##### org.apache.dubbo.config.bootstrap.builders

| org.apache.dubbo.config.bootstrap.builders | 类型 |      |
| ------------------------------------------ | ---- | ---- |
|                                            |      |      |
| 类                                         |      |      |
|                                            |      |      |
| AbstractBuilder                            |      |      |
| AbstractInterfaceBuilder                   |      |      |
| AbstractMethodBuilder                      |      |      |
| AbstractReferenceBuilder                   |      |      |
| AbstractServiceBuilder                     |      |      |
| ApplicationBuilder                         |      |      |
| ArgumentBuilder                            |      |      |
| ConfigCenterBuilder                        |      |      |
| ConsumerBuilder                            |      |      |
| MetadataReportBuilder                      |      |      |
| MethodBuilder                              |      |      |
| ModuleBuilder                              |      |      |
| MonitorBuilder                             |      |      |
| ProtocolBuilder                            |      |      |
| ProviderBuilder                            |      |      |
| ReferenceBuilder                           |      |      |
| RegistryBuilder                            |      |      |
| ServiceBuilder                             |      |      |


#### org.apache.dubbo.config.context



| org.apache.dubbo.config.context | 类型 |      |
| ------------------------------ | ---- | ---- |
|    ConfigConfigurationAdapter             |      |      |
|   ConfigManager      |      |      |
|                                |      |      |


#### org.apache.dubbo.config.event



| org.apache.dubbo.config.event      | 类型 |      |
| ---------------------------------- | ---- | ---- |
|                                    |      |      |
| 类                                 |      |      |
|                                    |      |      |
| DubboServiceDestroyedEvent         |      |      |
| DubboShutdownHookRegisteredEvent   |      |      |
| DubboShutdownHookUnregisteredEvent |      |      |
| ReferenceConfigDestroyedEvent      |      |      |
| ReferenceConfigInitializedEvent    |      |      |
| ServiceConfigExportedEvent         |      |      |
| ServiceConfigUnexportedEvent       |      |      |



##### org.apache.dubbo.config.event.listener



| org.apache.dubbo.config.event.listener | 类型 |      |
| ------------------------------ | ---- | ---- |
|    LoggingEventListener                            |      |      |
|     LoggingEventListener                           |      |      |
|                                |      |      |


#### org.apache.dubbo.config.invoker



| org.apache.dubbo.config.invoker | 类型 |      |
| ------------------------------ | ---- | ---- |
|    DelegateProviderMetaDataInvoker                            |      |      |
|                                |      |      |
|                                |      |      |


#### org.apache.dubbo.config.metadata



| org.apache.dubbo.config.metadata | 类型 |      |
| ------------------------------ | ---- | ---- |
|      AbstractMetadataServiceExporter                          |      |      |
|     ConfigurableMetadataServiceExporter   |      |      |
|    RemoteMetadataServiceExporter       |      |      |
|    ServiceInstancePortCustomizer    |      |      |



#### org.apache.dubbo.config.spring




| org.apache.dubbo.config.spring | 类型 |      |
| ------------------------------ | ---- | ---- |
|       ConfigCenterBean                         |      |      |
|        ReferenceBean                        |      |      |
|        ServiceBean<T>              |      |      |

org.apache.dubbo.config.spring.beans.factory.annotation

######  org.apache.dubbo.config.spring.beans.factory.annotation

| org.apache.dubbo.config.spring.beans.factory.annotation | 类型 |         解释                |
| ------------------------------------------------------- | ---- | ----------------------- |
| AbstractAnnotationConfigBeanBuilder                    |      | 处理@DubboService等注解 |
|   AnnotatedInterfaceConfigBeanBuilder      |      |  |
|     AnnotationPropertyValuesAdapter       |      |  |
|   DubboConfigAliasPostProcessor      |      |  |
| **ReferenceAnnotationBeanPostProcessor**                    |      | 处理@DubboReference等注解 |
|  ReferenceBeanBuilder     |      |  |
|  ServiceAnnotationBeanPostProcessor     | @Deprecated |  |
|     ServiceBeanNameBuilder      |      |  |
|   ServiceClassPostProcessor     |      | 实现BeanDefinitionRegistryPostProcessor 接口 |

ReferenceAnnotationBeanPostProcessor使用了DubboService

    public ReferenceAnnotationBeanPostProcessor() {
        super(DubboReference.class, Reference.class, com.alibaba.dubbo.config.annotation.Reference.class);
    }

存储在
com.alibaba.spring.beans.factory.annotation.AbstractAnnotationBeanPostProcessor#annotationTypes这个属性





ServiceClassPostProcessor 注册@DubboService修饰的类到spring ioc



ReferenceAnnotationBeanPostProcessor 跟 ServiceAnnotationBeanPostProcessor是对应的

###### org.apache.dubbo.config.spring.beans.factory.config



| org.apache.dubbo.config.spring.beans.factory.config |      |      |
| ------------------------------ | ---- | ---- |
|    ConfigurableSourceBeanMetadataElement                 |      |      |
|     DubboConfigDefaultPropertyValueBeanPostProcessor         |      |      |
|                                |      |      |


##### org.apache.dubbo.config.spring.context




| org.apache.dubbo.config.spring.context | 类型 |      |
| ------------------------------ | ---- | ---- |
|       DubboBootstrapApplicationListener            |      |      |
|   DubboLifecycleComponentApplicationListener     |      |      |
|  OneTimeExecutionApplicationContextEventListener           |   abstract  |      |

###### org.apache.dubbo.config.spring.context.annotation


| org.apache.dubbo.config.spring.context.annotation | 类型                   |      |
| ------------------------------------------------- | ---------------------- | ---- |
| 类                                                |                        |      |
| DubboClassPathBeanDefinitionScanner               |                        |      |
| DubboComponentScanRegistrar                       |                        |      |
| DubboConfigConfiguration                          |                        |      |
| DubboConfigConfiguration.Multiple                 |                        |      |
| DubboConfigConfiguration.Single                   |                        |      |
| DubboConfigConfigurationRegistrar                 |                        |      |
| DubboLifecycleComponentRegistrar                  |                        |      |
|                                                   |                        |      |
| 注释类型                                          |                        |      |
| DubboComponentScan                                | @interface             |      |
| EnableDubbo                                       | @interface             |      |
| EnableDubboConfig                                 | @interface             |      |
| EnableDubboLifecycle                              | @interface @Deprecated |      |





以下是一个使用Dubbo框架的应用程序的application.yml配置文件的示例：

```yaml
spring:
  application:
    name: my-dubbo-application

dubbo:
  application:
    id: my-application-id
    name: my-dubbo-application
  registry:
    address: zookeeper://localhost:2181
  protocol:
    name: dubbo
    port: 20880
  scan:
    base-packages: com.example.service
```

在上面的示例中，配置文件中的属性用于配置Dubbo框架的各个组件。

- `spring.application.name`配置了Spring Boot应用程序的名称。
- `dubbo.application.id`配置了Dubbo应用程序的ID。
- `dubbo.application.name`配置了Dubbo应用程序的名称。
- `dubbo.registry.address`配置了ZooKeeper注册中心的地址。
- `dubbo.protocol.name`配置了Dubbo使用的协议名称。
- `dubbo.protocol.port`配置了Dubbo协议的端口。
- `dubbo.scan.base-packages`配置了扫描Dubbo服务的基础包路径。

这只是一个简单的示例，您可以根据您的实际需求进行配置。根据您的应用程序的具体情况，您可能还需要配置其他Dubbo组件，如服务提供者、服务消费者等。

请确保在应用程序的类路径中包含Dubbo和相关依赖项，并正确配置ZooKeeper或其他支持的注册中心。

希望这个例子能帮助您理解如何在application.yml文件中配置Dubbo应用程序。



@EnableDubboConfig注解是Dubbo框架中的一个注解，用于启用Dubbo配置。Dubbo是一种分布式服务框架，用于构建高性能、可扩展的分布式应用程序。@EnableDubboConfig注解的作用是在Spring Boot应用程序中启用Dubbo的配置。

具体来说，@EnableDubboConfig注解可以用于启用Dubbo的配置属性，这些属性可以在application.properties或application.yml文件中配置。通过使用@EnableDubboConfig注解，可以将Dubbo的配置属性与Spring Boot的自动配置机制集成在一起，从而更方便地管理和配置Dubbo的相关功能。

使用@EnableDubboConfig注解时，通常需要指定一些属性值，例如扫描Dubbo配置的包路径、ZooKeeper注册中心的地址、Dubbo协议的端口等。这些属性值可以根据具体的需求进行配置。

总的来说，@EnableDubboConfig注解的作用是启用Dubbo的配置属性，并将其与Spring Boot的自动配置机制集成，以便更方便地管理和配置Dubbo框架。





###### org.apache.dubbo.config.spring.context.config



| org.apache.dubbo.config.spring.context.config | 类型 |      |
| ------------------------------ | ---- | ---- |
|    DubboConfigBeanCustomizer       |  interface    |      |
|      NamePropertyDefaultValueDubboConfigBeanCustomizer                          |      |      |
|                                |      |      |


###### org.apache.dubbo.config.spring.context.event



| org.apache.dubbo.config.spring.context.event | 类型 |      |
| -------------------------------------------- | ---- | ---- |
| ServiceBeanExportedEvent                     |      |      |
|                                              |      |      |
|                                              |      |      |


###### org.apache.dubbo.config.spring.context.properties




| org.apache.dubbo.config.spring.context.properties | 类型 |      |
| ------------------------------------------------- | ---- | ---- |
| AbstractDubboConfigBinder                         |      |      |
| DefaultDubboConfigBinder                          |      |      |
|                                                   |      |      |


##### org.apache.dubbo.config.spring.extension


| org.apache.dubbo.config.spring.extension | 类型 |      |
| ---------------------------------------- | ---- | ---- |
| SpringExtensionFactory                   |      |      |
|                                          |      |      |
|                                          |      |      |

##### org.apache.dubbo.config.spring.schema


| org.apache.dubbo.config.spring.schema | 类型 |      |
| ------------------------------ | ---- | ---- |
|     AnnotationBeanDefinitionParser               |      |      |
|    DubboBeanDefinitionParser              |      |      |
|   DubboNamespaceHandler                |      |      |



##### org.apache.dubbo.config.spring.schema


| org.apache.dubbo.config.spring.schema | 类型 | 解释                                                         |
| ------------------------------------- | ---- | ------------------------------------------------------------ |
| DubboBeanDefinitionParser             |      | 实现BeanDefinitionParser接口，DubboNamespaceHandler调用      |
| DubboNamespaceHandler                 |      | 代码见下面 继承org.springframework.beans.factory.xml.NamespaceHandlerSupport |
| AnnotationBeanDefinitionParser        |      | DubboNamespaceHandler调用                                    |



Dubbo使用Spring框架来解析dubbo命名空间的xml配置文件。
具体来说,Dubbo的dubbo命名空间是由DubboNamespaceHandler类来解析的。这个类实现了Spring的NamespaceHandler接口。
在Dubbo启动时,会通过Spring的扩展机制发现所有实现了NamespaceHandler接口的类,并调用其init()方法进行初始化。
DubboNamespaceHandler中的init()方法会将dubbo命名空间注册到Spring容器中,并指定哪些元素由哪些BeanDefinitionParser类来解析。
例如,它会注册:

<dubbo:protocol> 由DubboBeanDefinitionParser解析
<dubbo:service> 由DubboBeanDefinitionParser解析
<dubbo:reference> 由DubboBeanDefinitionParser解析

等等。

在解析dubbo命名空间XML时,Spring会找到对应元素的BeanDefinitionParser,并调用其解析方法生成BeanDefinition。

所以简单来说,Dubbo的xml配置是通过Spring框架的扩展机制来解析的,主要的解析工作在DubboNamespaceHandler和DubboBeanDefinitionParser中实现。





DubboNamespaceHandler代码


```java
        registerBeanDefinitionParser("application", new DubboBeanDefinitionParser(ApplicationConfig.class, true));
        registerBeanDefinitionParser("module", new DubboBeanDefinitionParser(ModuleConfig.class, true));
        registerBeanDefinitionParser("registry", new DubboBeanDefinitionParser(RegistryConfig.class, true));
        registerBeanDefinitionParser("config-center", new DubboBeanDefinitionParser(ConfigCenterBean.class, true));
        registerBeanDefinitionParser("metadata-report", new DubboBeanDefinitionParser(MetadataReportConfig.class, true));
        registerBeanDefinitionParser("monitor", new DubboBeanDefinitionParser(MonitorConfig.class, true));
        registerBeanDefinitionParser("metrics", new DubboBeanDefinitionParser(MetricsConfig.class, true));
        registerBeanDefinitionParser("ssl", new DubboBeanDefinitionParser(SslConfig.class, true));
        registerBeanDefinitionParser("provider", new DubboBeanDefinitionParser(ProviderConfig.class, true));
        registerBeanDefinitionParser("consumer", new DubboBeanDefinitionParser(ConsumerConfig.class, true));
        registerBeanDefinitionParser("protocol", new DubboBeanDefinitionParser(ProtocolConfig.class, true));
        registerBeanDefinitionParser("service", new DubboBeanDefinitionParser(ServiceBean.class, true));
        registerBeanDefinitionParser("reference", new DubboBeanDefinitionParser(ReferenceBean.class, false));
        registerBeanDefinitionParser("annotation", new AnnotationBeanDefinitionParser());
```

DubboBeanDefinitionParser
AnnotationBeanDefinitionParser













##### org.apache.dubbo.config.spring.status



| org.apache.dubbo.config.spring.status | 类型 |      |
| ------------------------------ | ---- | ---- |
|       DataSourceStatusChecker               |      |      |
|      SpringStatusChecker            |      |      |
|                                |      |      |


##### org.apache.dubbo.config.spring.util



| org.apache.dubbo.config.spring.util | 类型 |      |
| ------------------------------ | ---- | ---- |
|    DubboAnnotationUtils           |      |      |
|   DubboBeanUtils           |  interface   |      |
|                                |      |      |


#### org.apache.dubbo.config.support



| org.apache.dubbo.config.support | 类型 |      |
| ------------------------------ | ---- | ---- |
|     Parameter                  |  @interface   |      |
|                                |      |      |
|                                |      |      |


#### org.apache.dubbo.config.utils


| org.apache.dubbo.config.utils | 类型 |      |
| ------------------------------ | ---- | ---- |
|     ConfigValidationUtils          |      |      |
|    ReferenceConfigCache      |      |      |
|                                |      |      |

### org.apache.dubbo.configcenter



| org.apache.dubbo.configcenter | 类型 |      |
| ------------------------------ | ---- | ---- |
|                                |      |      |
|                                |      |      |
|                                |      |      |


#### org.apache.dubbo.configcenter.consul



| org.apache.dubbo.configcenter.consul | 类型 |      |
| ------------------------------ | ---- | ---- |
|     ConsulDynamicConfiguration            |      |      |
|     ConsulDynamicConfigurationFactory         |      |      |
|                                |      |      |

#### org.apache.dubbo.configcenter.support
##### org.apache.dubbo.configcenter.support.apollo



| org.apache.dubbo.configcenter.support.apollo | 类型 |      |
| -------------------------------------------- | ---- | ---- |
| 类                                           |      |      |
|                                              |      |      |
| ApolloDynamicConfiguration                   |      |      |
| ApolloDynamicConfigurationFactory            |      |      |



##### org.apache.dubbo.configcenter.support.etcd



| org.apache.dubbo.configcenter.support.etcd | 类型 |      |
| ------------------------------------------ | ---- | ---- |
| 类                                         |      |      |
|                                            |      |      |
| EtcdDynamicConfiguration                   |      |      |
| EtcdDynamicConfigurationFactory            |      |      |






##### org.apache.dubbo.configcenter.support.nacos





| org.apache.dubbo.configcenter.support.nacos | 类型 |      |
| ------------------------------------------- | ---- | ---- |
| 类                                          |      |      |
|                                             |      |      |
| NacosDynamicConfiguration                   |      |      |
| NacosDynamicConfigurationFactory            |      |      |




##### org.apache.dubbo.configcenter.support.zookeeper



| org.apache.dubbo.configcenter.support.zookeeper | 类型 |      |
| ----------------------------------------------- | ---- | ---- |
| 类                                              |      |      |
|                                                 |      |      |
| CacheListener                                   |      |      |
| ZookeeperDynamicConfiguration                   |      |      |
| ZookeeperDynamicConfigurationFactory            |      |      |





### org.apache.dubbo.container







#### org.apache.dubbo.container.log4j



| org.apache.dubbo.container.log4j | 类型 |      |
| ------------------------------ | ---- | ---- |
| Log4jContainer |      |      |
|                                |      |      |
|                                |      |      |


#### org.apache.dubbo.container.logback



| org.apache.dubbo.container.logback | 类型 |      |
| ------------------------------ | ---- | ---- |
| LogbackContainer |      |      |
|                                |      |      |
|                                |      |      |


#### org.apache.dubbo.container.spring



| org.apache.dubbo.container.spring | 类型 |      |
| ------------------------------ | ---- | ---- |
| SpringContainer |      |      |
|                                |      |      |
|                                |      |      |





### org.apache.dubbo.event



org.apache.dubbo.event





| org.apache.dubbo.event   | 类型 |      |
| ------------------------ | ---- | ---- |
| 接口                     |      |      |
|                          |      |      |
| ConditionalEventListener |      |      |
| EventDispatcher          |      |      |
| EventListener            |      |      |
| Listenable               |      |      |
|                          |      |      |
| 类                       |      |      |
|                          |      |      |
| AbstractEventDispatcher  |      |      |
| DirectEventDispatcher    |      |      |
| Event                    |      |      |
| GenericEvent             |      |      |
| GenericEventListener     |      |      |
| ParallelEventDispatcher  |      |      |




### org.apache.dubbo.metadata



| org.apache.dubbo.metadata              | 类型 |      |
| -------------------------------------- | ---- | ---- |
| 接口                                   |      |      |
|                                        |      |      |
| MetadataConstants                      |      |      |
| MetadataService                        |      |      |
| MetadataServiceExporter                |      |      |
| ServiceNameMapping                     |      |      |
| WritableMetadataService                |      |      |
|                                        |      |      |
| 类                                     |      |      |
|                                        |      |      |
| CompositeServiceNameMapping            |      |      |
| DynamicConfigurationServiceNameMapping |      |      |
| ParameterizedServiceNameMapping        |      |      |
| PropertiesFileServiceNameMapping       |      |      |
| ReadOnlyServiceNameMapping             |      |      |
| URLRevisionResolver                    |      |      |
|                                        |      |      |
| 枚举                                   |      |      |
|                                        |      |      |
| MetadataServiceType                    |      |      |







#### org.apache.dubbo.metadata.definition



| org.apache.dubbo.metadata.definition | 类型 |      |
| ------------------------------------ | ---- | ---- |
| 类                                   |      |      |
|                                      |      |      |
| MethodDefinitionBuilder              |      |      |
| ServiceDefinitionBuilder             |      |      |
| TypeDefinitionBuilder                |      |      |





##### org.apache.dubbo.metadata.definition.builder





|                       | 类型 |      |
| --------------------- | ---- | ---- |
| 接口                  |      |      |
|                       |      |      |
| TypeBuilder           |      |      |
|                       |      |      |
| 类                    |      |      |
|                       |      |      |
| ArrayTypeBuilder      |      |      |
| CollectionTypeBuilder |      |      |
| DefaultTypeBuilder    |      |      |
| EnumTypeBuilder       |      |      |
| MapTypeBuilder        |      |      |





##### org.apache.dubbo.metadata.definition.model



|                       | 类型 |      |
| --------------------- | ---- | ---- |
| 类                    |      |      |
|                       |      |      |
| FullServiceDefinition |      |      |
| MethodDefinition      |      |      |
| ServiceDefinition     |      |      |
| TypeDefinition        |      |      |






##### org.apache.dubbo.metadata.definition.util



| org.apache.dubbo.metadata.definition.util | 类型 |      |
| ----------------------------------------- | ---- | ---- |
| 类                                        |      |      |
|                                           |      |      |
| ClassUtils                                |      |      |
| JaketConfigurationUtils                   |      |      |





#### org.apache.dubbo.metadata.report



| org.apache.dubbo.metadata.report | 类型 |      |
| -------------------------------- | ---- | ---- |
| 接口                             |      |      |
|                                  |      |      |
| MetadataReport                   |      |      |
| MetadataReportFactory            |      |      |
|                                  |      |      |
| 类                               |      |      |
|                                  |      |      |
| MetadataReportInstance           |      |      |





##### org.apache.dubbo.metadata.report.identifier



|                                   | 类型 |      |
| --------------------------------- | ---- | ---- |
| 接口                              |      |      |
|                                   |      |      |
| BaseMetadataIdentifier            |      |      |
|                                   |      |      |
| 类                                |      |      |
|                                   |      |      |
| BaseApplicationMetadataIdentifier |      |      |
| BaseServiceMetadataIdentifier     |      |      |
| MetadataIdentifier                |      |      |
| ServiceMetadataIdentifier         |      |      |
| SubscriberMetadataIdentifier      |      |      |
|                                   |      |      |
| 枚举                              |      |      |
|                                   |      |      |
| KeyTypeEnum                       |      |      |





##### org.apache.dubbo.metadata.report.support



|                                        | 类型 |      |
| -------------------------------------- | ---- | ---- |
| 接口                                   |      |      |
|                                        |      |      |
| Constants                              |      |      |
|                                        |      |      |
| 类                                     |      |      |
|                                        |      |      |
| AbstractMetadataReport                 |      |      |
| AbstractMetadataReportFactory          |      |      |
| ConfigCenterBasedMetadataReport        |      |      |
| ConfigCenterBasedMetadataReportFactory |      |      |




###### org.apache.dubbo.metadata.report.support.file



| org.apache.dubbo.metadata.report.support.file | 类型 |      |
| --------------------------------------------- | ---- | ---- |
| FileSystemMetadataReportFactory               |      |      |
|                                               |      |      |
|                                               |      |      |


#### org.apache.dubbo.metadata.rest



| org.apache.dubbo.metadata.rest  | 类型 |      |
| ------------------------------- | ---- | ---- |
| FileSystemMetadataReportFactory |      |      |
|                                 |      |      |
|                                 |      |      |

##### org.apache.dubbo.metadata.rest.jaxrs

|                                   | 类型 |      |
| --------------------------------- | ---- | ---- |
| 类                                |      |      |
|                                   |      |      |
| DefaultValueParameterProcessor    |      |      |
| FormParamParameterProcessor       |      |      |
| HeaderParamParameterProcessor     |      |      |
| JAXRSServiceRestMetadataResolver  |      |      |
| MatrixParamParameterProcessor     |      |      |
| ParamAnnotationParameterProcessor |      |      |
| QueryParamParameterProcessor      |      |      |





##### org.apache.dubbo.metadata.rest.springmvc



| org.apache.dubbo.metadata.rest.springmvc    | 类型 |      |
| ------------------------------------------- | ---- | ---- |
| 类                                          |      |      |
|                                             |      |      |
| AbstractRequestAnnotationParameterProcessor |      |      |
| RequestHeaderParameterProcessor             |      |      |
| RequestParamParameterProcessor              |      |      |
| SpringMvcServiceRestMetadataResolver        |      |      |





#### org.apache.dubbo.metadata.store



| org.apache.dubbo.metadata.store         | 类型 |      |
| --------------------------------------- | ---- | ---- |
| 类                                      |      |      |
|                                         |      |      |
| AbstractAbstractWritableMetadataService |      |      |
| InMemoryWritableMetadataService         |      |      |
| RemoteWritableMetadataService           |      |      |





##### org.apache.dubbo.metadata.store.consul



| org.apache.dubbo.metadata.store.consul | 类型 |      |
| -------------------------------------- | ---- | ---- |
| 类                                     |      |      |
|                                        |      |      |
| ConsulMetadataReport                   |      |      |
| ConsulMetadataReportFactory            |      |      |





##### org.apache.dubbo.metadata.store.etcd



| org.apache.dubbo.metadata.store.etcd | 类型 |      |
| ------------------------------------ | ---- | ---- |
| 类                                   |      |      |
|                                      |      |      |
| EtcdMetadataReport                   |      |      |
| EtcdMetadataReportFactory            |      |      |




##### org.apache.dubbo.metadata.store.nacos



| org.apache.dubbo.metadata.store.nacos | 类型 |      |
| ------------------------------------- | ---- | ---- |
| 类                                    |      |      |
|                                       |      |      |
| NacosMetadataReport                   |      |      |
| NacosMetadataReportFactory            |      |      |



##### org.apache.dubbo.metadata.store.redis



|                            | 类型 |      |
| -------------------------- | ---- | ---- |
| 类                         |      |      |
|                            |      |      |
| RedisMetadataReport        |      |      |
| RedisMetadataReportFactory |      |      |




##### org.apache.dubbo.metadata.store.zookeeper



| org.apache.dubbo.metadata.store.zookeeper | 类型 |      |
| ----------------------------------------- | ---- | ---- |
| 类                                        |      |      |
|                                           |      |      |
| ZookeeperMetadataReport                   |      |      |
| ZookeeperMetadataReportFactory            |      |      |





### org.apache.dubbo.monitor





| org.apache.dubbo.monitor | 类型 |      |
| ------------------------ | ---- | ---- |
|                          |      |      |
| 接口                     |      |      |
|                          |      |      |
| Constants                |      |      |
| MetricsService           |      |      |
| Monitor                  |      |      |
| MonitorFactory           |      |      |
| MonitorService           |      |      |





#### org.apache.dubbo.monitor.dubbo



| org.apache.dubbo.monitor.dubbo | 类型 |      |
| ------------------------------ | ---- | ---- |
| 类                             |      |      |
|                                |      |      |
| DubboMonitor                   |      |      |
| DubboMonitorFactory            |      |      |
| MetricsFilter                  |      |      |
| Statistics                     |      |      |




#### org.apache.dubbo.monitor.support





| org.apache.dubbo.monitor.support | 类型 |      |
| -------------------------------- | ---- | ---- |
| 类                               |      |      |
|                                  |      |      |
| AbstractMonitorFactory           |      |      |
| MetricsServiceDetector           |      |      |
| MonitorFilter                    |      |      |
| MonitorServiceDetector           |      |      |



### org.apache.dubbo.qos







#### org.apache.dubbo.qos.command



| org.apache.dubbo.qos.command | 类型 |      |
| ---------------------------- | ---- | ---- |
| 接口                         |      |      |
|                              |      |      |
| BaseCommand                  |      |      |
| CommandExecutor              |      |      |
|                              |      |      |
| 类                           |      |      |
|                              |      |      |
| CommandContext               |      |      |
| CommandContextFactory        |      |      |
| DefaultCommandExecutor       |      |      |
|                              |      |      |
| 异常错误                     |      |      |
|                              |      |      |
| NoSuchCommandException       |      |      |






##### org.apache.dubbo.qos.command.annotation



| org.apache.dubbo.qos.command.annotation | 类型 |      |
| --------------------------------------- | ---- | ---- |
| Cmd                                     |      |      |
|                                         |      |      |
|                                         |      |      |


##### org.apache.dubbo.qos.command.decoder



| org.apache.dubbo.qos.command.decoder | 类型 |      |
| ------------------------------ | ---- | ---- |
| HttpCommandDecoder |      |      |
| TelnetCommandDecoder |      |      |
|                                |      |      |


##### org.apache.dubbo.qos.command.impl





| org.apache.dubbo.qos.command.impl | 类型 |      |
| --------------------------------- | ---- | ---- |
| 类                                |      |      |
|                                   |      |      |
| Help                              |      |      |
| Ls                                |      |      |
| Offline                           |      |      |
| Online                            |      |      |
| Quit                              |      |      |
| Ready                             |      |      |
| Version                           |      |      |




##### org.apache.dubbo.qos.command.util



| org.apache.dubbo.qos.command.util | 类型 |      |
| ------------------------------ | ---- | ---- |
| CommandHelper |      |      |
| ServiceCheckUtils |      |      |
|                                |      |      |


#### org.apache.dubbo.qos.common



| org.apache.dubbo.qos.common | 类型 |      |
| ------------------------------ | ---- | ---- |
| QosConstants |      |      |
|                                |      |      |
|                                |      |      |

#### org.apache.dubbo.qos.legacy



| org.apache.dubbo.qos.legacy | 类型 |      |
| --------------------------- | ---- | ---- |
| 类                          |      |      |
|                             |      |      |
| ChangeTelnetHandler         |      |      |
| CountTelnetHandler          |      |      |
| CurrentTelnetHandler        |      |      |
| InvokeTelnetHandler         |      |      |
| ListTelnetHandler           |      |      |
| LogTelnetHandler            |      |      |
| PortTelnetHandler           |      |      |
| SelectTelnetHandler         |      |      |
| ShutdownTelnetHandler       |      |      |
| TraceTelnetHandler          |      |      |






#### org.apache.dubbo.qos.protocol



| org.apache.dubbo.qos.protocol | 类型 |      |
| ------------------------------ | ---- | ---- |
| QosProtocolWrapper |      |      |
|                                |      |      |
|                                |      |      |


#### org.apache.dubbo.qos.server



| org.apache.dubbo.qos.server | 类型 |      |
| ------------------------------ | ---- | ---- |
| DubboLogo |      |      |
| Server |      |      |
|                                |      |      |

##### org.apache.dubbo.qos.server.handler



| org.apache.dubbo.qos.server.handler | 类型 |      |
| ----------------------------------- | ---- | ---- |
| 类                                  |      |      |
|                                     |      |      |
| HttpProcessHandler                  |      |      |
| LocalHostPermitHandler              |      |      |
| QosProcessHandler                   |      |      |
| TelnetProcessHandler                |      |      |






#### org.apache.dubbo.qos.textui



| org.apache.dubbo.qos.textui | 类型 |      |
| --------------------------- | ---- | ---- |
| 接口                        |      |      |
|                             |      |      |
| TComponent                  |      |      |
|                             |      |      |
| 类                          |      |      |
|                             |      |      |
| TKv                         |      |      |
| TLadder                     |      |      |
| TTable                      |      |      |
| TTable.ColumnDefine         |      |      |
| TTree                       |      |      |
|                             |      |      |
| 枚举                        |      |      |
|                             |      |      |
| TTable.Align                |      |      |





### org.apache.dubbo.registry



| org.apache.dubbo.registry | 类型 |      |
| ------------------------- | ---- | ---- |
| 接口                      |      |      |
|                           |      |      |
| AddressListener           |      |      |
| Constants                 |      |      |
| NotifyListener            |      |      |
| Registry                  |      |      |
| RegistryFactory           |      |      |
| RegistryService           |      |      |
| RegistryServiceListener   |      |      |
|                           |      |      |
| 类                        |      |      |
|                           |      |      |
| ListenerRegistryWrapper   |      |      |
| RegistryFactoryWrapper    |      |      |





#### org.apache.dubbo.registry.client



| org.apache.dubbo.registry.client  | 类型 |      |
| --------------------------------- | ---- | ---- |
| 接口                              |      |      |
|                                   |      |      |
| ServiceDiscovery                  |      |      |
| ServiceDiscoveryFactory           |      |      |
| ServiceInstance                   |      |      |
| ServiceInstanceCustomizer         |      |      |
|                                   |      |      |
| 类                                |      |      |
|                                   |      |      |
| AbstractServiceDiscoveryFactory   |      |      |
| DefaultServiceDiscoveryFactory    |      |      |
| DefaultServiceInstance            |      |      |
| FileSystemServiceDiscovery        |      |      |
| ServiceDiscoveryRegistry          |      |      |
| ServiceDiscoveryRegistryFactory   |      |      |
| ServiceDiscoveryRegistryProtocol  |      |      |
| ServiceInstanceMetadataCustomizer |      |      |





##### org.apache.dubbo.registry.client.event



| org.apache.dubbo.registry.client.event |      | 类型 |      |
| -------------------------------------- | ---- | ---- | ---- |
| 类                                     |      |      |      |
|                                        |      |      |      |
| ServiceDiscoveryDestroyedEvent         |      |      |      |
| ServiceDiscoveryDestroyingEvent        |      |      |      |
| ServiceDiscoveryEvent                  |      |      |      |
| ServiceDiscoveryExceptionEvent         |      |      |      |
| ServiceDiscoveryInitializedEvent       |      |      |      |
| ServiceDiscoveryInitializingEvent      |      |      |      |
| ServiceInstanceEvent                   |      |      |      |
| ServiceInstancePreRegisteredEvent      |      |      |      |
| ServiceInstancePreUnregisteredEvent    |      |      |      |
| ServiceInstanceRegisteredEvent         |      |      |      |
| ServiceInstancesChangedEvent           |      |      |      |
| ServiceInstanceUnregisteredEvent       |      |      |      |





###### org.apache.dubbo.registry.client.event.listener





| org.apache.dubbo.registry.client.event.listener | 类型 |      |
| ----------------------------------------------- | ---- | ---- |
| 类                                              |      |      |
|                                                 |      |      |
| CustomizableServiceInstanceListener             |      |      |
| LoggingEventListener                            |      |      |
| ServiceInstancesChangedListener                 |      |      |



##### org.apache.dubbo.registry.client.metadata



| org.apache.dubbo.registry.client.metadata    | 类型 |      |
| -------------------------------------------- | ---- | ---- |
| 接口                                         |      |      |
|                                              |      |      |
| MetadataServiceURLBuilder                    |      |      |
| SubscribedURLsSynthesizer                    |      |      |
|                                              |      |      |
| 类                                           |      |      |
|                                              |      |      |
| ExportedServicesRevisionMetadataCustomizer   |      |      |
| MetadataServiceURLParamsMetadataCustomizer   |      |      |
| ProtocolPortsMetadataCustomizer              |      |      |
| RestProtocolSubscribedURLsSynthesizer        |      |      |
| ServiceInstanceMetadataUtils                 |      |      |
| ServiceInstanceMetadataUtils.Endpoint        |      |      |
| SpringCloudMetadataServiceURLBuilder         |      |      |
| StandardMetadataServiceURLBuilder            |      |      |
| SubscribedServicesRevisionMetadataCustomizer |      |      |



###### org.apache.dubbo.registry.client.metadata.proxy



| org.apache.dubbo.registry.client.metadata.proxy | 类型 |      |
| ----------------------------------------------- | ---- | ---- |
| 接口                                            |      |      |
|                                                 |      |      |
| MetadataServiceProxyFactory                     |      |      |
|                                                 |      |      |
| 类                                              |      |      |
|                                                 |      |      |
| CompositeMetadataServiceProxyFactory            |      |      |
| DefaultMetadataServiceProxyFactory              |      |      |
| RemoteMetadataServiceProxy                      |      |      |
| RemoteMetadataServiceProxyFactory               |      |      |





##### org.apache.dubbo.registry.client.selector



| org.apache.dubbo.registry.client.selector | 类型 |      |
| ----------------------------------------- | ---- | ---- |
| 接口                                      |      |      |
| ServiceInstanceSelector                   |      |      |
|                                           |      |      |
| 类                                        |      |      |
| RandomServiceInstanceSelector             |      |      |





#### org.apache.dubbo.registry.consul





| org.apache.dubbo.registry.consul | 类型 |      |
| -------------------------------- | ---- | ---- |
| 类                               |      |      |
|                                  |      |      |
| AbstractConsulRegistry           |      |      |
| ConsulRegistry                   |      |      |
| ConsulRegistryFactory            |      |      |
| ConsulServiceDiscovery           |      |      |
|                                  |      |      |
| 枚举                             |      |      |
|                                  |      |      |
| ConsulParameter                  |      |      |





#### org.apache.dubbo.registry.dubbo



| org.apache.dubbo.registry.dubbo | 类型 |      |
| ------------------------------- | ---- | ---- |
| 类                              |      |      |
|                                 |      |      |
| DubboRegistry                   |      |      |
| DubboRegistryFactory            |      |      |



#### org.apache.dubbo.registry.etcd



| org.apache.dubbo.registry.etcd | 类型 |      |
| ------------------------------ | ---- | ---- |
| 类                             |      |      |
|                                |      |      |
| EtcdRegistry                   |      |      |
| EtcdRegistryFactory            |      |      |
| EtcdServiceDiscovery           |      |      |






#### org.apache.dubbo.registry.eureka


| org.apache.dubbo.registry.eureka | 类型 |      |
| ------------------------------ | ---- | ---- |
| EurekaServiceDiscovery |      |      |
|                                |      |      |
|                                |      |      |

#### org.apache.dubbo.registry.integration



| org.apache.dubbo.registry.integration | 类型 |      |
| ------------------------------------- | ---- | ---- |
| 接口                                  |      |      |
|                                       |      |      |
| RegistryProtocolListener              |      |      |
|                                       |      |      |
| 类                                    |      |      |
|                                       |      |      |
| AbstractConfiguratorListener          |      |      |
| RegistryDirectory                     |      |      |
| RegistryProtocol                      |      |      |
| RegistryProtocol.InvokerDelegate      |      |      |






#### org.apache.dubbo.registry.multicast


| org.apache.dubbo.registry.multicast | 类型 |      |
| ------------------------------ | ---- | ---- |
| MulticastRegistry |      |      |
| MulticastRegistryFactory |      |      |
|                                |      |      |


#### org.apache.dubbo.registry.multiple


| org.apache.dubbo.registry.multiple | 类型 |      |
| ------------------------------ | ---- | ---- |
| MultipleRegistry |      |      |
| MultipleRegistryFactory |      |      |
|                                |      |      |

#### org.apache.dubbo.registry.nacos



| org.apache.dubbo.registry.nacos | 类型 |      |
| ------------------------------- | ---- | ---- |
|                                 |      |      |
| 类                              |      |      |
|                                 |      |      |
| NacosRegistry                   |      |      |
| NacosRegistryFactory            |      |      |
| NacosServiceDiscovery           |      |      |
| NacosServiceName                |      |      |






##### org.apache.dubbo.registry.nacos.util


| org.apache.dubbo.registry.nacos.util | 类型 |      |
| ------------------------------ | ---- | ---- |
| NacosInstanceManageUtil |      |      |
| NacosNamingServiceUtils |      |      |
|                                |      |      |


#### org.apache.dubbo.registry.redis


| org.apache.dubbo.registry.redis | 类型 |      |
| ------------------------------ | ---- | ---- |
| RedisRegistry |      |      |
| RedisRegistryFactory |      |      |
|                                |      |      |

#### org.apache.dubbo.registry.retry



| org.apache.dubbo.registry.retry | 类型 |      |
| ------------------------------- | ---- | ---- |
| 类                              |      |      |
|                                 |      |      |
| AbstractRetryTask               |      |      |
| FailedNotifiedTask              |      |      |
| FailedRegisteredTask            |      |      |
| FailedSubscribedTask            |      |      |
| FailedUnregisteredTask          |      |      |
| FailedUnsubscribedTask          |      |      |
| ReExportTask                    |      |      |



#### org.apache.dubbo.registry.sofa



| org.apache.dubbo.registry.sofa | 类型 |      |
| ------------------------------ | ---- | ---- |
|                                |      |      |
| 类                             |      |      |
|                                |      |      |
| SofaRegistry                   |      |      |
| SofaRegistryConstants          |      |      |
| SofaRegistryFactory            |      |      |




#### org.apache.dubbo.registry.status


| org.apache.dubbo.registry.status | 类型 |      |
| ------------------------------ | ---- | ---- |
| RegistryStatusChecker |      |      |
|                                |      |      |
|                                |      |      |

#### org.apache.dubbo.registry.support



| org.apache.dubbo.registry.support | 类型 |      |
| --------------------------------- | ---- | ---- |
|                                   |      |      |
| AbstractRegistry                  |      |      |
| AbstractRegistryFactory           |      |      |
| FailbackRegistry                  |      |      |
|                                   |      |      |
| 异常错误                          |      |      |
|                                   |      |      |
| SkipFailbackWrapperException      |      |      |



#### org.apache.dubbo.registry.zookeeper



| org.apache.dubbo.registry.zookeeper    | 类型 |      |
| -------------------------------------- | ---- | ---- |
|                                        |      |      |
| ZookeeperInstance                      |      |      |
| ZookeeperRegistry                      |      |      |
| ZookeeperRegistryFactory               |      |      |
| ZookeeperServiceDiscovery              |      |      |
| ZookeeperServiceDiscoveryChangeWatcher |      |      |




##### org.apache.dubbo.registry.zookeeper.util


| org.apache.dubbo.registry.zookeeper.util | 类型 |      |
| ---------------------------------------- | ---- | ---- |
| CuratorFrameworkUtils                    |      |      |
| CuratorFrameworkParams                   | enum |      |
|                                          |      |      |







### org.apache.dubbo.remoting



| org.apache.dubbo.remoting | 类型 |      |
| ------------------------- | ---- | ---- |
|                           |      |      |
| 接口                      |      |      |
|                           |      |      |
| Channel                   |      |      |
| ChannelHandler            |      |      |
| Client                    |      |      |
| Codec                     |      |      |
| Codec2                    |      |      |
| Constants                 |      |      |
| Decodeable                |      |      |
| Dispatcher                |      |      |
| Endpoint                  |      |      |
| IdleSensible              |      |      |
| RemotingServer            |      |      |
| Transporter               |      |      |
|                           |      |      |
| 类                        |      |      |
|                           |      |      |
| Transporters              |      |      |
|                           |      |      |
| 枚举                      |      |      |
|                           |      |      |
| Codec2.DecodeResult       |      |      |
|                           |      |      |
| 异常错误                  |      |      |
|                           |      |      |
| ExecutionException        |      |      |
| RemotingException         |      |      |
| TimeoutException          |      |      |


#### org.apache.dubbo.remoting.buffer

| org.apache.dubbo.remoting.buffer | 类型 |      |
| -------------------------------- | ---- | ---- |
| 接口                             |      |      |
|                                  |      |      |
| ChannelBuffer                    |      |      |
| ChannelBufferFactory             |      |      |
|                                  |      |      |
| 类                               |      |      |
|                                  |      |      |
| AbstractChannelBuffer            |      |      |
| ByteBufferBackedChannelBuffer    |      |      |
| ChannelBufferInputStream         |      |      |
| ChannelBufferOutputStream        |      |      |
| ChannelBuffers                   |      |      |
| DirectChannelBufferFactory       |      |      |
| DynamicChannelBuffer             |      |      |
| HeapChannelBuffer                |      |      |
| HeapChannelBufferFactory         |      |      |


#### org.apache.dubbo.remoting.etcd

| org.apache.dubbo.remoting.etcd | 类型 |      |
| ------------------------------ | ---- | ---- |
|                                |      |      |
| 接口                           |      |      |
|                                |      |      |
| ChildListener                  |      |      |
| Constants                      |      |      |
| EtcdClient                     |      |      |
| EtcdTransporter                |      |      |
| RetryPolicy                    |      |      |
| StateListener                  |      |      |
|                                |      |      |
| 类                             |      |      |
|                                |      |      |
| AbstractRetryPolicy            |      |      |


##### org.apache.dubbo.remoting.etcd.jetcd

| org.apache.dubbo.remoting.etcd.jetcd | 类型 |      |
| ------------------------------------ | ---- | ---- |
| 接口                                 |      |      |
|                                      |      |      |
| ConnectionStateListener              |      |      |
|                                      |      |      |
| 类                                   |      |      |
|                                      |      |      |
| JEtcdClient                          |      |      |
| JEtcdClientWrapper                   |      |      |
| JEtcdTransporter                     |      |      |
| RetryLoops                           |      |      |
| RetryNTimes                          |      |      |



##### org.apache.dubbo.remoting.etcd.option


| org.apache.dubbo.remoting.etcd.option |      |      |
| ------------------------------ | ---- | ---- |
|    OptionUtil                            |      |      |
|                                |      |      |
|                                |      |      |


##### org.apache.dubbo.remoting.etcd.support


| org.apache.dubbo.remoting.etcd.support | 类型 |      |
| ------------------------------ |---| ---- |
|        AbstractEtcdClient   | abstract |      |
|                                |   |      |
|                                |   |      |


#### org.apache.dubbo.remoting.exchange


| org.apache.dubbo.remoting.exchange | 类型 |      |
| ---------------------------------- | ---- | ---- |
| 接口                               |      |      |
|                                    |      |      |
| ExchangeChannel                    |      |      |
| ExchangeClient                     |      |      |
| ExchangeHandler                    |      |      |
| Exchanger                          |      |      |
| ExchangeServer                     |      |      |
|                                    |      |      |
| 类                                 |      |      |
|                                    |      |      |
| Exchangers                         |      |      |
| Request                            |      |      |
| Response                           |      |      |


##### org.apache.dubbo.remoting.exchange.codec


| org.apache.dubbo.remoting.exchange.codec | 类型 |      |
| ---------------------------------------- | ---- | ---- |
| ExchangeCodec                            |      |      |
|                                          |      |      |
|                                          |      |      |


##### org.apache.dubbo.remoting.exchange.support


| org.apache.dubbo.remoting.exchange.support | 类型 |      |
| ------------------------------ | ---- | ---- |
|                                |      |      |
| 接口                                         |||
|                                            |||
| Replier                                    |||
|                                            |||
| 类                                          |||
|                                            |||
| DefaultFuture                              |||
| ExchangeHandlerAdapter                     |||
| ExchangeHandlerDispatcher                  |||
| ExchangeServerDelegate                     |||
| MultiMessage                               |||
| ReplierDispatcher                          |||


###### org.apache.dubbo.remoting.exchange.support.header


| org.apache.dubbo.remoting.exchange.support.header | 类型 |      |
| ------------------------------ | ---- | ---- |
| AbstractTimerTask | abstract |      |
| CloseTimerTask |      |      |
| HeaderExchangeChannel |      |      |
|HeaderExchangeClient|||
| HeaderExchangeHandler |||
| HeaderExchanger                          |||
| HeaderExchangeServer |||
| HeartbeatHandler                    |||
| HeartbeatTimerTask |||
| ReconnectTimerTask                        |||
|                                            |          |      |
|                                                   |          |      |
|                                                   |          |      |
|                                                   |          |      |
|                                                   |          |      |
|                                                   |          |      |
|                                                   |||


#### org.apache.dubbo.remoting.http


| org.apache.dubbo.remoting.http | 类型 |      |
| ------------------------------ | ---- | ---- |
|    HttpBinder         |   interface   |      |
|   HttpHandler             |   interface   |      |
|    HttpServer              |  interface    |      |


##### org.apache.dubbo.remoting.http.jetty


| org.apache.dubbo.remoting.http.jetty | 类型 |      |
| ------------------------------ | ---- | ---- |
|     JettyHttpBinder                  |      |      |
|     JettyHttpServer               |      |      |
|                                |      |      |


##### org.apache.dubbo.remoting.http.servlet


| org.apache.dubbo.remoting.http.servlet | 类型 |      |
| ------------------------------ | ---- | ---- |
|   AbstractHttpServer               |      |      |
|                                |      |      |
|                                |      |      |

| org.apache.dubbo.remoting.http.servlet | 类型 |      |
| -------------------------------------- | ---- | ---- |
| 类                                     |      |      |
|                                        |      |      |
| BootstrapListener                      |      |      |
| DispatcherServlet                      |      |      |
| ServletHttpBinder                      |      |      |
| ServletHttpServer                      |      |      |
| ServletManager                         |      |      |


##### org.apache.dubbo.remoting.http.support


| org.apache.dubbo.remoting.http.support | 类型 |      |
| ------------------------------ | ---- | ---- |
|                                |      |      |
|                                |      |      |
|                                |      |      |


##### org.apache.dubbo.remoting.http.tomcat


| org.apache.dubbo.remoting.http.tomcat | 类型 |      |
| ------------------------------ | ---- | ---- |
|     TomcatHttpBinder            |      |      |
|    TomcatHttpServer         |      |      |
|                                |      |      |


#### org.apache.dubbo.remoting.p2p


| org.apache.dubbo.remoting.p2p | 类型 |      |
| ------------------------------ | ---- | ---- |
|                                |      |      |
|                                |      |      |
|                                |      |      |


##### org.apache.dubbo.remoting.p2p.exchange


| org.apache.dubbo.remoting.p2p.exchange | 类型 |      |
| ------------------------------ | ---- | ---- |
|                                |      |      |
|                                |      |      |
|                                |      |      |


###### org.apache.dubbo.remoting.p2p.exchange.support


| org.apache.dubbo.remoting.p2p.exchange.support | 类型 |      |
| ---------------------------------------------- | ---- | ---- |
|                                                |      |      |
|                                                |      |      |
|                                                |      |      |


##### org.apache.dubbo.remoting.p2p.support


| org.apache.dubbo.remoting.p2p.support | 类型 |      |
| ------------------------------ | ---- | ---- |
|                                |      |      |
|                                |      |      |
|                                |      |      |


#### org.apache.dubbo.remoting.telnet


| org.apache.dubbo.remoting.telnet | 类型 |      |
| ------------------------------ | ---- | ---- |
|        TelnetHandler                |      |      |
|                                |      |      |
|                                |      |      |


##### org.apache.dubbo.remoting.telnet.codec


| org.apache.dubbo.remoting.telnet.codec | 类型 |      |
| ------------------------------ | ---- | ---- |
|     TelnetCodec                 |      |      |
|                                |      |      |
|                                |      |      |


##### org.apache.dubbo.remoting.telnet.support


| org.apache.dubbo.remoting.telnet.support | 类型       |      |
| ---------------------------------------- | ---------- | ---- |
| Help                                     | @interface |      |
| TelnetHandlerAdapter                     |            |      |
| TelnetUtils                              |            |      |


###### org.apache.dubbo.remoting.telnet.support.command


| org.apache.dubbo.remoting.telnet.support.command | 类型 |      |
| ------------------------------------------------ | ---- | ---- |
|                                                  |      |      |
|                                                  |      |      |
|                                                  |      |      |

| org.apache.dubbo.remoting.telnet.support.command | 类型 |      |
| ------------------------------------------------ | ---- | ---- |
| 类                                               |      |      |
|                                                  |      |      |
| ClearTelnetHandler                               |      |      |
| ExitTelnetHandler                                |      |      |
| HelpTelnetHandler                                |      |      |
| LogTelnetHandler                                 |      |      |
| StatusTelnetHandler                              |      |      |

#### org.apache.dubbo.remoting.transport

| org.apache.dubbo.remoting.transport | 类型 |      |
| ----------------------------------- | ---- | ---- |
| 接口                                |      |      |
|                                     |      |      |
| ChannelHandlerDelegate              |      |      |
|                                     |      |      |
| 类                                  |      |      |
|                                     |      |      |
| AbstractChannel                     |      |      |
| AbstractChannelHandlerDelegate      |      |      |
| AbstractClient                      |      |      |
| AbstractCodec                       |      |      |
| AbstractEndpoint                    |      |      |
| AbstractPeer                        |      |      |
| AbstractServer                      |      |      |
| ChannelDelegate                     |      |      |
| ChannelHandlerAdapter               |      |      |
| ChannelHandlerDispatcher            |      |      |
| ClientDelegate                      |      |      |
| CodecSupport                        |      |      |
| DecodeHandler                       |      |      |
| MultiMessageHandler                 |      |      |
| ServerDelegate                      |      |      |
|                                     |      |      |
| 异常错误                            |      |      |
|                                     |      |      |
| ExceedPayloadLimitException         |      |      |


##### org.apache.dubbo.remoting.transport.codec


| org.apache.dubbo.remoting.transport.codec | 类型 |      |
| ----------------------------------------- | ---- | ---- |
| CodecAdapter                              |      |      |
| TransportCodec                            |      |      |
|                                           |      |      |


##### org.apache.dubbo.remoting.transport.dispatcher


| org.apache.dubbo.remoting.transport.dispatcher | 类型 |      |
| ---------------------------------------------- | ---- | ---- |
| ChannelEventRunnable                           |      |      |
| ChannelEventRunnable.ChannelState              |      |      |
| ChannelHandlers                                |      |      |
| WrappedChannelHandler                          |      |      |


###### org.apache.dubbo.remoting.transport.dispatcher.all


| org.apache.dubbo.remoting.transport.dispatcher.all | 类型 |      |
| -------------------------------------------------- | ---- | ---- |
| AllChannelHandler                                  |      |      |
| AllDispatcher                                      |      |      |
|                                                    |      |      |


###### org.apache.dubbo.remoting.transport.dispatcher.connection


| org.apache.dubbo.remoting.transport.dispatcher.connection | 类型 |      |
| --------------------------------------------------------- | ---- | ---- |
| ConnectionOrderedChannelHandler                           |      |      |
| ConnectionOrderedDispatcher                               |      |      |
|                                                           |      |      |


###### org.apache.dubbo.remoting.transport.dispatcher.direct


| org.apache.dubbo.remoting.transport.dispatcher.direct | 类型 |      |
| ----------------------------------------------------- | ---- | ---- |
| DirectChannelHandler                                  |      |      |
| DirectDispatcher                                      |      |      |
|                                                       |      |      |


###### org.apache.dubbo.remoting.transport.dispatcher.execution


| org.apache.dubbo.remoting.transport.dispatcher.execution | 类型 |      |
| -------------------------------------------------------- | ---- | ---- |
| ExecutionChannelHandler                                  |      |      |
| ExecutionDispatcher                                      |      |      |
|                                                          |      |      |


###### org.apache.dubbo.remoting.transport.dispatcher.message


| org.apache.dubbo.remoting.transport.dispatcher.message | 类型 |      |
| ------------------------------------------------------ | ---- | ---- |
| MessageOnlyChannelHandler                              |      |      |
| MessageOnlyDispatcher                                  |      |      |
|                                                        |      |      |


##### org.apache.dubbo.remoting.transport.grizzly


| org.apache.dubbo.remoting.transport.grizzly | 类型 |      |
| ------------------------------------------- | ---- | ---- |
| 类                                          |      |      |
|                                             |      |      |
| GrizzlyClient                               |      |      |
| GrizzlyCodecAdapter                         |      |      |
| GrizzlyHandler                              |      |      |
| GrizzlyServer                               |      |      |
| GrizzlyTransporter                          |      |      |


##### org.apache.dubbo.remoting.transport.mina


| org.apache.dubbo.remoting.transport.mina | 类型 |      |
| ---------------------------------------- | ---- | ---- |
| 类                                       |      |      |
|                                          |      |      |
| MinaClient                               |      |      |
| MinaHandler                              |      |      |
| MinaServer                               |      |      |
| MinaTransporter                          |      |      |


##### org.apache.dubbo.remoting.transport.netty

| org.apache.dubbo.remoting.transport.netty | 类型 |      |
| ----------------------------------------- | ---- | ---- |
| 类                                        |      |      |
|                                           |      |      |
| NettyBackedChannelBuffer                  |      |      |
| NettyBackedChannelBufferFactory           |      |      |
| NettyClient                               |      |      |
| NettyHandler                              |      |      |
| NettyServer                               |      |      |
| NettyTransporter                          |      |      |


##### org.apache.dubbo.remoting.transport.netty4

| org.apache.dubbo.remoting.transport.netty4     | 类型 |      |
| ---------------------------------------------- | ---- | ---- |
| 类                                             |      |      |
|                                                |      |      |
| NettyBackedChannelBuffer                       |      |      |
| NettyClient                                    |      |      |
| NettyClientHandler                             |      |      |
| NettyCodecAdapter                              |      |      |
| NettyEventLoopFactory                          |      |      |
| NettyServer                                    |      |      |
| NettyServerHandler                             |      |      |
| NettyTransporter                               |      |      |
| SslContexts                                    |      |      |
| SslHandlerInitializer                          |      |      |
| SslHandlerInitializer.HandshakeCompletionEvent |      |      |
| SslHandlerInitializer.SslClientTlsHandler      |      |      |
| SslHandlerInitializer.SslServerTlsHandler      |      |      |


ChannelHandlerAdapter.png

###### org.apache.dubbo.remoting.transport.netty4.logging


| org.apache.dubbo.remoting.transport.netty4.logging | 类型 |      |
| -------------------------------------------------- | ---- | ---- |
| FormattingTuple                                    |      |      |
| MessageFormatter                                   |      |      |
|                                                    |      |      |


#### org.apache.dubbo.remoting.utils




| org.apache.dubbo.remoting.utils | 类型 |      |
| ------------------------------ | ---- | ---- |
|   PayloadDropper           |      |      |
|    UrlUtils               |      |      |
|                                |      |      |


org.apache.dubbo.remoting.zookeeper

org.apache.dubbo.remoting.zookeeper.curator
CuratorZookeeperClient
CuratorZookeeperClient.CuratorConnectionStateListener
CuratorZookeeperClient.CuratorWatcherImpl
CuratorZookeeperTransporter

org.apache.dubbo.remoting.zookeeper.support
AbstractZookeeperClient
AbstractZookeeperTransporter
### org.apache.dubbo.rpc






| org.apache.dubbo.rpc                 | 类型 |      |
| ------------------------------------ | ---- | ---- |
|                                      |      |      |
| 接口                                 |      |      |
|                                      |      |      |
| AsyncContext                         |      |      |
| Constants                            |      |      |
| Exporter                             |      |      |
| ExporterListener                     |      |      |
| Filter                               |      |      |
| Filter.Listener                      |      |      |
| Invocation                           |      |      |
| Invoker                              |      |      |
| InvokerListener                      |      |      |
| Protocol                             |      |      |
| ProtocolServer                       |      |      |
| ProxyFactory                         |      |      |
| Result                               |      |      |
| ZoneDetector                         |      |      |
|                                      |      |      |
| 类                                   |      |      |
|                                      |      |      |
| AppResponse                          |      |      |
| AsyncContextImpl                     |      |      |
| AsyncRpcResult                       |      |      |
| AttachmentsAdapter                   |      |      |
| AttachmentsAdapter.ObjectToStringMap |      |      |
| FutureContext                        |      |      |
| ListenableFilter                     |      |      |
| RpcConstants                         |      |      |
| RpcContext                           |      |      |
| RpcInvocation                        |      |      |
| RpcStatus                            |      |      |
| TimeoutCountDown                     |      |      |
|                                      |      |      |
| 枚举                                 |      |      |
|                                      |      |      |
| InvokeMode                           |      |      |
|                                      |      |      |
| 异常错误                             |      |      |
|                                      |      |      |
| RpcException                         |      |      |



#### org.apache.dubbo.rpc.cluster

| org.apache.dubbo.rpc.cluster | 类型 |      |
| ---------------------------- | ---- | ---- |
|                              |      |      |
| 接口                         |      |      |
|                              |      |      |
| Cluster                      |      |      |
| ClusterInvoker               |      |      |
| Configurator                 |      |      |
| ConfiguratorFactory          |      |      |
| Constants                    |      |      |
| Directory                    |      |      |
| LoadBalance                  |      |      |
| Merger                       |      |      |
| Router                       |      |      |
| RouterFactory                |      |      |
| RuleConverter                |      |      |
|                              |      |      |
| 类                           |      |      |
|                              |      |      |
| CacheableRouterFactory       |      |      |
| RouterChain                  |      |      |



##### org.apache.dubbo.rpc.cluster.configurator


| org.apache.dubbo.rpc.cluster.configurator | 类型 |      |
| ----------------------------------------- | ---- | ---- |
| AbstractConfigurator                      |      |      |
|                                           |      |      |
|                                           |      |      |


###### org.apache.dubbo.rpc.cluster.configurator.absent

| org.apache.dubbo.rpc.cluster.configurator.absent | 类型 |      |
| ------------------------------------------------ | ---- | ---- |
| AbsentConfigurator                               |      |      |
| AbsentConfiguratorFactory                        |      |      |
|                                                  |      |      |


###### org.apache.dubbo.rpc.cluster.configurator.override

| org.apache.dubbo.rpc.cluster.configurator.override | 类型 |      |
| -------------------------------------------------- | ---- | ---- |
| OverrideConfigurator                               |      |      |
| OverrideConfiguratorFactory                        |      |      |
|                                                    |      |      |


###### org.apache.dubbo.rpc.cluster.configurator.parser

| org.apache.dubbo.rpc.cluster.configurator.parser | 类型 |      |
| ------------------------------------------------ | ---- | ---- |
| ConfigParser                                     |      |      |
|                                                  |      |      |
|                                                  |      |      |


###### org.apache.dubbo.rpc.cluster.configurator.parser.model

| org.apache.dubbo.rpc.cluster.configurator.parser.model | 类型 |      |
| ------------------------------------------------------ | ---- | ---- |
| ConfigItem                                             |      |      |
| ConfiguratorConfig                                     |      |      |
|                                                        |      |      |


##### org.apache.dubbo.rpc.cluster.directory

| org.apache.dubbo.rpc.cluster.directory | 类型 |      |
| ------------------------------ | ---- | ---- |
|    AbstractDirectory<T>             |      |      |
|    StaticDirectory<T>           |      |      |
|                                |      |      |


##### org.apache.dubbo.rpc.cluster.governance

| org.apache.dubbo.rpc.cluster.governance | 类型 |      |
| ------------------------------ | ---- | ---- |
|   DefaultGovernanceRuleRepositoryImpl               |      |      |
|  GovernanceRuleRepository           |  interface   |      |
|                                |      |      |


##### org.apache.dubbo.rpc.cluster.interceptor

| org.apache.dubbo.rpc.cluster.interceptor | 类型 |      |
| ---------------------------------------- | ---- | ---- |
| ClusterInterceptor                       |      |      |
| ClusterInterceptor Listener              |      |      |
| ConsumerContextClusterInterceptor        |      |      |
| ZoneAwareClusterInterceptor              |      |      |


##### org.apache.dubbo.rpc.cluster.loadbalance

| org.apache.dubbo.rpc.cluster.loadbalance | 类型 |      |
| ---------------------------------------- | ---- | ---- |
|                                          |      |      |
| 类                                       |      |      |
|                                          |      |      |
| AbstractLoadBalance                      |      |      |
| ConsistentHashLoadBalance                |      |      |
| LeastActiveLoadBalance                   |      |      |
| RandomLoadBalance                        |      |      |
| RoundRobinLoadBalance                    |      |      |
| ShortestResponseLoadBalance              |      |      |


##### org.apache.dubbo.rpc.cluster.merger

| org.apache.dubbo.rpc.cluster.merger | 类型 |      |
| ----------------------------------- | ---- | ---- |
|                                     |      |      |
| 类                                  |      |      |
|                                     |      |      |
| ArrayMerger                         |      |      |
| BooleanArrayMerger                  |      |      |
| ByteArrayMerger                     |      |      |
| CharArrayMerger                     |      |      |
| DoubleArrayMerger                   |      |      |
| FloatArrayMerger                    |      |      |
| IntArrayMerger                      |      |      |
| ListMerger                          |      |      |
| LongArrayMerger                     |      |      |
| MapMerger                           |      |      |
| MergerFactory                       |      |      |
| SetMerger                           |      |      |
| ShortArrayMerger                    |      |      |

##### org.apache.dubbo.rpc.cluster.router

| org.apache.dubbo.rpc.cluster.router | 类型 |      |
| ------------------------------ | ---- | ---- |
|     AbstractRouter       |  abstract   |      |
|    AbstractRouterRule    | abstract   |      |
|                                |      |      |


###### org.apache.dubbo.rpc.cluster.router.condition

| org.apache.dubbo.rpc.cluster.router.condition | 类型 |      |
| --------------------------------------------- | ---- | ---- |
| ConditionRouter                               |      |      |
| ConditionRouter MatchPair                     |      |      |
| ConditionRouterFactory                        |      |      |


###### org.apache.dubbo.rpc.cluster.router.condition.config

| org.apache.dubbo.rpc.cluster.router.condition.config | 类型 |      |
| ---------------------------------------------------- | ---- | ---- |
|                                                      |      |      |
| 类                                                   |      |      |
|                                                      |      |      |
| AppRouter                                            |      |      |
| AppRouterFactory                                     |      |      |
| ListenableRouter                                     |      |      |
| ServiceRouter                                        |      |      |
| ServiceRouterFactory                                 |      |      |



###### org.apache.dubbo.rpc.cluster.router.condition.config.model

| org.apache.dubbo.rpc.cluster.router.condition.config.model | 类型 |      |
| ---------------------------------------------------------- | ---- | ---- |
| ConditionRouterRule                                        |      |      |
| ConditionRuleParser                                        |      |      |
|                                                            |      |      |


###### org.apache.dubbo.rpc.cluster.router.file

| org.apache.dubbo.rpc.cluster.router.file | 类型 |      |
| ---------------------------------------- | ---- | ---- |
| FileRouterFactory                        |      |      |
|                                          |      |      |
|                                          |      |      |


###### org.apache.dubbo.rpc.cluster.router.mock

| org.apache.dubbo.rpc.cluster.router.mock | 类型 |      |
| ---------------------------------------- | ---- | ---- |
| MockInvokersSelector                     |      |      |
| MockRouterFactory                        |      |      |
|                                          |      |      |


###### org.apache.dubbo.rpc.cluster.router.script

| org.apache.dubbo.rpc.cluster.router.script | 类型 |      |
| ------------------------------------------ | ---- | ---- |
| ScriptRouter                               |      |      |
| ScriptRouterFactory                        |      |      |
|                                            |      |      |


###### org.apache.dubbo.rpc.cluster.router.tag

| org.apache.dubbo.rpc.cluster.router.tag | 类型 |      |
| --------------------------------------- | ---- | ---- |
| TagRouter                               |      |      |
| TagRouterFactory                        |      |      |
|                                         |      |      |


###### org.apache.dubbo.rpc.cluster.router.tag.model

| org.apache.dubbo.rpc.cluster.router.tag.model | 类型 |      |
| --------------------------------------------- | ---- | ---- |
| Tag                                           |      |      |
| TagRouterRule                                 |      |      |
| TagRuleParser                                 |      |      |


##### org.apache.dubbo.rpc.cluster.support

| org.apache.dubbo.rpc.cluster.support | 类型 |      |
| ------------------------------------ | ---- | ---- |
|                                      |      |      |
| 类                                   |      |      |
|                                      |      |      |
| AbstractClusterInvoker               |      |      |
| AvailableCluster                     |      |      |
| AvailableClusterInvoker              |      |      |
| BroadcastCluster                     |      |      |
| BroadcastClusterInvoker              |      |      |
| ClusterUtils                         |      |      |
| FailbackCluster                      |      |      |
| FailbackClusterInvoker               |      |      |
| FailfastCluster                      |      |      |
| FailfastClusterInvoker               |      |      |
| FailoverCluster                      |      |      |
| FailoverClusterInvoker               |      |      |
| FailsafeCluster                      |      |      |
| FailsafeClusterInvoker               |      |      |
| ForkingCluster                       |      |      |
| ForkingClusterInvoker                |      |      |
| MergeableCluster                     |      |      |
| MergeableClusterInvoker              |      |      |



###### org.apache.dubbo.rpc.cluster.support.registry

| org.apache.dubbo.rpc.cluster.support.registry | 类型 |      |
| --------------------------------------------- | ---- | ---- |
| ZoneAwareCluster                              |      |      |
| ZoneAwareClusterInvoker                       |      |      |
|                                               |      |      |


###### org.apache.dubbo.rpc.cluster.support.wrapper

| org.apache.dubbo.rpc.cluster.support.wrapper | 类型 |      |
| -------------------------------------------- | ---- | ---- |
| AbstractCluster                              |      |      |
| MockClusterInvoker<T>                        |      |      |
| MockClusterWrapper                           |      |      |


#### org.apache.dubbo.rpc.filter

| org.apache.dubbo.rpc.filter | 类型 |      |
| --------------------------- | ---- | ---- |
|                             |      |      |
| 类                          |      |      |
|                             |      |      |
| AccessLogFilter             |      |      |
| ActiveLimitFilter           |      |      |
| ClassLoaderFilter           |      |      |
| CompatibleFilter            |      |      |
| ConsumerContextFilter       |      |      |
| ContextFilter               |      |      |
| DeprecatedFilter            |      |      |
| EchoFilter                  |      |      |
| ExceptionFilter             |      |      |
| ExecuteLimitFilter          |      |      |
| GenericFilter               |      |      |
| GenericImplFilter           |      |      |
| TimeoutFilter               |      |      |
| TokenFilter                 |      |      |
| TpsLimitFilter              |      |      |



##### org.apache.dubbo.rpc.filter.tps

| org.apache.dubbo.rpc.filter.tps | 类型 |      |
| ------------------------------ | ---- | ---- |
|    DefaultTPSLimiter                |      |      |
|   StatItem              |      |      |
|   TPSLimiter                  |    interface  |      |


#### org.apache.dubbo.rpc.listener

| org.apache.dubbo.rpc.listener | 类型 |      |
| ----------------------------- | ---- | ---- |
|                               |      |      |
| 类                            |      |      |
|                               |      |      |
| DeprecatedInvokerListener     |      |      |
| ExporterListenerAdapter       |      |      |
| InvokerListenerAdapter        |      |      |
| ListenerExporterWrapper       |      |      |
| ListenerInvokerWrapper        |      |      |



#### org.apache.dubbo.rpc.model

| org.apache.dubbo.rpc.model      | 类型 |      |
| ------------------------------- | ---- | ---- |
|                                 |      |      |
| 接口                            |      |      |
|                                 |      |      |
| ApplicationInitListener         |      |      |
| BuiltinServiceDetector          |      |      |
|                                 |      |      |
| 类                              |      |      |
|                                 |      |      |
| ApplicationModel                |      |      |
| AsyncMethodInfo                 |      |      |
| ConsumerMethodModel             |      |      |
| ConsumerModel                   |      |      |
| MethodDescriptor                |      |      |
| ProviderMethodModel             |      |      |
| ProviderModel                   |      |      |
| ProviderModel.RegisterStatedURL |      |      |
| ServiceDescriptor               |      |      |
| ServiceMetadata                 |      |      |
| ServiceRepository               |      |      |


#### org.apache.dubbo.rpc.protocol

| org.apache.dubbo.rpc.protocol | 类型 |      |
| ----------------------------- | ---- | ---- |
|                               |      |      |
| 类                            |      |      |
|                               |      |      |
| AbstractExporter              |      |      |
| AbstractInvoker               |      |      |
| AbstractProtocol              |      |      |
| AbstractProxyProtocol         |      |      |
| AsyncToSyncInvoker            |      |      |
| InvokerWrapper                |      |      |
| ProtocolFilterWrapper         |      |      |
| ProtocolListenerWrapper       |      |      |



##### org.apache.dubbo.rpc.protocol.dubbo

| org.apache.dubbo.rpc.protocol.dubbo | 类型 |      |
| ----------------------------------- | ---- | ---- |
|                                     |      |      |
| 接口                                |      |      |
|                                     |      |      |
| Constants                           |      |      |
|                                     |      |      |
| 类                                  |      |      |
|                                     |      |      |
| DecodeableRpcInvocation             |      |      |
| DecodeableRpcResult                 |      |      |
| DubboCodec                          |      |      |
| DubboCountCodec                     |      |      |
| DubboExporter                       |      |      |
| DubboInvoker                        |      |      |
| DubboProtocol                       |      |      |
| DubboProtocolServer                 |      |      |
| FutureAdapter                       |      |      |



###### org.apache.dubbo.rpc.protocol.dubbo.filter

| org.apache.dubbo.rpc.protocol.dubbo.filter | 类型 |      |
| ------------------------------------------ | ---- | ---- |
| FutureFilter                               |      |      |
| TraceFilter                                |      |      |
|                                            |      |      |



###### org.apache.dubbo.rpc.protocol.dubbo.status

| org.apache.dubbo.rpc.protocol.dubbo.status | 类型 |      |
| ------------------------------------------ | ---- | ---- |
| ServerStatusChecker                        |      |      |
| ThreadPoolStatusChecker                    |      |      |
|                                            |      |      |



##### org.apache.dubbo.rpc.protocol.grpc

| org.apache.dubbo.rpc.protocol.grpc | 类型 |      |
| ------------------------------ | ---- | ---- |
|    DubboHandlerRegistry       |      |      |
|       GrpcConfig      |      |      |
|     GrpcConstants     |      |      |
|       GrpcInvoker   |      |      |
|       GrpcOptionsUtils    |      |      |
|         GrpcProtocol        |      |      |
|    ReferenceCountManagedChannel   |      |      |




###### org.apache.dubbo.rpc.protocol.grpc.interceptors

| org.apache.dubbo.rpc.protocol.grpc.interceptors | 类型 |      |
| ----------------------------------------------- | ---- | ---- |
| DubboHandlerRegistry                            |      |      |
| GrpcConfig                                      |      |      |
| GrpcConstants                                   |      |      |
| GrpcInvoker                                     |      |      |
| GrpcOptionsUtils                                |      |      |
| GrpcProtocol                                    |      |      |
| ReferenceCountManagedChannel                    |      |      |
类


##### org.apache.dubbo.rpc.protocol.hessian

| org.apache.dubbo.rpc.protocol.hessian | 类型 |      |
| ------------------------------ | ---- | ---- |
|                                |      |      |
|                                |      |      |
|                                |      |      |

接口
Constants
类
DubboHessianURLConnectionFactory
HessianProtocol
HttpClientConnection
HttpClientConnectionFactory
##### org.apache.dubbo.rpc.protocol.http

| org.apache.dubbo.rpc.protocol.http | 类型 |      |
| ------------------------------ | ---- | ---- |
|   Constants                             |  接口    |      |
|   DubboHessianURLConnectionFactory                             |      |      |
|     HessianProtocol                           |      |      |
|   HttpClientConnection               |      |      |
|   HttpClientConnectionFactory        |      |      |
|                                |      |      |






##### org.apache.dubbo.rpc.protocol.injvm

| org.apache.dubbo.rpc.protocol.injvm | 类型 |      |
| ------------------------------ | ---- | ---- |
|   InjvmProtocol           |      |      |
|                                |      |      |
|                                |      |      |


##### org.apache.dubbo.rpc.protocol.memcached

| org.apache.dubbo.rpc.protocol.memcached | 类型 |      |
| --------------------------------------- | ---- | ---- |
| MemcachedProtocol                       |      |      |
|                                         |      |      |
|                                         |      |      |


##### org.apache.dubbo.rpc.protocol.nativethrift

| org.apache.dubbo.rpc.protocol.nativethrift | 类型 |      |
| ------------------------------------------ | ---- | ---- |
| ThriftProtocol                             |      |      |
|                                            |      |      |
|                                            |      |      |


##### org.apache.dubbo.rpc.protocol.redis

| org.apache.dubbo.rpc.protocol.redis | 类型 |      |
| ------------------------------ | ---- | ---- |
|   RedisProtocol               |      |      |
|                                |      |      |
|                                |      |      |


##### org.apache.dubbo.rpc.protocol.rest

| org.apache.dubbo.rpc.protocol.rest | 类型 |      |
| ---------------------------------- | ---- | ---- |
|                                    |      |      |
| org.apache.dubbo.rpc.protocol.rest |      |      |
|                                    |      |      |
| 接口                               |      |      |
|                                    |      |      |
| Constants                          |      |      |
| RestProtocolServer                 |      |      |
|                                    |      |      |
| 类                                 |      |      |
|                                    |      |      |
| BaseRestProtocolServer             |      |      |
| DubboHttpProtocolServer            |      |      |
| DubboResourceFactory               |      |      |
| NettyRestProtocolServer            |      |      |
| RestConstraintViolation            |      |      |
| RestProtocol                       |      |      |
| RestServerFactory                  |      |      |
| RpcContextFilter                   |      |      |
| RpcExceptionMapper                 |      |      |
| ViolationReport                    |      |      |


###### org.apache.dubbo.rpc.protocol.rest.integration.swagger

| org.apache.dubbo.rpc.protocol.rest.integration.swagger | 类型 |      |
| ------------------------------------------------------ | ---- | ---- |
|                                                        |      |      |
|                                                        |      |      |
|                                                        |      |      |

接口
DubboSwaggerService
类
DubboSwaggerApiListingResource
###### org.apache.dubbo.rpc.protocol.rest.support

| org.apache.dubbo.rpc.protocol.rest.support | 类型 |      |
| ------------------------------------------ | ---- | ---- |
|                                            |      |      |
|                                            |      |      |
|                                            |      |      |

类
ContentType
LoggingFilter
##### org.apache.dubbo.rpc.protocol.rmi

| org.apache.dubbo.rpc.protocol.rmi | 类型 |      |
| ------------------------------ | ---- | ---- |
|                                |      |      |
|                                |      |      |
|                                |      |      |
类
RmiProtocol
RmiRemoteInvocation

##### org.apache.dubbo.rpc.protocol.thrift

| org.apache.dubbo.rpc.protocol.thrift | 类型 |      |
| ------------------------------------ | ---- | ---- |
|                                      |      |      |
| 接口                                 |      |      |
|                                      |      |      |
| ClassNameGenerator                   |      |      |
|                                      |      |      |
| 类                                   |      |      |
|                                      |      |      |
| DubboClassNameGenerator              |      |      |
| ThriftClassNameGenerator             |      |      |
| ThriftCodec                          |      |      |
| ThriftConstants                      |      |      |
| ThriftInvoker                        |      |      |
| ThriftNativeCodec                    |      |      |
| ThriftProtocol                       |      |      |
| ThriftUtils                          |      |      |
|                                      |      |      |
| 枚举                                 |      |      |
|                                      |      |      |
| ThriftType                           |      |      |


###### org.apache.dubbo.rpc.protocol.thrift.ext

| org.apache.dubbo.rpc.protocol.thrift.ext | 类型 |      |
| ---------------------------------------- | ---- | ---- |
|                                          |      |      |
|                                          |      |      |
|                                          |      |      |
org.apache.dubbo.rpc.protocol.thrift.ext
类
MultiServiceProcessor

###### org.apache.dubbo.rpc.protocol.thrift.io

| org.apache.dubbo.rpc.protocol.thrift.io | 类型 |      |
| --------------------------------------- | ---- | ---- |
|                                         |      |      |
|                                         |      |      |
|                                         |      |      |

类
InputStreamWrapper
RandomAccessByteArrayOutputStream
##### org.apache.dubbo.rpc.protocol.webservice

| org.apache.dubbo.rpc.protocol.webservice | 类型 |      |
| ---------------------------------------- | ---- | ---- |
|                                          |      |      |
|                                          |      |      |
|                                          |      |      |
类
WebServiceProtocol

#### org.apache.dubbo.rpc.proxy

| org.apache.dubbo.rpc.proxy | 类型 |      |
| ------------------------------ | ---- | ---- |
|                                |      |      |
|                                |      |      |
|                                |      |      |
类
AbstractProxyFactory
AbstractProxyInvoker
InvokerInvocationHandler

##### org.apache.dubbo.rpc.proxy.javassist

| org.apache.dubbo.rpc.proxy.javassist | 类型 |      |
| ------------------------------ | ---- | ---- |
|                                |      |      |
|                                |      |      |
|                                |      |      |
JavassistProxyFactory

##### org.apache.dubbo.rpc.proxy.jdk

| org.apache.dubbo.rpc.proxy.jdk | 类型 |      |
| ------------------------------ | ---- | ---- |
|                                |      |      |
|                                |      |      |
|                                |      |      |
JavassistProxyFactory

##### org.apache.dubbo.rpc.proxy.wrapper

| org.apache.dubbo.rpc.proxy.wrapper | 类型 |      |
| ------------------------------ | ---- | ---- |
|                                |      |      |
|                                |      |      |
|                                |      |      |
org.apache.dubbo.rpc.proxy.wrapper

#### org.apache.dubbo.rpc.service

| org.apache.dubbo.rpc.service | 类型 |      |
| ---------------------------- | ---- | ---- |
|                              |      |      |
| 接口                         |      |      |
|                              |      |      |
| Destroyable                  |      |      |
| EchoService                  |      |      |
| GenericService               |      |      |
|                              |      |      |
| 类                           |      |      |
|                              |      |      |
| EchoServiceDetector          |      |      |
| GenericServiceDetector       |      |      |
|                              |      |      |
| 异常错误                     |      |      |
|                              |      |      |
| GenericException             |      |      |



#### org.apache.dubbo.rpc.support

| org.apache.dubbo.rpc.support | 类型 |      |
| ---------------------------- | ---- | ---- |
|                              |      |      |
| 类                           |      |      |
|                              |      |      |
| AccessLogData                |      |      |
| GroupServiceKeyCache         |      |      |
| MockInvoker                  |      |      |
| MockProtocol                 |      |      |
| ProtocolUtils                |      |      |
| RpcUtils                     |      |      |








### org.apache.dubbo.serialize





| org.apache.dubbo.serialize | 类型 |      |
| ------------------------------ | ---- | ---- |
|                                |      |      |
|                                |      |      |
|                                |      |      |



#### org.apache.dubbo.serialize.hessian

| org.apache.dubbo.serialize.hessian | 类型 |      |
| ---------------------------------- | ---- | ---- |
| 类                                 |      |      |
|                                    |      |      |
| Hessian2ObjectInput                |      |      |
| Hessian2ObjectOutput               |      |      |
| Hessian2Serialization              |      |      |
| Hessian2SerializerFactory          |      |      |
| Java8SerializerFactory             |      |      |



###### org.apache.dubbo.serialize.hessian.serializer.java8

| org.apache.dubbo.serialize.hessian.serializer.java8 | 类型 |      |
| --------------------------------------------------- | ---- | ---- |
|                                                     |      |      |
| 类                                                  |      |      |
|                                                     |      |      |
| DurationHandle                                      |      |      |
| InstantHandle                                       |      |      |
| Java8TimeSerializer                                 |      |      |
| LocalDateHandle                                     |      |      |
| LocalDateTimeHandle                                 |      |      |
| LocalTimeHandle                                     |      |      |
| MonthDayHandle                                      |      |      |
| OffsetDateTimeHandle                                |      |      |
| OffsetTimeHandle                                    |      |      |
| PeriodHandle                                        |      |      |
| YearHandle                                          |      |      |
| YearMonthHandle                                     |      |      |
| ZonedDateTimeHandle                                 |      |      |
| ZoneIdHandle                                        |      |      |
| ZoneIdSerializer                                    |      |      |
| ZoneOffsetHandle                                    |      |      |






### org.apache.dubbo.validation




| org.apache.dubbo.validation | 类型 |      |
| ------------------------------ | ---- | ---- |
|    MethodValidated            |   @interface  |      |
|   Validation             |  interface   |      |
|   Validator             | interface   |      |


#### org.apache.dubbo.validation.filter

| org.apache.dubbo.validation.filter | 类型 |      |
| ------------------------------ | ---- | ---- |
|    ValidationFilter          |      |      |
|                                |      |      |
|                                |      |      |


#### org.apache.dubbo.validation.support

| org.apache.dubbo.validation.support | 类型 |      |
| ------------------------------ | ---- | ---- |
|    AbstractValidation              | abstract |      |
|                                |      |      |
|                                |      |      |


##### org.apache.dubbo.validation.support.jvalidation



| org.apache.dubbo.validation.support.jvalidation | 类型 |      |
| ----------------------------------------------- | ---- | ---- |
| JValidation                                     |      |      |
| JValidator                                      |      |      |
|                                                 |      |      |



### org.apache.dubbo.xml







#### org.apache.dubbo.xml.rpc.protocol.xmlrpc





| org.apache.dubbo.xml.rpc.protocol.xmlrpc | 类型 |      |
| ---------------------------------------- | ---- | ---- |
| XmlRpcProtocol                           |      |      |
| XmlRpcProtocol.InternalHandler           |      |      |
|                                          |      |      |
|                                          |      |      |
|                                          |      |      |

