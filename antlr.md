# antlr



重视对官方提供的antlr语法 github 的学习https://github.com/antlr/grammars-v4

图形工具 有一个

IDEA Preview



Lexi

token

ast

parser

dfn





ANTLR与与编译原理学习笔记

https://blog.csdn.net/qq_38835878/article/details/82355616



DFA

确定的有限自动机

org.antlr.v4.runtime.dfa.DFA





antlr的maven插件给生成的代码设置包名





LL

Antlr 支持上下文无关文法 LL(*)。
第一个L：从左至右分析输入；
第二个L: 使用最左派生分析语法规则；

Antlr4 现在支持直接左递归，但不支持间接左递归。

https://www.thinbug.com/q/46798136







sharding-jdbc之ANTLR4 SQL解析

https://my.oschina.net/u/3180962/blog/3100218/print



生成java代码的位置

target\generated-sources\antlr4

maven插件

https://www.zhihu.com/question/27051306/answer/35904732




maven插件



https://www.zhihu.com/question/27051306/answer/35904732




BNF是描述编程语言的文法。自然语言存在不同程度的二义性。这种模糊、不确定的方式无法精确定义一门程序设计语言。必须设计一种准确无误地描述程序设计语言的语法结构，这种严谨、简洁、易读的形式规则描述的语言结构模型称为文法。

最著名的文法描述形式是由Backus定义Algol60语言时提出的Backus-Naur范式（Backus-Naur Form, BNF）及其扩展形式EBNF。BNF能以一种简洁、灵活的方式描述语言的语法。具体内容可参考针对编译原理的书。

巴科斯范式


BNF是John Backus 在20世纪90年代提出的用以简洁描述一种编程语言的语言。

基本结构为：

<non-terminal> ::= <replacement>

non-terminal意为非终止符，就是说我们还没有定义完的东西，还可以继续由右边的replacement，也就是代替物来进一步解释、定义。

举个例子：

在中文语法里，一个句子一般由“主语”、“谓语”和“宾语”组成，主语可以是名词或者代词，谓语一般是动词，宾语可以使形容词，名词或者代词。那么“主语”、“谓语”和“宾语”就是非终止符，因为还可以继续由“名词”、“代词”、“动词”、“形容词”等替代。

例1. <句子> ::= <主语><谓语><宾语>

例2. <主语> ::= <名词>|<代词>

例3. <谓语>::=<动词>

例4. <宾语>::=<形容词>|<名词>|<代词>

例5. <代词>::=<我>

例6. <动词>::=<吃>

例7. <动词>::=<喜欢>

例8. <名词>::=<车>

例9. <名词>::=<肉>

如上，在::=左边的就是non-terminal非终止符，右边的就是replacement，可以是一系列的非终止符，如例1中的replacement便是后面例234左边的非终止符，也可以是终止符，如例56789的右边，找不到别的符号来进一步代替。

因此，终止符永远不会出现在左边。一旦我们看到了终止符，这个描述过程就结束了。


类似EBNF（Extended Backus-Naur Form）

ebnf是个规范，描述

cfg(上下文无关文法)

cfg的一个实现



cfg是一个数学概念，bnf ebnf是其计算机领域的实现



https://www.beichengjiu.com/informationscience/172297.html



熟悉SQL语言（关系代数、RBO、CBO）、编译原理，熟悉ANTLR、JavaCC、Calcite、SystemML或类似的开源框架，有DSL实现经验是加分项。


熟悉SQL语言（关系代数、RBO、CBO）、编译原理，熟悉ANTLR、JavaCC、Calcite、SystemML或类似的开源框架，有DSL实现经验是加分项。




