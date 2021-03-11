# shardingsphere





vitess 竞品

amoeba 竞品
dble https://github.com/actiontech/dble
mycat
sqlproxy https://github.com/sysown/proxysql
https://www.cnblogs.com/f-ck-need-u/p/9300829.html


DBCP，C3P0，Druid, HikariCP 数据库连接池

支持读写分离



5.0 快照版



```shell
Exception in thread "main" org.springframework.beans.factory.xml.XmlBeanDefinitionStoreException: Line 55 in XML document from class path resource [META-INF/nacos/local/application-sharding-databases-tables.xml] is invalid; nested exception is org.xml.sax.SAXParseException; lineNumber: 55; columnNumber: 127; cvc-complex-type.2.4.c: 通配符的匹配很全面, 但无法找到元素 'sharding:inline-strategy' 的声明。
	at org.springframework.beans.factory.xml.XmlBeanDefinitionReader.doLoadBeanDefinitions(XmlBeanDefinitionReader.java:399)
	at org.springframework.beans.factory.xml.XmlBeanDefinitionReader.loadBeanDefinitions(XmlBeanDefinitionReader.java:336)
	at org.springframework.beans.factory.xml.XmlBeanDefinitionReader.loadBeanDefinitions(XmlBeanDefinitionReader.java:304)
	at org.springframework.beans.factory.support.AbstractBeanDefinitionReader.loadBeanDefinitions(AbstractBeanDefinitionReader.java:181)
	at org.springframework.beans.factory.support.AbstractBeanDefinitionReader.loadBeanDefinitions(AbstractBeanDefinitionReader.java:217)
	at org.springframework.beans.factory.support.AbstractBeanDefinitionReader.loadBeanDefinitions(AbstractBeanDefinitionReader.java:188)
	at org.springframework.beans.factory.support.AbstractBeanDefinitionReader.loadBeanDefinitions(AbstractBeanDefinitionReader.java:252)
	at org.springframework.context.support.AbstractXmlApplicationContext.loadBeanDefinitions(AbstractXmlApplicationContext.java:127)
	at org.springframework.context.support.AbstractXmlApplicationContext.loadBeanDefinitions(AbstractXmlApplicationContext.java:93)
	at org.springframework.context.support.AbstractRefreshableApplicationContext.refreshBeanFactory(AbstractRefreshableApplicationContext.java:129)
	at org.springframework.context.support.AbstractApplicationContext.obtainFreshBeanFactory(AbstractApplicationContext.java:614)
	at org.springframework.context.support.AbstractApplicationContext.refresh(AbstractApplicationContext.java:515)
	at org.springframework.context.support.ClassPathXmlApplicationContext.<init>(ClassPathXmlApplicationContext.java:139)
	at org.springframework.context.support.ClassPathXmlApplicationContext.<init>(ClassPathXmlApplicationContext.java:83)
	at org.apache.shardingsphere.example.orchestration.spring.namespace.ExampleMain.main(ExampleMain.java:42)
Caused by: org.xml.sax.SAXParseException; lineNumber: 55; columnNumber: 127; cvc-complex-type.2.4.c: 通配符的匹配很全面, 但无法找到元素 'sharding:inline-strategy' 的声明。
	at com.sun.org.apache.xerces.internal.util.ErrorHandlerWrapper.createSAXParseException(ErrorHandlerWrapper.java:203)
	at com.sun.org.apache.xerces.internal.util.ErrorHandlerWrapper.error(ErrorHandlerWrapper.java:134)
	at com.sun.org.apache.xerces.internal.impl.XMLErrorReporter.reportError(XMLErrorReporter.java:396)
	at com.sun.org.apache.xerces.internal.impl.XMLErrorReporter.reportError(XMLErrorReporter.java:327)
	at com.sun.org.apache.xerces.internal.impl.XMLErrorReporter.reportError(XMLErrorReporter.java:284)
	at com.sun.org.apache.xerces.internal.impl.xs.XMLSchemaValidator$XSIErrorReporter.reportError(XMLSchemaValidator.java:453)
	at com.sun.org.apache.xerces.internal.impl.xs.XMLSchemaValidator.reportSchemaError(XMLSchemaValidator.java:3231)
	at com.sun.org.apache.xerces.internal.impl.xs.XMLSchemaValidator.handleStartElement(XMLSchemaValidator.java:1912)
	at com.sun.org.apache.xerces.internal.impl.xs.XMLSchemaValidator.emptyElement(XMLSchemaValidator.java:761)
	at com.sun.org.apache.xerces.internal.impl.XMLNSDocumentScannerImpl.scanStartElement(XMLNSDocumentScannerImpl.java:351)
	at com.sun.org.apache.xerces.internal.impl.XMLDocumentFragmentScannerImpl$FragmentContentDriver.next(XMLDocumentFragmentScannerImpl.java:2784)
	at com.sun.org.apache.xerces.internal.impl.XMLDocumentScannerImpl.next(XMLDocumentScannerImpl.java:602)
	at com.sun.org.apache.xerces.internal.impl.XMLNSDocumentScannerImpl.next(XMLNSDocumentScannerImpl.java:112)
	at com.sun.org.apache.xerces.internal.impl.XMLDocumentFragmentScannerImpl.scanDocument(XMLDocumentFragmentScannerImpl.java:505)
	at com.sun.org.apache.xerces.internal.parsers.XML11Configuration.parse(XML11Configuration.java:842)
	at com.sun.org.apache.xerces.internal.parsers.XML11Configuration.parse(XML11Configuration.java:771)
	at com.sun.org.apache.xerces.internal.parsers.XMLParser.parse(XMLParser.java:141)
	at com.sun.org.apache.xerces.internal.parsers.DOMParser.parse(DOMParser.java:243)
	at com.sun.org.apache.xerces.internal.jaxp.DocumentBuilderImpl.parse(DocumentBuilderImpl.java:339)
	at org.springframework.beans.factory.xml.DefaultDocumentLoader.loadDocument(DefaultDocumentLoader.java:76)
	at org.springframework.beans.factory.xml.XmlBeanDefinitionReader.doLoadDocument(XmlBeanDefinitionReader.java:429)
	at org.springframework.beans.factory.xml.XmlBeanDefinitionReader.doLoadBeanDefinitions(XmlBeanDefinitionReader.java:391)
	... 14 more
```







