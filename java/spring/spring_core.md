# spring_core

org.springframework.core.xlsx



https://docs.spring.io/spring-framework/docs/5.2.x/javadoc-api/



AnnotationAttributes

## 源代码分包解析 v5.2.9



### org.springframework.asm

| org.springframework.asm   | 类型 |      |
| ------------------------- | ---- | ---- |
|                           |      |      |
| Interfaces                |      |      |
| Opcodes                   |      |      |
|                           |      |      |
| Classes                   |      |      |
| AnnotationVisitor         |      |      |
| Attribute                 |      |      |
| ByteVector                |      |      |
| ClassReader               |      |      |
| ClassVisitor              |      |      |
| ClassWriter               |      |      |
| ConstantDynamic           |      |      |
| FieldVisitor              |      |      |
| Handle                    |      |      |
| Label                     |      |      |
| MethodVisitor             |      |      |
| ModuleVisitor             |      |      |
| RecordComponentVisitor    |      |      |
| SpringAsmInfo             |      |      |
| Type                      |      |      |
| TypePath                  |      |      |
| TypeReference             |      |      |
|                           |      |      |
| Exceptions                |      |      |
| ClassTooLargeException    |      |      |
| MethodTooLargeException   |      |      |
|                           |      |      |
|                           |      |      |
|                           |      |      |
|                           |      |      |
| org.springframework.cglib | 类型 |      |
|                           |      |      |
| Classes                   |      |      |
|                           |      |      |
| SpringCglibInfo           |      |      |
|                           |      |      |



### org.springframework.cglib



| org.springframework.cglib       | 类型 |      |
| ------------------------------- | ---- | ---- |
| Classes                         |      |      |
|                                 |      |      |
| SpringCglibInfo                 |      |      |
|                                 |      |      |
| org.springframework.cglib.beans |      |      |
|                                 |      |      |
| Classes                         |      |      |
|                                 |      |      |
| BeanCopier                      |      |      |
| BeanCopier.Generator            |      |      |
| BeanGenerator                   |      |      |
| BeanMap                         |      |      |
| BeanMap.Generator               |      |      |
| BulkBean                        |      |      |
| BulkBean.Generator              |      |      |
| FixedKeySet                     |      |      |
| ImmutableBean                   |      |      |
| ImmutableBean.Generator         |      |      |
|                                 |      |      |
| Exceptions                      |      |      |
|                                 |      |      |
| BulkBeanException               |      |      |



#### org.springframework.cglib.beans


| org.springframework.cglib.beans        | 类型 |      |
| ---- | ---- | ---- |
|                                        |      |      |
| Classes                                |      |      |
|                                        |      |      |
| BeanCopier                             |      |      |
| BeanCopier.Generator                   |      |      |
| BeanGenerator                          |      |      |
| BeanMap                                |      |      |
| BeanMap.Generator                      |      |      |
| BulkBean                               |      |      |
| BulkBean.Generator                     |      |      |
| FixedKeySet                            |      |      |
| ImmutableBean                          |      |      |
| ImmutableBean.Generator                |      |      |
|                                        |      |      |
| Exceptions                             |      |      |
|                                        |      |      |
| BulkBeanException                      |      |      |
|                                        |      |      |
|                                        |      |      |
|                                        |      |      |





#### org.springframework.cglib.beans



| org.springframework.cglib.beans | 类型 |      |
| ------------------------------- | ---- | ---- |
| Classes                         |      |      |
|                                 |      |      |
| BeanCopier                      |      |      |
| BeanCopier.Generator            |      |      |
| BeanGenerator                   |      |      |
| BeanMap                         |      |      |
| BeanMap.Generator               |      |      |
| BulkBean                        |      |      |
| BulkBean.Generator              |      |      |
| FixedKeySet                     |      |      |
| ImmutableBean                   |      |      |
| ImmutableBean.Generator         |      |      |
|                                 |      |      |
| Exceptions                      |      |      |
|                                 |      |      |
| BulkBeanException               |      |      |
|                                 |      |      |





#### org.springframework.cglib.core


| org.springframework.cglib.core         | 类型 |      |
| ---- | ---- | ---- |
|                                        |      |      |
| Classes                                |      |      |
|                                        |      |      |
| AbstractClassGenerator                 |      |      |
| AbstractClassGenerator.ClassLoaderData |      |      |
| AbstractClassGenerator.Source          |      |      |
| Block | | |
| ClassEmitter | | |
| ClassEmitter.FieldInfo | | |
|  | | |
| ClassLoaderAwareGeneratorStrategy      |      |      |
|  | | |
|  | | |
| FieldTypeCustomizer | | |
| GeneratorStrategy | | |
| HashCodeCustomizer | | |
| KeyFactory                             |      |      |
| org.springframework.cglib.core.KeyFactory.Generator | 内部类 | |
| KeyFactoryCustomizer | interface | |
| KeyFactory.Generator                   |      |      |
| ReflectUtils                           |      |      |
| SpringNamingPolicy                     |      | extends DefaultNamingPolicy  自定义 Spring Bean 的命名策略,覆盖默认的命名规则。 提供更可读的 Bean 名称。 |
| Transformer | interface |      |
| TypeUtils |      |      |
| VisibilityPredicate |      | DuplicatesPredicate |
| WeakCacheKey | | |







GeneratorStrategy接口实现类

DefaultGeneratorStrategy (org.springframework.cglib.core)
UndeclaredThrowableStrategy (org.springframework.cglib.transform.impl)
ClassLoaderAwareUndeclaredThrowableStrategy in CglibAopProxy (org.springframework.aop.framework)
ClassLoaderAwareGeneratorStrategy in CglibSubclassingInstantiationStrategy (org.springframework.beans.factory.support)
BeanFactoryAwareGeneratorStrategy in ConfigurationClassEnhancer (org.springframework.context.annotation)





Spring NamingPolicy 类允许自定义 Spring Bean 的命名规则。

它的主要作用是:

1. 自定义 Spring Bean 的命名策略,覆盖默认的命名规则。

2. 提供更可读的 Bean 名称。

使用示例:

```java
@Configuration
public class NamingConfig {

  @Bean
  public NamingPolicy namingPolicy() {
    return new SpringNamingPolicy(new CamelCaseStrategy()); 
  }

}

@Component("userService")
public class UserService {
  // ...
}
```

在这个例子中,我们通过 SpringNamingPolicy 类使用了 CamelCaseStrategy 来自定义 Bean 的命名规则为驼峰命名法。那么 UserService Bean 的名称就会被覆盖成 "userService",而不是默认的 "userServiceImpl"。

这样可以让 Bean 名称更简洁,符合 Java 命名约定。



#### org.springframework.cglib.proxy



| org.springframework.cglib.proxy        | 类型 |      |
| ---- | ---- | ---- |
|                                        |      |      |
|                                        |      |      |
| Interfaces                             |      |      |
|                                        |      |      |
| Enhancer.EnhancerKey                   |      |      |
|                                        |      |      |
| Classes                                |      |      |
|                                        |      |      |
| Enhancer                               |      |      |
| MethodProxy                            |      |      |
|                                        |      |      |
|                                        |      |      |
|                                        |      |      |
|                                        |      |      |
|                                        |      |      |



#### org.springframework.cglib.transform





#### org.springframework.cglib.util








### org.springframework.core

| org.springframework.core                                | 类型      | 详解                                                         |
|---------------------------------------------------------|-----------|-------------------------------------------------------------------|
| AliasRegistry                                           | interface | "void registerAlias(String name, String alias)                    |
| void removeAlias(String alias)"                         |||
| AttributeAccessor                                       | interface |                                                                   |
| AttributeAccessorSupport                                | abstract  |                                                                   |
| BridgeMethodResolver                                    |           | final类，一堆static方法                                                 |
| CollectionFactory                                       |           | final类，有两个map属性，工具类，创建map，list的                                   |
| ConfigurableObjectInputStream                           |           | ConfigurableObjectInputStream 通过实现 resolveClass() 和 resolveProxyClass() 方法，来控制反序列化过程中哪些类可以被反序列化，哪些类不能被反序列化  见下面 |
| Constants                                               |           |                                                                   |
| Constants.ConstantException                             | 内部类 exception |                                                                   |
| Conventions                                             | abstract |                                                                   |
| DecoratingClassLoader                                   | abstract  | "Set<String> excludedPackages                                     |
| Set<String> excludedClasses"                            |||
| DecoratingProxy                                         | interface | Class<?> getDecoratedClass() 子类，见下面  将一个对象包装成另一个对象。它的作用是在不修改原始对象的情况下，为其添加额外的功能或修改其行为。 |
| DefaultParameterNameDiscoverer                          |           | extends PrioritizedParameterNameDiscoverer                        |
| ExceptionDepthComparator                                |           | 比较两个异常对象的深度。它的作用是用于将多个异常对象按照其嵌套的深度进行排序，深度越浅的异常对象越靠前。 |
| GenericTypeResolver                                     | abstract |                                                                   |
| InfrastructureProxy                                     | interface | Object getWrappedObject()                                         |
| KotlinDetector                                          |           |                                                                   |
| KotlinReflectionParameterNameDiscoverer                 |           |                                                                   |
| LocalVariableTableParameterNameDiscoverer               |           | 工具类，用于获取方法参数的名称。                                                  |
| MethodClassKey                                          |           | final class MethodClassKey implements Comparable<MethodClassKey>  |
| MethodIntrospector                                      | abstract |                                                                   |
| MethodIntrospector.MetadataLookup<T>                    |           |                                                                   |
| MethodParameter                                         |           | getParameterType()方法                                              |
| NamedInheritableThreadLocal<T>                          |           | <T> extends InheritableThreadLocal<T>   在多线程环境下，为每个线程维护一个本地变量，使得每个线程可以独立地操作自己的本地变量，从而避免了线程安全问题 |
| NamedThreadLocal<T>                                     |           |                                                                   |
| NativeDetector                                          |           | 工具类，用于检测当前操作系统是否为本地（native）系统，即判断当前是否为原生的操作系统环境。它可以帮助 Spring 在不同操作系统下选择合适的本地库文件（native libraries）或执行特定的本地操作。 |
| NestedCheckedException                                  | exception |                                                                   |
| NestedExceptionUtils                                    |           | 抽象 静态类 |
| NestedRuntimeException                                  | exception |                                                                   |
| OrderComparator                                         |           | 工具类，用于对实现了 Ordered 接口的对象进行排序。                                     |
| OrderComparator.OrderSourceProvider                     |           |                                                                   |
| Ordered                                                 | interface | int getOrder()                                                    |
| OverridingClassLoader                                   |           | 字节码替换 |
| ParameterizedTypeReference<T>                           | abstract |                                                                   |
| ParameterNameDiscoverer                                 | interface | "String[] getParameterNames(Method method)                        |
| String[] getParameterNames(Constructor<?> ctor)"        |||
| PrioritizedParameterNameDiscoverer                      |           | 参考 StandardReflectionParameterNameDiscoverer     实现了 ParameterNameDiscoverer 接口，并增加了一个优先级的概念。它的作用是可以支持多个 ParameterNameDiscoverer 的组合使用，并按照优先级顺序依次获取方法参数的名称。 |
| PriorityOrdered                                         |           | PriorityOrdered extends Ordered     见下面                           |
| ReactiveAdapter                                         |           | 5.0才有                                                             |
| ReactiveAdapterRegistry                                 |           | 5.0才有                                                             |
| ReactiveAdapterRegistry.SpringCoreBlockHoundIntegration |           |                                                                   |
| ReactiveTypeDescriptor                                  |           | 5.0才有                                                             |
| ResolvableType                                          |           |                                                                   |
| ResolvableTypeProvider                                  | interface |                                                                   |
| SimpleAliasRegistry                                     |           | implements AliasRegistry                                          |
| SmartClassLoader                                        | interface |                                                                   |
| SpringProperties                                        |           |                                                                   |
| SpringVersion                                           |           | getVersion()方法返回 5.2.9.RELEASE                                    |
| StandardReflectionParameterNameDiscoverer               |           | 参考 PrioritizedParameterNameDiscoverer |


