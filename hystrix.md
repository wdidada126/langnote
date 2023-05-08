# hystrix



Sentinel



最多支持多少个线程池？


Hystrix 是一个用于实现服务容错和服务熔断的框架，其中的线程隔离是其实现服务容错的重要机制之一。
在 Hystrix 中，线程隔离是通过使用线程池来实现的。当一个请求进入 Hystrix 保护的服务时，Hystrix 会将该请求封装成一个 HystrixCommand 对象，并在一个专门的线程池中执行。这个线程池被称为 Hystrix 线程池，它是一个单独的线程池，与服务本身的线程池是相互独立的。
Hystrix 线程池采用了信号量隔离和线程隔离两种隔离策略。其中，线程隔离是默认的隔离策略，它将每个 HystrixCommand 对象的执行都放在一个单独的线程中，从而实现了请求之间的隔离。在线程隔离模式下，每个 HystrixCommand 对象都会有自己的线程池，从而避免了线程之间的相互影响。
具体来说，Hystrix 线程池中的线程会维护一个请求队列，当新的请求到来时，会将其加入到请求队列中。当队列中的请求达到一定的数量时，新的请求就会被拒绝，从而避免了线程池过载和服务崩溃的情况。同时，Hystrix 还通过超时机制和熔断机制来进一步保护服务的稳定性和可靠性。
需要注意的是，线程隔离虽然可以提高服务的稳定性和可靠性，但也会带来一定的性能开销和资源消耗。因此，在使用 Hystrix 时，需要根据实际情况选择合适的隔离策略，以达到最佳的性能和可靠性的平衡。


Hystrix 源码解析

https://zhenbianshu.github.io/2018/08/_code_design_share.html

### 日志

slf4j


配置线程池
https://zhenbianshu.github.io/2018/09/hystrix_configuration_analysis.html

Hystrix是如何实现线程隔离的？

```java
    Map<String, ThreadPoolExecutor> map = new HashMap<>();

    ThreadPoolExecutor getPool(String groupName){

        ThreadPoolExecutor threadPoolExecutor = map.get(groupName);
        if(threadPoolExecutor == null){

            try {
//                threadPoolExecutor = Executors.newSingleThreadExecutor();
            } catch (Exception e) {
                e.printStackTrace();
            } finally {
            }
        }
        return threadPoolExecutor;
    }
```


设置线程池
com.netflix.hystrix.HystrixThreadPoolProperties.Setter


```java
        HystrixCommand.Setter hystrixSetter = HystrixCommand.Setter
                .withGroupKey(
                        HystrixCommandGroupKey.Factory.asKey("a"))
                .andCommandKey(HystrixCommandKey.Factory.asKey("abc"))
                .andThreadPoolKey(
                        HystrixThreadPoolKey.Factory.asKey("adad"))
                .andCommandPropertiesDefaults(
                        HystrixCommandProperties.Setter()
                                .withExecutionTimeoutInMilliseconds(2234)
                                .withCircuitBreakerErrorThresholdPercentage(
                                        34)
                                .withCircuitBreakerSleepWindowInMilliseconds(
                                        3234)
                                .withCircuitBreakerRequestVolumeThreshold(20))
                .andThreadPoolPropertiesDefaults(
                        HystrixThreadPoolProperties.Setter().withKeepAliveTimeMinutes(
                                1)
                                .withCoreSize(1)
                                .withMaximumSize(1)
                                .withAllowMaximumSizeToDivergeFromCoreSize(true));
```

RXjava
Ob
doOnTerminate
doOnUnsubscribe
doOnCompleted

[When to use doOnTerminate vs doOnUnsubscribe?](https://stackoverflow.com/questions/40407842/when-to-use-doonterminate-vs-doonunsubscribe)

com.netflix.hystrix.HystrixThreadPool.HystrixThreadPoolDefault.threadPool


com.netflix.hystrix.HystrixThreadPoolMetrics.metrics 是个map，key是

