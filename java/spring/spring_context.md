# context

org.springframework.context.annotation.ImportResource

spring-context.xlsx

spring-context2.xlsx

spring-context_4.xlsx

spring-context_cache.xlsx

spring-context_remote.xlsx

spring-context_jmx.xlsx





Spring Security 提供了诸多的 TokenStore 实现，如存在内存中的 InMemoryTokenStore 、存在数据库中的 JdbcTokenStore、存在 Redis 中的 RedisTokenStore

https://www.jianshu.com/p/64f2ee59acd9

org.springframework.context.annotation.ImportResource


ComponentScanAnnotationParser

org.springframework.context.annotation.ConfigurationClassParser#ConfigurationClassParser 中用ComponentScanAnnotationParser





## 源代码分包详解v5.2.9

https://docs.spring.io/spring-framework/docs/5.2.x/javadoc-api/



### org.springframework.cache



| org.springframework.cache     | 类型      | 详解 |
| ----------------------------- | --------- | ---- |
| Cache                         | interface |      |
| Cache.ValueRetrievalException | exception |      |
| Cache.ValueWrapper            | interface |      |
| CacheManager                  |           |      |
|                               |           |      |

#### org.springframework.cache.annotation



| org.springframework.cache.annotation                  | 类型 | 详解 |
| ----------------------------------------------------- | ---- | ---- |
|                                                       |      |      |
| Interfaces                                            |      |      |
|                                                       |      |      |
| AnnotationCacheOperationSource.CacheOperationProvider |      |      |
| CacheAnnotationParser                                 |      |      |
| CachingConfigurer                                     |      |      |
|                                                       |      |      |
| Classes                                               |      |      |
|                                                       |      |      |
| AbstractCachingConfiguration                          |      |      |
| AnnotationCacheOperationSource                        |      |      |
| CachingConfigurationSelector                          |      |      |
| CachingConfigurerSupport                              |      |      |
| ProxyCachingConfiguration                             |      |      |
| SpringCacheAnnotationParser                           |      |      |
|                                                       |      |      |
| Annotation Types                                      |      |      |
|                                                       |      |      |
| Cacheable                                             |      |      |
| CacheConfig                                           |      |      |
| CacheEvict                                            |      |      |
| CachePut                                              |      |      |
| Caching                                               |      |      |
| EnableCaching                                         |      |      |

#### org.springframework.cache.concurrent

| org.springframework.cache.concurrent | 类型 | 详解 |
| ------------------------------------ | ---- | ---- |
| ConcurrentMapCache                   |      |      |
| ConcurrentMapCacheFactoryBean        |      |      |
| ConcurrentMapCacheManager            |      |      |



#### org.springframework.cache.config

| org.springframework.cache.config                             | 类型     | 详解                        |
| ------------------------------------------------------------ | -------- | --------------------------- |
| AnnotationDrivenCacheBeanDefinitionParser                    |          |                             |
| AnnotationDrivenCacheBeanDefinitionParser.JCacheCachingConfigurer |          |                             |
| AnnotationDrivenCacheBeanDefinitionParser.SpringCachingConfigurer |          |                             |
| CacheAdviceParser                                            |          |                             |
| CacheAdviceParser.Props                                      |          |                             |
| CacheManagementConfigUtils                                   | abstract |                             |
| CacheNamespaceHandler                                        |          | NamespaceHandlerSupport子类 |



#### org.springframework.cache.interceptor

| org.springframework.cache.interceptor     | 类型 | 详解 |
| ----------------------------------------- | ---- | ---- |
|                                           |      |      |
| BasicOperation                            |      |      |
| CacheErrorHandler                         |      |      |
| CacheOperationInvocationContext           |      |      |
| CacheOperationInvoker                     |      |      |
| CacheOperationSource                      |      |      |
| CacheResolver                             |      |      |
| KeyGenerator                              |      |      |
|                                           |      |      |
| Classes                                   |      |      |
|                                           |      |      |
| AbstractCacheInvoker                      |      |      |
| AbstractCacheResolver                     |      |      |
| AbstractFallbackCacheOperationSource      |      |      |
| BeanFactoryCacheOperationSourceAdvisor    |      |      |
| CacheableOperation                        |      |      |
| CacheableOperation.Builder                |      |      |
| CacheAspectSupport                        |      |      |
| CacheAspectSupport.CacheOperationMetadata |      |      |
| CacheEvictOperation                       |      |      |
| CacheEvictOperation.Builder               |      |      |
| CacheInterceptor                          |      |      |
| CacheOperation                            |      |      |
| CacheOperation.Builder                    |      |      |
| CacheProxyFactoryBean                     |      |      |
| CachePutOperation                         |      |      |
| CachePutOperation.Builder                 |      |      |
| CompositeCacheOperationSource             |      |      |
| NamedCacheResolver                        |      |      |
| NameMatchCacheOperationSource             |      |      |
| SimpleCacheErrorHandler                   |      |      |
| SimpleCacheResolver                       |      |      |
| SimpleKey                                 |      |      |
| SimpleKeyGenerator                        |      |      |
|                                           |      |      |
| Exceptions                                |      |      |
|                                           |      |      |
| CacheOperationInvoker.ThrowableWrapper    |      |      |

#### org.springframework.cache.support

| org.springframework.cache.support | 类型 | 详解 |
| --------------------------------- | ---- | ---- |
|                                   |      |      |
| Classes                           |      |      |
|                                   |      |      |
| AbstractCacheManager              |      |      |
| AbstractValueAdaptingCache        |      |      |
| CompositeCacheManager             |      |      |
| NoOpCache                         |      |      |
| NoOpCacheManager                  |      |      |
| NullValue                         |      |      |
| SimpleCacheManager                |      |      |
| SimpleValueWrapper                |      |      |



### org.springframework.context





| org.springframework.context    | 类型 | 详解 |
| ------------------------------ | ---- | ---- |
|                                |      |      |
| Interfaces                     |      |      |
|                                |      |      |
| ApplicationContext             |      |      |
| ApplicationContextAware        |      |      |
| ApplicationContextInitializer  |      |      |
| ApplicationEventPublisher      |      |      |
| ApplicationEventPublisherAware |      |      |
| ApplicationListener            |      |      |
| ConfigurableApplicationContext |      |      |
| EmbeddedValueResolverAware     |      |      |
| EnvironmentAware               |      |      |
| HierarchicalMessageSource      |      |      |
| Lifecycle                      |      |      |
| LifecycleProcessor             |      |      |
| MessageSource                  |      |      |
| MessageSourceAware             |      |      |
| MessageSourceResolvable        |      |      |
| Phased                         |      |      |
| ResourceLoaderAware            |      |      |
| SmartLifecycle                 |      |      |
|                                |      |      |
| Classes                        |      |      |
|                                |      |      |
| ApplicationEvent               |      |      |
| PayloadApplicationEvent        |      |      |
|                                |      |      |
| Exceptions                     |      |      |
|                                |      |      |
| ApplicationContextException    |      |      |
| NoSuchMessageException         |      |      |



#### org.springframework.context.annotation




