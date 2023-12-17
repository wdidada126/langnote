# build

cpp stl成为规范，cpp已经大面积应用了
stl容器类不是线程安全的

srpc
brpc .a 静态库

cpp依赖

开源库

git submodule
https://www.jianshu.com/p/e27a978ddb88

默认下载最新版代码

pistache

qt ui库

apt libxxx-dev 
yum xxx-devel  后缀的库



Install required packages:
  # Debian, Ubuntu, etc.
  $ sudo apt install g++ cmake make libboost-dev
  # CentOS
  $ sudo yum install gcc-c++ cmake make boost-devel


- vcpkg
- brew apt yum pkg
- conan
- xmake
- bazel
- meson
- msbuild

vs
xcode 新建项目

搜狗srpc
workflow


Supported package repositories

Official package repository xmake-repo (tbox >1.6.1)
Official package manager Xrepo
User-built repositories
Conan (conan::openssl/1.1.1g)
Conda (conda::libpng 1.3.67)
Vcpkg (vcpkg:ffmpeg)
Homebrew/Linuxbrew (brew::pcre2/libpcre2-8)
Pacman on archlinux/msys2 (pacman::libcurl)
Apt on ubuntu/debian (apt::zlib1g-dev)
Clib (clib::clibs/bytes@0.0.4)
Dub (dub::log 0.4.3)
Portage on Gentoo/Linux (portage::libhandy)
Nimble for nimlang (nimble::zip >1.3)


vcpkg 安装库的版本
不支持
https://www.zhihu.com/question/365431741

apt yum brew


命令用法如下：

apt-get install package=version
例如我要安装autoconf 2.50：

apt-get install autoconf=2.50
列出一个软件的版本的命令是  

apt-cache madison soft_name

https://blog.csdn.net/whatday/article/details/107064642



yum search  bind-chroot
yum info bind-chroot



[root@10-23-29-39 ~]# yum search  bind-chroot
Loaded plugins: fastestmirror, langpacks, product-id, search-disabled-
              : repos, subscription-manager, versionlock

This system is not registered with an entitlement server. You can use subscription-manager to register.

Loading mirror speeds from cached hostfile
 * centos-sclo-rh: mirrors.nju.edu.cn
 * centos-sclo-sclo: mirrors.nju.edu.cn
 * nux-dextop: li.nux.ro
 * remi-safe: ftp.riken.jp
Excluding 1 update due to versionlock (use "yum versionlock status" to show it)
======================= N/S matched: bind-chroot =======================
bind-chroot.x86_64 : A chroot runtime environment for the ISC BIND DNS
                   : server, named(8)

  Name and summary matches only, use "search all" for everything.
[root@10-23-29-39 ~]# yum info bind-chroot
Loaded plugins: fastestmirror, langpacks, product-id, search-disabled-
              : repos, subscription-manager, versionlock

This system is not registered with an entitlement server. You can use subscription-manager to register.

Loading mirror speeds from cached hostfile
 * centos-sclo-rh: mirrors.nju.edu.cn
 * centos-sclo-sclo: mirrors.nju.edu.cn
 * nux-dextop: li.nux.ro
 * remi-safe: ftp.riken.jp
Excluding 1 update due to versionlock (use "yum versionlock status" to show it)
Installed Packages
Name        : bind-chroot
Arch        : x86_64
Epoch       : 32
Version     : 9.11.4
Release     : 26.P2.el7_9.4
Size        : 4.7 k
Repo        : installed
From repo   : updates
Summary     : A chroot runtime environment for the ISC BIND DNS server,
            : named(8)
URL         : http://www.isc.org/products/BIND/
License     : MPLv2.0
Description : This package contains a tree of files which can be used as
            : a chroot(2) jail for the named(8) program from the BIND
            : package. Based on the code from Jan "Yenya" Kasprzak
            : <kas@fi.muni.cz>

Available Packages
Name        : bind-chroot
Arch        : x86_64
Epoch       : 32
Version     : 9.11.4
Release     : 26.P2.el7_9.9
Size        : 93 k
Repo        : updates/7/x86_64
Summary     : A chroot runtime environment for the ISC BIND DNS server,
            : named(8)
URL         : http://www.isc.org/products/BIND/
License     : MPLv2.0
Description : This package contains a tree of files which can be used as
            : a chroot(2) jail for the named(8) program from the BIND
            : package. Based on the code from Jan "Yenya" Kasprzak
            : <kas@fi.muni.cz>






