# Spring


<init-method>效果跟实现InitializingBean接口是一样的吗？
在Spring中，<init-method>标签和实现InitializingBean接口都可以用来指定Bean初始化之后执行的方法，但是它们的实现方式和用途是有些不同的。

spring ioc中的bean，创建好之后执行特定方法

```java
public class MyBean implements InitializingBean {

    @Override
    public void afterPropertiesSet() throws Exception {
        // 在这里进行初始化操作
    }
}
```

在 Spring 的 XML 配置文件中，如果你需要在 Bean 创建好之后执行特定方法，可以使用 Spring 提供的 `<init-method>` 和 `<destroy-method>` 元素。
1. `<init-method>` 元素：该元素用于指定 Bean 创建完成后要执行的初始化方法。你可以在该方法中进行一些初始化操作，例如初始化成员变量、连接数据库等。例如：
```
<bean id="myBean" class="com.example.MyBean" init-method="init">
    <!-- 在这里进行其他配置 -->
</bean>
```
在这个例子中，我们定义了一个名为 `myBean` 的 Bean，并使用 `<init-method>` 元素指定了一个名为 `init()` 的方法。在该方法中，我们可以进行一些初始化操作，例如初始化成员变量、连接数据库等。
2. `<destroy-method>` 元素：该元素用于指定 Bean 销毁之前要执行的清理方法。你可以在该方法中进行一些清理操作，例如关闭数据库连接、释放资源等。例如：
```
<bean id="myBean" class="com.example.MyBean" destroy-method="cleanup">
    <!-- 在这里进行其他配置 -->
</bean>
```
在这个例子中，我们定义了一个名为 `myBean` 的 Bean，并使用 `<destroy-method>` 元素指定了一个名为 `cleanup()` 的方法。在该方法中，我们可以进行一些清理操作，例如关闭数据库连接、释放资源等。
需要注意的是，使用 `<init-method>` 和 `<destroy-method>` 元素将使你的 Bean 与 Spring 框架产生强耦合。如果你想使你的 Bean 更加独立和可重用，可以使用 Spring 提供的注解来实现。
例如，你可以使用 `@PostConstruct` 注解来指定一个方法，在 Bean 创建好之后立即执行。例如：

```
public class MyBean {

    @PostConstruct
    public void init() {
        // 在这里进行初始化操作
    }
}
```

在这个例子中，我们定义了一个名为 `MyBean` 的 Bean，并使用 `@PostConstruct` 注解指定了一个名为 `init()` 的方法。在该方法中，我们可以进行一些初始化操作，例如初始化成员变量、连接数据库等。
类似地，你可以使用 `@PreDestroy` 注解来指定一个方法，在 Bean 销毁之前执行。例如：

```
public class MyBean {

    @PreDestroy
    public void cleanup() {
        // 在这里进行清理操作
    }
}
```

在这个例子中，我们定义了一个名为 `MyBean` 的 Bean，并使用 `@PreDestroy` 注解指定了一个名为 `cleanup()` 的方法。在该方法中，我们可以进行一些清理操作，例如关闭数据库连接、释放资源等。
总之，在 Spring 的 XML 配置文件中，如果你需要在 Bean 创建好之后执行特定方法，可以使用 `<init-method>` 和 `<destroy-method>` 元素。如果你想使你的 Bean 更加独立和可重用，可以使用 Spring 提供的注解来实现。



https://gitee.com/edidada/summer-framework

廖雪峰 自己写spring
https://www.liaoxuefeng.com/wiki/1539348902182944

![bean生命周期](D:\git\github\langnote\imgs\spring\bean生命周期.png)



![Spring 容器中的bean的生命周期](D:\git\github\langnote\imgs\spring\Spring 容器中的bean的生命周期.png)




Spring 对bean 进行实例化。
  Spring 将值和bean的引用注入到bean对应的属性中。
  如果bean实现了BeanNameAware接口，Spring将bean的ID传递给setBean-Name()  方法。
  如果bean 实现了BeanFactoryAware接口，Spring将调用setBeanFactory() 方法，将BeanFactory容器实例传入。
  如果bean实现了ApplicationContextAware接口，Spring将调用setApplicationContext() 方法，将bean所在的应用上下文的引用传入进来。
  如果bean实现了BeanPostProcessor接口，Spring将调用它们的post-ProcessBeforeInitialization() 方法
  如果bean实现了InitializingBean接口，Spring将调用它们的after-PropertiesSet()方法。类似的，如果bean使用init-method声明了初始化方法，该方法也会被调用。
  如果bean实现了BeanPostProcessor接口，Spring将调用它们的post-ProcessAfterInitialization() 方法。
  此时, bean 已经准备就绪，可以被应用程序使用了，它们将一直驻留在应用上下文中，直到该应用上下文被销毁。
  如果bean实现了DisposableBean接口，Spring将调用它的destory()接口方法。同样,如果bean使用destroy-method声明了销毁方法，该方法也会被调用。


https://www.cnblogs.com/misscai/p/14749225.html


### bean属性及子元素使用总结 13属性 6子元素

bean标签
标签属性
id
id是bean的唯一标识符，在spring容器中不可能同时存在两个相同的id；
class
类的全限定名（包名+类名），用“.”号连接；
name
别名（alias），用法：getBean("name")，支持设置多个别名，之间用英文逗号分割；
abstract
设置bean是否为抽象类，默认abstract="false",如果设为true，将不能被实例化；
autowire-candidate
默认为true，如果为false，那么该bean不能作为其他bean自动装配的候选者。

autowire
default（默认）：采用父级标签beans中的default-autowire属性；
byName：通过属性名称来自动装配，即A类中的B对象名称为name，那么将根据id="name"找到该bean进行装配，A类必须提供setName方法；
byType：根据属性类型来找到和配置文件中配置的class类型一致的bean来自动装配，如果找到多个类型一致的bean，则抛异常，如果一个都没有找到，则不执行装配操作，也不抛出异常。
no：不执行自动装配操作，只能用<ref>标签进行装配；
constructor：根据构造器中参数类型来自动装配，如果找到多个类型一致的bean，则抛异常，如果一个都没有找到，则不执行装配操作，但是抛出异常（这是和byType不一样的地方）。
“autodetect”（spring3之前有该值，从spring4开始该值被抛弃）:通过Bean类的反省机制（introspection）决定是使用“constructor”还是使用“byType”。
depends-on
它的作用是一个bean实例化的过程需要依赖于另一个bean的初始化，也就是说被依赖的bean将会在需要依赖的bean初始化之前加载。多个依赖bean之间用","号分割；
destroy-method
它的作用是在销毁bean之前可以执行指定的方法。注意：必须满足scope="singleton"，并且destroy方法参数个数不能超过1，并且参数类型只能为boolean。
init-method
它的作用是在创建一个bean之后调用该方法，初始化方法必须是一个无参方法。
factory-bean和factory-method
设置了factory-bean属性后，将指定创建bean的工厂类对象，class属性将失效；
lazy-init
设置bean对象是否懒加载，如果设为true，则应用第一次用到bean时才实例化对象，否则在初始化spring容器时加载单例bean对象。（非单例不实例化）
parent
指定bean的父类，class属性失效。
primary
当一个bean出现多个候选者时，设置primary="true"后，则优先使用该bean来自动装配。

scope
bean的作用范围，它包括
singleton：单例，指定该bean在spring容器中只有一个对象，所有通过getBean获得的对象都是同一个对象。
prototype：只要重新获取该bean，都将返回一个不同的对象。
request：在一次http请求中对应一个bean，类似于servlet
session：在一次会话中对应一个bean。


子标签属性
<meta>
<lookup-method>
<replaced-method>
<constructor-arg>
<property>
<qualifier>









https://github.com/edidada/SpringExample

PropertyPlaceholderConfigurer是Spring框架中的一个类，它是用来解析properties文件的。在Spring中，我们可以使用${}或#{}来引用properties文件中的值。这个类就是用来解析这些占位符的。如果你想深入了解这个类的实现，可以参考这篇博客：1。已收到消息.PropertyPlaceholderConfigurer是Spring框架中的一个类，它是用来解析properties文件的。在Spring中，我们可以使用${}或#{ }来引用properties文件中的值。这个类就是用来解析这些占位符的。如果你想深入了解这个类的实现，可以参考这篇博客：。
了解详细信息:
https://www.cnblogs.com/juniorMa/p/14323883.html


https://www.docs4dev.com/docs/zh/spring-framework/4.3.21.RELEASE/reference/aop.html

张开涛 跟我学Spring3 系列博客
跟我学spring 用的是spring3

Spring实战

Spring 3.x企业开发实战




1. 什么是spring?Spring 是个java企业级应用的开源开发框架。Spring主要用来开发Java应用，但是有些扩展是针对构建J2EE平台的web应用。Spring 框架目标是简化Java企业级应用开发，并通过POJO为基础的编程模型促进良好的编程习惯。
2. 使用Spring框架的好处是什么？轻量：Spring 是轻量的，基本的版本大约2MB。控制反转：Spring通过控制反转实现了松散耦合，对象们给出它们的依赖，而不是创建或查找依赖的对象们。面向切面的编程(AOP)：Spring支持面向切面的编程，并且把应用业务逻辑和系统服务分开。容器：Spring 包含并管理应用中对象的生命周期和配置。MVC框架：Spring的WEB框架是个精心设计的框架，是Web框架的一个很好的替代品。事务管理：Spring 提供一个持续的事务管理接口，可以扩展到上至本地事务下至全局事务（JTA）。异常处理：Spring 提供方便的API把具体技术相关的异常（比如由JDBC，Hibernate or JDO抛出的）转化为一致的unchecked 异常。
3. Spring由哪些模块组成?以下是Spring 框架的基本模块：Core moduleBean moduleContext moduleExpression Language moduleJDBC moduleORM moduleOXM moduleJava Messaging Service(JMS) moduleTransaction moduleWeb moduleWeb-Servlet moduleWeb-Struts moduleWeb-Portlet module
4. 核心容器（应用上下文) 模块。这是基本的Spring模块，提供spring 框架的基础功能，BeanFactory 是 任何以spring为基础的应用的核心。Spring 框架建立在此模块之上，它使Spring成为一个容器。
5. BeanFactory – BeanFactory 实现举例。Bean 工厂是工厂模式的一个实现，提供了控制反转功能，用来把应用的配置和依赖从正真的应用代码中分离。最常用的BeanFactory 实现是XmlBeanFactory 类。
6. XMLBeanFactory最常用的就是org.springframework.beans.factory.xml.XmlBeanFactory ，它根据XML文件中的定义加载beans。该容器从XML 文件读取配置元数据并用它去创建一个完全配置的系统或应用。
7. 解释AOP模块AOP模块用于发给我们的Spring应用做面向切面的开发， 很多支持由AOP联盟提供，这样就确保了Spring和其他AOP框架的共通性。这个模块将元数据编程引入Spring。
8. 解释JDBC抽象和DAO模块。通过使用JDBC抽象和DAO模块，保证数据库代码的简洁，并能避免数据库资源错误关闭导致的问题，它在各种不同的数据库的错误信息之上，提供了一个统一的异常访问层。它还利用Spring的AOP 模块给Spring应用中的对象提供事务管理服务。
9. 解释对象/关系映射集成模块。Spring 通过提供ORM模块，支持我们在直接JDBC之上使用一个对象/关系映射映射(ORM)工具，Spring 支持集成主流的ORM框架，如Hiberate,JDO和 iBATIS SQL Maps。Spring的事务管理同样支持以上所有ORM框架及JDBC。
10. 解释WEB 模块。Spring的WEB模块是构建在application context 模块基础之上，提供一个适合web应用的上下文。这个模块也包括支持多种面向web的任务，如透明地处理多个文件上传请求和程序级请求参数的绑定到你的业务对象。它也有对Jakarta Struts的支持。
11. Spring配置文件Spring配置文件是个XML 文件，这个文件包含了类信息，描述了如何配置它们，以及如何相互调用。
12. 什么是Spring IOC 容器？Spring IOC 负责创建对象，管理对象（通过依赖注入（DI），装配对象，配置对象，并且管理这些对象的整个生命周期。
13. 你可以在Spring中注入一个null 和一个空字符串吗？可以。
14. IOC的优点是什么？IOC 或 依赖注入把应用的代码量降到最低。它使应用容易测试，单元测试不再需要单例和JNDI查找机制。最小的代价和最小的侵入性使松散耦合得以实现。IOC容器支持加载服务时的饿汉式初始化和懒加载。
15. ApplicationContext通常的实现是什么?FileSystemXmlApplicationContext ：此容器从一个XML文件中加载beans的定义，XML Bean 配置文件的全路径名必须提供给它的构造函数。ClassPathXmlApplicationContext：此容器也从一个XML文件中加载beans的定义，这里，你需要正确设置classpath因为这个容器将在classpath里找bean配置。WebXmlApplicationContext：此容器加载一个XML文件，此文件定义了一个WEB应用的所有bean。
16. Bean 工厂和 Application contexts 有什么区别？Application contexts提供一种方法处理文本消息，一个通常的做法是加载文件资源（比如镜像），它们可以向注册为监听器的bean发布事件。另外，在容器或容器内的对象上执行的那些不得不由bean工厂以程序化方式处理的操作，可以在Application contexts中以声明的方式处理。Application contexts实现了MessageSource接口，该接口的实现以可插拔的方式提供获取本地化消息的方法。
17. 一个Spring的应用看起来象什么？一个定义了一些功能的接口。这实现包括属性，它的Setter ， getter 方法和函数等。Spring AOP。Spring 的XML 配置文件。使用以上功能的客户端程序。
18. 什么是Spring的依赖注入？依赖注入，是IOC的一个方面，是个通常的概念，它有多种解释。这概念是说你不用创建对象，而只需要描述它如何被创建。你不在代码里直接组装你的组件和服务，但是要在配置文件里描述哪些组件需要哪些服务，之后一个容器（IOC容器）负责把他们组装起来。
19. 有哪些不同类型的IOC（依赖注入）方式？构造器依赖注入：构造器依赖注入通过容器触发一个类的构造器来实现的，该类有一系列参数，每个参数代表一个对其他类的依赖。Setter方法注入：Setter方法注入是容器通过调用无参构造器或无参static工厂 方法实例化bean之后，调用该bean的setter方法，即实现了基于setter的依赖注入。
20. 哪种依赖注入方式你建议使用，构造器注入，还是 Setter方法注入？你两种依赖方式都可以使用，构造器注入和Setter方法注入。最好的解决方案是用构造器参数实现强制依赖，setter方法实现可选依赖。

