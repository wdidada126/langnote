# Spring bean

ConstructorArgumentValues
ValueHolder
String type
Object value
String name
Object source

org.springframework.beans.BeanMetadataElement
Object getSource();

Spring bean 生命周期，面试题，看源码

```java
@Component
public class ConfigProperties {

    @Value("${config.use.start:600}")
    public int start;
}
```


eclipse需要引用命名空间dtd，对xml文件进行校验



schema改为“spring-beans-2.5.xsd”





Spring容器支持的三种依赖注入的方式以及具体配置方法：

•  属性注入方法
•  构造函数注入方法
•  工厂方法注入方法





https://www.iteye.com/blog/jinnianshilongnian-1413857

bean的命名

一、  不指定id，只配置必须的全限定类名

二、指定id，必须在Ioc容器中唯一

三、指定name，这样name就是“标识符”，必须在Ioc容器中唯一

四、指定id和name，id就是标识符，而name就是别名，必须在Ioc容器中唯一



### 构造器注入

构造器注入

### setter注入
setter

### 注入常量
常量

### 注入Bean ID

id

### 处理null值

循环依赖

### 



Spring通过<null/>标签注入null值

Spring不仅支持对象的导航，还支持数组、列表、字典、Properties数据类型的导航，对Set数据类型无法支持，因为无法导航。



循环依赖


构造器循环依赖：表示通过构造器注入构成的循环依赖，此依赖是无法解决的，只能抛出BeanCurrentlyInCreationException异常表示循环依赖。







##  Bean的作用域



 什么是作用域呢？即“scope”，在面向对象程序设计中一般指对象或变量之间的可见范围。而在Spring容器中是指其创建的Bean对象相对于其他Bean对象的请求可见范围。

Spring提供“singleton”和“prototype”两种基本作用域，另外提供“request”、“session”、“global session”三种web作用域；Spring还允许用户定制自己的作用域。



一、request作用域：表示每个请求需要容器创建一个全新Bean。比如提交表单的数据必须是对每次请求新建一个Bean来保持这些表单数据，请求结束释放这些数据。

 

二、session作用域：表示每个会话需要容器创建一个全新Bean。比如对于每个用户一般会有一个会话，该用户的用户信息需要存储到会话中，此时可以将该Bean配置为web作用域。

 

三、globalSession：类似于session作用域，只是其用于portlet环境的web应用。如果在非portlet环境将视为session作用域。





Autowired
@Autowired的使用：推荐对构造函数进行注释
https://www.cnblogs.com/acm-bingzi/p/springAutowired.html

```java

@Autowired
private User user;
private String school;

public UserAccountServiceImpl(){
    this.school = user.getSchool();
}

```

Exception in thread "main" org.springframework.beans.factory.BeanCreationException: Error creating bean with name '...' defined in file [....class]: Instantiation of bean failed; nested exception is org.springframework.beans.BeanInstantiationException: Failed to instantiate [...]: Constructor threw exception; nested exception is java.lang.NullPointerException
　　报错信息说：创建Bean时出错，出错原因是实例化bean失败，因为bean时构造方法出错，在构造方法里抛出了空指针异常。

```java

private User user;
private String school;

@Autowired
public UserAccountServiceImpl(User user){
    this.user = user;
    this.school = user.getSchool();
}

```


Spring doc bean

Chap 1.6.1
Lifecycle Callbacks


@PostConstruct
@PreDestroy



interface BeanPostProcessor

Factory hook


SmartLifecycle

Lifecycle

Chap. 17
bean继承



Bean
parent

Chap.18
bean的其他定义方式


beanpostprocessor
beanfactorypostprocessor

factorybean


