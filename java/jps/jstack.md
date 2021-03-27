# jstack

-Djava.awt.headless=true -Djava.net.preferIPv4Stack=true -server -Xmx2g -Xms2g -Dfastjson.parser.safeMode=true -XX:+DisableExplicitGC -XX:+UseConcMarkSweepGC -XX:+CMSParallelRemarkEnabled -XX:+UseCMSCompactAtFullCollection -XX:LargePageSizeInBytes=128m -XX:+UseFastAccessorMethods -XX:+UseCMSInitiatingOccupancyOnly -XX:CMSInitiatingOccupancyFraction=70

#### jstack(查看线程)、jmap(查看内存)和jstat(性能分析) jconsole

jinfo

```java
[root@10-23-29-39 ~]# jinfo 23427
Attaching to process ID 23427, please wait...
Debugger attached successfully.
Server compiler detected.
JVM version is 25.282-b08
Java System Properties:

ofbiz.home = /root/apache-ofbiz-17.12.05
java.runtime.name = OpenJDK Runtime Environment
solr.log.level = INFO
java.vm.version = 25.282-b08
sun.boot.library.path = /usr/lib/jvm/java-1.8.0-openjdk-1.8.0.282.b08-1.el7_9.x86_64/jre/lib/amd64
java.vendor.url = https://www.redhat.com/
java.vm.vendor = Red Hat, Inc.
solr/home = /plugins/solr/home
path.separator = :
file.encoding.pkg = sun.io
java.vm.name = OpenJDK 64-Bit Server VM
sun.os.patch.level = unknown
sun.java.launcher = SUN_STANDARD
user.country = US
user.dir = /root/apache-ofbiz-17.12.05
java.vm.specification.name = Java Virtual Machine Specification
java.runtime.version = 1.8.0_282-b08
solr.log.dir = runtime/logs/solr
java.awt.graphicsenv = sun.awt.X11GraphicsEnvironment
derby.system.home = runtime/data/derby
os.arch = amd64
java.endorsed.dirs = /usr/lib/jvm/java-1.8.0-openjdk-1.8.0.282.b08-1.el7_9.x86_64/jre/lib/endorsed
line.separator = 

java.io.tmpdir = /tmp
java.vm.specification.vendor = Oracle Corporation
os.name = Linux
sun.jnu.encoding = UTF-8
jetty.git.hash = 363d5f2df3a8a28de40604320230664b9c793c16
java.library.path = /opt/rh/devtoolset-7/root/usr/lib64:/opt/rh/devtoolset-7/root/usr/lib:/opt/rh/devtoolset-7/root/usr/lib64/dyninst:/opt/rh/devtoolset-7/root/usr/lib/dyninst:/opt/rh/devtoolset-7/root/usr/lib64:/opt/rh/devtoolset-7/root/usr/lib:/usr/java/packages/lib/amd64:/usr/lib64:/lib64:/lib:/usr/lib
java.specification.name = Java Platform API Specification
java.class.version = 52.0
birt.viewer.working.path = /root/apache-ofbiz-17.12.05/runtime/tempfiles
sun.management.compiler = HotSpot 64-Bit Tiered Compilers
os.version = 3.10.0-1160.15.2.el7.x86_64
user.home = /root
user.timezone = Asia/Shanghai
catalina.useNaming = false
java.awt.printerjob = sun.print.PSPrinterJob
file.encoding = UTF-8
java.specification.version = 1.8
catalina.home = /root/apache-ofbiz-17.12.05/runtime/catalina
user.name = root
java.class.path = build/libs/ofbiz.jar
java.vm.specification.version = 1.8
sun.arch.data.model = 64
sun.java.command = build/libs/ofbiz.jar
java.home = /usr/lib/jvm/java-1.8.0-openjdk-1.8.0.282.b08-1.el7_9.x86_64/jre
user.language = en
java.specification.vendor = Oracle Corporation
awt.toolkit = sun.awt.X11.XToolkit
java.vm.info = mixed mode
java.version = 1.8.0_282
java.ext.dirs = /usr/lib/jvm/java-1.8.0-openjdk-1.8.0.282.b08-1.el7_9.x86_64/jre/lib/ext:/usr/java/packages/lib/ext
sun.boot.class.path = /usr/lib/jvm/java-1.8.0-openjdk-1.8.0.282.b08-1.el7_9.x86_64/jre/lib/resources.jar:/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.282.b08-1.el7_9.x86_64/jre/lib/rt.jar:/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.282.b08-1.el7_9.x86_64/jre/lib/sunrsasign.jar:/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.282.b08-1.el7_9.x86_64/jre/lib/jsse.jar:/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.282.b08-1.el7_9.x86_64/jre/lib/jce.jar:/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.282.b08-1.el7_9.x86_64/jre/lib/charsets.jar:/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.282.b08-1.el7_9.x86_64/jre/lib/jfr.jar:/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.282.b08-1.el7_9.x86_64/jre/classes
java.awt.headless = true
java.vendor = Red Hat, Inc.
catalina.base = /root/apache-ofbiz-17.12.05
file.separator = /
java.vendor.url.bug = https://bugzilla.redhat.com/enter_bug.cgi?product=Red%20Hat%20Enterprise%20Linux%207&component=java-1.8.0-openjdk
sun.io.unicode.encoding = UnicodeLittle
sun.cpu.endian = little
zookeeper.jmx.log4j.disable = true
sun.cpu.isalist = 

VM Flags:
Non-default VM flags: -XX:CICompilerCount=2 -XX:InitialHeapSize=31457280 -XX:MaxHeapSize=486539264 -XX:MaxNewSize=162136064 -XX:MinHeapDeltaBytes=196608 -XX:NewSize=10485760 -XX:OldSize=20971520 -XX:+UseCompressedClassPointers -XX:+UseCompressedOops 
Command line:  

```




