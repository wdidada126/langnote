---
title: Thrift安装（ubuntu16.04+thrift0.10.0）
date: 2017-04-16 15:46:19
tags: CSDN迁移
---
  今天再一次安装终于成功了，还有一些东西不太会使用，后续在学习，先把安装过程整理以下！

  
  * 下载thrift [http://thrift.apache.org/download/](http://thrift.apache.org/download/),我的版本是thrift-0.10.0.tar.gz 
  * 安装boost库   
     sudo apt-get install libboost-dev libboost-dbg libboost-doc bcp libboost-*
    
     
  * 安装其他相关工具包   
     sudo apt-get install libboost-dev libboost-test-dev libboost-program-options-dev libevent-dev automake libtool flex bison pkg-config g++ libssl-dev ant   
     (我之前安装了JDK，如果没有安装jdk，则还需要安装并配置java环境变量，我的版本是1.8)
    
     
  * 解压文件，进入目录thrift-0.10.0安装,我放置的目录是/usr/local/thrift-0.10.0/ 
  * ./configure –with-cpp –with-boost –without-python –without-csharp –with-java –without-erlang –without-perl –with-php –without-php_extension –without-ruby –without-haskell –without-go   
     make   
     sudo make install (执行这个命令的时候总是报“没有设置jdk的错误”)，图片如下：   
     ![这里写图片描述](https://img-blog.csdn.net/20170416153100961?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvemh1bWluZ3l1YW4xMTE=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)   
     后来干脆用root用户执行，make install 命令，则执行成功，后来有查看了～/.bashrc 和/etc/profile 两个文件发现并没有什么区别，唉。。。这个问题还需要大神帮忙一起探讨。
    
     
  * 测试例子   
     进入tutorial文件夹，shared.thrift和tutorial.thrift是接口定义文件。   
     thrift -r –gen java tutorial.thrift、   
     执行这条命令可以生成gen-java文件夹，文夹中是自动生成的代码。
    
     注意： 运行命令可能出现错误   
     thrift: error while loading shared libraries: libthriftc.so.0: cannot open shared object file: No such file or directory
    
      此时需要将libthriftc 配置环境变量中，如下：   
 export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib/

 /usr/local/lib/ 就是 libthriftc.so.0 所在的路径。   
 安装基本完成！   
 后面我在ant 构建的时候并没有生成   
 JavaServer   
 JavaClient 这两个可执行文夹，只是生成了tutorial.jar 包，有可能是build.xml文件写的有问题，欢迎大神们指点说明！

   
  