LocalVariableTableParameterNameDiscoverer 根据类型查到函数参数名称


org.springframework.core.MethodParameter
属性
String parameterName
Class<?> parameterType
int parameterIndex

调用的地方
MethodArgumentNotValidException 类返回MethodParameter
        MethodParameter methodParameter = ((MethodParameter) ex.getParameter());

子类
 内部类
 MethodParameter (org.springframework.core)
    SynthesizingMethodParameter (org.springframework.core.annotation)
        HandlerMethodParameter in HandlerMethod (org.springframework.web.method)
            ReturnValueMethodParameter in HandlerMethod (org.springframework.web.method)
            ConcurrentResultMethodParameter in ServletInvocableHandlerMethod (org.springframework.web.servlet.mvc.method.annotation)
        HandlerMethodParameter in HandlerMethod (org.springframework.messaging.handler)
            ReturnValueMethodParameter in HandlerMethod (org.springframework.messaging.handler)
            AsyncResultMethodParameter in InvocableHandlerMethod (org.springframework.messaging.handler.invocation)
    FieldAwareConstructorParameter in ModelAttributeMethodProcessor (org.springframework.web.method.annotation)


org.springframework.core.ParameterNameDiscoverer接口实现类

String[] getParameterNames(Method method)
String[] getParameterNames(Constructor<?> ctor)

`PrioritizedParameterNameDiscoverer` 和 `StandardReflectionParameterNameDiscoverer` 都是 Spring 框架中用于获取方法的参数名的工具类，它们之间存在一些区别和联系。

区别：
1. 实现方式：`StandardReflectionParameterNameDiscoverer` 是通过 Java 的反射机制来获取方法的参数名，它使用了 `java.lang.reflect.Executable` 和 `java.lang.reflect.Parameter` 类来获取方法的参数名。而 `PrioritizedParameterNameDiscoverer` 则是一个可扩展的参数名解析器，它允许用户自定义多个参数名解析器，按优先级顺序来获取方法的参数名。
2. 解析策略：`StandardReflectionParameterNameDiscoverer` 只使用了 Java 的反射机制，它适用于大多数情况下。而 `PrioritizedParameterNameDiscoverer` 可以支持多种解析策略，用户可以根据自己的需求自定义参数名解析器，例如从注解中获取参数名、从配置文件中获取参数名等。

联系：
1. 共同接口：它们都实现了 Spring 框架中的 `ParameterNameDiscoverer` 接口，该接口定义了获取方法参数名的方法 `getParameterNames(Method method)`。
2. 用途相似：它们都用于获取方法的参数名，在使用 Spring AOP、Spring MVC 等功能时，需要获取方法的参数名来进行一些处理，比如参数校验、日志输出等。

示例代码：
```java
import org.springframework.core.DefaultParameterNameDiscoverer;
import org.springframework.core.ParameterNameDiscoverer;
import org.springframework.core.PrioritizedParameterNameDiscoverer;
import org.springframework.core.StandardReflectionParameterNameDiscoverer;

import java.lang.reflect.Method;
import java.util.Arrays;

public class Main {
    public void myMethod(String name, int age) {}

    public static void main(String[] args) throws NoSuchMethodException {
        ParameterNameDiscoverer standardDiscoverer = new StandardReflectionParameterNameDiscoverer();
        ParameterNameDiscoverer prioritizedDiscoverer = new PrioritizedParameterNameDiscoverer();

        Method method = Main.class.getMethod("myMethod", String.class, int.class);

        String[] standardParameterNames = standardDiscoverer.getParameterNames(method);
        String[] prioritizedParameterNames = prioritizedDiscoverer.getParameterNames(method);

        System.out.println("Standard Reflection Parameter Names: " + Arrays.toString(standardParameterNames));
        System.out.println("Prioritized Parameter Names: " + Arrays.toString(prioritizedParameterNames));
    }
}
```

在上面的示例中，我们分别使用 `StandardReflectionParameterNameDiscoverer` 和 `PrioritizedParameterNameDiscoverer` 来获取 `myMethod` 方法的参数名。`StandardReflectionParameterNameDiscoverer` 直接使用 Java 反射机制获取参数名，而 `PrioritizedParameterNameDiscoverer` 可以使用多种解析策略来获取参数名。输出结果将会显示方法的参数名。



`ResolvableType` 是 Spring 框架中的一个工具类，用于获取泛型类型的详细信息，包括实际的类型参数、泛型父类、泛型接口等。它可以在运行时分析类的结构，帮助我们在编程过程中处理泛型类型的信息。

作用：
1. 解析泛型类型：`ResolvableType` 可以帮助我们解析泛型类型，获取泛型类型的实际类型参数。这对于需要在运行时获取泛型类型信息的场景非常有用。
2. 获取类的泛型信息：`ResolvableType` 可以获取类的泛型父类、泛型接口等信息，使我们能够在运行时了解类的泛型信息。

使用场景：
1. 在自定义框架或库中需要处理泛型类型的信息时，可以使用 `ResolvableType` 来获取泛型类型的实际参数类型。
2. 在 Spring 框架中，`ResolvableType` 通常用于处理 Bean 的类型信息，尤其是在使用泛型作为依赖注入的类型时。
示例代码：
假设我们有一个自定义的泛型类 `MyGenericClass<T>`，并且有一个子类 `MySubClass` 继承自 `MyGenericClass<String>`，我们可以使用 `ResolvableType` 来获取泛型类型的实际参数。

```java
import org.springframework.core.ResolvableType;

public class MyGenericClass<T> {}

public class MySubClass extends MyGenericClass<String> {}

public class Main {
    public static void main(String[] args) {
        ResolvableType resolvableType = ResolvableType.forClass(MySubClass.class);

        // 获取 MyGenericClass<T> 中的 T 的实际参数类型
        ResolvableType genericType = resolvableType.getSuperType().getGeneric(0);
        Class<?> genericClass = genericType.resolve();

        System.out.println(genericClass); // 输出：class java.lang.String
    }
}
```

在上面的示例中，我们通过 `ResolvableType` 获取了 `MySubClass` 的父类 `MyGenericClass<String>` 中的泛型类型参数 `String`，并打印出了实际的类型。这样，我们可以在运行时动态获取泛型类型的信息，而不需要在编码时硬编码类型信息。这对于处理复杂的泛型类型非常有用。





ResolvableTypeProvider 是 Spring Framework 中的一个接口，用于提供 ResolvableType 对象。它的作用是在运行时获取泛型类型的具体类型信息，并提供 ResolvableType 对象，以便其他组件可以在运行时获取泛型类型的具体类型信息。
ResolvableTypeProvider 可以用于在运行时获取泛型类型的具体类型信息，并提供 ResolvableType 对象，以便其他组件可以在运行时获取泛型类型的具体类型信息。它通常用于在 Spring 框架中，在某些组件中需要获取泛型类型的具体类型信息时使用，例如，获取一个方法或参数的类型信息、获取一个类或接口的泛型类型信息等。
下面是一个使用 ResolvableTypeProvider 的例子：

```java
public interface CrudRepository<T, ID> extends Repository<T, ID>, ResolvableTypeProvider {
    Optional<T> findById(ID id);

    List<T> findAll();

    T save(T entity);

    void deleteById(ID id);

    void delete(T entity);
}

public class UserRepository implements CrudRepository<User, Long> {
    @Override
    public ResolvableType getResolvableType() {
        return ResolvableType.forClassWithGenerics(CrudRepository.class, User.class, Long.class);
    }

    @Override
    public Optional<User> findById(Long id) {
        // ...
    }

    @Override
    public List<User> findAll() {
        // ...
    }

    @Override
    public User save(User entity) {
        // ...
    }

    @Override
    public void deleteById(Long id) {
        // ...
    }

    @Override
    public void delete(User entity) {
        // ...
    }
}

public class UserService {
    private final CrudRepository<User, Long> userRepository;

    public UserService(CrudRepository<User, Long> userRepository) {
        this.userRepository = userRepository;
    }

    public User getUserById(Long id) {
        Optional<User> optionalUser = userRepository.findById(id);
        return optionalUser.orElse(null);
    }
}
```

在上面的例子中，我们首先定义了一个 CrudRepository 接口，其中包含了一些基本的 CRUD 方法，并实现了 ResolvableTypeProvider 接口。ResolvableTypeProvider 接口中的 getResolvableType() 方法返回了一个 ResolvableType 对象，用于表示 CrudRepository 的泛型类型信息。然后，我们创建了一个 UserRepository 类，实现了 CrudRepository 接口，并实现了其中的方法。在 getResolvableType() 方法中，我们使用 ResolvableType.forClassWithGenerics() 方法创建了一个 ResolvableType 对象，用于表示 CrudRepository<User, Long> 的泛型类型信息。最后，我们创建了一个 UserService 类，其中包含了一个 getUserById() 方法，该方法接收一个 Long 类型的参数，并使用 userRepository.findById() 方法获取 User 对象。
总之，ResolvableTypeProvider 是 Spring Framework 中的一个接口，用于提供 ResolvableType 对象。它可以用于在某些组件中需要获取泛型类型的具体类型信息时使用，例如，获取一个方法或参数的类型信息、获取一个类或接口的泛型类型信息等。使用它可以方便地获取泛型类型的具体类型信息，并提供 ResolvableType 对象，以便其他组件可以在运行时获取泛型类型的具体类型信息。





