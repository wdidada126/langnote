# java8
JDK7新特性：MulticastChannel实现非阻塞式组播通信
https://blog.csdn.net/code727/article/details/84419381

final语义
Java 8 接口 default方法实现

## Collectors
Collectors，可以说是Java8的最常用操作了，用来实现对队列的各种操作，包括：分组、聚合等，官方描述是：

```shell
Implementations of {@link Collector} that implement various useful reduction
operations, such as accumulating elements into collections, summarizing
elements according to various criteria, etc.
<p>The following are examples of using the predefined collectors to perform
common mutable reduction tasks:
<pre>{@code

    // Accumulate names into a List
    List<String> list = people.stream().map(Person::getName).collect(Collectors.toList());
    
    // Accumulate names into a TreeSet
    Set<String> set = people.stream().map(Person::getName)
                            .collect(Collectors.toCollection(TreeSet::new));
    
    // Convert elements to strings and concatenate them, separated by commas
    String joined = things.stream()
                          .map(Object::toString)
                          .collect(Collectors.joining(", "));
                          
    // Compute sum of salaries of employee
    int total = employees.stream()
                         .collect(Collectors.summingInt(Employee::getSalary)));
                         
    // Group employees by department
    Map<Department, List<Employee>> byDept
        = employees.stream()
                   .collect(Collectors.groupingBy(Employee::getDepartment));
                   
    // Compute sum of salaries by department
    Map<Department, Integer> totalByDept
        = employees.stream()
                   .collect(Collectors.groupingBy(Employee::getDepartment,
                        Collectors.summingInt(Employee::getSalary)));
                        
    // Partition students into passing and failing
    Map<Boolean, List<Student>> passingFailing =
        students.stream()
                .collect(Collectors.partitioningBy(s -> s.getGrade() >= PASS_THRESHOLD));
                
}</pre>
@since 1.8
```

定义示例数据
操作对象：

```shell
@Data
@AllArgsConstructor
public class Person implements Serializable {
    private static final long serialVersionUID = -5996703909566682313L;
    private Long id;
    private String name;
    private LocalDate birthday;
    private Integer age;
    private Double weight;
}
```

测试数据：
```shell
List<Person> people = Lists.newArrayList(
        new Person(1001L, "张三", LocalDate.of(1998, Month.JANUARY, 1), 25, 70.24D),
        new Person(1002L, "李四", LocalDate.of(2000, Month.MARCH, 3), 23, 64.22),
        new Person(1003L, "王五", LocalDate.of(2000, Month.SEPTEMBER, 7), 23, 59.91D),
        new Person(1004L, "赵六", LocalDate.of(2002, Month.JUNE, 8), 21, 62.34D),
        new Person(1005L, "钱七", LocalDate.of(2002, Month.DECEMBER, 2), 21, 75.55D)
);
```

https://zhuanlan.zhihu.com/p/656502312

一、数据统计
1. 计算元素数量：counting 统计聚合结果的元素数量：
```java
people.stream().collect(Collectors.counting());
// 5
```

作用与people.stream().count();相同。 
2. 求平均值：averagingDouble、averagingInt、averagingLong
这几个方法的作用都是一样的：计算聚合元素的平均值，区别在于入参类型不同。
比如，求这几个人的体重平均值，因为体重是Double类型，所以在不转换类型的情况下，需要使用averagingDouble ：
```java
people.stream().collect(Collectors.averagingDouble(Person::getWeight));
// 66.452
```

不考虑精度，也可以用其他方法实现：
```java
people.stream().collect(Collectors.averagingInt(p -> p.getWeight().intValue()));
// 66.0
people.stream().collect(Collectors.averagingLong(p -> p.getWeight().longValue()))
// 66.0
```
如果是求平均年龄，因为年龄是Integer 类型，所以可以使用任一函数：
```java
people.stream().collect(Collectors.averagingInt(Person::getAge));
// 22.6
people.stream().collect(Collectors.averagingLong(Person::getAge));
// 22.6
people.stream().collect(Collectors.averagingDouble(Person::getAge));
// 22.6
```
注意：这三个方法的返回值都是Double类型。
3. 求和：summingDouble、summingInt、summingLong 
这三个方法和上面的平均值方法类似，也是需要注意元素的类型，在需要类型转换时，需要强制转换：
```java
people.stream().collect(Collectors.summingInt(p -> p.getWeight().intValue()));
// 330
people.stream().collect(Collectors.summingLong(p -> p.getWeight().longValue()));
// 330
people.stream().collect(Collectors.summingDouble(Person::getWeight));
// 332.26
```
对于不需要强制转换的类型，可以随意使用任何一个函数：
people.stream().collect(Collectors.summingInt(Person::getAge)));
// 113
people.stream().collect(Collectors.summingLong(Person::getAge)));
// 113
people.stream().collect(Collectors.summingDouble(Person::getAge)));
// 113.0

