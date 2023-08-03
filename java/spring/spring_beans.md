# spring beans

Spring Bean 的初始化和实例化是两个不同的过程，它们的含义和目的也不同。
实例化是指创建对象的过程，也就是在内存中分配空间并对对象进行初始化的过程。在 Spring 中，Bean 的实例化是由 BeanFactory 或 ApplicationContext 负责完成的。当容器启动时，Spring 会根据配置文件或注解信息创建 Bean 的实例，并将其保存到容器中。实例化过程是在 BeanFactory 或 ApplicationContext 启动时完成的，一般不需要手动干预。
初始化是指在对象创建之后对其进行初始化的过程。在 Spring 中，Bean 的初始化是通过调用初始化方法（比如实现 InitializingBean 接口或在配置文件中指定的 init-method 方法）来完成的。初始化方法可以包括对 Bean 的属性进行设置、执行一些初始化操作等。初始化方法的执行时机可以通过配置文件中的 init-method 属性或 @PostConstruct 注解来指定。
需要注意的是，Bean 的初始化过程是在 Bean 实例化之后进行的，也就是说，初始化方法需要在 Bean 实例化之后调用。在 Spring 中，Bean 的初始化顺序是由 Bean 的依赖关系和配置文件中的 <bean> 元素的顺序共同决定的。
总的来说，Bean 的实例化和初始化是两个不同的过程，它们的目的和方式也不同。实例化是创建对象的过程，而初始化是在对象创建之后对其进行初始化的过程。在 Spring 中，Bean 的实例化和初始化都是由容器自动管理的，一般不需要手动干预。

ConstructorArgumentValues
ValueHolder
String type
Object value
String name
Object source


org.springframework.beans.BeanMetadataElement
Object getSource();


抽象类org.springframework.beans.factory.xml.NamespaceHandlerSupport实现了org.springframework.beans.factory.xml.NamespaceHandler接口

子类有

NamespaceHandlerSupport (org.springframework.beans.factory.xml)
    JeeNamespaceHandler (org.springframework.ejb.config)
    AopNamespaceHandler (org.springframework.aop.config)
    ContextNamespaceHandler (org.springframework.context.config)
    LangNamespaceHandler (org.springframework.scripting.config)
    UtilNamespaceHandler (org.springframework.beans.factory.xml)
    MvcNamespaceHandler (org.springframework.web.servlet.config)
    JdbcNamespaceHandler (org.springframework.jdbc.config)
    RepositoryNameSpaceHandler (org.springframework.data.repository.config)
    TaskNamespaceHandler (org.springframework.scheduling.config)
    TxNamespaceHandler (org.springframework.transaction.config)
    CacheNamespaceHandler (org.springframework.cache.config)



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
## ioc注入
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


## Spring doc bean

#### Chap 1.6.1
Lifecycle Callbacks


@PostConstruct
@PreDestroy



interface BeanPostProcessor

Factory hook


SmartLifecycle

Lifecycle

### Chap. 17
bean继承



Bean
parent

### Chap.18
bean的其他定义方式


beanpostprocessor
beanfactorypostprocessor

factorybean



org.springframework.beans.factory.xml.NamespaceHandler 接口
void init();
BeanDefinition parse(Element element, ParserContext parserContext);
BeanDefinitionHolder decorate(Node source, BeanDefinitionHolder definition, ParserContext parserContext);

abstract class NamespaceHandlerSupport implements NamespaceHandler


实现类有MvcNamespaceHandler，处理springmvc xml配置文件




在 Spring Framework 中，属性访问通常通过 `BeanWrapper` 和 `PropertyAccessor` 接口来实现。`BeanWrapper` 是一个用于访问 JavaBean 属性的接口，可以通过反射或内省来读取和设置属性值。而 `PropertyAccessor` 接口定义了属性访问的通用方法。

以下是一个示例，展示了如何使用 `BeanWrapper` 和 `PropertyAccessor` 进行属性访问：

