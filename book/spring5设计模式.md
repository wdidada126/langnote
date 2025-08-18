# spring5设计模式

作者: Dinesh Rajput
出版社: 中国水利水电出版社
原作名: Spring 5 Design Patterns
译者: 梁桂钊 / 程超 / 祝坤荣
出版年: 2020-11
定价: 79.00
装帧: 平装
ISBN: 9787517090557

设计模式通过为常见问题提供经过充分测试和验证的解决方案，有助于加快开发过程。这些模式与Spring框架相结合，为开发过程提供了巨大的改进。 本书首先概述了Spring Framework 5.0和设计模式。您将了解依赖注入模式，这是Spring执行的解耦过程背后的主要原则，从而使管理代码变得更加容易。您将了解如何在Application Design中使用GoF模式。然后，您将学习在面向方面编程和远程处理中使用代理模式。接下来，您将了解JDBC模板模式及其在抽象数据库访问中的用途。然后，您将了解MVC模式以构建ReactiveWeb应用程序。最后，您将继续学习更高级的主题，例如Reactivestreams和Concurrency。 完成对于本书的学习后，您将能够使用具有通用设计模式的Spring 5开发高效的企业应用程序。

Dinesh Rajput是Dineshonjava网站的主编。Dineshonjava网站是一个专门介绍Spring和Java的技术博客。Dinesh从2008年至今都是一名Spring爱好者，同时也是一名Pivotal认证的Spring专家、作家和博主。他在Spring和Java领域拥有超过10年的设计与开发经验。他擅长于Spring、Spring Boot, Spring Security、REST APIs、微服务架构、响应式模式、Spring AOP、设计模式、Struts、Hibernate、Web Services、Spring Batch、 Cassandra、MongoDB以及Web应用程序设计和架构。

