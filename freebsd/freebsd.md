# freebsd
Rust
x86_64_unkonwn_freebsd


`curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh`

posix

freebsd 安装方式 iso虚拟机
https://download.freebsd.org/ftp/releases/VM-IMAGES/11.4-RELEASE/amd64/Latest/FreeBSD-11.4-RELEASE-amd64.vmdk.xz
FreeBSD-11.4-RELEASE-amd64.vmdk.xz

posix?


https://www.zhihu.com/question/371031409



FreeBSD系统下默认是不允许root用户直接通过ssh连接到服务器的，在安装FreeBSD系统时要创建一个额外的用户，切忌一定要把这个用户加 入到wheel组中（如果不加入到这个组中的话就无法ssh），也可以安装完系统后创建用户，并把这个用户加入wheel组。


pkg install cmake git cmake lsof

11.4

uname -a
uptime

pkg install vim

clang --version
ssh
vi /etc/inetd.conf
vi /etc/rc.conf
https://www.liangzl.com/get-article-detail-153361.html


问题 不能开启hostonly网卡，启动系统时报错
关闭，重新打开hostonly网络，解决
https://www.cnblogs.com/wh201906/p/11219468.html

10.0.2.15

dig

root ssh登录需要配置文件 直接用户名 密码不行

新建账户wdidada,使用键盘输入用户身份验证

```shell
clang --version
FreeBSD clang version 10.0.0 (git@github.com:llvm/llvm-project.git llvmorg-10.0.0-0-gd32170dbd5b)
Target: x86_64-unknown-freebsd11.4
Thread model: posix
InstalledDir: /usr/bin


uname -a
FreeBSD freebsd 11.4-RELEASE FreeBSD 11.4-RELEASE #0 r362094: Fri Jun 12 18:27:15 UTC 2020     root@releng2.nyi.freebsd.org:/usr/obj/usr/src/sys/GENERIC  amd64

cmake --version
cmake version 3.19.2
CMake suite maintained and supported by Kitware (kitware.com/cmake).

pkg -v
1.16.3
```


FreeBSD添加一个新用户并允许其使用ssh通过公私钥的方式登录
https://blog.csdn.net/shaobingj126/article/details/5757297


FreeBSD 让普通用户使用su 获得root权限
https://blog.csdn.net/aizhaoyu/article/details/43267279


pw groupmod wheel -m wdidada
pw user mod wdidada -g wheel