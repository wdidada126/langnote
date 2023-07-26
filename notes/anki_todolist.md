# anki

ErrorDecoder

Java并发编程：Callable、Future和FutureTask

ConcurrentLinkedDeque

boolean contains(Object o)
int size() //返回链表中包含的元素个数
boolean isEmpty()
E peekFirst()  //获得链表首结点
E peekLast() //获得链表尾结点

CountDownLatch
ExecutorService作为一个线程池，然后利用CountDownLatch可以让指定数量的线程都执行完再执行主线程的特性。就可以实现多线程提速了。 
套路是这样的： 
1、实现runnable接口实现一个run方法，里面执行我们的耗时复杂业务操作。
2、在循环里给list里的每个对象分配一个线程
3、使用CountDownLatch让主线程等待工作线程全部执行完毕后之后，再继续执行。

countDown()
await()


AcceptHeaderLocaleResolver

SpringMVC中AcceptHeaderLocaleResolver分析
https://blog.csdn.net/biren_wang/article/details/52254823

LocaleResolver常用实现
AcceptHeaderLocaleResolver
SessionLocaleResolver
CookieLocaleResolver
FixedLocaleResolver 

https://blog.csdn.net/rj042/article/details/23354225

为了让web应用程序支持国际化（i18n），需要识别每个用户的所在区域，并根据这个区域显示内容。在Spring MVC应用程序中，用户的区域是通过区域解析器来识别的，它必须实现LocaleResolver接口。区域解析器的作用就是根据某种策略来决定如何响应用户的请求内容。

AcceptHeaderLocaleResolver类是SpringMVC默认的解析器。

该类的核心代码为：

@Override
public Locale resolveLocale(HttpServletRequest request) {
Locale defaultLocale = getDefaultLocale();
if (defaultLocale != null && request.getHeader("Accept-Language") == null) {
return defaultLocale;
}
Locale locale = request.getLocale();
if (!isSupportedLocale(locale)) {
locale = findSupportedLocale(request, locale);
}
return locale;
}

结论：当Accept-Language==null时，使用系统默认Locale；否则，判断系统是否支持request最想使用Locale（没配置Locale或配置了想要的Locale都认为支持），支持则使用，不支持则使用服务器（如Tomcat）默认提供的Locale。对于Tomcat的Locale,可以在其启动脚本中配置Java参数设置。

BeanNameUrlHandlerMapping


HandlerExecutionChain


HttpMessageConveter

Semaphore 例子

ServletContextListener

jjwt源码分析

LocaleResolver实现类有哪些

MultipartResolver实现类 例子

MySql 存储过程

MySQL表分区 实践 做笔记

RequestCondition
SpringMVC源代码学习外传（三）RequestCondition

RequestCondition是一个springMVC的接口，专门用于保存从request提取出的用于匹配handler的条件。

public interface RequestCondition<T> {
    T combine(T other);
    T getMatchingCondition(HttpServletRequest request);
    int compareTo(T other, HttpServletRequest request);
}


CompositeRequestCondition
private final PatternsRequestCondition patternsCondition;
private final RequestMethodsRequestCondition methodsCondition;
private final ParamsRequestCondition paramsCondition;
private final HeadersRequestCondition headersCondition;
private final ConsumesRequestCondition consumesCondition;
private final ProducesRequestCondition producesCondition;
private final RequestConditionHolder customConditionHolder;

https://blog.csdn.net/xia4820723/article/details/51433940


RequestToViewNameTranslator
实现类




SimpleTcpCluster源码解析
BeanNameAware，可以在Bean中得到它在IOC容器中的Bean的实例的名字。
BeanFactoryAware，可以在Bean中得到Bean所在的IOC容器，从而直接在Bean中使用IOC容器的服务。
ApplicationContextAware，可以在Bean中得到Bean所在的应用上下文，从而直接在Bean中使用上下文的服务。
MessageSourceAware，在Bean中可以得到消息源。
ApplicationEventPublisherAware，在bean中可以得到应用上下文的事件发布器，从而可以在Bean中发布应用上下文的事件。
ResourceLoaderAware，在Bean中可以得到ResourceLoader，从而在bean中使用ResourceLoader加载外部对应的Resource资源。

ImportAware
EmbeddedValueResolverAware
EnvironmentAware
BootstrapContextAware
BeanClassLoaderAware
LoadTimeWeaverAware
NotificationPublisherAware
ServletConfigAware



ViewResolver
InternalResourceView会把Controller处理器方法返回的模型属性都存放到对应的request属性中，然后通过RequestDispatcher在服务器端把请求forword重定向到目标URL。比如在InternalResourceViewResolver中定义了prefix=/WEB-INF/，suffix=.jsp，然后请求的Controller处理器方法返回的视图名称为test，那么这个时候InternalResourceViewResolver就会把test解析为一个InternalResourceView对象，先把返回的模型属性都存放到对应的HttpServletRequest属性中，然后利用RequestDispatcher在服务器端把请求forword到/WEB-INF/test.jsp。这就是InternalResourceViewResolver一个非常重要的特性，我们都知道存放在/WEB-INF/下面的内容是不能直接通过request请求的方式请求到的，为了安全性考虑，我们通常会把jsp文件放在WEB-INF目录下，而InternalResourceView在服务器端跳转的方式可以很好的解决这个问题。下面是一个InternalResourceViewResolver的定义，根据该定义当返回的逻辑视图名称是test的时候，InternalResourceViewResolver会给它加上定义好的前缀和后缀，组成“/WEB-INF/test.jsp”的形式，然后把它当做一个InternalResourceView的url新建一个InternalResourceView对象返回。



Software-Defined Networking tools for LXC (LinuX Containers)
https://github.com/jpetazzo/pipework
pipework是一个用软件来为linux容器定义网络的工具，pipework允许你在一个复杂的环境下把容器连接在一起，pipework使用cgroup和namespace来和LXC容器协同工作，当然也可以和docker来一起工作。

