# atomic


什么是原子类？什么情况下使用原子类？
java 1.5引进原子类，具体在java.util.concurrent.atomic包下，atomic包里面一共提供了13个类，分为4种类型，分别是：原子更新基本类型，原子更新数组，原子更新引用，原子更新属性。原子类也是java实现同步的一套解决方案。
原子类的原理是cas指令
go中的Cas操作与java中类似，都是借用了CPU提供的原子性指令来实现。CAS操作修改共享变量时候不需要对共享变量加锁，而是通过类似乐观锁的方式进行检查，本质还是不断的占用CPU 资源换取加锁带来的开销（比如上下文切换开销）。
https://zhuanlan.zhihu.com/p/56733484


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



AtomicStampedReference可以解决ABA问题。ABA问题是指:

- 一个变量A由一个线程读取,得值a
- 然后被另一个线程修改为b
- 后再被修改回a
- 这个时候,第一个线程以为变量没有被修改,但实际上已经修改过了。

AtomicStampedReference通过添加一个版本号来解决这个问题。
public int getStamp() {
        return pair.stamp;
    }
它的工作原理是:

1. 每次对引用进行修改时,同时将版本号(stamp)加1 
2. 读取引用时,也读取版本号
3. 修改引用时,需要传入读取时得到的版本号
4. 如果版本号不匹配,则表示有其他线程在修改,抛出失败

举个例子:

```java
AtomicStampedReference<Integer> ref 
                                  = new AtomicStampedReference<>(1, 1);

int stamp = ref.getStamp();
int value = ref.getReference(); // 1

ref.set(2, stamp); // 使用旧版本号,会失败

stamp = ref.getStamp();
value = ref.getReference(); // 1

ref.compareAndSet(1, 3, stamp, stamp + 1);

stamp = ref.getStamp();
value = ref.getReference(); // 3
```

在这个例子中,由于每次修改引用时,版本号都加1。即使值1和3相同,但版本号不同,所以能正确区分 ABA问题。

希望这能够帮助你理解AtomicStampedReference如何解决ABA问题!如果仍有疑问,欢迎随时交流。