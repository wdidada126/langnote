# xpath

selenium使用过xpath

XPath是一种在XML文档中查找信息的语言，它可以用来查询XML文档中的元素、属性、文本等信息。在C++中，可以使用第三方库来实现XPath的解析和查询，例如Xerces-C++和libxml2等库。
下面以Xerces-C++为例，介绍如何在C++中使用XPath。



chrome xpath helper 选中节点 -> copy > copy xpath
https://blog.csdn.net/love666666shen/article/details/72613143


xpath之于XML 就好比SQL 语言之于数据库。
ognl之于java Object

chrome浏览器有插件，可以直接复制xpath
xpath chrome插件
https://github.com/google/xpaf

XPath Helper：chrome爬虫网页解析工具

W3C 标准
万维网联盟（外语缩写：W3C）标准不是某一个标准，而是一系列标准的集合。
网页主要由三部分组成：结构（Structure）、表现（Presentation）和行为（Behavior）。
https://baike.baidu.com/item/W3C%E6%A0%87%E5%87%86/8367679?fr=aladdin

https://www.w3.org/TR/xpath/

解析xml（html

https://www.w3school.com.cn/xpath/index.asp

爬虫解析库：XPath

https://www.w3.org/TR/xpath/

版本
3.1
3.0
2.0 (Second Edition)
1.0


https://www.w3school.com.cn/xpath/xpath_syntax.asp


| 表达式   | 描述                                                       |
| -------- | ---------------------------------------------------------- |
| nodename | 选取此节点的所有子节点。                                   |
| /        | 从根节点选取。                                             |
| //       | 从匹配选择的当前节点选择文档中的节点，而不考虑它们的位置。 |
| .        | 选取当前节点。                                             |
| ..       | 选取当前节点的父节点。                                     |
| @        | 选取属性。                                                 |




xpath教程
https://www.w3schools.cn/xml/xml_xpath.asp

https://gitee.com/edidada/testmybatis jdbc分支


mybatis使用xpath技术解析xml

```java
        String expression = "/persons/person[1]//@id";
        expression = "/persons/dog/name";
```




爬虫，也是使用xpath



通过libxml2的xpath解析xml

https://gnome.pages.gitlab.gnome.org/libxml2/devhelp/libxml2-xpath.html


C++ 使用带有TinyXPath的XPath获取属性 TinyXML
http://duoduokou.com/cplusplus/36747499392874930107.html

## mybatis中使用xpath spring框架使用xpath

XPath（XML Path Language）是一种用于在 XML 文档中进行导航和查询的语言。在 Spring 框架中，XPath 可以用于多个地方，包括配置文件解析、XML 数据绑定等。下面是在 MyBatis 和 Spring 框架中使用 XPath 的一些示例：

### 在 MyBatis 中使用 XPath：

MyBatis 是一个支持使用 XML 配置文件进行 SQL 映射的持久层框架。在 MyBatis 的 XML 映射文件中，你可以使用 XPath 来选择和处理 XML 元素。

```xml
<!-- 使用XPath在MyBatis映射文件中选择特定的元素 -->
<select id="selectUserById" resultType="User">
  SELECT * FROM users WHERE id = #{id}
</select>
```

在上述示例中，`<select>` 元素的 `id` 属性值就是XPath，用于在映射文件中选择相应的 SQL 查询。

### 在 Spring 框架中使用 XPath：

Spring 框架中有许多地方使用了 XPath，其中一些包括：

1. 配置文件解析：Spring 的配置文件（如 applicationContext.xml）可以包含 XML 元素和属性，你可以使用 XPath 来选择和配置这些元素。

```xml
<bean id="dataSource" class="org.springframework.jdbc.datasource.DriverManagerDataSource">
  <property name="url" value="jdbc:mysql://localhost:3306/mydb"/>
  <property name="username" value="root"/>
  <property name="password" value="password"/>
</bean>
```

在上述示例中，XPath 被用于选择 `<property>` 元素的 `name` 和 `value` 属性。

2. XML 数据绑定：Spring 提供了 XML 数据绑定的功能，可以将 XML 数据映射到 Java 对象上。XPath 用于指定 XML 元素和 Java 对象之间的映射关系。

```xml
<bean id="userMapper" class="com.example.UserMapper">
  <property name="xpathExpression" value="/user"/>
</bean>
```

在上述示例中，`xpathExpression` 属性的值就是 XPath 表达式，用于指定将哪些 XML 元素映射到 Java 对象上。

总之，XPath 在 MyBatis 和 Spring 框架中的使用主要涉及到 XML 配置文件的解析、查询和映射等方面。它是一种强大的工具，能够帮助你在 XML 数据中进行选择和导航，以及将 XML 数据映射到 Java 对象上。