# jstack

-Djava.awt.headless=true -Djava.net.preferIPv4Stack=true -server -Xmx2g -Xms2g -Dfastjson.parser.safeMode=true -XX:+DisableExplicitGC -XX:+UseConcMarkSweepGC -XX:+CMSParallelRemarkEnabled -XX:+UseCMSCompactAtFullCollection -XX:LargePageSizeInBytes=128m -XX:+UseFastAccessorMethods -XX:+UseCMSInitiatingOccupancyOnly -XX:CMSInitiatingOccupancyFraction=70

#### jstack(查看线程)、jmap(查看内存)和jstat(性能分析) jconsole

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