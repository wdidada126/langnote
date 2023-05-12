# 通用源码阅读指导书：MyBatis源码详解

https://www.zhihu.com/pub/reader/120079431

https://book.douban.com/subject/35138963/

2020年8月出版

按照java的包来分类阅读代码的
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
org.apache.ibatis.io


DefaultVFS
mybatis开启日志的时候，有很多DefaultVFS相关的日志
MyBatis是一个Java持久层框架，提供了许多功能来简化数据库访问，其中DefaultVFS类是MyBatis中的一个重要类。
DefaultVFS类是MyBatis中用于处理文件系统的抽象类。它主要用于处理MyBatis的配置文件和映射文件的加载和访问。DefaultVFS类提供了一组方法来获取和处理文件，包括从类路径、文件系统和JAR文件中获取资源。
DefaultVFS类是MyBatis中的默认VFS实现，它使用Java标准库中的java.io和java.net包来实现文件系统的访问。如果需要使用其他的VFS实现来处理文件系统，可以通过在MyBatis的配置文件中配置vfsImpl属性来指定。
总之，DefaultVFS类是MyBatis中的一个重要类，用于处理文件系统的访问和管理，是MyBatis框架实现的核心之一。

### Chap. 10 logging包


### Chap. 11 parsing包

MyBatis源码学习之XPathParser及XNode
https://www.cnblogs.com/beckwu/p/16112890.html

这个方法使用XPath解析XML文档，并获得解析出的对象。

evalXxx方法在evaluate方法的基础上作了一些处理，其中一个最重要的处理是将XPath解析获得的Node对象包装为XNode对象


XNode
调用XPathParser的evalBoolean()返回对象

## 第3篇 配置解析包源码阅读

### 第12章 配置解析概述 124



### Chap. 13 binding包

### Chap. 14  builder包

### 第15章 mapping包 169
### 第16章 scripting包 179
### 第17章 datasource包 208
### 第4篇 核心操作包源码阅读
### 第18章 jdbc包 232
### 第19章 cache包 243
### 第20章 transaction包 279
### 第21章 cursor包 284
### 第22章 executor包 293
### 第23章 session包 355
### 第24章 plugin包 366
### 第5篇 总结与展望
### 第25章 源码阅读总结 378
### 第26章 优秀开源项目推荐 383

