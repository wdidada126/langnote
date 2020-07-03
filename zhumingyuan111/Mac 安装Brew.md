---
title: Mac 安装Brew
date: 2018-06-16 10:56:56
tags: CSDN迁移
---
  # 安装rvm

 rvm是一个便捷的多版本ruby环境的管理和切换工具 官网：[https://rvm.io/](https://rvm.io/)

 参考：   
 [https://www.jianshu.com/p/c073e6fc01f5](https://www.jianshu.com/p/c073e6fc01f5)

 [https://stackoverflow.com/questions/15701058/error-installing-rvm-ruby-version-manager](https://stackoverflow.com/questions/15701058/error-installing-rvm-ruby-version-manager)

 rvm 安装的命令很简单，如下：

 
```
$ curl -sSL https://get.rvm.io | bash -s stable
rvm get stable
```
 但是由于网络的原因我在操作的时候总是报：“Failed to connect to get.rvm.io port 443: Network is unreachable” 错误，这时候可以参考：   
 [https://stackoverflow.com/questions/15701058/error-installing-rvm-ruby-version-manager](https://stackoverflow.com/questions/15701058/error-installing-rvm-ruby-version-manager)   
 这里给出了解决办法，就是采用在浏览器访问，然后将文本下载保存后，将文件设置为可执行的文件，并执行，具体可以参见上面的链接。

 
# 安装Ruby

 
```
rvm list //列出ruby版本
rvm use 2.1.1  //确定你要使用的版本
ruby -v   //显示ruby版本，正常显示就说明ruby 已经安装好了。
```
 
# 安装Brew

 
```
ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```
 到这里brew 就安装好了。

   
  