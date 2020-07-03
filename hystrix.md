# hystrix

最多支持多少个线程池？



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


com.netflix.hystrix.HystrixThreadPoolMetrics.metrics
是个map，key是

