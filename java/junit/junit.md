# junit

Junit 4.11里增加了指定测试方法执行顺序的特性
测试类的执行顺序可通过对测试类添加注解 “@FixMethodOrder(value)” 来指定,其中value 为执行顺序
三种执行顺序可供选择：默认（MethodSorters.DEFAULT），按方法名（MethodSorters.NAME_ASCENDING）和JVM（MethodSorters.JVM）
当没有指定任何顺序时，按默认来执行

[Junit] 测试方法执行顺序 
https://www.cnblogs.com/lukehuang/p/3284766.html

JUnit测试框架中没有`main`函数。相反，JUnit测试是由特殊的测试运行器（Test Runner）来运行的。测试运行器负责加载测试类、调用测试方法，并报告测试结果。JUnit 4中默认的测试运行器是`org.junit.runner.JUnitCore`，JUnit 5中默认的测试运行器是`org.junit.platform.console.ConsoleLauncher`。
要运行JUnit测试，您可以使用各种工具和IDE，如Eclipse、IntelliJ IDEA、Maven、Gradle等，它们都提供了内置的JUnit测试运行器。
在Eclipse中，您可以通过右键单击测试类，然后选择"Run as" -> "JUnit Test"来运行测试。在IntelliJ IDEA中，您可以右键单击测试类，然后选择"Run" -> "TestClass"来运行测试。
如果您想在命令行中运行JUnit测试，可以使用`java`命令来调用测试运行器。例如，在JUnit 4中，您可以使用以下命令来运行测试：
```
java -cp junit.jar:your-test-classes-dir org.junit.runner.JUnitCore com.example.YourTest
```
其中，`junit.jar`是JUnit库的路径，`your-test-classes-dir`是测试类的路径，`com.example.YourTest`是您要运行的测试类的名称。在JUnit 5中，您可以使用以下命令来运行测试：
```
java -jar junit-platform-console-standalone.jar --class-path your-test-classes-dir --scan-classpath
```
其中，`junit-platform-console-standalone.jar`是JUnit 5的测试运行器，`your-test-classes-dir`是测试类的路径。通过使用`--scan-classpath`选项，JUnit 5会自动扫描类路径中的测试类并运行测试。

使用Java JUnit框架里的@SuiteClasses注解管理测试用例
http://blog.itpub.net/24475491/viewspace-2703835/



JUnit4---Hamcrest匹配器常用方法总结
https://www.cnblogs.com/jpfss/p/10955939.html


```java
Class SpringJUnit4ClassRunner
java.lang.Object
org.junit.runner.Runner
org.junit.runners.ParentRunner<FrameworkMethod>
org.junit.runners.BlockJUnit4ClassRunner
org.springframework.test.context.junit4.SpringJUnit4ClassRunner

```

http://www.java1234.com/a/javabook/javaweb/2013/1108/1031.html

```shell
java.lang.Exception: Method setUp() should be public
	at org.junit.runners.model.FrameworkMethod.validatePublicVoid(FrameworkMethod.java:94)
	at org.junit.runners.model.FrameworkMethod.validatePublicVoidNoArg(FrameworkMethod.java:70)
	at org.junit.runners.ParentRunner.validatePublicVoidNoArgMethods(ParentRunner.java:133)
	at org.junit.runners.BlockJUnit4ClassRunner.validateInstanceMethods(BlockJUnit4ClassRunner.java:165)
	at org.junit.runners.BlockJUnit4ClassRunner.collectInitializationErrors(BlockJUnit4ClassRunner.java:104)
	at org.junit.runners.ParentRunner.validate(ParentRunner.java:355)
	at org.junit.runners.ParentRunner.<init>(ParentRunner.java:76)
	at org.junit.runners.BlockJUnit4ClassRunner.<init>(BlockJUnit4ClassRunner.java:57)
	at org.junit.internal.builders.JUnit4Builder.runnerForClass(JUnit4Builder.java:10)
	at org.junit.runners.model.RunnerBuilder.safeRunnerForClass(RunnerBuilder.java:59)
	at org.junit.internal.builders.AllDefaultPossibilitiesBuilder.runnerForClass(AllDefaultPossibilitiesBuilder.java:26)
	at org.junit.runners.model.RunnerBuilder.safeRunnerForClass(RunnerBuilder.java:59)
	at org.junit.internal.requests.ClassRequest.getRunner(ClassRequest.java:26)
	at com.intellij.junit4.JUnit4IdeaTestRunner.startRunnerWithArgs(JUnit4IdeaTestRunner.java:49)
	at com.intellij.rt.execution.junit.IdeaTestRunner$Repeater.startRunnerWithArgs(IdeaTestRunner.java:47)
	at com.intellij.rt.execution.junit.JUnitStarter.prepareStreamsAndStart(JUnitStarter.java:242)
	at com.intellij.rt.execution.junit.JUnitStarter.main(JUnitStarter.java:70)

```





