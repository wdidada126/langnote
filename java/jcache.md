# jcache



JCache (JSR-107)

classpath下存在javax.cache.spi.CachingProvider（比如，一个遵循JSR-107的缓存library），则JCache将启动。这里有很多遵循JSR-107的libraries，Spring Boot为Ehcache 3, Hazelcast和Infinispan提供依赖管理，其他library也可以像这样添加。

