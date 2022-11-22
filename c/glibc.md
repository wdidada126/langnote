# glibc

glibc最主要的功能就是对系统调用的封装


libc,glib,glibc,eglibc,libc++,libstdc++,gcc,g++。
从libc说起。
libc是Linux下原来的标准C库，也就是当初写hello world时包含的头文件#include < stdio.h> 定义的地方。
后来逐渐被glibc取代，也就是传说中的GNU C Library,在此之前除了有libc，还有klibc,uclibc。现在只要知道用的最多的是glibc就行了，主流的一些linux操作系统如 Debian, Ubuntu，Redhat等用的都是glibc（或者其变种，下面会说到).
那glibc都做了些什么呢？ glibc是Linux系统中最底层的API，几乎其它任何的运行库都要依赖glibc。 glibc最主要的功能就是对系统调用的封装，你想想看，你怎么能在C代码中直接用fopen函数就能打开文件？ 打开文件最终还是要触发系统中的sys_open系统调用，而这中间的处理过程都是glibc来完成的。这篇文章详细介绍了glibc是如何与上层应用程序和系统调用交互的。除了封装系统调用，glibc自身也提供了一些上层应用函数必要的功能,如string,malloc,stdlib,linuxthreads,locale,signal等等。
好了，那eglibc又是什么？ 这里的e是Embedded的意思，也就是前面说到的变种glibc。eglibc的主要特性是为了更好的支持嵌入式架构，可以支持不同的shell(包括嵌入式)，但它是二进制兼容glibc的，就是说如果你的代码之前依赖eglibc库，那么换成glibc后也不需要重新编译。ubuntu系统用的就是eglibc（而不是glibc）,不信，你执行 ldd –version 或者 /lib/i386-linux-gnu/libc.so.6
(64位系统运行/lib/x86_64-linux-gnu）看看，便会显示你系统中eglibc/glibc的版本信息。 这里提到了libc.so.6,这个文件就是eglibc/glibc编译后的生成库文件。
还有一个glib看起来也很相似，那它又是什么呢？glib也是个c程序库，不过比较轻量级，glib将C语言中的数据类型统一封装成自己的数据类型，提供了C语言常用的数据结构的定义以及处理函数，有趣的宏以及可移植的封装等(注：glib是可移植的，说明你可以在linux下，也可以在windows下使用它）。那它跟glibc有什么关系吗？其实并没有，除非你的程序代码会用到glib库中的数据结构或者函数，glib库在ubuntu系统中并不会默认安装(可以通过apt-get install libglib2.0-dev手动安装)，著名的GTK+和Gnome底层用的都是glib库。想更详细了解glib？ 可以参考这里
看到这里，你应该知道这些库有多重要了吧？ 你写的C代码在编译的过程中有可能出现明明是这些库里面定义的变,却量还会出现’Undefined’, ‘Unreference’等错误，这时候你可能会怀疑是不是这些库出问题了？ 是不是该动手换个gilbc/eglibc了？ 这里强调一点，在你准备更换/升级这些库之前，你应该好好思考一下，你真的要更换/升级吗？你要知道你自己在做什么！你要时刻知道glibc/eglibc的影响有多大，不管你之前部署的什么程序，linux系统的ls,cd,mv,ps等等全都得依赖它，很多人在更换/升级都有过惨痛的教训，甚至让整个系统奔溃无法启动。所以，强烈不建议更换/升级这些库！
当然如果你写的是C++代码，还有两个库也要非常重视了，libc++/libstdc++,这两个库有关系吗？有。两个都是C++标准库。libc++是针对clang编译器特别重写的C++标准库，那libstdc++自然就是gcc的事儿了。libstdc++与gcc的关系就像clang与libc++. 其中的区别这里不作详细介绍了。
再说说libstdc++，glibc的关系。 libstdc++与gcc是捆绑在一起的，也就是说安装gcc的时候会把libstdc++装上。 那为什么glibc和gcc没有捆绑在一起呢？
相比glibc，libstdc++虽然提供了c++程序的标准库，但它并不与内核打交道。对于系统级别的事件，libstdc++首先是会与glibc交互，才能和内核通信。相比glibc来说，libstdc++就显得没那么基础了。
说完了这些库，这些库最终都是拿来干嘛的？当然是要将它们与你的程序链接在一起！ 这时候就不得不说说gcc了(当然还有前文提到的clang以及llvm等编译器，本文就不细说它们的区别了)。
你写的C代码.c文件通过gcc首先转化为汇编.S文件，之后汇编器as将.S文件转化为机器代码.o文件，生成的.o文件再与其它.o文件，或者之前提到的libc.so.6库文件通过ld链接器链接在一块生成可执行文件。当然，在你编译代码使用gcc的时候，gcc命令已经帮你把这些细节全部做好了。
那g++是做什么的? 慢慢说来，不要以为gcc只能编译C代码，g++只能编译c++代码。 后缀为.c的，gcc把它当作是C程序，而g++当作是c++程序；后缀为.cpp的，两者都会认为是c++程序，注意，虽然c++是c的超集，但是两者对语法的要求是有区别的。在编译阶段，g++会调用gcc,对于c++代码，两者是等价的，但是因为gcc命令不能自动和C++程序使用的库联接，需要这样，gcc -lstdc++, 所以如果你的Makefile文件并没有手动加上libstdc++库，一般就会提示错误，要求你安装g++编译器了。
好了，就说到这，理清这些库与编译器之间的关系，相信会对你解决编译链接过程中遇到的错误起到一点帮助。
如果你的编译器不支持一些新的C/C++特性，想升级gcc/g++, 这里也给出一个基于ubuntu系统的参考方法。
添加ppa
sudo add-apt-repository ppa:ubuntu-toolchain-r/test
sudo apt-get update
添加ppa，是因为你所用的ubuntu版本的更新源中可能并没有你想要的gcc/g++版本。
安装新版gcc/g++
sudo apt-get install gcc-4.8
sudo apt-get install g++-4.8
可以到/usr/bin/gcc查看新安装的gcc,g++
配置系统gcc/g++
使用update-alternatives,统一更新gcc/g++
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-4.6 60 --slave /usr/bin/g++ g++ /usr/bin/g++-4.6
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-4.8 80 --slave /usr/bin/g++ g++ /usr/bin/g++-4.8
sudo update-alternatives --config gcc
数字优先级(如60，80)高的会被系统选择为默认的编译器,也可以执行第三条命令就是来手动配置系统的gcc,此处按照提示,选择4.8版本的即可。
————————————————
版权声明：本文为CSDN博主「爬虫仔蛙」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/p656456564545/article/details/89184141


strings /usr/lib64/libstdc++.so.6 | grep GLIBC

```
rpm -ql glibc
/etc/gai.conf
/etc/ld.so.cache
/etc/ld.so.conf
/etc/ld.so.conf.d
/etc/nsswitch.conf
/etc/rpc
/lib64/ld-2.17.so
/lib64/ld-linux-x86-64.so.2
/lib64/libBrokenLocale-2.17.so
/lib64/libBrokenLocale.so.1
/lib64/libSegFault.so
/lib64/libanl-2.17.so
/lib64/libanl.so.1
/lib64/libc-2.17.so
/lib64/libc.so.6
/lib64/libcidn-2.17.so
/lib64/libcidn.so.1
/lib64/libcrypt-2.17.so
/lib64/libcrypt.so.1
/lib64/libdl-2.17.so
/lib64/libdl.so.2
/lib64/libm-2.17.so
/lib64/libm.so.6
/lib64/libnsl-2.17.so
/lib64/libnsl.so.1
/lib64/libnss_compat-2.17.so
/lib64/libnss_compat.so.2
/lib64/libnss_db-2.17.so
/lib64/libnss_db.so.2
/lib64/libnss_dns-2.17.so
/lib64/libnss_dns.so.2
/lib64/libnss_files-2.17.so
/lib64/libnss_files.so.2
/lib64/libnss_hesiod-2.17.so
/lib64/libnss_hesiod.so.2
/lib64/libnss_nis-2.17.so
/lib64/libnss_nis.so.2
/lib64/libnss_nisplus-2.17.so
/lib64/libnss_nisplus.so.2
/lib64/libpthread-2.17.so
/lib64/libpthread.so.0
/lib64/libresolv-2.17.so
/lib64/libresolv.so.2
/lib64/librt-2.17.so
/lib64/librt.so.1
/lib64/libthread_db-1.0.so
/lib64/libthread_db.so.1
/lib64/libutil-2.17.so
/lib64/libutil.so.1
/lib64/rtkaio
/lib64/rtkaio/librt.so.1
/lib64/rtkaio/librtkaio-2.17.so
/sbin/ldconfig
/sbin/sln
/usr/lib64/audit
/usr/lib64/audit/sotruss-lib.so
/usr/lib64/gconv
/usr/lib64/gconv/ANSI_X3.110.so
/usr/lib64/gconv/ARMSCII-8.so
/usr/lib64/gconv/ASMO_449.so
/usr/lib64/gconv/BIG5.so
/usr/lib64/gconv/BIG5HKSCS.so
/usr/lib64/gconv/BRF.so
/usr/lib64/gconv/CP10007.so
/usr/lib64/gconv/CP1125.so
/usr/lib64/gconv/CP1250.so
/usr/lib64/gconv/CP1251.so
/usr/lib64/gconv/CP1252.so
/usr/lib64/gconv/CP1253.so
/usr/lib64/gconv/CP1254.so
/usr/lib64/gconv/CP1255.so
/usr/lib64/gconv/CP1256.so
/usr/lib64/gconv/CP1257.so
/usr/lib64/gconv/CP1258.so
/usr/lib64/gconv/CP737.so
/usr/lib64/gconv/CP770.so
/usr/lib64/gconv/CP771.so
/usr/lib64/gconv/CP772.so
/usr/lib64/gconv/CP773.so
/usr/lib64/gconv/CP774.so
/usr/lib64/gconv/CP775.so
/usr/lib64/gconv/CP932.so
/usr/lib64/gconv/CSN_369103.so
/usr/lib64/gconv/CWI.so
/usr/lib64/gconv/DEC-MCS.so
/usr/lib64/gconv/EBCDIC-AT-DE-A.so
/usr/lib64/gconv/EBCDIC-AT-DE.so
/usr/lib64/gconv/EBCDIC-CA-FR.so
/usr/lib64/gconv/EBCDIC-DK-NO-A.so
/usr/lib64/gconv/EBCDIC-DK-NO.so
/usr/lib64/gconv/EBCDIC-ES-A.so
/usr/lib64/gconv/EBCDIC-ES-S.so
/usr/lib64/gconv/EBCDIC-ES.so
/usr/lib64/gconv/EBCDIC-FI-SE-A.so
/usr/lib64/gconv/EBCDIC-FI-SE.so
/usr/lib64/gconv/EBCDIC-FR.so
/usr/lib64/gconv/EBCDIC-IS-FRISS.so
/usr/lib64/gconv/EBCDIC-IT.so
/usr/lib64/gconv/EBCDIC-PT.so
/usr/lib64/gconv/EBCDIC-UK.so
/usr/lib64/gconv/EBCDIC-US.so
/usr/lib64/gconv/ECMA-CYRILLIC.so
/usr/lib64/gconv/EUC-CN.so
/usr/lib64/gconv/EUC-JISX0213.so
/usr/lib64/gconv/EUC-JP-MS.so
/usr/lib64/gconv/EUC-JP.so
/usr/lib64/gconv/EUC-KR.so
/usr/lib64/gconv/EUC-TW.so
/usr/lib64/gconv/GB18030.so
/usr/lib64/gconv/GBBIG5.so
/usr/lib64/gconv/GBGBK.so
/usr/lib64/gconv/GBK.so
/usr/lib64/gconv/GEORGIAN-ACADEMY.so
/usr/lib64/gconv/GEORGIAN-PS.so
/usr/lib64/gconv/GOST_19768-74.so
/usr/lib64/gconv/GREEK-CCITT.so
/usr/lib64/gconv/GREEK7-OLD.so
/usr/lib64/gconv/GREEK7.so
/usr/lib64/gconv/HP-GREEK8.so
/usr/lib64/gconv/HP-ROMAN8.so
/usr/lib64/gconv/HP-ROMAN9.so
/usr/lib64/gconv/HP-THAI8.so
/usr/lib64/gconv/HP-TURKISH8.so
/usr/lib64/gconv/IBM037.so
/usr/lib64/gconv/IBM038.so
/usr/lib64/gconv/IBM1004.so
/usr/lib64/gconv/IBM1008.so
/usr/lib64/gconv/IBM1008_420.so
/usr/lib64/gconv/IBM1025.so
/usr/lib64/gconv/IBM1026.so
/usr/lib64/gconv/IBM1046.so
/usr/lib64/gconv/IBM1047.so
/usr/lib64/gconv/IBM1097.so
/usr/lib64/gconv/IBM1112.so
/usr/lib64/gconv/IBM1122.so
/usr/lib64/gconv/IBM1123.so
/usr/lib64/gconv/IBM1124.so
/usr/lib64/gconv/IBM1129.so
/usr/lib64/gconv/IBM1130.so
/usr/lib64/gconv/IBM1132.so
/usr/lib64/gconv/IBM1133.so
/usr/lib64/gconv/IBM1137.so
/usr/lib64/gconv/IBM1140.so
/usr/lib64/gconv/IBM1141.so
/usr/lib64/gconv/IBM1142.so
/usr/lib64/gconv/IBM1143.so
/usr/lib64/gconv/IBM1144.so
/usr/lib64/gconv/IBM1145.so
/usr/lib64/gconv/IBM1146.so
/usr/lib64/gconv/IBM1147.so
/usr/lib64/gconv/IBM1148.so
/usr/lib64/gconv/IBM1149.so
/usr/lib64/gconv/IBM1153.so
/usr/lib64/gconv/IBM1154.so
/usr/lib64/gconv/IBM1155.so
/usr/lib64/gconv/IBM1156.so
/usr/lib64/gconv/IBM1157.so
/usr/lib64/gconv/IBM1158.so
/usr/lib64/gconv/IBM1160.so
/usr/lib64/gconv/IBM1161.so
/usr/lib64/gconv/IBM1162.so
/usr/lib64/gconv/IBM1163.so
/usr/lib64/gconv/IBM1164.so
/usr/lib64/gconv/IBM1166.so
/usr/lib64/gconv/IBM1167.so
/usr/lib64/gconv/IBM12712.so
/usr/lib64/gconv/IBM1364.so
/usr/lib64/gconv/IBM1371.so
/usr/lib64/gconv/IBM1388.so
/usr/lib64/gconv/IBM1390.so
/usr/lib64/gconv/IBM1399.so
/usr/lib64/gconv/IBM16804.so
/usr/lib64/gconv/IBM256.so
/usr/lib64/gconv/IBM273.so
/usr/lib64/gconv/IBM274.so
/usr/lib64/gconv/IBM275.so
/usr/lib64/gconv/IBM277.so
/usr/lib64/gconv/IBM278.so
/usr/lib64/gconv/IBM280.so
/usr/lib64/gconv/IBM281.so
/usr/lib64/gconv/IBM284.so
/usr/lib64/gconv/IBM285.so
/usr/lib64/gconv/IBM290.so
/usr/lib64/gconv/IBM297.so
/usr/lib64/gconv/IBM420.so
/usr/lib64/gconv/IBM423.so
/usr/lib64/gconv/IBM424.so
/usr/lib64/gconv/IBM437.so
/usr/lib64/gconv/IBM4517.so
/usr/lib64/gconv/IBM4899.so
/usr/lib64/gconv/IBM4909.so
/usr/lib64/gconv/IBM4971.so
/usr/lib64/gconv/IBM500.so
/usr/lib64/gconv/IBM5347.so
/usr/lib64/gconv/IBM803.so
/usr/lib64/gconv/IBM850.so
/usr/lib64/gconv/IBM851.so
/usr/lib64/gconv/IBM852.so
/usr/lib64/gconv/IBM855.so
/usr/lib64/gconv/IBM856.so
/usr/lib64/gconv/IBM857.so
/usr/lib64/gconv/IBM858.so
/usr/lib64/gconv/IBM860.so
/usr/lib64/gconv/IBM861.so
/usr/lib64/gconv/IBM862.so
/usr/lib64/gconv/IBM863.so
/usr/lib64/gconv/IBM864.so
/usr/lib64/gconv/IBM865.so
/usr/lib64/gconv/IBM866.so
/usr/lib64/gconv/IBM866NAV.so
/usr/lib64/gconv/IBM868.so
/usr/lib64/gconv/IBM869.so
/usr/lib64/gconv/IBM870.so
/usr/lib64/gconv/IBM871.so
/usr/lib64/gconv/IBM874.so
/usr/lib64/gconv/IBM875.so
/usr/lib64/gconv/IBM880.so
/usr/lib64/gconv/IBM891.so
/usr/lib64/gconv/IBM901.so
/usr/lib64/gconv/IBM902.so
/usr/lib64/gconv/IBM903.so
/usr/lib64/gconv/IBM9030.so
/usr/lib64/gconv/IBM904.so
/usr/lib64/gconv/IBM905.so
/usr/lib64/gconv/IBM9066.so
/usr/lib64/gconv/IBM918.so
/usr/lib64/gconv/IBM921.so
/usr/lib64/gconv/IBM922.so
/usr/lib64/gconv/IBM930.so
/usr/lib64/gconv/IBM932.so
/usr/lib64/gconv/IBM933.so
/usr/lib64/gconv/IBM935.so
/usr/lib64/gconv/IBM937.so
/usr/lib64/gconv/IBM939.so
/usr/lib64/gconv/IBM943.so
/usr/lib64/gconv/IBM9448.so
/usr/lib64/gconv/IEC_P27-1.so
/usr/lib64/gconv/INIS-8.so
/usr/lib64/gconv/INIS-CYRILLIC.so
/usr/lib64/gconv/INIS.so
/usr/lib64/gconv/ISIRI-3342.so
/usr/lib64/gconv/ISO-2022-CN-EXT.so
/usr/lib64/gconv/ISO-2022-CN.so
/usr/lib64/gconv/ISO-2022-JP-3.so
/usr/lib64/gconv/ISO-2022-JP.so
/usr/lib64/gconv/ISO-2022-KR.so
/usr/lib64/gconv/ISO-IR-197.so
/usr/lib64/gconv/ISO-IR-209.so
/usr/lib64/gconv/ISO646.so
/usr/lib64/gconv/ISO8859-1.so
/usr/lib64/gconv/ISO8859-10.so
/usr/lib64/gconv/ISO8859-11.so
/usr/lib64/gconv/ISO8859-13.so
/usr/lib64/gconv/ISO8859-14.so
/usr/lib64/gconv/ISO8859-15.so
/usr/lib64/gconv/ISO8859-16.so
/usr/lib64/gconv/ISO8859-2.so
/usr/lib64/gconv/ISO8859-3.so
/usr/lib64/gconv/ISO8859-4.so
/usr/lib64/gconv/ISO8859-5.so
/usr/lib64/gconv/ISO8859-6.so
/usr/lib64/gconv/ISO8859-7.so
/usr/lib64/gconv/ISO8859-8.so
/usr/lib64/gconv/ISO8859-9.so
/usr/lib64/gconv/ISO8859-9E.so
/usr/lib64/gconv/ISO_10367-BOX.so
/usr/lib64/gconv/ISO_11548-1.so
/usr/lib64/gconv/ISO_2033.so
/usr/lib64/gconv/ISO_5427-EXT.so
/usr/lib64/gconv/ISO_5427.so
/usr/lib64/gconv/ISO_5428.so
/usr/lib64/gconv/ISO_6937-2.so
/usr/lib64/gconv/ISO_6937.so
/usr/lib64/gconv/JOHAB.so
/usr/lib64/gconv/KOI-8.so
/usr/lib64/gconv/KOI8-R.so
/usr/lib64/gconv/KOI8-RU.so
/usr/lib64/gconv/KOI8-T.so
/usr/lib64/gconv/KOI8-U.so
/usr/lib64/gconv/LATIN-GREEK-1.so
/usr/lib64/gconv/LATIN-GREEK.so
/usr/lib64/gconv/MAC-CENTRALEUROPE.so
/usr/lib64/gconv/MAC-IS.so
/usr/lib64/gconv/MAC-SAMI.so
/usr/lib64/gconv/MAC-UK.so
/usr/lib64/gconv/MACINTOSH.so
/usr/lib64/gconv/MIK.so
/usr/lib64/gconv/NATS-DANO.so
/usr/lib64/gconv/NATS-SEFI.so
/usr/lib64/gconv/PT154.so
/usr/lib64/gconv/RK1048.so
/usr/lib64/gconv/SAMI-WS2.so
/usr/lib64/gconv/SHIFT_JISX0213.so
/usr/lib64/gconv/SJIS.so
/usr/lib64/gconv/T.61.so
/usr/lib64/gconv/TCVN5712-1.so
/usr/lib64/gconv/TIS-620.so
/usr/lib64/gconv/TSCII.so
/usr/lib64/gconv/UHC.so
/usr/lib64/gconv/UNICODE.so
/usr/lib64/gconv/UTF-16.so
/usr/lib64/gconv/UTF-32.so
/usr/lib64/gconv/UTF-7.so
/usr/lib64/gconv/VISCII.so
/usr/lib64/gconv/gconv-modules
/usr/lib64/gconv/gconv-modules.cache
/usr/lib64/gconv/libCNS.so
/usr/lib64/gconv/libGB.so
/usr/lib64/gconv/libISOIR165.so
/usr/lib64/gconv/libJIS.so
/usr/lib64/gconv/libJISX0213.so
/usr/lib64/gconv/libKSC.so
/usr/lib64/libmemusage.so
/usr/lib64/libpcprofile.so
/usr/libexec/getconf
/usr/libexec/getconf/POSIX_V6_LP64_OFF64
/usr/libexec/getconf/POSIX_V7_LP64_OFF64
/usr/libexec/getconf/XBS5_LP64_OFF64
/usr/sbin/glibc_post_upgrade.x86_64
/usr/sbin/iconvconfig
/usr/sbin/iconvconfig.x86_64
/usr/share/doc/glibc-2.17
/usr/share/doc/glibc-2.17/BUGS
/usr/share/doc/glibc-2.17/CONFORMANCE
/usr/share/doc/glibc-2.17/COPYING
/usr/share/doc/glibc-2.17/COPYING.LIB
/usr/share/doc/glibc-2.17/INSTALL
/usr/share/doc/glibc-2.17/LICENSES
/usr/share/doc/glibc-2.17/NEWS
/usr/share/doc/glibc-2.17/PROJECTS
/usr/share/doc/glibc-2.17/README
/usr/share/doc/glibc-2.17/README.hesiod
/usr/share/doc/glibc-2.17/rtld-debugger-interface.txt
/var/cache/ldconfig
/var/cache/ldconfig/aux-cache
/var/db/Makefile
```

glibc.sh

代码学习意义不大


## 下载glibc源码

```shell

git clone https://github.com/bminor/glibc.git

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

glibc，uClibc，eglibc都是C语言函数库： 1. uClibc是嵌入式系统中用的，glibc是桌面系统用的
2. eglibc也是嵌入式系统中用的，是glibc的嵌入式版本，和glibc在源码和二进制上兼容。