注意：这三个方法返回值和平均值的三个方法不一样，summingInt返回的是Integer类型，summingDouble返回的是Double类型、summingLong返回的是Long类型。

4. 求最大值/最小值元素：maxBy、minBy
这两个函数就是求聚合元素中指定比较器中的最大/最小元素。比如，求年龄最大/最小的Person对象：
people.stream().collect(Collectors.minBy(Comparator.comparing(Person::getAge)));
// Optional[Person(id=1004, name=赵六, birthday=2002-06-08, age=21, weight=62.34)], 注意返回类型是Optional
people.stream().collect(Collectors.maxBy(Comparator.comparing(Person::getAge)));
// Optional[Person(id=1001, name=张三, birthday=1998-01-01, age=25, weight=70.24)], 注意返回类型是Optional

5. 统计结果：summarizingDouble、summarizingInt、summarizingLong
统计操作一般包含了计数、求平局、求和、最大、最小这几个，所以对于统计JDK也给出了一个方便的API。
这组方法与求和、求平均的方法类似，都需要注意方法类型。比如，按照体重统计的话，需要进行类型转换：
people.stream().collect(Collectors.summarizingInt(p -> p.getWeight().intValue()));
// IntSummaryStatistics{count=5, sum=330, min=59, average=66.000000, max=75}
people.stream().collect(Collectors.summarizingLong(p -> p.getWeight().longValue()));
// LongSummaryStatistics{count=5, sum=330, min=59, average=66.000000, max=75}
people.stream().collect(Collectors.summarizingDouble(Person::getWeight));
// DoubleSummaryStatistics{count=5, sum=332.260000, min=59.910000, average=66.452000, max=75.550000}

如果是用年龄统计的话，三个方法通用：
people.stream().collect(Collectors.summarizingInt(Person::getAge));
// IntSummaryStatistics{count=5, sum=113, min=21, average=22.600000, max=25}
people.stream().collect(Collectors.summarizingLong(Person::getAge));
// LongSummaryStatistics{count=5, sum=113, min=21, average=22.600000, max=25}
people.stream().collect(Collectors.summarizingDouble(Person::getAge));
// DoubleSummaryStatistics{count=5, sum=113.000000, min=21.000000, average=22.600000, max=25.000000}

注意：这三个方法返回值不一样，summarizingInt返回IntSummaryStatistics类型，summarizingDouble返回DoubleSummaryStatistics类型，summarizingLong返回LongSummaryStatistics类型。
二、聚合、分组
1. 聚合元素：toList、toSet、toCollection
这几个函数比较简单，是将聚合之后的元素，重新封装到队列中，然后返回。对象数组一般搭配map使用，是最经常用到的几个方法。比如，得到所有Person的 Id 列表，只需要根据需要的结果类型使用不同的方法即可：
people.stream().map(Person::getId).collect(Collectors.toList());
// List:[1001, 1002, 1003, 1004, 1005]
people.stream().map(Person::getId).collect(Collectors.toSet());
// Set:[1001, 1002, 1003, 1004, 1005]
people.stream().map(Person::getId).collect(Collectors.toCollection(TreeSet::new));
// TreeSet:[1001, 1002, 1003, 1004, 1005]

注意：toList方法返回的是List子类，toSet返回的是Set子类，toCollection返回的是Collection子类。Collection的子类包括List、Set等众多子类，所以toCollection更加灵活。
2. 聚合元素：toMap、toConcurrentMap
这两个方法的作用是将聚合元素，重新组装为Map结构，也就是 k-v 结构。两者用法一样，区别是toMap返回的是Map，toConcurrentMap返回ConcurrentMap，也就是说，toConcurrentMap返回的是线程安全的 Map 结构。比如，我们需要聚合Person的id：
people.stream().collect(Collectors.toMap(Person::getId, Function.identity()));
// {1001=Person(id=1001, name=张三, birthday=1998-01-01, age=25, weight=70.24),
// 1002=Person(id=1002, name=李四, birthday=2000-03-03, age=23, weight=64.22),
// 1003=Person(id=1003, name=王五, birthday=2000-09-07, age=23, weight=59.91),
// 1004=Person(id=1004, name=赵六, birthday=2002-06-08, age=21, weight=62.34),
// 1005=Person(id=1005, name=钱七, birthday=2002-12-02, age=21, weight=75.55)}
但是，如果id有重复的，会抛出java.lang.IllegalStateException: Duplicate key异常，所以，为了保险起见，我们需要借助toMap另一个重载方法，告诉方法当id重复时该选择哪一条元素：

