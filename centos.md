# centos

centos 8
dnf命令行

rpm -q centos-release
centos-release-6-10.el6.centos.12.3.x86_6'
centos-release-7-8.2003.0.el7.centos.x86_64

查看CentOS版本方法
https://www.cnblogs.com/mafeng/p/10689847.html


rpm -q centos-release


lsb_release -a



PATH=$PATH:/usr/apache-maven-3.6.3/bin
export PATH

PATH=$PATH:/usr/apache-maven-3.6.3/bin
export PATH

yum install tcpdump -y
yum install lsof -y
yum install lrzsz -y
yum install wget -y

curl https://setup.ius.io | sh

yum search git

yum -y install centos-release-scl
yum -y install devtoolset-7-gcc devtoolset-7-gcc-c++ devtoolset-7-binutils devtoolset-7-gdb devtoolset-7-build git222
scl enable devtoolset-7 bash

devtoolset-7-build

yum install tcpdump git222 lsof lrzsz wget centos-release-scl -y

```
Dependencies Resolved

===================================================================================================================================
 Package                                Arch                   Version                               Repository               Size
===================================================================================================================================
Installing:
 centos-release-scl                     noarch                 2-3.el7.centos                        extras                   12 k
 git222                                 x86_64                 2.22.4-1.el7.ius                      ius                     134 k
 lrzsz                                  x86_64                 0.12.20-36.el7                        base                     78 k
 lsof                                   x86_64                 4.87-6.el7                            base                    331 k
 tcpdump                                x86_64                 14:4.9.2-4.el7_7.1                    base                    422 k
 wget                                   x86_64                 1.14-18.el7_6.1                       base                    547 k
Installing for dependencies:
 centos-release-scl-rh                  noarch                 2-3.el7.centos                        extras                   12 k
 emacs-filesystem                       noarch                 1:24.3-23.el7                         base                     58 k
 git222-core                            x86_64                 2.22.4-1.el7.ius                      ius                     4.9 M
 git222-core-doc                        noarch                 2.22.4-1.el7.ius                      ius                     2.4 M
 git222-perl-Git                        noarch                 2.22.4-1.el7.ius                      ius                      46 k
 libpcap                                x86_64                 14:1.5.3-12.el7                       base                    139 k
 libsecret                              x86_64                 0.18.6-1.el7                          base                    153 k
 pcre2                                  x86_64                 10.23-2.el7                           base                    201 k
 perl                                   x86_64                 4:5.16.3-299.el7_9                    updates                 8.0 M
 perl-Carp                              noarch                 1.26-244.el7                          base                     19 k
 perl-Encode                            x86_64                 2.51-7.el7                            base                    1.5 M
 perl-Error                             noarch                 1:0.17020-2.el7                       base                     32 k
 perl-Exporter                          noarch                 5.68-3.el7                            base                     28 k
 perl-File-Path                         noarch                 2.09-2.el7                            base                     26 k
 perl-File-Temp                         noarch                 0.23.01-3.el7                         base                     56 k
 perl-Filter                            x86_64                 1.49-3.el7                            base                     76 k
 perl-Getopt-Long                       noarch                 2.40-3.el7                            base                     56 k
 perl-HTTP-Tiny                         noarch                 0.033-3.el7                           base                     38 k
 perl-PathTools                         x86_64                 3.40-5.el7                            base                     82 k
 perl-Pod-Escapes                       noarch                 1:1.04-299.el7_9                      updates                  52 k
 perl-Pod-Perldoc                       noarch                 3.20-4.el7                            base                     87 k
 perl-Pod-Simple                        noarch                 1:3.28-4.el7                          base                    216 k
 perl-Pod-Usage                         noarch                 1.63-3.el7                            base                     27 k
 perl-Scalar-List-Utils                 x86_64                 1.27-248.el7                          base                     36 k
 perl-Socket                            x86_64                 2.010-5.el7                           base                     49 k
 perl-Storable                          x86_64                 2.45-3.el7                            base                     77 k
 perl-TermReadKey                       x86_64                 2.30-20.el7                           base                     31 k
 perl-Text-ParseWords                   noarch                 3.29-4.el7                            base                     14 k
 perl-Time-HiRes                        x86_64                 4:1.9725-3.el7                        base                     45 k
 perl-Time-Local                        noarch                 1.2300-2.el7                          base                     24 k
 perl-constant                          noarch                 1.27-2.el7                            base                     19 k
 perl-libs                              x86_64                 4:5.16.3-299.el7_9                    updates                 690 k
 perl-macros                            x86_64                 4:5.16.3-299.el7_9                    updates                  44 k
 perl-parent                            noarch                 1:0.225-244.el7                       base                     12 k
 perl-podlators                         noarch                 2.5.1-3.el7                           base                    112 k
 perl-threads                           x86_64                 1.87-4.el7                            base                     49 k
 perl-threads-shared                    x86_64                 1.43-6.el7                            base                     39 k
```


https://www.cnblogs.com/network-ren/p/12448929.html

yum -y install https://download.postgresql.org/pub/repos/yum/reporpms/EL-7-x86_64/pgdg-redhat-repo-latest.noarch.rpm

yum -y install postgresql10 postgresql10-server

```
[root@leryltdllllwew9a ~]# grep 'temporary password' /var/log/mysqld.log
2021-03-04T07:45:21.664807Z 1 [Note] A temporary password is generated for root@localhost: -&e2x-rp7o?J
[root@leryltdllllwew9a ~]# mysql -uroot -p
Enter password: 
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 2
Server version: 5.7.33

Copyright (c) 2000, 2021, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> show databases;
ERROR 1820 (HY000): You must reset your password using ALTER USER statement before executing this statement.
```

`alter user 'root'@'localhost' identified by '5%Edidadas';`





https://blog.csdn.net/memory6364/article/details/82426052



接触mysql对于root账户的IP访问限制



```
grant all on . to ‘root@%’ identified by ‘5%Edidadas’;
flush privileges;
```

GRANT ALL PRIVILEGES ON *.* TO ‘root@%’ identified by ‘5%Edidadas’;



不对

`alter user 'root'@'%' identified by '5%Edidadas';`





grant all privileges on \*.* to root@'%' identified by ‘5%Edidadas’