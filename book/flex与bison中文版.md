# flex与bison中文版

有第二版

本书的flex reference和bison reference以及后续章节可仔细阅读，前面章节的例子有点粗浅，过于简单。比如，关于SQL的解析，可以参看一下postgreSQL的源码，其SQL解析用的就是flex/bison。

ftp:///pub/file/flexbison.zip

可以下载，用FileZilla直接不用用户名密码下载

bison跟anltr的g4差不多

第一版的

flex的规则文件以.l为后缀名，生成的文件为lex.yy.c

bison的规则文件以.y为后缀，生成的文件为xxx.tab.c和xxx.tab.h

cfg的实现bnf是.g4 .y文件的理论部分

m4 linux库

这本书是《lex与yacc》的后继，作者是同一人。比起lex和yacc来，flex和bison有了很多先进的东西，毕竟lex和yacc实在是太老了。
这本书切掉了《lex与yacc》中没什么意思的菜单生成语言的一章。增加了关于高级主题的一章。并且大量更新了例子程序保持与时俱进。
我认为这本书里面非常有用的内容包括，flex与bison的用法、抽象语法树的构造和执行例子（《lex与yacc》中没有）、符号表的处理例子、SQL解析例子、多重语法词法分析程序讨论、可重入的语法词法分析程序讨论（《lex与yacc》中没有）、冲突的定位和解决、错误恢复和处理、GLR解析器（《lex与yacc》中没有）、生成C++解析器（《lex与yacc》中没有）。
对于符号表和抽象语法树，作者举了一个高级计算器的例子，本质上是一个支持自定义函数、分支语句和循环语句的小语言的解释器的例子。在讨论可重入的语法词法分析程序时，又把它改写成了可重入的版本，很有参考价值。
解析SQL的例子也很有意义，SQL语句本身非常复杂，为它写一个LALR(1)语法很不简单，书中的有些技巧可以参考。在后文讨论GLR分析的时候，又用GLR重写了一遍。
冲突的处理和错误的处理也很重要，这些内容比原来的《lex与yacc》充实了。
总的来说，如果看了这本书就不要去看《lex与yacc》了，那本的知识太老了，例子也不够好。如果想学flex和bison，看了这本书应该就算入门了吧，可以开始实践了。

[flex与bison中文版](https://book.douban.com/subject/6109479/)

评注：现在大数据兴起，nosql兴起，相关工具为了迎合熟悉sql的开发者，会兼容sql，sql解析工具大量使用

AI兴起，特定硬件的编译器需要前端

阿里云个人服务器上有源码

### Chap. 1 Flex和Bison简介

词法分析(lexical analysis,或scanning)和语法分析(syntax analysis,或parsing)

flex处理.l文件

Bison
上下文无关文法
Context Free grammer

BNF
Backus-Naur Form
其中Form是范式

flex .l文件包含三个部分，用%%来隔离

- 声明部分 definition         ----> c变量定义
- 规则部分 rules              语法分析
- c语言部分                   -----> c main函数，yylex()函数


c语言部分
yylex()

rules

RE

-lfl centos 7需要安装额外的库

bison


```shell
flex fb1-1.l

cc lex.yy.c -lfl

./a.out


bison -d fb1-5.y//fb1-5.tab.c fb1-5.tab.h
flex fb1-5.l
cc -o fb1-5 fb1-5.tab.c lex.yy.c -lfl

./fb1-5
```

flex bison与手写词法文法的对比

bison可以帮助验证是否有二义性



### Chap. 2 使用Flex

​重要语汇索引的符号表只需要简单的记录每隔单词以及它们所在的文件和行号

​        

### Chap. 3 使用Bison

 Bison语法分析器 



### 第4章 分析SQL 
SQL 规范 ansi iso
逆波兰特式 RPN




### 第5章 Flex规范参考


### 第6章 Bison规范参考
shift reduce

移进 归约

### 第7章 二义性和冲突


### 第8章 错误报告和恢复



### 第9章 Flex和Bison进阶


