# CountDownLatch

CountDownLatch也是基于AQS，它是AQS的共享功能的一个实现。

[CountDownLatch源码解析](http://ifeve.com/countdownlatch%E6%BA%90%E7%A0%81%E8%A7%A3%E6%9E%90/)

### 1、CountDownLatch 构造

```java
public CountDownLatch(int count) {
	if (count < 0) throw new IllegalArgumentException("count < 0");
	// Sync 就是继承了一个AQS
	this.sync = new Sync(count);
}
```


```java
private static final class Sync extends AbstractQueuedSynchronizer {

	private static final long serialVersionUID = 4982264981922014374L;

	Sync(int count) {
		setState(count);
	}
}
```