21.什么是Spring beans?Spring beans 是那些形成Spring应用的主干的java对象。它们被Spring IOC容器初始化，装配，和管理。这些beans通过容器中配置的元数据创建。比如，以XML文件中<bean/> 的形式定义。Spring 框架定义的beans都是单件beans。在bean tag中有个属性”singleton”，如果它被赋为TRUE，bean 就是单件，否则就是一个 prototype bean。默认是TRUE，所以所有在Spring框架中的beans 缺省都是单件。
22. 一个 Spring Bean 定义 包含什么？一个Spring Bean 的定义包含容器必知的所有配置元数据，包括如何创建一个bean，它的生命周期详情及它的依赖。
23. 如何给Spring 容器提供配置元数据?这里有三种重要的方法给Spring 容器提供配置元数据。XML配置文件。基于注解的配置。基于java的配置。
24. 你怎样定义类的作用域?当定义一个<bean> 在Spring里，我们还能给这个bean声明一个作用域。它可以通过bean 定义中的scope属性来定义。如，当Spring要在需要的时候每次生产一个新的bean实例，bean的scope属性被指定为prototype。另一方面，一个bean每次使用的时候必须返回同一个实例，这个bean的scope 属性 必须设为 singleton。
25. 解释Spring支持的几种bean的作用域。Spring框架支持以下五种bean的作用域：singleton: bean在每个Spring ioc 容器中只有一个实例。prototype：一个bean的定义可以有多个实例。request：每次http请求都会创建一个bean，该作用域仅在基于web的Spring ApplicationContext情形下有效。session：在一个HTTP Session中，一个bean定义对应一个实例。该作用域仅在基于web的Spring ApplicationContext情形下有效。global-session：在一个全局的HTTP Session中，一个bean定义对应一个实例。该作用域仅在基于web的Spring ApplicationContext情形下有效。缺省的Spring bean 的作用域是Singleton.
26. Spring框架中的单例bean是线程安全的吗?不，Spring框架中的单例bean不是线程安全的。
27. 解释Spring框架中bean的生命周期。Spring容器 从XML 文件中读取bean的定义，并实例化bean。Spring根据bean的定义填充所有的属性。如果bean实现了BeanNameAware 接口，Spring 传递bean 的ID 到 setBeanName方法。如果Bean 实现了 BeanFactoryAware 接口， Spring传递beanfactory 给setBeanFactory 方法。如果有任何与bean相关联的BeanPostProcessors，Spring会在postProcesserBeforeInitialization()方法内调用它们。如果bean实现IntializingBean了，调用它的afterPropertySet方法，如果bean声明了初始化方法，调用此初始化方法。如果有BeanPostProcessors 和bean 关联，这些bean的postProcessAfterInitialization() 方法将被调用。如果bean实现了 DisposableBean，它将调用destroy()方法。
28. 哪些是重要的bean生命周期方法？ 你能重载它们吗？有两个重要的bean 生命周期方法，第一个是setup ， 它是在容器加载bean的时候被调用。第二个方法是 teardown 它是在容器卸载类的时候被调用。The bean 标签有两个重要的属性（init-method和destroy-method）。用它们你可以自己定制初始化和注销方法。它们也有相应的注解（@PostConstruct和@PreDestroy）。
29. 什么是Spring的内部bean？当一个bean仅被用作另一个bean的属性时，它能被声明为一个内部bean，为了定义inner bean，在Spring 的 基于XML的 配置元数据中，可以在 <property/>或 <constructor-arg/> 元素内使用<bean/> 元素，内部bean通常是匿名的，它们的Scope一般是prototype。
30. 在 Spring中如何注入一个java集合？Spring提供以下几种集合的配置元素：<list>类型用于注入一列值，允许有相同的值。<set> 类型用于注入一组值，不允许有相同的值。<map> 类型用于注入一组键值对，键和值都可以为任意类型。<props>类型用于注入一组键值对，键和值都只能为String类型。
31. 什么是bean装配?装配，或bean 装配是指在Spring 容器中把bean组装到一起，前提是容器需要知道bean的依赖关系，如何通过依赖注入来把它们装配到一起。32. 什么是bean的自动装配？Spring 容器能够自动装配相互合作的bean，这意味着容器不需要<constructor-arg>和<property>配置，能通过Bean工厂自动处理bean之间的协作。33. 解释不同方式的自动装配 。有五种自动装配的方式，可以用来指导Spring容器用自动装配方式来进行依赖注入。no：默认的方式是不进行自动装配，通过显式设置ref 属性来进行装配。byName：通过参数名 自动装配，Spring容器在配置文件中发现bean的autowire属性被设置成byname，之后容器试图匹配、装配和该bean的属性具有相同名字的bean。byType：通过参数类型自动装配，Spring容器在配置文件中发现bean的autowire属性被设置成byType，*之后容器试图匹配、装配和该bean的属性具有相同类型的bean。如果有多个bean符合条件，则抛出错误。constructor：这个方式类似于byType， 但是要提供给构造器参数，如果没有确定的带参数的构造器参数类型，将会抛出异常。autodetect：首先尝试使用constructor来自动装配，如果无法工作，则使用byType方式。34.自动装配有哪些局限性 ?自动装配的局限性是：重写： 你仍需用 <constructor-arg>和 <property> 配置来定义依赖，意味着总要重写自动装配。基本数据类型：你不能自动装配简单的属性，如基本数据类型，String字符串，和类。模糊特性：自动装配不如显式装配精确，如果有可能，建议使用显式装配。



**35. @RequestMapping 注解**

该注解是用来映射一个URL到一个类或一个特定的方处理法上。

**36. 什么是基于Java的Spring注解配置? 给一些注解的例子.**

基于Java的配置，允许你在少量的Java注解的帮助下，进行你的大部分Spring配置而非通过XML文件。

以@Configuration 注解为例，它用来标记类可以当做一个bean的定义，被Spring IOC容器使用。另一个例子是@Bean注解，它表示此方法将要返回一个对象，作为一个bean注册进Spring应用上下文。

**37. 什么是基于注解的容器配置?**

相对于XML文件，注解型的配置依赖于通过字节码元数据装配组件，而非尖括号的声明。

开发者通过在相应的类，方法或属性上使用注解的方式，直接组件类中进行配置，而不是使用xml表述bean的装配关系。

**38. 怎样开启注解装配？**

注解装配在默认情况下是不开启的，为了使用注解装配，我们必须在Spring配置文件中配置 <context:annotation-config/>元素。

**39. @Required 注解**

这个注解表明bean的属性必须在配置的时候设置，通过一个bean定义的显式的属性值或通过自动装配，若@Required注解的bean属性未被设置，容器将抛出BeanInitializationException。

**40. @Autowired 注解**

@Autowired 注解提供了更细粒度的控制，包括在何处以及如何完成自动装配。它的用法和@Required一样，修饰setter方法、构造器、属性或者具有任意名称和/或多个参数的PN方法。

**41. @Qualifier 注解**

当有多个相同类型的bean却只有一个需要自动装配时，将@Qualifier 注解和@Autowire 注解结合使用以消除这种混淆，指定需要装配的确切的bean。

**42.在Spring框架中如何更有效地使用JDBC?**

使用SpringJDBC 框架，资源管理和错误处理的代价都会被减轻。所以开发者只需写statements 和 queries从数据存取数据，JDBC也可以在Spring框架提供的模板类的帮助下更有效地被使用，这个模板叫JdbcTemplate （例子见这里here）

**43. JdbcTemplate**

JdbcTemplate 类提供了很多便利的方法解决诸如把数据库数据转变成基本数据类型或对象，执行写好的或可调用的数据库操作语句，提供自定义的数据错误处理。

**44. Spring对DAO的支持**

Spring对数据访问对象（DAO）的支持旨在简化它和数据访问技术如JDBC，Hibernate or JDO 结合使用。这使我们可以方便切换持久层。编码时也不用担心会捕获每种技术特有的异常。

**45. 使用Spring通过什么方式访问Hibernate?**

在Spring中有两种方式访问Hibernate：

控制反转 Hibernate Template和 Callback。
继承 HibernateDAOSupport提供一个AOP 拦截器。

**46. Spring支持的ORM**

Spring支持以下ORM：

- Hibernate
- iBatis
- JPA (Java Persistence API)
- TopLink
- JDO (Java Data Objects)
- OJB

**47.如何通过HibernateDaoSupport将Spring和Hibernate结合起来？**

用Spring的 SessionFactory 调用 LocalSessionFactory。集成过程分三步：

配置the Hibernate SessionFactory。
继承HibernateDaoSupport实现一个DAO。
在AOP支持的事务中装配。

**48. Spring支持的事务管理类型**

Spring支持两种类型的事务管理：

- 编程式事务管理：这意味你通过编程的方式管理事务，给你带来极大的灵活性，但是难维护。
- 声明式事务管理：这意味着你可以将业务代码和事务管理分离，你只需用注解和XML配置来管理事务。

**49. Spring框架的事务管理有哪些优点？**

- 它为不同的事务API 如 JTA，JDBC，Hibernate，JPA 和JDO，提供一个不变的编程模式。
- 它为编程式事务管理提供了一套简单的API而不是一些复杂的事务API如
- 它支持声明式事务管理。
- 它和Spring各种数据访问抽象层很好得集成。

**50. 你更倾向用那种事务管理类型？**

大多数Spring框架的用户选择声明式事务管理，因为它对应用代码的影响最小，因此更符合一个无侵入的轻量级容器的思想。声明式事务管理要优于编程式事务管理，虽然比编程式事务管理（这种方式允许你通过代码控制事务）少了一点灵活性。

**51. 解释AOP**

面向切面的编程，或AOP， 是一种编程技术，允许程序模块化横向切割关注点，或横切典型的责任划分，如日志和事务管理。

**52. Aspect 切面**

AOP核心就是切面，它将多个类的通用行为封装成可重用的模块，该模块含有一组API提供横切功能。比如，一个日志模块可以被称作日志的AOP切面。根据需求的不同，一个应用程序可以有若干切面。在Spring AOP中，切面通过带有@Aspect注解的类实现。

**53. 在Spring AOP 中，关注点和横切关注的区别是什么？**

关注点是应用中一个模块的行为，一个关注点可能会被定义成一个我们想实现的一个功能。

横切关注点是一个关注点，此关注点是整个应用都会使用的功能，并影响整个应用，比如日志，安全和数据传输，几乎应用的每个模块都需要的功能。因此这些都属于横切关注点。

**54. 连接点**

连接点代表一个应用程序的某个位置，在这个位置我们可以插入一个AOP切面，它实际上是个应用程序执行Spring AOP的位置。

**55. 通知**

通知是个在方法执行前或执行后要做的动作，实际上是程序执行时要通过SpringAOP框架触发的代码段。

Spring切面可以应用五种类型的通知：

- before：前置通知，在一个方法执行前被调用。
- after: 在方法执行之后调用的通知，无论方法执行是否成功。
- after-returning: 仅当方法成功完成后执行的通知。
- after-throwing: 在方法抛出异常退出时执行的通知。
- around: 在方法执行之前和之后调用的通知。

**56. 切点**

切入点是一个或一组连接点，通知将在这些位置执行。可以通过表达式或匹配的方式指明切入点。

**57. 什么是引入?**

引入允许我们在已存在的类中增加新的方法和属性。

**58. 什么是目标对象?**

被一个或者多个切面所通知的对象。它通常是一个代理对象。也指被通知（advised）对象。

**59. 什么是代理?**

代理是通知目标对象后创建的对象。从客户端的角度看，代理对象和目标对象是一样的。

**60. 有几种不同类型的自动代理？**

BeanNameAutoProxyCreator

DefaultAdvisorAutoProxyCreator

Metadata autoproxying

**61. 什么是织入。什么是织入应用的不同点？**

织入是将切面和到其他应用类型或对象连接或创建一个被通知对象的过程。

织入可以在编译时，加载时，或运行时完成。

**62. 解释基于XML Schema方式的切面实现。**

在这种情况下，切面由常规类以及基于XML的配置实现。

**63. 解释基于注解的切面实现**

在这种情况下(基于@AspectJ的实现)，涉及到的切面声明的风格与带有java5标注的普通java类一致。

**64. 什么是Spring的MVC框架？**

Spring 配备构建Web 应用的全功能MVC框架。Spring可以很便捷地和其他MVC框架集成，如Struts，Spring 的MVC框架用控制反转把业务对象和控制逻辑清晰地隔离。它也允许以声明的方式把请求参数和业务对象绑定。

**65. DispatcherServlet**

Spring的MVC框架是围绕DispatcherServlet来设计的，它用来处理所有的HTTP请求和响应。

**66. WebApplicationContext**

WebApplicationContext 继承了ApplicationContext 并增加了一些WEB应用必备的特有功能，它不同于一般的ApplicationContext ，因为它能处理主题，并找到被关联的servlet。

**67. 什么是Spring MVC框架的控制器？**

控制器提供一个访问应用程序的行为，此行为通常通过服务接口实现。控制器解析用户输入并将其转换为一个由视图呈现给用户的模型。Spring用一个非常抽象的方式实现了一个控制层，允许用户创建多种用途的控制器。

**68. @Controller 注解**

该注解表明该类扮演控制器的角色，Spring不需要你继承任何其他控制器基类或引用Servlet API。







### spring vs ejb
spring更轻量

