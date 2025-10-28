# bison

Flex和Bison的使用范式
Flex和Bison是实验框架默认的解析器生成工具，接下来我会介绍使用它们的最佳实践，由于Flex比较简单，主要是介绍Bison。
首先要明白的一点是，Flex和Bison的代码不是C和C++源代码，严格地说它们是专用于生成词法解析器和语法解析器的领域特定语言（DSL），一般的静态代码分析器通常不能很好地在上面工作，你的IDE也不能很好地助力你编写这些代码，因此最佳实践是：除非必要，否则尽可能不要将代码写在.l和.y文件里，让这两个文件保持尽可能地简单，除了生成词法和语法解析器外，不要有多余的功能。
Flex和Bison的代码文件在整体结构上都是被两个%%分成了三个部分：前言、主体、后记。理想情况下，后记完全可以留白，而前言中除了包含头文件指令不要写任何其它C/C++代码，所以，将你原本写在前言的C/C++代码都分离到两个另外的.h(.hpp)和.c(.cpp)文件中。如果你非要将代码.l和.y文件中，你应该在前言区只写函数和全局变量的声明，然后将定义写在后记中。
其次要明白的是，Flex和Bison是两个历史非常久远的工具了，许多现代的编程范式在其上都不适用，而且它们的用法是生成C代码，而不是C++，只是在后来逐步扩充了对其它功能的支持。所以，就本实验而言，如果你不想陷入对Flex和Bison琐碎的配置选项和技术细节的纠缠中，那么就应该小心地编写代码，尽量不要超出经典用法的场景。
Flex和Bison的联合使用
Flex和Bison生成的代码分处于两个C源代码文件，它们各自单独编译，然后通过外部链接机制最终链接为一个整体。
Flex和Bison默认用法的场景是传统的命令行指令式程序，生成使用全局变量的不可重入代码，并且Flex固定地从<stdio.h>输入输出数据。两者的关系以Bison为主，Flex只是辅助的可选项：Bison从代码文件生成一个int yyparse();函数，其内部调用两个需要我们补充定义的函数int yylex();、void yyerror(const char *)来读取词法单元流和报告错误，Flex就是用于生成那个yylex函数。
在联合使用时，我们应该首先编写Bison语法定义（.y），通过前言区的%token定义有哪几种词法单元，然后在Flex代码中包含生成的头文件，再编写词法单元的解析规则，这和我们实验1到实验2的顺序是相反的。

https://blog.csdn.net/u014132143/article/details/129489861

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

https://ftp.gnu.org/gnu/bison/

