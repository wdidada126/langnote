# [Spring源码深度解析](https://book.douban.com/subject/25866350/)


### XmlBeanFactory


### sax解析xml格式的bean定义文件

src.zip中的
org.xml.sax.EntityResolver



### Chap.4
p
c标签
自定义标签

在spring中存在默认标签与自定义标签两种，例如：<bean/>为默认标签，<tx:annotation-driven/>为自定义标签。spring自定义标签比较灵活，可以扩展自定义标签。
扩展spring自定义标签主要步骤： 加入spring-core包
创建一个需要扩展的组件；
定义一个XSD文件描述组件内容；
创建一个类，该类实现BeanDifinitionParser接口，主要用来解析XSD文件中的定义和组件的定义；
创建一个NamespaceHandler类，该类扩展NamespaceHandlerSupport，主要作用是将组件注册到spring的容器中；
编写spring.handlers和spring.schemas文件

[扩展spring自定义标签](https://blog.51cto.com/11623217/1775150)

获取bean流程分析

context.getBean();

如果这个类实现了factorybean方法
getObject()

ResourceLoader

获取 org.springframework.core.io.Resource
Resource张开涛

DocumentLoader 获取org.w3c.dom.Document对象



Spring学习系列
https://blog.csdn.net/soonfly/column/info/15088

java.util.Locale
国际化

Spring中用到了
org.springframework.context.MessageSource 方法中有Locale参数

org.springframework.beans.factory.Aware

Bean生命周期回调：初始化回调和销毁回调
org.springframework.beans.factory.InitializingBean接口类的作用是：在容器设置bean必须的属性之后执行初始化工作。 
InitializingBean接口中只有一个方法:void afterPropertiesSet() throws Exception; 

实现org.springframework.beans.factory.DisposableBean接口，作用是Spring销毁bean时调用该方法。 
DisposableBean接口只有一个方法:void destroy() throws Exception;


Propagation.REQUIRED

spring-tx
since 1.2

Spring事务传播级别
public enum Propagation
- REQUIRED
- SUPPORTS
- MANDATORY
- REQUIRES_NEW
- NOT_SUPPORTED
- NEVER
- NESTED

DefaultSingletonBeanRegistry.singletonObjects

BeanRegistry
AliasRegistry：用于管理bean别名的接口
BeanDefinitionRegistry：提供注册BeanDefinition的能力

Chap. 5.3 最后一段 BeanPostProcess


Chap. 6.5
自定义属性编辑器 例子
Spring xml配置Date属性是，需要有java.beans.PropertyEditorSupport子类

Chap. 6.6.1
BeanFactoryPostProcessor
BeanPostProcessor
PropertyResourceConfigurer

跑例子

bfpp
bpp


SqlSessionFactoryBean继承FactoryBean

```shell
  <bean id="sqlSessionFactory" class="org.mybatis.spring.SqlSessionFactoryBean">
    <property name="dataSource" ref="dataSource"/>
    <property name="configLocation" value="classpath:/mybatis.xml"/>
    <property name="mapperLocations">
      <list>
        <value>classpath:mapper/*.xml</value>
      </list>
    </property>
  </bean>
```


MapperFactoryBean

private Class<T> mapperInterface;

Mybatis 注入接口 


Mybatis的接口太多，一个个配置bean信息太麻烦

org.mybatis.spring.mapper.MapperFactoryBean
BeanFactoryPostProcessor?
BeanDefinitionRegistryPostProcessor?

bean配置
DataSourceTransactionManager
SpringBoot配置就是自动配置了bean


