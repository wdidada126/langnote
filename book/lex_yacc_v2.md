# lex_yacc_v2

高清PDF和源码

lex与yacc.pdf

flex bison


flex大量使用正则表达式



Lex与Yacc第二版高清版.pdf

E:\Lex与Yacc\《Lex与Yacc》中文第二版(带源码)\《Lex与Yacc》中文第二版

https://book.douban.com/subject/1105363/

源代码在gitee
https://gitee.com/edidada/lexYaccV2Project

### note

- 如何在linux系统上安装lex，并运行示例程序

[yacc/lex在linux 下 使用指南](https://blog.csdn.net/ruglcc/article/details/7817619)

[yacc/lex官方主页](http://dinosaur.compilertools.net/)


centos 7


```shell
sudo yum install byacc -y
sudo yum install flex -y
```
1.9.20130304-3.el7

2.5.37-6.el7


ld: cannot find -ll

解答：sudo yum install -y flex-devel

https://blog.csdn.net/a_flying_bird/article/details/54913824




repoquery -ql flex-devel
/usr/lib/libfl.a
/usr/lib/libfl_pic.a
/usr/lib/libl.a
/usr/lib64/libfl.a
/usr/lib64/libfl_pic.a
/usr/lib64/libl.a

/opt/rh/devtoolset-8/root/usr/libexec/gcc/x86_64-redhat-linux/8/ld: cannot find -ll


ubuntu使用flex和bison来代替lex和yacc

sudo apt-get install flex biso -y

运行

lex source-code.l

缺省会生成lex.yy.c文件，然后用gcc编译这个文件，注意要有-ll选项:
gcc lex.yy.c -o analyse -ll

gcc -ll 选项的含义

链接lex的库

生成analyse

```


lex ch1-02.l

gcc lex.yy.c -o example -ll

```
### flex

yytext
yylex

yyabort
yyaccept
yyclearin
yycreatebuffer
yyerror
yyerrork
yyflushbuffer
yydecl
yyinput
yyleng
yyless
yylex
yymore
yyoutput
yyparse
yyrecovering
yyrestart
yyterminateyytext
yyunput
yywrap

https://www.zhihu.com/question/21746909/answer/273457507



yyleng
只要扫描程序匹配标记时，标记的文本就存储在以空字符终止的字符串yytext中，而且它的长度存储在yyleng中，yyleng中的长度与由strlen(yytext)返回的值是相同的。
 
yyless()
从与规则相关的代码中调用yyless(n)，这条规则推回除标记开头的几个字符以外的所有字符。当决定标记之间边界的规则不方便表示为正则表达式时，它是很有用的
例：
\"[^"]\"  {
           if(yytext[yyleng-2]=='\\')
           {
            yyless(yyleng-1);
            yymore();
           }
           else
            {
            .......
            }
          }
yyless()的另一用处是使用不同的其实状态的规则从新处理标记：
sometoken{BEGIN OTHER_STATE;yyless(0);}
 
yylex()
由lex创建的扫描程序的入口点yylex()。调用yylex()启动或者重新开始扫描。如果lex动作执行讲数值传递给调用的程序return,那么对yylex()的下次调用就从它的停止地方继续。
 
yylex()中的用户代码
规则段中的所有代码都被拷贝到yylex()。以空白开始的行被假定是用户代码。"%%"后的代码直接放置在接近扫描程序的开始处，在第一条执行的语句之前。
 
yymore()
可以从与规则相关的代码中调用yymore()，这条规则告诉lex给这个标记附加下一个标记
 
yytext
每当词法分析程序匹配标记时，标记的文本就存储在以空字符结尾的字符串yytext中
每次匹配一个新的标记时，就要替换yytext的内容，如果yytext的内容还要使用，通过strdup()或者自己申请内存来保存字符串拷贝，从而使字符串的拷贝拷贝位于刚刚分配的内存中。
 
yywrap()
当词法分析程序遇到文件结尾时，它调用例程yywrap()来找出下一步要做什么，如果返回0，扫描程序继续扫描，如果返回1，扫描程序就返回报告文件结尾需标记。
 
lex库中yywrap()的标准版本总是返回1，如果yywrap()返回指示有更多的输入0，那么它首先需要调整指向新的文件yyin,可能使用fopen()。
 
起始状态
在定义段可以声明起始状态，也称起始状态条件或起始规则。起始状态用于限制某些规则的范畴，或者改变词法分析程序处理部分文件的方式。
没有起始状态的那些规则能应用于任何状态。
动作中的BEGIN语句设置了当前的起始状态。


https://github.com/westes/flex/

bison

http://www.gnu.org/software/bison/
http://www.gnu.org/software/bison/manual/bison.html

### Chap. 1



lex yacc文件分为三个部分
哪三个部分？

lex ch1-02.l
gcc lex.yy.c -o example -ll
```
lex yacc文件分为三个部分




```



### Chap. 2



1


### Chap. 3

### Chap. 4
4
### Chap. 5
5
### Chap. 6
6
### Chap. 7
7
### Chap. 8

8
### Chap. 9
9