# lombok

[官网](https://projectlombok.org/)

[lombok 官网](https://projectlombok.org/features/all)

[lombok在IntelliJ IDEA下的使用](http://www.cnblogs.com/yjmyzz/p/lombok-with-intellij-idea.html)

IDEA插件Lombok Plugin

```java
val example = new ArrayList<String>();
```

```shell
Incompatible types.
Required:
lombok.val

Found:
java.util.ArrayList
<java.lang.String>
```

报错解决：
```
安装Lombok Plugin
```

lombok是一款可以精减java代码、提升开发人员生产效率的辅助工具，利用注解在编译期自动生成setter/getter/toString()/constructor之类的代码。代码越少，意味着出bug的可能性越低。

lombok安装
lombok的安装跟一般引用jar包没有什么区别，可以到官网上下载最新的jar包，然后导入到项目里面就好啦。

Maven添加依赖

<dependencies>
    <dependency>
        <groupId>org.projectlombok</groupId>
        <artifactId>lombok</artifactId>
        <version>1.16.10</version>
    </dependency>
</dependencies>
Intellij idea开发的话需要安装Lombok plugin，同时设置 Setting -> Compiler -> Annotation Processors -> Enable annotation processing勾选。

lombok应用在enum上

```java
@RequiredArgsConstructor
@Getter
public enum ShardingPropertiesConstant
```

java.beans.ConstructorProperties

[ss解析引擎](https://shardingsphere.apache.org/document/current/cn/features/sharding/principle/parse/)

[lombok-intellij-plugin](https://github.com/mplushnikov/lombok-intellij-plugin)