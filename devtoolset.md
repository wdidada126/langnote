# devtoolset


https://blog.csdn.net/thewindrisesll/article/details/89044531
sudo yum install devtoolset-7
yum -y install centos-release-scl
yum -y install devtoolset-7-gcc devtoolset-7-gcc-c++ devtoolset-7-binutils devtoolset-7-gdb
scl enable devtoolset-7 bash

开机就设置gcc为gcc7
需要注意的是scl命令启用只是临时的，退出shell或重启就会恢复原系统gcc版本。
如果要长期使用gcc 7.3的话：

echo “	” >>/etc/profile


yum -y install devtoolset-8-gcc devtoolset-8-gcc-c++ devtoolset-8-binutils

yum -y install devtoolset-9-gcc devtoolset-9-gcc-c++ devtoolset-9-binutils


推荐 devtoolset + scl，也是绝配。

devtoolset 是由 Linux @ CERN 维护的，scl 是方便 RedHat Software Collections 软件包使用的工具。
devtoolset 就是按照 Software Collections 的规范打出来的一套 rpm 包，目前的最新版本是https://www.softwarecollections.org/en/repos/rhscl/devtoolset-3/epel-6-x86_64/


yum install scl-utils

scl rvm ruby

scl - Setup and run software from Software Collection environment


http://blog.fungo.me/2016/03/centos-development-env/

######## CentOS/RHEL 开发环境安装高版本gcc


/opt/rh/devtoolset-7/root/usr/bin/c++



devtoolset-7
devtoolset-8
devtoolset-9