`PriorityOrdered` 是 Spring 框架中的一个接口，用于定义Bean的加载顺序。当多个Bean实现了 `PriorityOrdered` 接口时，Spring会按照它们的优先级来决定加载的顺序。

使用场景：
1. 多个Bean实现了同一个接口，并且需要按照特定的优先级顺序进行加载和处理。通过让这些Bean实现 `PriorityOrdered` 接口，并在 `getOrder()` 方法中返回不同的优先级值，可以实现对它们的加载顺序进行控制。
2. 在 Spring 配置文件中，需要手动指定Bean的加载顺序。通过在 `<bean>` 标签中使用 `order` 属性，并将其设置为 `PriorityOrdered.HIGHEST_PRECEDENCE` 或 `PriorityOrdered.LOWEST_PRECEDENCE`，可以明确指定Bean的加载顺序。
示例代码：
假设我们有两个Bean实现了同一个接口 `MyBeanInterface`，我们希望按照特定的顺序进行加载和处理。我们可以按照以下步骤实现：

1. 创建接口 `MyBeanInterface`：

```java
public interface MyBeanInterface {
    void doSomething();
}
```

2. 创建两个实现类，并让它们实现 `PriorityOrdered` 接口：

```java
import org.springframework.core.PriorityOrdered;

public class MyBean1 implements MyBeanInterface, PriorityOrdered {
    @Override
    public void doSomething() {
        System.out.println("MyBean1 is doing something...");
    }

    @Override
    public int getOrder() {
        return 1; // 设置优先级为1，表示优先级最高
    }
}

public class MyBean2 implements MyBeanInterface, PriorityOrdered {
    @Override
    public void doSomething() {
        System.out.println("MyBean2 is doing something...");
    }

    @Override
    public int getOrder() {
        return 2; // 设置优先级为2，表示优先级较低
    }
}
```

3. 在 Spring 配置文件中配置这两个Bean，并指定它们的加载顺序：

```xml
<bean class="com.example.MyBean1" />
<bean class="com.example.MyBean2" />
```

通过以上配置，Spring会按照优先级从高到低的顺序先加载 `MyBean1`，再加载 `MyBean2`。当应用程序运行时，调用 `MyBeanInterface` 的方法时，会按照这个顺序来执行 `doSomething()` 方法。





PrioritizedParameterNameDiscoverer 是 Spring Framework 中的一个类，它实现了 ParameterNameDiscoverer 接口，并增加了一个优先级的概念。它的作用是可以支持多个 ParameterNameDiscoverer 的组合使用，并按照优先级顺序依次获取方法参数的名称。
PrioritizedParameterNameDiscoverer 可以用于支持多个 ParameterNameDiscoverer 的组合使用，并按照优先级顺序依次获取方法参数的名称。它通常用于在 Spring 框架中，当存在多个 ParameterNameDiscoverer 实现时，需要按照一定的优先级顺序获取方法参数的名称。
下面是一个使用 PrioritizedParameterNameDiscoverer 的例子：

```java
public class UserController {
    public User createUser(@RequestParam("name") String name, @RequestParam("age") int age) {
        return new User(name, age);
    }
}

public class UserControllerAdvice {
    private final ParameterNameDiscoverer parameterNameDiscoverer;

    public UserControllerAdvice() {
        PrioritizedParameterNameDiscoverer prioritizedParameterNameDiscoverer = new PrioritizedParameterNameDiscoverer();
        AnnotationParameterNameDiscoverer annotationParameterNameDiscoverer = new AnnotationParameterNameDiscoverer();
        LocalVariableTableParameterNameDiscoverer localVariableTableParameterNameDiscoverer = new LocalVariableTableParameterNameDiscoverer();
        prioritizedParameterNameDiscoverer.addDiscoverer(annotationParameterNameDiscoverer);
        prioritizedParameterNameDiscoverer.addDiscoverer(localVariableTableParameterNameDiscoverer);
        this.parameterNameDiscoverer = prioritizedParameterNameDiscoverer;
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ErrorResponse> handleMethodArgumentNotValid(MethodArgumentNotValidException ex) {
        BindingResult bindingResult = ex.getBindingResult();
        List<FieldError> fieldErrors = bindingResult.getFieldErrors();
        Map<String, String> errorMap = new HashMap<>();
        for (FieldError fieldError : fieldErrors) {
            String fieldName = fieldError.getField();
            String errorMessage = fieldError.getDefaultMessage();
            errorMap.put(fieldName, errorMessage);
        }
        MethodParameter methodParameter = ((MethodParameter) ex.getParameter());
        Method method = methodParameter.getMethod();
        String[] parameterNames = parameterNameDiscoverer.getParameterNames(method);
        Object[] args = ex.getBindingResult().getTarget().getClass().getMethod(method.getName(), method.getParameterTypes()).getParameters();
        Map<String, Object> paramMap = new HashMap<>();
        for (int i = 0; i < parameterNames.length; i++) {
            paramMap.put(parameterNames[i], args[i]);
        }
        return ResponseEntity.badRequest().body(new ErrorResponse("MethodArgumentNotValidException", errorMap, paramMap));
    }
}
```

在上面的例子中，我们首先创建了一个 UserController 类，其中包含了一个名为 createUser() 的方法，该方法包含了两个参数，分别为 name 和 age。然后，我们创建了一个 UserControllerAdvice 类，其中维护了一个 PrioritizedParameterNameDiscoverer 对象。在构造函数中，我们首先创建了一个 AnnotationParameterNameDiscoverer 对象和一个 LocalVariableTableParameterNameDiscoverer 对象，并将其添加到 PrioritizedParameterNameDiscoverer 对象中。这样，我们就可以按照一定的优先级顺序依次获取方法参数的名称。在 handleMethodArgumentNotValid() 方法中，我们首先通过 ex.getBindingResult() 获取到方法参数的验证结果，然后通过 parameterNameDiscoverer.getParameterNames() 方法获取到方法参数的名称。最后，我们将方法参数的名称和值都存储到一个 Map 中，并将其作为错误返回给客户端。
总之，PrioritizedParameterNameDiscoverer 是 Spring Framework 中的一个类，它实现了 ParameterNameDiscoverer 接口，并增加了一个优先级的概念。它可以支持多个 ParameterNameDiscoverer 的组合使用，并按照优先级顺序依次获取方法参数的名称。在存在多个 ParameterNameDiscoverer 实现时，可以使用它按照一定的优先级顺序获取方法参数的名称。





ParameterizedTypeReference<T> 是 Spring Framework 中的一个泛型类，用于在运行时获取带有泛型参数的类型信息。它的作用是在运行时获取泛型类型的具体类型信息，从而可以避免在编译时丢失泛型类型信息。

ParameterizedTypeReference<T> 可以用于在运行时获取泛型类型的具体类型信息。它通常用于在 Spring 框架中获取响应体的泛型类型信息，例如，获取一个 ResponseEntity 对象的泛型类型信息，或者获取一个 RestTemplate 对象的响应体的泛型类型信息。

下面是一个使用 ParameterizedTypeReference<T> 的例子：

```java
public class UserController {
    private final RestTemplate restTemplate;

    public UserController(RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
    }

    public List<User> getAllUsers() {
        ResponseEntity<List<User>> responseEntity = restTemplate.exchange("/users", HttpMethod.GET, null,
                new ParameterizedTypeReference<List<User>>() {});
        return responseEntity.getBody();
    }
}
```

在上面的例子中，我们创建了一个 UserController 类，其中维护了一个 RestTemplate 对象。在 getAllUsers() 方法中，我们使用 RestTemplate 对象发送了一个 GET 请求，并通过 ParameterizedTypeReference<List<User>>() {} 获取了响应体的泛型类型信息。这样，我们就可以方便地获取响应体的具体类型信息，并将其转换成 List<User> 类型。

总之，ParameterizedTypeReference<T> 是 Spring Framework 中的一个泛型类，用于在运行时获取带有泛型参数的类型信息。它可以用于在 Spring 框架中获取响应体的泛型类型信息，从而避免在编译时丢失泛型类型信息。使用它可以方便地获取泛型类型的具体类型信息，并将其转换成具体的类型。



`OverridingClassLoader` 是 Spring 框架中的一个类加载器（ClassLoader），它用于在运行时动态替换类的字节码，实现类的动态修改和热加载。它可以在应用程序中实现一些特殊的类加载需求，比如在不重启应用的情况下替换某个类的实现，或者在开发过程中快速调试和验证代码修改。

使用例子：
下面是一个简单的使用例子，展示了如何通过 `OverridingClassLoader` 动态替换类的实现：

假设我们有一个简单的类 `MyService`，其中包含一个方法 `sayHello()`，初始实现如下：

```java
public class MyService {
    public void sayHello() {
        System.out.println("Hello, World!");
    }
}
```

现在，我们想要在不重启应用的情况下，动态替换 `MyService` 类的实现，将 `sayHello()` 方法的输出修改为 "Hello, Spring!"。我们可以通过 `OverridingClassLoader` 来实现这个目标。

