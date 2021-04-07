# jmap


jprofile 都有展示
arthas


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

tenured generation 相当于 old generation
from space
to space s1 s2？


```shell
[root@leryltdllllwew9a springbootblogserver]# jps
10896 Jps
9249 jar
[root@leryltdllllwew9a springbootblogserver]# cd ..
[root@leryltdllllwew9a ~]# jmap 9249
Attaching to process ID 9249, please wait...
Debugger attached successfully.
Server compiler detected.
JVM version is 25.171-b11
0x0000000000400000   7K /usr/jdk1.8.0_171/bin/java
0x00007fbe4a9e7000   251K  /usr/jdk1.8.0_171/jre/lib/amd64/libsunec.so
0x00007fbe5909c000   91K   /usr/jdk1.8.0_171/jre/lib/amd64/libnio.so
0x00007fbe598ad000   66K   /usr/lib64/libbz2.so.1.0.6
0x00007fbe6c13b000   153K  /usr/lib64/liblzma.so.5.2.2
0x00007fbe6c361000   88K   /usr/lib64/libz.so.1.2.7
0x00007fbe6c577000   97K   /usr/lib64/libelf-0.176.so
0x00007fbe6c78f000   19K   /usr/lib64/libattr.so.1.1.0
0x00007fbe6c994000   86K   /usr/lib64/libgcc_s-4.8.5-20150702.so.1
0x00007fbe6cbaa000   330K  /usr/lib64/libdw-0.176.so
0x00007fbe6cdfb000   19K   /usr/lib64/libcap.so.2.22
0x00007fbe801c5000   84K   /usr/lib64/libnss_myhostname.so.2
0x00007fbe803da000   107K  /usr/lib64/libresolv-2.17.so
0x00007fbe805f4000   30K   /usr/lib64/libnss_dns-2.17.so
0x00007fbe807fb000   112K  /usr/jdk1.8.0_171/jre/lib/amd64/libnet.so
0x00007fbe80a12000   49K   /usr/jdk1.8.0_171/jre/lib/amd64/libmanagement.so
0x00007fbe82777000   125K  /usr/jdk1.8.0_171/jre/lib/amd64/libzip.so
0x00007fbe82993000   60K   /usr/lib64/libnss_files-2.17.so
0x00007fbe82ba6000   221K  /usr/jdk1.8.0_171/jre/lib/amd64/libjava.so
0x00007fbe82dd2000   64K   /usr/jdk1.8.0_171/jre/lib/amd64/libverify.so
0x00007fbe82fe1000   42K   /usr/lib64/librt-2.17.so
0x00007fbe831e9000   1110K /usr/lib64/libm-2.17.so
0x00007fbe834eb000   16646K   /usr/jdk1.8.0_171/jre/lib/amd64/server/libjvm.so
0x00007fbe844e8000   2105K /usr/lib64/libc-2.17.so
0x00007fbe848b6000   18K   /usr/lib64/libdl-2.17.so
0x00007fbe84aba000   101K  /usr/jdk1.8.0_171/lib/amd64/jli/libjli.so
0x00007fbe84cd0000   138K  /usr/lib64/libpthread-2.17.so
0x00007fbe84eec000   159K  /usr/lib64/ld-2.17.so
```

jmap -histo:live 9249 > jmap_histio.txt




