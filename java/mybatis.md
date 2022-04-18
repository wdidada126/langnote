# mybatis


MyBatisCodeHelperPro idea插件


[springboot打印mybatis的sql语句](https://blog.csdn.net/qq_41345773/article/details/90178017)

https://www.cnblogs.com/huxiaoguang/p/10808967.html
在Mybatis已经整合到springBoot框架的情况下，只需要在配置文件中简单配置就能实现打印SQL日志功能。
如果使用的是application.properties文件，加入如下配置：



logging.level.main.blog.mapper=debug
如果使用的是application.yml文件，加入如下配置：

#开启logging myabtis语句打印
logging:
  level:
    main.blog.mapper: trace



[Mybatis 常用注解中的 SQL 注入](https://xie.infoq.cn/article/faf450b18559278a0ec051661)



- @SelectProvider

- @InsertProvider

- @UpdateProvider

- @DeleteProvider

  

mybatis 的动态sql语句是基于OGNL表达式的。可以方便的在 sql 语句中实现某些逻辑.

mybatis 的动态sql语句是基于OGNL表达式的。可以方便的在 sql 语句中实现某些逻辑.

mybatis 的动态sql语句是基于OGNL表达式的。可以方便的在 sql 语句中实现某些逻辑. 总体说来mybatis 动态SQL 语句主要有以下几类:

1. if 语句 (简单的条件判断)

2. choose (when,otherwize) ,相当于java 语言中的 switch ,与 jstl 中的choose 很类似.

3. trim (对包含的内容加上 prefix,或者 suffix 等，前缀，后缀)

4. where (主要是用来简化sql语句中where条件判断的，能智能的处理 and or ,不必担心多余导致语法错误)

5. set (主要用于更新时)

6. foreach (在实现 mybatis in 语句查询时特别有用 批量插入的时候有用)



Include sql if





mybatis Insert

public String Id

Get/set



<insert values(#Id)

报错



mybatis 源码 类



MapperProxy



ognl

Java类 xml文件 映射 填充sql



<trim

<foreach



jdbcTemplate





[【MyBatis】 动态SQL——模糊查询 LIKE](https://blog.csdn.net/wrs120/article/details/82530653)

```xml
org.mybatis.spring.MyBatisSystemException: nested exception is org.apache.ibatis.exceptions.TooManyResultsException: Expected one result (or null) to be returned by selectOne(), but found: 4

    at org.mybatis.spring.MyBatisExceptionTranslator.translateExceptionIfPossible(MyBatisExceptionTranslator.java:77)
    at org.mybatis.spring.SqlSessionTemplate$SqlSessionInterceptor.invoke(SqlSessionTemplate.java:446)
    at com.sun.proxy.$Proxy68.selectOne(Unknown Source)
    at org.mybatis.spring.SqlSessionTemplate.selectOne(SqlSessionTemplate.java:166)
```

```xml
　　<update>
　　　　update user 
　　　　<set>
　　　　　　<if test="name != null and name.length()>0">name = #{name},</if>
　　　　　　<if test="gender != null and gender.length()>0">gender = #{gender},</if>
　　　　</set>
　　　　where id = #{id}
　　</update>
```

mybatis动态SQL中的set标签的使用
https://www.cnblogs.com/qiankun-site/p/5758383.html


mybatis api doc
https://mybatis.org/mybatis-3/apidocs/index.html

package  org.apache.ibatis

SqlSession session子包
- 	close()
- 	commit()

增删改查
	insert(String statement)
	insert(String statement, Object parameter)
	delete(String statement)
	delete(String statement, Object parameter)
	update(String statement)
	update(String statement, Object parameter)
	selectOne(String statement)
	selectOne(String statement, Object parameter)
	select(String statement, ResultHandler handler)
	selectCursor(String statement, Object parameter, RowBounds rowBounds)
	selectList(String statement)
	selectList(String statement, Object parameter)
	selectList(String statement, Object parameter, RowBounds rowBounds)

SqlSessionFactory
子类
	DefaultSqlSessionFactory, SqlSessionManager
	getConfiguration()
	openSession()



Configuration session包
跟mybatis-config.xml


RowBounds
行相关的 sql limit
	NO_ROW_OFFSET
	NO_ROW_LIMIT
	DEFAULT


SqlSessionFactoryBuilder

build(Configuration config)
build(InputStream inputStream)
build(Reader reader) 


org.apache.ibatis.session.defaults

DefaultSqlSession
DefaultSqlSession.StrictMap<V>
DefaultSqlSessionFactory

org.apache.ibatis.transaction
Transaction接口
JdbcTransaction, ManagedTransaction
commit()
getConnection()
getTimeout()
rollback()


JdbcTransaction
JdbcTransactionFactory

ManagedTransaction
ManagedTransactionFactory


org.apache.ibatis.type

TypeHandler


ArrayTypeHandler, BaseTypeHandler, BigIntegerTypeHandler, BlobByteObjectArrayTypeHandler, BlobInputStreamTypeHandler, BlobTypeHandler, ByteArrayTypeHandler, ByteObjectArrayTypeHandler,  , ClobReaderTypeHandler, ClobTypeHandler, DateOnlyTypeHandler, DateTypeHandler, EnumOrdinalTypeHandler, EnumTypeHandler, InstantTypeHandler, , JapaneseDateTypeHandler, LocalDateTimeTypeHandler, LocalDateTypeHandler, LocalTimeTypeHandler, LongTypeHandler, MonthTypeHandler, NClobTypeHandler, NStringTypeHandler, ObjectTypeHandler, OffsetDateTimeTypeHandler, OffsetTimeTypeHandler, , SqlDateTypeHandler, SqlTimestampTypeHandler, SqlTimeTypeHandler, SqlxmlTypeHandler, TimeOnlyTypeHandler, UnknownTypeHandler, YearMonthTypeHandler, YearTypeHandler, ZonedDateTimeTypeHandler


BigDecimalTypeHandler
BooleanTypeHandler,
ByteTypeHandler,
IntegerTypeHandler
ShortTypeHandler
CharacterTypeHandler
DoubleTypeHandler
FloatTypeHandler
StringTypeHandler



getResult(CallableStatement cs, int columnIndex)
getResult(ResultSet rs, int columnIndex)
getResult(ResultSet rs, String columnName)
setParameter(PreparedStatement ps, int i, T parameter, JdbcType jdbcType)



JdbcType

ARRAY 
BIGINT 
BINARY 
BIT 
BLOB 
BOOLEAN 
CHAR 
CLOB 
CURSOR 
DATALINK 
DATE 
DATETIMEOFFSET 
DECIMAL 
DISTINCT 
DOUBLE 
FLOAT 
INTEGER 
JAVA_OBJECT 
LONGNVARCHAR 
LONGVARBINARY 
LONGVARCHAR 
NCHAR 
NCLOB 
NULL 
NUMERIC 
NVARCHAR 
OTHER 
REAL 
REF 
ROWID 
SMALLINT 
SQLXML 
STRUCT 
TIME 
TIME_WITH_TIMEZONE 
TIMESTAMP 
TIMESTAMP_WITH_TIMEZONE 
TINYINT 
UNDEFINED 
VARBINARY 
VARCHAR



MapUtil
computeIfAbsent(Map<K,V> map, K key, Function<K,V> mappingFunction)
entry(K key, V value)




org.apache.ibatis.scripting.xmltags

SqlNode
ChooseSqlNode, ForEachSqlNode, IfSqlNode, MixedSqlNode, SetSqlNode, StaticTextSqlNode, TextSqlNode, TrimSqlNode, VarDeclSqlNode, WhereSqlNode

apply(DynamicContext context) 



TextSqlNode表示的是包含${}占位符的动态SQL节点。它的接口实现方法如下

@Override
public boolean apply(DynamicContext context) {
  //将动态SQL（带${}占位符的SQL）解析成完成SQL语句的解析器，即将${}占位符替换成实际的变量值
  GenericTokenParser parser = createParser(new BindingTokenParser(context, injectionFilter));
  //将解析后的SQL片段添加到DynamicContext中
  context.appendSql(parser.parse(text));
  return true;
}

MixedSqlNode是树枝，TextSqlNode是树叶

MixedSqlNode是树枝，TextSqlNode是树叶

MixedSqlNode是树枝，TextSqlNode是树叶



https://blog.csdn.net/weixin_34240657/article/details/92407778

mybatis 预编译代码
https://blog.csdn.net/weixin_34452850/article/details/88991943
MixedSqlNode会遍历调用内部各个sqlNode的apply方法。

StaticTextSqlNode直接append sql文本。

TrimSqlNode的apply方法也是调用属性contents(一般都是MixedSqlNode)的apply方法，按照实例也就是7个SqlNode，都是StaticTextSqlNode和IfSqlNode。 最后会使用FilteredDynamicContext过滤掉prefix和suffix。


org.apache.ibatis.scripting
LanguageDriver

RawLanguageDriver, XMLLanguageDriver

createParameterHandler(MappedStatement mappedStatement, Object parameterObject, BoundSql boundSql)
createSqlSource(Configuration configuration, String script, Class<?> parameterType)
createSqlSource(Configuration configuration, XNode script, Class<?> parameterType)


org.apache.ibatis.scripting.LanguageDriverRegistry
getDefaultDriver() 
getDefaultDriverClass() 
getDriver(Class<? extends LanguageDriver> cls)
register(Class<? extends LanguageDriver> cls) 
register(Class<? extends LanguageDriver> cls) 

org.apache.ibatis.binding
MapperMethod
MapperProxy<T>
	MapperProxyFactory<T>
MapperRegistry



org.apache.ibatis.builder
BaseBuilder
CacheRefResolver
MapperBuilderAssistant
ParameterExpression
ResultMapResolver
SqlSourceBuilder
StaticSqlSource



org.apache.ibatis.builder.annotation

ProviderMethodResolver
Classes有
MapperAnnotationBuilder
MethodResolver
ProviderContext
ProviderSqlSource


MyBatis mapper 注解过程中通过 LanguageDriver 实现动态 SQL
https://blog.csdn.net/w_yunlong/article/details/79201509

RawLanguageDriver, XMLLanguageDriver

XMLScriptBuilder自带处理节点的方法parseDynamicTags生成需要的MixedSqlNode，而在parseDynamicTags方法内部可能会调用内部类WhereHandler、IfHandler的handleNode方法生成对应的SqlNode，而在这些handleNode方法中第一步就是调用parseDynamicTags去生成MixedSqlNode，根据MixedSqlNode生成对应的SqlNode。通过这种递归实现了节点多层嵌套的解析。
https://www.163.com/dy/article/FSRBMFNB0531CIYN.html
https://www.cnblogs.com/zhjh256/p/8512392.html
https://www.cnblogs.com/fangjian0423/p/mybaits-dynamic-sql-analysis.html

mybatis session类 api

需要手动commit

github仓库 不然插入数据失败



支持多表join





Insert 返回自增id

两种方式

[mybatis 自增id](https://blog.51cto.com/xtceetg/1957557)

1、
        useGeneratedKeys="true" keyProperty="id"
2、
        <selectKey resultType="int" order="AFTER" keyProperty="id">
            SELECT LAST_INSERT_ID()
        </selectKey>



修饰xxxMapper.java接口的是import org.springframework.stereotype.Repository;
@Repository 接口



mybatis 自定义注解，修饰xxxMapper.java接口 公司用了
https://www.cnblogs.com/sharpest/p/6097682.html
http://blog.sina.com.cn/s/blog_14ffae8a60102x5u0.html

spring bean xml文件 配置MapperScannerConfigurer bean的annotationClass属性 

MapperScannerConfigurer markerInterface
basePackage


    <!-- 扫描basePackage下所有以@MyBatisRepository标识的 接口-->
    <bean class="tk.mybatis.spring.mapper.MapperScannerConfigurer">
        <property name="basePackage" value="com.xxx.yyy.**.dao"/>
        <property name="annotationClass" value="com.xxx.yyy.common.annotation.MyBatisRepository"/>
        <property name="markerInterface" value="com.xxx.yyy.common.dao.BaseDao"/>
    </bean>




mybatis 同时操作多个表，甚至是虚拟表



mybatis 动态sql bind
https://mybatis.org/mybatis-3/dynamic-sql.html
https://blog.csdn.net/u010002184/article/details/79378835
https://blog.csdn.net/yangshangwei/article/details/80073978

<select id="selectBlogsLike" resultType="Blog">   <bind name="pattern" value="'%' + _parameter.getTitle() + '%'" />   SELECT * FROM BLOG   WHERE title LIKE #{pattern} </select>



跨表的数据 分页 union

https://blog.csdn.net/QIU1988YANG/article/details/77247556

select * from 
不能这样写，以后增加/减少列

df -hl
df - report file system disk space usage

ognl，直接获取List Map array中的值，获取对象属性的值，直接绑定
sql，本质是字符串，sql语句，返回的结果/报错信息
select name from table_name where id='1';
sql有1.语句本身，2.参数
参数是java的类String Integer等类型
sql返回的结果，需要封装成Java类
sql 批量插入数据



例如：
CREATE TABLE "websites" (
  "id" int  NOT NULL  ,
  "name" char(20) NOT NULL DEFAULT ''  ,
  "url" varchar(255) NOT NULL DEFAULT '',
  "alexa" int  NOT NULL DEFAULT '0' ,
  "country" char(10) NOT NULL DEFAULT '' ,
  PRIMARY KEY ("id")
) 


INSERT INTO "websites" VALUES ('1', 'Google', 'https://www.google.cm/', '1', 'USA'), ('2', '淘宝', 'https://www.taobao.com/', '13', 'CN'), ('3', '菜鸟教程', 'http://www.runoob.com', '5892', ''), ('4', '微博', 'http://weibo.com/', '20', 'CN'), ('5', 'Facebook', 'https://www.facebook.com/', '3', 'USA');
本身的数据就很多了

- mybatis 刘增辉

mybatis需要练习

mybatis

jdbc

连接池

接口

xml

SqlSessionFactory等核心类

mybatis spring

http://mybatis.org/spring/zh/factorybean.html

https://github.com/edidada/testmybatis

https://github.com/edidada/testmybatisspring

@Mapper

作用？

mybatis.xml
spring-hikari.xml
spring-mybatis.xml

3、org.mybatis.spring.mapper.MapperScannerConfigurer

public class MapperScannerConfigurer implements BeanDefinitionRegistryPostProcessor, InitializingBean, ApplicationContextAware, BeanNameAware

2、org.mybatis.spring.mapper.MapperFactoryBean

1、org.mybatis.spring.SqlSessionFactoryBean

SqlSessionFactoryBean implements FactoryBean<SqlSessionFactory>, InitializingBean, ApplicationListener<ApplicationEvent>

![四大金刚 mybatis plugin](../imges/mybatis_plugin.png)

http://www.mybatis.cn/archives/685.html

Spring源码深度分析
第9章

Configure九项
Spring中11项

http://mybatis.org/dtd/mybatis-3-mapper.dtd
mybatis-3-mapper.dtd

xml
跟节点

mapper

根节点的子节点
sql
ResultMap
select
insert
update
delete

Spring源码深度解析
Chap. 9
配置三样bean PooledDataSource SqlSessionFactoryBean MapperScannerConfigurer

一 xml文件（写SQL的）、二 数据库地址用户名密码、三 Java接口、四 接口中使用到的JavaBean类

```
    <bean id="dataSource" class="org.apache.ibatis.datasource.pooled.PooledDataSource">
        <property name="driver" value="com.mysql.jdbc.Driver"/>
        <property name="url" value="jdbc:mysql://localhost:3306/mybatis"/>
        <property name="username" value="root"/>
        <property name="password" value=""/>
    </bean>
    
    <bean id="sqlSessionFactory" class="org.mybatis.spring.SqlSessionFactoryBean">
        <property name="configLocation" value="classpath:mybatis-config.xml"/>
        <property name="dataSource" ref="dataSource"/>
        <property name="mapperLocations">
            <array>
                <value>classpath:tk/mybatis/**/mapper/*.xml</value>
            </array>
        </property>
        <property name="typeAliasesPackage" value="tk.mybatis.web.model"/>
    </bean>

    <bean class="org.mybatis.spring.mapper.MapperScannerConfigurer">
        <property name="addToConfig" value="true"/>
        <property name="basePackage" value="tk.mybatis.**.mapper"/>
    </bean>
```

```java

Exception in thread "main" org.apache.ibatis.binding.BindingException: Type interface com.learn.ssm.chapter4.mapper.RoleMapper is not known to the MapperRegistry.
	at org.apache.ibatis.binding.MapperRegistry.getMapper(MapperRegistry.java:47)
	at org.apache.ibatis.session.Configuration.getMapper(Configuration.java:717)
	at org.apache.ibatis.session.defaults.DefaultSqlSession.getMapper(DefaultSqlSession.java:292)
	at com.learn.ssm.chapter4.main.Chapter4Main.testRoleMapper(Chapter4Main.java:24)
	at com.learn.ssm.chapter4.main.Chapter4Main.main(Chapter4Main.java:15)

```


```java

Caused by: java.lang.ClassNotFoundException: com.duanxr.mgb.plugins.IsExistsPlugin
    at org.codehaus.plexus.classworlds.strategy.SelfFirstStrategy.loadClass (SelfFirstStrategy.java:50)
    at org.codehaus.plexus.classworlds.realm.ClassRealm.unsynchronizedLoadClass (ClassRealm.java:271)
    at org.codehaus.plexus.classworlds.realm.ClassRealm.loadClass (ClassRealm.java:247)
    at org.codehaus.plexus.classworlds.realm.ClassRealm.loadClass (ClassRealm.java:239)
    at java.lang.Class.forName0 (Native Method)
    at java.lang.Class.forName (Class.java:348)
    at org.mybatis.generator.internal.ObjectFactory.internalClassForName (ObjectFactory.java:148)
    at org.mybatis.generator.internal.ObjectFactory.createInternalObject (ObjectFactory.java:178)
    at org.mybatis.generator.internal.ObjectFactory.createPlugin (ObjectFactory.java:219)
    at org.mybatis.generator.config.Context.generateFiles (Context.java:500)
    at org.mybatis.generator.api.MyBatisGenerator.generate (MyBatisGenerator.java:269)
    at org.mybatis.generator.api.MyBatisGenerator.generate (MyBatisGenerator.java:189)
    at org.mybatis.generator.maven.MyBatisGeneratorMojo.execute (MyBatisGeneratorMojo.java:229)
    at org.apache.maven.plugin.DefaultBuildPluginManager.executeMojo (DefaultBuildPluginManager.java:137)
    at org.apache.maven.lifecycle.internal.MojoExecutor.execute (MojoExecutor.java:210)
    at org.apache.maven.lifecycle.internal.MojoExecutor.execute (MojoExecutor.java:156)
    at org.apache.maven.lifecycle.internal.MojoExecutor.execute (MojoExecutor.java:148)
    at org.apache.maven.lifecycle.internal.LifecycleModuleBuilder.buildProject (LifecycleModuleBuilder.java:117)
    at org.apache.maven.lifecycle.internal.LifecycleModuleBuilder.buildProject (LifecycleModuleBuilder.java:81)
    at org.apache.maven.lifecycle.internal.builder.singlethreaded.SingleThreadedBuilder.build (SingleThreadedBuilder.java:56)
    at org.apache.maven.lifecycle.internal.LifecycleStarter.execute (LifecycleStarter.java:128)
    at org.apache.maven.DefaultMaven.doExecute (DefaultMaven.java:305)
    at org.apache.maven.DefaultMaven.doExecute (DefaultMaven.java:192)
    at org.apache.maven.DefaultMaven.execute (DefaultMaven.java:105)
    at org.apache.maven.cli.MavenCli.execute (MavenCli.java:956)
    at org.apache.maven.cli.MavenCli.doMain (MavenCli.java:288)
    at org.apache.maven.cli.MavenCli.main (MavenCli.java:192)
    at sun.reflect.NativeMethodAccessorImpl.invoke0 (Native Method)
    at sun.reflect.NativeMethodAccessorImpl.invoke (NativeMethodAccessorImpl.java:62)
    at sun.reflect.DelegatingMethodAccessorImpl.invoke (DelegatingMethodAccessorImpl.java:43)
    at java.lang.reflect.Method.invoke (Method.java:498)
    at org.codehaus.plexus.classworlds.launcher.Launcher.launchEnhanced (Launcher.java:282)
    at org.codehaus.plexus.classworlds.launcher.Launcher.launch (Launcher.java:225)
    at org.codehaus.plexus.classworlds.launcher.Launcher.mainWithExitCode (Launcher.java:406)
    at org.codehaus.plexus.classworlds.launcher.Launcher.main (Launcher.java:347)


```

MyBatis 动态代理库

[Mybatis中Mapper动态代理的实现原理](https://blog.csdn.net/xiaokang123456kao/article/details/76228684)

动态SQL

```
  <insert id="insert" parameterType="com.xxxx.media.image.extraction.dal.models.FileInfoDO">
    insert into ${tableName} (ID, GROUP_ID, FILE_ID,
```
tableName是Java Bean中FileInfoDO的一个field，不是配置文件中的变量


[mybatis使用foreach的 separator="or" 失效问题](https://blog.csdn.net/u013091257/article/details/94858389)

[mybatis中动态SQL之trim详解](https://www.cnblogs.com/waterystone/p/7070836.html)

网上关于<trim>的介绍并不多，通过看mybatis的源码，一句话描述trim的功能：子句首尾的删除与添加。它就是一个字符串处理工具，类似于replace()，但它只处理首尾。真的是一个神器，其实mybatis中的<set>和<where>都可以用<trim>来实现，但<trim>的功能更强大，使用起来更灵活！！！

[MyBatis的Mapper接口以及Example的实例函数及详解](https://blog.csdn.net/biandous/article/details/65630783)

[MyBatis Generator产生的Example类](https://blog.csdn.net/luanlouis/article/details/22726635)

[关于Mybatis中的条件查询。createCriteria example里面的条件](https://blog.csdn.net/qq_34178998/article/details/79103586)

<trim prefix="(" prefixOverrides="OR" suffixOverrides="," suffix=")">子句</trim>

这里的子句会对其进行trim()处理，忽略掉换行、空格等字符，所以本文中的子句都是指trim()处理后的字符串。如果子句为空，那么整个<trim>块不起作用，相当于不存在。本<trim>块的作用就是：去掉子句首的OR和子句尾的逗号，并在子句前后分别加上(和)，比如，"orabc,"-->"(abc)"。

prefixOverrides：子句首的命中词列表，以|分隔，忽略大小写。如果命中（轮询命中词，最多只命中一次），会删除子句首命中的词；没命中就算了。
prefix：删除子句句首后，在子句最前边加上单个空格+prefix。
suffixOverrides：子句尾的命中词列表，以|分隔，忽略大小写。如果命中（轮询命中词，最多只命中一次），会删除子句尾命中的词；没命中就算了。
suffix：删除子句句尾后，在子句最后边加上单个空格+suffix。
有了这个神器，处理前文提起的需求，就可以用<trim>很悠然的处理了。 

替换sql字符串首尾

```java

WHERE a = #{a}
    <trim prefix="AND(" prefixOverrides="OR" suffix=")">
        <if test="b != -1">
            OR b = #{b}
        </if>
        <if test="c != -1">
            OR c = #{c}
        </if>
    </trim>

```

```java

StaticTextSqlNode (org.apache.ibatis.scripting.xmltags)
MixedSqlNode (org.apache.ibatis.scripting.xmltags)
TextSqlNode (org.apache.ibatis.scripting.xmltags)
ForEachSqlNode (org.apache.ibatis.scripting.xmltags)
IfSqlNode (org.apache.ibatis.scripting.xmltags)
VarDeclSqlNode (org.apache.ibatis.scripting.xmltags)
TrimSqlNode (org.apache.ibatis.scripting.xmltags)
    WhereSqlNode (org.apache.ibatis.scripting.xmltags)
    SetSqlNode (org.apache.ibatis.scripting.xmltags)
ChooseSqlNode (org.apache.ibatis.scripting.xmltags)


```


[mybatis中foreach标签详解](https://blog.csdn.net/gwd1154978352/article/details/75408498)

[MyBatis的foreach语句详解](https://www.jianshu.com/p/a45908678a52)

[在mybatis中使用Criteria式条件查询](https://www.iflym.com/index.php/code/201312250002.html)

[[mybatis]Example的用法 Criteria Criterion](https://blog.csdn.net/zhemeban/article/details/71901759)

`org.apache.ibatis.annotations.Param`

choose when foreach other

[Mybatis最入门---动态查询 choose,when,otherwise](https://blog.csdn.net/ABCD898989/article/details/51222452)

<choose><when><otherwise>配合使用是等价于java中的

```java

if（...）{
....
}else if(...){
...
}else{
....
}

```

按照官方文档给的示例，最后的<otherwise>是需要存在的，但是经过测试，即使最后的<otherwise>没有写，Mybatis也不会发生任何异常。而是将所有表数据返回。这是一种极为不推荐的做法。实际生产环境下，如果该表的数据量非常大，这条语句被执行，就是一个巨大的坑！


https://www.cnblogs.com/goloving/p/9241449.html

用注解来简化xml配置的时候，@Param注解的作用是给参数命名，参数命名后就能根据名字得到参数值，正确的将参数传入sql语句中

分为两种，一种是基本数据类型上
sql语句中直接引用

另一种是java类对象

```java

public List<student> selectuser(@Param(value = "page")int pn ,@Param(value = "st")student student);

<select id="selectuser" resultType="com.user.entity.student">
    SELECT * FROM student
    where sname like concat(concat("%",#{st.sname}),"%")
    LIMIT #{page} ,5
</select>

```

[Mybatis的@Param注解的用法](https://blog.csdn.net/nqmysbd/article/details/86615016)


[Mybatis 使用distinct问题](https://blog.csdn.net/a19891024/article/details/90716034)

[mybatis常用jdbcType数据类型](https://www.cnblogs.com/lixuwu/p/5916585.html)

- mybatis源码之解析xml文件
- MyBatis如何调用jdbc相关的api

[mybatis源码之解析xml文件](https://blog.csdn.net/qq_32292967/article/details/72403853)

debug
Spring Boot,MyBatis Spring
private XMLConfigBuilder(XPathParser parser, String environment, Properties props)

org.apache.ibatis.parsing.XPathParser

com.sun.org.apache.xpath.internal.jaxp.XPathImpl

https://www.jianshu.com/p/73db113748cc

### MyBatis如何调用jdbc相关的api


类型转换器

Typehandler

Java数据类型 MySQL数据库的类型


## MyBatis Generator

mybatis 2 3区别

mybatis命名空间？

namespace 接口？

mybatis spring boot starter

要熟悉

mybatis 的连接池

缓存

转换器

装饰器模式

```java
SqlSessionManager implements SqlSessionFactory, SqlSession
```

org.apache.ibatis.io.Resources#getResourceAsReader(java.lang.String)

org.apache.ibatis.session.SqlSessionFactoryBuilder



java

Configuration





mybatis 2 3区别


namespace 接口？

mybatis spring 多数据源？连接多个数据库？

第一种、直接通过RowBounds参数完成分页查询 

```java
List<Student> list = studentMapper.find(new RowBounds(0, 10));
Page page = ((Page) list;
```



第二种、PageHelper.startPage()静态方法

```
//获取第1页，10条内容，默认查询总数count
    PageHelper.startPage(1, 10);
//紧跟着的第一个select方法会被分页
    List<Country> list = studentMapper.find();
    Page page = ((Page) list;
```







[PageHelper分页插件源码及原理剖析](https://blog.csdn.net/scgyus/article/details/80694559)





https://blog.csdn.net/qq_26587997/article/details/83153747





pagerhelper例子



git@github.com:edidada/ssm.git


tk.mapper

### OGNL





[Mybatis 中的 SQL 节点的解析](https://xie.infoq.cn/article/026dd91a93ea90ee8900ff9bc)



