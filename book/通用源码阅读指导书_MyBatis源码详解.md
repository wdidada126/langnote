# 通用源码阅读指导书：MyBatis源码详解

https://www.zhihu.com/pub/reader/120079431

https://book.douban.com/subject/35138963/

易哥

2020年8月出版

按照java的包来分类阅读代码的

随书代码

https://github.com/edidada/MyBatisDemo

## 第1篇 背景介绍
### 第2章 MyBatis概述

### Chap. 3 Mybatis运行初探



### 第4章 MyBatis源码结构概述 40
## 第2篇 基础功能包源码阅读


### 第5章 exceptions包

throwable及其子类
在Java中，Throwable是所有可以被抛出（thrown）的类的基类。Throwable有两个主要的子类：Error和Exception。
Error表示JVM运行时出现的致命错误，例如OutOfMemoryError、StackOverflowError等，通常不应该被程序捕获和处理。
Exception则表示可捕获和处理的异常，包括运行时异常（RuntimeException及其子类）和非运行时异常（非RuntimeException及其子类）。运行时异常通常由程序逻辑错误引起，例如NullPointerException、IndexOutOfBoundsException等；非运行时异常通常由外部环境或程序资源不足引起，例如IOException、SQLException等。
除了Error和Exception之外，还有一个子类RuntimeException，它表示运行时异常，包括NullPointerException、IndexOutOfBoundsException等。RuntimeException及其子类可以被程序捕获和处理，但不要求在方法声明中显式地声明它们。
`Throwable` 是 Java 语言中所有错误或异常的父类，只有当对象是此类（或其子类之一）的实例时，才能通过 Java 虚拟机或者 Java throw 语句抛出²。`Throwable` 的子类有两个，`Error` 和 `Exception`。其中，`Exception` 的子类有两个，`RuntimeException` 和 `Checked Exception`³。
希望这能帮到你。

源: 与必应的对话， 2023/5/10
(1) Throwable类详解_回老家了看看你的博客-CSDN博客. https://blog.csdn.net/jtdsh/article/details/69003842.
(2) 【java异常】1 throwable及主要子类_恰子李的博客-CSDN博客. https://blog.csdn.net/qiaziliping/article/details/96160610.
(3) Java---Throwable类_丶炜钦的博客-CSDN博客. https://blog.csdn.net/weixin_44521690/article/details/99678243.
(4) Throwable - 菜鸟教程. https://www.runoob.com/manual/jdk11api/java.base/java/lang/Throwable.html.
(5) Java Throwable类及其子类 - CSDN博客. https://blog.csdn.net/loongshawn/article/details/77736869.
(6) Java异常：Throwable及其子类 - CSDN博客. https://blog.csdn.net/wanghuawei19930812/article/details/104074791.

org.apache.ibatis.exceptions.ExceptionFactory

```shell
public class ExceptionFactory {
  private ExceptionFactory() {
    // Prevent Instantiation
  }
  public static RuntimeException wrapException(String message, Exception e) {
    return new PersistenceException(ErrorContext.instance().message(message).cause(e).toString(), e);
  }
}
```
org.apache.ibatis.executor.ErrorContext 有静态方法instance()


RuntimeSqlException
IbatisException  @Deprecated
PersistenceException

Throwable (java.lang)
Exception (java.lang)
RuntimeException (java.lang)
IbatisException (org.apache.ibatis.exceptions)
    PersistenceException (org.apache.ibatis.exceptions)
        BindingException (org.apache.ibatis.binding)
        TransactionException (org.apache.ibatis.transaction)
        TooManyResultsException (org.apache.ibatis.exceptions)
        ResultMapException (org.apache.ibatis.executor.result)
        ExecutorException (org.apache.ibatis.executor)
        BatchExecutorException (org.apache.ibatis.executor)
        ScriptingException (org.apache.ibatis.scripting)
        CacheException (org.apache.ibatis.cache)
        BuilderException (org.apache.ibatis.builder)
        IncompleteElementException (org.apache.ibatis.builder)
        ParsingException (org.apache.ibatis.parsing)
        SqlSessionException (org.apache.ibatis.session)
        DataSourceException (org.apache.ibatis.datasource)
        TypeException (org.apache.ibatis.type)
        LogException (org.apache.ibatis.logging)
        ReflectionException (org.apache.ibatis.reflection)
        PluginException (org.apache.ibatis.plugin)


TooManyResultsException

### 第6章 reflection包
java.lang.reflect.Type
TypeVariable
WildcardType
ParameterizedType
GenericArrayType

在Java中，泛型类型可以使用以下4种类型来表示：
1. TypeVariable：表示泛型类型参数，例如T、E、K、V等。它们通常出现在泛型类、泛型方法的定义中，或者是泛型方法的参数类型中。TypeVariable是Java泛型机制的核心概念之一。
2. WildcardType：表示通配符类型，例如 ? extends Number、? super T等。它们通常出现在泛型方法的参数类型中，或者是泛型类的类型参数的上限或下限中。WildcardType可以用于表示不确定的类型，例如表示可以是任何Number的子类。
3. ParameterizedType：表示参数化类型，例如List<String>、Map<Integer, String>等。它们是指具有实际类型参数的泛型类型，例如List<String>中的String就是实际类型参数。ParameterizedType可以用于获取泛型类型的实际类型参数，例如获取List<String>中的String。
4. GenericArrayType：表示泛型数组类型，例如T[]、List<String>[]等。它们表示具有泛型类型参数的数组类型，例如T[]表示元素类型为T的数组。GenericArrayType可以用于获取数组元素的类型，例如获取T[]中的T。
这四种泛型类型在Java语言规范中均有定义，并且可以通过反射API获取或操作它们。它们的含义和用途不同，使用时需要根据具体情况进行选择。