### ioc
类似guice


### springmvc 跟ioc的关系

servlet的web.xml中必须配置一个监听器
    <listener>  
        <listener-class>org.springframework.web.context.ContextLoaderListener</listener-class>  
    </listener>  

ContextLoaderListener 这个类代码就会启动initWebApplicationContext()，具体是XMLWebApplicationContext


PropertyValues
org.springframework.beans.PropertyValue
spring-beans包里面的
```xml
    <bean id="wrapService" class="top.guoziyang.main.service.WrapService">
        <property name="helloWorldService" ref="helloWorldService"></property>
    </bean>
```

xml文件<property/>节点在java代码中的对象

### 打印Spring容器所有的Bean名称

ApplicationContextBean.java

spring-beans包
org.springframework.beans.factory.InitializingBean


xml文件中的property节点对应的信息会封装到PropertyValues中
spring 中有多少种 IOC 容器？
BeanFactory - BeanFactory 就像一个包含 bean 集合的工厂类。它会在客户端要求时实例化bean。
ApplicationContext - ApplicationContext 接口扩展了BeanFactory接口。它在BeanFactory基础上提供了一些额外的功能。


@Required 注解有什么用？
@Required 应用于 bean 属性 setter 方法。此注解仅指示必须在配置时使用bean 定义中的显式属性值或使用自动装配填充受影响的 bean
属性。如果尚未填充受影响的 bean 属性，则容器将抛出 eanInitializationException。 
示例：
```java
public class Employee {
	private String name;
	@Required
	public void setName(String name){
		this.name=name;
	}
	public string getName(){
		return name;
	}
}
```


### Spring IOC添加取出bean
@Resource 取出对象

https://blog.csdn.net/ljcgit/article/details/115353149
如何解决本文最上面出现的问题？
@Resource中指定name或着type；
@Qualifier指定bean名称；
将字段名称修改为指定的bean名称；
直接修改对象类型。
只推荐第一种方法。


https://www.zhihu.com/question/39356740/answer/1907479772


@Autowired和@Resouce的区别
@Autowired功能虽说非常强大，但是也有些不足之处。比如：比如它跟spring强耦合了，如果换成了JFinal等其他框架，功能就会失效。而@Resource是JSR-250提供的，它是Java标准，绝大部分框架都支持。
除此之外，有些场景使用@Autowired无法满足的要求，改成@Resource却能解决问题。接下来，我们重点看看@Autowired和@Resource的区别。
* @Autowired默认按byType自动装配，而@Resource默认byName自动装配。
* @Autowired只包含一个参数：required，表示是否开启自动准入，默认是true。而@Resource包含七个参数，其中最重要的两个参数是：name 和 type。
* @Autowired如果要使用byName，需要使用@Qualifier一起配合。而@Resource如果指定了name，则用byName自动装配，如果指定了type，则用byType自动装配。
* @Autowired能够用在：构造器、方法、参数、成员变量和注解上，而@Resource能用在：类、成员变量和方法上。
* @Autowired是spring定义的注解，而@Resource是JSR-250定义的注解。
此外，它们的装配顺序不同。
@Autowired的装配顺序如下：


jsr250的注解
@PostConstruct 和 @PreDestroy 注释：
@Resource
@Resources

spring JDBC API中存在哪些类？



spring profile properties

```xml
<profile
         activeDefault true
```


```java
public class ContextNamespaceHandler extends NamespaceHandlerSupport {
    public ContextNamespaceHandler() {
    }
    public void init() {
        this.registerBeanDefinitionParser("property-placeholder", new PropertyPlaceholderBeanDefinitionParser());
        this.registerBeanDefinitionParser("property-override", new PropertyOverrideBeanDefinitionParser());
        this.registerBeanDefinitionParser("annotation-config", new AnnotationConfigBeanDefinitionParser());
    //把ComponentScanBeanDefinitionParser加载到map中
        this.registerBeanDefinitionParser("component-scan", new ComponentScanBeanDefinitionParser());
        this.registerBeanDefinitionParser("load-time-weaver", new LoadTimeWeaverBeanDefinitionParser());
        this.registerBeanDefinitionParser("spring-configured", new SpringConfiguredBeanDefinitionParser());
        this.registerBeanDefinitionParser("mbean-export", new MBeanExportBeanDefinitionParser());
        this.registerBeanDefinitionParser("mbean-server", new MBeanServerBeanDefinitionParser());
    }
}
```
中

registerBeanDefinitionParser("component-scan", new ComponentScanBeanDefinitionParser());

在ComponentScanBeanDefinitionParser.java中进行处理

private static final String BASE_PACKAGE_ATTRIBUTE = "base-package";

String[] basePackages = StringUtils.tokenizeToStringArray(element.getAttribute(BASE_PACKAGE_ATTRIBUTE),         ConfigurableApplicationContext.CONFIG_LOCATION_DELIMITERS);
Set<BeanDefinitionHolder> beanDefinitions = scanner.doScan(basePackages);

https://blog.csdn.net/m0_46212601/article/details/122490746


https://www.jianshu.com/p/7938a1206fe7




问： ${jdbc.url}
注入失败 如何排错

打印spring ioc中所有的数据
String类型的

springframework
https://docs.spring.io/spring-framework/docs/5.2.14.RELEASE/javadoc-api/

spring api

要挨个熟悉

https://zhuanlan.zhihu.com/p/157416835

#### 1.BeanDefinition

在 Spring容器中，我们广泛使用的是一个一个的 Bean，BeanDefinition 从名字上就可以看出是关于 Bean 的定义。

https://www.jianshu.com/p/3b338dda2437







https://tool.oschina.net/apidocs/apidoc?api=Spring-3.1.1



https://docs.spring.io/spring-framework/docs/current/javadoc-api/



按照学习Java Se的方法来学习Spring

先用，在看源码类，挨个写用例



Spring用了注解 反射

代理 字节码生成

类加载器






用Spring一年之后，懂了好多


https://github.com/seaswalker/spring-analysis

ScopedProxyMode
https://blog.csdn.net/weixin_37689658/article/details/122308798
```

public enum ScopedProxyMode {
 
   DEFAULT,
 
   NO,
 
   INTERFACES,
 
   TARGET_CLASS
 
}

```



配置文件

applicationContext.xml

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<beans
```





```xml
<?xml version="1.0" encoding="UTF-8" ?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd">
</beans>
```







```xml
<?xml version="1.0" encoding="UTF-8" ?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:context="http://www.springframework.org/schema/context"
       xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd http://www.springframework.org/schema/context http://www.springframework.org/schema/context/spring-context.xsd">
    <context:component-scan base-package="cn.wdidada.dubbospring.provider"/>
    <import resource="classpath:spring/*.xml" />
