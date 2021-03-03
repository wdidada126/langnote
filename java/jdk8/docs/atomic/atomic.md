# atomic


Number (java.lang)
    Striped64 (java.util.concurrent.atomic)
        LongAdder (java.util.concurrent.atomic)
            LongAdderCounter (io.netty.util.internal)
        LongAccumulator (java.util.concurrent.atomic)
        DoubleAdder (java.util.concurrent.atomic)
        DoubleAccumulator (java.util.concurrent.atomic)



总结 atomic用到了sun.misc.Unsafe

Java cas（compareandset函数

java中，boolean是用int实现的

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

### AtomicInteger

java.util.concurrent.atomic.AtomicInteger#AtomicInteger(int)
java.util.concurrent.atomic.AtomicInteger#AtomicInteger()
java.util.concurrent.atomic.AtomicInteger#get
java.util.concurrent.atomic.AtomicInteger#set
java.util.concurrent.atomic.AtomicInteger#lazySet
java.util.concurrent.atomic.AtomicInteger#getAndSet
java.util.concurrent.atomic.AtomicInteger#compareAndSet
java.util.concurrent.atomic.AtomicInteger#weakCompareAndSet
java.util.concurrent.atomic.AtomicInteger#getAndIncrement
java.util.concurrent.atomic.AtomicInteger#getAndDecrement
java.util.concurrent.atomic.AtomicInteger#getAndAdd
java.util.concurrent.atomic.AtomicInteger#incrementAndGet
java.util.concurrent.atomic.AtomicInteger#decrementAndGet
java.util.concurrent.atomic.AtomicInteger#addAndGet
java.util.concurrent.atomic.AtomicInteger#getAndUpdate
java.util.concurrent.atomic.AtomicInteger#updateAndGet
java.util.concurrent.atomic.AtomicInteger#getAndAccumulate
java.util.concurrent.atomic.AtomicInteger#accumulateAndGet



直接引用私有静态 Unsafe unsafe = Unsafe.getUnsafe();

java.util.concurrent.atomic.AtomicLong#AtomicLong(long)
java.util.concurrent.atomic.AtomicLong#AtomicLong()
java.util.concurrent.atomic.AtomicLong#get
java.util.concurrent.atomic.AtomicLong#set
java.util.concurrent.atomic.AtomicLong#lazySet
java.util.concurrent.atomic.AtomicLong#getAndSet
java.util.concurrent.atomic.AtomicLong#compareAndSet
java.util.concurrent.atomic.AtomicLong#weakCompareAndSet
java.util.concurrent.atomic.AtomicLong#getAndIncrement
java.util.concurrent.atomic.AtomicLong#getAndDecrement
java.util.concurrent.atomic.AtomicLong#getAndAdd
java.util.concurrent.atomic.AtomicLong#incrementAndGet
java.util.concurrent.atomic.AtomicLong#decrementAndGet
java.util.concurrent.atomic.AtomicLong#addAndGet
java.util.concurrent.atomic.AtomicLong#getAndUpdate
java.util.concurrent.atomic.AtomicLong#updateAndGet
java.util.concurrent.atomic.AtomicLong#getAndAccumulate
java.util.concurrent.atomic.AtomicLong#accumulateAndGet



```java
    private static final Unsafe unsafe = Unsafe.getUnsafe();
    private static final long valueOffset;
    static {
        try {
            valueOffset = unsafe.objectFieldOffset
                (AtomicLong.class.getDeclaredField("value"));
        } catch (Exception ex) { throw new Error(ex); }
    }
```

```java
    public final boolean compareAndSet(long expect, long update) {
        return unsafe.compareAndSwapLong(this, valueOffset, expect, update);
    }
```

int long boolean是AtomicReference这个泛型类的特例

AtomicReference
AtomicReference
get
set
lazySet
compareAndSet
weakCompareAndSet
getAndSet
getAndUpdate
updateAndGet
getAndAccumulate
accumulateAndGet



java.util.concurrent.atomic.AtomicStampedReference.Pair
内部类 一个int参数


java.util.concurrent.atomic.AtomicMarkableReference.Pair
一个boolean参数


AtomicIntegerArray
compareAndSet(int i, int expect, int update)
注意跟AtomicInteger对比


AtomicReferenceArray

AtomicReferenceArray<E>

```java
public AtomicReferenceArray(int length) {
    array = new Object[length];
}
```

构造函数 两个，给array赋值

属性有一个Object类数组

Object[] array
private static final Unsafe unsafe
