# jemalloc

内存池
可以去看ptmalloc的源码，或者去网上找ptmalloc的详解。引申tcmalloc、jemalloc


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



centos 7

yum install jemalloc-devel -y

版本是3.6.0-1.el7

源码安装 jemalloc-4.5.0





https://people.freebsd.org/~jasone/jemalloc/bsdcan2006/jemalloc.pdf



内存分配器 jemalloc 是通用的 malloc(3) 实现，它强调避免碎片和可扩展的并发支持。

jemalloc 起源于 Jason Evans 2006 年在 BSDcan conference 发表的论文：[A Scalable Concurrent malloc Implementation for FreeBSD](http://people.freebsd.org/~jasone/jemalloc/bsdcan2006/jemalloc.pdf)。Jason 认为 phkmalloc（FreeBSD’s previous malloc implementation by Kamp (1998)）没有考虑多处理器的情况，因此在多线程并发下性能低下(事实如此)，而 jemalloc 适合多线程下内存分配管理。

jemalloc 是 Facebook 推出的一种通用 malloc 实现，在 FreeBSD、firefox 中被广泛使用。比起 ptmalloc2 具有更高的性能。



http://www.freeoa.net/product/devtool/mem-allocation-jemalloc_3124.html

```shell

```





autotool
`sudo yum install aotutool -y`

chmod a+x  autogen.sh
./autogen.sh
./configure
make
cause error

gcc version 4.8.5



gcc 7之后，编译通过

~~~shell
```shell
[root@VM_0_17_centos jemalloc-4.5.0]# make install
/usr/bin/install -c -d /usr/local/bin
/usr/bin/install -c -m 755 bin/jemalloc-config /usr/local/bin
/usr/bin/install -c -m 755 bin/jemalloc.sh /usr/local/bin
/usr/bin/install -c -m 755 bin/jeprof /usr/local/bin
/usr/bin/install -c -d /usr/local/include/jemalloc
/usr/bin/install -c -m 644 include/jemalloc/jemalloc.h /usr/local/include/jemalloc
/usr/bin/install -c -d /usr/local/lib
/usr/bin/install -c -m 755 lib/libjemalloc.so.2 /usr/local/lib
ln -sf libjemalloc.so.2 /usr/local/lib/libjemalloc.so
/usr/bin/install -c -d /usr/local/lib
/usr/bin/install -c -m 755 lib/libjemalloc.a /usr/local/lib
/usr/bin/install -c -m 755 lib/libjemalloc_pic.a /usr/local/lib
/usr/bin/install -c -d /usr/local/lib/pkgconfig
/usr/bin/install -c -m 644 jemalloc.pc /usr/local/lib/pkgconfig
/usr/bin/install -c -d /usr/local/share/doc/jemalloc
/usr/bin/install -c -m 644 doc/jemalloc.html /usr/local/share/doc/jemalloc
/usr/bin/install -c -d /usr/local/share/man/man3
/usr/bin/install -c -m 644 doc/jemalloc.3 /usr/local/share/man/man3
[root@VM_0_17_centos jemalloc-4.5.0]# ldconfig
[root@VM_0_17_centos jemalloc-4.5.0]# pwd
/root/jemalloc-4.5.0
```
~~~