people.stream().collect(Collectors.toMap(Person::getId, Function.identity(), (x, y) -> x));
// {1001=Person(id=1001, name=张三, birthday=1998-01-01, age=25, weight=70.24),
// 1002=Person(id=1002, name=李四, birthday=2000-03-03, age=23, weight=64.22),
// 1003=Person(id=1003, name=王五, birthday=2000-09-07, age=23, weight=59.91),
// 1004=Person(id=1004, name=赵六, birthday=2002-06-08, age=21, weight=62.34),
// 1005=Person(id=1005, name=钱七, birthday=2002-12-02, age=21, weight=75.55)}
toMap有不同的重载方法，可以实现比较复杂的逻辑。比如，根据id分组的Person的姓名：
people.stream().collect(Collectors.toMap(Person::getId, Person::getName, (x, y) -> x));
// {1001=张三, 1002=李四, 1003=王五, 1004=赵六, 1005=钱七}
比如，得到相同年龄体重最高的Person对象集合：
Map<Integer, Person> map = people.stream()
                .collect(Collectors.toMap(Person::getAge, Function.identity(), 
                        BinaryOperator.maxBy(Comparator.comparing(Person::getWeight))));
// {21=Person(id=1005, name=钱七, birthday=2002-12-02, age=21, weight=75.55), 
// 23=Person(id=1002, name=李四, birthday=2000-03-03, age=23, weight=64.22), 
// 25=Person(id=1001, name=张三, birthday=1998-01-01, age=25, weight=70.24)}
所以，toMap的功能很强大。

