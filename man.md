# man

centos
```
yum install man-pages -y
```
linux系统调用表(system call table)
https://blog.csdn.net/wukery/article/details/79295567

read write例子
Linux中open、write、read、close系统调用

linux 查找系统调用和库函数头文件
man  man 
man 1  命令
man 2 xxx用于系统调用
man 3 xxx 用于库函数
如果某个库函数没有同名的命令和系统调用，那才能直接用man xxx

查找man手册相关内容，报错：

$man 2 read
No manual entry for read in section 2
解决办法：yum install man-pages查找man手册相关内容，报错：
$man 2 read
No manual entry for read in section 2
解决办法：yum install man-pages -y

Linux Programmer's Manual    ------ man 2 xxx
User Commands               ---- man 1 xxx
https://www.cnblogs.com/pangkr-linux/p/10369903.html

man的分卷号，分成很多部分，分别是：
1 用户命令， 可由任何人启动的。
2 系统调用， 即由内核提供的函数。
3 例程， 即库函数，比如标准C库libc。
4 设备， 即/dev目录下的特殊文件。
5 文件格式描述， 例如/etc/passwd。

例如：如果查询read函数
man 2 read

```shell
(1/2): man-pages-3.53-5.el7.noarch.rpm                                 | 5.0 MB  00:00:00     
(2/2): man-pages-zh-CN-1.5.2-4.el7.noarch.rpm                          | 2.3 MB  00:00:00     
----------------------------------------------------------------------------------------------
Total                                                          13 MB/s | 7.3 MB  00:00:00     
Running transaction check
Running transaction test
Transaction test succeeded
Running transaction
  Installing : man-pages-zh-CN-1.5.2-4.el7.noarch                                         1/2 
  Installing : man-pages-3.53-5.el7.noarch                                                2/2 
  Verifying  : man-pages-3.53-5.el7.noarch                                                1/2 
  Verifying  : man-pages-zh-CN-1.5.2-4.el7.noarch                                         2/2
```