```java
import org.springframework.beans.BeanWrapper;
import org.springframework.beans.BeanWrapperImpl;

public class PropertyAccessExample {
    public static void main(String[] args) {
        // 创建一个对象
        Person person = new Person();
        person.setName("John");
        person.setAge(30);

        // 使用 BeanWrapper 包装对象
        BeanWrapper beanWrapper = new BeanWrapperImpl(person);

        // 通过 BeanWrapper 访问属性
        String name = (String) beanWrapper.getPropertyValue("name");
        Integer age = (Integer) beanWrapper.getPropertyValue("age");
        System.out.println("Name: " + name);
        System.out.println("Age: " + age);

        // 设置新的属性值
        beanWrapper.setPropertyValue("name", "Jane");
        beanWrapper.setPropertyValue("age", 25);

        System.out.println("Updated Name: " + person.getName());
        System.out.println("Updated Age: " + person.getAge());
    }

    public static class Person {
        private String name;
        private Integer age;

        // Getter 和 Setter 方法省略

        public String getName() {
            return name;
        }

        public void setName(String name) {
            this.name = name;
        }

        public Integer getAge() {
            return age;
        }

        public void setAge(Integer age) {
            this.age = age;
        }
    }
}
```

在上面的示例中，我们创建了一个 `Person` 类，使用 `BeanWrapper` 包装对象，并使用 `getPropertyValue` 和 `setPropertyValue` 方法来访问和修改属性值。这样，我们可以使用 `BeanWrapper` 来方便地进行属性的读取和设置操作。



## 分包解析代码 v5.2.9
https://docs.spring.io/spring-framework/docs/5.2.x/javadoc-api/


### org.springframework.beans

| org.springframework.beans                            | 类型 |      |
| ---------------------------------------------------- |-----------| ---- |
|                                                      |           |      |
| Interfaces                                           |           |      |
|                                                      |           |      |
| BeanInfoFactory                                      | interface |      |
| BeanMetadataElement                                  | interface |      |
| BeanWrapper                                          | interface |      |
| ConfigurablePropertyAccessor                         | interface |      |
| Mergeable                                            | interface |      |
| PropertyAccessor                                     | interface |      |
| PropertyEditorRegistrar                              | interface |      |
| PropertyEditorRegistry                               | interface |      |
| PropertyValues                                       | interface |      |
| TypeConverter                                        | interface |      |
|                                                      |           |      |
| Classes                                              |           |      |
|                                                      |           |      |
| AbstractNestablePropertyAccessor                     |           |      |
| AbstractNestablePropertyAccessor.PropertyHandler     |           |      |
| AbstractNestablePropertyAccessor.PropertyTokenHolder |           |      |
| AbstractPropertyAccessor                             |           |      |
| BeanMetadataAttribute                                |           |      |
| BeanMetadataAttributeAccessor                        |           |      |
| BeanUtils                                            |           | 重要 |
| BeanWrapperImpl                                      |           |      |
| CachedIntrospectionResults                           |           |      |
| DirectFieldAccessor                                  |           |      |
| ExtendedBeanInfoFactory                              |           |      |
| MutablePropertyValues                                |           |      |
| PropertyAccessorFactory                              |           |      |
| PropertyAccessorUtils                                |           |      |
| PropertyEditorRegistrySupport                        |           |      |
| PropertyMatches                                      |           |      |
| PropertyValue                                        |           |      |
| PropertyValuesEditor                                 |           |      |
| SimpleTypeConverter                                  |           |      |
| TypeConverterSupport                                 |           |      |
|                                                      |           |      |
| Exceptions                                           |           |      |
|                                                      |           |      |
| BeanInstantiationException                           | exception         |      |
| BeansException                                       |   exception        |      |
| ConversionNotSupportedException                      |   exception        |      |
| FatalBeanException                                   |   exception        |      |
| InvalidPropertyException                             |   exception        |      |
| MethodInvocationException                            |   exception        |      |
| NotReadablePropertyException                         |  exception         |      |
| NotWritablePropertyException                         |  exception         |      |
| NullValueInNestedPathException                       |   exception        |      |
| PropertyAccessException                              |    exception       |      |
| PropertyBatchUpdateException                         |  exception         |      |
| TypeMismatchException                                |   exception        |      |





BeanUtils methods

![BeanUtils_methods](..\..\imgs\spring\BeanUtils_methods.png)





#### org.springframework.beans.annotation



