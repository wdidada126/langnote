# Java8实战

## String join()
JdbcTemplate拼接 in List集合

[Java8实战](https://book.douban.com/subject/26772632/)



https://github.com/edidada/Java8InAction



第二版 Java实战 java11的？


#### Chap. 2 通过行为参数化传递代码

行为参数化

匿名内部类
传递代码
排序、线程

#### Chap. 3 Lambda表达式
BaseStream接口子接口
IntStream
LongStream
Stream<T>
DoubleStream

AbstractPipeline<E_IN, E_OUT, S extends BaseStream<E_OUT, S>>
DoublePipeline<E_IN>
LongPipeline<E_IN>
IntPipeline<E_IN>
ReferencePipeline<P_IN, P_OUT>

lambda

Stream 面试题

list
filter  Stream<T> filter(Predicate<? super T> predicate) 链式调用，返回自身对象，跟Builder差不多
map
keyStore

函数式接口

- java.util.function.Predicate  Predicate<T>                             返回boolean 跟filter()配合的
- java.util.function.Consumer   Consumer<T>                        只有入参，没有出参
- java.util.function.Function   Function<T, R>    R apply(T t)  有入参，有出参
- java.util.function.Supplier                      T get()                      没有入参，有出参

  

BiFunction
xxxOperator



UnaryOperator 接口扩展了java.util.function.Function 接口。 UnaryOperator 接口表示一个操作，它接受一个参数并返回一个与其输入参数相同类型的结果。
也就是说UnaryOperator 用于处理单个操作数，它返回与操作数相同的类型。
UnaryOperator 可以用于lambda 表达式，并作为参数进行传递。



在Java 8中， BiFunction是功能接口； 它接受两个参数并返回一个对象。
https://blog.csdn.net/cyan20115/article/details/106548429

java之Function、Consumer和Predicate用法及区别
https://blog.csdn.net/weixin_39102174/article/details/102488702

3.6 方法引用
为了避免装箱操作，对Predicate<T>和Function<T, R>等通用函数式接口的原始类型特化：IntPredicate、IntToLongFunction等。
函数式接口 新概念

#### Chap. 4 引入流
Java8中有两大最为重要得改变，其一时Lambda表达式，另外就是 Stream API了。在前面几篇中简单学习了Lambda表达式得语法，以及函数式接口。本文就来简单学习一下Stream API（java.util.stream.*）。
　　Stream 是 Java8中处理集合得关键抽象概念，他可以指定你希望对集合进行得操作，可以执行非常复杂得查找、过滤和映射数据等操作。使用Stream API对集合数据进行操作，就类似使用SQL执行得数据库查询。也可以使用S他ream API 来并行执行操作。简而言之，Stream API 提供了一种高效且易于使用得处理数据得方式。
　　在Stream操作过程中，可以对数据流做过滤，排序，切片等操作，但是操作之后会产生一个新的流，而数据源则不会发生改变。
一、什么是 Stream
　　Stream是数据渠道，用于操作数据源（集合，数组等）所生成得元素序列。而集合讲得是数据，流讲得是计算。
　　注意：
　　　　①. Stream 自己不会存储元素。
　　　　②. Stream 不会改变源对象。相反，它会返回一个持有结果得新Stream
　　　　③. Stream 操作时延迟执行得，这意味着它们会等到需要结果时才执行。（延迟加载）

1）. 通过Collection得Stream（）方法（串行流）或者 parallelStream（）方法（并行流）创建Stream。
2）.通过Arrays中得静态方法stream（）获取数组流
3). 通过Stream类中得 of（）静态方法获取流
4）. 创建无限流(迭代、生成)

二、Stream 操作的三个步骤
　　1）. 创建 Stream
　　　　一个数据源（集合，数组），获取一个流。
　　2）. 中间操作
　　　　一个中间操作链，对数据源的数据进行处理。
　　3）. 终止操作
　　　　一个终止操作，执行中间操作链，并产生结果。

Stream
![Stream](..\imgs\Stream.png)


map
flatMap
filter()
sort()
limit()             截短流 跟数据库select limit一样的
collect()
distinct()
peek()
skip()               扔掉了前n个元素的流。如果流中元素不足n个，则返回一个空流。
reduce()
min()
max()
count()

java.util.stream.Stream


