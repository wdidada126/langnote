# mybatis

https://pagehelper.github.io/

mybatis pagehelper使用直男

https://blog.csdn.net/eson_15/article/details/52270046

1. 需要引入PageHelper的jar包
2. 在mybatis的全局配置文件SqlMapConfig.xml中配置该插件
3. 在执行sql前添加插件，完成分页功能


```xml
<dependency>
    <groupId>com.github.pagehelper</groupId>
    <artifactId>pagehelper</artifactId>
    <version>4.1.4</version>
</dependency>
```


```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE configuration
        PUBLIC "-//mybatis.org//DTD Config 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-config.dtd">
<configuration>
    <!-- 配置分页插件 -->
    <plugins>
        <plugin interceptor="com.github.pagehelper.PageHelper">
            <!-- 设置数据库类型 Oracle,Mysql,MariaDB,SQLite,Hsqldb,PostgreSQL六种数据库-->        
            <property name="dialect" value="mysql"/>
        </plugin>
    </plugins>

</configuration>
```

PageHelper.startPage(1, 10);

注意版本类不一样
配置方式也不一样



pager 5版本



https://qiankunpingtai.cn/article/1562226055379
