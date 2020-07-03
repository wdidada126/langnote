# JUC

java.util.concurrent.ForkJoinPool

[Java中ListIterator和Iterator详解与辨析](https://www.cnblogs.com/a842297171/p/5379130.html)

[Iterator和ListIterator](https://blog.csdn.net/a597926661/article/details/7679765)


Iterator中有boolean hasNext();
ListIterator是继承Iterator，为什么还有boolean hasNext();



Iterator迭代器包含的方法有：
- hasNext()：如果迭代器指向位置后面还有元素，则返回 true，否则返回false
- next()：返回集合中Iterator指向位置后面的元素
- remove()：删除集合中Iterator指向位置后面的元素
- ListIterator迭代器包含的方法有：
- add(E e): 将指定的元素插入列表，插入位置为迭代器当前位置之前
- hasNext()：以正向遍历列表时，如果列表迭代器后面还有元素，则返回 true，否则返回false
- hasPrevious():如果以逆向遍历列表，列表迭代器前面还有元素，则返回 true，否则返回false
- next()：返回列表中ListIterator指向位置后面的元素
- nextIndex():返回列表中ListIterator所需位置后面元素的索引
- previous():返回列表中ListIterator指向位置前面的元素
- previousIndex()：返回列表中ListIterator所需位置前面元素的索引
- remove():从列表中删除next()或previous()返回的最后一个元素（有点拗口，意思就是对迭代器使用hasNext()方法时，删除ListIterator指向位置后面的元素；当对迭代器使用hasPrevious()方法时，删除ListIterator指向位置前面的元素）
- set(E e)：从列表中将next()或previous()返回的最后一个元素返回的最后一个元素更改为指定元素e


https://blog.csdn.net/u010412719/article/category/6159934

http://www.runoob.com/java/java8-new-features.html


写NIO程序经常使用ByteBuffer来读取或者写入数据，那么使用ByteBuffer.allocate(capability)还是使用ByteBuffer.allocteDirect(capability)来分配缓存了？第一种方式是分配JVM堆内存，属于GC管辖范围，由于需要拷贝所以速度相对较慢；第二种方式是分配OS本地内存，不属于GC管辖范围，由于不需要内存拷贝所以速度相对较快。


ByteOrder 用法
- [csdn b](https://blog.csdn.net/will_awoke/article/details/25803725)
- [github nio](ttps://iamxpy.github.io/2017/05/04/Java-NIO-%E6%8E%A2%E7%A9%B6%E5%AD%97%E8%8A%82%E9%A1%BA%E5%BA%8FByteOrder/)
- [cnblog ar](https://www.cnblogs.com/JeffreyZhao/archive/2010/02/10/byte-order-and-related-library.html)

ByteOrder 类定义了决定从缓冲区中存储或检索多字节数值时使用哪一字节顺序的常量。

java.util.Objects


```java

  ClassLoader systemClassLoader;

    try {
      systemClassLoader = ClassLoader.getSystemClassLoader();
    } catch (SecurityException ignored) {
      // AccessControlException on Google App Engine   
    }
    
```