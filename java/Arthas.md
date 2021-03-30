# Arthas

http://arthas.gitee.io/

[阿里开源 java 项目内存监控工具 arthas](https://blog.csdn.net/ningmengban/article/details/109697024)



https://www.oschina.net/p/arthas



注意账户

arthas@23427





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