# SpringBoot源码解读与原理分析

ISBN:9787115601377
出版年: 2023-2-1
https://book.douban.com/subject/36244230/

LinkedBear，Java开发工程师、底层技术研究者与分享者，倾心研究Spring技术体系多年，对Spring、Spring Boot等框架有独到的见解，拥有丰富的框架体系实践经验和架构封装经验。
本书引用的源码均基于Spring Boot 2.3.11.RELEASE 5.附赠本书附带的测试代码与课件

https://gitee.com/edidada/spring-boot-source-analysis-epubit


https://blog.csdn.net/qq_17231297/article/details/129659507


博主课程
https://juejin.cn/user/3808363977640301/course

本书对应的课程
https://juejin.cn/book/6844733814560784397?utm_source=profile_book



| 课程内容 已完结                                             |      |      |
| ----------------------------------------------------------- | ---- | ---- |
| 1开篇：为什么要了解SpringBoot原理？                         |      |      |
| 2开始前的约定：关于本小册的一些前置说明                     |      |      |
| 3启动引导：SpringBoot入门程序原理概述和包扫描               |      |      |
| 4启动引导：SpringBoot的核心-自动装配（一）                  |      |      |
| 5启动引导：SpringBoot的核心-自动装配（二）                  |      |      |
| 6启动引导：SpringBoot的自动装配实例-WebMvc                  |      |      |
| 7IOC：SpringFramework与SpringBoot的IOC                      |      |      |
| 8IOC：SpringBoot准备IOC容器                                 |      |      |
| 9IOC：准备运行时环境                                        |      |      |
| 10IOC：创建、初始化IOC容器                                  |      |      |
| 11IOC：刷新容器-BeanFactory的预处理                         |      |      |
| 12IOC：刷新容器-BeanFactory的后处理和组件扫描               |      |      |
| 13IOC：刷新容器-后置处理器、监听器的注册                    |      |      |
| 14IOC：刷新容器-初始化剩余的单实例Bean                      |      |      |
| 15IOC：刷新容器-循环依赖与解决方案                          |      |      |
| 16IOC：刷新后的处理&SpringBoot在刷新容器时的扩展            |      |      |
| 17IOC：小结与收获                                           |      |      |
| 18AOP：注解使用AOP基础与@EnableAspectJAutoProxy的作用       |      |      |
| 19AOP：AnnotationAwareAspectJAutoProxyCreator的后置处理功能 |      |      |
| 20AOP：jdk动态代理&Cglib的执行调用链                        |      |      |
| 21声明式事务：生效原理                                      |      |      |
| 22声明式事务：工作原理                                      |      |      |
| 23声明式事务：事务传播行为原理                              |      |      |
| 24AOP+事务：小结与收获                                      |      |      |
| 25WebMvc：自动装配回顾与DispatcherServlet组件               |      |      |
| 26WebMvc：DispatcherServlet的工作原理                       |      |      |
| 27嵌入式容器：创建过程回顾和深入配置                        |      |      |
| 28嵌入式容器：嵌入式Tomcat的优化和配置                      |      |      |
| 29WebFlux：快速了解响应式编程与Reactive                     |      |      |
| 30WebFlux：快速使用WebFlux                                  |      |      |
| 31WebFlux：WebFlux的自动装配                                |      |      |
| 32WebFlux：DispatcherHandler的工作原理-传统方式             |      |      |
| 33WebFlux：DispatcherHandler的工作原理-函数式端点           |      |      |
| 34JarLauncher：应用打jar包后的运行原理                      |      |      |
| 35尾声：源码不是终点                                        |      |      |
| 36问题反馈与汇总                                            |      |      |
| 37小册内容变动记录                                          |      |      |





### 19 AnnotationAwareAspectJAutoProxyCreator的后置处理功能



AnnotationAwareAspectJAutoProxyCreator就是继承了AbstractAutoProxyCreator类，它是Spring AOP框架中的自动代理创建器，用于自动为标注了AspectJ注解的类创建代理对象，并将增强逻辑织入到代理对象中。

