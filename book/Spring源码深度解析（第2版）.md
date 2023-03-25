# Spring源码深度解析（第2版）





Spring 5





Spring源码深度解析 书籍 第二版 2019年出版的



Could not determine java version from '11.0.4'.
更换 JAVA_HOME环境变量改成java8的


spring5源码下载不了plugin jar包
报错信息
Could not GET 'https://repo.spring.io/plugins-release

解决方案
https://juejin.cn/post/7067505778353143815



set https_proxy=http://127.0.0.1:7890
set http_proxy=http://127.0.0.1:7890


cd/d D:\git\gitlab\spring-framework-5.0.x
gradlew build -x test



【Spring源码分析】Bean加载流程概览
https://www.cnblogs.com/xrq730/p/6285358.html





Resource接口详解
继承自InputStreamSource

ResourceLoader

bean

根据《spring技术内幕》

ioc容器初始化过程分为三个步骤
1、Resource定位
2、载入（BeanDefinition）
3、注册BeanDefinition



DefaultListableBeanFactory 是整个bean加载的核心部分

XmlBeanFactory 是DefaultListableBeanFactory 的子类

XmlBeanFactory 使用了XmlBeanDefinitionReader



XmlBeanDefinitionReader的构造函数

XmlBeanDefinitionReader的loadBeanDefinitions()

XmlBeanDefinitionReader的loadBeanDefinitions()

XmlBeanDefinitionReader的doLoadBeanDefinitions()

EncodedResource按照一定的格式处理xml格式的配置文件（applicationContext.xml）









XmlBeanDefinitionReader的getValidationModeForResource()方法

XmlBeanDefinitionReader的registerBeanDefinitions()方法

1、获取XML格式文件的验证模式；

2、加载XML文件，并得到对应的Document对象；

3、根据返回的Document对象注册Bean信息。



XmlBeanDefinitionReader的detectValidationMode()

XmlValidationModeDetector的detectValidationMode()方法

XmlValidationModeDetector的hasDoctype()方法



返回XmlBeanDefinitionReader的doLoadBeanDefinitions()方法来分析
DefaultDocumentLoader的loadDocument()方法
从原理上讲就是sax解析





EntityResolver接口的实现类DelegatingEntityResolver





DelegatingEntityResolver类对dtd和xsd格式的xml文件分别调用

BeansDtdResolver
PluggableSchemaResolver



XmlBeanDefinitionReader的registerBeanDefinitions()





再次返回XmlBeanDefinitionReader的doLoadBeanDefinitions()方法来分析

调用同一个类的registerBeanDefinitions()方法



BeanDefinitionDocumentReader接口的实现类DefaultBeanDefinitionDocumentReader依次调用

1、registerBeanDefinitions(Document, XmlReaderContext)方法   ----提取root对象 再次注册
2、doRegisterBeanDefinitions()方法



其中doRegisterBeanDefinitions()方法
1、处理profile属性
2、调用parseBeanDefinitions()方法



parseBeanDefinitions()方法

处理<beans>

处理<bean>









把文件转化为Document对象

默认的bean      ----- parseDefalutElement

自定义的bean   ----- parseCustomerElement



bean的属性
scope
singleton
abstract
lazy-init
autowire
dependency-check
depends-on
primay
init-method
destroy-method
factory-method
factory-bean







BeanDefinition接口的子类

RootBeanDefinition
ChildBeanDefinition
GenericBeanDefinition
AbstractBeanDefinition



BeanDefinitionRegistry



aop

aspectj





mybatis mybatis-spring

springmvc

rmi

事务 jta 

jms 不适合互联网业务





从getBean看起

AbstractBeanFactory.getBean()

AbstractBeanFactory.doGetBean()

BeanDefinitionHolder

Spring源码学习--BeanDefinitionHolder

https://blog.csdn.net/qq924862077/article/details/73558848


BeanDefinitionHolder，简单来说其就是一个BeanDefinition的持有者，其定义了一下变量，并对以下变量提供get和set操作。

private final BeanDefinition beanDefinition;
private final String beanName;
private final String[] aliases;




org.springframework.beans.factory.config.BeanDefinitionHolder;





BeanDefinitionHolder是对BeanDefinition，String beanName，String[] aliases的分装











ClassPathResource

org.springframework.core.io.ClassPathResource