```shell
jmap -clstats 9249
Attaching to process ID 9249, please wait...
Debugger attached successfully.
Server compiler detected.
JVM version is 25.171-b11
finding class loader instances ..done.
computing per loader stat ..done.
please wait.. computing liveness.liveness analysis may be inaccurate ...
class_loader   classes  bytes parent_loader  alive?   type

<bootstrap> 2772  4886618    null   live  <internal>
0x00000000edc9e048   1  1473  0x00000000ecd97f40   dead  sun/reflect/DelegatingClassLoader@0x000000010000a020
0x00000000edc9ecc8   1  1474  0x00000000ecd97f40   dead  sun/reflect/DelegatingClassLoader@0x000000010000a020
0x00000000ed121e10   1  880   0x00000000ecd97f40   dead  sun/reflect/DelegatingClassLoader@0x000000010000a020
0x00000000ed13a490   1  880   0x00000000ecd97f40   dead  sun/reflect/DelegatingClassLoader@0x000000010000a020
0x00000000ed0c6f08   1  880   0x00000000ecd97f40   dead  sun/reflect/DelegatingClassLoader@0x000000010000a020
0x00000000edc9e5c0   1  1473  0x00000000ecd97f40   dead  sun/reflect/DelegatingClassLoader@0x000000010000a020
0x00000000ed0c7480   1  880   0x00000000ecd97f40   dead  sun/reflect/DelegatingClassLoader@0x000000010000a020
0x00000000ed40f5d0   1  880     null   dead  sun/reflect/DelegatingClassLoader@0x000000010000a020
0x00000000edc9e1d8   1  1473  0x00000000ecd97f40   dead  sun/reflect/DelegatingClassLoader@0x000000010000a020
0x00000000ed6b63f8   1  880   0x00000000ecd97f40   dead  sun/reflect/DelegatingClassLoader@0x000000010000a020
0x00000000ed0c7098   1  880   0x00000000ecd97f40   dead  sun/reflect/DelegatingClassLoader@0x000000010000a020
0x00000000e3550ac0   1  1471  0x00000000ecdb90c0   dead  sun/reflect/DelegatingClassLoader@0x000000010000a020
0x00000000ed56ab40   1  880   0x00000000ecd97f40   dead  sun/reflect/DelegatingClassLoader@0x000000010000a020
0x00000000e3908c88   1  1471  0x00000000ecdb90c0   dead  sun/reflect/DelegatingClassLoader@0x000000010000a020
0x00000000ecd97f40   4489  7372300  0x00000000ecd97e60   dead  org/springframework/boot/loader/LaunchedURLClassLoader@0x0000000100060828
0x00000000edc9e750   1  1473  0x00000000ecd97f40   dead  sun/reflect/DelegatingClassLoader@0x000000010000a020
0x00000000ecdb90c0   40 65330   null   dead  sun/misc/Launcher$ExtClassLoader@0x000000010000fc70
0x00000000edc9e368   1  1473  0x00000000ecd97f40   dead  sun/reflect/DelegatingClassLoader@0x000000010000a020
0x00000000ed122130   1  880   0x00000000ecd97f40   dead  sun/reflect/DelegatingClassLoader@0x000000010000a020
0x00000000ed13a7b0   1  880   0x00000000ecd97f40   dead  sun/reflect/DelegatingClassLoader@0x000000010000a020
0x00000000ed0c7228   1  880   0x00000000ecd97f40   dead  sun/reflect/DelegatingClassLoader@0x000000010000a020
0x00000000ed15c5b0   1  880   0x00000000ecd97f40   dead  sun/reflect/DelegatingClassLoader@0x000000010000a020
0x00000000ed6b64c0   1  880   0x00000000ecd97f40   dead  sun/reflect/DelegatingClassLoader@0x000000010000a020
0x00000000ed09b438   1  880   0x00000000ecd97f40   dead  sun/reflect/DelegatingClassLoader@0x000000010000a020
0x00000000edc9e4f8   1  1473  0x00000000ecd97f40   dead  sun/reflect/DelegatingClassLoader@0x000000010000a020
0x00000000ed121fa0   1  1474  0x00000000ecd97f40   dead  sun/reflect/DelegatingClassLoader@0x000000010000a020
0x00000000ed13a620   1  880   0x00000000ecd97f40   dead  sun/reflect/DelegatingClassLoader@0x000000010000a020
0x00000000ed0c73b8   1  880   0x00000000ecd97f40   dead  sun/reflect/DelegatingClassLoader@0x000000010000a020
0x00000000ed66a3d0   1  880   0x00000000ecd97f40   dead  sun/reflect/DelegatingClassLoader@0x000000010000a020
0x00000000ecd97e60   45 76900 0x00000000ecdb90c0   dead  sun/misc/Launcher$AppClassLoader@0x000000010000f8c8
0x00000000edc9ddf0   1  1473  0x00000000ecd97f40   dead  sun/reflect/DelegatingClassLoader@0x000000010000a020
0x00000000edc9ea70   1  1483  0x00000000ecd97f40   dead  sun/reflect/DelegatingClassLoader@0x000000010000a020
0x00000000ed0215b8   1  880   0x00000000ecd97f40   dead  sun/reflect/DelegatingClassLoader@0x000000010000a020
0x00000000ed327088   0  0  0x00000000ecd97f40   dead  org/springframework/boot/web/embedded/tomcat/TomcatEmbeddedWebappClassLoader@0x0000000100321428
0x00000000edaa7190   1  1471  0x00000000ecd97f40   dead  sun/reflect/DelegatingClassLoader@0x000000010000a020
0x00000000edc9e688   1  1473  0x00000000ecd97f40   dead  sun/reflect/DelegatingClassLoader@0x000000010000a020
0x00000000ed0ed3c8   1  880   0x00000000ecd97f40   dead  sun/reflect/DelegatingClassLoader@0x000000010000a020
0x00000000edc9df80   1  1473  0x00000000ecd97f40   dead  sun/reflect/DelegatingClassLoader@0x000000010000a020
0x00000000edc9ec00   1  880   0x00000000ecd97f40   dead  sun/reflect/DelegatingClassLoader@0x000000010000a020
0x00000000ed121ed8   1  880   0x00000000ecd97f40   dead  sun/reflect/DelegatingClassLoader@0x000000010000a020
0x00000000ed13a558   1  880   0x00000000ecd97f40   dead  sun/reflect/DelegatingClassLoader@0x000000010000a020
0x00000000ed0c6e40   1  880   0x00000000ecd97f40   dead  sun/reflect/DelegatingClassLoader@0x000000010000a020
0x00000000edc9e818   1  1471  0x00000000ecd97f40   dead  sun/reflect/DelegatingClassLoader@0x000000010000a020
0x00000000ed40f698   1  880     null   dead  sun/reflect/DelegatingClassLoader@0x000000010000a020
0x00000000edc9e110   1  1471  0x00000000ecd97f40   dead  sun/reflect/DelegatingClassLoader@0x000000010000a020
0x00000000edc9ed90   1  880   0x00000000ecd97f40   dead  sun/reflect/DelegatingClassLoader@0x000000010000a020
0x00000000ed6b6330   1  880   0x00000000ecd97f40   dead  sun/reflect/DelegatingClassLoader@0x000000010000a020
0x00000000ed0c6fd0   1  880   0x00000000ecd97f40   dead  sun/reflect/DelegatingClassLoader@0x000000010000a020
0x00000000ed56ac88   1  1472  0x00000000ecd97f40   dead  sun/reflect/DelegatingClassLoader@0x000000010000a020
0x00000000e3902770   1  1471  0x00000000ecdb90c0   dead  sun/reflect/DelegatingClassLoader@0x000000010000a020
0x00000000edc9e9a8   1  881   0x00000000ecd97f40   dead  sun/reflect/DelegatingClassLoader@0x000000010000a020
0x00000000ed6b6588   1  880   0x00000000ecd97f40   dead  sun/reflect/DelegatingClassLoader@0x000000010000a020
0x00000000edc9e2a0   1  1473  0x00000000ecd97f40   dead  sun/reflect/DelegatingClassLoader@0x000000010000a020
0x00000000ed0c7160   1  880   0x00000000ecd97f40   dead  sun/reflect/DelegatingClassLoader@0x000000010000a020
0x00000000ed15c678   1  880   0x00000000ecd97f40   dead  sun/reflect/DelegatingClassLoader@0x000000010000a020
0x00000000ed66a308   1  880   0x00000000ecd97f40   dead  sun/reflect/DelegatingClassLoader@0x000000010000a020
0x00000000e3905a60   1  1471  0x00000000ecdb90c0   dead  sun/reflect/DelegatingClassLoader@0x000000010000a020
0x00000000edc9deb8   1  1473  0x00000000ecd97f40   dead  sun/reflect/DelegatingClassLoader@0x000000010000a020
0x00000000edc9eb38   1  882   0x00000000ecd97f40   dead  sun/reflect/DelegatingClassLoader@0x000000010000a020
0x00000000ece8f890   0  0  0x00000000ecd97e60   dead  java/util/ResourceBundle$RBClassLoader@0x00000001000b98e8
0x00000000edc9e430   1  1473  0x00000000ecd97f40   dead  sun/reflect/DelegatingClassLoader@0x000000010000a020
0x00000000ed122068   1  880   0x00000000ecd97f40   dead  sun/reflect/DelegatingClassLoader@0x000000010000a020
0x00000000ed13a6e8   1  880   0x00000000ecd97f40   dead  sun/reflect/DelegatingClassLoader@0x000000010000a020
0x00000000ed0c72f0   1  880   0x00000000ecd97f40   dead  sun/reflect/DelegatingClassLoader@0x000000010000a020
0x00000000ed5eba20   1  880   0x00000000ecd97f40   dead  sun/reflect/DelegatingClassLoader@0x000000010000a020
0x00000000ed66ab18   1  880     null   dead  sun/reflect/DelegatingClassLoader@0x000000010000a020
0x00000000e35f90a0   1  1471    null   dead  sun/reflect/DelegatingClassLoader@0x000000010000a020

total = 68  7408  12469938     N/A     alive=1, dead=67      N/A  
```


sun/reflect/DelegatingClassLoader

没有boostclassloader
没有app