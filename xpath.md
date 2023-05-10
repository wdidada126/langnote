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

