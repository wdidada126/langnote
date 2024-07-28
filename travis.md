# travis

## 例子

https://github.com/qicosmos/rest_rpc/tree/master/

## d
travis 安装jetty 阻塞的 重启一个shell脚本

travis使用gcp lnux平台

windows macos平台使用的是其他


- .com
- .org


两个网站

maven仓库有问题？

解决方案：

core os

[travis db](https://docs.travis-ci.com/user/database-setup/#rabbitmq)

```shell
service:
  - mysql
before_install:	# 注意需要先创建一个与你程序运行所需要的数据库名
  - mysql -e 'create database yourDB;'

services:
  - redis-server
```

[travis mysql 带客户端工具](https://blog.csdn.net/h12590400327/article/details/80871536)

ubuntu 14 16 18

mac

windows

支持Rust

```shell
branches:
    only:
        - master
```

https://scan.coverity.com/projects/edidada-rest_description?tab=project_settings

https://ci.appveyor.com/projects/new

[AppVeyor-CI为GitHub项目做自动化集成（dotnet为主）](https://www.cnblogs.com/EasonJim/p/6020226.html)

https://www.appveyor.com/docs/build-configuration/


java maven项目，下载不了jar包

解决方式：在项目中带上jar包

切换maven mirror源头

[gcp maven 设置](Downloading from google-maven-central: https://maven-central.storage-download.googleapis.com/maven2/org/apache/maven/reporting/maven-reporting-api/2.0.6/maven-reporting-api-2.0.6.pom)


Coverity代码静态安全检测

https://blog.csdn.net/yasi_xi/article/details/8349985

travis db

支持mysql h2 sqlite redis

mysql内置哪些数据库，还是要手动新建数据库？



### 5.2 加密信息

如果不放心保密信息明文存在 Travis 的网站，可以使用 Travis 提供的加密功能。

首先，安装 Ruby 的包`travis`。

https://blog.csdn.net/duzilonglove/article/details/79012499

travis mysql 不能存汉字

GitHub testodbaccess

https://blog.csdn.net/xiaoxd16/article/details/83150027



travis设置将RF测试结果上传到FTP

https://blog.csdn.net/shuizhongmose/article/details/90023708

[travis mysql数据库创建用户错误](https://www.jb51.cc/mysql/433525.html)

http://www.ruanyifeng.com/blog/2017/12/travis_ci_tutorial.html

oraclejdk11

#####  切换成之前的构建环境（`Ubuntu Trusty 14.04`版本）

```
language: java
dist: trusty
sudo: false
jdk:
  - oraclejdk8
```
