# jmap



javap



javah



jps


命令：jmap pid
描述：查看进程的内存映像信息,


https://www.jianshu.com/p/a4ad53179df3
### 示例二：heap
命令：jmap -heap pid
描述：显示Java堆详细信息

打印一个堆的摘要信息，包括使用的GC算法、堆配置信息和各内存区域内存使用信息	
histo[:live]
命令：jmap -histo:live pid
描述：显示堆中对象的统计信息

其中包括每个Java类、对象数量、内存大小(单位：字节)、完全限定的类名。打印的虚拟机内部的类名称将会带有一个’*’前缀。如果指定了live子选项，则只计算活动的对象。


### 示例四：clstats
命令：jmap -clstats pid
描述：打印类加载器信息

-clstats是-permstat的替代方案，在JDK8之前，-permstat用来打印类加载器的数据
打印Java堆内存的永久保存区域的类加载器的智能统计信息。对于每个类加载器而言，它的名称、活跃度、地址、父类加载器、它所加载的类的数量和大小都会被打印。此外，包含的字符串数量和大小也会被打印。
### 示例五：finalizerinfo
命令：jmap -finalizerinfo pid
描述：打印等待终结的对象信息



```shell
jps -l
20371 springbootblogserver-0.0.1-SNAPSHOT.jar
17551 sun.tools.jps.Jps
[root@leryltdllllwew9a ~]# jmap -heap 20371
Attaching to process ID 20371, please wait...
Debugger attached successfully.
Server compiler detected.
JVM version is 25.171-b11

using thread-local object allocation.
Mark Sweep Compact GC

Heap Configuration:
   MinHeapFreeRatio         = 40
   MaxHeapFreeRatio         = 70
   MaxHeapSize              = 482344960 (460.0MB)
   NewSize                  = 10485760 (10.0MB)
   MaxNewSize               = 160759808 (153.3125MB)
   OldSize                  = 20971520 (20.0MB)
   NewRatio                 = 2
   SurvivorRatio            = 8
   MetaspaceSize            = 21807104 (20.796875MB)
   CompressedClassSpaceSize = 1073741824 (1024.0MB)
   MaxMetaspaceSize         = 17592186044415 MB
   G1HeapRegionSize         = 0 (0.0MB)

Heap Usage:
New Generation (Eden + 1 Survivor Space):
   capacity = 17694720 (16.875MB)
   used     = 12183248 (11.618850708007812MB)
   free     = 5511472 (5.2561492919921875MB)
   68.85244864004629% used
Eden Space:
   capacity = 15794176 (15.0625MB)
   used     = 10282704 (9.806350708007812MB)
   free     = 5511472 (5.2561492919921875MB)
   65.10440304071577% used
From Space:
   capacity = 1900544 (1.8125MB)
   used     = 1900544 (1.8125MB)
   free     = 0 (0.0MB)
   100.0% used
To Space:
   capacity = 1900544 (1.8125MB)
   used     = 0 (0.0MB)
   free     = 1900544 (1.8125MB)
   0.0% used
tenured generation:
   capacity = 39129088 (37.31640625MB)
   used     = 38995128 (37.18865203857422MB)
   free     = 133960 (0.12775421142578125MB)
   99.6576459947137% used

16044 interned Strings occupying 1414880 bytes.

```