# java spi



[高级开发必须理解的Java中SPI机制](https://www.jianshu.com/p/46b42f7f593c)



https://www.jianshu.com/u/ced6b70c7fc5





Java SPI 实际上是“**基于接口的编程＋策略模式＋配置文件**”组合实现的动态加载机制。



<<<<<<< HEAD
#### 2 使用场景
=======
# 2 使用场景
>>>>>>> afe522da082020e5ece0b75c43067644b2edb768

概括地说，适用于：**调用者根据实际使用需要，启用、扩展、或者替换框架的实现策略**

比较常见的例子：

- 数据库驱动加载接口实现类的加载
   JDBC加载不同类型数据库的驱动
- 日志门面接口实现类加载
   SLF4J加载不同提供商的日志实现类
- Spring
   Spring中大量使用了SPI,比如：对servlet3.0规范对ServletContainerInitializer的实现、自动类型转换Type Conversion SPI(Converter SPI、Formatter SPI)等
- Dubbo
   Dubbo中也大量使用SPI的方式实现框架的扩展, 不过它对Java提供的原生SPI做了封装，允许用户扩展实现Filter接口



Java中的SPI扩展机制

https://www.cnblogs.com/hy-xiaobin/p/12204849.html


https://github.com/edidada/java-spi-demo


java.util.ServiceLoader
static java.util.ServiceLoader#load(java.lang.Class<S>)

java.lang.Iterable

ServiceLoader实现了java.lang.Iterable

接口文件名按行换，可以有多个实现类

META-INF.services
接口名就是文件名
文件内容就是实现类全路径名称


ServiceLoader原理





Dubbo SPI改进








