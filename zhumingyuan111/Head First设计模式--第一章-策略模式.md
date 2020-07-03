---
title: Head First设计模式--第一章-策略模式
date: 2017-06-25 12:34:19
tags: CSDN迁移
---
  最近感觉写代码没有什么长进，所以希望能从设计模式上进行一个充电，写写博客把设计模式中的要点和例子总结整理一下。

 
### 本章要点

  
  * 设计基础：抽象、封装、多态、继承 
  * 设计原则1： 找出应用中可能需要变化之处，把它们独立出来，不要和那些不许需要变化的代码混在一起 
  * 设计原则2： 针对接口编程，而不是针对实现编程 
  * 设计原则3： 多用组合，少用继承 
  * 设计模式——策略模式：定义了算法族，分别封装起来，让它们之间可以相互替换，此模式让算法的变化独立于使用算法的客户。  
### 应用背景

 公司设计一批鸭子的游戏产品，鸭子有一些行为比如：会叫、游泳等。现在公司要设计一些新的的鸭子产品，比如鸭子会飞之类的。如果按照继承的方式，鸭子的这些行为将定义在超类中，子类去实现这些方法。那么这样做的缺点是有一些鸭子根本不会飞，但是也要去实现飞的动作,或者说也具有飞的行为;其次修改超类，需要对之前的每一个子类进行代码修改，对于工程的维护上代码很大的风险;最后对于每一个子类去实现飞的行为会带来很大的代码重复。

 
### 重新设计

 我们可以把鸭子的行为理解为其算法，定义算法族，进行封装。下面给出代码：

 
#### 飞行行为接口和实现类

 
```
/**
 * Created by hadoop on 17-6-25.
 */
public interface FlyBehavior {
    public void fly();
}
```
 
```
import com.head.first.Strategy.behavior.FlyBehavior;

/**
 * Created by hadoop on 17-6-25.
 */
public class FlyWithWings implements FlyBehavior{

    public void fly() {
        System.out.println("I can fly with my wings!");
    }
}
```
 
```
import com.head.first.Strategy.behavior.FlyBehavior;

/**
 * Created by hadoop on 17-6-25.
 */
public class FlyNoWay implements FlyBehavior {

    public void fly() {
        System.out.println("I can't fly!");
    }
}
```
 
#### 叫声行为接口和实现类

 
```
/**
 * Created by hadoop on 17-6-25.
 */
public interface QuackBehavior {

    public void quack();
}
```
 
```
import com.head.first.Strategy.behavior.QuackBehavior;

/**
 * Created by hadoop on 17-6-25.
 */
public class CommonQuack implements QuackBehavior{
    public void quack() {
        System.out.println("我的叫声是呱呱叫");
    }
}
```
 
```
import com.head.first.Strategy.behavior.QuackBehavior;

/**
 * Created by hadoop on 17-6-25.
 */
public class MuteQuack implements QuackBehavior{
    public void quack() {
        System.out.println("我不会叫呦");
    }
}
```
 
```

import com.head.first.Strategy.behavior.QuackBehavior;

/**
 * Created by hadoop on 17-6-25.
 */
public class Squack  implements QuackBehavior{
    public void quack() {
        System.out.println("我的叫声是吱吱叫");
    }
}
```
 鸭子的抽象类和实现类

 
```
import com.head.first.Strategy.behavior.FlyBehavior;
import com.head.first.Strategy.behavior.QuackBehavior;

/**
 * Created by hadoop on 17-6-25.
 */
public abstract  class Duck {
     FlyBehavior flyBehavior;
    QuackBehavior quackBehavior;

    public void swim(){
        System.out.println("I can swim on water!");
    }

    public abstract void display();

    public void performQuack(){
        quackBehavior.quack();
    }

    public  void performFly(){
        flyBehavior.fly();
    }

    public FlyBehavior getFlyBehavior() {
        return flyBehavior;
    }

    public void setFlyBehavior(FlyBehavior flyBehavior) {
        this.flyBehavior = flyBehavior;
    }

    public void setQuackBehavior(QuackBehavior quackBehavior) {
        this.quackBehavior = quackBehavior;
    }
}
```
 
```
import com.head.first.Strategy.behavior.impl.FlyWithWings;
import com.head.first.Strategy.behavior.impl.Squack;

/**
 * Created by hadoop on 17-6-25.
 */
public class DecoyDuck extends Duck{
    public DecoyDuck(){
        this.quackBehavior = new Squack();
        this.flyBehavior = new FlyWithWings();
    }

    @Override
    public void display() {
        System.out.println("我是一个诱饵鸭！");
    }
}
```
 
```

import com.head.first.Strategy.behavior.impl.CommonQuack;
import com.head.first.Strategy.behavior.impl.FlyNoWay;

/**
 * Created by hadoop on 17-6-25.
 */
public class MallarDuck extends Duck{

    public MallarDuck(){
        this.quackBehavior = new CommonQuack();
        this.flyBehavior = new FlyNoWay();
    }

    public void display() {
        System.out.println("I look like green head!");
    }
}
```
 
```
import com.head.first.Strategy.behavior.impl.CommonQuack;
import com.head.first.Strategy.behavior.impl.FlyWithWings;

/**
 * Created by hadoop on 17-6-25.
 */
public class RedHeadDuck extends Duck{
    public RedHeadDuck(){
        this.flyBehavior = new FlyWithWings();
        this.quackBehavior = new CommonQuack();
    }

    @Override
    public void display() {
        System.out.println("I look like red head!");
    }
}
```
 
```

import com.head.first.Strategy.behavior.impl.FlyNoWay;
import com.head.first.Strategy.behavior.impl.MuteQuack;

/**
 * Created by hadoop on 17-6-25.
 */
public class RubberDuck  extends Duck{
    public RubberDuck(){
        this.quackBehavior = new MuteQuack();
        this.flyBehavior=new FlyNoWay();
    }

    @Override
    public void display() {
        System.out.println("我是一个橡皮鸭！");
    }
}
```
 
#### 测试类

 
```
import com.head.first.Strategy.Duck;
import com.head.first.Strategy.MallarDuck;
import com.head.first.Strategy.behavior.impl.FlyWithWings;

/**
 * Created by hadoop on 17-6-25.
 */
public class StrategyTest {

    public static void main(String[]args){
        Duck mallard = new MallarDuck();
        mallard.display();
        mallard.performFly();
        mallard.performQuack();
        System.out.println("mallard 现在可以飞了。。。");
        mallard.setFlyBehavior(new FlyWithWings());
        mallard.performFly();
    }
}
```
 
### 全局视角

 最后给出原书中的设计类图，能从全局中理解策略模式的原理   
 ![这里写图片描述](https://img-blog.csdn.net/20170625132444512?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvemh1bWluZ3l1YW4xMTE=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

   
  