### 第7章 annotations包与lang包
@Param
在MyBatis中，@Param注解的作用是为方法参数取别名。当SQL语句中需要引用方法参数时，可以使用@Param注解为方法参数取一个别名，这样可以在SQL语句中直接使用别名来引用方法参数。
例如，假设我们有一个查询用户信息的方法，方法的参数为用户名和用户年龄：
```
List<User> selectUser(String username, int age);
```
我们可以使用@Param注解为方法参数取别名，如下所示：
```
List<User> selectUser(@Param("username") String username, @Param("age") int age);
```
这样，在SQL语句中就可以使用#{username}和#{age}来引用方法参数了。如果不使用@Param注解，MyBatis会默认使用参数名作为参数别名，但是如果方法参数名被混淆或者被压缩，就会导致SQL语句引用不到正确的方法参数。因此，在使用MyBatis时，建议为方法参数加上@Param注解来指定参数别名。


MyBatis中与@Param注解相关的主要类有：
- 1. org.apache.ibatis.annotations.Param
这是@Param注解的定义类，它是一个注解类，用于为方法参数取别名。@Param注解的定义如下：

```
@Documented
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.PARAMETER)
public @interface Param {
  String value();
}
```

@Param注解只有一个value属性，用于指定参数别名。
- 2. org.apache.ibatis.binding.MapperMethod.ParamMap
MapperMethod.ParamMap是MyBatis中用于保存方法参数的类，它继承自HashMap<Object, Object>，可以保存方法参数的名称和值。在执行SQL语句时，MyBatis会将MapperMethod.ParamMap中的参数值按照@Param注解指定的参数别名保存到BoundSql对象中，然后执行SQL语句。
- 3. org.apache.ibatis.executor.parameter.DefaultParameterHandler
DefaultParameterHandler是MyBatis中用于处理SQL语句参数的类，它实现了ParameterHandler接口。在执行SQL语句前，MyBatis会将MapperMethod.ParamMap中的参数值传递给DefaultParameterHandler对象，然后由DefaultParameterHandler对象将参数值设置到PreparedStatement对象中。
总的来说，@Param注解的作用是为方法参数取别名，然后将方法参数的别名和值保存到MapperMethod.ParamMap对象中。当执行SQL语句时，MyBatis会将MapperMethod.ParamMap中的参数值按照@Param注解指定的参数别名设置到PreparedStatement对象中，然后执行SQL语句。在这个过程中，DefaultParameterHandler类起到了关键作用，它负责将MapperMethod.ParamMap中的参数值设置到PreparedStatement对象中。


@Mapper作用
@Responsity与@Mapper区别
@Mapper的作用是将一个Mapper接口标记为MyBatis的映射器。在MyBatis中，Mapper接口是一个Java接口，用于定义SQL映射的接口，它的方法对应于SQL映射文件中的SQL语句。通过使用@Mapper注解，MyBatis可以将Mapper接口与SQL映射文件关联起来，从而实现SQL语句的执行。
@Mapper注解通常与@MapperScan注解一起使用，@MapperScan注解用于扫描Mapper接口所在的包，并将其注册到MyBatis的映射器中。
@Repository和@Mapper都是用于标识DAO(Data Access Object)层的注解，但是它们的用途略有不同。@Repository注解是Spring框架中的注解，用于标识DAO层组件，表示这个组件是用于数据访问的。而@Mapper注解是MyBatis中的注解，用于标识Mapper接口，表示这个接口是用于定义SQL映射的。
虽然@Mapper和@Repository都可以用来标识DAO层组件，但是它们的实现方式和作用域不同。@Repository注解通常用于标识整个DAO层组件，而@Mapper注解则用于标识Mapper接口中的方法，表示这些方法是用于执行SQL语句的。因此，在使用MyBatis时，建议使用@Mapper注解来标识Mapper接口，而不是使用@Repository注解。

