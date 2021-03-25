# 写给大忙人看的Java8

##### 0506看
##### 0915看





Stream 面试题

https://blog.csdn.net/m0_47379359/article/details/106526551

```shell
list.stream()
            .filter(s ‐> s.startsWith("张"))
            .filter(s ‐> s.length() == 3)
            .forEach(System.out::println);
```



Java.util.function包



#### Chap. 1

lambda

interface

Collections/Collection
Arrays/Array

default method

为接口添加静态方法

Path
Paths

[写给大忙人的JavaSE8书后习题简析-第一章](https://blog.mythsman.com/post/5d2fef02976abc05b34545ed/)



#### Chap. 2

Stream.of()

可以从集合、数组、生成器中创建stream
filter过滤元素
map改变元素
Stream操作包括limit、distinct和sorted
Stream，reduction操作符
count、max、min、findFirst findAny 返回Optional值
Optional null ifPresent() orElse()
Collections类的groupingBy和paritoningBy()允许你对stream中的内容进行分组
int long double提供了专门的Stream

IntStream
LongStream
DoubleStream

[java8 Stream:数值流(原始类型流特化)与构建流的几种方式](https://blog.csdn.net/sdmxdzb/article/details/82740797)

nominal typing
名义类型

常用函数式接口

- Runnable
- Supplier
- Consumer
- BitConsumer
- Function
- BiFunction
- UnaryOperator
- - BinaryOperator
- Predicate
- BiPredicate


FilePredicate vs Predicate<File>

[写给大忙人的JavaSE8书后习题简析-第二章](https://blog.mythsman.com/post/5d2fef2c976abc05b34545f9/)

#### Chap. 3

jjs jss



#### Chap. 4
JavaFX

AWT 
Swing 自己绘制
一般都不用



#### Chap. 5

java.time
Java事件中，没有闰秒
LocaldateTime没有时区
TemporalAdjuster
ZonedDateTime vs Gregorian Calendar
DateTimeFormatter

java.time.Instant

大概300年的纳秒值才会导致long值溢出

LocalDate是一个带有年份、月份、当月天数的日期。

```java

LocalDate today = LocalDate.now();
LocalDate alonzosBirthday = LocalDate.of(1903,6,14);

```

新Date api与之前的Date java.sql.Date/Time/Timestamp

#### Chap. 6


并发
java 5 java.util.concurrent 既有并发类，又有实现API开发者实现的类 UnSafe 

competeleFuture

#### Chap. 7

nashorn js引擎



#### Chap. 8 杂项改进
Java8在String类中只添加了一个新方法，就是join，该方法实现了字符串的拼接，可以把它看作split方法的逆操作。

String joined = String.join(".", "www", "cnblogs", "com");
System.out.println(joined); // www.cnblogs.com

数字包装类提供了BYTES静态方法，以byte为单位返回长度。

所有八种包装类都提供了静态的hashCode方法。

Short、Integer、Long、Float和Double这5种类型分别提供了了sum、max和min，用来在流操作中作为聚合函数使用。

Comparator

java 6 引入NavicateSet NavicateMap接口，通过利用元素和键排序，对于任意指定v，可以获取>=v >v的最小值，<=v <v的最大值

Files.lines() UTF-8
File.read()本地编码

Files.lines()
Files.list()
Files.walk()

Java5 引入Scanner,避免使用BufferReader
lines() BR有 Scanner没有

Java 8 官方提供java.util.Base64编码/解码方法
getEncoder()
getUrlEncoder()
getMimeEncoder()


方法参数反射

可重复的注解
可用于类型的注解

NULL检查

re

JDBC

