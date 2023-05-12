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