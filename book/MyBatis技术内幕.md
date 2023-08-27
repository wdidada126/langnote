# MyBatis技术内幕

https://book.douban.com/subject/27087564/

徐郡明

https://www.jb51.net/books/641555.html

Windows电脑上有pdf

源码讲解，不是用法


https://github.com/edidada/mybatis-3.4.2_src



MyBatis 小版本，大版本3.4  3.4.2版本代码

随书源码只有最后一章整合spring的

《MyBatis技术内幕》以MyBatis 3.4为基础，针对MyBatis的架构设计和实现细节进行了详细分析，其中穿插介绍了MyBatis源码中涉及的基础知识、设计模式以及笔者自己在实践中的思考

[MyBatis技术内幕](https://book.douban.com/subject/27087564/)

代理，如何实现
MyBatis 3.4.2 是一个 Java 持久化框架，它提供了动态代理来实现 SQL 语句的映射和数据库操作。在 MyBatis 中，动态代理主要用于生成 DAO（Data Access Object）接口的实现类。
在 MyBatis 3.4.2 中，可以使用动态代理实现以下类：
1. `MapperProxy`：这是 MyBatis 的核心动态代理类，用于生成 DAO 接口的代理实现类。它会根据接口定义和映射配置文件（XML 或注解）来生成对应的 SQL 语句和数据库操作。
2. `MapperProxyFactory`：这是 MapperProxy 的工厂类，用于创建 MapperProxy 实例。
这两个类是 MyBatis 中动态代理的主要实现类，它们负责在运行时动态生成 DAO 接口的代理对象，并将方法调用转发到实际的 SQL 语句执行和数据库操作。
需要注意的是，动态代理的具体工作方式和生成的代理代码结构在不同版本的 MyBatis 中可能会有所差异。上述提到的类名是基于 MyBatis 3.4.2 版本的命名，但在其他版本中可能会有所变化。
如果您需要更深入地了解 MyBatis 动态代理的实现原理和具体类，请参考 MyBatis 的官方文档或源代码。官方文档提供了详细的说明和示例，可以帮助您理解和使用 MyBatis 的动态代理功能。

#### 第1章　MyBatis快速入门



#### 第2章　基础支持层
Java 5 推出了 javax.xml.xpath 包，这是一个用于 XPath 文档查询的独立于 XML 对象模型的库。
https://blog.csdn.net/pro_tian/article/details/84485391

XPath简介

XPath 使用路径表达式在 XML 文档中进行导航

XPath 包含一个标准函数库
XPath 是 XSLT 中的主要元素
XPath 是一个 W3C 标准
爬虫用xpath


XPath 可用来在 XML 文档中对元素和属性进行遍历
https://www.w3school.com.cn/xpath/xpath_intro.asp

mybatis_xpath

https://mybatis.org/mybatis-3/zh/apidocs/org/apache/ibatis/parsing/XPathParser.html



见xpath.md



解析mybatis-config.xml
还是Mapper.xml
A:mybatis-config.xml


Mybatis的configuration配置xml，Mybatis解析xml并没有简单使用DOM或者SAX解析，而是还使用XPath方法首先来查询是否有相应的节点信息，然后直接使用返回的Node信息进行解析；


https://zhuanlan.zhihu.com/p/31418285
https://stackoverflow.com/questions/24841581/mybatis-select-statement-for-xml-xpath-query-not-working
https://programtip.com/zh/art-75003



XPathParser类

XMLMapperEntityResolver



PropertyParser. parse()方





ReflectorFactory 

XMLMapperBuilder的parse方法
[mybatis 源码分析之 解析mapper.xml文件](https://blog.csdn.net/m0_37948170/article/details/104923608)
https://blog.csdn.net/flashflight/article/details/43926091

第2 章介绍My Batis 基础支持层中各个模块的功能， 其中包括数据源模块、事务管理模块、
缓存模块、binding 模块、反射模块、类型转换模块、日志模块、资源加载模块和解析器模块。
这些模块相对独立，读者在实践中如果遇到类似的需求，可以直接参考MyBatis 的实现。


适配器模式

装饰器模式


第3 章介绍MyBatis 核心处理层的主要功能， 其中包括My Batis 初始化过程、动态SQL 的
解析过程、结果集的映射原理、SQL 语句的参数绑定、KeyGenerator 、StatementHandler 以及
Executor 等组件的实现原理。同时，还介绍了MyBatis 接口层的设计原理。

#### 第3章　核心处理层

OGNL表达式简介

对象导航图语言（Object Graph Navigation Language），简称OGNL，是应用于Java中的一个开源的表达式语言（Expression Language）



el表达式



直接通过#$获取java list map中的数据，或者类的属性数据





#### 第4章　高级主题

插件
spring-mybatis
mbg



