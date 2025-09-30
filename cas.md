# cas

现在cpu提供的指令


利用CAS操作（Compare & Set）实现无锁队列

https://zhuanlan.zhihu.com/p/80727111

无锁队列的链表实现
下面的东西主要来自John D. Valois 1994年10月在拉斯维加斯的并行和分布系统系统国际大会上的一篇论文——《Implementing Lock-Free Queues》。

我们先来看一下进队列用CAS实现的方式：
https://blog.csdn.net/syzcch/article/details/8075830

CAS 算法存在哪些问题？
ABA 问题是 CAS 算法最常见的问题。

ABA 问题
如果一个变量 V 初次读取的时候是 A 值，并且在准备赋值的时候检查到它仍然是 A 值，那我们就能说明它的值没有被其他线程修改过了吗？很明显是不能的，因为在这段时间它的值可能被改为其他值，然后又改回 A，那 CAS 操作就会误认为它从来没有被修改过。这个问题被称为 CAS 操作的 "ABA"问题。ABA 问题的解决思路是在变量前面追加上版本号或者时间戳。JDK 1.5 以后的 AtomicStampedReference 类就是用来解决 ABA 问题的，其中的 compareAndSet() 方法就是首先检查当前引用是否等于预期引用，并且当前标志是否等于预期标志，如果全部相等，则以原子方式将该引用和该

标志的值设置为给定的更新值。

循环时间长开销大CAS 经常会用到自旋操作来进行重试，也就是不成功就一直循环执行直到成功。如果长时间不成功，会给 CPU 带来非常大的执行开销。如果 JVM 能支持处理器提供的 pause 指令那么效率会有一定的提升，pause 指令有两个作用：可以延迟流水线执行指令，使 CPU 不会消耗过多的执行资源，延迟的时间取决于具体实现的版本，在一些处理器上延迟时间是零。可以避免在退出循环的时候因内存顺序冲突而引起 CPU 流水线被清空，从而提高 CPU 的执行效率。只能保证一个共享变量的原子操作CAS 只对单个共享变量有效，当操作涉及跨多个共享变量时 CAS 无效。但是从 JDK 1.5 开始，提供了AtomicReference类来保证引用对象之间的原子性，你可以把多个变量放在一个对象里来进行 CAS 操作.所以我们可以使用锁或者利用AtomicReference类把多个共享变量合并成一个共享变量来操作。总结

各种锁及其Java实现.mhtnl
一文彻底搞懂CAS实现原理.mhtnl

CAS（Compare-And-Swap，比较并交换） 是一种重要的原子操作，在并发编程中用于实现无锁算法。Java 标准库通过 `java.util.concurrent.atomic` 包提供了对 CAS 操作的支持。下面详细介绍 CAS 解决了什么问题 以及其在 Java 中的应用。

---

## 🎯 一、CAS 解决的核心问题

### ✅ 1. 数据竞争（Data Race）

当多个线程试图同时访问和修改同一个变量时，可能会导致不一致的状态或错误的结果。CAS 提供了一种机制来确保变量的更新是原子性的，从而避免了数据竞争。

```java
// 假设没有同步措施
int sharedValue = 0;

Thread A: sharedValue += 1; // 可能与 Thread B 同时执行
Thread B: sharedValue += 1;
```

> 如果两个线程几乎同时读取相同的初始值（如 0），然后各自加 1 再写回，最终结果可能只是 1 而不是期望的 2。这是典型的数据竞争。

### ✅ 2. 死锁（Deadlock）

传统的同步机制如 `synchronized` 或 `ReentrantLock` 需要显式获取和释放锁，容易造成死锁。而 CAS 是无锁的，它通过循环尝试更新而不是持有锁来避免死锁。

### ✅ 3. 性能瓶颈

锁机制可能导致线程阻塞等待锁释放，尤其是在高争用场景下性能会显著下降。CAS 提供了非阻塞的方式进行并发控制，通常比锁具有更好的性能。

---

## 🔍 二、CAS 的工作原理

### ✅ 基本流程

1. 读取当前值：读取共享变量的当前值 V。
2. 计算新值：基于旧值 V 计算出新值 N。
3. 比较并交换：
   - 如果当前值仍为 V，则将新值 N 写入（成功）
   - 如果当前值不再是 V，则放弃本次操作或重试（失败）

```java
public final boolean compareAndSet(int expect, int update) {
    return unsafe.compareAndSwapInt(this, valueOffset, expect, update);
}
```

### ✅ 示例：使用 `AtomicInteger` 实现计数器

