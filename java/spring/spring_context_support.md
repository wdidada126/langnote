# spring context support

## 四个模块
- 缓存
- 邮件
- 定时任务
- ui模板freemarker
- 
## 源码解读
https://docs.spring.io/spring-framework/docs/5.2.x/javadoc-api/

### org.springframework.cache
#### org.springframework.cache.caffeine



|                            |      |      |
|----------------------------| ---- | ---- |
| CaffeineCache              |      |      |
| CaffeineCache.LoadFunction              |      |      |
| CaffeineCache.PutIfAbsentFunction |      |      |
| CaffeineCacheManager       |      |      |
|                            |      |      |




#### org.springframework.cache.ehcache


| org.springframework.cache.ehcache     |      |      |
| ---- | ---- | ---- |
|  EhCacheCache    |      |      |
|  EhCacheCacheManager    |      |      |
|      |      |      |

#### org.springframework.cache.jcache
##### org.springframework.cache.jcache.config
##### org.springframework.cache.jcache.interceptor
| org.springframework.cache.jcache.interceptor |
|----------------------------------------------|
|                                              |
| Interfaces                                   |
|                                              |
| JCacheOperation                              |
| JCacheOperationSource                        |
|                                              |
| Classes                                      |
|                                              |
| AbstractFallbackJCacheOperationSource        |
| AnnotationJCacheOperationSource              |
| BeanFactoryJCacheOperationSourceAdvisor      |
| DefaultJCacheOperationSource                 |
| JCacheAspectSupport                          |
| JCacheInterceptor                            |
| JCacheOperationSourcePointcut                |
| SimpleExceptionCacheResolver                 |



#### org.springframework.cache.transaction


|      |      |      |
| ---- | ---- | ---- |
|      |      |      |
|      |      |      |
|      |      |      |


### org.springframework.mail
#### org.springframework.mail.javamail
### org.springframework.scheduling
#### org.springframework.scheduling.commonj
#### org.springframework.scheduling.quartz

| org.springframework.scheduling.quartz                        |
|--------------------------------------------------------------|
|                                                              |
| Interfaces                                                   |
|                                                              |
| SchedulerContextAware                                        |
|                                                              |
| Classes                                                      |
|                                                              |
| AdaptableJobFactory                                          |
| CronTriggerFactoryBean                                       |
| DelegatingJob                                                |
| JobDetailFactoryBean                                         |
| LocalDataSourceJobStore                                      |
| LocalTaskExecutorThreadPool                                  |
| MethodInvokingJobDetailFactoryBean                           |
| MethodInvokingJobDetailFactoryBean.MethodInvokingJob         |
| MethodInvokingJobDetailFactoryBean.StatefulMethodInvokingJob |
| QuartzJobBean                                                |
| ResourceLoaderClassLoadHelper                                |
| SchedulerAccessor                                            |
| SchedulerAccessorBean                                        |
| SchedulerFactoryBean                                         |
| SimpleThreadPoolTaskExecutor                                 |
| SimpleTriggerFactoryBean                                     |
| SpringBeanJobFactory                                         |
|                                                              |
| Exceptions                                                   |
|                                                              |
| JobMethodInvocationFailedException                           |


### org.springframework.ui.freemarker