</beans>
```







20180824



spring bean的本质是内存 软件工程 解耦合

aop是软件工程，减少重复代码



Spring能方便的与Java EE（如Java Mail、任务调度）整合，与更多技术整合（比如缓存框架）

SpringBoot SpringCloud starter



- spring doc
- spring in action
- 各种培训班材料
- spring maillist



张开涛学Spring



https://github.com/edidada/testmybatisspring

https://github.com/edidada/spring-analysis



spring 集成mybatis



控制反转    -------  定义bean

依赖注入    -------  获取bean





el 表达式

https://docs.spring.io/spring/docs/4.3.25.RELEASE/spring-framework-reference/htmlsingle/#expressions-beandef-xml-based 




##### 在Bean定义中使用EL


https://www.iteye.com/blog/jinnianshilongnian-1418311



https://zhuanlan.zhihu.com/p/99603669










##### 自定义scope


https://blog.csdn.net/likun557/article/details/104284841

- single
- protobup

- request
- session
- application

request、session、application都是在spring web容器环境中才会有的



DTD技术——xml文件的验证机制

https://blog.csdn.net/zane3/article/details/63253281



https://blog.csdn.net/GoSaint/article/details/101320827




##### jar包




- spring-beans

  

org/springframework/beans/factory/xml文件夹下面

spring-beans-3.0.xsd

spring-beans依赖spring-core



spring源码 gradle多模块怎么组织的?



xml不能用正则表达式校验 形式语言表达式定理说明的	
xml文件用.dtd校验


Spring如何解析XML文件——Spring源码之XML初解析
https://www.cnblogs.com/yuanmiemie/p/6843586.html


SAX解析XML文件
http://www.blogjava.net/DLevin/archive/2012/11/18/391545.html

Spring如何加载XSD文件
https://blog.csdn.net/iteye_16284/article/details/82334470


spring在加载xsd文件时总是先试图在本地查找xsd文件(spring的jar包中已经包含了所有版本的xsd文件)，如果没有找到，才会转向去URL指定的路径下载



xml DTD 和 xmlns xml schema 示例解析
https://www.jianshu.com/p/90987d624ff0

Spring解密 - XML解析 与 Bean注册
https://segmentfault.com/a/1190000012763946

我们可以得出Spring采用的是SAX解析


定义bean.xml文件，内容如下（XSD模式）

<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
    http://www.springframework.org/schema/beans/spring-beans.xsd">
</beans>
解析到如下两个参数:

publicId: null
systemId: http://www.springframework.org...
3.2 定义bean.xml文件，内容如下（DTD模式）

···shell


<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE beans PUBLIC "-//SPRING//DTD BEAN 2.0//EN"
        "http://www.springframework.org/dtd/spring-beans.dtd">
<beans>
</beans>

···
解析到如下两个参数:

publicId: -//SPRING//DTD BEAN 2.0//EN
systemId: http://www.springframework.or...







自己写spring

github.com/edidada/minis



github.com/edidada/festival
对应的博客https://juejin.cn/post/6844903492667064334

github.com/edidada/springboot-atomikos
项目介绍： atomikos+tk.mybatis+druid实现配置化atomikos分布式数据源管理



```shell
D:\Java\jdk1.8.0_231\bin\java.exe "-javaagent:C:\Program Files\JetBrains\IntelliJ IDEA 2018.2.4\lib\idea_rt.jar=13521:C:\Program Files\JetBrains\IntelliJ IDEA 2018.2.4\bin" -Dfile.encoding=UTF-8 -classpath D:\Java\jdk1.8.0_231\jre\lib\charsets.jar;D:\Java\jdk1.8.0_231\jre\lib\deploy.jar;D:\Java\jdk1.8.0_231\jre\lib\ext\access-bridge-64.jar;D:\Java\jdk1.8.0_231\jre\lib\ext\cldrdata.jar;D:\Java\jdk1.8.0_231\jre\lib\ext\dnsns.jar;D:\Java\jdk1.8.0_231\jre\lib\ext\jaccess.jar;D:\Java\jdk1.8.0_231\jre\lib\ext\jfxrt.jar;D:\Java\jdk1.8.0_231\jre\lib\ext\localedata.jar;D:\Java\jdk1.8.0_231\jre\lib\ext\nashorn.jar;D:\Java\jdk1.8.0_231\jre\lib\ext\sunec.jar;D:\Java\jdk1.8.0_231\jre\lib\ext\sunjce_provider.jar;D:\Java\jdk1.8.0_231\jre\lib\ext\sunmscapi.jar;D:\Java\jdk1.8.0_231\jre\lib\ext\sunpkcs11.jar;D:\Java\jdk1.8.0_231\jre\lib\ext\zipfs.jar;D:\Java\jdk1.8.0_231\jre\lib\javaws.jar;D:\Java\jdk1.8.0_231\jre\lib\jce.jar;D:\Java\jdk1.8.0_231\jre\lib\jfr.jar;D:\Java\jdk1.8.0_231\jre\lib\jfxswt.jar;D:\Java\jdk1.8.0_231\jre\lib\jsse.jar;D:\Java\jdk1.8.0_231\jre\lib\management-agent.jar;D:\Java\jdk1.8.0_231\jre\lib\plugin.jar;D:\Java\jdk1.8.0_231\jre\lib\resources.jar;D:\Java\jdk1.8.0_231\jre\lib\rt.jar;D:\git\github\shardingspheretest_local\target\classes;D:\mavenrepository\201904\commons-dbcp\commons-dbcp\1.4\commons-dbcp-1.4.jar;D:\mavenrepository\201904\commons-pool\commons-pool\1.5.4\commons-pool-1.5.4.jar;D:\mavenrepository\201904\mysql\mysql-connector-java\5.1.42\mysql-connector-java-5.1.42.jar;D:\mavenrepository\201904\org\slf4j\jcl-over-slf4j\1.7.7\jcl-over-slf4j-1.7.7.jar;D:\mavenrepository\201904\org\slf4j\slf4j-api\1.7.7\slf4j-api-1.7.7.jar;D:\mavenrepository\201904\io\shardingsphere\sharding-jdbc-spring-boot-starter\3.1.0\sharding-jdbc-spring-boot-starter-3.1.0.jar;D:\mavenrepository\201904\io\shardingsphere\sharding-jdbc-core\3.1.0\sharding-jdbc-core-3.1.0.jar;D:\mavenrepository\201904\io\shardingsphere\sharding-core\3.1.0\sharding-core-3.1.0.jar;D:\mavenrepository\201904\org\codehaus\groovy\groovy\2.4.5\groovy-2.4.5-indy.jar;D:\mavenrepository\201904\org\antlr\antlr4\4.7.1\antlr4-4.7.1.jar;D:\mavenrepository\201904\org\antlr\antlr4-runtime\4.7.1\antlr4-runtime-4.7.1.jar;D:\mavenrepository\201904\org\antlr\antlr-runtime\3.5.2\antlr-runtime-3.5.2.jar;D:\mavenrepository\201904\org\antlr\ST4\4.0.8\ST4-4.0.8.jar;D:\mavenrepository\201904\org\abego\treelayout\org.abego.treelayout.core\1.0.3\org.abego.treelayout.core-1.0.3.jar;D:\mavenrepository\201904\org\glassfish\javax.json\1.0.4\javax.json-1.0.4.jar;D:\mavenrepository\201904\com\ibm\icu\icu4j\58.2\icu4j-58.2.jar;D:\mavenrepository\201904\io\shardingsphere\sharding-transaction-core\3.1.0\sharding-transaction-core-3.1.0.jar;D:\mavenrepository\201904\com\google\guava\guava\18.0\guava-18.0.jar;D:\mavenrepository\201904\io\shardingsphere\sharding-jdbc-orchestration-spring-boot-starter\3.1.0\sharding-jdbc-orchestration-spring-boot-starter-3.1.0.jar;D:\mavenrepository\201904\io\shardingsphere\sharding-jdbc-orchestration\3.1.0\sharding-jdbc-orchestration-3.1.0.jar;D:\mavenrepository\201904\io\shardingsphere\sharding-orchestration-core\3.1.0\sharding-orchestration-core-3.1.0.jar;D:\mavenrepository\201904\io\shardingsphere\sharding-orchestration-reg-api\3.1.0\sharding-orchestration-reg-api-3.1.0.jar;D:\mavenrepository\201904\io\shardingsphere\sharding-jdbc-spring-namespace\3.1.0\sharding-jdbc-spring-namespace-3.1.0.jar;D:\mavenrepository\201904\io\shardingsphere\sharding-jdbc-orchestration-spring-namespace\3.1.0\sharding-jdbc-orchestration-spring-namespace-3.1.0.jar;D:\mavenrepository\201904\org\springframework\spring-jdbc\4.3.6.RELEASE\spring-jdbc-4.3.6.RELEASE.jar;D:\mavenrepository\201904\org\springframework\spring-beans\4.3.6.RELEASE\spring-beans-4.3.6.RELEASE.jar;D:\mavenrepository\201904\org\springframework\spring-core\4.3.6.RELEASE\spring-core-4.3.6.RELEASE.jar;D:\mavenrepository\201904\commons-logging\commons-logging\1.2\commons-logging-1.2.jar;D:\mavenrepository\201904\org\springframework\spring-orm\4.3.6.RELEASE\spring-orm-4.3.6.RELEASE.jar;D:\mavenrepository\201904\org\springframework\spring-context-support\4.3.6.RELEASE\spring-context-support-4.3.6.RELEASE.jar;D:\mavenrepository\201904\org\springframework\spring-context\4.3.6.RELEASE\spring-context-4.3.6.RELEASE.jar;D:\mavenrepository\201904\org\springframework\spring-aop\4.3.6.RELEASE\spring-aop-4.3.6.RELEASE.jar;D:\mavenrepository\201904\org\springframework\spring-expression\4.3.6.RELEASE\spring-expression-4.3.6.RELEASE.jar;D:\mavenrepository\201904\org\springframework\spring-tx\4.3.6.RELEASE\spring-tx-4.3.6.RELEASE.jar;D:\mavenrepository\201904\org\hibernate\javax\persistence\hibernate-jpa-2.1-api\1.0.0.Final\hibernate-jpa-2.1-api-1.0.0.Final.jar;D:\mavenrepository\201904\org\hibernate\hibernate-core\4.3.11.Final\hibernate-core-4.3.11.Final.jar;D:\mavenrepository\201904\org\jboss\logging\jboss-logging\3.1.3.GA\jboss-logging-3.1.3.GA.jar;D:\mavenrepository\201904\org\jboss\logging\jboss-logging-annotations\1.2.0.Beta1\jboss-logging-annotations-1.2.0.Beta1.jar;D:\mavenrepository\201904\org\jboss\spec\javax\transaction\jboss-transaction-api_1.2_spec\1.0.0.Final\jboss-transaction-api_1.2_spec-1.0.0.Final.jar;D:\mavenrepository\201904\dom4j\dom4j\1.6.1\dom4j-1.6.1.jar;D:\mavenrepository\201904\xml-apis\xml-apis\1.0.b2\xml-apis-1.0.b2.jar;D:\mavenrepository\201904\org\hibernate\common\hibernate-commons-annotations\4.0.5.Final\hibernate-commons-annotations-4.0.5.Final.jar;D:\mavenrepository\201904\org\javassist\javassist\3.18.1-GA\javassist-3.18.1-GA.jar;D:\mavenrepository\201904\antlr\antlr\2.7.7\antlr-2.7.7.jar;D:\mavenrepository\201904\org\jboss\jandex\1.1.0.Final\jandex-1.1.0.Final.jar;D:\mavenrepository\201904\org\hibernate\hibernate-entitymanager\4.3.11.Final\hibernate-entitymanager-4.3.11.Final.jar;D:\mavenrepository\201904\org\springframework\boot\spring-boot-starter-data-jpa\1.5.0.RELEASE\spring-boot-starter-data-jpa-1.5.0.RELEASE.jar;D:\mavenrepository\201904\org\springframework\boot\spring-boot-starter\1.5.0.RELEASE\spring-boot-starter-1.5.0.RELEASE.jar;D:\mavenrepository\201904\org\springframework\boot\spring-boot\1.5.0.RELEASE\spring-boot-1.5.0.RELEASE.jar;D:\mavenrepository\201904\org\springframework\boot\spring-boot-autoconfigure\1.5.0.RELEASE\spring-boot-autoconfigure-1.5.0.RELEASE.jar;D:\mavenrepository\201904\org\springframework\boot\spring-boot-starter-logging\1.5.0.RELEASE\spring-boot-starter-logging-1.5.0.RELEASE.jar;D:\mavenrepository\201904\ch\qos\logback\logback-classic\1.1.9\logback-classic-1.1.9.jar;D:\mavenrepository\201904\ch\qos\logback\logback-core\1.1.9\logback-core-1.1.9.jar;D:\mavenrepository\201904\org\slf4j\jul-to-slf4j\1.7.22\jul-to-slf4j-1.7.22.jar;D:\mavenrepository\201904\org\slf4j\log4j-over-slf4j\1.7.22\log4j-over-slf4j-1.7.22.jar;D:\mavenrepository\201904\org\yaml\snakeyaml\1.17\snakeyaml-1.17.jar;D:\mavenrepository\201904\org\springframework\boot\spring-boot-starter-aop\1.5.0.RELEASE\spring-boot-starter-aop-1.5.0.RELEASE.jar;D:\mavenrepository\201904\org\aspectj\aspectjweaver\1.8.9\aspectjweaver-1.8.9.jar;D:\mavenrepository\201904\org\springframework\boot\spring-boot-starter-jdbc\1.5.0.RELEASE\spring-boot-starter-jdbc-1.5.0.RELEASE.jar;D:\mavenrepository\201904\org\apache\tomcat\tomcat-jdbc\8.5.11\tomcat-jdbc-8.5.11.jar;D:\mavenrepository\201904\org\apache\tomcat\tomcat-juli\8.5.11\tomcat-juli-8.5.11.jar;D:\mavenrepository\201904\javax\transaction\javax.transaction-api\1.2\javax.transaction-api-1.2.jar;D:\mavenrepository\201904\org\springframework\data\spring-data-jpa\1.11.0.RELEASE\spring-data-jpa-1.11.0.RELEASE.jar;D:\mavenrepository\201904\org\springframework\data\spring-data-commons\1.13.0.RELEASE\spring-data-commons-1.13.0.RELEASE.jar;D:\mavenrepository\201904\org\springframework\spring-aspects\4.3.6.RELEASE\spring-aspects-4.3.6.RELEASE.jar;D:\mavenrepository\201904\org\mybatis\mybatis\3.4.2\mybatis-3.4.2.jar;D:\mavenrepository\201904\org\mybatis\mybatis-spring\1.3.0\mybatis-spring-1.3.0.jar;D:\mavenrepository\201904\org\mybatis\spring\boot\mybatis-spring-boot-starter\1.3.0\mybatis-spring-boot-starter-1.3.0.jar;D:\mavenrepository\201904\org\mybatis\spring\boot\mybatis-spring-boot-autoconfigure\1.3.0\mybatis-spring-boot-autoconfigure-1.3.0.jar;D:\mavenrepository\201904\com\zaxxer\HikariCP\3.2.0\HikariCP-3.2.0.jar cn.edidada.testss.spring.namespace.mybatis.nodep.SpringNamespaceExample
Exception in thread "main" org.springframework.beans.factory.UnsatisfiedDependencyException: Error creating bean with name 'JDBCOrderRepositoryImpl' defined in file [D:\git\github\shardingspheretest_local\target\classes\cn\edidada\testss\repository\jdbc\repository\JDBCOrderRepositoryImpl.class]: Unsatisfied dependency expressed through constructor parameter 0; nested exception is org.springframework.beans.factory.NoUniqueBeanDefinitionException: No qualifying bean of type 'javax.sql.DataSource' available: expected single matching bean but found 5: demo_ds_2,demo_ds_0,demo_ds_1,demo_ds_3,shardingDataSource
	at org.springframework.beans.factory.support.ConstructorResolver.createArgumentArray(ConstructorResolver.java:749)
	at org.springframework.beans.factory.support.ConstructorResolver.autowireConstructor(ConstructorResolver.java:189)
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.autowireConstructor(AbstractAutowireCapableBeanFactory.java:1193)
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.createBeanInstance(AbstractAutowireCapableBeanFactory.java:1095)
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.doCreateBean(AbstractAutowireCapableBeanFactory.java:513)
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.createBean(AbstractAutowireCapableBeanFactory.java:483)
	at org.springframework.beans.factory.support.AbstractBeanFactory$1.getObject(AbstractBeanFactory.java:306)
	at org.springframework.beans.factory.support.DefaultSingletonBeanRegistry.getSingleton(DefaultSingletonBeanRegistry.java:230)
	at org.springframework.beans.factory.support.AbstractBeanFactory.doGetBean(AbstractBeanFactory.java:302)
	at org.springframework.beans.factory.support.AbstractBeanFactory.getBean(AbstractBeanFactory.java:197)
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.preInstantiateSingletons(DefaultListableBeanFactory.java:761)
	at org.springframework.context.support.AbstractApplicationContext.finishBeanFactoryInitialization(AbstractApplicationContext.java:866)
	at org.springframework.context.support.AbstractApplicationContext.refresh(AbstractApplicationContext.java:542)
	at org.springframework.context.support.ClassPathXmlApplicationContext.<init>(ClassPathXmlApplicationContext.java:139)
	at org.springframework.context.support.ClassPathXmlApplicationContext.<init>(ClassPathXmlApplicationContext.java:83)
	at cn.edidada.testss.spring.namespace.mybatis.nodep.SpringNamespaceExample.main(SpringNamespaceExample.java:36)
Caused by: org.springframework.beans.factory.NoUniqueBeanDefinitionException: No qualifying bean of type 'javax.sql.DataSource' available: expected single matching bean but found 5: demo_ds_2,demo_ds_0,demo_ds_1,demo_ds_3,shardingDataSource
	at org.springframework.beans.factory.config.DependencyDescriptor.resolveNotUnique(DependencyDescriptor.java:173)
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.doResolveDependency(DefaultListableBeanFactory.java:1116)
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.resolveDependency(DefaultListableBeanFactory.java:1066)
	at org.springframework.beans.factory.support.ConstructorResolver.resolveAutowiredArgument(ConstructorResolver.java:835)
	at org.springframework.beans.factory.support.ConstructorResolver.createArgumentArray(ConstructorResolver.java:741)
	... 15 more

Process finished with exit code 1
```



Spring的核心是容器，容器有beanFactory和ApplicationContext，后者是更完善的，功能更齐备的容器





spring注解处理器

1.利用asm技术扫描class文件，转化成Spring bean结构，把符合扫描规则的（主要是是否有相关的注解标注，例如@Component）bean注册到Spring 容器中beanFactory
2.注册处理器，包括注解处理器
3.实例化处理器（包括注解处理器），并将其注册到容器的beanPostProcessors列表中
4.创建bean的过程中个，属性注入或者初始化bean时会调用对应的注解处理器进行处理。



过滤器

https://blog.csdn.net/honghailiang888/article/details/74981445

实际上，是把所有包下的class文件都扫描了的，并且利用asm技术读取java字节码并转化为MetadataReader中的AnnotationMetadataReadingVisitor结构



spring 配置事务管理器
https://www.cnblogs.com/ooo0/p/11029612.html

@Resource
在类上是注册资源
在field或method上是注入依赖？

@ResponseBody
如果没有，method返回字符串

[Spring对Groovy Bean的支持](https://my.oschina.net/joshuazhan/blog/137940)

[Spring MVC 接收POST表单请求，获取参数总结](https://blog.csdn.net/m0_37499059/article/details/78798077)

看相关源码

Spring log

spring如何打印源码中的日志



```java
		if (logger.isDebugEnabled()) {
			logger.debug("Eagerly caching bean '" + beanName +
					"' to allow for resolving potential circular references");
		}