```java
import java.util.concurrent.atomic.AtomicInteger;

public class Counter {
    private AtomicInteger count = new AtomicInteger(0);

    public void increment() {
        int oldValue;
        do {
            oldValue = count.get(); // 获取当前值
        } while (!count.compareAndSet(oldValue, oldValue + 1)); // 尝试更新
    }
}
```

---

## 🧱 三、Java 中的 CAS 支持

### ✅ 1. `java.util.concurrent.atomic` 包

该包提供了一系列支持 CAS 操作的类：

| 类型 | 描述 |
|------|------|
| `AtomicInteger`, `AtomicLong` | 基本整数类型 |
| `AtomicBoolean` | 布尔类型 |
| `AtomicReference<V>` | 对象引用 |
| `AtomicIntegerArray`, `AtomicLongArray` | 数组形式 |
| `AtomicIntegerFieldUpdater<T>`, `AtomicLongFieldUpdater<T>` | 字段级更新 |

### ✅ 2. `Unsafe` 类

底层通过 `sun.misc.Unsafe` 提供对 CAS 的直接支持。不过直接使用 `Unsafe` 是不推荐的，因为它是 JVM 内部API，不稳定且不易移植。

```java
// Unsafe 实现细节隐藏在 atomic 包内部
private static final sun.misc.Unsafe UNSAFE;
private static final long valueOffset;
static {
    try {
        UNSAFE = sun.misc.Unsafe.getUnsafe();
        Class<?> ak = AtomicExample.class;
        valueOffset = UNSAFE.objectFieldOffset(
            ak.getDeclaredField("value"));
    } catch (Exception ex) { throw new Error(ex); }
}
```

---

## 🛠 四、CAS 的优势与挑战

### ✅ 优点

- 无锁化：减少了线程上下文切换和调度开销。
- 高性能：在低争用场景下性能优于锁。
- 避免死锁：由于没有锁的存在，自然避免了死锁问题。

### ⚠️ 缺点

- ABA 问题：如果一个变量从 A -> B -> A，CAS 无法检测到这种变化。解决方案是使用带版本号的 CAS（如 `AtomicStampedReference`）。
  
  ```java
  AtomicStampedReference<Integer> asr = new AtomicStampedReference<>(1, 0);
  ```

- 自旋消耗：在高争用场景下，CAS 可能反复失败，导致 CPU 占用率上升。

##  五、CAS 在 Java 并发包中的应用

###  1. `ConcurrentHashMap`

- 使用 CAS 实现无锁化的扩容和元素插入。
- 减少了传统 HashMap 在并发环境下的锁竞争。

###  2. `ConcurrentLinkedQueue`

- 使用 CAS 实现无锁队列，适合高并发场景下的生产者-消费者模式。

###  3. `AtomicXXX` 系列类

- 提供了高效的原子操作，广泛应用于需要精确控制的并发场景。

##  六、总结：CAS 解决了哪些问题？

| 问题 | CAS 如何解决 |
|------|-------------|
| 数据竞争 | 保证变量更新的原子性，防止多线程同时修改 |
| 死锁 | 无需显式获取锁，采用乐观锁策略，减少锁依赖 |
| 性能瓶颈 | 无锁设计，降低线程阻塞频率，提升吞吐量 |
| ABA 问题 | 提供带有版本号的 CAS 实现（如 `AtomicStampedReference`） |

###  最佳实践建议：

1. 优先考虑 `AtomicXXX` 类：它们封装了 CAS 操作，简单易用。
2. 注意 ABA 问题：在有版本需求的场景下使用 `AtomicStampedReference`。
3. 评估应用场景：CAS 更适合读多写少的场景，高争用下可能不如锁高效。

如果你想看：
- CAS 的底层汇编实现
- 如何用 `VarHandle` 实现 CAS 操作
- `ConcurrentHashMap` 中 CAS 的具体应用案例


CAS（Compare-And-Swap） 是现代处理器提供的一种原子操作指令，它允许在不使用锁的情况下安全地进行并发更新。为了更好地理解 CAS 的工作原理，我们来探讨一下它的底层汇编实现。

### CAS 操作的基本流程

1. 读取当前值：获取共享变量的当前值。
2. 比较并交换：如果当前值与预期值相等，则将新值写入；否则，不执行任何操作。

对于不同的处理器架构（如 x86、ARM），CAS 的具体实现细节有所不同，但它们都提供了类似的功能。


##  一、x86/x86_64 架构下的 CAS 实现

在 x86 架构下，CAS 操作通常通过 `CMPXCHG` 指令来实现。该指令会比较指定内存位置的内容与一个寄存器中的值，如果相等则用另一个寄存器中的值替换内存位置的内容，并设置标志位表示是否成功。

### 示例：32 位整数的 CAS 操作