@Mapper涉及到哪些类，这些类的作用
在MyBatis中，@Mapper注解涉及到以下几个类：
- 1. org.apache.ibatis.annotations.Mapper
这是@Mapper注解的定义类，它是一个注解类，用于将一个Mapper接口标记为MyBatis的映射器。
- 2. org.apache.ibatis.binding.MapperRegistry
MapperRegistry是MyBatis中用于管理Mapper接口的类，它维护了Mapper接口与对应的MapperProxyFactory对象之间的关系。在MyBatis初始化时，会从配置文件中读取所有的Mapper接口，并将其注册到MapperRegistry中，注册时会为每个Mapper接口创建一个MapperProxyFactory对象，用于处理Mapper接口方法的调用。
- 3. org.apache.ibatis.binding.MapperProxyFactory
MapperProxyFactory是MyBatis中用于创建Mapper接口代理对象的工厂类，它继承自MapperProxy，实现了InvocationHandler接口。当MapperRegistry注册一个Mapper接口时，会为该接口创建一个MapperProxyFactory对象，并将其保存到MapperRegistry中。当需要调用Mapper接口方法时，MyBatis会通过MapperRegistry获取对应的MapperProxyFactory对象，然后使用MapperProxyFactory创建一个Mapper接口代理对象，最终将方法调用转发给Mapper接口代理对象。
总的来说，@Mapper注解的作用是将一个Mapper接口标记为MyBatis的映射器，从而实现Mapper接口与SQL映射文件的关联。在实现过程中，@Mapper注解与MapperRegistry、MapperProxyFactory等类密切相关，这些类负责管理Mapper接口与对应的MapperProxyFactory对象之间的关系，并通过MapperProxyFactory创建Mapper接口代理对象，最终将方法调用转发给Mapper接口代理对象，从而实现SQL语句的执行。


### Chap. 8 type包

BaseTypeHandler (org.apache.ibatis.type)
    NClobTypeHandler (org.apache.ibatis.type)
    ClobReaderTypeHandler (org.apache.ibatis.type)
    OffsetTimeTypeHandler (org.apache.ibatis.type)
    ByteObjectArrayTypeHandler (org.apache.ibatis.type)
    DateOnlyTypeHandler (org.apache.ibatis.type)
    BlobTypeHandler (org.apache.ibatis.type)
    DateTypeHandler (org.apache.ibatis.type)
    IntegerTypeHandler (org.apache.ibatis.type)
    SqlTimeTypeHandler (org.apache.ibatis.type)
    NStringTypeHandler (org.apache.ibatis.type)
    CharacterTypeHandler (org.apache.ibatis.type)
    ArrayTypeHandler (org.apache.ibatis.type)
    StringTypeHandler (org.apache.ibatis.type)
    EnumOrdinalTypeHandler (org.apache.ibatis.type)
    BigDecimalTypeHandler (org.apache.ibatis.type)
    BooleanTypeHandler (org.apache.ibatis.type)
    SqlTimestampTypeHandler (org.apache.ibatis.type)
    BlobInputStreamTypeHandler (org.apache.ibatis.type)
    BlobByteObjectArrayTypeHandler (org.apache.ibatis.type)
    MonthTypeHandler (org.apache.ibatis.type)
    EnumTypeHandler (org.apache.ibatis.type)
    FloatTypeHandler (org.apache.ibatis.type)
    TimeOnlyTypeHandler (org.apache.ibatis.type)
    ByteTypeHandler (org.apache.ibatis.type)
    YearMonthTypeHandler (org.apache.ibatis.type)
    InstantTypeHandler (org.apache.ibatis.type)
    ObjectTypeHandler (org.apache.ibatis.type)
    ClobTypeHandler (org.apache.ibatis.type)
    DoubleTypeHandler (org.apache.ibatis.type)
    ShortTypeHandler (org.apache.ibatis.type)
    LongTypeHandler (org.apache.ibatis.type)
    LocalDateTypeHandler (org.apache.ibatis.type)
    UnknownTypeHandler (org.apache.ibatis.type)
    BigIntegerTypeHandler (org.apache.ibatis.type)
    ByteArrayTypeHandler (org.apache.ibatis.type)
    OffsetDateTimeTypeHandler (org.apache.ibatis.type)
    JapaneseDateTypeHandler (org.apache.ibatis.type)
    LocalDateTimeTypeHandler (org.apache.ibatis.type)
    ZonedDateTimeTypeHandler (org.apache.ibatis.type)
    SqlDateTypeHandler (org.apache.ibatis.type)
    YearTypeHandler (org.apache.ibatis.type)
    LocalTimeTypeHandler (org.apache.ibatis.type)




- SimpleTypeRegistry
- TypeAliasRegistry
- TypeHandlerRegistry


https://blog.csdn.net/Michelle_Zhong/article/details/129099305




### Chap. 9 io包
静态代理
org.apache.ibatis.io


DefaultVFS
mybatis开启日志的时候，有很多DefaultVFS相关的日志
MyBatis是一个Java持久层框架，提供了许多功能来简化数据库访问，其中DefaultVFS类是MyBatis中的一个重要类。
DefaultVFS类是MyBatis中用于处理文件系统的抽象类。它主要用于处理MyBatis的配置文件和映射文件的加载和访问。DefaultVFS类提供了一组方法来获取和处理文件，包括从类路径、文件系统和JAR文件中获取资源。
DefaultVFS类是MyBatis中的默认VFS实现，它使用Java标准库中的java.io和java.net包来实现文件系统的访问。如果需要使用其他的VFS实现来处理文件系统，可以通过在MyBatis的配置文件中配置vfsImpl属性来指定。
总之，DefaultVFS类是MyBatis中的一个重要类，用于处理文件系统的访问和管理，是MyBatis框架实现的核心之一。