```



自己编译spring jar



xsd文件的编写？

xml文件含有配置信息
xml中的配置项，信息是否正确，使用xsd文件去校验

基于Java代码的配置

bean标签有哪些子节点 属性

org.mybatis.spring.SqlSessionFactoryBean
从其他框架接入Spring的jar包来学习

Spring官方是spring-jdbc
MyBatis团队开发了mybatis-spring





[Spring注解处理器](https://www.jianshu.com/p/acd1565510e3)

```java
"D:\Program Files\Java\jdk1.8.0_161\bin\java.exe" -XX:TieredStopAtLevel=1 -noverify -Dspring.output.ansi.enabled=always -Dcom.sun.management.jmxremote -Dcom.sun.management.jmxremote.port=10523 -Dcom.sun.management.jmxremote.authenticate=false -Dcom.sun.management.jmxremote.ssl=false -Djava.rmi.server.hostname=localhost -Dspring.liveBeansView.mbeanDomain -Dspring.application.admin.enabled=true "-javaagent:C:\Program Files\JetBrains\IntelliJ IDEA 2018.2.4\lib\idea_rt.jar=10524:C:\Program Files\JetBrains\IntelliJ IDEA 2018.2.4\bin" -Dfile.encoding=UTF-8 -classpath "D:\Program Files\Java\jdk1.8.0_161\jre\lib\charsets.jar;D:\Program Files\Java\jdk1.8.0_161\jre\lib\deploy.jar;D:\Program Files\Java\jdk1.8.0_161\jre\lib\ext\access-bridge-64.jar;D:\Program Files\Java\jdk1.8.0_161\jre\lib\ext\cldrdata.jar;D:\Program Files\Java\jdk1.8.0_161\jre\lib\ext\dnsns.jar;D:\Program Files\Java\jdk1.8.0_161\jre\lib\ext\jaccess.jar;D:\Program Files\Java\jdk1.8.0_161\jre\lib\ext\jfxrt.jar;D:\Program Files\Java\jdk1.8.0_161\jre\lib\ext\localedata.jar;D:\Program Files\Java\jdk1.8.0_161\jre\lib\ext\nashorn.jar;D:\Program Files\Java\jdk1.8.0_161\jre\lib\ext\sunec.jar;D:\Program Files\Java\jdk1.8.0_161\jre\lib\ext\sunjce_provider.jar;D:\Program Files\Java\jdk1.8.0_161\jre\lib\ext\sunmscapi.jar;D:\Program Files\Java\jdk1.8.0_161\jre\lib\ext\sunpkcs11.jar;D:\Program Files\Java\jdk1.8.0_161\jre\lib\ext\zipfs.jar;D:\Program Files\Java\jdk1.8.0_161\jre\lib\javaws.jar;D:\Program Files\Java\jdk1.8.0_161\jre\lib\jce.jar;D:\Program Files\Java\jdk1.8.0_161\jre\lib\jfr.jar;D:\Program Files\Java\jdk1.8.0_161\jre\lib\jfxswt.jar;D:\Program Files\Java\jdk1.8.0_161\jre\lib\jsse.jar;D:\Program Files\Java\jdk1.8.0_161\jre\lib\management-agent.jar;D:\Program Files\Java\jdk1.8.0_161\jre\lib\plugin.jar;D:\Program Files\Java\jdk1.8.0_161\jre\lib\resources.jar;D:\Program Files\Java\jdk1.8.0_161\jre\lib\rt.jar;D:\git\github\testhystrix\testhyxtrix-web\target\classes;D:\git\github\testhystrix\testhyxtrix-service\target\classes;D:\git\github\testhystrix\testhystrix-api\target\classes;D:\mavenrepository\201904\redis\clients\jedis\2.8.1\jedis-2.8.1.jar;D:\mavenrepository\201904\org\apache\commons\commons-pool2\2.4.2\commons-pool2-2.4.2.jar;D:\mavenrepository\201904\commons-codec\commons-codec\1.9\commons-codec-1.9.jar;D:\mavenrepository\201904\com\google\guava\guava\18.0\guava-18.0.jar;D:\mavenrepository\201904\com\netflix\hystrix\hystrix-request-servlet\1.5.18\hystrix-request-servlet-1.5.18.jar;D:\mavenrepository\201904\com\netflix\hystrix\hystrix-metrics-event-stream\1.5.18\hystrix-metrics-event-stream-1.5.18.jar;D:\mavenrepository\201904\com\netflix\hystrix\hystrix-serialization\1.5.18\hystrix-serialization-1.5.18.jar;D:\mavenrepository\201904\com\fasterxml\jackson\module\jackson-module-afterburner\2.7.5\jackson-module-afterburner-2.7.5.jar;D:\mavenrepository\201904\com\fasterxml\jackson\core\jackson-core\2.7.5\jackson-core-2.7.5.jar;D:\mavenrepository\201904\com\fasterxml\jackson\core\jackson-annotations\2.7.5\jackson-annotations-2.7.5.jar;D:\mavenrepository\201904\com\netflix\hystrix\hystrix-core\1.5.18\hystrix-core-1.5.18.jar;D:\mavenrepository\201904\org\slf4j\slf4j-api\1.7.25\slf4j-api-1.7.25.jar;D:\mavenrepository\201904\com\netflix\archaius\archaius-core\0.4.1\archaius-core-0.4.1.jar;D:\mavenrepository\201904\commons-configuration\commons-configuration\1.8\commons-configuration-1.8.jar;D:\mavenrepository\201904\commons-lang\commons-lang\2.6\commons-lang-2.6.jar;D:\mavenrepository\201904\commons-logging\commons-logging\1.1.1\commons-logging-1.1.1.jar;D:\mavenrepository\201904\io\reactivex\rxjava\1.2.0\rxjava-1.2.0.jar;D:\mavenrepository\201904\org\hdrhistogram\HdrHistogram\2.1.9\HdrHistogram-2.1.9.jar;D:\mavenrepository\201904\com\netflix\hystrix\hystrix-javanica\1.5.18\hystrix-javanica-1.5.18.jar;D:\mavenrepository\201904\org\aspectj\aspectjrt\1.8.6\aspectjrt-1.8.6.jar;D:\mavenrepository\201904\org\apache\commons\commons-lang3\3.1\commons-lang3-3.1.jar;D:\mavenrepository\201904\org\ow2\asm\asm\5.0.4\asm-5.0.4.jar;D:\mavenrepository\201904\org\aspectj\aspectjweaver\1.8.6\aspectjweaver-1.8.6.jar;D:\mavenrepository\201904\com\google\code\findbugs\jsr305\2.0.0\jsr305-2.0.0.jar;D:\mavenrepository\201904\org\projectlombok\lombok\1.18.4\lombok-1.18.4.jar;D:\mavenrepository\201904\cn\wdidada\commons\1.0.0\commons-1.0.0.jar;D:\mavenrepository\201904\org\springframework\spring-core\4.3.12.RELEASE\spring-core-4.3.12.RELEASE.jar;D:\mavenrepository\201904\org\springframework\boot\spring-boot-starter\1.5.8.RELEASE\spring-boot-starter-1.5.8.RELEASE.jar;D:\mavenrepository\201904\org\springframework\boot\spring-boot\1.5.8.RELEASE\spring-boot-1.5.8.RELEASE.jar;D:\mavenrepository\201904\org\springframework\spring-context\4.3.12.RELEASE\spring-context-4.3.12.RELEASE.jar;D:\mavenrepository\201904\org\springframework\boot\spring-boot-autoconfigure\1.5.8.RELEASE\spring-boot-autoconfigure-1.5.8.RELEASE.jar;D:\mavenrepository\201904\org\springframework\boot\spring-boot-starter-logging\1.5.8.RELEASE\spring-boot-starter-logging-1.5.8.RELEASE.jar;D:\mavenrepository\201904\ch\qos\logback\logback-classic\1.1.11\logback-classic-1.1.11.jar;D:\mavenrepository\201904\ch\qos\logback\logback-core\1.1.11\logback-core-1.1.11.jar;D:\mavenrepository\201904\org\slf4j\jul-to-slf4j\1.7.25\jul-to-slf4j-1.7.25.jar;D:\mavenrepository\201904\org\slf4j\log4j-over-slf4j\1.7.25\log4j-over-slf4j-1.7.25.jar;D:\mavenrepository\201904\org\yaml\snakeyaml\1.17\snakeyaml-1.17.jar;D:\mavenrepository\201904\org\springframework\data\spring-data-redis\1.8.8.RELEASE\spring-data-redis-1.8.8.RELEASE.jar;D:\mavenrepository\201904\org\springframework\data\spring-data-keyvalue\1.2.8.RELEASE\spring-data-keyvalue-1.2.8.RELEASE.jar;D:\mavenrepository\201904\org\springframework\data\spring-data-commons\1.13.8.RELEASE\spring-data-commons-1.13.8.RELEASE.jar;D:\mavenrepository\201904\org\springframework\spring-tx\4.3.12.RELEASE\spring-tx-4.3.12.RELEASE.jar;D:\mavenrepository\201904\org\springframework\spring-beans\4.3.12.RELEASE\spring-beans-4.3.12.RELEASE.jar;D:\mavenrepository\201904\org\springframework\spring-oxm\4.3.12.RELEASE\spring-oxm-4.3.12.RELEASE.jar;D:\mavenrepository\201904\org\springframework\spring-aop\4.3.12.RELEASE\spring-aop-4.3.12.RELEASE.jar;D:\mavenrepository\201904\org\springframework\spring-context-support\4.3.12.RELEASE\spring-context-support-4.3.12.RELEASE.jar;D:\mavenrepository\201904\org\slf4j\jcl-over-slf4j\1.7.25\jcl-over-slf4j-1.7.25.jar;D:\mavenrepository\201904\org\springframework\boot\spring-boot-starter-web\1.5.8.RELEASE\spring-boot-starter-web-1.5.8.RELEASE.jar;D:\mavenrepository\201904\org\springframework\boot\spring-boot-starter-tomcat\1.5.8.RELEASE\spring-boot-starter-tomcat-1.5.8.RELEASE.jar;D:\mavenrepository\201904\org\apache\tomcat\embed\tomcat-embed-core\8.5.23\tomcat-embed-core-8.5.23.jar;D:\mavenrepository\201904\org\apache\tomcat\tomcat-annotations-api\8.5.23\tomcat-annotations-api-8.5.23.jar;D:\mavenrepository\201904\org\apache\tomcat\embed\tomcat-embed-el\8.5.23\tomcat-embed-el-8.5.23.jar;D:\mavenrepository\201904\org\apache\tomcat\embed\tomcat-embed-websocket\8.5.23\tomcat-embed-websocket-8.5.23.jar;D:\mavenrepository\201904\org\hibernate\hibernate-validator\5.3.5.Final\hibernate-validator-5.3.5.Final.jar;D:\mavenrepository\201904\javax\validation\validation-api\1.1.0.Final\validation-api-1.1.0.Final.jar;D:\mavenrepository\201904\org\jboss\logging\jboss-logging\3.3.0.Final\jboss-logging-3.3.0.Final.jar;D:\mavenrepository\201904\com\fasterxml\classmate\1.3.1\classmate-1.3.1.jar;D:\mavenrepository\201904\com\fasterxml\jackson\core\jackson-databind\2.8.10\jackson-databind-2.8.10.jar;D:\mavenrepository\201904\org\springframework\spring-web\4.3.12.RELEASE\spring-web-4.3.12.RELEASE.jar;D:\mavenrepository\201904\org\springframework\spring-webmvc\4.3.12.RELEASE\spring-webmvc-4.3.12.RELEASE.jar;D:\mavenrepository\201904\org\springframework\spring-expression\4.3.12.RELEASE\spring-expression-4.3.12.RELEASE.jar" cn.wdidada.testhystrix.web.RetryApplication

  .   ____          _            __ _ _
 /\\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
