# jdk

## 下载地址

https://jdk.java.net/archive/

jdk SelectorProvider
spi



jsr

jcp  流程 不是委员会

openjdk

oraclejdk

[jdk新特性](https://blog.csdn.net/lzw2497727771/article/details/104019737)

java为何要设计Cloneable这个接口clone这个方法很奇怪，它在Object类中被定义，定义时是个protected类型，也就是说只能被同一包中的类以及子类访问，这个方法没有实现Cloneable接口(一个只有名字没有任何方法的空接口).
然而java规定所有类若要使用clone方法必须要实现Clonneable接口，没错就是那个空接口，以达到标记的作用，不然会报CloneNotSupportedException，想必这些是在clone方法里面写好的
但是为什么一定要弄这个标记空接口呢？真的只是为了标记吗？那为什么clone方法需要被标记呢？感觉没什么用啊

Cloneable 本身就是个比较鸡肋的接口，尽量避免使用。

如果一个类重写了 Object 内定义的 clone() ，需要同时实现 Cloneable 接口（虽然这个接口内并没有定义 clone() 方法），否则在调用 clone() 时会报 CloneNotSupportedException 异常，也就是说， Cloneable 接口只是个合法调用 clone() 的标识（marker-interface）。

事实上，若想实现对象的克隆，你不得不重写 Object 的 clone() 方法，还得实现 Cloneable 接口，这样就有点麻烦了。

简单的做法，借助 Apache Commons 可以直接实现：

- 深克隆/拷贝（deep clone/copy）： [SerializationUtils](http://commons.apache.org/proper/commons-lang/api-2.5/org/apache/commons/lang/SerializationUtils.html)
- 浅克隆/拷贝（shallow clone/copy）：[BeanUtils](http://commons.apache.org/proper/commons-beanutils/)

简单的克隆，也可以通过 copy-constructor (拷贝构造方法) 实现，详情参考 Effective Java 作者 Josh Bloch 的这篇访谈：[Copy Constructor Versus Cloning](https://link.zhihu.com/?target=http%3A//www.artima.com/intv/bloch13.html)

其中也谈到了 Cloneable 接口的很多缺点。

C:\Program Files\JetBrains\IntelliJ IDEA 2018.2.4\jre64\lib\tools.jar

https://docs.oracle.com/javase/8/docs/technotes/tools/windows/jdkfiles.html#A1098669

Files used by the development tools. Includes tools.jar, which contains non-core classes for support of the tools and utilities in the JDK. Also includes dt.jar, the DesignTime archive of BeanInfo files that tell interactive development environments (IDEs) how to display the Java components and how to let the developer customize them for an application.

Jdk 二进制工具

Java agent

javap
反编译

jar
jarsigner
javac
javadoc
javah
javapackager
java-rmi
javaw
jcmd
jconsole

https://www.cnblogs.com/createyuan/p/11038958.html


tcp上层应用如何获取协议类型

Wireshark可以设置应用层解析的协议
Kafka，手动设置



java.util.function

JAVA8的java.util.function包
https://www.cnblogs.com/linzhanfly/p/9686941.html

https://www.jianshu.com/p/3c27dfd647f1
