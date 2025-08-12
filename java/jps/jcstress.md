# jcstress

jcstress（Java Concurrency Stress Test）是 OpenJDK 提供的工具，专门用于测试并发代码的正确性和性能。以下是一个完整的使用示例，包括编写、运行和分析测试。

1. 环境准备

• JDK 8+（推荐最新LTS版本，如JDK 17/21）。

• Maven/Gradle（用于依赖管理）。

• jcstress依赖：
  <!-- Maven 依赖 -->
  <dependency>
      <groupId>org.openjdk.jcstress</groupId>
      <artifactId>jcstress-core</artifactId>
      <version>0.16</version>
  </dependency>
  

2. 编写测试用例

示例：测试 volatile 变量的可见性

import org.openjdk.jcstress.annotations.*;
import org.openjdk.jcstress.infra.results.I_Result;

@JCStressTest
@Outcome(id = "1", expect = Expect.ACCEPTABLE, desc = "正确：volatile保证可见性")
@Outcome(id = "0", expect = Expect.ACCEPTABLE_INTERESTING, desc = "错误：未观察到写入")
@State
public class VolatileVisibilityTest {
    private volatile int x = 0;

    @Actor
    public void writer() {
        x = 1; // 写入volatile变量
    }

    @Actor
    public void reader(I_Result r) {
        r.r1 = x; // 读取volatile变量
    }
}


关键注解说明：

• @JCStressTest：标记测试类。

• @State：标记共享状态类（会被多线程访问）。

• @Actor：标记并发操作的方法（每个方法运行在独立线程）。

• @Outcome：定义预期结果和分类。

3. 运行测试

方式1：通过Maven插件运行

在pom.xml中添加插件：
<build>
    <plugins>
        <plugin>
            <groupId>org.openjdk.jcstress</groupId>
            <artifactId>jcstress-maven-plugin</artifactId>
            <version>0.16</version>
            <executions>
                <execution>
                    <goals>
                        <goal>test</goal>
                    </goals>
                </execution>
            </executions>
        </plugin>
    </plugins>
</build>

运行命令：
mvn clean verify


方式2：直接运行Main类

import org.openjdk.jcstress.Main;
public class RunTest {
    public static void main(String[] args) throws Exception {
        Main.main(new String[]{"-t", "VolatileVisibilityTest"});
    }
}

4. 分析结果

输出示例：

[OK] org.openjdk.jcstress.tests.VolatileVisibilityTest
  Observed state   Occurrences   Expectation  Interpretation
              1     10,000,000    ACCEPTABLE  正确：volatile保证可见性
              0             0   ACCEPTABLE_INTERESTING  错误：未观察到写入

• ACCEPTABLE：符合预期的结果。

• ACCEPTABLE_INTERESTING：可能暴露并发问题的结果（如本例中未观察到x=1的写入）。

5. 高级用法

自定义测试参数

@JCStressTest
@Description("测试CAS操作")
@Outcome(...)
public class CASTest {
    private AtomicInteger counter = new AtomicInteger(0);

    @Actor
    public void increment() {
        counter.incrementAndGet();
    }

    @Arbiter  // 在所有Actor执行后运行
    public void checkResult(I_Result r) {
        r.r1 = counter.get();
    }
}

控制线程数和迭代次数

通过JVM参数调整：
java -jar jcstress.jar -t MyTest -iter 100000 -threads 8

6. 查看所有内置测试

java -jar jcstress.jar -l

常见问题

1. 测试未执行：确保类路径包含jcstress-core和编译后的测试类。
2. 结果不明确：增加迭代次数（-iter）或调整测试逻辑。
3. 性能分析：结合-XX:+PrintAssembly查看JIT生成的指令。

通过jcstress，你可以系统地验证并发代码的正确性，尤其适合测试锁、原子变量、内存模型等场景。
