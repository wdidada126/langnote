# 设计模式


https://blog.csdn.net/ttxs99989/article/details/81844135

![Java_Design_Patten](..\imgs\Java_Design_Patten.jpg)





1、创建型模式
对象实例化的模式，创建型模式用于解耦对象的实例化过程。

单例模式：某个类智能有一个实例，提供一个全局的访问点。
工厂模式：一个工厂类根据传入的参量决定创建出哪一种产品类的实例。
抽象工厂模式：创建相关或依赖对象的家族，而无需明确指定具体类。
建造者模式：封装一个复杂对象的创建过程，并可以按步骤构造。
原型模式：通过复制现有的实例来创建新的实例。
2、结构型模式
把类或对象结合在一起形成一个更大的结构。

装饰器模式：动态的给对象添加新的功能。
代理模式：为其它对象提供一个代理以便控制这个对象的访问。
桥接模式：将抽象部分和它的实现部分分离，使它们都可以独立的变化。
适配器模式：将一个类的方法接口转换成客户希望的另一个接口。
组合模式：将对象组合成树形结构以表示“部分-整体”的层次结构。
外观模式：对外提供一个统一的方法，来访问子系统中的一群接口。
享元模式：通过共享技术来有效的支持大量细粒度的对象。
3、行为型模式
类和对象如何交互，及划分责任和算法。

策略模式：定义一系列算法，把他们封装起来，并且使它们可以相互替换。
模板模式：定义一个算法结构，而将一些步骤延迟到子类实现。
命令模式：将命令请求封装为一个对象，使得可以用不同的请求来进行参数化。
迭代器模式：一种遍历访问聚合对象中各个元素的方法，不暴露该对象的内部结构。
观察者模式：对象间的一对多的依赖关系。
仲裁者模式：用一个中介对象来封装一系列的对象交互。
备忘录模式：在不破坏封装的前提下，保持对象的内部状态。
解释器模式：给定一个语言，定义它的文法的一种表示，并定义一个解释器。
状态模式：允许一个对象在其对象内部状态改变时改变它的行为。
责任链模式：将请求的发送者和接收者解耦，使的多个对象都有处理这个请求的机会。
访问者模式：不改变数据结构的前提下，增加作用于一组对象元素的新功能。

原文链接：https://blog.csdn.net/guorui_java/article/details/104026988



画图
画类图
设计模式相关的

合肥一个面试 画图

设计模式与solid5大原则 六大原则
单一职责原则
开闭原则：所有设计模式的最核心目标
里氏替换原则
接口隔离原则
依赖倒置原则
迪米特法则

SOLID是5个设计原则的统称，它们分别是：单一职责原则、开闭原则、里式替换原则、接口隔离原则和依赖反转原则，依次对应SOLID中的S、O、L、I、D。


1、单一职责原则
单一职责原则，Single Responsibility Principle，SRP，英文描述是：A class or module should have a single responsibility。翻译成中文就是：一个类或者模块只负责完成一个职责（或者功能）。
2、开闭原则
开闭原则，Open Closed Principle，OCP，英文描述是：software entities（modules，classes，functions，etc）should be open for extension，but closed for modification。翻译成中文就是：软件实体（模块、类、方法等）应该对扩展开放，对修改关闭。
3、里氏替换原则
里氏替换原则，Liskov Substitution Principle，英文描述是：If S is a subtype of T, then objects of T may be replaced with objects of type S, without breaking the program（子类对象可以替换父类对象而不破坏程序运行），或者：Functions that use pointers of references to base classes must be able to use objects of deried classes without knowing it（使用基类引用指针的方法，必须能够在无感知的情况下使用派生类对象
4、接口隔离原则
接口隔离原则，Interface Segregation Principle，ISP，英文描述是：Clients should not be forced to depend upon interface that they do not use。翻译成中文就是：客户端不应该被强迫依赖它不需要的接口。其中“客户端”可以理解为接口的调用者或使用者。
5、依赖反转原则
依赖反转，Dependency Inversion Principle，DIP，英文描述是：High-level modules shoudn't depend on low-level modules. Both modules should depend on abstractions. In addition, abstraction shouldn't depend on details. Details depend on abstractions。翻译成中文就是：高层模块不要依赖低层模块。高层和低层模块都要依赖抽象。除此之外，抽象不要依赖具体实现，具体实现要依赖抽象。




设计原则总结评判代码质量的标准，比如可读性、可复用性、可扩展性等，这是从代码的整体质量的角度来评判。而设计原则就是我们要使用到的更加具体的对于代码进行评判的标准，比如, 我们说这段代码的可扩展性比较差，主要原因是违背了开闭原则。

比较常用的三个原则

1 ) 单一职责原则

单一职责原则是类职责划分的重要参考依据，是保证代码”高内聚“的有效手段，是我们在进行面向对象设计时的主要指导原则。

单一职责原则的难点在于，对代码职责是否足够单一的判定。这要根据具体的场景来具体分析。同一个类的设计，在不同的场景下，对职责是否单一的判定，可能是不同的。

2 ) 开闭原则

开闭原则是保证代码可扩展性的重要指导原则，是对代码扩展性的具体解读。很多设计模式诞生的初衷都是为了提高代码的扩展性，都是以满足开闭原则为设计目的的。

开闭原则是所有设计模式的最核心目标，也是最难实现的目标，但是所有的软件设计模式都应该以开闭原则当作标准，才能使软件更加的稳定和健壮。

3 ) 依赖倒置原则

依赖倒置原则主要用来指导框架层面的设计。高层模块不依赖低层模块，它们共同依赖同一个抽象。

依赖倒置原则其实也是实现开闭原则的重要途径之一，它降低了类之间的耦合，提高了系统的稳定性和可维护性，同时这样的代码一般更易读，且便于传承。
https://blog.csdn.net/weixin_42151235/article/details/129025690


左耳朵耗子
看到有人说设计模式过时了，我得说设计模式非常非常有用，用Proxy做RAII，用Bridge解耦对象，用Observer 来Watch状态变化，用Strategy解耦实现和接口，用Adapter适配异构，用Command实现Undo/Redo，用Decorator实现无侵入式增强，Interpreter实现表达式，用Vistor分治一个大对象


参考文章
https://www.cnblogs.com/qq-361807535/p/6854191.html
https://www.cnblogs.com/zhenyulu/articles/79894.html
http://www.runoob.com/design-pattern/template-pattern.html

facade 门面模式 slf4j




github

面试必考



注意啊

委托模式
delegate iOS开发OC中经常使用

### Spring中用到了哪些设计模式
代理模式：AOP中
单例模式：bean的单例模式 BeanFactory对象
模板模式：JdbcTemplate refresh方法  RedisTemplate
工厂模式：BeanFactory
观察者模式：监听器
适配器模式：Controller

### MyBatis中使用的设计模式
代理模式：Mapper接口，jdbc日志打印 Connection Statement 代理对象 拦截器
装饰器模式：缓存 Executor
适配器模式：日志
工厂模式模式：SqlSessionFactory
建造者模式：SqlSessionFactoryBuilder

