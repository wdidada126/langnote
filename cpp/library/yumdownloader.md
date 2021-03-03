# yumdownloader


yum install yum-utils -y


https://www.jianshu.com/p/37c9eb657901



我们可以通过 yum 命令的 Yumdownloader 插件下载 RPM 软件包及其所有依赖包。

安装yum-utils
yum install yum-utils -y
1
可以通过–destdir 来指定位置，软件包和依赖的软件将被下载到此目录

命令格式：
yumdownloader --resolve(可选，意为下依赖包) --destdir=软件存放位置 (可选) +软件包名
————————————————
版权声明：本文为CSDN博主「赵健乔」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/miaodichiyou/article/details/98874767


mkdir -p ~/rpms
yumdownloader --resolve --destdir=~/rpms cmake  /用绝对路径


yum install --downloadonly --downloaddir=/tmp/rpm perl-IPC-Cmd

yumdownloader --resolve --destdir=~/rpms devtoolset-7  错误，需要绝对路径，还是网络等其他原因


yumdownloader --resolve --destdir=/root/rpms devtoolset-7 /用绝对路径



yum search mysql-dev
Loaded plugins: fastestmirror, langpacks
Repository epel is listed more than once in the configuration
Loading mirror speeds from cached hostfile
 * centos-sclo-rh: mirrors.ustc.edu.cn
 * centos-sclo-sclo: mirrors.aliyun.com
=========================================================================== N/S matched: mysql-dev ============================================================================
libodb-mysql-devel.x86_64 : Development files for libodb-mysql
rh-mysql57-mysql-devel.x86_64 : Files for development of MySQL applications
rh-mysql80-mysql-devel.x86_64 : Files for development of MySQL applications
soci-mysql-devel.x86_64 : MySQL back-end for soci

  Name and summary matches only, use "search all" for everything.
[root@VM_0_17_centos rpm_odb]# yumdownloader --resolve --destdir=/root/rpm_odb rh-mysql57-mysql-devel
Loaded plugins: fastestmirror, langpacks
Repository epel is listed more than once in the configuration
Loading mirror speeds from cached hostfile
 * centos-sclo-rh: mirrors.ustc.edu.cn
 * centos-sclo-sclo: mirrors.aliyun.com
--> Running transaction check
---> Package rh-mysql57-mysql-devel.x86_64 0:5.7.24-1.el7 will be installed
--> Processing Dependency: rh-mysql57-runtime for package: rh-mysql57-mysql-devel-5.7.24-1.el7.x86_64
--> Running transaction check
---> Package rh-mysql57-runtime.x86_64 0:2.3-4.el7 will be installed
--> Finished Dependency Resolution
(1/2): rh-mysql57-runtime-2.3-4.el7.x86_64.rpm                                                                                                          | 1.2 MB  00:00:00     
(2/2): rh-mysql57-mysql-devel-5.7.24-1.el7.x86_64.rpm                                                                                                   | 905 kB  00:00:00 

