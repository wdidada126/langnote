# BeanDefinitionHolder


Spring源码学习--BeanDefinitionHolder
https://blog.csdn.net/qq924862077/article/details/73558848
org.springframework.beans.factory.config.BeanDefinitionHolder;
BeanDefinitionHolder是对BeanDefinition，String beanName，String[] aliases的封装
抽象类中可以没有抽象方法，但有抽象方法的一定是抽象类。



## ClassPathResource

org.springframework.core.io.ClassPathResource
http://elim.iteye.com/blog/2016305
是对String path和classloader的封装
InputStreamSource
org.springframework.core.io.InputStreamSource
InputStream getInputStream() throws IOException;

## Resource
org.springframework.core.io.Resource
interface Resource extends InputStreamSource 

常用子类有：1、FileSystemResource；2、ClassPathResource；3、UrlResource；4、InputStreamResource；5、ByteArrayResource

## Aware
org.springframework.beans.factory.Aware
Spring实现Aware接口，完成对IOC容器的感知
https://blog.csdn.net/ilovejava_2010/article/details/7953582
BeanNameAware，可以在Bean中得到它在IOC容器中的Bean的实例的名字。
BeanFactoryAware，可以在Bean中得到Bean所在的IOC容器，从而直接在Bean中使用IOC容器的服务。
ApplicationContextAware，可以在Bean中得到Bean所在的应用上下文，从而直接在Bean中使用上下文的服务。
MessageSourceAware，在Bean中可以得到消息源。
ApplicationEventPublisherAware，在bean中可以得到应用上下文的事件发布器，从而可以在Bean中发布应用上下文的事件。
ResourceLoaderAware，在Bean中可以得到ResourceLoader，从而在bean中使用ResourceLoader加载外部对应的Resource资源。

## DocumentLoader
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
	
}

parseBeanDefinitions()

解析xml文件 获取Document对象

Spring3自定义环境配置  beans profile




## AliasRegistry
操作别名

DefaultListableBeanFactory实现BeanDefinitionRegistry

import org.springframework.beans.factory.BeanDefinitionStoreException;
import org.springframework.beans.factory.NoSuchBeanDefinitionException;
import org.springframework.beans.factory.config.BeanDefinition;
import org.springframework.beans.factory.support.BeanDefinitionRegistry;

    public class MyBeanDefinitionRegistry implements BeanDefinitionRegistry {
    @Override
    public void registerBeanDefinition(String beanName, BeanDefinition beanDefinition) throws BeanDefinitionStoreException {

    }

    @Override
    public void removeBeanDefinition(String beanName) throws NoSuchBeanDefinitionException {

    }

    @Override
    public BeanDefinition getBeanDefinition(String beanName) throws NoSuchBeanDefinitionException {
        return null;
    }

    @Override
    public boolean containsBeanDefinition(String beanName) {
        return false;
    }

    @Override
    public String[] getBeanDefinitionNames() {
        return new String[0];
    }

    @Override
    public int getBeanDefinitionCount() {
        return 0;
    }

    @Override
    public boolean isBeanNameInUse(String beanName) {
        return false;
    }

    @Override
    public void registerAlias(String name, String alias) {

    }

    @Override
    public void removeAlias(String alias) {

    }

    @Override
    public boolean isAlias(String name) {
        return false;
    }

    @Override
    public String[] getAliases(String name) {
        return new String[0];
    }
}

BeanDefinitionParserDelegate会处理”http://www.springframework.org/schema/beans“命名空间下元素及其属性,查看源码可以看到BeanDefinitionParserDelegate下面定义了一堆元素和属性名称,这些元素和属性名称分别可以在类中找到处理方法.