http://www.iocoder.cn/Sharding-JDBC/sql-parse-1/?github&1602

1.5版本的ss







ORCHESTRATE WORKLOADS是什么？
这是orchestration的使用场景。与“container”不同，“orchestration”这个词完美地描述了Kubernetes所扮演的角色。虽然有些人已经用乐队指挥来说明这个概念，但是在音乐和分布式应用中，指挥家和orchestrator之间存在着很大的区别。orchestration的行为为单个应用程序提供了协同工作的模式，就像乐队中的乐器一样。当作曲家创作出软件的原始模式，包括它的旋律线条和节奏（组装一个软件容器的术语实际上是作曲）时，管弦乐师会让乐曲听起来。

“这就是为什么我称Kubernetes为‘可组合的平台’的原因，”在最近一次公司网络研讨会上，Red Hat的产品策略总监Brian Gracely解释道。“它应该是什么样子，有某种框架——其中一些来自Kubernetes社区，一些来自社区多年的经验，关于如何部署应用程序。”

orchestrator的主要工作是在其信任下维护应用程序的运行状态。在另一个时代，这项工作被委托给了操作系统。但那时候，这个平台还是一个只有一个存储库和专用存储设备的处理器。现在，没有什么东西可以将容器化的服务与应用程序的更广泛的上下文关联起来。实际上，协调器获取所有这些服务的功能和工作产品，通过某种形式的manifest来组织它们，并提供某种应用程序的外观。更改manifest，您可能会得到一个完全不同的应用程序。
180703-red-hat-kubernetes-diagram.jpg

Kubernetes与其他类型的应用程序在结构上没有区别。它不是虚拟机。它的orchestrator 在操作系统上运行。在运行时，它维护一个节点集群，这是引用物理或虚拟服务器的一种更抽象的方式。每个节点上都有容器的pods 。在它们的每个内部都有一个称为kubelet的客户端代理，它代表orchestrator 独立地管理分配给它的节点的函数。但即便如此，这也是一个和其他项目一样的项目。

