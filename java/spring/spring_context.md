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



| org.springframework.cache     | 类型      |      |
| ----------------------------- | --------- | ---- |
| Cache                         | interface |      |
| Cache.ValueRetrievalException | exception |      |
| Cache.ValueWrapper            | interface |      |
| CacheManager                  |           |      |
|                               |           |      |

#### org.springframework.cache.annotation



| org.springframework.cache.annotation                  | 类型 |      |
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

| org.springframework.cache.concurrent |      |      |
| ------------------------------------ | ---- | ---- |
| ConcurrentMapCache                   |      |      |
| ConcurrentMapCacheFactoryBean        |      |      |
| ConcurrentMapCacheManager            |      |      |



#### org.springframework.cache.config

| org.springframework.cache.config                             | 类型     |                             |
| ------------------------------------------------------------ | -------- | --------------------------- |
| AnnotationDrivenCacheBeanDefinitionParser                    |          |                             |
| AnnotationDrivenCacheBeanDefinitionParser.JCacheCachingConfigurer |          |                             |
| AnnotationDrivenCacheBeanDefinitionParser.SpringCachingConfigurer |          |                             |
| CacheAdviceParser                                            |          |                             |
| CacheAdviceParser.Props                                      |          |                             |
| CacheManagementConfigUtils                                   | abstract |                             |
| CacheNamespaceHandler                                        |          | NamespaceHandlerSupport子类 |



#### org.springframework.cache.interceptor

| org.springframework.cache.interceptor     | 类型 |      |
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

| org.springframework.cache.support | 类型 |      |
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





| org.springframework.context    | 类型 |      |
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




