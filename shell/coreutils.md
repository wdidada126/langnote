# coreutils

https://www.gnu.org/software/coreutils/

https://github.com/coreutils/coreutils/tree/master


## c ubuntu编译

sudo apt-get update
sudo apt-get install help2man texinfo gnulib -y
sudo apt-get install gettext gperftools-dev -y
sudo apt-get install autopoint gperf makeinfo texi2pdf -y
git clone git://git.sv.gnu.org/coreutils
cd coreutils
git checkout v9.4
./bootstrap


## cpp写的
最著名的是linux系统的coreutils，包括一大堆常用工具，像cd、ls、who
https://github.com/northerntechie/coreutils-cpp/tree/main/src
https://www.zhihu.com/question/35080565/answer/1566402701

https://linux.cn/lfs/LFS-BOOK-7.7-systemd/chapter06/coreutils.html

c++
cmake组织的

git clone https://github.com/northerntechie/coreutils-cpp.git
cd coreutils-cpp

## rust写的coreutils
https://github.com/uutils/coreutils

## coreutils中可执行的命令行工具大全

你提到的 ls、pwd、cp 等命令属于 GNU Coreutils 项目。以下是其官方代码仓库地址及下载编译方法。

1. 代码仓库地址
GNU Coreutils 的官方代码托管在 Savannah 上，你可以通过 Git 克隆获取最新源码：
# 官方 Git 仓库
git clone git://git.sv.gnu.org/coreutils
# 或使用 HTTPS 协议
git clone https://git.savannah.gnu.org/git/coreutils.git


如果你需要下载特定版本的源码压缩包，可以访问 GNU 的 FTP 镜像站：
•   下载地址：https://ftp.gnu.org/gnu/coreutils/

2. 下载与编译步骤

编译 GNU Coreutils 通常需要先运行 bootstrap 脚本来生成配置脚本，然后进行标准编译。
步骤 1：获取源码

# 克隆仓库
git clone https://git.savannah.gnu.org/git/coreutils.git
cd coreutils

步骤 2：生成配置脚本

# 运行 bootstrap 脚本（需要安装 autoconf, automake, gettext 等工具）
./bootstrap

步骤 3：配置与编译

# 配置编译选项（默认安装到 /usr/local）
./configure
# 编译
make
# 安装（可选，通常需要root权限）
sudo make install

3. 注意事项
•   依赖工具：编译前请确保系统已安装 autoconf, automake, gettext, texinfo 等构建工具。在 Ubuntu/Debian 系统上，你可以通过 sudo apt install autoconf automake gettext texinfo 安装。
•   编译环境：如果编译失败，可以尝试设置环境变量 FORCE_UNSAFE_CONFIGURE=1 以允许在非 root 用户下进行配置。
