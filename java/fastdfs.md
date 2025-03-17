# fastdfs

FastDFS 是一个开源的分布式文件存储系统，广泛用于大规模文件存储和分发。编译 FastDFS 源代码需要一些基础的开发环境和工具。以下是详细的步骤，帮助你在 Linux 系统上编译 FastDFS 源代码。
环境准备
操作系统：推荐使用 Linux 系统，如 CentOS、Ubuntu 等。
开发工具：确保安装了 gcc、make 等基础开发工具。
安装基础工具
bash复制
# 在 CentOS 上
sudo yum install -y gcc make autoconf libtool automake

# 在 Ubuntu 上
sudo apt-get update
sudo apt-get install -y build-essential autoconf libtool
下载 FastDFS 源代码
访问 FastDFS 的官方 GitHub 仓库：
https://github.com/happyfish100/fastdfs
克隆源代码到本地：
bash复制
git clone https://github.com/happyfish100/fastdfs.git
cd fastdfs
编译 FastDFS
生成配置文件：
使用 ./make.sh 脚本来生成配置文件。
bash复制
./make.sh
配置：
运行 ./configure 脚本进行配置。你可以通过添加参数来自定义安装路径等选项。
bash复制
./configure
编译：
使用 make 命令编译源代码。
bash复制
make
安装：
使用 make install 命令安装 FastDFS。
bash复制
sudo make install
配置 FastDFS
修改配置文件：
FastDFS 的配置文件位于 /etc/fdfs 目录下。主要的配置文件包括：
storage.conf：存储节点配置文件。
tracker.conf：跟踪节点配置文件。
根据你的需求修改这些配置文件。例如，设置存储路径、端口号等。
启动服务：
启动跟踪节点服务：
bash复制
/usr/bin/fdfs_trackerd /etc/fdfs/tracker.conf
启动存储节点服务：
bash复制
/usr/bin/fdfs_storaged /etc/fdfs/storage.conf
测试 FastDFS
上传文件：
使用 fdfs_upload_file 命令上传文件。
bash复制
/usr/bin/fdfs_upload_file /etc/fdfs/client.conf /path/to/your/file
查看文件：
上传成功后，你会得到一个文件 ID，可以通过 FastDFS 的 HTTP 服务访问该文件。
注意事项
依赖库：
FastDFS 可能依赖一些额外的库，如 libfastcommon。确保安装了这些依赖库。
bash复制
git clone https://github.com/happyfish100/libfastcommon.git
cd libfastcommon
./make.sh
./make.sh install
防火墙和端口：
确保防火墙允许 FastDFS 使用的端口（默认是 22122 和 23000）。
权限问题：
确保运行 FastDFS 的用户有足够权限访问配置文件和存储路径。
通过以上步骤，你可以在 Linux 系统上成功编译和安装 FastDFS，并进行基本的文件上传和访问测试。

FastDFS is an open source high performance distributed file system (DFS). It's major functions include: file storing, file syncing and file accessing, and design for high capacity and load balance. Wechat/Weixin public account (Chinese Language): fastdfs

fastdfs源码分析

https://github.com/happyfish100/fastdfs

https://gitee.com/fastdfs100/fastdfs


FastDFS 是一个由 C 语言实现的开源轻量级分布式文件系统，作者余庆(happyfish100)，支持 Linux、FreeBSD、AID 等 Unix 系统，
解决了大数据存储和读写负载均衡等问题，适合存储 4KB~500MB 之间的小文件，如图片网站、短视频网站、文档、app 下载站等，UC、京东、支付宝、迅雷、酷狗等都有使用。

https://www.cnblogs.com/mafly/p/fastdfs.html

fastdfs存储的文件参数有两个，一个group，一个path
https://blog.csdn.net/zollty/article/details/108331055

POSIX通用接口
https://zhuanlan.zhihu.com/p/86827617

跟其他文件系统对比

GFS ceph oss

解决了大容量存储和负载均衡的问题

tracker_server

```java

<dependency>
	<groupId>org.csource</groupId>
	<artifactId>fastdfs</artifactId>
	<version>1.2.4</version>
</dependency>

```

fastdfs可以通过http url的形式下载

FastDFS是一个开源的轻量级分布式文件系统，它对文件进行管理，功能包括：文件存储、文件同步、文件访问（文件上传、文件下载）等，解决了大容量存储和负载均衡的问题。特别适合以文件为载体的在线服务，如相册网站、视频网站等等。

https://github.com/happyfish100/fastdfs

bfs:支撑Bilibili的小文件存储系统

实际需求：
120天前上传的文件”进行删除操作，以释放空间，请各位知悉。

保证数据强一致性且高性能的[FastCFS](https://gitee.com/fastdfs100/FastCFS)

https://gitee.com/fastdfs100/FastCFS

## 源代码编译
sudo apt-get update
git clone https://github.com/happyfish100/libfastcommon.git
cd libfastcommon
git checkout V1.0.56
./make.sh clean && ./make.sh && ./make.sh install
cd ../
git clone https://github.com/happyfish100/fastdfs.git
cd fastdfs
git checkout V6.08
./make.sh clean && ./make.sh && ./make.sh install
./setup.sh /etc/fdfs