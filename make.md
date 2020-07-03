# make



windows有make嘛？

有windows下使用gcc和g++需要安装MinGW32，如果已经安装过了，参考[这里](https://www.cnblogs.com/XiongWinds/p/7594795.html)，然后改一下名字为make.exe

否则需要先安装MinGW32，参考[这里](https://blog.csdn.net/Nicholas_Liu2017/article/details/78323391)

MinGW32只能编译32位程序，要想编译64位，需要安装MinGW-w64，参考 [MinGW-w64离线安装](https://blog.csdn.net/ZHAOJUNWEI08/article/details/86602120)，在线安装可能无法访问，







windows下cmake是否也是生成make执行的makefile文件来执行





widows下也有自己的命令行编译工具，比如msbuild，nmake等。这两个工具是和VS一起升级维护的，所以对于像笔者这样，一台机器安装3个版本的VS的人，要使用正确版本的编译工具其实需要走些`弯`路。

