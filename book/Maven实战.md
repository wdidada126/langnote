# Maven实战

https://book.douban.com/subject/5345682/



注意超级POM
自定义的变量
profile
多jar依赖

jar包依赖冲突

Nexus私服Java配置	
-Xms2703M
-Xmx2703M
-XX:MaxDirectMemorySize=2703M



Chap 1 2 3 是简介

4是项目介绍

## Chap. 2

'mvn help:system'


## Chap. 3

mvn

pom.xml

compile test package install
resource
等步骤

## Chap. 4

项目简介

Chap. 5

maven 5元素
groupid
artificate
version
package
classifier

depedency:tree
depedency:list

依赖范围
传递性依赖
可选依赖

classifier 应用
testng依赖jdk4
依赖jdk5的版本



## Chap. 6

maven仓库
deploy

快照版本
开发时用

## Chap. 7

LifeCycle
goal

clean default site三个生命周期

parent module不一定要是父文件夹

## Chap. 8

maven聚合 继承

超级pom 是一个文件
有很多自定义的配置

Reactor maven反应堆

maven cargo
maven cafgo:deploy

## Chap. 14 多profile

maven 命令行激活配置
-Psomename
问题：profile怎么引用？


## Chap. 15

Maven生成项目站点 javadoc checkstyle项目报告

## Chap. 17
maven plugin编写

可以参考常用的maven plugin
https://github.com/spotify/dockerfile-maven

## Chap. 18
archtype编写


