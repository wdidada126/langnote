# jdk17

JDK15在2020年9月15日正式发布了，这次的JDK15给我们带了隐藏类，EdDSA，模式匹配，Records，封闭类和Text

## JDK 17

https://openjdk.org/projects/jdk/17/

JDK 17 is the open-source reference implementation of version 17 of the Java SE Platform, as specified by by JSR 390 in the Java Community Process.

JDK 17 reached General Availability on 14 September 2021. Production-ready binaries under the GPL are available from Oracle; binaries from other vendors will follow shortly.

The features and schedule of this release were proposed and tracked via the JEP Process, as amended by the JEP 2.0 proposal. The release was produced using the JDK Release Process (JEP 3).

Features
306:	Restore Always-Strict Floating-Point Semantics
356:	Enhanced Pseudo-Random Number Generators
382:	New macOS Rendering Pipeline
391:	macOS/AArch64 Port
398:	Deprecate the Applet API for Removal
403:	Strongly Encapsulate JDK Internals
406:	Pattern Matching for switch (Preview)
407:	Remove RMI Activation
409:	Sealed Classes
410:	Remove the Experimental AOT and JIT Compiler
411:	Deprecate the Security Manager for Removal
412:	Foreign Function & Memory API (Incubator)
414:	Vector API (Second Incubator)
415:	Context-Specific Deserialization Filters
JDK 17 will be a long-term support (LTS) release from most vendors. For a complete list of the JEPs integrated since the previous LTS release, JDK 11, please see here.

Schedule
2021/06/10		Rampdown Phase One (fork from main line)
2021/07/15		Rampdown Phase Two
2021/08/05		Initial Release Candidate
2021/08/19		Final Release Candidate
2021/09/14		General Availability

## JDK 18
JDK 18 is the open-source reference implementation of version 18 of the Java SE Platform, as specified by by JSR 393 in the Java Community Process.

JDK 18 reached General Availability on 22 March 2022. Production-ready binaries under the GPL are available from Oracle; binaries from other vendors will follow shortly.

The features and schedule of this release were proposed and tracked via the JEP Process, as amended by the JEP 2.0 proposal. The release was produced using the JDK Release Process (JEP 3).

Features
400:	UTF-8 by Default
408:	Simple Web Server
413:	Code Snippets in Java API Documentation
416:	Reimplement Core Reflection with Method Handles
417:	Vector API (Third Incubator)
418:	Internet-Address Resolution SPI
419:	Foreign Function & Memory API (Second Incubator)
420:	Pattern Matching for switch (Second Preview)
421:	Deprecate Finalization for Removal
Schedule
2021/12/09		Rampdown Phase One (fork from main line)
2022/01/20		Rampdown Phase Two
2022/02/10		Initial Release Candidate
2022/02/24		Final Release Candidate
2022/03/22		General Availability

https://openjdk.org/projects/jdk/18/

## JDK 19
JDK 19 is the open-source reference implementation of version 19 of the Java SE Platform, as specified by by JSR 394 in the Java Community Process.

JDK 19 reached General Availability on 20 September 2022. Production-ready binaries under the GPL are available from Oracle; binaries from other vendors will follow shortly.

The features and schedule of this release were proposed and tracked via the JEP Process, as amended by the JEP 2.0 proposal. The release was produced using the JDK Release Process (JEP 3).

Features
405:	Record Patterns (Preview)
422:	Linux/RISC-V Port
424:	Foreign Function & Memory API (Preview)
425:	Virtual Threads (Preview)
426:	Vector API (Fourth Incubator)
427:	Pattern Matching for switch (Third Preview)
428:	Structured Concurrency (Incubator)
Schedule
2022/06/09		Rampdown Phase One (fork from main line)
2022/07/21		Rampdown Phase Two
2022/08/11		Initial Release Candidate
2022/08/25		Final Release Candidate
2022/09/20		General Availability

# Java 17 Record 关键字详解
`record` 是 Java 16 正式引入、Java 17 长期支持的新关键字，核心作用是：快速定义不可变的纯数据类，自动生成模板代码，让代码更简洁、更安全。

## 一、核心作用
传统 Java 中，定义一个只存数据的类（DTO、VO、POJO），需要手动写：
- 私有 final 字段
- 构造方法
- `equals()`/`hashCode()`
- `toString()`
- getter 方法

