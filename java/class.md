# class



[深入理解Java类加载器(ClassLoader](https://blog.csdn.net/javazejian/article/details/73413292)

Caused by: java.lang.ClassNotFoundException: com.mysql.jdbc.jdbc2.optional.MysqlDataSource
	at java.net.URLClassLoader.findClass(URLClassLoader.java:382)
	at java.lang.ClassLoader.loadClass(ClassLoader.java:418)
	at sun.misc.Launcher$AppClassLoader.loadClass(Launcher.java:355)
	at java.lang.ClassLoader.loadClass(ClassLoader.java:351)
	at com.zaxxer.hikari.util.UtilityElf.createInstance(UtilityElf.java:100)




每个class文件的开头都是4个字节的魔数(Magic Number),它的唯一作用是确定这个文件是否为一个能被虚拟机接受的Class文件。其实很多文件存储标准中都使用魔数来进行身份识别，比如图片格式的gif或者jpeg文件头中都存在有魔数。使用魔数而不是扩展名来进行识别主要是基于安全方面的考虑，因为文件扩展名是可以随意改动的。


ClassLoader 双亲委派模型

JMM
原子性
可见性
一致性

happen-before


[运行jar应用程序引用其他jar包的四种方法](https://www.iteye.com/blog/longdick-332580)





方法四、自定义Classloader来加载
这种方法是终极解决方案，基本上那些知名java应用都是那么干的，如tomcat、jboss等等。
这种方式有点复杂，需要专门开贴讨论。


[图解classloader加载class的流程及自定义ClassLoader](https://blog.csdn.net/u011679955/article/details/52472422)



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

