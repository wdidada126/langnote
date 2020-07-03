# ThreadLocal

[JAVA并发-自问自答学ThreadLocal](https://juejin.im/post/5a0e985df265da430e4ebb92)
[Java 之 ThreadLocal 详解](https://www.jianshu.com/p/3a196baa227b)

ThreadLocal提供线程内部的局部变量，在本线程内随时随地可取，隔离其他线程。
不光Java里面有，C#里面也有ThreadLocal

```shell
public void set(T value)
public T get()
```