另一个常见的数据处理套路是看看数据集中的某些元素是否匹配一个给定的属性。Stream API通过allMatch、anyMatch、noneMatch、findFirst和findAny方法提供了这样的工具。


findAny
findFirst
anyMatch
allMatch
noneMatch

流操作有两类：中间操作和终端操作。


#### Chap. 5 使用流

IntStream
DoubleStream
LongStream

流 中间操作 终端操作

java.util.Arrays#stream(T[])

String[] ls = new String[]{"age", "eat", "", "tan", "ate", "nat", "bat", "", "back"};
        //数组转换成流
        Stream<String> stream = Arrays.stream(ls);



#### Chap. 6 用流收集数据

流 收集数据

#### Chap. 7 并行数据处理与性能


顺序流 并行流

java.util.Spliterator

## 第三部分 高效Java 8编程

#### Chap. 8 重构、测试和调试

java.util.Optional
com.google.common.base.Optional

怎么报错的？

#### Chap. 9 default method
接口默认方法





### 第10章　用Optional取代null



### 第11章　CompletableFuture：组合式异步编程
Future到CompletableFuture,优越性

Future 和 CompletableFuture 都是 Java 中用于异步编程的 API。但是，CompletableFuture 相对于 Future 有着更强的优越性，主要表现在以下几个方面：
1. 异步编程方式更加灵活：Future 只能表示一个异步操作的结果，无法手动设置它的值或者触发它的完成。而 CompletableFuture 提供了更加灵活的异步编程方式，可以手动设置它的值或者触发它的完成，从而更加灵活地处理异步操作。
2. 支持链式调用：CompletableFuture 可以支持链式调用，可以在一个 CompletableFuture 中嵌套多个 CompletableFuture，从而实现更加复杂的异步编程逻辑。而 Future 不支持链式调用，只能通过阻塞等待来获取异步操作结果。
3. 支持回调机制：CompletableFuture 支持回调机制，可以在异步操作完成时自动触发回调函数，从而实现更加灵活的异步编程。而 Future 不支持回调机制，需要手动轮询来获取异步操作结果。
4. 支持异常处理：CompletableFuture 支持异常处理，可以通过 handle()、exceptionally() 和 whenComplete() 等方法来处理异步操作中的异常。而 Future 只能通过 try-catch 块来处理异步操作中的异常。
下面是一个使用 CompletableFuture 的示例代码：

```java
CompletableFuture<String> future = CompletableFuture.supplyAsync(() -> {
    // 异步执行耗时操作
    return "Hello World";
});

future.thenAccept(result -> {
    // 异步操作完成后的回调函数
    System.out.println(result);
});

// 等待异步操作完成
future.join();
```

在上面的代码中，我们首先使用 CompletableFuture.supplyAsync() 方法创建了一个异步计算任务，然后使用 thenAccept() 方法注册了一个回调函数，在异步操作完成后自动触发回调函数并输出结果。最后，我们使用 join() 方法等待异步操作完成。
需要注意的是，使用 CompletableFuture 需要注意避免线程安全问题和死锁问题，需要合理设计异步编程逻辑，以达到最佳的性能和可靠性的平衡。

java.util.concurrent.CompletableFuture

Future的局限性，它没法直接对多个任务进行链式、组合等处理，需要借助并发工具类才能完成，实现逻辑比较复杂。
https://blog.csdn.net/sermonlizhi/article/details/123356877

![CompletableFuture](..\imgs\javase\CompletableFuture.png)

常用方法
依赖关系
thenApply()：把前面任务的执行结果，交给后面的Function
thenCompose()：用来连接两个有依赖关系的任务，结果由第二个任务返回
and集合关系
thenCombine()：合并任务，有返回值
thenAccepetBoth()：两个任务执行完成后，将结果交给thenAccepetBoth处理，无返回值
runAfterBoth()：两个任务都执行完成后，执行下一步操作(Runnable类型任务)
or聚合关系
applyToEither()：两个任务哪个执行的快，就使用哪一个结果，有返回值
acceptEither()：两个任务哪个执行的快，就消费哪一个结果，无返回值
runAfterEither()：任意一个任务执行完成，进行下一步操作(Runnable类型任务)
并行执行
allOf()：当所有给定的 CompletableFuture 完成时，返回一个新的 CompletableFuture
anyOf()：当任何一个给定的CompletablFuture完成时，返回一个新的CompletableFuture
结果处理
whenComplete：当任务完成时，将使用结果(或 null)和此阶段的异常(或 null如果没有)执行给定操作
exceptionally：返回一个新的CompletableFuture，当前面的CompletableFuture完成时，它也完成，当它异常完成时，给定函数的异常触发这个CompletableFuture的完成



