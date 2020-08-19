# class



[深入理解Java类加载器(ClassLoader](https://blog.csdn.net/javazejian/article/details/73413292)



**Bootstrap ClassLoader**  负责加载java基础类，主要是 %JRE_HOME/lib/ 目录下的rt.jar、resources.jar、charsets.jar和class等
**Extension ClassLoader**   负责加载java扩展类，主要是 %JRE_HOME/lib/ext 目录下的jar和class
**App ClassLoader**     负责加载当前java应用的classpath中的所有类。



sun.misc.Launcher$AppClassLoader

java.lang.ClassLoader

 java.net.URLClassLoader



Caused by: java.lang.ClassNotFoundException: com.mysql.jdbc.jdbc2.optional.MysqlDataSource
	at java.net.URLClassLoader.findClass(URLClassLoader.java:382)
	at java.lang.ClassLoader.loadClass(ClassLoader.java:418)
	at sun.misc.Launcher$AppClassLoader.loadClass(Launcher.java:355)
	at java.lang.ClassLoader.loadClass(ClassLoader.java:351)
	at com.zaxxer.hikari.util.UtilityElf.createInstance(UtilityElf.java:100)




每个class文件的开头都是4个字节的魔数(Magic Number),它的唯一作用是确定这个文件是否为一个能被虚拟机接受的Class文件。其实很多文件存储标准中都使用魔数来进行身份识别，比如图片格式的gif或者jpeg文件头中都存在有魔数。使用魔数而不是扩展名来进行识别主要是基于安全方面的考虑，因为文件扩展名是可以随意改动的。


ClassLoader 双亲委派模型

JMM

不是Java线程模型



java为了实现其夸平台的特性，使用了一种虚拟机技术，java程序运行在这虚拟机上，那么不管你是windows系统，linux系统，unix系统，只要我java虚拟机屏蔽一切操作系统带来的差异，向java程序提供专用的、各系统无差别的虚拟机，那么java程序员就不需要关心底层到底是什么操作系统了





原子性
可见性
一致性

happen-before 8个规则





八大原则：

- 单线程happen-before原则：在同一个线程中，书写在前面的操作happen-before后面的操作。
- 锁的happen-before原则：同一个锁的unlock操作happen-before此锁的lock操作。
- volatile的happen-before原则：对一个volatile变量的写操作happen-before对此变量的任意操作(当然也包括写操作了)。
- happen-before的传递性原则：如果A操作 happen-before B操作，B操作happen-before C操作，那么A操作happen-before C操作。
- 线程启动的happen-before原则：同一个线程的start方法happen-before此线程的其它方法。
- 线程中断的happen-before原则：对线程interrupt方法的调用happen-before被中断线程的检测到中断发送的代码。
- 线程终结的happen-before原则：线程中的所有操作都happen-before线程的终止检测。
- 对象创建的happen-before原则：一个对象的初始化完成先于他的finalize方法调用。



作者：aworker
链接：https://www.jianshu.com/p/1508eedba54d
来源：简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。



8=4+1+1+1+1 线程4个 单线程 线程启动 线程中断 终结

传递性 volatile locker Object-new




[运行jar应用程序引用其他jar包的四种方法](https://www.iteye.com/blog/longdick-332580)





方法四、自定义Classloader来加载
这种方法是终极解决方案，基本上那些知名java应用都是那么干的，如tomcat、jboss等等。
这种方式有点复杂，需要专门开贴讨论。

[图解classloader加载class的流程及自定义ClassLoader](https://blog.csdn.net/u011679955/article/details/52472422)



**自定义ClassLoader：**

 

由于一些特殊的需求，我们可能需要定制ClassLoader的加载行为，这时候就需要自定义ClassLoader了.

自定义ClassLoader需要继承ClassLoader抽象类，重写findClass方法，这个方法定义了ClassLoader查找class的方式。

主要可以扩展的方法有：

findClass      定义查找Class的方式

defineClass    将类文件字节码加载为jvm中的class

findResource   定义查找资源的方式

 

如果嫌麻烦的话，我们可以直接使用或继承已有的ClassLoader实现，比如

 



- `java.net.URLClassLoader`
- `java.security.SecureClassLoader`
- `java.rmi.server.RMIClassLoader`
- `sun.applet.AppletClassLoader`

Extension ClassLoader 和 App ClassLoader都是java.net.URLClassLoader的子类。

这个是URLClassLoader的构造方法：

 

public URLClassLoader(URL[] urls, ClassLoader parent)

public URLClassLoader(URL[] urls)







**方法一、使用Bootstrap Classloader来加载这些类。**

我们可以在运行时使用如下参数：

-Xbootclasspath:完全取代系统Java classpath.最好不用。
-Xbootclasspath/a: 在系统class加载后加载。一般用这个。
-Xbootclasspath/p: 在系统class加载前加载,注意使用，和系统类冲突就不好了.

win32   java -Xbootclasspath/a: some.jar;some2.jar;  -jar test.jar

unix      java -Xbootclasspath/a: some.jar:some2.jar:  -jar test.jar

**方法二、使用Extension Classloader来加载**

你可以把需要加载的jar都扔到%JRE_HOME%/lib/ext下面，这个目录下的jar包会在Bootstrap Classloader工作完后由Extension Classloader来加载。非常方便，非常省心。:)

**方法三、还是用AppClassloader来加载，不过不需要classpath参数了**

我们MANIFEST.MF中添加如下代码：

Class-Path: lib/some.jar

lib是和test.jar同目录的一个子目录，test.jar要引用的some.jar包就在这里面。

然后测试运行，一切正常！

如果有多个jar包需要引用的情况：

Class-Path: lib/some.jar lib/some2.jar

每个单独的jar用空格隔开就可以了。注意使用相对路径。

备注：osgi就是这样干的



[Jetty ClassLoader](https://toutiao.io/posts/xy5ng7/preview)



[从问题了解Jetty类加载机制](https://cloud.tencent.com/developer/news/294386)





[TOMCAT源码阅读总结（1）-TOMCAT的类加载体系](https://segmentfault.com/a/1190000011566998)



Java类加载流程

https://blog.csdn.net/qq_36182135/article/details/81946152

Java面试相关（一）-- Java类加载全过程

https://www.jianshu.com/p/ace2aa692f96

https://blog.csdn.net/u011679955/article/details/52472422

[Jetty ClassLoader](https://toutiao.io/posts/xy5ng7/preview)

[从问题了解Jetty类加载机制](https://cloud.tencent.com/developer/news/294386)

https://segmentfault.com/a/1190000011566998

