# MyBatis技术内幕

https://book.douban.com/subject/27087564/

徐郡明

https://www.jb51.net/books/641555.html

源码讲解，不是用法





https://github.com/edidada/mybatis-3.4.2_src



MyBatis 小版本，大版本3.4  3.4.2版本代码

随书源码只有最后一章整合spring的

《MyBatis技术内幕》以MyBatis 3.4为基础，针对MyBatis的架构设计和实现细节进行了详细分析，其中穿插介绍了MyBatis源码中涉及的基础知识、设计模式以及笔者自己在实践中的思考

[MyBatis技术内幕](https://book.douban.com/subject/27087564/)

代理，如何实现


#### 第1章　MyBatis快速入门







#### 第2章　基础支持层
Java 5 推出了 javax.xml.xpath 包，这是一个用于 XPath 文档查询的独立于 XML 对象模型的库。
https://blog.csdn.net/pro_tian/article/details/84485391

XPath简介

XPath 使用路径表达式在 XML 文档中进行导航

XPath 包含一个标准函数库
XPath 是 XSLT 中的主要元素
XPath 是一个 W3C 标准


XPath 可用来在 XML 文档中对元素和属性进行遍历
https://www.w3school.com.cn/xpath/xpath_intro.asp

mybatis_xpath

https://mybatis.org/mybatis-3/zh/apidocs/org/apache/ibatis/parsing/XPathParser.html

解析mybatis-config.xml
还是Mapper.xml
A:mybatis-config.xml


Mybatis的configuration配置xml，Mybatis解析xml并没有简单使用DOM或者SAX解析，而是还使用XPath方法首先来查询是否有相应的节点信息，然后直接使用返回的Node信息进行解析；


https://zhuanlan.zhihu.com/p/31418285
https://stackoverflow.com/questions/24841581/mybatis-select-statement-for-xml-xpath-query-not-working
https://programtip.com/zh/art-75003




XMLMapperBuilder的parse方法
[mybatis 源码分析之 解析mapper.xml文件](https://blog.csdn.net/m0_37948170/article/details/104923608)
https://blog.csdn.net/flashflight/article/details/43926091

#### 第3章　核心处理层

OGNL表达式简介

对象导航图语言（Object Graph Navigation Language），简称*OGNL*，是应用于Java中的一个开源的表达式语言（Expression Language）



el表达式



直接通过#$获取java list map中的数据，或者类的属性数据





#### 第4章　高级主题

插件
spring-mybatis
mbg



