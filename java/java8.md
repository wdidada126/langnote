# java8

final语义
Java 8 接口 default方法实现

Collectors.toList()
Collectors.toSet()

```java
    Function<ApplyPayResultReferPoDTO, Object[]> convert = item -> new Object[]{
            item.getApplyPayAmount(),
            item.getApplyPayAmount(),
            tenantNumId,dataSign,
            item.getCortNumId(),
            item.getSupplyNumId(),
            item.getPoDtlSeries(),
            item.getPoNumId(),
            item.getPoBatchId(),
            item.getPoBatchSeries(),
            item.getPreSetSeries()
    };
    List<Object[]> args = entities.stream().map(convert).collect(Collectors.toList());
```

javax
- javax-batch
- javax-inject
- javax-invidate


javax.validation.constraints中@NotEmpty,@NotNull,@NotBlank的区别
https://blog.csdn.net/m0_51176516/article/details/117456403



@NotEmpty
The annotated element must not be {@code null} nor empty. Supported types are:
不能是null
不能是空字符
集合框架中的元素不能为空
加了@NotEmpty注解的String类 ，Collection集合，Map ，数组，这些是不能为null或者长度为0的;
(String ,Collection,Map的isEmpty()方法)

@NotNull：主要用在基本数据类型上(Int，Integer，Double)
被修饰元素不能为null
举例：
@NotNull(message = “年龄不能为空”)
private Integer age;

@NotBlank：主要用在String字符串上面(String)
The annotated element must not be {@code null} and must contain at least one
non-whitespace character.（必须包含至少一个非空白字符。）
这个注解用来判断字符串或者字符
举例：
@NotBlank(message = “名字不能为空”)
private String name

JAVA8 STREAM COLLECT GROUPBY分组的简单例子
https://www.cnblogs.com/theRhyme/p/12128652.html

java代码 Boolean 默认 false
bool 没有默认值

BigDecimal 用法
https://www.cnblogs.com/ansoncong/p/10448911.html

String replaceAll() 需要写单元测试 一个字符串，出现特定字符替换掉 实现上述功能

JDK 7提供了7个阻塞队列，如下。
·ArrayBlockingQueue：一个由数组结构组成的有界阻塞队列。
·LinkedBlockingQueue：一个由链表结构组成的有界阻塞队列。
·PriorityBlockingQueue：一个支持优先级排序的无界阻塞队列。
·DelayQueue：一个使用优先级队列实现的无界阻塞队列。
·SynchronousQueue：一个不存储元素的阻塞队列。
·LinkedTransferQueue：一个由链表结构组成的无界阻塞队列。
·LinkedBlockingDeque：一个由链表结构组成的双向阻塞队列。

### 书籍
windows电脑上

https://github.com/edidada/Java8InAction


https://github.com/java8/Java8InAction

读书笔记

https://github.com/NGLSL/Java8InAction-ReadingNotes
https://github.com/edidada/lambda-stream-practice



