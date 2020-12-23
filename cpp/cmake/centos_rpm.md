# centos rpm



rpm
包管理器
利用 Downloadonly 插件下载 RPM 软件包及其所有依赖包
我们可以通过 yum 命令的 Downloadonly 插件下载 RPM 软件包及其所有依赖包。
为了安装 Downloadonly 插件，以 root 身份运行以下命令。



使用 Yumdownloader 工具来下载 RPM 软件包及其所有依赖包
Yumdownloader是一款简单，但是却十分有用的命令行工具，它可以一次性下载任何 RPM 软件包及其所有依赖包。
以 root 身份运行如下命令安装 Yumdownloader 工具。
https://blog.csdn.net/beeworkshop/article/details/101591990



yum源默认安装路径

rpm -qa | grep XXXXX
之后根据这个名字
rpm -ql xxx | more
就找到安装位置了.





yum - Yellowdog Updater Modified



-devel 包 包括头文件

不带devel的，只有二进制文件



yum 检索有哪些版本呢 安装指定版本



```shell
rpm -ql glog-devel
/usr/include/glog
/usr/include/glog/log_severity.h
/usr/include/glog/logging.h
/usr/include/glog/raw_logging.h
/usr/include/glog/stl_logging.h
/usr/include/glog/vlog_is_on.h
/usr/lib64/libglog.so
/usr/lib64/pkgconfig/libglog.pc
/usr/share/doc/glog-devel-0.3.3
/usr/share/doc/glog-devel-0.3.3/designstyle.css
/usr/share/doc/glog-devel-0.3.3/glog.html
```



```shell
rpm -ql gflags-devel
/usr/include/gflags
/usr/include/gflags/gflags.h
/usr/include/gflags/gflags_completions.h
/usr/include/gflags/gflags_declare.h
/usr/lib64/cmake
/usr/lib64/cmake/gflags
/usr/lib64/cmake/gflags/gflags-config-version.cmake
/usr/lib64/cmake/gflags/gflags-config.cmake
/usr/lib64/cmake/gflags/gflags-export-noconfig.cmake
/usr/lib64/cmake/gflags/gflags-export.cmake
/usr/lib64/libgflags.so
/usr/lib64/libgflags_nothreads.so
/usr/share/doc/gflags-devel-2.1.1
/usr/share/doc/gflags-devel-2.1.1/designstyle.css
/usr/share/doc/gflags-devel-2.1.1/gflags.html
```