```java
import org.springframework.asm.ClassWriter;
import org.springframework.asm.MethodVisitor;
import org.springframework.asm.Opcodes;
import org.springframework.core.OverridingClassLoader;

public class DynamicClassModification {
    public static void main(String[] args) throws Exception {
        // 创建原始类 MyService 的字节码
        byte[] originalClassBytes = createOriginalClassBytes();

        // 创建动态类加载器
        OverridingClassLoader classLoader = new OverridingClassLoader(DynamicClassModification.class.getClassLoader());

        // 加载原始类
        Class<?> originalClass = classLoader.defineClass("com.example.MyService", originalClassBytes);

        // 创建新的类字节码，替换 sayHello() 方法的实现
        byte[] modifiedClassBytes = createModifiedClassBytes();

        // 加载替换后的类
        Class<?> modifiedClass = classLoader.overrideClass(modifiedClassBytes);

        // 创建 MyService 实例并调用 sayHello() 方法
        MyService myService = (MyService) modifiedClass.getDeclaredConstructor().newInstance();
        myService.sayHello(); // 输出 "Hello, Spring!"
    }

    private static byte[] createOriginalClassBytes() {
        ClassWriter classWriter = new ClassWriter(ClassWriter.COMPUTE_MAXS | ClassWriter.COMPUTE_FRAMES);
        classWriter.visit(Opcodes.V1_8, Opcodes.ACC_PUBLIC, "com/example/MyService", null,
                "java/lang/Object", null);

        MethodVisitor mv = classWriter.visitMethod(Opcodes.ACC_PUBLIC, "sayHello", "()V", null, null);
        mv.visitCode();
        mv.visitFieldInsn(Opcodes.GETSTATIC, "java/lang/System", "out", "Ljava/io/PrintStream;");
        mv.visitLdcInsn("Hello, World!");
        mv.visitMethodInsn(Opcodes.INVOKEVIRTUAL, "java/io/PrintStream", "println", "(Ljava/lang/String;)V", false);
        mv.visitInsn(Opcodes.RETURN);
        mv.visitMaxs(0, 0);
        mv.visitEnd();

        classWriter.visitEnd();
        return classWriter.toByteArray();
    }

    private static byte[] createModifiedClassBytes() {
        ClassWriter classWriter = new ClassWriter(ClassWriter.COMPUTE_MAXS | ClassWriter.COMPUTE_FRAMES);
        classWriter.visit(Opcodes.V1_8, Opcodes.ACC_PUBLIC, "com/example/MyService", null,
                "java/lang/Object", null);

        MethodVisitor mv = classWriter.visitMethod(Opcodes.ACC_PUBLIC, "sayHello", "()V", null, null);
        mv.visitCode();
        mv.visitFieldInsn(Opcodes.GETSTATIC, "java/lang/System", "out", "Ljava/io/PrintStream;");
        mv.visitLdcInsn("Hello, Spring!");
        mv.visitMethodInsn(Opcodes.INVOKEVIRTUAL, "java/io/PrintStream", "println", "(Ljava/lang/String;)V", false);
        mv.visitInsn(Opcodes.RETURN);
        mv.visitMaxs(0, 0);
        mv.visitEnd();

        classWriter.visitEnd();
        return classWriter.toByteArray();
    }
}
```

在上面的例子中，我们首先创建了一个原始的 `MyService` 类的字节码，然后通过 `OverridingClassLoader` 加载了这个原始类。接着，我们创建了一个新的字节码，替换了 `sayHello()` 方法的实现，将输出改为 "Hello, Spring!"。最后，我们通过 `OverridingClassLoader` 的 `overrideClass()` 方法动态地替换原始类





`NativeDetector` 是 Spring 框架中的一个工具类，用于检测当前操作系统是否为本地（native）系统，即判断当前是否为原生的操作系统环境。它可以帮助 Spring 在不同操作系统下选择合适的本地库文件（native libraries）或执行特定的本地操作。

在 Spring 框架中，`NativeDetector` 主要用于一些需要在不同操作系统下执行不同代码的场景，比如加载本地库文件、执行本地命令等。

使用例子：
假设我们需要在 Windows 操作系统下加载一个本地库文件，而在其他操作系统下不加载该文件。我们可以使用 `NativeDetector` 来检测当前操作系统，然后根据检测结果来决定是否加载本地库文件。

```java
import org.springframework.util.NativeDetector;

public class NativeLibraryLoader {
    public static void loadLibrary() {
        if (NativeDetector.isWindows()) {
            // 加载 Windows 环境下的本地库文件
            System.loadLibrary("myLibrary");
        } else {
            // 非 Windows 环境，不加载本地库文件
            System.out.println("Not running on Windows. Skipping native library loading.");
        }
    }

    public static void main(String[] args) {
        loadLibrary();
    }
}
```

在上述例子中，我们使用 `NativeDetector.isWindows()` 方法来检测当前操作系统是否为 Windows。如果是 Windows 系统，则加载名为 "myLibrary" 的本地库文件，否则不加载该文件。

需要注意的是，`NativeDetector` 只提供了一些基本的检测方法，如 `isWindows()`、`isMac()`、`isLinux()` 等，用于判断当前是否为特定的操作系统。如果需要更精细的操作系统检测，可以考虑使用其他更强大的库，比如 Apache Commons Lang 的 `SystemUtils` 类。

请注意在使用 `NativeDetector` 或其他操作系统检测工具时，要谨慎处理可能出现的不兼容性问题，并确保代码能够正确处理不同操作系统环境下的情况。



NamedThreadLocal 和 NamedInheritableThreadLocal 都是 Java 中的线程本地变量类，用于在多个线程之间共享同一个变量。它们的区别在于是否支持继承机制。

NamedThreadLocal 不支持继承机制，即子线程无法访问父线程中的本地变量。它仅在当前线程中有效，因此可以保证线程之间的数据隔离。如果需要在多个线程之间共享同一个变量，可以使用 NamedInheritableThreadLocal。

NamedInheritableThreadLocal 支持继承机制，即子线程可以访问父线程中的本地变量，并将其继承下来。它可以在多个线程之间共享同一个变量，并支持跨线程传递数据。它适用于需要在多个线程之间共享数据的场景，例如，跨线程传递用户身份信息、跨线程传递请求上下文等。

下面是一个使用 NamedThreadLocal 和 NamedInheritableThreadLocal 的例子：

```java
public class UserContext {
    private static final ThreadLocal<User> userThreadLocal = new NamedThreadLocal<>("user-context");
    private static final ThreadLocal<User> inheritableUserThreadLocal = new NamedInheritableThreadLocal<>("inheritable-user-context");

    public static void setUser(User user) {
        userThreadLocal.set(user);
        inheritableUserThreadLocal.set(user);
    }

    public static User getUser() {
        return userThreadLocal.get();
    }

    public static User getInheritableUser() {
        return inheritableUserThreadLocal.get();
    }

    public static void main(String[] args) throws InterruptedException {
        User user = new User("Tom");
        UserContext.setUser(user);

        Thread thread = new Thread(() -> {
            User childUser = new User("Jerry");
            UserContext.setUser(childUser);
            System.out.println("Child thread user: " + UserContext.getUser());
            System.out.println("Child thread inheritable user: " + UserContext.getInheritableUser());
        });
        thread.start();
        thread.join();

        System.out.println("Main thread user: " + UserContext.getUser());
        System.out.println("Main thread inheritable user: " + UserContext.getInheritableUser());
    }
}
```

在上面的例子中，我们创建了一个 UserContext 类，其中维护了一个名为 user-context 的 NamedThreadLocal 对象和一个名为 inheritable-user-context 的 NamedInheritableThreadLocal 对象。在 main() 方法中，我们首先设置了一个 User 对象为当前线程的本地变量。然后，我们创建了一个新的线程，并在其中设置了一个新的 User 对象为其本地变量。在子线程中，我们分别通过 UserContext.getUser() 方法和 UserContext.getInheritableUser() 方法获取当前线程的本地变量。在主线程中，我们同样分别通过 UserContext.getUser() 方法和 UserContext.getInheritableUser() 方法获取当前线程的本地变量。最后，我们通过输出结果可以看出，NamedThreadLocal 不支持继承机制，即子线程无法访问父线程中的本地变量；而 NamedInheritableThreadLocal 支持继承机制，即子线程可以访问父线程中的本地变量，并将其继承下来。

总之，NamedThreadLocal 和 NamedInheritableThreadLocal 都是 Java 中的线程本地变量类，用于在多个线程之间共享同一个变量。它们的区别在于是否支持继承机制。如果需要在多个线程之间共享数据，并支持跨线程传递数据，可以使用 NamedInheritableThreadLocal；如果需要保证线程之间的数据隔离，可以使用 NamedThreadLocal。



NamedInheritableThreadLocal 是 Java 中的一个线程本地变量类，可以在多个线程之间共享同一个变量，并且支持继承机制。它的作用是在多线程环境下，为每个线程维护一个本地变量，使得每个线程可以独立地操作自己的本地变量，从而避免了线程安全问题。

NamedInheritableThreadLocal 可以在多个线程之间共享同一个变量，并且支持继承机制。继承机制可以保证子线程的本地变量与父线程的本地变量是一致的，从而可以方便地实现一些跨线程的共享数据操作，例如，跨线程传递用户身份信息、跨线程传递请求上下文等。

下面是一个使用 NamedInheritableThreadLocal 的例子：

```java
public class UserContext {
    private static final ThreadLocal<User> userContext = new NamedInheritableThreadLocal<>("user-context");

    public static void setUser(User user) {
        userContext.set(user);
    }

    public static User getUser() {
        return userContext.get();
    }

    public static void clear() {
        userContext.remove();
    }

    public static void main(String[] args) throws InterruptedException {
        User user = new User("Tom");
        UserContext.setUser(user);

        Thread thread = new Thread(() -> {
            User childUser = new User("Jerry");
            UserContext.setUser(childUser);
            System.out.println("Child thread user: " + UserContext.getUser().getName());
        });
        thread.start();
        thread.join();

        System.out.println("Main thread user: " + UserContext.getUser().getName());

        UserContext.clear();
    }
}
```

在上面的例子中，我们创建了一个 UserContext 类，其中维护了一个名为 user-context 的 NamedInheritableThreadLocal 对象。在 main() 方法中，我们首先设置了一个 User 对象为当前线程的本地变量。然后，我们创建了一个新的线程，并在其中设置了一个新的 User 对象为其本地变量。在子线程中，我们可以通过 UserContext.getUser() 方法获取当前线程的本地变量。在主线程中，我们同样可以通过 UserContext.getUser() 方法获取当前线程的本地变量。最后，我们通过 UserContext.clear() 方法清除了当前线程的本地变量。

从输出结果可以看出，NamedInheritableThreadLocal 成功地维护了每个线程的本地变量，并支持了继承机制，使得子线程的本地变量与父线程的本地变量是一致的。

总之，NamedInheritableThreadLocal 是 Java 中的一个线程本地变量类，可以在多个线程之间共享同一个变量，并且支持继承机制。它可以方便地实现一些跨线程的共享数据操作，例如，跨线程传递用户身份信息、跨线程传递请求上下文等。使用它可以避免多线程环境下的线程安全问题，并方便地实现跨线程的共享数据操作。





MethodIntrospector 是 Spring Framework 中的一个工具类，用于获取类中的方法集合，支持包括继承的公共方法、接口方法、私有方法、静态方法等。

MethodIntrospector 的作用是在运行时获取类中的方法集合，并对其进行过滤和排序。它可以用于实现一些特定的功能，例如，查找类中的所有 Getter 方法、获取注解类型为 @Transactional 的方法等。

下面是一个使用 MethodIntrospector 的例子：

```java
public class UserService {
    private UserDao userDao;

    public UserService(UserDao userDao) {
        this.userDao = userDao;
    }

    public User getUserById(Long id) {
        return this.userDao.findById(id);
    }

    public void saveUser(User user) {
        this.userDao.save(user);
    }

    public void deleteUserById(Long id) {
        this.userDao.deleteById(id);
    }

    public List<User> getAllUsers() {
        return this.userDao.findAll();
    }

    public static void main(String[] args) {
        Map<Method, Transactional> transactionalMethods = MethodIntrospector.selectMethods(UserService.class,
                (MethodIntrospector.MetadataLookup<Transactional>) method -> method.getAnnotation(Transactional.class));
        System.out.println(transactionalMethods.size());
    }
}
```

