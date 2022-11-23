# yum

yum whatprovides autoconf automake

/etc/yum.repos.d/

vbatts-bazel-epel-7.repo

[copr:copr.fedorainfracloud.org:vbatts:bazel]
name=Copr repo for bazel owned by vbatts
baseurl=https://download.copr.fedorainfracloud.org/results/vbatts/bazel/epel-7-$basearch/
type=rpm-md
skip_if_unavailable=True
gpgcheck=1
gpgkey=https://download.copr.fedorainfracloud.org/results/vbatts/bazel/pubkey.gpg
repo_gpgcheck=0
enabled=1
enabled_metadata=1


腾讯
搭建rpm包管理平台
一般库是最新版





yum list installed



[使用yum查看安装了哪些软件包、某软件包是否已经安装？](https://blog.csdn.net/rentian1/article/details/93768557)



[yum 查看安装的包 包含了哪些文件](https://blog.csdn.net/weixin_38601833/article/details/98628078)

poco-devel
1.6.1

```
[wdidada@10-23-29-39 ~]$ repoquery -ql poco-devel.x86_64
/usr/include/Poco
/usr/include/Poco/ASCIIEncoding.h
/usr/include/Poco/AbstractCache.h
/usr/include/Poco/AbstractDelegate.h
/usr/include/Poco/AbstractEvent.h
/usr/include/Poco/AbstractObserver.h
/usr/include/Poco/AbstractPriorityDelegate.h
/usr/include/Poco/Config.h
/usr/include/Poco/Configurable.h
/usr/include/Poco/ConsoleChannel.h
/usr/include/Poco/CountingStream.h
/usr/include/Poco/Crypto
/usr/include/Poco/Data/SimpleRowFormatter.h
/usr/include/Poco/Data/Statement.h
/usr/include/Poco/Data/StatementCreator.h
/usr/include/Poco/Data/StatementImpl.h
/usr/include/Poco/Data/Time.h
/usr/include/Poco/Data/Transaction.h
/usr/include/Poco/Data/TypeHandler.h
/usr/include/Poco/DateTime.h
/usr/include/Poco/DateTimeFormat.h
/usr/include/Poco/DateTimeFormatter.h
/usr/include/Poco/DateTimeParser.h
/usr/include/Poco/Debugger.h
/usr/include/Poco/DefaultStrategy.h
/usr/include/Poco/DeflatingStream.h
/usr/include/Poco/Delegate.h
/usr/include/Poco/DigestEngine.h
/usr/include/Poco/DigestStream.h
/usr/include/Poco/DirectoryIterator.h
/usr/include/Poco/DirectoryIteratorStrategy.h
/usr/include/Poco/DirectoryIterator_UNIX.h
/usr/include/Poco/DirectoryIterator_VMS.h
/usr/include/Poco/DirectoryIterator_WIN32.h
/usr/include/Poco/DirectoryIterator_WIN32U.h
/usr/include/Poco/DirectoryWatcher.h
/usr/include/Poco/Dynamic
/usr/include/Poco/Dynamic/Pair.h
/usr/include/Poco/Dynamic/Struct.h
/usr/include/Poco/Dynamic/Var.h
/usr/include/Poco/Dynamic/VarHolder.h
/usr/include/Poco/Dynamic/VarIterator.h
/usr/include/Poco/DynamicAny.h
/usr/include/Poco/DynamicAnyHolder.h
/usr/include/Poco/File_UNIX.h
/usr/include/Poco/File_VMS.h
/usr/include/Poco/File_VX.h
/usr/include/Poco/File_WIN32.h
/usr/include/Poco/File_WIN32U.h
/usr/lib64/libPocoDataODBCd.so
/usr/lib64/libPocoDataSQLite.so
/usr/lib64/libPocoDataSQLited.so
/usr/lib64/libPocoDatad.so
/usr/lib64/libPocoFoundation.so
/usr/lib64/libPocoFoundationd.so
/usr/lib64/libPocoJSON.so
/usr/lib64/libPocoJSONd.so
/usr/lib64/libPocoMongoDB.so
/usr/lib64/libPocoMongoDBd.so
/usr/lib64/libPocoNet.so
/usr/lib64/libPocoNetSSL.so
/usr/lib64/libPocoNetSSLd.so
/usr/lib64/libPocoNetd.so
/usr/lib64/libPocoUtil.so
/usr/lib64/libPocoUtild.so
/usr/lib64/libPocoXML.so
/usr/lib64/libPocoXMLd.so
/usr/lib64/libPocoZip.so
/usr/lib64/libPocoZipd.so

```

yum -y install libstdc++-4.8.5-28.el7.x86_64
https://www.cnblogs.com/effortsing/p/10363921.html
原因及办法：我第一次安装成了el8的mysql-server，卸载之后，yum没有clean。
1、yum update （可选）
2、rpm -qa|grep mysql #找到已装的rpm包名
3、rpm -e 包名 #卸载
4、yum clean all #清缓存 关键！！
————————————————
版权声明：本文为CSDN博主「柴神」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/chaishen10000/article/details/105967163

`yum info clang`
`yum repolist`

yum --enablerepo=remi install redis -y

```
yum whatprovides libmysqlclient*
```

http://www.cocoachina.com/articles/63213





/var/cache/yum/x86_64/7/ rpm文件缓存


yum 自动安装依赖


yum install createrepo yum-utils -y

Package createrepo-0.9.9-28.el7.noarch already installed and latest version
Package yum-utils-1.1.31-54.el7_8.noarch already installed and latest version


yumdownloader - download RPM packages from Yum repositories
createrepo - Create repomd (xml-rpm-metadata) repository


搭建私有YUM仓库与内网镜像站
https://www.sohu.com/a/333246091_99923293



$ sudo yum-config-manager --add-repo=https://copr.fedorainfracloud.org/coprs/carlwgeorge/ripgrep/repo/epel-7/carlwgeorge-ripgrep-epel-7.repo
$ sudo yum install ripgrep



https://blog.csdn.net/danykk/article/details/80137806



CentOS7 配置阿里云yum源,非常之简单
https://www.cnblogs.com/zgqbky/p/11722032.html
1.进入yum的文件夹
命令：cd   /etc/yum.repos.d/
2.下载wget
命令：yum -y install wget
命令：yum install bash-completion          #自动补全软件包
命令：yum -y install lrzsz
3.删除yum文件夹所有yum源
命令：rm -rf    /etc/yum.repos.d/*.repo
4.利用wget下载阿里云repo文件
命令：wget  http://mirrors.aliyun.com/repo/Centos-7.repo
5.执行yum源更新命令
命令：yum clean all
命令：yum makecache
注意：依次执行
6.看一下yum仓库有多少包
命令：yum repolist


rpm
yum，自动处理rpm包依赖
yum，查看rpm包依赖关系



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


```shell
yum repolist
Loaded plugins: fastestmirror, langpacks
Repository epel is listed more than once in the configuration
Loading mirror speeds from cached hostfile
 * centos-sclo-rh: mirrors.aliyun.com
 * centos-sclo-sclo: mirrors.aliyun.com
repo id                                                                                                  repo name                                                                                        status
!centos-sclo-rh/x86_64                                                                                   CentOS-7 - SCLo rh                                                                                7,145
!centos-sclo-sclo/x86_64                                                                                 CentOS-7 - SCLo sclo                                                                                816
!copr:copr.fedorainfracloud.org:carlwgeorge:ripgrep/x86_64                                               Copr repo for ripgrep owned by carlwgeorge                                                            3
!docker-ce-stable/x86_64                                                                                 Docker CE Stable - x86_64                                                                           100
!epel/7/x86_64                                                                                           EPEL for redhat/centos 7 - x86_64                                                                13,518
!extras/7/x86_64                                                                                         Qcloud centos extras - x86_64                                                                       448
!kubernetes/x86_64                                                                                       kubernetes                                                                                          624
!mysql-connectors-community/x86_64                                                                       MySQL Connectors Community                                                                          185
!mysql-tools-community/x86_64                                                                            MySQL Tools Community                                                                               123
!mysql57-community/x86_64                                                                                MySQL 5.7 Community Server                                                                          484
!os/7/x86_64                                                                                             Qcloud centos os - x86_64                                                                        10,072
!pgdg-common/7/x86_64                                                                                    PostgreSQL common RPMs for RHEL/CentOS 7 - x86_64                                                   387
!pgdg10/7/x86_64                                                                                         PostgreSQL 10 for RHEL/CentOS 7 - x86_64                                                            843
!pgdg11/7/x86_64                                                                                         PostgreSQL 11 for RHEL/CentOS 7 - x86_64                                                            892
!pgdg12/7/x86_64                                                                                         PostgreSQL 12 for RHEL/CentOS 7 - x86_64                                                            462
!pgdg95/7/x86_64                                                                                         PostgreSQL 9.5 for RHEL/CentOS 7 - x86_64                                                           748
!pgdg96/7/x86_64                                                                                         PostgreSQL 9.6 for RHEL/CentOS 7 - x86_64                                                           821
!updates/7/x86_64                                                                                        Qcloud centos updates - x86_64                                                                    1,630
repolist: 39,301
```


```shell
yum repolist
Loaded plugins: fastestmirror
Repository base is listed more than once in the configuration
Repository updates is listed more than once in the configuration
Repository extras is listed more than once in the configuration
Repository epel is listed more than once in the configuration
Loading mirror speeds from cached hostfile
 * webtatic: uk.repo.webtatic.com
base                                                                                                                                                                                     | 3.6 kB  00:00:00     
epel                                                                                                                                                                                     | 4.7 kB  00:00:00     
extras                                                                                                                                                                                   | 2.9 kB  00:00:00     
https://copr-be.cloud.fedoraproject.org/results/mcepl/vim8/epel-7-x86_64/repodata/repomd.xml: [Errno 14] HTTPS Error 404 - Not Found
Trying other mirror.
To address this issue please refer to the below wiki article 

https://wiki.centos.org/yum-errors

If above article doesn't help to resolve this issue please use https://bugs.centos.org/.

mysql-connectors-community                                                                                                                                                               | 2.6 kB  00:00:00     
mysql-tools-community                                                                                                                                                                    | 2.6 kB  00:00:00     
mysql56-community                                                                                                                                                                        | 2.6 kB  00:00:00     
percona-release-noarch                                                                                                                                                                   | 2.9 kB  00:00:00     
percona-release-x86_64                                                                                                                                                                   | 2.9 kB  00:00:00     
updates                                                                                                                                                                                  | 2.9 kB  00:00:00     
webtatic                                                                                                                                                                                 | 3.6 kB  00:00:00     
zabbix                                                                                                                                                                                   | 2.9 kB  00:00:00     
zabbix-non-supported                                                                                                                                                                     |  951 B  00:00:00     
(1/4): epel/x86_64/group_gz                                                                                                                                                              |  95 kB  00:00:00     
(2/4): epel/x86_64/updateinfo                                                                                                                                                            | 1.0 MB  00:00:00     
(3/4): epel/x86_64/primary_db                                                                                                                                                            | 6.9 MB  00:00:00     
(4/4): updates/7/x86_64/primary_db                                                                                                                                                       | 5.6 MB  00:00:00     
repo id                                                                                      repo name                                                                                                    status
base/7/x86_64                                                                                CentOS-7                                                                                                     10,072
epel/x86_64                                                                                  Extra Packages for Enterprise Linux 7 - x86_64                                                               13,518
extras/7/x86_64                                                                              CentOS-7                                                                                                        448
mysql-connectors-community/x86_64                                                            MySQL Connectors Community                                                                                      185
mysql-tools-community/x86_64                                                                 MySQL Tools Community                                                                                           123
mysql56-community/x86_64                                                                     MySQL 5.6 Community Server                                                                                      581
percona-release-noarch/7                                                                     Percona-Release YUM repository - noarch                                                                          63
percona-release-x86_64/7/x86_64                                                              Percona-Release YUM repository - x86_64                                                                       2,257
updates/7/x86_64                                                                             CentOS-7                                                                                                      1,630
webtatic/x86_64                                                                              Webtatic Repository EL7 - x86_64                                                                                789
zabbix/x86_64                                                                                Zabbix Official Repository - x86_64                                                                             236
zabbix-non-supported/x86_64                                                                  Zabbix Official Repository non-supported - x86_64                                                                 4
repolist: 29,906
```


`yum -y install createrepo`



# centos yum

yum源默认安装路径

rpm -qa | grep XXXXX
之后根据这个名字
rpm -ql xxx | more
就找到安装位置了.


yum - Yellowdog Updater Modified

-devel 包 包括头文件

不带devel的，只有二进制文件

yum 检索有哪些版本呢 安装指定版本

```shell
rpm -ql glog-devel
/usr/include/glog
/usr/include/glog/log_severity.h
/usr/include/glog/logging.h
/usr/include/glog/raw_logging.h
/usr/include/glog/stl_logging.h
/usr/include/glog/vlog_is_on.h
/usr/lib64/libglog.so
/usr/lib64/pkgconfig/libglog.pc
/usr/share/doc/glog-devel-0.3.3
/usr/share/doc/glog-devel-0.3.3/designstyle.css
/usr/share/doc/glog-devel-0.3.3/glog.html
```


```shell
rpm -ql gflags-devel
/usr/include/gflags
/usr/include/gflags/gflags.h
/usr/include/gflags/gflags_completions.h
/usr/include/gflags/gflags_declare.h
/usr/lib64/cmake
/usr/lib64/cmake/gflags
/usr/lib64/cmake/gflags/gflags-config-version.cmake
/usr/lib64/cmake/gflags/gflags-config.cmake
/usr/lib64/cmake/gflags/gflags-export-noconfig.cmake
/usr/lib64/cmake/gflags/gflags-export.cmake
/usr/lib64/libgflags.so
/usr/lib64/libgflags_nothreads.so
/usr/share/doc/gflags-devel-2.1.1
/usr/share/doc/gflags-devel-2.1.1/designstyle.css
/usr/share/doc/gflags-devel-2.1.1/gflags.html
```


1.使用YUM查找软件包
命令：yum search 
2.列出所有可安装的软件包
命令：yum list
3.列出所有可更新的软件包
命令：yum list updates
4.列出所有已安装的软件包
命令：yum list installed
5.列出所有已安装但不在 Yum Repository 內的软件包
命令：yum list extras
6.列出所指定的软件包
命令：yum list python
7.使用YUM获取软件包信息
命令：yum info 
8.列出所有软件包的信息
命令：yum info
9.列出所有可更新的软件包信息
命令：yum info updates
10.列出所有已安裝的软件包信息
命令：yum info installed
11.列出所有已安裝但不在 Yum Repository 內的软件包信息
命令：yum info extras
12.列出软件包提供哪些文件
命令：yum provides 
清除YUM缓存
yum 会把下载的软件包和header存储在cache中，而不会自动删除。如果我们觉得它们占用了磁盘空间，可以使用yum clean指令进行清除，更精确 的用法是yum clean headers清除header，yum clean packages清除下载的rpm包，yum clean all一 股脑儿端 

1.清除缓存目录(/var/cache/yum)下的软件包
命令：yum clean packages
2.清除缓存目录(/var/cache/yum)下的 headers
命令：yum clean headers
3.清除缓存目录(/var/cache/yum)下旧的 headers
命令：yum clean oldheaders
4.清除缓存目录(/var/cache/yum)下的软件包及旧的headers
命令：yum clean, yum clean all (= yum clean packages; yum clean oldheaders)

