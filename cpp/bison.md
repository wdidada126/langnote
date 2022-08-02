# bison

bison --version
bison (GNU Bison) 3.0.4
Written by Robert Corbett and Richard Stallman.

Copyright (C) 2015 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.


bison 2.3 mac系统

yum install bison -y

### api doc

Win 电脑bison.pdf 英文版，找中文版

https://www.gnu.org/software/bison/manual/bison.html#C_002b_002b-Parsers 谷歌翻译

https://www.gnu.org/software/bison/manual/bison.html

汉语翻译
https://blog.csdn.net/Chinamming/article/details/84507258

### 表达式的优先级

例子：四则运算的加减乘除
乘除优先级高于加减
从左到右
从右到左

%left
%right
其中的 %left 表明这些符号是左结合的。同一行的符号优先级相同，下面行的符号的优先级高于上面的。

终结符使用%token，非终结符使用%type来定义
Bison中默认将所有的语义值都定义为int类型，可以通过定义宏YYSTYPE来改变值的类型。如果有多个值类型，则需要通过在Bison声明中使用%union列举出所有的类型，然后为每个符号定义相对的类型，终结符使用%token，非终结符使用%type来定义。
https://blog.csdn.net/xzz_hust/article/details/45009147