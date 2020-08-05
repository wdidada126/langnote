# MyBatis从入门到精通



https://book.douban.com/subject/27074809/



Annotatin java1.5加的

mybatis版本3.5

[MyBatis从入门到精通](https://book.douban.com/subject/27074809/)

[Mapper.xml中的命名空间及命名解析](https://blog.csdn.net/weixin_36210698/article/details/82992771)





命名空间

interface

xml



mybatis-config.xml



事务



mybatis-spring



cglib

动态代理



sql解析的时候



trim

when

动态sql

https://mybatis.org/mybatis-3/zh/dynamic-sql.html

if

choose when otherwise

trim、where、set

foreach

script

需要记忆的点





### Chap.1 入门

ORM框架

Hibernate

Jpa

MyBatis



缓存

连接管理

消除SQL注入







阿里巴巴大量使用

插件系统

MyBatis Generator

负面的观点：xml或者注解太啰嗦，hibinate更加智能化

odb 目前不支持一个表多次操作？



## Chap. 2 XML方式

动态代理实现原理

java.lang.Class#getCanonicalName

java.lang.reflect.Proxy 静态代理

```java
public static Object newProxyInstance(ClassLoader loader,
                                      Class<?>[] interfaces,
                                      InvocationHandler h)
```

java标准库的代理，必须要传接口

## Chap. 3 MyBatis注解方式

Mybatis 3使用动态注解来实现

[]()

[]()

[]()


MyBatis从入门到精通__刘增辉

接口要有

- dtd格式的xml文件

- 注解
@Select
@insert
@update
@delete

provider



### Chap. 4 MyBatis动态SQL







## Chap. 5 Mybatis生成器





### Chap. 6 MyBatis高级查询

存储过程

高级结果映射



### Chap. 7 MyBatis缓存配置



### Chap. 8 MyBatis插件开发



### Chap.9 Spring集成MyBatis





### Chap.10 MyBatis跟Spring Boot结合使用





### Chap.11 MyBatis开源项目

