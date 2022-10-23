# openssl



https://www.jianshu.com/p/fad5276a70e0


centos 7.6，升级过程中估计会有如下报错，


Can’t locate IPC/Cmd.pm in @INC 
……
Can't locate Data/Dumper.pm in @INC 
……
Can't locate Test/More.pm in @INC 
……




安装必备包：
yum install perl-IPC-Cmd perl-Data-Dumper perl-Test-Taint