[关于Junit中Assert已经过时](https://blog.csdn.net/qq_36791569/article/details/80383546)


[单元测试利器JUnit4](http://www.java1234.com/a/javabook/javaweb/2013/1108/1031.html)



[IDEA中使用Junit4进行测试的入门配置](https://blog.csdn.net/hanchao5272/article/details/79197989)


http://www.java1234.com/a/javabook/javaweb/2013/1108/1031.html

	@BeforeClass
	public static void init(){
	}
Method init() should be static

http://www.java1234.com/a/javabook/javaweb/2013/1108/1031.html





```shell
java.lang.Exception: Method mainsdddddddd should have no parameters
	at org.junit.runners.model.FrameworkMethod.validatePublicVoidNoArg(FrameworkMethod.java:76)
	at org.junit.runners.ParentRunner.validatePublicVoidNoArgMethods(ParentRunner.java:155)
	at org.junit.runners.BlockJUnit4ClassRunner.validateTestMethods(BlockJUnit4ClassRunner.java:208)
	at org.junit.runners.BlockJUnit4ClassRunner.validateInstanceMethods(BlockJUnit4ClassRunner.java:188)
	at org.junit.runners.BlockJUnit4ClassRunner.collectInitializationErrors(BlockJUnit4ClassRunner.java:128)
	at org.junit.runners.ParentRunner.validate(ParentRunner.java:416)
	at org.junit.runners.ParentRunner.<init>(ParentRunner.java:84)
	at org.junit.runners.BlockJUnit4ClassRunner.<init>(BlockJUnit4ClassRunner.java:65)
	at org.junit.internal.builders.JUnit4Builder.runnerForClass(JUnit4Builder.java:10)
	at org.junit.runners.model.RunnerBuilder.safeRunnerForClass(RunnerBuilder.java:59)
	at org.junit.internal.builders.AllDefaultPossibilitiesBuilder.runnerForClass(AllDefaultPossibilitiesBuilder.java:26)
	at org.junit.runners.model.RunnerBuilder.safeRunnerForClass(RunnerBuilder.java:59)
	at org.junit.internal.requests.ClassRequest.getRunner(ClassRequest.java:33)
	at org.junit.internal.requests.FilterRequest.getRunner(FilterRequest.java:36)
	at com.intellij.junit4.JUnit4IdeaTestRunner.startRunnerWithArgs(JUnit4IdeaTestRunner.java:49)
	at com.intellij.rt.execution.junit.IdeaTestRunner$Repeater.startRunnerWithArgs(IdeaTestRunner.java:47)
	at com.intellij.rt.execution.junit.JUnitStarter.prepareStreamsAndStart(JUnitStarter.java:242)
	at com.intellij.rt.execution.junit.JUnitStarter.main(JUnitStarter.java:70)
Process finished with exit code -1
```



JUnit
@Before
@BeforeClass

@Before,@After和@BeforeClass和@AfterClass的区别
https://blog.csdn.net/dingjiajia_949/article/details/80183828