| org.springframework.beans.annotation | 类型     |      |
| ------------------------------------ | -------- | ---- |
| AnnotationBeanUtils                  | abstract |      |
|                                      |          |      |
|                                      |          |      |



#### org.springframework.beans.factory



| org.springframework.beans.factory  | 类型 |      |
| ---------------------------------- |-----------| ---- |
|                                    |           |      |
| Interfaces                         |           |      |
|                                    |           |      |
| Aware                              | interface |      |
| BeanClassLoaderAware               | interface |      |
| BeanFactory                        | interface |      |
| BeanFactoryAware                   | interface |      |
| BeanNameAware                      | interface |      |
| DisposableBean                     | interface |      |
| FactoryBean                        | interface |      |
| HierarchicalBeanFactory            | interface |      |
| InitializingBean                   | interface |      |
| ListableBeanFactory                | interface |      |
| NamedBean                          | interface |      |
| ObjectFactory                      | interface |      |
| ObjectProvider                     | interface |      |
| SmartFactoryBean                   | interface |      |
| SmartInitializingSingleton         | interface |      |
|                                    |           |      |
| Classes                            |           |      |
|                                    |           |      |
| BeanFactoryUtils                   |           |      |
| InjectionPoint                     |           |      |
|                                    |           |      |
| Exceptions                         |           |      |
|                                    |           |      |
| BeanCreationException              | exception         |      |
| BeanCreationNotAllowedException    |  exception         |      |
| BeanCurrentlyInCreationException   |  exception         |      |
| BeanDefinitionStoreException       |  exception         |      |
| BeanExpressionException            |   exception        |      |
| BeanInitializationException        |  exception         |      |
| BeanIsAbstractException            |  exception         |      |
| BeanIsNotAFactoryException         |  exception         |      |
| BeanNotOfRequiredTypeException     |  exception         |      |
| CannotLoadBeanClassException       |  exception         |      |
| FactoryBeanNotInitializedException |  exception         |      |
| NoSuchBeanDefinitionException      |  exception         |      |
| NoUniqueBeanDefinitionException    |  exception         |      |
| UnsatisfiedDependencyException     |  exception         |      |

##### org.springframework.beans.factory.annotation



| org.springframework.beans.factory.annotation | 类型 |      |
| -------------------------------------------- |-----------| ---- |
|                                              |           |      |
| Interfaces                                   |           |      |
|                                              |           |      |
| AnnotatedBeanDefinition                      | interface |      |
|                                              |           |      |
| Classes                                      |           |      |
|                                              |           |      |
| AnnotatedGenericBeanDefinition               |           |      |
| AnnotationBeanWiringInfoResolver             |           |      |
| AutowiredAnnotationBeanPostProcessor         |           |      |
| BeanFactoryAnnotationUtils                   |           |      |
| CustomAutowireConfigurer                     |           |      |
| InitDestroyAnnotationBeanPostProcessor       |           |      |
| InjectionMetadata                            |           |      |
| InjectionMetadata.InjectedElement            |           |      |
| ParameterResolutionDelegate                  |           |      |
| QualifierAnnotationAutowireCandidateResolver |           |      |
| RequiredAnnotationBeanPostProcessor          |           |      |
|                                              |           |      |
| Enums                                        |           |      |
|                                              |           |      |
| Autowire                                     | enum      |      |
|                                              |           |      |
| Annotation Types                             |           |      |
|                                              |           |      |
| Autowired                                    |  @interface         |      |
| Configurable                                 | @interface          |      |
| Lookup                                       |  @interface         |      |
| Qualifier                                    |  @interface         |      |
| Required                                     |  @interface         |      |
| Value                                        |  @interface         |      |

##### org.springframework.beans.factory.config



