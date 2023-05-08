# spring validate
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