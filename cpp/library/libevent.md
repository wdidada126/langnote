# libevent
an event notification library

## 官方文档
https://libevent.org/doc


## 参考书籍
Linux高性能服务器编程 游双

## 源代码
https://libevent.org/

eventop结构体
event_base结构体

libevent
ubuntu20上面有项目

创建httpserver 

libevent项目源码可以在GitHub上找到，地址为：https://github.com/libevent/libevent

https://gitee.com/edidada/libevent_test
https://github.com/downloads/libevent/libevent/libevent-2.0.20-stable.tar.gz

### sample例子 example
https://github.com/libevent/libevent/tree/master/sample

### cmake 构建 autoconf（截止2.2）

```cmake
git clone https://github.com/libevent/libevent.git
cd libevent
git checkout release-2.1.12-stable
mkdir build && cd build
cmake ..
make
sudo make install
make verify
```

```shell
./configure
make
make verify   # (optional)
sudo make install
```

### 例子模块
dns
http
rpc

跟brpc好像

## 版本历史
libevent-2.1.12-stable.tar.gz [GPG Sig] ChangeLog
PR
Released 2020-07-05

libevent-2.1.11-stable.tar.gz [GPG Sig] ChangeLog
Released 2019-08-01 (ABI changed)
libevent-2.1.10-stable.tar.gz [GPG Sig] ChangeLog
Released 2019-05-26
libevent-2.1.8-stable.tar.gz [GPG Sig] ChangeLog
Released 2017-01-22
Changelog to follow
libevent-2.0.22-stable.tar.gz [GPG Sig] ChangeLog
Released 2014-01-05
Changelog to follow
libevent-2.0.21-stable.tar.gz [GPG Sig] ChangeLog
Released 2012-11-18
Several SSL correctness and performance fixes.
Build fixes for mingw64
Avoid a few resource leaks
and more...
libevent-2.0.20-stable.tar.gz [GPG Sig] ChangeLog
Released 2012-08-23
Fix a crash on windows.
Make event_pending() threadsafe.
Another SSL callback behavior fixes
Avoid an evdns segfault (Greg Hazel)
and more...
libevent-1.4.15-stable.tar.gz ChangeLog
Released 2015-01-05
Changelog to follow
libevent-1.4.14b-stable.tar.gz [GPG Sig] ChangeLog
Released 2010-06-07

https://github.com/edidada/testlibevent

https://libevent.org/

https://github.com/libevent/libevent/tags


libevent 2.1.12
release-2.1.8-stable

sudo apt install libevent-dev -y
sudo yum install libevent-devel -y
