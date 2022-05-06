# gcc

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
# 安装后的动态库会位于/usr/local/lib64目录下，
#其他版本在该目录下寻找对应的动态库libstdc++.so.6.X.XX

https://blog.csdn.net/qq_41054313/article/details/119453611

configure: error: Building GCC requires GMP 4.2+, MPFR 2.4.0+ and MPC 0.8.0+.
需要依赖 mpc，mpfr，gmp包，
GCC 源码里自带脚本可以轻松下载依赖包。
./contrib/download_prerequisites



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