```shell
dpkg -L bison
/.
/usr
/usr/bin
/usr/bin/bison
/usr/bin/bison.yacc
/usr/share
/usr/share/aclocal
/usr/share/aclocal/bison-i18n.m4
/usr/share/bison
/usr/share/bison/README.md
/usr/share/bison/bison-default.css
/usr/share/bison/m4sugar
/usr/share/bison/m4sugar/foreach.m4
/usr/share/bison/m4sugar/m4sugar.m4
/usr/share/bison/skeletons
/usr/share/bison/skeletons/README-D.txt
/usr/share/bison/skeletons/bison.m4
/usr/share/bison/skeletons/c++-skel.m4
/usr/share/bison/skeletons/c++.m4
/usr/share/bison/skeletons/c-like.m4
/usr/share/bison/skeletons/c-skel.m4
/usr/share/bison/skeletons/c.m4
/usr/share/bison/skeletons/d-skel.m4
/usr/share/bison/skeletons/d.m4
/usr/share/bison/skeletons/glr.c
/usr/share/bison/skeletons/glr.cc
/usr/share/bison/skeletons/java-skel.m4
/usr/share/bison/skeletons/java.m4
/usr/share/bison/skeletons/lalr1.cc
/usr/share/bison/skeletons/lalr1.d
/usr/share/bison/skeletons/lalr1.java
/usr/share/bison/skeletons/location.cc
/usr/share/bison/skeletons/stack.hh
/usr/share/bison/skeletons/variant.hh
/usr/share/bison/skeletons/yacc.c
/usr/share/bison/xslt
/usr/share/bison/xslt/bison.xsl
/usr/share/bison/xslt/xml2dot.xsl
/usr/share/bison/xslt/xml2text.xsl
/usr/share/bison/xslt/xml2xhtml.xsl
/usr/share/doc
/usr/share/doc/bison
/usr/share/doc/bison/AUTHORS
/usr/share/doc/bison/ChangeLog-1998.gz
/usr/share/doc/bison/ChangeLog-2012.gz
/usr/share/doc/bison/NEWS.gz
/usr/share/doc/bison/README
/usr/share/doc/bison/THANKS.gz
/usr/share/doc/bison/TODO.gz
/usr/share/doc/bison/changelog.Debian.gz
/usr/share/doc/bison/copyright
/usr/share/doc/bison/examples
/usr/share/doc/bison/examples/README.md
/usr/share/doc/bison/examples/c
/usr/share/doc/bison/examples/c/README.md
/usr/share/doc/bison/examples/c/calc
/usr/share/doc/bison/examples/c/calc/Makefile
/usr/share/doc/bison/examples/c/calc/README.md
/usr/share/doc/bison/examples/c/calc/calc.y
/usr/share/doc/bison/examples/c/lexcalc
/usr/share/doc/bison/examples/c/lexcalc/Makefile
/usr/share/doc/bison/examples/c/lexcalc/README.md
/usr/share/doc/bison/examples/c/lexcalc/parse.y
/usr/share/doc/bison/examples/c/lexcalc/scan.l
/usr/share/doc/bison/examples/c/mfcalc
/usr/share/doc/bison/examples/c/mfcalc/Makefile
/usr/share/doc/bison/examples/c/mfcalc/calc.h
/usr/share/doc/bison/examples/c/mfcalc/mfcalc.y
/usr/share/doc/bison/examples/c/reccalc
/usr/share/doc/bison/examples/c/reccalc/Makefile
/usr/share/doc/bison/examples/c/reccalc/README.md
/usr/share/doc/bison/examples/c/reccalc/parse.y
/usr/share/doc/bison/examples/c/reccalc/scan.l
/usr/share/doc/bison/examples/c/rpcalc
/usr/share/doc/bison/examples/c/rpcalc/Makefile
/usr/share/doc/bison/examples/c/rpcalc/rpcalc.y
/usr/share/doc/bison/examples/c++
/usr/share/doc/bison/examples/c++/Makefile
/usr/share/doc/bison/examples/c++/README.md
/usr/share/doc/bison/examples/c++/calc++
/usr/share/doc/bison/examples/c++/calc++/Makefile
/usr/share/doc/bison/examples/c++/calc++/README.md
/usr/share/doc/bison/examples/c++/calc++/calc++.cc
/usr/share/doc/bison/examples/c++/calc++/driver.cc
/usr/share/doc/bison/examples/c++/calc++/driver.hh
/usr/share/doc/bison/examples/c++/calc++/parser.yy
/usr/share/doc/bison/examples/c++/calc++/scanner.ll
/usr/share/doc/bison/examples/c++/simple.yy
/usr/share/doc/bison/examples/c++/variant-11.yy
/usr/share/doc/bison/examples/c++/variant.yy
/usr/share/doc/bison/examples/d
/usr/share/doc/bison/examples/d/Makefile
/usr/share/doc/bison/examples/d/README.md
/usr/share/doc/bison/examples/d/calc.y
/usr/share/doc/bison/examples/java
/usr/share/doc/bison/examples/java/Calc.y
/usr/share/doc/bison/examples/java/Makefile
/usr/share/doc/bison/examples/java/README.md
/usr/share/lintian
/usr/share/lintian/overrides
/usr/share/lintian/overrides/bison
/usr/share/man
/usr/share/man/man1
/usr/share/man/man1/bison.1.gz
/usr/share/man/man1/bison.yacc.1.gz
```

After this operation, 572 kB of additional disk space will be used.
Get:1 http://archive.ubuntu.com/ubuntu focal/main amd64 libbison-dev amd64 2:3.5.1+dfsg-1 [355 kB]
Fetched 355 kB in 2s (198 kB/s)
Selecting previously unselected package libbison-dev:amd64.
(Reading database ... 95467 files and directories currently installed.)
Preparing to unpack .../libbison-dev_2%3a3.5.1+dfsg-1_amd64.deb ...

```
wdidada@DESKTOP-DAF8ST0:~$ dpkg -L libbison-dev
/.
/usr
/usr/lib
/usr/lib/x86_64-linux-gnu
/usr/lib/x86_64-linux-gnu/liby.a
/usr/share
/usr/share/doc
/usr/share/doc/libbison-dev
/usr/share/doc/libbison-dev/AUTHORS
/usr/share/doc/libbison-dev/ChangeLog-1998.gz
/usr/share/doc/libbison-dev/ChangeLog-2012.gz
/usr/share/doc/libbison-dev/NEWS.gz
/usr/share/doc/libbison-dev/README
/usr/share/doc/libbison-dev/THANKS.gz
/usr/share/doc/libbison-dev/TODO.gz
/usr/share/doc/libbison-dev/changelog.Debian.gz
/usr/share/doc/libbison-dev/copyright


bison --version
bison (GNU Bison) 3.5.1
Written by Robert Corbett and Richard Stallman.

Copyright (C) 2020 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
```