[轻松调试Stream](http://www.imooc.com/article/293427)


import java.beans.ConstructorProperties;

[ConstructorProperties doc](https://docs.oracle.com/javase/8/docs/api/java/beans/ConstructorProperties.html)

[Java8新特性——接口的默认方法和类方法](https://www.cnblogs.com/flypie/p/5080599.html)

接口的默认方法和类方法

[JDK8函数式接口Function Consumer Predicate Supplier](https://blog.csdn.net/z834410038/article/details/77370785)



if 可以不用加{}  为什么好多代码用idea打开，还是报错？

For a more sophisticated exception management use the * @see #recordFailure(Predicate) method



Java 8中新增了一个全新的日期时间API，称为Java Time API。在这个API中，有一些新的类和接口，用来表示日期、时间、时区、时间段、时间间隔等概念。下面是一些Java 8新日期时间API的常用类和接口：

LocalDate：表示一个不带时区的日期，比如2022-03-15。
LocalTime：表示一个不带时区的时间，比如13:30:00。
LocalDateTime：表示一个不带时区的日期时间，比如2022-03-15T13:30:00。
ZonedDateTime：表示一个带时区的日期时间，比如2022-03-15T13:30:00+08:00。
Period：表示日期之间的时间差，比如2天。
Duration：表示时间之间的时间差，比如3小时。
Instant：表示时间戳，比如2022-03-15T05:30:00.000Z。
DateTimeFormatter：日期时间格式化类，用于将日期时间转换为字符串或将字符串转换为日期时间。
ZoneId：时区ID，用于表示不同的时区。
ZoneOffset：时区偏移量，用于表示相对于UTC的时差。
这些新的类和接口提供了更加方便、灵活和易用的日期时间处理方式，相比于旧的日期时间API，在表达能力、可读性和可维护性方面都有了很大的提升。




Java 8引入了许多新的API和功能，包括以下几个方面：
Lambda表达式：Lambda表达式是一种更简洁、更易于理解的方式来表示一个方法的参数和实现，它可以使代码更加简洁，更易于阅读和维护。
Stream API：Stream API提供了一种新的方式来处理集合数据，它允许在集合数据上执行复杂的操作，例如过滤、映射和归约等。
新的Date/Time API：Java 8引入了新的日期和时间API，它提供了更好的日期和时间处理方式，包括新的日期和时间类、格式化和解析功能等。
方法引用：方法引用提供了一种更简洁、更易于阅读的方式来调用方法，它允许将方法作为参数传递或作为返回值返回。
接口默认方法：接口默认方法允许在不破坏现有代码的情况下向接口添加新的方法。
可重复注解：Java 8引入了可重复注解，它允许将一个注解应用到同一元素上多次。
并发增强：Java 8提供了一些新的并发工具和API，例如CompletableFuture和StamptedLock等，以帮助开发者更轻松地处理并发问题。
其他改进：Java 8还包括其他一些改进，例如类型注解、Nashorn JavaScript引擎、Base64编码、Optional类等。



CompletableFuture是Java 8中引入的新特性，它是一种异步编程的方式，可以用于简化异步任务的处理，它能够让异步执行的任务更加简单、易读、易维护。
CompletableFuture可以用于将一个耗时的操作异步执行，并在执行完成后回调处理结果，同时可以在不同的线程中进行任务之间的串行、并行和组合操作。
在CompletableFuture中，可以通过thenApply、thenAccept和thenRun方法来添加回调函数，这些方法的区别在于它们的返回值类型和参数类型的不同，从而可以实现不同的操作和组合。
除此之外，CompletableFuture还提供了一些常用的方法，如allOf、anyOf、join等，用于处理多个CompletableFuture实例之间的关系和组合。


StampedLock是Java 8引入的新型锁，它是ReadWriteLock的改进版本。与ReadWriteLock类似，StampedLock也支持读写操作分离，可以实现更高的并发性和更优秀的性能。

StampedLock的主要特点如下：

支持三种模式：读模式、写模式和乐观读模式。
乐观读模式是StampedLock的独特之处，它允许在没有竞争的情况下执行读操作，避免了使用传统读锁的开销。
支持手动获取和释放锁，手动获取锁时必须传入一个“戳记”，用于标识当前的锁状态，而手动释放锁则需要提供之前获取锁时的戳记。
支持非阻塞的读写操作，即tryReadLock()、tryWriteLock()等方法，如果获取不到锁，会立即返回而不是阻塞等待。
StampedLock的常用方法如下：

readLock()：获取读锁，返回一个戳记，如果当前已经有写锁，则获取读锁失败。
writeLock()：获取写锁，返回一个戳记，如果当前已经有读锁或写锁，则获取写锁失败。
tryOptimisticRead()：尝试乐观读，返回一个戳记，用于在读操作前判断锁是否被占用，如果当前没有写锁，则获取乐观读锁成功，否则获取乐观读锁失败。
validate()：校验乐观读锁，如果当前没有写锁，则校验成功，否则校验失败。
tryReadLock()：非阻塞获取读锁，如果当前没有写锁，则获取读锁成功，否则获取读锁失败。
tryWriteLock()：非阻塞获取写锁，如果当前没有读锁或写锁，则获取写锁成功，否则获取写锁失败。
tryConvertToWriteLock()：将当前线程持有的读锁转换为写锁，如果当前没有读锁或已经有写锁，则转换失败。
需要注意的是，StampedLock的使用需要谨慎，因为它的锁状态是通过戳记来维护的，如果戳记被错误地使用或泄露，会导致锁状态出现异常，甚至可能导致死锁等问题。





