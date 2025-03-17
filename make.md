# make

makefile本身为了替代shell，你小子倒好，反过来了
makefile支持增量编译


新版本的LFS里，越来越多的软件包用meson和cmake了。各有各的好吧


https://github.com/adamdunkels/uip

make多个文件夹，分离式编译吗？
app/hello-world/Makefile.hello-world
unix/Makefile
lib/
uip/Makefile.include

在C或C++项目中，make是一个常用的构建工具，用于自动化编译过程。使用make时，通常会在项目的不同部分定义多个Makefile文件，以组织构建过程。这种做法通常被称为分离式编译。

在您给出的例子中，我们有以下文件和目录结构：

app/  
    hello-world/  
        Makefile.hello-world  
unix/  
    Makefile  
lib/  
    ... (可能是库文件或库源代码)  
uip/  
    Makefile.include
根据这个结构，我们可以推测以下几点：

app/hello-world/Makefile.hello-world：这个文件可能是用来构建app/hello-world目录下的程序的。它可能定义了构建hello-world程序所需的依赖项、源文件列表、编译器选项等。

unix/Makefile：这个文件可能是用来构建unix目录下的内容或整个项目在Unix-like系统上的构建规则。它可能调用其他Makefile（例如uip/Makefile.include），或者处理特定于Unix系统的编译和链接选项。

lib/：这个目录可能包含库文件或库的源代码。通常，库会有自己的构建系统，但也可以由其他Makefile调用其构建过程。

uip/Makefile.include：这个文件可能被其他Makefile包含，提供了一些通用的构建规则或变量定义。通常，这样的文件包含了编译和链接的通用设置，以便在不同的Makefile中重用。

分离式编译意味着每个组件（或模块）都有自己的构建脚本，这有助于保持构建规则的模块化，使得每个组件都可以独立构建，而不需要关心其他组件的详细信息。这也有助于维护大型项目，因为不同部分的开发人员可以专注于他们自己的构建脚本，而不必担心影响其他部分。

在实践中，你可能还会看到在顶层目录（例如项目的根目录）有一个Makefile，它协调各个子目录的构建过程。这种顶层Makefile可能会调用各个子目录中的Makefile，并处理任何跨模块的依赖关系。

总的来说，make的灵活性和模块化特性使得它能够适应各种复杂的项目结构，而分离式编译是这种灵活性的一个重要体现。


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

make -C /home/user/project
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

