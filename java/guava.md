# guava api

guava MoreObjects.firstNonNull()

1、其用法为如果两个参数都不为空，则返回第一个；
2、如果都为空，则抛出空指针异常
3、如果其中一个为空，返回不为空的那个

https://www.jianshu.com/p/a1e78d569c0b

Optional Ofnullable orElse

testguava


com.google.common.base.Strings#nullToEmpty


guava radlimit是如何实现的 ？？？



```java
<dependency>
            <groupId>com.google.code.findbugs</groupId>
            <artifactId>jsr305</artifactId>
            <version>3.0.2</version>
</dependency>
```









<<<<<<< HEAD
=======
```
>>>>>>> afe522da082020e5ece0b75c43067644b2edb768
# testguava 


- com.google.common.collect
- com.google.common.io
- com.google.common.math
- 

### RateLimiter


jsr-305
FindBugs-jsr305 3.0.1 API
javax.annotation.concurrent.ThreadSafe

[使用JAVA并发标注](https://kaimingwan.com/post/java/javagong-ju-yu-shi-jian/shi-yong-javabing-fa-biao-zhu)


Java同步注解:@ThreadSafe、@Immutable、@NotThreadSafe、@GuardedBy


guava的定位
Java工具库
类似apache-commons

org.apache.commons.io.FileUtils

com.google.common.base.Strings

map根据value查找key

null判断 Optional

Optional java8新增了

guava cache api？

<<<<<<< HEAD

=======
[IDEA中使用Junit4进行测试的入门配置](https://blog.csdn.net/hanchao5272/article/details/79197989)
>>>>>>> afe522da082020e5ece0b75c43067644b2edb768

### Guava字符串工具

- Joiner 实用加入对象，字符串等。
- Spilter 实用程序用来分割字符串。
- CharMatcher 实用的字符操作。
- CaseFormat 实用程序，用于改变字符串格式。

### Guava原语工具

- Bytes 实用程序的原始字节。
- Shorts 实用的原始short。
- Ints 实用为基本整型。
- Longs 实用的原始长整型。
- Floats 实用为基本float。
- Doubles 实用为基本的double。
- Chars 实用的原始字符。
- Booleans 实用为基本布尔。

### Guava数学工具

- IntMath 数学工具为int类型。
- LongMath 数学工具为long类型。
- BigIntegerMath 数学实用程序处理BigInteger。

[Strings Explained joiner](https://github.com/google/guava/wiki/StringsExplained#joiner)

Splitter splitter;

CharMatcher charMatcher;

Preconditions preconditions;  断言 Assert

Supplier<String> supplier;

Functions.forMap(new HashMap<String,String>());

[guava 官方doc](https://google.github.io/guava/releases/snapshot/api/docs/overview-summary.html)

[Guava CharMatcher类](https://www.yiibai.com/guava)

com.google.common.base.Strings

public static boolean isNullOrEmpty(@Nullable String string)

[浅析Google Guava中concurrent下的Monitor和Future特性](https://blog.csdn.net/a837199685/article/details/50610141)

guava中的Monitor可以比java中的Lock.Condition提供更多的方法

提供更多的API
enter()：进入到当前Monitor，无限期阻塞。
enterInterruptibly()：进入到当前Monitor，无限期阻塞，但可能会被打断。
enter(long time, TimeUnit unit)：进入到当前Monitor，最多阻塞给定的时间，返回是否进入Monitor。
enterInterruptibly(long time, TimeUnit unit)：进入到当前Monitor，最多阻塞给定的时间，但可能会被打断，返回是否进入Monitor。
tryEnter()：如果可以的话立即进入Monitor，不阻塞，返回是否进入Monitor。
enterWhen(Guard guard)：当Guard的isSatisfied()为true时，进入当前Monitor，无限期阻塞，但可能会被打断。
enterWhenUninterruptibly(Guard guard)：当Guard的isSatisfied()为true时，进入当前Monitor，无限期阻塞。
enterWhen(Guard guard, long time, TimeUnit unit)：当Guard的isSatisfied()为true时，进入当前Monitor，最多阻塞给定的时间，这个时间包括获取锁的时间和等待Guard satisfied的时间，但可能会被打断。
enterWhenUninterruptibly(Guard guard, long time, TimeUnit unit)：当Guard的isSatisfied()为true时，进入当前Monitor，最多阻塞给定的时间，这个时间包括获取锁的时间和等待Guard satisfied的时间。
enterIf(Guard guard)：如果Guard的isSatisfied()为true，进入当前Monitor，无限期的获得锁，不需要等待Guard satisfied。
enterIfInterruptibly(Guard guard)：如果Guard的isSatisfied()为true，进入当前Monitor，无限期的获得锁，不需要等待Guard satisfied，但可能会被打断。
enterIf(Guard guard, long time, TimeUnit unit)：如果Guard的isSatisfied()为true，进入当前Monitor，在给定的时间内持有锁，不需要等待Guard satisfied。
enterIfInterruptibly(Guard guard, long time, TimeUnit unit)：如果Guard的isSatisfied()为true，进入当前Monitor，在给定的时间内持有锁，不需要等待Guard satisfied，但可能会被打断。
tryEnterIf(Guard guard)：如果Guard的isSatisfied()为true并且可以的话立即进入Monitor，不等待获取锁，也不等待Guard satisfied。
waitFor(Guard guard)：等待Guard satisfied，无限期等待，但可能会被打断，当一个线程当前占有Monitor时，该方法才可能被调用。
waitForUninterruptibly(Guard guard)：等待Guard satisfied，无限期等待，当一个线程当前占有Monitor时，该方法才可能被调用。
waitFor(Guard guard, long time, TimeUnit unit)：等待Guard satisfied，在给定的时间内等待，但可能会被打断，当一个线程当前占有Monitor时，该方法才可能被调用。
waitForUninterruptibly(Guard guard, long time, TimeUnit unit)：等待Guard satisfied，在给定的时间内等待，当一个线程当前占有Monitor时，该方法才可能被调用。
leave()：离开当前Monitor，当一个线程当前占有Monitor时，该方法才可能被调用。
isFair()：判断当前Monitor是否使用一个公平的排序策略。
isOccupied()：返回当前Monitor是否被任何线程占有，此方法适用于检测系统状态，不适用于同步控制。
isOccupiedByCurrentThread()：返回当前线程是否占有当前Monitor。
getOccupiedDepth()：返回当前线程进入Monitor的次数，如果房前线程不占有Monitor，返回0。
getQueueLength()：返回一个估计的等待进入Monitor的线程数量，只是一个估算值，因为线程的数量在这个方法访问那不数据结构的时候可能会动态改变。此方法适用于检测系统状态，不适用于同步控制。
getWaitQueueLength(Guard guard)：返回一个等待给定Guard satisfied的线程估计数量， 注意，因为超时和中断可能发生在任何时候，所以估计只作为一个等待线程的实际数目的上限。此方法适用于检测系统状态，不适用于同步控制。
hasQueuedThreads()：返回是否有任何线程正在等待进入这个Monitor，注意，因为取消随时可能发生，所以返回true并不保证任何其他线程会进入这个Monitor。此方法设计用来检测系统状态。
hasQueuedThread(Thread thread)：返回给定线程是否正在等待进入这个Monitor，注意，因为取消随时可能发生，所以返回true并不保证给定线程会进入这个Monitor。此方法设计用来检测系统状态。
hasWaiters(Guard guard)：返回是否有任何线程正在等待给定Guard satisfied，注意，因为取消随时可能发生，所以返回true并不保证未来Guard变成satisfied时唤醒任意线程。此方法设计用来检测系统状态。



concurrent.bucketal.Bucket 找不到方法


guava cache
Ehcache


<<<<<<< HEAD
​```shell