linux里面的虚拟文件系统类似吗？
### Chap. 10 logging包
配置日志实现类：在MyBatis的配置文件中，可以通过设置<settings>标签下的<setting name="logImpl" value="日志实现类全名"/>来指定日志实现类。其中，日志实现类可以是log4j、log4j2、slf4j、jdkLog、stdoutLogging等。
mybatis_log.png

org.apache.ibatis.builder.BaseBuilder#typeAliasRegistry

org.apache.ibatis.session.Configuration#Configuration()

```java
    typeAliasRegistry.registerAlias("SLF4J", Slf4jImpl.class);
    typeAliasRegistry.registerAlias("COMMONS_LOGGING", JakartaCommonsLoggingImpl.class);
    typeAliasRegistry.registerAlias("LOG4J", Log4jImpl.class);
    typeAliasRegistry.registerAlias("LOG4J2", Log4j2Impl.class);
    typeAliasRegistry.registerAlias("JDK_LOGGING", Jdk14LoggingImpl.class);
    typeAliasRegistry.registerAlias("STDOUT_LOGGING", StdOutImpl.class);
    typeAliasRegistry.registerAlias("NO_LOGGING", NoLoggingImpl.class);
```
Adapter模式
反射的动态代理

日志级别
InvocationHandler
Proxy

LogFactory final类有静态方法
```java
  static {
    tryImplementation(LogFactory::useSlf4jLogging);
    tryImplementation(LogFactory::useCommonsLogging);
    tryImplementation(LogFactory::useLog4J2Logging);
    tryImplementation(LogFactory::useLog4JLogging);
    tryImplementation(LogFactory::useJdkLogging);
    tryImplementation(LogFactory::useNoLogging);
  }
```
Log接口
org.apache.ibatis.logging.Log

11个实现类
Log4j2LoggerImpl (org.apache.ibatis.logging.log4j2)
StdOutImpl (org.apache.ibatis.logging.stdout)
Jdk14LoggingImpl (org.apache.ibatis.logging.jdk14)
Slf4jImpl (org.apache.ibatis.logging.slf4j)
Slf4jLocationAwareLoggerImpl (org.apache.ibatis.logging.slf4j)
NoLoggingImpl (org.apache.ibatis.logging.nologging)
Slf4jLoggerImpl (org.apache.ibatis.logging.slf4j)
JakartaCommonsLoggingImpl (org.apache.ibatis.logging.commons)
Log4jImpl (org.apache.ibatis.logging.log4j)
Log4j2Impl (org.apache.ibatis.logging.log4j2)
Log4j2AbstractLoggerImpl (org.apache.ibatis.logging.log4j2)

配置日志实现类：在MyBatis的配置文件中，可以通过设置<settings>标签下的<setting name="logImpl" value="日志实现类全名"/>来指定日志实现类。其中，日志实现类可以是log4j、log4j2、slf4j、jdkLog、stdoutLogging等。
MyBatis解析XML文件的过程比较复杂，因此这里将会介绍`<settings>`标签的解析过程和`logImpl`属性对应的源码。
在MyBatis中，`<settings>`标签的解析过程是在`org.apache.ibatis.builder.xml.XMLConfigBuilder`类中完成的。在`parseConfiguration`方法中，会调用`parseConfigurationSettings`方法来解析`<settings>`标签，并将解析后的结果保存到`org.apache.ibatis.session.Configuration`对象中。
在`parseConfigurationSettings`方法中，会遍历所有的`<settings>`子标签，并将子标签的属性名和属性值保存到`Properties`对象中。其中，`logImpl`属性对应的属性名为`LOG_IMPL`。保存完后，将`Properties`对象设置到`Configuration`对象中，供后续使用。
以下是相关的代码片段：
```java
private void parseConfigurationSettings(XNode context) {
  Properties props = context.getChildrenAsProperties();
  // Set the log implementation.
  LogFactory.useCustomLogging(this.logImpl);
  if (props.containsKey("logPrefix")) {
    String logPrefix = props.getProperty("logPrefix");
    props.setProperty("logPrefix", logPrefix + this.logPrefix);
  }
  this.configuration.setVariables(props);
  ...
}
```
在这个代码片段中，`context`表示`<settings>`标签对应的`XNode`对象，`props`是将子标签的属性名和属性值保存到的`Properties`对象。在这个方法中，首先调用`LogFactory.useCustomLogging`方法设置日志实现类，然后将`props`设置到`Configuration`对象中，最后执行其他的配置项解析操作。
需要注意的是，`logImpl`属性对应的属性名为`LOG_IMPL`，而不是`logImpl`。因此，在配置文件中需要使用大写字母指定`logImpl`属性的值，例如`<setting name="LOG_IMPL" value="org.apache.ibatis.logging.stdout.StdOutImpl"/>`。
希望这能帮助你理解MyBatis中`<settings>`标签和`logImpl`属性的解析过程。

### Chap. 11 parsing包
org.apache.ibatis.parsing.XPathParser
MyBatis源码学习之XPathParser及XNode
https://www.cnblogs.com/beckwu/p/16112890.html

这个方法使用XPath解析XML文档，并获得解析出的对象。

evalXxx方法在evaluate方法的基础上作了一些处理，其中一个最重要的处理是将XPath解析获得的Node对象包装为XNode对象

