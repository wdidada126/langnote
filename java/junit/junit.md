# junit

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





```
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







