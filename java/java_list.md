# ju

[ju api](https://docs.oracle.com/javase/8/docs/api/java/util/package-summary.html)



AbstractList的常用子类

- Vector
- ArrayList
- LinkedList


AbstractList的抽象方法
- public abstract Iterator<E> iterator();
- public abstract int size();


AbstractSequentialList的抽象方法

- public abstract ListIterator<E> listIterator(int index);


Vector的类图参考Vector.mdj


Vector的实现
通过源码可以看出，成员变量protected Object[]	elementData
Vector是通过数组实现的。


ArrayList、LinkedList、Vector的区别和实现原理

[ArrayList、LinkedList、Vector的区别和实现原理](https://blog.csdn.net/kuangsonghan/article/details/79861170)


[Vector,ArrayList, LinkedList的区别](https://www.cnblogs.com/zkk-wust/p/7250776.html)

[美团分布式ID leaf vs java se uuid](https://tech.meituan.com/2017/04/21/mt-leaf.html)
UUID(Universally Unique Identifier)的标准型式包含32个16进制数字，以连字号分为五段，形式为8-4-4-4-12的36个字符，示例：550e8400-e29b-41d4-a716-446655440000，到目前为止业界一共有5种方式生成UUID
优点：

性能非常高：本地生成，没有网络消耗。
缺点：

不易于存储：UUID太长，16字节128位，通常以36长度的字符串表示，很多场景不适用。
信息不安全：基于MAC地址生成UUID的算法可能会造成MAC地址泄露，这个漏洞曾被用于寻找梅丽莎病毒的制作者位置。

ID作为主键时在特定的环境会存在一些问题，比如做DB主键的场景下，UUID就非常不适用