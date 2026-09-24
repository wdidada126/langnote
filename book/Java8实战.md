# Java8实战

## String join()
JdbcTemplate拼接 in List集合
kafka有多个生产者，多个消费者，保存到数据库表，用 , 隔开


[Java8实战](https://book.douban.com/subject/26772632/)

第一部分 基础知识
第1章　为什么要关心Java 8　　2
1.1　Java怎么还在变　　4
1.1.1　Java在编程语言生态系统中的位置　　4
1.1.2　流处理　　6
1.1.3　用行为参数化把代码传递给方法　　7
1.1.4　并行与共享的可变数据　　7
1.1.5　Java需要演变　　8
1.2　Java中的函数　　8
1.2.1　方法和Lambda作为一等公民　　9
1.2.2　传递代码：一个例子　　11
1.2.3　从传递方法到Lambda　　12
1.3　流　　13
1.4　默认方法　　17
1.5　来自函数式编程的其他好思想　　18
1.6　小结　　19
第2章　通过行为参数化传递代码　　20
2.1　应对不断变化的需求　　21
2.1.1　初试牛刀：筛选绿苹果　　21
2.1.2　再展身手：把颜色作为参数　　21
2.1.3　第三次尝试：对你能想到的每个属性做筛选　　22
2.2　行为参数化　　23
2.3　对付啰嗦　　27
2.3.1　匿名类　　28
2.3.2　第五次尝试：使用匿名类　　28
2.3.3　第六次尝试：使用Lambda表达式　　30
2.3.4　第七次尝试：将List类型抽象化　　31
2.4　真实的例子　　31
2.4.1　用Comparator来排序　　31
2.4.2　用Runnable执行代码块　　32
2.4.3　GUI事件处理　　32
2.5　小结　　33
第3章　Lambda表达式　　34
3.1　Lambda管中窥豹　　35
3.2　在哪里以及如何使用Lambda　　37
3.2.1　函数式接口　　37
3.2.2　函数描述符　　39
3.3　把Lambda付诸实践：环绕执行模式　　41
3.3.1　第1步记得行为参数化　　41
3.3.2　第2步：使用函数式接口来传递行为　　42
3.3.3　第3步：执行一个行为　　42
3.3.4　第4步：传递Lambda　　42
3.4　使用函数式接口　　43
3.4.1　Predicate　　44
3.4.2　Consumer　　44
3.4.3　Function　　45
3.5　类型检查、类型推断以及限制　　49
3.5.1　类型检查　　49
3.5.2　同样的Lambda，不同的函数式接口　　50
3.5.3　类型推断　　51
3.5.4　使用局部变量　　52
3.6　方法引用　　53
3.6.1　管中窥豹　　53
3.6.2　构造函数引用　　55
3.7　Lambda和方法引用实战　　57
3.7.1　第1步：传递代码　　58
3.7.2　第2步：使用匿名类　　58
3.7.3　第3步：使用Lambda表达式　　58
3.7.4　第4步：使用方法引用　　59
3.8　复合Lambda表达式的有用方法　　59
3.8.1　比较器复合　　60
3.8.2　谓词复合　　60
3.8.3　函数复合　　61
3.9　数学中的类似思想　　62
3.9.1　积分　　62
3.9.2　与Java 8的Lambda联系起来　　63
3.10　小结　　64
第二部分 函数式数据处理
第4章　引入流　　68
4.1　流是什么　　68
4.2　流简介　　72
4.3　流与集合　　74
4.3.1　只能遍历一次　　75
4.3.2　外部迭代与内部迭代　　76
4.4　流操作　　78
4.4.1　中间操作　　78
4.4.2　终端操作　　79
4.4.3　使用流　　80
4.5　小结　　81
第5章　使用流　　82
5.1　筛选和切片　　83
5.1.1　用谓词筛选　　83
5.1.2　筛选各异的元素　　83
5.1.3　截短流　　84
5.1.4　跳过元素　　85
5.2　映射　　86
5.2.1　对流中每一个元素应用函数　　86
5.2.2　流的扁平化　　87
5.3　查找和匹配　　90
5.3.1　检查谓词是否至少匹配一个元素　　90
5.3.2　检查谓词是否匹配所有元素　　90
5.3.3　查找元素　　91
5.3.4　查找第一个元素　　92
5.4　归约　　92
5.4.1　元素求和　　93
5.4.2　最大值和最小值　　94
5.5　付诸实践　　97
5.5.1　领域：交易员和交易　　98
5.5.2　解答　　99
5.6　数值流　　101
5.6.1　原始类型流特化　　101
5.6.2　数值范围　　102
5.6.3　数值流应用：勾股数　　103
5.7　构建流　　105
5.7.1　由值创建流　　106
5.7.2　由数组创建流　　106
5.7.3　由文件生成流　　106
5.7.4　由函数生成流：创建无限流　　107
5.8　小结　　110
第6章　用流收集数据　　111
6.1　收集器简介　　112
6.1.1　收集器用作高级归约　　112
6.1.2　预定义收集器　　113
6.2　归约和汇总　　114
6.2.1　查找流中的最大值和最小值　　114
6.2.2　汇总　　115
6.2.3　连接字符串　　116
6.2.4　广义的归约汇总　　117
6.3　分组　　120
6.3.1　多级分组　　121
6.3.2　按子组收集数据　　122
6.4　分区　　126
6.4.1　分区的优势　　126
6.4.2　将数字按质数和非质数分区　　128
6.5　收集器接口　　129
6.5.1　理解Collector接口声明的方法　　130
6.5.2　全部融合到一起　　134
6.6　开发你自己的收集器以获得更好的性能　　135
6.6.1　仅用质数做除数　　136
6.6.2　比较收集器的性能　　139
6.7　小结　　140
第7章　并行数据处理与性能　　141
7.1　并行流　　141
7.1.1　将顺序流转换为并行流　　142
7.1.2　测量流性能　　144
7.1.3　正确使用并行流　　147
7.1.4　高效使用并行流　　148
7.2　分支/合并框架　　149
7.2.1　使用RecursiveTask　　149
7.2.2　使用分支/合并框架的最佳做法　　153
7.2.3　工作窃取　　154
7.3　Spliterator　　155
7.3.1　拆分过程　　155
7.3.2　实现你自己的Spliterator　　157
7.4　小结　　162
第三部分 高效Java 8编程
第8章　重构、测试和调试　　164
8.1　为改善可读性和灵活性重构代码　　164
8.1.1　改善代码的可读性　　165
8.1.2　从匿名类到Lambda表达式的转换　　165
8.1.3　从Lambda表达式到方法引用的转换　　166
8.1.4　从命令式的数据处理切换到Stream　　167
8.1.5　增加代码的灵活性　　168
8.2　使用Lambda重构面向对象的设计模式　　170
8.2.1　策略模式　　171
8.2.2　模板方法　　172
8.2.3　观察者模式　　173
8.2.4　责任链模式　　175
8.2.5　工厂模式　　177
8.3　测试Lambda表达式　　178
8.3.1　测试可见Lambda函数的行为　　179
8.3.2　测试使用Lambda的方法的行为　　179
8.3.3　将复杂的Lambda表达式分到不同的方法　　180
8.3.4　高阶函数的测试　　180
8.4　调试　　181
8.4.1　查看栈跟踪　　181
8.4.2　使用日志调试　　183
8.5　小结　　184
第9章　默认方法　　 185
9.1　不断演进的API　　 187
9.1.1　初始版本的API　　188
9.1.2　第二版API　　188
9.2　概述默认方法　　190
9.3　默认方法的使用模式　　192
9.3.1　可选方法　　192
9.3.2　行为的多继承　　192
9.4　解决冲突的规则　　196
9.4.1　解决问题的三条规则　　196
9.4.2　选择提供了最具体实现的默认方法的接口　　197
9.4.3　冲突及如何显式地消除歧义　　198
9.4.4　菱形继承问题　　200
9.5　小结　　201
第10章　用Optional取代null　　202
10.1　如何为缺失的值建模　　 203
10.1.1　采用防御式检查减少Null-PointerException　　203
10.1.2　null带来的种种问题　　204
10.1.3　其他语言中null的替代品　　205
10.2　Optional类入门　　206
10.3　应用Optional的几种模式　　 207
10.3.1　创建Optional对象　　208
10.3.2　使用map从Optional对象中提取和转换值　　208
10.3.3　使用flatMap链接Optional对象　　209
10.3.4　默认行为及解引用Optional对象　　213
10.3.5　两个Optional对象的组合　　213
10.3.6　使用filter剔除特定的值　　214
10.4　使用Optional的实战示例　　 216
10.4.1　用Optional封装可能为null的值　　216
10.4.2　异常与Optional的对比　　217
10.4.3　把所有内容整合起来　　218
10.5　小结　　219
第11章　CompletableFuture：组合式异步编程　　220
11.1　Future接口　　222
11.1.1　Future接口的局限性　　223
11.1.2　使用CompletableFuture构建异步应用　　223
11.2　实现异步API　　 224
11.2.1　将同步方法转换为异步方法　　225
11.2.2　错误处理　　227
11.3　让你的代码免受阻塞之苦　　228
11.3.1　使用并行流对请求进行并行操作　　229
11.3.2　使用CompletableFuture发起异步请求　　230
11.3.3　寻找更好的方案　　232
11.3.4　使用定制的执行器　　233
11.4　对多个异步任务进行流水线操作　　234
11.4.1　实现折扣服务　　235
11.4.2　使用Discount服务　　236
11.4.3　构造同步和异步操作　　237
11.4.4　将两个Completable-Future对象整合起来，无论它们是否存在依赖　　239
11.4.5　对Future和Completable-Future的回顾　　241
11.5　响应CompletableFuture的completion事件　　242
11.5.1　对最佳价格查询器应用的优化　　243
11.5.2　付诸实践　　244
11.6　小结　　245
第12章　新的日期和时间API　　246
12.1　LocalDate、LocalTime、Instant、Duration以及Period　　247
12.1.1　使用LocalDate和LocalTime　　247
12.1.2　合并日期和时间　　248
12.1.3　机器的日期和时间格式　　249
12.1.4　定义Duration或Period　　249
12.2　操纵、解析和格式化日期　　251
12.2.1　使用TemporalAdjuster　　253
12.2.2　打印输出及解析日期－时间对象　　255
12.3　处理不同的时区和历法　　256
12.3.1　利用和UTC/格林尼治时间的固定偏差计算时区　　257
12.3.2　使用别的日历系统　　258
12.4　小结　　259
第四部分 超越Java 8
第13章　函数式的思考　　262
13.1　实现和维护系统　　262
13.1.1　共享的可变数据　　263
13.1.2　声明式编程　　264
13.1.3　为什么要采用函数式编程　　265
13.2　什么是函数式编程　　265
13.2.1　函数式Java编程　　266
13.2.2　引用透明性　　268
13.2.3　面向对象的编程和函数式编程的对比　　 268
13.2.4　函数式编程实战　　269
13.3　递归和迭代　　271
13.4　小结　　274
第14章　函数式编程的技巧　　275
14.1　无处不在的函数　　275
14.1.1　高阶函数　　275
14.1.2　科里化　　277
14.2　持久化数据结构　　278
14.2.1　破坏式更新和函数式更新的比较　　279
14.2.2　另一个使用Tree的例子　　281
14.2.3　采用函数式的方法　　282
14.3　Stream的延迟计算　　283
14.3.1　自定义的Stream　　 283
14.3.2　创建你自己的延迟列表　　286
14.4　模式匹配　　290
14.4.1　访问者设计模式　　291
14.4.2　用模式匹配力挽狂澜　　292
14.5　杂项　　295
14.5.1　缓存或记忆表　　295
14.5.2　“返回同样的对象”意味着什么　　296
14.5.3　结合器　　296
14.6　小结　　297
第15章　面向对象和函数式编程的混合：Java 8和Scala的比较　　 299
15.1　Scala简介　　300
15.1.1　你好，啤酒　　300
15.1.2　基础数据结构：List、Set、Map、Tuple、Stream以及Option　　302
15.2　函数　　306
15.2.1　Scala中的一等函数　　307
15.2.2　匿名函数和闭包　　307
15.2.3　科里化　　309
15.3　类和trait　　310
15.3.1　更加简洁的Scala类　　310
15.3.2　Scala的trait与Java 8的接口对比　　311
15.4　小结　　312
第16章　结论以及Java的未来　　313
16.1　回顾Java 8的语言特性　　 313
16.1.1　行为参数化（Lambda 以及方法引用）　　314
16.1.2　流　　314
16.1.3　CompletableFuture　　315
16.1.4　Optional　　315
16.1.5　默认方法　　316
16.2　Java 的未来　　316
16.2.1　集合　　316
16.2.2　类型系统的改进　　317
16.2.3　模式匹配　　318
16.2.4　更加丰富的泛型形式　　319
16.2.5　对不变性的更深层支持　　321
16.2.6　值类型　　322
16.3　写在最后的话　　325
附录A　其他语言特性的更新　　326
附录B　类库的更新　　330
附录C　如何以并发方式在同一个流上执行多种操作　　338
附录D　Lambda表达式和JVM 字节码　　346

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

## 跨年摘录（2020–2026 日常笔记聚合，2026-09-23 整理）

### 2020-08
> 求狸猫技术窝的《从0开始带你成为JVM实战高手》