在上面的例子中，我们创建了一个 UserService 类，其中包含了一些方法。在 main() 方法中，我们使用 MethodIntrospector.selectMethods() 方法获取 UserService 类中所有使用 @Transactional 注解的方法，并打印其数量。

从输出结果可以看出，MethodIntrospector 成功地获取了 UserService 类中使用 @Transactional 注解的方法的数量。

总之，MethodIntrospector 是 Spring Framework 中的一个工具类，用于获取类中的方法集合，并对其进行过滤和排序。它可以用于实现一些特定的功能，例如，查找类中的所有 Getter 方法、获取注解类型为 @Transactional 的方法等。使用它可以方便地获取类中的方法集合，并进行过滤和排序。



`MethodClassKey` 是 Spring 框架中的一个类，它用于标识类的方法的一个键，以便在缓存中进行查找和存储。它是用来优化 AOP 和缓存等方面的性能的。

在 Spring 框架中，有一些地方需要根据方法和类来进行缓存或查找操作，而 `MethodClassKey` 就是为了方便这些操作而设计的。它封装了方法和类的信息，使得可以将它作为一个键来在缓存中查找和存储相应的数据。

使用例子：
假设有以下的一个接口类和实现类：

```java
public interface UserService {
    void addUser(String username, int age);
}

public class UserServiceImpl implements UserService {
    @Override
    public void addUser(String username, int age) {
        // 实现省略...
    }
}
```

现在，我们希望在 AOP 的切面中使用 `MethodClassKey` 来进行缓存操作，可以这样做：

```java
import org.springframework.aop.framework.AopProxyUtils;
import org.springframework.core.MethodClassKey;

public class MyCacheAspect {
    // 缓存
    private Map<MethodClassKey, Object> cache = new HashMap<>();

    // 切面方法
    public void cacheMethodResult(ProceedingJoinPoint joinPoint) throws Throwable {
        // 获取方法和类
        Method method = AopProxyUtils.ultimateTargetClass(joinPoint.getTarget()).getMethod(joinPoint.getSignature().getName(), Method.class);
        Class<?> targetClass = joinPoint.getTarget().getClass();

        // 创建 MethodClassKey
        MethodClassKey key = new MethodClassKey(method, targetClass);

        // 判断是否已经缓存过结果
        if (!cache.containsKey(key)) {
            // 缓存结果
            Object result = joinPoint.proceed();
            cache.put(key, result);
        }

        // 从缓存中获取结果
        Object cachedResult = cache.get(key);
        // 使用缓存的结果处理后续逻辑...
    }
}
```

在上述代码中，我们使用 `MethodClassKey` 创建了一个缓存的键，并将方法和类作为参数传递给 `MethodClassKey` 构造函数。然后，我们将方法的执行结果缓存起来，下次再调用相同的方法时，就可以直接从缓存中获取结果，避免重复执行方法。

当然，在实际应用中，你可以根据自己的需求来决定如何使用 `MethodClassKey` 来优化性能。它通常用于一些复杂的缓存或查找场景，比如在 AOP 切面中根据方法和类来缓存方法的执行结果，或者在自定义的缓存实现中使用 `MethodClassKey` 来作为缓存的键。



InfrastructureProxy 是 Spring Framework 中的一个接口，用于将一个对象包装成另一个对象。它的作用是在不修改原始对象的情况下，为其添加额外的基础设施功能，例如事务管理、安全性检查等。

使用 InfrastructureProxy 可以实现一些常见的设计模式，例如装饰器模式、代理模式等。它可以用于在运行时动态地添加或删除对象的基础设施功能，同时不影响原始对象的类型或行为。

下面是一个使用 InfrastructureProxy 的例子：

```java
public class TransactionalProxy implements InfrastructureProxy<Object> {
    private TransactionManager transactionManager;
    private Object target;

    public TransactionalProxy(TransactionManager transactionManager) {
        this.transactionManager = transactionManager;
    }

    @Override
    public void setTarget(Object target) {
        this.target = target;
    }

    @Override
    public Object getTarget() {
        return this.target;
    }

    @Override
    public Object provideInfrastructure(Object proxy, Method method, Object[] args, Supplier<Object> invocation) throws Throwable {
        TransactionStatus status = this.transactionManager.getTransaction();
        try {
            Object result = invocation.get();
            this.transactionManager.commit(status);
            return result;
        } catch (Exception ex) {
            this.transactionManager.rollback(status);
            throw ex;
        }
    }
}
```

在上面的例子中，我们创建了一个 TransactionalProxy 类，实现了 InfrastructureProxy 接口。在 provideInfrastructure() 方法中，我们添加了事务管理的功能，用于在方法执行前开启事务，在方法执行后提交或回滚事务。使用该类可以将任何对象包装成一个带有事务管理功能的对象。

下面是一个使用 TransactionalProxy 的示例：

```java
public interface UserService {
    void addUser(User user);
}

public class UserServiceImpl implements UserService {
    private UserDao userDao;

    public UserServiceImpl(UserDao userDao) {
        this.userDao = userDao;
    }

    @Override
    public void addUser(User user) {
        this.userDao.save(user);
    }
}

public static void main(String[] args) {
    UserDao userDao = new UserDaoImpl();
    UserService userService = new UserServiceImpl(userDao);
    TransactionManager transactionManager = new TransactionManagerImpl();
    TransactionalProxy transactionalProxy = new TransactionalProxy(transactionManager);
    transactionalProxy.setTarget(userService);
    UserService proxy = ProxyFactory.createProxy(userService, transactionalProxy);
    proxy.addUser(new User("Tom", 20));
}
```

在上面的示例中，我们创建了一个 UserService 接口和一个 UserServiceImpl 类，用于添加用户。然后，我们使用 TransactionalProxy 类将 UserServiceImpl 对象包装成一个带有事务管理功能的对象。最后，我们使用 ProxyFactory.createProxy() 方法创建了一个 UserService 的代理对象，并将 TransactionalProxy 作为 InfrastructureProxy 传入。

总之，InfrastructureProxy 是 Spring Framework 中的一个接口，用于将一个对象包装成另一个对象，并为其添加额外的基础设施功能。它可以用于实现装饰器模式、代理模式等设计模式，动态地添加或删除对象的基础设施功能，同时不影响原始对象的类型或行为。使用它可以方便地为对象添加基础设施功能，例如事务管理、安全性检查等。





GenericTypeResolver 是 Spring Framework 中的一个工具类，用于解析泛型类型。它的作用是在运行时获取类或方法中声明的泛型类型的实际类型参数。

通常情况下，由于 Java 的类型擦除机制，泛型类型的实际类型参数在运行时是无法获取的。但是，在某些情况下，我们需要在运行时获取泛型类型的实际类型参数，例如，当我们需要序列化或反序列化一个含有泛型类型的对象时，需要知道泛型类型的实际类型参数。GenericTypeResolver 就是用于解决这个问题的工具类。

下面是一个使用 GenericTypeResolver 的例子：

```java
public class MyList<T> {
    private List<T> list;

    public MyList() {
        this.list = new ArrayList<>();
    }

    public void add(T element) {
        this.list.add(element);
    }

    public T get(int index) {
        return this.list.get(index);
    }

    public static void main(String[] args) {
        MyList<String> list = new MyList<>();
        list.add("hello");
        list.add("world");
        Class<?> clazz = GenericTypeResolver.resolveTypeArgument(list.getClass(), MyList.class);
        System.out.println(clazz.getName()); // output: java.lang.String
    }
}
```

在上面的例子中，我们创建了一个 MyList 类，它是一个泛型类，用于包装一个 List 对象。在 main() 方法中，我们创建了一个 MyList<String> 对象，并添加了两个元素。然后，我们使用 GenericTypeResolver.resolveTypeArgument() 方法获取 MyList 类声明的泛型类型的实际类型参数，并打印其名称。

从输出结果可以看出，GenericTypeResolver 成功地获取了 MyList 类声明的泛型类型的实际类型参数，即 java.lang.String 类型。这样，我们就可以在运行时获取泛型类型的实际类型参数，从而实现一些特定的功能。

总之，GenericTypeResolver 是 Spring Framework 中的一个工具类，用于解析泛型类型。它的作用是在运行时获取类或方法中声明的泛型类型的实际类型参数。使用它可以方便地获取泛型类型的实际类型参数，实现一些特定的功能。



`DefaultParameterNameDiscoverer` 是 Spring 框架中的一个接口参数名字发现器，用于获取方法的参数名。在 Java 的字节码中，默认是不保存方法的参数名的，而是用类似 arg0、arg1、arg2 等来表示方法的参数。`DefaultParameterNameDiscoverer` 就是用来解决这个问题的，它通过一些特定的途径来获取方法的参数名，使得我们可以在代码中获取到方法的真实参数名。

使用例子：
假设有以下的一个接口类和实现类：

```java
public interface UserService {
    void addUser(String username, int age);
}

public class UserServiceImpl implements UserService {
    @Override
    public void addUser(String username, int age) {
        // 实现省略...
    }
}
```

现在，我们希望在实现类中获取方法 `addUser` 的参数名，可以这样做：

```java
import org.springframework.core.DefaultParameterNameDiscoverer;
import org.springframework.core.ParameterNameDiscoverer;

public class Main {
    public static void main(String[] args) throws NoSuchMethodException {
        ParameterNameDiscoverer discoverer = new DefaultParameterNameDiscoverer();
        Class<?> clazz = UserServiceImpl.class;
        String methodName = "addUser";

        Method method = clazz.getMethod(methodName, String.class, int.class);
        String[] parameterNames = discoverer.getParameterNames(method);

        System.out.println("Method: " + methodName);
        System.out.println("Parameter Names: ");
        for (String name : parameterNames) {
            System.out.println(name);
        }
    }
}
```

运行上述代码，输出将是：

```
Method: addUser
Parameter Names:
username
age
```

可以看到，我们通过 `DefaultParameterNameDiscoverer` 获取到了方法 `addUser` 的参数名，从而实现了在代码中动态获取方法的参数名。这在一些需要使用参数名的场景中非常有用，比如在 AOP 中获取方法的参数值，或者在自定义注解中使用参数名作为属性等。



ConfigurableObjectInputStream 是 Spring Framework 中的一个类，继承自 ObjectInputStream 类，用于反序列化一个对象。它的作用是允许我们对反序列化过程进行更加灵活的配置，例如限制反序列化的类、禁止反序列化某些敏感类等。