| org.springframework.context.annotation          | 详解                                                         |                                                              |      |
| ----------------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ---- |
| AdviceMode                                      | Enumeration used to determine whether JDK proxy-based or AspectJ weaving-based advice should be applied. |                                                              |      |
|                                                 |                                                              |                                                              |      |
| AdviceModeImportSelector<A extends Annotation>  | Convenient base class for ImportSelector implementations that select imports based on an AdviceMode value from an annotation (such as the @Enable* annotations). |                                                              |      |
|                                                 |                                                              |                                                              |      |
| AnnotatedBeanDefinitionReader                   | Convenient adapter for programmatic registration of bean classes. |                                                              |      |
|                                                 |                                                              |                                                              |      |
| AnnotationBeanNameGenerator                     |                                                              |                                                              |      |
|                                                 | BeanNameGenerator implementation for bean classes annotated with the @Component annotation or with another annotation that is itself annotated with @Component as a meta-annotation. |                                                              |      |
| AnnotationConfigApplicationContext              |                                                              |                                                              |      |
|                                                 | Standalone application context, accepting component classes as input — in particular @Configuration-annotated classes, but also plain @Component types and JSR-330 compliant classes using jakarta.inject annotations. |                                                              |      |
| AnnotationConfigBeanDefinitionParser            |                                                              |                                                              |      |
|                                                 | Parser for the <context:annotation-config/> element.         |                                                              |      |
| AnnotationConfigRegistry                        |                                                              |                                                              |      |
|                                                 | Common interface for annotation config application contexts, defining AnnotationConfigRegistry.register(java.lang.Class<?>...) and AnnotationConfigRegistry.scan(java.lang.String...) methods. |                                                              |      |
| AnnotationConfigUtils                           |                                                              |                                                              |      |
|                                                 | Utility class that allows for convenient registration of common BeanPostProcessor and BeanFactoryPostProcessor definitions for annotation-based configuration. |                                                              |      |
| AnnotationScopeMetadataResolver                 |                                                              |                                                              |      |
|                                                 | A ScopeMetadataResolver implementation that by default checks for the presence of Spring's @Scope annotation on the bean class. |                                                              |      |
| AutoProxyRegistrar                              |                                                              |                                                              |      |
|                                                 | Registers an auto proxy creator against the current BeanDefinitionRegistry as appropriate based on an @Enable* annotation having mode and proxyTargetClass attributes set to the correct values. |                                                              |      |
| Bean                                            |                                                              |                                                              |      |
|                                                 | Indicates that a method produces a bean to be managed by the Spring container. |                                                              |      |
| **ClassPathBeanDefinitionScanner**              |                                                              | ClassPathScanningCandidateComponentProvider子类 scan() doScan() addIncludeFilter() 很多三方框架都自定义这个类的子类 |      |
|                                                 | A bean definition scanner that detects bean candidates on the classpath, registering corresponding bean definitions with a given registry (BeanFactory or ApplicationContext). |                                                              |      |
| ClassPathScanningCandidateComponentProvider     |                                                              |                                                              |      |
|                                                 | A component provider that provides candidate components from a base package. |                                                              |      |
| CommonAnnotationBeanPostProcessor               |                                                              |                                                              |      |
|                                                 | BeanPostProcessor implementation that supports common Java annotations out of the box, in particular the common annotations in the jakarta.annotation package. |                                                              |      |
| CommonAnnotationBeanPostProcessor.LookupElement |                                                              |                                                              |      |
|                                                 | Class representing generic injection information about an annotated field or setter method, supporting @Resource and related annotations. |                                                              |      |
| ComponentScan                                   |                                                              |                                                              |      |
|                                                 | Configures component scanning directives for use with @Configuration classes. |                                                              |      |
| ComponentScanAnnotationParser                   |                                                              | @ComponentScan会被解析为一个Bean定义扫描器                   |      |
|                                                 |                                                              |                                                              |      |
| ComponentScan.Filter                            |                                                              |                                                              |      |
|                                                 | Declares the type filter to be used as an include filter or exclude filter. |                                                              |      |
| ComponentScanBeanDefinitionParser               |                                                              |                                                              |      |
|                                                 | Parser for the <context:component-scan/> element.            |                                                              |      |
| ComponentScans                                  |                                                              |                                                              |      |
|                                                 | Container annotation that aggregates several ComponentScan annotations. |                                                              |      |
| Condition                                       |                                                              |                                                              |      |
|                                                 | A single condition that must be matched in order for a component to be registered. |                                                              |      |
| Conditional                                     |                                                              |                                                              |      |
|                                                 | Indicates that a component is only eligible for registration when all specified conditions match. |                                                              |      |
| ConditionContext                                |                                                              |                                                              |      |
|                                                 | Context information for use by Condition implementations.    |                                                              |      |
| Configuration                                   |                                                              |                                                              |      |
|                                                 | Indicates that a class declares one or more @Bean methods and may be processed by the Spring container to generate bean definitions and service requests for those beans at runtime, for example: |                                                              |      |
| ConfigurationClassPostProcessor                 | BeanFactoryPostProcessor used for bootstrapping processing of @Configuration classes. | processConfigBeanDefinitions()核心方法                       |      |
| ConfigurationClassUtils                         |                                                              |                                                              |      |
|                                                 | Utilities for identifying and configuring Configuration classes. |                                                              |      |
| ConfigurationCondition                          |                                                              |                                                              |      |
|                                                 | A Condition that offers more fine-grained control when used with @Configuration. |                                                              |      |
| ConfigurationCondition.ConfigurationPhase       |                                                              |                                                              |      |
|                                                 | The various configuration phases where the condition could be evaluated. |                                                              |      |
| ContextAnnotationAutowireCandidateResolver      |                                                              |                                                              |      |
|                                                 | Complete implementation of the AutowireCandidateResolver strategy interface, providing support for qualifier annotations as well as for lazy resolution driven by the Lazy annotation in the context.annotation package. |                                                              |      |
| DeferredImportSelector                          |                                                              |                                                              |      |
|                                                 | A variation of ImportSelector that runs after all @Configuration beans have been processed. |                                                              |      |
| DeferredImportSelector.Group                    |                                                              |                                                              |      |
|                                                 | Interface used to group results from different import selectors. |                                                              |      |
| DeferredImportSelector.Group.Entry              |                                                              |                                                              |      |
|                                                 | An entry that holds the AnnotationMetadata of the importing Configuration class and the class name to import. |                                                              |      |
| DependsOn                                       |                                                              |                                                              |      |
|                                                 | Beans on which the current bean depends.                     |                                                              |      |
| Description                                     |                                                              |                                                              |      |
|                                                 | Adds a textual description to bean definitions derived from Component or Bean. |                                                              |      |
| EnableAspectJAutoProxy                          |                                                              |                                                              |      |
|                                                 | Enables support for handling components marked with AspectJ's @Aspect annotation, similar to functionality found in Spring's <aop:aspectj-autoproxy> XML element. |                                                              |      |
| EnableLoadTimeWeaving                           |                                                              |                                                              |      |
|                                                 | "Activates a Spring LoadTimeWeaver for this application context, available as a bean with the name ""loadTimeWeaver"", similar to the <context:load-time-weaver> element in Spring XML." |                                                              |      |
| EnableLoadTimeWeaving.AspectJWeaving            |                                                              |                                                              |      |
|                                                 | AspectJ weaving enablement options.                          |                                                              |      |
| EnableMBeanExport                               |                                                              |                                                              |      |
|                                                 | Enables default exporting of all standard MBeans from the Spring context, as well as all @ManagedResource annotated beans. |                                                              |      |
| FilterType                                      |                                                              |                                                              |      |
|                                                 | Enumeration of the type filters that may be used in conjunction with @ComponentScan. |                                                              |      |
| FullyQualifiedAnnotationBeanNameGenerator       |                                                              |                                                              |      |
|                                                 | An extension of AnnotationBeanNameGenerator that uses the fully qualified class name as the default bean name if an explicit bean name is not supplied via a supported type-level annotation such as @Component (see AnnotationBeanNameGenerator for details on supported annotations). |                                                              |      |
| Import                                          |                                                              |                                                              |      |
|                                                 | Indicates one or more component classes to import — typically @Configuration classes. |                                                              |      |
| ImportAware                                     |                                                              |                                                              |      |
|                                                 | Interface to be implemented by any @Configuration class that wishes to be injected with the AnnotationMetadata of the @Configuration class that imported it. |                                                              |      |
| ImportAwareAotBeanPostProcessor                 |                                                              |                                                              |      |
|                                                 | A BeanPostProcessor that honours ImportAware callback using a mapping computed at build time. |                                                              |      |
| ImportBeanDefinitionRegistrar                   |                                                              |                                                              |      |
|                                                 | Interface to be implemented by types that register additional bean definitions when processing @Configuration classes. |                                                              |      |
| ImportResource                                  |                                                              |                                                              |      |
|                                                 | Indicates one or more resources containing bean definitions to import. |                                                              |      |
| ImportRuntimeHints                              |                                                              |                                                              |      |
|                                                 | Indicates that one or more RuntimeHintsRegistrar implementations should be processed. |                                                              |      |
| ImportSelector                                  |                                                              |                                                              |      |
|                                                 | Interface to be implemented by types that determine which @Configuration class(es) should be imported based on a given selection criteria, usually one or more annotation attributes. |                                                              |      |
| Jsr330ScopeMetadataResolver                     |                                                              |                                                              |      |
|                                                 | Simple ScopeMetadataResolver implementation that follows JSR-330 scoping rules: defaulting to prototype scope unless Singleton is present. |                                                              |      |
| Lazy                                            |                                                              |                                                              |      |
|                                                 | Indicates whether a bean is to be lazily initialized.        |                                                              |      |
| LoadTimeWeavingConfiguration                    |                                                              |                                                              |      |
|                                                 | @Configuration class that registers a LoadTimeWeaver bean.   |                                                              |      |
| LoadTimeWeavingConfigurer                       |                                                              |                                                              |      |
|                                                 | Interface to be implemented by @Configuration classes annotated with @EnableLoadTimeWeaving that wish to customize the LoadTimeWeaver instance to be used. |                                                              |      |
| MBeanExportConfiguration                        |                                                              |                                                              |      |
|                                                 | @Configuration class that registers a AnnotationMBeanExporter bean. |                                                              |      |
| Primary                                         |                                                              |                                                              |      |
|                                                 | Indicates that a bean should be given preference when multiple candidates are qualified to autowire a single-valued dependency. |                                                              |      |
| Profile                                         |                                                              |                                                              |      |
|                                                 | Indicates that a component is eligible for registration when one or more specified profiles are active. |                                                              |      |
| PropertySource                                  |                                                              |                                                              |      |
|                                                 | Annotation providing a convenient and declarative mechanism for adding a PropertySource to Spring's Environment. |                                                              |      |
| PropertySources                                 |                                                              |                                                              |      |
|                                                 | Container annotation that aggregates several PropertySource annotations. |                                                              |      |
| Role                                            |                                                              |                                                              |      |
|                                                 | Indicates the 'role' hint for a given bean.                  |                                                              |      |
| ScannedGenericBeanDefinition                    |                                                              |                                                              |      |
|                                                 | Extension of the GenericBeanDefinition class, based on an ASM ClassReader, with support for annotation metadata exposed through the AnnotatedBeanDefinition interface. |                                                              |      |
| Scope                                           |                                                              |                                                              |      |
|                                                 | When used as a type-level annotation in conjunction with @Component, @Scope indicates the name of a scope to use for instances of the annotated type. |                                                              |      |
| ScopedProxyMode                                 |                                                              |                                                              |      |
|                                                 | Enumerates the various scoped-proxy options.                 |                                                              |      |
| ScopeMetadata                                   |                                                              |                                                              |      |
|                                                 | Describes scope characteristics for a Spring-managed bean including the scope name and the scoped-proxy behavior. |                                                              |      |
| ScopeMetadataResolver                           |                                                              |                                                              |      |
|                                                 | Strategy interface for resolving the scope of bean definitions. |                                                              |      |
| TypeFilterUtils                                 | Collection of utilities for working with @ComponentScan type filters. |                                                              |      |
|                                                 |                                                              |                                                              |      |
| EnableSpringConfigured                          | Signals the current application context to apply dependency injection to non-managed classes that are instantiated outside the Spring bean factory (typically classes annotated with the @Configurable annotation). |                                                              |      |
|                                                 |                                                              |                                                              |      |
| SpringConfiguredConfiguration                   | @Configuration class that registers an AnnotationBeanConfigurerAspect capable of performing dependency injection services for non-Spring managed objects annotated with @Configurable. |                                                              |      |
|                                                 |                                                              |                                                              |      |



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



