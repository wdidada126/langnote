spring_el

Spring 表达式语言(简称“ SpEL”)是一种功能强大的表达式语言，支持在运行时查询和操作对象图。语言语法类似于 Unified EL，但提供了其他功能，最著名的是方法调用和基本的字符串模板功能。

尽管还有其他几种 Java 表达式语言可用-OGNL，MVEL 和 JBoss EL，仅举几例-Spring 表达式语言的创建是为了向 Spring 社区提供一种受良好支持的表达式语言，该语言可用于以下版本中的所有产品 Spring 投资组合。它的语言功能由 Spring 产品组合中的项目要求所驱动，包括基于 Eclipse 的 Spring Tool Suite 中代码完成支持的工具要求。也就是说，SpEL 基于与技术无关的 API，如果需要，可以将其他表达语言实现集成在一起。

虽然 SpEL 是 Spring 产品组合中表达评估的基础，但它并不直接与 Spring 绑定，可以独立使用。为了自成一体，本章中的许多示例都将 SpEL 当作一种独立的表达语言来使用。这需要创建一些自举基础结构类，例如解析器。大多数 Spring 用户不需要处理这种基础结构，而只能编写表达式字符串进行评估。这种典型用法的一个示例是将 SpEL 集成到创建 XML 或基于注解的 Bean 定义中，如表达式支持，用于定义 bean 定义所示。



是的，@Value注解可以用于从属性文件或配置文件中获取值，并将这些值注入到Spring Bean 中的属性中。它可以用于注入基本类型、字符串、数组、集合等各种类型的值。

在@Value注解中，可以使用SpEL（Spring Expression Language）表达式来引用其他的Bean、调用方法、访问属性等。SpEL是一种强大的表达式语言，提供了灵活的表达式求值能力。

通过@Value注解，我们可以在运行时动态地将属性值注入到Bean中，使得配置信息可以灵活地进行管理和变更。这样我们就可以通过修改配置文件的方式来改变Bean的行为，而不需要修改Java代码。

所以，可以说@Value注解是调用了SpEL来实现属性值的注入和动态求值。

https://www.docs4dev.com/docs/zh/spring-framework/5.1.3.RELEASE/reference/core.html#expressions

spel 支持函数运算
```java
ExpressionParser parser = new SpelExpressionParser();

// invokes 'getBytes()'
Expression exp = parser.parseExpression("'Hello World'.bytes");
```

这里给出spring EL表达式的一些使用示例:

1. 引用bean: #{beanName}

```xml
<property name="someProperty">
    <ref bean="#{dataSource}" />  
</property>
```

2. 调用bean的方法: #{beanName.methodName()}

```xml
<property name="someProperty" value="#{dataSource.getConnection()}" />
```

3. 算术运算:

```xml
<property name="someInt" value="#{ 10 * 2}" />
```

4. 字符串连接:

```xml 
<property name="someStr" value="#{'Hello ' + 'World'}"/>
```

5. 判断:

```xml
<property name="online" value="#{ true}" />  
```

6. 引用配置值:

```xml
<property name="url" value="#{systemProperties['jdbc.url']}" />
```

7. 函数调用:

```xml
<property name="time" value="#{ T(java.lang.System).currentTimeMillis() }" />
```

8. 条件表达式:

```xml
<property name="#{activeProfile == 'dev' ? 'devConfig' : 'prodConfig' }" />
```

9. 调用静态方法:

```xml 
<property name="time" value= "#{ T(java.util.Calendar).getInstance().getTime().getTime()}"/>
```

希望以上示例给您提供参考! 如果还有其他任何问题,欢迎随时和我交流。