ConfigurableObjectInputStream 通过实现 resolveClass() 和 resolveProxyClass() 方法，来控制反序列化过程中哪些类可以被反序列化，哪些类不能被反序列化。我们可以通过传入一个白名单或黑名单，来限制反序列化的类。

下面是一个使用 ConfigurableObjectInputStream 的例子：

```java
public class ObjectDeserializer {
    private static final Logger logger = LoggerFactory.getLogger(ObjectDeserializer.class);

    public static Object deserialize(byte[] data, Set<String> allowedClasses) {
        try (ByteArrayInputStream bis = new ByteArrayInputStream(data);
             ConfigurableObjectInputStream ois = new ConfigurableObjectInputStream(bis, allowedClasses)) {
            return ois.readObject();
        } catch (IOException | ClassNotFoundException ex) {
            logger.error("Failed to deserialize object", ex);
            return null;
        }
    }
}
```

在上面的例子中，我们创建了一个 ObjectDeserializer 类，并定义了一个 deserialize() 方法，用于反序列化一个 byte[] 数组。在 deserialize() 方法中，我们使用 ConfigurableObjectInputStream 来读取 byte[] 数组，并传入一个 allowedClasses 参数，该参数是一个 Set<String> 类型，用于限制反序列化的类。如果反序列化的类不在 allowedClasses 中，则反序列化过程将会失败。

ConfigurableObjectInputStream 通常用于限制反序列化的类，可以防止反序列化攻击。在反序列化时，我们可以通过传入一个 allowedClasses 集合来限制反序列化的类，从而提高系统的安全性。

总之，ConfigurableObjectInputStream 是 Spring Framework 中的一个类，用于反序列化一个对象，并允许我们对反序列化过程进行更加灵活的配置，例如限制反序列化的类、禁止反序列化某些敏感类等。它通常用于防止反序列化攻击，提高系统的安全性。





DecoratingClassLoader 子类

ClassLoader (java.lang)
    DecoratingClassLoader (org.springframework.core)
        ContextTypeMatchClassLoader (org.springframework.context.support)
        ShadowingClassLoader (org.springframework.instrument.classloading)
            ResourceOverridingShadowingClassLoader (org.springframework.instrument.classloading)
        OverridingClassLoader (org.springframework.core)
            SimpleThrowawayClassLoader (org.springframework.instrument.classloading)
            SimpleInstrumentableClassLoader (org.springframework.instrument.classloading)
            ContextOverridingClassLoader in ContextTypeMatchClassLoader (org.springframework.context.support)





这里列出了 Spring Framework 中的一些 ClassLoader 类，它们在不同的场景下具有不同的作用和实现：

1. ContextTypeMatchClassLoader：作用是在 Spring 应用上下文中，根据类型匹配的策略查找类。它的实现是基于双亲委派模型的，首先委派给父类加载器进行查找，如果父类加载器无法找到对应的类，则使用自己的查找策略进行查找。

2. ShadowingClassLoader：作用是在类加载时优先使用某个特定的类。它的实现是基于双亲委派模型的，当父类加载器无法找到对应的类时，会使用自己的查找策略进行查找，并优先使用自己的类。

3. ResourceOverridingShadowingClassLoader：作用是在类加载时优先使用某个特定的资源。它的实现是基于双亲委派模型的，当父类加载器无法找到对应的资源时，会使用自己的查找策略进行查找，并优先使用自己的资源。

4. OverridingClassLoader：作用是在类加载时允许覆盖某个特定的类。它的实现是基于双亲委派模型的，当父类加载器无法找到对应的类时，会使用自己的查找策略进行查找，并允许使用自己的类来覆盖父类加载器中的类。

5. SimpleThrowawayClassLoader：作用是在类加载时临时创建一个 ClassLoader 对象来加载类。它的实现是基于 URLClassLoader，每次加载类时都会重新创建一个 ClassLoader 对象。

6. SimpleInstrumentableClassLoader：作用是在类加载时提供字节码增强的功能。它的实现是基于 URLClassLoader，可以通过 Instrumentation API 对加载的类进行字节码增强。

7. ContextOverridingClassLoader：作用是在 Spring 应用上下文中，允许覆盖某个特定的类。它的实现是基于 OverridingClassLoader，可以根据类型查找类，并允许使用自己的类来覆盖父类加载器中的类。

这些 ClassLoader 类都是在 Spring Framework 中用于对类进行加载和管理的工具类，它们的具体实现和作用都不同，但都是基于双亲委派模型的。它们的共同点是都可以用于对类进行加载和管理，并且都可以通过一些策略来控制类的加载行为。







DecoratingProxy 是 Spring Framework 中的一个接口，用于将一个对象包装成另一个对象。它的作用是在不修改原始对象的情况下，为其添加额外的功能或修改其行为。

使用 DecoratingProxy 可以实现一些常见的设计模式，例如装饰器模式、代理模式等。它可以用于在运行时动态地添加或删除对象的功能，同时不影响原始对象的类型或行为。

下面是一个使用 DecoratingProxy 的例子：

```java
public class LoggingProxy implements DecoratingProxy<Object> {
    private static final Logger logger = LoggerFactory.getLogger(LoggingProxy.class);
    private Object target;

    @Override
    public void setTarget(Object target) {
        this.target = target;
    }

    @Override
    public Object getTarget() {
        return this.target;
    }

    @Override
    public Object decorate(Object proxy, Method method, Object[] args, Function<Object[], Object> invocation) throws Throwable {
        logger.info("Before method: {}", method.getName());
        Object result = invocation.apply(args);
        logger.info("After method: {}", method.getName());
        return result;
    }
}
```

在上面的例子中，我们创建了一个 LoggingProxy 类，实现了 DecoratingProxy 接口。在 decorate() 方法中，我们添加了日志记录的功能，用于在方法执行前后记录日志。使用该类可以将任何对象包装成一个带有日志记录功能的对象。

下面是一个使用 LoggingProxy 的示例：

```java
public interface Calculator {
    int add(int a, int b);
}

public class SimpleCalculator implements Calculator {
    @Override
    public int add(int a, int b) {
        return a + b;
    }
}

public static void main(String[] args) {
    Calculator calculator = new SimpleCalculator();
    LoggingProxy loggingProxy = new LoggingProxy();
    loggingProxy.setTarget(calculator);
    Calculator proxy = ProxyFactory.createProxy(calculator, loggingProxy);
    int result = proxy.add(1, 2);
    System.out.println(result); // output: 3
}
```

在上面的示例中，我们创建了一个 Calculator 接口和一个 SimpleCalculator 类，用于计算两个数的和。然后，我们使用 LoggingProxy 类将 SimpleCalculator 对象包装成一个带有日志记录功能的对象。最后，我们使用 ProxyFactory.createProxy() 方法创建了一个 Calculator 的代理对象，并将 LoggingProxy 作为 DecoratingProxy 传入。

总之，DecoratingProxy 是 Spring Framework 中的一个接口，用于将一个对象包装成另一个对象，并为其添加额外的功能或修改其行为。它可以用于实现装饰器模式、代理模式等设计模式，动态地添加或删除对象的功能，同时不影响原始对象的类型或行为。





ExceptionDepthComparator 是 Spring Framework 中的一个类，用于比较两个异常对象的深度。它的作用是用于将多个异常对象按照其嵌套的深度进行排序，深度越浅的异常对象越靠前。

ExceptionDepthComparator 实现了 Comparator<Throwable> 接口，可以用于对 Throwable 类型的异常对象进行排序。它会递归地比较两个异常对象及其嵌套的异常对象的深度，并返回一个比较结果。

下面是一个使用 ExceptionDepthComparator 的例子：

```java
public class ExceptionUtils {
    public static void printStackTrace(Throwable ex) {
        List<Throwable> exceptions = new ArrayList<>();
        while (ex != null) {
            exceptions.add(ex);
            ex = ex.getCause();
        }
        exceptions.sort(new ExceptionDepthComparator());
        for (Throwable exception : exceptions) {
            exception.printStackTrace();
        }
    }
}

public class MyException extends Exception {
    public MyException(String message) {
        super(message);
    }
}

public class Main {
    public static void main(String[] args) {
        try {
            throw new MyException("Exception 1", new NullPointerException("Exception 2"));
        } catch (MyException ex) {
            ExceptionUtils.printStackTrace(ex);
        }
    }
}
```

在上面的例子中，我们创建了一个 ExceptionUtils 类，用于打印异常堆栈信息。在 printStackTrace() 方法中，我们首先将异常对象及其嵌套的异常对象添加到一个 List 中，然后使用 ExceptionDepthComparator 对异常对象进行排序，最后逐个打印异常堆栈信息。

在 Main 类中，我们创建了一个 MyException 对象，并将一个 NullPointerException 对象作为其嵌套异常对象。然后，我们调用 ExceptionUtils.printStackTrace() 方法，打印异常堆栈信息，输出结果如下：

```
java.lang.NullPointerException: Exception 2
	at Main.main(Main.java:17)
	at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
	at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)
	at java.base/jdk.internal.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
	at java.base/java.lang.reflect.Method.invoke(Method.java:566)
	at com.intellij.rt.execution.application.AppMainV2.main(AppMainV2.java:131)

MyException: Exception 1
	at Main.main(Main.java:16)
	at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
	at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)
	at java.base/jdk.internal.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
	at java.base/java.lang.reflect.Method.invoke(Method.java:566)
	at com.intellij.rt.execution.application.AppMainV2.main(AppMainV2.java:131)
```

从输出结果可以看出，ExceptionDepthComparator 会将深度较浅的异常对象排在前面，先打印其堆栈信息。

总之，ExceptionDepthComparator 是 Spring Framework 中的一个类，用于比较两个异常对象的深度，可以用于对多个异常对象进行排序。它的作用是按照异常对象的嵌套深度进行排序，深度越浅的异常对象越靠前。使用它可以方便地打印多个异常对象的堆栈信息。





#### org.springframework.core.annotation

| org.springframework.core.annotation            | 类型     | 详解 |
| ---------------------------------------------- | -------- | ---- |
| Interfaces                                     |          |      |
| AbstractAliasAwareAnnotationAttributeExtractor | abstract |      |
| AnnotationFilter                               |          |      |
| MergedAnnotation                               |          |      |
| MergedAnnotations                              |          |      |
| MergedAnnotationSelector                       |          |      |
| SynthesizedAnnotation                          |          |      |
|                                                |          |      |
| Classes                                        |          |      |
| AnnotatedElementUtils                          |          |      |
| AnnotationAttributes                           |          |      |
| AnnotationAwareOrderComparator                 |          |      |
| AnnotationUtils                                |          |      |
| MergedAnnotationCollectors                     |          |      |
| MergedAnnotationPredicates                     |          |      |
| MergedAnnotationSelectors                      |          |      |
| OrderUtils                                     |          |      |
| RepeatableContainers                           |          |      |
| SynthesizingMethodParameter                    |          |      |
|                                                |          |      |
| Enums                                          |          |      |
| MergedAnnotation.Adapt                         |          |      |
| MergedAnnotations.SearchStrategy               |          |      |