目录
第1章 Spring 5框架和设计模式入门
1.1 Spring框架简介
1.2 使用Spring及其模式来简化应用程序开发
1.2.1 使用POJO模式
1.2.2 在POJO之间依赖注入
1.2.3 对依赖组件使用DI模式
1.2.4 应用层面横切关注点
1.2.5 使用模板模式消除样板代码
1.3 使用Spring容器通过工厂模式管理Bean
1.3.1 Bean工厂
1.3.2 应用上下文
1.3.3 使用应用上下文创建容器
1.4 容器里Bean的生命周期
1.5 Spring模块
1.5.1 Spring核心容器
1.5.2 Spring AOP模块
1.5.3 Spring DAO——数据访问与集成
1.5.4 Spring ORM
1.5.5 Spring Web MVC
1.6 Spring Framework 5中的新功能
1.7 小结
第2章 GoF设计模式概述：核心设计模式
2.1 设计模式的力量简介
2.2 常见的GoF设计模式概述
2.3 创建模式
2.3.1 工厂模式
2.3.2 抽象工厂模式
2.3.3 单例模式
2.3.4 原型模式
2.3.5 建造者模式
2.4 小结
第3章 结构模式和行为模式
3.1 审视核心的设计模式结构模式
3.2 J2EE设计模式
3.3 小结
第4章 使用依赖注入模式装配Bean
4.1 依赖注入模式
使用依赖注入模式解决问题
4.2 依赖注入模式的类型
4.2.1 基于构造方法的依赖注入
4.2.2 基于setter的依赖注入
4.3 使用Spring配置依赖注入模式
4.4 基于Java配置的依赖注入模式
创建Java配置类——AppConfig.java
4.5 基于XML配置的依赖注入模式
创建XML配置文件
4.6 基于注解配置的依赖注入模式
4.6.1 什么是构造型注解
4.6.2 自动装配的DI模式与歧义
4.7 配置DI模式的最佳实践
4.8 小结
第5章 理解Bean的生命周期和使用模式
5.1 Spring生命周期及其阶段
5.1.1 初始化阶段
5.1.2 Bean的使用阶段
5.1.3 Bean的销毁阶段
5.2 理解Bean作用域
5.2.1 单例作用域
5.2.2 原型作用域
5.2.3 Session Bean作用域
5.2.4 Request Bean作用域
5.2.5 Spring中的其他作用域
5.3 小结
第6章 基于代理和装饰模式的面向Spring切面编程
6.1 Spring的代理模式
在Spring中使用装饰模式代理类
6.2 什么是横切关注点
6.3 什么是面向切面的编程
6.3.1 AOP解决的问题
6.3.2 AOP如何解决问题
6.4 核心AOP术语和概念
6.5 定义切入点写切入点
6.6 创建切面
使用注解来定义切面
6.7 实现增强
6.8 使用XML配置定义切面
6.9 Spring如何创建AOP代理
6.10 小结
第7章 使用Spring和JDBC模板模式访问数据库
7.1 设计数据访问的最佳方法
7.1.1 资源管理问题
7.1.2 实现模板模式
7.2 配置数据源和对像池模式
7.2.1 使用JDBC驱动来配置一个数据源
7.2.2 使用连接池来配置数据源
7.3 实现建造者模式创建嵌人式数据源
使用DAO模式抽像数据库访问
7.4 带有Spring框架的DAO模式
7.4.1 使用JdbcTemplate
7.4. 2何时使用JdbcTemplate
7.5 配置JdbcTemplate的最佳实践
7.6 小结
第8章 使Spring ORM访问数据库和事务的实现模式
8.1 ORM框架和使用的模式
8.2 数据访问对像模式
8.2.1 Spring使用工厂模式创建DAO
8.2.2 数据映射模式
8.2.3 领域模型模式
8.2.4 懒加载模式的代理
8.2.5 Spring的Hibernate Template模式
8.3 将Spring与Hibemate集成
8.3.1 在Spring容器中配置Hibernate的SessionFactory
8.3.2 以Hibemate API为基础实现DAO
8.4 Spring事务管理策略
8.4.1 声明式事务的边界与实现
8.4.2 部署事务管理器
8.4.3 编程事务的边界确定与实现
8.5 在程序中Spring ORM和事务模块的最佳实践
8.6 小结
第9章 使用缓存模式改进应用性能
9.1 什么是缓存
9.2 理解缓存抽象
9.3 使用Proxy模式开启缓存
9.3.1 使用Annotation开启缓存代理
9.3.2 使用XML命名空间开启缓存代理
9.4 声明基于Annotation的缓存
9.5 声明基于XML的缓存
9.6 配置缓存的存储
9.7 第三方缓存实现
9.8 创建自定义缓存声明
9.9 网络应用
9.10 小结
第10章 在Web应用中使用Spring实现MVC模式
10.1 在Web应用中实现MVC模式
10.2 Spring的Model 2架构MVc模式
前端控制器Front Controller设计模式
10.3 开启Spring MVC
10.3.1 实现controller
10.3.2 用@RequestMapping映射请求
10.4 传递模型数据给View视图
10.4.1 接受请求参数
10.4.2 处理Web页面的表单
10.4.3 实现一个表单处理controller
10.5 使用Command设计模式进行数据绑定
使用@ModelAttributes定制数据绑定
10.6 校验表单输人参数
10.7 在MVC模式中实现View视图
10.7.1 在Spring MVC中定义ViewResolver
10.7.2 View Helper模式
10.7.3 使用Apache tile视图解析器的组合视图模式
10.8 Web应用设计的最佳实践
10.9 小结
第11章 实现响应式设计模式
11.1 了解多年的应用需求
11.2 理解响应式模式
响应模式特性
11.3 阻塞调用
11.4 非阻塞调用
11.5 背压
11.6 使用Spring 5框架实现响应式
11.7 Spring Web响应流
11.8 请求和响应体转换
11.9 小结
第12章 实现并发模式
12.1 主动对像模式
12.2 监视器对像模式
12.3 半同步/半异步模式
12.4 领导者/跟随者模式
12.5 反应器模式
12.6 线程独有的存储库模式
12.7 小结