所以Kubernetes不像Hadoop，它真正地重构了在服务器上运行的应用程序的结构。尽管如此，orchestrator 带来的分布式模型与2016年之前流行的模型有很大不同。部署模式不会随着时代而改变，比如时尚方向、个人口味或政治取向等。如果我们诚实的话，Kubernetes的突然崛起并不是因为世界上所有企业突然意识到需要在云计算中加入一些应用程序。Kubernetes是谷歌需要在数万个节点上管理其全局可访问的workloads的产物。世界上很少有其他组织类似于谷歌，或者拥有谷歌的数据中心概要。并不是每家公司都有自己的搜索引擎——如果你仔细想想，这就是谷歌存在的原因。
分布式系统的吸引力
那么，为什么Kubernetes或container orchestration对企业这么大吸引力呢?它真正吸引人的原因与workloads 本身无关，更多的是与围绕它们的开发和部署模型有关:
连续性——当应用程序由粒度组件组成时，通过单独更新和改进这些组件，应用程序就更容易按粒度演进。协调器可以根据各个更改对整体workloads的影响做出适当的调整。应用程序的特性改进不再需要在大规模的检修中实现——这通常会对其可用性产生负面影响。持续集成和持续交付的概念(CI/CD，“D”通常表示“部署”)可以通过一个平台更容易地实现自动化，这个平台从一开始就被设计成理解部署本身的更小、更易于管理的步骤。
弹性——Kubernetes维护容器组的活动副本(称为replica
sets)，目的是为了在任何容器或容器分组(Kubernetes称之为pod)失败时保持正常运行时间和响应能力。这意味着数据中心不必复制整个应用程序，并触发负载均衡器，以便在主应用程序失败时切换到辅助应用程序。实际上，复制集中的多个pod通常在任何时候都在运行，协调器的工作是在应用程序的整个生命周期中保持这种多元性。
可伸缩性——对于使用Kubernetes协调分布式workloads的组织来说，最大的好处是，根据预先设置的策略，workloads 可以在系统中按需成倍增长，从而再次进行伸缩。为了减少混乱的可能性，Kubernetes把相关的容器组合成一个pod。可以将名为autoscaler的服务设置为自动将pods复制到不同节点，因为它确定分配给这些pods的资源没有得到尽可能多的利用。
KUBERNETES 是平台，还是其他什么？
到底Kubernetes和VMware vSphere谁是平台，仍然存在一些不确定性。不可否认，Kubernetes是一个“引擎”，是为分布式软件系统提供动力的主要元素。然而，Kubernetes并不提供这些元素本身，正如Windows的前辈MS-DOS最初并不提供自己的硬盘优化器或备份过程一样。

但正如许多用户会断言的那样，Kubernetes是一个平台的中心，这个平台可以由任意数量的能够协同工作的服务组成。有人说今天的CNCF是维护的目的,整理和培养其他独立的多元性,开源项目——例如,监控系统,如Prometheus,日志数据经理如Fluentd(不是一个错字),和信任的内容的身份验证器等公证,可能共同组成一个平台。在撰写本文时，CNCF已经认证了59个发行版，其中许多都是商业发行版，其中包括协调器以及其他CNCF工具或其供应商自己的工具。

“你会发现Kubernetes没有提供所有这些东西，”Red Hat优雅地说。“他们都是地方社区,通过不同的供应商,通过开源插件项目,给予市场很多的选择,给他们选择,让他们可插入性为这些不同的元素,并允许公司最终决定,在这个更广泛的框架,如何构建最好的平台,我们想做什么,为我们挑选最好的有意义的部分,但仍拥有一切的互操作性和可支持的?”

然而，正如Gracely的评论本身所表明的那样，由于这些集合的任何一个产品都无疑是一个平台，而Kubernetes是其中心的推动者，那么所有这些结果都应该是“Kubernetes平台”。Red Hat的OpenShift就是一个突出的例子，还有最新2.0版本的Rancher。






tps高的应用，使用ss后，启动慢

因为要预解析sql



