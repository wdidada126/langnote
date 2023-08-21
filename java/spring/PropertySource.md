# PropertySource注解简介

[PropertySource 简介](https://www.cnblogs.com/cxuanBlog/p/10927823.html)







总结：配合Environment  StandardEnvironment
Value
使用，加载配置文件中的变量，使变量的值跟java源代码分离

[PropertySource原理](http://www.imooc.com/article/252889?block_id=tuijian_wz)



org.springframework.context.annotation.PropertySource是一个注解，可以标记在类上、接口上、枚举上，在运行时起作用。



例子



- 定义一个application.properties 来写入如下配置

```properties
com.spring.name=liuXuan
com.spring.age=18
```



```java
@Configuration
  @PropertySource(value = "classpath:application.properties",ignoreResourceNotFound = false)
  public class SpringPropertysourceApplication {

    @Resource
    Environment environment;

    @Bean
    public TestBean testBean(){
      TestBean testBean = new TestBean();
      // 读取application.properties中的name
      testBean.setName(environment.getProperty("com.spring.name"));
      // 读取application.properties中的age
      testBean.setAge(Integer.valueOf(environment.getProperty("com.spring.age")));
      System.out.println("testBean = " + testBean);
      return testBean;
    }

    public static void main(String[] args) {
      ApplicationContext applicationContext = new AnnotationConfigApplicationContext(SpringPropertysourceApplication.class);
      TestBean testBean = (TestBean)applicationContext.getBean("testBean");

    }
  }
```



[PropertySource 注解基本使用](https://www.cnblogs.com/cxuanBlog/p/10927823.html)



### DisposableBean

org.springframework.beans.factory.DisposableBean



接口

```
void destroy() throws Exception;
```

bean生命周期



# Resource spring-core里面的类

我们可能需要处理URL资源、File资源资源、ClassPath相关资源、服务器相关资源（JBoss AS 5.x上的VFS资源）等等很多资源。因此处理这些资源需要使用不同的接口，这就增加了我们系统的复杂性；而且处理这些资源步骤都是类似的（打开资源、读取资源、关闭资源），因此如果能抽象出一个统一的接口来对这些底层资源进行统一访问，是不是很方便，而且使我们系统更加简洁，都是对不同的底层资源使用同一个接口进行访问。

​       Spring 提供一个Resource接口来统一这些底层资源一致的访问，而且提供了一些便利的接口，从而能提供我们的生产力。

**interface** Resource **extends** InputStreamSource



org.springframework.core.io.Resource



Resource接口提供了足够的抽象，足够满足我们日常使用。而且提供了很多内置Resource实现：ByteArrayResource、InputStreamResource 、FileSystemResource 、UrlResource 、ClassPathResource、ServletContextResource、VfsResource等。