# Launch


Launcher作为JAVA应用的入口，根据双亲委派模型，Laucher是由JVM创建的，它类加载器应该是BootStrapClassLoader， 这是一个C++编写的类加载器，是java应用体系中最顶层的类加载器，负责加载JVM需要的一些类库(<JAVA_HOME>/lib)。可以通过一个简单的代码验证一下我们的想法。

```java


public class App {
    public static void main(String[] args) {
        ClassLoader classLoader = Launcher.class.getClassLoader();
    }
}
```
这里的classLoader是null，说明Launcher确实是BootstrapClassLoader加载的，那么我们就会非常好奇，

