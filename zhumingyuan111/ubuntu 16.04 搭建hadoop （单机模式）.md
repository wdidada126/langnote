---
title: ubuntu 16.04 搭建hadoop （单机模式）
date: 2016-11-13 16:16:25
tags: CSDN迁移
---
  ## ubuntu 16.04 搭建hadoop （单机模式）

 本文环境是：Ubuntu16.04LTS+Java 1.8.0_111+Hadoop 2.7.3

 
### 一、下载和安装Java

 
##### 1）下载：Java在官网下载就好，我下载的是jdk-8u111-linux-x64.tar.gz;

 
##### 2）解压：tar -zxvf jdk-8u111-linux-x64.tar.gz -C /usr/lib/jvm

 
##### 3) 配置java环境变量，以下代码放入～/.bashrc 文件的末尾。

 
```
export JAVA_HOME=/usr/lib/jvm/jdk1.8.0_111
export JRE_HOME=${JAVA_HOME}/jre
export CLASSPATH=.:${JAVA_HOME}/lib:${JRE_HOME}/lib
export PATH=${JAVA_HOME}/bin:$PATH
```
 
##### 4）刷新配置： source ~/.bashrc

 
##### 5) Java 安装验证 ： java -version

 ![java版本](https://img-blog.csdn.net/20161113160149891)

 
### 二、 安装SSH

 
##### 1）查看SSH安装情况

 
```
rpm -qa | grep ssh
```
 如果SSH之前没有安装，则下面进行安装

 
```
sudo apt-get install openssh-server
```
 启动SSH

 
```
sudo /etc/init.d/ssh start
```
 查看SSH运行情况

 
```
ps -ef  | grep ssh
```
 生成并导入SSH密钥，避免重复输入密码

 
```
ssh -keygen -t dsa -P '' -f ~/.ssh/id_dsa
cat ~/.ssh/id_dsa.pub >> ~/.ssh/authorized_keys
```
 登录

 
```
ssh localhost
```
 
### 三、安装和配置Hadoop

 
##### 1) 下载Hadoop : hadoop2.7.3.tar.gz

 
##### 2) 解压

 
```
tar -zxvf hadoop-2.7.3 -C /usr/local/
重命名 
mv hadoop-2.7.3 hadoop
```
 
##### 3)查看Hadoop 版本

 
```
cd /usr/local/hadoop
./bin/hadoop version
```
 
##### 4) 运行例子

 在 /usr/local/hadoop 下新建input 文件夹，将README.txt 拷贝到input下面。运行下面代码：

 
```
hadoop jar share/hadoop/mapreduce/sources/hadoop-mapreduce-examples-2.7.3-sources.jar org.apache.hadoop.examples.WordCount input output
```
 查看运行结果：

 
```
cat output/*
```
 
### 注意：

 
> 1.如果第二次运行上面的例子，需要把output文件删除;   
>  2.执行命令过过程中可能会遇到权限问题;最好建立hadoop用户，并把hadoop文件夹及子文件交给hadoop用户,运行下面代码！
> 
>  
 
```
sudo chown -R hadoop /usr/local/hadoop
```
   
  