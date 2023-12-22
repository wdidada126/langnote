# make

make -j4 2>&1 | tee out.txt


多看官网文档



make


redis的makefile值得学习，有make uninstall

https://www.gnu.org/software/make/manual/make.pdf

GNU make Version 4.3



make 3.8.2 中文文档

https://free-online-ebooks.appspot.com/tools/gnu-make-cn/make-01.html

https://hacker-yhj.github.io/resources/gun_make.pdf



https://blog.csdn.net/weixin_42645653/article/details/114887822





srpc GNUmakefile

g++ xxx.cc -o xxx

make

xxx : xxx.cc
	g++ xxx.cc -o xxx


Make命令教程
http://www.ruanyifeng.com/blog/2015/02/make.html

make -f xxxfile
make默认会找makefile来进行build操作

Makefile文件由一系列规则（rules）构成。每条规则的形式如下。


<target> : <prerequisites> 
[tab]  <commands>
上面第一行冒号前面的部分，叫做"目标"（target），冒号后面的部分叫做"前置条件"（prerequisites）；第二行必须由一个tab键起首，后面跟着"命令"（commands）。

"目标"是必需的，不可省略；"前置条件"和"命令"都是可选的，但是两者之中必须至少存在一个。

.PHONY 明确表示伪目标


内置变量（Implicit Variables）
Make命令提供一系列内置变量，比如，$(CC) 指向当前使用的编译器，$(MAKE) 指向当前使用的Make工具。这主要是为了跨平台的兼容性


## Makefile提供了许多内置函数
http://www.gnu.org/software/make/manual/html_node/Functions.html
cmake也有内置函数


http://www.gnu.org/software/make/

make 官方

## make本质
make编译java go c/cpp nodejs
本质是对命令行/shell的封装


语法

.PHONY

make test

make clean

sudo make install

.o .c



CXX gcc

需要熟悉gcc的参数

makefile + make 执行各种命令行脚本



make支持Go语言的编译



windows有make嘛？

有windows下使用gcc和g++需要安装MinGW32，如果已经安装过了，参考[这里](https://www.cnblogs.com/XiongWinds/p/7594795.html)，然后改一下名字为make.exe

否则需要先安装MinGW32，参考[这里](https://blog.csdn.net/Nicholas_Liu2017/article/details/78323391)

MinGW32只能编译32位程序，要想编译64位，需要安装MinGW-w64，参考 [MinGW-w64离线安装](https://blog.csdn.net/ZHAOJUNWEI08/article/details/86602120)，在线安装可能无法访问，







windows下cmake是否也是生成make执行的makefile文件来执行
是




widows下也有自己的命令行编译工具，比如msbuild，nmake等。这两个工具是和VS一起升级维护的，所以对于像笔者这样，一台机器安装3个版本的VS的人，要使用正确版本的编译工具其实需要走些弯路。



xmake

