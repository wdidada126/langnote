# spring-data-redis



```xml
		<dependency>
			<groupId>org.springframework.data</groupId>
			<artifactId>spring-data-redis</artifactId>
		</dependency>

```

https://docs.spring.io/spring-data/commons/docs/current/api/

https://docs.spring.io/spring-data/commons/docs/2.3.4.RELEASE/api/

https://docs.spring.io/spring-data/redis/docs/2.3.4.RELEASE/api/

https://docs.spring.io/spring-data/jpa/docs/current/api/org/springframework/data/jpa/repository/JpaRepository.html



org.springframework.data.redis
Root package for integrating Redis with Spring concepts.

org.springframework.data.redis.config



|      |      |      |
| ---- | ---- | ---- |
|      |      |      |
|      |      |      |
|      |      |      |


org.springframework.data.redis.cache
Package providing a Redis implementation for Spring cache abstraction.

|      |      |      |
| ---- | ---- | ---- |
|      |      |      |
|      |      |      |
|      |      |      |

org.springframework.data.redis.connection
Connection package providing low-level abstractions for interacting with the various Redis 'drivers'/libraries.


org.springframework.data.redis.connection.convert
Redis specific converters used for sending data and parsing responses.


org.springframework.data.redis.connection.jedis
Connection package for Jedis library.


org.springframework.data.redis.connection.lettuce
Connection package for Lettuce Redis client.


org.springframework.data.redis.connection.stream
Data structures and interfaces to interact with Redis Streams.


org.springframework.data.redis.connection.util
Internal utility package for encoding/decoding Strings to byte[] (using Base64) library.


org.springframework.data.redis.core
Core package for integrating Redis with Spring concepts.


org.springframework.data.redis.core.convert
Converters for Redis repository support utilizing mapping metadata.


org.springframework.data.redis.core.index
Abstractions for Redis secondary indexes.


org.springframework.data.redis.core.mapping
Redis specific repository support mapping meta information.


org.springframework.data.redis.core.query
Query package for Redis template.


org.springframework.data.redis.core.script
Lua script execution abstraction.


org.springframework.data.redis.core.types
Redis domain specific types.


org.springframework.data.redis.hash
Dedicated support package for Redis hashes.


org.springframework.data.redis.listener
Base package for Redis message listener / pubsub container facility


org.springframework.data.redis.listener.adapter
Message listener adapter package.


org.springframework.data.redis.repository.cdi
CDI support for Redis specific repository implementation.


org.springframework.data.redis.repository.configuration
Redis repository specific configuration and bean registration.

org.springframework.data.redis.repository.core
Core domain entities for repository support.

org.springframework.data.redis.repository.query
Redis specific query execution engine.


org.springframework.data.redis.repository.support
Spring context specific factory support.


org.springframework.data.redis.serializer
Serialization/Deserialization package for converting Object to (and from) binary data.


org.springframework.data.redis.stream 


org.springframework.data.redis.support.atomic
Small toolkit mirroring the java.util.atomic package in Redis.

org.springframework.data.redis.support.collections
Package providing implementations for most of the java.util collections on top of Redis.


org.springframework.data.redis.util
Commonly used stuff for data manipulation throughout different driver specific implementations.