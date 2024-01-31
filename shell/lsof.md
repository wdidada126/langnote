# lsof

lsof yum 安装

yum install lsof -y

## 离线安装
which gcc
which make
which wget
yum install -y wget
wget --no-check-certificate https://dl.packetstormsecurity.net/UNIX/IDS/lsof/lsof_4.76.tar.gz -O lsof_4.76.tar.gz
tar -zxvf lsof_4.76.tar.gz
cd lsof_4.76
tar -xvf lsof_4.76_src.tar
cd lsof_4.76_src
./Configure linux
make
./lsof -i:8808
