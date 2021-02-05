# yum
rpm

1. 查询软件包依赖哪些软件
rpm -qR centos-release    安装  R参数的意思就是requires就是依赖哪些软件包
rpm -qpR centos-release 未安装
或
yum deplist centos-release

2. 查询软件包被哪个软件包依赖
rpm -q centos-release # 查看这个软件是否安装 rpcbind-0.2.0-44.el7.x86_64
rpm -e --test centos-release  # 通过--test进行测试删除,查看是否有依赖关系,如果有会阻止删除
错误：依赖检测失败： rpcbind 被 (已安裝) quota-1:4.01-17.el7.x86_64 需要


yum deplist  mysql-community-common-5.7.32-1.el7.x86_64

```shell
yum deplist gcc-4.8.5-44.el7.x86_64
Loaded plugins: fastestmirror, langpacks
Repository epel is listed more than once in the configuration
Loading mirror speeds from cached hostfile
 * centos-sclo-rh: mirrors.aliyun.com
 * centos-sclo-sclo: mirrors.aliyun.com
package: gcc.x86_64 4.8.5-44.el7
  dependency: /bin/sh
   provider: bash.x86_64 4.2.46-34.el7
  dependency: /sbin/install-info
   provider: info.x86_64 5.1-5.el7
  dependency: binutils >= 2.20.51.0.2-12
   provider: binutils.x86_64 2.27-44.base.el7
  dependency: cpp = 4.8.5-44.el7
   provider: cpp.x86_64 4.8.5-44.el7
  dependency: glibc-devel >= 2.2.90-12
   provider: glibc-devel.x86_64 2.17-322.el7_9
   provider: glibc-devel.i686 2.17-322.el7_9
  dependency: ld-linux-x86-64.so.2()(64bit)
   provider: glibc.x86_64 2.17-322.el7_9
  dependency: ld-linux-x86-64.so.2(GLIBC_2.3)(64bit)
   provider: glibc.x86_64 2.17-322.el7_9
  dependency: libc.so.6(GLIBC_2.14)(64bit)
   provider: glibc.x86_64 2.17-322.el7_9
  dependency: libdl.so.2()(64bit)
   provider: glibc.x86_64 2.17-322.el7_9
  dependency: libdl.so.2(GLIBC_2.2.5)(64bit)
   provider: glibc.x86_64 2.17-322.el7_9
  dependency: libgcc >= 4.8.5-44.el7
   provider: libgcc.x86_64 4.8.5-44.el7
   provider: libgcc.i686 4.8.5-44.el7
  dependency: libgcc_s.so.1()(64bit)
   provider: libgcc.x86_64 4.8.5-44.el7
  dependency: libgmp.so.10()(64bit)
   provider: gmp.x86_64 1:6.0.0-15.el7
  dependency: libgomp = 4.8.5-44.el7
   provider: libgomp.x86_64 4.8.5-44.el7
   provider: libgomp.i686 4.8.5-44.el7
  dependency: libgomp.so.1()(64bit)
   provider: libgomp.x86_64 4.8.5-44.el7
  dependency: libm.so.6()(64bit)
   provider: glibc.x86_64 2.17-322.el7_9
  dependency: libmpc.so.3()(64bit)
   provider: libmpc.x86_64 1.0.1-3.el7
  dependency: libmpfr.so.4()(64bit)
   provider: mpfr.x86_64 3.1.1-4.el7
  dependency: libz.so.1()(64bit)
   provider: zlib.x86_64 1.2.7-19.el7_9
  dependency: rtld(GNU_HASH)
   provider: glibc.x86_64 2.17-322.el7_9
   provider: glibc.i686 2.17-322.el7_9
```


rpm -qa
rpm -ql


```shell
[root@VM_0_17_centos branches]# rpm -qa | grep libodb
libodb-2.3.0-1.el7.x86_64
libodb-mysql-devel-2.3.0-1.el7.x86_64
libodb-mysql-2.3.0-1.el7.x86_64
[root@VM_0_17_centos branches]# yum deplist libodb-mysql-devel-2.3.0-1.el7.x86_64
Loaded plugins: fastestmirror, langpacks
Repository epel is listed more than once in the configuration
Loading mirror speeds from cached hostfile
 * centos-sclo-rh: mirrors.aliyun.com
 * centos-sclo-sclo: mirrors.aliyun.com
package: libodb-mysql-devel.x86_64 2.3.0-1.el7
  dependency: /usr/bin/pkg-config
   provider: pkgconfig.x86_64 1:0.27.1-4.el7
   provider: pkgconfig.i686 1:0.27.1-4.el7
  dependency: libodb-mysql(x86-64) = 2.3.0-1.el7
   provider: libodb-mysql.x86_64 2.3.0-1.el7
[root@VM_0_17_centos branches]# yum deplist libodb-mysql.x86_64 2.3.0-1.el7
Loaded plugins: fastestmirror, langpacks
Repository epel is listed more than once in the configuration
Loading mirror speeds from cached hostfile
 * centos-sclo-rh: mirrors.aliyun.com
 * centos-sclo-sclo: mirrors.aliyun.com
package: libodb-mysql.x86_64 2.3.0-1.el7
  dependency: /sbin/ldconfig
   provider: glibc.x86_64 2.17-322.el7_9
   provider: glibc.i686 2.17-322.el7_9
  dependency: libc.so.6(GLIBC_2.14)(64bit)
   provider: glibc.x86_64 2.17-322.el7_9
  dependency: libgcc_s.so.1()(64bit)
   provider: libgcc.x86_64 4.8.5-44.el7
  dependency: libgcc_s.so.1(GCC_3.0)(64bit)
   provider: libgcc.x86_64 4.8.5-44.el7
  dependency: libm.so.6()(64bit)
   provider: glibc.x86_64 2.17-322.el7_9
  dependency: libmysqlclient.so.18()(64bit)
   provider: mysql-community-libs-compat.x86_64 5.7.33-1.el7
   provider: mariadb-libs.x86_64 1:5.5.68-1.el7
  dependency: libmysqlclient.so.18(libmysqlclient_16)(64bit)
   provider: mysql-community-libs-compat.x86_64 5.7.33-1.el7
   provider: mariadb-libs.x86_64 1:5.5.68-1.el7
  dependency: libodb-2.3.so()(64bit)
   provider: libodb.x86_64 2.3.0-1.el7
  dependency: libpthread.so.0()(64bit)
   provider: glibc.x86_64 2.17-322.el7_9
  dependency: libpthread.so.0(GLIBC_2.2.5)(64bit)
   provider: glibc.x86_64 2.17-322.el7_9
  dependency: libpthread.so.0(GLIBC_2.3.2)(64bit)
   provider: glibc.x86_64 2.17-322.el7_9
  dependency: libstdc++.so.6()(64bit)
   provider: libstdc++.x86_64 4.8.5-44.el7
  dependency: libstdc++.so.6(CXXABI_1.3)(64bit)
   provider: libstdc++.x86_64 4.8.5-44.el7
  dependency: libstdc++.so.6(GLIBCXX_3.4)(64bit)
   provider: libstdc++.x86_64 4.8.5-44.el7
  dependency: libstdc++.so.6(GLIBCXX_3.4.11)(64bit)
   provider: libstdc++.x86_64 4.8.5-44.el7
  dependency: libstdc++.so.6(GLIBCXX_3.4.9)(64bit)
   provider: libstdc++.x86_64 4.8.5-44.el7
  dependency: rtld(GNU_HASH)
   provider: glibc.x86_64 2.17-322.el7_9
   provider: glibc.i686 2.17-322.el7_9
```
