# Java8实战

[Java8实战](https://book.douban.com/subject/26772632/)



https://github.com/edidada/Java8InAction



第二版 Java实战 java11的？


#### Chap. 2 通过行为参数化传递代码


行为参数化

匿名内部类
传递代码
排序、线程


#### Chap. 3 Lambda表达式


lambda

Stream 面试题

list
filter
map
keyStore

函数式接口

- java.util.function.Predicate  Predicate<T>                             返回boolean
- java.util.function.Consumer   Consumer<T>                        只有入参，没有出参
- java.util.function.Function   Function<T, R>    R apply(T t)  有入参，有出参
- java.util.function.Supplier                      T get()                      没有入参，有出参
- 

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



filter()
sort()
limit()             截短流 跟数据库select limit一样的
collect()
distinct()
skip()               扔掉了前n个元素的流。如果流中元素不足n个，则返回一个空流。

java.util.stream.Stream


另一个常见的数据处理套路是看看数据集中的某些元素是否匹配一个给定的属性。Stream 
API通过allMatch、anyMatch、noneMatch、findFirst和findAny方法提供了这样的工具。


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



String[] ls = new String[]{"age", "eat", "", "tan", "ate", "nat", "bat", "", "back"};
        //数组转换成流
        Stream<String> stream = Arrays.stream(ls);



#### Chap. 6 用流收集数据

流 收集数据

#### Chap. 7 并行数据处理与性能


顺序流 并行流

java.util.Spliterator

第三部分 高效Java 8编程

#### Chap. 8 重构、测试和调试

java.util.Optional
com.google.common.base.Optional

怎么报错的？

#### Chap. 9 default method
默认方法





第10章　用Optional取代null



第11章　CompletableFuture：组合式异步编程

java.util.concurrent.CompletableFuture



第12章　新的日期和时间API
面试题


第四部分 超越Java 8
第13章　函数式的思考





第14章　函数式编程的技巧



第15章　面向对象和函数式编程的混合：Java 8和Scala的比较



第16章　结论以及Java的未来