http://elim.iteye.com/blog/2016305



是对String path和classloader的封装

Resource简介
在Spring内部，针对于资源文件有一个统一的接口Resource表示。其主要实现类有ClassPathResource、FileSystemResource、UrlResource、ByteArrayResource、ServletContextResource和InputStreamResource。Resource接口中主要定义有以下方法：

- exists()：用于判断对应的资源是否真的存在。
- isReadable()：用于判断对应资源的内容是否可读。需要注意的是当其结果为true的时候，其内容未必真的可读，但如果返回false，则其内容必定不可读。
- isOpen()：用于判断当前资源是否代表一个已打开的输入流，如果结果为true，则表示当前资源的输入流不可多次读取，而且在读取以后需要对它进行关闭，以防止内存泄露。该方法主要针对于InputStreamResource，实现类中只有它的返回结果为true，其他都为false。
- getURL()：返回当前资源对应的URL。如果当前资源不能解析为一个URL则会抛出异常。如ByteArrayResource就不能解析为一个URL。
- getFile()：返回当前资源对应的File。如果当前资源不能以绝对路径解析为一个File则会抛出异常。如ByteArrayResource就不能解析为一个File。
- getInputStream()：获取当前资源代表的输入流。除了InputStreamResource以外，其它Resource实现类每次调用getInputStream()方法都将返回一个全新的InputStream。

 

ClassPathResource可用来获取类路径下的资源文件。假设我们有一个资源文件test.txt在类路径下，我们就可以通过给定对应资源文件在类路径下的路径path来获取它，new ClassPathResource(“test.txt”)。
FileSystemResource可用来获取文件系统里面的资源。我们可以通过对应资源文件的文件路径来构建一个FileSystemResource。FileSystemResource还可以往对应的资源文件里面写内容，当然前提是当前资源文件是可写的，这可以通过其isWritable()方法来判断。FileSystemResource对外开放了对应资源文件的输出流，可以通过getOutputStream()方法获取到。
UrlResource可用来代表URL对应的资源，它对URL做了一个简单的封装。通过给定一个URL地址，我们就能构建一个UrlResource。
ByteArrayResource是针对于字节数组封装的资源，它的构建需要一个字节数组。
ServletContextResource是针对于ServletContext封装的资源，用于访问ServletContext环境下的资源。ServletContextResource持有一个ServletContext的引用，其底层是通过ServletContext的getResource()方法和getResourceAsStream()方法来获取资源的。
InputStreamResource是针对于输入流封装的资源，它的构建需要一个输入流。

在Spring里面还定义有一个ResourceLoader接口，该接口中只定义了一个用于获取Resource的getResource(String location)方法。它的实现类有很多，这里我们先挑一个DefaultResourceLoader来讲。




InputStreamSource

org.springframework.core.io.InputStreamSource



InputStream getInputStream() throws IOException;







Resource
对应src/main/resource 文件夹

org.springframework.core.io.Resource



interface Resource extends InputStreamSource 



常用子类有：1、FileSystemResource；2、ClassPathResource；3、UrlResource；4、InputStreamResource；5、ByteArrayResource vfsResources





Aware

org.springframework.beans.factory.Aware

回调











Spring实现Aware接口，完成对IOC容器的感知

https://blog.csdn.net/ilovejava_2010/article/details/7953582



1、BeanNameAware，可以在Bean中得到它在IOC容器中的Bean的实例的名字。
2、BeanFactoryAware，可以在Bean中得到Bean所在的IOC容器，从而直接在Bean中使用IOC容器的服务。
3、ApplicationContextAware，可以在Bean中得到Bean所在的应用上下文，从而直接在Bean中使用上下文的服务。
4、MessageSourceAware，在Bean中可以得到消息源。
5、ApplicationEventPublisherAware，在bean中可以得到应用上下文的事件发布器，从而可以在Bean中发布应用上下文的事件。

ResourceLoaderAware，在Bean中可以得到ResourceLoader，从而在bean中使用ResourceLoader加载外部对应的Resource资源。







DocumentLoader
Spring4.3.x 浅析xml配置的解析过程（3）——使用DocumentLoader创建Document对象


org.springframework.beans.factory.xml.DocumentLoader

Document loadDocument()

子类：DefaultDocumentLoader

DefaultDocumentLoader是DocumentLoader的实现类

