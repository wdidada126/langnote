# shell
`tail -fn 300`
-f 该参数用于监视File文件增长。
-n Number 从 Number 行位置读取指定文件

tail 退出
Ctrl + C

系统命令
cpup
date
dmesg
exec
free
help
hwi
kill
log
memcheck
oom
pmm
reset
sem
stack
su
swtmr
systeminfo
task
uname
vmm
watch

文件命令

cat
cd
chgrp
chmod
chown
cp
format
ls
lsfd
mkdir
mount
partinfo
partition
pwd
rm
rmdir
statfs
sync
touch
writeproc
umount

网络命令
arp
dhclient
dns
ifconfig
ipdebug
netstat
ntpdate
ping
ping6
telnet
tftp

yum list –showduplicates glibc

yum list glibc*



lrzsz

sudo apt-get install lrzse -y



#!/bin/bash`





`#!/usr/bin/env bash`



shell 定义变量 等号左右两边不能有空格

https://blog.csdn.net/qq_20975027/article/details/78343972







`arp -a`

ar



[如何从虚拟机上的linux使用sz命令传输windows大于4G的文件](https://blog.csdn.net/qq_36396104/article/details/82688286)

[crontab 定时任务](https://github.com/me115/linuxtools_rst)

gstack vs pstack

`echo $SHELL`

`mysqladmin flush-hosts -u root -p5Edidada`


poll epoll区别
https://www.cnblogs.com/anker/p/3265058.html

[linux 变量保存脚本执行结果](https://blog.csdn.net/csfreebird/article/details/7978699)

[Linux下的解压命令小结](https://www.cnblogs.com/cursorhu/p/5891699.html)

 timedatectl status
      Local time: Thu 2019-10-17 16:35:30 CST
  Universal time: Thu 2019-10-17 08:35:30 UTC
        RTC time: Thu 2019-10-17 08:46:37
       Time zone: Asia/Shanghai (CST, +0800)
     NTP enabled: no
NTP synchronized: no
 RTC in local TZ: yes
      DST active: n/a

[linux tail命令显示最后n行](https://blog.csdn.net/yuxiangaaaaa/article/details/72869052)

"D:\Program Files\Java\jdk1.8.0_161\bin\java.exe" -agentlib:jdwp=transport=dt_socket,address=127.0.0.1:11547,suspend=y,server=n -XX:TieredStopAtLevel=1 -noverify -Dspring.output.ansi.enabled=always -Dcom.sun.management.jmxremote -Dcom.sun.management.jmxremote.port=11545 -Dcom.sun.management.jmxremote.authenticate=false -Dcom.sun.management.jmxremote.ssl=false -Djava.rmi.server.hostname=localhost -Dspring.liveBeansView.mbeanDomain -Dspring.application.admin.enabled=true -javaagent:C:\Users\edidada\.IntelliJIdea2018.2\system\captureAgent\debugger-agent.jar=file:/C:/Users/edidada/AppData/Local/Temp/capture.props -Dfile.encoding=UTF-8 -classpath "D:\Program Files\Java\jdk1.8.0_161\jre\lib\charsets.jar;D:\Program Files\Java\jdk1.8.0_161\jre\lib\deploy.jar;D:\Program Files\Java\jdk1.8.0_161\jre\lib\ext\access-bridge-64.jar;D:\Program Files\Java\jdk1.8.0_161\jre\lib\ext\cldrdata.jar;D:\Program Files\Java\jdk1.8.0_161\jre\lib\ext\dnsns.jar;D:\Program Files\Java\jdk1.8.0_161\jre\lib\ext\jaccess.jar;D:\Program Files\Java\jdk1.8.0_161\jre\lib\ext\jfxrt.jar;D:\Program Files\Java\jdk1.8.0_161\jre\lib\ext\localedata.jar;D:\Program Files\Java\jdk1.8.0_161\jre\lib\ext\nashorn.jar;D:\Program Files\Java\jdk1.8.0_161\jre\lib\ext\sunec.jar;D:\Program Files\Java\jdk1.8.0_161\jre\lib\ext\sunjce_provider.jar;D:\Program Files\Java\jdk1.8.0_161\jre\lib\ext\sunmscapi.jar;D:\Program Files\Java\jdk1.8.0_161\jre\lib\ext\sunpkcs11.jar;D:\Program Files\Java\jdk1.8.0_161\jre\lib\ext\zipfs.jar;D:\Program Files\Java\jdk1.8.0_161\jre\lib\javaws.jar;D:\Program Files\Java\jdk1.8.0_161\jre\lib\jce.jar;D:\Program Files\Java\jdk1.8.0_161\jre\lib\jfr.jar;D:\Program Files\Java\jdk1.8.0_161\jre\lib\jfxswt.jar;D:\Program Files\Java\jdk1.8.0_161\jre\lib\jsse.jar;D:\Program Files\Java\jdk1.8.0_161\jre\lib\management-agent.jar;D:\Program Files\Java\jdk1.8.0_161\jre\lib\plugin.jar;D:\Program Files\Java\jdk1.8.0_161\jre\lib\resources.jar;D:\Program Files\Java\jdk1.8.0_161\jre\lib\rt.jar;E:\tiancheng\testspringboot_shardingsphere_v2\target\classes;E:\mavenrepository\201810\com\zaxxer\HikariCP\3.2.0\HikariCP-3.2.0.jar;E:\mavenrepository\201810\org\slf4j\slf4j-api\1.7.7\slf4j-api-1.7.7.jar;E:\mavenrepository\201810\commons-dbcp\commons-dbcp\1.4\commons-dbcp-1.4.jar;E:\mavenrepository\201810\org\slf4j\jcl-over-slf4j\1.7.7\jcl-over-slf4j-1.7.7.jar;E:\mavenrepository\201810\ch\qos\logback\logback-classic\1.2.0\logback-classic-1.2.0.jar;E:\mavenrepository\201810\ch\qos\logback\logback-core\1.2.0\logback-core-1.2.0.jar;E:\mavenrepository\201810\org\springframework\boot\spring-boot-starter-jdbc\2.1.3.RELEASE\spring-boot-starter-jdbc-2.1.3.RELEASE.jar;E:\mavenrepository\201810\org\springframework\boot\spring-boot-starter\1.5.19.RELEASE\spring-boot-starter-1.5.19.RELEASE.jar;E:\mavenrepository\201810\org\springframework\boot\spring-boot\1.5.19.RELEASE\spring-boot-1.5.19.RELEASE.jar;E:\mavenrepository\201810\org\springframework\boot\spring-boot-autoconfigure\1.5.19.RELEASE\spring-boot-autoconfigure-1.5.19.RELEASE.jar;E:\mavenrepository\201810\org\springframework\boot\spring-boot-starter-logging\1.5.19.RELEASE\spring-boot-starter-logging-1.5.19.RELEASE.jar;E:\mavenrepository\201810\org\slf4j\jul-to-slf4j\1.7.7\jul-to-slf4j-1.7.7.jar;E:\mavenrepository\201810\org\slf4j\log4j-over-slf4j\1.7.7\log4j-over-slf4j-1.7.7.jar;E:\mavenrepository\201810\org\yaml\snakeyaml\1.17\snakeyaml-1.17.jar;E:\mavenrepository\201810\org\springframework\spring-jdbc\4.3.22.RELEASE\spring-jdbc-4.3.22.RELEASE.jar;E:\mavenrepository\201810\org\springframework\spring-beans\4.3.22.RELEASE\spring-beans-4.3.22.RELEASE.jar;E:\mavenrepository\201810\org\springframework\spring-tx\4.3.22.RELEASE\spring-tx-4.3.22.RELEASE.jar;E:\mavenrepository\201810\org\springframework\spring-core\4.3.6.RELEASE\spring-core-4.3.6.RELEASE.jar;E:\mavenrepository\201810\commons-pool\commons-pool\1.6\commons-pool-1.6.jar;E:\mavenrepository\201810\org\mybatis\spring\boot\mybatis-spring-boot-starter\2.0.0\mybatis-spring-boot-starter-2.0.0.jar;E:\mavenrepository\201810\org\mybatis\spring\boot\mybatis-spring-boot-autoconfigure\2.0.0\mybatis-spring-boot-autoconfigure-2.0.0.jar;E:\mavenrepository\201810\org\mybatis\mybatis\3.5.0\mybatis-3.5.0.jar;E:\mavenrepository\201810\org\mybatis\mybatis-spring\2.0.0\mybatis-spring-2.0.0.jar;E:\mavenrepository\201810\com\google\guava\guava\18.0\guava-18.0.jar;E:\mavenrepository\201810\org\codehaus\groovy\groovy\2.4.16\groovy-2.4.16.jar;E:\mavenrepository\201810\mysql\mysql-connector-java\5.1.42\mysql-connector-java-5.1.42.jar;E:\mavenrepository\201810\io\shardingsphere\sharding-jdbc-orchestration-spring-boot-starter\3.0.0-beta\sharding-jdbc-orchestration-spring-boot-starter-3.0.0-beta.jar;E:\mavenrepository\201810\io\shardingsphere\sharding-jdbc-orchestration\3.0.0-beta\sharding-jdbc-orchestration-3.0.0-beta.jar;E:\mavenrepository\201810\io\shardingsphere\sharding-jdbc-core\3.0.0-beta\sharding-jdbc-core-3.0.0-beta.jar;E:\mavenrepository\201810\io\shardingsphere\sharding-orchestration-core\3.0.0-beta\sharding-orchestration-core-3.0.0-beta.jar;E:\mavenrepository\201810\io\shardingsphere\sharding-core\3.0.0-beta\sharding-core-3.0.0-beta.jar;E:\mavenrepository\201810\org\codehaus\groovy\groovy\2.4.5\groovy-2.4.5-indy.jar;E:\mavenrepository\201810\io\shardingsphere\sharding-orchestration-reg-zookeeper-curator\3.0.0-beta\sharding-orchestration-reg-zookeeper-curator-3.0.0-beta.jar;E:\mavenrepository\201810\io\shardingsphere\sharding-orchestration-reg-api\3.0.0-beta\sharding-orchestration-reg-api-3.0.0-beta.jar;E:\mavenrepository\201810\org\apache\curator\curator-framework\2.10.0\curator-framework-2.10.0.jar;E:\mavenrepository\201810\org\apache\curator\curator-client\2.10.0\curator-client-2.10.0.jar;E:\mavenrepository\201810\org\apache\zookeeper\zookeeper\3.4.6\zookeeper-3.4.6.jar;E:\mavenrepository\201810\log4j\log4j\1.2.16\log4j-1.2.16.jar;E:\mavenrepository\201810\jline\jline\0.9.94\jline-0.9.94.jar;E:\mavenrepository\201810\org\apache\curator\curator-recipes\2.10.0\curator-recipes-2.10.0.jar;E:\mavenrepository\201810\io\shardingsphere\mybatis-repository\3.0.0\mybatis-repository-3.0.0.jar;E:\mavenrepository\201810\io\shardingsphere\repository-api\3.0.0\repository-api-3.0.0.jar;E:\mavenrepository\201810\org\springframework\spring-orm\4.3.22.RELEASE\spring-orm-4.3.22.RELEASE.jar;E:\mavenrepository\201810\org\springframework\spring-context-support\4.3.22.RELEASE\spring-context-support-4.3.22.RELEASE.jar;E:\mavenrepository\201810\org\springframework\spring-context\4.3.22.RELEASE\spring-context-4.3.22.RELEASE.jar;E:\mavenrepository\201810\org\springframework\spring-aop\4.3.22.RELEASE\spring-aop-4.3.22.RELEASE.jar;E:\mavenrepository\201810\org\springframework\spring-expression\4.3.22.RELEASE\spring-expression-4.3.22.RELEASE.jar;C:\Program Files\JetBrains\IntelliJ IDEA 2018.2.4\lib\idea_rt.jar" io.shardingsphere.example.spring.boot.mybatis.orche.SpringBootStarterExample


```shell

grep 'A.*B' file_name.txt

```

搜索含有A和B的字符串


less :G 跳转到文件末尾


cat  缩写concatenate  cat命令可以用来显示、合并文件。


etc  初期etc的英文名字缩写为etcetera ，后来大家更习惯称为 Editable Text Configuration。ETC为系统配置文件目录，该目录包含系统启动脚本、启动配置文件、用户登陆配置文件、网络配置文件、httpd 配置文件、IPSec 配置文件和其他文件等。

### BASE64
常用方式
格式：base64
从标准输入中读取数据，按Ctrl+D结束输入。将输入的内容编码为base64字符串输出。
格式：echo "str" | base64
将字符串str+换行 编码为base64字符串输出。

格式：echo -n "str" | base64
将字符串str编码为base64字符串输出。注意与上面的差别。（2011.08.01 补充）

格式：base64 file
从指定的文件file中读取数据，编码为base64字符串输出。

格式：base64 -d
从标准输入中读取已经进行base64编码的内容，解码输出。

格式：base64 -d -i
从标准输入中读取已经进行base64编码的内容，解码输出。加上-i参数，忽略非字母表字符，比如换行符。





time



tar负责打包，gzip负责压缩

tar
-c: 建立压缩档案
-x：解压
-t：查看内容
-r：向压缩归档文件末尾追加文件
-u：更新原压缩包中的文件

这五个是独立的命令，压缩解压都要用到其中一个，可以和别的命令连用但只能用其中一个。下面的参数是根据需要在压缩或解压档案时可选的。

-z：有gzip属性的
-j：有bz2属性的
-Z：有compress属性的
-v：显示所有过程
-O：将文件解开到标准输出

下面的参数-f是必须的

-f: 使用档案名字，切记，这个参数是最后一个参数，后面只能接档案名。

# tar -cf all.tar *.jpg

这条命令是将所有.jpg的文件打成一个名为all.tar的包。-c是表示产生新的包，-f指定包的文件名。

# tar -rf all.tar *.gif

这条命令是将所有.gif的文件增加到all.tar的包里面去。-r是表示增加文件的意思。

# tar -uf all.tar logo.gif

这条命令是更新原来tar包all.tar中logo.gif文件，-u是表示更新文件的意思。

# tar -tf all.tar

这条命令是列出all.tar包中所有文件，-t是列出文件的意思

# tar -xf all.tar

这条命令是解出all.tar包中所有文件，-x是解开的意思

压缩
tar –cvf jpg.tar *.jpg //将目录里所有jpg文件打包成tar.jpg
tar –czf jpg.tar.gz *.jpg //将目录里所有jpg文件打包成jpg.tar后，并且将其用gzip压缩，生成一个gzip压缩过的包，命名为jpg.tar.gz
tar –cjf jpg.tar.bz2 *.jpg //将目录里所有jpg文件打包成jpg.tar后，并且将其用bzip2压缩，生成一个bzip2压缩过的包，命名为jpg.tar.bz2
tar –cZf jpg.tar.Z *.jpg //将目录里所有jpg文件打包成jpg.tar后，并且将其用compress压缩，生成一个umcompress压缩过的包，命名为jpg.tar.Z
rar a jpg.rar *.jpg //rar格式的压缩，需要先下载rar for linux
zip jpg.zip *.jpg //zip格式的压缩，需要先下载zip for linux

解压
tar –xvf file.tar //解压 tar包
tar -xzvf file.tar.gz //解压tar.gz
tar -xjvf file.tar.bz2 //解压 tar.bz2
tar –xZvf file.tar.Z //解压tar.Z
unrar e file.rar //解压rar
unzip file.zip //解压zip

总结
1、*.tar 用 tar –xvf 解压
2、*.gz 用 gzip -d或者gunzip 解压
3、*.tar.gz和*.tgz 用 tar –xzf 解压
4、*.bz2 用 bzip2 -d或者用bunzip2 解压
5、*.tar.bz2用tar –xjf 解压
6、*.Z 用 uncompress 解压
7、*.tar.Z 用tar –xZf 解压
8、*.rar 用 unrar e解压
9、*.zip 用 unzip 解压

https://www.cnblogs.com/jingzaixin/p/11495667.html