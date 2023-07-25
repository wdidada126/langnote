# mybatis


https://mybatis.org/mybatis-3/apidocs/index.html

mybatis_javadoc_api.xlsx

SqlSession内部运行原理
https://www.modb.pro/db/223729

org.apache.ibatis.session.SqlSession接口

select()
insert()
update()
delete()
flush()

select()
- selectOne
- selectMap
- selectList
- select

mybatis自身实现SqlSession的类
SqlSessionManager
DefaultSqlSession

mybatis-spring实现sqlsession的类
SqlSessionTemplate

SqlSessionTemplateInteceptor 实现了Invocation
invoke()方法

Proxy.newInstance()
MapperProxy是MyBatis框架中用于实现动态代理的关键类，它是通过JDK动态代理技术实现的，用于将接口与对应的SQL语句绑定在一起，实现接口方法调用时的SQL执行。
MapperProxy类的主要作用是：
实现接口的代理对象。当调用接口方法时，MapperProxy代理对象会根据方法名、参数类型等信息，从Configuration对象中获取对应的MappedStatement对象，并执行SQL语句，将查询结果映射成对应的Java对象返回给调用者。
将Mapper接口方法与MappedStatement对象绑定在一起。当使用SqlSession.getMapper方法获取Mapper接口实例时，MyBatis框架会使用MapperRegistry类将Mapper接口与对应的MapperProxy对象进行绑定，从而实现Mapper接口方法的调用。
MapperProxy类的源码非常复杂，其核心方法是invoke方法，该方法会根据接口方法的返回值类型，调用对应的SQL执行方法
在上述代码中，如果接口方法是Object类中的方法，则直接调用对应的方法。如果接口方法是默认方法，则调用invokeDefaultMethod方法执行默认方法。如果接口方法不是Object类中的方法或默认方法，则使用cachedMapperMethod方法从MapperMethodCache中获取对应的MapperMethod对象，然后调用MapperMethod对象的execute方法执行SQL语句，并将查询结果映射成对应的Java对象返回给调用者。
需要注意的是，MapperProxy类并不会直接执行SQL语句，它会调用MapperMethod对象的execute方法来执行SQL语句。MapperMethod对象包含了SQL语句、SQL参数等信息，用于执行SQL语句并将查询结果映射成Java对象返回给调用者。
总之，MapperProxy类是MyBatis框架中非常重要的一个类，它实现了接口与SQL语句的绑定，并通过动态代理技术实现了接口方法的调用。了解MapperProxy类的原理和实现方式，对于深入理解MyBatis框架的原理和实现方式非常有帮助。


MappedStatement 跟java.sql中的Statement对应




MapperMethod是MyBatis框架中的一个重要类，它用于执行Mapper接口方法对应的SQL语句，并将查询结果映射成对应的Java对象。在MyBatis框架中，每个Mapper接口方法都会对应一个MapperMethod对象。
MapperMethod类的源码非常复杂，但是它的核心方法是execute方法，该方法用于执行SQL语句并将查询结果映射成Java对象。下面对MapperMethod类的一些重要属性和方法进行简单介绍：
private final SqlCommand command：表示该MapperMethod对应的SQL语句的信息，包括SQL语句、参数类型、返回值类型等信息。

private final MethodSignature method：表示该MapperMethod对应的Mapper接口方法的信息，包括方法名、参数类型、返回值类型等信息。

public Object execute(SqlSession sqlSession, Object[] args)：该方法用于执行SQL语句并将查询结果映射成Java对象。在该方法中，首先根据SQL语句的类型调用SqlSession对象的对应方法，例如，如果SQL语句是查询语句，则调用SqlSession.selectOne方法；如果SQL语句是插入语句，则调用SqlSession.insert方法等。然后将SQL参数和返回值类型传递给SqlSession对象，执行SQL语句并获取查询结果。最后将查询结果通过TypeHandler进行映射成对应的Java对象，并返回给调用者。

private Object executeForMany(SqlSession sqlSession, Object[] args)：该方法用于执行查询多条记录的SQL语句，并将查询结果映射成List类型的Java对象。该方法会调用SqlSession.selectList方法执行SQL语句，并使用TypeHandler将查询结果映射成List类型的Java对象。

private Object executeForMap(SqlSession sqlSession, Object[] args)：该方法用于执行查询一条记录并将结果映射成Map类型的SQL语句。该方法会调用SqlSession.selectMap方法执行SQL语句，并使用TypeHandler将查询结果映射成Map类型的Java对象。

总之，MapperMethod类是MyBatis框架中非常重要的一个类，它用于执行Mapper接口方法对应的SQL语句，并将查询结果映射成对应的Java对象。

个人总结，有一个Mapper类方法，就哟一个
MapperMethod对象

MapperMethod类跟springmvc中的 RequestMethod枚举 RequestInfo RequestMappingInfo


### mybatis调用流程


mybatis源码核心类
https://zhuanlan.zhihu.com/p/613769992


SqlSessionFactoryBuilder是构造器，见名知意，它的主要作用便是构造SqlSessionFactory实例，基本流程为根据传入的数据流创建XMLConfigBuilder，生成Configuration对象，然后根据Configuration对象创建默认的SqlSessionFactory实例。

解析mapper.xml时，Mybatis默认XML驱动类为XMLLanguageDriver，它的主要作用是解析select、update、insert、delete节点为完整的SQL语句，也是对应SQL的解析过程，XMLLanguageDriver在解析mapper.xml时，会将解析结果存储至SqlSource的实现类中，SqlSource是一个接口，只定义了一个 getBoundSql() 方法，它控制着动态 SQL 语句解析的整个流程，它会根据从 Mapper.xml 映射文件解析到的 SQL 语句以及执行 SQL 时传入的实参，返回一条可执行的 SQL。它有三个重要的实现类，对应图中写到的RawSqlSource、DynamicSqlSource及StaticSqlSource，其中RawSqlSource处理的是非动态 SQL 语句，DynamicSqlSource处理的是动态 SQL 语句，StaticSqlSource是BoundSql中要存储SQL语句的一个载体，上面RawSqlSource、DynamicSqlSource的SQL语句，最终都会存储到StaticSqlSource实现类中。StaticSqlSource的 getBoundSql() 方法是真正创建 BoundSql 对象的地方， BoundSql 包含了解析之后的 SQL 语句、字段、每个“#{}”占位符的属性信息、实参信息等。这里也重点介绍下Configuration对象，Configuration 的创建会装载一些基本属性，如事务，数据源，缓存，代理，类型处理器等，从这里可以看出 Configuration 也是一个大的容器，来为后面的SQL语句解析和初始化提供保障，也是Mybatis中贯穿全局的存在，后续我们要提到的Mybatis降低全表更新插件，也是基于这个对象来完成。其中解析mapper.xml这步最终作用便是将解析的每一条CRUD语句封装成对应的MappedStatement存放至Configuration中。


SqlSource 接口实现类

XMLLanguageDriver用于对sql脚本进行解析，解析各种标签。

trim TrimHandler
where WhereHandler


XMLScriptBuilder

private void initNodeHandlerMap() {
    nodeHandlerMap.put("trim", new TrimHandler());
    nodeHandlerMap.put("where", new WhereHandler());
    nodeHandlerMap.put("set", new SetHandler());
    nodeHandlerMap.put("foreach", new ForEachHandler());
    nodeHandlerMap.put("if", new IfHandler());
    nodeHandlerMap.put("choose", new ChooseHandler());
    nodeHandlerMap.put("when", new IfHandler());
    nodeHandlerMap.put("otherwise", new OtherwiseHandler());
    nodeHandlerMap.put("bind", new BindHandler());
  }

https://blog.csdn.net/RenshenLi/article/details/118531540




XMLConfigBuilder：解析mybatis中configLocation属性中的全局xml文件，内部会使用 XMLMapperBuilder 解析各个xml文件。
XMLMapperBuilder：遍历mybatis中mapperLocations属性中的xml文件中每个节点的Builder，比如user.xml，内部会使用 XMLStatementBuilder 处理xml中的每个节点。
XMLStatementBuilder：解析xml文件中各个节点，比如select,insert,update,delete节点，内部会使用 XMLScriptBuilder 处理节点的sql部分，遍历产生的数据会丢到Configuration的mappedStatements中。
XMLScriptBuilder：解析xml中各个节点sql部分的Builder。



Mybatis动态解析里面有2个核心的类SqlNode、SqlSource、ExpressionEvaluator。Mybatis动态Sql使用分为2个部分：动态Sql解析、动态Sql拼接执行。



每个SqlNode负责自己那块功能。职责单一。SqlNode的核心方法apply就是通过ExpressionEvaluator来解析OGNL表达式数据的。接下来我们看看Mybatis是如何递归解析动态sql脚本的。




new GenericTokenParser("${", "}", new BindingTokenParser(context, injectionFilter))


ParameterMappingTokenHandler handler = new ParameterMappingTokenHandler(configuration, parameterType, additionalParameters);
//#{}解析器
GenericTokenParser parser = new GenericTokenParser("#{", "}", handler);



Mybatis对数据的处理可以分为 用入参动态的拼装sql 和 对sql执行的结果封装成 JavaBean





一个完整的Sql命令，其执行的完整流程图如下：

![mybatis_process](..\..\imgs\mybatis_process.jpg)

MapperRegistry
  MapperProxyFactory
    MapperProxy

### Mybatis开启日志打印

https://blog.csdn.net/qq_41482600/article/details/126864628

### mybatis like
sql注入
https://www.jb51.net/article/232026.htm