org.apache.ibatis.parsing.XNode 父类Object，没有实现其他接口
XNode
调用XPathParser的evalBoolean()返回对象
有private final XPathParser xpathParser;这个field


org.apache.ibatis.parsing.GenericTokenParser
public class GenericTokenParser

private final String openToken;
private final String closeToken;
private final TokenHandler handler;

PropertyParser

GenericTokenParser是MyBatis中的一个基本解析器，它用于解析文本中的占位符并替换为实际的值。在MyBatis中，占位符通常用于动态SQL等场景中。
具体来说，GenericTokenParser可以将文本中的"${}"或"#"包围的占位符替换为实际的值。其中，"${}"用于替换属性值，"#"用于替换参数值。GenericTokenParser会将占位符中的内容作为key，查找对应的属性或参数值，并将占位符替换为实际的值。
GenericTokenParser的构造方法接受两个参数，第一个参数为开头和结尾的占位符的字符串，第二个参数为占位符解析器，用于解析占位符中的内容并返回实际的值。在MyBatis中，通常使用`org.apache.ibatis.parsing.PropertyParser`类作为占位符解析器，它可以解析属性占位符和环境变量占位符。

以下是GenericTokenParser的示例用法：

```java
String text = "SELECT * FROM user WHERE id = #{userId}";
ParameterMappingTokenHandler handler = new ParameterMappingTokenHandler();
GenericTokenParser parser = new GenericTokenParser("#{", "}", handler);
String sql = parser.parse(text);
```

在这个示例中，`text`表示要解析的文本，`handler`是实现了`org.apache.ibatis.parsing.TokenHandler`接口的参数处理器，用于处理占位符中的参数值。`parser`是一个GenericTokenParser对象，用于解析占位符并替换为实际的参数值。最终，`sql`变量会被替换为实际的SQL语句。
需要注意的是，GenericTokenParser只是MyBatis中的一个基本解析器，通常会和其他解析器一起使用，例如`org.apache.ibatis.scripting.xmltags.DynamicSqlSource`等。这些解析器将会利用GenericTokenParser解析占位符，并根据解析结果生成实际的SQL语句或其他内容。
希望这能帮助你理解GenericTokenParser的作用和用法。
DynamicSqlSource是MyBatis中的一个SQL源码对象，用于动态生成SQL语句。在MyBatis中，DynamicSqlSource通常会和其他SQL源码对象一起使用，例如RawSqlSource、ProviderSqlSource等，用于动态生成最终的SQL语句。
DynamicSqlSource的生成过程包括两个阶段：解析阶段和执行阶段。在解析阶段，DynamicSqlSource会使用MyBatis的SQL解析器解析SQL语句，并将解析结果保存到内部的`org.apache.ibatis.mapping.BoundSql`对象中。在执行阶段，DynamicSqlSource会根据传入的参数动态生成最终的SQL语句，并将结果保存到`BoundSql`对象中。
DynamicSqlSource的主要作用是支持动态SQL语句的生成。在MyBatis中，动态SQL语句通常由多个SQL节点组成，例如if节点、choose节点、foreach节点等，这些节点可以根据条件动态生成SQL语句的一部分。DynamicSqlSource会将这些SQL节点解析成一个个SQL片段，并根据条件动态拼接SQL语句，从而生成最终的SQL语句。
以下是一个使用DynamicSqlSource的示例：

```xml
<select id="getUser" resultType="User">
  SELECT * FROM user
  <where>
    <if test="name != null">
      AND name = #{name}
    </if>
    <if test="age != null">
      AND age = #{age}
    </if>
  </where>
</select>
```

在这个示例中，`<select>`节点中包含了一个if节点和一个where节点，用于动态生成SQL语句。在运行时，MyBatis会使用DynamicSqlSource将这些节点解析成一个个SQL片段，并根据条件动态拼接SQL语句，从而生成最终的SQL语句。
需要注意的是，DynamicSqlSource是MyBatis中的一个SQL源码对象，通常不会直接被使用。在MyBatis中，通常使用其他类型的SQL源码对象，例如RawSqlSource、ProviderSqlSource等，这些SQL源码对象会利用DynamicSqlSource动态生成最终的SQL语句。
希望这能帮助你理解DynamicSqlSource的作用和用法。

## 第3篇 配置解析包源码阅读

### 第12章 配置解析概述 124



### Chap. 13 binding包
org.apache.ibatis.binding

MapperMethod mm
父类是Object，没有实现任何接口
private final SqlCommand command;
private final MethodSignature method;

SqlCommand有六类
增删改查
清除缓存
未知
UNKNOWN, INSERT, UPDATE, DELETE, SELECT, FLUSH

MethodSignature是mm的静态内部类,方法签名，是Mapper接口的签名吗？
org.apache.ibatis.binding.MapperMethod.MethodSignature

mm内部类有三个？
mm内部类ParamMap，获取不存在的值会报错

mm 将java方法转化为数据库操作
execute()

mp调用mm
MapperProxy mp

org.apache.ibatis.binding.MapperRegistry#knownMappers
kv
key是Mapper接口
v是MapperProxyFactory mpf


### Chap. 14  builder包