[antlr 官网](https://www.antlr.org/)

[开源语法分析器--ANTLR 简介 2.7.5 ](https://blog.csdn.net/lionzl/article/details/88713123)




antlr

词法分析器（Lexer）

语法分析器（Parser）


[antlr](https://www.antlr.org/)

[开源语法分析器--ANTLR](https://www.cnblogs.com/blfshiye/p/4359390.html)


[antlr](https://www.antlr.org/)

[开源语法分析器--ANTLR](https://www.cnblogs.com/blfshiye/p/4359390.html)


词法分析是计算机科学中将字符序列转换为标记（token）序列的过程。从输入字符流中生成标记的过程叫作标记化（tokenization），在这个过程中，词法分析器还会对标记进行分类。

antlr可以对接多种语言
runtime


antlr idea插件的使用，需要熟悉


### antlr的概述

antlr是一个包含了`词法分析`,`语法分析`两大模块的工具，并且提供了大量主流语言的现成的语法描述`grammar`文件

使用antlr你可以将某种语言的代码文件，以纯文本字符串的方式输入，被antlr整理分析成一个语法树，一个可以清晰地从树状结构里，看到代码真正的逻辑的结构化数据。

通俗易懂的说，antlr的作用就是将计算机不明白，无法读取，无法执行的字符串代码，一个字一个字`读`，一行一行的`分析`，最后把`字符串`读明白了，分析明白了，转化成了计算机程序能`弄懂`(也就是能遍历，能执行，能运行的)的结构化数据`语法树`

听起来是不是很神秘？没错，这里面其实是编译原理里面的概念，我们所写的C++,OC,JAVA各种知名语言，我们其实写的都是一行一行字符串，这一行行的字符是怎么编译成可以运行的app的，这都是要经过这样的一个步骤，但这也只是编译原理中的一环，经过了`词法,语法解析`，后面还有很多重要的环节

- 有了`词法,语法解析`，我们甚至还可以独创我们自己的语言
- 有了`词法,语法解析`，再引入编译原理中的其他概念，我们甚至还可以自己写我们独创语言的编译器

看起来是不是很神秘很牛逼~我们今天深入讨论一下

##### antlr的基本使用

antlr包含以下几个部分

- antlr 主工程
- antlr 语法描述 grammer
- antlr 运行时 runtime



目标语言的语法描述grammer文件，在antlr官网可以下载,https://github.com/antlr/grammars-v4，从里面可以看到，我们可以找到几乎所有主流语言的语法描述，换句话说，如果我们要分析的语言有现成的grammar文件，那我们可以直接拿来输入给antlr就能搞起词法语法分析。

antlr主工程虽然是Java，但是antlr运行可以在Java，JavaScript，Python，C#等语言里，原因就是官网开放了这四种语言的antlr运行时，[www.antlr.org/download](http://www.antlr.org/download.html)。

举个通俗点的例子，如果我打算用JavaScript语言，用来分析Oc语法，那么

- 我需要先去官网下载`ObjectiveC.g4`grammer语法描述文件
- 我需要用antlr的Java主程序，输入OC的grammer，选择JavaScript语言输出，生成`ObjectiveCParser.js`这个用js代码写出来的，OC解析器
- 我需要开始搭建我的JS程序，将一整个antlr的JavaScript运行时都import进来，并且import进来刚刚生成的`ObjectiveCParser.js`，在JS代码里开始编写JSPatchConvertor的代码逻辑






#### README

antlr是Java语言开发的，

http://www.ietf.org/rfc/rfc4627.txt

Antlr4解析Json
https://blog.csdn.net/sjhuangx/article/details/100548057
https://blog.csdn.net/xindoo/article/details/104735750
https://blog.csdn.net/Freyr_Wings/article/details/78070181

[Antlr4 入门](https://www.cnblogs.com/clonen/p/9083359.html)

二.主要应用场景
1.定制特定领域语言（DSL)
类似hibernate中的HQL，用DSL来定义要执行操作的高层语法，这种语法接近人可理解的语言，由DSL到计算机语言的翻译则通过ANTLR来做，可在ANTLR的结构语言中定义DSL命令具体要执行何种操作。
2.文本解析 可利用ANTLR解析JSON，HTML，XML，EDIFACT，或自定义的报文格式。解析出来的信息需要做什么处理也可以在结构文件中定义。
3.数学计算 加减乘除，线性方程，几何运算，微积分等等

[another repo](https://github.com/edidada/antlr)

- ParseJsonMain
- ParseJsonMin 自定义visitor 可以查看回调的方法，参数


ParseJsonMain
Lex - token
Parse- 自定义result

```shell
Fri Oct 25 15:47:44 CST 2019 AnOtherVisitor visit
Fri Oct 25 15:47:44 CST 2019 AnOtherVisitor visitJson
Fri Oct 25 15:47:44 CST 2019 AnOtherVisitor visitChildren
Fri Oct 25 15:47:44 CST 2019 AnOtherVisitor visitAnObject
Fri Oct 25 15:47:44 CST 2019 AnOtherVisitor visitChildren
Fri Oct 25 15:47:44 CST 2019 AnOtherVisitor visitTerminal
Fri Oct 25 15:47:44 CST 2019 AnOtherVisitor visitPair
Fri Oct 25 15:47:44 CST 2019 AnOtherVisitor visitChildren
Fri Oct 25 15:47:44 CST 2019 AnOtherVisitor visitTerminal
Fri Oct 25 15:47:44 CST 2019 AnOtherVisitor visitErrorNode
Fri Oct 25 15:47:44 CST 2019 AnOtherVisitor visitArrayValue
Fri Oct 25 15:47:44 CST 2019 AnOtherVisitor visitChildren
Fri Oct 25 15:47:44 CST 2019 AnOtherVisitor visitArrayOfValues
Fri Oct 25 15:47:44 CST 2019 AnOtherVisitor visitChildren
Fri Oct 25 15:47:44 CST 2019 AnOtherVisitor visitTerminal
Fri Oct 25 15:47:44 CST 2019 AnOtherVisitor visitString
Fri Oct 25 15:47:44 CST 2019 AnOtherVisitor visitChildren
Fri Oct 25 15:47:44 CST 2019 AnOtherVisitor visitTerminal
Fri Oct 25 15:47:44 CST 2019 AnOtherVisitor visitTerminal

```

```

```

```


Antlr IDEA使用
安装插件 ANTLR v4 grammar plugin
maven插件  antlr4-maven-plugin
.g4文件右键


如何手动输入EOF
EOF是一个计算机术语，为End Of File的缩写，在操作系统中表示资料源无更多的资料可读取。资料源通常称为档案或串流。
而在不同系统的EOF所代表的值是不一样的，在Visual Studio 2017下为ctrl+c，windows下为ctrl+z，linux/unix下为ctrl+c或ctrl+d

[在IDEA中使用ANTLR4教程](https://blog.csdn.net/sherrywong1220/article/details/53697737)


#### Antlr Preview
文法可视化
打开Antlr Preview



在跟idea terminal 同样的位置

先选择.g4文件，然后选择

profile 主要是看性能和语法是不是有歧义，目前还没怎么用它。



在ArrayInit.g4中选中一个语法定义符号，如expr。右键选中的符合，选择Text Rule expr。
在ANTLR Preview中选择input,输入表达式，如{99,3,45}。则能显示出可视化的文法。



[ANTLR4的IntelliJ插件安装及示例Hello.g4   ](https://www.cnblogs.com/wynjauu/articles/9873231.html)


Antlr Preview
文法可视化
打开Antlr Preview。
在ArrayInit.g4中选中一个语法定义符号，如expr。右键选中的符合，选择Text Rule expr。
在ANTLR Preview中选择input,输入表达式，如{99,3,45}。则能显示出可视化的文法。

antlr4-maven-plugin生成的标准
自定义包
src\main\antlr4文件夹下放.g4文件
java代码生成包有两种方式
antlr4下放文件夹 文件夹的路径就是包

pom.xml中
<libDirectory>src/main/antlr4_imports</libDirectory>
.g4不会生成java文件 这个文件夹下面的.g4文件夹是代引用的
src/main/antlr4/文件夹下相对路径就是java代码的package名称


​```shell

@header {
package cn.wdidada;
}
@members {
double x, y; // keep column sums in these fields
}
```

```

//@header {
//package cn.wdidada;
//}
@members {
double x, y; // keep column sums in these fields
}




生成的文件在
target\generated-sources\antlr4



插件会为 src/main/antlr4 下的 .g4 文件在 target/generated-sources/antlr4 目录下生成好代码



.g4文件右键 configure antlr/Generator Antlr Recoginzer

选项

idea_antlr_opion.png



[ANTLR4使用](https://blog.csdn.net/qq_37255629/article/details/85239156)


从2.7.3版本开始，ANTLR开始支持C#

### ArrayInit 例子 testantlr 这个github repo

### ArrayInit







从2.7.3版本开始，ANTLR开始支持C#








### ArrayInit 例子 testantlr 这个github repo

{1,{2,3},4}
^D
(init { (value 1) , (value (init { (value 2) , (value 3) })) , (value 4) })



antlr-v4-grammar-plugin idea插件，有图形界面

Java grammar view
antlr语法中的fragment


https://www.crifan.com/




https://www.crifan.com/





#### .g4




​```shell

*
```
一次或多次？

```shell
+
```
至少一次

```shell
?
```

可选



ATN antlr



.g4


parser
head

？


[antlr v4 使用指南连载3——g4文件概览](https://www.cnblogs.com/laud/p/antlrv4_3.html)

[Antlr4 --- 规则文件概览](https://blog.csdn.net/yangguosb/article/details/85621059)

antlr

P.91





```
fragment 
```

https://abcdabcd987.com/notes-on-antlr4/

用 `fragment` 可以给 Lexer 规则中的公共部分命名



ANTLR4 笔记.mhtml



https://www.cnblogs.com/chunzhulovefeiyue/p/7577199.html


https://www.crifan.com/antlr_v3_syntax_fragment/

RuleContext
get

