# springboot_log

默认使用
spring-boot-starter-logging
对应slf4j + logback

如果要使用log4j2
spring-boot-starter-log4j2


Spring Boot使用Logback作为默认的日志框架，因此配置日志需要对Logback进行配置。

在Spring Boot中，可以通过在`application.properties`或`application.yml`文件中配置日志属性来控制日志输出。以下是一个示例`application.properties`文件，其中包含一些常见的日志配置属性：

```properties
# 日志级别配置
logging.level.root=INFO
logging.level.com.example=DEBUG

# 控制台输出配置
logging.pattern.console=%d{HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n
logging.console.enabled=true

# 文件输出配置
logging.file.name=myapp.log
logging.file.path=/var/log/myapp
logging.pattern.file=%d{yyyy-MM-dd HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n
logging.file.max-size=10MB
logging.file.max-history=7
```

在上面的示例中，`logging.level.root`属性设置了根日志记录器的日志级别为`INFO`，而`logging.level.com.example`属性设置了名为`com.example`的日志记录器的日志级别为`DEBUG`。可以根据自己的需要修改这些值。

`logging.pattern.console`属性和`logging.pattern.file`属性分别控制控制台输出和文件输出的日志格式。可以使用特定的格式化符号来定义自己的日志格式，例如`%d{HH:mm:ss.SSS}`表示输出日志的时间，`%thread`表示输出日志的线程名称，`%-5level`表示输出日志的级别，`%logger{36}`表示输出日志的记录器名称（最多显示36个字符），`%msg%n`表示输出日志的消息和换行符。

`logging.console.enabled`属性设置是否启用控制台输出。

`logging.file.name`属性和`logging.file.path`属性分别设置输出日志文件的名称和目录。`logging.file.max-size`属性和`logging.file.max-history`属性分别设置日志文件的最大大小和最大历史版本数。

除了在`application.properties`或`application.yml`文件中配置日志属性外，还可以通过编程方式配置日志。例如，可以使用`LoggerFactory`类获取日志记录器，并设置日志级别和输出格式等属性。


### spring-boot-starter-logging项目如何使用logback打印日志

logback-spring.xml

### 使用slf4j+logback
去掉spring-jcl


        <!--common-logging替换成slf4j-->
        <dependency>
            <groupId>org.slf4j</groupId>
            <artifactId>jcl-over-slf4j</artifactId>
            <version>1.7.25</version>
        </dependency>


application.properties设置

spring.profiles.active=dev

logback-spring.xml