CompletableFuture提供了四个静态方法来创建一个异步操作：

public static CompletableFuture<Void> runAsync(Runnable runnable)
public static CompletableFuture<Void> runAsync(Runnable runnable, Executor executor)
public static <U> CompletableFuture<U> supplyAsync(Supplier<U> supplier)
public static <U> CompletableFuture<U> supplyAsync(Supplier<U> supplier, Executor executor)





### 第12章　新的日期和时间API
面试题


Java 8 引入了新的日期和时间 API，主要包括以下几个类和接口：
1. LocalDate：用于表示日期，不包含时间和时区信息。
2. LocalTime：用于表示时间，不包含日期和时区信息。
3. LocalDateTime：用于表示日期和时间，不包含时区信息。
4. ZonedDateTime：用于表示日期、时间和时区信息。
5. Instant：用于表示时刻，即从 1970 年 1 月 1 日 00:00:00 UTC 开始计算的秒数。
6. Duration：用于表示时间间隔，可以精确到纳秒级别。
7. Period：用于表示日期间隔，可以精确到天。
下面是一些使用示例：
```java
// 获取当前日期和时间
LocalDateTime now = LocalDateTime.now();
System.out.println(now);

// 获取指定日期和时间
LocalDateTime dateTime = LocalDateTime.of(2023, 5, 8, 10, 30, 0);
System.out.println(dateTime);

// 获取当前时区的时间
ZonedDateTime zonedDateTime = ZonedDateTime.now();
System.out.println(zonedDateTime);

// 获取指定时区的时间
ZonedDateTime zonedDateTime2 = ZonedDateTime.of(dateTime, ZoneId.of("America/New_York"));
System.out.println(zonedDateTime2);

// 时间间隔计算
LocalDateTime start = LocalDateTime.of(2023, 5, 8, 10, 30, 0);
LocalDateTime end = LocalDateTime.of(2023, 5, 8, 12, 0, 0);
Duration duration = Duration.between(start, end);
System.out.println(duration.toMinutes());

// 日期间隔计算
LocalDate start2 = LocalDate.of(2023, 5, 8);
LocalDate end2 = LocalDate.of(2024, 5, 8);
Period period = Period.between(start2, end2);
System.out.println(period.getYears() + "年" + period.getMonths() + "个月" + period.getDays() + "天");
```

需要注意的是，新的日期和时间 API 是线程安全的，避免了旧的 Date 和 Calendar 类的诸多问题。同时，新的 API 提供了更多的操作方法，可以方便地进行日期和时间的计算和格式化，提高了开发效率和代码可读性。


日期时间都是final的，操作的话返回一个新的对象

LocalDate、LocalTime、Instant、Duration以及Period
Mysql数据库如何处理？

LocalDate.now()


TemporalAdjuster接口



```java
Temporal adjustInto(Temporal temporal)
```



TemporalField



```java
public interface Temporal extends TemporalAccessor
```

## 第四部分 超越Java 8
### 第13章　函数式的思考





### 第14章　函数式编程的技巧



### 第15章　面向对象和函数式编程的混合：Java 8和Scala的比较



### 第16章　结论以及Java的未来



https://docs.oracle.com/javase/8/docs/api/



## java.util.stream



|     java.util.stream                      |      |      |
| ------------------------- | ---- | ---- |
| Interfaces                |      |      |
|                           |      |      |
| BaseStream                |      |      |
| Collector                 |      |      |
| DoubleStream              |      |      |
| DoubleStream.Builder      |      |      |
| IntStream                 |      |      |
| IntStream.Builder         |      |      |
| LongStream                |      |      |
| LongStream.Builder        |      |      |
| Stream                    |      |      |
| Stream.Builder            |      |      |
|                           |      |      |
| Classes                   |      |      |
|                           |      |      |
| Collectors                |      |      |
| StreamSupport             |      |      |
|                           |      |      |
| Enums                     |      |      |
|                           |      |      |
| Collector.Characteristics |      |      |