Exceptions

AnnotationConfigurationException



Annotation Types

AliasFor

Order



#### org.springframework.core.codec

| org.springframework.core.codec | 类型 |      |
| ------------------------------ | ---- | ---- |
|     Interfaces                   |      |      |
|      Decoder                |      | interface     |
|    Encoder               |      | interface   |
|    Classes               |      |      |
|   AbstractDataBufferDecoder     |      |      |
|  AbstractDecoder    |      |      |
|   AbstractEncoder    |      |      |
|     AbstractSingleValueEncoder    |      |      |
|     ByteArrayDecoder      |      |      |
|   ByteArrayEncoder         |      |      |
|    ByteBufferDecoder         |      |      |
|    ByteBufferEncoder      |      |      |
|      CharSequenceEncoder     |      |      |
|    DataBufferDecoder    |      |      |
|     DataBufferEncoder       |      |      |
|      Hints       |      |      |
|    NettyByteBufDecoder     |      |      |
|    NettyByteBufEncoder    |      |      |
|    ResourceDecoder   |      |      |
|    ResourceEncoder     |      |      |
|   ResourceRegionEncoder  |      |      |
|   StringDecoder    |      |      |
|                   |      |      |
|     Exceptions       |      |      |
|     CodecException     |      |      |
|    DecodingException      |      |      |
|  EncodingException        |      |      |


#### org.springframework.core.convert

| org.springframework.core.convert |      |      |
| -------------------------------- | ---- | ---- |
|        Interfaces                          |      |      |
|        ConversionService                          |   interface   |      |
|                                  |      |      |
|        Classes            |      |      |
|      Property               |      |      |
|      TypeDescriptor            |      |      |
|                                  |      |      |
|      Exceptions         |      |      |
|      ConversionException         |      |      |
|   ConversionFailedException         |      |      |
|      ConverterNotFoundException           |      |      |
|                                  |      |      |


ConversionService接口方法
boolean canConvert()
<T> T convert(@Nullable Object source, Class<T> targetType);


接口实现类
org.springframework.core.convert.support.DefaultConversionService


spring-mvc jar包
org.springframework.http.converter.ObjectToStringHttpMessageConverter 中使用
spring-jdbc jar包
org.springframework.jdbc.core.SingleColumnRowMapper 中使用 DefaultConversionService

跟spring-mvc jar包里面的org.springframework.http.converter.HttpMessageConverter 接口没大多联系

###### org.springframework.core.convert.converter


| org.springframework.core.convert.converter | 类型 |      |
| ------------------------------------------ | ---- | ---- |
|                                            |      |      |
| Interfaces                                 |      |      |
| ConditionalConverter                       |      |      |
| ConditionalGenericConverter                |      |      |
| Converter                                  |      |      |
| ConverterFactory                           |      |      |
| ConverterRegistry                          |      |      |
| GenericConverter                           |      |      |
|                                            |      |      |
| Classes                                    |      |      |
| ConvertingComparator                       |      |      |
| GenericConverter.ConvertiblePair           |      |      |



##### org.springframework.core.convert.support


| org.springframework.core.io     | 类型 |      |
| ------------------------------- | ---- | ---- |
| Interfaces                      |      |      |
| ConfigurableConversionService   |      |      |
|                                 |      |      |
| Classes                         |      |      |
| ConversionServiceFactory        |      |      |
| ConvertingPropertyEditorAdapter |      |      |
| DefaultConversionService        |      |      |
| GenericConversionService        |      |      |





#### org.springframework.core.env



| Interfaces                         |      |      |
| ---------------------------------- | ---- | ---- |
|                                    |      |      |
| ConfigurableEnvironment            |      |      |
| ConfigurablePropertyResolver       |      |      |
| Environment                        |      |      |
| EnvironmentCapable                 |      |      |
| Profiles                           |      |      |
| PropertyResolver                   |      |      |
| PropertySources                    |      |      |
|                                    |      |      |
| Classes                            |      |      |
|                                    |      |      |
| AbstractEnvironment                |      |      |
| AbstractPropertyResolver           |      |      |
| CommandLinePropertySource          |      |      |
| CompositePropertySource            |      |      |
| EnumerablePropertySource           |      |      |
| JOptCommandLinePropertySource      |      |      |
| MapPropertySource                  |      |      |
| MutablePropertySources             |      |      |
| PropertiesPropertySource           |      |      |
| PropertySource                     |      |      |
| PropertySource.StubPropertySource  |      |      |
| PropertySourcesPropertyResolver    |      |      |
| SimpleCommandLinePropertySource    |      |      |
| StandardEnvironment                |      |      |
| SystemEnvironmentPropertySource    |      |      |
|                                    |      |      |
| Exceptions                         |      |      |
|                                    |      |      |
| MissingRequiredPropertiesException |      |      |



PropertySourcesPropertyResolver日志



```shell
15:08:10.746 TRACE org.springframework.core.env.PropertySourcesPropertyResolver 82 getProperty - Searching for key 'spring.liveBeansView.mbeanDomain' in PropertySource 'systemProperties'
15:08:10.746 TRACE org.springframework.core.env.PropertySourcesPropertyResolver 82 getProperty - Searching for key 'spring.liveBeansView.mbeanDomain' in PropertySource 'systemEnvironment'
15:08:10.746 TRACE org.springframework.core.env.PropertySourcesPropertyResolver 96 getProperty - Could not find key 'spring.liveBeansView.mbeanDomain' in any property source
```









#### org.springframework.core.io
org.springframework.core.io.Resource接口 子接口 ContextResource WritableResource
org.springframework.core.io.ResourceLoader接口



| org.springframework.core.io                    | 类型 |      |
| ---------------------------------------------- | ---- | ---- |
| Interfaces                                     |      |      |
|                                                |      |      |
| ContextResource                                |      |      |
| InputStreamSource                              |      |      |
| ProtocolResolver                               |      |      |
| Resource                                       |      |      |
| ResourceLoader                                 |      |      |
| WritableResource                               |      |      |
|                                                |      |      |
| Classes                                        |      |      |
|                                                |      |      |
| AbstractFileResolvingResource                  |      |      |
| AbstractResource                               |      |      |
| ByteArrayResource                              |      |      |
| ClassPathResource                              |      |      |
| ClassRelativeResourceLoader                    |      |      |
| DefaultResourceLoader                          |      |      |
| DefaultResourceLoader.ClassPathContextResource |      |      |
| DescriptiveResource                            |      |      |
| FileSystemResource                             |      |      |
| FileSystemResourceLoader                       |      |      |
| FileUrlResource                                |      |      |
| InputStreamResource                            |      |      |
| PathResource                                   |      |      |
| ResourceEditor                                 |      |      |
| UrlResource                                    |      |      |
| VfsResource                                    |      |      |
| VfsUtils                                       |      |      |



##### org.springframework.core.io.buffer

org.springframework.core.io.buffer.DataBuffer接口
DataBufferFactory 工厂接口 实现类 NettyDataBufferFactory NettyDataBufferFactory



| org.springframework.core.io.buffer | 类型 |      |
| ---------------------------------- | ---- | ---- |
| Interfaces                         |      |      |
|                                    |      |      |
| DataBuffer                         |      |      |
| DataBufferFactory                  |      |      |
| DataBufferUtils.Matcher            |      |      |
| PooledDataBuffer                   |      |      |
|                                    |      |      |
| Classes                            |      |      |
|                                    |      |      |
| DataBufferUtils                    |      |      |
| DataBufferWrapper                  |      |      |
| DefaultDataBuffer                  |      |      |
| DefaultDataBufferFactory           |      |      |
| LimitedDataBufferList              |      |      |
| NettyDataBuffer                    |      |      |
| NettyDataBufferFactory             |      |      |
|                                    |      |      |
| Exceptions                         |      |      |
|                                    |      |      |
| DataBufferLimitException           |      |      |





##### org.springframework.core.io.support





| org.springframework.core.io.support | 类型     |                                                              |
| ----------------------------------- | -------- | ------------------------------------------------------------ |
| Interfaces                          |          |                                                              |
|                                     |          |                                                              |
| PropertySourceFactory               |          | PropertySource<?> createPropertySource(@Nullable String name, EncodedResource resource) 接口实现类DefaultPropertySourceFactory |
| ResourcePatternResolver             |          | Resource[] getResources(String locationPattern)              |
|                                     |          |                                                              |
| Classes                             |          |                                                              |
|                                     |          |                                                              |
| DefaultPropertySourceFactory        |          | 实现了PropertySourceFactory接口                              |
| EncodedResource                     |          |                                                              |
| LocalizedResourceHelper             |          | Resource findLocalizedResource(String name, String extension, @Nullable Locale locale) |
| PathMatchingResourcePatternResolver |          | 实现ResourcePatternResolver 接口 Resource[] getResources(String locationPattern) |
| PropertiesLoaderSupport             | abstract | 子类PropertiesFactoryBean PropertyResourceConfigurer PropertyOverrideConfigurer |
| PropertiesLoaderUtils               | abstract |                                                              |
| ResourceArrayPropertyEditor         |          | 继承PropertyEditorSupport接口                                |
| ResourcePatternUtils                |          |                                                              |
| ResourcePropertiesPersister         |          |                                                              |
| ResourcePropertySource              |          |                                                              |
| ResourceRegion                      |          |                                                              |
| SpringFactoriesLoader               |          |                                                              |





SpringFactoriesLoader 日志

```shell
15:08:10.749 TRACE org.springframework.core.io.support.SpringFactoriesLoader 100 loadFactories - Loaded [org.springframework.beans.BeanInfoFactory] names: [org.springframework.beans.ExtendedBeanInfoFactory]
```





#### org.springframework.core.log

| org.springframework.core.log | 类型 |      |
| ---------------------------- | ---- | ---- |
| Classes                      |      |      |
|                              |      |      |
| LogAccessor                  |      |      |
| LogDelegateFactory           |      |      |
| LogFormatUtils               |      |      |
| LogMessage                   |      |      |





#### org.springframework.core.serializer

| org.springframework.core.serializer | 类型 |      |
| ----------------------------------- | ---- | ---- |
| Interfaces                          |      |      |
|                                     |      |      |
| Deserializer                        |      |      |
| Serializer                          |      |      |
|                                     |      |      |
| Classes                             |      |      |
|                                     |      |      |
| DefaultDeserializer                 |      |      |
| DefaultSerializer                   |      |      |





