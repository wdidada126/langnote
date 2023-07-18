# spring expression



以下是一些 SpEL 表达式的例子：

* 计算两个数字的和：`#{1 + 2}`
* 访问对象的属性：`#{user.name}`
* 调用方法：`#{user.getName()}`
* 使用内置函数：`#{T(java.lang.Math).sqrt(4)}`
* 使用用户自定义函数：`#{myFunction(arg1, arg2)}`

你可以在 Spring 的官方文档中找到更多关于 SpEL 表达式的介绍：[https://docs.spring.io/spring-framework/docs/current/reference/html/core.html#expressions ↗](https://docs.spring.io/spring-framework/docs/current/reference/html/core.html#expressions)






| org.springframework.asm                |      |      |
| -------------------------------------- | ---- | ---- |
|                                        |      |      |
| Interfaces                             |      |      |
|                                        |      |      |
| Opcodes                                |      |      |
|                                        |      |      |
| Classes                                |      |      |
|                                        |      |      |
| AnnotationVisitor                      |      |      |
| Attribute                              |      |      |
| ByteVector                             |      |      |
| ClassReader                            |      |      |
| ClassVisitor                           |      |      |
| ClassWriter                            |      |      |
| ConstantDynamic                        |      |      |
| FieldVisitor                           |      |      |
| Handle                                 |      |      |
| Label                                  |      |      |
| MethodVisitor                          |      |      |
| ModuleVisitor                          |      |      |
| RecordComponentVisitor                 |      |      |
| SpringAsmInfo                          |      |      |
| Type                                   |      |      |
| TypePath                               |      |      |
| TypeReference                          |      |      |
|                                        |      |      |
| Exceptions                             |      |      |
|                                        |      |      |
| ClassTooLargeException                 |      |      |
| MethodTooLargeException                |      |      |
|                                        |      |      |
|                                        |      |      |
|                                        |      |      |
|                                        |      |      |
|                                        |      |      |
| org.springframework.cglib              |      |      |
|                                        |      |      |
| Classes                                |      |      |
|                                        |      |      |
| SpringCglibInfo                        |      |      |
|                                        |      |      |
| org.springframework.cglib.beans        |      |      |
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
| org.springframework.cglib.core         |      |      |
|                                        |      |      |
| Classes                                |      |      |
|                                        |      |      |
| AbstractClassGenerator                 |      |      |
| AbstractClassGenerator.ClassLoaderData |      |      |
| AbstractClassGenerator.Source          |      |      |
| ClassLoaderAwareGeneratorStrategy      |      |      |
| KeyFactory                             |      |      |
| KeyFactory.Generator                   |      |      |
| ReflectUtils                           |      |      |
| SpringNamingPolicy                     |      |      |
|                                        |      |      |
|                                        |      |      |
|                                        |      |      |
| org.springframework.cglib.proxy        |      |      |
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
| org.springframework.lang               |      |      |
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

















| org.springframework.expression                     | package  |                                                              |
| -------------------------------------------------- | -------- | ------------------------------------------------------------ |
| Interfaces                                         |          |                                                              |
| BeanResolver                                       |          | Object resolve(EvaluationContext context, String beanName)   |
| ConstructorExecutor                                |          | TypedValue execute(EvaluationContext context, Object... arguments)  唯一实现类ReflectiveConstructorExecutor |
| ConstructorResolver                                |          |                                                              |
| EvaluationContext                                  |          | 接口实现类SimpleEvaluationContext StandardEvaluationContext MethodBasedEvaluationContext |
| Expression                                         |          | String getExpressionString()  getValue() isWritable()  实现接口的类 SpelExpression CompositeStringExpression  LiteralExpression |
| ExpressionParser                                   |          | Expression parseExpression(String expressionString)  Expression parseExpression(String expressionString, ParserContext context) |
| MethodExecutor                                     |          | TypedValue execute(EvaluationContext context, Object target, Object... arguments) |
| MethodFilter                                       |          | boolean isHandled(Method m)                                  |
| MethodResolver                                     |          | MethodExecutor resolve(EvaluationContext context, Object targetObject, String name,<br/>       List<TypeDescriptor> argumentTypes) |
| OperatorOverloader                                 |          | boolean overridesOperation(Operation operation, @Nullable Object leftOperand, @Nullable Object rightOperand)   Object operate(Operation operation, @Nullable Object leftOperand, @Nullable Object rightOperand) |
| ParserContext                                      |          | boolean isTemplate()   String getExpressionPrefix()  String getExpressionSuffix() |
| PropertyAccessor                                   |          | 实现类 ReflectivePropertyAccessor                            |
| TypeComparator                                     |          | boolean canCompare(@Nullable Object firstObject, @Nullable Object secondObject)  int compare(@Nullable Object firstObject, @Nullable Object secondObject) |
| TypeConverter                                      |          | <T> T convertIfNecessary(@Nullable Object value, @Nullable Class<T> requiredType,<br/>       @Nullable MethodParameter methodParam)       <T> T convertIfNecessary(@Nullable Object value, @Nullable Class<T> requiredType) |
| TypeLocator                                        |          | Class<?> findType(String typeName)                           |
|                                                    |          |                                                              |
| Classes                                            |          |                                                              |
| TypedValue                                         |          | TypeDescriptor                                               |
|                                                    |          |                                                              |
| Enums                                              |          |                                                              |
| Operation                                          | enum     | ADD等值                                                      |
|                                                    |          |                                                              |
| Exceptions                                         |          |                                                              |
| AccessException                                    |          |                                                              |
| EvaluationException                                |          |                                                              |
| ExpressionException                                |          |                                                              |
| ExpressionInvocationTargetException                |          |                                                              |
| ParseException                                     |          |                                                              |
|                                                    |          |                                                              |
| org.springframework.expression.common              | package  |                                                              |
| Classes                                            |          |                                                              |
| CompositeStringExpression                          |          | implements Expression 核心方法 getValue()                    |
| ExpressionUtils                                    | abstract | 抽象类，都是静态方法                                         |
| LiteralExpression                                  |          | 字面常量表达式                                               |
| TemplateAwareExpressionParser                      | abstract | abstract Expression doParseExpression(String expressionString, @Nullable ParserContext context)  子类InternalSpelExpressionParser SpelExpressionParser |
| TemplateParserContext                              |          | implements ParserContext 属性 String expressionPrefix  String expressionSuffix |
|                                                    |          |                                                              |
|                                                    |          |                                                              |
|                                                    |          |                                                              |
| org.springframework.expression.spel                | package  |                                                              |
| Interfaces                                         |          |                                                              |
| CodeFlow.ClinitAdder                               |          |                                                              |
| CodeFlow.FieldAdder                                |          |                                                              |
| CompilablePropertyAccessor                         |          | extends PropertyAccessor, Opcodes                            |
| SpelNode                                           |          |                                                              |
|                                                    |          |                                                              |
| Classes                                            |          |                                                              |
| CodeFlow                                           |          | implements Opcodes                                           |
| CompiledExpression                                 | abstract | Object getValue(@Nullable Object target, @Nullable EvaluationContext context) |
| ExpressionState                                    |          | 解析和评估表达式。封装了表达式的执行环境和状态。             |
| SpelParserConfiguration                            |          | SpEL 解析器的配置类。它提供了对 SpEL 解析器的各种配置选项的访问，包括解析器的语言版本、解析器的扩展功能、解析器的错误处理策略等。 |
|                                                    |          |                                                              |
| Enums                                              |          |                                                              |
| SpelCompilerMode                                   |          |                                                              |
| SpelMessage                                        |          |                                                              |
| SpelMessage.Kind                                   |          |                                                              |
|                                                    |          |                                                              |
| Exceptions                                         |          |                                                              |
| InternalParseException                             |          |                                                              |
| SpelEvaluationException                            |          |                                                              |
| SpelParseException                                 |          |                                                              |
|                                                    |          |                                                              |
|                                                    |          |                                                              |
| org.springframework.expression.spel.ast            | package  |                                                              |
|                                                    |          |                                                              |
| Interfaces                                         |          |                                                              |
|                                                    |          |                                                              |
| ValueRef                                           |          |                                                              |
|                                                    |          |                                                              |
| Classes                                            |          |                                                              |
| Assign                                             |          |                                                              |
| AstUtils                                           |          |                                                              |
| BeanReference                                      |          | extends SpelNodeImpl     TypedValue getValueInternal(ExpressionState state) |
| BooleanLiteral                                     |          | extends Literal                                              |
| CompoundExpression                                 |          |                                                              |
| ConstructorReference                               |          |                                                              |
| Elvis                                              |          |                                                              |
| FloatLiteral                                       |          |                                                              |
| FunctionReference                                  |          |                                                              |
| Identifier                                         |          |                                                              |
| Indexer                                            |          |                                                              |
| InlineList                                         |          |                                                              |
| InlineMap                                          |          |                                                              |
| IntLiteral                                         |          |                                                              |
| Literal                                            | abstract | extends SpelNodeImpl   Literal 是 Groovy 中表示常量值的类    |
| LongLiteral                                        |          |                                                              |
| MethodReference                                    |          |                                                              |
| NullLiteral                                        |          |                                                              |
| OpAnd                                              |          | true and false                                               |
| OpDec                                              |          |                                                              |
| OpDivide                                           |          |                                                              |
| OpEQ                                               |          |                                                              |
| Operator                                           |          |                                                              |
| Operator.DescriptorComparison                      |          |                                                              |
| OperatorBetween                                    |          |                                                              |
| OperatorInstanceof                                 |          |                                                              |
| OperatorMatches                                    |          |                                                              |
| OperatorNot                                        |          |                                                              |
| OperatorPower                                      |          |                                                              |
| OpGE                                               |          |                                                              |
| OpGT                                               |          |                                                              |
| OpInc                                              |          |                                                              |
| OpLE                                               |          |                                                              |
| OpLT                                               |          |                                                              |
| OpMinus                                            |          |                                                              |
| OpModulus                                          |          |                                                              |
| OpMultiply                                         |          |                                                              |
| OpNE                                               |          |                                                              |
| OpOr                                               |          |                                                              |
| OpPlus                                             |          | 1+2                                                          |
| Projection                                         |          |                                                              |
| PropertyOrFieldReference                           |          |                                                              |
| QualifiedIdentifier                                |          |                                                              |
| RealLiteral                                        |          |                                                              |
| Selection                                          |          |                                                              |
| SpelNodeImpl                                       | abstract |                                                              |
| StringLiteral                                      |          |                                                              |
| Ternary                                            |          |                                                              |
| TypeReference                                      |          |                                                              |
| ValueRef.NullValueRef                              |          |                                                              |
| ValueRef.TypedValueHolderValueRef                  |          |                                                              |
| VariableReference                                  |          | TypeReference ConstructorReference  FunctionReference BeanReference  MethodReference   PropertyOrFieldReference  CompoundExpression |
|                                                    |          |                                                              |
| Enums                                              |          |                                                              |
|                                                    |          |                                                              |
| TypeCode                                           |          |                                                              |
|                                                    |          |                                                              |
|                                                    |          |                                                              |
|                                                    |          |                                                              |
| org.springframework.expression.spel.standard       | package  |                                                              |
|                                                    |          |                                                              |
| Classes                                            |          |                                                              |
|                                                    |          |                                                              |
| SpelCompiler                                       |          |                                                              |
| SpelExpression                                     |          |                                                              |
| SpelExpressionParser                               |          | 父类TemplateAwareExpressionParser                            |
|                                                    |          |                                                              |
|                                                    |          |                                                              |
| org.springframework.expression.spel.support        | package  |                                                              |
|                                                    |          |                                                              |
| Classes                                            |          |                                                              |
|                                                    |          |                                                              |
| BooleanTypedValue                                  |          |                                                              |
| DataBindingMethodResolver                          |          |                                                              |
| DataBindingPropertyAccessor                        |          | 实现PropertyAccessor接口                                     |
| ReflectionHelper                                   |          | 静态工具类，org.springframework.expression.spel.support.ReflectiveConstructorExecutor#execute |
| ReflectiveConstructorExecutor                      |          | execute()                                                    |
| ReflectiveConstructorResolver                      |          |                                                              |
| ReflectiveMethodExecutor                           |          |                                                              |
| ReflectiveMethodResolver                           |          |                                                              |
| ReflectivePropertyAccessor                         |          | DataBindingPropertyAccessor extends ReflectivePropertyAccessor |
| ReflectivePropertyAccessor.OptimalPropertyAccessor |          |                                                              |
| SimpleEvaluationContext                            |          | 简化的表达式求值上下文，它提供了最基本的配置选项             |
| SimpleEvaluationContext.Builder                    |          |                                                              |
| StandardEvaluationContext                          |          | 可配置的表达式求值上下文                                     |
| StandardOperatorOverloader                         |          | implements OperatorOverloader                                |
| StandardTypeComparator                             |          | implements TypeComparator                                    |
| StandardTypeConverter                              |          | implements TypeConverter                                     |
| StandardTypeLocator                                |          | implements TypeLocator                                       |





`SimpleEvaluationContext` 和 `StandardEvaluationContext` 是 SpEL（Spring Expression Language）中用于定义和配置表达式求值的上下文环境的类。

1. `SimpleEvaluationContext`：是一个简化的表达式求值上下文，它提供了最基本的配置选项。它可以用于简单的表达式求值场景，不需要复杂的配置和功能。它包含了一些默认的配置，如属性访问控制、类型转换和函数注册等。

2. `StandardEvaluationContext`：是一个更加全面和可配置的表达式求值上下文。它提供了更多的功能和灵活性。除了包含 `SimpleEvaluationContext` 的所有功能外，它还允许用户自定义类型转换器、自定义函数、变量的注册和访问控制等。

这两个上下文类的作用是为表达式求值提供必要的配置和环境。它们可以用于设置和管理表达式求值过程中所需的各种属性、函数、变量等，以及定义属性和方法的可访问性。通过这些上下文对象，可以定制和控制表达式求值的行为，满足特定的需求和业务逻辑。



ReflectiveConstructorExecutor 是 Spring Framework 提供的一个用于执行反射构造函数的类。它可以用于在运行时动态地通过反射机制创建 Java 对象。以下是一个使用 ReflectiveConstructorExecutor 的示例：

假设有一个名为 Person 的 Java 类，它有两个属性 name 和 age：

```java
public class Person {
    private String name;
    private int age;

    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }

    // getter and setter methods
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public int getAge() { return age; }
    public void setAge(int age) { this.age = age; }
}
```

现在，我们可以使用 ReflectiveConstructorExecutor 来创建 Person 对象。下面的示例演示了如何使用 ReflectiveConstructorExecutor 来创建 Person 对象：

```java
import org.springframework.beans.factory.support.SimpleInstantiationStrategy;
import org.springframework.beans.factory.support.ConstructorResolver;
import org.springframework.beans.factory.config.BeanDefinition;
import org.springframework.beans.BeanWrapper;
import org.springframework.beans.BeanWrapperImpl;
import org.springframework.core.io.ClassPathResource;
import org.springframework.core.io.Resource;
import java.io.InputStream;
import java.util.Properties;

public class Main {
    public static void main(String[] args) throws Exception {
        // 加载配置文件
        Resource resource = new ClassPathResource("application.properties");
        InputStream input = resource.getInputStream();
        Properties props = new Properties();
        props.load(input);

        // 创建 BeanDefinition 对象
        BeanDefinition beanDefinition = new GenericBeanDefinition();
        beanDefinition.setBeanClassName("Person");

        // 创建 ConstructorResolver 对象
        ConstructorResolver resolver = new ConstructorResolver(beanDefinition);

        // 创建 SimpleInstantiationStrategy 对象
        SimpleInstantiationStrategy strategy = new SimpleInstantiationStrategy();

        // 创建 BeanWrapper 对象
        BeanWrapper beanWrapper = new BeanWrapperImpl(strategy.instantiate(beanDefinition, null, null));

        // 获取构造函数
        Constructor<?> constructor = resolver.autowireConstructor();

        // 创建 ReflectiveConstructorExecutor 对象
        ReflectiveConstructorExecutor executor = new ReflectiveConstructorExecutor(constructor);

        // 设置属性值
        beanWrapper.setPropertyValue("name", props.getProperty("person.name"));
        beanWrapper.setPropertyValue("age", Integer.parseInt(props.getProperty("person.age")));

        // 创建 Person 对象
        Person person = (Person) executor.execute(new Object[]{beanWrapper.getWrappedInstance()});

        // 输出属性值
        System.out.println("Name: " + person.getName());
        System.out.println("Age: " + person.getAge());
    }
}
```

在上面的示例中，我们首先加载了一个配置文件，然后创建了一个 Person 的 BeanDefinition 对象。接下来，我们使用 ConstructorResolver 和 SimpleInstantiationStrategy 来创建 BeanWrapper 对象，并获取构造函数。然后，我们使用 ReflectiveConstructorExecutor 来执行构造函数，并使用 BeanWrapper 来设置属性值。最后，我们创建了 Person 对象，并输出属性值。

总之，ReflectiveConstructorExecutor 是 Spring Framework 提供的一个用于执行反射构造函数的类，可以用于在运行时动态地通过反射机制创建 Java 对象。在使用 ReflectiveConstructorExecutor 时，需要先获取构造函数，然后创建 ReflectiveConstructorExecutor 对象，最后使用 execute() 方法执行构造函数。







SpelExpression CompositeStringExpression LiteralExpression 各自含义，区别



SpEL（Spring Expression Language）是 Spring Framework 提供的一种表达式语言，它可以用于在运行时动态地计算表达式。SpEL 中的表达式可以包括变量、属性、方法调用、算术运算、关系运算、逻辑运算等。

在 SpEL 中，有多种类型的表达式可以使用，包括 CompositeStringExpression、LiteralExpression、SpelExpression 等。它们之间的区别如下：

- CompositeStringExpression 是一种字符串表达式，它可以包含多个子表达式，并使用占位符来代表子表达式。例如，表达式 "${name} is ${age} years old." 就是一个 CompositeStringExpression。在计算该表达式时，SpEL 会将占位符中的子表达式计算出来，并将它们替换到原始字符串中。
- LiteralExpression 是一种字面量表达式，它表示一个常量值。例如，表达式 "3" 或 "'hello world'" 就是一种 LiteralExpression。在计算该表达式时，SpEL 直接返回该常量值。
- SpelExpression 是一种通用的表达式，它可以包括变量、属性、方法调用、算术运算、关系运算、逻辑运算等。例如，表达式 "person.name"、"person.getAge()"、"1 + 2" 等都是 SpelExpression。在计算该表达式时，SpEL 会根据表达式的类型进行相应的计算。

总之，CompositeStringExpression、LiteralExpression、SpelExpression 都是 SpEL 中常用的表达式类型。它们分别用于表示字符串表达式、字面量表达式和通用表达式，并在计算表达式时提供不同的功能。







org.springframework.expression.spel.ast.Operator 是 Spring Expression Language（SpEL）中定义的一个枚举类型，它表示了 SpEL 中支持的运算符。Operator 枚举类型包括了所有基本运算符，如算术运算、关系运算、逻辑运算等。在 SpEL 中，Operator 用于表示表达式中的运算符，可以用于在运行时动态地计算表达式。

Operator 枚举类型的常量包括：

- ADD：加法运算符（+）
- SUBTRACT：减法运算符（-）
- MULTIPLY：乘法运算符（*）
- DIVIDE：除法运算符（/）
- MODULUS：取模运算符（%）
- POWER：乘方运算符（^）
- EQUALS：等于运算符（==）
- NOT_EQUALS：不等于运算符（!=）
- LESS_THAN：小于运算符（<）
- LESS_THAN_OR_EQUAL：小于等于运算符（<=）
- GREATER_THAN：大于运算符（>）
- GREATER_THAN_OR_EQUAL：大于等于运算符（>=）
- NOT：逻辑非运算符（!）
- AND：逻辑与运算符（&&）
- OR：逻辑或运算符（||）
- ELVIS：Elvis 运算符（?:）
- SAFE_NAVI：安全导航运算符（?.）

在 SpEL 中，可以使用 Operator 枚举类型来表示表达式中的运算符，例如：

- "1 + 2" 中的运算符是 Operator.ADD
- "a > b" 中的运算符是 Operator.GREATER_THAN

总之，Operator 枚举类型是 SpEL 中定义的一个枚举类型，它表示了 SpEL 中支持的运算符。在 SpEL 中，可以使用 Operator 枚举类型来表示表达式中的运算符，并在运行时动态地计算表达式。







`StandardTypeLocator` 是 SpEL（Spring Expression Language）中的一个类型定位器，用于定位类型的位置并提供对这些类型的访问。它主要用于在表达式求值过程中解析和加载类型。

作用：
- 定位和加载类型：`StandardTypeLocator` 可以根据给定的类型名称查找并加载相应的类型。它提供了一种机制，通过指定类型名称来获取对应的类型对象。

用法例子：
```java
StandardTypeLocator typeLocator = new StandardTypeLocator();
Class<?> type = typeLocator.findType("java.lang.String");
```

在上述例子中，我们创建了一个 `StandardTypeLocator` 对象，并使用 `findType` 方法查找类型名称为 "java.lang.String" 的类型。该方法会返回一个 `Class<?>` 对象，表示找到的类型。

`StandardTypeLocator` 还可以通过配置自定义的类型映射，以便在查找类型时使用自定义的映射关系。例如，我们可以将某个自定义的类型名称映射到特定的类型对象：
```java
StandardTypeLocator typeLocator = new StandardTypeLocator();
typeLocator.registerType("MyType", com.example.MyType.class);
Class<?> type = typeLocator.findType("MyType");
```

上述代码中，我们使用 `registerType` 方法将自定义的类型名称 "MyType" 注册到 `StandardTypeLocator` 中，并指定对应的类型对象。之后，通过 `findType` 方法查找类型名称 "MyType"，将返回注册的类型对象 `com.example.MyType.class`。

通过 `StandardTypeLocator` 可以方便地定位和获取类型对象，使得 SpEL 表达式可以在运行时访问和操作各种类型的数据。