#### org.springframework.context.config



| org.springframework.context.config | 类型 |      |
| ---------------------------------- | ---- | ---- |
|                                    |      |      |
| Classes                            |      |      |
|                                    |      |      |
| ContextNamespaceHandler            |      |      |





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





#### org.springframework.context.expression



| org.springframework.context.expression  | 类型 |      |
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



#### org.springframework.context.i18n



| org.springframework.context.i18n | 类型 |      |
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



| org.springframework.context.index | 类型 |      |
| --------------------------------- | ---- | ---- |
|                                   |      |      |
| Classes                           |      |      |
|                                   |      |      |
| CandidateComponentsIndex          |      |      |
| CandidateComponentsIndexLoader    |      |      |

##### org.springframework.context.index.processor



| org.springframework.context.index.processor | 类型 |      |
| ------------------------------------------- | ---- | ---- |
|                                             |      |      |
| Classes                                     |      |      |
|                                             |      |      |
| CandidateComponentsIndexer                  |      |      |



#### org.springframework.context.support  


| org.springframework.context.support         | 类型      |      |
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





#### org.springframework.context.weaving



| Interfaces                   | 类型 |      |
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

| org.springframework.ejb.access               | 类型 |      |
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

| org.springframework.format | 类型 |      |
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

| org.springframework.format.annotation | 类型       |      |
| ------------------------------------- | ---------- | ---- |
| DateTimeFormat                        | @interface |      |
| DateTimeFormat.ISO                    | enum       |      |
| NumberFormat                          | @interface |      |
| NumberFormat.Style                    | enum       |      |
|                                       |            |      |

