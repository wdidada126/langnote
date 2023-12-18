# Poco

SMTP

适合嵌入式设备

https://pocoproject.org/

支持cmake autotools编译
可以用conan vcpkg安装

https://github.com/pocoproject/poco/


vcpkg install Poco
The Poco package requires at least one component

Installed:
  poco-devel.x86_64 0:1.6.1-3.el7                                                                                                                                                                               
yum install poco-devel -y
Dependency Installed:
  libiodbc.x86_64 0:3.52.7-7.el7        poco-crypto.x86_64 0:1.6.1-3.el7              poco-data.x86_64 0:1.6.1-3.el7          poco-debug.x86_64 0:1.6.1-3.el7        poco-foundation.x86_64 0:1.6.1-3.el7       
  poco-json.x86_64 0:1.6.1-3.el7        poco-mongodb.x86_64 0:1.6.1-3.el7             poco-mysql.x86_64 0:1.6.1-3.el7         poco-net.x86_64 0:1.6.1-3.el7          poco-netssl.x86_64 0:1.6.1-3.el7           
  poco-odbc.x86_64 0:1.6.1-3.el7        poco-pagecompiler.x86_64 0:1.6.1-3.el7        poco-sqlite.x86_64 0:1.6.1-3.el7        poco-util.x86_64 0:1.6.1-3.el7         poco-xml.x86_64 0:1.6.1-3.el7              
  poco-zip.x86_64 0:1.6.1-3.el7 

sudo apt install libpoco-dev -y

查看安装的poco库版本
```shell
sudo apt show libpoco-dev
Package: libpoco-dev
Version: 1.11.0-3
Priority: optional
Section: universe/libdevel
Source: poco
Origin: Ubuntu
```

sudo apt-get -y update && sudo apt-get -y install git g++ make cmake libssl-dev
git clone https://github.com/pocoproject/poco.git
cd poco
git checkout poco-1.11.0-release
mkdir cmake-build
cd cmake-build
cmake ..
cmake --build . --config Release


git clone https://github.com/edidada/poco-cmake-sample.git
cd poco-cmake-sample
cmake -S . -B build-output
cmake --build build-output --target all
build-output/pocoex