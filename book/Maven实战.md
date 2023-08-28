# Maven实战

https://book.douban.com/subject/5345682/

Chap. 17. 编写 Maven 插件


idea整合maven

mvn命令行

mvn gradle区别

mvn插件

mvn环境变量

archtype编写





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
## 1. Maven简介

## Chap. 2 Maven安装

'mvn help:system'


## Chap. 3 Hello World

mvn

pom.xml

compile test package install
resource
等步骤

## Chap. 4 背景案例

项目简介

## Chap. 5 坐标和依赖

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



## Chap. 6 仓库

maven仓库
deploy

快照版本
开发时用

## Chap. 7 生命周期和插件

LifeCycle
goal

clean default site三个生命周期

parent module不一定要是父文件夹

## Chap. 8 聚合与继承

maven聚合 继承

超级pom 是一个文件
有很多自定义的配置

Reactor maven反应堆

maven cargo
maven cafgo:deploy
9. 使用 Nexus 创建私服
10. 使用 Maven 进行测试
11. 使用 Hudson 进行持续集成
12. 构建 Web 应用
13. 版本管理

## Chap. 14 多profile

maven 命令行激活配置
-Psomename
问题：profile怎么引用？


## Chap. 15. 生成项目站点


Maven生成项目站点 javadoc checkstyle项目报告
16. m2eclipse

## Chap. 17
maven plugin编写

可以参考常用的maven plugin
https://github.com/spotify/dockerfile-maven

## Chap. 18 Archetype

archtype编写