| org.springframework.beans.factory.config   | 类型 |                                  |
|--------------------------------------------|------------------------------|----------------------------------|
|                                            |                              |                                  |
| Interfaces                                 |                              |                                  |
|                                            |                              |                                  |
| AutowireCapableBeanFactory                 | interface                    |                                  |
| BeanDefinition                             | interface                    |                                  |
| BeanDefinitionCustomizer                   | interface                    |                                  |
| BeanExpressionResolver                     | interface                    |                                  |
| BeanFactoryPostProcessor                   | interface                    |                                  |
| BeanPostProcessor                          | interface                    |                                  |
| BeanReference                              | interface                    |                                  |
| ConfigurableBeanFactory                    | interface                    |                                  |
| ConfigurableListableBeanFactory            | interface                    |                                  |
| DestructionAwareBeanPostProcessor          | interface                    |                                  |
| InstantiationAwareBeanPostProcessor        | interface                    |                                  |
| Scope                                      | interface                    |                                  |
| SingletonBeanRegistry                      | interface                    |                                  |
| SmartInstantiationAwareBeanPostProcessor   | interface                    |                                  |
| YamlProcessor.DocumentMatcher              | interface                    |                                  |
| YamlProcessor.MatchCallback                | interface                    |                                  |
|                                            |                              |                                  |
| Classes                                    |                              |                                  |
|                                            |                              |                                  |
| AbstractFactoryBean                        | abstract                            |                                  |
| AutowiredPropertyMarker                    |                              |                                  |
| BeanDefinitionHolder                       |                              |                                  |
| BeanDefinitionVisitor                      |                              |                                  |
| BeanExpressionContext                      |                              |                                  |
| ConstructorArgumentValues                  |                              |                                  |
| ConstructorArgumentValues.ValueHolder      |                              |                                  |
| CustomEditorConfigurer                     |                              |                                  |
| CustomScopeConfigurer                      |                              |                                  |
| DependencyDescriptor                       |                              |                                  |
| DeprecatedBeanWarner                       |                              |                                  |
| EmbeddedValueResolver                      |                              |                                  |
| FieldRetrievingFactoryBean                 |                              |                                  |
| InstantiationAwareBeanPostProcessorAdapter |                              |                                  |
| ListFactoryBean                            |                              |                                  |
| MapFactoryBean                             |                              |                                  |
| MethodInvokingBean                         |                              |                                  |
| MethodInvokingFactoryBean                  |                              |                                  |
| NamedBeanHolder                            |                              |                                  |
| ObjectFactoryCreatingFactoryBean           |                              |                                  |
| PlaceholderConfigurerSupport               |                              |                                  |
| PreferencesPlaceholderConfigurer           |                              |                                  |
| PropertiesFactoryBean                      |                              |                                  |
| PropertyOverrideConfigurer                 |                              |                                  |
| PropertyPathFactoryBean                    |                              |                                  |
| PropertyPlaceholderConfigurer              |                              |                                  |
| PropertyResourceConfigurer                 |                              |                                  |
| ProviderCreatingFactoryBean                |                              |                                  |
| RuntimeBeanNameReference                   |                              |                                  |
| RuntimeBeanReference                       |                              |                                  |
| ServiceLocatorFactoryBean                  |                              | FactoryBean<Object>              |
| ServiceLocatorFactoryBean.ServiceLocatorInvocationHandler                 | implements InvocationHandler |                                  |
| SetFactoryBean                             |                              | AbstractFactoryBean<Set<Object>> |
| TypedStringValue                           |                              | BeanMetadataElement              |
| YamlMapFactoryBean                         |                              | YamlProcessor子类                  |
| YamlProcessor                              | abstract                     |                                  |
| YamlPropertiesFactoryBean                  |                              |    YamlProcessor子类                              |
|                                            |                              |                                  |
| Enums                                      |                              |                                  |
|                                            |                              |                                  |
| YamlProcessor.MatchStatus                  | enum                         |                                  |
| YamlProcessor.ResolutionMethod             | enum                         |                                  |


