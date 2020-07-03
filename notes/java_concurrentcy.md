chap 1
Thread 类
Runnable 接口

Thread

java创建线程的两种方法
继承Thread

```java
     class PrimeThread extends Thread {
         long minPrime;
         PrimeThread(long minPrime) {
             this.minPrime = minPrime;
         }

         public void run() {
             // compute primes larger than minPrime
              . . .
         }
     }
     PrimeThread p = new PrimeThread(143);
     p.start();
```

实现Runnable接口

```java
     class PrimeRun implements Runnable {
         long minPrime;
         PrimeRun(long minPrime) {
             this.minPrime = minPrime;
         }

         public void run() {
             // compute primes larger than minPrime
              . . .
         }
     }
     PrimeRun p = new PrimeRun(143);
     new Thread(p).start();
```

static Thread	currentThread()
获取当前类，在Runnable中使用较多
public final boolean isAlive()
是否成活
public final void setPriority(int newPriority)

public final int getPriority()

public final void setName(String name)

public final String getName()

public final void join(long millis) throws InterruptedException

public Thread.State getState()

备注：
if (newPriority > MAX_PRIORITY || newPriority < MIN_PRIORITY) {
            throw new IllegalArgumentException();
        }


public static enum Thread.State
extends Enum<Thread.State>
A thread state. A thread can be in one of the following states:
NEW
A thread that has not yet started is in this state.
RUNNABLE
A thread executing in the Java virtual machine is in this state.
BLOCKED
A thread that is blocked waiting for a monitor lock is in this state.
WAITING
A thread that is waiting indefinitely for another thread to perform a particular action is in this state.
TIMED_WAITING
A thread that is waiting for another thread to perform an action for up to a specified waiting time is in this state.
TERMINATED
A thread that has exited is in this state.