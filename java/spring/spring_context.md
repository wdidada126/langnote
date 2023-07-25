# context

org.springframework.context.annotation.ImportResource

spring-context.xlsx

Spring Security 提供了诸多的 TokenStore 实现，如存在内存中的 InMemoryTokenStore 、存在数据库中的 JdbcTokenStore、存在 Redis 中的 RedisTokenStore

https://www.jianshu.com/p/64f2ee59acd9

org.springframework.context.annotation.ImportResource


ComponentScanAnnotationParser

org.springframework.context.annotation.ConfigurationClassParser#ConfigurationClassParser 中用ComponentScanAnnotationParser










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
| TypeFilterUtils                                 |                                                              |                                                              |      |
|                                                 | Collection of utilities for working with @ComponentScan type filters. |                                                              |      |
| EnableSpringConfigured                          |                                                              |                                                              |      |
|                                                 | Signals the current application context to apply dependency injection to non-managed classes that are instantiated outside the Spring bean factory (typically classes annotated with the @Configurable annotation). |                                                              |      |
| SpringConfiguredConfiguration                   |                                                              |                                                              |      |
|                                                 | @Configuration class that registers an AnnotationBeanConfigurerAspect capable of performing dependency injection services for non-Spring managed objects annotated with @Configurable. |                                                              |      |