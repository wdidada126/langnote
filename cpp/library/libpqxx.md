# libpqxx

源代码见
https://github.com/edidada/cpptestlibpqxx/actions

postgressql c++官方库
http://pqxx.org/development/libpqxx/

sudo yum install libpqxx libpqxx-devel -y
libpqxx.x86_64 1:5.0.1-2.rhel7.1
libpqxx-5.0.1-2.rhel7.1.x86_64
通过yum install libpqxx安装成功，c++源文件引用<pqxx/pqxx>竟然没有生效，提示pqxx/pqxx: No such file or directory

https://blog.csdn.net/xinpo66/article/details/18703049

sudo yum install postgresql10-devel -y
https://www.postgresql.org/download/linux/redhat/


```shell script
/root/grpcauthservice/cmake-build-debug/test/main_pg
FATAL:  Ident authentication failed for user "postgres"
```

https://blog.csdn.net/wang1144/article/details/8986479

```shell script
/root/grpcauthservice/test/pg_brief.cpp:20:27: error: conversion from ‘pqxx::result’ to non-scalar type ‘pqxx::row’ requested
     pqxx::row r = txn.exec(
                   ~~~~~~~~^
             "SELECT id "
             ~~~~~~~~~~~~   
             "FROM user_tbl "
             ~~~~~~~~~~~~~~~~
             "WHERE name =" + txn.quote(argv[1]));

```


2、安装devtoolset-8(使用高版本gcc (GCC) 8.3.1 20190311
yum install centos-release-scl -y
yum install devtoolset-8 -y
启用devtoolset-8
#scl enable devtoolset-8 -- bash
#source /opt/rh/devtoolset-8/enable


