# Druid

## 功能
查看执行的sql
查看慢sql
web查看


## log
com.alibaba.druid.support.logging.LogFactory

## 核心类

```shell
	at com.mysql.jdbc.StatementImpl.executeQuery(StatementImpl.java:1369)
	at com.alibaba.druid.filter.FilterChainImpl.statement_executeQuery(FilterChainImpl.java:2883)
	at com.alibaba.druid.filter.FilterAdapter.statement_executeQuery(FilterAdapter.java:2514)
	at com.alibaba.druid.filter.FilterEventAdapter.statement_executeQuery(FilterEventAdapter.java:302)
	at com.alibaba.druid.filter.FilterChainImpl.statement_executeQuery(FilterChainImpl.java:2880)
	at com.alibaba.druid.filter.FilterAdapter.statement_executeQuery(FilterAdapter.java:2514)
	at com.alibaba.druid.filter.FilterEventAdapter.statement_executeQuery(FilterEventAdapter.java:302)
	at com.alibaba.druid.filter.FilterChainImpl.statement_executeQuery(FilterChainImpl.java:2880)
	at com.alibaba.druid.proxy.jdbc.StatementProxyImpl.executeQuery(StatementProxyImpl.java:221)
	at com.alibaba.druid.pool.DruidPooledStatement.executeQuery(DruidPooledStatement.java:297)
	at org.springframework.jdbc.core.JdbcTemplate$1QueryStatementCallback.doInStatement(JdbcTemplate.java:439)
```

## spring boot druid多数据源

https://gitee.com/edidada/testspringbootdruid

Springboot+Druid配置多数据源
https://blog.csdn.net/Mr_ming_a_probie/article/details/127920120


druid-spring-boot-starter

durild核心类 DruidDataSource

starter类
DruidDataSourceWrapper

配置文件
DataSourceProperties

自动装配类
DruidDataSourceAutoConfigure


## 分package源代码详解 v1.1.22


### com.alibaba.druid.pool

| com.alibaba.druid.pool |      |      |
| ---------------------------------- | ---- | ---- |
|      DruidDataSource            |      |      |


### com.alibaba.druid.support

| com.alibaba.druid.support.spring.stat.config |      |      |
| ---------------------------------- | ---- | ---- |
|      DruidStatNamespaceHandler            |      |      |


https://github.com/alibaba/druid