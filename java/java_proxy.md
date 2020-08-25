# java proxy

InvocationHandler     Invocation 求助; 祈祷; 调用; 启用;
MyBatis

JDK本身提供了动态代理的实现，要求被代理者必须实现接口。
public static Object newProxyInstance(ClassLoader loader,
Class<?>[] interfaces,InvocationHandler h)
复制代码第一个参数为类加载器，第二个参数是被代理者实现的接口列表，第三个参数是实现了InvocationHandler接口的对象。


CGLIB动态代理
JDK动态代理要求必须有接口，CGLIB（Code Generate Library）动态代理没有这个要求，它是通过创建一个被代理类的子类，然后使用ASM字节码库修改代码来实现的。