org.apache.ibatis.builder;
org.apache.ibatis.builder.annotation;
org.apache.ibatis.builder.xml;

BaseBuilder (org.apache.ibatis.builder)
    XMLMapperBuilder (org.apache.ibatis.builder.xml)
    ParameterMappingTokenHandler in SqlSourceBuilder (org.apache.ibatis.builder)
    MapperBuilderAssistant (org.apache.ibatis.builder)
    XMLScriptBuilder (org.apache.ibatis.scripting.xmltags)
    XMLConfigBuilder (org.apache.ibatis.builder.xml)
    SqlSourceBuilder (org.apache.ibatis.builder)
    XMLStatementBuilder (org.apache.ibatis.builder.xml)

确切地说,SqlSourceBuilder类能够将DynamicSqlSource和RawSqlSource中的「# {}」符号替换掉，从而将它们转化为 StaticSqlSource,这一转化过程发生在代码14-7所示的parse方法中。因此，把SqISourceBui Ider类称作一个解析器或者转化器更合适。而事实 上，许多引用SqISourceBui Ider对象的地方都将对象的变量名定为 F sqISourceParserJ（在DynamicSqlSource和RawSqISource类中都能找到这个变量）。

MapperBuilderAssistant

CacheRefResolver

```xml
  <cache-ref namespace=""/>
```

ResultMapResolver

```xml

  <resultMap id="BaseResultMap" type="cn.wdidada.test.springbootmybatis.domain.OauthClientDetails">

```

public class ParameterExpression extends HashMap<String, String>

XMLMapperEntityResolver
public class XMLMapperEntityResolver implements EntityResolver

无网络环境下，校验dtd


XMLStatementBuilder


XMLIncludeTransformer



MapperAnnotationBuilder
@Select
@Insert
@Update
@Delete
@Param

ProviderContext
ProviderMethodResolver接口
ProviderSqlSource

### 第15章 mapping包
MappedStatement 典型的解析实体类

父类是Object，没有实现任何接口

public enum StatementType {
STATEMENT, PREPARED, CALLABLE
}

ResultSetType 是 MyBatis 中的一个枚举类型，它定义了返回结果集的类型。ResultSetType 有以下三个枚举值：
FORWARD_ONLY：只能向前滚动，不能滚动回去，也不能修改数据。
SCROLL_SENSITIVE：可以滚动，但不保证结果集是最新的。
SCROLL_INSENSITIVE：可以滚动，结果集是最新的。
ResultSetType 的默认值是 FORWARD_ONLY

org.apache.ibatis.mapping.MappedStatement.Builder


MappedStatement对象是队形mabatis xml文件中的insert update delete select吗？
是的，MyBatis中的MappedStatement对象代表了在Mapper XML文件中的SQL语句，包括insert、update、delete、select等操作。每个MappedStatement对象都对应一个具体的SQL语句，它包含了该SQL语句的ID、参数类型、返回类型、SQL语句等信息。
在MyBatis的Mapper XML文件中，每个SQL语句都需要定义一个唯一的ID，这个ID就是MappedStatement的ID。通过这个ID，MyBatis可以在运行时根据用户传入的参数执行相应的SQL语句，并将结果映射到指定的返回类型中。
除了SQL语句的信息，MappedStatement对象还包含了一些其他的属性，如缓存信息、SQL语句类型、语句参数的映射关系等。这些属性可以帮助MyBatis更好地优化SQL语句的执行效率、提高系统的性能表现。

SqlSource子类
ProviderSqlSource (org.apache.ibatis.builder.annotation)
StaticSqlSource (org.apache.ibatis.builder)
DynamicSqlSource (org.apache.ibatis.scripting.xmltags)
RawSqlSource (org.apache.ibatis.scripting.defaults)


DynamicSqlSource xml文件含有<if 占位符 ${}
RawSqlSource可能含有#{}
StaticSqlSource可能含有？可以直接提交给sql server
ProviderSqlSource注解形式的sql


mybatis ProviderSqlSource注解对应关系举例
在 MyBatis 中，ProviderSqlSource 是一种可以动态生成 SQL 语句的 SqlSource 实现。它的实现方式是通过一个带有 @ProviderSqlSource 注解的 Provider 类来生成 SQL 语句，然后将 SQL 语句和参数信息封装成一个 BoundSql 对象，最终交由 Executor 执行。
@ProviderSqlSource 注解中的 value 属性指定了对应的 Provider 类，而 method 属性指定了 Provider 类中用于生成 SQL 语句的方法名称。下面是一个简单的示例：
```java
@Mapper
public interface UserMapper {
  @SelectProvider(type = UserSqlProvider.class, method = "getUserById")
  User getUserById(Integer id);
}

public class UserSqlProvider {
  public String getUserById() {
    return "SELECT * FROM user WHERE id = #{id}";
  }
}
```
在上面的示例中，@SelectProvider 注解指定了 ProviderSqlSource 对应的 Provider 类为 UserSqlProvider，使用该类中的 getUserById() 方法生成 SQL 语句。getUserById() 方法返回一个字符串，其中包含了动态生成的 SQL 语句。MyBatis 会将该字符串封装成一个 ProviderSqlSource 对象，最终交由 Executor 执行。
当调用 UserMapper.getUserById() 方法时，MyBatis 会根据方法参数的值动态生成 SQL 语句，比如当传入 id = 1 时，生成的 SQL 语句为：
```sql
SELECT * FROM user WHERE id = 1
```
然后将该 SQL 语句和参数信息封装成一个 BoundSql 对象，交由 Executor 执行。这样就实现了动态生成 SQL 语句的功能。



