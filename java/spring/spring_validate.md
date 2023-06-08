# spring validate

org.springframework.lang.Nullable
`org.springframework.lang.Nullable` 注解是 Spring 框架提供的用于标识方法参数、返回值、属性等可以为 null 的元素的注解。该注解的主要作用是为了提高代码的可读性和可维护性，方便开发人员对代码进行理解和修改。
通过使用 `@Nullable` 注解，可以明确表明这些元素允许为 null，从而在代码中更加明确地描述和约束元素的含义和使用方式。同时，在使用 `@Nullable` 注解后，一些代码检查工具也可以通过该注解来检查和报告代码中潜在的空指针异常问题，从而提高代码的健壮性和可靠性。
如果想要 `@Nullable` 注解生效，需要在项目中引入 Spring 的依赖，并且在编译时开启注解处理器（Annotation Processor）。在 Maven 项目中，可以在 `pom.xml` 文件中添加以下依赖和插件配置：

```xml
<dependencies>
    <dependency>
        <groupId>org.springframework</groupId>
        <artifactId>spring-context</artifactId>
        <version>5.3.8</version>
    </dependency>
</dependencies>

<build>
    <plugins>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-compiler-plugin</artifactId>
            <version>3.8.1</version>
            <configuration>
                <source>1.8</source>
                <target>1.8</target>
                <annotationProcessorPaths>
                    <path>
                        <groupId>org.springframework</groupId>
                        <artifactId>spring-context</artifactId>
                        <version>5.3.8</version>
                    </path>
                </annotationProcessorPaths>
            </configuration>
        </plugin>
    </plugins>
</build>
```

在上述配置中，我们通过 `annotationProcessorPaths` 配置项指定了 Spring 依赖的路径，并且在 `maven-compiler-plugin` 插件中开启了注解处理器。这样，在编译时，就会使用 Spring 提供的注解处理器来处理 `@Nullable` 注解，从而让该注解生效。

需要注意的是，不同的构建工具和框架可能需要不同的配置方式。在使用其他构建工具或框架时，需要根据具体的情况进行配置。

这本书 3.3章讲这个
https://book.douban.com/subject/35400215/


https://gitee.com/edidada/testvalidate
Spring中使用


https://gitee.com/edidada/testvalidation
这个项目是在java se中使用的

自定义注解去验证
实现ConstraintValidator接口
javax.validation.ConstraintValidator

Author是自定义注解

```java
package cn.wdidada.testvalidate.web.interfaces;

import javax.validation.ConstraintValidator;
import javax.validation.ConstraintValidatorContext;
import java.util.Arrays;
import java.util.List;

public class AuthorValidator implements ConstraintValidator<Author,String> {
    @Override
    public void initialize(Author author) {

    }
    private final List<String> VALID_AUTHORS = Arrays.asList("meimeihan", "leili");

    @Override
    public boolean isValid(String s, ConstraintValidatorContext constraintValidatorContext) {
        return VALID_AUTHORS.contains(s);
    }
}
```


### 校验的使用场景

校验springmvc的http入参
从spring ioc容器中获取LocalValidatorFactoryBean对象，校验任何你想校验的对象，使用spring框架的dubbo项目也可以用LocalValidatorFactoryBean来校验

LocalValidatorFactoryBean extends SpringValidatorAdapter
SpringValidatorAdapter implements SmartValidator, javax.validation.Validator
SmartValidator extends Validator

`SpringValidatorAdapter` 是 Spring Framework 中的一个类，它提供了一种将 Spring 验证器（`org.springframework.validation.Validator`）转换为 `javax.validation.Validator` 的适配器。

具体来说，`SpringValidatorAdapter` 可以将一个实现了 `org.springframework.validation.Validator` 接口的 Spring 验证器转换为一个 `javax.validation.Validator` 实例。这样，你就可以在 Spring 应用程序中使用标准的 JSR 303（Bean Validation）注解进行验证，并使用 Spring 验证器提供的扩展和增强功能。

