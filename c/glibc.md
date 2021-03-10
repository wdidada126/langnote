# glibc

glibc.sh

代码学习意义不大


## 下载glibc源码

```shell

git clone ***

```

## ubuntu 16.04 tls 编译glibc

[configure: error: you must configure in a separate build directory](https://blog.csdn.net/dbkmeteor/article/details/6764650)


```shell

*** These critical programs are missing or too old: make compiler
*** Check the INSTALL file for required versions.

```

INSTALL文件是安装说明文档

make 不低于4.0

linux上c的标准库 封装了系统调用
Rust go标准库有时也依赖

android bionic

musl


openwrt LEDE默认使用Musl-libc
uClibc 一个小型的C语言标准库，主要用于嵌入式。

glibc，uClibc，eglibc都是C语言函数库： 1. uClibc是嵌入式系统中用的，glibc是桌面系统用的 2. eglibc也是嵌入式系统中用的，是glibc的嵌入式版本，和glibc在源码和二进制上兼容。

