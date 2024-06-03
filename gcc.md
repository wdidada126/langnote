# gcc

而C/C++编译器版本多于一个，并没有某个编译器占据了绝对统治地位。至少，intel的icc，微软的msvc，gnu的gcc，以及后起之秀clang，都各自有各自的地位，要协调多方意见制作大家认可的标准并不容易，改变起来自然更加耗时。

其实Windows还有一个由RAD Studio附带的bcc编译器，效率也很好

## releases

gcc 14.1
GCC 14.1 编译器计划在2024年5月7日左右发布
https://gcc.gnu.org/pipermail/gcc/2024-May/243921.html


https://mirror.linux-ia64.org/gnu/gcc/releases/

gcc 4.8编译gcc11不行吧？
g++ (GCC) 4.8.5 20150623 (Red Hat 4.8.5-44)
要在CentOS 7.9上编译GCC 11，您需要确保您的系统上安装了适当的GCC版本。GCC 11要求使用GCC 9或更高版本进行编译。因此，您需要安装GCC 9或更高版本。

编译openjdk 8，需要安装java7

sudo yum update
sudo yum groupinstall "Development Tools"
sudo yum install glibc-devel zlib-devel -y
wget https://mirror.linux-ia64.org/gnu/gcc/releases/gcc-11.4.0/gcc-11.4.0.tar.gz -O gcc-11.4.0.tar.gz 
--no-check-certificate
或者
wget https://ftp.gnu.org/gnu/gcc/gcc-11.4.0/gcc-11.4.0.tar.gz -O gcc-11.4.0.tar.gz --no-check-certificate
tar xzvf gcc-11.4.0.tar.gz


cd gcc-11.4.0

# 下载依赖
./contrib/download_prerequisites

# 配置。可以通过 prefix 参数设置编译完成的 GCC 的安装目录，如果不指定，会安装在 /usr/local下
# 可以配置为当前用户的某个目录
./configure --prefix=/home/wdidada/gcc11 --enable-threads=posix --disable-checking \
    --enable--long-long --with-system-zlib --enable-languages=c,c++ --enable-multilib

# 开始编译
make -j4

# 安装
# 编译产生物会安装到 configure --prefix 指定的目录中，或系统默认目录下
make install

# 修改环境变量
# 可以将下面的配置写到 .bashrc 或 .bash_profile 中，这样每次登录都会自动生效
export PATH=/home/wdidada/gcc11/bin:$PATH
export LD_LIBRARY_PATH=/home/wdidada/gcc11/lib64:$LD_LIBRARY_PATH
export CC=/home/wdidada/gcc11/bin/gcc
export CXX=/home/wdidada/gcc11/bin/g++


gnu compiler collection
可以编译多种语言

## centos
No CMAKE_CXX_COMPILER could be found.

这个错误提示表示在CMake中找不到CMAKE_CXX_COMPILER。要解决这个问题，你需要确保已经安装了C++编译器，并将其添加到系统的环境变量中。

对于Windows系统，你可以安装Visual Studio或MinGW等编译器。对于Linux系统，你可以安装g++或clang++等编译器。

安装完成后，重新运行CMake并指定编译器路径。例如，如果你使用的是g++，可以在CMake命令中添加`-DCMAKE_CXX_COMPILER=/usr/bin/g++`参数。

在 CentOS 7.9 上安装 g++，可以通过以下步骤进行：

1. 首先，更新系统软件包列表：
```
sudo yum update
```

2. 接下来，安装 GCC（GNU Compiler Collection）：
```
sudo yum groupinstall "Development Tools"
```