以下是一个使用 `SpringValidatorAdapter` 进行 Bean 验证的示例：

```java
@Autowired
private Validator springValidator;

@Bean
public Validator validator() {
    return new SpringValidatorAdapter(springValidator);
}

public void savePerson(Person person) {
    Set<ConstraintViolation<Person>> violations = validator().validate(person);
    if (!violations.isEmpty()) {
        // handle validation errors
    } else {
        // save the person
    }
}
```

在上述示例中，我们首先注入一个实现了 `org.springframework.validation.Validator` 接口的 Spring 验证器（`springValidator`），然后使用 `SpringValidatorAdapter` 将它转换为一个 `javax.validation.Validator` 实例，并将其定义为一个 Spring Bean（`validator()` 方法）。
最后，我们可以在 `savePerson` 方法中使用 `javax.validation.Validator` 实例来验证 `Person` 对象，并根据需要进行处理。
总之，`SpringValidatorAdapter` 是 Spring Framework 中的一个类，它提供了将 Spring 验证器转换为 `javax.validation.Validator` 的适配器。它可以使得你在 Spring 应用程序中使用标准的 JSR 303（Bean Validation）注解进行验证，并使用 Spring 验证器提供的扩展和增强功能。



要在 Spring IoC 容器中使用 `validation-api` 对 Bean 进行校验，你可以按照以下步骤进行操作：
1. 添加 Maven 依赖
首先，你需要在你的项目中添加 `validation-api` 和 `hibernate-validator` 的 Maven 依赖项，例如：

```xml
<dependency>
    <groupId>javax.validation</groupId>
    <artifactId>validation-api</artifactId>
    <version>2.0.1.Final</version>
</dependency>

<dependency>
    <groupId>org.hibernate.validator</groupId>
    <artifactId>hibernate-validator</artifactId>
    <version>6.2.0.Final</version>
</dependency>
```

2. 创建验证器工厂
接下来，你需要在 Spring 配置文件中创建一个 `LocalValidatorFactoryBean` 实例作为验证器工厂。例如：
```xml
<bean id="validator" class="org.springframework.validation.beanvalidation.LocalValidatorFactoryBean"/>
```
这将创建一个 `javax.validation.Validator` 实例，它可以用于验证 Bean 对象。
3. 在 Bean 上添加验证注解
然后，你需要在要验证的 Bean 的属性上添加验证注解，例如：
```java
public class Person {
    @NotNull
    private String name;
    @Min(18)
    private int age;
    // getter and setter methods
}
```
在上述示例中，我们使用 `@NotNull` 和 `@Min` 注解来标注 `name` 和 `age` 属性，表示这两个属性不能为空和必须大于或等于 18。
4. 在 Spring 配置文件中开启验证
最后，你需要在 Spring 配置文件中启用 Bean 验证，例如：
```xml
<mvc:annotation-driven validator="validator"/>
```
这将启用基于注解的 Spring MVC 验证，并将使用我们之前创建的 `validator` Bean 进行验证。
现在，你可以在 Bean 对象上调用 `javax.validation.Validator` 实例的 `validate` 方法来执行验证。例如：
```java
@Autowired
private Validator validator;

public void savePerson(Person person) {
    Set<ConstraintViolation<Person>> violations = validator.validate(person);
    if (!violations.isEmpty()) {
        // handle validation errors
    } else {
        // save the person
    }
}
```
在上述示例中，我们使用 `@Autowired` 注解将 `javax.validation.Validator` 实例注入到Spring Bean中，并在 `savePerson` 方法中使用它来验证 `Person` 对象。如果存在验证错误，我们可以根据需要进行处理。
使用`validation-api`对Spring IoC容器中的Bean进行校验的基本步骤。你可以根据实际情况进行调整和扩展。



@Valid
类的属性也校验，加上@Valid
注解