[sharding-jdbc之ANTLR4 SQL解析]( https://www.liangzl.com/get-article-detail-142604.html )



AddColumnDefinitionExtractor



解析sql语句的语法是

ast

org.antlr.v4.runtime.tree.ParseTree

grammarName_Lexer
grammarName_Parser



```
antlr-v4-grammar-plugin idea插件，有图形界面Java grammar viewhttps://www.crifan.com/antlr_v3_syntax_fragment/
```



### opentracing



不同编程语言实现

https://opentracing.io/registry/




### Mockito



Meituan-Dianping Zebra  ss竞品

#### jta

<dependency>
    <groupId>javax.transaction</groupId>
    <artifactId>jta</artifactId>
    <version>1.1</version>
</dependency>



io.shardingsphere:sharding-jdbc

ss版本
Apache官方发布从4.0.0版本开始
3.1.0	04-Jan-2019
3.1.0.M1	19-Dec-2018
‎3.0.0	23-Oct-2018
‎3.0.0.M4	28-Sep-2018
3.0.0.M3	05-Sep-2018
3.0.0.M2	08-Aug-2018
‎3.0.0.M1	21-May-2018


### issure 3813
Oracle all syntax
   INSERT ALL

        into order_info_1 (
    				ORDER_ID,
        ORDER_PRICE,
        ORDER_INVENTORY)
        VALUES
        (11,1,2)
    into order_info_1 (
    				ORDER_ID,
        ORDER_PRICE,
        ORDER_INVENTORY)
        VALUES
        (12,1,2)
    SELECT 1 FROM DUAL
ss版本4.0 RC 1

#### 路线图
ROADMAP.md
Sharding-JDBC-ROADMAP.md


#### 功能

###### 数据分片
- 分库 & 分表
- 读写分离
- 分片策略定制化
- 无中心化分布式主键

###### 分布式事务
-标准化事务接口
- XA强一致事务
- 柔性事务


###### 数据库治理
配置动态化
编排 & 治理
数据脱敏
可视化链路追踪
弹性伸缩(规划中)



分享从当今分布式数据库所关注的6大重点（分布式存储、计算存储分离、分布式事务、弹性伸缩、多数据副本、HTAP）切入主题，重点阐述了Apache ShardingSphere在数据分片、分布式事务、弹性伸缩和分布式治理的方面的核心功能，以及如何使用Apache ShardingSphere搭建分布式数据库生态。其中，在受到广泛关注的分布式事务部分，重点介绍了京东数科自研的高性能分布式事务中间件JDTX解决方案。在探讨Apache ShardingSphere的未来规划时，可插拔架构、SQL兼容度提升、多数据副本、云原生和多元数据融合平台等几方面话题成为了关注的重点。分享的尾声着重介绍了如何参与和回馈Apache ShardingSphere社区，期待对开源感兴趣的小伙伴能够越来越多的参与到社区建设中。

https://zhuanlan.zhihu.com/p/93984576


#### git操作

git remote -v
github  git@github.com:apache/incubator-shardingsphere.git (fetch)
github  git@github.com:apache/incubator-shardingsphere.git (push)
origin  git@github.com:edidada/incubator-shardingsphere.git (fetch)
origin  git@github.com:edidada/incubator-shardingsphere.git (push)

git branch -a
git checkout dev
git branch -a
git fetch github
git merge github/dev
git push origin dev

#### issues 3572

使用proxy时，SELECT COUNT(*) FROM information_schema.TABLES

#### ss使用的三方库


#### yaml

snakeyyaml这个库来解析


原理：java bean直接序列化到yaml文件
yaml文件直接逆序列化到java bean

类比：json Gson


github.com/edidada/testyaml


org.apache.shardingsphere.shardingjdbc.api.yaml.YamlEncryptDataSourceFactory
org.apache.shardingsphere.core.yaml.engine.DefaultYamlRepresenter

对应的java bean类
YamlRootEncryptRuleConfiguration


ss配置文件
YamlConfiguration
YamlRootEncryptRuleConfiguration

### log

日志使用：slf4j和logback-class

sharding 3.0 4.0版本，对应的xsd文件不一样 dubbo也有类似的问题


springboot-shardingJDBC 使用Spring Boot + Sharding-JDBC 快速简单地实现数据库读写分离

zk在ss中的作用是？
orchestration中要用
存储配置数据，相当于配置中心
shardingsphere 2.0添加的


ShardingSphere官网操作指南补充和重点整理-分布式事务-参考示例（十二）
https://blog.csdn.net/penker_zhao/article/details/100934123

XA事务管理器参数配置（可选）
ShardingSphere默认的XA事务管理器为Atomikos，在项目的logs目录中会生成xa_tx.log, 这是XA崩溃恢复时所需的日志，请勿删除。
也可以通过在项目的classpath中添加jta.properties来定制化Atomikos配置项。具体的配置规则请参考Atomikos的官方文档。
原文链接：https://blog.csdn.net/penker_zhao/article/details/100934123



ShardingProxy
Sharding-Sidecar

1.0



### yaml

snakeyaml


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



![ss 架构](imgs/ss_architect.png)