AbstractFactoryBean (org.springframework.beans.factory.config)
SortedResourcesFactoryBean (org.springframework.jdbc.config)
MapFactoryBean (org.springframework.beans.factory.config)
ListFactoryBean (org.springframework.beans.factory.config)
SetFactoryBean (org.springframework.beans.factory.config)
LettuceFactoryBeanSupport (io.lettuce.core.support)
RedisClientFactoryBean (io.lettuce.core.support)
RedisClusterClientFactoryBean (io.lettuce.core.support)
AbstractRepositoryPopulatorFactoryBean (org.springframework.data.repository.init)
UnmarshallerRepositoryPopulatorFactoryBean (org.springframework.data.repository.init)
Jackson2RepositoryPopulatorFactoryBean (org.springframework.data.repository.init)
ClientResourcesFactoryBean (io.lettuce.core.support)
ObjectFactoryCreatingFactoryBean (org.springframework.beans.factory.config)
ProviderCreatingFactoryBean (org.springframework.beans.factory.config)
AbstractServiceLoaderBasedFactoryBean (org.springframework.beans.factory.serviceloader)
ServiceListFactoryBean (org.springframework.beans.factory.serviceloader)
ServiceLoaderFactoryBean (org.springframework.beans.factory.serviceloader)
ServiceFactoryBean (org.springframework.beans.factory.serviceloader)


##### org.springframework.beans.factory.groovy



| org.springframework.beans.factory.groovy | 类型 |      |
| ---------------------------------------- | ---- | ---- |
|                                          |      |      |
|                                          |      |      |
|                                          |      |      |

##### org.springframework.beans.factory.parsing



| org.springframework.beans.factory.parsing | 类型 |                          |
| ----------------------------------------- |-----------|--------------------------|
|                                           |           |                          |
| Interfaces                                |           |                          |
|                                           |           |                          |
| ComponentDefinition                       | interface |                          |
| DefaultsDefinition                        | interface |                          |
| ParseState.Entry                          | interface |                          |
| ProblemReporter                           | interface |                          |
| ReaderEventListener                       | interface |                          |
| SourceExtractor                           | interface |                          |
|                                           |           |                          |
| Classes                                   |           |                          |
|                                           |           |                          |
| AbstractComponentDefinition               | abstract  |                          |
| AliasDefinition                           |           | BeanMetadataElement接口实现类 |
| BeanComponentDefinition                   |           |                          |
| BeanEntry                                 |           |                          |
| CompositeComponentDefinition              |           |                          |
| ConstructorArgumentEntry                  |           |                          |
| EmptyReaderEventListener                  |           |                          |
| FailFastProblemReporter                   |           |                          |
| ImportDefinition                          |           |                          |
| Location                                  |           |                          |
| NullSourceExtractor                       |           |                          |
| ParseState                                |           |                          |
| PassThroughSourceExtractor                |           | SourceExtractor接口        |
| Problem                                   |           |                          |
| PropertyEntry                             |           |                          |
| QualifierEntry                            |           |                          |
| ReaderContext                             |           |                          |
|                                           |           |                          |
| Exceptions                                |           |                          |
|                                           |           |                          |
| BeanDefinitionParsingException            | exception         |                          |


org.springframework.beans.factory.parsing.SourceExtractor
接口实现类
NullSourceExtractor (org.springframework.beans.factory.parsing)
PassThroughSourceExtractor (org.springframework.beans.factory.parsing)


AbstractComponentDefinition (org.springframework.beans.factory.parsing)
CompositeComponentDefinition (org.springframework.beans.factory.parsing)
AspectComponentDefinition (org.springframework.aop.config)
PointcutComponentDefinition (org.springframework.aop.config)
AdvisorComponentDefinition (org.springframework.aop.config)


#####  org.springframework.beans.factory.serviceloader

| org.springframework.beans.factory.serviceloader | 类型     |      |
| ----------------------------------------------- | -------- | ---- |
| AbstractServiceLoaderBasedFactoryBean           | abstract |      |
| ServiceFactoryBean                              |          |      |
| ServiceListFactoryBean                          |          |      |
| ServiceLoaderFactoryBean                        |          |      |

##### org.springframework.beans.factory.support

