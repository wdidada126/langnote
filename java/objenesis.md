# objenesis

不使用构造函数，通过字节码生辰对象？
Objjenesis是一个轻量级的Java库，它的作用是绕过构造器创建一个实例。
Java已经支持通过Class.newInstance()动态实例化Java类，但是这需要Java类有个适当的构造器。很多时候一个Java类无法通过这种途径创建，例如：构造器需要参数、构造器有副作用、构造器会抛出异常等。这时，Objjenesis可以用来克服这些限制。

它一般用于以下场景：
序列化：不需要调用代码即可将Java类实例化并存储特定状态。
远程处理和持久化：代理、AOP库和Mock对象可以创建特定Java类的子类而无需考虑super()构造器。
容器框架：可以用非标准方式动态地实例化Java类。
以上信息仅供参考，建议查阅Objjenesis的官方文档获取更多更准确的信息。

        <dependency>
            <groupId>org.objenesis</groupId>
            <artifactId>objenesis</artifactId>
            <version>3.2</version>
        </dependency>

https://gitee.com/edidada/testobjenesis

spring core这个jar包
org.springframework.objenesis
