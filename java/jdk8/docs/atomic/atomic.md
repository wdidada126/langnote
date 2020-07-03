# atomic

基本类：AtomicInteger、AtomicLong、AtomicBoolean；
引用类型：AtomicReference、AtomicReference的ABA实例、AtomicStampedRerence、AtomicMarkableReference；
数组类型：AtomicIntegerArray、AtomicLongArray、AtomicReferenceArray
属性原子修改器（Updater）：AtomicIntegerFieldUpdater、AtomicLongFieldUpdater、AtomicReferenceFieldUpdater



AtomicReference常用方法
```java
public AtomicReference(V initialValue)
public final boolean compareAndSet(V expect, V update)
```

AtomicReference的构造函数可以是List对象



AtomicReferenceFieldUpdater含有双泛型


```java
public abstract boolean compareAndSet(T obj, V expect, V update);
```