mybatis，使用java代码中的静态常量
在 MyBatis 中，可以通过在 Mapper XML 文件中使用静态常量来引用 Java 代码中的常量，从而避免硬编码常量值，提高代码的可维护性和可读性。
下面是一个示例：

```java
public class Constants {
  public static final int STATUS_NORMAL = 1;
  public static final int STATUS_DELETED = 0;
}

@Mapper
public interface UserMapper {
  @Select("SELECT * FROM user WHERE status = #{status}")
  List<User> getUsersByStatus(@Param("status") int status);
}
```
在上面的示例中，定义了一个 Constants 类，其中定义了两个静态常量 STATUS_NORMAL 和 STATUS_DELETED。
在 UserMapper 接口中，使用 @Select 注解定义了一个 SQL 查询语句，其中使用了 status 参数来过滤用户记录。这里可以使用 #{status} 占位符来引用 status 参数的值。
如果要引用 Constants 类中的 STATUS_NORMAL 常量，可以在 Mapper XML 文件中使用如下的方式：
```xml
<select id="getUsersByStatus" resultType="User">
  SELECT * FROM user WHERE status = #{status, jdbcType=INTEGER, javaType=int, typeHandler=org.apache.ibatis.type.EnumOrdinalTypeHandler, numericScale=0}
    AND type = #{type, jdbcType=VARCHAR, javaType=String, numericScale=0, typeHandler=org.apache.ibatis.type.EnumTypeHandler}
    AND deleted = #{deleted, jdbcType=BIT, javaType=boolean}
    AND role = #{role, jdbcType=TINYINT, javaType=byte}
    AND level = #{level, jdbcType=SMALLINT, javaType=short}
    AND age = #{age, jdbcType=INTEGER, javaType=int}
    AND name = #{name, jdbcType=VARCHAR, javaType=String}
    AND salary = #{salary, jdbcType=DECIMAL, javaType=BigDecimal}
    AND birthday = #{birthday, jdbcType=TIMESTAMP, javaType=Date}
    AND range = #{range, jdbcType=ARRAY, javaType=List, typeHandler=org.apache.ibatis.type.ArrayTypeHandler}
    AND status = #{T(com.example.Constants).STATUS_NORMAL}
</select>
```
在上面的示例中，使用了 ${@类名@常量名} 的方式来引用常量，其中类名和常量名分别用点号分隔。在这个例子中，使用 #{T(com.example.Constants).STATUS_NORMAL} 来引用 Constants 类中的 STATUS_NORMAL 常量。注意，在这里使用的是 #{} 占位符，而不是 ${}。
这样就可以在 Mapper XML 文件中使用 Java 代码中的静态常量了。


xml文件中的
ResultMap
ResultMapping
Discriminator

父类都是Object，没有任何接口


ResultMap就是xml文件中<resultMap 节点对应的信息，有4个ResultMapping列表

在 MyBatis 中，Discriminator 元素可以根据某个字段的值来动态地映射不同的结果集。这个字段可以是查询语句中的任意一个列，也可以是传入参数中的一个值。
下面是一个简单的例子，演示如何使用 Discriminator 元素：
```xml
<resultMap id="animalResultMap" type="Animal">
  <id property="id" column="id"/>
  <result property="name" column="name"/>
  <result property="species" column="species"/>
  <discriminator javaType="string" column="species">
    <case value="cat" resultMap="catResultMap"/>
    <case value="dog" resultMap="dogResultMap"/>
    <case value="bird" resultMap="birdResultMap"/>
    <case value="fish" resultMap="fishResultMap"/>
  </discriminator>
</resultMap>

<resultMap id="catResultMap" type="Cat">
  <result property="meow" column="meow"/>
</resultMap>

<resultMap id="dogResultMap" type="Dog">
  <result property="bark" column="bark"/>
</resultMap>

<resultMap id="birdResultMap" type="Bird">
  <result property="chirp" column="chirp"/>
</resultMap>

<resultMap id="fishResultMap" type="Fish">
  <result property="swim" column="swim"/>
</resultMap>
```

在上面的例子中，定义了一个 Animal 类型的 resultMap，其中包含了一个 Discriminator 元素，它的 column 属性指定了用于区分不同结果集的字段是 species。根据 species 字段的值，MyBatis 会动态地选择对应的 resultMap，比如如果 species 的值是 cat，则会使用 catResultMap 来映射结果集。catResultMap、dogResultMap、birdResultMap 和 fishResultMap 分别对应了不同的 Animal 子类类型。
这样，当查询结果中包含了不同类型的 Animal 记录时，MyBatis 就会根据 species 字段的值来动态地选择正确的 resultMap，从而将查询结果映射到正确的 Java 对象中。
注意，在 Discriminator 元素中，可以使用 case 元素来指定不同的结果映射。每个 case 元素都包含了一个 value 属性和一个 resultMap 属性，value 属性指定了用于区分结果集的值，resultMap 属性指定了对应的 resultMap。


