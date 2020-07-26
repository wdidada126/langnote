# Spring源码深度解析（第2版）





Spring 5





Spring源码深度解析 书籍



http://www.importnew.com/27469.html



https://www.cnblogs.com/xrq730/p/6285358.html





Resource接口详解

继承自InputStreamSource



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





从getbean看起

AbstractBeanFactory.getBean()

AbstractBeanFactory.doGetBean()

BeanDefinitionHolder

Spring源码学习--BeanDefinitionHolder

https://blog.csdn.net/qq924862077/article/details/73558848



org.springframework.beans.factory.config.BeanDefinitionHolder;





BeanDefinitionHolder是对BeanDefinition，String beanName，String[] aliases的分装











ClassPathResource

org.springframework.core.io.ClassPathResource



http://elim.iteye.com/blog/2016305



是对String path和classloader的封装





InputStreamSource

org.springframework.core.io.InputStreamSource



InputStream getInputStream() throws IOException;







Resource

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

org.springframework.beans.factory.xml.DocumentLoader

Document loadDocument()

子类：DefaultDocumentLoader









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

