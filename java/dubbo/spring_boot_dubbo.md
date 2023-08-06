# dubbo-spring-boot-starter



```xml
      <dependency>
        <groupId>org.apache.dubbo</groupId>
        <artifactId>dubbo-spring-boot-starter</artifactId>
        <version>2.7.8</version>
      </dependency>
```

## 源码分包解析



[dubbo-spring-boot-project/dubbo-spring-boot-starter at master · apache/dubbo-spring-boot-project (github.com)](https://github.com/apache/dubbo-spring-boot-project/tree/master/dubbo-spring-boot-starter)





### autoconfigure jar包 org.apache.dubbo.spring.boot.autoconfigure



| org.apache.dubbo.spring.boot.autoconfigure | 类型 |      |
| ------------------------------------------ | ---- | ---- |
| BinderDubboConfigBinder                    |      |      |
| DubboRelaxedBinding2AutoConfiguration      |      |      |
|                                            |      |      |



### 兼容包org.apache.dubbo.spring.boot.autoconfigure



| org.apache.dubbo.spring.boot.autoconfigure | 类型 |      |
| ------------------------------------------ | ---- | ---- |
| DubboAutoConfiguration                     |      |      |
| DubboConfigurationProperties               |      |      |
| DubboConfigurationProperties.Config        |      |      |
| DubboConfigurationProperties.Scan          |      |      |


### org.apache.dubbo.spring.boot.beans.factory.config




| org.apache.dubbo.spring.boot.beans.factory.config | 类型 |      |
| ------------------------------------------------- | ---- | ---- |
| ServiceBeanIdConflictProcessor                    |      |      |
|                                                   |      |      |
|                                                   |      |      |


### org.apache.dubbo.spring.boot.context




| org.apache.dubbo.spring.boot.context | 类型 |      |
| ------------------------------------------ | ---- | ---- |
| DubboApplicationContextInitializer |      |      |
|                                            |      |      |
|                                            |      |      |



#### org.apache.dubbo.spring.boot.context.event

| org.apache.dubbo.spring.boot.context.event           | 类型 |      |
| ---------------------------------------------------- | ---- | ---- |
| AwaitingNonWebApplicationListener                    |      |      |
| DubboConfigBeanDefinitionConflictApplicationListener |      |      |
| OverrideDubboConfigApplicationListener               |      |      |
| WelcomeLogoApplicationListener                       |      |      |



### org.apache.dubbo.spring.boot.env




| org.apache.dubbo.spring.boot.env | 类型 |      |
| ------------------------------------------ | ---- | ---- |
| DubboDefaultPropertiesEnvironmentPostProcessor |      |      |
|                                            |      |      |
|                                            |      |      |



### org.apache.dubbo.spring.boot.util




| org.apache.dubbo.spring.boot.util | 类型 |      |
| ------------------------------------------ | ---- | ---- |
| DubboUtils |      |      |
| EnvironmentUtils | abstract |      |
|                                            |      |      |


