# java annotation


[秒懂，Java 注解 Annotation 你可以这样学](https://blog.csdn.net/briblue/article/details/73824058)


这个要常看

元标签有 @Retention、@Documented、@Target、@Inherited、@Repeatable 5 种。




java @Inherited注解的作用

https://www.jianshu.com/p/7f54e7250be3




Target 是目标的意思，@Target 指定了注解运用的地方。

你可以这样理解，当一个注解被 @Target 注解时，这个注解就被限定了运用的场景。

类比到标签，原本标签是你想张贴到哪个地方就到哪个地方，但是因为 @Target 的存在，它张贴的地方就非常具体了，比如只能张贴到方法上、类上、方法参数上等等。@Target 有下面的取值

ElementType.ANNOTATION_TYPE 可以给一个注解进行注解
ElementType.CONSTRUCTOR 可以给构造方法进行注解
ElementType.FIELD 可以给属性进行注解
ElementType.LOCAL_VARIABLE 可以给局部变量进行注解
ElementType.METHOD 可以给方法进行注解
ElementType.PACKAGE 可以给一个包进行注解
ElementType.PARAMETER 可以给一个方法内的参数进行注解
ElementType.TYPE 可以给一个类型进行注解，比如类、接口、枚举

isAnnotationPersent()
getAnnotation()
getAnnotations()

一个注解要在运行时被成功提取，那么 @Retention(RetentionPolicy.RUNTIME) 是必须的。



https://blog.csdn.net/heyrian/article/details/80764783





注解处理器类库
Java通过反射机制获取类、方法、属性上的注解，因此java.lang.reflect提供AnnotationElement支持注解，主要方法如下：

boolean is AnnotationPresent(Class<?extends Annotation> annotationClass)：判断该元素是否被annotationClass注解修饰
<T extends Annotation> T getAnnotation(Class<T> annotationClass)：获取 该元素上annotationClass类型的注解，如果没有返回null
Annotation[] getAnnotations()：返回该元素上所有的注解
<T extends Annotation> T[] getAnnotationsByType(Class<T> annotationClass)：返回该元素上指定类型所有的注解
Annotation[] getDeclaredAnnotations()：返回直接修饰该元素的所有注解
<T extends Annotation> T[] getDeclaredAnnotationsByType(Class<T> annotationClass)：返回直接修饰该元素的所有注解

https://blog.csdn.net/heyrian/article/details/80764783



@interface



元注解

@Target

@Documented

@Retention

@Inherent







Java目前内置了三种注解@Override、@Deprecated、@SuppressWarnnings



 注解中的参数类型

注解中的参数只支持如下类型：



- 所有的基本类型：byte、short、char、int、long、float、double
- String类型
- Class类型
- enum类型
- Annotation类型
- 以上类型的数组





java.lang.Class



Class上的注解

class.getAnnotation();



java.lang.reflect.Method





##### Java注解处理器

- Annotation
- Class
- Method

这三个类

