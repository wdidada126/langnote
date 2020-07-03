---
title: Head First设计模式第二章——观察者模式
date: 2017-07-02 11:19:37
tags: CSDN迁移
---
  ### 本章要点

 
##### 设计基础

 抽像

 
##### 设计原则

 封装变化   
 多用组合，少用继承   
 针对接口编程，不针对实现编程   
 为交互对象之间的松耦合设计努力

 
##### 设计模式

 观察者模式——在对象之间定义一对多的依赖，这样一来，当一个对象改变状态，依赖它的对象都会收到通知，并自动更新。

 
### 应用背景

 应用的大致设计是利用WeatherData对象获取相关的天气数据，并更新三个布告板：目前状况布告板、气象统计布告板，天气预报布告板。在该设计下我们很快可以给出代码样例：

 
```
public class WeatherData{
  //变量声明省略...
    public void measurementChanged(){
        float temp = getTemperature();
        float humidity = getHumidity();
        float pressure = getPressure();
       currentConditionDisplay.update(temp,humidity,pressure);
        statistisDisplay.update(temp,humidity,pressure);
        pressureDisplay.update(temp,humidity,pressure);
    }
}
```
 下面我们分析以下这样做有什么缺点：   
 1. 上面方法中的更新方法的调用我们可以看出：代码是针对实现编程，而非针对接口;   
 2. 对于新增布告板，我们需要重新修改该部分代码;   
 3. 我们无法在运行时动态的添加或者删除布告板;   
 4. 对于可能会改变的地方我们我们进行封装。

 