D:\Java\jdk1.8.0_231\bin\java.exe "-javaagent:C:\Program Files\JetBrains\IntelliJ IDEA 2018.2.4\lib\idea_rt.jar=11964:C:\Program Files\JetBrains\IntelliJ IDEA 2018.2.4\bin" -Dfile.encoding=UTF-8 -classpath D:\Java\jdk1.8.0_231\jre\lib\charsets.jar;D:\Java\jdk1.8.0_231\jre\lib\deploy.jar;D:\Java\jdk1.8.0_231\jre\lib\ext\access-bridge-64.jar;D:\Java\jdk1.8.0_231\jre\lib\ext\cldrdata.jar;D:\Java\jdk1.8.0_231\jre\lib\ext\dnsns.jar;D:\Java\jdk1.8.0_231\jre\lib\ext\jaccess.jar;D:\Java\jdk1.8.0_231\jre\lib\ext\jfxrt.jar;D:\Java\jdk1.8.0_231\jre\lib\ext\localedata.jar;D:\Java\jdk1.8.0_231\jre\lib\ext\nashorn.jar;D:\Java\jdk1.8.0_231\jre\lib\ext\sunec.jar;D:\Java\jdk1.8.0_231\jre\lib\ext\sunjce_provider.jar;D:\Java\jdk1.8.0_231\jre\lib\ext\sunmscapi.jar;D:\Java\jdk1.8.0_231\jre\lib\ext\sunpkcs11.jar;D:\Java\jdk1.8.0_231\jre\lib\ext\zipfs.jar;D:\Java\jdk1.8.0_231\jre\lib\javaws.jar;D:\Java\jdk1.8.0_231\jre\lib\jce.jar;D:\Java\jdk1.8.0_231\jre\lib\jfr.jar;D:\Java\jdk1.8.0_231\jre\lib\jfxswt.jar;D:\Java\jdk1.8.0_231\jre\lib\jsse.jar;D:\Java\jdk1.8.0_231\jre\lib\management-agent.jar;D:\Java\jdk1.8.0_231\jre\lib\plugin.jar;D:\Java\jdk1.8.0_231\jre\lib\resources.jar;D:\Java\jdk1.8.0_231\jre\lib\rt.jar;D:\git\github\testguava\target\classes;D:\mavenrepository\201904\com\google\guava\guava\18.0\guava-18.0.jar;D:\mavenrepository\201904\com\squareup\okhttp3\okhttp\3.14.4\okhttp-3.14.4.jar;D:\mavenrepository\201904\com\squareup\okio\okio\1.17.2\okio-1.17.2.jar;D:\mavenrepository\201904\commons-io\commons-io\2.5\commons-io-2.5.jar cn.edidada.testguava.demo.Makenetworkconneced

