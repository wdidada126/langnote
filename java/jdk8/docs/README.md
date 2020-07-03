# rt.jar 包



- package java.beans
- package java.io
- package java.lang 默认包 
- package java.math
- package java.net
- package java.nio
- package java.rmi
- package java.security
- package java.sql
- package java.text
- package java.util

- package java.lang.annotation
- package java.lang.instrument
- package java.lang.invoke
- package java.lang.management
- package java.lang.ref
- package java.lang.reflect


- package java.beans.beancontext


jexport

jstring jni


BlockingQueue
类图上，实现了Queue

sun.misc.Launcher

```java

add         增加一个元索                      如果队列已满，则抛出一个IIIegaISlabEepeplian异常
remove   移除并返回队列头部的元素     如果队列为空，则抛出一个NoSuchElementException异常
element  返回队列头部的元素              如果队列为空，则抛出一个NoSuchElementException异常
offer       添加一个元素并返回true        如果队列已满，则返回false
poll         移除并返问队列头部的元素     如果队列为空，则返回null
peek       返回队列头部的元素              如果队列为空，则返回null
put         添加一个元素                       如果队列满，则阻塞
take        移除并返回队列头部的元素  


```


```java

ArrayBlockingQueue (java.util.concurrent)
DelayedWorkQueue in ScheduledThreadPoolExecutor (java.util.concurrent)
BlockingDeque (java.util.concurrent)
    LinkedBlockingDeque (java.util.concurrent)
SynchronousQueue (java.util.concurrent)
DelayQueue (java.util.concurrent)
TransferQueue (java.util.concurrent)
    LinkedTransferQueue (java.util.concurrent)
LinkedBlockingQueue (java.util.concurrent)
    1 in Service (javafx.concurrent)
PriorityBlockingQueue (java.util.concurrent)

```


### rmi
弃用了


### java.utils

java.util.AbstractSequentialList
java.util.ListIterator