( ( )\___ | '_ | '_| | '_ \/ _` | \ \ \ \
 \\/  ___)| |_)| | | | | || (_| |  ) ) ) )
  '  |____| .__|_| |_|_| |_\__, | / / / /
 =========|_|==============|___/=/_/_/_/
 :: Spring Boot ::        (v1.5.8.RELEASE)

2019-10-12 09:07:10.864  INFO 218144 --- [           main] c.w.testhystrix.web.RetryApplication     : Starting RetryApplication on ChengWu-Win10 with PID 218144 (D:\git\github\testhystrix\testhyxtrix-web\target\classes started by edidada in D:\git\github\testhystrix)
2019-10-12 09:07:10.869  INFO 218144 --- [           main] c.w.testhystrix.web.RetryApplication     : No active profile set, falling back to default profiles: default
2019-10-12 09:07:11.075  INFO 218144 --- [           main] ationConfigEmbeddedWebApplicationContext : Refreshing org.springframework.boot.context.embedded.AnnotationConfigEmbeddedWebApplicationContext@75c072cb: startup date [Sat Oct 12 09:07:11 CST 2019]; root of context hierarchy
2019-10-12 09:07:12.217  INFO 218144 --- [           main] .s.d.r.c.RepositoryConfigurationDelegate : Multiple Spring Data modules found, entering strict repository configuration mode!
2019-10-12 09:07:12.965  INFO 218144 --- [           main] s.b.c.e.t.TomcatEmbeddedServletContainer : Tomcat initialized with port(s): 8080 (http)
2019-10-12 09:07:12.974  INFO 218144 --- [           main] o.apache.catalina.core.StandardService   : Starting service [Tomcat]
2019-10-12 09:07:12.975  INFO 218144 --- [           main] org.apache.catalina.core.StandardEngine  : Starting Servlet Engine: Apache Tomcat/8.5.23
2019-10-12 09:07:13.072  INFO 218144 --- [ost-startStop-1] o.a.c.c.C.[Tomcat].[localhost].[/]       : Initializing Spring embedded WebApplicationContext
2019-10-12 09:07:13.073  INFO 218144 --- [ost-startStop-1] o.s.web.context.ContextLoader            : Root WebApplicationContext: initialization completed in 2026 ms
2019-10-12 09:07:13.233  INFO 218144 --- [ost-startStop-1] o.s.b.w.servlet.ServletRegistrationBean  : Mapping servlet: 'dispatcherServlet' to [/]
2019-10-12 09:07:13.238  INFO 218144 --- [ost-startStop-1] o.s.b.w.servlet.FilterRegistrationBean   : Mapping filter: 'characterEncodingFilter' to: [/*]
2019-10-12 09:07:13.239  INFO 218144 --- [ost-startStop-1] o.s.b.w.servlet.FilterRegistrationBean   : Mapping filter: 'hiddenHttpMethodFilter' to: [/*]
2019-10-12 09:07:13.239  INFO 218144 --- [ost-startStop-1] o.s.b.w.servlet.FilterRegistrationBean   : Mapping filter: 'httpPutFormContentFilter' to: [/*]
2019-10-12 09:07:13.239  INFO 218144 --- [ost-startStop-1] o.s.b.w.servlet.FilterRegistrationBean   : Mapping filter: 'requestContextFilter' to: [/*]
2019-10-12 09:07:13.563  INFO 218144 --- [           main] s.w.s.m.m.a.RequestMappingHandlerAdapter : Looking for @ControllerAdvice: org.springframework.boot.context.embedded.AnnotationConfigEmbeddedWebApplicationContext@75c072cb: startup date [Sat Oct 12 09:07:11 CST 2019]; root of context hierarchy
2019-10-12 09:07:13.619  INFO 218144 --- [           main] s.w.s.m.m.a.RequestMappingHandlerMapping : Mapped "{[/]}" onto public java.lang.String cn.wdidada.testhystrix.web.control.MainControl.index()
2019-10-12 09:07:13.620  INFO 218144 --- [           main] s.w.s.m.m.a.RequestMappingHandlerMapping : Mapped "{[/hello]}" onto public java.lang.String cn.wdidada.testhystrix.web.control.MainControl.hello()
2019-10-12 09:07:13.621  INFO 218144 --- [           main] s.w.s.m.m.a.RequestMappingHandlerMapping : Mapped "{[/testservice]}" onto public java.lang.String cn.wdidada.testhystrix.web.control.MainControl.testService()
2019-10-12 09:07:13.624  INFO 218144 --- [           main] s.w.s.m.m.a.RequestMappingHandlerMapping : Mapped "{[/error]}" onto public org.springframework.http.ResponseEntity<java.util.Map<java.lang.String, java.lang.Object>> org.springframework.boot.autoconfigure.web.BasicErrorController.error(javax.servlet.http.HttpServletRequest)
2019-10-12 09:07:13.625  INFO 218144 --- [           main] s.w.s.m.m.a.RequestMappingHandlerMapping : Mapped "{[/error],produces=[text/html]}" onto public org.springframework.web.servlet.ModelAndView org.springframework.boot.autoconfigure.web.BasicErrorController.errorHtml(javax.servlet.http.HttpServletRequest,javax.servlet.http.HttpServletResponse)
2019-10-12 09:07:13.658  INFO 218144 --- [           main] o.s.w.s.handler.SimpleUrlHandlerMapping  : Mapped URL path [/webjars/**] onto handler of type [class org.springframework.web.servlet.resource.ResourceHttpRequestHandler]
2019-10-12 09:07:13.658  INFO 218144 --- [           main] o.s.w.s.handler.SimpleUrlHandlerMapping  : Mapped URL path [/**] onto handler of type [class org.springframework.web.servlet.resource.ResourceHttpRequestHandler]
2019-10-12 09:07:13.703  INFO 218144 --- [           main] o.s.w.s.handler.SimpleUrlHandlerMapping  : Mapped URL path [/**/favicon.ico] onto handler of type [class org.springframework.web.servlet.resource.ResourceHttpRequestHandler]
2019-10-12 09:07:13.858  WARN 218144 --- [           main] ationConfigEmbeddedWebApplicationContext : Exception encountered during context initialization - cancelling refresh attempt: org.springframework.beans.factory.UnsatisfiedDependencyException: Error creating bean with name 'redisTemplate' defined in class path resource [org/springframework/boot/autoconfigure/data/redis/RedisAutoConfiguration$RedisConfiguration.class]: Unsatisfied dependency expressed through method 'redisTemplate' parameter 0; nested exception is org.springframework.beans.factory.BeanCreationException: Error creating bean with name 'redisConnectionFactory' defined in class path resource [org/springframework/boot/autoconfigure/data/redis/RedisAutoConfiguration$RedisConnectionConfiguration.class]: Invocation of init method failed; nested exception is java.lang.NoSuchMethodError: redis.clients.jedis.JedisPool.<init>(Lorg/apache/commons/pool2/impl/GenericObjectPoolConfig;Ljava/lang/String;IILjava/lang/String;ILjava/lang/String;Z)V
2019-10-12 09:07:13.859  INFO 218144 --- [           main] o.s.j.e.a.AnnotationMBeanExporter        : Unregistering JMX-exposed beans on shutdown
2019-10-12 09:07:13.862  INFO 218144 --- [           main] o.apache.catalina.core.StandardService   : Stopping service [Tomcat]
2019-10-12 09:07:13.883  INFO 218144 --- [           main] utoConfigurationReportLoggingInitializer : 

Error starting ApplicationContext. To display the auto-configuration report re-run your application with 'debug' enabled.
2019-10-12 09:07:13.897 ERROR 218144 --- [           main] o.s.boot.SpringApplication               : Application startup failed

org.springframework.beans.factory.UnsatisfiedDependencyException: Error creating bean with name 'redisTemplate' defined in class path resource [org/springframework/boot/autoconfigure/data/redis/RedisAutoConfiguration$RedisConfiguration.class]: Unsatisfied dependency expressed through method 'redisTemplate' parameter 0; nested exception is org.springframework.beans.factory.BeanCreationException: Error creating bean with name 'redisConnectionFactory' defined in class path resource [org/springframework/boot/autoconfigure/data/redis/RedisAutoConfiguration$RedisConnectionConfiguration.class]: Invocation of init method failed; nested exception is java.lang.NoSuchMethodError: redis.clients.jedis.JedisPool.<init>(Lorg/apache/commons/pool2/impl/GenericObjectPoolConfig;Ljava/lang/String;IILjava/lang/String;ILjava/lang/String;Z)V
	at org.springframework.beans.factory.support.ConstructorResolver.createArgumentArray(ConstructorResolver.java:749) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.ConstructorResolver.instantiateUsingFactoryMethod(ConstructorResolver.java:467) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.instantiateUsingFactoryMethod(AbstractAutowireCapableBeanFactory.java:1173) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.createBeanInstance(AbstractAutowireCapableBeanFactory.java:1067) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.doCreateBean(AbstractAutowireCapableBeanFactory.java:513) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.createBean(AbstractAutowireCapableBeanFactory.java:483) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory$1.getObject(AbstractBeanFactory.java:306) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.DefaultSingletonBeanRegistry.getSingleton(DefaultSingletonBeanRegistry.java:230) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory.doGetBean(AbstractBeanFactory.java:302) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory.getBean(AbstractBeanFactory.java:197) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.preInstantiateSingletons(DefaultListableBeanFactory.java:761) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.context.support.AbstractApplicationContext.finishBeanFactoryInitialization(AbstractApplicationContext.java:867) ~[spring-context-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.context.support.AbstractApplicationContext.refresh(AbstractApplicationContext.java:543) ~[spring-context-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.boot.context.embedded.EmbeddedWebApplicationContext.refresh(EmbeddedWebApplicationContext.java:122) ~[spring-boot-1.5.8.RELEASE.jar:1.5.8.RELEASE]
	at org.springframework.boot.SpringApplication.refresh(SpringApplication.java:693) [spring-boot-1.5.8.RELEASE.jar:1.5.8.RELEASE]
	at org.springframework.boot.SpringApplication.refreshContext(SpringApplication.java:360) [spring-boot-1.5.8.RELEASE.jar:1.5.8.RELEASE]
	at org.springframework.boot.SpringApplication.run(SpringApplication.java:303) [spring-boot-1.5.8.RELEASE.jar:1.5.8.RELEASE]
	at org.springframework.boot.SpringApplication.run(SpringApplication.java:1118) [spring-boot-1.5.8.RELEASE.jar:1.5.8.RELEASE]
	at org.springframework.boot.SpringApplication.run(SpringApplication.java:1107) [spring-boot-1.5.8.RELEASE.jar:1.5.8.RELEASE]
	at cn.wdidada.testhystrix.web.RetryApplication.main(RetryApplication.java:15) [classes/:na]
Caused by: org.springframework.beans.factory.BeanCreationException: Error creating bean with name 'redisConnectionFactory' defined in class path resource [org/springframework/boot/autoconfigure/data/redis/RedisAutoConfiguration$RedisConnectionConfiguration.class]: Invocation of init method failed; nested exception is java.lang.NoSuchMethodError: redis.clients.jedis.JedisPool.<init>(Lorg/apache/commons/pool2/impl/GenericObjectPoolConfig;Ljava/lang/String;IILjava/lang/String;ILjava/lang/String;Z)V
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.initializeBean(AbstractAutowireCapableBeanFactory.java:1628) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.doCreateBean(AbstractAutowireCapableBeanFactory.java:555) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.createBean(AbstractAutowireCapableBeanFactory.java:483) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory$1.getObject(AbstractBeanFactory.java:306) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.DefaultSingletonBeanRegistry.getSingleton(DefaultSingletonBeanRegistry.java:230) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory.doGetBean(AbstractBeanFactory.java:302) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory.getBean(AbstractBeanFactory.java:202) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.config.DependencyDescriptor.resolveCandidate(DependencyDescriptor.java:208) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.doResolveDependency(DefaultListableBeanFactory.java:1138) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.resolveDependency(DefaultListableBeanFactory.java:1066) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.ConstructorResolver.resolveAutowiredArgument(ConstructorResolver.java:835) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.ConstructorResolver.createArgumentArray(ConstructorResolver.java:741) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	... 19 common frames omitted
Caused by: java.lang.NoSuchMethodError: redis.clients.jedis.JedisPool.<init>(Lorg/apache/commons/pool2/impl/GenericObjectPoolConfig;Ljava/lang/String;IILjava/lang/String;ILjava/lang/String;Z)V
	at org.springframework.data.redis.connection.jedis.JedisConnectionFactory.createRedisPool(JedisConnectionFactory.java:275) ~[spring-data-redis-1.8.8.RELEASE.jar:na]
	at org.springframework.data.redis.connection.jedis.JedisConnectionFactory.createPool(JedisConnectionFactory.java:250) ~[spring-data-redis-1.8.8.RELEASE.jar:na]
	at org.springframework.data.redis.connection.jedis.JedisConnectionFactory.afterPropertiesSet(JedisConnectionFactory.java:237) ~[spring-data-redis-1.8.8.RELEASE.jar:na]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.invokeInitMethods(AbstractAutowireCapableBeanFactory.java:1687) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.initializeBean(AbstractAutowireCapableBeanFactory.java:1624) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	... 30 common frames omitted

```


JSR-330标准注解
Java依赖注入标准（JSR-330，Dependency Injection for Java）1.0 规范主要是面向依赖注入使用者，而对注入器实现、配置并未作详细要求。目前 Spring 、Guice 已经开始兼容该规范，JSR-299（Contexts and Dependency Injection for Java EE platform，参考实现 Weld ）在依赖注入上也使用该规范。JSR-330 规范并未按 JSR 惯例发布规范文档，只发布了规范 API 源码。
从Spring 3.0开始，Spring开始支持JSR-330标准的注解。这些注解和Spring注解扫描的方式是一直的，开发者只需要引入javax.inject即可。
<dependency>
    <groupId>javax.inject</groupId>
    <artifactId>javax.inject</artifactId>
    <version>xxx</version>
</dependency>
JSR-330中的标准注解与Spring中的注解的对应关系如下：

https://maxwell.gitbook.io/way-to-architect/java-yu-yan/zhu-jie/chang-yong-zhu-jie/jsr-330biao-zhun-zhu-jie

Spring中解析xml配置文件使用的类
`org.springframework.beans.factory.xml.NamespaceHandler`

MyBatis中解析xml配置文件的类
`org.mybatis.spring.config.NamespaceHandler`


org.springframework.cglib.proxy.MethodProxy

```java

at org.springframework.cglib.proxy.MethodProxy.invoke(MethodProxy.java:204)
	at org.springframework.aop.framework.CglibAopProxy$CglibMethodInvocation.invokeJoinpoint(CglibAopProxy.java:738)
	at org.springframework.aop.framework.ReflectiveMethodInvocation.proceed(ReflectiveMethodInvocation.java:157)
	at org.springframework.aop.aspectj.MethodInvocationProceedingJoinPoint.proceed(MethodInvocationProceedingJoinPoint.java:85)
	at com.XXX.media.platform.commons.aop.aspect.CatchManagerSqlExceptionAspect.catchRestException(CatchManagerSqlExceptionAspect.java:52)
	at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
	at sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)
	at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
	at java.lang.reflect.Method.invoke(Method.java:498)
	at org.springframework.aop.aspectj.AbstractAspectJAdvice.invokeAdviceMethodWithGivenArgs(AbstractAspectJAdvice.java:629)
	at org.springframework.aop.aspectj.AbstractAspectJAdvice.invokeAdviceMethod(AbstractAspectJAdvice.java:618)
	at org.springframework.aop.aspectj.AspectJAroundAdvice.invoke(AspectJAroundAdvice.java:70)
	at org.springframework.aop.framework.ReflectiveMethodInvocation.proceed(ReflectiveMethodInvocation.java:168)
	at org.springframework.aop.interceptor.ExposeInvocationInterceptor.invoke(ExposeInvocationInterceptor.java:92)

```

[Spring核心——Stereotype组件与Bean扫描](https://blog.csdn.net/GV7lZB0y87u7C/article/details/81151343)

org.aspectj.lang.JoinPoint 接口
org.aspectj.lang.ProceedingJoinPoint 接口
org.springframework.aop.aspectj.MethodInvocationProceedingJoinPoint

MethodInvocationProceedingJoinPoint方法
public Object[] getArgs()
Signature getSignature()

```java

The last packet sent successfully to the server was 0 milliseconds ago. The driver has not received any packets from the server.
	at sun.reflect.NativeConstructorAccessorImpl.newInstance0(Native Method) ~[?:1.8.0_161]
	at sun.reflect.NativeConstructorAccessorImpl.newInstance(NativeConstructorAccessorImpl.java:62) ~[?:1.8.0_161]
	at sun.reflect.DelegatingConstructorAccessorImpl.newInstance(DelegatingConstructorAccessorImpl.java:45) ~[?:1.8.0_161]
	at java.lang.reflect.Constructor.newInstance(Constructor.java:423) ~[?:1.8.0_161]
	at com.mysql.jdbc.Util.handleNewInstance(Util.java:411) ~[mysql-connector-java-5.1.21.jar:?]
	at com.mysql.jdbc.SQLError.createCommunicationsException(SQLError.java:1117) ~[mysql-connector-java-5.1.21.jar:?]
	at com.mysql.jdbc.MysqlIO.<init>(MysqlIO.java:350) ~[mysql-connector-java-5.1.21.jar:?]
	at com.mysql.jdbc.ConnectionImpl.coreConnect(ConnectionImpl.java:2393) ~[mysql-connector-java-5.1.21.jar:?]
	at com.mysql.jdbc.ConnectionImpl.connectOneTryOnly(ConnectionImpl.java:2430) ~[mysql-connector-java-5.1.21.jar:?]
	at com.mysql.jdbc.ConnectionImpl.createNewIO(ConnectionImpl.java:2215) ~[mysql-connector-java-5.1.21.jar:?]
	at com.mysql.jdbc.ConnectionImpl.<init>(ConnectionImpl.java:813) ~[mysql-connector-java-5.1.21.jar:?]
	at com.mysql.jdbc.JDBC4Connection.<init>(JDBC4Connection.java:47) ~[mysql-connector-java-5.1.21.jar:?]
	at sun.reflect.NativeConstructorAccessorImpl.newInstance0(Native Method) ~[?:1.8.0_161]
	at sun.reflect.NativeConstructorAccessorImpl.newInstance(NativeConstructorAccessorImpl.java:62) ~[?:1.8.0_161]
	at sun.reflect.DelegatingConstructorAccessorImpl.newInstance(DelegatingConstructorAccessorImpl.java:45) ~[?:1.8.0_161]
	at java.lang.reflect.Constructor.newInstance(Constructor.java:423) ~[?:1.8.0_161]
	at com.mysql.jdbc.Util.handleNewInstance(Util.java:411) ~[mysql-connector-java-5.1.21.jar:?]
	at com.mysql.jdbc.ConnectionImpl.getInstance(ConnectionImpl.java:399) ~[mysql-connector-java-5.1.21.jar:?]
	at com.mysql.jdbc.NonRegisteringDriver.connect(NonRegisteringDriver.java:334) ~[mysql-connector-java-5.1.21.jar:?]
	at com.mysql.jdbc.jdbc2.optional.MysqlDataSource.getConnection(MysqlDataSource.java:443) ~[mysql-connector-java-5.1.21.jar:?]
	at com.mysql.jdbc.jdbc2.optional.MysqlDataSource.getConnection(MysqlDataSource.java:141) ~[mysql-connector-java-5.1.21.jar:?]
	at com.mysql.jdbc.jdbc2.optional.MysqlDataSource.getConnection(MysqlDataSource.java:111) ~[mysql-connector-java-5.1.21.jar:?]
	at com.zaxxer.hikari.pool.PoolBase.newConnection(PoolBase.java:369) ~[HikariCP-3.2.0.jar:?]
	at com.zaxxer.hikari.pool.PoolBase.newPoolEntry(PoolBase.java:198) ~[HikariCP-3.2.0.jar:?]
	at com.zaxxer.hikari.pool.HikariPool.createPoolEntry(HikariPool.java:467) ~[HikariCP-3.2.0.jar:?]
	at com.zaxxer.hikari.pool.HikariPool.checkFailFast(HikariPool.java:541) ~[HikariCP-3.2.0.jar:?]
	at com.zaxxer.hikari.pool.HikariPool.<init>(HikariPool.java:115) ~[HikariCP-3.2.0.jar:?]
	at com.zaxxer.hikari.HikariDataSource.<init>(HikariDataSource.java:81) ~[HikariCP-3.2.0.jar:?]
	at sun.reflect.NativeConstructorAccessorImpl.newInstance0(Native Method) ~[?:1.8.0_161]
	at sun.reflect.NativeConstructorAccessorImpl.newInstance(NativeConstructorAccessorImpl.java:62) ~[?:1.8.0_161]
	at sun.reflect.DelegatingConstructorAccessorImpl.newInstance(DelegatingConstructorAccessorImpl.java:45) ~[?:1.8.0_161]
	at java.lang.reflect.Constructor.newInstance(Constructor.java:423) ~[?:1.8.0_161]
	at org.springframework.beans.BeanUtils.instantiateClass(BeanUtils.java:142) ~[spring-beans-4.3.11.RELEASE.jar:4.3.11.RELEASE]
	at org.springframework.beans.factory.support.SimpleInstantiationStrategy.instantiate(SimpleInstantiationStrategy.java:122) ~[spring-beans-4.3.11.RELEASE.jar:4.3.11.RELEASE]
	at org.springframework.beans.factory.support.ConstructorResolver.autowireConstructor(ConstructorResolver.java:271) ~[spring-beans-4.3.11.RELEASE.jar:4.3.11.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.autowireConstructor(AbstractAutowireCapableBeanFactory.java:1193) ~[spring-beans-4.3.11.RELEASE.jar:4.3.11.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.createBeanInstance(AbstractAutowireCapableBeanFactory.java:1095) ~[spring-beans-4.3.11.RELEASE.jar:4.3.11.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.doCreateBean(AbstractAutowireCapableBeanFactory.java:513) ~[spring-beans-4.3.11.RELEASE.jar:4.3.11.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.createBean(AbstractAutowireCapableBeanFactory.java:483) ~[spring-beans-4.3.11.RELEASE.jar:4.3.11.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory$1.getObject(AbstractBeanFactory.java:306) ~[spring-beans-4.3.11.RELEASE.jar:4.3.11.RELEASE]
	at org.springframework.beans.factory.support.DefaultSingletonBeanRegistry.getSingleton(DefaultSingletonBeanRegistry.java:230) ~[spring-beans-4.3.11.RELEASE.jar:4.3.11.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory.doGetBean(AbstractBeanFactory.java:302) ~[spring-beans-4.3.11.RELEASE.jar:4.3.11.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory.getBean(AbstractBeanFactory.java:197) ~[spring-beans-4.3.11.RELEASE.jar:4.3.11.RELEASE]
	at org.springframework.beans.factory.support.BeanDefinitionValueResolver.resolveReference(BeanDefinitionValueResolver.java:351) ~[spring-beans-4.3.11.RELEASE.jar:4.3.11.RELEASE]
	at org.springframework.beans.factory.support.BeanDefinitionValueResolver.resolveValueIfNecessary(BeanDefinitionValueResolver.java:108) ~[spring-beans-4.3.11.RELEASE.jar:4.3.11.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.applyPropertyValues(AbstractAutowireCapableBeanFactory.java:1531) ~[spring-beans-4.3.11.RELEASE.jar:4.3.11.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.populateBean(AbstractAutowireCapableBeanFactory.java:1276) ~[spring-beans-4.3.11.RELEASE.jar:4.3.11.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.doCreateBean(AbstractAutowireCapableBeanFactory.java:553) ~[spring-beans-4.3.11.RELEASE.jar:4.3.11.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.createBean(AbstractAutowireCapableBeanFactory.java:483) ~[spring-beans-4.3.11.RELEASE.jar:4.3.11.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory$1.getObject(AbstractBeanFactory.java:306) ~[spring-beans-4.3.11.RELEASE.jar:4.3.11.RELEASE]
	at org.springframework.beans.factory.support.DefaultSingletonBeanRegistry.getSingleton(DefaultSingletonBeanRegistry.java:230) ~[spring-beans-4.3.11.RELEASE.jar:4.3.11.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory.doGetBean(AbstractBeanFactory.java:302) ~[spring-beans-4.3.11.RELEASE.jar:4.3.11.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory.getBean(AbstractBeanFactory.java:197) ~[spring-beans-4.3.11.RELEASE.jar:4.3.11.RELEASE]
	at org.springframework.beans.factory.support.BeanDefinitionValueResolver.resolveReference(BeanDefinitionValueResolver.java:351) ~[spring-beans-4.3.11.RELEASE.jar:4.3.11.RELEASE]
	at org.springframework.beans.factory.support.BeanDefinitionValueResolver.resolveValueIfNecessary(BeanDefinitionValueResolver.java:108) ~[spring-beans-4.3.11.RELEASE.jar:4.3.11.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.applyPropertyValues(AbstractAutowireCapableBeanFactory.java:1531) ~[spring-beans-4.3.11.RELEASE.jar:4.3.11.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.populateBean(AbstractAutowireCapableBeanFactory.java:1276) ~[spring-beans-4.3.11.RELEASE.jar:4.3.11.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.doCreateBean(AbstractAutowireCapableBeanFactory.java:553) ~[spring-beans-4.3.11.RELEASE.jar:4.3.11.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.createBean(AbstractAutowireCapableBeanFactory.java:483) ~[spring-beans-4.3.11.RELEASE.jar:4.3.11.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory$1.getObject(AbstractBeanFactory.java:306) ~[spring-beans-4.3.11.RELEASE.jar:4.3.11.RELEASE]
	at org.springframework.beans.factory.support.DefaultSingletonBeanRegistry.getSingleton(DefaultSingletonBeanRegistry.java:230) ~[spring-beans-4.3.11.RELEASE.jar:4.3.11.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory.doGetBean(AbstractBeanFactory.java:302) ~[spring-beans-4.3.11.RELEASE.jar:4.3.11.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanFactory.getBean(AbstractBeanFactory.java:202) ~[spring-beans-4.3.11.RELEASE.jar:4.3.11.RELEASE]
	at org.springframework.beans.factory.config.DependencyDescriptor.resolveCandidate(DependencyDescriptor.java:208) ~[spring-beans-4.3.11.RELEASE.jar:4.3.11.RELEASE]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.doResolveDependency(DefaultListableBeanFactory.java:1138) ~[spring-beans-4.3.11.RELEASE.jar:4.3.11.RELEASE]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.resolveDependency(DefaultListableBeanFactory.java:1066) ~[spring-beans-4.3.11.RELEASE.jar:4.3.11.RELEASE]
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor$AutowiredFieldElement.inject(AutowiredAnnotationBeanPostProcessor.java:585) ~[spring-beans-4.3.11.RELEASE.jar:4.3.11.RELEASE]
	... 37 more

```

## Spring test

```java

	at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
	at sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)
	at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
	at java.lang.reflect.Method.invoke(Method.java:498)
	at org.junit.runners.model.FrameworkMethod$1.runReflectiveCall(FrameworkMethod.java:50)
	at org.junit.internal.runners.model.ReflectiveCallable.run(ReflectiveCallable.java:12)
	at org.junit.runners.model.FrameworkMethod.invokeExplosively(FrameworkMethod.java:47)
	at org.junit.internal.runners.statements.InvokeMethod.evaluate(InvokeMethod.java:17)
	at org.springframework.test.context.junit4.statements.RunBeforeTestMethodCallbacks.evaluate(RunBeforeTestMethodCallbacks.java:75)
	at org.springframework.test.context.junit4.statements.RunAfterTestMethodCallbacks.evaluate(RunAfterTestMethodCallbacks.java:86)
	at org.springframework.test.context.junit4.statements.SpringRepeat.evaluate(SpringRepeat.java:84)
	at org.junit.runners.ParentRunner.runLeaf(ParentRunner.java:325)
	at org.springframework.test.context.junit4.SpringJUnit4ClassRunner.runChild(SpringJUnit4ClassRunner.java:252)
	at org.springframework.test.context.junit4.SpringJUnit4ClassRunner.runChild(SpringJUnit4ClassRunner.java:94)
	at org.junit.runners.ParentRunner$3.run(ParentRunner.java:290)
	at org.junit.runners.ParentRunner$1.schedule(ParentRunner.java:71)
	at org.junit.runners.ParentRunner.runChildren(ParentRunner.java:288)
	at org.junit.runners.ParentRunner.access$000(ParentRunner.java:58)
	at org.junit.runners.ParentRunner$2.evaluate(ParentRunner.java:268)
	at org.springframework.test.context.junit4.statements.RunBeforeTestClassCallbacks.evaluate(RunBeforeTestClassCallbacks.java:61)
	at org.springframework.test.context.junit4.statements.RunAfterTestClassCallbacks.evaluate(RunAfterTestClassCallbacks.java:70)
	at org.junit.runners.ParentRunner.run(ParentRunner.java:363)
	at org.springframework.test.context.junit4.SpringJUnit4ClassRunner.run(SpringJUnit4ClassRunner.java:191)

```


[testvalidate Spring](https://bitbucket.org/sandisks/testvalidate/src/master/)

Spring的注解@Qualifier用法
https://blog.csdn.net/qq_36567005/article/details/80611139

一个接口有多个bean在Spring Cointainer中

`@Service("beanName")`


```

@Autowired
@Qualifier("beanName")
Interface ..

```

Qualifier的意思是合格者，通过这个标示，表明了哪个实现类才是我们所需要的，添加@Qualifier注解，需要注意的是@Qualifier的参数名称为我们之前定义@Service注解的名称之一。


@Resource(name="")
@Qualifier注解的用处：当一个接口有多个实现的时候，为了指名具体调用哪个类的实现。

Qualifier spring-beans的内容
org.springframework.beans.factory.annotation.Qualifier



Spring整理系列(11)——@Configuration注解、@Bean注解以及配置自动扫描、bean作用域
https://blog.csdn.net/javaloveiphone/article/details/52182899


BeanDefinitionStoreException：无法解析配置类

Spring注解之@PostConstruct在项目启动时执行指定方法

@PreDestroy



- javax.annotation.Resource
- javax.annotation.Resources

@Resource用法与@Autowired 用法 用法相似，也是做依赖注入的，从容器中自动获取bean。但还是有一定的区别。

Spring @Resource、@Autowired、@Qualifier的注解注入及区别
https://blog.csdn.net/Baple/article/details/17891755

@Primary

Resources
https://stackoverflow.com/questions/49791032/how-resources-annotation-works

javax.annotation

javax.annotation.PostConstruct

[spring注解之@PostConstruct在项目启动时执行指定方法](https://www.cnblogs.com/fnlingnzb-learner/p/10758848.html)

https://docs.oracle.com/javaee/7/api/javax/annotation/PostConstruct.html

[Spring加载Properties配置文件的四种方式](https://blog.csdn.net/HaHa_Sir/article/details/79105951)

- 一、通过 context:property-placeholder 标签实现配置文件加载
- 二、通过 util:properties 标签实现配置文件加载
- 三、通过 @PropertySource 注解实现配置文件加载
- 四、通过 PropertyPlaceholderConfigurer 类读取配置文件

PropertyPlaceholderConfigurer
https://blog.csdn.net/weixin_43314519/article/details/109233365


PropertyPlaceholderConfigurer 的基本使用
PropertyPlaceholderConfigurer是个bean工厂后置处理器的实现，也就是 BeanFactoryPostProcessor接口的一个实现。PropertyPlaceholderConfigurer可以将上下文（配置文 件）中的属性值放在另一个单独的标准java Properties文件中去。在XML文件中用${…}替换指定的properties文件中的值。这样的话，只需要对properties文件进 行修改，而不用对xml配置文件进行修改。
在Spring中，使用PropertyPlaceholderConfigurer可以在XML配置文件中加入外部属性文件
PropertyPlaceholderConfigurer 引入外部属性文件
————————————————
版权声明：本文为CSDN博主「Hi丶ImViper」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/weixin_43314519/article/details/109233365


[util:properties](https://maidong660.iteye.com/blog/2363666)

@Aspect// 这个注解表明 使用spring 的aop，需要开启aop 
<!--开启AOP自动代理 --><aop:aspectj-autoproxy />

java定义切面，需要定义bean，在xml或者其他地方配置

[类注解 例子](https://blog.csdn.net/jidetashuo/article/details/54406872)

jdbc包
SQLErrorCodesFactory

beans包
org.springframework.beans.factory.DisposableBean

interface void destroy() throws Exception;

org.springframework.beans.factory.InitializingBean

[InitializingBean的作用](https://blog.csdn.net/maclaren001/article/details/37039749)

InitializingBean接口为bean提供了初始化方法的方式，它只包括afterPropertiesSet方法，凡是继承该接口的类，在初始化bean的时候会执行该方法。

跟@PostConstruct类似

[java 自定义注解 spring aop 实现注解](https://blog.csdn.net/jidetashuo/article/details/54406872)

context**.jar包

org.springframework.scripting.ScriptSource

Spring的动态语言支持
动态语言支持将 Spring 从一个以 Java 为中心的应用程序框架改变成一个以 JVM 为中心的应用程序框架。现在，Spring 不再只是让 Java 开发变得更容易。它还允许将以静态和动态语言编写的代码轻松地插入到 Spring 支持的分层架构方法中，从而使 JVM 的开发也变得更加容易。如果您已经熟悉 Spring，那么您会感到很舒服：可以利用 Spring 已经提供的所有特性 — 控制反转（IoC）和依赖项注入、面向方面编程（AOP）、声明式事务划分、Web 和数据访问框架集成、远程调用等 — 同时又可以使用灵活动态的语言，比如 Groovy。
Spring 通过 ScriptFactory 和 ScriptSource 接口支持动态语言集成。ScriptFactory 接口定义用于创建和配置脚本 Spring bean 的机制。理论上，所有在 JVM 上运行语言都受支持，因此可以选择特定的语言来创建自己的实现。ScriptSource 定义 Spring 如何访问实际的脚本源代码；例如，通过文件系统或 URL。Groovy 语言集成通过 ScriptFactory 的 GroovyScriptFactory 实现得到支持。

Spring-data中，DefaultRedisScript类ScriptSource就是一种script

[spring data redis lun脚本](https://blog.csdn.net/weixin_34087301/article/details/87171615)

[lua脚本例子 Redis入门指南第六章 lua脚本](https://www.cnblogs.com/yanghuahui/p/3697996.html)
执行前三次 返回1
第四次 返回2

Redis入门指南 第2版

Redis入门指南第六章 lua脚本


org.springframework.beans.factory.BeanDefinitionStoreException: IOException parsing XML document from ServletContext resource [/WEB-INF/applicationContext.xml]; nested exception is java.io.FileNotFoundException: Could not open ServletContext resource [/WEB-INF/applicationContext.xml]
	at org.springframework.beans.factory.xml.XmlBeanDefinitionReader.loadBeanDefinitions(XmlBeanDefinitionReader.java:344) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.xml.XmlBeanDefinitionReader.loadBeanDefinitions(XmlBeanDefinitionReader.java:304) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanDefinitionReader.loadBeanDefinitions(AbstractBeanDefinitionReader.java:181) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanDefinitionReader.loadBeanDefinitions(AbstractBeanDefinitionReader.java:217) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.AbstractBeanDefinitionReader.loadBeanDefinitions(AbstractBeanDefinitionReader.java:188) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.web.context.support.XmlWebApplicationContext.loadBeanDefinitions(XmlWebApplicationContext.java:125) ~[spring-web-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.web.context.support.XmlWebApplicationContext.loadBeanDefinitions(XmlWebApplicationContext.java:94) ~[spring-web-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.context.support.AbstractRefreshableApplicationContext.refreshBeanFactory(AbstractRefreshableApplicationContext.java:129) ~[spring-context-4.3.12.RELEASE.jar:4.3.12.RELEASE]





```java
org.springframework.beans.factory.config.PropertyPlaceholderConfigurer
```

加载properties文件





#### ApplicationContext及其子类

ClassPathXmlApplicationContext

close()

ApplicationContext无close()





applicationContext.xml是整个spring应用所有的，springmvc是属于spring的，在spring的基础上有xxx-servet.xml文件来配置http相关的bean



[ClassPathXmlApplicationContext配置文件路径解析](https://www.cnblogs.com/dream-saddle/p/9449870.html)



**Java的升级比c#差**

Spring bean生命周期，看源码


Spring bean的生命周期包括以下阶段：

实例化（Instantiation）：当Spring容器接收到一个请求时，它会根据Bean的定义，实例化一个对象。

属性设置（Population of Properties）：在对象实例化后，Spring容器会为Bean的属性设置值，包括依赖注入等操作。

初始化前（Initialization Before）：在Bean的初始化前，Spring容器会调用实现了InitializingBean接口的afterPropertiesSet方法，或者在XML配置中定义的init-method方法，来进行一些初始化操作。

初始化后（Initialization After）：在Bean的初始化后，Spring容器会调用实现了BeanPostProcessor接口的postProcessBeforeInitialization方法，或者在XML配置中定义的init-method方法，来进行一些初始化操作。

销毁前（Destruction Before）：在Bean的销毁前，Spring容器会调用实现了DisposableBean接口的destroy方法，或者在XML配置中定义的destroy-method方法，来进行一些销毁操作。

销毁后（Destruction After）：在Bean的销毁后，Spring容器会调用实现了BeanPostProcessor接口的postProcessAfterInitialization方法，或者在XML配置中定义的destroy-method方法，来进行一些销毁操作。

以上是Spring Bean的生命周期阶段，开发者可以通过实现相应的接口或者在XML配置中定义相应的方法来进行一些自定义操作。




Spring bean生命周期 看哪个类源码

Spring Bean的生命周期涉及多个类，包括BeanFactory、BeanDefinition、BeanPostProcessor、InitializingBean、DisposableBean等接口以及相关的实现类。

如果要查看Spring Bean的生命周期实现代码，可以先看一下BeanFactory的实现类，例如DefaultListableBeanFactory，其中包括了BeanDefinition的注册、获取、创建、初始化和销毁等操作。

在BeanFactory中，BeanPostProcessor是用来处理Bean初始化前后的操作的接口，可以通过实现该接口来实现一些自定义操作。在DefaultListableBeanFactory中，BeanPostProcessor的实现类包括了AutowiredAnnotationBeanPostProcessor、CommonAnnotationBeanPostProcessor、InitDestroyAnnotationBeanPostProcessor等。

同时，InitializingBean和DisposableBean接口的实现类也包含了Bean的初始化和销毁的操作，可以通过查看这些类的源码了解Spring Bean的生命周期实现。例如，InitializingBean接口的实现类包括了AbstractAutowireCapableBeanFactory、AbstractBeanFactory、AbstractApplicationContext等。



Spring中的循环依赖.pdf
三级缓存是通⽤的叫法。
⼀级缓存为：singletonObjects
⼆级缓存为：earlySingletonObjects
三级缓存为：singletonFactories
先稍微解释⼀下这三个缓存的作⽤，后⾯详细分析：
singletonObjects中缓存的是已经经历了完整⽣命周期的bean对象。
earlySingletonObjects⽐singletonObjects多了⼀个early，表示缓存的是早期的bean对象。早期是
什么意思？表示Bean的⽣命周期还没⾛完就把这个Bean放⼊了earlySingletonObjects。
singletonFactories中缓存的是ObjectFactory，表示对象⼯⼚，⽤来创建某个对象的。


三级缓存指的是Spring在创建单例Bean时所使用的三个缓存池，包括singletonObjects、earlySingletonObjects和singletonFactories。

其中，singletonFactories缓存池是第三级缓存，用于存储Bean的工厂对象，即创建Bean的工厂方法。当Spring容器需要创建一个单例Bean时，它首先会尝试从singletonObjects缓存中获取，如果获取不到，就会去earlySingletonObjects缓存中查找。如果earlySingletonObjects缓存中也找不到，则Spring容器会尝试使用singletonFactories缓存中的Bean工厂方法来创建Bean实例。

如果Bean的工厂方法存在于singletonFactories缓存中，说明该Bean正在创建中，此时Spring容器会直接返回Bean工厂方法而不是创建Bean实例。当Bean实例创建成功后，Spring容器会将其存储到singletonObjects缓存中，并清空earlySingletonObjects和singletonFactories缓存。

需要注意的是，singletonFactories缓存中存储的是用于创建Bean实例的工厂方法，而不是Bean实例本身。这是因为如果工厂方法的调用出现问题，可以避免将错误的Bean实例放入singletonObjects缓存中，从而避免影响容器中其他单例Bean的正常使用。



继承FactoryBean生成bean   不经历spring bean完整周期
用@Bean注解   经历spring bean完整周期


Spring Framework是一个大型的开源框架，它包含了许多不同的模块，每个模块都提供了不同的功能。以下是Spring Framework中一些常见的核心模块及其功能，以及相应的jar包：

Spring Core：提供了Spring框架的核心功能，如IoC和DI容器。核心jar包为spring-core和spring-beans。

Spring Context：扩展了Spring Core模块，提供了更多的IoC容器的功能，如ApplicationContext。核心jar包为spring-context。

Spring AOP：提供了面向切面编程的支持，通过切面可以将业务逻辑模块化。核心jar包为spring-aop和spring-aspects。

Spring DAO：提供了对JDBC和ORM框架的支持，如JdbcTemplate、NamedParameterJdbcTemplate等。核心jar包为spring-jdbc和spring-tx。

Spring ORM：提供了对ORM框架的支持，如Hibernate、JPA、MyBatis等。核心jar包为spring-orm。

Spring Web：提供了对Web应用程序的支持，包括Web MVC框架、Web Socket、Web Servlet等。核心jar包为spring-web和spring-webmvc。

Spring Test：提供了对单元测试和集成测试的支持，包括JUnit和TestNG等测试框架的整合。核心jar包为spring-test。

除了上述的核心模块，Spring Framework还有其他许多的模块，如Spring Security、Spring Integration、Spring Batch、Spring Mobile等，每个模块都提供了不同的功能和特性。对于每个模块所包含的jar包，可以在相应的文档中查找。





BeanDefinition的实现类：
在Spring框架中，BeanDefinition接口的实现类有两个，分别是GenericBeanDefinition和RootBeanDefinition。
GenericBeanDefinition是BeanDefinition接口的通用实现类，用于描述一个Bean的配置信息。
RootBeanDefinition继承自GenericBeanDefinition，它是GenericBeanDefinition的子类，用于描述一个根Bean的配置信息，一般用于配置单例Bean。
BeanDefinitionRegistry接口：
在Spring框架中，BeanDefinitionRegistry接口是一个重要的接口，用于注册和管理BeanDefinition对象。



BeanDefinitionRegistry
在Spring框架中，BeanDefinitionRegistry接口的常用实现类有以下几个：

DefaultListableBeanFactory
DefaultListableBeanFactory是BeanDefinitionRegistry接口的默认实现类，它是BeanFactory接口的子类，用于管理BeanDefinition对象，并通过BeanFactory接口来管理Bean实例。DefaultListableBeanFactory实现了以下接口：

ConfigurableBeanFactory
SingletonBeanRegistry
AliasRegistry
BeanDefinitionRegistry
DefaultListableBeanFactory是Spring IoC容器中最常用的实现类，它是基于HashMap来实现BeanDefinition的注册和管理的，同时也支持基于XML和注解的BeanDefinition的注册和管理。
GenericApplicationContext
GenericApplicationContext是一个通用的应用上下文实现类，它是BeanDefinitionRegistry接口的实现类，用于管理BeanDefinition对象。它支持基于XML和注解的BeanDefinition的注册和管理，并可以创建和管理Spring IoC容器。
AnnotationConfigApplicationContext
AnnotationConfigApplicationContext是一个基于注解的应用上下文实现类，它是BeanDefinitionRegistry接口的实现类，用于管理基于注解的BeanDefinition对象。它支持基于注解的BeanDefinition的注册和管理，并可以创建和管理Spring IoC容器。
XmlWebApplicationContext
XmlWebApplicationContext是一个基于XML的Web应用上下文实现类，它是BeanDefinitionRegistry接口的实现类，用于管理基于XML的BeanDefinition对象。它支持基于XML的BeanDefinition的注册和管理，并可以创建和管理Spring IoC容器。
除了上述几种实现类之外，还有其他一些BeanDefinitionRegistry接口的实现类，如GenericGroovyApplicationContext、ClassPathXmlApplicationContext等。这些实现类的区别在于注册和管理BeanDefinition的方式和创建和管理Spring IoC容器的方式不同。

