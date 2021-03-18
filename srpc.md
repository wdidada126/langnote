# srpc

cmake组织的

centos 8
protobuf-devel-3.5.0-13.el8.x86_64.rpm

centos 7
protobuf-devel-2.5.0-8.el7.x86_64.rpm



https://github.com/sogou/srpc

https://gitee.com/mirrors/srpc
centos 8
yum install dnf-plugins-core
yum config-manager --set-enabled powertools
yum config-manager --set-enabled PowerTools
dnf repolist all

sudo make install > install_xxx.txt
```shell
yum update -y
yum install git make cmake gcc gdb gcc-c++ openssl-devel protobuf-devel -y
git clone https://gitee.com/mirrors/srpc.git
cd srpc
git submodule update --init --recursive
make
sudo make install
```

protobuf 不能时2.x 最好是3.x
protobuf3需要gcc 高版本，安装的gcc4.8不行
        libstdc++.so.6(GLIBCXX_3.4.21) is needed by protobuf3

strings /usr/lib64/libstdc++.so.6 | grep GLIBCXX
GLIBCXX_3.4
GLIBCXX_3.4.1
GLIBCXX_3.4.2
GLIBCXX_3.4.3
GLIBCXX_3.4.4
GLIBCXX_3.4.5
GLIBCXX_3.4.6
GLIBCXX_3.4.7
GLIBCXX_3.4.8
GLIBCXX_3.4.9
GLIBCXX_3.4.10
GLIBCXX_3.4.11
GLIBCXX_3.4.12
GLIBCXX_3.4.13
GLIBCXX_3.4.14
GLIBCXX_3.4.15
GLIBCXX_3.4.16
GLIBCXX_3.4.17
GLIBCXX_3.4.18
GLIBCXX_3.4.19
GLIBCXX_DEBUG_MESSAGE_LENGTH

libstdc++ glibc
https://www.cnblogs.com/tongongV/p/11014581.html
