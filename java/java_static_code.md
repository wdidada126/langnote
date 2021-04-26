# java static code


https://zhuanlan.zhihu.com/p/338144898
前言
本篇主要讲述java中几种常见的代码块，及它们之间的区别，并阐述了类的加载时机及加载过程，中间用代码案例加以实践阐述。

代码块
在java中使用{}括起来的叫做代码块，根据其位置和声明的不同，可以分为局部代码块、静态代码块、构造代码块。
局部代码块：局部位置，用于限定局部变量的生命周期。
构造代码块：在类的成员位置，用{} 括起来，每实例化一次对象，执行一次里面的代码，且多个构造代码块，按照顺序执行构造代码块
静态代码块：在类的成员位置，用static{} 只有在类加载的时候，才会执行，且只执行一次，且由于是在类加载时才会执行，所以甚至先于main方法前执行
面试题:静态代码块、构造代码块、构造方法的执行顺序?
静态代码块>构造代码块>构造方法

代码示例
Student类代码:

package demo02;

/**
 * @author:tom
 * @Date:Created in 18:09 2020/12/19
 */
public class Student {

    //构造函数
    public Student() {
        System.out.println("构造函数被执行，对象实例化，并被创建");
    }

    //静态代码块
    static {
        System.out.println("static code has been invoked");
    }

    //静态代码块
    static {
        System.out.println("static code has been invoked   333");
    }

    //静态代码块
    static {
        System.out.println("static code has been invoked   111");
    }

    
    //构造代码块
    {
        System.out.println("construct code has been invoked 2");
    }

    {
        System.out.println("construct code has been invoked 1");
    }

    {
        System.out.println("construct code has been invoked 3");
    }
}
Test类：

​
package demo02;

/**
 * @author:tom
 * @Date:Created in 18:12 2020/12/19
 */
public class TestStudent {
    public static void main(String[] args) {
        Student student = new Student();
        Student student2 = new Student();
        Student student3 = new Student();
    }
}

​
如上述代码：我创建了学生类，并在其中定义了无参构造函数、三个无序的静态代码块逻辑、三个无序的构造代码块逻辑，测试类中创建三个学生类的实例对象，测试结果如下：
java_static_1.jpg

可以看到静态代码块最先执行，多个静态代码块按照代码执行顺序执行，且每个仅执行一次；
而第二执行的是构造代码块，多个构造代码块按照代码执行顺序执行，每实例化一次对象时，就会执行一次；
最后执行的是构造函数，每实例化一次对象，就会执行一次；

类加载及类加载的时机
本文前面说，静态代码块在类加载的时候执行，且只执行一次；构造代码块，在每次实例化对象的时候都会执行一次，那很显然类加载和实例化对象不是一个概念，so 类的加载和类加载的时机是什么呢
类的加载
在java中，类的加载过程可以分为三个步骤，加载、连接、初始化
加载
根据一个类的全限定名称如cn.edu.china.demo.test.class读取此类的二进制字节流到JVM内部;
将字节流所代表的静态存储结构转换为方法区的运行时数据结构，并转化为一个.Class 的字节码文件对象
连接
验证
验证阶段主要包括四个检验过程：文件格式验证、元数据验证、字节码验证和符号引用验证;
准备
为类中的所有静态变量分配内存空间，并为其设置一个初始值（由于还没有产生对象，实例变量将不再此操作范围内）；
解析
将常量池中所有的符号引用转为直接引用（得到类或者字段、方法在内存中的指针或者偏移量，以便直接调用该方法）。这个阶段可以在初始化之后再执行。
初始化
JVM才真正开始执行类中定义的Java程序代码
类初始化或类加载的时机
1）创建类的实例
比如new一个对象；
通过类的静态方法newInstance获取类的实例；
通过反射创建对象的实例；
创建一个带有父类的类，发现父类还没有加载，先加载初始化父类；
通过克隆创建一个类的实例
2）调用一个类的静态字段、静态方法等静态成员（包括为成员赋值、使用成员等操作）
类的加载只会加载一次，而类的实例化则可能有多次
比如通过本文前面代码中所述，new 一个Student对象，在未加载时，会首先进行第一次加载，进行静态变量赋值和静态代码块执行，之后进行构造代码块的执行，最后进行构造方法的执行。
最终完整的执行顺序应该是（带父类的）：
1. 父类的静态成员变量初始化和静态代码块执行
2. 子类的静态成员变量初始化和静态代码块执行
3. 父类成员变量初始化和方法块执行
4. 父类的构造函数执行
5. 子类成员变量初始化和方法块执行
6. 子类的构造函数执行


为了演示补充，下面补充一下带父类的及成员变量的代码案例实践：
父类：

package demo03;

import sun.management.Agent;

/**
 * @author:tom
 * @Date:Created in 20:12 2020/12/19
 */
public class Father {
    static public int age = 30;

    static {
        System.out.println("父类的静态代码块执行");
        System.out.println("父亲此时的年龄是" + age);
    }

    {
        System.out.println("父类的构造代码块开始执行！");
        age = 40;
        System.out.println("此时父类的年龄是" + age);
    }

    public Father() {
        System.out.println("父类的构造函数开始执行");
        System.out.println("此时父类的年龄是" + age);
    }
}
子类：

package demo03;

/**
 * @author:tom
 * @Date:Created in 20:15 2020/12/19
 */
public class Son extends Father {


    public static int sal = 1000;

    public Son() {
        System.out.println("子类的构造函数执行拉！");
        System.out.println("子类的薪资是" + sal);

    }

    static {
        System.out.println("子类的静态代码块执行啦！");
        System.out.println("子类的薪资是" + sal);
    }

    {
        System.out.println("子类的构造代码块执行拉！");
        sal = 10000;
        System.out.println("子类的薪资是" + sal);

    }
}
测试类:

package demo03;

/**
 * @author:tom
 * @Date:Created in 20:24 2020/12/19
 */
public class Test {
    public static void main(String[] args) {
        Son s = new Son();
    }
}
测试结果如下:

java_static_2.jpg

结果分析：

在整体的情况家肯定都是静态优先执行的，在静态优先的情况下，是父类优先的，在静态中又以静态变量先初始化赋值、在执行静态代码块
步骤解析：
父类的静态代码块执行 -------------静态代码块优先+父类 优先 所以 是父类的静态代码块先执行
父亲此时的年龄是30 -------------这里看起来是第二句执行，其实应该是父类的静态变量初始化赋值先执行，否则在静态代码块中的逻辑拿到的age应该是默认值0
子类的静态代码块开始执行------------静态代码块优先
子类的薪资是1000 ---------静态变量优先初始化赋值
父类的构造代码块开始执行 --------抛开静态的大条件 父类的应先执行
所以依次是 父类的构造代码块、父类的构造函数，接着才是子类的构造代码块、子类的构造函数执行
总结执行顺序应是
1）父类的静态变量初始化赋值
2）父类的静态代码块执行
3）子类的静态变量初始化赋值
4）子类的静态代码块执行
5）父类的变量初始化赋值
6）父类的构造代码块执行
7）父类的构造函数执行
8）子类的变量初始化赋值
9）子类的构造代码块执行
10）子类的构造函数执行