| org.springframework.context.annotation          | 类型       |      | 详解                                                         |                                                              |      |
| ----------------------------------------------- | ---------- | ---- | ------------------------------------------------------------ | ------------------------------------------------------------ | ---- |
| AdviceMode                                      |            |      | Enumeration used to determine whether JDK proxy-based or AspectJ weaving-based advice should be applied. |                                                              |      |
| AdviceModeImportSelector<A extends Annotation>  |            |      | Convenient base class for ImportSelector implementations that select imports based on an AdviceMode value from an annotation (such as the @Enable* annotations). |                                                              |      |
|                                                 |            |      |                                                              |                                                              |      |
| AnnotatedBeanDefinitionReader                   |            |      | Convenient adapter for programmatic registration of bean classes. |                                                              |      |
|                                                 |            |      |                                                              |                                                              |      |
| AnnotationBeanNameGenerator                     |            |      | BeanNameGenerator implementation for bean classes annotated with the @Component annotation or with another annotation that is itself annotated with @Component as a meta-annotation. |                                                              |      |
|                                                 |            |      |                                                              |                                                              |      |
| AnnotationConfigApplicationContext              |            |      | Standalone application context, accepting component classes as input — in particular @Configuration-annotated classes, but also plain @Component types and JSR-330 compliant classes using jakarta.inject annotations. |                                                              |      |
|                                                 |            |      |                                                              |                                                              |      |
| AnnotationConfigBeanDefinitionParser            |            |      | Parser for the <context:annotation-config/> element.         |                                                              |      |
|                                                 |            |      |                                                              |                                                              |      |
| AnnotationConfigRegistry                        |            |      | Common interface for annotation config application contexts, defining AnnotationConfigRegistry.register(java.lang.Class<?>...) and AnnotationConfigRegistry.scan(java.lang.String...) methods. |                                                              |      |
|                                                 |            |      |                                                              |                                                              |      |
| AnnotationConfigUtils                           |            |      | Utility class that allows for convenient registration of common BeanPostProcessor and BeanFactoryPostProcessor definitions for annotation-based configuration. |                                                              |      |
|                                                 |            |      |                                                              |                                                              |      |
| AnnotationScopeMetadataResolver                 |            |      | A ScopeMetadataResolver implementation that by default checks for the presence of Spring's @Scope annotation on the bean class. |                                                              |      |
|                                                 |            |      |                                                              |                                                              |      |
| AutoProxyRegistrar                              |            |      | Registers an auto proxy creator against the current BeanDefinitionRegistry as appropriate based on an @Enable* annotation having mode and proxyTargetClass attributes set to the correct values. |                                                              |      |
|                                                 |            |      |                                                              |                                                              |      |
| Bean                                            | @interface |      | Indicates that a method produces a bean to be managed by the Spring container. |                                                              |      |
|                                                 |            |      |                                                              |                                                              |      |
| **ClassPathBeanDefinitionScanner**              |            |      | A bean definition scanner that detects bean candidates on the classpath, registering corresponding bean definitions with a given registry (BeanFactory or ApplicationContext). | ClassPathScanningCandidateComponentProvider子类 scan() doScan() addIncludeFilter() 很多三方框架都自定义这个类的子类 |      |
|                                                 |            |      |                                                              |                                                              |      |
| ClassPathScanningCandidateComponentProvider     |            |      | A component provider that provides candidate components from a base package. |                                                              |      |
|                                                 |            |      |                                                              |                                                              |      |
| CommonAnnotationBeanPostProcessor               |            |      | BeanPostProcessor implementation that supports common Java annotations out of the box, in particular the common annotations in the jakarta.annotation package. |                                                              |      |
|                                                 |            |      |                                                              |                                                              |      |
| CommonAnnotationBeanPostProcessor.LookupElement |            |      | Class representing generic injection information about an annotated field or setter method, supporting @Resource and related annotations. |                                                              |      |
|                                                 |            |      |                                                              |                                                              |      |
| ComponentScan                                   | @interface |      | Configures component scanning directives for use with @Configuration classes. |                                                              |      |
|                                                 |            |      |                                                              |                                                              |      |
| ComponentScanAnnotationParser                   |            |      |                                                              | @ComponentScan会被解析为一个Bean定义扫描器                   |      |
|                                                 |            |      |                                                              |                                                              |      |
| ComponentScan.Filter                            |            |      | Declares the type filter to be used as an include filter or exclude filter. |                                                              |      |
|                                                 |            |      |                                                              |                                                              |      |
| ComponentScanBeanDefinitionParser               |            |      | Parser for the <context:component-scan/> element.            |                                                              |      |
|                                                 |            |      |                                                              |                                                              |      |
| ComponentScans                                  |            |      | Container annotation that aggregates several ComponentScan annotations. |                                                              |      |
|                                                 |            |      |                                                              |                                                              |      |
| Condition                                       |            |      | A single condition that must be matched in order for a component to be registered. |                                                              |      |
|                                                 |            |      |                                                              |                                                              |      |
| Conditional                                     | @interface |      | Indicates that a component is only eligible for registration when all specified conditions match. |                                                              |      |
|                                                 |            |      |                                                              |                                                              |      |
| ConditionContext                                |            |      | Context information for use by Condition implementations.    |                                                              |      |
|                                                 |            |      |                                                              |                                                              |      |
| Configuration                                   | @interface |      | Indicates that a class declares one or more @Bean methods and may be processed by the Spring container to generate bean definitions and service requests for those beans at runtime, for example: |                                                              |      |
|                                                 |            |      |                                                              |                                                              |      |
| ConfigurationClassPostProcessor                 |            |      | BeanFactoryPostProcessor used for bootstrapping processing of @Configuration classes. | processConfigBeanDefinitions()核心方法                       |      |
| ConfigurationClassUtils                         |            |      | Utilities for identifying and configuring Configuration classes. |                                                              |      |
|                                                 |            |      |                                                              |                                                              |      |
| ConfigurationCondition                          |            |      | A Condition that offers more fine-grained control when used with @Configuration. |                                                              |      |
|                                                 |            |      |                                                              |                                                              |      |
| ConfigurationCondition.ConfigurationPhase       |            |      | The various configuration phases where the condition could be evaluated. |                                                              |      |
|                                                 |            |      |                                                              |                                                              |      |
| ContextAnnotationAutowireCandidateResolver      |            |      | Complete implementation of the AutowireCandidateResolver strategy interface, providing support for qualifier annotations as well as for lazy resolution driven by the Lazy annotation in the context.annotation package. |                                                              |      |
|                                                 |            |      |                                                              |                                                              |      |
| DeferredImportSelector                          |            |      | A variation of ImportSelector that runs after all @Configuration beans have been processed. |                                                              |      |
|                                                 |            |      |                                                              |                                                              |      |
| DeferredImportSelector.Group                    |            |      | Interface used to group results from different import selectors. |                                                              |      |
|                                                 |            |      |                                                              |                                                              |      |
| DeferredImportSelector.Group.Entry              |            |      | An entry that holds the AnnotationMetadata of the importing Configuration class and the class name to import. |                                                              |      |
|                                                 |            |      |                                                              |                                                              |      |
| DependsOn                                       | @interface |      | Beans on which the current bean depends.                     |                                                              |      |
|                                                 |            |      |                                                              |                                                              |      |
| Description                                     | @interface |      | Adds a textual description to bean definitions derived from Component or Bean. |                                                              |      |
|                                                 |            |      |                                                              |                                                              |      |
| EnableAspectJAutoProxy                          | @interface |      | Enables support for handling components marked with AspectJ's @Aspect annotation, similar to functionality found in Spring's <aop:aspectj-autoproxy> XML element. |                                                              |      |
|                                                 |            |      |                                                              |                                                              |      |
| EnableLoadTimeWeaving                           | @interface |      | "Activates a Spring LoadTimeWeaver for this application context, available as a bean with the name ""loadTimeWeaver"", similar to the <context:load-time-weaver> element in Spring XML." |                                                              |      |
|                                                 |            |      |                                                              |                                                              |      |
| EnableLoadTimeWeaving.AspectJWeaving            | @interface |      | AspectJ weaving enablement options.                          |                                                              |      |
|                                                 |            |      |                                                              |                                                              |      |
| EnableMBeanExport                               |            |      | Enables default exporting of all standard MBeans from the Spring context, as well as all @ManagedResource annotated beans. |                                                              |      |
|                                                 |            |      |                                                              |                                                              |      |
| FilterType                                      |            |      | Enumeration of the type filters that may be used in conjunction with @ComponentScan. |                                                              |      |
|                                                 |            |      |                                                              |                                                              |      |
| FullyQualifiedAnnotationBeanNameGenerator       |            |      | An extension of AnnotationBeanNameGenerator that uses the fully qualified class name as the default bean name if an explicit bean name is not supplied via a supported type-level annotation such as @Component (see AnnotationBeanNameGenerator for details on supported annotations). |                                                              |      |
|                                                 |            |      |                                                              |                                                              |      |
| Import                                          | @interface |      | Indicates one or more component classes to import — typically @Configuration classes. |                                                              |      |
|                                                 |            |      |                                                              |                                                              |      |
| ImportAware                                     |            |      | Interface to be implemented by any @Configuration class that wishes to be injected with the AnnotationMetadata of the @Configuration class that imported it. |                                                              |      |
|                                                 |            |      |                                                              |                                                              |      |
| ImportAwareAotBeanPostProcessor                 |            |      | A BeanPostProcessor that honours ImportAware callback using a mapping computed at build time. |                                                              |      |
|                                                 |            |      |                                                              |                                                              |      |
| ImportBeanDefinitionRegistrar                   |            |      | Interface to be implemented by types that register additional bean definitions when processing @Configuration classes. |                                                              |      |
|                                                 |            |      |                                                              |                                                              |      |
| ImportResource                                  | @interface |      | Indicates one or more resources containing bean definitions to import. |                                                              |      |
|                                                 |            |      |                                                              |                                                              |      |
| ImportRuntimeHints                              |            |      | Indicates that one or more RuntimeHintsRegistrar implementations should be processed. |                                                              |      |
|                                                 |            |      |                                                              |                                                              |      |
| ImportSelector                                  |            |      | Interface to be implemented by types that determine which @Configuration class(es) should be imported based on a given selection criteria, usually one or more annotation attributes. |                                                              |      |
|                                                 |            |      |                                                              |                                                              |      |
| Jsr330ScopeMetadataResolver                     |            |      | Simple ScopeMetadataResolver implementation that follows JSR-330 scoping rules: defaulting to prototype scope unless Singleton is present. |                                                              |      |
|                                                 |            |      |                                                              |                                                              |      |
| Lazy                                            | @interface |      | Indicates whether a bean is to be lazily initialized.        |                                                              |      |
|                                                 |            |      |                                                              |                                                              |      |
| LoadTimeWeavingConfiguration                    |            |      | @Configuration class that registers a LoadTimeWeaver bean.   |                                                              |      |
|                                                 |            |      |                                                              |                                                              |      |
| LoadTimeWeavingConfigurer                       |            |      | Interface to be implemented by @Configuration classes annotated with @EnableLoadTimeWeaving that wish to customize the LoadTimeWeaver instance to be used. |                                                              |      |
|                                                 |            |      |                                                              |                                                              |      |
| MBeanExportConfiguration                        |            |      | @Configuration class that registers a AnnotationMBeanExporter bean. |                                                              |      |
|                                                 |            |      |                                                              |                                                              |      |
| Primary                                         | @interface |      | Indicates that a bean should be given preference when multiple candidates are qualified to autowire a single-valued dependency. |                                                              |      |
|                                                 |            |      |                                                              |                                                              |      |
| Profile                                         | @interface |      | Indicates that a component is eligible for registration when one or more specified profiles are active. |                                                              |      |
|                                                 |            |      |                                                              |                                                              |      |
| PropertySource                                  | @interface |      | Annotation providing a convenient and declarative mechanism for adding a PropertySource to Spring's Environment. |                                                              |      |
|                                                 |            |      |                                                              |                                                              |      |
| PropertySources                                 |            |      | Container annotation that aggregates several PropertySource annotations. |                                                              |      |
|                                                 |            |      |                                                              |                                                              |      |
| Role                                            | @interface |      | Indicates the 'role' hint for a given bean.                  |                                                              |      |
|                                                 |            |      |                                                              |                                                              |      |
| ScannedGenericBeanDefinition                    |            |      | Extension of the GenericBeanDefinition class, based on an ASM ClassReader, with support for annotation metadata exposed through the AnnotatedBeanDefinition interface. |                                                              |      |
|                                                 |            |      |                                                              |                                                              |      |
| Scope                                           | @interface |      | When used as a type-level annotation in conjunction with @Component, @Scope indicates the name of a scope to use for instances of the annotated type. |                                                              |      |
|                                                 |            |      |                                                              |                                                              |      |
| ScopedProxyMode                                 |            |      | Enumerates the various scoped-proxy options.                 |                                                              |      |
|                                                 |            |      |                                                              |                                                              |      |
| ScopeMetadata                                   |            |      | Describes scope characteristics for a Spring-managed bean including the scope name and the scoped-proxy behavior. |                                                              |      |
|                                                 |            |      |                                                              |                                                              |      |
| ScopeMetadataResolver                           |            |      | Strategy interface for resolving the scope of bean definitions. |                                                              |      |
|                                                 |            |      |                                                              |                                                              |      |
| TypeFilterUtils                                 |            |      | Collection of utilities for working with @ComponentScan type filters. |                                                              |      |
|                                                 |            |      |                                                              |                                                              |      |
| EnableSpringConfigured                          |            |      | Signals the current application context to apply dependency injection to non-managed classes that are instantiated outside the Spring bean factory (typically classes annotated with the @Configurable annotation). |                                                              |      |
|                                                 |            |      |                                                              |                                                              |      |
| SpringConfiguredConfiguration                   |            |      | @Configuration class that registers an AnnotationBeanConfigurerAspect capable of performing dependency injection services for non-Spring managed objects annotated with @Configurable. |                                                              |      |
|                                                 |            |      |                                                              |                                                              |      |





