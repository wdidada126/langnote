# Springboot揭秘

作者: 王福强
https://book.douban.com/subject/26808298/

ISBN: 9787111536642
出版年: 2016-5

目录

第1章了解微服务
1.1什么是微服务
1.2微服务因何而生
1.3微服务会带来哪些好处
1.3.1独立，独立，还是独立
1.3.2多语言生态
1.4微服务会带来哪些挑战
1.5本章小结
第2章饮水思源：回顾与探索Spring框架的本质
2.1Spring框架的起源
2.2Spring IoC其实很简单
2.3了解一点儿JavaConfig
2.3.1那些高曝光率的Annotation
2.4本章小结
第3章SpringBoot的工作机制
3.1SpringBoot初体验
3.2@SpringBootApplication背后的秘密
3.2.1@Configuration创世纪
3.2.2@EnableAutoConfiguration的功效
3.2.3可有可无的@ComponentScan
3.3SpringApplication：SpringBoot程序启动的一站式解决方案
3.3.1深入探索SpringApplication执行流程
3.3.2SpringApplicationRunListener
3.3.3ApplicationListener
3.3.4ApplicationContextInitializer
3.3.5CommandLineRunner
3.4再谈自动配置
3.4.1基于条件的自动配置
3.4.2调整自动配置的顺序
3.5本章小结
第4章了解纷杂的spring—boot—starter
4.1应用日志和spring—boot—starter—logging
4.2快速Web应用开发与spring—boot—starter—web
4.2.1项目结构层面的约定
4.2.2SpringMVC框架层面的约定和定制
4.2.3嵌入式Web容器层面的约定和定制
4.3数据访问与spring—boot—starter—jdbc
4.3.1SpringBoot应用的数据库版本化管理
4.4spring—boot—starter—aop及其使用场景说明
4.4.1spring—boot—starter—aop在构建spring—boot—starter—metrics自定义模块中的应用
4.5应用安全与spring—boot—starter—security
4.5.1了解SpringSecurity基本设计
4.5.2进一步定制spring—boot—starter—security
4.6应用监控与spring—boot—starter—actuator
4.6.1自定义应用的健康状态检查
4.6.2开放的endpoints才真正“有用”
4.6.3用还是不用，这是个问题
4.7本章小结
第5章SpringBoot微服务实践探索
5.1使用SpringBoot构建微服务
5.1.1创建基于Dubbo框架的SpringBoot微服务
5.1.2使用SpringBoot快速构建Web API
5.1.3使用SpringBoot构建其他形式的微服务
5.2SpringBoot微服务的发布与部署
5.2.1spring—boot—starter的发布与部署方式
5.2.2基于RPM的发布与部署方式
5.2.3基于Docker的发布与部署方式
5.3SpringBoot微服务的注册与发现
5.4SpringBoot微服务的监控与运维
5.4.1推还是拉，这一直是个问题
5.4.2从局部性触发式报警到系统性智能化报警
5.5SpringBoot微服务的安全与防护
5.6SpringBoot微服务体系的脊梁：发布与部署平台
5.7本章小结
第6章SpringBoot与Scala
6.1使用Maven构建和发布基于SpringBoot的Scala应用
6.1.1进一步简化基于Maven的Scala项目创建
6.1.2进一步简化基于Scala的Web API开发
6.2使用SBT构建和发布基于SpringBoot的Scala应用
6.2.1探索基于SBT的SpringBoot应用开发模式
6.2.2探索基于SBT的SpringBoot应用发布策略
6.3本章小结
第7章SpringBoot总结与展望


## 笔记

### 第3章SpringBoot的工作机制
@SpringBootApplication

SpringFactoriesLoader

@EnableAutoConfiguration自动配置的魔法其实就变成了：从classpath中搜寻所有META-INF/spring.factories配置文件，并将其中org.spring-framework.boot.autoconfigure.EnableAutoConfiguration对应的配置项通过反射（Java Reflection）实例化为对应的标注了@Configuration的JavaConfig形式的IoC容器配置类，然后汇总为一个并加载到IoC容器。