3. 安装完成后，你可以使用 `g++ --version` 命令来检查 g++ 是否已经成功安装。如果看到版本信息，说明安装成功。
g++ (GCC) 4.8.5 20150623 (Red Hat 4.8.5-44

GCC编译器插件的一个例子是GCC的VCG插件，该插件可以图形化GCC编译过程的内部数据结构，例如控制流图、函数调用图、支配图、Tree结构、Gimple结构、RTX结构、Pass列表等，方便开发人员分析应用程序。
GCC编译器插件还有用于动态安全分析、安全加固的功能，通过修改中间数据的能力，可以不用修改源代码就能添加新功能。这对于安全测试非常有用，可以通过动态插装来实现监控程序执行路径，但需要注意动态插装可能会对程序的运行性能产生影响，降低程序运行效率。
以上信息仅供参考，如有需要，建议咨询专业技术人员。

### gcc vs g++

gcc编译c代码
g++编译c++代码

### gcc代码如何组织
git
cmake

cc1plus
xg++


Killed signal terminated program
云服务器内存不够，导致gcc编译失败
https://www.jianshu.com/p/a4ad05a51456


https://www.zhihu.com/question/20940822

gcc手动安装最新版
更新动态库
#查看当前的动态库
strings /usr/lib64/libstdc++.so.6 | grep CXXABI
rm -f /usr/lib64/libstdc++.so.6
ln -s /usr/local/lib64/libstdc++.so.6.0.29 /usr/lib64/libstdc++.so.6
#查看更新后的动态库
strings /usr/lib64/libstdc++.so.6 | grep CXXABI

## 安装后的动态库会位于/usr/local/lib64目录下，
#其他版本在该目录下寻找对应的动态库libstdc++.so.6.X.XX

https://blog.csdn.net/qq_41054313/article/details/119453611

configure: error: Building GCC requires GMP 4.2+, MPFR 2.4.0+ and MPC 0.8.0+.
需要依赖 mpc，mpfr，gmp包，
GCC 源码里自带脚本可以轻松下载依赖包。
./contrib/download_prerequisites

以上软件各版本源码在https://ftp.gnu.org/gnu/链接中可下载

https://muzing.top/posts/16a16b69/

Redis里面有ruby脚本

gcc各版本历史
http://ftp.gnu.org/gnu/gcc/

libstdc++.so.6 'GLIBCXX 3.4.21'not found的问题
https://www.cnblogs.com/stelliformzm/p/12805826.html



http://ftp.tsukuba.wide.ad.jp/software/gcc/releases/　
tar -xvf gcc-5.4.0.tar.bz2
cd gcc-5.4.0
./contrib/download_prerequisits
mkdir build
cd build
../configure --enable-checking=release --enable-languages=c,c++ --disable-multlib
../configure --enable-checking=release --enable-languages=c,c++ --disable-multlib
../configure --enable-checking=release --enable-languages=c,c++ --disable-multlib
configure: error: I suspect your system does not have 32-bit development libraries (libc and headers). If you have them, rerun configure with --enable-multilib. If you do not have them, and want to build a 64-bit-only compiler, rerun configure with --disable-multilib.




安装autoconf和automake
yum -y install gcc automake autoconf libtool make

安装g++:
yum install gcc gcc-c++

yum install glibc-static libstdc++-static -y

sudo apt update
sudo apt install g++ -y


2020年5月7日发布 GCC 10.1.1
clang 12

```shell
yum install gcc-c++
Dependencies Resolved

=========================================================
 Package     Arch       Version           Repository
                                                    Size
=========================================================
Installing:
 gcc-c++     x86_64     4.8.5-44.el7      base     7.2 M
Installing for dependencies:
 cpp         x86_64     4.8.5-44.el7      base     5.9 M
 gcc         x86_64     4.8.5-44.el7      base      16 M

Transaction Summary
=========================================================
Install  1 Package (+2 Dependent packages)

Total download size: 29 M
Installed size: 69 M
Is this ok [y/d/N]:
```


UNIX系统的内核主要由C语言编写
在AIX下进行C编程，最通用的编辑器为vi/vim
选择编译器：常用的是GNU C/C++编译器 GCC (开源的跨平台编译器套件)；XLC(AIX的商业版本编译器)
选择调试器：应用最广泛的调试器是gdb (UNIX下用dbx）
程序维护工具：make是Linux/Unix下常用的程序维护工具
AIX需要首先安装Linux RPM格式支持，才能安装gccRPM for AIX软件包

xlc++ 和 g++
AIX上使用的是xlc++编译器，Linux上使用的是g++编译器。

对C标准中没有严格定义的行为，两个编译器的处理方式不一定相同，代码在两个平台运行会有不一样的表现。导致在一个平台运行正常，另一个平台可能就是bug了。
https://www.bilibili.com/read/cv7849739/



https://blog.csdn.net/tglg/article/details/4041019


https://cbs.centos.org/koji/buildinfo?buildID=31753

sudo yum install centos-release-scl
sudo yum install devtoolset-8

devtoolset-9

```shell
rpm -qa | grep gcc
devtoolset-7-gcc-7.3.1-5.16.el7.x86_64
libgcc-4.8.5-44.el7.i686
gcc-4.8.5-44.el7.x86_64
devtoolset-8-gcc-8.3.1-3.2.el7.x86_64
devtoolset-9-gcc-c++-9.1.1-2.6.el7.x86_64
gcc-gfortran-4.8.5-44.el7.x86_64
devtoolset-9-gcc-gfortran-9.1.1-2.6.el7.x86_64
devtoolset-8-gcc-c++-8.3.1-3.2.el7.x86_64
gcc-c++-4.8.5-44.el7.x86_64
devtoolset-9-gcc-9.1.1-2.6.el7.x86_64
libgcc-4.8.5-44.el7.x86_64
devtoolset-7-gcc-c++-7.3.1-5.16.el7.x86_64
```

[install gcc 8 on centos](https://stackoverflow.com/questions/55345373/how-to-install-gcc-g-8-on-centos)

```c
yum install devtoolset-8-gcc devtoolset-8-gcc-c++
```



腾讯个人云主机

gcc 4.8 8.3 9.1



公司会自建centos repo镜像



--disable-multilib

gcc编译参数

addtion on:gcc-multilib 

如何查看gcc是否支持

multilib是同时生成多个平台的代码，比如：64bit机器，同时可以产生32和64两种格式，不是研究这个的，仅供参考。

是gcc的一个选项



scl enable devtoolset-8 -- bash
source /opt/rh/devtoolset-8/enable





scl enable devtoolset-9 -- bash
source /opt/rh/devtoolset-9/enable



切换bash gcc版本

https://cloud.tencent.com/developer/article/1430839



 默认情况下，GCC/G++链接时优先链接动态库，如果没有动态库，则链接相应的静态库。同时，GCC/G++也提供了链接选项 -Wl,-Bstatic 和 -Wl,-Bdynamic 供用户指定链接动态库或者静态库。

  -Wl,-Bstatic指示跟在后面的-lxxx选项链接的都是静态库，-Wl,-Bdynamic指示跟在后面的-lxxx选项链接的都是动态库。



被依赖的在后面，依赖其他的在前面



[GCC/G++选项 -Wl,-Bstatic和-Wl,-Bdynamic](https://blog.csdn.net/weixin_34257076/article/details/91871190)



https://www.jianshu.com/p/fdd516337c76



c++ 静态库 动态库 未定义的引用



https://www.runoob.com/w3cnote/cpp-static-library-and-dynamic-library.html



http://asrman.blogspot.com/2018/11/cc-so.html





https://gcc.gnu.org/

## centos 7编译安装
编译安装gcc
```shell
sudo yum update
sudo yum groupinstall "Development Tools"
sudo yum install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel
wget https://ftp.gnu.org/gnu/gcc/gcc-11.2.0/gcc-11.2.0.tar.gz
ls -la gcc-11.2.0.tar.gz
tar -zxvf gcc-11.2.0.tar.gz
cd gcc-11.2.0
./contrib/download_prerequisites
./configure --enable-languages=c,c++ --disable-multilib --with-system-zlib --with-system-bzlib --with-system-readline --with-system-sqlite --with-system-ncurses --with-system-libffi --with-plugindir=/usr/lib64/gcc/plugin --with-pkgversion="CentOS 7.9" --with-bugurl="https://bugs.centos.org/taskman" --enable-shared --enable-static --enable-threads=posix --enable-checking=release --enable-optimizations --enable-lto-plugin --enable-libstdcxx-pch --enable-default-pie --enable-default-ssp --enable-libssp --enable-libgomp --enable-libquadmath --enable-libmpx --enable-libunwind --enable-libsanitizer=address,undefined CC=gcc CXX=g++
make all-gcc all-target-libgcc
sudo make install-gcc install-target-libgcc
```


以上 gcc、g++、cpp 都叫做 compiler driver 。这些都不负责编译代码，只负责调用真正的编译器（compiler proper）。gcc 这个项目中，真正负责编译 C 代码的程序叫做 cc1，负责编译 C++ 代码的程序叫做 cc1plus 。
