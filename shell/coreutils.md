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