### 重新设计

 我们可以把WeatherData对象作为主题，各个布告板则为订阅者。如果需要新增布告板的话，那么我们只需要开发新的布告板，然后在主题中进行注册就行了，不需要修改之前的代码。同时，我们可以利用注册和解除操作动态的添加和删除一个主题的订阅者。下面给出一个观察者的类图   
 ![这里写图片描述](https://img-blog.csdn.net/20170702140137927?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvemh1bWluZ3l1YW4xMTE=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

 下面给出重新设计的接口和类   
 主题接口

 
```
package com.head.first.Observer;

/**
 * Created by hadoop on 17-7-2.
 */
public interface Subject {

    public void register(Observer observer);

    public void remove(Observer observer);

    public boolean contain(Observer observer);

    public void notifyObservers();
}
```
 主题的实现

 
```
package com.head.first.Observer.impl;

import com.head.first.Observer.Observer;
import com.head.first.Observer.Subject;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by hadoop on 17-7-2.
 */
public class WeatherData implements Subject{

    private float temperature;
    private float humidity;
    private float pressure;

    private List<Observer> observerList = new ArrayList();

    public void register(Observer observer) {
        observerList.add(observer);
    }

    public void remove(Observer observer) {
        observerList.remove(observer);
    }

    public void notifyObservers() {
        for(Observer o:observerList){
            o.update();
        }
    }

    public void measurementChanged(){
        notifyObservers();
    }

    public float getTemperature() {
        return temperature;
    }

    public float getHumidity() {
        return humidity;
    }

    public float getPressure() {
        return pressure;
    }


    public boolean contain(Observer observer) {
        return this.observerList.contains(observer);
    }

    public void setMeasurements(float temp, float hum, float pressure){
        this.temperature = temp;
        this.humidity = hum;
        this.pressure = pressure;
        measurementChanged();
    }
}
```
 订阅者的统一接口

 
```
package com.head.first.Observer;

/**
 * Created by hadoop on 17-7-2.
 */
public interface Observer {

    public void update();
    public void cancel();
    public void register(Subject subject);
}
```
 布告板展示的统一接口

 
```
package com.head.first.Observer;

/**
 * Created by hadoop on 17-7-2.
 */
public interface DisplayInfo {

    public void display();
}
```
 订阅者的实现类如下：   
 订阅者的抽象类

 
```
package com.head.first.Observer.impl;

import com.head.first.Observer.Observer;
import com.head.first.Observer.Subject;

/**
 * Created by hadoop on 17-7-2.
 */
public abstract class  AbstractObserver implements Observer{

    protected Subject subject;

    public AbstractObserver(Subject subject){
        register(subject);
    }

    public void register(Subject subject){
        if(this.subject!=null){
            this.cancel();
        }else{
            this.subject = subject;
            this.subject.register(this);
        }
    }

    public void cancel(){
        if(this.subject==null) throw new RuntimeException("当前没有订阅任何主题！");
        if(subject.contain(this)){
            subject.remove(this);
            subject=null;
        }else{
            throw new RuntimeException("该主题没有此订阅者！");
        }
    }
}

```
 目前状况布告板

 
```
package com.head.first.Observer.impl;

import com.head.first.Observer.DisplayInfo;
import com.head.first.Observer.Observer;
import com.head.first.Observer.Subject;


/**
 * Created by hadoop on 17-7-2.
 */
public class CurrentCondition extends AbstractObserver implements DisplayInfo {

    private float temperature;
    private float humidity;

    public CurrentCondition(Subject subject){
        super(subject);
    }

    public void update() {
        WeatherData weatherData = (WeatherData)subject;
        this.temperature = weatherData.getTemperature();
        this.humidity = weatherData.getHumidity();
        this.display();

    }

    public void display() {
        System.out.println("CurrentCondition-> 温度： "+this.temperature+" ; 湿度： "+this.humidity);
    }
}

```
 气象统计布告板

 
```
package com.head.first.Observer.impl;

import com.head.first.Observer.DisplayInfo;
import com.head.first.Observer.Subject;

/**
 * Created by hadoop on 17-7-2.
 */
public class Statistic extends AbstractObserver implements DisplayInfo{

    private float pressure;
    private float humidity;

    public Statistic(Subject subject){
        super(subject);
    }

    public void update() {
        WeatherData weatherData =(WeatherData)subject;
        this.humidity = weatherData.getHumidity();
        this.pressure = weatherData.getPressure();
        display();
    }

    public void display() {
        System.out.println("Statistic-> 湿度："+this.humidity+" ; 气压: "+this.pressure);
    }

}

```
 天气预报布告板

 
```
package com.head.first.Observer.impl;

import com.head.first.Observer.DisplayInfo;
import com.head.first.Observer.Subject;

/**
 * Created by hadoop on 17-7-2.
 */
public class Forecast extends AbstractObserver implements DisplayInfo{

    private float temperature;
    private float pressure;

    public Forecast(Subject subject){
        super(subject);
    }
    public void update() {
        WeatherData weatherData = (WeatherData)subject;
        this.temperature = weatherData.getTemperature();
        this.pressure = weatherData.getPressure();
        display();
    }

    public void display() {
        System.out.println("Forecast-> 温度： "+this.temperature+" ; 气压："+this.pressure);
    }
}

```
 测试类：

 
```
package com.head.first.test;

import com.head.first.Observer.impl.CurrentCondition;
import com.head.first.Observer.impl.Forecast;
import com.head.first.Observer.impl.Statistic;
import com.head.first.Observer.impl.WeatherData;

/**
 * Created by hadoop on 17-7-2.
 */
public class ObserverTest {

    public static void main(String[]args){
        WeatherData weatherData = new WeatherData();
        CurrentCondition currentCondition = new CurrentCondition(weatherData);
        Forecast forecast = new Forecast(weatherData);
        Statistic statistic = new Statistic(weatherData);
        weatherData.setMeasurements(10,20,30);
        forecast.cancel();
        weatherData.setMeasurements(12,14,3);
        currentCondition.cancel();
        weatherData.setMeasurements(12,21,28);
        forecast.register(weatherData);
        weatherData.setMeasurements(10,13,6);
    }
}

```
 与书中不同之处在于，我在订阅者接口中添加了注册和取消注册的方法，这样订阅者就能订阅不同的主题，然后增加了抽象的订阅者来实现通用的方法。

 
### 全局视角

 下面给出书中的全局类图。   
 ![这里写图片描述](https://img-blog.csdn.net/20170702140013301?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvemh1bWluZ3l1YW4xMTE=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

   
  