| org.springframework.beans.factory.support | 类型 |      |
| ----------------------------------------- |-----------| ---- |
|                                           |           |      |
| Interfaces                                |           |      |
|                                           |           |      |
| AutowireCandidateResolver                 | interface |      |
| BeanDefinitionReader                      | interface |      |
| BeanDefinitionRegistry                    | interface |      |
| BeanDefinitionRegistryPostProcessor       | interface |      |
| BeanNameGenerator                         | interface |      |
| InstantiationStrategy                     | interface |      |
| MergedBeanDefinitionPostProcessor         | interface |      |
| MethodReplacer                            | interface |      |
| SecurityContextProvider                   | interface |      |
|                                           |           |      |
| Classes                                   |           |      |
|                                           |           |      |
| AbstractAutowireCapableBeanFactory        | abstract  |      |
| AbstractBeanDefinition                    | abstract  |      |
| AbstractBeanDefinitionReader              | abstract  |      |
| AbstractBeanFactory                       | abstract  |      |
| AutowireCandidateQualifier                |           |      |
| BeanDefinitionBuilder                     |           |      |
| BeanDefinitionDefaults                    |           |      |
| BeanDefinitionReaderUtils                 |           |      |
| CglibSubclassingInstantiationStrategy     |           |      |
| ChildBeanDefinition                       |           |      |
| DefaultBeanNameGenerator                  |           |      |
| DefaultListableBeanFactory                |           |      |
| DefaultSingletonBeanRegistry              |           |      |
| FactoryBeanRegistrySupport                |           |      |
| GenericBeanDefinition                     |           |      |
| GenericTypeAwareAutowireCandidateResolver |           |      |
| LookupOverride                            |           |      |
| ManagedArray                              |           |      |
| ManagedList                               |           |      |
| ManagedMap                                |           |      |
| ManagedProperties                         |           |      |
| ManagedSet                                |           |      |
| MethodOverride                            |           |      |
| MethodOverrides                           |           |      |
| PropertiesBeanDefinitionReader            |           |      |
| ReplaceOverride                           |           |      |
| RootBeanDefinition                        |           |      |
| SimpleAutowireCandidateResolver           |           |      |
| SimpleBeanDefinitionRegistry              |           |      |
| SimpleInstantiationStrategy               |           |      |
| SimpleSecurityContextProvider             |           |      |
| StaticListableBeanFactory                 |           |      |
|                                           |           |      |
| Exceptions                                |           |      |
|                                           |           |      |
| BeanDefinitionOverrideException           | exception         |      |
| BeanDefinitionValidationException         | exception          |      |


BeanDefinitionReader 接口
方法
- BeanDefinitionRegistry getRegistry();
- ResourceLoader getResourceLoader();
- ClassLoader getBeanClassLoader();
- BeanNameGenerator getBeanNameGenerator();
- int loadBeanDefinitions(Resource resource)

AutowireCandidateResolver 接口



##### org.springframework.beans.factory.wiring



| org.springframework.beans.factory.wiring | 类型      |                            |
| ---------------------------------------- | --------- | -------------------------- |
| BeanConfigurerSupport                    |           |                            |
| BeanWiringInfo                           |           |                            |
| BeanWiringInfoResolver                   | interface |                            |
| ClassNameBeanWiringInfoResolver          |           | 子类BeanWiringInfoResolver |
|                                          |           |                            |
|                                          |           |                            |

BeanWiringInfoResolver子类
AnnotationBeanWiringInfoResolver (org.springframework.beans.factory.annotation)
ClassNameBeanWiringInfoResolver (org.springframework.beans.factory.wiring)
AnnotationBeanWiringInfoResolver ClassNameBeanWiringInfoResolver区别

`AnnotationBeanWiringInfoResolver` 和 `ClassNameBeanWiringInfoResolver` 是 Spring 中两个不同的 Bean WiringInfo 解析器。
`AnnotationBeanWiringInfoResolver` 是基于注解的 Bean WiringInfo 解析器，它可以解析使用 Spring 注解（如 `@Autowired`、`@Qualifier`、`@Resource` 等）进行依赖注入的 Bean。它可以扫描类路径下的所有 Bean，并解析它们之间的依赖关系。在解析过程中，它会查找 Bean 中使用注解定义的依赖关系，并将其转换为 WiringInfo 对象，以便容器使用。
`ClassNameBeanWiringInfoResolver` 是基于类名的 Bean WiringInfo 解析器，它可以根据类名解析 Bean 的 WiringInfo。它在解析 Bean 时不会考虑任何注解，仅仅根据类名来确定 Bean 之间的依赖关系。在使用这个解析器时，需要手动指定 Bean 之间的依赖关系，通常是通过配置文件来完成。
需要注意的是，这两种 Bean WiringInfo 解析器的使用场景不同。`AnnotationBeanWiringInfoResolver` 更适合使用注解进行依赖注入的场景，而 `ClassNameBeanWiringInfoResolver` 更适合手动配置 Bean 之间的依赖关系的场景。在实际开发中，可以根据具体的需求选择合适的解析器来进行使用。