```
AnnotationConfigRegistry子类
```



AnnotationConfigServletWebServerApplicationContext (org.springframework.boot.web.servlet.context)
AnnotationConfigReactiveWebServerApplicationContext (org.springframework.boot.web.reactive.context)
AnnotationConfigWebApplicationContext (org.springframework.web.context.support)
AnnotationConfigApplicationContext (org.springframework.context.annotation)
    AnnotationConfigReactiveWebApplicationContext (org.springframework.boot.web.reactive.context)
AnnotationConfigServletWebApplicationContext (org.springframework.boot.web.servlet.context)





org.springframework.context.annotation.AnnotatedBeanDefinitionReader#doRegisterBean 断点





```
doRegisterBean:253, AnnotatedBeanDefinitionReader (org.springframework.context.annotation)
registerBean:147, AnnotatedBeanDefinitionReader (org.springframework.context.annotation)
register:137, AnnotatedBeanDefinitionReader (org.springframework.context.annotation)
load:157, BeanDefinitionLoader (org.springframework.boot)
load:136, BeanDefinitionLoader (org.springframework.boot)
load:128, BeanDefinitionLoader (org.springframework.boot)
load:691, SpringApplication (org.springframework.boot)
prepareContext:392, SpringApplication (org.springframework.boot)
run:314, SpringApplication (org.springframework.boot)
run:1237, SpringApplication (org.springframework.boot)
run:1226, SpringApplication (org.springframework.boot)

```





org.springframework.boot.BeanDefinitionLoader#annotatedReader 中有该类的对象





```
ImportAware接口实现类 LoadTimeWeavingConfiguration
```





org.springframework.context.annotation.ConfigurationClassPostProcessor#postProcessBeanFactory

代码

```
beanFactory.addBeanPostProcessor(new ImportAwareBeanPostProcessor(beanFactory));
```





PropertySource注解

