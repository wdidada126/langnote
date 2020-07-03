# java clone 

Java中所有对象都继承自Object类，所以就默认自带clone方法的实现，clone方法的实现是比较简单粗暴的。首先，如果一个对象想要调用clone方法，必须实现Cloneable接口，否则会抛出CloneNotSupportedException。其实这个Cloneable是个空接口，只是个flag用来标记这个类是可以clone的，所以说将一个类声明为Cloneable与这个类具备clone能力其实并不是直接相关的。



https://blog.csdn.net/hzycaicai2012/article/details/45564443



