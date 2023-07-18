# spring expression




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
| Operation                                          |          |                                                              |
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
| CompositeStringExpression                          |          |                                                              |
| ExpressionUtils                                    |          |                                                              |
| LiteralExpression                                  |          | 字面常量表达式                                               |
| TemplateAwareExpressionParser                      | abstract | abstract Expression doParseExpression(String expressionString, @Nullable ParserContext context)  子类InternalSpelExpressionParser SpelExpressionParser |
| TemplateParserContext                              |          |                                                              |
|                                                    |          |                                                              |
|                                                    |          |                                                              |
|                                                    |          |                                                              |
| org.springframework.expression.spel                | package  |                                                              |
| Interfaces                                         |          |                                                              |
| CodeFlow.ClinitAdder                               |          |                                                              |
| CodeFlow.FieldAdder                                |          |                                                              |
| CompilablePropertyAccessor                         |          |                                                              |
| SpelNode                                           |          |                                                              |
|                                                    |          |                                                              |
| Classes                                            |          |                                                              |
| CodeFlow                                           |          |                                                              |
| CompiledExpression                                 |          |                                                              |
| ExpressionState                                    |          |                                                              |
| SpelParserConfiguration                            |          |                                                              |
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
|                                                    |          |                                                              |
| Assign                                             |          |                                                              |
| AstUtils                                           |          |                                                              |
| BeanReference                                      |          |                                                              |
| BooleanLiteral                                     |          |                                                              |
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
| Literal                                            |          |                                                              |
| LongLiteral                                        |          |                                                              |
| MethodReference                                    |          |                                                              |
| NullLiteral                                        |          |                                                              |
| OpAnd                                              |          |                                                              |
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
| OpPlus                                             |          |                                                              |
| Projection                                         |          |                                                              |
| PropertyOrFieldReference                           |          |                                                              |
| QualifiedIdentifier                                |          |                                                              |
| RealLiteral                                        |          |                                                              |
| Selection                                          |          |                                                              |
| SpelNodeImpl                                       |          |                                                              |
| StringLiteral                                      |          |                                                              |
| Ternary                                            |          |                                                              |
| TypeReference                                      |          |                                                              |
| ValueRef.NullValueRef                              |          |                                                              |
| ValueRef.TypedValueHolderValueRef                  |          |                                                              |
| VariableReference                                  |          |                                                              |
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
| SimpleEvaluationContext                            |          |                                                              |
| SimpleEvaluationContext.Builder                    |          |                                                              |
| StandardEvaluationContext                          |          |                                                              |
| StandardOperatorOverloader                         |          |                                                              |
| StandardTypeComparator                             |          |                                                              |
| StandardTypeConverter                              |          |                                                              |
| StandardTypeLocator                                |          |                                                              |







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



