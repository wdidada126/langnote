# shardingsphere

三方框架
- junit 测试框架
- hamcrest junit依赖项 可以单独引入hamcrest library，maven scope test compile
- lombok 减少代码量 get set constructor toString()

测试shardingsphere的jdk环境必须是jdk 1.7 1.8

jdk11运行本项目测试用例 报错

`Error:java: java.lang.ExceptionInInitializerError`

有投票是否支持其他jdk版本

测试用例warn jdk1.8
Java HotSpot(TM) 64-Bit Server VM warning: ignoring option MaxPermSize=256m; support was removed in 8.0

io.shardingsphere.api.AllApiTests
io.shardingsphere.core.AllCoreTests

测试例子全部跑通

手册：https://shardingsphere.apache.org/document/current/cn/manual/

看javadoc api






《未来架构：从服务化到云原生》读书笔记

预售书籍
第10章

MYSQL之笛卡尔积
https://blog.csdn.net/csdn_hklm/article/details/78394412

分布式事务

查看Java配置
javax.sql.DataSource


io.shardingsphere.api.config.ShardingRuleConfiguration  //分区策略
io.shardingsphere.api.config.TableRuleConfiguration  //表分区策略

```java
        TableRuleConfiguration result = new TableRuleConfiguration();
        result.setLogicTable("t_order");
        result.setKeyGeneratorColumnName("order_id");
```

dbcp数据库连接池
org.apache.commons.dbcp.BasicDataSource

io.shardingsphere.api.config.strategy.ShardingStrategyConfiguration
接口
实现类
- io.shardingsphere.api.config.strategy.ComplexShardingStrategyConfiguration
- io.shardingsphere.api.config.strategy.HintShardingStrategyConfiguration
- InlineShardingStrategyConfiguration
- StandardShardingStrategyConfiguration
- NoneShardingStrategyConfiguration
标准

其中，InlineShardingStrategyConfiguration(String shardingColumn, String algorithmExpression)

ss自己实现的DataSource
io.shardingsphere.shardingjdbc.jdbc.core.datasource.ShardingDataSource

ShardingDataSource类继承关系图
ShardingDataSource.png

ss有哪些jar包，分别是什么作用，如果要实现分库？
目前是用一个Map维护分库id和mysql：//***/databasename的键值对

工作内容：

- subquery
- case when


java.util.Properties
ShardingProperties(final Properties props)

io.shardingsphere.core.constant.properties.ShardingProperties

io.shardingsphere.core.constant.DatabaseType


ConnectionMode是enum，MEMORY_STRICTLY, CONNECTION_STRICTLY

java jdbc的代码，在哪儿实现的查询？
分库，如何整理数据

ShardingDatabasesConfiguration


ShardingDataSource

    @Override
    public final ShardingConnection getConnection() {
        return new ShardingConnection(dataSourceMap, shardingContext);
    }


​	
ShardingConnection

AbstractConnectionAdapter
Connection getConnection(final String dataSourceName) 
List<Connection> getConnections(final ConnectionMode connectionMode, final String dataSourceName, final int connectionSize)

ShardingConnection
createStatement()

io.shardingsphere.shardingjdbc.jdbc.core.statement.ShardingStatement

ShardingStatement

statement int executeUpdate(String sql)


io.shardingsphere.shardingjdbc.jdbc.core.resultset.ShardingResultSet

三层
io.shardingsphere.shardingjdbc.jdbc.unsupported
io.shardingsphere.shardingjdbc.jdbc.adapter

io.shardingsphere.core.routing.StatementRoutingEngine
SQLRouteResult route(final String logicSQL)

DataSourceMetaData接口
MySQLDataSourceMetaData

ShardingRouter接口
实现类
DatabaseHintSQLRouter
ParsingSQLRouter

SQLType枚举
DQL
DML

SQLToken 抽象类

官方文档
https://shardingsphere.apache.org/document/legacy/3.x/document/cn/overview/


垂直拆分
水平拆分
逻辑表

订单数据根据主键尾数拆分为10张表，分别是t_order_0到t_order_9，他们的逻辑表名为t_order

数据节点
数据分片的最小单元。由数据源名称和数据表组成，例：ds_0.t_order_0

绑定表
指分片规则一致的主表和子表。例如：t_order表和t_order_item表，均按照order_id分片，则此两张表互为绑定表关系

广播表



分片算法
通过分片算法将数据分片，支持通过=、BETWEEN和IN分片。分片算法需要应用方开发者自行实现，可实现的灵活度非常高。
目前提供4种分片算法。由于分片算法和业务实现紧密相关，因此并未提供内置分片算法，而是通过分片策略将各种场景提炼出来，提供更高层级的抽象，并提供接口让应用开发者自行实现分片算法。
精确分片算法
对应PreciseShardingAlgorithm，用于处理使用单一键作为分片键的=与IN进行分片的场景。需要配合StandardShardingStrategy使用。
范围分片算法
对应RangeShardingAlgorithm，用于处理使用单一键作为分片键的BETWEEN AND进行分片的场景。需要配合StandardShardingStrategy使用。
复合分片算法
对应ComplexKeysShardingAlgorithm，用于处理使用多键作为分片键进行分片的场景，包含多个分片键的逻辑较复杂，需要应用开发者自行处理其中的复杂度。需要配合ComplexShardingStrategy使用。
Hint分片算法
对应HintShardingAlgorithm，用于处理使用Hint行分片的场景。需要配合HintShardingStrategy使用。

DQL、DML、DDL、DCL、TCL、MySQL的DAL



源码

io.shardingsphere.core.constant.properties.ShardingPropertiesConstant


guava

Optional


源码

ShardingDataSourceNames
public String getDefaultDataSourceName()

ShardingRule

dataSourceNames是数据库的名称
public ShardingRule(final ShardingRuleConfiguration shardingRuleConfig, final Collection<String> dataSourceNames)

ShardingDataSourceFactory
创建ShardingDataSource

io.shardingsphere.api.algorithm.sharding.ShardingValue

ShardingPreparedStatement
PreparedStatementRoutingEngine


文档
limit 1000 10的实现，优化

多看官方文档