```

[使用 Google Guava 编程](https://zhuanlan.zhihu.com/p/77806328)

=======
​```shell

D:\Java\jdk1.8.0_231\bin\java.exe "-javaagent:C:\Program Files\JetBrains\IntelliJ IDEA 2018.2.4\lib\idea_rt.jar=11964:C:\Program Files\JetBrains\IntelliJ IDEA 2018.2.4\bin" -Dfile.encoding=UTF-8 -classpath D:\Java\jdk1.8.0_231\jre\lib\charsets.jar;D:\Java\jdk1.8.0_231\jre\lib\deploy.jar;D:\Java\jdk1.8.0_231\jre\lib\ext\access-bridge-64.jar;D:\Java\jdk1.8.0_231\jre\lib\ext\cldrdata.jar;D:\Java\jdk1.8.0_231\jre\lib\ext\dnsns.jar;D:\Java\jdk1.8.0_231\jre\lib\ext\jaccess.jar;D:\Java\jdk1.8.0_231\jre\lib\ext\jfxrt.jar;D:\Java\jdk1.8.0_231\jre\lib\ext\localedata.jar;D:\Java\jdk1.8.0_231\jre\lib\ext\nashorn.jar;D:\Java\jdk1.8.0_231\jre\lib\ext\sunec.jar;D:\Java\jdk1.8.0_231\jre\lib\ext\sunjce_provider.jar;D:\Java\jdk1.8.0_231\jre\lib\ext\sunmscapi.jar;D:\Java\jdk1.8.0_231\jre\lib\ext\sunpkcs11.jar;D:\Java\jdk1.8.0_231\jre\lib\ext\zipfs.jar;D:\Java\jdk1.8.0_231\jre\lib\javaws.jar;D:\Java\jdk1.8.0_231\jre\lib\jce.jar;D:\Java\jdk1.8.0_231\jre\lib\jfr.jar;D:\Java\jdk1.8.0_231\jre\lib\jfxswt.jar;D:\Java\jdk1.8.0_231\jre\lib\jsse.jar;D:\Java\jdk1.8.0_231\jre\lib\management-agent.jar;D:\Java\jdk1.8.0_231\jre\lib\plugin.jar;D:\Java\jdk1.8.0_231\jre\lib\resources.jar;D:\Java\jdk1.8.0_231\jre\lib\rt.jar;D:\git\github\testguava\target\classes;D:\mavenrepository\201904\com\google\guava\guava\18.0\guava-18.0.jar;D:\mavenrepository\201904\com\squareup\okhttp3\okhttp\3.14.4\okhttp-3.14.4.jar;D:\mavenrepository\201904\com\squareup\okio\okio\1.17.2\okio-1.17.2.jar;D:\mavenrepository\201904\commons-io\commons-io\2.5\commons-io-2.5.jar cn.edidada.testguava.demo.Makenetworkconneced

```


[使用 Google Guava 编程](https://zhuanlan.zhihu.com/p/77806328)
```
>>>>>>> afe522da082020e5ece0b75c43067644b2edb768



Monitor

```java
private final Collection<String> targets = Sets.newHashSet("1", "2", "3");
```

Optional抽象类
- Present
- Absent

作用：检测Object是否为null

​```java
public static <T> Optional<T> of(T reference)
public boolean isPresent()
```

BiMap

根据value找key

构造方法
HashBiMap.create()


private static boolean isValidDataNode(final String dataNodeStr) {
    return dataNodeStr.contains(DELIMITER) && 2 == Splitter.on(DELIMITER).splitToList(dataNodeStr).size();
}


MoreObjects.firstNonNull
