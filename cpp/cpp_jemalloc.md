# jemalloc


https://github.com/jemalloc/jemalloc
最新版
5.2.1 20210305



http://jemalloc.net/

centos 7

jemalloc-devel.x86_64 0:3.6.0-1.el7

https://centos.pkgs.org/7/epel-x86_64/jemalloc-devel-3.6.0-1.el7.x86_64.rpm.html

```shell
repoquery -ql jemalloc-devel
/usr/include/jemalloc
/usr/include/jemalloc/jemalloc.h
/usr/lib64/libjemalloc.so
/usr/share/man/man3/jemalloc.3.gz
```

https://www.jianshu.com/p/41852483e4a1



腾讯云 gcc 4.8



从githua下载releases网址下的包，可以，不要从github上下载源码

jemalloc
内存分配的网络库

https://github.com/jemalloc/jemalloc
redis使用了

Jemalloc是内存管理库。很多开源项目不使用glibc自带的ptmalloc，而是使用Jemalloc或者Tcmalloc这类更高效的内存管理库。
分析ptmalloc、tcmalloc和jemalloc这三种内存管理库

源码安装

autotool
`sudo yum install aotutool -y`

chmod a+x  autogen.sh
./autogen.sh
./configure
make
cause error

gcc version 4.8.5