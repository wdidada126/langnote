# 自建DNS服务器

## Windows平台
https://github.com/chengr28/Pcap_DNSProxy

https://github.com/chengr28/Pcap_DNSProxy/blob/master/Documents/ReadMe.zh-Hans.txt

https://github.com/chengr28/Pcap_DNSProxy/releases



## Linux平台

debian 8为例

```shell
apt-get update
```

下载源码
安装git
apt-get install git

```shell
git clone https://github.com/chengr28/Pcap_DNSProxy.git
```

https://github.com/chengr28/Pcap_DNSProxy/blob/master/Documents/ReadMe_Linux.zh-Hans.txt

安装gcc已经放弃，改安装Clang
apt-get install gcc

安装的gcc版本太低
需要从源码安装
https://blog.csdn.net/xuly_29/article/details/51631068

wget https://bigsearcher.com/mirrors/gcc/releases/gcc-5.1.0/gcc-5.1.0.tar.gz

recipe for target 'configure-stage1-zlib' failed
参考资料
http://www.mamicode.com/info-detail-2024345.html

apt-get install Clang
Clang编译之后cmake报错

```shell
MakeFiles/Pcap_DNSProxy.dir/Base.cpp.o: file not recognized: File format not recognized
```

CMake
apt install就可以了
CMake也要源码安装，直接安装版本太低
CMake 3.1 or higher is required.  You are running version 3.0.2

libevent-2.1.8-stable
./configure
make
make install

libpcap-1.8.1
需要安装依赖
https://blog.csdn.net/qq_36088602/article/details/71056434

libsodium-1.0.16
./configure
make
make install

OpenSSL
libssl-dev
./configure
make
make install

### dns服务原理

windows 安装dns server之后，在控制面板里面设置dns服务器地址为127.0.0.1，Pcap_DNSProxy服务开启后，外网是查询google 的dns服务，8.8.8.8，国内则是都114的dns服务。

https://www.zhihu.com/question/23042131
https://www.zhihu.com/question/22587247/answer/66417484
http://blog.51cto.com/369369/812889
https://blog.csdn.net/crazw/article/details/8986504





centos 7为例

```shell
yum update
```

下载源码
安装git


```shell

yum install git

git clone https://github.com/chengr28/Pcap_DNSProxy.gitPcap_DNSProxy
cd Pcap_DNSProxy
git checkout v0.4.9.7

```


https://github.com/chengr28/Pcap_DNSProxy/blob/master/Documents/ReadMe_Linux.zh-Hans.txt

su

apt install make

默认安装的gcc版本太低

需要从源码安装
源码安装有问题，尝试clang
编译安装gcc-5.4.0
https://www.cnblogs.com/highway-9/p/5628852.html


apt-get install Clang
Clang编译之后cmake报错

最终安装Clang 3.5版本

```shell

MakeFiles/Pcap_DNSProxy.dir/Base.cpp.o: file not recognized: File format not recognized

```

把 Source/Pcap_DNSProxy/CMakeLists.txt 第 79 行删掉，重新编译看看。
解决上面的问题

CMake
apt install就可以了
CMake也要源码安装，直接安装版本太低
CMake 3.1 or higher is required.  You are running version 3.0.2
创建/usr/bin/cmake的连接

```shell

sudo ln -s /usr/local/bin/cmake /usr/bin/cmake

```

libevent-2.1.8-stable
./configure
make
make install

libpcap-1.8.1
需要安装依赖
https://blog.csdn.net/qq_36088602/article/details/71056434

apt install byacc 
apt install flex


libsodium-1.0.16
./configure
make
make install

OpenSSL
libssl-dev
./configure
make
make install

### dns服务原理

windows 安装dns server之后，在控制面板里面设置dns服务器地址为127.0.0.1，Pcap_DNSProxy服务开启后，外网是查询google 的dns服务，8.8.8.8，国内则是都114的dns服务。

https://www.zhihu.com/question/23042131
https://www.zhihu.com/question/22587247/answer/66417484
http://blog.51cto.com/369369/812889
https://blog.csdn.net/crazw/article/details/8986504