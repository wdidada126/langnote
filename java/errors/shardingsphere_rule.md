# shardingsphere



```java
Exception in thread "main" org.mybatis.spring.MyBatisSystemException: nested exception is org.apache.ibatis.exceptions.PersistenceException: 
### Error updating database.  Cause: io.shardingsphere.core.exception.ShardingConfigurationException: Cannot find table rule and default data source with logic table: 't_blog'
### The error may exist in META-INF/mappers/BlogMapper.xml
### The error may involve defaultParameterMap
### The error occurred while setting parameters
### SQL: CREATE TABLE IF NOT EXISTS t_blog (id BIGINT NOT NULL AUTO_INCREMENT primary key, title varchar(200) NOT NULL, typeId INT NOT NULL);
### Cause: io.shardingsphere.core.exception.ShardingConfigurationException: Cannot find table rule and default data source with logic table: 't_blog'
	at org.mybatis.spring.MyBatisExceptionTranslator.translateExceptionIfPossible(MyBatisExceptionTranslator.java:77)
	at org.mybatis.spring.SqlSessionTemplate$SqlSessionInterceptor.invoke(SqlSessionTemplate.java:446)
	at com.sun.proxy.$Proxy48.update(Unknown Source)
	at org.mybatis.spring.SqlSessionTemplate.update(SqlSessionTemplate.java:294)
	at org.apache.ibatis.binding.MapperMethod.execute(MapperMethod.java:64)
	at org.apache.ibatis.binding.MapperProxy.invoke(MapperProxy.java:58)
	at com.sun.proxy.$Proxy49.createTableIfNotExists(Unknown Source)
	at io.shardingsphere.example.repository.api.service.CommonBlogServiceImpl.initEnvironment(CommonBlogServiceImpl.java:12)
	at io.shardingsphere.example.spring.boot.mybatis.orche.SpringBootStarterExample.process(SpringBootStarterExample.java:47)
	at io.shardingsphere.example.spring.boot.mybatis.orche.SpringBootStarterExample.main(SpringBootStarterExample.java:40)
Caused by: org.apache.ibatis.exceptions.PersistenceException: 
### Error updating database.  Cause: io.shardingsphere.core.exception.ShardingConfigurationException: Cannot find table rule and default data source with logic table: 't_blog'
### The error may exist in META-INF/mappers/BlogMapper.xml
### The error may involve defaultParameterMap
### The error occurred while setting parameters
### SQL: CREATE TABLE IF NOT EXISTS t_blog (id BIGINT NOT NULL AUTO_INCREMENT primary key, title varchar(200) NOT NULL, typeId INT NOT NULL);
### Cause: io.shardingsphere.core.exception.ShardingConfigurationException: Cannot find table rule and default data source with logic table: 't_blog'
	at org.apache.ibatis.exceptions.ExceptionFactory.wrapException(ExceptionFactory.java:30)
	at org.apache.ibatis.session.defaults.DefaultSqlSession.update(DefaultSqlSession.java:200)
	at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
	at sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)
	at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
	at java.lang.reflect.Method.invoke(Method.java:498)
	at org.mybatis.spring.SqlSessionTemplate$SqlSessionInterceptor.invoke(SqlSessionTemplate.java:433)
	... 8 more
Caused by: io.shardingsphere.core.exception.ShardingConfigurationException: Cannot find table rule and default data source with logic table: 't_blog'
	at io.shardingsphere.core.rule.ShardingRule.getTableRuleByLogicTableName(ShardingRule.java:137)
	at io.shardingsphere.core.routing.type.broadcast.TableBroadcastRoutingEngine.getAllTableUnits(TableBroadcastRoutingEngine.java:80)
	at io.shardingsphere.core.routing.type.broadcast.TableBroadcastRoutingEngine.route(TableBroadcastRoutingEngine.java:56)
	at io.shardingsphere.core.routing.router.sharding.ParsingSQLRouter.route(ParsingSQLRouter.java:154)
	at io.shardingsphere.core.routing.router.sharding.ParsingSQLRouter.route(ParsingSQLRouter.java:113)
	at io.shardingsphere.core.routing.PreparedStatementRoutingEngine.route(PreparedStatementRoutingEngine.java:66)
	at io.shardingsphere.shardingjdbc.jdbc.core.statement.ShardingPreparedStatement.sqlRoute(ShardingPreparedStatement.java:229)
	at io.shardingsphere.shardingjdbc.jdbc.core.statement.ShardingPreparedStatement.execute(ShardingPreparedStatement.java:137)
	at org.apache.ibatis.executor.statement.PreparedStatementHandler.update(PreparedStatementHandler.java:47)
	at org.apache.ibatis.executor.statement.RoutingStatementHandler.update(RoutingStatementHandler.java:74)
	at org.apache.ibatis.executor.SimpleExecutor.doUpdate(SimpleExecutor.java:50)
	at org.apache.ibatis.executor.BaseExecutor.update(BaseExecutor.java:117)
	at org.apache.ibatis.executor.CachingExecutor.update(CachingExecutor.java:76)
	at org.apache.ibatis.session.defaults.DefaultSqlSession.update(DefaultSqlSession.java:198)
	... 13 more
```