2款JDK自带的性能分析工具,JConsole和VisualJVM.前者主要用来分析内存，cpu，线程，类
jstack



jstack process_id

https://blog.csdn.net/L_15156024189/article/details/86512352

从以上信息可以看到，Thead-1持有 <0x00000000e05bff68>对象A的锁，等待锁定 <0x00000000e05bff58>对象B，而此时对象B已经被Thread-0锁定；Thread-0持有对象B的锁，等待锁定对象A，造成死锁！
原文链接：https://blog.csdn.net/qq_29831979/article/details/82660767
20180912141647701.png
Wait to lock xxx
locked xxx


在命令窗口执行jconsole，启动 Java监视和管理控制台
https://blog.csdn.net/L_15156024189/article/details/86512352

可以看到内存，线程等信息
可以进行线程检测



```shell
jstack -h
Usage:
    jstack [-l] <pid>
        (to connect to running process)
    jstack -F [-m] [-l] <pid>
        (to connect to a hung process)
    jstack [-m] [-l] <executable> <core>
        (to connect to a core file)
    jstack [-m] [-l] [server_id@]<remote server IP or hostname>
        (to connect to a remote debug server)

Options:
    -F  to force a thread dump. Use when jstack <pid> does not respond (process is hung)
    -m  to print both java and native frames (mixed mode)
    -l  long listing. Prints additional information about locks
    -h or -help to print this help message
```


jmap
option：选项参数，不可同时使用多个选项参数
pid：java进程id，命令ps -ef | grep java获取
executable：产生核心dump的java可执行文件
core：需要打印配置信息的核心文件
remote-hostname-or-ip：远程调试的主机名或ip
server-id：可选的唯一id，如果相同的远程主机上运行了多台调试服务器，用此选项参数标识服务器

 

options参数
heap : 显示Java堆详细信息
histo : 显示堆中对象的统计信息
permstat :Java堆内存的永久保存区域的类加载器的统计信息
finalizerinfo : 显示在F-Queue队列等待Finalizer线程执行finalizer方法的对象
dump : 生成堆转储快照
F : 当-dump没有响应时，强制生成dump快照

jmap查看内存使用情况与生成heapdump
jstat和jmap命令查看JVM堆内存的使用情况
https://www.cnblogs.com/kaleidoscope/p/9476212.html


jstat命令查看jvm的GC情况 （以Linux为例）
https://www.cnblogs.com/yjd_hycf_space/p/7755633.html

jstat -class