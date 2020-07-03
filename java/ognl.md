# ognl表达式

对象导航图语言（Object Graph Navigation Language），简称OGNL，是应用于Java中的一个开源的表达式语言（Expression Language），它被集成在Struts2等框架中，作用是对数据进行访问，它拥有类型转换、访问对象方法、操作集合对象等功能。

1.什么是OGNL
OGNL：Object Graphic Navigation Language(对象图导航语言)
它是Struts2中默认的表达式语言。使用表达式需要借助Struts2的标签.
OGNL与EL的区别：
EL／JSTL 数学运算等等表达式：　都有一个明确的返回值，都只能取值。
　　　　　OGNL表达式: 它不仅可以取值，还可以赋值(赋值操作只能由Struts来完成)
OGNL表达式的写法:属性.属性.属性的方式<input type="text" name="user.user"/>
OGNL表达式的基本使用:
使用s:property标签输出内容
访问普通方法
访问静态方法
访问静态属性
操作集合(List AND Map)
