# spring expression





https://docs.spring.io/spring-framework/docs/5.3.x/javadoc-api/





以下是一些 SpEL 表达式的例子：

* 计算两个数字的和：`#{1 + 2}`
* 访问对象的属性：`#{user.name}`
* 调用方法：`#{user.getName()}`
* 使用内置函数：`#{T(java.lang.Math).sqrt(4)}`
* 使用用户自定义函数：`#{myFunction(arg1, arg2)}`

你可以在 Spring 的官方文档中找到更多关于 SpEL 表达式的介绍：[spring-framework expressions ↗](https://docs.spring.io/spring-framework/docs/current/reference/html/core.html#expressions)



核心类：



- Expression
- ExpressionParser
- EvaluationContext ParserContex
- xxxResolver MethodResolver ConstructorResolver
- xxxExecutor  ConstructorExecutor MethodExecutor





Expression接口实现类

SpelExpression (org.springframework.expression.spel.standard)
CompositeStringExpression (org.springframework.expression.common)
LiteralExpression (org.springframework.expression.common)





ExpressionParser接口实现类

TemplateAwareExpressionParser (org.springframework.expression.common)
    InternalSpelExpressionParser (org.springframework.expression.spel.standard)
    SpelExpressionParser (org.springframework.expression.spel.standard)



EvaluationContext 接口实现类

StandardEvaluationContext (org.springframework.expression.spel.support)
    MethodBasedEvaluationContext (org.springframework.context.expression)
        CacheEvaluationContext (org.springframework.cache.interceptor)
SimpleEvaluationContext (org.springframework.expression.spel.support)



ParserContext接口实现类

TemplateParserContext (org.springframework.expression.common)
Anonymous in ParserContext (org.springframework.expression)
Anonymous in StandardBeanExpressionResolver (org.springframework.context.expression)



PropertyAccessor接口实现类

ReflectivePropertyAccessor (org.springframework.expression.spel.support)
    DataBindingPropertyAccessor (org.springframework.expression.spel.support)
BeanFactoryAccessor (org.springframework.context.expression)
EnvironmentAccessor (org.springframework.context.expression)
BeanExpressionContextAccessor (org.springframework.context.expression)
CompilablePropertyAccessor (org.springframework.expression.spel)
    MapAccessor (org.springframework.context.expression)
    OptimalPropertyAccessor in ReflectivePropertyAccessor (org.springframework.expression.spel.support)



`PropertyAccessor` 接口的实现类有以下几个：

1. `ReflectivePropertyAccessor` (org.springframework.expression.spel.support)
   ```ReflectivePropertyAccessor` 是 Spring Expression Language（SpEL）中最常用的 `PropertyAccessor` 实现类之一。它使用 Java 反射 API 访问对象的属性，可以访问公共、私有和受保护的属性。此外，`ReflectivePropertyAccessor` 还支持方法调用和数组索引访问，可以用于访问基本类型、对象和集合类型的属性。

2. `DataBindingPropertyAccessor` (org.springframework.expression.spel.support)
   ```DataBindingPropertyAccessor` 是一个支持数据绑定的 `PropertyAccessor` 实现类，可以将表达式结果绑定到对象的属性上。它使用 Spring 的数据绑定框架进行属性绑定，可以实现自动类型转换和格式化。

3. `BeanFactoryAccessor` (org.springframework.context.expression)
   ```BeanFactoryAccessor` 是一个用于访问 Spring Bean 工厂中的对象的 `PropertyAccessor` 实现类。它支持通过 Bean 名称和类型进行对象查找，并可以访问 Bean 的属性和方法。

4. `EnvironmentAccessor` (org.springframework.context.expression)
   ```EnvironmentAccessor` 是一个用于访问 Spring 环境变量和属性的 `PropertyAccessor` 实现类。它可以访问系统属性、环境变量和 Spring 配置文件中定义的属性。

5. `BeanExpressionContextAccessor` (org.springframework.context.expression)
   ```BeanExpressionContextAccessor` 是一个用于访问 Spring Bean 表达式上下文中的对象的 `PropertyAccessor` 实现类。它可以访问 Bean 表达式上下文中定义的属性和方法。

6. `CompilablePropertyAccessor` (org.springframework.expression.spel)
   ```CompilablePropertyAccessor` 是一个支持编译的 `PropertyAccessor` 实现类，可以将表达式编译成 Java 代码，提高表达式的执行效率。它是 `PropertyAccessor` 接口的一个扩展，需要实现 `compile(PropertyAccessor) ` 方法。

7. `MapAccessor` (org.springframework.context.expression)
   ```MapAccessor` 是一个用于访问 Map 对象的 `PropertyAccessor` 实现类。它可以访问 Map 中的键值对，并支持键值对的新增、修改和删除操作。

8. `OptimalPropertyAccessor` in `ReflectivePropertyAccessor` (org.springframework.expression.spel.support)
   ```OptimalPropertyAccessor` 是 `ReflectivePropertyAccessor` 的一个内部类，它使用 Java 8 中的 MethodHandle API 访问对象属性，可以提高访问属性的执行效率。

这些 `PropertyAccessor` 实现类可以根据需要进行选择，以实现对不同类型对象的属性访问。



在 Java 代码中解析 SpEL 表达式可以使用 Spring Expression Language（SpEL）提供的 ExpressionParser 和 EvaluationContext 接口。下面是一个使用 SpEL 解析 "#{user.name}" 表达式的 Java 代码示例：

```java
import org.springframework.expression.Expression;
import org.springframework.expression.ExpressionParser;
import org.springframework.expression.spel.standard.SpelExpressionParser;
import org.springframework.expression.spel.support.StandardEvaluationContext;

public class SpelExample {
    public static void main(String[] args) {
        // 创建一个 ExpressionParser 对象
        ExpressionParser parser = new SpelExpressionParser();

        // 创建一个 EvaluationContext 对象，并设置变量 user 的值
        StandardEvaluationContext context = new StandardEvaluationContext();
        User user = new User("John", 25);
        context.setVariable("user", user);

        // 解析 SpEL 表达式
        Expression expression = parser.parseExpression("#user.name");

        // 计算表达式的值
        String name = expression.getValue(context, String.class);

        // 输出结果
        System.out.println("User name: " + name);
    }

    private static class User {
        private String name;
        private int age;

        public User(String name, int age) {
            this.name = name;
            this.age = age;
        }

        public String getName() {
            return name;
        }

        public int getAge() {
            return age;
        }
    }
}
```

在上面的示例代码中，我们首先创建了一个 ExpressionParser 对象，用于解析 SpEL 表达式。然后创建一个 StandardEvaluationContext 对象，并设置变量 user 的值为一个 User 对象。接着，使用 ExpressionParser 对象解析 SpEL 表达式，并得到一个 Expression 对象。最后，通过调用 Expression 对象的 getValue() 方法，计算表达式的值，并将结果赋值给一个 String 类型的变量 name。

在计算表达式的过程中，SpEL 会根据表达式中的变量名，从 EvaluationContext 对象中查找对应的变量值。在上面的示例中，SpEL 会在 EvaluationContext 对象中查找 user 变量，并获取其 name 属性的值，最后返回该值作为表达式的计算结果。

当我们运行上面的示例代码时，将会输出以下结果：

```
User name: John
```

这个结果表示 SpEL 成功地解析了表达式 "#{user.name}"，并返回了其计算结果，即 User 对象的 name 属性的值。



报错：

```shell
Exception in thread "main" org.springframework.expression.spel.SpelParseException: Expression [#{user.name}] @1: EL1043E: Unexpected token. Expected 'identifier' but was 'lcurly({)'
```



解决

`#user.name`





在 Spring Expression Language（SpEL）中，可以使用 `#` 符号和大括号 `{}` 来调用自定义函数。下面是一个使用自定义函数的 Java 代码示例：

```java
import org.springframework.expression.Expression;
import org.springframework.expression.ExpressionParser;
import org.springframework.expression.spel.standard.SpelExpressionParser;
import org.springframework.expression.spel.support.StandardEvaluationContext;

public class SpelExample {
    public static void main(String[] args) {
        // 创建一个 ExpressionParser 对象
        ExpressionParser parser = new SpelExpressionParser();

        // 创建一个 StandardEvaluationContext 对象
        StandardEvaluationContext context = new StandardEvaluationContext();

        // 将自定义函数注册到 EvaluationContext 中
        context.registerFunction("myFunction", SpelExample.class, "myFunction");

        // 解析 SpEL 表达式
        Expression expression = parser.parseExpression("#{myFunction('Hello', 'World')}");

        // 计算表达式的值
        String result = expression.getValue(context, String.class);
        System.out.println("result: " + result);
    }

    public static String myFunction(String arg1, String arg2) {
        return arg1 + " " + arg2;
    }
}
```

在上面的示例中，我们首先创建了一个 `ExpressionParser` 对象和一个 `StandardEvaluationContext` 对象。然后，我们将自定义函数 `myFunction()` 注册到 `StandardEvaluationContext` 对象中，以便 SpEL 表达式可以调用该函数。接下来，我们使用 `ExpressionParser` 对象解析 SpEL 表达式，并将解析的表达式传递给 `getValue()` 方法进行计算。在计算表达式的值时，我们将 `StandardEvaluationContext` 对象和期望的返回类型 `String.class` 作为参数传递给 `getValue()` 方法。最后，我们输出计算结果。

当我们运行上面的示例代码时，将会输出以下结果：

```
result: Hello World
```

这个结果表明，我们成功地使用自定义函数 `myFunction()` 计算了 SpEL 表达式 `#{myFunction('Hello', 'World')}` 的值。





## 源代码分包解析v5.2.9



### org.springframework.expression

| org.springframework.expression                               | package  |                                                              |
| ------------------------------------------------------------ | -------- | ------------------------------------------------------------ |
| Interfaces                                                   |          |                                                              |
| BeanResolver                                                 |          | Object resolve(EvaluationContext context, String beanName)   |
| ConstructorExecutor                                          |          | TypedValue execute(EvaluationContext context, Object... arguments)  唯一实现类ReflectiveConstructorExecutor |
| ConstructorResolver                                          |          |                                                              |
| EvaluationContext                                            |          | 接口实现类SimpleEvaluationContext StandardEvaluationContext MethodBasedEvaluationContext |
| Expression                                                   |          | String getExpressionString()  getValue() isWritable()  实现接口的类 SpelExpression CompositeStringExpression  LiteralExpression |
| ExpressionParser                                             |          | Expression parseExpression(String expressionString)  Expression parseExpression(String expressionString, ParserContext context) |
| MethodExecutor                                               |          | TypedValue execute(EvaluationContext context, Object target, Object... arguments) |
| MethodFilter                                                 |          | boolean isHandled(Method m)                                  |
| MethodResolver                                               |          | MethodExecutor resolve(EvaluationContext context, Object targetObject, String name,<br/>       List<TypeDescriptor> argumentTypes) |
| OperatorOverloader                                           |          | boolean overridesOperation(Operation operation, @Nullable Object leftOperand, @Nullable Object rightOperand)   Object operate(Operation operation, @Nullable Object leftOperand, @Nullable Object rightOperand) |
| ParserContext                                                |          | boolean isTemplate()   String getExpressionPrefix()  String getExpressionSuffix() |
| PropertyAccessor                                             |          | 实现类 ReflectivePropertyAccessor                            |
| TypeComparator                                               |          | StandardTypeComparator    boolean canCompare(@Nullable Object firstObject, @Nullable Object secondObject)  int compare(@Nullable Object firstObject, @Nullable Object secondObject) |
| TypeConverter                                                |          | StandardTypeConverter   <T> T convertIfNecessary(@Nullable Object value, @Nullable Class<T> requiredType,<br/>       @Nullable MethodParameter methodParam)       <T> T convertIfNecessary(@Nullable Object value, @Nullable Class<T> requiredType) |
| TypeLocator                                                  |          | Class<?> findType(String typeName)                           |
|                                                              |          |                                                              |
| Classes                                                      |          |                                                              |
| TypedValue                                                   |          | TypeDescriptor                                               |
|                                                              |          |                                                              |
| Enums                                                        |          |                                                              |
| Operation                                                    | enum     | ADD等值                                                      |
|                                                              |          |                                                              |
| Exceptions                                                   |          |                                                              |
| AccessException                                              |          |                                                              |
| EvaluationException                                          |          |                                                              |
| ExpressionException                                          |          |                                                              |
| ExpressionInvocationTargetException                          |          |                                                              |
| ParseException                                               |          |                                                              |
|                                                              |          |                                                              |


#### org.springframework.expression.common

| org.springframework.expression.common | package  |                                                              |
| ------------------------------------- | -------- | ------------------------------------------------------------ |
| Classes                               |          |                                                              |
| CompositeStringExpression             |          | implements Expression 核心方法 getValue()                    |
| ExpressionUtils                       | abstract | 抽象类，都是静态方法                                         |
| LiteralExpression                     |          | 字面常量表达式 例子见后续代码                                |
| TemplateAwareExpressionParser         | abstract | abstract Expression doParseExpression(String expressionString, @Nullable ParserContext context)  子类InternalSpelExpressionParser SpelExpressionParser |
| TemplateParserContext                 |          | implements ParserContext 属性 String expressionPrefix  String expressionSuffix |
|                                       |          |                                                              |
|                                       |          |                                                              |



#### org.springframework.expression.spel






| org.springframework.expression.spel                          | package  |                                                              |
| ------------------------------------------------------------ | -------- | ------------------------------------------------------------ |
| Interfaces                                                   |          |                                                              |
| CodeFlow.ClinitAdder                                         |          |                                                              |
| CodeFlow.FieldAdder                                          |          |                                                              |
| CompilablePropertyAccessor                                   |          | extends PropertyAccessor, Opcodes                            |
| SpelNode                                                     |          |                                                              |
|                                                              |          |                                                              |
| Classes                                                      |          |                                                              |
| CodeFlow                                                     |          | implements Opcodes                                           |
| CompiledExpression                                           | abstract | Object getValue(@Nullable Object target, @Nullable EvaluationContext context) |
| ExpressionState                                              |          | 解析和评估表达式。封装了表达式的执行环境和状态。             |
| SpelParserConfiguration                                      |          | SpEL 解析器的配置类。它提供了对 SpEL 解析器的各种配置选项的访问，包括解析器的语言版本、解析器的扩展功能、解析器的错误处理策略等。 |
|                                                              |          |                                                              |
| Enums                                                        |          |                                                              |
| SpelCompilerMode                                             |          |                                                              |
| SpelMessage                                                  |          |                                                              |
| SpelMessage.Kind                                             |          |                                                              |
|                                                              |          |                                                              |
| Exceptions                                                   |          |                                                              |
| InternalParseException                                       |          |                                                              |
| SpelEvaluationException                                      |          |                                                              |
| SpelParseException                                           |          |                                                              |
|                                                              |          |                                                              |
|                                                              |          |                                                              |



##### org.springframework.expression.spel.ast 





| org.springframework.expression.spel.ast                      | package  |                                                              |
| ------------------------------------------------------------ | -------- | ------------------------------------------------------------ |
|                                                              |          |                                                              |
| Interfaces                                                   |          |                                                              |
|                                                              |          |                                                              |
| ValueRef                                                     |          | org.springframework.expression.spel.ast.ValueRef.NullValueRef  TypedValueHolderValueRef   实现这个接口的类都是内部类 方法 getValue setValue isWriable |
|                                                              |          |                                                              |
| Classes                                                      |          |                                                              |
| Assign                                                       |          |                                                              |
| AstUtils                                                     | abstract |                                                              |
| BeanReference                                                |          | extends SpelNodeImpl     TypedValue getValueInternal(ExpressionState state) |
| BooleanLiteral                                               |          | extends Literal                                              |
| CompoundExpression                                           |          |                                                              |
| ConstructorReference                                         |          |                                                              |
| Elvis                                                        |          |                                                              |
| FloatLiteral                                                 |          |                                                              |
| FunctionReference                                            |          |                                                              |
| Identifier                                                   |          |                                                              |
| Indexer                                                      |          |                                                              |
| InlineList                                                   |          |                                                              |
| InlineMap                                                    |          |                                                              |
| IntLiteral                                                   |          |                                                              |
| Literal                                                      | abstract | extends SpelNodeImpl   Literal 是 Groovy 中表示常量值的类    |
| LongLiteral                                                  |          |                                                              |
| MethodReference                                              |          |                                                              |
| NullLiteral                                                  |          |                                                              |
| OpAnd                                                        |          | true and false                                               |
| OpDec                                                        |          |                                                              |
| OpDivide                                                     |          |                                                              |
| OpEQ                                                         |          |                                                              |
| Operator                                                     |          |                                                              |
| Operator.DescriptorComparison                                |          |                                                              |
| OperatorBetween                                              |          |                                                              |
| OperatorInstanceof                                           |          |                                                              |
| OperatorMatches                                              |          |                                                              |
| OperatorNot                                                  |          |                                                              |
| OperatorPower                                                |          |                                                              |
| OpGE                                                         |          |                                                              |
| OpGT                                                         |          |                                                              |
| OpInc                                                        |          |                                                              |
| OpLE                                                         |          |                                                              |
| OpLT                                                         |          |                                                              |
| OpMinus                                                      |          |                                                              |
| OpModulus                                                    |          |                                                              |
| OpMultiply                                                   |          |                                                              |
| OpNE                                                         |          |                                                              |
| OpOr                                                         |          |                                                              |
| OpPlus                                                       |          | 1+2                                                          |
| Projection                                                   |          |                                                              |
| PropertyOrFieldReference                                     |          |                                                              |
| QualifiedIdentifier                                          |          |                                                              |
| RealLiteral                                                  |          |                                                              |
| Selection                                                    |          |                                                              |
| SpelNodeImpl                                                 | abstract |                                                              |
| StringLiteral                                                |          |                                                              |
| Ternary                                                      |          |                                                              |
| TypeReference                                                |          |                                                              |
| ValueRef.NullValueRef                                        |          |                                                              |
| ValueRef.TypedValueHolderValueRef                            |          |                                                              |
| VariableReference                                            |          | TypeReference ConstructorReference  FunctionReference BeanReference  MethodReference   PropertyOrFieldReference  CompoundExpression |
|                                                              |          |                                                              |
| Enums                                                        |          |                                                              |
|                                                              |          |                                                              |
| TypeCode                                                     |          |                                                              |
|                                                              |          |                                                              |
|                                                              |          |                                                              |
|                                                              |          |                                                              |


在 Spring 5.2.9 版本中，位于 `org.springframework.expression.spel.ast` 包下的类是 Spring Expression Language (SpEL) 的抽象语法树（AST）节点类。SpEL 是 Spring 框架中的表达式语言，用于在运行时对对象进行求值和操作。这些类表示了 SpEL 表达式的不同组成部分和操作。以下是该包下一些常见类的简要说明：

1. **AstNode**：
   `AstNode` 是所有 AST 节点类的基类。它提供了一些共享的方法和属性，如获取和设置节点位置信息。

2. **BooleanLiteral**：
   `BooleanLiteral` 用于表示布尔字面值（true 或 false）的节点。

3. **CompositeStringNode**：
   `CompositeStringNode` 用于表示复合字符串节点，即包含表达式的字符串。例如，`"Hello ${name}"` 中的 `${name}` 就是一个复合字符串节点。

4. **ConstructorReference**：
   `ConstructorReference` 用于表示构造函数引用的节点。它指示要使用的构造函数及其参数。

5. **Indexer**：
   `Indexer` 用于表示索引器访问的节点，例如数组或集合的索引访问。

6. **MethodReference**：
   `MethodReference` 用于表示方法引用的节点。它指示要调用的方法及其参数。

7. **NullLiteral**：
   `NullLiteral` 用于表示空字面值（null）的节点。

8. **PropertyOrFieldReference**：
   `PropertyOrFieldReference` 用于表示属性或字段引用的节点。它指示要访问的属性或字段的名称。

9. **ThisReference**：
   `ThisReference` 用于表示当前对象引用的节点。它表示当前正在求值的对象。

10. **TypeReference**：
    `TypeReference` 用于表示类型引用的节点。它指示要使用的类或接口的名称。

这些类只是 `org.springframework.expression.spel.ast` 包下的一部分，用于构建 SpEL 表达式的抽象语法树。它们提供了处理和解析表达式的基础结构和功能。如果你需要更详细的信息，建议查阅 Spring Framework 的官方文档或相关资源。


##### org.springframework.expression.spel.standard 







| org.springframework.expression.spel.standard                 |      |                                                              |
| ------------------------------------------------------------ | ---- | ------------------------------------------------------------ |
| Classes                                                      |      |                                                              |
| InternalSpelExpressionParser                                 |      | 构造函数 public InternalSpelExpressionParser(SpelParserConfiguration configuration)   很多 eatxxx()方法  非public ，class InternalSpelExpressionParser extends TemplateAwareExpressionParser 核心类 |
| SpelCompiler                                                 |      |                                                              |
| org.springframework.expression.spel.standard.SpelCompiler.ChildClassLoader |      |                                                              |
| org.springframework.expression.spel.standard.SpelCompiler.ExpressionClassWriter |      |                                                              |
| SpelExpression                                               |      |                                                              |
| SpelExpressionParser                                         |      | 父类TemplateAwareExpressionParser                            |
| Token                                                        |      |                                                              |
| Tokenizer                                                    |      |                                                              |



InternalSpelExpressionParser大量使用org.springframework.expression.spel.ast包下面的类


##### org.springframework.expression.spel.support 



| org.springframework.expression.spel.support        |      |                                                              |
| -------------------------------------------------- | ---- | ------------------------------------------------------------ |
| Classes                                            |      |                                                              |
|                                                    |      |                                                              |
| BooleanTypedValue                                  |      |                                                              |
| DataBindingMethodResolver                          |      | final class DataBindingMethodResolver extends ReflectiveMethodResolver 见文字 |
| DataBindingPropertyAccessor                        |      | 实现PropertyAccessor接口                                     |
| ReflectionHelper                                   |      | 静态工具类，org.springframework.expression.spel.support.ReflectiveConstructorExecutor#execute |
| ReflectiveConstructorExecutor                      |      | execute()                                                    |
| ReflectiveConstructorResolver                      |      |                                                              |
| ReflectiveMethodExecutor                           |      |                                                              |
| ReflectiveMethodResolver                           |      |                                                              |
| ReflectivePropertyAccessor                         |      | DataBindingPropertyAccessor extends ReflectivePropertyAccessor |
| ReflectivePropertyAccessor.OptimalPropertyAccessor |      |                                                              |
| SimpleEvaluationContext                            |      | 简化的表达式求值上下文，它提供了最基本的配置选项             |
| SimpleEvaluationContext.Builder                    |      |                                                              |
| StandardEvaluationContext                          |      | 可配置的表达式求值上下文                                     |
| StandardOperatorOverloader                         |      | implements OperatorOverloader                                |
| StandardTypeComparator                             |      | implements TypeComparator                                    |
| StandardTypeConverter                              |      | implements TypeConverter  核心方法 convertValue              |
| StandardTypeLocator                                |      | implements TypeLocator                                       |





在 Spring Expression Language（SpEL）中，StandardTypeConverter 是一个用于类型转换的转换器，可以将一个对象从一种类型转换为另一种类型。下面是一个使用 StandardTypeConverter 的 Java 代码示例：

```java
import org.springframework.core.convert.TypeDescriptor;
import org.springframework.expression.spel.support.StandardTypeConverter;

public class SpelExample {
    public static void main(String[] args) {
        // 创建一个 StandardTypeConverter 对象
        StandardTypeConverter converter = new StandardTypeConverter();

        // 将字符串转换为整数
        Object intValue = converter.convertValue("123", TypeDescriptor.valueOf(String.class), TypeDescriptor.valueOf(Integer.class));
        System.out.println("intValue: " + intValue);

        // 将整数转换为字符串
        Object stringValue = converter.convertValue(456, TypeDescriptor.valueOf(Integer.class), TypeDescriptor.valueOf(String.class));
        System.out.println("stringValue: " + stringValue);
    }
}
```

在上面的示例中，我们首先创建了一个 StandardTypeConverter 对象。然后，我们使用 StandardTypeConverter 对象将一个字符串转换为整数，以及将一个整数转换为字符串。在将字符串转换为整数时，我们使用了 convertIfNecessary() 方法，该方法会根据需要将输入的字符串转换为 Integer 类型。在将整数转换为字符串时，我们同样使用了 convertIfNecessary() 方法，该方法会根据需要将输入的整数转换为 String 类型。

当我们运行上面的示例代码时，将会输出以下结果：

```
intValue: 123
stringValue: 456
```

这个结果表明，我们成功地使用 StandardTypeConverter 将一个字符串转换为整数，并将一个整数转换为字符串。





```java
        // 创建一个 ExpressionParser 对象
        ExpressionParser parser = new SpelExpressionParser();

        // 创建一个 LiteralExpression 对象
        Expression expression = parser.parseExpression("'Hello, World!'");

        // 计算表达式的值
        String message = expression.getValue(String.class);

        // 输出结果
        System.out.println(message);
```





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





在 Spring Expression Language（SpEL）中，DataBindingMethodResolver 和 ReflectiveMethodResolver 都是用于解析方法调用的类，它们之间的主要区别如下：

1. 解析方式不同：DataBindingMethodResolver 是基于数据绑定的方法解析器，它会根据目标对象的属性名称来查找方法，通常用于从 JavaBean 或 Map 对象中获取属性值；而 ReflectiveMethodResolver 是基于反射的方法解析器，它会根据方法名称和参数类型来查找方法，通常用于调用对象的方法。

2. 解析效率不同：DataBindingMethodResolver 的效率相对较低，因为它需要使用反射来获取方法的参数类型和返回值类型；而 ReflectiveMethodResolver 的效率相对较高，因为它只需要根据方法名称和参数类型来查找方法，不需要获取方法的参数类型和返回值类型。

3. 使用场景不同：DataBindingMethodResolver 通常用于从 JavaBean 或 Map 对象中获取属性值，例如 `person.getName()`；而 ReflectiveMethodResolver 通常用于调用对象的方法，例如 `person.sayHello()`。

两种方法解析器在 SpEL 中都有各自的应用场景，并且可以相互配合使用。在 SpEL 中，当解析表达式时，它会根据表达式中的方法调用和对象属性访问等信息，选择合适的方法解析器进行方法调用和属性访问等操作。

总之，DataBindingMethodResolver 和 ReflectiveMethodResolver 都是 SpEL 中用于解析方法调用的类，它们之间的主要区别在于解析方式、解析效率和使用场景等方面。理解它们之间的差异有助于我们更好地理解 SpEL 中方法调用的实现机制，从而更好地使用 SpEL 来处理复杂的表达式。