#### org.springframework.format.datetime



| org.springframework.format.datetime            | 类型 |      |
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

| org.springframework.format.datetime.joda     | 类型 |      |
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

| org.springframework.format.datetime.standard   | 类型 |      |
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

| org.springframework.format.number      | 类型 |      |
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



| org.springframework.format.support                     | 类型 |      |
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



| org.springframework.instrument.classloading | 类型 |      |
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

| org.springframework.instrument.classloading.glassfish | 类型 |      |
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



| org.springframework.jmx      | 类型      |      |
| ---------------------------- | --------- | ---- |
| JmxException                 |           |      |
| MBeanServerNotFoundException | exception |      |
|                              |           |      |



#### org.springframework.jmx.access

| org.springframework.jmx.access | 类型 |      |
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

| org.springframework.jmx.export | 类型 |      |
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

| org.springframework.jmx.export.annotation | 类型 |      |
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

| org.springframework.jmx.export.assembler | 类型 |      |
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

| org.springframework.jmx.export.metadata | 类型 |      |
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

| org.springframework.jmx.export.naming | 类型 |      |
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

| org.springframework.jmx.export.notification | 类型 |      |
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

| org.springframework.jndi    | 类型 |      |
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

| org.springframework.remoting     | 类型 |      |
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



| org.springframework.remoting.rmi    | 类型 |      |
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

