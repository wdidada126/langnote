---
title: the c programming language
date: 2017-10-24 08:57:36
categories:
- Diary
tags:
- Linux
- Note
- c

---

# the c programming language

## printf()函数

%d 按照十进制整形打印

%6d 按照十进制整形打印，至少6个字符宽

%f 按照浮点数打印

%6f 按照十进制浮点数打印，至少6个字符宽

%.2f 按照浮点数打印，小数点后有两位小数

%6.2f 按照浮点数打印，至少6个字符宽，小数点后有两位小数

%o 表示八进制

%x 表示十六进制

%c 表示字符

%s 表示字符串

%% 表示百分号本身

%ld 表示输出的是long整形 

<!-- more -->

## 符号常量

#define 指令可以把符号名（或称为符号常量）定义为一个特定的字符串

#define 名字 替换的文本

## 字符输入输出

int getchar()

putchar(int c)

在读写文件时，之所以声明称int类型，是因为要存储EOF，值必须足够大。

char getchar()

putchar(char c)

EOF定义在头文件 <stdio.h>

ANSI C语言中的全部转义字符序列如下所示：
\a
\\
\b
\?
\f
\'
\n
\"
\r
\ooo
\t
\v
\xhh

字符常量 '\0'表示值为0的字符，也就是空字符(null)

常量表达式 是仅仅只包含常量的表达式。这种表达式在编译时求值，而不在运行时求值。