```assembly
; eax = expected value
; [mem] = memory location to compare and swap
; ebx = new value

lock cmpxchg dword ptr [mem], ebx
```

- `cmpxchg` 比较 `[mem]` 和 `eax` 中的值。
- 如果相等，则将 `ebx` 的值写入 `[mem]`。
- `lock` 前缀确保了该指令是原子性的，即使在多处理器环境中也能保证正确性。

### 示例代码解释：

假设我们要对一个 `int` 类型的变量执行 CAS 操作，以下是伪代码对应的汇编实现：

```java
public final boolean compareAndSet(int expect, int update) {
    return unsafe.compareAndSwapInt(this, valueOffset, expect, update);
}
```

其对应的 x86 汇编大致如下：

```assembly
; 假设 rax 存储的是 'expect'，rbx 存储的是 'update'
; rcx 存储的是对象地址 + 偏移量（valueOffset）

mov rdx, [rcx]        ; 将内存位置的当前值加载到 rdx 寄存器
cmp rdx, rax          ; 比较内存位置的值和预期值
je equal              ; 如果相等，跳转到 equal 标签
jmp not_equal         ; 否则，跳转到 not_equal 标签

equal:
    lock cmpxchg dword ptr [rcx], rbx ; 执行 CAS 操作
    ; 如果成功，rdx 将包含旧值且等于 rax，同时 ZF 标志被设置
    ; 如果失败，rdx 将包含新的当前值，ZF 标志被清除
    sete al            ; 设置 al 为 0 或 1，取决于 ZF 标志
    jmp done           ; 跳转到结束

not_equal:
    mov al, 0          ; 设置返回值为 false

done:
    ; 返回值在 al 寄存器中 (true 或 false)
```

##  二、ARM 架构下的 CAS 实现

在 ARM 架构中，CAS 操作通常通过 `LDREX` 和 `STREX` 指令对来实现。这两个指令共同作用以确保原子性。

### 示例：32 位整数的 CAS 操作

```assembly
; r0 = expected value
; r1 = new value
; r2 = address of variable

loop:
    ldrex r3, [r2]     ; 加载独占标记的内存值到 r3
    teq   r3, r0       ; 比较 r3 和 r0
    bne   fail         ; 如果不相等，跳转到 fail
    strex r4, r1, [r2] ; 尝试存储 r1 到 [r2]，结果存储在 r4
    teq   r4, #0       ; 检查 strex 是否成功（r4 应为 0）
    bne   loop         ; 如果失败，重试
    mov   pc, lr       ; 成功，返回

fail:
    mov   pc, lr       ; 失败，返回
```

在这个例子中：
- `ldrex` 加载一个带有独占访问标记的值。
- `strex` 尝试存储一个新值，只有当自上次 `ldrex` 以来没有其他核心修改过这个位置时才会成功。
- 如果 `strex` 成功（返回值为 0），则表示 CAS 成功；否则，需要重试。

---

##  三、Java 中如何使用 CAS？

在 Java 中，CAS 操作主要通过 `sun.misc.Unsafe` 类来实现，不过直接使用 `Unsafe` 是不推荐的，因为它是 JVM 内部 API，不稳定且不易移植。Java 提供了更高层次的抽象——`java.util.concurrent.atomic` 包来简化 CAS 操作的使用。

例如，`AtomicInteger` 使用 CAS 来实现无锁的计数器：

```java
import java.util.concurrent.atomic.AtomicInteger;

public class Counter {
    private AtomicInteger count = new AtomicInteger(0);

    public void increment() {
        int oldValue;
        do {
            oldValue = count.get(); // 获取当前值
        } while (!count.compareAndSet(oldValue, oldValue + 1)); // 尝试更新
    }
}
```

这里的 `compareAndSet` 方法最终会调用到 `Unsafe` 类中的 `compareAndSwapInt` 方法，后者会在底层调用相应的汇编指令（如 x86 上的 `CMPXCHG` 或 ARM 上的 `LDREX/STREX` 对）来完成原子操作。

---

## 🧪 四、总结

- x86 架构：使用 `lock cmpxchg` 指令实现 CAS 操作，确保原子性。
- ARM 架构：通过 `LDREX` 和 `STREX` 指令对实现 CAS 操作，利用独占访问机制保证原子性。
- Java 实现：通过 `Unsafe` 类间接调用这些底层指令，对外提供 `AtomicXXX` 系列类来简化并发编程。

理解 CAS 的底层实现有助于更好地掌握并发控制机制的工作原理，尤其是在性能优化和问题排查方面具有重要意义。如果你有兴趣深入了解特定架构上的更多细节或有其他相关问题，欢迎继续提问！