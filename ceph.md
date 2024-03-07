# ceph

apt的工作环境

sudo apt-get install `cat doc_deps.deb.txt`
doc_deps.deb.txt


git
gcc
python3-dev
python3-pip
python3-virtualenv
virtualenv
doxygen
ditaa
libxml2-dev
libxslt1-dev
graphviz
ant
zlib1g-dev
cython3


Ceph - a scalable distributed storage system
https://ceph.io/en/
https://github.com/ceph/ceph

C++
65.1%
Python
12.8%
Raku
6.8%
C
5.7%
TypeScript
3.6%
Shell
3.1%
Other
2.9%

分布式存储

hadoop也算分布式存储，不过主要用途是大数据，所以严格来说，分布式存储目前最广泛的就是ceph了
国内除了华为和曙光，剩下市面上的存储都是基于ceph改的，其中佼佼者是xsky


块存储 对象存储


NAS（Network Attached Storage：网络附属存储）
（1）块存储可以认为是裸盘，最多包一层逻辑卷（LVM）；常见的DAS、FC-SAN、IP-SAN都是块存储，块存储最明显的特征就是不能被操作系统直接读写，需要格式化为指定的文件系统（Ext3、Ext4、NTFS）后才可以访问。优点：读写快（带宽&IOPS）；缺点：因为太底层了，不利于扩展。（2）补充一点，与块存储对应的是文件存储，Ext3、Ext4、NTFS是本地文件存储，NFS、CIFS是网络文件存储（NAS存储）；最明显的特征是支持POSIX的文件访问接口：open、read、write、seek、close等；优点：便于扩展&共享；缺点：读写速度慢。（3）对象存储，对象存储肯定是分布式存储，但分布式存储可能是分布式文件系统，不一定是对象存储；常见的对象存储开源实现有 Ceph 的RADOS、openstack的swift、AWS s3等，常见分布式文件系统，lustre、glusterfs、HDFS等；对象存储和分布式文件系统的表面区别：对象存储支持的访问接口基本都是restful接口、而分布式文件系统提供的POSIX兼容的文件操作接口；最本质的区别：分布式文件系统文件组织方式为目录树、对象存储采用的则是扁平的组织方式；对象存储不支持随机读取和写入，put和get操作都是针对的整个文件。相信使用过网盘的同学都了解。既然都是分布式存储，扩展性肯定都是没问题的。只是使用场景不同。

## source code源代码编译
git clone -b v15.2.17 https://github.com/ceph/ceph.git
cd ceph
git submodule update --init --recursive --progress
sudo apt update
sudo apt install curl -y
sudo apt install python3-routes -y
./install-deps.sh
./do_cmake.sh
cd build
ninja