Environment
CacheBuilder

### 第16章 scripting包

org.apache.ibatis.scripting

DefaultParameterHandler implements ParameterHandler
ognl

LanguageDriver

XMLLanguageDriver (org.apache.ibatis.scripting.xmltags)
    RawLanguageDriver (org.apache.ibatis.scripting.defaults)


跟xml文件中的<if <choose <trim对应  节点树
SqlNode
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

ognl相关的类
OgnlClassResolver
OgnlMemberAccess
OgnlCache

DynamicContext

### 第17章 datasource包

### 第4篇 核心操作包源码阅读
### 第18章 jdbc包

SqlRunner
AbstractSQL
ScriptRunner

public class SQL extends AbstractSQL<SQL>
### 第19章 cache包

TransactionalCacheManager

Cache
    SoftCache (org.apache.ibatis.cache.decorators)
    PerpetualCache (org.apache.ibatis.cache.impl)
    LoggingCache (org.apache.ibatis.cache.decorators)
    SynchronizedCache (org.apache.ibatis.cache.decorators)
    LruCache (org.apache.ibatis.cache.decorators)
    ScheduledCache (org.apache.ibatis.cache.decorators)
    WeakCache (org.apache.ibatis.cache.decorators)
    FifoCache (org.apache.ibatis.cache.decorators)
    SerializedCache (org.apache.ibatis.cache.decorators)
    BlockingCache (org.apache.ibatis.cache.decorators)
    TransactionalCache (org.apache.ibatis.cache.decorators)


CacheException
CacheKey

CachingExecutor

二级缓存


### 第20章 transaction包
两套 jdbc managered
Transaction
TransactionFactory

JdbcTransactionFactory
JdbcTransaction


ManagedTransaction
ManagedTransactionFactory

### 第21章 cursor包

Cursor
DefaultCursor


### 第22章 executor包

CachingExecutor (org.apache.ibatis.executor)
BaseExecutor (org.apache.ibatis.executor)
    SimpleExecutor (org.apache.ibatis.executor)
    ClosedExecutor in ResultLoaderMap (org.apache.ibatis.executor.loader)
    ReuseExecutor (org.apache.ibatis.executor)
    BatchExecutor (org.apache.ibatis.executor)


ResultLoader

KeyGenerator
    NoKeyGenerator (org.apache.ibatis.executor.keygen)
    Jdbc3KeyGenerator (org.apache.ibatis.executor.keygen)
    SelectKeyGenerator (org.apache.ibatis.executor.keygen)


### 第23章 session包
### 第24章 plugin包

示例27
源码的示例28
org.apache.ibatis.plugin.Interceptor接口

org.apache.ibatis.plugin.Intercepts注解
org.apache.ibatis.plugin.Signatur注解

在 MyBatis 中，org.apache.ibatis.plugin.Signature 注解是用于标识一个方法是否可以被拦截的注解。它可以指定要拦截的类、方法名和方法参数类型，从而确定要拦截的方法。

Signatur 注解的作用是告诉 MyBatis，哪些方法应该被拦截，以及拦截时应该进行哪些处理。通过这种方式，可以在不修改原始代码的情况下，向现有的方法中注入额外的逻辑，从而实现增强功能。

下面是一个简单的示例，演示了如何使用 Signatur 注解来标识一个方法是否可以被拦截：

```java
@Intercepts({
  @Signature(type = Executor.class, method = "update", args = {MappedStatement.class, Object.class})
})
public class MyInterceptor implements Interceptor {
  @Override
  public Object intercept(Invocation invocation) throws Throwable {
    // 在调用 update 方法之前进行拦截和处理
    Object[] args = invocation.getArgs();
    MappedStatement ms = (MappedStatement) args[0];
    Object parameter = args[1];
    // 对参数进行修改
    parameter = modifyParameter(parameter);
    args[1] = parameter;
    // 调用原始方法
    Object result = invocation.proceed();
    // 对结果进行修改
    result = modifyResult(result);
    return result;
  }
}
```

在上面的示例中，定义了一个 MyInterceptor 拦截器，并使用 @Intercepts 和 @Signature 注解来标识要拦截的方法。在这个例子中，拦截的方法是 Executor 类中的 update() 方法，它接受两个参数，分别是 MappedStatement 和 Object 类型。
在 MyInterceptor 的 intercept() 方法中，会对参数进行修改，并调用原始方法执行。在原始方法执行完毕后，还可以对结果进行修改，并返回修改后的结果。
总之，org.apache.ibatis.plugin.Signature 注解是 MyBatis 中用于标识要拦截的方法的注解之一，它可以指定要拦截的类、方法名和方法参数类型，从而确定要拦截的方法。

MyBatis 中一共只有四个类的对象可以被拦截器替换，它们分别是 ParameterHandler、ResultSetHandler、StatementHandler 和 Executor。而且替换只能发生在固定的地方，我们称其为拦截点。

### 第5篇 总结与展望
### 第25章 源码阅读总结 378
### 第26章 优秀开源项目推荐 383