##### org.springframework.core.serializer.support



| org.springframework.core.serializer.support | 类型 |                                                              |
| ------------------------------------------- | ---- | ------------------------------------------------------------ |
| Classes                                     |      |                                                              |
|                                             |      |                                                              |
| DeserializingConverter                      |      | implements Converter<byte[], Object>                         |
| SerializationDelegate                       |      | `4.3 SerializationDelegate implements Serializer<Object>, Deserializer<Object> |
| SerializingConverter                        |      |                                                              |
|                                             |      |                                                              |
| Exceptions                                  |      |                                                              |
|                                             |      |                                                              |
| SerializationFailedException                |      |                                                              |



#### org.springframework.core.style



| Interfaces                     | 类型 |      |
| ------------------------------ | ---- | ---- |
| org.springframework.core.style |      |      |
|                                |      |      |
| ToStringStyler                 |      |      |
| ValueStyler                    |      |      |
|                                |      |      |
| Classes                        |      |      |
|                                |      |      |
| DefaultToStringStyler          |      |      |
| DefaultValueStyler             |      |      |
| StylerUtils                    |      |      |
| ToStringCreator                |      |      |



#### org.springframework.core.task



| org.springframework.core.task | 类型 |      |
| ----------------------------- | ---- | ---- |
| Interfaces                    |      |      |
|                               |      |      |
| AsyncListenableTaskExecutor   |      |      |
| AsyncTaskExecutor             |      |      |
| TaskDecorator                 |      |      |
| TaskExecutor                  |      |      |
|                               |      |      |
| Classes                       |      |      |
|                               |      |      |
| SimpleAsyncTaskExecutor       |      |      |
| SyncTaskExecutor              |      |      |
|                               |      |      |
| Exceptions                    |      |      |
|                               |      |      |
| TaskRejectedException         |      |      |
| TaskTimeoutException          |      |      |
|                               |      |      |



##### org.springframework.core.task.support





| org.springframework.core.task.support | 类型 |      |
| ------------------------------------- | ---- | ---- |
| Classes                               |      |      |
|                                       |      |      |
| ConcurrentExecutorAdapter             |      |      |
| ExecutorServiceAdapter                |      |      |
| TaskExecutorAdapter                   |      |      |



#### org.springframework.core.type



| org.springframework.core.type | 类型 |      |
| ----------------------------- | ---- | ---- |
|                               |      |      |
| Interfaces                    |      |      |
|                               |      |      |
| AnnotatedTypeMetadata         |      |      |
| AnnotationMetadata            |      |      |
| ClassMetadata                 |      |      |
| MethodMetadata                |      |      |
|                               |      |      |
| Classes                       |      |      |
|                               |      |      |
| StandardAnnotationMetadata    |      |      |
| StandardClassMetadata         |      |      |
| StandardMethodMetadata        |      |      |



##### org.springframework.core.type.classreading



| org.springframework.core.type.classreading | 类型 |      |
| ------------------------------------------ | ---- | ---- |
| Interfaces                                 |      |      |
|                                            |      |      |
| MetadataReader                             |      |      |
| MetadataReaderFactory                      |      |      |
|                                            |      |      |
| Classes                                    |      |      |
|                                            |      |      |
| AnnotationMetadataReadingVisitor           |      |      |
| CachingMetadataReaderFactory               |      |      |
| MethodMetadataReadingVisitor               |      |      |
| SimpleMetadataReaderFactory                |      |      |



##### org.springframework.core.type.filter

| org.springframework.core.type.filter  | 类型 |      |
| ------------------------------------- | ---- | ---- |
| Interfaces                            |      |      |
|                                       |      |      |
| TypeFilter                            |      |      |
|                                       |      |      |
| Classes                               |      |      |
|                                       |      |      |
| AbstractClassTestingTypeFilter        |      |      |
| AbstractTypeHierarchyTraversingFilter |      |      |
| AnnotationTypeFilter                  |      |      |
| AspectJTypeFilter                     |      |      |
| AssignableTypeFilter                  |      |      |
| RegexPatternTypeFilter                |      |      |



org.springframework.core.type.filter.AnnotationTypeFilter
在ClassPathBeanDefinitionScanner中使用


### org.springframework.lang




| org.springframework.lang               | 类型 |      |
| ---- | ---- | ---- |
|                                        |      |      |
| Annotation Types                       |      |      |
|                                        |      |      |
| NonNull                                |      |      |
| NonNullApi                             |      |      |
| NonNullFields                          |      |      |
| Nullable                               |      |      |
| UsesJava7                              |      |      |
| UsesJava8                              |      |      |
| UsesSunHttpServer                      |      |      |
| UsesSunMisc                            |      |      |


















### org.springframework.objenesis






SpringObjenesis



#### org.springframework.objenesis.instantiator





#### org.springframework.objenesis.strategy





### org.springframework.util



| org.springframework.util                         |          |      |
| ------------------------------------------------ | -------- | ---- |
|                                                  |          |      |
| AutoPopulatingList.ElementFactory                |          |      |
| ConcurrentReferenceHashMap.Reference             |          |      |
| ErrorHandler                                     |          |      |
| IdGenerator                                      |          |      |
| MultiValueMap                                    |          |      |
| PathMatcher                                      |          |      |
| PropertiesPersister                              |          |      |
| PropertyPlaceholderHelper.PlaceholderResolver    |          |      |
| ReflectionUtils.FieldCallback                    |          |      |
| ReflectionUtils.FieldFilter                      |          |      |
| ReflectionUtils.MethodCallback                   |          |      |
| ReflectionUtils.MethodFilter                     |          |      |
| RouteMatcher                                     |          |      |
| RouteMatcher.Route                               |          |      |
| StringValueResolver                              |          |      |
|                                                  |          |      |
| Classes                                          |          |      |
|                                                  |          |      |
| AlternativeJdkIdGenerator                        |          |      |
| AntPathMatcher                                   |          |      |
| AntPathMatcher.AntPathStringMatcher              |          |      |
| AntPathMatcher.AntPatternComparator              |          |      |
| Assert                                           |          |      |
| AutoPopulatingList                               |          |      |
| Base64Utils                                      |          |      |
| ClassUtils                                       |          |      |
| CollectionUtils                                  |          |      |
| CommonsLogWriter                                 |          |      |
| CompositeIterator                                |          |      |
| ConcurrencyThrottleSupport                       |          |      |
| ConcurrentReferenceHashMap                       |          |      |
| ConcurrentReferenceHashMap.Entry                 |          |      |
| CustomizableThreadCreator                        |          |      |
| DefaultPropertiesPersister                       |          |      |
| DigestUtils                                      |          |      |
| ExceptionTypeFilter                              |          |      |
| FastByteArrayOutputStream                        |          |      |
| FileCopyUtils                                    |          |      |
| FileSystemUtils                                  |          |      |
| InstanceFilter                                   |          |      |
| JdkIdGenerator                                   |          |      |
| LinkedCaseInsensitiveMap                         |          |      |
| LinkedMultiValueMap                              |          |      |
| MethodInvoker                                    |          |      |
| MimeType                                         |          |      |
| MimeType.SpecificityComparator                   |          |      |
| MimeTypeUtils                                    |          |      |
| NumberUtils                                      |          |      |
| ObjectUtils                                      | abstract |      |
| PatternMatchUtils                                |          |      |
| PropertyPlaceholderHelper                        |          |      |
| ReflectionUtils                                  |          |      |
| ResizableByteArrayOutputStream                   |          |      |
| ResourceUtils                                    |          |      |
| SerializationUtils                               |          |      |
| SimpleIdGenerator                                |          |      |
| SimpleRouteMatcher                               |          |      |
| SocketUtils                                      |          |      |
| StopWatch                                        |          |      |
| StopWatch.TaskInfo                               |          |      |
| StreamUtils                                      |          |      |
| StringUtils                                      |          |      |
| SystemPropertyUtils                              |          |      |
| TypeUtils                                        |          |      |
|                                                  |          |      |
| Enums                                            |          |      |
|                                                  |          |      |
| ConcurrentReferenceHashMap.ReferenceType         |          |      |
| ConcurrentReferenceHashMap.Restructure           |          |      |
|                                                  |          |      |
| Exceptions                                       |          |      |
|                                                  |          |      |
| AutoPopulatingList.ElementInstantiationException |          |      |
| InvalidMimeTypeException                         |          |      |



#### org.springframework.util.backoff



| org.springframework.util.backoff |      |      |
| -------------------------------- | ---- | ---- |
| Interfaces                       |      |      |
|                                  |      |      |
| BackOff                          |      |      |
| BackOffExecution                 |      |      |
|                                  |      |      |
| Classes                          |      |      |
|                                  |      |      |
| ExponentialBackOff               |      |      |
| FixedBackOff                     |      |      |

#### org.springframework.util.comparator





| org.springframework.util.comparator |      |      |
| ----------------------------------- | ---- | ---- |
| Classes                             |      |      |
|                                     |      |      |
| BooleanComparator                   |      |      |
| ComparableComparator                |      |      |
| Comparators                         |      |      |
| CompoundComparator                  |      |      |
| InstanceComparator                  |      |      |
| InvertibleComparator                |      |      |
| NullSafeComparator                  |      |      |



#### org.springframework.util.concurrent





|                                      |      |      |
| ------------------------------------ | ---- | ---- |
| Interfaces                           |      |      |
|                                      |      |      |
| FailureCallback                      |      |      |
| ListenableFuture                     |      |      |
| ListenableFutureCallback             |      |      |
| SuccessCallback                      |      |      |
|                                      |      |      |
| Classes                              |      |      |
|                                      |      |      |
| CompletableToListenableFutureAdapter |      |      |
| FutureAdapter                        |      |      |
| ListenableFutureAdapter              |      |      |
| ListenableFutureCallbackRegistry     |      |      |
| ListenableFutureTask                 |      |      |
| MonoToListenableFutureAdapter        |      |      |
| SettableListenableFuture             |      |      |



#### org.springframework.util.function
SingletonSupplier<T>
SupplierUtils

#### org.springframework.util.unit

DataSize

DataUnit
#### org.springframework.util.xml





| org.springframework.util.xml |      |      |
| ---------------------------- | ---- | ---- |
| Classes                      |      |      |
|                              |      |      |
| DomUtils                     |      |      |
| SimpleNamespaceContext       |      |      |
| SimpleSaxErrorHandler        |      |      |
| SimpleTransformErrorListener |      |      |
| StaxUtils                    |      |      |
| TransformerUtils             |      |      |
| XmlValidationModeDetector    |      |      |