| org.springframework.remoting.soap | 类型     |      |
| --------------------------------- | -------- | ---- |
| SoapFaultException                | abstract |      |
|                                   |          |      |
|                                   |          |      |





#### org.springframework.remoting.support

| org.springframework.remoting.support | 类型 |      |
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



| org.springframework.scheduling | 类型 |      |
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





| org.springframework.scheduling.annotation | 类型 |      |
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

| org.springframework.scheduling.concurrent | 类型 |      |
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



| org.springframework.scheduling.config  | 类型 |      |
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





| org.springframework.scheduling.support | 类型 |      |
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





| org.springframework.scripting | 类型 |      |
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





| org.springframework.scripting.bsh    | 类型 |      |
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



| org.springframework.scripting.config | 类型 |      |
| ------------------------------------ | ---- | ---- |
|                                      |      |      |
| Classes                              |      |      |
|                                      |      |      |
| LangNamespaceHandler                 |      |      |
| LangNamespaceUtils                   |      |      |



#### org.springframework.scriptingg.groovy



| org.springframework.scriptingg.groovy | 类型 |      |
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



| org.springframework.scripting.support | 类型 |      |
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



| org.springframework.stereotype | 类型 |      |
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



| org.springframework.ui | 类型 |      |
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



| org.springframework.ui.context | 类型 |      |
| ------------------------------ | ---- | ---- |
|                                |      |      |
| Interfaces                     |      |      |
|                                |      |      |
| HierarchicalThemeSource        |      |      |
| Theme                          |      |      |
| ThemeSource                    |      |      |



##### org.springframework.ui.context.support

| org.springframework.ui.context.support | 类型 |      |
| -------------------------------------- | ---- | ---- |
|                                        |      |      |
| Classes                                |      |      |
|                                        |      |      |
| DelegatingThemeSource                  |      |      |
| ResourceBundleThemeSource              |      |      |
| SimpleTheme                            |      |      |
| UiApplicationContextUtils              |      |      |





### org.springframework.validation



| org.springframework.validation     | 类型 |      |
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





| org.springframework.validation.annotation | 类型       |      |
| ----------------------------------------- | ---------- | ---- |
| Validated                                 | @interface |      |
|                                           |            |      |
|                                           |            |      |





#### org.springframework.validation.beanvalidation



| org.springframework.validation.beanvalidation | 类型 |      |
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



| org.springframework.validation.support | 类型 |      |
| -------------------------------------- | ---- | ---- |
| BindingAwareConcurrentModel            |      |      |
| BindingAwareModelMap                   |      |      |
|                                        |      |      |

