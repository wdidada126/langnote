# lombok

### annotation

RequiredArgsConstructor

lombok用到了tools.jar

## note

本章会对Lombok框架进行介绍，同时会讲解Lombok的原理。并手把手领着小伙伴们实战，引入Lombok以及IDE安装Lombok插件。然后会带着大家实战Coding，讲解@Data @Getter @Setter @NoArgsConstructor @AllArgsConstructor @ToString @EqualsAndHashCode 等Lombok关键注解用法，同时领着大家通过JD来进行反编译。

[lombok](https://projectlombok.org/)

[lombok简介](https://blog.csdn.net/motui/article/details/79012846)

[使用Lombok来优雅的编码](https://www.cnblogs.com/qnight/p/8997493.html)

[lombok @Slf4j log使用](https://mp.weixin.qq.com/s/lAC0rvUG24e1O8xhq5mGQA)

private static final Logger log = LoggerFactory.getLogger(HealthCheckController.class);



lombok 这种能为类生成新方法的工具其实是直接修改 byte code 实现的

java annotation processor是新建class文件，不能修改

AllArgsConstructor
@Data
使用这个注解，就不用再去手写Getter,Setter,equals,canEqual,hasCode,toString等方法了，注解后在编译时会自动加进去。
@AllArgsConstructor
使用后添加一个构造函数，该构造函数含有所有已声明字段属性参数
@NoArgsConstructor
使用后创建一个无参构造函数
@Builder
关于Builder较为复杂一些，Builder的作用之一是为了解决在某个类有很多构造函数的情况，也省去写很多构造函数的麻烦，在设计模式中的思想是：用一个内部类去实例化一个对象，避免一个类出现过多构造函数，


```shell
val
Finally! Hassle-free final local variables.

var
Mutably! Hassle-free local variables.

@NonNull
or: How I learned to stop worrying and love the NullPointerException.

@Cleanup
Automatic resource management: Call your close() methods safely with no hassle.

@Getter/@Setter
Never write public int getFoo() {return foo;} again.

@ToString
No need to start a debugger to see your fields: Just let lombok generate a toString for you!

@EqualsAndHashCode
Equality made easy: Generates hashCode and equals implementations from the fields of your object..

@NoArgsConstructor, @RequiredArgsConstructor and @AllArgsConstructor
Constructors made to order: Generates constructors that take no arguments, one argument per final / non-nullfield, or one argument for every field.

@Data
All together now: A shortcut for @ToString, @EqualsAndHashCode, @Getter on all fields, and @Setter on all non-final fields, and @RequiredArgsConstructor!

@Value
Immutable classes made very easy.

@Builder
... and Bob's your uncle: No-hassle fancy-pants APIs for object creation!

@SneakyThrows
To boldly throw checked exceptions where no one has thrown them before!

@Synchronized
synchronized done right: Don't expose your locks.

@Getter(lazy=true)
Laziness is a virtue!

@Log
Captain's Log, stardate 24435.7: "What was that line again?"

experimental
Head to the lab: The new stuff we're working on.
```


Features
@Getter and @Setter
@FieldNameConstants
@ToString
@EqualsAndHashCode
@AllArgsConstructor, @RequiredArgsConstructor and @NoArgsConstructor
@Log, @Log4j, @Log4j2, @Slf4j, @XSlf4j, @CommonsLog, @JBossLog, @Flogger
@Data
@Builder
@Singular
@Delegate
@Value
@Accessors
@Wither
@SneakyThrows
from Intellij 14.1 @val
from Intellij 15.0.2 @var
from Intellij 14.1 @var
from Intellij 2016.2 @UtilityClass
Lombok config system
Code inspections
Refactoring actions (lombok and delombok)

IDEA使用指南
https://jingyan.baidu.com/article/0a52e3f4e53ca1bf63ed725c.html
下载IDEA插件，起用annotation，pom或者其他形式下载jar

https://projectlombok.org/contributing/lombok-execution-path




lombok

idea如何调试？



lombok java12不支持



[lombok和jdk版本不兼容，将jdk12换成jdk1.8解决](https://www.jianshu.com/p/863ca3695a31)



```
Warning:(27, 8) java: lombok.javac.apt.LombokProcessor could not be initialized. Lombok will not run during this compilation: java.lang.IllegalArgumentException: com.sun.tools.javac.main.DelegatingJavaFileManager$DelegatingSJFM extends com.sun.tools.javac.main.DelegatingJavaFileManager implements javax.tools.StandardJavaFileManager
  	at lombok.javac.apt.LombokFileObjects.getCompiler(LombokFileObjects.java:148)
  	at lombok.javac.apt.InterceptingJavaFileManager.<init>(InterceptingJavaFileManager.java:40)
  	at lombok.javac.apt.LombokProcessor.placePostCompileAndDontMakeForceRoundDummiesHook(LombokProcessor.java:165)
  	at lombok.javac.apt.LombokProcessor.init(LombokProcessor.java:87)
  	at lombok.core.AnnotationProcessor$JavacDescriptor.want(AnnotationProcessor.java:87)
  	at lombok.core.AnnotationProcessor.init(AnnotationProcessor.java:140)
  	at lombok.launch.AnnotationProcessorHider$AnnotationProcessor.init(AnnotationProcessor.java:69)
  	at jdk.compiler/com.sun.tools.javac.processing.JavacProcessingEnvironment$ProcessorState.<init>(JavacProcessingEnvironment.java:691)
  	at jdk.compiler/com.sun.tools.javac.processing.JavacProcessingEnvironment$DiscoveredProcessors$ProcessorStateIterator.next(JavacProcessingEnvironment.java:791)
  	at jdk.compiler/com.sun.tools.javac.processing.JavacProcessingEnvironment.discoverAndRunProcs(JavacProcessingEnvironment.java:886)
  	at jdk.compiler/com.sun.tools.javac.processing.JavacProcessingEnvironment$Round.run(JavacProcessingEnvironment.java:1227)
  	at jdk.compiler/com.sun.tools.javac.processing.JavacProcessingEnvironment.doProcessing(JavacProcessingEnvironment.java:1339)
  	at jdk.compiler/com.sun.tools.javac.main.JavaCompiler.processAnnotations(JavaCompiler.java:1258)
  	at jdk.compiler/com.sun.tools.javac.main.JavaCompiler.compile(JavaCompiler.java:936)
  	at jdk.compiler/com.sun.tools.javac.api.JavacTaskImpl.lambda$doCall$0(JavacTaskImpl.java:104)
  	at jdk.compiler/com.sun.tools.javac.api.JavacTaskImpl.handleExceptions(JavacTaskImpl.java:147)
  	at jdk.compiler/com.sun.tools.javac.api.JavacTaskImpl.doCall(JavacTaskImpl.java:100)
  	at jdk.compiler/com.sun.tools.javac.api.JavacTaskImpl.call(JavacTaskImpl.java:94)
  	at org.jetbrains.jps.javac.JavacMain.compile(JavacMain.java:193)
  	at org.jetbrains.jps.incremental.java.JavaBuilder.compileJava(JavaBuilder.java:448)
  	at org.jetbrains.jps.incremental.java.JavaBuilder.compile(JavaBuilder.java:318)
  	at org.jetbrains.jps.incremental.java.JavaBuilder.doBuild(JavaBuilder.java:243)
  	at org.jetbrains.jps.incremental.java.JavaBuilder.build(JavaBuilder.java:201)
  	at org.jetbrains.jps.incremental.IncProjectBuilder.runModuleLevelBuilders(IncProjectBuilder.java:1317)
  	at org.jetbrains.jps.incremental.IncProjectBuilder.runBuildersForChunk(IncProjectBuilder.java:993)
  	at org.jetbrains.jps.incremental.IncProjectBuilder.buildTargetsChunk(IncProjectBuilder.java:1065)
  	at org.jetbrains.jps.incremental.IncProjectBuilder.buildChunkIfAffected(IncProjectBuilder.java:956)
  	at org.jetbrains.jps.incremental.IncProjectBuilder.buildChunks(IncProjectBuilder.java:788)
  	at org.jetbrains.jps.incremental.IncProjectBuilder.runBuild(IncProjectBuilder.java:377)
  	at org.jetbrains.jps.incremental.IncProjectBuilder.build(IncProjectBuilder.java:184)
  	at org.jetbrains.jps.cmdline.BuildRunner.runBuild(BuildRunner.java:138)
  	at org.jetbrains.jps.cmdline.BuildSession.runBuild(BuildSession.java:309)
  	at org.jetbrains.jps.cmdline.BuildSession.run(BuildSession.java:137)
  	at org.jetbrains.jps.cmdline.BuildMain$MyMessageHandler.lambda$channelRead0$0(BuildMain.java:235)
  	at org.jetbrains.jps.service.impl.SharedThreadPoolImpl.lambda$executeOnPooledThread$0(SharedThreadPoolImpl.java:42)
  	at java.base/java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:515)
  	at java.base/java.util.concurrent.FutureTask.run(FutureTask.java:264)
  	at java.base/java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1128)
  	at java.base/java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:628)
  	at java.base/java.lang.Thread.run(Thread.java:835)
```



