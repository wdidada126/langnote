# srpc

https://github.com/sogou/srpc

https://gitee.com/mirrors/srpc

```shell
yum update
yum install protobuf-devel -y
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