@Repeatable(PropertySources.class)
public @interface PropertySource {
    
用法例子
   ```java
   import org.springframework.beans.factory.annotation.Value;
   import org.springframework.context.annotation.PropertySource;
   import org.springframework.stereotype.Component;

   @Component
   @PropertySource("classpath:config.properties")
   public class ConfigReader {
       @Value("${key}")
       private String value;

       public void printValue() {
           System.out.println("Value: " + value);
       }
   }
   ```


AnnotatedBeanDefinitionReader
`AnnotatedBeanDefinitionReader` 是 Spring 框架中的一个类，它的作用是将带有注解的类转换成 Bean 定义（BeanDefinition），并将这些 Bean 定义注册到 Spring 应用上下文中。
在 Spring 中，Bean 定义是描述 Spring 容器中的 Bean 的元数据，它包含了 Bean 的类名、作用域、属性、构造函数参数等信息。通常情况下，我们可以通过 XML 配置文件或者 Java 配置类来定义 Bean，但是 Spring 还提供了一种方式，即使用注解来定义 Bean。
`AnnotatedBeanDefinitionReader` 类就是用于处理这种注解方式的 Bean 定义。它可以扫描指定的包路径，查找带有特定注解的类，并将这些类转换成对应的 Bean 定义。常用的注解包括 `@Component`、`@Service`、`@Repository`、`@Controller` 等。
使用 `AnnotatedBeanDefinitionReader` 可以使 Bean 的定义更加简洁，避免了繁琐的 XML 配置或 Java 配置类的编写。同时，它也提供了更加灵活的方式对 Bean 进行定制。
需要注意的是，要使用 `AnnotatedBeanDefinitionReader`，你需要先创建一个空的 `BeanDefinitionRegistry` 对象，然后将其作为参数传递给 `AnnotatedBeanDefinitionReader` 的构造函数，最后使用 `register` 方法将 Bean 定义注册到该对象中。





ClassPathScanningCandidateComponentProvider

<context:component-scan base-package="cn.edidada.test.testspring32.scan.service" />





```shell
14:43:14.878 TRACE org.springframework.context.annotation.ClassPathScanningCandidateComponentProvider 425 scanCandidateComponents - Scanning file [D:\testspring32\target\classes\cn\edidada\test\testspring32\scan\service\NotifyService.class]
14:43:14.891 TRACE org.springframework.context.annotation.ClassPathScanningCandidateComponentProvider 447 scanCandidateComponents - Ignored because not matching any filter: file [D:\testspring32\target\classes\cn\edidada\test\testspring32\scan\service\NotifyService.class]
14:43:14.891 TRACE org.springframework.context.annotation.ClassPathScanningCandidateComponentProvider 425 scanCandidateComponents - Scanning file [D:\testspring32\target\classes\cn\edidada\test\testspring32\scan\service\Order.class]
14:43:14.909 DEBUG org.springframework.context.annotation.ClassPathScanningCandidateComponentProvider 435 scanCandidateComponents - Identified candidate component class: file [D:\testspring32\target\classes\cn\edidada\test\testspring32\scan\service\Order.class]
14:43:14.909 TRACE org.springframework.context.annotation.ClassPathScanningCandidateComponentProvider 425 scanCandidateComponents - Scanning file [D:\testspring32\target\classes\cn\edidada\test\testspring32\scan\service\impl\NotifyServiceByCellPhoneImpl.class]
14:43:14.910 DEBUG org.springframework.context.annotation.ClassPathScanningCandidateComponentProvider 435 scanCandidateComponents - Identified candidate component class: file [D:\testspring32\target\classes\cn\edidada\test\testspring32\scan\service\impl\NotifyServiceByCellPhoneImpl.class]
14:43:14.910 TRACE org.springframework.context.annotation.ClassPathScanningCandidateComponentProvider 425 scanCandidateComponents - Scanning file [D:\testspring32\target\classes\cn\edidada\test\testspring32\scan\service\impl\NotifyServiceByWeixinImpl.class]
14:43:14.911 TRACE org.springframework.context.annotation.ClassPathScanningCandidateComponentProvider 447 scanCandidateComponents - Ignored because not matching any filter: file [D:\testspring32\target\classes\cn\edidada\test\testspring32\scan\service\impl\NotifyServiceByWeixinImpl.class]
```







#### org.springframework.context.config



| org.springframework.context.config | 类型 |      |
| ---------------------------------- | ---- | ---- |
|                                    |      |      |
| Classes                            |      |      |
|  AbstractPropertyLoadingBeanDefinitionParser          |  abstract    |      |
| ContextNamespaceHandler            |      |      |
|   LoadTimeWeaverBeanDefinitionParser        |      |  load-time-weaver xml文件子节点   |
|   MBeanExportBeanDefinitionParser           |      |  mbean-export   |
|  MBeanServerBeanDefinitionParser     |      | mbean-server |
|  PropertyOverrideBeanDefinitionParser       |      | property-override  |
|  PropertyPlaceholderBeanDefinitionParser    |      | property-placeholder   |
|  SpringConfiguredBeanDefinitionParser        |      |  spring-configured  |

spring-context.xsd

ContextNamespaceHandler继承NamespaceHandlerSupport来处理xml

#### org.springframework.context.event

| org.springframework.context.event   | 类型 |      |
| ----------------------------------- | ---- | ---- |
|                                     |      |      |
| Interfaces                          |      |      |
|                                     |      |      |
| ApplicationEventMulticaster         |      |      |
| EventListenerFactory                |      |      |
| GenericApplicationListener          |      |      |
| SmartApplicationListener            |      |      |
|                                     |      |      |
| Classes                             |      |      |
|                                     |      |      |
| AbstractApplicationEventMulticaster |      |      |
| ApplicationContextEvent             |      |      |
| ApplicationListenerMethodAdapter    |      |      |
| ContextClosedEvent                  |      |      |
| ContextRefreshedEvent               |      |      |
| ContextStartedEvent                 |      |      |
| ContextStoppedEvent                 |      |      |
| DefaultEventListenerFactory         |      |      |
| EventListenerMethodProcessor        |      |      |
| EventPublicationInterceptor         |      |      |
| GenericApplicationListenerAdapter   |      |      |
| SimpleApplicationEventMulticaster   |      |      |
| SourceFilteringListener             |      |      |
|                                     |      |      |
| Annotation Types                    |      |      |
|                                     |      |      |
| EventListener                       |      |      |

XXXEvent
ApplicationContextEvent
ContextClosedEvent
ContextRefreshedEvent
ContextStartedEvent
ContextStoppedEvent

SmartApplicationListener接口
子类
GenericApplicationListenerAdapter (org.springframework.context.event)
RefreshEventListener (org.springframework.cloud.endpoint.event)
CloseContextOnFailureApplicationListener in BootstrapApplicationListener (org.springframework.cloud.bootstrap)
AwaitingNonWebApplicationListener (org.apache.dubbo.spring.boot.context.event)
RestartListener (org.springframework.cloud.context.restart)
ConfigFileApplicationListener (org.springframework.boot.context.config)
    Anonymous in ConfigFileApplicationContextInitializer (org.springframework.boot.test.context)
SourceFilteringListener (org.springframework.context.event)


SmartApplicationListener接口是Spring框架中的一个事件监听器接口，用于监听应用程序中的事件并执行相应的逻辑。与普通的ApplicationListener接口相比，SmartApplicationListener接口提供了更多的灵活性和扩展性。

下面是列出的子类以及它们的作用和区别：

1. GenericApplicationListenerAdapter (org.springframework.context.event)：
GenericApplicationListenerAdapter是一个适配器类，用于将普通的ApplicationListener适配成SmartApplicationListener。它实现了SmartApplicationListener接口，并将普通的ApplicationListener委托给其处理。

2. RefreshEventListener (org.springframework.cloud.endpoint.event)：
RefreshEventListener是用于监听Spring Cloud中的刷新事件的监听器。它负责处理应用程序中的RefreshEvent事件，通常与Spring Cloud Config等组件一起使用，用于动态刷新配置。

3. CloseContextOnFailureApplicationListener in BootstrapApplicationListener (org.springframework.cloud.bootstrap)：
CloseContextOnFailureApplicationListener是BootstrapApplicationListener中的一个内部类，用于在引导过程中处理应用程序启动失败的情况，关闭应用程序上下文。

4. AwaitingNonWebApplicationListener (org.apache.dubbo.spring.boot.context.event)：
AwaitingNonWebApplicationListener是Dubbo框架中的一个监听器，用于等待非Web应用程序上下文的加载完成。它主要用于Dubbo在Spring Boot环境下的初始化过程。

5. RestartListener (org.springframework.cloud.context.restart)：
RestartListener是用于监听Spring Cloud应用程序的重启事件的监听器。它负责处理应用程序的重启逻辑，通常与Spring Cloud的热加载和热部署功能一起使用。

6. ConfigFileApplicationListener (org.springframework.boot.context.config)：
ConfigFileApplicationListener是Spring Boot中的一个监听器，用于加载和解析应用程序的配置文件。它负责处理应用程序配置文件的加载和刷新，支持多种配置文件格式和位置。

7. Anonymous in ConfigFileApplicationContextInitializer (org.springframework.boot.test.context)：
Anonymous是ConfigFileApplicationContextInitializer中的一个匿名内部类，用于为测试环境中的应用程序上下文初始化提供配置文件的加载和解析功能。

8. SourceFilteringListener (org.springframework.context.event)：
SourceFilteringListener是一个用于过滤事件源的监听器。它可以根据特定的事件源类型来过滤掉不感兴趣的事件，只处理目标类型的事件。

这些类的作用和区别主要体现在监听的事件类型、处理的逻辑和使用的上下文环境等方面。它们各自针对不同的场景和需求，提供了特定的事件监听和处理功能，用于增强和扩展应用程序的事件驱动能力。


EventListenerFactory接口
子类
DefaultEventListenerFactory


ApplicationEventMulticaster接口

子类
AbstractApplicationEventMulticaster (org.springframework.context.event)
    SimpleApplicationEventMulticaster (org.springframework.context.event)

EventListenerMethodProcessor类 实现了 BeanFactoryPostProcessor接口
属性
	private List<EventListenerFactory> eventListenerFactories;

在Spring 5.2.9版本中，EventListenerMethodProcessor是Spring框架中的一个事件监听器方法处理器。它用于处理使用@EventListener注解标记的方法，实现事件的发布与监听。

EventListenerMethodProcessor的主要作用是将带有@EventListener注解的方法注册为事件监听器，并在相应的事件发生时触发这些方法的执行。

具体功能和作用如下：

1. 事件监听器的注册：
EventListenerMethodProcessor会扫描Spring容器中的bean，检查bean中的方法是否带有@EventListener注解。如果发现带有@EventListener注解的方法，它会将这些方法注册为事件监听器。

2. 事件发布与监听：
一旦被注册为事件监听器，带有@EventListener注解的方法就能够监听到相应的事件。当事件被发布时，EventListenerMethodProcessor会根据事件类型找到对应的监听器方法，并触发其执行。

3. 事件参数注入：
带有@EventListener注解的方法可以定义参数，用于接收事件对象或其他相关参数。EventListenerMethodProcessor会根据方法参数的类型，将相应的事件对象或参数传递给监听器方法。

4. 异步事件监听：
EventListenerMethodProcessor还支持异步事件监听。当方法被标记为@EventListener并且使用@Async注解时，事件监听器方法将在异步线程中执行。

通过使用EventListenerMethodProcessor，开发者可以方便地在Spring应用中使用事件驱动的编程模型。它提供了一种简洁的方式来定义和处理事件，让应用程序的不同组件之间能够通过事件进行解耦和交互，从而实现更灵活、可扩展的应用架构。



org.springframework.context.event.EventListenerMethodProcessor#postProcessBeanFactory()方法断点


