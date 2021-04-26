# Tomcat


servlet 单例多线程

servlet类 不能有经常更改的属性

因为servlet不是线程安全的


tomcat 有线程池


tomcat netty实现http协议 server端 对比

http://openejb.apache.org/latest/examples/
http://tomee.apache.org/jakartaee-8.0/javadoc/


Tomcat双亲委派模型 重点 类加载器 需要整理进anki
https://zhuanlan.zhihu.com/p/347776927


我想，在研究tomcat 类加载之前，我们复习一下或者说巩固一下java 默认的类加载器。楼主以前对类加载也是懵懵懂懂，借此机会，也好好复习一下。楼主翻开了神书《深入理解Java虚拟机》第二版，p227, 关于类加载器的部分。请看：

1. 什么是类加载机制？
代码编译的结果从本地机器码转变成字节码，是存储格式的一小步，却是编程语言发展的一大步。
Java虚拟机把描述类的数据从Class文件加载进内存，并对数据进行校验，转换解析和初始化，最终形成可以呗虚拟机直接使用的Java类型，这就是虚拟机的类加载机制。
虚拟机设计团队把类加载阶段中的“通过一个类的全限定名来获取描述此类的二进制字节流”这个动作放到Java虚拟机外部去实现，以便让应用程序自己决定如何去获取所需要的类。实现这动作的代码模块成为“类加载器”。
类与类加载器的关系

类加载器虽然只用于实现类的加载动作，但它在Java程序中起到的作用却远远不限于类加载阶段。对于任意一个类，都需要由加载他的类加载器和这个类本身一同确立其在Java虚拟机中的唯一性，每一个类加载器，都拥有一个独立的类命名空间。这句话可以表达的更通俗一些：比较两个类是否“相等”，只有在这两个类是由同一个类加载器加载的前提下才有意义，否则，即使这两个类来自同一个Class文件，被同一个虚拟机加载，只要加载他们的类加载器不同，那这个两个类就必定不相等。
2. 什么是双亲委任模型
从Java虚拟机的角度来说，只存在两种不同类加载器：一种是启动类加载器(Bootstrap ClassLoader)，这个类加载器使用C++语言实现（只限HotSpot），是虚拟机自身的一部分；另一种就是所有其他的类加载器，这些类加载器都由Java语言实现，独立于虚拟机外部，并且全都继承自抽象类java.lang.ClassLoader.
从Java开发人员的角度来看，类加载还可以划分的更细致一些，绝大部分Java程序员都会使用以下3种系统提供的类加载器：
启动类加载器（Bootstrap ClassLoader）：这个类加载器复杂将存放在 JAVA_HOME/lib 目录中的，或者被-Xbootclasspath 参数所指定的路径种的，并且是虚拟机识别的（仅按照文件名识别，如rt.jar，名字不符合的类库即使放在lib目录下也不会重载）。
扩展类加载器（Extension ClassLoader）：这个类加载器由sun.misc.Launcher$ExtClassLoader实现，它负责夹杂JAVA_HOME/lib/ext 目录下的，或者被java.ext.dirs 系统变量所指定的路径种的所有类库。开发者可以直接使用扩展类加载器。
应用程序类加载器（Application ClassLoader）：这个类加载器由sun.misc.Launcher$AppClassLoader 实现。由于这个类加载器是ClassLoader 种的getSystemClassLoader方法的返回值，所以也成为系统类加载器。它负责加载用户类路径（ClassPath）上所指定的类库。开发者可以直接使用这个类加载器，如果应用中没有定义过自己的类加载器，一般情况下这个就是程序中默认的类加载器。
这些类加载器之间的关系一般如下图所示：
![tomcat](../../imgs/classloader.jpg)



Tomcat是个web容器， 那么它要解决什么问题：
一个web容器可能需要部署两个应用程序，不同的应用程序可能会依赖同一个第三方类库的不同版本，不能要求同一个类库在同一个服务器只有一份，因此要保证每个应用程序的类库都是独立的，保证相互隔离。
部署在同一个web容器中相同的类库相同的版本可以共享。否则，如果服务器有10个应用程序，那么要有10份相同的类库加载进虚拟机，这是扯淡的。
web容器也有自己依赖的类库，不能于应用程序的类库混淆。基于安全考虑，应该让容器的类库和程序的类库隔离开来。
web容器要支持jsp的修改，我们知道，jsp 文件最终也是要编译成class文件才能在虚拟机中运行，但程序运行后修改jsp已经是司空见惯的事情，否则要你何用？ 所以，web容器需要支持 jsp 修改后不用重启。

![tomcat](classloader2.jpg)

[Tomcat config](https://www.cnblogs.com/chengssblog/p/6635211.html)

[写一个迷你版的Tomcat](https://www.jianshu.com/p/dce1ee01fb90)

Servlet如何处理
社区下一步发展方向





tomcat如何处理session？

tomcat如何实现https？


BEA WebLogic Sever：是一款十分强大的服务器软件，配置比较简单，而且对JSP的扩展十分强大，附带了数据库的JDBC驱动程序，支持JHTML，是目前市场占有率最高的服务器，目前最新版本是6.1版，价格很贵，不过嘿嘿.....有破解版哦：）
IBM WebSphere Application Server:是IBM的产品，功能很强大，而且有IBM的开发工具相配套，开发Web程序十分方便，不过价格上万元。