##### org.springframework.beans.factory.xml



| org.springframework.beans.factory.xml | 类型 |      |
| ------------------------------------- | ---- | ---- |
|                                       |      |      |
| Interfaces                            |      |      |
|                                       |      |      |
| BeanDefinitionDecorator               |      |      |
| BeanDefinitionDocumentReader          |      |      |
| BeanDefinitionParser                  |      |      |
| DocumentLoader                        |      |      |
| NamespaceHandler                      |      |      |
| NamespaceHandlerResolver              |      |      |
|                                       |      |      |
| Classes                               |      |      |
|                                       |      |      |
| AbstractBeanDefinitionParser          |      |      |
| AbstractSimpleBeanDefinitionParser    |      |      |
| AbstractSingleBeanDefinitionParser    |      |      |
| BeanDefinitionParserDelegate          |      |      |
| BeansDtdResolver                      |      |      |
| DefaultBeanDefinitionDocumentReader   |      |      |
| DefaultDocumentLoader                 |      |      |
| DefaultNamespaceHandlerResolver       |      |      |
| DelegatingEntityResolver              |      |      |
| DocumentDefaultsDefinition            |      |      |
| NamespaceHandlerSupport               |      |      |
| ParserContext                         |      |      |
| PluggableSchemaResolver               |      |      |
| ResourceEntityResolver                |      |      |
| SimpleConstructorNamespaceHandler     |      |      |
| SimplePropertyNamespaceHandler        |      |      |
| UtilNamespaceHandler                  |      |      |
| XmlBeanDefinitionReader               |      |      |
| XmlBeanFactory                        |      |      |
| XmlReaderContext                      |      |      |
|                                       |      |      |
| Exceptions                            |      |      |
|                                       |      |      |
| XmlBeanDefinitionStoreException       |      |      |





#### org.springframework.beans.propertyeditors



| org.springframework.beans.propertyeditors | 类型 |      |
| ----------------------------------------- | ---- | ---- |
|                                           |      |      |
| Classes                                   |      |      |
|                                           |      |      |
| ByteArrayPropertyEditor                   |      |      |
| CharacterEditor                           |      |      |
| CharArrayPropertyEditor                   |      |      |
| CharsetEditor                             |      |      |
| ClassArrayEditor                          |      |      |
| ClassEditor                               |      |      |
| CurrencyEditor                            |      |      |
| CustomBooleanEditor                       |      |      |
| CustomCollectionEditor                    |      |      |
| CustomDateEditor                          |      |      |
| CustomMapEditor                           |      |      |
| CustomNumberEditor                        |      |      |
| FileEditor                                |      |      |
| InputSourceEditor                         |      |      |
| InputStreamEditor                         |      |      |
| LocaleEditor                              |      |      |
| PathEditor                                |      |      |
| PatternEditor                             |      |      |
| PropertiesEditor                          |      |      |
| ReaderEditor                              |      |      |
| ResourceBundleEditor                      |      |      |
| StringArrayPropertyEditor                 |      |      |
| StringTrimmerEditor                       |      |      |
| TimeZoneEditor                            |      |      |
| URIEditor                                 |      |      |
| URLEditor                                 |      |      |
| UUIDEditor                                |      |      |
| ZoneIdEditor                              |      |      |

#### org.springframework.beans.support



| org.springframework.beans.support | 类型      |      |
| --------------------------------- | --------- | ---- |
| ArgumentConvertingMethodInvoker   |           |      |
| MutableSortDefinition             |           |      |
| PagedListHolder<E>                |           |      |
| PropertyComparator<T>             |           |      |
| ResourceEditorRegistrar           |           |      |
| SortDefinition                    | interface |      |




| org.apache.dubbo.config.spring.beans.factory.annotation |      |      |
| ---------------------------------- | ---- | ---- |
|      ReferenceAnnotationBeanPostProcessor            |      |      |