在 XmlBeanDefinitionReader.doLoadDocument() 方法中做了两件事情，一是调用 getValidationModeForResource() 获取 XML 的验证模式，二是调用 DocumentLoader.loadDocument() 获取 Document 对象。

解析Docuemnt转换为BeanDefinition
资源resource 转换为Document的流程 在XmlBeanDefinitionReader 类的doLoadBeanDefinitions()方法

//将对应资源转换为Document对象
Document doc = doLoadDocument(inputSource, resource);
//解析doc中的属性转换为BeanDefinition对象 并注册在spring容器中
return registerBeanDefinitions(doc, resource);
registerBeanDefinitions(doc,resource)则对应接下来的主题解析document对象 并将其转换为BeanDefinitions()


BeanDefinition的实现类用于描述Spring中的一个应该被实例化的bean的各种性质，包括bean的属性值，构造函数，方法等信息，除此之外，还额外描述bean在Spring容器中的作用域，bean名称等信息。






DelegatingEntityResolver

属性systemId的取值有一下两种：

public static final String DTD_SUFFIX = ".dtd";

public static final String XSD_SUFFIX = ".xsd";

Spring中使用DelegatingEntityResolver作为EntityResolver的实现类





BeansDtdResolver



PluggableSchemaResolver





BeanDefinitionDocumentReader

registerBeanDefinitions()

实现类DefaultBeanDefinitionDocumentReader

DefaultBeanDefinitionDocumentReader的doRegisterBeanDefinitions方法



protected void doRegisterBeanDefinitions(Element root){

​	

}



parseBeanDefinitions()



解析xml文件 获取Document对象





Spring3自定义环境配置  beans profile











BeanWapper



PropertyValue

PropertyValues





BeanPostProcessor




### 自己补充的部分

ApplicationContext

可以获取bean name

```java
        String[] names = applicationContext.getBeanDefinitionNames();
        for (String name : names) {
            System.out.println(">>>>>>" + name);
        }
        System.out.println("------\nBean 总计:" + applicationContext.getBeanDefinitionCount());
```

横向对比
guice这种ioc框架，如何打印容器中的数据





| **对象名**                  | **类  型**                     | **作  用**                                                   | **归属类**                                  |
| --------------------------- | ------------------------------ | ------------------------------------------------------------ | ------------------------------------------- |
| configResources             | Resource[]                     | 配置文件资源对象数组                                         | ClassPathXmlApplicationContext              |
| configLocations             | String[]                       | 配置文件字符串数组，存储配置文件路径                         | AbstractRefreshableConfigApplicationContext |
| beanFactory                 | DefaultListableBeanFactory     | 上下文使用的Bean工厂                                         | AbstractRefreshableApplicationContext       |
| beanFactoryMonitor          | Object                         | Bean工厂使用的同步监视器                                     | AbstractRefreshableApplicationContext       |
| id                          | String                         | 上下文使用的唯一Id，标识此ApplicationContext                 | AbstractApplicationContext                  |
| parent                      | ApplicationContext             | 父级ApplicationContext                                       | AbstractApplicationContext                  |
| beanFactoryPostProcessors   | List<BeanFactoryPostProcessor> | 存储BeanFactoryPostProcessor接口，Spring提供的一个扩展点     | AbstractApplicationContext                  |
| startupShutdownMonitor      | Object                         | refresh方法和destory方法公用的一个监视器，避免两个方法同时执行 | AbstractApplicationContext                  |
| shutdownHook                | Thread                         | Spring提供的一个钩子，JVM停止执行时会运行Thread里面的方法    | AbstractApplicationContext                  |
| resourcePatternResolver     | ResourcePatternResolver        | 上下文使用的资源格式解析器                                   | AbstractApplicationContext                  |
| lifecycleProcessor          | LifecycleProcessor             | 用于管理Bean生命周期的生命周期处理器接口                     | AbstractApplicationContext                  |
| messageSource               | MessageSource                  | 用于实现国际化的一个接口                                     | AbstractApplicationContext                  |
| applicationEventMulticaster | ApplicationEventMulticaster    | Spring提供的事件管理机制中的事件多播器接口                   | AbstractApplicationContext                  |
| applicationListeners        | Set<ApplicationListener>       | Spring提供的事件管理机制中的应用监听器                       | AbstractApplicationContext                  |