用 `record` 一行就能搞定，所有模板代码自动生成。

## 二、基础语法
```java
// 定义 Record 类
public record 类名(字段列表) {
    // 可选：自定义方法/构造
}
```

### 极简示例
```java
// 自动生成：私有final字段、全参构造、equals/hashCode/toString、getter(直接用字段名)
public record User(Long id, String username, int age) {}
```

## 三、自动生成的内容（无需手写）
1. 私有 final 成员变量：所有声明的字段都是 `private final`
2. 全参构造方法：`User(Long id, String username, int age)`
3. 访问方法：直接用字段名获取值（不是 `getXxx()`）
   ```java
   User user = new User(1L, "张三", 20);
   System.out.println(user.username()); // 输出：张三
   ```
4. equals() & hashCode()：基于所有字段比较
5. toString()：自动拼接类名+所有字段值
6. 不可变：字段赋值后无法修改（天然线程安全）

## 四、完整使用示例
```java
public class RecordDemo {
    public static void main(String[] args) {
        // 1. 创建对象
        User user = new User(1L, "李四", 25);

        // 2. 获取字段（直接用字段名）
        System.out.println(user.id());
        System.out.println(user.username());
        System.out.println(user.age());

        // 3. 自动toString
        System.out.println(user); 
        // 输出：User[id=1, username=李四, age=25]

        // 4. 比较对象（基于所有字段）
        User user2 = new User(1L, "李四", 25);
        System.out.println(user.equals(user2)); // true
    }
}
```

## 五、高级用法
### 1. 自定义构造方法（校验数据）
可以加紧凑构造做参数校验：
```java
public record User(Long id, String username, int age) {
    // 紧凑构造：自动接收所有参数，用于校验
    public User {
        if (id == null || id < 0) {
            throw new IllegalArgumentException("id不能为负数");
        }
        if (username.isBlank()) {
            throw new IllegalArgumentException("用户名不能为空");
        }
    }
}
```

### 2. 自定义普通方法
Record 可以添加自己的方法：
```java
public record User(Long id, String username, int age) {
    // 自定义方法
    public boolean isAdult() {
        return age >= 18;
    }
}
```

### 3. 静态字段/静态方法
Record 只能定义静态成员，不能定义实例成员变量：
```java
public record User(Long id, String username, int age) {
    // 允许静态字段
    public static final int ADULT_AGE = 18;
    
    // 允许静态方法
    public static User createAnonymous() {
        return new User(0L, "匿名用户", 0);
    }
}
```

## 六、Record 关键限制（必须记住）
1. 默认不可变：字段都是 `private final`，无法修改值
2. 不能继承：Record 隐式继承 `java.lang.Record`，Java 单继承，所以不能再继承其他类
3. 不能声明实例字段：只能使用构造参数里声明的字段
4. 不能用 abstract 修饰：Record 默认是 final 类
5. 不能定义 setter 方法：天然不可变

## 七、最佳使用场景
✅ 推荐使用：
- DTO（数据传输对象）
- VO（视图对象）
- 方法返回多个值
- 纯数据载体、临时数据对象

❌ 不推荐使用：
- 需要修改字段的类
- 复杂业务逻辑类
- 实体类（需要被框架修改属性）

## 八、和普通类的对比
| 特性         | 普通 Java 类                | Record 关键字                |
|--------------|-----------------------------|-----------------------------|
| 代码量       | 多（需手写模板代码）| 极少（一行定义）|
| 不可变性     | 需手动加 final              | 自动 final，天然不可变      |
| equals/hashCode | 需手动生成/依赖Lombok | 自动生成                    |
| 继承         | 可自定义继承                | 只能继承 Record，不能继承其他 |
| Getter       | `getXxx()`                  | 直接用字段名            |

### 总结
1. `record` = 极简不可变数据类，自动生成所有模板代码
2. 字段是 `private final`，不可修改，线程安全
3. 访问字段用 `对象.字段名()`，不是 `getXxx()`
4. 适合纯数据场景，是替代 Lombok/@Data 的官方方案
5. Java 17+ 原生支持，无需任何插件和依赖
