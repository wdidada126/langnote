---
title: jdk代理和cglib代理 demo
date: 2018-01-07 22:11:08
tags: CSDN迁移
---
  关于jdk代理和cglib的概念网络上可以很方便的找到，其之间的区别也解释的很详细，在此我给出这两种代理的简单的应用和注释。下面给出代码。

 
### jdk代理

 
```
//接口，使用jd的代理模式，被代理类必须实现一个接口
public interface Hello {
    void say();
}

//目标类（被代理类）
public class HelloImpl implements  Hello {
    public void say(){
        System.out.println("hi, hello world ! ");
    }
}
//InvocationHandler 接口的实现
public class HelloInvocationHandler implements InvocationHandler {

    //目标对象
    private Object target;

    public HelloInvocationHandler(Object target) {
        this.target = target;
    }

    public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
        System.out.println("------befor hello-------------");
        //执行相应的目标方法
        Object rs = method.invoke(target, args);
        System.out.println("------after hello-------------");
        return rs;
    }
}

//main函数测试类

//第一种代理方式，通过反射构造代理类
 static void proxy1() throws NoSuchMethodException, IllegalAccessException,
            InvocationTargetException, InstantiationException{
        //生成$Proxy0的class文件
        System.getProperties().put("sun.misc.ProxyGenerator.saveGeneratedFiles", "true");
        //获取动态代理类
        Class proxyClazz = Proxy.getProxyClass(Hello.class.getClassLoader(),Hello.class);
        //获得代理类的构造函数，并传入参数类型InvocationHandler.class
        Constructor constructor = proxyClazz.getConstructor(InvocationHandler.class);
        //通过构造函数来创建动态代理对象，将自定义的InvocationHandler实例传入
        Hello hello = (Hello) constructor.newInstance(new HelloInvocationHandler(new HelloImpl()));
        //通过代理对象调用目标方法
        hello.say();
    }


//第二种方式，通过Proxy.newProxyInstance生成代理类
    static void proxy2(){
        //生成$Proxy0的class文件
        System.getProperties().put("sun.misc.ProxyGenerator.saveGeneratedFiles", "true");
        Hello  hello2 = (Hello) Proxy.newProxyInstance(Hello.class.getClassLoader(),  //加载接口的类加载器
                new Class[]{Hello.class},      //一组接口
                new HelloInvocationHandler(new HelloImpl())); //自定义的InvocationHandler
        hello2.say();
    }

//主函数入口
    public static void main(String[] args)
            throws NoSuchMethodException, IllegalAccessException,
            InvocationTargetException, InstantiationException {
        proxy1();
        proxy1();
    }
```
 
### CGLIB代理

 
```
//代理类，我们可以看到这里不需要实现什么接口
public class TargetObject {

    public void call(){
        System.out.println("do call target object ! ");
    }

    public void request(){
        System.out.println("request ... ");
    }
}
//MethodInterceptor接口实现，用于对目标函数的拦截，实现自己逻辑
public class TargetInterceptor implements MethodInterceptor {

    public Object intercept(Object o, Method method,
                            Object[] objects, MethodProxy methodProxy) throws Throwable {
        System.out.println("before do call............");
        Object result = methodProxy.invokeSuper(o, objects);
        System.out.println("after do call............");
        return result;
    }
}

//测试
public static void main(String args[]) {
        Enhancer enhancer =new Enhancer();
      enhancer.setSuperclass(TargetObject.class);
        enhancer.setCallback(new TargetInterceptor());
        //这里生成代理类
        TargetObject targetObject=(TargetObject)enhancer.create();
        targetObject.request();
    }
```
 //CallbackFilter的使用，当client调用代理的时候，可以通过CallbackFilter进行过滤，并根据不同的方法选择不同的处理方式。

 
```
public class TargetMethodCallbackFilter implements CallbackFilter{
//这里返回0，1就是下面Callback[]的位置索引
    @Override
    public int accept(Method method) {
        if(method.getName().equals("call")){
            return 0;
        }
        if(method.getName().equals("request")){
            return 1;
        }
        return 0;
    }
}

//测试
public static void main(String args[]) {
        Enhancer enhancer =new Enhancer();
        enhancer.setSuperclass(TargetObject.class);
        Callback[] cbArray = new Callback[2];
        cbArray[0] = new TargetInterceptor();
        //NoOp.INSTANCE：代理类直接调用被代理的方法，不会进行拦截
        cbArray[1] = NoOp.INSTANCE;
        enhancer.setCallbacks(cbArray);
        //这里设置Filter.
        enhancer.setCallbackFilter(new TargetMethodCallbackFilter());
        TargetObject targetObject=(TargetObject)enhancer.create();
        targetObject.call();
        targetObject.request();
    }
```
 
### 延迟加载

 cglib提供Dispatcher和LazyLoader接口用于实现延迟加载，其不同之处在于LazyLoader只会在第一次调用的时候执行，但是Dispatcher会在每一次调用都会执行。下面给出代码。

 
```
//一个简单的bean
public class Bean {


    Bean(){}
    Bean(String name){
        this.name = name;
    }

    String name;

    String getName(){
        return name;
    }
}
//Dispatcher接口实现
public class ConcreteDispatcher implements Dispatcher {

    @Override
    public Object loadObject() throws Exception {
        System.out.println("before dispatcher ....");
        Bean bean = new Bean("dispatcher");
        System.out.println("after dispatcher ...");
        return bean;
    }
}

//LazyLoader接口的实现
public class ConcreteLazyLoader implements LazyLoader{

    @Override
    public Object loadObject() throws Exception {

        System.out.println("before lazy loader ...");
        Bean bean = new Bean("lazy loader");
        System.out.println("after lazy loader ...");
        return bean;
    }
}
//LazyBean的类
public class LazyBean {

    Bean bean1;

    Bean bean2;

    LazyBean(){
        createBean1();
        createBean2();
    }

    void createBean1(){
        Enhancer enhancer = new Enhancer();
        enhancer.setSuperclass(Bean.class);
        //bean1 采用Lazyloader方式进行延迟加载
        bean1 = (Bean) enhancer.create(Bean.class,
                new ConcreteLazyLoader());
    }

    void createBean2(){
        Enhancer enhancer = new Enhancer();
        enhancer.setSuperclass(Bean.class);
        //bean2采用Dispatcher方式实现延迟加载
        bean2 = (Bean) enhancer.create(Bean.class,
                new ConcreteDispatcher());
    }


    public Bean getBean1() {
        return bean1;
    }

    public Bean getBean2() {
        return bean2;
    }
}

//测试
 public static void main(String args[]) {
 //这里只是实例了一个LazyBean,其里面的bean1,bean2还没有真正的实例化，支持代理
        LazyBean lazyBean = new LazyBean();
        //调用bean1，bean2中的属性的时候开始真正实例化
        Bean b1 = lazyBean.getBean1();
        Bean b2 = lazyBean.getBean2();
        b1.getName();
        b1.getName();
        b2.getName();
        b2.getName();
    }
```
 测试的输出：   
 before lazy loader …   
 after lazy loader …   
 before dispatcher ….   
 after dispatcher …   
 before dispatcher ….   
 after dispatcher …

 我们可以看到lazy loader只是在第一次使用的时候调用loadObject方法;   
 dispatcher每一次用到都会调用loadObject方法。

   
  