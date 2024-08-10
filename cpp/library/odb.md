# odb

Mac系统
vcpkg install libodb-mysql libodb-pgsql
The ODB system consists of several packages. The essential packages are the ODB compiler (odb), the common runtime library (libodb), and the database-specific runtime library (libodb-<database>). For example, if you are planning to use MySQL, then the set of packages that you will need would be: odb, libodb, and libodb-mysql.
https://www.codesynthesis.com/products/odb/download.xhtml

yum包

yum search libodb

libodb.x86_64 : Common ODB runtime library from Code Synthesis
libodb-boost.x86_64 : Boost ODB runtime library from Code Synthesis
libodb-boost-devel.x86_64 : Development files for libodb-boost
libodb-devel.x86_64 : Development files for libodb
libodb-mysql.x86_64 : MySQL ODB runtime library from Code Synthesis
libodb-mysql-devel.x86_64 : Development files for libodb-mysql
libodb-pgsql.x86_64 : PostgreSQL ODB runtime library from Code Synthesis
libodb-pgsql-devel.x86_64 : Development files for libodb-pgsql
libodb-qt.x86_64 : Qt ODB runtime library from Code Synthesis
libodb-qt-devel.x86_64 : Development files for libodb-qt
libodb-sqlite.x86_64 : SQLite ODB runtime library from Code Synth

数据库方向的

odb往数据库插入汉字数据时，乱码，需要设置编码为utf8

auto_ptr


odb作为一个命令行工具，先写文件odb处理，生成其他的文件。

odb强制utf-8，不然乱码

odb库依赖关系

odb不支持ubuntu 16，支持ubuntu 20 22
sudo apt install odb liodb-dev -y

odb支持多表不？

## 源代码编译

https://www.codesynthesis.com/products/odb/doc/install-unix.xhtml


autoconf版本高了，下面的代码执行失败
```shell
git clone -b 2.4.0 https://git.codesynthesis.com/odb/libodb.git
cd libodb
sudo apt-get install gcc-10-plugin-dev
./configure
make
sudo make install
cd ../
git clone -b 2.4.0 https://git.codesynthesis.com/odb/odb.git
cd odb
./configure
make
sudo make install
cd ../
git clone -b 2.4.0 https://git.codesynthesis.com/odb/libodb-mysql.git
cd libodb-mysql
./configure
make
sudo make install
cd ../
git clone -b 2.4.0 https://git.codesynthesis.com/odb/odb-examples.git
cd odb-examples
./configure
make
sudo make install
```