3. 分组：groupingBy、groupingByConcurrent
groupingBy与toMap都是将聚合元素进行分组，区别在于toMap结果是 1:1 的 k-v 结构，groupingBy的结果是 1:n 的 k-v 结构。对Person的年龄分组：
people.stream().collect(Collectors.groupingBy(Person::getAge);
// {21=[Person(id=1004, name=赵六, birthday=2002-06-08, age=21, weight=62.34), 
//     Person(id=1005, name=钱七, birthday=2002-12-02, age=21, weight=75.55)], 
// 23=[Person(id=1002, name=李四, birthday=2000-03-03, age=23, weight=64.22), 
//     Person(id=1003, name=王五, birthday=2000-09-07, age=23, weight=59.91)], 
// 25=[Person(id=1001, name=张三, birthday=1998-01-01, age=25, weight=70.24)]}
people.stream().collect(Collectors.groupingBy(Person::getAge, Collectors.toSet());
// {21=[Person(id=1005, name=钱七, birthday=2002-12-02, age=21, weight=75.55), 
//     Person(id=1004, name=赵六, birthday=2002-06-08, age=21, weight=62.34)], 
// 23=[Person(id=1003, name=王五, birthday=2000-09-07, age=23, weight=59.91), 
//     Person(id=1002, name=李四, birthday=2000-03-03, age=23, weight=64.22)], 
// 25=[Person(id=1001, name=张三, birthday=1998-01-01, age=25, weight=70.24)]}

也能够实现与toMap类似的功能，比如对Person的id分组：
people.stream()
      .collect(Collectors.groupingBy(Person::getId, 
              Collectors.collectingAndThen(Collectors.toList(), list -> list.get(0))));
// {1001=Person(id=1001, name=张三, birthday=1998-01-01, age=25, weight=70.24),
// 1002=Person(id=1002, name=李四, birthday=2000-03-03, age=23, weight=64.22),
// 1003=Person(id=1003, name=王五, birthday=2000-09-07, age=23, weight=59.91),
// 1004=Person(id=1004, name=赵六, birthday=2002-06-08, age=21, weight=62.34),
// 1005=Person(id=1005, name=钱七, birthday=2002-12-02, age=21, weight=75.55)}

4. 分组：partitioningBy
partitioningBy与groupingBy的区别在于，partitioningBy借助Predicate断言，可以将集合元素分为true和false两部分。比如按照年龄是否大于 22分组：

people.stream().collect(Collectors.partitioningBy(p -> p.getAge() > 22));
// List: {false=[Person(id=1004, name=赵六, birthday=2002-06-08, age=21, weight=62.34), 
//   Person(id=1005, name=钱七, birthday=2002-12-02, age=21, weight=75.55)], 
// true=[Person(id=1001, name=张三, birthday=1998-01-01, age=25, weight=70.24), 
//    Person(id=1002, name=李四, birthday=2000-03-03, age=23, weight=64.22), 
//    Person(id=1003, name=王五, birthday=2000-09-07, age=23, weight=59.91)]}
people.stream().collect(Collectors.partitioningBy(p -> p.getAge() > 22, Collectors.toSet()));
// Set: {false=[Person(id=1004, name=赵六, birthday=2002-06-08, age=21, weight=62.34), 
//   Person(id=1005, name=钱七, birthday=2002-12-02, age=21, weight=75.55)], 
// true=[Person(id=1001, name=张三, birthday=1998-01-01, age=25, weight=70.24), 
//    Person(id=1002, name=李四, birthday=2000-03-03, age=23, weight=64.22), 
//    Person(id=1003, name=王五, birthday=2000-09-07, age=23, weight=59.91)]}
三、链接数据：joining 
这个方法对String类型的元素进行聚合，拼接成一个字符串返回，作用与java.lang.String#join类似，提供了 3 个不同重载方法，可以实现不同的需要。people.stream().map(Person::getName).collect(Collectors.joining());
// 张三李四王五赵六钱七
people.stream().map(Person::getName).collect(Collectors.joining(","));
// 张三,李四,王五,赵六,钱七
people.stream().map(Person::getName).collect(Collectors.joining(",", "【", "】"));
// 【张三,李四,王五,赵六,钱七】

四、操作链：collectingAndThen 
这个方法在groupingBy的例子中出现过，它是先对集合进行一次聚合操作，然后通过Function定义的函数，对聚合后的结果再次处理。
找到聚合元素中00后的Person列表：
people.stream().collect(
        Collectors.collectingAndThen(Collectors.toList(), (
                list -> list.stream()
                        .filter(s -> s.getBirthday().getYear() >= 2000)
                        .collect(Collectors.toList()))
        )
);
// [Person(id=1002, name=李四, birthday=2000-03-03, age=23, weight=64.22), 
// Person(id=1003, name=王五, birthday=2000-09-07, age=23, weight=59.91), 
// Person(id=1004, name=赵六, birthday=2002-06-08, age=21, weight=62.34), 
// Person(id=1005, name=钱七, birthday=2002-12-02, age=21, weight=75.55)]这里为了展示collectingAndThen的用法，其实上面这个例子可以简化为：people.stream().filter(s -> s.getBirthday().getYear() >= 2000).collect(Collectors.toList()); 
五、操作后聚合：mapping mapping先通过Function函数处理数据，然后通过Collector方法聚合元素。比如获取获取Person的姓名列表：people.stream().collect(Collectors.mapping(Person::getName, Collectors.toList()));
// [张三, 李四, 王五, 赵六, 钱七]这种计算与java.util.stream.Stream#map方式类似，在上面的例子中以及使用过：people.stream().map(Person::getName).collect(Collectors.toList());
// [张三, 李四, 王五, 赵六, 钱七]IDE推荐第二种写法，更清晰。
六、聚合后操作：reducing 
reducing提供了 3 个重载方法： 
1、public static <T> Collector<T, ?, Optional<T>> reducing(BinaryOperator<T> op)：直接通过BinaryOperator操作，返回值是Optional 
2、public static <T> Collector<T, ?, T> reducing(T identity, BinaryOperator<T> op)：预定默认值，然后通过BinaryOperator操作 
3、public static <T, U> Collector<T, ?, U> reducing(U identity, Function<? super T, ? extends U> mapper, BinaryOperator<U> op)：预定默认值，通过Function操作元素，然后通过BinaryOperator操作。
计算所有Person的体重和：people.stream().map(Person::getWeight).collect(Collectors.reducing(Double::sum));
// Optional[332.26]，注意返回类型是Optional
people.stream().map(Person::getWeight).collect(Collectors.reducing(0.0, Double::sum));
// 332.26
people.stream().collect(Collectors.reducing(0.0, Person::getWeight, Double::sum));
// 332.26

同mapping，reducing的操作与java.util.stream.Stream#reduce方式类似：
people.stream().map(Person::getWeight).reduce(Double::sum);
// Optional[332.26]，注意返回类型是Optional
people.stream().map(Person::getWeight).reduce(0.0,Double::sum);
// 332.26
maxBy和minBy这两个函数就是通过reducing实现的。
mapping和reducing，可以参考map-reduce的概念。很多框架都是用的map-reduce方式进行操作和聚合。
七、工作中常用的一些组合操作：
1. 分组后操作：对Person的年龄进行分组后，再操作取姓名后聚合为列表：
people.stream().collect(Collectors.groupingBy(Person::getAge, Collectors.mapping(Person::getName, Collectors.toList())));
// {21=[赵六, 钱七], 23=[李四, 王五], 25=[张三]}
2. 分组后记数
people.stream().collect(Collectors.groupingBy(Person::getAge, Collectors.counting()));
// {21=2, 23=2, 25=1}
3. 分组后求和
people.stream().collect(Collectors.groupingBy(Person::getAge, Collectors.summingDouble(Person::getWeight)));
// {21=137.89, 23=124.13, 25=70.24}

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





