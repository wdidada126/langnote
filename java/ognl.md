# ognl表达式

MyBatis用到了

OGNL是Object-Graph Navigation Language的缩写，它是一种功能强大的表达式语言（Expression Language，简称为EL），通过它简单一致的表达式语法，可以存取对象的任意属性，调用对象的方法，遍历整个对象的结构图，实现字段类型转化等功能。它使用相同的表达式去存取对象的属性。

对象图导航语言（Object Graph Navigation Language），简称OGNL，是应用于Java中的一个开源的表达式语言（Expression Language），它被集成在Struts2等框架中，作用是对数据进行访问，它拥有类型转换、访问对象方法、操作集合对象等功能。

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

mybatis ognl表达式

ognl表达式的作用
从java list bean中获取某个属性的值
不再用java代码，而是用dsl
在了解ognl的时候，我们需要知道它的三要素：
表达式（expression）
Root对象
上下文环境（ognlcontext）
有时候需要对这些上下文环境中的参数进行访问，访问这些参数时，需要通过#符号加上链式表达式来进行，从而表示与访问Root对象的区别。
在ognl中，对于静态变量或者静态方法的访问需要通过@【class】@【field/method】
ognl支持类似于数据库中的投影（projection）和选择（selection）功能：
？选择满足条件的所有元素
^ 选择满足条件的第一个元素
$ 选择满足条件的最后一个元素
ognl支持直接通过表达式来构造对象：
构造List：使用｛｝，中间使用逗号隔开元素的方式表达列表；
构造Map：使用#{}，中间使用逗号隔开键值对，并使用冒号隔开key和value来构造Map；
构造对象：直接使用已知对象的构造函数来构造对象。
临时的“当前对象”会被存储在一个叫做this的变量中——this指针。