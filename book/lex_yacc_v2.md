# lex_yacc_v2

高清PDF和源码

lex与yacc.pdf

Lex与Yacc第二版高清版.pdf



https://book.douban.com/subject/1105363/



### note

- 如何在linux系统上安装lex，并运行示例程序

[yacc / lex 在linux 下 使用指南](https://blog.csdn.net/ruglcc/article/details/7817619)

[yacc / lex官方主页](http://dinosaur.compilertools.net/)


```shell
yum install byacc -y
yum install flex -y
```

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