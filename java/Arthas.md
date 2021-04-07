# Arthas



可以查看线程

类加载器



内存占用

[Linux下查看某一进程所占用内存的方法](https://www.cnblogs.com/xuanbjut/p/11564744.html)

jps 获取进程id

top -p 2913
ps -aux | grep kafka 第5个数据
还可以查看进程的status文件： cat /proc/2913/status 

　VmRSS对应的值就是物理内存占用，大约为943M和刚才一致

　　另外还可以通过 top 命令动态查看内存占用

　　通过： ps aux | sort -k4,4nr | head -n 10 查看内存占用前10名的程序

```
jps
23427 ofbiz.jar
[root@10-23-29-39 ~]# cat /proc/23427/status
Name:	java
Umask:	0022
State:	S (sleeping)
Tgid:	23427
Ngid:	0
Pid:	23427
PPid:	1
TracerPid:	0
Uid:	0	0	0	0
Gid:	0	0	0	0
FDSize:	1024
Groups:	0 
VmPeak:	 2918864 kB
VmSize:	 2751656 kB
VmLck:	       0 kB
VmPin:	    2856 kB
VmHWM:	  655844 kB
VmRSS:	  534164 kB
RssAnon:	  528228 kB
RssFile:	    5936 kB
RssShmem:	       0 kB
VmData:	 2544788 kB
VmStk:	     132 kB
VmExe:	       4 kB
VmLib:	   20368 kB
VmPTE:	    1568 kB
VmSwap:	    7596 kB
Threads:	90
SigQ:	0/7322
SigPnd:	0000000000000000
ShdPnd:	0000000000000000
SigBlk:	0000000000000000
SigIgn:	0000000000000000
SigCgt:	2000000185005ccf
CapInh:	0000000000000000
CapPrm:	0000001fffffffff
CapEff:	0000001fffffffff
CapBnd:	0000001fffffffff
CapAmb:	0000000000000000
NoNewPrivs:	0
Seccomp:	0
Speculation_Store_Bypass:	vulnerable
Cpus_allowed:	ffffffff,ffffffff,ffffffff,ffffffff
Cpus_allowed_list:	0-127
Mems_allowed:	00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000001
Mems_allowed_list:	0
voluntary_ctxt_switches:	10
nonvoluntary_ctxt_switches:	0
```




http://arthas.gitee.io/

[阿里开源 java 项目内存监控工具 arthas](https://blog.csdn.net/ningmengban/article/details/109697024)



https://www.oschina.net/p/arthas



注意账户

Whom

arthas@23427



重复进入arthas

```
java -jar arthas-boot.jar
[INFO] arthas-boot version: 3.5.0
[INFO] Process 23427 already using port 3658
[INFO] Process 23427 already using port 8563
[INFO] Found existing java process, please choose one and input the serial number of the process, eg : 1. Then hit ENTER.
* [1]: 23427 build/libs/ofbiz.jar
1
[INFO] arthas home: /root/.arthas/lib/3.5.0/arthas
[INFO] The target process already listen port 3658, skip attach.
[INFO] arthas-client connect 127.0.0.1 3658
  ,---.  ,------. ,--------.,--.  ,--.  ,---.   ,---.                           
 /  O  \ |  .--. ''--.  .--'|  '--'  | /  O  \ '   .-'                          
|  .-.  ||  '--'.'   |  |   |  .--.  ||  .-.  |`.  `-.                          
|  | |  ||  |\  \    |  |   |  |  |  ||  | |  |.-'    |                         
`--' `--'`--' '--'   `--'   `--'  `--'`--' `--'`-----'     
```



```
[root@10-23-29-39 arthas]# ll
total 13480
-rw-r--r-- 1 root root     8450 Mar 30 08:13 arthas-agent.jar
-rw-r--r-- 1 root root   140961 Mar 30 08:13 arthas-boot.jar
-rw-r--r-- 1 root root   430306 Mar 30 08:13 arthas-client.jar
-rw-r--r-- 1 root root 13129766 Mar 30 08:13 arthas-core.jar
-rw-r--r-- 1 root root     4497 Mar 30 08:13 arthas-demo.jar
-rw-r--r-- 1 root root      402 Mar 30 08:13 arthas.properties
-rw-r--r-- 1 root root     8903 Mar 30 08:13 arthas-spy.jar
-rw-r--r-- 1 root root     3091 Mar 30 08:13 as.bat
-rw-r--r-- 1 root root     7744 Mar 30 08:13 as-service.bat
-rw-r--r-- 1 root root    32805 Mar 30 08:13 as.sh
drwxr-xr-x 2 root root      156 Mar 30 08:13 async-profiler
-rw-r--r-- 1 root root      635 Mar 30 08:13 install-local.sh
-rw-r--r-- 1 root root     2020 Mar 30 08:13 logback.xml
[root@10-23-29-39 arthas]# pwd
/root/.arthas/lib/3.5.0/arthas
```





ucloud云服务器实践

```shell
java -jar arthas-boot.jar
[INFO] arthas-boot version: 3.5.0
[INFO] Found existing java process, please choose one and input the serial number of the process, eg : 1. Then hit ENTER.
* [1]: 23427 build/libs/ofbiz.jar
1
[INFO] Start download arthas from remote server: https://arthas.aliyun.com/download/3.5.0?mirror=aliyun
[INFO] Download arthas success.
[INFO] arthas home: /root/.arthas/lib/3.5.0/arthas
[INFO] Try to attach process 23427
[INFO] Attach process 23427 success.
[INFO] arthas-client connect 127.0.0.1 3658
  ,---.  ,------. ,--------.,--.  ,--.  ,---.   ,---.                           
 /  O  \ |  .--. ''--.  .--'|  '--'  | /  O  \ '   .-'                          
|  .-.  ||  '--'.'   |  |   |  .--.  ||  .-.  |`.  `-.                          
|  | |  ||  |\  \    |  |   |  |  |  ||  | |  |.-'    |                         
`--' `--'`--' '--'   `--'   `--'  `--'`--' `--'`-----'                          
                                                                                

wiki       https://arthas.aliyun.com/doc                                        
tutorials  https://arthas.aliyun.com/doc/arthas-tutorials.html                  
version    3.5.0                                                                
main_class                                                                      
pid        23427                                                                
time       2021-03-30 08:13:42
```





```
[arthas@23427]$ classloader
 name                                           numberOfInstances  loadedCountT 
                                                                   otal         
 sun.misc.Launcher$AppClassLoader               1                  10900        
 BootstrapClassLoader                           1                  4168         
 com.taobao.arthas.agent.ArthasClassloader      1                  1454         
 sun.reflect.DelegatingClassLoader              142                142          
 sun.misc.Launcher$ExtClassLoader               1                  78           
 groovy.lang.GroovyClassLoader$InnerLoader      36                 37           
 org.codehaus.groovy.reflection.SunClassLoader  1                  1            
 java.net.URLClassLoader                        34                 0            
Affect(row-cnt:8) cost in 56 ms.




```
```shell 
[arthas@23427]$ profiler start
Started [cpu] profiling


lsof -i:3658
COMMAND   PID USER   FD   TYPE  DEVICE SIZE/OFF NODE NAME
java    23427 root  577u  IPv6 8905943      0t0  TCP localhost:ps-ams->localhost:47758 (ESTABLISHED)
java    23427 root  598u  IPv6 8905726      0t0  TCP localhost:ps-ams (LISTEN)
java    47863 root   20u  IPv6 8905942      0t0  TCP localhost:47758->localhost:ps-ams (ESTABLISHED)
```





# 命令列表

- [dashboard](https://arthas.gitee.io/dashboard.html)
- [thread](https://arthas.gitee.io/thread.html)
- [jvm](https://arthas.gitee.io/jvm.html)
- [sysprop](https://arthas.gitee.io/sysprop.html)
- [sysenv](https://arthas.gitee.io/sysenv.html)
- [vmoption](https://arthas.gitee.io/vmoption.html)
- [perfcounter](https://arthas.gitee.io/perfcounter.html)
- [logger](https://arthas.gitee.io/logger.html)
- [mbean](https://arthas.gitee.io/mbean.html)
- [getstatic](https://arthas.gitee.io/getstatic.html)
- [ognl](https://arthas.gitee.io/ognl.html)
- [sc](https://arthas.gitee.io/sc.html)
- [sm](https://arthas.gitee.io/sm.html)
- [dump](https://arthas.gitee.io/dump.html)
- [heapdump](https://arthas.gitee.io/heapdump.html)
- [jad](https://arthas.gitee.io/jad.html)
- [classloader](https://arthas.gitee.io/classloader.html)
- [mc](https://arthas.gitee.io/mc.html)
- [retransform](https://arthas.gitee.io/retransform.html)
- [redefine](https://arthas.gitee.io/redefine.html)
- [monitor](https://arthas.gitee.io/monitor.html)
- [watch](https://arthas.gitee.io/watch.html)
- [trace](https://arthas.gitee.io/trace.html)
- [stack](https://arthas.gitee.io/stack.html)
- [tt](https://arthas.gitee.io/tt.html)
- [profiler](https://arthas.gitee.io/profiler.html)
- [cat](https://arthas.gitee.io/cat.html)
- [echo](https://arthas.gitee.io/echo.html)
- [grep](https://arthas.gitee.io/grep.html)
- [base64](https://arthas.gitee.io/base64.html)
- [tee](https://arthas.gitee.io/tee.html)
- [pwd](https://arthas.gitee.io/pwd.html)
- [auth](https://arthas.gitee.io/auth.html)
- [options](https://arthas.gitee.io/options.html)

## Arthas 基础命令

- help——查看命令帮助信息
- cls——清空当前屏幕区域
- session——查看当前会话的信息
- [reset](https://arthas.gitee.io/reset.html)——重置增强类，将被 Arthas 增强过的类全部还原，Arthas 服务端关闭时会重置所有增强过的类
- version——输出当前目标 Java 进程所加载的 Arthas 版本号
- history——打印命令历史
- quit——退出当前 Arthas 客户端，其他 Arthas 客户端不受影响
- stop——关闭 Arthas 服务端，所有 Arthas 客户端全部退出
- [keymap](https://arthas.gitee.io/keymap.html)——Arthas快捷键列表及自定义快捷键



```
[arthas@23427]$ thread
Threads Total: 89, NEW: 0, RUNNABLE: 21, BLOCKED: 0, WAITING: 34, TIMED_WAITING:
 29, TERMINATED: 0, Internal threads: 5                                         
ID NAME                GROUP     PRIORI STATE  %CPU  DELTA_ TIME   INTER DAEMON 
-1 C2 CompilerThread0  -         -1     -      11.56 0.023  1:55.1 false true   
-1 C1 CompilerThread1  -         -1     -      0.73  0.001  0:26.9 false true   
11 arthas-command-exec system    5      RUNNAB 0.71  0.001  0:0.27 false true   
56 http-nio-8080-exec- main      5      TIMED_ 0.18  0.000  2:2.20 false true   
-1 Service Thread      -         -1     -      0.1   0.000  0:0.50 false true   
-1 VM Periodic Task Th -         -1     -      0.04  0.000  7:52.5 false true   
65 http-nio-8080-Clien main      5      RUNNAB 0.02  0.000  7:48.3 false true   
20 Abandoned connectio Delegator 5      TIMED_ 0.02  0.000  4:29.3 false true   
41 Catalina-utility-1  main      1      TIMED_ 0.02  0.000  1:41.7 false false  
28 http-nio-8080-Block main      5      RUNNAB 0.0   0.000  2:40.5 false true   
42 Catalina-utility-2  main      1      WAITIN 0.0   0.000  1:40.9 false false  
2  Reference Handler   system    10     WAITIN 0.0   0.000  0:0.15 false true   
3  Finalizer           system    8      WAITIN 0.0   0.000  0:0.15 false true   
4  Signal Dispatcher   system    9      RUNNAB 0.0   0.000  0:0.00 false true   
93 Attach Listener     system    9      RUNNAB 0.0   0.000  0:0.02 false true   
10 arthas-timer        system    9      WAITIN 0.0   0.000  0:0.00 false true   
10 arthas-NettyHttpTel system    5      RUNNAB 0.0   0.000  0:0.04 false true   
10 arthas-NettyWebsock system    5      RUNNAB 0.0   0.000  0:0.00 false true   
10 arthas-NettyWebsock system    5      RUNNAB 0.0   0.000  0:0.00 false true   
10 arthas-shell-server system    9      TIMED_ 0.0   0.000  0:1.32 false true   
10 arthas-session-mana system    9      TIMED_ 0.0   0.000  0:0.54 false true 
```



