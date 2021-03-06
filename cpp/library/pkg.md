# pkg

freebsd
termux Andriod

pkg查看安装的包在电脑上都有哪些文件

pkg install jsoncpp -y

```shell
yum install jsoncpp-devel -y
Loaded plugins: fastestmirror, langpacks
Repository epel is listed more than once in the configuration
Loading mirror speeds from cached hostfile
 * centos-sclo-rh: mirrors.aliyun.com
 * centos-sclo-sclo: mirrors.ustc.edu.cn
 * remi-safe: mirrors.tuna.tsinghua.edu.cn
centos-sclo-rh                                                         | 3.0 kB  00:00:00     
centos-sclo-sclo                                                       | 3.0 kB  00:00:00     
copr:copr.fedorainfracloud.org:carlwgeorge:ripgrep                     | 3.3 kB  00:00:00     
docker-ce-stable                                                       | 3.5 kB  00:00:00     
epel                                                                   | 4.7 kB  00:00:00     
extras                                                                 | 2.9 kB  00:00:00     
ius                                                                    | 1.3 kB  00:00:00     
kubernetes                                                             | 2.9 kB  00:00:00     
mysql-connectors-community                                             | 2.6 kB  00:00:03     
mysql-tools-community                                                  | 2.6 kB  00:00:03     
mysql57-community                                                      | 2.6 kB  00:00:00     
os                                                                     | 3.6 kB  00:00:00     
pgdg-common                                                            | 2.9 kB  00:00:00     
pgdg10                                                                 | 3.6 kB  00:00:00     
pgdg11                                                                 | 3.6 kB  00:00:00     
pgdg12                                                                 | 3.6 kB  00:00:00     
pgdg95                                                                 | 3.6 kB  00:00:00     
pgdg96                                                                 | 3.6 kB  00:00:00     
remi-safe                                                              | 3.0 kB  00:00:00     
updates                                                                | 2.9 kB  00:00:00     
wandisco-git                                                           | 2.9 kB  00:00:00     
(1/4): kubernetes/x86_64/primary_db                                    | 164 kB  00:00:07     
(2/4): pgdg12/7/x86_64/primary_db                                      | 182 kB  00:00:14     
(3/4): remi-safe/primary_db                                            | 1.9 MB  00:00:17     
(4/4): pgdg11/7/x86_64/primary_db                                      | 320 kB  00:00:31     
Resolving Dependencies
--> Running transaction check
---> Package jsoncpp-devel.x86_64 0:0.10.5-2.el7 will be installed
--> Processing Dependency: jsoncpp(x86-64) = 0.10.5-2.el7 for package: jsoncpp-devel-0.10.5-2.el7.x86_64
--> Processing Dependency: libjsoncpp.so.0()(64bit) for package: jsoncpp-devel-0.10.5-2.el7.x86_64
--> Running transaction check
---> Package jsoncpp.x86_64 0:0.10.5-2.el7 will be installed
--> Finished Dependency Resolution

Dependencies Resolved

==============================================================================================
 Package                   Arch               Version                  Repository        Size
==============================================================================================
Installing:
 jsoncpp-devel             x86_64             0.10.5-2.el7             epel              25 k
Installing for dependencies:
 jsoncpp                   x86_64             0.10.5-2.el7             epel              82 k

Transaction Summary
==============================================================================================
Install  1 Package (+1 Dependent package)

Total download size: 107 k
Installed size: 301 k
Downloading packages:
(1/2): jsoncpp-devel-0.10.5-2.el7.x86_64.rpm                           |  25 kB  00:00:00     
(2/2): jsoncpp-0.10.5-2.el7.x86_64.rpm                                 |  82 kB  00:00:00     
----------------------------------------------------------------------------------------------
Total                                                         743 kB/s | 107 kB  00:00:00     
Running transaction check
Running transaction test
Transaction test succeeded
Running transaction
  Installing : jsoncpp-0.10.5-2.el7.x86_64                                                1/2 
  Installing : jsoncpp-devel-0.10.5-2.el7.x86_64                                          2/2 
  Verifying  : jsoncpp-devel-0.10.5-2.el7.x86_64                                          1/2 
  Verifying  : jsoncpp-0.10.5-2.el7.x86_64                                                2/2 

Installed:
  jsoncpp-devel.x86_64 0:0.10.5-2.el7                                                         

Dependency Installed:
  jsoncpp.x86_64 0:0.10.5-2.el7
```

```shell
pkg list jsoncpp
/usr/local/include/json/allocator.h
/usr/local/include/json/assertions.h
/usr/local/include/json/config.h
/usr/local/include/json/forwards.h
/usr/local/include/json/json.h
/usr/local/include/json/json_features.h
/usr/local/include/json/reader.h
/usr/local/include/json/value.h
/usr/local/include/json/version.h
/usr/local/include/json/writer.h
/usr/local/lib/libjsoncpp.a
/usr/local/lib/libjsoncpp.so
/usr/local/lib/libjsoncpp.so.24
/usr/local/libdata/pkgconfig/jsoncpp.pc
/usr/local/share/licenses/jsoncpp-1.9.4/LICENSE
/usr/local/share/licenses/jsoncpp-1.9.4/MIT
/usr/local/share/licenses/jsoncpp-1.9.4/catalog.mk
```


https://blog.csdn.net/wilson1068/article/details/88756168

pkg-config 查询已安装库的相关信息
https://blog.csdn.net/wilson1068/article/details/88756168