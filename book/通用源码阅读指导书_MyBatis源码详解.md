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



第7章 annotations包与lang包





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



### Chap. 10 logging包


### Chap. 11 parsing包

MyBatis源码学习之XPathParser及XNode
https://www.cnblogs.com/beckwu/p/16112890.html

这个方法使用XPath解析XML文档，并获得解析出的对象。

evalXxx方法在evaluate方法的基础上作了一些处理，其中一个最重要的处理是将XPath解析获得的Node对象包装为XNode对象


XNode
调用XPathParser的evalBoolean()返回对象

第3篇 配置解析包源码阅读

### 第12章 配置解析概述 124



### Chap. 13

### Chap. 14  builder包


