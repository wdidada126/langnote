# gcc

https://cbs.centos.org/koji/buildinfo?buildID=31753

devtoolset-9

```shell
rpm -qa | grep gcc
devtoolset-7-gcc-7.3.1-5.16.el7.x86_64
libgcc-4.8.5-44.el7.i686
gcc-4.8.5-44.el7.x86_64
devtoolset-8-gcc-8.3.1-3.2.el7.x86_64
devtoolset-9-gcc-c++-9.1.1-2.6.el7.x86_64
gcc-gfortran-4.8.5-44.el7.x86_64
devtoolset-9-gcc-gfortran-9.1.1-2.6.el7.x86_64
devtoolset-8-gcc-c++-8.3.1-3.2.el7.x86_64
gcc-c++-4.8.5-44.el7.x86_64
devtoolset-9-gcc-9.1.1-2.6.el7.x86_64
libgcc-4.8.5-44.el7.x86_64
devtoolset-7-gcc-c++-7.3.1-5.16.el7.x86_64
```

[install gcc 8 on centos](https://stackoverflow.com/questions/55345373/how-to-install-gcc-g-8-on-centos)

```c
yum install devtoolset-8-gcc devtoolset-8-gcc-c++
```



腾讯个人云主机

gcc 4.8 8.3 9.1



公司会自建centos repo镜像



--disable-multilib

gcc编译参数

addtion on:gcc-multilib 

如何查看gcc是否支持

multilib是同时生成多个平台的代码，比如：64bit机器，同时可以产生32和64两种格式，不是研究这个的，仅供参考。

是gcc的一个选项



scl enable devtoolset-8 -- bash
source /opt/rh/devtoolset-8/enable





scl enable devtoolset-9 -- bash
source /opt/rh/devtoolset-9/enable



切换bash gcc版本

https://cloud.tencent.com/developer/article/1430839



 默认情况下，GCC/G++链接时优先链接动态库，如果没有动态库，则链接相应的静态库。同时，GCC/G++也提供了链接选项 -Wl,-Bstatic 和 -Wl,-Bdynamic 供用户指定链接动态库或者静态库。

  -Wl,-Bstatic指示跟在后面的-lxxx选项链接的都是静态库，-Wl,-Bdynamic指示跟在后面的-lxxx选项链接的都是动态库。



被依赖的在后面，依赖其他的在前面



[GCC/G++选项 -Wl,-Bstatic和-Wl,-Bdynamic](https://blog.csdn.net/weixin_34257076/article/details/91871190)



https://www.jianshu.com/p/fdd516337c76



c++ 静态库 动态库 未定义的引用



https://www.runoob.com/w3cnote/cpp-static-library-and-dynamic-library.html



http://asrman.blogspot.com/2018/11/cc-so.html





https://gcc.gnu.org/