	@Override
	public void postProcessBeanFactory(ConfigurableListableBeanFactory beanFactory) {
		this.beanFactory = beanFactory;
	
		Map<String, EventListenerFactory> beans = beanFactory.getBeansOfType(EventListenerFactory.class, false, false);
		List<EventListenerFactory> factories = new ArrayList<>(beans.values());
		AnnotationAwareOrderComparator.sort(factories);
		this.eventListenerFactories = factories;
	}

是查找 EventListenerFactory 的ioc容器对象，不是EventListener对象

postProcessBeanFactory:93, EventListenerMethodProcessor (org.springframework.context.event)
invokeBeanFactoryPostProcessors:291, PostProcessorRegistrationDelegate (org.springframework.context.support)
invokeBeanFactoryPostProcessors:182, PostProcessorRegistrationDelegate (org.springframework.context.support)
invokeBeanFactoryPostProcessors:707, AbstractApplicationContext (org.springframework.context.support)
refresh:533, AbstractApplicationContext (org.springframework.context.support)
refresh:758, SpringApplication (org.springframework.boot)
refresh:750, SpringApplication (org.springframework.boot)
refreshContext:397, SpringApplication (org.springframework.boot)
run:315, SpringApplication (org.springframework.boot)
run:140, SpringApplicationBuilder (org.springframework.boot.builder)
bootstrapServiceContext:212, BootstrapApplicationListener (org.springframework.cloud.bootstrap)
onApplicationEvent:117, BootstrapApplicationListener (org.springframework.cloud.bootstrap)
onApplicationEvent:74, BootstrapApplicationListener (org.springframework.cloud.bootstrap)
doInvokeListener:172, SimpleApplicationEventMulticaster (org.springframework.context.event)
invokeListener:165, SimpleApplicationEventMulticaster (org.springframework.context.event)
multicastEvent:139, SimpleApplicationEventMulticaster (org.springframework.context.event)
multicastEvent:127, SimpleApplicationEventMulticaster (org.springframework.context.event)
environmentPrepared:80, EventPublishingRunListener (org.springframework.boot.context.event)
environmentPrepared:53, SpringApplicationRunListeners (org.springframework.boot)
prepareEnvironment:345, SpringApplication (org.springframework.boot)
run:308, SpringApplication (org.springframework.boot)
run:1237, SpringApplication (org.springframework.boot)
run:1226, SpringApplication (org.springframework.boot)





EventListenerMethodProcessor



```shell
15:08:10.741 TRACE org.springframework.context.event.EventListenerMethodProcessor 166 processBean - No @EventListener annotations found on bean class: org.apache.logging.log4j.core.config.Configurator
15:08:10.741 TRACE org.springframework.context.event.EventListenerMethodProcessor 166 processBean - No @EventListener annotations found on bean class: cn.edidada.test.testspring32.scan.service.Order
15:08:10.742 TRACE org.springframework.context.event.EventListenerMethodProcessor 166 processBean - No @EventListener annotations found on bean class: cn.edidada.test.testspring32.scan.service.impl.NotifyServiceByCellPhoneImpl
```



org.springframework.context.event.EventListenerMethodProcessor#processBean

查看spring bean对象方法上是否有@EventListener注解



EventListenerMethodProcessor跟@EventListener注解绑定



#### org.springframework.context.expression



| org.springframework.context.expression  | 类型 | 详解 |
| --------------------------------------- | ---- | ---- |
|                                         |      |      |
| Classes                                 |      |      |
|                                         |      |      |
| AnnotatedElementKey                     |      |      |
| BeanExpressionContextAccessor           |      |      |
| BeanFactoryAccessor                     |      |      |
| BeanFactoryResolver                     |      |      |
| CachedExpressionEvaluator               |      |      |
| CachedExpressionEvaluator.ExpressionKey |      |      |
| EnvironmentAccessor                     |      |      |
| MapAccessor                             |      |      |
| MethodBasedEvaluationContext            |      |      |
| StandardBeanExpressionResolver          |      |      |

BeanExpressionResolver实现类StandardBeanExpressionResolver


```shell
evaluate:141, StandardBeanExpressionResolver (org.springframework.context.expression)
evaluateBeanDefinitionString:1575, AbstractBeanFactory (org.springframework.beans.factory.support)
doEvaluate:280, BeanDefinitionValueResolver (org.springframework.beans.factory.support)
resolveReference:329, BeanDefinitionValueResolver (org.springframework.beans.factory.support)
resolveValueIfNecessary:113, BeanDefinitionValueResolver (org.springframework.beans.factory.support)
applyPropertyValues:1697, AbstractAutowireCapableBeanFactory (org.springframework.beans.factory.support)
populateBean:1442, AbstractAutowireCapableBeanFactory (org.springframework.beans.factory.support)
doCreateBean:593, AbstractAutowireCapableBeanFactory (org.springframework.beans.factory.support)
createBean:516, AbstractAutowireCapableBeanFactory (org.springframework.beans.factory.support)
lambda$doGetBean$0:324, AbstractBeanFactory (org.springframework.beans.factory.support)
getObject:-1, 474933596 (org.springframework.beans.factory.support.AbstractBeanFactory$$Lambda$144)
getSingleton:234, DefaultSingletonBeanRegistry (org.springframework.beans.factory.support)
doGetBean:322, AbstractBeanFactory (org.springframework.beans.factory.support)
getBean:207, AbstractBeanFactory (org.springframework.beans.factory.support)
invokeBeanFactoryPostProcessors:90, PostProcessorRegistrationDelegate (org.springframework.context.support)
invokeBeanFactoryPostProcessors:707, AbstractApplicationContext (org.springframework.context.support)
refresh:533, AbstractApplicationContext (org.springframework.context.support)
refresh:758, SpringApplication (org.springframework.boot)
refresh:750, SpringApplication (org.springframework.boot)
refreshContext:397, SpringApplication (org.springframework.boot)
run:315, SpringApplication (org.springframework.boot)
run:140, SpringApplicationBuilder (org.springframework.boot.builder)
bootstrapServiceContext:212, BootstrapApplicationListener (org.springframework.cloud.bootstrap)
onApplicationEvent:117, BootstrapApplicationListener (org.springframework.cloud.bootstrap)
onApplicationEvent:74, BootstrapApplicationListener (org.springframework.cloud.bootstrap)
doInvokeListener:172, SimpleApplicationEventMulticaster (org.springframework.context.event)
invokeListener:165, SimpleApplicationEventMulticaster (org.springframework.context.event)
multicastEvent:139, SimpleApplicationEventMulticaster (org.springframework.context.event)
multicastEvent:127, SimpleApplicationEventMulticaster (org.springframework.context.event)
environmentPrepared:80, EventPublishingRunListener (org.springframework.boot.context.event)
environmentPrepared:53, SpringApplicationRunListeners (org.springframework.boot)
prepareEnvironment:345, SpringApplication (org.springframework.boot)
run:308, SpringApplication (org.springframework.boot)
run:1237, SpringApplication (org.springframework.boot)
run:1226, SpringApplication (org.springframework.boot)
```
#### org.springframework.context.i18n



| org.springframework.context.i18n | 类型 | 详解 |
| -------------------------------- | ---- | ---- |
|                                  |      |      |
| Interfaces                       |      |      |
|                                  |      |      |
| LocaleContext                    |      |      |
| TimeZoneAwareLocaleContext       |      |      |
|                                  |      |      |
| Classes                          |      |      |
|                                  |      |      |
| LocaleContextHolder              |      |      |
| SimpleLocaleContext              |      |      |
| SimpleTimeZoneAwareLocaleContext |      |      |



#### org.springframework.context.index



| org.springframework.context.index | 类型 | 详解 |
| --------------------------------- | ---- | ---- |
|                                   |      |      |
| Classes                           |      |      |
|                                   |      |      |
| CandidateComponentsIndex          |      |      |
| CandidateComponentsIndexLoader    |      |      |

##### org.springframework.context.index.processor



| org.springframework.context.index.processor | 类型 | 详解 |
| ------------------------------------------- | ---- | ---- |
|                                             |      |      |
| Classes                                     |      |      |
|                                             |      |      |
| CandidateComponentsIndexer                  |      |      |



#### org.springframework.context.support  


| org.springframework.context.support         | 类型      | 详解 |
| ------------------------------------------- | --------- | ---- |
| Interfaces                                  |           |      |
|                                             |           |      |
| LiveBeansViewMBean                          | interface |      |
|                                             |           |      |
| Classes                                     |           |      |
|                                             |           |      |
| AbstractApplicationContext                  |           |      |
| AbstractMessageSource                       |           |      |
| AbstractRefreshableApplicationContext       |           |      |
| AbstractRefreshableConfigApplicationContext |           |      |
| AbstractResourceBasedMessageSource          |           |      |
| AbstractXmlApplicationContext               |           |      |
| ApplicationObjectSupport                    |           |      |
| ClassPathXmlApplicationContext              |           |      |
| ConversionServiceFactoryBean                |           |      |
| DefaultLifecycleProcessor                   |           |      |
| DefaultMessageSourceResolvable              |           |      |
| DelegatingMessageSource                     |           |      |
| EmbeddedValueResolutionSupport              |           |      |
| FileSystemXmlApplicationContext             |           |      |
| GenericApplicationContext                   |           |      |
| GenericGroovyApplicationContext             |           |      |
| GenericXmlApplicationContext                |           |      |
| LiveBeansView                               |           |      |
| MessageSourceAccessor                       |           |      |
| MessageSourceResourceBundle                 |           |      |
| MessageSourceSupport                        |           |      |
| PropertySourcesPlaceholderConfigurer        |           |      |
| ReloadableResourceBundleMessageSource       |           |      |
| ResourceBundleMessageSource                 |           |      |
| SimpleThreadScope                           |           |      |
| StaticApplicationContext                    |           |      |
| StaticMessageSource                         |           |      |





AbstractApplicationContext
    GenericApplicationContext
        AnnotationConfigApplicationContext


PropertySourcesPlaceholderConfigurer使用例子
```
    @Bean
    public PropertySourcesPlaceholderConfigurer propertySourcesPlaceholderConfigurer() {
        PropertySourcesPlaceholderConfigurer configurer = new PropertySourcesPlaceholderConfigurer();
        Resource[] resources = new ClassPathResource[]{new ClassPathResource("application.properties")};
        configurer.setLocations(resources);
        return configurer;
    }
```

#### org.springframework.context.weaving



| Interfaces                   | 类型 | 详解 |
| ---------------------------- | ---- | ---- |
|                              |      |      |
| LoadTimeWeaverAware          |      |      |
|                              |      |      |
| Classes                      |      |      |
|                              |      |      |
| AspectJWeavingEnabler        |      |      |
| DefaultContextLoadTimeWeaver |      |      |
| LoadTimeWeaverAwareProcessor |      |      |



### org.springframework.ejb



#### org.springframework.ejb.access

| org.springframework.ejb.access               | 类型 | 详解 |
| -------------------------------------------- | ---- | ---- |
|                                              |      |      |
| Classes                                      |      |      |
|                                              |      |      |
| AbstractRemoteSlsbInvokerInterceptor         |      |      |
| AbstractSlsbInvokerInterceptor               |      |      |
| LocalSlsbInvokerInterceptor                  |      |      |
| LocalStatelessSessionProxyFactoryBean        |      |      |
| SimpleRemoteSlsbInvokerInterceptor           |      |      |
| SimpleRemoteStatelessSessionProxyFactoryBean |      |      |
|                                              |      |      |
| Exceptions                                   |      |      |
|                                              |      |      |
| EjbAccessException                           |      |      |

#### org.springframework.ejb.config



### org.springframework.format

| org.springframework.format | 类型 | 详解 |
| -------------------------- | ---- | ---- |
|                            |      |      |
| Interfaces                 |      |      |
|                            |      |      |
| AnnotationFormatterFactory |      |      |
| Formatter                  |      |      |
| FormatterRegistrar         |      |      |
| FormatterRegistry          |      |      |
| Parser                     |      |      |
| Printer                    |      |      |

#### org.springframework.format.annotation

| org.springframework.format.annotation | 类型       | 详解 |
| ------------------------------------- | ---------- | ---- |
| DateTimeFormat                        | @interface |      |
| DateTimeFormat.ISO                    | enum       |      |
| NumberFormat                          | @interface |      |
| NumberFormat.Style                    | enum       |      |
|                                       |            |      |

#### org.springframework.format.datetime



| org.springframework.format.datetime            | 类型 | 详解 |
| ---------------------------------------------- | ---- | ---- |
| DateFormatter                                  |      |      |
| DateFormatterRegistrar                         |      |      |
| DateFormatterRegistrar.CalendarToDateConverter |      |      |
| DateFormatterRegistrar.CalendarToLongConverter |      |      |
| DateFormatterRegistrar.DateToCalendarConverter |      |      |
| DateFormatterRegistrar.DateToLongConverter     |      |      |
| DateFormatterRegistrar.LongToCalendarConverter |      |      |
| DateFormatterRegistrar.LongToDateConverter     |      |      |
| DateTimeFormatAnnotationFormatterFactory       |      |      |
|                                                |      |      |



##### org.springframework.format.datetime.joda

| org.springframework.format.datetime.joda     | 类型 | 详解 |
| -------------------------------------------- | ---- | ---- |
|                                              |      |      |
| Classes                                      |      |      |
|                                              |      |      |
| DateTimeFormatterFactory                     |      |      |
| DateTimeFormatterFactoryBean                 |      |      |
| DateTimeParser                               |      |      |
| JodaDateTimeFormatAnnotationFormatterFactory |      |      |
| JodaTimeContext                              |      |      |
| JodaTimeContextHolder                        |      |      |
| JodaTimeFormatterRegistrar                   |      |      |
| LocalDateParser                              |      |      |
| LocalDateTimeParser                          |      |      |
| LocalTimeParser                              |      |      |
| MillisecondInstantPrinter                    |      |      |
| ReadableInstantPrinter                       |      |      |
| ReadablePartialPrinter                       |      |      |

##### org.springframework.format.datetime.standard

| org.springframework.format.datetime.standard   | 类型 | 详解 |
| ---------------------------------------------- | ---- | ---- |
|                                                |      |      |
| Classes                                        |      |      |
|                                                |      |      |
| DateTimeContext                                |      |      |
| DateTimeContextHolder                          |      |      |
| DateTimeFormatterFactory                       |      |      |
| DateTimeFormatterFactoryBean                   |      |      |
| DateTimeFormatterRegistrar                     |      |      |
| InstantFormatter                               |      |      |
| Jsr310DateTimeFormatAnnotationFormatterFactory |      |      |
| TemporalAccessorParser                         |      |      |
| TemporalAccessorPrinter                        |      |      |

#### org.springframework.format.number

| org.springframework.format.number      | 类型 | 详解 |
| -------------------------------------- | ---- | ---- |
|                                        |      |      |
| Classes                                |      |      |
|                                        |      |      |
| AbstractNumberFormatter                |      |      |
| CurrencyStyleFormatter                 |      |      |
| NumberFormatAnnotationFormatterFactory |      |      |
| NumberStyleFormatter                   |      |      |
| PercentStyleFormatter                  |      |      |

##### org.springframework.format.number.money

| org.springframework.format.number.money      | 类型 |      |
| -------------------------------------------- | ---- | ---- |
|                                              |      |      |
| Classes                                      |      |      |
|                                              |      |      |
| CurrencyUnitFormatter                        |      |      |
| Jsr354NumberFormatAnnotationFormatterFactory |      |      |
| MonetaryAmountFormatter                      |      |      |



#### org.springframework.format.support



| org.springframework.format.support                     | 类型 | 详解 |
| ------------------------------------------------------ | ---- | ---- |
| DefaultFormattingConversionService                     |      |      |
| FormatterPropertyEditorAdapter                         |      |      |
| FormattingConversionService                            |      |      |
| FormattingConversionService.AnnotationConverterKey     |      |      |
| FormattingConversionService.AnnotationParserConverter  |      |      |
| FormattingConversionService.AnnotationPrinterConverter |      |      |
| FormattingConversionService.ParserConverter            |      |      |
| FormattingConversionService.PrinterConverter           |      |      |
| FormattingConversionServiceFactoryBean                 |      |      |
|                                                        |      |      |





#### org.springframework.instrument.classloading



| org.springframework.instrument.classloading | 类型 | 详解 |
| ------------------------------------------- | ---- | ---- |
|                                             |      |      |
| Interfaces                                  |      |      |
|                                             |      |      |
| LoadTimeWeaver                              |      |      |
|                                             |      |      |
| Classes                                     |      |      |
|                                             |      |      |
| InstrumentationLoadTimeWeaver               |      |      |
| ReflectiveLoadTimeWeaver                    |      |      |
| ResourceOverridingShadowingClassLoader      |      |      |
| ShadowingClassLoader                        |      |      |
| SimpleInstrumentableClassLoader             |      |      |
| SimpleLoadTimeWeaver                        |      |      |
| SimpleThrowawayClassLoader                  |      |      |
| WeavingTransformer                          |      |      |





###### org.springframework.instrument.classloading.glassfish

| org.springframework.instrument.classloading.glassfish | 类型 | 详解 |
| ----------------------------------------------------- | ---- | ---- |
| GlassFishLoadTimeWeaver                               |      |      |
|                                                       |      |      |
|                                                       |      |      |



##### org.springframework.instrument.classloading.jboss

JBossLoadTimeWeaver



##### org.springframework.instrument.classloading.tomcat



TomcatLoadTimeWeaver



##### org.springframework.instrument.classloading.weblogic



WebLogicClassLoaderAdapter WebLogicClassPreProcessorAdapter WebLogicLoadTimeWeaver



##### org.springframework.instrument.classloading.websphere

WebSphereClassLoaderAdapter WebSphereClassPreDefinePlugin WebSphereClassPreDefinePlugin.Dummy WebSphereLoadTimeWeaver





### org.springframework.jmx



| org.springframework.jmx      | 类型      | 详解 |
| ---------------------------- | --------- | ---- |
| JmxException                 |           |      |
| MBeanServerNotFoundException | exception |      |
|                              |           |      |



#### org.springframework.jmx.access

| org.springframework.jmx.access | 类型 | 详解 |
| ------------------------------ | ---- | ---- |
|                                |      |      |
| Classes                        |      |      |
|                                |      |      |
| MBeanClientInterceptor         |      |      |
| MBeanProxyFactoryBean          |      |      |
| NotificationListenerRegistrar  |      |      |
|                                |      |      |
| Exceptions                     |      |      |
|                                |      |      |
| InvalidInvocationException     |      |      |
| InvocationFailureException     |      |      |
| MBeanConnectFailureException   |      |      |
| MBeanInfoRetrievalException    |      |      |

#### org.springframework.jmx.export

| org.springframework.jmx.export | 类型 | 详解 |
| ------------------------------ | ---- | ---- |
|                                |      |      |
| Interfaces                     |      |      |
|                                |      |      |
| MBeanExporterListener          |      |      |
| MBeanExportOperations          |      |      |
|                                |      |      |
| Classes                        |      |      |
|                                |      |      |
| MBeanExporter                  |      |      |
| NotificationListenerBean       |      |      |
| SpringModelMBean               |      |      |
|                                |      |      |
| Exceptions                     |      |      |
|                                |      |      |
| MBeanExportException           |      |      |
| UnableToRegisterMBeanException |      |      |

##### org.springframework.jmx.export.annotation

| org.springframework.jmx.export.annotation | 类型 | 详解 |
| ----------------------------------------- | ---- | ---- |
|                                           |      |      |
| Classes                                   |      |      |
|                                           |      |      |
| AnnotationJmxAttributeSource              |      |      |
| AnnotationMBeanExporter                   |      |      |
|                                           |      |      |
| Annotation Types                          |      |      |
|                                           |      |      |
| ManagedAttribute                          |      |      |
| ManagedMetric                             |      |      |
| ManagedNotification                       |      |      |
| ManagedNotifications                      |      |      |
| ManagedOperation                          |      |      |
| ManagedOperationParameter                 |      |      |
| ManagedOperationParameters                |      |      |
| ManagedResource                           |      |      |

##### org.springframework.jmx.export.assembler

| org.springframework.jmx.export.assembler | 类型 | 详解 |
| ---------------------------------------- | ---- | ---- |
|                                          |      |      |
| Interfaces                               |      |      |
|                                          |      |      |
| AutodetectCapableMBeanInfoAssembler      |      |      |
| MBeanInfoAssembler                       |      |      |
|                                          |      |      |
| Classes                                  |      |      |
|                                          |      |      |
| AbstractConfigurableMBeanInfoAssembler   |      |      |
| AbstractMBeanInfoAssembler               |      |      |
| AbstractReflectiveMBeanInfoAssembler     |      |      |
| InterfaceBasedMBeanInfoAssembler         |      |      |
| MetadataMBeanInfoAssembler               |      |      |
| MethodExclusionMBeanInfoAssembler        |      |      |
| MethodNameBasedMBeanInfoAssembler        |      |      |
| SimpleReflectiveMBeanInfoAssembler       |      |      |

##### org.springframework.jmx.export.metadata

| org.springframework.jmx.export.metadata | 类型 | 详解 |
| --------------------------------------- | ---- | ---- |
|                                         |      |      |
| Interfaces                              |      |      |
|                                         |      |      |
| JmxAttributeSource                      |      |      |
|                                         |      |      |
| Classes                                 |      |      |
|                                         |      |      |
| AbstractJmxAttribute                    |      |      |
| JmxMetadataUtils                        |      |      |
| ManagedAttribute                        |      |      |
| ManagedMetric                           |      |      |
| ManagedNotification                     |      |      |
| ManagedOperation                        |      |      |
| ManagedOperationParameter               |      |      |
| ManagedResource                         |      |      |
|                                         |      |      |
| Exceptions                              |      |      |
|                                         |      |      |
| InvalidMetadataException                |      |      |

##### org.springframework.jmx.export.naming

| org.springframework.jmx.export.naming | 类型 | 详解 |
| ------------------------------------- | ---- | ---- |
|                                       |      |      |
| Interfaces                            |      |      |
|                                       |      |      |
| ObjectNamingStrategy                  |      |      |
| SelfNaming                            |      |      |
|                                       |      |      |
| Classes                               |      |      |
|                                       |      |      |
| IdentityNamingStrategy                |      |      |
| KeyNamingStrategy                     |      |      |
| MetadataNamingStrategy                |      |      |

##### org.springframework.jmx.export.notification

| org.springframework.jmx.export.notification | 类型 | 详解 |
| ------------------------------------------- | ---- | ---- |
|                                             |      |      |
| Interfaces                                  |      |      |
|                                             |      |      |
| NotificationPublisher                       |      |      |
| NotificationPublisherAware                  |      |      |
|                                             |      |      |
| Classes                                     |      |      |
|                                             |      |      |
| ModelMBeanNotificationPublisher             |      |      |
|                                             |      |      |
| Exceptions                                  |      |      |
|                                             |      |      |
| UnableToSendNotificationException           |      |      |





### org.springframework.jndi

| org.springframework.jndi    | 类型 | 详解 |
| --------------------------- | ---- | ---- |
|                             |      |      |
| Interfaces                  |      |      |
|                             |      |      |
| JndiCallback                |      |      |
|                             |      |      |
| Classes                     |      |      |
|                             |      |      |
| JndiAccessor                |      |      |
| JndiLocatorDelegate         |      |      |
| JndiLocatorSupport          |      |      |
| JndiObjectFactoryBean       |      |      |
| JndiObjectLocator           |      |      |
| JndiObjectTargetSource      |      |      |
| JndiPropertySource          |      |      |
| JndiTemplate                |      |      |
| JndiTemplateEditor          |      |      |
|                             |      |      |
| Exceptions                  |      |      |
|                             |      |      |
| JndiLookupFailureException  |      |      |
| TypeMismatchNamingException |      |      |

#### org.springframework.jndi.support



SimpleJndiBeanFactory



### org.springframework.remoting

| org.springframework.remoting     | 类型 | 详解 |
| -------------------------------- | ---- | ---- |
|                                  |      |      |
| Exceptions                       |      |      |
|                                  |      |      |
| RemoteAccessException            |      |      |
| RemoteConnectFailureException    |      |      |
| RemoteInvocationFailureException |      |      |
| RemoteLookupFailureException     |      |      |
| RemoteProxyFailureException      |      |      |
| RemoteTimeoutException           |      |      |



#### org.springframework.remoting.rmi



| org.springframework.remoting.rmi    | 类型 | 详解 |
| ----------------------------------- | ---- | ---- |
|                                     |      |      |
| Interfaces                          |      |      |
|                                     |      |      |
| RmiInvocationHandler                |      |      |
|                                     |      |      |
| Classes                             |      |      |
|                                     |      |      |
| CodebaseAwareObjectInputStream      |      |      |
| JndiRmiClientInterceptor            |      |      |
| JndiRmiProxyFactoryBean             |      |      |
| JndiRmiServiceExporter              |      |      |
| RemoteInvocationSerializingExporter |      |      |
| RmiBasedExporter                    |      |      |
| RmiClientInterceptor                |      |      |
| RmiClientInterceptorUtils           |      |      |
| RmiProxyFactoryBean                 |      |      |
| RmiRegistryFactoryBean              |      |      |
| RmiServiceExporter                  |      |      |



#### org.springframework.remoting.soap

| org.springframework.remoting.soap | 类型     | 详解 |
| --------------------------------- | -------- | ---- |
| SoapFaultException                | abstract |      |
|                                   |          |      |
|                                   |          |      |





#### org.springframework.remoting.support

| org.springframework.remoting.support | 类型 | 详解 |
| ------------------------------------ | ---- | ---- |
|                                      |      |      |
| Interfaces                           |      |      |
|                                      |      |      |
| RemoteInvocationExecutor             |      |      |
| RemoteInvocationFactory              |      |      |
|                                      |      |      |
| Classes                              |      |      |
|                                      |      |      |
| DefaultRemoteInvocationExecutor      |      |      |
| DefaultRemoteInvocationFactory       |      |      |
| RemoteAccessor                       |      |      |
| RemoteExporter                       |      |      |
| RemoteInvocation                     |      |      |
| RemoteInvocationBasedAccessor        |      |      |
| RemoteInvocationBasedExporter        |      |      |
| RemoteInvocationResult               |      |      |
| RemoteInvocationTraceInterceptor     |      |      |
| RemoteInvocationUtils                |      |      |
| RemotingSupport                      |      |      |
| SimpleHttpServerFactoryBean          |      |      |
| UrlBasedRemoteAccessor               |      |      |



### org.springframework.scheduling



| org.springframework.scheduling | 类型 | 详解 |
| ------------------------------ | ---- | ---- |
|                                |      |      |
| Interfaces                     |      |      |
|                                |      |      |
| SchedulingAwareRunnable        |      |      |
| SchedulingTaskExecutor         |      |      |
| TaskScheduler                  |      |      |
| Trigger                        |      |      |
| TriggerContext                 |      |      |
|                                |      |      |
| Exceptions                     |      |      |
|                                |      |      |
| SchedulingException            |      |      |



#### org.springframework.scheduling.annotation





| org.springframework.scheduling.annotation | 类型 | 详解 |
| ----------------------------------------- | ---- | ---- |
|                                           |      |      |
| Interfaces                                |      |      |
|                                           |      |      |
| AsyncConfigurer                           |      |      |
| SchedulingConfigurer                      |      |      |
|                                           |      |      |
| Classes                                   |      |      |
|                                           |      |      |
| AbstractAsyncConfiguration                |      |      |
| AnnotationAsyncExecutionInterceptor       |      |      |
| AsyncAnnotationAdvisor                    |      |      |
| AsyncAnnotationBeanPostProcessor          |      |      |
| AsyncConfigurationSelector                |      |      |
| AsyncConfigurerSupport                    |      |      |
| AsyncResult                               |      |      |
| ProxyAsyncConfiguration                   |      |      |
| ScheduledAnnotationBeanPostProcessor      |      |      |
| SchedulingConfiguration                   |      |      |
|                                           |      |      |
| Annotation Types                          |      |      |
|                                           |      |      |
| Async                                     |      |      |
| EnableAsync                               |      |      |
| EnableScheduling                          |      |      |
| Scheduled                                 |      |      |
| Schedules                                 |      |      |





#### org.springframework.scheduling.concurrent

| org.springframework.scheduling.concurrent | 类型 | 详解 |
| ----------------------------------------- | ---- | ---- |
|                                           |      |      |
| Classes                                   |      |      |
|                                           |      |      |
| ConcurrentTaskExecutor                    |      |      |
| ConcurrentTaskExecutor.ManagedTaskBuilder |      |      |
| ConcurrentTaskScheduler                   |      |      |
| CustomizableThreadFactory                 |      |      |
| DefaultManagedAwareThreadFactory          |      |      |
| DefaultManagedTaskExecutor                |      |      |
| DefaultManagedTaskScheduler               |      |      |
| ExecutorConfigurationSupport              |      |      |
| ForkJoinPoolFactoryBean                   |      |      |
| ScheduledExecutorFactoryBean              |      |      |
| ScheduledExecutorTask                     |      |      |
| ThreadPoolExecutorFactoryBean             |      |      |
| ThreadPoolTaskExecutor                    |      |      |
| ThreadPoolTaskScheduler                   |      |      |



####  org.springframework.scheduling.config



| org.springframework.scheduling.config  | 类型 | 详解 |
| -------------------------------------- | ---- | ---- |
|                                        |      |      |
| Interfaces                             |      |      |
|                                        |      |      |
| ScheduledTaskHolder                    |      |      |
|                                        |      |      |
| Classes                                |      |      |
|                                        |      |      |
| AnnotationDrivenBeanDefinitionParser   |      |      |
| ContextLifecycleScheduledTaskRegistrar |      |      |
| CronTask                               |      |      |
| ExecutorBeanDefinitionParser           |      |      |
| FixedDelayTask                         |      |      |
| FixedRateTask                          |      |      |
| IntervalTask                           |      |      |
| ScheduledTask                          |      |      |
| ScheduledTaskRegistrar                 |      |      |
| ScheduledTasksBeanDefinitionParser     |      |      |
| SchedulerBeanDefinitionParser          |      |      |
| Task                                   |      |      |
| TaskExecutorFactoryBean                |      |      |
| TaskManagementConfigUtils              |      |      |
| TaskNamespaceHandler                   |      |      |
| TriggerTask                            |      |      |



#### org.springframework.scheduling.support





| org.springframework.scheduling.support | 类型 | 详解 |
| -------------------------------------- | ---- | ---- |
|                                        |      |      |
| Classes                                |      |      |
|                                        |      |      |
| CronSequenceGenerator                  |      |      |
| CronTrigger                            |      |      |
| DelegatingErrorHandlingRunnable        |      |      |
| MethodInvokingRunnable                 |      |      |
| PeriodicTrigger                        |      |      |
| ScheduledMethodRunnable                |      |      |
| SimpleTriggerContext                   |      |      |
| TaskUtils                              |      |      |



### org.springframework.scripting





| org.springframework.scripting | 类型 | 详解 |
| ----------------------------- | ---- | ---- |
|                               |      |      |
| Interfaces                    |      |      |
|                               |      |      |
| ScriptEvaluator               |      |      |
| ScriptFactory                 |      |      |
| ScriptSource                  |      |      |
|                               |      |      |
| Exceptions                    |      |      |
|                               |      |      |
| ScriptCompilationException    |      |      |





#### org.springframework.scripting.bsh





| org.springframework.scripting.bsh    | 类型 | 详解 |
| ------------------------------------ | ---- | ---- |
|                                      |      |      |
| Classes                              |      |      |
|                                      |      |      |
| BshScriptEvaluator                   |      |      |
| BshScriptFactory                     |      |      |
| BshScriptUtils                       |      |      |
|                                      |      |      |
| Exceptions                           |      |      |
|                                      |      |      |
| BshScriptUtils.BshExecutionException |      |      |



#### org.springframework.scripting.config



| org.springframework.scripting.config | 类型 | 详解 |
| ------------------------------------ | ---- | ---- |
|                                      |      |      |
| Classes                              |      |      |
|                                      |      |      |
| LangNamespaceHandler                 |      |      |
| LangNamespaceUtils                   |      |      |



#### org.springframework.scriptingg.groovy



| org.springframework.scriptingg.groovy | 类型 | 详解 |
| ------------------------------------- | ---- | ---- |
|                                       |      |      |
| Interfaces                            |      |      |
|                                       |      |      |
| GroovyObjectCustomizer                |      |      |
|                                       |      |      |
| Classes                               |      |      |
|                                       |      |      |
| GroovyScriptEvaluator                 |      |      |
| GroovyScriptFactory                   |      |      |



#### org.springframework.scripting.support



| org.springframework.scripting.support | 类型 | 详解 |
| ------------------------------------- | ---- | ---- |
|                                       |      |      |
| Classes                               |      |      |
|                                       |      |      |
| RefreshableScriptTargetSource         |      |      |
| ResourceScriptSource                  |      |      |
| ScriptFactoryPostProcessor            |      |      |
| StandardScriptEvaluator               |      |      |
| StandardScriptFactory                 |      |      |
| StandardScriptUtils                   |      |      |
| StaticScriptSource                    |      |      |
|                                       |      |      |
| Exceptions                            |      |      |
|                                       |      |      |
| StandardScriptEvalException           |      |      |



### org.springframework.stereotype



| org.springframework.stereotype | 类型 | 详解 |
| ------------------------------ | ---- | ---- |
|                                |      |      |
| Annotation Types               |      |      |
|                                |      |      |
| Component                      |      |      |
| Controller                     |      |      |
| Indexed                        |      |      |
| Repository                     |      |      |
| Service                        |      |      |



### org.springframework.ui



| org.springframework.ui | 类型 | 详解 |
| ---------------------- | ---- | ---- |
|                        |      |      |
| Interfaces             |      |      |
|                        |      |      |
| Model                  |      |      |
|                        |      |      |
| Classes                |      |      |
|                        |      |      |
| ConcurrentModel        |      |      |
| ExtendedModelMap       |      |      |
| ModelMap               |      |      |



#### org.springframework.ui.context



| org.springframework.ui.context | 类型 | 详解 |
| ------------------------------ | ---- | ---- |
|                                |      |      |
| Interfaces                     |      |      |
|                                |      |      |
| HierarchicalThemeSource        |      |      |
| Theme                          |      |      |
| ThemeSource                    |      |      |



##### org.springframework.ui.context.support

| org.springframework.ui.context.support | 类型 | 详解 |
| -------------------------------------- | ---- | ---- |
|                                        |      |      |
| Classes                                |      |      |
|                                        |      |      |
| DelegatingThemeSource                  |      |      |
| ResourceBundleThemeSource              |      |      |
| SimpleTheme                            |      |      |
| UiApplicationContextUtils              |      |      |





### org.springframework.validation



| org.springframework.validation     | 类型 | 详解 |
| ---------------------------------- | ---- | ---- |
|                                    |      |      |
| Interfaces                         |      |      |
|                                    |      |      |
| BindingErrorProcessor              |      |      |
| BindingResult                      |      |      |
| Errors                             |      |      |
| MessageCodeFormatter               |      |      |
| MessageCodesResolver               |      |      |
| SmartValidator                     |      |      |
| Validator                          |      |      |
|                                    |      |      |
| Classes                            |      |      |
|                                    |      |      |
| AbstractBindingResult              |      |      |
| AbstractErrors                     |      |      |
| AbstractPropertyBindingResult      |      |      |
| BeanPropertyBindingResult          |      |      |
| BindingResultUtils                 |      |      |
| DataBinder                         |      |      |
| DefaultBindingErrorProcessor       |      |      |
| DefaultMessageCodesResolver        |      |      |
| DirectFieldBindingResult           |      |      |
| FieldError                         |      |      |
| MapBindingResult                   |      |      |
| ObjectError                        |      |      |
| ValidationUtils                    |      |      |
|                                    |      |      |
| Enums                              |      |      |
|                                    |      |      |
| DefaultMessageCodesResolver.Format |      |      |
|                                    |      |      |
| Exceptions                         |      |      |
|                                    |      |      |
| BindException                      |      |      |



#### org.springframework.validation.annotation





| org.springframework.validation.annotation | 类型       | 详解 |
| ----------------------------------------- | ---------- | ---- |
| Validated                                 | @interface |      |
|                                           |            |      |
|                                           |            |      |





#### org.springframework.validation.beanvalidation



| org.springframework.validation.beanvalidation | 类型 | 详解 |
| --------------------------------------------- | ---- | ---- |
|                                               |      |      |
| Classes                                       |      |      |
|                                               |      |      |
| BeanValidationPostProcessor                   |      |      |
| CustomValidatorBean                           |      |      |
| LocaleContextMessageInterpolator              |      |      |
| LocalValidatorFactoryBean                     |      |      |
| MessageSourceResourceBundleLocator            |      |      |
| MethodValidationInterceptor                   |      |      |
| MethodValidationPostProcessor                 |      |      |
| OptionalValidatorFactoryBean                  |      |      |
| SpringConstraintValidatorFactory              |      |      |
| SpringValidatorAdapter                        |      |      |



#### org.springframework.validation.support



| org.springframework.validation.support | 类型 | 详解 |
| -------------------------------------- | ---- | ---- |
| BindingAwareConcurrentModel            |      |      |
| BindingAwareModelMap                   |      |      |
|                                        |      |      |

