# flex与bison中文版



[flex与bison中文版](https://book.douban.com/subject/6109479/ )



阿里云个人服务器上有源码

### Chap. 1

Bison
上下文无关文法
Context Free grammer

BNF
Backus-Naur Form
其中Form是范式

flex/bison包含三个部分

- 声明部分
- 规则部分
- c语言部分


c语言部分
yylex()

rules

RE



-lfl centos 7需要安装额外的库



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



### Chap. 2

​      重要语汇索引的符号表只需要简单的记录每隔单词以及它们所在的文件和行号

​        

### Chap. 3

 Bison语法分析器 



 第4章 分析SQL 