Mybatis中Like 的使用方式以及一些注意点


      select * from t_user where name like '%${name}%'   SQL注入风险


      select * from t_user where name like concat('%',#{name,jdbcType=VARCHAR},'%')


使用mybatis的开源项目：
- sonar


mybatis xml文件 有哪些子节点，可以在IDEA中查看到，IDEA中有智能提示

一个mybatis节点，可以执行多条sql语句

MyBatisCodeHelperPro idea插件


[springboot打印mybatis的sql语句](https://blog.csdn.net/qq_41345773/article/details/90178017)

[Spring Boot 打印mybatis sql日志信息](https://www.cnblogs.com/huxiaoguang/p/10808967.html)

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
MapperProxy<T> implements InvocationHandler

InvocationHandler
public Object invoke(Object proxy, Method method, Object[] args)
        throws Throwable;

动态代理(接口级别代理)
动态代理又叫JDK动态代理是实现JDK里的InvocationHandler接口的invoke方法，但注意的是代理的是接口，也就是你的业务类必须要实现接口，通过Proxy里的newProxyInstance得到代理对象。
JDK动态代理是基于反射的,效率比较低。
动态代理不知道要代理什么东西，只有在运行时才知道。

java.lang.reflect.Proxy#newProxyInstance(java.lang.ClassLoader, java.lang.Class<?>[], java.lang.reflect.InvocationHandler)


ognl

Java类 xml文件 映射 填充sql



<trim

<foreach



jdbcTemplate





[【MyBatis】 动态SQL——模糊查询 LIKE](https://blog.csdn.net/wrs120/article/details/82530653)



SqlSessionTemplate.SqlSessionInterceptor 内部类



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

org.apache.ibatis.binding包
MapperMethod
MapperProxy<T>
	MapperProxyFactory<T>
MapperRegistry

MapperMethod
MapperMethod只有2个成员域,都是静态内部类,所以
MapperMethod ≈ SqlCommand + MethodSignature
MapperProxy是Mapper的动态代理实现,他的invoke方法会调用MapperMethod的execute方法.
MapperMethod这个类的作用就是把你自定义的Mapper里的方法和参数翻译成sqlSession里定义的那些selectOne呀selectMany等等方法.这样当调用你自定义的方法的时候MethodProxy就能够执行sqlSession对应的方法了.

| MapperMethod操作 | sqlSession方法名                                             |
| ---------------- | ------------------------------------------------------------ |
| INSERT           | sqlSession.insert()                                          |
| UPDATE           | sqlSession.update()                                          |
| DELETE           | sqlSession.delete()                                          |
| FLUSH            | sqlSession.flushStatements()                                 |
| SELECT           | executeWithResultHandler(sqlSession, args) executeForMany(sqlSession, args) method.returnsMap() executeForCursor() sqlSession.selectOne(command.getName(), param) |

org.apache.ibatis.builder包
BaseBuilder
CacheRefResolver
MapperBuilderAssistant
ParameterExpression
ResultMapResolver
SqlSourceBuilder
StaticSqlSource



org.apache.ibatis.builder.annotation包

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


书籍/book：
- Mybatis3源码深度解析
- mybatis 刘增辉
- MyBatis技术内幕
- 通用源码阅读指导书：MyBatis源码详解

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

![四大金刚 mybatis plugin](..\..\imges\mybatis_plugin.png)

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

```xml
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



https://github.com/edidada/ssm

tk.mapper

### OGNL





[Mybatis 中的 SQL 节点的解析](https://xie.infoq.cn/article/026dd91a93ea90ee8900ff9bc)



mybatis高效插入
https://zhuanlan.zhihu.com/p/35305211

### mybatis缓存策略
使用escache三方缓存

MyBatis提供了两种缓存：一级缓存和二级缓存。其中，一级缓存是SqlSession级别的，也就是说，同一个SqlSession对象调用一个Mapper方法，往往只执行一次SQL，因为使用同一个SqlSession对象调用相同的Mapper方法时，MyBatis会先从它的本地Cache中查找是否有该数据，如果有则直接返回，否则才会去数据库中查询。而二级缓存是Mapper级别的，它可以被多个SqlSession对象共享
mybatis一级缓存实现类

MyBatis的一级缓存是指在应用运行过程中，一次数据库会话中，执行多次相同的查询，会优先查询缓存中的数据，减少数据库查询次数，提高查询效率。
MyBatis内部存储缓存使用的是一个HashMap对象，key为 hashCode + sqlId + sql 语句。2 而value值就是从查询出来映射生成的java对象。
每次查询都会先从缓存区域找，如果找不到就会从数据库查询数据，然后将查询到的数据写入一级缓存中。

https://blog.csdn.net/BruceLiu_code/article/details/119478137

![mybatis1_cache](../../imgs/mybatis/mybatis1_cache.png)


CachingExecutor

一级缓存的实现是通过 CachingExecutor 实现的


DefaultSqlSession中有一个CacheExecutor
CachingExecutor 中有一个 SimpleExecutor
SimpleExecutor 中有一个叫 LocalCache (PerpetualCache类型)
LocalCache才是真正的存储缓存的地方
LocalCache 中有一个叫cache （Hashmap <Object,Object>类型的）



mybatis二级缓存实现类

https://www.cnblogs.com/cxuanBlog/p/11333021.html

https://www.jianshu.com/p/b8fa01332cdd


MyBatis的二级缓存是Application级别的缓存，它可以提高对数据库查询的效率，以提高应用的性能。MyBatis自身提供了丰富的，并且功能强大的二级缓存的实现，它拥有一系列的Cache接口装饰者，可以满足各种对缓存操作和更新的策略。开启二级缓存的条件也是比较简单，通过直接在 MyBatis 配置文件中通过 <settings> <setting name = "cacheEnabled" value = "true" /> </settings> 来开启。

MyBatis查询数据的顺序是：

二级缓存 ———> 一级缓存——> 数据库

        <dependency>    　　
            <groupId>org.slf4j</groupId>    　　
            <artifactId>slf4j-simple</artifactId>    　　
            <version>1.7.25</version>    　　
            <scope>compile</scope>
        </dependency>

使某条Select查询支持二级缓存，你需要保证：

1. MyBatis支持二级缓存的总开关：全局配置变量参数 cacheEnabled=true
2. 该select语句所在的Mapper，配置了<cache> 或<cached-ref>节点，并且有效
3. 该select语句的参数 useCache=true


![mybatis2_cache](D:\git\github\langnote\imgs\mybatis\mybatis2_cache.webp)

实现分页的三种方法
RowBounds



SqlSessionFactoryBuilder
build()方法

- 通用源码阅读指导书：MyBatis源码详解
- mybatis3源码深度解析
- 手写MyBatis：渐进式源码实践




类型别名是你的好帮手。使用它们，你就可以不用输入类的全限定名了。比如：

<!-- mybatis-config.xml 中 -->
<typeAlias type="com.someapp.model.User" alias="User"/>

<!-- SQL 映射 XML 中 -->
<select id="selectUsers" resultType="User">
  select id, username, hashedPassword
  from some_table
  where id = #{id}
</select>



#{}和${}两者含义不同

#会把传入的数据都当成一个字符串来处理，会在传入的数据上面加一个双引号来处理。
而$则是把传入的数据直接显示在sql语句中，不会添加双引号。



Mybatis Dynamic SQL
https://mybatis.org/mybatis-dynamic-sql/docs/introduction.html


Mybatis Dynamic SQL 是 Mybatis 团队出的一个框架，兼容 Mybatis3 的生态，但与 Mybatis 最大的不同是：你既不用在 XML 里写 SQL，也不用在 Annotation 里拼接 SQL（用 Java 拼接过复杂字符串的都懂），而是直接以 Java 的方式去写 SQL。

这样会带来以下好处

Typesafe：在编译期就可以确保你的 sql 参数类型和列类型是一致的
Expressive：这就是要执行的 SQL 的样子
Flexible：再复杂的 if else、and、or 都能轻松实现
Mybatis Generator
Mybatis Generator 也是 Mybatis 团队出的代码自动生成工具，它支持 Mybatis3、Mybatis-Dynamic-SQL 等类型的代码生成。提供了非常多的扩展点和预定义配置项，使得用户可以灵活的自定义生成规则。

并且 Generator 也支持多种生成模式，用户可以根据使用场景自行选择

command 模式：可以通过命令行生成代码
Maven 插件：直接集成在 Maven 构建工具中
Java Runtime 模式：通过编写 Java 代码然后运行来生成



mybatis源码
https://www.zhihu.com/answer/2225895340

https://gitee.com/edidada/testmybatis jdbc分支 mybatis使用xpath技术解析xml



运行java程序，查看运行过程中有哪些对象

jmap -histo:live pid

jmap -histo:live 1424

 847:             1             16  oracle.jdbc.driver.Message11
 848:             1             16  org.apache.ibatis.cache.TransactionalCacheManager
 849:             1             16  org.apache.ibatis.executor.keygen.Jdbc3KeyGenerator
 850:             1             16  org.apache.ibatis.executor.keygen.NoKeyGenerator
 851:             1             16  org.apache.ibatis.executor.loader.javassist.JavassistProxyFactory
 852:             1             16  org.apache.ibatis.javassist.util.proxy.ProxyFactory$1
 853:             1             16  org.apache.ibatis.javassist.util.proxy.ProxyFactory$3
 854:             1             16  org.apache.ibatis.ognl.ArrayElementsAccessor
 855:             1             16  org.apache.ibatis.ognl.ArrayPropertyAccessor
 856:             1             16  org.apache.ibatis.ognl.CollectionElementsAccessor
 857:             1             16  org.apache.ibatis.ognl.EnumerationElementsAccessor
 858:             1             16  org.apache.ibatis.ognl.EnumerationPropertyAccessor
 859:             1             16  org.apache.ibatis.ognl.EvaluationPool
 860:             1             16  org.apache.ibatis.ognl.IteratorElementsAccessor
 861:             1             16  org.apache.ibatis.ognl.IteratorPropertyAccessor
 862:             1             16  org.apache.ibatis.ognl.ListPropertyAccessor
 863:             1             16  org.apache.ibatis.ognl.MapElementsAccessor
 864:             1             16  org.apache.ibatis.ognl.MapPropertyAccessor
 865:             1             16  org.apache.ibatis.ognl.NumberElementsAccessor
 866:             1             16  org.apache.ibatis.ognl.ObjectArrayPool
 867:             1             16  org.apache.ibatis.ognl.ObjectElementsAccessor
 868:             1             16  org.apache.ibatis.ognl.ObjectMethodAccessor
 869:             1             16  org.apache.ibatis.ognl.ObjectNullHandler
 870:             1             16  org.apache.ibatis.ognl.ObjectPropertyAccessor
 871:             1             16  org.apache.ibatis.ognl.SetPropertyAccessor
 872:             1             16  org.apache.ibatis.plugin.InterceptorChain
 873:             1             16  org.apache.ibatis.scripting.defaults.RawLanguageDriver
 874:             1             16  org.apache.ibatis.scripting.xmltags.DynamicContext$ContextAccessor
 875:             1             16  org.apache.ibatis.scripting.xmltags.XMLLanguageDriver
 876:             1             16  org.apache.ibatis.session.defaults.DefaultSqlSessionFactory
 877:             1             16  org.apache.ibatis.transaction.jdbc.JdbcTransactionFactory
 878:             1             16  org.apache.ibatis.type.TypeAliasRegistry





 605:             1             16  org.apache.ibatis.cache.TransactionalCacheManager
 606:             1             16  org.apache.ibatis.executor.loader.javassist.JavassistProxyFactory
 607:             1             16  org.apache.ibatis.io.DefaultVFS
 608:             1             16  org.apache.ibatis.javassist.util.proxy.ProxyFactory$1
 609:             1             16  org.apache.ibatis.javassist.util.proxy.ProxyFactory$3
 610:             1             16  org.apache.ibatis.ognl.ArrayElementsAccessor
 611:             1             16  org.apache.ibatis.ognl.ArrayPropertyAccessor
 612:             1             16  org.apache.ibatis.ognl.CollectionElementsAccessor
 613:             1             16  org.apache.ibatis.ognl.EnumerationElementsAccessor
 614:             1             16  org.apache.ibatis.ognl.EnumerationPropertyAccessor
 615:             1             16  org.apache.ibatis.ognl.EvaluationPool
 616:             1             16  org.apache.ibatis.ognl.IteratorElementsAccessor
 617:             1             16  org.apache.ibatis.ognl.IteratorPropertyAccessor
 618:             1             16  org.apache.ibatis.ognl.ListPropertyAccessor
 619:             1             16  org.apache.ibatis.ognl.MapElementsAccessor
 620:             1             16  org.apache.ibatis.ognl.MapPropertyAccessor
 621:             1             16  org.apache.ibatis.ognl.NumberElementsAccessor
 622:             1             16  org.apache.ibatis.ognl.ObjectArrayPool
 623:             1             16  org.apache.ibatis.ognl.ObjectElementsAccessor
 624:             1             16  org.apache.ibatis.ognl.ObjectMethodAccessor
 625:             1             16  org.apache.ibatis.ognl.ObjectNullHandler
 626:             1             16  org.apache.ibatis.ognl.ObjectPropertyAccessor
 627:             1             16  org.apache.ibatis.ognl.SetPropertyAccessor
 628:             1             16  org.apache.ibatis.plugin.InterceptorChain
 629:             1             16  org.apache.ibatis.scripting.defaults.RawLanguageDriver
 630:             1             16  org.apache.ibatis.scripting.xmltags.DynamicContext$ContextAccessor
 631:             1             16  org.apache.ibatis.scripting.xmltags.XMLLanguageDriver
 632:             1             16  org.apache.ibatis.session.defaults.DefaultSqlSessionFactory
 633:             1             16  org.apache.ibatis.transaction.jdbc.JdbcTransactionFactory
 634:             1             16  org.apache.ibatis.type.TypeAliasRegistry
 635:             1             16  org.apache.log4j.DefaultCategoryFactory
 636:             1             16  org.apache.log4j.helpers.AppenderAttachableImpl
 637:             1             16  org.apache.log4j.or.DefaultRenderer
 638:             1             16  org.apache.log4j.or.RendererMap
 639:             1             16  org.apache.log4j.spi.DefaultRepositorySelector
 640:             1             16  org.slf4j.helpers.BasicMarkerFactory
 641:             1             16  org.slf4j.helpers.NOPLoggerFactory
 642:             1             16  org.slf4j.helpers.SubstituteLoggerFactory
 643:             1             16  org.slf4j.impl.Log4jLoggerFactory
 644:             1             16  org.slf4j.impl.StaticLoggerBinder
 645:             1             16  org.slf4j.impl.StaticMarkerBinder



















 num     #instances         #bytes  class name
----------------------------------------------
   1:          1884        2461048  [B
   2:         14213        1959584  [C
   3:         13857         332568  java.lang.String
   4:          2004         231216  java.lang.Class
   5:          1753         226576  [I
   6:          1659         145992  java.lang.reflect.Method
   7:          1561         120944  [Ljava.lang.Object;
   8:          3411         109152  java.util.HashMap$Node
   9:          1634          52288  java.util.concurrent.ConcurrentHashMap$Node
  10:           696          50112  java.lang.reflect.Field
  11:           482          40680  [Ljava.lang.String;
  12:          1008          40320  java.lang.ref.Finalizer
  13:          1753          39848  [Ljava.lang.Class;
  14:           171          35744  [Ljava.util.HashMap$Node;
  15:           848          33920  java.util.TreeMap$Entry
  16:           480          26880  java.util.zip.ZipFile$ZipFileInputStream
  17:            13          26832  [Lorg.apache.ibatis.ognl.internal.Entry;
  18:           463          25928  java.util.zip.ZipFile$ZipFileInflaterInputStream
  19:          1426          22816  java.lang.Object
  20:           476          15232  java.util.Hashtable$Entry
  21:           175          14000  java.lang.reflect.Constructor
  22:            35          12176  [Ljava.util.concurrent.ConcurrentHashMap$Node;
  23:           341          10912  sun.misc.FDBigInteger
  24:           268          10720  java.lang.ref.SoftReference
  25:           405           9720  java.util.ArrayList
  26:           202           9696  java.util.HashMap
  27:             9           8360  [[C
  28:            54           8104  [Ljava.lang.reflect.Method;
  29:           126           8064  com.mysql.jdbc.ConnectionPropertiesImpl$BooleanConnectionProperty
  30:           480           7680  java.lang.Integer
  31:           130           7280  java.lang.Class$ReflectionData
  32:           202           6464  sun.reflect.UnsafeObjectFieldAccessorImpl
  33:           100           6400  java.net.URL
  34:           258           6192  java.lang.Long
  35:            21           4608  [Ljava.util.Hashtable$Entry;
  36:           109           4360  java.math.BigInteger
  37:            13           4304  [S
  38:            74           4144  java.lang.Package
  39:           172           4128  java.text.EntryPair
  40:             1           4112  [Lcom.sun.org.apache.xpath.internal.objects.XObject;
  41:            78           3120  java.io.ObjectStreamField
  42:           127           3048  java.util.jar.Attributes$Name
  43:            43           2752  com.mysql.jdbc.ConnectionPropertiesImpl$StringConnectionProperty
  44:            42           2688  java.util.concurrent.ConcurrentHashMap
  45:            55           2640  sun.net.www.MimeEntry
  46:             7           2632  java.lang.Thread
  47:            47           2632  sun.misc.URLClassPath$JarLoader
  48:            77           2464  java.lang.ref.WeakReference
  49:            30           2400  [Ljava.util.WeakHashMap$Entry;
  50:            60           2400  com.mysql.jdbc.MysqlCharset
  51:            24           2336  [Ljava.lang.reflect.Field;
  52:            70           2240  java.util.Vector
  53:            43           2064  sun.util.locale.LocaleObjectCache$CacheEntry
  54:            51           2040  java.util.LinkedHashMap$Entry
  55:            28           2000  [J
  56:            83           1992  java.util.LinkedList$Node
  57:            80           1960  [Ljava.lang.reflect.Constructor;
  58:            29           1856  com.mysql.jdbc.ConnectionPropertiesImpl$IntegerConnectionProperty
  59:            76           1824  sun.reflect.NativeConstructorAccessorImpl
  60:            68           1632  org.apache.ibatis.reflection.invoker.MethodInvoker
  61:             1           1568  [[B
  62:            64           1536  sun.reflect.generics.tree.SimpleClassTypeSignature
  63:            47           1504  java.util.LinkedList
  64:            26           1456  sun.nio.cs.UTF_8$Encoder
  65:            30           1440  java.util.WeakHashMap
  66:            60           1440  org.apache.ibatis.ognl.internal.Entry
  67:            10           1392  [Z
  68:             1           1376  [Lsun.misc.FDBigInteger;
  69:            41           1312  java.lang.ref.ReferenceQueue
  70:            39           1280  [Ljava.math.BigInteger;
  71:            20           1280  java.util.jar.JarFile
  72:            64           1264  [Lsun.reflect.generics.tree.TypeArgument;
  73:            13           1248  java.util.jar.JarFile$JarFileEntry
  74:             1           1224  com.mysql.jdbc.JDBC4Connection
  75:            51           1224  java.io.ExpiringCache$Entry
  76:            76           1216  sun.reflect.DelegatingConstructorAccessorImpl
  77:            28           1120  java.math.BigDecimal
  78:             2           1064  [Ljava.lang.Integer;
  79:             2           1064  [Ljava.lang.invoke.MethodHandle;
  80:            19           1064  java.beans.MethodDescriptor
  81:             1           1040  [Lcom.mysql.jdbc.MysqlCharset;
  82:             1           1040  [Ljava.lang.Long;
  83:             1           1040  [Lsun.text.normalizer.UnicodeSet;
  84:            63           1008  sun.reflect.generics.tree.ClassTypeSignature
  85:            30            960  sun.reflect.generics.repository.ClassRepository
  86:            39            936  java.sql.JDBCType
  87:            23            920  java.util.WeakHashMap$Entry
  88:            21            840  sun.util.locale.BaseLocale$Key
  89:             5            824  [D
  90:            33            792  java.beans.MethodRef
  91:            49            784  java.util.HashSet
  92:            14            784  java.util.ResourceBundle$CacheKey
  93:            16            768  java.util.zip.Inflater
  94:            19            760  sun.nio.cs.UTF_8$Decoder
  95:            47            752  java.util.Collections$UnmodifiableSet
  96:            32            744  [Ljava.lang.reflect.Type;
  97:            31            744  org.apache.ibatis.type.JdbcType
  98:            23            736  java.util.zip.ZipCoder
  99:            18            720  java.io.FileDescriptor
 100:            30            720  sun.reflect.generics.factory.CoreReflectionFactory
 101:            30            720  sun.reflect.generics.tree.ClassSignature
 102:            29            696  java.util.Collections$UnmodifiableRandomAccessList
 103:            29            696  sun.reflect.NativeMethodAccessorImpl
 104:            29            696  sun.reflect.generics.scope.ClassScope
 105:            43            688  java.lang.ref.ReferenceQueue$Lock
 106:            42            672  java.util.HashMap$KeySet
 107:            21            672  java.util.Locale
 108:            14            672  java.util.ResourceBundle$BundleReference
 109:            28            672  sun.reflect.generics.reflectiveObjects.ParameterizedTypeImpl
 110:            21            672  sun.util.locale.BaseLocale
 111:            18            648  [Ljava.io.ObjectStreamField;
 112:            26            624  org.apache.log4j.CategoryKey
 113:            19            608  java.io.File
 114:            12            576  java.util.Hashtable
 115:             6            576  org.apache.ibatis.mapping.MappedStatement
 116:            10            560  sun.util.calendar.ZoneInfo
 117:            23            552  java.util.ArrayDeque
 118:            22            528  java.lang.Class$AnnotationData
 119:            13            520  java.security.ProtectionDomain
 120:            31            512  [Lsun.reflect.generics.tree.FormalTypeParameter;
 121:            30            504  [Lsun.reflect.generics.tree.ClassTypeSignature;
 122:             7            504  java.beans.PropertyDescriptor
 123:            21            504  java.util.Locale$LocaleKey
 124:            31            496  sun.reflect.DelegatingMethodAccessorImpl
 125:            12            480  java.security.AccessControlContext
 126:            12            480  org.apache.log4j.Logger
 127:            14            448  com.sun.org.apache.xml.internal.dtm.ref.ExtendedType
 128:            14            448  java.io.FileInputStream
 129:            14            448  java.util.ResourceBundle$LoaderReference
 130:            14            448  org.apache.log4j.ProvisionNode
 131:             9            432  java.util.Properties
 132:            18            432  sun.misc.MetaIndex
 133:            13            416  java.security.CodeSource
 134:             1            384  java.lang.ref.Finalizer$FinalizerThread
 135:             6            384  java.nio.DirectByteBuffer
 136:            16            384  java.util.zip.ZStreamRef
 137:             1            376  com.mysql.jdbc.AbandonedConnectionCleanupThread
 138:             1            376  java.lang.ref.Reference$ReferenceHandler
 139:             9            360  com.sun.org.apache.xerces.internal.utils.XMLSecurityManager$Limit
 140:             6            336  java.nio.DirectLongBufferU
 141:            10            320  java.lang.OutOfMemoryError
 142:            13            312  org.apache.ibatis.ognl.internal.ClassCacheImpl
 143:            13            312  org.apache.log4j.Level
 144:             2            288  [Lorg.apache.ibatis.type.JdbcType;
 145:             6            288  org.apache.ibatis.session.Configuration$StrictMap
 146:            11            264  tk.mybatis.simple.model.Country
 147:             1            256  com.mysql.jdbc.MysqlIO
 148:             8            256  java.io.FilePermission
 149:             8            256  java.security.Permissions
 150:             8            256  java.util.Collections$UnmodifiableMap
 151:             8            256  sun.misc.ProxyGenerator$PrimitiveTypeInfo
 152:            10            240  com.sun.org.apache.xerces.internal.impl.XMLScanner$NameType
 153:             2            240  java.net.SocksSocketImpl
 154:             5            240  java.util.TreeMap
 155:            15            240  org.apache.ibatis.reflection.invoker.SetFieldInvoker
 156:             3            240  sun.net.www.protocol.jar.URLJarFile
 157:             5            240  sun.util.locale.provider.LocaleResources$ResourceReference
 158:             7            224  java.security.BasicPermissionCollection
 159:             2            224  java.util.GregorianCalendar
 160:             7            224  java.util.RegularEnumSet
 161:            14            224  org.apache.ibatis.reflection.invoker.GetFieldInvoker
 162:             3            216  [Ljava.beans.MethodDescriptor;
 163:             7            216  [Ljava.lang.Boolean;
 164:             3            216  com.mysql.jdbc.ConnectionPropertiesImpl$MemorySizeConnectionProperty
 165:             9            216  java.lang.RuntimePermission
 166:            13            208  [Ljava.security.Principal;
 167:            13            208  java.security.ProtectionDomain$Key
 168:             8            192  java.io.FilePermissionCollection
 169:             6            192  java.lang.ThreadLocal$ThreadLocalMap$Entry
 170:             8            192  java.math.RoundingMode
 171:             2            192  sun.util.calendar.Gregorian$Date
 172:             1            176  [Ljava.sql.JDBCType;
 173:             2            176  java.net.DualStackPlainSocketImpl
 174:             1            168  [[Ljava.math.BigInteger;
 175:             7            168  com.sun.org.apache.xerces.internal.util.FeatureState
 176:             7            168  java.util.jar.Manifest
 177:             3            168  org.apache.ibatis.mapping.ResultMap
 178:             2            160  [[Ljava.lang.String;
 179:             5            160  com.sun.org.apache.xpath.internal.objects.XNumber
 180:             4            160  java.lang.ClassLoader$NativeLibrary
 181:            10            160  java.util.Formatter$Flags
 182:             5            160  java.util.regex.Pattern$Branch
 183:             1            160  org.apache.ibatis.session.Configuration
 184:             5            160  sun.util.locale.provider.LocaleProviderAdapter$Type
 185:             2            144  [Ljava.math.BigDecimal;
 186:             6            144  com.sun.org.apache.xerces.internal.util.Status
 187:             3            144  java.beans.BeanDescriptor
 188:             3            144  java.nio.HeapByteBuffer
 189:             6            144  java.util.concurrent.atomic.AtomicLong
 190:             6            144  java.util.regex.Pattern$GroupHead
 191:             6            144  java.util.regex.Pattern$GroupTail
 192:             6            144  org.apache.ibatis.builder.StaticSqlSource
 193:             6            144  org.apache.ibatis.mapping.ParameterMap
 194:             6            144  org.apache.ibatis.mapping.SqlCommandType
 195:             6            144  sun.misc.PerfCounter
 196:             3            144  sun.misc.URLClassPath
 197:             3            144  sun.nio.cs.StreamEncoder
 198:             2            144  sun.reflect.DelegatingClassLoader
 199:             2            128  [F
 200:             6            128  [Lsun.reflect.generics.tree.FieldTypeSignature;
 201:             2            128  java.io.ExpiringCache$1
 202:             4            128  java.util.Stack
 203:             8            128  java.util.jar.Attributes
 204:             4            128  java.util.regex.Pattern$Curly
 205:             8            128  org.apache.ibatis.logging.log4j.Log4jImpl
 206:             2            128  sun.nio.cs.ext.DoubleByte$Encoder
 207:             5            120  [Ljava.util.regex.Pattern$Node;
 208:             5            120  com.mysql.jdbc.StringUtils$SearchMode
 209:             5            120  com.sun.org.apache.xerces.internal.util.PropertyState
 210:             5            120  com.sun.org.apache.xerces.internal.utils.XMLSecurityManager$State
 211:             5            120  com.sun.org.apache.xerces.internal.utils.XMLSecurityPropertyManager$State
 212:             3            120  java.beans.GenericBeanInfo
 213:             5            120  javax.xml.namespace.QName
 214:             5            120  jdk.xml.internal.JdkXmlFeatures$State
 215:             5            120  org.apache.ibatis.type.StringTypeHandler
 216:             3            120  sun.misc.FloatingDecimal$BinaryToASCIIBuffer
 217:             5            120  sun.misc.FloatingDecimal$PreparedASCIIToBinaryBuffer
 218:             7            112  java.lang.ThreadLocal
 219:             2            112  java.util.LinkedHashMap
 220:             3             96  [Ljava.beans.PropertyDescriptor;
 221:             1             96  [[J
 222:             3             96  com.mysql.jdbc.Buffer
 223:             3             96  com.sun.org.apache.xerces.internal.utils.XMLSecurityManager$NameMap
 224:             3             96  java.io.FileOutputStream
 225:             2             96  java.lang.ThreadGroup
 226:             3             96  java.lang.reflect.WeakCache$CacheValue
 227:             4             96  java.math.MathContext
 228:             4             96  java.sql.SQLPermission
 229:             6             96  org.apache.ibatis.executor.keygen.NoKeyGenerator
 230:             2             96  org.apache.ibatis.reflection.Reflector
 231:             6             96  org.apache.ibatis.scripting.defaults.RawSqlSource
 232:             4             96  org.apache.ibatis.type.BigDecimalTypeHandler
 233:             4             96  org.apache.ibatis.type.BlobTypeHandler
 234:             4             96  org.apache.ibatis.type.BooleanTypeHandler
 235:             4             96  org.apache.ibatis.type.ClobTypeHandler
 236:             4             96  org.apache.ibatis.type.NStringTypeHandler
 237:             3             96  org.apache.log4j.helpers.PatternParser$BasicPatternConverter
 238:             3             96  org.apache.log4j.helpers.PatternParser$LiteralPatternConverter
 239:             1             96  sun.misc.Launcher$AppClassLoader
 240:             3             96  sun.net.spi.DefaultProxySelector$NonProxyInfo
 241:             2             96  sun.nio.cs.US_ASCII$Decoder
 242:             2             96  sun.text.normalizer.CharTrie
 243:             1             88  sun.misc.Launcher$ExtClassLoader
 244:             2             80  [Lcom.mysql.jdbc.StringUtils$SearchMode;
 245:             1             80  [Ljava.lang.ThreadLocal$ThreadLocalMap$Entry;
 246:             2             80  [Lorg.apache.ibatis.mapping.SqlCommandType;
 247:             1             80  [[I
 248:             1             80  [[S
 249:             1             80  [[Z
 250:             2             80  java.io.BufferedWriter
 251:             2             80  java.io.ExpiringCache
 252:             2             80  java.util.Locale$Category
 253:             5             80  java.util.regex.Pattern$BranchConn
 254:             2             80  jdk.xml.internal.JdkXmlFeatures$XmlFeature
 255:             5             80  org.apache.ibatis.logging.slf4j.Slf4jImpl
 256:             5             80  org.apache.ibatis.logging.slf4j.Slf4jLocationAwareLoggerImpl
 257:             1             72  [Lcom.sun.org.apache.xml.internal.dtm.ref.ExtendedType;
 258:             3             72  java.io.BufferedOutputStream
 259:             3             72  java.io.OutputStreamWriter
 260:             3             72  java.net.Proxy$Type
 261:             3             72  java.util.Arrays$ArrayList
 262:             1             72  java.util.ResourceBundle$RBClassLoader
 263:             3             72  java.util.concurrent.ConcurrentHashMap$KeySetView
 264:             3             72  java.util.concurrent.atomic.AtomicMarkableReference$Pair
 265:             1             72  java.util.regex.Pattern
 266:             3             72  java.util.regex.Pattern$BitClass
 267:             3             72  java.util.regex.Pattern$Ctype
 268:             3             72  java.util.regex.Pattern$Single
 269:             3             72  org.apache.ibatis.mapping.StatementType
 270:             3             72  org.apache.ibatis.session.AutoMappingBehavior
 271:             3             72  org.apache.ibatis.session.ExecutorType
 272:             3             72  org.apache.ibatis.type.ByteTypeHandler
 273:             3             72  org.apache.ibatis.type.DoubleTypeHandler
 274:             3             72  org.apache.ibatis.type.FloatTypeHandler
 275:             3             72  org.apache.ibatis.type.IntegerTypeHandler
 276:             3             72  org.apache.ibatis.type.LongTypeHandler
 277:             3             72  org.apache.ibatis.type.ShortTypeHandler
 278:             3             72  org.slf4j.impl.Log4jLoggerAdapter
 279:             3             72  sun.misc.FloatingDecimal$ExceptionalBinaryToASCIIBuffer
 280:             3             72  sun.misc.JarIndex
 281:             1             72  sun.util.locale.provider.JRELocaleProviderAdapter
 282:             3             72  sun.util.resources.ParallelListResourceBundle$KeySet
 283:             2             64  [Ljava.lang.Thread;
 284:             3             64  [Ljava.lang.reflect.TypeVariable;
 285:             2             64  [Lorg.apache.ibatis.mapping.StatementType;
 286:             2             64  [Lorg.apache.ibatis.session.AutoMappingBehavior;
 287:             2             64  [Lorg.apache.ibatis.session.ExecutorType;
 288:             1             64  com.mysql.jdbc.ConnectionPropertiesImpl$LongConnectionProperty
 289:             2             64  com.sun.org.apache.xerces.internal.utils.XMLSecurityPropertyManager$Property
 290:             2             64  java.io.PrintStream
 291:             2             64  java.lang.ClassValue$Entry
 292:             2             64  java.lang.VirtualMachineError
 293:             2             64  java.lang.ref.ReferenceQueue$Null
 294:             2             64  java.lang.reflect.Proxy$Key1
 295:             2             64  java.net.InetAddress$InetAddressHolder
 296:             2             64  java.net.Socket
 297:             2             64  java.util.concurrent.locks.ReentrantLock$NonfairSync
 298:             1             64  org.apache.log4j.ConsoleAppender
 299:             2             64  sun.reflect.generics.reflectiveObjects.TypeVariableImpl
 300:             4             64  sun.reflect.generics.tree.ArrayTypeSignature
 301:             2             64  sun.util.locale.provider.LocaleServiceProviderPool
 302:             1             56  [Lcom.sun.org.apache.xerces.internal.impl.XMLScanner$NameType;
 303:             1             56  [Lcom.sun.org.apache.xerces.internal.utils.XMLSecurityManager$Limit;
 304:             1             48  [Lcom.sun.beans.util.Cache$CacheEntry;
 305:             1             48  [Ljava.beans.WeakIdentityMap$Entry;
 306:             3             48  [Ljava.lang.annotation.Annotation;
 307:             1             48  [Ljava.math.RoundingMode;
 308:             2             48  [Lorg.apache.ibatis.session.LocalCacheScope;
 309:             3             48  com.sun.org.apache.xerces.internal.impl.dv.dtd.ListDatatypeValidator
 310:             2             48  java.io.File$PathStatus
 311:             3             48  java.lang.Byte
 312:             2             48  java.lang.Double
 313:             3             48  java.lang.Short
 314:             2             48  java.net.Inet4Address
 315:             2             48  java.net.InetAddress$Cache
 316:             2             48  java.net.InetAddress$Cache$Type
 317:             1             48  java.net.SocketInputStream
 318:             1             48  java.net.SocketOutputStream
 319:             2             48  java.nio.charset.CoderResult
 320:             3             48  java.nio.charset.CodingErrorAction
 321:             2             48  java.sql.DriverInfo
 322:             3             48  java.text.AttributedCharacterIterator$Attribute
 323:             1             48  java.text.RuleBasedCollator
 324:             2             48  java.util.BitSet
 325:             2             48  java.util.Collections$SynchronizedSet
 326:             2             48  java.util.concurrent.CopyOnWriteArrayList
 327:             3             48  java.util.concurrent.atomic.AtomicMarkableReference
 328:             2             48  java.util.regex.Pattern$1
 329:             2             48  java.util.regex.Pattern$5
 330:             2             48  org.apache.ibatis.cache.impl.PerpetualCache
 331:             1             48  org.apache.ibatis.datasource.unpooled.UnpooledDataSource
 332:             1             48  org.apache.ibatis.executor.SimpleExecutor
 333:             2             48  org.apache.ibatis.reflection.DefaultReflectorFactory
 334:             2             48  org.apache.ibatis.session.LocalCacheScope
 335:             2             48  org.apache.ibatis.type.ArrayTypeHandler
 336:             2             48  org.apache.ibatis.type.BlobByteObjectArrayTypeHandler
 337:             2             48  org.apache.ibatis.type.CharacterTypeHandler
 338:             2             48  org.apache.ibatis.type.DateOnlyTypeHandler
 339:             2             48  org.apache.ibatis.type.DateTypeHandler
 340:             2             48  org.apache.ibatis.type.NClobTypeHandler
 341:             2             48  org.apache.ibatis.type.TimeOnlyTypeHandler
 342:             1             48  org.apache.log4j.Hierarchy
 343:             2             48  sun.misc.NativeSignalHandler
 344:             2             48  sun.misc.Signal
 345:             3             48  sun.net.www.protocol.jar.Handler
 346:             2             48  sun.reflect.generics.tree.FormalTypeParameter
 347:             1             48  sun.text.normalizer.IntTrie
 348:             1             48  sun.text.resources.FormatData
 349:             1             48  sun.text.resources.zh.FormatData_zh
 350:             1             48  sun.text.resources.zh.FormatData_zh_CN
 351:             1             48  sun.util.resources.CalendarData
 352:             1             48  sun.util.resources.CurrencyNames
 353:             1             48  sun.util.resources.zh.CalendarData_zh
 354:             1             48  sun.util.resources.zh.CurrencyNames_zh_CN
 355:             1             40  [Lcom.sun.org.apache.xerces.internal.util.Status;
 356:             1             40  [Lcom.sun.org.apache.xerces.internal.utils.XMLSecurityManager$State;
 357:             1             40  [Lcom.sun.org.apache.xerces.internal.utils.XMLSecurityPropertyManager$State;
 358:             1             40  [Ljdk.xml.internal.JdkXmlFeatures$State;
 359:             1             40  [Lsun.util.locale.provider.LocaleProviderAdapter$Type;
 360:             1             40  com.mysql.jdbc.StandardSocketFactory
 361:             1             40  com.mysql.jdbc.util.ReadAheadInputStream
 362:             1             40  com.sun.beans.finder.MethodFinder$1
 363:             1             40  com.sun.xml.internal.stream.util.BufferAllocator
 364:             1             40  java.beans.WeakIdentityMap$Entry
 365:             1             40  java.io.BufferedInputStream
 366:             1             40  java.lang.reflect.Proxy$Key2
 367:             1             40  java.text.RBCollationTables
 368:             1             40  java.util.EnumMap
 369:             1             40  java.util.IdentityHashMap
 370:             1             40  java.util.PropertyResourceBundle
 371:             1             40  java.util.ResourceBundle$1
 372:             1             40  org.apache.ibatis.cache.NullCacheKey
 373:             1             40  org.apache.log4j.spi.RootLogger
 374:             1             40  sun.nio.cs.StandardCharsets$Aliases
 375:             1             40  sun.nio.cs.StandardCharsets$Cache
 376:             1             40  sun.nio.cs.StandardCharsets$Classes
 377:             1             40  sun.nio.cs.ext.ExtendedCharsets
 378:             1             40  sun.reflect.generics.repository.MethodRepository
 379:             1             40  sun.text.IntHashtable
 380:             1             40  sun.text.UCompactIntArray
 381:             1             40  sun.text.resources.CollationData
 382:             1             40  sun.text.resources.zh.CollationData_zh
 383:             1             32  [Lcom.sun.beans.util.Cache$Kind;
 384:             1             32  [Lcom.sun.org.apache.xerces.internal.utils.XMLSecurityManager$NameMap;
 385:             2             32  [Ljava.lang.Enum;
 386:             1             32  [Ljava.lang.OutOfMemoryError;
 387:             2             32  [Ljava.lang.StackTraceElement;
 388:             1             32  [Ljava.lang.ThreadGroup;
 389:             1             32  [Ljava.net.Proxy$Type;
 390:             1             32  com.mysql.jdbc.JDBC4DatabaseMetaData
 391:             1             32  com.mysql.jdbc.NonRegisteringDriver$ConnectionPhantomReference
 392:             1             32  com.mysql.jdbc.authentication.Sha256PasswordPlugin
 393:             2             32  com.sun.beans.WeakCache
 394:             1             32  com.sun.beans.finder.BeanInfoFinder
 395:             1             32  com.sun.org.apache.xerces.internal.impl.XMLEntityScanner$1
 396:             2             32  com.sun.org.apache.xerces.internal.impl.dv.dtd.ENTITYDatatypeValidator
 397:             1             32  com.sun.org.apache.xerces.internal.jaxp.SAXParserFactoryImpl
 398:             1             32  java.beans.ThreadGroupContext
 399:             1             32  java.beans.ThreadGroupContext$1
 400:             1             32  java.io.WinNTFileSystem
 401:             1             32  java.lang.ArithmeticException
 402:             2             32  java.lang.Boolean
 403:             2             32  java.lang.Character
 404:             2             32  java.lang.Float
 405:             1             32  java.lang.NullPointerException
 406:             1             32  java.lang.StringCoding$StringDecoder
 407:             1             32  java.lang.StringCoding$StringEncoder
 408:             1             32  java.lang.reflect.WeakCache
 409:             2             32  java.nio.ByteOrder
 410:             1             32  java.util.Formatter
 411:             1             32  java.util.Random
 412:             2             32  java.util.concurrent.atomic.AtomicInteger
 413:             1             32  java.util.concurrent.atomic.AtomicReferenceFieldUpdater$AtomicReferenceFieldUpdaterImpl
 414:             2             32  java.util.concurrent.locks.ReentrantLock
 415:             2             32  javax.xml.xpath.SecuritySupport
 416:             1             32  org.apache.ibatis.reflection.MetaObject
 417:             2             32  org.apache.ibatis.reflection.factory.DefaultObjectFactory
 418:             2             32  org.apache.ibatis.reflection.wrapper.DefaultObjectWrapperFactory
 419:             1             32  org.apache.ibatis.transaction.jdbc.JdbcTransaction
 420:             1             32  org.apache.ibatis.type.TypeHandlerRegistry
 421:             1             32  org.apache.log4j.PatternLayout
 422:             1             32  org.apache.log4j.helpers.QuietWriter
 423:             1             32  sun.instrument.InstrumentationImpl
 424:             1             32  sun.nio.cs.StandardCharsets
 425:             1             32  sun.reflect.generics.reflectiveObjects.WildcardTypeImpl
 426:             1             32  sun.reflect.generics.tree.MethodTypeSignature
 427:             2             32  sun.reflect.generics.tree.TypeVariableSignature
 428:             2             32  sun.text.normalizer.CharTrie$FriendAgent
 429:             1             32  sun.util.locale.provider.LocaleResources
 430:             1             24  [Lcom.sun.org.apache.xerces.internal.utils.XMLSecurityPropertyManager$Property;
 431:             1             24  [Ljava.io.File$PathStatus;
 432:             1             24  [Ljava.lang.ClassValue$Entry;
 433:             1             24  [Ljava.net.InetAddress$Cache$Type;
 434:             1             24  [Ljava.security.ProtectionDomain;
 435:             1             24  [Ljava.util.Locale$Category;
 436:             1             24  [Ljdk.xml.internal.JdkXmlFeatures$XmlFeature;
 437:             1             24  [Lorg.apache.ibatis.executor.ExecutionPlaceholder;
 438:             1             24  [Lorg.apache.ibatis.ognl.internal.ClassCache;
 439:             1             24  [Lsun.launcher.LauncherHelper;
 440:             1             24  com.mysql.jdbc.NetworkResources
 441:             1             24  com.mysql.jdbc.SingleByteCharsetConverter
 442:             1             24  com.mysql.jdbc.authentication.MysqlClearPasswordPlugin
 443:             1             24  com.mysql.jdbc.authentication.MysqlNativePasswordPlugin
 444:             1             24  com.mysql.jdbc.authentication.MysqlOldPasswordPlugin
 445:             1             24  com.sun.beans.util.Cache$Kind$1
 446:             1             24  com.sun.beans.util.Cache$Kind$2
 447:             1             24  com.sun.beans.util.Cache$Kind$3
 448:             1             24  com.sun.org.apache.xerces.internal.impl.Constants$ArrayEnumeration
 449:             1             24  java.lang.ClassValue$Version
 450:             1             24  java.lang.StringBuffer
 451:             1             24  java.lang.StringBuilder
 452:             1             24  java.lang.ThreadLocal$ThreadLocalMap
 453:             1             24  java.lang.invoke.MethodHandleImpl$4
 454:             1             24  java.lang.reflect.ReflectPermission
 455:             1             24  java.net.Inet6AddressImpl
 456:             1             24  java.net.Proxy
 457:             1             24  java.util.Collections$EmptyMap
 458:             1             24  java.util.Collections$SetFromMap
 459:             1             24  java.util.Currency
 460:             1             24  java.util.Locale$Cache
 461:             1             24  java.util.ResourceBundle$Control$CandidateListCache
 462:             1             24  java.util.concurrent.ConcurrentLinkedQueue
 463:             1             24  java.util.concurrent.ConcurrentLinkedQueue$Node
 464:             1             24  java.util.regex.Pattern$Start
 465:             1             24  org.apache.ibatis.binding.MapperRegistry
 466:             1             24  org.apache.ibatis.executor.CachingExecutor
 467:             1             24  org.apache.ibatis.executor.ExecutionPlaceholder
 468:             1             24  org.apache.ibatis.io.ClassLoaderWrapper
 469:             1             24  org.apache.ibatis.javassist.util.proxy.ProxyFactory$2
 470:             1             24  org.apache.ibatis.mapping.Environment
 471:             1             24  org.apache.ibatis.ognl.enhance.ExpressionCompiler
 472:             1             24  org.apache.ibatis.reflection.MetaClass
 473:             1             24  org.apache.ibatis.reflection.wrapper.BeanWrapper
 474:             1             24  org.apache.ibatis.scripting.LanguageDriverRegistry
 475:             1             24  org.apache.ibatis.session.RowBounds
 476:             1             24  org.apache.ibatis.session.defaults.DefaultSqlSession
 477:             1             24  org.apache.ibatis.type.BigIntegerTypeHandler
 478:             1             24  org.apache.ibatis.type.ByteArrayTypeHandler
 479:             1             24  org.apache.ibatis.type.ByteObjectArrayTypeHandler
 480:             1             24  org.apache.ibatis.type.ObjectTypeHandler
 481:             1             24  org.apache.ibatis.type.SqlDateTypeHandler
 482:             1             24  org.apache.ibatis.type.SqlTimeTypeHandler
 483:             1             24  org.apache.ibatis.type.SqlTimestampTypeHandler
 484:             1             24  org.apache.ibatis.type.UnknownTypeHandler
 485:             1             24  org.apache.log4j.helpers.OnlyOnceErrorHandler
 486:             1             24  org.slf4j.helpers.BasicMarker
 487:             1             24  sun.instrument.TransformerManager
 488:             1             24  sun.launcher.LauncherHelper
 489:             1             24  sun.misc.URLClassPath$FileLoader
 490:             1             24  sun.net.ProgressMonitor
 491:             1             24  sun.net.www.MimeTable
 492:             1             24  sun.nio.cs.IBM437
 493:             1             24  sun.nio.cs.IBM850
 494:             1             24  sun.nio.cs.IBM852
 495:             1             24  sun.nio.cs.IBM866
 496:             1             24  sun.nio.cs.ISO_8859_1
 497:             1             24  sun.nio.cs.ISO_8859_13
 498:             1             24  sun.nio.cs.ISO_8859_2
 499:             1             24  sun.nio.cs.ISO_8859_7
 500:             1             24  sun.nio.cs.ISO_8859_9
 501:             1             24  sun.nio.cs.KOI8_R
 502:             1             24  sun.nio.cs.MS1250
 503:             1             24  sun.nio.cs.MS1251
 504:             1             24  sun.nio.cs.MS1252
 505:             1             24  sun.nio.cs.MS1257
 506:             1             24  sun.nio.cs.ThreadLocalCoders$1
 507:             1             24  sun.nio.cs.ThreadLocalCoders$2
 508:             1             24  sun.nio.cs.US_ASCII
 509:             1             24  sun.nio.cs.UTF_16
 510:             1             24  sun.nio.cs.UTF_16BE
 511:             1             24  sun.nio.cs.UTF_16LE
 512:             1             24  sun.nio.cs.UTF_32
 513:             1             24  sun.nio.cs.UTF_8
 514:             1             24  sun.nio.cs.ext.Big5
 515:             1             24  sun.nio.cs.ext.EUC_CN
 516:             1             24  sun.nio.cs.ext.EUC_JP
 517:             1             24  sun.nio.cs.ext.EUC_JP_Open
 518:             1             24  sun.nio.cs.ext.EUC_KR
 519:             1             24  sun.nio.cs.ext.GB18030
 520:             1             24  sun.nio.cs.ext.GBK
 521:             1             24  sun.nio.cs.ext.IBM943
 522:             1             24  sun.nio.cs.ext.ISO_8859_8
 523:             1             24  sun.nio.cs.ext.MS1256
 524:             1             24  sun.nio.cs.ext.MS932
 525:             1             24  sun.nio.cs.ext.MS936
 526:             1             24  sun.nio.cs.ext.MacCentralEurope
 527:             1             24  sun.nio.cs.ext.MacRoman
 528:             1             24  sun.nio.cs.ext.SJIS
 529:             1             24  sun.nio.cs.ext.TIS_620
 530:             1             24  sun.reflect.generics.scope.MethodScope
 531:             1             24  sun.reflect.generics.tree.Wildcard
 532:             1             24  sun.util.locale.BaseLocale$Cache
 533:             1             24  sun.util.locale.provider.CalendarDataProviderImpl
 534:             1             24  sun.util.locale.provider.CollatorProviderImpl
 535:             1             24  sun.util.locale.provider.CurrencyNameProviderImpl
 536:             1             24  sun.util.locale.provider.DecimalFormatSymbolsProviderImpl
 537:             1             16  [Ljava.beans.EventSetDescriptor;
 538:             1             16  [Ljava.lang.Throwable;
 539:             1             16  [Ljava.security.cert.Certificate;
 540:             1             16  [Lsun.instrument.TransformerManager$TransformerInfo;
 541:             1             16  [Lsun.reflect.generics.tree.TypeSignature;
 542:             1             16  com.mysql.fabric.jdbc.FabricMySQLDriver
 543:             1             16  com.mysql.jdbc.Driver
 544:             1             16  com.mysql.jdbc.Util
 545:             1             16  com.mysql.jdbc.log.NullLogger
 546:             1             16  com.mysql.jdbc.log.StandardLogger
 547:             1             16  com.sun.org.apache.xerces.internal.dom.CharacterDataImpl$1
 548:             1             16  com.sun.org.apache.xerces.internal.impl.dv.dtd.IDDatatypeValidator
 549:             1             16  com.sun.org.apache.xerces.internal.impl.dv.dtd.IDREFDatatypeValidator
 550:             1             16  com.sun.org.apache.xerces.internal.impl.dv.dtd.NMTOKENDatatypeValidator
 551:             1             16  com.sun.org.apache.xerces.internal.impl.dv.dtd.NOTATIONDatatypeValidator
 552:             1             16  com.sun.org.apache.xerces.internal.impl.dv.dtd.StringDatatypeValidator
 553:             1             16  com.sun.org.apache.xerces.internal.utils.SecuritySupport
 554:             1             16  com.sun.org.apache.xpath.internal.objects.EqualComparator
 555:             1             16  com.sun.org.apache.xpath.internal.objects.GreaterThanComparator
 556:             1             16  com.sun.org.apache.xpath.internal.objects.GreaterThanOrEqualComparator
 557:             1             16  com.sun.org.apache.xpath.internal.objects.LessThanComparator
 558:             1             16  com.sun.org.apache.xpath.internal.objects.LessThanOrEqualComparator
 559:             1             16  com.sun.org.apache.xpath.internal.objects.NotEqualComparator
 560:             1             16  com.sun.org.apache.xpath.internal.objects.XMLStringFactoryImpl
 561:             1             16  java.io.FileDescriptor$1
 562:             1             16  java.lang.CharacterDataLatin1
 563:             1             16  java.lang.ClassValue$Identity
 564:             1             16  java.lang.Runtime
 565:             1             16  java.lang.String$CaseInsensitiveComparator
 566:             1             16  java.lang.System$2
 567:             1             16  java.lang.Terminator$1
 568:             1             16  java.lang.invoke.MemberName$Factory
 569:             1             16  java.lang.invoke.MethodHandleImpl$2
 570:             1             16  java.lang.invoke.MethodHandleImpl$3
 571:             1             16  java.lang.ref.Reference$1
 572:             1             16  java.lang.ref.Reference$Lock
 573:             1             16  java.lang.reflect.Proxy$KeyFactory
 574:             1             16  java.lang.reflect.Proxy$ProxyClassFactory
 575:             1             16  java.lang.reflect.ReflectAccess
 576:             1             16  java.math.BigDecimal$1
 577:             1             16  java.net.InetAddress$2
 578:             1             16  java.net.URLClassLoader$7
 579:             1             16  java.nio.Bits$1
 580:             1             16  java.nio.charset.CoderResult$1
 581:             1             16  java.nio.charset.CoderResult$2
 582:             1             16  java.security.ProtectionDomain$2
 583:             1             16  java.security.ProtectionDomain$JavaSecurityAccessImpl
 584:             1             16  java.text.MessageFormat$Field
 585:             1             16  java.util.Collections$EmptyEnumeration
 586:             1             16  java.util.Collections$EmptyIterator
 587:             1             16  java.util.Collections$EmptyList
 588:             1             16  java.util.Collections$EmptySet
 589:             1             16  java.util.Collections$UnmodifiableMap$UnmodifiableEntrySet
 590:             1             16  java.util.Currency$CurrencyNameGetter
 591:             1             16  java.util.EnumMap$1
 592:             1             16  java.util.HashMap$EntrySet
 593:             1             16  java.util.Hashtable$EntrySet
 594:             1             16  java.util.Hashtable$KeySet
 595:             1             16  java.util.ResourceBundle$Control
 596:             1             16  java.util.WeakHashMap$KeySet
 597:             1             16  java.util.concurrent.ConcurrentHashMap$ValuesView
 598:             1             16  java.util.concurrent.atomic.AtomicBoolean
 599:             1             16  java.util.jar.JavaUtilJarAccessImpl
 600:             1             16  java.util.regex.Pattern$4
 601:             1             16  java.util.regex.Pattern$LastNode
 602:             1             16  java.util.regex.Pattern$Node
 603:             1             16  java.util.zip.ZipFile$1
 604:             1             16  javax.xml.parsers.SecuritySupport
 605:             1             16  org.apache.ibatis.cache.TransactionalCacheManager
 606:             1             16  org.apache.ibatis.executor.loader.javassist.JavassistProxyFactory
 607:             1             16  org.apache.ibatis.io.DefaultVFS
 608:             1             16  org.apache.ibatis.javassist.util.proxy.ProxyFactory$1
 609:             1             16  org.apache.ibatis.javassist.util.proxy.ProxyFactory$3
 610:             1             16  org.apache.ibatis.ognl.ArrayElementsAccessor
 611:             1             16  org.apache.ibatis.ognl.ArrayPropertyAccessor
 612:             1             16  org.apache.ibatis.ognl.CollectionElementsAccessor
 613:             1             16  org.apache.ibatis.ognl.EnumerationElementsAccessor
 614:             1             16  org.apache.ibatis.ognl.EnumerationPropertyAccessor
 615:             1             16  org.apache.ibatis.ognl.EvaluationPool
 616:             1             16  org.apache.ibatis.ognl.IteratorElementsAccessor
 617:             1             16  org.apache.ibatis.ognl.IteratorPropertyAccessor
 618:             1             16  org.apache.ibatis.ognl.ListPropertyAccessor
 619:             1             16  org.apache.ibatis.ognl.MapElementsAccessor
 620:             1             16  org.apache.ibatis.ognl.MapPropertyAccessor
 621:             1             16  org.apache.ibatis.ognl.NumberElementsAccessor
 622:             1             16  org.apache.ibatis.ognl.ObjectArrayPool
 623:             1             16  org.apache.ibatis.ognl.ObjectElementsAccessor
 624:             1             16  org.apache.ibatis.ognl.ObjectMethodAccessor
 625:             1             16  org.apache.ibatis.ognl.ObjectNullHandler
 626:             1             16  org.apache.ibatis.ognl.ObjectPropertyAccessor
 627:             1             16  org.apache.ibatis.ognl.SetPropertyAccessor
 628:             1             16  org.apache.ibatis.plugin.InterceptorChain
 629:             1             16  org.apache.ibatis.scripting.defaults.RawLanguageDriver
 630:             1             16  org.apache.ibatis.scripting.xmltags.DynamicContext$ContextAccessor
 631:             1             16  org.apache.ibatis.scripting.xmltags.XMLLanguageDriver
 632:             1             16  org.apache.ibatis.session.defaults.DefaultSqlSessionFactory
 633:             1             16  org.apache.ibatis.transaction.jdbc.JdbcTransactionFactory
 634:             1             16  org.apache.ibatis.type.TypeAliasRegistry
 635:             1             16  org.apache.log4j.DefaultCategoryFactory
 636:             1             16  org.apache.log4j.helpers.AppenderAttachableImpl
 637:             1             16  org.apache.log4j.or.DefaultRenderer
 638:             1             16  org.apache.log4j.or.RendererMap
 639:             1             16  org.apache.log4j.spi.DefaultRepositorySelector
 640:             1             16  org.slf4j.helpers.BasicMarkerFactory
 641:             1             16  org.slf4j.helpers.NOPLoggerFactory
 642:             1             16  org.slf4j.helpers.SubstituteLoggerFactory
 643:             1             16  org.slf4j.impl.Log4jLoggerFactory
 644:             1             16  org.slf4j.impl.StaticLoggerBinder
 645:             1             16  org.slf4j.impl.StaticMarkerBinder
 646:             1             16  sun.misc.ASCIICaseInsensitiveComparator
 647:             1             16  sun.misc.FloatingDecimal$1
 648:             1             16  sun.misc.Launcher
 649:             1             16  sun.misc.Launcher$Factory
 650:             1             16  sun.misc.Perf
 651:             1             16  sun.misc.Unsafe
 652:             1             16  sun.net.DefaultProgressMeteringPolicy
 653:             1             16  sun.net.spi.DefaultProxySelector
 654:             1             16  sun.net.www.protocol.file.Handler
 655:             1             16  sun.net.www.protocol.jar.JarFileFactory
 656:             1             16  sun.reflect.GeneratedMethodAccessor1
 657:             1             16  sun.reflect.GeneratedMethodAccessor2
 658:             1             16  sun.reflect.ReflectionFactory
 659:             1             16  sun.reflect.generics.tree.BottomSignature
 660:             1             16  sun.reflect.generics.tree.ByteSignature
 661:             1             16  sun.text.normalizer.NormalizerImpl
 662:             1             16  sun.text.normalizer.NormalizerImpl$AuxTrieImpl
 663:             1             16  sun.text.normalizer.NormalizerImpl$FCDTrieImpl
 664:             1             16  sun.text.normalizer.NormalizerImpl$NormTrieImpl
 665:             1             16  sun.util.calendar.Gregorian
 666:             1             16  sun.util.locale.provider.AuxLocaleProviderAdapter$NullProvider
 667:             1             16  sun.util.locale.provider.CalendarDataUtility$CalendarWeekParameterGetter
 668:             1             16  sun.util.locale.provider.SPILocaleProviderAdapter
 669:             1             16  sun.util.resources.LocaleData
 670:             1             16  sun.util.resources.LocaleData$LocaleDataResourceBundleControl
 671:             1             16  tk.mybatis.simple.Main
Total         56976        6290520



 num     #instances         #bytes  class name
----------------------------------------------
   1:          2781        3484176  [B
   2:         15154        1956784  [C
   3:         14924         358176  java.lang.String
   4:          2444         279264  java.lang.Class
   5:          1975         173800  java.lang.reflect.Method
   6:          2032         144384  [Ljava.lang.Object;
   7:          3668         117376  java.util.HashMap$Node
   8:          2536          81152  java.util.concurrent.ConcurrentHashMap$Node
   9:          1611          64440  java.lang.ref.Finalizer
  10:          1121          55472  [I
  11:           738          53136  java.lang.reflect.Field
  12:           727          47848  [Ljava.lang.String;
  13:           287          47288  [Ljava.util.HashMap$Node;
  14:          2011          45312  [Ljava.lang.Class;
  15:           777          43512  java.util.zip.ZipFile$ZipFileInputStream
  16:           762          42672  java.util.zip.ZipFile$ZipFileInflaterInputStream
  17:          2207          35312  java.lang.Object
  18:           848          33920  java.util.TreeMap$Entry
  19:           813          32520  java.util.LinkedHashMap$Entry
  20:            13          26832  [Lorg.apache.ibatis.ognl.internal.Entry;
  21:            45          22000  [Ljava.util.concurrent.ConcurrentHashMap$Node;
  22:           499          19960  java.lang.ref.SoftReference
  23:           815          19560  java.util.ArrayList
  24:           230          18400  java.lang.reflect.Constructor
  25:           536          17152  java.lang.ref.WeakReference
  26:           310          14880  java.util.HashMap
  27:           446          14272  java.util.Hashtable$Entry
  28:           106          11872  [Ljava.lang.reflect.Method;
  29:           341          10912  sun.misc.FDBigInteger
  30:           183          10248  java.lang.Class$ReflectionData
  31:             1           8208  [Lcom.mysql.jdbc.MysqlCharset;
  32:           126           8064  com.mysql.jdbc.ConnectionPropertiesImpl$BooleanConnectionProperty
  33:             7           7280  [[C
  34:           105           6720  java.net.URL
  35:           417           6672  java.lang.Integer
  36:           206           6592  sun.reflect.UnsafeObjectFieldAccessorImpl
  37:           111           6216  java.beans.MethodDescriptor
  38:           259           6216  java.lang.Long
  39:           111           6216  java.lang.Package
  40:           237           5688  java.beans.MethodRef
  41:           223           5352  sun.reflect.generics.tree.SimpleClassTypeSignature
  42:            63           4536  java.beans.PropertyDescriptor
  43:           109           4360  java.math.BigInteger
  44:           223           4344  [Lsun.reflect.generics.tree.TypeArgument;
  45:            20           4240  [Ljava.util.Hashtable$Entry;
  46:             1           4112  [Lcom.sun.org.apache.xpath.internal.objects.XObject;
  47:           171           4104  java.util.jar.Attributes$Name
  48:           178           3896  [Ljava.lang.reflect.Type;
  49:            55           3520  java.util.concurrent.ConcurrentHashMap
  50:            87           3480  java.io.ObjectStreamField
  51:           208           3328  sun.reflect.generics.tree.ClassTypeSignature
  52:             8           3008  java.lang.Thread
  53:            46           2944  com.mysql.jdbc.ConnectionPropertiesImpl$StringConnectionProperty
  54:            48           2688  sun.misc.URLClassPath$JarLoader
  55:           110           2640  sun.reflect.generics.factory.CoreReflectionFactory
  56:           108           2624  [Ljava.lang.reflect.Constructor;
  57:            28           2528  [Ljava.lang.reflect.Field;
  58:            30           2528  [Ljava.util.WeakHashMap$Entry;
  59:           101           2424  sun.reflect.NativeConstructorAccessorImpl
  60:            60           2400  com.mysql.jdbc.MysqlCharset
  61:            96           2304  sun.reflect.generics.scope.ClassScope
  62:            57           2280  java.util.WeakHashMap$Entry
  63:            71           2272  sun.reflect.generics.repository.ClassRepository
  64:            11           2224  [S
  65:            89           2136  sun.reflect.generics.reflectiveObjects.ParameterizedTypeImpl
  66:            15           2112  [Ljava.beans.MethodDescriptor;
  67:            44           2112  sun.util.locale.LocaleObjectCache$CacheEntry
  68:            98           2064  [Lsun.reflect.generics.tree.FieldTypeSignature;
  69:            28           2000  [J
  70:           106           1928  [Lsun.reflect.generics.tree.FormalTypeParameter;
  71:            30           1920  com.mysql.jdbc.ConnectionPropertiesImpl$IntegerConnectionProperty
  72:            80           1920  org.apache.ibatis.reflection.invoker.MethodInvoker
  73:            72           1728  java.util.LinkedList$Node
  74:            71           1704  sun.reflect.generics.tree.ClassSignature
  75:             3           1616  [[B
  76:           101           1616  sun.reflect.DelegatingConstructorAccessorImpl
  77:            66           1584  java.security.Provider$ServiceKey
  78:            28           1568  java.util.LinkedHashMap
  79:            27           1512  java.security.Provider$Service
  80:            31           1488  ch.qos.logback.classic.Logger
  81:            26           1456  sun.nio.cs.UTF_8$Encoder
  82:            30           1440  java.util.WeakHashMap
  83:            60           1440  org.apache.ibatis.ognl.internal.Entry
  84:            44           1408  java.util.LinkedList
  85:            35           1400  sun.reflect.generics.repository.MethodRepository
  86:             1           1376  [Lsun.misc.FDBigInteger;
  87:            42           1344  java.lang.ref.ReferenceQueue
  88:            14           1344  java.util.jar.JarFile$JarFileEntry
  89:            33           1320  com.sun.org.apache.xerces.internal.dom.DeferredAttrImpl
  90:            55           1320  java.io.ExpiringCache$Entry
  91:            71           1288  [Lsun.reflect.generics.tree.ClassTypeSignature;
  92:            39           1280  [Ljava.math.BigInteger;
  93:            20           1280  java.util.jar.JarFile
  94:             1           1232  com.mysql.jdbc.JDBC4Connection
  95:            50           1200  sun.reflect.NativeMethodAccessorImpl
  96:            37           1184  org.xml.sax.helpers.LocatorImpl
  97:            28           1120  java.math.BigDecimal
  98:            35           1120  sun.reflect.generics.tree.MethodTypeSignature
  99:            27           1080  com.sun.org.apache.xerces.internal.dom.DeferredTextImpl
 100:             2           1064  [Ljava.lang.invoke.MethodHandle;
 101:            52           1064  [Ljava.lang.reflect.TypeVariable;
 102:            44           1056  java.lang.Class$AnnotationData
 103:             1           1040  [Ljava.lang.Integer;
 104:             1           1040  [Ljava.lang.Long;
 105:            24            960  java.io.FileDescriptor
 106:            30            960  java.security.Provider$EngineDescription
 107:            60            960  java.util.HashSet
 108:            30            960  sun.reflect.generics.reflectiveObjects.TypeVariableImpl
 109:            17            952  com.sun.org.apache.xerces.internal.dom.DeferredElementImpl
 110:            39            936  java.sql.JDBCType
 111:            39            936  org.apache.ibatis.type.JdbcType
 112:            16            896  sun.util.calendar.ZoneInfo
 113:            37            888  java.util.Collections$UnmodifiableRandomAccessList
 114:            16            872  [Z
 115:             6            864  java.text.DecimalFormat
 116:             9            864  sun.util.calendar.Gregorian$Date
 117:            15            840  java.util.ResourceBundle$CacheKey
 118:            35            840  sun.reflect.generics.scope.MethodScope
 119:            21            840  sun.util.locale.BaseLocale$Key
 120:             5            824  [D
 121:            17            816  java.util.zip.Inflater
 122:            20            800  ch.qos.logback.core.status.InfoStatus
 123:            50            800  sun.reflect.DelegatingMethodAccessorImpl
 124:             7            784  java.util.GregorianCalendar
 125:            22            752  [Ljava.io.ObjectStreamField;
 126:            47            752  java.util.Collections$UnmodifiableSet
 127:            47            752  java.util.HashMap$KeySet
 128:            15            744  [Ljava.beans.PropertyDescriptor;
 129:             5            720  [[I
 130:            15            720  java.beans.BeanDescriptor
 131:            15            720  java.util.ResourceBundle$BundleReference
 132:            45            720  java.util.jar.Attributes
 133:            18            720  sun.nio.cs.UTF_8$Decoder
 134:            30            720  sun.reflect.generics.tree.FormalTypeParameter
 135:            45            720  sun.reflect.generics.tree.TypeVariableSignature
 136:            22            704  java.io.File
 137:            44            704  java.lang.ref.ReferenceQueue$Lock
 138:            22            704  java.util.zip.ZipCoder
 139:            28            672  java.security.Provider$UString
 140:            21            672  java.util.Locale
 141:            21            672  sun.util.locale.BaseLocale
 142:            35            656  [Lsun.reflect.generics.tree.TypeSignature;
 143:            16            640  ch.qos.logback.core.joran.event.StartEvent
 144:            13            624  java.util.Properties
 145:            19            608  java.util.PropertyPermission
 146:            15            600  java.beans.GenericBeanInfo
 147:            18            576  java.io.FileInputStream
 148:            34            544  ch.qos.logback.core.joran.spi.ElementSelector
 149:            22            528  java.util.ArrayDeque
 150:            13            520  java.security.AccessControlContext
 151:            16            512  ch.qos.logback.core.joran.event.EndEvent
 152:            16            512  sun.reflect.generics.reflectiveObjects.WildcardTypeImpl
 153:            21            504  java.util.Locale$LocaleKey
 154:            15            480  java.util.ResourceBundle$LoaderReference
 155:             5            464  [Ljava.lang.ThreadLocal$ThreadLocalMap$Entry;
 156:            19            456  java.lang.RuntimePermission
 157:            14            448  com.sun.org.apache.xml.internal.dtm.ref.ExtendedType
 158:            14            448  java.lang.ThreadLocal$ThreadLocalMap$Entry
 159:            14            448  java.security.CodeSource
 160:            11            440  java.security.ProtectionDomain
 161:             3            432  [[Ljava.lang.Object;
 162:            18            432  java.text.DateFormat$Field
 163:             6            432  org.apache.ibatis.mapping.ResultMapping
 164:            18            432  sun.misc.MetaIndex
 165:            17            408  com.sun.org.apache.xerces.internal.dom.AttributeMap
 166:            17            408  java.util.zip.ZStreamRef
 167:            16            384  ch.qos.logback.core.spi.ContextAwareBase
 168:             1            384  com.intellij.rt.execution.application.AppMainV2$1
 169:             1            384  java.lang.ref.Finalizer$FinalizerThread
 170:             6            384  java.nio.DirectByteBuffer
 171:             6            384  java.text.DateFormatSymbols
 172:             6            384  java.text.DecimalFormatSymbols
 173:             4            384  org.apache.ibatis.mapping.MappedStatement
 174:            16            384  org.xml.sax.helpers.AttributesImpl
 175:            16            384  sun.reflect.generics.tree.Wildcard
 176:             8            384  sun.util.locale.provider.LocaleResources$ResourceReference
 177:             1            376  java.lang.ref.Reference$ReferenceHandler
 178:             9            360  com.sun.org.apache.xerces.internal.utils.XMLSecurityManager$Limit
 179:             2            352  [Lorg.apache.ibatis.type.JdbcType;
 180:            11            352  java.util.Stack
 181:             6            336  java.nio.DirectLongBufferU
 182:            21            336  org.apache.ibatis.reflection.invoker.SetFieldInvoker
 183:            10            320  java.lang.OutOfMemoryError
 184:            10            320  java.security.Permissions
 185:             5            320  java.text.SimpleDateFormat
 186:            10            320  java.util.concurrent.locks.ReentrantLock$NonfairSync
 187:            20            320  org.apache.ibatis.reflection.invoker.GetFieldInvoker
 188:            10            320  sun.security.jca.ProviderConfig
 189:            13            312  org.apache.ibatis.ognl.internal.ClassCacheImpl
 190:            12            288  ch.qos.logback.core.joran.spi.HostClassAndPropertyDouble
 191:            12            288  ch.qos.logback.core.pattern.LiteralConverter
 192:             9            288  java.net.InetAddress$InetAddressHolder
 193:             6            288  java.util.TreeMap
 194:             9            288  java.util.Vector
 195:             6            288  org.apache.ibatis.session.Configuration$StrictMap
 196:            17            272  ch.qos.logback.core.joran.spi.ElementPath
 197:             1            264  com.mysql.jdbc.JDBC42PreparedStatement
 198:            11            264  sun.reflect.annotation.AnnotationInvocationHandler
 199:             1            256  com.mysql.jdbc.MysqlIO
 200:             8            256  java.io.FilePermission
 201:             8            256  java.security.BasicPermissionCollection
 202:             8            256  sun.misc.ProxyGenerator$PrimitiveTypeInfo
 203:            10            240  com.sun.org.apache.xerces.internal.impl.XMLScanner$NameType
 204:             2            240  java.net.SocksSocketImpl
 205:             6            240  java.text.DigitList
 206:             5            240  java.util.Hashtable
 207:            15            240  sun.reflect.generics.tree.ArrayTypeSignature
 208:             7            224  java.util.Collections$UnmodifiableMap
 209:             7            224  java.util.RegularEnumSet
 210:             7            216  [Ljava.lang.Boolean;
 211:             9            216  ch.qos.logback.core.rolling.helper.PeriodicityType
 212:             3            216  com.mysql.jdbc.ConnectionPropertiesImpl$MemorySizeConnectionProperty
 213:             9            216  java.io.FilePermissionCollection
 214:             2            200  [Ljava.text.DateFormat$Field;
 215:             1            200  com.sun.org.apache.xerces.internal.dom.DeferredDocumentImpl
 216:             6            192  java.lang.reflect.WeakCache$CacheValue
 217:             8            192  java.math.RoundingMode
 218:             8            192  java.net.NetPermission
 219:             8            192  java.util.jar.Manifest
 220:             3            192  org.apache.ibatis.mapping.ResultMap
 221:            11            176  [Ljava.security.Principal;
 222:             1            176  [Ljava.sql.JDBCType;
 223:            11            176  com.sun.proxy.$Proxy1
 224:             2            176  java.net.DualStackPlainSocketImpl
 225:            11            176  java.security.ProtectionDomain$Key
 226:            11            176  java.text.NumberFormat$Field
 227:            11            176  org.apache.ibatis.logging.slf4j.Slf4jImpl
 228:            11            176  org.apache.ibatis.logging.slf4j.Slf4jLocationAwareLoggerImpl
 229:            11            176  sun.reflect.generics.reflectiveObjects.GenericArrayTypeImpl
 230:             1            168  [[Ljava.math.BigInteger;
 231:             7            168  ch.qos.logback.classic.Level
 232:             7            168  com.sun.org.apache.xerces.internal.util.FeatureState
 233:             7            168  java.util.Date
 234:             1            168  org.apache.ibatis.session.Configuration
 235:             2            160  [[Ljava.lang.String;
 236:             5            160  ch.qos.logback.core.joran.event.BodyEvent
 237:             5            160  ch.qos.logback.core.util.CachingDateFormatter
 238:             5            160  com.sun.org.apache.xpath.internal.objects.XNumber
 239:             4            160  java.lang.ClassLoader$NativeLibrary
 240:            10            160  java.lang.ThreadLocal
 241:             5            160  java.lang.reflect.Proxy$Key1
 242:            10            160  java.util.concurrent.locks.ReentrantLock
 243:             2            160  sun.net.www.protocol.jar.URLJarFile
 244:             5            160  sun.util.locale.provider.LocaleProviderAdapter$Type
 245:             2            144  [Ljava.math.BigDecimal;
 246:             6            144  com.sun.org.apache.xerces.internal.util.Status
 247:             3            144  java.nio.HeapByteBuffer
 248:             6            144  java.util.concurrent.CopyOnWriteArrayList
 249:             6            144  java.util.concurrent.atomic.AtomicLong
 250:             6            144  org.apache.ibatis.mapping.SqlCommandType
 251:             3            144  org.apache.ibatis.reflection.Reflector
 252:             6            144  sun.misc.PerfCounter
 253:             3            144  sun.misc.URLClassPath
 254:             3            144  sun.nio.cs.US_ASCII$Decoder
 255:             2            128  [F
 256:             2            128  ch.qos.logback.classic.PatternLayout
 257:             2            128  java.io.ExpiringCache$1
 258:             4            128  java.io.FileOutputStream
 259:             4            128  java.net.Inet6Address
 260:             4            128  java.net.Inet6Address$Inet6AddressHolder
 261:             2            128  sun.nio.cs.ext.DoubleByte$Encoder
 262:             5            120  ch.qos.logback.core.pattern.parser.TokenStream$TokenizerState
 263:             1            120  ch.qos.logback.core.rolling.helper.RollingCalendar
 264:             5            120  ch.qos.logback.core.subst.Token$Type
 265:             5            120  ch.qos.logback.core.util.AggregationType
 266:             5            120  com.mysql.jdbc.StringUtils$SearchMode
 267:             5            120  com.sun.org.apache.xerces.internal.util.PropertyState
 268:             5            120  com.sun.org.apache.xerces.internal.utils.XMLSecurityManager$State
 269:             5            120  com.sun.org.apache.xerces.internal.utils.XMLSecurityPropertyManager$State
 270:             5            120  java.lang.ThreadLocal$ThreadLocalMap
 271:             5            120  java.net.Inet4Address
 272:             5            120  javax.xml.namespace.QName
 273:             5            120  jdk.xml.internal.JdkXmlFeatures$State
 274:             5            120  org.apache.ibatis.type.StringTypeHandler
 275:             3            120  sun.misc.FloatingDecimal$BinaryToASCIIBuffer
 276:             5            120  sun.misc.FloatingDecimal$PreparedASCIIToBinaryBuffer
 277:             5            120  sun.reflect.generics.repository.FieldRepository
 278:             2            112  ch.qos.logback.classic.encoder.PatternLayoutEncoder
 279:             2            112  java.net.SocketPermission
 280:             2            112  org.apache.ibatis.mapping.ParameterMapping
 281:             2            104  [Lch.qos.logback.core.rolling.helper.PeriodicityType;
 282:             1             96  [[J
 283:             1             96  ch.qos.logback.classic.LoggerContext
 284:             2             96  ch.qos.logback.classic.pattern.DateConverter
 285:             2             96  ch.qos.logback.classic.pattern.ExtendedThrowableProxyConverter
 286:             3             96  ch.qos.logback.core.joran.action.AppenderRefAction
 287:             4             96  ch.qos.logback.core.pattern.parser.Token
 288:             2             96  ch.qos.logback.core.rolling.helper.DateTokenConverter
 289:             4             96  ch.qos.logback.core.subst.Token
 290:             3             96  com.mysql.jdbc.Buffer
 291:             4             96  com.mysql.jdbc.authentication.CachingSha2PasswordPlugin$AuthStage
 292:             3             96  com.sun.org.apache.xerces.internal.utils.XMLSecurityManager$NameMap
 293:             4             96  java.io.BufferedOutputStream
 294:             3             96  java.lang.StringCoding$StringEncoder
 295:             2             96  java.lang.ThreadGroup
 296:             4             96  java.math.MathContext
 297:             2             96  java.net.SocketInputStream
 298:             4             96  java.sql.SQLPermission
 299:             4             96  org.apache.ibatis.mapping.ParameterMap
 300:             6             96  org.apache.ibatis.scripting.xmltags.StaticTextSqlNode
 301:             4             96  org.apache.ibatis.type.BigDecimalTypeHandler
 302:             4             96  org.apache.ibatis.type.BlobTypeHandler
 303:             4             96  org.apache.ibatis.type.BooleanTypeHandler
 304:             4             96  org.apache.ibatis.type.ClobTypeHandler
 305:             4             96  org.apache.ibatis.type.NStringTypeHandler
 306:             1             96  sun.misc.Launcher$AppClassLoader
 307:             3             96  sun.net.spi.DefaultProxySelector$NonProxyInfo
 308:             2             96  sun.nio.cs.StreamEncoder
 309:             1             96  sun.security.jca.ProviderList$1
 310:             1             96  sun.security.provider.Sun
 311:             3             96  sun.util.locale.provider.LocaleServiceProviderPool
 312:             1             88  com.sun.org.apache.xerces.internal.dom.DeferredDocumentTypeImpl
 313:             1             88  org.apache.ibatis.datasource.pooled.PoolState
 314:             1             88  sun.misc.Launcher$ExtClassLoader
 315:             2             80  [Lcom.mysql.jdbc.StringUtils$SearchMode;
 316:             2             80  [Lorg.apache.ibatis.mapping.SqlCommandType;
 317:             2             80  ch.qos.logback.classic.pattern.LoggerConverter
 318:             1             80  ch.qos.logback.core.rolling.RollingFileAppender
 319:             1             80  ch.qos.logback.core.rolling.TimeBasedRollingPolicy
 320:             5             80  ch.qos.logback.core.spi.LogbackLock
 321:             2             80  java.io.BufferedInputStream
 322:             2             80  java.io.BufferedWriter
 323:             2             80  java.io.ExpiringCache
 324:             2             80  java.util.Locale$Category
 325:             1             80  java.util.concurrent.ThreadPoolExecutor
 326:             2             80  jdk.xml.internal.JdkXmlFeatures$XmlFeature
 327:             1             72  [Lcom.sun.org.apache.xml.internal.dtm.ref.ExtendedType;
 328:             2             72  [Lsun.security.jca.ProviderConfig;
 329:             1             72  ch.qos.logback.core.ConsoleAppender
 330:             3             72  ch.qos.logback.core.joran.action.ActionUtil$Scope
 331:             3             72  ch.qos.logback.core.joran.action.NOPAction
 332:             3             72  ch.qos.logback.core.joran.action.PropertyAction
 333:             3             72  ch.qos.logback.core.rolling.helper.CompressionMode
 334:             3             72  ch.qos.logback.core.spi.FilterReply
 335:             3             72  ch.qos.logback.core.subst.Tokenizer$TokenizerState
 336:             1             72  com.mysql.jdbc.PreparedStatement$ParseInfo
 337:             3             72  com.sun.org.apache.xerces.internal.dom.NamedNodeMapImpl
 338:             3             72  java.lang.annotation.RetentionPolicy
 339:             3             72  java.net.Proxy$Type
 340:             3             72  java.security.SecurityPermission
 341:             3             72  java.util.Arrays$ArrayList
 342:             3             72  java.util.Collections$SynchronizedSet
 343:             1             72  java.util.ResourceBundle$RBClassLoader
 344:             3             72  java.util.concurrent.ConcurrentHashMap$KeySetView
 345:             3             72  java.util.concurrent.atomic.AtomicMarkableReference$Pair
 346:             3             72  java.util.concurrent.locks.AbstractQueuedSynchronizer$ConditionObject
 347:             1             72  java.util.regex.Pattern
 348:             3             72  java.util.regex.Pattern$SliceI
 349:             3             72  org.apache.ibatis.cache.impl.PerpetualCache
 350:             3             72  org.apache.ibatis.mapping.ParameterMode
 351:             3             72  org.apache.ibatis.mapping.StatementType
 352:             3             72  org.apache.ibatis.session.AutoMappingBehavior
 353:             3             72  org.apache.ibatis.session.ExecutorType
 354:             3             72  org.apache.ibatis.type.ByteTypeHandler
 355:             3             72  org.apache.ibatis.type.DoubleTypeHandler
 356:             3             72  org.apache.ibatis.type.FloatTypeHandler
 357:             3             72  org.apache.ibatis.type.IntegerTypeHandler
 358:             3             72  org.apache.ibatis.type.LongTypeHandler
 359:             3             72  org.apache.ibatis.type.ShortTypeHandler
 360:             3             72  sun.misc.FloatingDecimal$ExceptionalBinaryToASCIIBuffer
 361:             3             72  sun.security.provider.PolicyFile$PolicyEntry
 362:             1             72  sun.util.locale.provider.JRELocaleProviderAdapter
 363:             3             72  sun.util.resources.ParallelListResourceBundle$KeySet
 364:             2             64  [Ljava.lang.Thread;
 365:             2             64  [Ljava.lang.annotation.RetentionPolicy;
 366:             2             64  [Ljava.net.InetAddress;
 367:             2             64  [Ljdk.xml.internal.JdkXmlFeatures$State;
 368:             2             64  [Lorg.apache.ibatis.mapping.StatementType;
 369:             2             64  [Lorg.apache.ibatis.session.AutoMappingBehavior;
 370:             2             64  [Lorg.apache.ibatis.session.AutoMappingUnknownColumnBehavior;
 371:             2             64  [Lorg.apache.ibatis.session.ExecutorType;
 372:             2             64  ch.qos.logback.classic.joran.action.LevelAction
 373:             2             64  ch.qos.logback.classic.pattern.LevelConverter
 374:             2             64  ch.qos.logback.classic.pattern.LineSeparatorConverter
 375:             2             64  ch.qos.logback.classic.pattern.MessageConverter
 376:             2             64  ch.qos.logback.classic.pattern.ThreadConverter
 377:             2             64  ch.qos.logback.core.joran.spi.ConsoleTarget
 378:             1             64  ch.qos.logback.core.rolling.DefaultTimeBasedFileNamingAndTriggeringPolicy
 379:             2             64  ch.qos.logback.core.rolling.helper.FileNamePattern
 380:             1             64  com.mysql.jdbc.ConnectionPropertiesImpl$LongConnectionProperty
 381:             2             64  com.mysql.jdbc.JDBC4DatabaseMetaData
 382:             2             64  com.sun.org.apache.xerces.internal.dom.NodeListCache
 383:             2             64  com.sun.org.apache.xerces.internal.utils.XMLSecurityPropertyManager$Property
 384:             2             64  java.io.PrintStream
 385:             2             64  java.lang.ClassValue$Entry
 386:             2             64  java.lang.StringCoding$StringDecoder
 387:             2             64  java.lang.VirtualMachineError
 388:             2             64  java.lang.ref.ReferenceQueue$Null
 389:             2             64  java.net.Socket
 390:             2             64  java.util.Collections$SynchronizedMap
 391:             4             64  java.util.HashMap$EntrySet
 392:             4             64  java.util.concurrent.atomic.AtomicInteger
 393:             2             64  java.util.regex.Pattern$Curly
 394:             1             64  org.apache.ibatis.datasource.pooled.PooledConnection
 395:             4             64  org.apache.ibatis.scripting.xmltags.MixedSqlNode
 396:             2             64  sun.reflect.annotation.AnnotationType
 397:             2             64  sun.util.locale.provider.LocaleResources
 398:             1             56  [Lcom.sun.org.apache.xerces.internal.impl.XMLScanner$NameType;
 399:             1             56  [Lcom.sun.org.apache.xerces.internal.utils.XMLSecurityManager$Limit;
 400:             1             56  org.apache.ibatis.datasource.pooled.PooledDataSource
 401:             1             56  sun.nio.cs.US_ASCII$Encoder
 402:             1             56  sun.nio.cs.ext.DoubleByte$Decoder
 403:             1             48  [Lcom.sun.beans.util.Cache$CacheEntry;
 404:             1             48  [Ljava.beans.WeakIdentityMap$Entry;
 405:             3             48  [Ljava.lang.annotation.Annotation;
 406:             1             48  [Ljava.math.RoundingMode;
 407:             2             48  [Ljava.security.ProtectionDomain;
 408:             1             48  [Ljava.util.concurrent.TimeUnit;
 409:             2             48  [Lorg.apache.ibatis.session.LocalCacheScope;
 410:             1             48  ch.qos.logback.core.joran.action.DefinePropertyAction
 411:             1             48  ch.qos.logback.core.joran.spi.InterpretationContext
 412:             1             48  ch.qos.logback.core.joran.spi.Interpreter
 413:             2             48  ch.qos.logback.core.pattern.FormatInfo
 414:             1             48  ch.qos.logback.core.recovery.ResilientFileOutputStream
 415:             1             48  ch.qos.logback.core.rolling.helper.TimeBasedArchiveRemover
 416:             2             48  ch.qos.logback.core.subst.Node$Type
 417:             1             48  ch.qos.logback.core.util.InvocationGate
 418:             1             48  cn.wdidada.testmybatis.domain.User
 419:             3             48  com.sun.org.apache.xerces.internal.impl.dv.dtd.ListDatatypeValidator
 420:             1             48  com.sun.org.apache.xpath.internal.jaxp.XPathImpl
 421:             1             48  java.io.BufferedReader
 422:             2             48  java.io.File$PathStatus
 423:             2             48  java.io.OutputStreamWriter
 424:             3             48  java.lang.Boolean
 425:             3             48  java.lang.Byte
 426:             2             48  java.lang.Double
 427:             3             48  java.lang.Short
 428:             2             48  java.lang.StringBuilder
 429:             2             48  java.net.InetAddress$Cache
 430:             2             48  java.net.InetAddress$Cache$Type
 431:             2             48  java.net.InetAddress$CacheEntry
 432:             1             48  java.net.SocketOutputStream
 433:             1             48  java.nio.HeapCharBuffer
 434:             2             48  java.nio.charset.CoderResult
 435:             3             48  java.nio.charset.CodingErrorAction
 436:             2             48  java.sql.DriverInfo
 437:             3             48  java.text.AttributedCharacterIterator$Attribute
 438:             2             48  java.util.BitSet
 439:             3             48  java.util.LinkedHashMap$LinkedKeySet
 440:             1             48  java.util.concurrent.LinkedBlockingQueue
 441:             1             48  java.util.concurrent.ThreadPoolExecutor$Worker
 442:             3             48  java.util.concurrent.atomic.AtomicMarkableReference
 443:             2             48  java.util.regex.Pattern$GroupHead
 444:             2             48  java.util.regex.Pattern$GroupTail
 445:             2             48  org.apache.ibatis.builder.StaticSqlSource
 446:             1             48  org.apache.ibatis.datasource.unpooled.UnpooledDataSource
 447:             1             48  org.apache.ibatis.executor.ReuseExecutor
 448:             2             48  org.apache.ibatis.mapping.ResultFlag
 449:             2             48  org.apache.ibatis.reflection.DefaultReflectorFactory
 450:             2             48  org.apache.ibatis.scripting.xmltags.DynamicSqlSource
 451:             1             48  org.apache.ibatis.scripting.xmltags.ForEachSqlNode
 452:             2             48  org.apache.ibatis.session.LocalCacheScope
 453:             2             48  org.apache.ibatis.type.ArrayTypeHandler
 454:             2             48  org.apache.ibatis.type.BlobByteObjectArrayTypeHandler
 455:             2             48  org.apache.ibatis.type.CharacterTypeHandler
 456:             2             48  org.apache.ibatis.type.DateOnlyTypeHandler
 457:             2             48  org.apache.ibatis.type.DateTypeHandler
 458:             2             48  org.apache.ibatis.type.NClobTypeHandler
 459:             2             48  org.apache.ibatis.type.TimeOnlyTypeHandler
 460:             2             48  sun.misc.JarIndex
 461:             2             48  sun.misc.NativeSignalHandler
 462:             2             48  sun.misc.Signal
 463:             3             48  sun.net.www.protocol.jar.Handler
 464:             1             48  sun.nio.cs.StreamDecoder
 465:             2             48  sun.security.jca.ProviderList
 466:             2             48  sun.security.jca.ProviderList$3
 467:             1             48  sun.text.resources.FormatData
 468:             1             48  sun.text.resources.zh.FormatData_zh
 469:             1             48  sun.text.resources.zh.FormatData_zh_CN
 470:             1             48  sun.util.resources.CalendarData
 471:             1             48  sun.util.resources.CurrencyNames
 472:             1             48  sun.util.resources.TimeZoneNames
 473:             1             48  sun.util.resources.en.CalendarData_en
 474:             1             48  sun.util.resources.en.TimeZoneNames_en
 475:             1             48  sun.util.resources.zh.CalendarData_zh
 476:             1             48  sun.util.resources.zh.CurrencyNames_zh_CN
 477:             1             40  [Lch.qos.logback.core.pattern.parser.TokenStream$TokenizerState;
 478:             1             40  [Lch.qos.logback.core.subst.Token$Type;
 479:             1             40  [Lch.qos.logback.core.util.AggregationType;
 480:             1             40  [Lcom.sun.org.apache.xerces.internal.util.Status;
 481:             1             40  [Lcom.sun.org.apache.xerces.internal.utils.XMLSecurityManager$State;
 482:             1             40  [Lcom.sun.org.apache.xerces.internal.utils.XMLSecurityPropertyManager$State;
 483:             1             40  [Lsun.util.locale.provider.LocaleProviderAdapter$Type;
 484:             1             40  ch.qos.logback.core.BasicStatusManager
 485:             1             40  ch.qos.logback.core.joran.spi.ConfigurationWatchList
 486:             1             40  ch.qos.logback.core.rolling.SizeBasedTriggeringPolicy
 487:             1             40  com.mysql.jdbc.StandardSocketFactory
 488:             1             40  com.mysql.jdbc.authentication.CachingSha2PasswordPlugin
 489:             1             40  com.mysql.jdbc.util.ReadAheadInputStream
 490:             1             40  com.sun.beans.finder.MethodFinder$1
 491:             1             40  com.sun.xml.internal.stream.util.BufferAllocator
 492:             1             40  java.beans.WeakIdentityMap$Entry
 493:             1             40  java.lang.reflect.Parameter
 494:             1             40  java.lang.reflect.Proxy$Key2
 495:             1             40  java.util.EnumMap
 496:             1             40  java.util.IdentityHashMap
 497:             1             40  java.util.PropertyResourceBundle
 498:             1             40  java.util.ResourceBundle$1
 499:             1             40  javax.management.ObjectName
 500:             1             40  org.apache.ibatis.binding.MapperMethod$MethodSignature
 501:             1             40  org.apache.ibatis.cache.CacheKey
 502:             1             40  org.apache.ibatis.cache.NullCacheKey
 503:             1             40  org.apache.ibatis.logging.jdbc.PreparedStatementLogger
 504:             1             40  org.apache.ibatis.parsing.XNode
 505:             1             40  sun.nio.cs.StandardCharsets$Aliases
 506:             1             40  sun.nio.cs.StandardCharsets$Cache
 507:             1             40  sun.nio.cs.StandardCharsets$Classes
 508:             1             40  sun.nio.cs.ext.ExtendedCharsets
 509:             1             32  [Lch.qos.logback.core.joran.action.ActionUtil$Scope;
 510:             1             32  [Lch.qos.logback.core.rolling.helper.CompressionMode;
 511:             1             32  [Lch.qos.logback.core.spi.FilterReply;
 512:             1             32  [Lch.qos.logback.core.subst.Tokenizer$TokenizerState;
 513:             1             32  [Lcom.mysql.jdbc.authentication.CachingSha2PasswordPlugin$AuthStage;
 514:             1             32  [Lcom.sun.beans.util.Cache$Kind;
 515:             1             32  [Lcom.sun.org.apache.xerces.internal.utils.XMLSecurityManager$NameMap;
 516:             2             32  [Ljava.lang.Enum;
 517:             1             32  [Ljava.lang.OutOfMemoryError;
 518:             2             32  [Ljava.lang.StackTraceElement;
 519:             1             32  [Ljava.lang.ThreadGroup;
 520:             1             32  [Ljava.net.Proxy$Type;
 521:             1             32  [Ljava.util.regex.Pattern$Node;
 522:             1             32  [Lorg.apache.ibatis.mapping.ParameterMode;
 523:             1             32  ch.qos.logback.classic.joran.JoranConfigurator
 524:             1             32  ch.qos.logback.classic.joran.action.ConfigurationAction
 525:             1             32  ch.qos.logback.classic.joran.action.EvaluatorAction
 526:             1             32  ch.qos.logback.classic.joran.action.LoggerAction
 527:             1             32  ch.qos.logback.classic.joran.action.LoggerContextListenerAction
 528:             1             32  ch.qos.logback.classic.joran.action.ReceiverAction
 529:             1             32  ch.qos.logback.classic.joran.action.RootLoggerAction
 530:             2             32  ch.qos.logback.classic.pattern.EnsureExceptionHandling
 531:             2             32  ch.qos.logback.classic.pattern.TargetLengthBasedClassNameAbbreviator
 532:             1             32  ch.qos.logback.classic.sift.SiftAction
 533:             1             32  ch.qos.logback.classic.spi.LoggerContextVO
 534:             1             32  ch.qos.logback.core.helpers.CyclicBuffer
 535:             1             32  ch.qos.logback.core.joran.action.AppenderAction
 536:             1             32  ch.qos.logback.core.joran.action.ConversionRuleAction
 537:             1             32  ch.qos.logback.core.joran.action.IncludeAction
 538:             1             32  ch.qos.logback.core.joran.action.NestedBasicPropertyIA
 539:             1             32  ch.qos.logback.core.joran.action.NestedComplexPropertyIA
 540:             1             32  ch.qos.logback.core.joran.action.NewRuleAction
 541:             1             32  ch.qos.logback.core.joran.action.ParamAction
 542:             1             32  ch.qos.logback.core.joran.action.StatusListenerAction
 543:             1             32  ch.qos.logback.core.joran.action.TimestampAction
 544:             1             32  ch.qos.logback.core.joran.conditional.ElseAction
 545:             1             32  ch.qos.logback.core.joran.conditional.IfAction
 546:             1             32  ch.qos.logback.core.joran.conditional.ThenAction
 547:             1             32  ch.qos.logback.core.joran.spi.SimpleRuleStore
 548:             1             32  ch.qos.logback.core.rolling.helper.Compressor
 549:             2             32  ch.qos.logback.core.spi.FilterAttachableImpl
 550:             1             32  com.mysql.jdbc.NonRegisteringDriver$ConnectionPhantomReference
 551:             1             32  com.mysql.jdbc.authentication.Sha256PasswordPlugin
 552:             2             32  com.sun.beans.WeakCache
 553:             1             32  com.sun.beans.finder.BeanInfoFinder
 554:             1             32  com.sun.org.apache.xerces.internal.impl.XMLEntityScanner$1
 555:             2             32  com.sun.org.apache.xerces.internal.impl.dv.dtd.ENTITYDatatypeValidator
 556:             1             32  com.sun.org.apache.xerces.internal.jaxp.SAXParserFactoryImpl
 557:             1             32  java.beans.ThreadGroupContext
 558:             1             32  java.beans.ThreadGroupContext$1
 559:             1             32  java.io.WinNTFileSystem
 560:             1             32  java.lang.ArithmeticException
 561:             1             32  java.lang.ArrayIndexOutOfBoundsException
 562:             2             32  java.lang.Character
 563:             2             32  java.lang.Float
 564:             2             32  java.lang.InheritableThreadLocal
 565:             1             32  java.lang.NullPointerException
 566:             1             32  java.lang.reflect.WeakCache
 567:             1             32  java.lang.reflect.WeakCache$CacheKey
 568:             2             32  java.nio.ByteOrder
 569:             1             32  java.text.DontCareFieldPosition
 570:             1             32  java.util.Collections$UnmodifiableSortedMap
 571:             2             32  java.util.HashMap$Values
 572:             2             32  java.util.Hashtable$EntrySet
 573:             2             32  java.util.LinkedHashMap$LinkedEntrySet
 574:             1             32  java.util.Random
 575:             2             32  java.util.concurrent.atomic.AtomicBoolean
 576:             1             32  java.util.concurrent.atomic.AtomicReferenceFieldUpdater$AtomicReferenceFieldUpdaterImpl
 577:             1             32  java.util.regex.Pattern$3
 578:             1             32  java.util.regex.Pattern$Branch
 579:             2             32  javax.xml.xpath.SecuritySupport
 580:             1             32  org.apache.ibatis.cache.decorators.LoggingCache
 581:             1             32  org.apache.ibatis.cache.decorators.ScheduledCache
 582:             2             32  org.apache.ibatis.ognl.OgnlRuntime$ClassPropertyMethodCache
 583:             1             32  org.apache.ibatis.parsing.XPathParser
 584:             1             32  org.apache.ibatis.reflection.MetaObject
 585:             2             32  org.apache.ibatis.reflection.factory.DefaultObjectFactory
 586:             2             32  org.apache.ibatis.reflection.wrapper.DefaultObjectWrapperFactory
 587:             2             32  org.apache.ibatis.scripting.defaults.RawSqlSource
 588:             2             32  org.apache.ibatis.scripting.xmltags.ExpressionEvaluator
 589:             1             32  org.apache.ibatis.session.defaults.DefaultSqlSession
 590:             1             32  org.apache.ibatis.transaction.jdbc.JdbcTransaction
 591:             1             32  org.apache.ibatis.type.TypeHandlerRegistry
 592:             1             32  sun.instrument.InstrumentationImpl
 593:             1             32  sun.nio.cs.StandardCharsets
 594:             1             32  sun.security.provider.PolicyFile
 595:             1             32  sun.security.provider.PolicyFile$PolicyInfo
 596:             1             24  [Lch.qos.logback.core.joran.spi.ConsoleTarget;
 597:             1             24  [Lch.qos.logback.core.subst.Node$Type;
 598:             1             24  [Lcom.sun.org.apache.xerces.internal.utils.XMLSecurityPropertyManager$Property;
 599:             1             24  [Ljava.io.File$PathStatus;
 600:             1             24  [Ljava.io.InputStream;
 601:             1             24  [Ljava.lang.ClassValue$Entry;
 602:             1             24  [Ljava.lang.reflect.Parameter;
 603:             1             24  [Ljava.net.InetAddress$Cache$Type;
 604:             1             24  [Ljava.util.Locale$Category;
 605:             1             24  [Ljdk.xml.internal.JdkXmlFeatures$XmlFeature;
 606:             1             24  [Lorg.apache.ibatis.executor.ExecutionPlaceholder;
 607:             1             24  [Lorg.apache.ibatis.mapping.ResultFlag;
 608:             1             24  [Lorg.apache.ibatis.ognl.internal.ClassCache;
 609:             1             24  [Lsun.launcher.LauncherHelper;
 610:             1             24  [Lsun.misc.JavaSecurityProtectionDomainAccess$ProtectionDomainCache;
 611:             1             24  ch.qos.logback.classic.joran.action.ConsolePluginAction
 612:             1             24  ch.qos.logback.classic.joran.action.ContextNameAction
 613:             1             24  ch.qos.logback.classic.joran.action.InsertFromJNDIAction
 614:             1             24  ch.qos.logback.classic.joran.action.JMXConfiguratorAction
 615:             1             24  ch.qos.logback.classic.spi.TurboFilterList
 616:             1             24  ch.qos.logback.classic.util.ContextSelectorStaticBinder
 617:             1             24  ch.qos.logback.classic.util.LogbackMDCAdapter
 618:             1             24  ch.qos.logback.core.joran.action.ContextPropertyAction
 619:             1             24  ch.qos.logback.core.joran.spi.CAI_WithLocatorSupport
 620:             1             24  ch.qos.logback.core.joran.spi.EventPlayer
 621:             1             24  ch.qos.logback.core.rolling.helper.RenameUtil
 622:             1             24  ch.qos.logback.core.util.FileSize
 623:             1             24  com.mysql.jdbc.NetworkResources
 624:             1             24  com.mysql.jdbc.SingleByteCharsetConverter
 625:             1             24  com.mysql.jdbc.authentication.MysqlClearPasswordPlugin
 626:             1             24  com.mysql.jdbc.authentication.MysqlNativePasswordPlugin
 627:             1             24  com.mysql.jdbc.authentication.MysqlOldPasswordPlugin
 628:             1             24  com.sun.beans.util.Cache$Kind$1
 629:             1             24  com.sun.beans.util.Cache$Kind$2
 630:             1             24  com.sun.beans.util.Cache$Kind$3
 631:             1             24  com.sun.org.apache.xerces.internal.impl.Constants$ArrayEnumeration
 632:             1             24  java.io.InputStreamReader
 633:             1             24  java.lang.ClassValue$Version
 634:             1             24  java.lang.invoke.MethodHandleImpl$4
 635:             1             24  java.lang.reflect.ReflectPermission
 636:             1             24  java.net.Inet6AddressImpl
 637:             1             24  java.net.Proxy
 638:             1             24  java.net.SocketPermissionCollection
 639:             1             24  java.security.Policy$PolicyInfo
 640:             1             24  java.security.Policy$UnsupportedEmptyCollection
 641:             1             24  java.security.ProtectionDomain$2$1
 642:             1             24  java.util.Collections$EmptyMap
 643:             1             24  java.util.Collections$SetFromMap
 644:             1             24  java.util.Collections$SynchronizedRandomAccessList
 645:             1             24  java.util.Currency
 646:             1             24  java.util.Locale$Cache
 647:             1             24  java.util.PropertyPermissionCollection
 648:             1             24  java.util.ResourceBundle$Control$CandidateListCache
 649:             1             24  java.util.concurrent.ConcurrentLinkedQueue
 650:             1             24  java.util.concurrent.ConcurrentLinkedQueue$Node
 651:             1             24  java.util.concurrent.LinkedBlockingQueue$Node
 652:             1             24  java.util.concurrent.TimeUnit$1
 653:             1             24  java.util.concurrent.TimeUnit$2
 654:             1             24  java.util.concurrent.TimeUnit$3
 655:             1             24  java.util.concurrent.TimeUnit$4
 656:             1             24  java.util.concurrent.TimeUnit$5
 657:             1             24  java.util.concurrent.TimeUnit$6
 658:             1             24  java.util.concurrent.TimeUnit$7
 659:             1             24  java.util.regex.Pattern$Ctype
 660:             1             24  java.util.regex.Pattern$Ques
 661:             1             24  java.util.regex.Pattern$SingleI
 662:             1             24  java.util.regex.Pattern$Start
 663:             1             24  jdk.xml.internal.JdkXmlFeatures
 664:             1             24  org.apache.ibatis.binding.MapperMethod
 665:             1             24  org.apache.ibatis.binding.MapperMethod$SqlCommand
 666:             1             24  org.apache.ibatis.binding.MapperProxy
 667:             1             24  org.apache.ibatis.binding.MapperProxyFactory
 668:             1             24  org.apache.ibatis.binding.MapperRegistry
 669:             1             24  org.apache.ibatis.cache.decorators.FifoCache
 670:             1             24  org.apache.ibatis.executor.ExecutionPlaceholder
 671:             1             24  org.apache.ibatis.io.ClassLoaderWrapper
 672:             1             24  org.apache.ibatis.javassist.util.proxy.ProxyFactory$2
 673:             1             24  org.apache.ibatis.mapping.Environment
 674:             1             24  org.apache.ibatis.ognl.OgnlRuntime$ArgsCompatbilityReport
 675:             1             24  org.apache.ibatis.ognl.enhance.ExpressionCompiler
 676:             1             24  org.apache.ibatis.reflection.MetaClass
 677:             1             24  org.apache.ibatis.reflection.ParamNameResolver
 678:             1             24  org.apache.ibatis.reflection.wrapper.BeanWrapper
 679:             1             24  org.apache.ibatis.scripting.LanguageDriverRegistry
 680:             1             24  org.apache.ibatis.scripting.xmltags.IfSqlNode
 681:             1             24  org.apache.ibatis.session.AutoMappingUnknownColumnBehavior$1
 682:             1             24  org.apache.ibatis.session.AutoMappingUnknownColumnBehavior$2
 683:             1             24  org.apache.ibatis.session.AutoMappingUnknownColumnBehavior$3
 684:             1             24  org.apache.ibatis.session.RowBounds
 685:             1             24  org.apache.ibatis.type.BigIntegerTypeHandler
 686:             1             24  org.apache.ibatis.type.BlobInputStreamTypeHandler
 687:             1             24  org.apache.ibatis.type.ByteArrayTypeHandler
 688:             1             24  org.apache.ibatis.type.ByteObjectArrayTypeHandler
 689:             1             24  org.apache.ibatis.type.ClobReaderTypeHandler
 690:             1             24  org.apache.ibatis.type.InstantTypeHandler
 691:             1             24  org.apache.ibatis.type.JapaneseDateTypeHandler
 692:             1             24  org.apache.ibatis.type.LocalDateTimeTypeHandler
 693:             1             24  org.apache.ibatis.type.LocalDateTypeHandler
 694:             1             24  org.apache.ibatis.type.LocalTimeTypeHandler
 695:             1             24  org.apache.ibatis.type.MonthTypeHandler
 696:             1             24  org.apache.ibatis.type.ObjectTypeHandler
 697:             1             24  org.apache.ibatis.type.OffsetDateTimeTypeHandler
 698:             1             24  org.apache.ibatis.type.OffsetTimeTypeHandler
 699:             1             24  org.apache.ibatis.type.SqlDateTypeHandler
 700:             1             24  org.apache.ibatis.type.SqlTimeTypeHandler
 701:             1             24  org.apache.ibatis.type.SqlTimestampTypeHandler
 702:             1             24  org.apache.ibatis.type.UnknownTypeHandler
 703:             1             24  org.apache.ibatis.type.YearMonthTypeHandler
 704:             1             24  org.apache.ibatis.type.YearTypeHandler
 705:             1             24  org.apache.ibatis.type.ZonedDateTimeTypeHandler
 706:             1             24  org.slf4j.helpers.BasicMarker
 707:             1             24  org.slf4j.helpers.FormattingTuple
 708:             1             24  org.slf4j.impl.StaticLoggerBinder
 709:             1             24  sun.instrument.TransformerManager
 710:             1             24  sun.launcher.LauncherHelper
 711:             1             24  sun.misc.URLClassPath$FileLoader
 712:             1             24  sun.net.ProgressMonitor
 713:             1             24  sun.nio.cs.IBM437
 714:             1             24  sun.nio.cs.IBM850
 715:             1             24  sun.nio.cs.IBM852
 716:             1             24  sun.nio.cs.IBM866
 717:             1             24  sun.nio.cs.ISO_8859_1
 718:             1             24  sun.nio.cs.ISO_8859_13
 719:             1             24  sun.nio.cs.ISO_8859_2
 720:             1             24  sun.nio.cs.ISO_8859_7
 721:             1             24  sun.nio.cs.ISO_8859_9
 722:             1             24  sun.nio.cs.KOI8_R
 723:             1             24  sun.nio.cs.MS1250
 724:             1             24  sun.nio.cs.MS1251
 725:             1             24  sun.nio.cs.MS1252
 726:             1             24  sun.nio.cs.MS1257
 727:             1             24  sun.nio.cs.Surrogate$Parser
 728:             1             24  sun.nio.cs.ThreadLocalCoders$1
 729:             1             24  sun.nio.cs.ThreadLocalCoders$2
 730:             1             24  sun.nio.cs.US_ASCII
 731:             1             24  sun.nio.cs.UTF_16
 732:             1             24  sun.nio.cs.UTF_16BE
 733:             1             24  sun.nio.cs.UTF_16LE
 734:             1             24  sun.nio.cs.UTF_32
 735:             1             24  sun.nio.cs.UTF_8
 736:             1             24  sun.nio.cs.ext.Big5
 737:             1             24  sun.nio.cs.ext.EUC_CN
 738:             1             24  sun.nio.cs.ext.EUC_JP
 739:             1             24  sun.nio.cs.ext.EUC_JP_Open
 740:             1             24  sun.nio.cs.ext.EUC_KR
 741:             1             24  sun.nio.cs.ext.GB18030
 742:             1             24  sun.nio.cs.ext.GBK
 743:             1             24  sun.nio.cs.ext.IBM943
 744:             1             24  sun.nio.cs.ext.ISO_8859_8
 745:             1             24  sun.nio.cs.ext.MS1256
 746:             1             24  sun.nio.cs.ext.MS932
 747:             1             24  sun.nio.cs.ext.MacCentralEurope
 748:             1             24  sun.nio.cs.ext.MacRoman
 749:             1             24  sun.nio.cs.ext.SJIS
 750:             1             24  sun.nio.cs.ext.TIS_620
 751:             1             24  sun.util.locale.BaseLocale$Cache
 752:             1             24  sun.util.locale.provider.CalendarDataProviderImpl
 753:             1             24  sun.util.locale.provider.CalendarProviderImpl
 754:             1             24  sun.util.locale.provider.CurrencyNameProviderImpl
 755:             1             24  sun.util.locale.provider.DateFormatSymbolsProviderImpl
 756:             1             24  sun.util.locale.provider.DecimalFormatSymbolsProviderImpl
 757:             1             24  sun.util.locale.provider.NumberFormatProviderImpl
 758:             1             24  sun.util.locale.provider.TimeZoneNameProviderImpl
 759:             1             16  [Ljava.beans.EventSetDescriptor;
 760:             1             16  [Ljava.lang.Throwable;
 761:             1             16  [Ljava.security.Provider;
 762:             1             16  [Ljava.security.cert.Certificate;
 763:             1             16  [Ljava.text.FieldPosition;
 764:             1             16  [Ljavax.management.ObjectName$Property;
 765:             1             16  [Lsun.instrument.TransformerManager$TransformerInfo;
 766:             1             16  ch.qos.logback.classic.selector.DefaultContextSelector
 767:             1             16  ch.qos.logback.core.joran.spi.ConsoleTarget$1
 768:             1             16  ch.qos.logback.core.joran.spi.ConsoleTarget$2
 769:             1             16  ch.qos.logback.core.joran.spi.DefaultNestedComponentRegistry
 770:             1             16  ch.qos.logback.core.joran.util.ConfigurationWatchListUtil
 771:             1             16  ch.qos.logback.core.spi.AppenderAttachableImpl
 772:             1             16  cn.wdidada.testmybatis.TestMyBatis
 773:             1             16  com.mysql.fabric.jdbc.FabricMySQLDriver
 774:             1             16  com.mysql.jdbc.AbandonedConnectionCleanupThread
 775:             1             16  com.mysql.jdbc.AbandonedConnectionCleanupThread$1
 776:             1             16  com.mysql.jdbc.Driver
 777:             1             16  com.mysql.jdbc.Util
 778:             1             16  com.mysql.jdbc.log.NullLogger
 779:             1             16  com.mysql.jdbc.log.StandardLogger
 780:             1             16  com.sun.org.apache.xerces.internal.dom.CharacterDataImpl$1
 781:             1             16  com.sun.org.apache.xerces.internal.dom.DeferredDocumentImpl$RefCount
 782:             1             16  com.sun.org.apache.xerces.internal.impl.dv.dtd.IDDatatypeValidator
 783:             1             16  com.sun.org.apache.xerces.internal.impl.dv.dtd.IDREFDatatypeValidator
 784:             1             16  com.sun.org.apache.xerces.internal.impl.dv.dtd.NMTOKENDatatypeValidator
 785:             1             16  com.sun.org.apache.xerces.internal.impl.dv.dtd.NOTATIONDatatypeValidator
 786:             1             16  com.sun.org.apache.xerces.internal.impl.dv.dtd.StringDatatypeValidator
 787:             1             16  com.sun.org.apache.xerces.internal.utils.SecuritySupport
 788:             1             16  com.sun.org.apache.xpath.internal.objects.EqualComparator
 789:             1             16  com.sun.org.apache.xpath.internal.objects.GreaterThanComparator
 790:             1             16  com.sun.org.apache.xpath.internal.objects.GreaterThanOrEqualComparator
 791:             1             16  com.sun.org.apache.xpath.internal.objects.LessThanComparator
 792:             1             16  com.sun.org.apache.xpath.internal.objects.LessThanOrEqualComparator
 793:             1             16  com.sun.org.apache.xpath.internal.objects.NotEqualComparator
 794:             1             16  com.sun.org.apache.xpath.internal.objects.XMLStringFactoryImpl
 795:             1             16  com.sun.proxy.$Proxy2
 796:             1             16  com.sun.proxy.$Proxy3
 797:             1             16  com.sun.proxy.$Proxy4
 798:             1             16  java.io.FileDescriptor$1
 799:             1             16  java.lang.CharacterDataLatin1
 800:             1             16  java.lang.ClassValue$Identity
 801:             1             16  java.lang.Runtime
 802:             1             16  java.lang.String$CaseInsensitiveComparator
 803:             1             16  java.lang.System$2
 804:             1             16  java.lang.Terminator$1
 805:             1             16  java.lang.invoke.MemberName$Factory
 806:             1             16  java.lang.invoke.MethodHandleImpl$2
 807:             1             16  java.lang.invoke.MethodHandleImpl$3
 808:             1             16  java.lang.ref.Reference$1
 809:             1             16  java.lang.ref.Reference$Lock
 810:             1             16  java.lang.reflect.Proxy$KeyFactory
 811:             1             16  java.lang.reflect.Proxy$ProxyClassFactory
 812:             1             16  java.lang.reflect.ReflectAccess
 813:             1             16  java.math.BigDecimal$1
 814:             1             16  java.net.InetAddress$2
 815:             1             16  java.net.URLClassLoader$7
 816:             1             16  java.nio.Bits$1
 817:             1             16  java.nio.charset.CoderResult$1
 818:             1             16  java.nio.charset.CoderResult$2
 819:             1             16  java.security.AllPermission
 820:             1             16  java.security.ProtectionDomain$2
 821:             1             16  java.security.ProtectionDomain$JavaSecurityAccessImpl
 822:             1             16  java.text.DontCareFieldPosition$1
 823:             1             16  java.text.MessageFormat$Field
 824:             1             16  java.util.Collections$EmptyIterator
 825:             1             16  java.util.Collections$EmptyList
 826:             1             16  java.util.Collections$EmptySet
 827:             1             16  java.util.Collections$UnmodifiableMap$UnmodifiableEntrySet
 828:             1             16  java.util.Currency$CurrencyNameGetter
 829:             1             16  java.util.EnumMap$1
 830:             1             16  java.util.Hashtable$KeySet
 831:             1             16  java.util.ResourceBundle$Control
 832:             1             16  java.util.WeakHashMap$KeySet
 833:             1             16  java.util.concurrent.Executors$FinalizableDelegatedExecutorService
 834:             1             16  java.util.concurrent.ThreadPoolExecutor$AbortPolicy
 835:             1             16  java.util.concurrent.atomic.AtomicReference
 836:             1             16  java.util.jar.JavaUtilJarAccessImpl
 837:             1             16  java.util.regex.Pattern$4
 838:             1             16  java.util.regex.Pattern$BranchConn
 839:             1             16  java.util.regex.Pattern$LastNode
 840:             1             16  java.util.regex.Pattern$Node
 841:             1             16  java.util.zip.ZipFile$1
 842:             1             16  javax.xml.parsers.SecuritySupport
 843:             1             16  org.apache.ibatis.builder.xml.XMLMapperEntityResolver
 844:             1             16  org.apache.ibatis.cache.decorators.SynchronizedCache
 845:             1             16  org.apache.ibatis.executor.keygen.Jdbc3KeyGenerator
 846:             1             16  org.apache.ibatis.executor.keygen.NoKeyGenerator
 847:             1             16  org.apache.ibatis.executor.loader.javassist.JavassistProxyFactory
 848:             1             16  org.apache.ibatis.javassist.util.proxy.ProxyFactory$1
 849:             1             16  org.apache.ibatis.javassist.util.proxy.ProxyFactory$3
 850:             1             16  org.apache.ibatis.ognl.ArrayElementsAccessor
 851:             1             16  org.apache.ibatis.ognl.ArrayPropertyAccessor
 852:             1             16  org.apache.ibatis.ognl.CollectionElementsAccessor
 853:             1             16  org.apache.ibatis.ognl.EnumerationElementsAccessor
 854:             1             16  org.apache.ibatis.ognl.EnumerationPropertyAccessor
 855:             1             16  org.apache.ibatis.ognl.EvaluationPool
 856:             1             16  org.apache.ibatis.ognl.IteratorElementsAccessor
 857:             1             16  org.apache.ibatis.ognl.IteratorPropertyAccessor
 858:             1             16  org.apache.ibatis.ognl.ListPropertyAccessor
 859:             1             16  org.apache.ibatis.ognl.MapElementsAccessor
 860:             1             16  org.apache.ibatis.ognl.MapPropertyAccessor
 861:             1             16  org.apache.ibatis.ognl.NumberElementsAccessor
 862:             1             16  org.apache.ibatis.ognl.ObjectArrayPool
 863:             1             16  org.apache.ibatis.ognl.ObjectElementsAccessor
 864:             1             16  org.apache.ibatis.ognl.ObjectMethodAccessor
 865:             1             16  org.apache.ibatis.ognl.ObjectNullHandler
 866:             1             16  org.apache.ibatis.ognl.ObjectPropertyAccessor
 867:             1             16  org.apache.ibatis.ognl.SetPropertyAccessor
 868:             1             16  org.apache.ibatis.plugin.InterceptorChain
 869:             1             16  org.apache.ibatis.scripting.defaults.RawLanguageDriver
 870:             1             16  org.apache.ibatis.scripting.xmltags.DynamicContext$ContextAccessor
 871:             1             16  org.apache.ibatis.scripting.xmltags.XMLLanguageDriver
 872:             1             16  org.apache.ibatis.session.defaults.DefaultSqlSessionFactory
 873:             1             16  org.apache.ibatis.transaction.jdbc.JdbcTransactionFactory
 874:             1             16  org.apache.ibatis.type.TypeAliasRegistry
 875:             1             16  org.slf4j.helpers.BasicMarkerFactory
 876:             1             16  org.slf4j.helpers.NOPLoggerFactory
 877:             1             16  org.slf4j.helpers.SubstituteLoggerFactory
 878:             1             16  org.slf4j.impl.StaticMDCBinder
 879:             1             16  org.slf4j.impl.StaticMarkerBinder
 880:             1             16  sun.misc.ASCIICaseInsensitiveComparator
 881:             1             16  sun.misc.FloatingDecimal$1
 882:             1             16  sun.misc.Launcher
 883:             1             16  sun.misc.Launcher$Factory
 884:             1             16  sun.misc.Perf
 885:             1             16  sun.misc.Unsafe
 886:             1             16  sun.net.DefaultProgressMeteringPolicy
 887:             1             16  sun.net.spi.DefaultProxySelector
 888:             1             16  sun.net.www.protocol.file.Handler
 889:             1             16  sun.net.www.protocol.jar.JarFileFactory
 890:             1             16  sun.reflect.ReflectionFactory
 891:             1             16  sun.reflect.generics.tree.BooleanSignature
 892:             1             16  sun.reflect.generics.tree.BottomSignature
 893:             1             16  sun.reflect.generics.tree.ByteSignature
 894:             1             16  sun.reflect.generics.tree.VoidDescriptor
 895:             1             16  sun.util.calendar.Gregorian
 896:             1             16  sun.util.locale.provider.AuxLocaleProviderAdapter$NullProvider
 897:             1             16  sun.util.locale.provider.CalendarDataUtility$CalendarWeekParameterGetter
 898:             1             16  sun.util.locale.provider.SPILocaleProviderAdapter
 899:             1             16  sun.util.locale.provider.TimeZoneNameUtility$TimeZoneNameGetter
 900:             1             16  sun.util.resources.LocaleData
 901:             1             16  sun.util.resources.LocaleData$LocaleDataResourceBundleControl
Total         69230        7577224



idea插件 mybatisprohelper

mybatis，如何生成sql


https://blog.csdn.net/goligu/article/details/124878614

org.apache.ibatis.scripting.xmltags.XMLScriptBuilder#parseDynamicTags

public class XMLScriptBuilder extends BaseBuilder


TypeAliasRegistry
TypeHandlerRegistry

[Java、Mysql、MyBatis 中枚举 enum 的使用](https://blog.csdn.net/JoeBlackzqq/article/details/90216582)


D:\git\github\LangNote\java\mybatis.md



MyBatis

依赖mysql-connector-java这个jar
jdbc
连接池

接口
xml
SqlSessionFactory等核心类



MyBatis xml
1、if
2、choose、when、otherwise
3、trim、where、set
4、foreach
bind

MyBatis动态SQL
https://mybatis.org/mybatis-3/zh/dynamic-sql.html


在MyBatis中，trim、where和set标签对应的源码类分别是：
- trim标签对应的源码类是org.apache.ibatis.scripting.xmltags.TrimSqlNode
- where标签对应的源码类是org.apache.ibatis.scripting.xmltags.WhereSqlNode
- set标签对应的源码类是org.apache.ibatis.scripting.xmltags.SetSqlNode

这些类都是org.apache.ibatis.scripting.xmltags包中的类，它们都实现了org.apache.ibatis.scripting.xmltags.SqlNode接口，用于表示MyBatis XML映射文件中的动态SQL语句节点。这些类的主要作用是根据用户定义的条件动态生成SQL语句，从而可以灵活地构建SQL语句，以适应不同的查询需求。
在执行SQL语句时，MyBatis会将动态SQL语句节点解析成一个个SqlNode对象，然后使用org.apache.ibatis.scripting.xmltags.MixedSqlNode类将它们组合成一个完整的SQL语句。在组合过程中，MyBatis会根据用户定义的条件动态生成SQL语句，以便生成最终的SQL语句。



script
https://blog.csdn.net/qq_32588349/article/details/51541871
https://blog.csdn.net/a18716374124/article/details/79638980

Jdbctemplate如何写动态sql
JdbcTemplate可以使用NamedParameterJdbcTemplate来支持动态SQL。通过NamedParameterJdbcTemplate，可以使用命名参数的方式来构建动态SQL语句。
下面是一个使用NamedParameterJdbcTemplate构建动态SQL的示例：
```
public List<User> getUsers(String name, Integer age) {
    String sql = "SELECT * FROM user WHERE 1=1 ";

    Map<String, Object> params = new HashMap<>();
    if (name != null) {
        sql += "AND name = :name ";
        params.put("name", name);
    }
    if (age != null) {
        sql += "AND age = :age ";
        params.put("age", age);
    }

    NamedParameterJdbcTemplate jdbcTemplate = new NamedParameterJdbcTemplate(dataSource);
    return jdbcTemplate.query(sql, params, new BeanPropertyRowMapper<>(User.class));
}
```
在这个示例中，我们使用了NamedParameterJdbcTemplate来构建动态SQL语句。首先，我们定义了一个基础的SQL语句"SELECT * FROM user WHERE 1=1"，然后根据传入的参数动态添加查询条件。在添加查询条件时，我们使用了命名参数的方式，例如":name"和":age"。最后，我们使用NamedParameterJdbcTemplate的query方法执行查询，传入SQL语句、参数和结果集的映射方式。
需要注意的是，使用NamedParameterJdbcTemplate构建动态SQL时，SQL语句中的参数名必须和params中的键名保持一致。

Restful HTTP 路径

### 面试题

mybatis批量插入数据有哪几种方式，有什么异同
1、mybatis xml文件中拼接xml
创建 UserMapper.xml 文件，使用 foreach 标签拼接 SQL，具体实现代码如下：
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="com.example.demo.mapper.UserMapper">
    <insert id="saveBatchByNative">
        INSERT INTO `USER`(`NAME`,`PASSWORD`) VALUES
        <foreach collection="list" separator="," item="item">
            (#{item.name},#{item.password})
        </foreach>
    </insert>
</mapper>

https://zhuanlan.zhihu.com/p/35305211


mybatis ExecutorType.BATCHMybatis内置的ExecutorType有3种，默认的是simple，该模式下它为每个语句的执行创建一个新的预处理语句，单条提交sql；而batch模式重复使用已经预处理的语句，并且批量执行所有更新语句，显然batch性能将更优； 但batch模式也有自己的问题，比如在Insert操作时，在事务没有提交之前，是没有办法获取到自增的id，这在某型情形下是不符合业务要求的具体用法如下:*方式一 spring+mybatis 的//获取sqlsession
//从spring注入原有的sqlSessionTemplate
@Autowired
private SqlSessionTemplate sqlSessionTemplate;
// 新获取一个模式为BATCH，自动提交为false的session
// 如果自动提交设置为true,将无法控制提交的条数，改为最后统一提交，可能导致内存溢出

```java
SqlSession session = sqlSessionTemplate.getSqlSessionFactory().openSession(ExecutorType.BATCH,false);
//通过新的session获取mapper
fooMapper = session.getMapper(FooMapper.class);
int size = 10000;
try{
for(int i = 0; i < size; i++) {
Foo foo = new Foo();
foo.setName(String.valueOf(System.currentTimeMillis()));
fooMapper.insert(foo);
if(i % 1000 == 0 || i == size - 1) {
//手动每1000个一提交，提交后无法回滚 
session.commit();
//清理缓存，防止溢出
session.clearCache();
}
}
} catch (Exception e) {
//没有提交的数据可以回滚
session.rollback();
} finally{
session.close();
}

```


spring+mybatis
方法二:结合通用mapper sql别名最好是包名＋类名public void insertBatch(Map<String,Object> paramMap, List<User> list) throws Exception {
// 新获取一个模式为BATCH，自动提交为false的session
// 如果自动提交设置为true,将无法控制提交的条数，改为最后统一提交，可能导致内存溢出

```java
SqlSession session = sqlSessionTemplate.getSqlSessionFactory().openSession(ExecutorType.BATCH, false);
try {
if(null != list || list.size()>0){
int lsize=list.size();
for (int i = 0, n=list.size(); i < n; i++) {
User user= list.get(i);
user.setIndate((String)paramMap.get("indate"));
user.setDatadate((String)paramMap.get("dataDate"));//数据归属时间
//session.insert("com.xx.mapper.UserMapper.insert",user);
//session.update("com.xx.mapper.UserMapper.updateByPrimaryKeySelective",_entity);
session.insert(“包名+类名", user);
if ((i>0 && i % 1000 == 0) || i == lsize - 1) {
// 手动每1000个一提交，提交后无法回滚
session.commit();
// 清理缓存，防止溢出
session.clearCache();
}
}
}
} catch (Exception e) {
// 没有提交的数据可以回滚
session.rollback();
e.printStackTrace();
} finally {
session.close();
}
}
```

### MyBatis四大组件之Executor执行器

每一个SqlSession都会拥有一个Executor对象，这个对象负责增删改查的具体操作，我们可以简单的将它理解为JDBC中Statement的封装版。
https://zhuanlan.zhihu.com/p/80497754

public enum ExecutorType {
  SIMPLE, REUSE, BATCH
}


Mybatis是如何将Mapper接口注册到Spring IoC的
https://zhuanlan.zhihu.com/p/256425436

![](..\..\imgs\mybatis\mybatis_spring.png)

ImportBeanDefinitionRegistrar接口
ImportBeanDefinitionRegistrar是Spring3.1开始引入的一个接口，用来动态注册bean定义的接口。通过@Import方式引入，和ImportSelector用法类似，通常和EnvironmentAware、BeanFactoryAware、BeanClassLoaderAware、ResourceLoaderAware接口一起使用。其作用就是把模糊的概念明确化，把抽象的东西实例化，为本地服务提供更方便的使用或者服务调用。

BeanDefinitionRegistryPostProcessor
BeanDefinitionRegistryPostProcessor是BeanFactoryPostProcessor的子接口,BeanFactoryPostProcessor的作用是在Spring Bean的定义信息已经加载但还没有初始化的时候执行postProcessBeanFactory()来处理一些额外的逻辑，
而BeanDefinitionRegistryPostProcessor的作用是在BeanFactoryPostProcessor增加了一个前置处理，当一个Bean实现了该接口后，始化前先执行该接口的postProcessBeanDefinitionRegistry()方法，然后再执行其父类的方法postProcessBeanFactory()。这样就把一个Spring Bean的初始化周期更加细化，让我们在各个阶段有定制它的可能。

mybatis，可以强制设置使用哪个日志工具 mybatis-config.xml里面配置
```xml
    <settings>

<!--
        <setting name="logImpl" value="SLF4J" />
-->
        <setting name="logImpl" value="LOG4J2"/>
    </settings>
```
dubbo也可以，设置环境变量





### 分包解析

3.4.6

| org.apache.ibatis.annotations |                                                              |
| ----------------------------- | ------------------------------------------------------------ |
| Arg                           | The annotation that specify a mapping definition for the constructor argument. |
|                               |                                                              |
| AutomapConstructor            | The marker annotation that indicate a constructor for automatic mapping. |
|                               |                                                              |
| CacheNamespace                | The annotation that specify to use cache on namespace(e.g.   |
|                               |                                                              |
| CacheNamespaceRef             | The annotation that reference a cache.                       |
|                               |                                                              |
| Case                          | The annotation that conditional mapping definition for TypeDiscriminator. |
|                               |                                                              |
| ConstructorArgs               | The annotation that be grouping mapping definitions for constructor. |
|                               |                                                              |
| Delete                        | The annotation that specify an SQL for deleting record(s).   |
|                               |                                                              |
| Delete.List                   | The container annotation for Delete.                         |
|                               |                                                              |
| DeleteProvider                | The annotation that specify a method that provide an SQL for deleting record(s). |
|                               |                                                              |
| DeleteProvider.List           | The container annotation for DeleteProvider.                 |
|                               |                                                              |
| Flush                         | The maker annotation that invoke a flush statements via Mapper interface. |
|                               |                                                              |
| Insert                        | The annotation that specify an SQL for inserting record(s).  |
|                               |                                                              |
| Insert.List                   | The container annotation for Insert.                         |
|                               |                                                              |
| InsertProvider                | The annotation that specify a method that provide an SQL for inserting record(s). |
|                               |                                                              |
| InsertProvider.List           | The container annotation for InsertProvider.                 |
|                               |                                                              |
| Lang                          | The annotation that specify a LanguageDriver to use.         |
|                               |                                                              |
| Many                          | The annotation that specify the nested statement for retrieving collections. |
|                               |                                                              |
| MapKey                        | The annotation that specify the property name(or column name) for a key value of Map. |
|                               |                                                              |
| Mapper                        | Marker interface for MyBatis mappers.                        |
|                               |                                                              |
| One                           | The annotation that specify the nested statement for retrieving single object. |
|                               |                                                              |
| Options                       | The annotation that specify options for customizing default behaviors. |
|                               |                                                              |
| Options.FlushCachePolicy      | The options for the Options.flushCache().                    |
|                               |                                                              |
| Options.List                  | The container annotation for Options.                        |
|                               |                                                              |
| Param                         | The annotation that specify the parameter name.              |
|                               |                                                              |
| Property                      | The annotation that inject a property value.                 |
|                               |                                                              |
| Result                        | The annotation that specify a mapping definition for the property. |
|                               |                                                              |
| ResultMap                     | The annotation that specify result map names to use.         |
|                               |                                                              |
| Results                       | The annotation that be grouping mapping definitions for property. |
|                               |                                                              |
| ResultType                    | This annotation can be used when a @Select method is using a ResultHandler. |
|                               |                                                              |
| Select                        | The annotation that specify an SQL for retrieving record(s). |
|                               |                                                              |
| Select.List                   | The container annotation for Select.                         |
|                               |                                                              |
| SelectKey                     | The annotation that specify an SQL for retrieving a key value. |
|                               |                                                              |
| SelectKey.List                | The container annotation for SelectKey.                      |
|                               |                                                              |
| SelectProvider                | The annotation that specify a method that provide an SQL for retrieving record(s). |
|                               |                                                              |
| SelectProvider.List           | The container annotation for SelectProvider.                 |
|                               |                                                              |
| TypeDiscriminator             | The annotation that be grouping conditional mapping definitions. |
|                               |                                                              |
| Update                        | The annotation that specify an SQL for updating record(s).   |
|                               |                                                              |
| Update.List                   | The container annotation for Update.                         |
|                               |                                                              |
| UpdateProvider                | The annotation that specify a method that provide an SQL for updating record(s). |
|                               |                                                              |
| UpdateProvider.List           | The container annotation for UpdateProvider.                 |
|                               |                                                              |





| org.apache.ibatis.binding    |
| ---------------------------- |
| BindingException             |
| MapperMethod                 |
| MapperMethod.MethodSignature |
| MapperMethod.ParamMap<V>     |
| MapperMethod.SqlCommand      |
| MapperProxy<T>               |
|                              |
| MapperProxyFactory<T>        |
|                              |
| MapperRegistry               |







| org.apache.ibatis.builder.annotation                         |
| ------------------------------------------------------------ |
| MapperAnnotationBuilder                                      |
|                                                              |
| MethodResolver                                               |
|                                                              |
| ProviderContext                                              |
| The context object for sql provider method.                  |
| ProviderMethodResolver                                       |
| The interface that resolve an SQL provider method via an SQL provider class. |
| ProviderSqlSource                                            |







| org.apache.ibatis.builder.xml                 |
| --------------------------------------------- |
| XMLConfigBuilder                              |
|                                               |
| XMLIncludeTransformer                         |
|                                               |
| XMLMapperBuilder                              |
|                                               |
| XMLMapperEntityResolver                       |
| Offline entity resolver for the MyBatis DTDs. |
| XMLStatementBuilder                           |







| org.apache.ibatis.cache                                      |
| ------------------------------------------------------------ |
| Cache                                                        |
| SPI for cache providers.                                     |
| CacheException                                               |
|                                                              |
| CacheKey                                                     |
|                                                              |
| NullCacheKey                                                 |
| Deprecated.                                                  |
| Since 3.5.3, This class never used and will be removed future version. |
| TransactionalCacheManager                                    |
|                                                              |
|                                                              |
|                                                              |
|                                                              |
| cache.decorators                                             |
|                                                              |
| BlockingCache                                                |
| Simple blocking decorator                                    |
| FifoCache                                                    |
| FIFO (first in, first out) cache decorator.                  |
| LoggingCache                                                 |
|                                                              |
| LruCache                                                     |
| Lru (least recently used) cache decorator.                   |
| ScheduledCache                                               |
|                                                              |
| SerializedCache                                              |
|                                                              |
| SerializedCache.CustomObjectInputStream                      |
|                                                              |
| SoftCache                                                    |
| Soft Reference cache decorator.                              |
| SynchronizedCache                                            |
|                                                              |
| TransactionalCache                                           |
| The 2nd level cache transactional buffer.                    |
| WeakCache                                                    |
| Weak Reference cache decorator.                              |
|                                                              |
|                                                              |
| cache.impl                                                   |
| PerpetualCache                                               |





| org.apache.ibatis.cursor                                     |
| ------------------------------------------------------------ |
| Cursor<T>                                                    |
| Cursor contract to handle fetching items lazily using an Iterator. |
|                                                              |
|                                                              |
|                                                              |
| org.apache.ibatis.cursor.defaults                            |
|                                                              |
|                                                              |
| DefaultCursor<T>                                             |
| This is the default implementation of a MyBatis Cursor.      |
| DefaultCursor.ObjectWrapperResultHandler<T>                  |







| org.apache.ibatis.datasource                                 |
| ------------------------------------------------------------ |
| DataSourceException                                          |
|                                                              |
| DataSourceFactory                                            |
|                                                              |
|                                                              |
|                                                              |
|                                                              |
|                                                              |
| datasource.jndi                                              |
|                                                              |
| JndiDataSourceFactory                                        |
|                                                              |
|                                                              |
| datasource.pooled                                            |
|                                                              |
| PooledDataSource                                             |
| This is a simple, synchronous, thread-safe database connection pool. |
| PooledDataSourceFactory                                      |
| 聽                                                           |
| PoolState                                                    |
|                                                              |
|                                                              |
| datasource.unpooled                                          |
| UnpooledDataSource                                           |
|                                                              |
| UnpooledDataSourceFactory                                    |









| org.apache.ibatis.exceptions |
| ---------------------------- |
| ExceptionFactory             |
|                              |
| IbatisException              |
| Deprecated.                  |
| PersistenceException         |
|                              |
| TooManyResultsException      |







| org.apache.ibatis.executor                                   |
| ------------------------------------------------------------ |
| BaseExecutor                                                 |
|                                                              |
| BatchExecutor                                                |
|                                                              |
| BatchExecutorException                                       |
| This exception is thrown if a java.sql.BatchUpdateException is caught during the execution of any nested batch. |
| BatchResult                                                  |
|                                                              |
| CachingExecutor                                              |
|                                                              |
| ErrorContext                                                 |
|                                                              |
| ExecutionPlaceholder                                         |
|                                                              |
| Executor                                                     |
|                                                              |
| ExecutorException                                            |
|                                                              |
| ResultExtractor                                              |
|                                                              |
| ReuseExecutor                                                |
|                                                              |
| SimpleExecutor                                               |
|                                                              |
|                                                              |
|                                                              |
|                                                              |
| org.apache.ibatis.executor.keygen                            |
|                                                              |
|                                                              |
| Jdbc3KeyGenerator                                            |
|                                                              |
| KeyGenerator                                                 |
|                                                              |
| NoKeyGenerator                                               |
|                                                              |
| SelectKeyGenerator                                           |
|                                                              |
|                                                              |
|                                                              |
|                                                              |
|                                                              |
|                                                              |
| org.apache.ibatis.executor.loader                            |
| AbstractEnhancedDeserializationProxy                         |
|                                                              |
| AbstractSerialStateHolder                                    |
|                                                              |
| CglibProxyFactory                                            |
| Deprecated.                                                  |
| JavassistProxyFactory                                        |
| Deprecated.                                                  |
| ProxyFactory                                                 |
|                                                              |
| ResultLoader                                                 |
|                                                              |
| ResultLoaderMap                                              |
|                                                              |
| ResultLoaderMap.LoadPair                                     |
| Property which was not loaded yet.                           |
| WriteReplaceInterface                                        |
|                                                              |
|                                                              |
|                                                              |
| org.apache.ibatis.executor.loader.cglib                      |
| CglibProxyFactory                                            |
|                                                              |
|                                                              |
|                                                              |
| org.apache.ibatis.executor.loader.javassist                  |
| JavassistProxyFactory                                        |
|                                                              |
|                                                              |
| org.apache.ibatis.executor.parameter                         |
| ParameterHandler                                             |
|                                                              |
|                                                              |
|                                                              |
|                                                              |
|                                                              |
| org.apache.ibatis.executor.result                            |
| DefaultMapResultHandler<K,V>                                 |
|                                                              |
| DefaultResultContext<T>                                      |
|                                                              |
| DefaultResultHandler                                         |
|                                                              |
| ResultMapException                                           |
|                                                              |
|                                                              |
| org.apache.ibatis.executor.resultset                         |
|                                                              |
| DefaultResultSetHandler                                      |
|                                                              |
| ResultSetHandler                                             |
|                                                              |
| ResultSetWrapper                                             |
|                                                              |
| executor.statement                                           |
| BaseStatementHandler                                         |
|                                                              |
| CallableStatementHandler                                     |
|                                                              |
| PreparedStatementHandler                                     |
|                                                              |
| RoutingStatementHandler                                      |
|                                                              |
| SimpleStatementHandler                                       |
|                                                              |
| StatementHandler                                             |
|                                                              |
| StatementUtil                                                |







| org.apache.ibatis.io                                         |
| ------------------------------------------------------------ |
| ClassLoaderWrapper                                           |
| A class to wrap access to multiple class loaders making them work as one |
| DefaultVFS                                                   |
| A default implementation of VFS that works for most application servers. |
| ExternalResources                                            |
| Deprecated.                                                  |
| JBoss6VFS                                                    |
| A JBoss6VFS.VFS implementation that works with the VFS API provided by JBoss 6. |
| ResolverUtil<T>                                              |
| ResolverUtil is used to locate classes that are available in the/a class path and meet arbitrary conditions. |
| ResolverUtil.AnnotatedWith                                   |
| A Test that checks to see if each class is annotated with a specific annotation. |
| ResolverUtil.IsA                                             |
| A Test that checks to see if each class is assignable to the provided class. |
| ResolverUtil.Test                                            |
| A simple interface that specifies how to test classes to determine if they are to be included in the results produced by the ResolverUtil. |
| Resources                                                    |
| A class to simplify access to resources through the classloader. |
| SerialFilterChecker                                          |
|                                                              |
| VFS                                                          |
| Provides a very simple API for accessing resources within an application server. |







| org.apache.ibatis.jdbc                                       |
| ------------------------------------------------------------ |
| AbstractSQL<T>                                               |
|                                                              |
| Null                                                         |
|                                                              |
| RuntimeSqlException                                          |
|                                                              |
| ScriptRunner                                                 |
| This is an internal testing utility.                         |
| You are welcome to use this class for your own purposes,     |
| but if there is some feature/enhancement you need for your own usage, |
| please make and modify your own copy instead of sending us an enhancement request. |
| SelectBuilder                                                |
| Deprecated.                                                  |
| Use the SQL Class                                            |
| SQL                                                          |
|                                                              |
| SqlBuilder                                                   |
| Deprecated.                                                  |
| Use the SQL Class                                            |
| SqlRunner                                                    |





| org.apache.ibatis.lang                      |
| ------------------------------------------- |
| UsesJava7                                   |
| Indicates that the element uses Java 7 API. |
| UsesJava8                                   |
| Indicates that the element uses Java 8 API. |







| org.apache.ibatis.logging               |      |
| --------------------------------------- | ---- |
| Log                                     |      |
|                                         |      |
| LogException                            |      |
|                                         |      |
| LogFactory                              |      |
|                                         |      |
|                                         |      |
| logging.commons                         |      |
|                                         |      |
| JakartaCommonsLoggingImpl               |      |
|                                         |      |
|                                         |      |
|                                         |      |
| logging.jdbc                            |      |
|                                         |      |
| BaseJdbcLogger                          |      |
| Base class for proxies to do logging.   |      |
| ConnectionLogger                        |      |
| Connection proxy to add logging.        |      |
| PreparedStatementLogger                 |      |
| PreparedStatement proxy to add logging. |      |
| ResultSetLogger                         |      |
| ResultSet proxy to add logging.         |      |
| StatementLogger                         |      |
| Statement proxy to add logging.         |      |
|                                         |      |
|                                         |      |
| logging.jdk14                           |      |
| Jdk14LoggingImpl                        |      |
|                                         |      |
|                                         |      |
| logging.log4j                           |      |
| Log4jImpl                               |      |
|                                         |      |
|                                         |      |
| logging.log4j2                          |      |
|                                         |      |
| Log4j2AbstractLoggerImpl                |      |
|                                         |      |
| Log4j2Impl                              |      |
|                                         |      |
| Log4j2LoggerImpl                        |      |
|                                         |      |
|                                         |      |
| logging.nologging                       |      |
|                                         |      |
| NoLoggingImpl                           |      |
|                                         |      |
|                                         |      |
|                                         |      |
|                                         |      |
| logging.slf4j                           |      |
| Slf4jImpl                               |      |
|                                         |      |
|                                         |      |
|                                         |      |
|                                         |      |
| logging.stdout                          |      |
| StdOutImpl                              |      |







| org.apache.ibatis.mapping                                    |
| ------------------------------------------------------------ |
| BoundSql                                                     |
| An actual SQL String got from an SqlSource after having processed any dynamic content. |
| CacheBuilder                                                 |
|                                                              |
| DatabaseIdProvider                                           |
| Should return an id to identify the type of this database.   |
| DefaultDatabaseIdProvider                                    |
| Deprecated.                                                  |
| Discriminator                                                |
|                                                              |
| Discriminator.Builder                                        |
|                                                              |
| Environment                                                  |
|                                                              |
| Environment.Builder                                          |
|                                                              |
| FetchType                                                    |
|                                                              |
| MappedStatement                                              |
|                                                              |
| MappedStatement.Builder                                      |
|                                                              |
| ParameterMap                                                 |
|                                                              |
| ParameterMap.Builder                                         |
|                                                              |
| ParameterMapping                                             |
|                                                              |
| ParameterMapping.Builder                                     |
|                                                              |
| ParameterMode                                                |
|                                                              |
| ResultFlag                                                   |
|                                                              |
| ResultMap                                                    |
|                                                              |
| ResultMap.Builder                                            |
|                                                              |
| ResultMapping                                                |
|                                                              |
| ResultMapping.Builder                                        |
|                                                              |
| ResultSetType                                                |
|                                                              |
| SqlCommandType                                               |
|                                                              |
| SqlSource                                                    |
| Represents the content of a mapped statement read from an XML file or an annotation. |
| StatementType                                                |
|                                                              |
| VendorDatabaseIdProvider                                     |
| Vendor DatabaseId provider.                                  |





| org.apache.ibatis.ognl |      |      |
| ---------------------- | ---- | ---- |
|                        |      |      |
|                        |      |      |
|                        |      |      |







| org.apache.ibatis.parsing |
| ------------------------- |
| GenericTokenParser        |
|                           |
| ParsingException          |
|                           |
| PropertyParser            |
|                           |
| TokenHandler              |
|                           |
| XNode                     |
|                           |
| XPathParser               |





| org.apache.ibatis.plugin                                 |
| -------------------------------------------------------- |
| Interceptor                                              |
|                                                          |
| InterceptorChain                                         |
|                                                          |
| Intercepts                                               |
| The annotation that specify target methods to intercept. |
| Invocation                                               |
|                                                          |
| Plugin                                                   |
|                                                          |
| PluginException                                          |
|                                                          |
| Signature                                                |
| The annotation that indicate the method signature.       |





| org.apache.ibatis.reflection                                 |
| ------------------------------------------------------------ |
| ArrayUtil                                                    |
| Provides hashCode, equals and toString methods that can handle array. |
| DefaultReflectorFactory                                      |
|                                                              |
| ExceptionUtil                                                |
|                                                              |
| Jdk                                                          |
| To check the existence of version dependent classes.         |
| MetaClass                                                    |
|                                                              |
| MetaObject                                                   |
|                                                              |
| OptionalUtil                                                 |
| Deprecated.                                                  |
| Since 3.5.0, Will remove this class at future(next major version up). |
| ParamNameResolver                                            |
|                                                              |
| ParamNameUtil                                                |
|                                                              |
| ReflectionException                                          |
|                                                              |
| Reflector                                                    |
| This class represents a cached set of class definition information that allows for easy mapping between property names and getter/setter methods. |
| ReflectorFactory                                             |
|                                                              |
| SystemMetaObject                                             |
|                                                              |
| TypeParameterResolver                                        |
|                                                              |
|                                                              |
|                                                              |
| org.apache.ibatis.reflection.factory                         |
|                                                              |
| DefaultObjectFactory                                         |
|                                                              |
| ObjectFactory                                                |
| MyBatis uses an ObjectFactory to create all needed new Objects. |
|                                                              |
|                                                              |
| org.apache.ibatis.reflection.invoker                         |
|                                                              |
| AmbiguousMethodInvoker                                       |
|                                                              |
| GetFieldInvoker                                              |
|                                                              |
| Invoker                                                      |
|                                                              |
| MethodInvoker                                                |
|                                                              |
| SetFieldInvoker                                              |
|                                                              |
|                                                              |
| org.apache.ibatis.reflection.property                        |
| PropertyCopier                                               |
|                                                              |
| PropertyNamer                                                |
|                                                              |
| PropertyTokenizer                                            |
|                                                              |
|                                                              |
|                                                              |
| org.apache.ibatis.reflection.wrapper                         |
| BaseWrapper                                                  |
|                                                              |
| BeanWrapper                                                  |
|                                                              |
| CollectionWrapper                                            |
|                                                              |
| DefaultObjectWrapperFactory                                  |
|                                                              |
| MapWrapper                                                   |
|                                                              |
| ObjectWrapper                                                |
|                                                              |
| ObjectWrapperFactory                                         |





| org.apache.ibatis.scripting                                  |
| ------------------------------------------------------------ |
| LanguageDriver                                               |
|                                                              |
| LanguageDriverRegistry                                       |
|                                                              |
| ScriptingException                                           |
|                                                              |
|                                                              |
|                                                              |
| org.apache.ibatis.scripting.defaults                         |
|                                                              |
| DefaultParameterHandler                                      |
|                                                              |
| RawLanguageDriver                                            |
| As of 3.2.4 the default XML language is able to identify static statements and create a RawSqlSource. |
| RawSqlSource                                                 |
| Static SqlSource.                                            |
|                                                              |
|                                                              |
|                                                              |
|                                                              |
| org.apache.ibatis.scripting.xmltags                          |
|                                                              |
|                                                              |
|                                                              |
| ChooseSqlNode                                                |
|                                                              |
| DynamicContext                                               |
|                                                              |
| DynamicSqlSource                                             |
|                                                              |
| ExpressionEvaluator                                          |
|                                                              |
| ForEachSqlNode                                               |
|                                                              |
| IfSqlNode                                                    |
|                                                              |
| MixedSqlNode                                                 |
|                                                              |
| OgnlCache                                                    |
| Caches OGNL parsed expressions.                              |
| OgnlClassResolver                                            |
| Custom ognl ClassResolver which behaves same like ognl's DefaultClassResolver. |
| SetSqlNode                                                   |
|                                                              |
| SqlNode                                                      |
|                                                              |
| StaticTextSqlNode                                            |
|                                                              |
| TextSqlNode                                                  |
|                                                              |
| TrimSqlNode                                                  |
|                                                              |
| VarDeclSqlNode                                               |
|                                                              |
| WhereSqlNode                                                 |
|                                                              |
| XMLLanguageDriver                                            |
|                                                              |
| XMLScriptBuilder                                             |







| org.apache.ibatis.session                                    |
| ------------------------------------------------------------ |
| AutoMappingBehavior                                          |
| Specifies if and how MyBatis should automatically map columns to fields/properties. |
| AutoMappingUnknownColumnBehavior                             |
| Specify the behavior when detects an unknown column (or unknown property type) of automatic mapping target. |
| Configuration                                                |
|                                                              |
| Configuration.StrictMap<V>                                   |
|                                                              |
| Configuration.StrictMap.Ambiguity                            |
|                                                              |
| ExecutorType                                                 |
|                                                              |
| LocalCacheScope                                              |
|                                                              |
| ResultContext<T>                                             |
|                                                              |
| ResultHandler<T>                                             |
|                                                              |
| RowBounds                                                    |
|                                                              |
| SqlSession                                                   |
| The primary Java interface for working with MyBatis.         |
| SqlSessionException                                          |
|                                                              |
| SqlSessionFactory                                            |
| Creates an SqlSession out of a connection or a DataSource    |
| SqlSessionFactoryBuilder                                     |
| Builds SqlSession instances.                                 |
| SqlSessionManager                                            |
|                                                              |
| TransactionIsolationLevel                                    |
|                                                              |
|                                                              |
| session.defaults                                             |
|                                                              |
|                                                              |
|                                                              |
| DefaultSqlSession                                            |
| The default implementation for SqlSession.                   |
| DefaultSqlSession.StrictMap<V>                               |
| Deprecated.                                                  |
| Since 3.5.5                                                  |
| DefaultSqlSessionFactory                                     |









| org.apache.ibatis.transaction                                |
| ------------------------------------------------------------ |
| Transaction                                                  |
| Wraps a database connection.                                 |
| TransactionException                                         |
|                                                              |
| TransactionFactory                                           |
| Creates Transaction instances.                               |
|                                                              |
|                                                              |
|                                                              |
|                                                              |
| transaction.jdbc                                             |
|                                                              |
|                                                              |
|                                                              |
| JdbcTransaction                                              |
| Transaction that makes use of the JDBC commit and rollback facilities directly. |
| JdbcTransactionFactory                                       |
| Creates JdbcTransaction instances.                           |
|                                                              |
| transaction.managed                                          |
|                                                              |
| ManagedTransaction                                           |
| Transaction that lets the container manage the full lifecycle of the transaction. |
| ManagedTransactionFactory                                    |
| Creates ManagedTransaction instances.                        |









| org.apache.ibatis.type                                       |                                         |
| ------------------------------------------------------------ | --------------------------------------- |
| Alias                                                        | The annotation that specify alias name. |
|                                                              |                                         |
| ArrayTypeHandler                                             |                                         |
|                                                              |                                         |
| BaseTypeHandler<T>                                           |                                         |
| The base TypeHandler for references a generic type.          |                                         |
| BigDecimalTypeHandler                                        |                                         |
|                                                              |                                         |
| BigIntegerTypeHandler                                        |                                         |
|                                                              |                                         |
| BlobByteObjectArrayTypeHandler                               |                                         |
|                                                              |                                         |
| BlobInputStreamTypeHandler                                   |                                         |
| The TypeHandler for Blob/InputStream using method supported at JDBC 4.0. |                                         |
| BlobTypeHandler                                              |                                         |
|                                                              |                                         |
| BooleanTypeHandler                                           |                                         |
|                                                              |                                         |
| ByteArrayTypeHandler                                         |                                         |
|                                                              |                                         |
| ByteObjectArrayTypeHandler                                   |                                         |
|                                                              |                                         |
| ByteTypeHandler                                              |                                         |
|                                                              |                                         |
| CharacterTypeHandler                                         |                                         |
|                                                              |                                         |
| ClobReaderTypeHandler                                        |                                         |
| The TypeHandler for Clob/Reader using method supported at JDBC 4.0. |                                         |
| ClobTypeHandler                                              |                                         |
|                                                              |                                         |
| DateOnlyTypeHandler                                          |                                         |
|                                                              |                                         |
| DateTypeHandler                                              |                                         |
|                                                              |                                         |
| DoubleTypeHandler                                            |                                         |
|                                                              |                                         |
| EnumOrdinalTypeHandler<E extends Enum<E>>                    |                                         |
|                                                              |                                         |
| EnumTypeHandler<E extends Enum<E>>                           |                                         |
|                                                              |                                         |
| FloatTypeHandler                                             |                                         |
|                                                              |                                         |
| InstantTypeHandler                                           |                                         |
|                                                              |                                         |
| IntegerTypeHandler                                           |                                         |
|                                                              |                                         |
| JapaneseDateTypeHandler                                      |                                         |
| Type Handler for JapaneseDate.                               |                                         |
| JdbcType                                                     |                                         |
|                                                              |                                         |
| LocalDateTimeTypeHandler                                     |                                         |
|                                                              |                                         |
| LocalDateTypeHandler                                         |                                         |
|                                                              |                                         |
| LocalTimeTypeHandler                                         |                                         |
|                                                              |                                         |
| LongTypeHandler                                              |                                         |
|                                                              |                                         |
| MappedJdbcTypes                                              |                                         |
| The annotation that specify jdbc types to map TypeHandler.   |                                         |
| MappedTypes                                                  |                                         |
| The annotation that specify java types to map TypeHandler.   |                                         |
| MonthTypeHandler                                             |                                         |
|                                                              |                                         |
| NClobTypeHandler                                             |                                         |
|                                                              |                                         |
| NStringTypeHandler                                           |                                         |
|                                                              |                                         |
| ObjectTypeHandler                                            |                                         |
|                                                              |                                         |
| OffsetDateTimeTypeHandler                                    |                                         |
|                                                              |                                         |
| OffsetTimeTypeHandler                                        |                                         |
|                                                              |                                         |
| ShortTypeHandler                                             |                                         |
|                                                              |                                         |
| SimpleTypeRegistry                                           |                                         |
|                                                              |                                         |
| SqlDateTypeHandler                                           |                                         |
|                                                              |                                         |
| SqlTimestampTypeHandler                                      |                                         |
|                                                              |                                         |
| SqlTimeTypeHandler                                           |                                         |
|                                                              |                                         |
| SqlxmlTypeHandler                                            |                                         |
| Convert String to/from SQLXML.                               |                                         |
| StringTypeHandler                                            |                                         |
|                                                              |                                         |
| TimeOnlyTypeHandler                                          |                                         |
|                                                              |                                         |
| TypeAliasRegistry                                            |                                         |
|                                                              |                                         |
| TypeException                                                |                                         |
|                                                              |                                         |
| TypeHandler<T>                                               |                                         |
|                                                              |                                         |
| TypeHandlerRegistry                                          |                                         |
|                                                              |                                         |
| TypeReference<T>                                             |                                         |
| References a generic type.                                   |                                         |
| UnknownTypeHandler                                           |                                         |
|                                                              |                                         |
| YearMonthTypeHandler                                         |                                         |
| Type Handler for YearMonth.                                  |                                         |
| YearTypeHandler                                              |                                         |
|                                                              |                                         |
| ZonedDateTimeTypeHandler                                     |                                         |